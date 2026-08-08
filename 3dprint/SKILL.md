---
name: "3dprint"
description: "Drives OpenSCAD or Blender via MCP to design, verify, export 3D-printable models (checks, STL/3MF, slice params). Invoke when the user wants to create/check/fix/prepare any model for 3D printing."
---

# 3DPrint — MCP-Driven 3D Printing Skill

> **中文速览 (Chinese Quick Start)**
>
> 本 Skill 让 AI 通过 MCP 控制 **OpenSCAD** 或 **Blender** 建模，并把模型做成**真正能上机打印**的成品。
> 核心动作有四步，每步都有硬性检查：
> 1. **问清打印约束**（打印机、喷嘴、材料、构建体积）——不知道就默认 FDM 0.4mm 喷嘴 + PLA + 220×220×250mm，并明确告知用户假设。
> 2. **选引擎并建模**（OpenSCAD=参数化/机械件；Blender=有机曲面/复杂装配；用户指定优先）。涉及螺丝/嵌件时查 `references/thread-library.md` 的参数表。
> 3. **可打印性体检**（水密流形、壁厚 ≥0.8mm、悬垂 ≤45°、最小特征 ≥0.4mm、公差预留）——不通过就修，通过才导出。
> 4. **导出 + 切片报告**（单件用 STL；多零件装配用 3MF 一文件多 part，见 `references/multi-part-assembly.md`；单位毫米，附切片参数表）。
>
> 引擎不绑死：运行时先探测可用的 MCP 工具（LS/Read 描述文件），再决定走哪条工作流；没有 MCP 就回退到本地 CLI。详细规则见下。

## Purpose

This skill guarantees that models produced through MCP-controlled CAD (OpenSCAD) or Blender sessions actually satisfy 3D-printing constraints: watertight geometry, minimum wall thickness, manageable overhangs, correct units, tolerances, and a slice-ready export. It acts as a **generic adaptation layer** — it does not depend on any single MCP server, and detects whatever OpenSCAD/Blender MCP tooling is available at runtime.

## When to Invoke

Invoke this skill whenever the user wants to:

- Generate a 3D model from text/parameters **for the purpose of 3D printing** (not just visualization).
- Check, analyze, or fix an existing model for printability (wall thickness, overhangs, manifoldness, tolerances).
- Export a model as **STL / 3MF** with correct units and orientation, or get **slicer-ready parameters** (layer height, infill, supports, material temps).
- Drive OpenSCAD or Blender through MCP for any print-oriented modeling task.

Do **not** invoke for pure visualization/animation/rendering work with no printing intent.

## Architecture: Generic MCP Adaptation Layer

<!-- 中文：通用适配层 —— 不绑定任何特定 MCP 服务器。运行时按以下优先级探测能力，再路由到对应工作流。 -->

1. **Discover** — inspect the available MCP tool descriptors (LS the MCP servers folder, Read each relevant tool schema) before calling anything. Never assume tool names from memory; always verify. If the user explicitly names an MCP server (e.g., "use blender-mcp"), prefer it.
2. **Classify** — identify which engine the available tools drive:
   - **OpenSCAD MCP**: typically exposes tools like `render` / `compile` (scad → STL/3MF/AMF), `preview` (scad → PNG/SVG), `validate` / `check_openscad`, `info`.
   - **Blender MCP**: typically exposes `execute_blender_code` (full bpy Python) plus structured helpers (create object, transform, material, screenshot, scene info).
