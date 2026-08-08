# Blender Workflow — Blender 引擎工作流

> **中文说明**：Blender 通过其内置 Python (bpy) 被 MCP 控制。多数 Blender MCP 服务器提供 `execute_blender_code`（直接跑 bpy 代码）加一组结构化辅助工具。本文件规范 bpy 建模、单位、体检（3D-Print Toolbox）与 STL 导出。

## 1. Tool Mapping — 工具映射（通用适配层）

Discover at runtime (LS + Read descriptors). Typical Blender MCP tool families:

| Logical operation 逻辑操作 | Typical MCP tools 常见工具名 | Fallback 回退 |
|---|---|---|
| Run arbitrary bpy code | `execute_blender_code` (primary) | `blender --background --python script.py` |
| Create/modify objects | `create_object`, `transform_object`, `delete_object`, `set_material` (if present) | bpy via `execute_blender_code` |
| Scene inspection | `get_scene_info`, `list_objects`, `get_object_properties` | bpy: `bpy.data.objects`, `bpy.context.scene` |
| Visual check | `screenshot`, `take_viewport_screenshot`, `render` | `bpy.ops.render.opengl()` |
| Mesh health | `check_mesh`, `validate_mesh` (if present) | 3D-Print Toolbox operators (see §3) |
| Export | `export_stl`, `export_mesh` (if present) | `bpy.ops.export_mesh.stl()` |

