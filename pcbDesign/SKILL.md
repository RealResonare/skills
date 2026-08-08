---
name: pcbDesign
description: PCB 设计 playbook：需求澄清、叠层/阻抗规划、原理图到布局、布局布线规则、DFM/EMC 检查、制造文件导出。用于"设计/评审/检查某个 PCB 板"类任务，可通过 MCP 驱动 KiCad。
---

# pcbDesign — PCB 设计 playbook

> **English Quick Start**
>
> This skill drives PCB (printed circuit board) design from requirements to manufacturing files: requirement clarification, stackup/impedance planning, schematic-to-layout, placement/routing rules, DFM/EMC review, and Gerber/assembly export. It works through MCP-driven KiCad when available (generic adaptation layer — detect tools at runtime) and produces a review gate before any fabrication file is delivered.
> Core loop: **需求澄清 → 叠层与设计规则规划 → 原理图 → 布局 → 布线 → 设计规则检查(DRC/DFM/EMC) → 制造文件 → 交付**.
> Hard rules: never invent component/stackup values from memory (verify against datasheet/fab capability), always run DRC before export, state UNVERIFIED for anything not checked, and default the stackup/impedance targets per this skill's references.

## Purpose

This skill guarantees that PCB designs produced with the AI's help are **manufacturable, electrically sound, and reviewable**: correct stackup & impedance plan, clean schematic-to-netlist flow, placement/routing that respects design rules, a DRC/DFM/EMC gate before Gerbers, and a complete delivery package (Gerber, drill, BOM, pick&place). It acts as a generic adaptation layer over KiCad MCP servers (or local KiCad CLI), detecting whatever tooling exists at runtime.

## When to Invoke

Invoke whenever the user wants to:

- Design a PCB from a schematic (or from scratch from requirements).
- Plan stackup / layer count / controlled impedance (single-ended 50Ω, differential 90–100Ω, etc.).
- Review or check an existing PCB design for DRC errors, DFM issues, EMC risks.
- Generate manufacturing files (Gerber, drill, BOM, pick-and-place) from a finished layout.
- Troubleshoot layout/routing problems (noise, return path, thermal, clearance).

Do **not** invoke for pure circuit design without a board target (see `electricDesign`), or for firmware (see `embeddedDev`).

## Architecture: Generic KiCad Adaptation Layer

<!-- 中文：不绑定特定 MCP。运行时 LS/Read 描述文件发现工具，按逻辑操作映射到实际工具名。 -->

1. **Discover** — inspect available MCP tool descriptors (LS + Read) before calling anything. Known KiCad MCP servers (verify at runtime, names vary): `MCP-KiCad` (placement/netlist/analysis), `blwfish/kicad-mcp` (17-tool workflow), `KiCAD-MCP-Server` (100+ tools incl. DRC/DFM), `kicad-mcp-pro` (pip installable; schematic/PCB/DRC/DFM/manufacturing).
2. **Map operations** — logical operations (open board, place footprint, route, run DRC, export gerbers) map to whatever tool names the server exposes.
3. **Fallback** — if no MCP server: use KiCad CLI headless (`kicad-cli pcb drc`, `kicad-cli pcb export gerbers`), or ask the user to open the board in KiCad GUI.

## Unified Pipeline (Mandatory Order)

| # | Step | Gate / Rule |
|---|---|---|
| 1 | **Collect requirements** | Always establish: board size & layer count, component list / schematic source, technology (RF/high-speed/power), current & voltage per rail, impedance targets, operating environment (industrial/consumer/automotive), fab process limits (min trace/spacing/via). Defaults if unknown: 4-layer FR4 1.6mm, 1oz copper, min 6/6mil, 50Ω SE / 90Ω diff. State assumptions. |
| 2 | **Stackup & design rules** | Define layer stackup (signal/plane alternating, ground adjacent to signal), impedance plan per net class, design rules (trace width/spacing/via/clearance) matching fab capability. See `references/design-rules.md`. |
| 3 | **Schematic** | Generate/check schematic (KiCad `.kicad_sch` via MCP or generate netlist). Run ERC (electrical rule check) — 0 errors. Verify footprints match real packages. See `references/design-rules.md` §Schematic. |
| 4 | **Placement** | Position components per placement rules (decoupling near pins, crystal near MCU, connectors at edge, power devices with thermal relief). See `references/design-rules.md` §Placement. |
| 5 | **Routing** | Route per net class (power traces sized for current, differential pairs matched, high-speed length-matched). See `references/design-rules.md` §Routing. |
| 6 | **Review gate** | Run DRC (0 errors; explain warnings). Then DFM check (see `references/dfm-checklist.md`) and EMC review (see `references/emc-guidelines.md`). **Never export without passing this gate.** |
| 7 | **Manufacturing files** | Export Gerber (RS-274X) + drill (Excellon) + BOM + pick&place (centroid). Zip them with a readme. See `references/manufacturing-export.md`. |
| 8 | **Deliver** | Design package + review report (DRC/DFM/EMC results) + assumptions + next steps. |

## Core Rules (Non-Negotiable)

1. **Never invent datasheet or fab values.** Pinouts, pad sizes, stackup Dk, impedance calculators, process limits come from datasheets / fab capability tables / the actual design. If unverified, say so and mark UNVERIFIED.
2. **DRC before any export.** Zero errors required; every warning must be explained or fixed.
3. **Ground reference discipline.** Every signal layer needs an adjacent continuous reference plane; never route across a split plane unless a return path exists.
4. **Decoupling placement.** Bypass caps as close as possible to power pins (≤3mm), with short low-inductance path to the pin and its via.
5. **Units & precision.** Metric mm for design; Gerber RS-274X with proper format spec (e.g., 4:4 or 4:5) agreed with fab.
6. **Thermal relief on plane-connected pads** unless the joint must carry current (then discuss).
7. **State what you cannot verify.** If no MCP/CLI available to run DRC, deliver a manual checklist review and clearly say DRC was not executed by the tool.

## References

| File | Content |
|---|---|
| `references/design-rules.md` | Stackup & layer count, impedance targets, schematic rules, placement rules, routing rules, PDN/decoupling |
| `references/dfm-checklist.md` | Manufacturing checklist: trace/spacing, vias, solder mask, silkscreen, panelization, board edge, copper balance |
| `references/emc-guidelines.md` | EMC design: return path, plane splits, filtering, I/O protection, ground stitching, high-speed nets |
| `references/manufacturing-export.md` | Export spec: Gerber RS-274X, drill, BOM, pick&place, file naming, delivery zip |

## Output Contract

Every deliverable must include:

1. **Design files**: schematic (`.kicad_sch`), board (`.kicad_pcb`), and/or the MCP operations log.
2. **Review report**: DRC result (error/warning counts + explanations), DFM checklist results, EMC review notes.
3. **Stackup & impedance plan**: layer table with material/thickness/Dk, impedance targets per net class.
4. **Manufacturing package**: Gerber + drill + BOM + pick&place (when requested and design passes gate).
5. **Assumptions**: fab process limits, stackup defaults, anything left for user confirmation.