3. **Route** — per the routing table below.
4. **Fallback** — if no MCP server exists for the target engine, drive it headless via local CLI:
   - OpenSCAD: `openscad -o out.stl -D var=val model.scad`, `openscad -o out.png --viewall model.scad`, `openscad --check-parameters -o /dev/null model.scad`.
   - Blender: `blender --background --python script.py` (bpy is only available inside Blender's Python).
   - If neither engine is reachable, say so and ask the user to install/launch one (MCP server or the app itself).

## Engine Routing

| Signal | Route |
|---|---|
| User names a tool/engine | Always honor it |
| Parametric / mechanical / precise dimensions / math-defined shapes (gears, brackets, enclosures, threads) | **OpenSCAD** |
| Organic shapes / sculpt / smooth freeform / multi-part assemblies / artistic forms | **Blender** |
| Both available and ambiguous | Ask the user; default to OpenSCAD for engineering parts |
| Only one engine available | Use it |

<!-- 中文：OpenSCAD 是代码式 CSG 建模，精确可复现，适合机械件；Blender 用 bpy Python 控制，适合曲面与视觉复杂的模型。 -->

## Unified Pipeline (Mandatory Order)

Run every project through this pipeline. Do not skip the verification and printability gates.

| # | Step | Gate / Rule |
|---|---|---|
| 1 | **Collect print constraints** | Always establish: printer technology (FDM/SLA), nozzle Ø (FDM), material, build volume, layer height. Defaults if unknown: FDM, 0.4mm nozzle, PLA, 220×220×250mm, 0.2mm layer. State assumptions to the user. |
| 2 | **Design intent** | Confirm target dimensions, tolerances/fit type, strength needs, aesthetics. For mating parts, ask fit type: press / sliding / snap. If screws/inserts are involved, pick the approach from `references/thread-library.md` §1 and use its size tables. |
| 3 | **Model** | Build incrementally via the engine workflow (see references). One logical operation per step; verify after each. Units MUST be millimeters. For assemblies, build parts in-place at final relative positions. |
| 4 | **Verify geometry** | Render/preview and inspect (OpenSCAD `preview`/render; Blender screenshot/viewport). Check dimensions programmatically where possible. |
| 5 | **Printability gate** | Run the full checklist in `references/printability-checklist.md`. Fix every failing item (thicken walls, chamfer overhangs, compensate holes, make solid/manifold). **Never export a model that fails this gate.** |
| 6 | **Orient for printing** | Largest flat face down; minimize supports; avoid trapping resin/FDM cavities. Rotate if it reduces supports without hurting strength. |
| 7 | **Export** | Single part: Binary STL (default). Multi-part assembly: **3MF** (one file, named parts, embedded mm units) per `references/multi-part-assembly.md`. Correct mesh resolution ($fa/$fs or deviation ≤ 0.01mm). See `references/slicing-params.md`. |
| 8 | **Slice report** | Produce a print-settings report (layer height, infill, supports, temps, brim/raft) matching material + printer. See `references/slicing-params.md`. |
| 9 | **Deliver** | Provide file path(s), a verification summary (checklist results), and the slice report. State any remaining risks (e.g., "threads are fine for PLA but may be brittle in resin"). |

## Core Rules (Non-Negotiable)

<!-- 中文：这些是硬性规则，任何时候都不得违反。 -->

1. **Units are millimeters, always.** STL has no unit metadata; exporting in any other unit silently scales the print.
2. **Every exported mesh must be manifold/watertight** (each edge shared by exactly two faces, closed volume, consistent normals).
3. **Minimum wall thickness ≥ 2× nozzle Ø** (≥ 0.8mm at 0.4mm nozzle). Thinner walls are brittle or unprintable.
4. **Features smaller than the nozzle Ø (0.4mm default) are unprintable.** Compensate: emboss text ≥ 0.5mm depth, details ≥ 0.6mm.
5. **Overhangs > 45° need supports** (or a redesign). Surface quality suffers; tell the user and decide with them.
6. **Leave tolerance for moving/snap fits** (see checklist table: sliding ≈ 0.3–0.4mm, press ≈ 0.1–0.2mm interference, snap ≈ 0.2–0.3mm).
7. **Verify tools exist before calling** — inspect MCP descriptors first; never hallucinate tool names.
8. **Never claim a model is printable without running the gate.** If you cannot verify (no render, no mesh analysis), say exactly what you could not verify.

## Output Contract

Every deliverable must include:

1. **Model file(s)**: `.stl` / `.3mf` / source (`.scad`, `.blend`, or generated script).
2. **Printability report**: pass/fail per checklist item, with measured/estimated values.
3. **Slice/print settings**: table with layer height, infill, supports, temps, brim/raft, orientation.
4. **Assumptions**: printer profile defaults used, and anything left to the user to confirm.

## References

| File | Content |
|---|---|
| `references/printability-checklist.md` | Full printability gate: checklist, tolerance tables, per-technology notes (FDM/SLA) |
| `references/thread-library.md` | Screw/insert authority: ISO metric threads, clearance holes, heat-set insert pilot holes, head/nut traps, printed-thread design rules, OpenSCAD example |
| `references/multi-part-assembly.md` | Assembly design & 3MF export: when to use 3MF, part naming, alignment features, OpenSCAD lazy-union & Blender 3MF export, verification |
| `references/openscad-workflow.md` | OpenSCAD engine: MCP tool mapping, code conventions, verification, export |
| `references/blender-workflow.md` | Blender engine: MCP tool mapping, bpy conventions, print-toolbox checks, export |
| `references/slicing-params.md` | Slice/export spec: format rules, resolution, material temperature table, infill/support guidance |
