# ACM — acmart 投稿指南

> **中文说明**：ACM 期刊/会议 LaTeX 投稿速查：acmart 变体选择、两阶段投稿流程、TAPS 规则、CCS 分类与无障碍要求。以 authors.acm.org 官方文档与目标会议 CfP 为准。

## 1. 模板获取

- **官方**：authors.acm.org "Preparing Your Article with LaTeX"（下载 acmart 模板包 v2.18+，或 `portalparts.acm.org` 直链）[$TRAE_REF](https://authors.acm.org/proceedings/production-information/preparing-your-article-with-latex)
- **Overleaf**：搜索 "ACM" 官方模板（acm-official 标签）
- **TeX Live**：`acmart` 随发行（安装 `acmart` 宏包）
- 配套：`ACM-Reference-Format.bst`（BibTeX）或 biblatex `acmnumeric`/`acmauthoryear`

## 2. acmart 变体选择

```latex
% 会议（大多数 ACM 会议）：
\documentclass[sigconf]{acmart}
% SIGPLAN 会议（PLDI/POPL/ICFP/OOPSLA 等，唯一有专属变体的 SIG）：
\documentclass[sigplan]{acmart}
% 期刊：
\documentclass[acmsmall]{acmart}   % 大多数 ACM 期刊
% \documentclass[acmlarge]{acmart} % DGOV/DTRAP/HEALTH/IMWUT/JOCCH/TAP 等
% \documentclass[acmtog]{acmart}   % ACM TOG + SIGGRAPH 论文
```

| 变体 | 用途 |
|---|---|
| `sigconf` | 绝大多数 ACM 会议：KDD、SIGMOD、SIGCOMM、SIGIR、WWW、SOSP、CCS、CHI、UIST... |
| `sigplan` | 仅 SIGPLAN 会议（非 SIGPLAN 会议不要用） |
| `acmsmall` | 大多数 ACM 期刊 |
| `acmlarge` | 部分期刊（按期刊指引） |
| `acmtog` | ACM Transactions on Graphics |

**规则**：不确定时用 `sigconf`（会议）或查期刊指引；别用错变体（编译能过但版面细微错误，生产阶段会被标出）。

## 3. 两阶段投稿流程（ACM 独有）

### Phase 1 — 评审提交（单栏）

```latex
\documentclass[manuscript,review,anonymous]{acmart}
\setcopyright{none}   % 未完成 rights form 前
```

- `manuscript`：单栏输出（评审格式）
- `review`：加行号
- `anonymous`：双盲隐藏作者（单盲去掉此选项）
- `\setcopyright{none}`：录用前必设

### Phase 2 — Camera-ready（双栏）

```latex
\documentclass[sigconf]{acmart}
% 填 rights form 后得到的版权命令：
\setcopyright{acmlicensed}
\copyrightyear{2026}
\acmYear{2026}
\acmDOI{10.1145/xxxxxxx.xxxxxxx}
\acmConference[...]{...}{...}{...}   % 会议信息（来自 rights confirmation email）
\acmISBN{...}
```

**常见错误**：评审阶段用双栏、或 camera-ready 忘改 `\setcopyright`。

## 4. 元数据与必填项

```latex
\title{Title}
\author{Ann Author}
\affiliation{%
  \institution{University of ...}
  \department{Department of ...}
  \city{City} \country{Country}}
\email{ann@institution.edu}

% 审稿号（投稿系统给）：
% \acmSubmissionID{123-A56-BU3}

% 摘要：
\begin{abstract}...\end{abstract}

% CCS 概念（必须，用 CCS 生成器）：
\begin{CCSXML}
<ccs2012>
<concept><concept_id>10010147</concept_id><concept_desc>...</concept_desc></concept>
</ccs2012>
\end{CCSXML}
\ccsdesc[500]{...}

% 关键词：
\keywords{...}
```

- **CCS 分类码**：用 ACM CCS 生成器生成后粘贴，**必填**。
- **`\Description{}`**：每个 `\begin{figure}` 必须加（无障碍要求，TAPS 检查）:

```latex
\begin{figure}[t]
  \includegraphics[width=\columnwidth]{fig1}
  \Description{图中展示了...（对图内容的文字描述）}
  \caption{图题}
\end{figure}
```

## 5. 参考文献（ACM 数字引用）

```latex
\bibliographystyle{ACM-Reference-Format}
\bibliography{sample-bibliography}
```

- 多数 ACM 出版用数字引用；biblatex 可选 `acmnumeric`（数字）或 `acmauthoryear`。
- 编译：`pdflatex → bibtex → pdflatex → pdflatex`。

## 6. TAPS 规则（录用后生产）

TAPS（The ACM Publishing System）把 LaTeX 转成 PDF + HTML5，**会拒收不合规文件**：

1. **只允许 ACM 批准包列表内的 LaTeX 包**（acmart 已内置 amsmath/array/booktabs/caption/graphicx/booktabs 等，无需重复加载）；列表外包会被退回。
2. **不要自定义 `\newcommand`**（会转换失败或退回）。
3. 每个图 `\Description{}` 必填。
4. CCS 概念必填；rights 命令按 rights form 填写。
5. 图表文字、标题格式遵循模板（勿手动 `\textbf{}` 等覆盖）。

## 7. 投稿系统

- 会议：EasyChair / HotCRP / OpenReview 等（按会议官网）。
- 期刊：Editorial Manager 或期刊指定系统（按期刊）。
- 评审提交通常单栏 PDF（`manuscript` 模式）；录用后 camera-ready 双栏源文件进 TAPS。

## 8. 常见问题

| 问题 | 处理 |
|---|---|
| 评审稿用了双栏 | 改用 `[manuscript,review,anonymous]` 单栏 |
| camera-ready 版权标记错 | 按 rights form 填 `\setcopyright`/`\acmDOI` 等 |
| TAPS 退回：包不在列表 | 移除列表外包（如无用）或申请加入 |
| 图没有描述 | 每个 figure 加 `\Description{}` |
| 缺 CCS | 用 CCS 生成器生成 `\ccsdesc` |
| 变体选错 | 按 §2 表重选（sigconf vs acmsmall 等） |

## 9. 提交清单

- [ ] 评审稿：`[manuscript,review,anonymous]` 单栏 + `\setcopyright{none}`
- [ ] camera-ready：双栏变体 + rights 命令齐全
- [ ] CCS 概念（生成器）已插入
- [ ] 每个 figure 有 `\Description{}`
- [ ] 只用 ACM 批准包、无自定义 `\newcommand`
- [ ] 参考文献 `ACM-Reference-Format` + 四步编译
- [ ] 页数符合 CfP
