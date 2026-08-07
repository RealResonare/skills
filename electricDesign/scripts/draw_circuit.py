#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""draw_circuit.py — 用 schemdraw 从 DSL 文件画电路示意图。

用法:
    python draw_circuit.py circuit.elements out.png

DSL 每行一个元件(空白分隔;参数为剩余部分):
    类型 名称 起点 终点 参数

支持类型:
    V    电压源      V V1 (0,0)-(0,4) 5V
    I    电流源      I I1 (0,0)-(0,4) 1mA
    R    电阻        R R1 (0,4)-(4,4) 10k
    C    电容        C C1 (4,4)-(4,0) 100n
    L    电感        L L1 (0,4)-(4,4) 100u
    D    二极管      D D1 (4,4)-(4,0) 1N4007
    Q    NPN三极管   Q Q1 (4,2)-(4,0) 2N2222
    M    NMOS        M M1 (4,2)-(4,0) IRFZ44N
    GND  地          GND G1 (4,0)-(4,-1) 0
    WIRE 导线        WIRE W1 (0,0)-(4,0) -
    LBL  标签        LBL L1 (2,4) out

坐标网格:y 向上为正。约定:电源轨在上、地在下、信号从左到右。

依赖: pip install schemdraw  (会自带 matplotlib)
"""
import argparse
import re
import sys


def parse_point(s):
    m = re.fullmatch(r"\s*\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)\s*", s)
    if not m:
        raise ValueError(f"无法解析坐标: {s!r}(应为 (x,y) 格式)")
    return (float(m.group(1)), float(m.group(2)))


_POINT_PAIR = re.compile(
    r"\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)\s*-\s*\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)"
)


def parse_line(line):
    parts = line.split()
    if len(parts) < 4:
        raise ValueError(f"DSL 行格式错误(至少 4 段): {line!r}")
    typ = parts[0].upper()
    name = parts[1]
    m = _POINT_PAIR.fullmatch(parts[2])
    if m:
        # 合并形式: (x1,y1)-(x2,y2)  例: R R1 (0,4)-(4,4) 10k
        x1, y1, x2, y2 = (float(v) for v in m.groups())
        p1, p2 = (x1, y1), (x2, y2)
        param = " ".join(parts[3:])
    else:
        p1 = parse_point(parts[2])
        try:
            p2 = parse_point(parts[3])
            param = " ".join(parts[4:])
        except ValueError:
            # 单点元素(LBL/GND): 类型 名称 位置 参数
            p2 = p1
            param = " ".join(parts[3:])
    return typ, name, p1, p2, param


def main():
    ap = argparse.ArgumentParser(description="用 schemdraw 从 DSL 画电路示意图")
    ap.add_argument("elements", help="DSL 文件")
    ap.add_argument("out", help="输出 PNG 路径")
    args = ap.parse_args()

    try:
        import schemdraw
        import schemdraw.elements as elm
    except ImportError:
        print("缺少 schemdraw,请先执行: pip install schemdraw", file=sys.stderr)
        sys.exit(2)

    d = schemdraw.Drawing()
    with open(args.elements, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                typ, name, p1, p2, param = parse_line(line)
            except ValueError as e:
                print(f"第 {lineno} 行: {e}", file=sys.stderr)
                sys.exit(1)

            if typ == "V":
                e = elm.SourceV().at(p1).to(p2).label(param, loc="left")
            elif typ == "I":
                e = elm.SourceI().at(p1).to(p2).label(param, loc="left")
            elif typ == "R":
                e = elm.Resistor().at(p1).to(p2).label(param)
            elif typ == "C":
                e = elm.Capacitor().at(p1).to(p2).label(param)
            elif typ == "L":
                e = elm.Inductor().at(p1).to(p2).label(param)
            elif typ == "D":
                e = elm.Diode().at(p1).to(p2).label(param)
            elif typ == "Q":
                e = elm.BjtNpn().at(p1).to(p2).label(param)
            elif typ == "M":
                e = elm.NFet().at(p1).to(p2).label(param)
            elif typ == "GND":
                e = elm.Ground().at(p1)
            elif typ == "WIRE":
                e = elm.Line().at(p1).to(p2)
            elif typ == "LBL":
                d += elm.Dot().at(p1)
                d += elm.Label().at(p1).label(param)
                continue
            else:
                print(f"第 {lineno} 行: 未知类型 {typ}(支持 V I R C L D Q M GND WIRE LBL)",
                      file=sys.stderr)
                sys.exit(1)
            d += e

    d.save(args.out, dpi=150)
    print(f"示意图已保存: {args.out}")


if __name__ == "__main__":
    main()
