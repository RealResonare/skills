# Elsevier — elsarticle 投稿指南

> **中文说明**：Elsevier 期刊 LaTeX 投稿速查：elsarticle/cas 文档类与选项、前置信息、参考文献样式、Editorial Manager 提交规则与常见错误修复。以目标期刊 Guide for Authors 与 Elsevier 官方 LaTeX instructions 为准。

## 1. 模板获取

- **官方**：Elsevier LaTeX instructions 页下载 `elsarticle.zip`（含 `elsarticle.cls`、三种 .bst、示例）[$TRAE_REF](https://www.elsevier.com/en-in/researcher/author/policies-and-guidelines/latex-instructions)
- **CAS 模板**：`els-cas-templates.zip`（`cas-sc.cls` 单栏 / `cas-dc.cls` 双栏）
- **Overleaf**：搜索 "Elsevier" 官方模板
- elsarticle 也随 TeX Live / MiKTeX 发行。

## 2. 三个文档类怎么选

| 文档类 | 用途 | 何时用 |
|---|---|---|
| `elsarticle.cls` (v3.4c) | 大多数 Elsevier 期刊 | Guide for Authors 未提 graphical abstract/highlights 时 |
| `cas-sc.cls` / `cas-dc.cls` | CAS（Complex Article Service）期刊 | 需要 graphical abstract、highlights、结构化作者贡献时 |
| `ecrc.sty` | CRC（Camera-Ready Copy）期刊如 Procedia | 录用后按期刊要求 |

## 3. elsarticle 文档类选项

```latex
% 初稿提交（默认最安全）：
\documentclass[preprint,12pt]{elsarticle}

% 双倍行距评审版（期刊要求时）：
\documentclass[preprint,review,12pt]{elsarticle}

% 作者-年份引用（期刊用 Harvard 样式时）：
\documentclass[preprint,12pt,authoryear]{elsarticle}

% 仅 camera-ready（不要用于初稿）：
% \documentclass[final,1p,times]{elsarticle}              % 1p 单栏
% \documentclass[final,3p,times]{elsarticle}              % 3p 单栏
% \documentclass[final,3p,times,twocolumn]{elsarticle}    % 3p 双栏
% \documentclass[final,5p,times]{elsarticle}              % 5p 双栏
```

| 选项 | 作用 | 注意 |
|---|---|---|
| `preprint` | 单栏、宽边距、Elsevier 页眉 | **初稿默认**，即使期刊双栏也用 |
| `review` | preprint + 双倍行距 | 期刊要求才用 |
| `authoryear` | natbib 切到作者-年份 | 默认是数字 [1] |
| `final` | 去掉 "Preprint submitted to" 页眉 | **仅 camera-ready** |
| `1p/3p/5p` | 模拟最终版面 | 仅 CRC 期刊或检查公式断行 |

**规则**：初稿用 `preprint`；`final`/`1p`/`3p`/`5p` 只在 camera-ready 阶段用。

## 4. 前置信息（frontmatter）

```latex
\title{论文标题\tnoteref{t1}}
\tnotetext[t1]{Title footnote（可选）}

\author[aff1]{Ann Author\corref{c1}\fnref{f1}}
\author[aff2]{Bob Author}
\ead{ann.author@institution.edu}        % 邮箱
\cortext[c1]{Corresponding author}
\fntext[f1]{Equal contribution（可选）}
\affiliation[aff1]{organization={Department, University},
                   city={City}, country={Country}}

\begin{abstract}
摘要。
\end{abstract}

\begin{keyword}
Keyword 1 \sep Keyword 2
\end{keyword}
```

- **通讯作者**：`\corref` + `\cortext` 必须成对，否则致谢作者信息丢失。
- `\ead{}` 邮箱；`\fnref` 共同贡献脚注。
- CAS 期刊：graphical abstract / highlights 按模板专用命令。

## 5. 参考文献样式

| .bst | 样式 | 场景 |
|---|---|---|
| `elsarticle-num` | 数字 [1] | 默认 |
| `elsarticle-harv` | 作者-年份 (Smith, 2020) | 期刊要求 Harvard |
| `elsarticle-num-names` | 数字 + 作者名 | 部分期刊 |

```latex
\bibliographystyle{elsarticle-num}
\bibliography{references}
```

> 中文提醒：`elsarticle-num.bst` 把 DOI/PMID/arXiv ID 当一级字段处理（自动超链接）；字段名必须小写。

## 6. Editorial Manager 提交规则（关键！）

EM 用 TeX Live 2022 编译，规则严格：

1. **扁平化**：所有文件放同一目录，**禁止子文件夹**（`figures/`、`sections/`、`bib/` 都不行）。
2. **去路径**：删掉 `\includegraphics{figures/fig1.pdf}`、`\bibliography{bib/refs}` 里的所有目录路径，甚至 `./` 前缀——EM 把所有文件放一个目录。
3. **文件命名**：无特殊字符（`+ & # %` 等）、文件名只允许一个点（`fig.1.eps` → `fig1.eps`）、避开 Windows 保留名。
4. **条目类型分类**：
   - `.tex`、`.bib`、`.bbl`、`.bst`、`.sty`、`.cls`、`.nls`、`.ilg`、`.nlo` → 一律选 **"Manuscript"**（不是 Supplemental！）
   - 图片 → **"Figure"**
   - 表格（.tex 格式）→ **"Table"**
   - `.bib` 标成 Supplemental 是 #1 投稿错误。
5. 图片格式：`.eps` 常报 "Unknown graphics extension"——转 PDF（pdflatex 原生支持）或加载 `epstopdf`。
6. 初稿多数期刊只要 PDF；要求源文件时按上述打包。

## 7. 常见错误修复

| 错误 | 修复 |
|---|---|
| 编译报错只有 error log | EM 不像 Overleaf 会硬出 PDF——先本地/Overleaf 确认 0 error |
| 图不显示 | 图片在子文件夹/路径未去除；重命名去路径 |
| 引用全是 [?] | 四步编译；.bib 以 "Manuscript" 类型上传 |
| .eps 报错 | 转 PDF 或加载 epstopdf |
| ORCID 无法解析 | 检查 `\author` 中多余空格/格式 |
| 致谢标题被跳过 | 用模板的 `\section*{Acknowledgements}` 标准命令，不要手动 `\textbf{}` |

## 8. 提交清单

- [ ] 文档类 `[preprint,12pt]`（初稿）
- [ ] 文件全部扁平化、无路径
- [ ] 文件名合规（单点、无特殊字符）
- [ ] 上传类型正确（.bib 等 = Manuscript；图 = Figure）
- [ ] 参考文献 .bst 与期刊要求一致
- [ ] 本地编译 0 error
- [ ] Graphical abstract/highlights（CAS 期刊）
- [ ] Guide for Authors 逐项核对
