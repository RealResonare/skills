#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_sim.py — 用 ngspice 运行 SPICE 网表并输出关键结果。

用法:
    python run_sim.py circuit.cir [--plot wave.png] [--probe n1,n2]

支持分析:
  .op   打印全部节点电压/支路电流
  .dc   打印扫描变量范围与各探针 min/max
  .tran 打印各探针 max/min/终值;--plot 输出时间波形 PNG
  .ac   打印各探针的幅值/相位,寻找 -3dB 点;--plot 输出 Bode PNG

ngspice 查找顺序:
  1. 环境变量 NGSPICE(指向 ngspice 可执行文件)
  2. PATH 中的 ngspice / ngspice.exe
  3. 常见安装路径(Windows): C:\\Spice64\\bin\\ngspice.exe 等

找不到 ngspice 时:
  - Windows: 从 https://ngspice.sourceforge.io/download.html 下载安装,
    或 `winget install ngspice`;装好后把可执行文件放入 PATH,或设置环境变量 NGSPICE。
  - 也可走 PySpice 路线: pip install pyspice 后运行 pyspice-post-installation
    下载 ngspice 共享库,再用本脚本的 --shared 模式(实验性,需 PySpice 已就绪)。
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# ngspice 查找
# ---------------------------------------------------------------------------

def find_ngspice():
    env = os.environ.get("NGSPICE")
    if env and Path(env).is_file():
        return str(env)
    exe = "ngspice.exe" if sys.platform == "win32" else "ngspice"
    p = shutil.which(exe) or shutil.which("ngspice")
    if p:
        return p
    if sys.platform == "win32":
        for c in [
            r"C:\Spice64\bin\ngspice.exe",
            r"C:\Program Files\ngspice\bin\ngspice.exe",
            str(Path.home() / "ngspice" / "bin" / "ngspice.exe"),
            str(Path(os.environ.get("LOCALAPPDATA", "")) / "ngspice" / "bin" / "ngspice.exe"),
        ]:
            if Path(c).is_file():
                return c
    return None


def ngspice_install_hint():
    return (
        "未找到 ngspice。请任选一种方式安装:\n"
        "  1. Windows: https://ngspice.sourceforge.io/download.html 下载安装,"
        "并把 ngspice.exe 所在目录加入 PATH;\n"
        "  2. 或执行: winget install ngspice\n"
        "  3. 或设置环境变量 NGSPICE 指向 ngspice 可执行文件路径。\n"
        "装好后重跑本脚本即可。"
    )


def probe_ngspice(ng):
    try:
        r = subprocess.run([ng, "--version"], capture_output=True, text=True, timeout=30)
        return r.returncode == 0
    except Exception:
        return False


# ---------------------------------------------------------------------------
# 运行网表
# ---------------------------------------------------------------------------

def prepare_netlist(cir_path):
    """复制网表到临时目录,追加 .control 块:显式执行分析并输出 ASCII raw。

    ngspice 规则:网表含 .control 块时,分析指令(.tran/.ac/...)不会自动执行,
    必须在 control 块中显式调用。这里把网表里的分析行转为 control 命令。
    """
    src = Path(cir_path).resolve()
    if not src.is_file():
        raise FileNotFoundError(f"网表文件不存在: {src}")
    text = src.read_text(encoding="utf-8", errors="replace")
    if re.search(r"^\s*\.control\b", text, re.M):
        return src, text  # 已有 control 块,直接用原文件
    # 收集分析指令(.tran/.ac/.op/.dc),去掉行首点号即为 control 命令
    analyses = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("."):
            continue
        m = re.match(r"\.(tran|ac|op|dc)(\s.*)?$", s, re.I)
        if m:
            cmd = m.group(1).lower() + (m.group(2) or "")
            analyses.append(cmd)
    if not analyses:
        raise ValueError(
            "网表中未找到 .tran/.ac/.op/.dc 分析指令,无法生成仿真数据。"
        )
    body = "\n".join(analyses)
    ctrl = (
        "\n.control\n"
        "set filetype=ascii\n"
        "set nomoremode\n"
        f"{body}\n"
        "write out.raw\n"
        "quit\n"
        ".endc\n"
    )
    tmpdir = tempfile.mkdtemp(prefix="ed_sim_")
    work = Path(tmpdir) / "circuit.cir"
    work.write_text(text + ctrl, encoding="utf-8")
    return work, text


