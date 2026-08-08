# IEEE Format — IEEEtran 格式速查

> **中文说明**：本文件是 IEEEtran 文档类的格式速查：模式与选项、作者块、摘要/索引词、图表公式、参考文献。IEEEtran 由 Michael Shell 编写（开源，CTAN 发布）。正式投稿以目标期刊/会议的 Instructions for Authors / Call for Papers 为准。

## 1. 模板获取（官方路径）

| 路径 | 说明 |
|---|---|
| **IEEE Template Selector** | `template-selector.ieee.org`——按期刊精确匹配模板（部分期刊有定制模板，如 Photonics、Computer Society） |
| **IEEE Author Center** | `journals.ieeeauthorcenter.ieee.org`——官方模板包（IEEEtran.cls + IEEEtran.bst + 示例） |
| **Overleaf** | 搜索 "IEEE" 官方模板，一键打开 |
| **CTAN** | `ctan.org/pkg/ieeetran`——开源宏包 + IEEEtran_HOWTO.pdf 文档 |

**禁止**：第三方论坛/网盘下载的"山寨"模板（PDF eXpress 会拒收）。

## 2. 文档类五大模式（IEEEtran）

```latex
\documentclass[journal]{IEEEtran}      % 期刊（Transactions/Letters/Access）
\documentclass[conference]{IEEEtran}   % 会议
\documentclass[9pt,technote]{IEEEtran} % 通信/短论文（correspondence）
\documentclass[journal,peerreview]{IEEEtran}      % 双盲评审（单栏封面页）
\documentclass[journal,peerreviewca]{IEEEtran}    % 双盲评审（带"作者确认"行）
```

| 模式 | 布局 | 用途 |
|---|---|---|
| `journal` | 双栏 | IEEE 期刊（10pt Times、US Letter） |
| `conference` | 双栏 | IEEE 会议 |
| `technote` | 双栏 | 通信/短论文（9pt） |
| `peerreview` | 单栏封面 + 正文 | 匿名评审（标题重复在正文页） |
| `peerreviewca` | 同上 + 作者确认行 | 匿名评审（部分期刊） |

**常用辅助选项**：`draft`（大行距、图不显示）、`draftcls`（大行距、图正常）、`draftclsnofoot`（无 DRAFT 页脚）、`onecolumn`（初稿用）。

**关键区别**：会议模板**禁止作者添加页眉/页脚/页码**（出版时统一加会议名与版号）；期刊首页含期刊出版标记。纸张默认 US Letter（8.5×11in），除非征稿启事明确允许 A4。

## 3. 期刊与会议差异速查

| 维度 | 会议 (conference) | 期刊 (journal) |
|---|---|---|
| 作者信息 | 并列/网格排列于标题下方 | 首页左下角脚注区（机构+基金） |
| 页眉页脚 | 禁止自定义 | 投稿阶段含期刊标记 |
| 页数限制 | 按 CfP（典型 4–8 页） | 正文常 ≤14 页（各刊不同） |
| 匿名评审 | 按 CfP（很多会议双盲） | peerreview 选项或单独盲稿 |
| 投稿系统 | EDAS/CMT/EasyChair/HotCRP | ScholarOne Manuscripts |
| PDF 认证 | **IEEE PDF eXpress 必需**（camera-ready） | 不需要（ScholarOne 自带 PDF 生成） |

## 4. 作者块（期刊）

```latex
\author{Ann Author,~\IEEEmembership{Senior Member,~IEEE,}
        and Bob Author,~\IEEEmembership{Member,~IEEE}%
\thanks{Manuscript received ...; revised ... (对应期刊格式).}%
\thanks{This work was supported in part by ... (基金).}%
\thanks{Ann Author is with the Department of ..., University ..., City, Country (e-mail: ...).}%
\thanks{Bob Author is with ... (e-mail: ...).}}

% 会议作者块：
\author{\IEEEauthorblockN{Ann Author and Bob Author}
\IEEEauthorblockA{\textit{Department of ..., University of ...}\\
City, Country\\
Email: \{ann, bob\}@institution.edu}}
```

- 期刊：`\IEEEmembership{}` 会员级别 + `\thanks{}` 脚注（收稿/修订日期、基金、作者单位、邮箱）。
- 会议：`\IEEEauthorblockN`（姓名）+ `\IEEEauthorblockA`（单位+邮箱）。
- **期刊投稿要求所有作者提供 ORCID**；双盲评审时删除作者身份信息（文件名元数据、致谢、自引）。

## 5. 摘要与索引词

```latex
\begin{abstract}
摘要：简明概述问题、方法、结果与意义。期刊摘要通常 ≤250 词（各刊不同）。
\end{abstract}

\begin{IEEEkeywords}
Index Terms, 索引词, 4–6 个, 用逗号分隔, 首字母大写
\end{IEEEkeywords}
```

## 6. 正文、图表、公式

- 章节：`\section{}` / `\subsection{}` / `\subsubsection{}`；编号自动罗马数字（I, II, ...）。
- 图：`figure` 环境 + `\includegraphics`；图表文字用 Times（默认）；跨栏大图用 `figure*`。
- 表：`table` 环境 + 三线式（`\hline`）；跨栏用 `table*`。
- 公式：`equation` 环境编号连续；引用 `(\ref{eq:...})`；变量斜体、单位正体。
- **符号一致性**：一个符号一个含义贯穿全文（IEEE 社区强调符号表/算法伪代码与图注文字一致）。

## 7. 参考文献（IEEE 数字引用）

- 格式：`IEEEtran.bst`（BibTeX）；正文 `\cite{key}`，**首个引用必须是 [1]**。
- IEEE 引用风格（示例）：

```bibtex
@article{key,
  author  = {A. Author and B. Author},
  title   = {Title of the paper},
  journal = {IEEE Trans. Inf. Theory},
  volume  = {60},
  number  = {1},
  pages   = {100--110},
  year    = {2014}
}
```

- 期刊缩写用 IEEE 标准缩写（如 IEEE Trans. Inf. Theory）；作者名首字母+姓；会议论文写 `in Proc. ...`；arXiv 预印本按 IEEE 政策标注。
- 编译：`pdflatex → bibtex → pdflatex → pdflatex`。

## 8. 页数与纸张

- 正文页数限制：期刊常 ≤14 页（参考文献/作者简介/附录是否计入按刊）；会议按 CfP。
- **纸张：US Letter**（避免 A4 导致版心漂移，除非目标期刊/会议明确允许）。
- 不要擅自改 IEEEtran 的页边距/字号（`geometry` 等）；期刊有定制模板时用定制模板。

## 9. 常见问题

| 问题 | 处理 |
|---|---|
| 用会议模板投期刊（或反之） | 换 `journal`/`conference` 选项（最常导致 desk reject） |
| PDF eXpress 拒收 | 99% 是字体未嵌入；用官方模板 + pdflatex 重新生成 |
| 页码/页眉在会议稿上 | 删除——会议稿禁止作者添加 |
| 参考文献全是问号 | 跑完整四步编译 |
| 期刊要求单栏双倍行距初稿 | `\documentclass[journal,draftcls,onecolumn]{IEEEtran}` |
