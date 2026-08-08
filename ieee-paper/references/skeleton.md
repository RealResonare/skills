# IEEE Skeleton — 最小可编译骨架

> **中文说明**：本骨架用 `article` 类模拟 IEEE 双栏格式，用于**快速起草与内容组织**。**正式投稿必须替换为官方 IEEEtran 模板**（见 ieee-format.md §1），本骨架不保证通过 PDF eXpress 或期刊格式审查。

## 1. 期刊骨架（IEEE 风格，双栏）

```latex
\documentclass[10pt,twocolumn]{article}
\usepackage[margin=0.75in]{geometry}
\usepackage{times}           % Times 字体（IEEE 风格）
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{cite}            % 数字引用 [1]

\title{论文标题}
\author{Ann Author and Bob Author\\[1ex]
\small \textit{Department of ..., University of ..., City, Country}\\
\small \{ann, bob\}@institution.edu}

\begin{document}
\maketitle

\begin{abstract}
摘要：问题 → 方法 → 结果 → 意义。
\end{abstract}

\begin{IEEEkeywords} % 需 \usepackage{IEEEtrantools} 或自定义
Index Terms, A, B, C
\end{IEEEkeywords}

\section{Introduction}
...

\section{Method}
...

\section{Experiments}
...

\section{Conclusion}
...

\begin{thebibliography}{99}
\bibitem{ref1} A. Author and B. Author, ``Title,'' \emph{IEEE Trans. Inf. Theory}, vol.~60, no.~1, pp.~100--110, 2014.
\end{thebibliography}

\end{document}
```

> 注意：`IEEEkeywords` 环境在 article 类中不存在，需自定义或仅作为小节；正式模板用 `\begin{IEEEkeywords}`（IEEEtran 内置）。

## 2. 会议骨架（IEEE 风格）

```latex
\documentclass[10pt,twocolumn]{article}
\usepackage[margin=0.75in]{geometry}
\usepackage{times}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{cite}

\title{会议论文标题}
\author{Ann Author, Bob Author\\
\small \textit{Department of ..., University of ...}\\
\small City, Country\\[1ex]
\small Email: \{ann, bob\}@institution.edu}

\begin{document}
\maketitle

\begin{abstract}
...
\end{abstract}

\section{Introduction}
...

% ... 正文章节 ...

\begin{thebibliography}{99}
...
\end{thebibliography}

\end{document}
```

## 3. 正式投稿模板替换指引

1. 从官方路径获取 IEEEtran（Template Selector / Author Center / Overleaf / CTAN）。
2. 用官方示例（`bare_jrnl.tex` 期刊 / `bare_conf.tex` 会议）替换本骨架。
3. 迁移内容：标题/作者块 → 官方格式；`thebibliography` → `IEEEtran.bst` + BibTeX；正文章节原样复制。
4. 按目标期刊/会议要求调整：期刊加 `\IEEEmembership`/`\thanks`；会议用 `\IEEEauthorblockN/A`。
5. 编译：`pdflatex → bibtex → pdflatex → pdflatex`。

## 4. 迁移检查表

- [ ] 文档类改为 `\documentclass[journal]{IEEEtran}` 或 `[conference]`
- [ ] 作者块按模式重写（期刊脚注式 / 会议 block 式）
- [ ] 摘要/Index Terms 用 IEEEtran 环境
- [ ] 参考文献改 BibTeX + IEEEtran.bst（或保留手写 thebibliography 但按 IEEE 格式）
- [ ] 删除 article 类专属包（如 `times`、`cite` 可保留，`geometry` 边距删除用模板默认）
- [ ] 编译无 error；字体嵌入检查（`pdffonts`）
- [ ] 会议稿无自定义页眉页脚页码
