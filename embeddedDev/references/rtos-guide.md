# RTOS Guide — RTOS 使用指南 (FreeRTOS / Zephyr / RT-Thread)

> **中文说明**：本文件规范 RTOS 任务划分、优先级、栈大小、同步原语、看门狗与实时性检查。以 FreeRTOS 语法为主，Zephyr/RT-Thread 给出等价概念对照。

## 1. Task Split — 任务划分原则

| 维度 | 原则 |
|---|---|
| 实时性 | 硬实时任务（电机、通信超时）高优先级；软实时（显示、日志）低优先级 |
| 频率 | 不同执行频率的任务拆开（1kHz 控制 vs 10Hz 上报），用定时器/延迟触发 |
| 阻塞 | 阻塞型操作（UART 等外设等待）放进独立任务，不阻塞主任务 |
| 规模 | 任务数量克制（5–15 个典型），过多增加调度开销与栈内存 |

## 2. Priority & Scheduling — 优先级与调度

- FreeRTOS：数字越大优先级越高（`configMAX_PRIORITIES`）；`xTaskCreate(..., priority, ...)`。
- 高优先级任务不可阻塞时，低优先级饿死 → 用时间片/合作调度（`configUSE_TIME_SLICING`）或降级。
- 中断优先级与任务优先级**分开**：ISR 只做"信号"（置标志/队列），实际工作在任务里。
- Zephyr：`K_PRIO_PREEMPT(n)` / `K_PRIO_COOP(n)`；RT-Thread：数值越小优先级越高（与 FreeRTOS 相反，注意区分）。

## 3. Stack Sizing — 栈大小（关键）

- 栈估算：任务内局部数组/结构体 + 调用深度 × 每层栈帧（HAL 函数可能较大）+ 中断嵌套（ISR 栈通常独立）。
- 经验值起步：简单任务 128–256 字（words），带 HAL/printf 的任务 512–1024 字；**用 `uxTaskGetStackHighWaterMark()` 实测余量**，留 30% 余量。
- 全局总 RAM 预算：`任务栈和 + 空闲任务栈 + 定时器栈 + 堆`，必须 ≤ MCU SRAM，超过就减任务/栈。

## 4. Synchronization Primitives — 同步原语怎么选

| 场景 | 原语 | 说明 |
|---|---|---|
| ISR → 任务通知 | 任务通知 (TaskNotify) / 信号量 (GiveFromISR) | 最轻量；不要用阻塞 API 在 ISR 内 |
| 任务 → 任务数据传递 | 队列 (Queue) / 消息队列 | 带长度限制，防积压 |
| 多任务共享资源 | 互斥量 (Mutex) | 防优先级翻转；临界区只用于极短代码 |
| 事件通知（多信号） | 事件组 (EventGroup) / 信号量计数 | 计数信号量用于"资源计数" |
| 任务间共享数据 | 原子操作/临界区 | 多字节数据必须加保护 |

**错误模式**：在 ISR 中调用 `xSemaphoreTake`（阻塞 API）→ 崩溃；忘记 `xSemaphoreGiveFromISR` 的 `pxHigherPriorityTaskWoken` → 调度异常。

## 5. Watchdog — 看门狗纪律

- 硬件看门狗（IWDG/WWDG）+ 可选软件看门狗；喂狗位置：**主循环或低优先级任务**，绝不能在 ISR 里喂（ISR 活着不代表主逻辑活着）。
- 窗口看门狗（WWDG）：喂早了也不行（窗口期外复位）——正好用于检测"跑飞但还在定时执行"的故障。
- 设计：每个任务更新独立"心跳位"，喂狗前检查所有心跳位，任何任务卡死 → 不喂 → 复位。`任务心跳机制`：

```c
// 每任务在循环末尾置位
static volatile uint8_t task_heartbeat[8];
#define HEARTBEAT_TASK_CTRL 0

// 喂狗函数：全部心跳位为 1 才喂
void watchdog_kick(void) {
    uint8_t all_ok = 1;
    for (int i = 0; i < 8; i++) all_ok &= task_heartbeat[i];
    if (all_ok) { /* IWDG_Reload(); */ }
    else        { /* 记录哪个任务卡死，等复位 */ }
}
```

## 6. Timing & Real-Time Checks — 实时性检查清单

- **ISR 延迟**：`portMAX_DELAY` 之类无；ISR 到任务切换延迟与 ISR 长度成正比——ISR 必须短。
- 用 `xTaskGetTickCount()`/`vTaskDelayUntil()` 做固定周期任务，避免 `vTaskDelay()` 累积漂移：

```c
TickType_t last = xTaskGetTickCount();
for (;;) {
    vTaskDelayUntil(&last, pdMS_TO_TICKS(10));  // 精确 10ms 周期
    control_step();                             // 实时任务体
}
```

- 统计任务最大运行时间（`xTaskGetRunTimeStats()` 开启 `configGENERATE_RUN_TIME_STATS`），交付时给出最坏情况执行时间（WCET）与余量。
- 优先级反转案例：低优先级任务持锁被中优先级抢占 → 高优先级被卡。解法：互斥量带优先级继承（FreeRTOS mutex 默认继承）。

## 7. Memory Management — 内存管理

- FreeRTOS 默认 heap：`heap_4`（合并碎片）适用于多数场景；**ISR 中禁止分配**。
- 静态分配优先：`xTaskCreateStatic` 配合 `configSUPPORT_STATIC_ALLOCATION`，栈与 TCB 编译期定。
- 检查 `configTOTAL_HEAP_SIZE` 与运行时的 `xPortGetFreeHeapSize()` 余量，交付时报告。

## 8. Zephyr / RT-Thread 对照

| 概念 | FreeRTOS | Zephyr | RT-Thread |
|---|---|---|---|
| 任务 | Task | Thread | Thread |
| 优先级方向 | 大 = 高 | 0 最高，大 = 低 | 0 最高，大 = 低 |
| 队列 | Queue | Message queue | Message queue |
| 互斥量 | Mutex (priority inherit) | Mutex | Mutex |
| 信号量 | Semaphore | Semaphore | Semaphore |
| 任务通知 | TaskNotify | k_poll / Sem | — |

**规则**：先确认用户用哪个 RTOS，再按其 API 写；不要混用不同 RTOS 的 API 名。
