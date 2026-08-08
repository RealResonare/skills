# Coding Standards — 编码规范 (MISRA C:2012 要点 + BARR-C)

> **中文说明**：本文件是嵌入式 C/C++ 编码规范速查。MISRA C:2012 是安全关键系统的行业标准（航空航天/汽车/医疗），BARR-C 是面向一般嵌入式可靠性且免费的标准，二者不冲突（MISRA 可视为 BARR-C 的子集）。AI 生成的代码应默认满足以下规则。

## 1. 必须遵守的核心规则（Mandatory）

| 规则 | 反例 ❌ | 正例 ✅ |
|---|---|---|
| 无未定义行为 (Rule 1.3) | `int x; return x+5;`（未初始化） | `int x = 0;` |
| 变量使用前必须初始化 (Rule 9.1) | 声明后条件分支才赋值 | 声明即初始化 |
| 越界检查 (Rule 18.1) | `arr[10]=5`（越界写） | `if (idx < 10) arr[idx]=5;` |
| 显式布尔比较 (Rule 14.4) | `if (ptr)` / `if (count)` | `if (ptr != NULL)` / `if (count != 0U)` |
| 检查返回值 (Rule 17.7) | `pvPortMalloc(1024);` 忽略 | `void* p = pvPortMalloc(...); if (p == NULL) {...}` |
| 禁止动态内存（安全关键）(Rule 21.3) | `malloc/free` 散落 | 静态数组/内存池 |
| 最小作用域 (Rule 8.9) | 全局变量到处用 | `static` 局部 |
| 禁止 goto (Rule 15.1) | 用 goto 跳转 | 单出口结构化流程 |

## 2. 类型规范（跨平台一致）

- 一律使用 `<stdint.h>` 定宽类型：`uint8_t/uint16_t/uint32_t/int32_t`；禁止裸 `int/char` 表示硬件值。
- 常量加后缀：`U`（无符号）、`L`（长），如 `(10U)`；避免隐式符号转换警告。
- 枚举用于状态机/错误码；`typedef enum` 显式类型。
- 指针转换显式且注意对齐（`(uintptr_t)&x & 0x3` 检查）。

## 3. 防御性编程模式

```c
/* 防御性模式：入参校验 + 边界检查 + 返回值检查 */
bool adc_read_mv(AdcDev *dev, uint16_t *out_mv) {
    if (dev == NULL || out_mv == NULL) {        // 空指针
        return false;
    }
    if (dev->channel >= dev->max_channels) {    // 越界
        return false;
    }
    uint32_t raw = read_adc_raw(dev->channel);
    if (raw > dev->full_scale) {                // 数据合法性
        return false;
    }
    *out_mv = (uint16_t)((raw * dev->vref_mv) / dev->full_scale);
    return true;
}
```

要点：入参校验、边界检查、返回值检查、不做假设（"调用者不会传错"不可靠）。

## 4. 函数与文件组织

- 每函数 ≤ 100 行、嵌套 ≤ 4 层；单一职责，一个函数只做一件事。
- `.c`/`.h` 成对；头文件职责单一、防循环依赖（`#ifndef` include guard 或 `#pragma once`）。
- 头文件里只放接口声明与常量，实现放 .c；导出符号加模块前缀（`uart_`、`i2c_`）。
- 注释说明"为什么"而不是"是什么"；API 注释写明入参/出参/错误码。

## 5. 中断与并发安全

- ISR 内：只置标志/通知；不 printf、不 malloc、不调用阻塞 API（见 SKILL.md Core Rules）。
- ISR 与主循环共享变量：`volatile` + 原子访问；多字节数据用临界区/关中断保护。
- 可重入函数：避免静态局部变量累积状态。

## 6. 静态分析清单（交付前自检）

- [ ] 全部变量已初始化
- [ ] 无未使用变量/函数（编译警告为 0）
- [ ] 所有返回值已检查
- [ ] 无越界访问（数组/缓冲区）
- [ ] 无动态分配泄漏
- [ ] 指针使用前判空
- [ ] switch 无 fall-through（MISRA 禁止隐式贯穿）
- [ ] 所有路径都有 return
- [ ] `-Wall -Wextra -Werror` 通过
- [ ] cppcheck（如可用）High/Medium 级别无告警

## 7. 使用建议

- 一般嵌入式项目：至少满足 BARR-C 级别；安全关键（ASIL/医疗/航空）：必须 MISRA C:2012 全量合规 + 认证静态分析工具（PC-lint Plus、Polyspace、LDRA）。
- AI 生成代码默认按本文件规则写，交付时说明遵循的标准级别。
