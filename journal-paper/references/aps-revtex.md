# APS — REVTeX 4.2 论文格式

> **中文说明**：APS（美国物理学会）期刊投稿使用官方 REVTeX 4.2 宏包。本文档为格式速查：文档类选项、结构、参考文献、编译与提交。具体以 `journals.aps.org/revtex` 的当前 REVTeX 文档与目标期刊 Author Guidelines 为准。

## 1. 模板获取

- **官方**：https://journals.aps.org/revtex （下载 REVTeX 4.2 发行包，含 `apssamp.tex` 示例）
- **Overleaf**："RevTeX 4.2 Template and Sample"（官方模板，Overleaf 模板库可一键打开）
- 依赖：REVTeX 4.2 需要 `natbib`(≥8.31a)、`textcase`、`bm`、AMS-LaTeX；TeX Live / MiKTeX 已含。

## 2. 文档类与期刊选项

```latex
\documentclass[%
aps,          % APS 期刊统一选项（或具体期刊）
pra,          % 期刊选项：prl, pra, prb, prc, prd, pre, prx, prap, prfluids, prmaterials...
%reprint,     % 双栏（接近出版格式）
%preprint,    % 单栏（预印本格式，投稿亦可）
10pt,         % 字号
amsmath, amssymb,
]{revtex4-2}
```

| 期刊 | 选项 | 备注 |
|---|---|---|
| Physical Review Letters | `prl` | 4 页正文约束 |
| Physical Review A/B/C/D/E | `pra`/`prb`/... | |
| Physical Review X | `prx` | |
| Physical Review Applied | `prap` | |
| Reviews of Modern Physics | `rmp` | |
| 通用物理评论 | `physrev` | 统一选项 |

**纸张**：US Letter（APS 要求）。**布局**：reprint 双栏 / preprint 单栏，投稿两皆可。

## 3. 文稿结构（front matter）

```latex
\title{The title should simply and concisely convey the main findings}
\author{Ann Author}
\affiliation{Department, Institution, City, State, Country}
\author{Second Author\email{Second.Author@institution.edu}}  % 通讯作者
\affiliation{...}
\date{\today}
\begin{abstract}
摘要：简明总结。APS 未设硬性字数限制，但应精炼；避免在摘要中放参考文献（如必须引用，按 REVTeX 允许的写法处理）。
\end{abstract}
\maketitle
```

- **作者/单位**：`\affiliation{}` 声明完成工作所在机构（部门、机构、城市、州、国家）。
- **PACS / 关键词**：`\pacs{}` 与 `\keywords{}`（视期刊要求）。
- **合作组**：`\collaboration{}`。

## 4. 正文与引用

- 章节：`\section{}`（一级标题自动大写）、`\subsection{}`、`\subsubsection{}`。
- 跨栏宽内容：`\begin{widetext}...\end{widetext}`（宽表格/公式）。
- 引用：`\cite{key}`（数字引用，natbib）；`\onlinecite{key}` 用于行内非上标。
- 合并引用：`\cite{key1,key2}`；同一条目多文献用 `*key` 语法合并（REVTeX 特色）。
- BibTeX 样式：APS 用 `apsrev4-2.bst`（BibTeX）或 `apsrev4-2`（biblatex 不默认支持，按文档处理）。

## 5. 编译流程

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

（或 `latex` + `dvipdf`；REVTeX 示例文档默认 pdflatex 即可。）

## 6. 提交

- 上传源文件（.tex + 图 + .bib）+ 编译的 PDF。
- PRL 等有页数约束的期刊：正文（含图注）需在限制内；补充材料（Supplemental Material）单独上传——注意部分期刊对补充材料有政策（如 PR 系列允许但需单独文件）。
- 投稿系统：PRX 等用 APS 投稿系统（Editorial Manager）；按期刊页面指引。

## 7. 常见问题

| 问题 | 处理 |
|---|---|
| `natbib` 版本过旧 | 更新 TeX Live / MiKTeX |
| 参考文献显示问号 | 跑完整四步编译（含 bibtex） |
| 需要 16:9 幻灯片 | 这是论文格式，不适用——用 `bupt-beamer-slides` |
| 投稿格式问题 | 以 journals.aps.org 当前 Author Guidelines 为准 |
