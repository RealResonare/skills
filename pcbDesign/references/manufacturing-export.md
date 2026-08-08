# Manufacturing Export — 制造文件导出

> **中文说明**：本文件规范制造文件（Gerber/钻孔/BOM/贴片）的导出与交付。KiCad MCP 服务器通常提供 `export_gerbers` 等工具；无 MCP 时用 `kicad-cli` 命令行导出。

## 1. 文件清单（交付包）

| 文件 | 内容 | 格式 |
|---|---|---|
| Gerber 光绘 | 各层布线/阻焊/丝印/板框 | RS-274X（.gbr） |
| 钻孔文件 | 机械孔/激光孔 | Excellon（.drl） |
| BOM | 物料清单 | CSV/Excel（含位号、值、封装、供应商） |
| Pick&Place | 贴片坐标 | CSV（位号、X/Y、角度、层） |
| 叠层表 | 层结构/材料/阻抗 | PDF/文本 |
| 制造说明 | 特殊工艺（阻抗、背钻、表面处理） | PDF/文本 |
| 装配图 | 位号+极性标识 | PDF/图片 |

## 2. Gerber 导出规范

- 格式：**RS-274X**（现代标准）；精度常用 4:4 或 4:5（整数+小数位数），与板厂确认。
- 单位：公制 mm（与板厂确认，避免英制/公制错乱）。
- 各层命名规范（KiCad 默认即合规）：
  - 铜层：`*.F_Cu.gbr` / `*.B_Cu.gbr` / `*.In1_Cu.gbr`...
  - 阻焊：`*.F_Mask.gbr` / `*.B_Mask.gbr`
  - 丝印：`*.F_Silkscreen.gbr` / `*.B_Silkscreen.gbr`
  - 板框：`*.Edge_Cuts.gbr`
- 钻孔：`*.drl`（Excellon），含 `*.drl` 孔径列表 `*.drl`（tool list）或附 drill map。
- 用板厂免费 DFM 工具（JLCPCB/JLCTest、嘉立创 DFM、Oshpark）预检一次再下单。

## 3. KiCad CLI 导出（无 MCP 回退）

```bash
# 生成所有制造文件到 fab/ 目录
kicad-cli pcb export gerbers <board>.kicad_pcb -o fab/
kicad-cli pcb export drill <board>.kicad_pcb -o fab/
kicad-cli pcb export pos <board>.kicad_pcb -o fab/        # Pick&Place
kicad-cli pcb export bom <board>.kicad_pcb -o fab/        # BOM（需要 XSLT 转换器）
```

> 中文提醒：`kicad-cli` 的 bom 导出需要 `--xsl` 样式表或配合插件；更稳的做法是从原理图导出 BOM（`kicad-cli sch export bom`）。

## 4. BOM 规范

| 列 | 示例 | 必填 |
|---|---|---|
| Reference | R1, C2, U3 | ✅ |
| Value | 10kΩ, 100nF, ESP32-S3 | ✅ |
| Footprint | 0603, SOT-23, QFN-48 | ✅ |
| Quantity | 2 | ✅ |
| MPN / Supplier | RC0603FR-0710KL (Yageo) | 建议 |
| 备注 | 耐压/精度/替代料 | 可选 |

- 汇总同值同封装数量；标注易缺料件（长交期、专用型号）。
- 无源件建议给替代料；关键器件（电源 IC、主控）给首选+备选。

## 5. 交付 ZIP 结构与命名

```
project_v1.0_fab/
├── Gerber/            # 全部 .gbr + .drl
├── BOM/
│   └── BOM_v1.0.csv
├── PickPlace/
│   └── pos_v1.0.csv
├── Stackup/
│   └── stackup_v1.0.pdf
└── README.txt         # 版本、阻抗需求、特殊工艺、板厂确认项
```

命名：`项目名_版本_日期`；每次改版递增版本号，不覆盖旧包。

## 6. 下单前最后确认（与板厂核对）

- [ ] 最小线宽/间距满足制程（见 dfm-checklist）
- [ ] 最小孔径/孔径比满足制程
- [ ] 阻抗目标+容差已写明（叠层表）
- [ ] 表面处理（HASL/ENIG/OSP）选择
- [ ] 板厚、层数、铜厚确认
- [ ] 拼板/工艺边/邮票孔确认
- [ ] 特殊工艺：背钻、树脂塞孔、半孔、阻抗控制说明
- [ ] DRC 0 error（KiCad DRC 报告随包交付）
