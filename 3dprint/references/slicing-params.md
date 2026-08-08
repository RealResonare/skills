# Slicing & Export Spec — 切片与导出规范

> **中文说明**：本文件定义导出文件格式和切片参数报告。AI 不一定能直接驱动切片器（除非环境里有切片器 MCP/CLI），但**必须**交付一份可直接套用的切片参数表，并尽可能给出切片器 CLI 命令。

## 1. Export Format Rules — 导出格式

| Decision 决策 | Rule 规则 |
|---|---|
| Default format (single part) | **Binary STL** (`.stl`) — universal slicer support, small size |
| Preferred when supported | **3MF** — carries units, mesh, and print metadata; **mandatory for multi-part assemblies** (one file, named parts, relative positions). See `multi-part-assembly.md` |
| Units | **Millimeters only.** STL has no unit field — state "mm" in delivery. 3MF embeds units. |
| Mesh resolution | OpenSCAD `$fa=1; $fs=0.2;`; Blender deviation ≤ 0.01mm (Blender's default is typically fine) |
| Orientation | Largest flat face on the bed; minimal supports; no trapped cavities |
| Naming | Single: `part-name_v{N}.stl`. Assembly parts: `P01_base`, `P02_lid`… (object names become 3MF part names) |
| Source files | Deliver `.scad` / `.blend` / generated script alongside the mesh |

## 2. Slice Parameter Report — 切片参数报告（必交付）

Produce this table for every export. Defaults assume **FDM, 0.4mm nozzle, PLA** unless the user's printer says otherwise.

| Parameter 参数 | Default 默认 | Guidance 指导 |
|---|---|---|
| Layer height 层高 | 0.2mm | 0.12 fine detail; 0.28 draft; SLA 0.05mm |
| Line width 线宽 | 0.4mm | match nozzle; thinner for small details |
| Infill 填充 | 15–20% | grid/gyroid; 40% strong; 100% functional; 0% vase mode |
| Infill pattern 填充图案 | Gyroid (or grid) | gyroid = strong + isotropic; triangles for vertical strength |
| Perimeter/wall count 壁数 | 2–3 | increases strength & water-tightness; use ≥3 for pressure vessels |
| Top/bottom layers 顶底 | 4 | avoid pillowing on large flat tops |
| Supports 支撑 | Auto, only when needed | enable tree/organic supports for overhangs >45°; touch-building-plate only if possible |
| Support density 支撑密度 | 10–15% | lower = easier removal |
| Brim 裙边 | None; Brim when small base or ABS/warp-prone | 5–8mm brim for small parts |
| Raft 底座 | None unless bed adhesion is poor | raft = extra cleanup |
| Retraction 回抽 | 0.8–1.2mm direct / 4–6mm bowden | reduces stringing (PETG needs more) |
| Cooling 冷却 | PLA 100% fan; PETG 30–50%; ABS off (enclosure) | |
| Speed 速度 | 50–80mm/s default; first layer 20–30mm/s | |

## 3. Material Temperature Table — 材料温度表 (FDM)

| Material 材料 | Nozzle 喷嘴 | Bed 热床 | Notes 备注 |
|---|---|---|---|
| PLA | 190–220°C | 50–60°C | Easiest; brittle; keep cool |
| PETG | 230–250°C | 70–90°C | Strong & slightly flexible; stringy — dry filament, more retraction |
| ABS | 240–260°C | 95–110°C | Needs enclosure; warps without it |
| TPU | 220–250°C | 40–60°C | Flexible; slow speed, direct drive recommended |
| Resin (SLA) | — | — | Layer 0.05mm; heavy supports on overhangs; drain cavities; post-cure per resin datasheet |

> 中文提醒：以上是通用参考区间，具体以耗材厂商标称与用户实测为准。温度写进报告时注明"建议以耗材标签为准"。

## 4. Slicer CLI Commands (optional automation) — 可选自动切片

When a slicer CLI is available locally, offer a one-command slice instead of only a report. Verify the binary exists before running.

```bash
# PrusaSlicer / Bambu Studio (same engine family)
prusa-slicer --export-gcode --center 110,110 \
  --print-setting "0.20mm Standard" \
  --filament-setting "Generic PLA" \
  part.stl

# CuraEngine (headless)
curaengine slice -v -j fdmprinter.def.json -s infill_sparse_density=20 \
  -e "model_file=part.stl" -o part.gcode
```

## 5. Delivery Checklist — 交付清单

1. Mesh file (STL/3MF) + source (`.scad`/`.blend`/script).
2. Printability report (from `printability-checklist.md`).
3. Slice table above, customized to the user's printer/material.
4. Optional: GCode if slicer CLI ran successfully.
5. Assumptions & risks (e.g., "tolerance fits may need a test print").
