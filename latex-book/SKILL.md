---
name: latex-book
description: 中文数学书籍 LaTeX 模板：创建/修改/编译 book 类书籍（含定理环境、封面、章格式）。用于"写书/教材/讲义/专著 LaTeX"类任务，模板内置无需克隆远程仓库。
---

# latex-book — 中文数学书籍 LaTeX 模板

面向"用 LaTeX 写一本书 / 教材 / 讲义 / 数学专著"类任务。模板内置在本 Skill 内（无需克隆远程仓库），基于 `book` 文档类，预置：中文支持（ctex）、数学字体与定理环境（定理/定义/引理/推论/命题/例题/注/证明/解）、三色章节样式、封面页与页眉页脚。

## 资产清单

所有路径均为**相对本 Skill 目录**（`<skill_dir>/`）。运行时解析 Skill 自身位置（脚本用 `Path(__file__)`），禁止硬编码绝对路径。

- 模板目录：`assets/template/`
- 主入口：`main.tex`
- 封面图片：`cover.png`（脚本可生成占位图，可替换）
- 初始化脚本：`scripts/init_book.py`（复制模板 + 生成占位封面）

复制 `assets/template/` 到用户目标目录后再修改，不要直接改 Skill 内的资产。

## 标准流程

1. 初始化书籍项目（必要时）：

   ```bash
   python <skill_dir>/scripts/init_book.py <target-dir>
   ```

   `--force` 覆盖已存在的模板文件；`--skip-cover` 跳过占位封面生成。默认会生成一张纯色占位 `cover.png`，保证开箱可编译。

2. 修改 `<target-dir>/main.tex` 的"用户替换区"：
   - `\title{书名}`
   - `\author{作者}`
   - `\date{\today}`（可改具体日期）
   - 如需自定义封面图：用真实图片替换 `cover.png`（模板用 `\includegraphics[width=\linewidth]{cover.png}` 铺满页宽）

3. 编写正文（在 `\mainmatter` 之后）：
   - 用 `\chapter{...}` / `\section{...}` / `\subsection{...}` / `\subsubsection{...}` 组织结构
   - 数学内容直接用 `amsmath` 环境（`equation`、`align` 等）
   - 交叉引用：`\label{...}` + `\ref{...}`；章节引用会着色高亮

4. 编译（从项目根目录，需 XeLaTeX）：

   ```bash
   xelatex -interaction=nonstopmode -file-line-error main.tex
   xelatex -interaction=nonstopmode -file-line-error main.tex
   ```

   **必须编译两遍**：第一遍生成目录/交叉引用，第二遍落地。若使用 `\frontmatter`/`\mainmatter` 后的罗马页码与正文页码，也以两遍为准。

## 定理环境速查

模板预置以下环境（编号按章，`\newtheorem{...}[theorem]{...}` 共享计数器）：

| 环境 | 标题 | 样式色 |
|---|---|---|
| `theorem` | 定理 | second（蓝灰） |
| `definition` | 定义 | main（深蓝） |
| `lemma` | 引理 | main |
| `corollary` | 推论 | main |
| `proposition` | 命题 | third（紫灰） |
| `example` | 例题 | third |
| `remark` | 注 | third |
| `proof` | 证明（可选参数换标题，如 `\begin{proof}[定理1的证明]`） | 仿宋 |
| `solution` | 解 | 楷书 |

用法示例：

```tex
\begin{theorem}[勾股定理]
直角三角形斜边的平方等于两直角边的平方和。
\end{theorem}

\begin{proof}
证明如下：$\cdots$ \qed
\end{proof}
```

另提供 `\intro{...}` 命令（右对齐小字引言段，可用于章首简介）。

## 样式说明（可自定义）

- 页面：A4，上下 25.4mm、左右 20mm；页眉章标题（楷书、structurecolor），页脚居中页码
- 章节：章首大号 "Chapter N" + 双线标题；节为框式 `§ N`；小节/subsubsection 蓝灰加粗
- 颜色变量：`winered`（链接）、`structurecolor`（结构色，默认 RGB 122,122,142）、`main`/`second`/`third`（三档标题/定理色，可改 `\definecolor`）
- 字体：正文 Palatino 风格（mathpazo + newpxtext），中文由 ctex 提供（楷书 `\kaishu`、仿宋 `\fangsong`）

## 常见问题

| 问题 | 处理 |
|---|---|
| 编译报缺字体 | 安装 `texlive-xetex`、`texlive-lang-chinese`、`fonts-noto-cjk` 等（Linux apt）；Windows 用 TeX Live 全量或 MiKTeX |
| `cover.png` 找不到 | 初始化脚本已生成占位图；若手工复制模板，需自行提供 cover.png 或删除 `\includegraphics` 行 |
| 目录/引用显示为 `??` | 重新编译两遍（见标准流程第 4 步） |
| 编译在 `?` 提示符卡住 | 退出 `X`，改用 `-interaction=nonstopmode` |
| 需要 16:9 幻灯片 | 这是书籍模板，不适用——见 `bupt-beamer-slides` Skill |

## 验证

每次修改后至少编译两遍并确认：
- `main.pdf` 生成于项目根目录
- 无 `LaTeX Error` / `Package ... Error` / `Undefined control sequence`
- 目录（TOC）页码正确、无 `??` 交叉引用
- 正文文本无溢出（数学公式过长时用 `split`/`align` 换行）
