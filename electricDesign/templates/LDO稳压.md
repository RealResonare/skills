# LDO 稳压

## 适用场景
低压差线性稳压:给数字/模拟电路提供干净稳定的电源轨。注意效率与功耗:压差 × 电流 = 发热;大压差大电流请改用 DC-DC。

## 电路结构
```
Vin ──┬── LDO_IN ──── LDO_OUT ──┬── Vout
      │      │        │         │
     Cin    GND      Cout     负载
      │                         │
     GND                       GND
(输入/输出各加去耦电容;某些 LDO 需要 BYPASS/EN/ADJ 引脚)
```

## 关键公式
- 输出:Vout = VREF × (1 + R1/R2)(可调型,通常 VREF=1.2V 或 0.6V);固定输出型直接用
- 功耗:P = (Vin − Vout) × Iout,是发热的唯一来源
- 压差(Dropout):Vin 须 > Vout + Vdropout(典型 100mV~600mV,查规格书)
- 纹波抑制:PSRR 典型 60~90dB(100Hz~1MHz 内不同)
- 静态电流 Iq:电池场景关心,选低 Iq 型号

## 参数计算步骤
1. 确定 Vout、Iout_max、Vin 范围。
2. 验证压差:Vin_min − Vdropout > Vout,否则输出跌落。
3. 算最大功耗 P_max = (Vin_max − Vout) × Iout_max,选封装/散热(如 SOT-23 约 0.3~0.5W,SOT-223 约 1W,留 50% 裕量)。
4. 选输入/输出电容:按规格书要求(常用 Cin 1µF、Cout 1~10µF,X7R/X5R),ESR 范围要符合稳定性要求。

## 自检要点
- **发热**:P_max 超过封装能力必须降额、加散热或换 DC-DC。
- **最小负载**:部分 LDO 需要最小输出电流(如 1~5mA)才稳定,轻载场景注意。
- **输出电容 ESR**:老式 LDO 对 ESR 有上下限要求,错选低 ESR 陶瓷电容可能振荡;新型 LDO(如 TPS7xxx、HT7xxx 系列)通常兼容陶瓷电容,仍以规格书为准。
- **噪声敏感**:给模拟/RF 供电选低噪声 + 高 PSRR 型号,输入输出都加大电容滤波。
- **反向电流**:Vin 掉电而 Vout 有电时电流会倒灌,精密场景加反向保护二极管。

## 示例网表(可调 LDO 简化行为模型,5V→3.3V)
```spice
* 用行为源模拟理想 LDO:Vout=3.3V,压差 0.5V
Vin vcc 0 DC 5
Rload vout 0 330   ; 10mA 负载
E1 vout 0 VALUE{IF(V(vcc)>3.8, 3.3, V(vcc)-0.5)}
C1 vcc 0 1u
C2 vout 0 10u
.op
.end
```
仿真仅供定性验证 LDO 特性;真实型号请用厂商 SPICE 模型(如 TI/ADI 官网下载 .lib)替换 E1,交付时说明。

## 常见坑
- 忽略压差:Vin=3.3V 想输出 3.3V,实际只有 3.3−Vdropout。
- 忽略散热:5V→3.3V @ 500mA = 0.85W,SOT-23 直接过热保护。
- 输入输出电容接反/漏接 → 振荡或纹波变差。
