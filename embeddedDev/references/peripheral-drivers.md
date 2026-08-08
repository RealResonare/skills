# Peripheral Drivers & Pin Planning — 外设驱动与引脚规划

> **中文说明**：本文件规范引脚规划、时钟树、以及各外设（GPIO/UART/I2C/SPI/ADC/PWM/Timer/DMA）的驱动模式与常见坑。寄存器级内容必须以目标芯片数据手册/参考手册为准；HAL/CMSIS/Arduino API 可按标准写法直接生成，但涉及具体寄存器值时标注"需查数据手册"。

## 1. Pin Planning — 引脚规划（建模先行）

1. **先列外设清单**：每个外设需要的引脚（如 UART=TX/RX，I2C=SDA/SCL，SPI=4 根，ADC=1+，PWM=1+）。
2. **查目标板的引脚图/复用表**（AF 表）确认可用引脚；不要凭记忆猜 AF 编号。
3. **冲突检查**：避免同一引脚被两个外设占用；注意默认调试口（SWD/JTAG）引脚不要被占用，否则无法下载调试。
4. **电平匹配**：3.3V vs 5V 逻辑；开漏/推挽选择；上拉/下拉需求（I2C 必须上拉）。
5. **电气**：ADC 引脚输入阻抗；PWM 引脚输出能力；中断引脚去抖。

交付物：`引脚映射表`（外设 → 引脚 → AF 功能 → 备注），例如：

| 外设 | 引脚 | AF/功能 | 备注 |
|---|---|---|---|
| UART1_TX | PA9 | AF7 (USART1) | 默认调试串口，勿与 SWD 冲突 |
| UART1_RX | PA10 | AF7 (USART1) | |
| I2C1_SDA | PB7 | AF4 (I2C1) | 需 4.7kΩ 上拉 |
| ... | ... | ... | ... |

## 2. Clock Tree — 时钟树

- **先配时钟，再配外设**：外设波特率/定时器分频都依赖总线时钟（APB1/APB2/AHB）。
- 常见顺序：外部晶振 HSE → PLL → SYSCLK → 总线分频（AHB/APB1/APB2）。各总线频率上限查数据手册（如 STM32F1 APB1 ≤36MHz、APB2 ≤72MHz）。
- 用官方工具生成初值（STM32CubeMX、ESP-IDF menuconfig），AI 手写时**必须**核对分频数：`波特率 = 时钟/(16×BRR)` 这类公式算完要验证。
- 交付时给出时钟树摘要：`SYSCLK=72MHz, AHB=72MHz, APB1=36MHz, APB2=72MHz`。

## 3. GPIO 驱动模式

```c
// HAL 示例（STM32）
GPIO_InitTypeDef gpio = {0};
gpio.Pin   = GPIO_PIN_5;
gpio.Mode  = GPIO_MODE_OUTPUT_PP;   // 推挽输出
gpio.Pull  = GPIO_NOPULL;
gpio.Speed = GPIO_SPEED_FREQ_LOW;
HAL_GPIO_Init(GPIOA, &gpio);
HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);
```

| 场景 | Mode | 备注 |
|---|---|---|
| LED/继电器（驱动） | OUTPUT_PP | 注意灌电流/拉电流上限 |
| 开漏总线（I2C） | OUTPUT_OD | 需外部上拉 |
| 输入（按键） | INPUT + 上拉 | 按下为低 |
| 模拟输入 | ANALOG | ADC 引脚 |
| 复用功能 | AF_PP / AF_OD | 串口/SPI 等 |

**坑**：GPIO 初始化后立即写初值（避免上电瞬间误动作）；外部中断回调里只置标志位。

## 4. UART 驱动要点

```c
// 配置：波特率、8-N-1、无流控（3 线）
huart1.Instance        = USART1;
huart1.Init.BaudRate   = 115200;
huart1.Init.WordLength = UART_WORDLENGTH_8B;
huart1.Init.Parity     = UART_PARITY_NONE;
huart1.Init.StopBits   = UART_STOPBITS_1;
HAL_UART_Init(&huart1);
```