**Known community servers (examples — not exhaustive; verify at runtime):**
- `ahujasid/blender-mcp` — the original PoC; run with `uvx blender-mcp` ([github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp))
- `harveyxiacn/blender-mcp` — 69 tool groups / 550+ actions; `execute_blender_code` is the primary tool ([github.com/harveyxiacn/blender-mcp](https://github.com/harveyxiacn/blender-mcp))
- `djeada/blender-mcp-server` — production-grade, pip-installable ([github.com/djeada/blender-mcp-server](https://github.com/djeada/blender-mcp-server))
- `nowcika/blender_mcp` — v1.0.0, Blender 4.2+, TCP socket :9999 ([github.com/nowcika/blender_mcp](https://github.com/nowcika/blender_mcp))

<!-- 中文：所有 Blender MCP 都要求本机已安装并运行 Blender（bpy 只在 Blender 内存在）。连接失败时提示用户启动 Blender 与插件。 -->

## 2. bpy Conventions for Printable Models — 打印建模规范

### 2.1 Units & scale — 单位与缩放（必须）

```python
# Force metric millimeters — ALWAYS first  (中文：必须先把场景单位设为毫米)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.001   # 1 BU = 1 mm

# Apply transforms so 1 Blender unit == 1 mm on export
for obj in bpy.context.selected_objects:
    bpy.ops.object.transform_apply(scale=True, rotation=True, location=True)
```

### 2.2 Workflow skeleton — 建模骨架

```python
import bpy, math

# 1) Clean slate for a fresh part
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()

# 2) Build solids with exact mm dimensions
bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0))
box = bpy.context.object
box.scale = (60.0, 30.0, 40.0)            # 60x30x40 mm
bpy.ops.object.transform_apply(scale=True)

# 3) Boolean hole with a cylinder (extend cut through body: fudge)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=5.1, depth=41, location=(0,0,0))
cut = bpy.context.object
mod = box.modifiers.new(name="Cut", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = cut
bpy.context.view_layer.objects.active = box
bpy.ops.object.modifier_apply(modifier="Cut")
bpy.data.objects.remove(cut)

# 4) Wall thickness via Solidify modifier
bpy.ops.object.modifier_add(type='SOLIDIFY')
box.modifiers["Solidify"].thickness = 2.0   # mm, >= 2x nozzle
box.modifiers["Solidify"].offset = 1.0
bpy.ops.object.modifier_apply(modifier="Solidify")
```

### 2.3 Rules — 规则

- **One mesh object per solid body** at export time; apply all modifiers first.
- **Solidify for walls** (exact thickness, easy to check); keep thickness ≥ 2× nozzle (0.8mm default).
- **Boolean fudge**: extend cutting solids 0.01–0.1mm beyond the target to avoid coplanar-face artifacts.
- **Round edges** with Bevel modifier (`width = min(wall, 2)/2`) or subdivision only when topology allows.
- **Avoid tiny triangles**: keep minimum edge ≥ 0.05mm; merge by distance (ε=0.001mm) before export.
- **Organic parts**: if coming from sculpt, remesh (Remesh modifier, Blocks/Quad mode) at a resolution that keeps features ≥ 0.4mm and faces reasonably uniform, then Solidify + check.

## 3. Printability Checks in Blender — 体检（3D-Print Toolbox）

Enable the built-in addon and run checks via bpy (works headless if the addon is enabled):

```python
import bpy
# Enable the 3D-Print Toolbox addon once
bpy.ops.preferences.addon_enable(module="mesh_3d_print_toolbox")

# Solid / manifold check -> writes to context.scene.print3d (result in console/UI)
bpy.ops.mesh.print3d_check_solid()
# Intersections, degenerate (zero-area/thin) faces
bpy.ops.mesh.print3d_check_intersections()
bpy.ops.mesh.print3d_check_degenerate()
# Overhang analysis (angle threshold, e.g. 45 deg)
bpy.ops.mesh.print3d_check_overhang(threshold=45)
# Clean up: make normals consistent, merge by distance
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.mesh.remove_doubles(threshold=0.001)
```

Interpret results (read from `context.scene.print3d` or tool output): **any non-manifold edge, intersecting face, or degenerate face = FAIL** the gate. Fix before exporting. For wall-thickness analysis use the Solidify-cancellation trick or the "Thickness" analysis in the toolbox UI.

## 4. Verification & Screenshot — 验证

1. Run the print checks above; require all clean.
2. Confirm dimensions: `obj.dimensions` (should equal mm after unit setup) — verify against the user's spec.
3. Take a screenshot / OpenGL render via the MCP `screenshot` tool (or `bpy.ops.render.opengl(write_still=True)`) and review the visual, or ask the user to look.
4. Check orientation: largest flat face on the Z=0 plane (print bed); reposition with `obj.location.z = obj.dimensions.z/2` if needed.

## 5. Export — 导出

### 5.1 STL（单件，默认）

```python
import bpy
# Ensure active object selected, then export (binary STL by default)
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = box
box.select_set(True)
bpy.ops.export_mesh.stl(filepath="/path/to/part.stl", use_selection=True, use_scene_unit=True)
```

- `use_scene_unit=True` → exports in real-world mm (requires the metric setup in §2.1).
- Prefer **binary STL**; use 3MF only if the MCP/slicer supports it.
- After export, check file size sanity (a valid STL of a typical part is ≥ tens of KB).
- Keep the `.blend` (or the bpy script) as the editable source; deliver both when possible.

### 5.2 3MF（单件或多零件装配）

Blender 的 3MF 导出依赖 3MF 插件（内置或 Blender3mfFormat，Core Spec 1.2.3）。多零件时**对象名即 3MF part 名**，场景内位置即装配位置：

```python
import bpy
# 1) Ensure the 3MF export operator exists; enable addon if missing
try:
    bpy.ops.export_mesh.threemf
except AttributeError:
    bpy.ops.preferences.addon_enable(module="io_mesh_3mf")
    # if the built-in addon is absent, instruct user to install Blender3mfFormat (Ghostkeeper/ansonl)

# 2) Name parts (these become 3MF part names) and select them
for n in ["P01_base", "P02_lid"]:
    bpy.data.objects[n].select_set(True)

# 3) Export: mm units, modifiers applied, 4-decimal precision
bpy.ops.export_mesh.threemf(
    filepath="/path/to/assembly.3mf",
    use_selection=True,
    global_scale=1.0,
    use_mesh_modifiers=True,
    coordinate_precision=4,
)
```

Full multi-part workflow (naming rules, alignment features, verification, fallback to per-part STL) in `multi-part-assembly.md` §3.2.
