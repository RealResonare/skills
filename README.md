# skills

可复用的 AI 技能集合。仓库中的每个目录都是一个独立 Skill，以 `SKILL.md` 为入口定义，可被支持 Agent Skills 标准的助手（reasonix、Claude Code 等）加载使用。

## 技能列表

| 技能 | 目录 | 适用场景 |
| --- | --- | --- |
| electricDesign | `electricDesign/` | 模拟与数字电路设计：需求澄清、参数计算、SPICE 网表生成、仿真验证与示意图绘制 |

## 安装

将技能目录放入助手的 skills 目录即可，例如 reasonix 的默认位置为 `%APPDATA%\reasonix\skills\`：

```powershell
# 以 electricDesign 为例
Copy-Item -Recurse electricDesign "$env:APPDATA\reasonix\skills\"
```

也可以克隆本仓库后从本地引用所需技能：

```bash
git clone https://github.com/RealResonare/skills.git
```

## electricDesign：电路设计

面向"设计 / 计算 / 验证某个电路"类任务，走完整闭环：**需求澄清 → 选模板或从原理设计 → 参数计算 → 自检 → SPICE 网表 → 仿真验证 → 示意图 → 交付**。参数缺失时不会编造，会向用户询问或显式标注假设。

### 目录结构

```
electricDesign/
├── SKILL.md            # 技能定义（工作流、交付模板、公式速查）
├── templates/          # 9 个内置电路模板
├── scripts/
│   ├── run_sim.py      # 用 ngspice 跑 SPICE 网表，输出统计值与波形
│   └── draw_circuit.py # 用 schemdraw 按 DSL 画电路示意图
└── examples/           # 完整设计样例
```

### 内置模板

| 模板 | 适用场景 |
| --- | --- |
| 电阻分压器 | 电压衰减、ADC 分压、偏置 |
| RC 低通/高通滤波 | 滤波、积分、去耦、一阶频率整形 |
| 运放放大电路 | 同相/反相/跟随/差分放大 |
| LED 限流 | LED 驱动、指示灯 |
| 三极管开关 | 电平转换、继电器/负载开关 |
| MOSFET 开关 | 高侧/低侧功率开关 |
| LDO 稳压 | 低压差稳压电源 |
| 整流滤波 | AC 转 DC（半波/全波/桥式） |
| 逻辑门与上拉下拉 | 数字输入/输出、总线电平、开漏 |

### 脚本与依赖

仿真与绘图脚本位于 `scripts/`：

```bash
# 仿真：输出统计值与波形
python scripts/run_sim.py circuit.cir --plot wave.png --probe out,in

# 绘图：按 DSL 生成电路示意图 PNG
python scripts/draw_circuit.py circuit.elements out.png
```

依赖：

- `pip install schemdraw`：绘制电路示意图
- ngspice：执行仿真。`run_sim.py` 依次查找环境变量 `NGSPICE` → PATH → 常见安装路径，找不到时打印安装指引（Windows 可 `winget install ngspice`）

### 使用示例

`examples/示例RC低通.md` 给出一个完整的 RC 低通滤波器设计样例，覆盖从需求澄清到交付的每一步，可作参照。

## 新增技能

每个技能目录以 `SKILL.md` 为核心，frontmatter 声明 `name` 与 `description`，正文描述使用场景与工作流；模板、脚本、示例等资源与 `SKILL.md` 同级组织。新增技能后同步更新上方技能列表与安装说明。
