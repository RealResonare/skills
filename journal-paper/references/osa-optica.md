# OSA / Optica — 期刊论文格式

> **中文说明**：Optica 出版集团（原 OSA）期刊使用官方 Universal Manuscript Template（`optica-article` 文档类）。本文档为格式速查：模板获取、期刊选择、作者/摘要/引用规则、编译与 .tar 提交。具体以 Optica 官网当前 Author Guidelines 为准。

## 1. 模板获取

- **Overleaf 官方模板**："Universal manuscript template for Optica Publishing Group journals"（`optica-article.cls`）[$TRAE_REF](https://nl.overleaf.com/latex/templates/universal-manuscript-template-for-optica-publishing-group-journals/ybkgndgdxpzy.pdf)
- 适用期刊：Optics Express (OE)、Biomedical Optics Express (BOE)、Optical Materials Express (OME)、Optics Continuum、Applied Optics、JOSA A/B、Optics Letters、Optica、Photonics Research 等。

## 2. 文档类与期刊选择

```latex
\documentclass{optica-article}
\journal{oe}   % 选择目标期刊
\articletype{Research Article}   % 非 Express 期刊需要（OE/BOE/OME/OPTCON 不需要）
\usepackage{lineno}
\linenumbers    % 行号（投稿需要）
```

| `\journal{}` 值 | 期刊 |
|---|---|
| `oe` | Optics Express |
| `boe` | Biomedical Optics Express |
| `ome` | Optical Materials Express |
| `optcon` | Optics Continuum |
| `opticajournal` | Applied Optics、JOSA A/B、Optics Letters、Optica、Photonics Research 等 |

> 中文提醒：Express 期刊（OE/BOE/OME/OPTCON）基于单栏 Express 版面，模板可精确估算页数；双栏期刊（Applied Optics 等）估算页数时把模板页数 × 60%。

## 3. 作者与单位格式

```latex
\author{Author One\authormark{1}, Author Two\authormark{2,*}, and Author Three\authormark{2,3}}
\address{\authormark{1}Department, Institution, City, Country\\
         \authormark{2}Department, Institution, City, Country}
\email{\authormark{*}author@institution.edu}   % 通讯作者邮箱（必填）
```

- **必须指定唯一通讯作者**（`*` 标注）。
- 共同贡献：`\authormark{1,$\dag$}` + `\address` 中注明 "The authors contributed equally to this work."

## 4. 摘要与正文规则

- **摘要 ~100 词**（无编号、无项目符号、无列表）。
- 摘要中引用他文必须写出完整出处而非编号：`[Opt. Express 22, 1234 (2014)]`，并在正文中单独引用。
- **正文第一个引用的参考文献必须是 [1]**。
- 正文中第一处引用从 [1] 开始连续编号。
- 手稿上**不要加版权/许可声明**（编辑部在录用后统一处理）。

## 5. 参考文献（严格格式）

- **脚注不用于文献**（期刊不用页脚注）。
- 参考文献要求：**全部作者、完整标题、起止页码**。
- 示例：`K. Gallo and G. Assanto, "All-optical diode based on second-harmonic generation in an asymmetric waveguide," J. Opt. Soc. Am. B 16, 267–269 (1999).`
- 使用模板提供的 `thebibliography` 或 BibTeX（模板含 `ref.bib` 示例）。

## 6. 编译

```bash
pdflatex main.tex
bibtex main        # 如用 BibTeX
pdflatex main.tex
pdflatex main.tex
```

- **单一 .tex 文件**：Optica 要求只含一个 .tex（`\include`/多文件将无法编译）[$TRAE_REF](https://www.cnblogs.com/quantum-condensed-matter-physics/p/19375416)。
- 尽量用标准 LaTeX 命令，避免自定义宏。
- 图片推荐 PDF 格式（模板图片即 PDF）。

## 7. 提交（关键：.tar）

- **必须压缩为 `.tar`（不能 .zip）**——Optica 投稿系统用 Overleaf 编译，只认 .tar。
- 提交前务必用 Overleaf 官方模板编译一遍确认无报错（本地编译通过不代表官方系统能编译；bib 中难以发现的小空格常导致官方编译失败）。
- 需要注册 Optica 账户，填写 ORCID。

## 8. 常见问题

| 问题 | 处理 |
|---|---|
| 官方系统编译失败 | 本地用 Overleaf 官方模板复现，检查 bib 空格等隐藏问题 |
| 压缩包用 zip 被拒 | 改用 `.tar` |
| 多 .tex 文件 | 合并为单文件 |
| 摘要超长/带编号 | 压到 ~100 词，去编号列表 |
| 引用格式不符 | 全部作者 + 完整标题 + 起止页码 |