def run_ngspice(ng, netlist_path):
    log_path = netlist_path.with_name("ngspice.log")
    try:
        r = subprocess.run(
            [ng, "-b", "-o", str(log_path), str(netlist_path)],
            capture_output=True, text=True, timeout=600,
            cwd=str(netlist_path.parent),  # 让 write out.raw 落在网表目录
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("ngspice 运行超时(600s),网表可能有收敛问题或无限仿真。")
    return r, log_path


# ---------------------------------------------------------------------------
# ASCII raw 解析
# ---------------------------------------------------------------------------

def parse_raw_ascii(text):
    plots = []
    lines = text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        if not lines[i].startswith("Plotname:"):
            i += 1
            continue
        plot = {"plotname": lines[i].split(":", 1)[1].strip()}
        i += 1
        flags = ""
        if i < n and lines[i].startswith("Flags:"):
            flags = lines[i].split(":", 1)[1].strip()
            plot["flags"] = flags
            i += 1
        nvar = 0
        if i < n and lines[i].startswith("No. Variables:"):
            nvar = int(lines[i].split(":")[1].strip())
            plot["nvar"] = nvar
            i += 1
        if i < n and lines[i].startswith("No. Points:"):
            plot["npts"] = int(lines[i].split(":")[1].strip())
            i += 1
        while i < n and not lines[i].startswith("Variables:"):
            i += 1
        i += 1
        vars_ = []
        for _ in range(nvar):
            if i >= n:
                break
            parts = re.split(r"[\s\t]+", lines[i].strip())
            if len(parts) >= 2:
                try:
                    idx = int(parts[0])
                except ValueError:
                    idx = len(vars_)
                vars_.append({"index": idx, "name": parts[1],
                              "type": parts[2] if len(parts) > 2 else ""})
            i += 1
        while i < n and not lines[i].startswith("Values:"):
            i += 1
        i += 1
        complex_ = flags.startswith("complex")
        ncol = nvar * 2 if complex_ else nvar
        values = []
        row = []
        while i < n:
            line = lines[i].strip()
            if not line:  # ngspice 数据点之间有空行,跳过
                i += 1
                continue
            if line.startswith("Plotname:"):
                break
            # ngspice ASCII raw: 每个数值单独一行(real),或每行"实部,虚部"(complex);
            # 仅该数据点的第一个数值行首带索引(如 " 0 1.23e+00")。
            # 索引是纯整数,数据值总是科学计数法,据此区分。
            idx = None
            vals = []
            for tok in re.split(r"[\s,]+", line):
                if not tok:
                    continue
                if idx is None and re.fullmatch(r"\d+", tok):
                    idx = int(tok)
                    continue
                try:
                    vals.append(float(tok))
                except ValueError:
                    vals = []
                    break
            if not vals:
                break
            if idx is not None:
                row = []
            row.extend(vals)
            if len(row) == ncol:
                values.append(row)
                row = []
            i += 1
        plot["vars"] = vars_
        plot["values"] = values
        plot["complex"] = complex_
        plots.append(plot)
    return plots


def find_raw_files(work_dir):
    return sorted(Path(work_dir).glob("*.raw"))


# ---------------------------------------------------------------------------
# 结果汇总
# ---------------------------------------------------------------------------

def pick_probes(vars_, probes):
    wanted = []
    for v in vars_:
        name = v["name"].lower()
        if name == "time" or name == "frequency":
            continue
        base = re.sub(r"^[vi]\(", "", name).rstrip(")")
        if not probes or base in probes or name in probes:
            wanted.append(v)
    return wanted


def fmt(x):
    return f"{x:.6g}"


def summarize_plot(plot, probes):
    """按分析类型输出摘要,返回 (文本行列表, 供绘图的数据 dict)。"""
    vars_ = plot["vars"]
    values = plot["values"]
    complex_ = plot["complex"]
    lines = []
    data = {"vars": vars_, "values": values, "complex": complex_}
    if not values:
        return lines, data
    pname = plot["plotname"].lower()
    sel = pick_probes(vars_, probes)
    names = [v["name"] for v in vars_]

    if "operating point" in pname:
        row = values[0]
        units = {"voltage": "V", "current": "A", "time": "s", "frequency": "Hz"}
        lines.append("工作点(Operating Point):")
        for j, v in enumerate(vars_):
            if j < len(row):
                u = units.get(v["type"], "")
                lines.append(f"  {v['name']:<12} = {fmt(row[j]):>12} {u}")
        return lines, data

    if "transient" in pname:
        idx_time = next((i for i, v in enumerate(vars_) if v["name"].lower() == "time"), None)
        lines.append("瞬态分析(Transient):")
        t0 = values[0][idx_time] if idx_time is not None else 0.0
        t1 = values[-1][idx_time] if idx_time is not None else 0.0
        for v in sel:
            j = v["index"]
            col = [row[j] for row in values]
            lines.append(
                f"  {v['name']:<12} min={fmt(min(col)):>10}  "
                f"max={fmt(max(col)):>10}  终值={fmt(col[-1]):>10}"
            )
        if idx_time is not None:
            lines.append(f"  时间范围: {fmt(t0)} ~ {fmt(t1)} s,共 {len(values)} 点")
        return lines, data

    if pname.startswith("ac") or "ac analysis" in pname:  # 注意不能只查 "ac" 子串,会误中 characteristic
        idx_freq = next((i for i, v in enumerate(vars_) if v["name"].lower() == "frequency"), None)
        lines.append("交流分析(AC):")
        for v in sel:
            j = v["index"]
            col = []
            for row in values:
                if complex_:
                    re_, im_ = row[2 * j], row[2 * j + 1]
                    col.append((abs(complex(re_, im_)), math_deg(im_, re_)))
                else:
                    col.append((abs(row[j]), 0.0))
            mags = [c[0] for c in col]
            i_max = max(range(len(mags)), key=lambda k: mags[k])
            fmax = values[i_max][idx_freq] if idx_freq is not None else i_max
            db_max = 20 * math_log10(mags[i_max]) if mags[i_max] > 0 else -300
            # -3dB 点:从峰值往下 3dB
            target = mags[i_max] / math_sqrt(2)
            i3 = None
            for k in range(i_max, len(mags)):
                if mags[k] <= target:
                    i3 = k
                    break
            if i3 is None and mags:
                i3 = len(mags) - 1
            line = (f"  {v['name']:<12} 峰值 {db_max:7.2f} dB @ {fmt(fmax)} Hz")
            if i3 is not None and idx_freq is not None:
                line += f"  | -3dB 点 ≈ {fmt(values[i3][idx_freq])} Hz"
            lines.append(line)
        return lines, data

    if "dc transfer" in pname or "dc" in pname:
        lines.append("直流扫描(DC):")
        for v in sel:
            j = v["index"]
            col = [row[j] for row in values]
            lines.append(
                f"  {v['name']:<12} min={fmt(min(col)):>10}  max={fmt(max(col)):>10}"
            )
        return lines, data

    lines.append(f"分析: {plot['plotname']}({len(values)} 点,未识别类型,原始数据见 raw 文件)")
    return lines, data


# 简单数学别名,避免顶部 import 混乱
from math import atan2, log10, sqrt as math_sqrt

def math_deg(im, re_):
    return atan2(im, re_) * 180.0 / 3.141592653589793

def math_log10(x):
    return log10(x) if x > 0 else -300.0


# ---------------------------------------------------------------------------
# 绘图
# ---------------------------------------------------------------------------

def plot_results(plot, out_png, probes):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    vars_ = plot["vars"]
    values = plot["values"]
    if not values:
        return
    pname = plot["plotname"].lower()
    sel = pick_probes(vars_, probes)
    if not sel:
        sel = [v for v in vars_ if v["name"].lower() not in ("time", "frequency")]

    if "transient" in pname:
        idx_time = next((i for i, v in enumerate(vars_) if v["name"].lower() == "time"), None)
        if idx_time is None:
            return
        t = [row[idx_time] for row in values]
        fig, ax = plt.subplots(figsize=(9, 5))
        for v in sel:
            j = v["index"]
            ax.plot(t, [row[j] for row in values], label=v["name"])
        ax.set_xlabel("time (s)")
        ax.set_ylabel("voltage (V) / current (A)")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(out_png, dpi=150)
        plt.close(fig)

    elif "ac" in pname:
        idx_freq = next((i for i, v in enumerate(vars_) if v["name"].lower() == "frequency"), None)
        if idx_freq is None:
            return
        f = [row[idx_freq] for row in values]
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
        for v in sel:
            j = v["index"]
            mag, ph = [], []
            for row in values:
                if plot["complex"]:
                    re_, im_ = row[2 * j], row[2 * j + 1]
                    mag.append(abs(complex(re_, im_)))
                    ph.append(atan2(im_, re_) * 180.0 / 3.141592653589793)
                else:
                    mag.append(abs(row[j]))
                    ph.append(0.0)
            ax1.loglog(f, mag, label=v["name"])
            ax2.semilogx(f, ph, label=v["name"])
        ax1.set_ylabel("magnitude")
        ax1.grid(True, which="both", alpha=0.3)
        ax1.legend()
        ax2.set_ylabel("phase (deg)")
        ax2.set_xlabel("frequency (Hz)")
        ax2.grid(True, which="both", alpha=0.3)
        fig.tight_layout()
        fig.savefig(out_png, dpi=150)
        plt.close(fig)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="用 ngspice 跑 SPICE 网表并输出关键结果")
    ap.add_argument("cir", help="SPICE 网表文件 (.cir)")
    ap.add_argument("--plot", default=None, help="输出波形 PNG 路径")
    ap.add_argument("--probe", default=None, help="要关注的节点,逗号分隔,如 out,in")
    ap.add_argument("--shared", action="store_true",
                    help="用 PySpice 的 ngspice 共享库模式(实验性)")
    args = ap.parse_args()

    ng = find_ngspice()
    if not ng:
        print(ngspice_install_hint(), file=sys.stderr)
        sys.exit(2)

    probes = [p.strip().lower() for p in args.probe.split(",")] if args.probe else None

    if args.shared:
        print("--shared 模式需要 PySpice 已安装且 ngspice 共享库就绪;"
              "当前版本建议直接用 ngspice 可执行文件模式。", file=sys.stderr)
        sys.exit(3)

    work, _ = prepare_netlist(args.cir)
    work_dir = work.parent
    r, log_path = run_ngspice(ng, work)

    raw_files = find_raw_files(work_dir)
    if not raw_files:
        log_text = log_path.read_text(encoding="utf-8", errors="replace")
        print("仿真未产生数据。ngspice 日志(最后 40 行):", file=sys.stderr)
        print("\n".join(log_text.splitlines()[-40:]), file=sys.stderr)
        sys.exit(1)

    any_error = False
    for raw in raw_files:
        text = raw.read_text(encoding="utf-8", errors="replace")
        plots = parse_raw_ascii(text)
        for plot in plots:
            lines, data = summarize_plot(plot, probes)
            print("\n".join(lines))
            if args.plot and plot["values"]:
                plot_results(plot, args.plot, probes)
                print(f"\n波形图已保存: {args.plot}")

    if r.returncode != 0:
        print(f"\n注意: ngspice 退出码 {r.returncode},可能存在模型/语法警告。"
              f"完整日志: {log_path}", file=sys.stderr)
        any_error = True

    if not any_error:
        shutil.rmtree(work_dir, ignore_errors=True)  # 成功时清理临时目录
    else:
        print(f"\n临时目录已保留,便于排查: {work_dir}", file=sys.stderr)

    sys.exit(1 if any_error else 0)


if __name__ == "__main__":
    main()
