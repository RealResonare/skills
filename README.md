# skills

可复用的 AI 技能集合。仓库中的每个目录都是一个独立 Skill，以 `SKILL.md` 为入口定义，可被支持 Agent Skills 标准的助手（reasonix、Claude Code 等）加载使用。

## 技能列表

| 技能 | 目录 | 适用场景 |
| --- | --- | --- |
| electricDesign | `electricDesign/` | 模拟与数字电路设计：需求澄清、参数计算、SPICE 网表生成、仿真验证与示意图绘制 |
| 3dprint | `3dprint/` | 3D 打印建模：通过 MCP 控制 OpenSCAD / Blender 建模、可打印性检查、STL/3MF 导出与切片参数报告 |
| embeddedDev | `embeddedDev/` | 嵌入式固件开发：需求澄清、MCU/外设选型、引脚规划、外设驱动、RTOS、通信协议、功耗优化、调试与验证 |
| bupt-bachelor-thesis | `bupt-bachelor-thesis/` | 北邮本科毕业论文：基于内置 LaTeX 模板创建/修改/编译毕业论文（含封面、摘要、章节、参考文献） |
| bupt-beamer-slides | `bupt-beamer-slides/` | 北邮风格 Beamer 幻灯片：论文/报告转 Beamer、课程汇报 PPT，内置 BUPT 主题模板 |
| latex-book | `latex-book/` | 中文数学书籍 LaTeX 模板：写书/教材/讲义/数学专著，内置定理环境、封面、章节样式 |
| pcbDesign | `pcbDesign/` | PCB 设计：需求澄清、叠层/阻抗规划、原理图到布局、布线规则、DFM/EMC 检查、制造文件导出（可 MCP 驱动 KiCad） |

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

## bupt-bachelor-thesis：北邮本科毕业论文

面向"写北邮本科毕业论文 / 将内容转为北邮论文 LaTeX 格式"类任务。模板内置于 Skill（无需 clone 远程仓库），工作流：**复制模板 → 填元数据（main.cfg）→ 填摘要关键词（abstract.cfg）→ 替换正文（main.tex）→ 加图/表/代码 → 填参考文献（ref.bib）→ XeLaTeX 编译**。

### 目录结构

```
bupt-bachelor-thesis/
├── SKILL.md            # 技能定义（资产清单、标准流程、常见问题修复）
└── assets/template/    # 内置完整模板
    ├── main.tex        # 主入口（封面/任务书/摘要/章节/参考文献/附录）
    ├── main.cfg        # 论文元数据（题目、致谢）
    ├── abstract.cfg    # 中英文摘要与关键词
    ├── ref.bib         # BibTeX 参考文献
    ├── BUPTthesisbachelor.sty / buptbachelor.bst  # 样式与参考文献风格
    ├── pictures/       # 图
    ├── docs/           # 封面/任务书/成绩单/声明等行政材料（PDF+Word 源）
    └── guidebook/      # 使用说明
```

### 使用示例

- "帮我写北邮毕设论文，题目是 XX" → 复制模板 → 填元数据/摘要 → 按章节写入正文 → 编译
- "论文编译报错 Times New Roman 缺失" → 换 Tinos 或装微软字体
- "参考文献全是问号" → 跑完整四步编译序列

## bupt-beamer-slides：北邮风格 Beamer 幻灯片

面向"北邮 Beamer / 论文报告转 PPT / 课程汇报幻灯片"类任务。内置 BUPT 主题（北邮蓝 #3434b4、smoothbars 导航、标题页 logo、编号题注），工作流：**初始化项目 → 编辑 slide.tex → 转换内容为幻灯片结构 → 编译验证**。

### 目录结构

```
bupt-beamer-slides/
├── SKILL.md            # 技能定义（资产清单、标准流程、模板说明、验证）
├── scripts/
│   └── init_bupt_beamer.py   # 从模板初始化新幻灯片项目（可移植，自动定位模板）
└── assets/template/    # 内置 BUPT Beamer 模板
    ├── slide.tex       # 主入口
    ├── BUPT.sty        # 主题样式
    ├── ref.bib         # 参考文献
    └── pic/            # BUPT logo 等
```

