---
name: embeddedDev
description: 嵌入式固件开发 playbook：需求澄清、MCU/外设选型、引脚规划、外设驱动、RTOS、通信协议、功耗优化、调试与验证。用于"开发/编写/调试某个单片机固件"类任务。
---

# embeddedDev — 嵌入式固件开发 playbook

> **English Quick Start**
>
> This skill drives firmware development for resource-constrained MCUs: requirement clarification, MCU/peripheral selection, pin planning, peripheral drivers, RTOS, communication protocols, power optimization, debugging and verification.
> Core loop: **需求澄清 → 选型与引脚规划 → 分层编码（HAL/驱动/应用） → 静态检查与构建 → 硬件在环验证 → 交付**.
> Hard rules: never fabricate register values/datasheet facts (verify against the datasheet or state the assumption), never use dynamic allocation in ISRs, always check return values, keep ISRs short. When in doubt about hardware behavior, ask the user or mark it UNVERIFIED.

## Purpose

This skill guarantees that firmware produced by the AI is correct against real hardware constraints: correct clock/pin configuration, deterministic timing, safe interrupt handling, bounded memory use, and a build that actually compiles. It works across common toolchains (PlatformIO, ESP-IDF, STM32Cube, Arduino, Zephyr) and detects whatever build/verify tooling is available at runtime (MCP or CLI). It acts as a **generic adaptation layer** — it does not depend on any single MCP server.

## When to Invoke

Invoke whenever the user wants to:

- Develop firmware for a microcontroller (STM32, ESP32, AVR/Arduino, nRF, RP2040, RISC-V, etc.).
- Plan pins/peripherals, configure clocks, write peripheral drivers (GPIO/UART/I2C/SPI/ADC/PWM/DMA/Timer).
- Add RTOS tasks (FreeRTOS/Zephyr/RT-Thread), synchronization, or solve real-time scheduling problems.
- Debug firmware: build errors, hard faults, timing issues, protocol issues, power consumption.
- Generate code with HAL/CMSIS/Arduino/ESP-IDF APIs.

Do **not** invoke for pure hardware/PCB design (see electricDesign for circuit-level work) or general-purpose software engineering without an MCU target.

## Unified Pipeline (Mandatory Order)

Run every firmware task through this pipeline. Do not skip the verification gates.

| # | Step | Gate / Rule |
|---|---|---|
| 1 | **Collect requirements** | Always establish: MCU family & board, framework (HAL/LL/CMSIS/Arduino/ESP-IDF), toolchain, target clock, peripherals needed, real-time constraints, power budget, memory budget. If the user names a board (e.g. "ESP32 devkit"), pin out the default wiring. State assumptions explicitly. |
| 2 | **Select & plan** | Choose MCU/peripheral mapping, clock tree, pin assignment (see `references/peripheral-drivers.md`). For RTOS: task split, priorities, stack sizes (see `references/rtos-guide.md`). For low power: sleep/wake plan (see `references/power-optimization.md`). |
| 3 | **Code by layers** | Write HAL/driver layer first (pin, clock, peripheral init), then BSP/application on top. One logical unit per step; verify after each. Never skip init-order requirements (clock before UART, etc.). |
| 4 | **Static check & build** | Compile with the real toolchain (PlatformIO `pio run`, `idf.py build`, `make`, etc.) or MCP build tools. Fix every warning; treat warnings as errors in release builds. Run static analysis (cppcheck, `-Wall -Wextra -Werror`) where available. |
| 5 | **Hardware-in-loop gate** | Flash & run on target when available (or clearly mark UNVERIFIED). Verify: system clock correct, peripherals respond, interrupts fire, no hard fault, timing meets spec, memory within budget. Report what was and wasn't verified. |
| 6 | **Deliver** | Source tree, build log summary, pin mapping table, verified/UNVERIFIED list, power & memory numbers, next steps. |

## Core Rules (Non-Negotiable)

<!-- 中文：以下为硬性规则，任何时候不得违反。 -->

1. **Never invent datasheet facts.** Register addresses, bit fields, clock values, pin functions come from the datasheet/reference manual or the HAL — verify before writing. If you cannot verify, write the code against HAL/CMSIS APIs and state "needs datasheet check".
2. **ISRs must be short and non-blocking.** Set a flag / post to a queue; do the work in the main loop or task. No `printf`, no `malloc`, no long loops in ISR.
3. **No dynamic allocation in ISRs or safety-critical paths.** Prefer static allocation; check `malloc`/`new` return values everywhere.
4. **Always check return values** of HAL calls, `xSemaphoreTake`, `pvPortMalloc`, etc. Handle errors, don't ignore them.
5. **Use fixed-width types** (`stdint.h`: `uint8_t`, `uint32_t`, ...). No bare `int` for registers/hardware values.
6. **Initialize all variables before use.** Declared-but-uninitialized is a bug.
7. **Bounds-check everything** — arrays, buffers, protocol parsing. Buffer overflow is a hard fault waiting to happen.
8. **Watchdog discipline.** If a watchdog is enabled, ensure it is fed from a safe place, never from an ISR-only path, and design the system so a hang triggers reset.
9. **Volatile for shared variables** between ISR and main context; use atomics or critical sections for multi-byte access.
10. **State what you cannot verify.** If you can't flash the board, say so. If the exact register value needs the datasheet, say so.

## Communication Protocols Cheat-sheet (see `references/peripheral-drivers.md`)

| Protocol | Pins/Interface | Typical use | Common gotchas |
|---|---|---|---|
| UART | TX/RX (+CTS/RTS) | Debug, GPS, sensors | baud rate mismatch; no flow control in 3-wire; buffer overflow at high baud |
| I2C | SDA/SCL (+pull-ups) | Sensors, EEPROM | pull-up resistors required; address conflicts; clock stretching |
| SPI | MOSI/MISO/SCK/CS | Flash, displays, SD | CS polarity/timing; MISO float when CS high; clock phase/polarity (CPOL/CPHA) |
| ADC | analog pin | Sensors, battery | reference voltage; resolution; sampling time vs source impedance |
| PWM | timer output | LED, motor, servo | timer frequency vs resolution; dead-time for H-bridge |
| CAN | CAN_H/CAN_L + transceiver | Automotive, industrial | termination 120Ω; bit timing per bus length |

## References

| File | Content |
|---|---|
| `references/peripheral-drivers.md` | Pin planning, clock tree, GPIO/UART/I2C/SPI/ADC/PWM/Timer/DMA driver patterns, protocol gotchas |
| `references/rtos-guide.md` | FreeRTOS/Zephyr patterns: task split, priorities, stack sizing, queues/semaphores/mutexes, watchdog & timing |
| `references/power-optimization.md` | Sleep modes, clock gating, wake sources, battery math, measurement checklist |
| `references/debugging.md` | Build errors, hard faults, JTAG/SWD, printf/semihosting, logic analyzer tips, memory map analysis |
| `references/coding-standards.md` | MISRA C:2012 essentials, BARR-C, defensive coding patterns, code review checklist |

## Output Contract

Every deliverable must include:

1. **Source code tree** with layered structure (HAL/driver/app), ready to build.
2. **Pin mapping table**: peripheral → pin → alternate function (AF) → notes.
3. **Build verification**: compile result (PASS/FAIL), warnings fixed, size (flash/RAM) vs budget.
4. **Hardware verification status**: what was tested on target vs marked UNVERIFIED.
5. **Assumptions**: board/framework/datasheet facts assumed, left for user confirmation.
