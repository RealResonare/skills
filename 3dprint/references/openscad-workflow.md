# OpenSCAD Workflow — OpenSCAD 引擎工作流

> **中文说明**：OpenSCAD 是代码式 CSG（构造实体几何）建模。AI 产出 `.scad` 代码，通过 MCP 的 render/preview 工具（或本地 `openscad` CLI）编译渲染，最终导出 STL/3MF。本文件规范代码写法、验证与导出。

## 1. Tool Mapping — 工具映射（通用适配层）

Discover the actual tool names at runtime (LS + Read the MCP descriptors). Typical OpenSCAD MCP tool families and how to use them:

| Logical operation 逻辑操作 | Typical MCP tools 常见工具名 | Fallback (no MCP) 无 MCP 回退 |
|---|---|---|
| Check installation | `check_openscad`, `info` | `openscad --version` |
| Validate syntax | `validate`, `check` | `openscad --check-parameters -o /dev/null model.scad` (or compile and read stderr) |
| Render to mesh | `render`, `compile` (formats: stl/3mf/amf/off/csg) | `openscad -o out.stl model.scad` |
| Preview image | `preview`, `render_single`, `render_perspectives` (png/svg) | `openscad -o out.png --viewall --camera=... model.scad` |
| Pass variables | `parameters` / `-D` flags | `openscad -D 'width=40' -o out.stl model.scad` |

**Known community servers (examples — not exhaustive; verify at runtime):**
- `FeMa42/openscad_mcp` — explicitly built for OpenSCAD + 3D-printing workflow, includes docs search ([github.com/FeMa42/openscad_mcp](https://github.com/FeMa42/openscad_mcp))
- `dkpoulsen/openscad-mcp` — npm package; `render` (stl/off/amf/3mf/csg), `preview` (png/svg/dxf/pdf), `validate`, `info` ([github.com/dkpoulsen/openscad-mcp](https://github.com/dkpoulsen/openscad-mcp))
- `quellant/openscad-mcp` — `check_openscad`, `render_single`, `render_perspectives`; run via `uv` ([github.com/quellant/openscad-mcp](https://github.com/quellant/openscad-mcp))
- `N0t4R0b0t/openscad-mcp-server` — Rust; text-to-SCAD with STL export ([github.com/N0t4R0b0t/openscad-mcp-server](https://github.com/N0t4R0b0t/openscad-mcp-server))

<!-- 中文：工具名因服务器而异，必须先用 LS/Read 读描述文件确认，绝不能凭记忆编造工具名。 -->

## 2. Code Conventions — 代码规范

- **Units: millimeters.** All numbers in mm.
- **Global resolution** at the top, tuned for STL (not preview): `$fa = 1; $fs = 0.2;` — avoid `$fn = 360` everywhere (huge STL); use `$fn` only for specific features that need smoothness (e.g., `cylinder(h=10, r=5, $fn=64)`).
- **Single top-level `union()`** (or one final operation) so the result is one solid, watertight body — required for the manifold gate.
- **Parameterize everything** users might tweak: `width`, `height`, `wall`, `clearance`, `hole_d`. Provide a clear `module` API; no magic numbers in the body.
- **Wall thickness via difference**: build the outer solid, then `difference() { outer; translate(...) inner; }` — never model walls as thin 2D extrusions.
- **Fillets/chamfers**: `minkowski()` with a small sphere for rounded edges (cheap), or `hull()` tricks; chamfers via `rotate_extrude` profile or `intersection` with an angled cut block. Keep minkowski radius ≤ wall thickness.
- **Threads & gears**: use libraries (e.g., `threads.scad`, BOSL2) if available; otherwise model trapezoidal threads with `linear_extrude(twist=...)`.
- **Hole compensation**: `hole_d = target + 0.2;` (vertical FDM) — see checklist.
- **Comments**: brief; explain intent, not mechanics.

### Example skeleton 示例骨架

```scad
$fa = 1; $fs = 0.2;          // STL-quality resolution

// Parameters — all in mm  (中文：所有尺寸单位毫米)
wall    = 2.0;               // >= 2x nozzle
height  = 40;
width   = 60;
depth   = 30;
hole_d  = 5 + 0.2;           // vertical hole compensation +0.2

module box_with_hole() {
    difference() {
        cube([width, depth, height], center = true);      // outer solid
        translate([0, 0, 5]) cylinder(d = hole_d, h = height + 1, center = true); // hole
    }
}

box_with_hole();             // single top-level solid
```

## 3. Verification — 验证

1. **Validate** syntax (MCP `validate` or CLI check) — fix warnings, treat them as errors (`--hardwarnings`).
2. **Preview** to a PNG and inspect visually; confirm orientation and rough proportions. Ask the user to eyeball it if a visual review matters.
3. **Render to STL** and, when the tool exposes geometry info, confirm:
   - Mesh compiles without "not closed" / "non-manifold" warnings (these are the top causes of print failures).
   - Volume is nonzero and sane: `volume_mm3 = mass density check` — if the MCP returns mesh info use it; otherwise compute expected volume from primitives (cube = w·h·d, cylinder = π·r²·h) and sanity-check ±10%.
4. **Dimension spot-check** by computing bounding box from the parameters you wrote (you control the code — verify your own math before claiming dimensions).

## 4. Printability & Fix Loop — 体检与修复

Run `references/printability-checklist.md`. Common OpenSCAD fixes:

| Failure 问题 | Fix 修复 |
|---|---|
| Not watertight / open edges | Ensure final `union()`; check `difference()` leaves no zero-thickness shells; add `fudge` overlap (extend cutting solids 0.01–0.1mm beyond the body) |
| Thin walls | Increase `wall` param; avoid intersecting two thin surfaces at grazing angles |
| Overhang > 45° | Add chamfer/slope to the face, or `rotate()` the whole part to a better orientation |
| Holes too small after print | Bump `hole_d` compensation (+0.2 vertical, +0.3 horizontal) |
| Huge STL file | Lower `$fs`/`$fa` values (e.g., `$fs=0.4`), remove excessive `$fn` |
| Cavity traps resin/cannot drain | Add drainage holes (≥ 3mm) at the lowest point of any enclosed cavity |

## 5. Export — 导出

- **Binary STL** (default; smaller, slicer-compatible) unless the user requests ASCII (debugging) — `.stl`.
- **3MF** when available from the MCP `render` tool and the user's slicer supports it.
  - **Single object**: exported directly (one mesh, one part).
  - **Multi-object assembly**: requires **lazy-union** so each top-level statement becomes its own 3MF `<object>` (nightly 2025+, issue #350). Without it OpenSCAD merges all top-level geometry into one mesh. Details, code, and caveats (no color metadata, no custom part names) in `multi-part-assembly.md` §3.1.
- Always export with **millimeters** semantics — OpenSCAD has no unit concept, so state "unit = mm" in the delivery summary.
- Verify the exported file exists and is non-trivial in size (a valid STL of a 60mm part is typically ≥ tens of KB; a few-hundred-byte STL is almost certainly broken). For 3MF, unzip-check the `3D/3dmodel.model` and count `<object` entries when multi-part is expected.