### 使用示例

- "把我的报告转成北邮 Beamer" → 初始化项目 → 按"背景/方法/实验/结论"结构转幻灯片 → 编译
- "北邮风格的 16:9 汇报 PPT" → `\documentclass[aspectratio=169]{beamer}` + BUPT 主题
- "编译报字体错误" → 安装 Noto CJK/Tinos 字体（见 Template Notes）

## latex-book：中文数学书籍 LaTeX 模板

面向"用 LaTeX 写书 / 教材 / 讲义 / 数学专著"类任务。基于 `book` 文档类，内置：中文支持（ctex）、数学字体与定理环境（定理/定义/引理/推论/命题/例题/注/证明/解）、三色章节样式、封面页与页眉页脚。工作流：**初始化项目 → 改书名/作者 → 按章写正文 → 编译两遍**。

### 目录结构

```
latex-book/
├── SKILL.md            # 技能定义（资产清单、标准流程、定理环境速查、常见问题）
├── scripts/
│   └── init_book.py    # 初始化脚本：复制模板 + 生成占位封面（可移植，自动定位模板）
└── assets/template/    # 内置书籍模板
    ├── main.tex        # 主入口（含"用户替换区"：书名/作者/日期）
    └── cover.png       # 占位封面（脚本生成，可替换为真实封面）
```

### 使用示例

- "帮我写一本 LaTeX 教材，书名 XX" → 初始化项目 → 改书名作者 → 按章写正文 → 编译
- "数学讲义要定理/定义/证明环境" → 模板已预置，直接用 `theorem`/`definition`/`proof` 等环境
- "编译报缺字体" → 安装 `texlive-xetex` / `texlive-lang-chinese` / `fonts-noto-cjk`

## pcbDesign：PCB 设计

面向"设计 / 评审 / 检查某个 PCB 板"类任务，覆盖 PCB 设计全流程：**需求澄清 → 叠层与设计规则规划 → 原理图 → 布局 → 布线 → DRC/DFM/EMC 检查 → 制造文件 → 交付**。可通过 MCP 驱动 KiCad（通用适配层，运行时探测工具），无 MCP 时回退 `kicad-cli` 命令行。

### 核心规则

- 不编造数据手册/板厂数值：引脚、封装、叠层 Dk、制程极限以数据手册与厂商能力表为准
- 导出前必须 DRC：0 error，warning 逐条解释或修复
- 每个信号层邻接连续参考平面；高速信号禁止跨平面分割
- 去耦电容就近放置（≤3mm）；平面连接焊盘用热焊盘
- 无法验证项明确标注 UNVERIFIED，不假装通过

### 目录结构

```
pcbDesign/
├── SKILL.md            # 技能定义（统一流程、硬性规则、交付契约）
└── references/
    ├── design-rules.md         # 叠层/层数、阻抗目标表、原理图要点、布局布线规则、PDN
    ├── dfm-checklist.md        # 可制造性清单：线宽/过孔/阻焊/丝印/拼板/铜平衡/装配
    ├── emc-guidelines.md       # EMC 设计：回流路径、平面分割、滤波、I/O 防护、接地缝合
    └── manufacturing-export.md # Gerber RS-274X/钻孔/BOM/贴片导出、kicad-cli 命令、下单确认清单
```

### 使用示例

- "设计一个 ESP32 四层板，带 USB 和传感器" → 叠层/阻抗规划 → 原理图 → 布局布线 → DRC/DFM → 制造文件
- "帮我评审这块板的 DRC 和 DFM" → 跑 DRC + DFM 清单，逐项 PASS/FAIL 报告
- "导出 Gerber + BOM + 贴片文件" → kicad-cli 或 MCP 导出，打包交付

## 新增技能

每个技能目录以 `SKILL.md` 为核心，frontmatter 声明 `name` 与 `description`，正文描述使用场景与工作流；模板、脚本、示例等资源与 `SKILL.md` 同级组织。新增技能后同步更新上方技能列表与安装说明。
