# skills

可复用的 AI 技能集合。仓库中的每个目录都是一个独立 Skill，以 `SKILL.md` 为入口定义，可被支持 Agent Skills 标准的助手（reasonix、Claude Code 等）加载使用。

## 技能列表

| 技能 | 目录 | 适用场景 |
| --- | --- | --- |
| electricDesign | `electricDesign/` | 模拟与数字电路设计：需求澄清、参数计算、SPICE 网表生成、仿真验证与示意图绘制 |
| 3dprint | `3dprint/` | 3D 打印建模：通过 MCP 控制 OpenSCAD / Blender 建模、可打印性检查、STL/3MF 导出与切片参数报告 |
| embeddedDev | `embeddedDev/` | 嵌入式固件开发：需求澄清、MCU/外设选型、引脚规划、外设驱动、RTOS、通信协议、功耗优化、调试与验证 |

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

## 3dprint：3D 打印

面向"生成 / 检查 / 修复 / 准备 3D 打印模型"类任务：AI 通过 MCP 控制 **OpenSCAD** 或 **Blender** 建模，并保证模型真正满足可打印性约束（水密流形、壁厚、悬垂、公差、单位），最终导出 STL / 3MF 并附切片参数报告。不依赖任何特定 MCP 服务器：运行时探测可用工具，无 MCP 时回退本地 CLI。

### 核心流程

**收集打印约束 → 选引擎建模 → 可打印性体检 → 导出 + 切片报告**

- 打印约束默认假设：FDM、0.4mm 喷嘴、PLA、220×220×250mm，并向用户明示假设
- 引擎路由：OpenSCAD = 参数化/机械件；Blender = 有机曲面/复杂装配；用户指定优先
- 体检硬性门禁：水密流形、壁厚 ≥ 2×喷嘴（0.8mm）、悬垂 ≤ 45°、最小特征 ≥ 0.4mm、孔位补偿
- 导出：单件用二进制 STL；多零件装配用 3MF（一文件多 part，内嵌毫米单位）
- 涉及螺丝/嵌件时，查螺纹参数库选用对应方案与孔径

### 目录结构

```
3dprint/
├── SKILL.md            # 技能定义（统一流程、引擎路由、硬性规则、交付契约）
└── references/
    ├── printability-checklist.md   # 打印前体检清单：水密性/壁厚/悬垂/公差 + 材料差异表
    ├── thread-library.md           # 螺纹参数库：ISO 公制螺纹、间隙孔、热熔嵌件、打印螺纹规范
    ├── multi-part-assembly.md      # 多零件装配与 3MF 导出（lazy-union / Blender 3MF 插件）
    ├── openscad-workflow.md        # OpenSCAD 引擎：工具映射、代码规范、验证与导出
    ├── blender-workflow.md         # Blender 引擎：bpy 规范、3D-Print Toolbox 体检、导出
    └── slicing-params.md           # 切片与导出规范：格式规则、材料温度表、切片参数报告
```

### 使用示例

- "帮我设计一个 PLA 手机支架，0.4mm 喷嘴" → 走 OpenSCAD 流程，体检后导出 STL
- "这个 STL 能打印吗？帮我检查" → 跑可打印性清单，逐项报告 PASS/FAIL
- "做一个带 M3 热熔嵌件、分件上盖的电子壳，导出 3MF" → 螺纹库选嵌件孔位 + 多零件 3MF 导出

## embeddedDev：嵌入式固件开发

面向"开发 / 编写 / 调试某个单片机固件"类任务，覆盖 MCU（STM32 / ESP32 / AVR / nRF / RP2040 等）固件开发全流程：**需求澄清 → 选型与引脚规划 → 分层编码（HAL/驱动/应用） → 静态检查与构建 → 硬件在环验证 → 交付**。不编造数据手册事实：寄存器/时钟/引脚复用以数据手册或 HAL 为准，无法验证时明确标注"需查数据手册"。

### 核心规则

- ISR 短小无阻塞，只置标志/通知，禁止 printf / malloc
- 禁止在 ISR 与安全关键路径动态分配；静态分配优先
- 所有 HAL 调用 / 信号量 / 内存分配的返回值必须检查
- 使用 `<stdint.h>` 定宽类型；变量使用前初始化；边界检查
- 看门狗喂狗放在主循环/低优先级任务，绝不放在 ISR
- 无法真机验证时明确报告 UNVERIFIED，不假装通过

### 目录结构

```
embeddedDev/
├── SKILL.md            # 技能定义（统一流程、硬性规则、交付契约）
└── references/
    ├── peripheral-drivers.md   # 引脚规划、时钟树、GPIO/UART/I2C/SPI/ADC/PWM/DMA 驱动模式
    ├── rtos-guide.md           # FreeRTOS/Zephyr/RT-Thread：任务划分、优先级、栈大小、同步原语、看门狗
    ├── power-optimization.md   # 睡眠模式、时钟门控、唤醒源、电池寿命计算、测量清单
    ├── debugging.md            # 编译错误、HardFault、JTAG/SWD、printf/semihosting、逻辑分析仪
    └── coding-standards.md     # MISRA C:2012 要点、BARR-C、防御性编程、代码审查清单
```

### 使用示例

- "写一个 STM32F103 的 UART + 定时器点灯固件" → 走分层编码流程，编译验证后交付引脚映射表
- "FreeRTOS 三个任务一个卡死，帮我查" → 栈余量 + 心跳看门狗 + HardFault 定位
- "ESP32 电池供电，目标待机 1 年" → 功耗设计 + 平均电流/寿命计算

## 新增技能

每个技能目录以 `SKILL.md` 为核心，frontmatter 声明 `name` 与 `description`，正文描述使用场景与工作流；模板、脚本、示例等资源与 `SKILL.md` 同级组织。新增技能后同步更新上方技能列表与安装说明。
