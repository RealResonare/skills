# Multi-Part Assembly & 3MF Export — 多零件装配与 3MF 导出

> **中文说明**：当模型由多个独立打印的零件组成（装配体、分件打印、多色/多材料），首选 **3MF** 而不是一堆 STL：一个文件内可含多个命名零件、各自独立摆放，且单位内嵌。本文件规范装配设计、3MF 导出与验证。

## 1. When to Use 3MF (vs STL) — 何时用 3MF

| Scenario 场景 | Format 格式 |
|---|---|
| Single solid part 单件 | Binary STL（兼容性最好） |
| Assembly with multiple independent parts 多零件装配 | **3MF**（一文件多 part，保留相对位置与命名） |
| Multi-color / multi-material 多色多材料 | **3MF**（若工具链支持颜色元数据；OpenSCAD 颜色暂不支持） |
| Oversized part split into pieces 超大件分件 | 3MF（多个 part 一次交付）或多个 STL |
| Repeated identical parts 大量重复件（螺栓、栅格） | 3MF（Object 复用 Component，文件小 5–10x） |

<!-- 中文：3MF 是 ZIP 包，核心几何在 3D/3dmodel.model；Object=网格定义，Component=带变换矩阵的对象引用，Build item=顶层打印项。单位默认毫米。现代切片器（Cura/PrusaSlicer/Bambu Studio/Orca）均支持。 -->

## 2. Assembly Design Rules — 装配设计规范

1. **每零件独立命名**：3MF 中 object `name`（Blender 里即对象名）会成为切片器里的 part 名。命名规范：`P01_base`, `P02_lid`, `P03_hinge` — 排序前缀 + 功能名。
2. **装配定位**：把零件按装配关系摆在同一坐标系导出（如 Blender 场景内直接摆好；OpenSCAD 顶层 translate 到位）。切片器会按变换矩阵保持相对位置，无需手动对齐。
3. **对齐/防呆特征**：需要粘接或定位的零件之间加定位销/定位槽/燕尾槽：
   - 定位销/孔：`dowel = 4mm`，销直径 = 孔直径 − 0.3mm（滑动配合，见清单）。
   - 燕尾/榫卯：斜角 10–15° 防脱出，配合间隙 +0.3mm。
4. **打印策略标注**：不同零件可能不同朝向/填充——3MF 交付后在切片器里逐个摆放即可；文档中给出每个零件的建议朝向与支撑策略。
5. **嵌套避免**：零件之间不得互相包含（切片器可能合并或产生非流形交集），需要分件时用 `difference()`/布尔切割制造间隙 ≥ 0.4mm。

## 3. Export — 导出规范

### 3.1 OpenSCAD → 3MF（多对象）

OpenSCAD 默认把多个顶层对象合并成一个网格。要导出多对象 3MF，必须启用 **lazy-union**（nightly 2025+，issue #350）：

```bash
# CLI：--enable lazy-union 使每个顶层语句成为独立 3MF <object>
openscad --enable lazy-union -o assembly.3mf assembly.scad
```

```scad
// 顶层语句各自独立（lazy-union 下）——不要包进 union()！
module base()  { translate([0,0,0]) cube([60,40,4]); }
module lid()   { translate([0,0,6]) cube([60,40,3]); }

base();   // -> 3MF object 1
lid();    // -> 3MF object 2
```

注意（如实告知用户）：
- lazy-union 目前是开发版功能，旧版本（2025 之前）不支持，需升级或改用"逐零件渲染 + 多 STL"方案（用 `if (export_part=="base") base();` 参数化切换导出）。
- `color()` 目前仅预览，颜色元数据不会进入 3MF（跟踪 issue #4671/#5065）；多色需求在切片器里手动分配。
- 顶层对象名称无法自定义（切片器中显示为 OpenSCAD 生成的默认名），导入切片器后用重命名/分组确认零件。

### 3.2 Blender → 3MF（多对象）

Blender 的 3MF 导出需要 3MF 插件（Blender3mfFormat，Core Spec 1.2.3）。对象名即 3MF part 名，场景内位置即装配位置：

```python
import bpy
# 1) 确保 3MF 导出插件启用（内置或第三方 Blender3mfFormat）
try:
    bpy.ops.export_mesh.threemf
except AttributeError:
    bpy.ops.preferences.addon_enable(module="io_mesh_3mf")
    # 若内置没有，提示安装 Ghostkeeper/ansonl 的 Blender3mfFormat 插件

# 2) 命名与选中要导出的零件（改名后即 part 名）
names = ["P01_base", "P02_lid"]
for n in names:
    bpy.data.objects[n].select_set(True)

# 3) 导出：保留场景单位(毫米)、应用修改器
bpy.ops.export_mesh.threemf(
    filepath="/path/to/assembly.3mf",
    use_selection=True,
    global_scale=1.0,
    use_mesh_modifiers=True,
    coordinate_precision=4,
)
```

参数说明：`use_selection=True` 只导出选中的零件；`use_mesh_modifiers=True` 先应用修改器（布尔/实体化），确保导出的是最终几何；`global_scale=1.0` 保证毫米单位正确；`coordinate_precision=4` 是精度/体积平衡点（3–6 均可，精度越高文件越大）。

## 4. Verification — 验证

1. **文件即 ZIP**：`.3mf` 可改名 `.zip` 解压，检查 `3D/3dmodel.model` 存在且可读——快速排障手段。
2. **对象数量**：解压后 grep `<object` 计数，应与零件数一致（用 `unzip -p assembly.3mf 3D/3dmodel.model | grep -c "<object"`）。
3. **每零件水密**：在引擎侧对每个零件单独跑可打印性门禁（清单 §1），再组合导出。
4. **相对位置**：在切片器中打开确认零件相对位置正确、无重叠穿插（装配间隙 ≥ 0.4mm 除外）。
5. **单位**：`<model unit="millimeter"` 确认单位毫米。
6. 若 MCP 工具无法导出 3MF：回退为逐零件导出 STL（`P01_base.stl` 等），交付 ZIP 或文件列表，并说明"切片器里需手动摆放"。

## 5. Delivery — 交付

- 3MF（首选）或 STL 集合 + 零件清单表（part 名 → 功能 → 建议朝向/支撑）。
- 每个零件的可打印性体检结果。
- 装配说明：哪些零件需要胶水/嵌件/定位销，配合公差用的哪档。
