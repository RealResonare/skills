# Debugging — 调试手册

> **中文说明**：本文件覆盖嵌入式调试全链路：编译错误、硬故障(HardFault)、JTAG/SWD、printf/semihosting、逻辑分析仪、内存分析。目标是让 AI 遇到调试任务时按图索骥，而不是瞎猜。

## 1. Build Errors — 编译错误排查

| 错误类型 | 常见原因 | 处理 |
|---|---|---|
| undefined reference to `HAL_xxx` | 链接缺库/文件没加入编译 | 检查源文件是否在构建列表；库路径 |
| implicit declaration | 缺头文件/函数未声明 | 包含正确头文件；函数前向声明 |
| multiple definition | 全局变量在头文件定义 | `extern` + .c 定义；或 `static` |
| alignment/padding 警告 | 结构体对齐 | 加 `__attribute__((packed))` 前先想清楚（性能 vs 兼容）；协议结构体用 packed |
| 链接超 ROM/RAM | 固件太大 | 看 map 文件定位；优化级别；裁剪功能 |
| HardFault 复位 | 见 §2 | 定位异常 |

**工具**：`-Wall -Wextra -Werror`（开发期）；cppcheck 静态分析；看 `.map`/`size` 输出（`text`=flash，`data+bss`=RAM）。

## 2. Hard Fault — 硬故障排查（最重要）

**现象**：程序复位/卡死。**方法**：在 HardFault_Handler 里断点，读 `SCB->HFSR`、`SCB->CFSR`、`SCB->MMFAR/BFAR`，并用 `__get_PSP()/__get_MSP()` 拿到栈指针，从栈回溯 PC/LR。

```c
void HardFault_Handler(void) {
    volatile uint32_t hfsr = SCB->HFSR;
    volatile uint32_t cfsr = SCB->CFSR;
    volatile uint32_t mmfar = SCB->MMFAR;
    volatile uint32_t bfar  = SCB->BFAR;
    volatile uint32_t sp = __get_PSP();   // 线程模式栈
    (void)hfsr; (void)cfsr; (void)mmfar; (void)bfar; (void)sp;
    __asm volatile("bkpt #0");            // 断点停下，便于调试器读寄存器
    for(;;);
}
```

| CFSR 位 | 含义 | 常见根因 |
|---|---|---|
| IACCVIOL / DACCVIOL | 取指/数据访问违例 | 空指针、野指针 |
| UNALIGNED | 非对齐访问 | packed 结构体或未对齐指针强转 |
| IBUSERR / PRECISERR | 总线错误 | 访问未映射地址（0x00000000 等） |
| UNDEFINSTR | 未定义指令 | 跳到数据区/PC 错乱 |
| STKOF | 栈溢出 | 任务栈太小（FreeRTOS） |

**排查套路**：空指针 → 数组越界 → 未初始化指针 → 栈溢出 → 外设寄存器访问时机。最有效的工具：**寄存器转储 + 栈回溯**。

## 3. JTAG / SWD — 调试接口

- SWD 只需 2 线（SWDIO/SWCLK）+ GND + 可选 RST；JTAG 4 线。引脚被占用 → 无法连接（见 peripheral-drivers §1 冲突检查）。
- 常用命令：`openocd -f interface/... -f target/...` 后接 GDB；PlatformIO 内置 `pio debug`；STM32CubeIDE/ESP-IDF 自带调试器。
- **烧录失败排查**：确认 BOOT 引脚、供电、调试器驱动、芯片锁定（`connect under reset` 解锁）。
- 断点/单步会改变时序——实时性问题用 trace（ITM/SWO）或逻辑分析仪，而不是断点。

## 4. printf / Semihosting — 日志输出

| 方式 | 优点 | 缺点 |
|---|---|---|
| UART printf 重定向 | 简单、无线缆依赖 | 占用一个 UART；波特率限制；ISR 内禁止 |
| Semihosting (SWO/ITM) | 不占串口、速度快 | 需要调试器连接；正式运行不可用 |
| RTT (SEGGER) | 高速、双向、不断点 | 需 J-Link 或兼容调试器 |

```c
// UART printf 重定向示例（STM32 HAL）
int _write(int fd, char *ptr, int len) {
    HAL_UART_Transmit(&huart1, (uint8_t*)ptr, len, HAL_MAX_DELAY);
    return len;
}
```

**坑**：semihosting 在无调试器时会卡死（BKPT 指令挂起）——正式固件里用宏关闭（`#ifdef DEBUG`）。

## 5. Logic Analyzer / Oscilloscope — 波形工具

| 工具 | 看什么 | 典型问题定位 |
|---|---|---|
| 逻辑分析仪 | I2C/SPI/UART 时序、ACK、位序 | 协议无响应、数据错位 |
| 示波器 | 电平、边沿、毛刺、电源纹波 | 供电不稳、干扰、复位原因 |
| 电流探头/万用表 | 电流波形、睡眠电流 | 功耗异常 |

**协议排查步骤**：低速(如 I2C 100kHz / SPI 慢速)先跑通 → 抓波形对比数据手册时序图 → 逐步提速。

## 6. Memory Map Analysis — 内存分析

- 用 `.map` 文件查：最大函数、RAM 占用 TOP 榜（`bss/data`）。
- 栈使用：`uxTaskGetStackHighWaterMark()`（FreeRTOS）或链接器栈金丝雀检测。
- 堆使用：`xPortGetFreeHeapSize()`；内存泄漏排查：统计分配/释放对。
- Flash 占用：`size` 输出 `text` 段；超限时查 map 里最大的几项（通常 printf/浮点库很占）。

## 7. Debug Flow — 调试流程（按序执行）

1. **复现**：确认现象、条件（上电/特定操作/随机）。
2. **收集**：串口日志、复位原因寄存器（RCC->CSR 看复位源）、HardFault 寄存器。
3. **假设-验证**：每次只改一个变量；优先查"边界条件"（首次运行、缓冲区满、并发中断）。
4. **回归**：修复后跑全量功能测试，确认无副作用。
5. **记录**：交付时写明根因、修复、验证方式。
