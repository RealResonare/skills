# Nature — Nature / Scientific Reports 论文格式

> **中文说明**：Nature 主刊与 Nature Portfolio（含 Scientific Reports）使用 Springer Nature 官方 LaTeX 模板。本文档为格式速查：模板获取、字数/展示项限制、结构、参考文献（.bbl 要求）、投稿政策。具体以期刊当前 Author Guidelines 为准。

## 1. 模板获取

- **Springer Nature 官方模板**：https://www.springernature.com/gp/authors/campaigns/latex-author-support（下载 .zip 或 Overleaf 打开"Springer Nature LaTeX Template"）
- **Scientific Reports**：Overleaf 模板 "Template for submissions to Scientific Reports"（`wlscirep.cls`）[$TRAE_REF](https://www.underleaf.ai/templates/nature-scientific-reports)
- 文档类：`sn-jnl.cls`（Springer Nature 通用）；Scientific Reports 可用 `wlscirep.cls` 或标准 `article` 类。

> 中文提醒：主刊 Nature 与 Scientific Reports 格式要求不同——写之前先确认目标期刊。

## 2. 字数与展示项限制

### 2.1 Nature 主刊（Article）

| 项目 | 限制 |
|---|---|
| 正文 | ~3,000 词（不含摘要/Methods/参考文献/图注） |
| 摘要 | 150 词上限，**无结构**（单段，无小标题） |
| 参考文献 | ~30 条 |
| 展示项（图+表） | 最多 6 个 |
| Methods | 参考文献之后，~3,000 词 |

### 2.2 Scientific Reports（Article）

| 项目 | 限制 |
|---|---|
| 正文 | 4,500 词上限（不含摘要/Methods/参考文献/图注） |
| 标题 | 20 词上限 |
| 摘要 | 200 词上限，无结构，**不允许引用** |
| 参考文献 | 60 条（非严格强制） |
| 展示项 | 8 个（图+表）；≤2,000 词建议 ≤4 个 |
| 图注 | 每图 350 词上限 |

## 3. 文稿结构

Nature Portfolio 推荐结构（正文）：

1. Introduction（引用文献扩展背景）
2. Results（可带小标题）
3. Discussion（不带小标题）
4. Methods（放参考文献之后，Nature 主刊）

正文之后依次：References → Acknowledgements（可选）→ Author contributions（姓名用首字母）→ **Data availability statement（必填）** → Additional Information（含 Competing Interests Statement）→ Figure legends → Tables。

**规则**：不用脚注；不提供关键词（Scientific Reports 不发布关键词）；图表数要与字数相称。

## 4. 参考文献（关键差异）

- **仅数字引用**（numerical references）。
- **投稿系统不收 `.bib` 文件**——必须附上编译生成的 **`.bbl` 文件**（作为 LaTeX 补充文件上传）[$TRAE_REF](https://www.underleaf.ai/templates/nature-scientific-reports)。
- 摘要中**不允许**引用。

## 5. 编译

```bash
pdflatex main.tex
bibtex main          # 或按模板说明
pdflatex main.tex
pdflatex main.tex
```

Scientific Reports 模板（wlscirep）默认 pdflatex 可编译；图片用 `graphicx`，每个图一个独立输入文件（避免 subfigure 组合）。

## 6. 政策要点

- **LLM 作者声明**：LLM（如 ChatGPT）不满足 Nature Portfolio 的作者标准；使用 LLM 须在 Methods（或合适位置）中说明。
- 首次投稿可将正文与图合并为单个 ≤3MB 文件；Word 优先但 LaTeX/PDF 亦可。
- 补充信息：单独一个文件（最好 PDF）。
- Cover letter 必备：通讯作者信息、适合该刊的理由、建议审稿人、希望排除的审稿人、是否与编辑有过前期讨论。

## 7. 提交

- 系统：Nature Portfolio 期刊各自投稿系统（如 mts-nature.nature.com）。
- 源文件 + 编译 PDF；**必须含 .bbl**；Snapp 系统要求 pdflatex 可编译 + .zip 压缩。
- 提交前对照期刊 "Ready to submit" checklist 核对硬性限制。

## 8. 常见问题

| 问题 | 处理 |
|---|---|
| 上传后 .bib 报错 | 上传编译生成的 .bbl（系统不收 .bib） |
| 超字数被退稿 | 按正文限制删减（摘要/参考文献/图注不计入） |
| 摘要放了引用 | 删掉，摘要禁止引用 |
| 图片找不到 | 图片与 .tex 同目录，不用子文件夹（部分系统） |