- 收发都用**中断或 DMA**（`HAL_UART_Receive_IT` / `HAL_UART_Receive_DMA`），不要在 while 轮询里阻塞主循环（阻塞式只用于调试初始化阶段）。
- 接收缓冲溢出处理：环形缓冲 + `HAL_UART_ErrorCallback`。
- 波特率误差：`误差 = |实际波特率 − 目标| / 目标 ≤ 2~3%`，否则长包会乱码。
- 调试串口打印：`printf` 重定向到 UART（fputc），或 semihosting（见 debugging.md）；**ISR 内禁止 printf**。

## 5. I2C 驱动要点

- **必须上拉**（典型 4.7kΩ @100kHz，2.2kΩ @400kHz）；无外部上拉时用 MCU 内部上拉（不可靠，仅临时调试）。
- 地址：7 位地址；读/写位由协议自动处理，注意 HAL 传的是 `(addr << 1)` 还是裸地址。
- 时序：`HAL_I2C_Master_Transmit(&hi2c1, dev_addr, buf, len, timeout)`；用非阻塞/DMA 版本避免阻塞。
- 坑：总线卡死（SDA 被拉低）→ 软件复位或切换 GPIO 模式产生 9 个时钟脉冲解锁；多主机注意仲裁。

## 6. SPI 驱动要点

- 4 线：MOSI/MISO/SCK/CS；**CS 极性**（低有效默认）与 **CPOL/CPHA**（模式 0–3）必须与外设匹配——SD 卡常用模式 0/3，显示器各异。
- 从设备共享总线时，MISO 在 CS 无效时应为高阻，否则总线冲突。
- 高速时注意 MISO 采样沿：CPHA=0 在 SCK 第一个沿采样；超过几 MHz 用 DMA + 中断完成标志。
- 片选时序：某些器件要求 CS 拉高后再拉低才识别新命令（如 SD 卡）。

## 7. ADC 驱动要点

- 参考电压 `Vref`（内部 1.2V 或 VDD）；`电压 = ADC值 / 满量程 × Vref`。
- 分辨率/采样时间：源阻抗大时要加长采样时间，否则读数偏低。
- 多通道轮询/DMA 连续采集；校准（部分 MCU 需 ADC 校准寄存器）。
- 电池电压监测：分压电阻后读 ADC，注意分压比与输入阻抗（别超过 ADC 输入阻抗要求）。

## 8. Timer / PWM / DMA

- **定时器**：`定时周期 = (ARR+1)×(PSC+1)/TimerClock`；溢出中断里置标志/计数。
- **PWM**：`频率 = TimerClock/((ARR+1)×(PSC+1))`，占空比 = CCR/(ARR+1)；H 桥要配死区时间。
- **DMA**：外设↔内存搬运免 CPU；注意传输完成回调里处理数据；DMA 通道与外设绑定（查数据手册）；内存与外设地址对齐。
- 编码器模式（TIM 正交解码）可直接读电机位置，无需中断计数。

## 9. Protocol Gotchas — 协议常见坑汇总

| 协议 | 最常见问题 | 排查 |
|---|---|---|
| UART | 波特率不准、无流控丢包 | 示波器量 TX 波形周期；降速重试 |
| I2C | SDA 卡死、地址错、无应答 | 逻辑分析仪看 ACK；确认上拉；换地址测试 |
| SPI | 数据错位、CS 时序错 | 看 CPOL/CPHA；确认 CS 极性；低速测试 |
| ADC | 读数漂、偏低 | 查 Vref 与采样时间；加电容滤波 |
| CAN | 无 ACK、总线错误 | 确认 120Ω 终端；查波特率位时序 |
| PWM | 电机抖动、LED 闪烁 | 查频率与分辨率；查死区 |

## 10. Driver Code Template — 驱动代码模板（分层）

```
app/          # 业务逻辑（主循环/任务）
drivers/      # 外设驱动：uart.c, i2c.c, spi.c, adc.c, pwm.c
bsp/          # 板级支持：board.h, clock.c, pin_mux.c
hal/          # 芯片 HAL（厂商库，不改）
```

每个驱动文件建议导出：`xxx_init()`、`xxx_read()/xxx_write()`、`xxx_deinit()`，错误码统一 `int8_t` 或枚举，返回 0 成功。
