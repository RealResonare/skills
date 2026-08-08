# Printability Checklist — 可打印性检查清单

> **中文说明**：这是"打印前体检"的唯一权威清单。AI 在导出任何文件前必须逐项核对；能程序化测量的（如尺寸、体积、顶点数）必须测量，不能测量的要明确标注"未验证"。

## 1. Geometry & Mesh Integrity — 几何与水密性

| Check 检查项 | Pass criteria 通过标准 | How to verify 验证方法 |
|---|---|---|
| **Manifold / watertight 水密流形** | Closed volume; every edge shared by exactly 2 faces; no holes | OpenSCAD: compile without "not closed" warnings, wrap everything in one `union()`. Blender: 3D-Print Toolbox → "Solid" check (reports non-manifold edges, bad faces, zero faces); or `bpy.ops.mesh.print3d_check_solid()`. |
| **Normals 法线方向** | All faces outward, consistent | Blender: 3D-Print Toolbox "Distorted" / face orientation overlay; `bpy.ops.mesh.normals_make_consistent(inside=False)`. OpenSCAD: normals are auto-managed by CSG. |
| **No intersecting / internal faces 无交叉面与内部面** | No self-intersections, no duplicate overlapping geometry | Blender: 3D-Print Toolbox "Intersections" + "Degenerate" (zero-area faces, thin faces). OpenSCAD: prefer clean CSG (union/difference); avoid zero-thickness intersections. |
| **No duplicate vertices 无重复顶点** | No coincident vertices | Blender: Mesh → Clean Up → Merge by Distance (small epsilon, e.g. 0.001mm). |
| **Mesh resolution adequate 网格分辨率足够** | Curves smooth enough for the part's smallest radius; deviation ≤ 0.01mm | OpenSCAD: set `$fa=1; $fs=0.2;` (or `$fn` only where needed) before render. Blender: check triangle count vs feature size; use subdivision/remesh only if it does not break printability. |

<!-- 中文：3MF 格式自带单位与元数据，比 STL 更利于交换；但 STL 仍是通用标准。两者导出时都必须确保单位=毫米。 -->

## 2. Dimensional Constraints — 尺寸约束 (FDM, 0.4mm nozzle baseline)

| Check 检查项 | Min / recommended 最小/推荐 | Notes 备注 |
|---|---|---|
| **Wall thickness 壁厚** | ≥ 2× nozzle (0.8mm); 1.2mm+ for strength | Below 2× nozzle walls get thin/brittle or fail to extrude. For resin (SLA): ≥ 0.8mm recommended. |
| **Minimum feature 最小特征** | ≥ 0.4mm (nozzle Ø); details ≥ 0.6mm | Embossed/engraved text: depth ≥ 0.5mm, stroke width ≥ 0.5mm, cap height ≥ 2mm (readable). |
| **Vertical hole diameter 竖直孔** | ≥ 0.8mm at 0.4mm nozzle (ideally 1mm+) | Small vertical holes clog/close up; compensate diameter +0.2mm (see §4). |
| **Horizontal hole 水平孔** | ≥ 1mm; larger is safer | Horizontal holes need supports or bridging; add 0.1mm compensation. |
| **Overhang angle 悬垂角** | ≤ 45° free; 30° comfortable | 45°+ needs supports (FDM) or auto-supports (SLA). Chamfer/slope the surface to reduce supports. |
| **Bridge length 桥接长度** | ≤ 10mm unsupported; ≤ 5mm safe | Longer bridges sag. Add supports or change design (cut into supported segments). |
| **Part size vs build volume 尺寸 vs 构建体积** | Within printer volume, all axes | Ask for the printer model; default 220×220×250mm (FDM) / ~200×120×220mm (SLA). Split oversized parts with alignment features (dowels/keyways) and report the split plan. |
| **Clearance to bed/floor 离地间隙** | N/A — ensure first layer is full contact | Avoid floating islands; add supports or a base skirt if needed. |

## 3. Functional Tolerances — 公差配合表 (FDM, 0.4mm nozzle)

<!-- 中文：FDM 收缩、层纹和挤出膨胀让配合尺寸必须留余量。下表为常见经验值，最终以用户试打为准。 -->

| Fit type 配合类型 | Gap / interference 间隙/过盈 | Example 示例 |
|---|---|---|
| **Sliding / moving fit 滑动配合** | +0.3 ~ +0.5mm | Axle in hole, drawer in slot |
| **Snap fit 卡扣配合** | +0.2 ~ +0.3mm | Battery covers, clips |
| **Press / interference fit 过盈配合** | −0.1 ~ −0.2mm | Inserts, bearing seats (press-in) |
| **Thread clearance 螺纹间隙** | +0.3mm on outer Ø (non-printed threads) | Bolts into printed holes |
| **Printed threads 打印螺纹** | Use 0.4mm pitch minimum, trapezoidal profile preferred | Fine pitches fail in FDM |

**Hole compensation 孔位补偿 (FDM):** vertical holes print ~0.1–0.2mm undersized, horizontal holes ~0.3mm undersized. Compensate: `hole_diameter_design = target + 0.2mm (vertical)` / `+ 0.3mm (horizontal)`. For resin, holes may print **oversized** — verify with a calibration cube.

## 4. Material-Specific Notes — 材料差异

| Material 材料 | Key constraints 关键约束 | Temps 温度(喷嘴/热床) |
|---|---|---|
| PLA | Easy, low warp; weak at heat (>60°C softens) | 190–220°C / 50–60°C |
| PETG | Slightly flexible, good chemical resistance; stringy, requires dry filament | 230–250°C / 70–90°C |
| ABS | Strong, needs enclosure (warping); fumes | 240–260°C / 95–110°C |
| TPU | Flexible; needs direct drive + slower speed; thin walls collapse | 220–250°C / 40–60°C |
| Resin (SLA) | High detail; brittle; needs support everywhere on overhangs + drainage holes for cavities | Layer 0.05mm typical |

## 5. Mandatory Report Format

Run the gate and report as a table — do not skip items; mark unverifiable items explicitly:

| # | Check | Status (PASS/FAIL/NOT VERIFIED) | Measured value / note |
|---|---|---|---|
| 1 | Watertight / manifold | | |
| 2 | Min wall thickness | | |
| ... | ... | | |

If any item FAILs, fix the model and re-run the gate before exporting. If anything is NOT VERIFIED (e.g., no mesh-analysis tool available), state it in the delivery summary — never silently pass.
