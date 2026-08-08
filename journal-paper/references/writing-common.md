# Writing Common — 跨期刊写作规范

> **中文说明**：本文件是 APS/Nature/OSA 三家共通的论文写作规范：标题/摘要/图表/公式/引用、Cover letter、LLM 使用政策。写任何期刊论文前先读对应期刊的 references 文件，再按本文档的通用规范执行。

## 1. 标题与摘要

| 期刊 | 摘要上限 | 摘要可引用？ | 结构 |
|---|---|---|---|
| APS (REVTeX) | 无硬性（精炼） | 尽量避免 | 自由（可用 description 结构化） |
| Nature 主刊 | 150 词 | ❌ 禁止 | 单段无结构 |
| Scientific Reports | 200 词 | ❌ 禁止 | 单段无结构 |
| OSA/Optica | ~100 词 | 需写出完整出处 | 无编号列表 |

**通用**：标题 ≤20 词（Nature 系硬性）、一句话说清主要发现、避免缩写与双关语；摘要"问题 → 方法 → 主要发现 → 意义"四要素，面向跨学科读者。

## 2. 图表规范

| 期刊 | 展示项上限 | 图注 |
|---|---|---|
| APS (PRL) | PRL 4 页正文约束 | 图注随图 |
| Nature 主刊 | 图+表 ≤6 | 350 词/图 |
| Scientific Reports | 图+表 ≤8 | 350 词/图 |
| OSA/Optica | 按文章类型 | 模板规定 |

**通用**：
- 每图一个独立文件（PNG/PDF/EPS 按期刊）；单个图不拆 subfigure 组合（部分系统）。
- 图注独立成段，含"图题 + 关键参数 + 引用出处"；第一次出现处引用 `Fig. 1` / `图 1`。
- 表格用 `booktabs` 三线表风格（学术惯例）；数值对齐。
- 彩色图：确认期刊是否免费彩色印刷（APS 部分期刊彩图收费政策不同）。

## 3. 公式与符号

- 全部公式用数学环境（`equation`/`align`），编号连续，正文引用 `Eq. (1)`。
- 符号在首次出现处定义；向量/矩阵用粗体（REVTeX 提供 `\bm`）。
- 数值单位用 SI；量纲一致；物理量用斜体、单位用正体。

## 4. 引用与参考文献

- 三家均用**数字引用**（非作者-年份）。
- 参考文献完整性：作者全名（OSA 要求全部作者；Nature/APS 视期刊）、完整标题、期刊缩写、卷、起止页、年份；DOI 按期刊要求。
- 引用管理：BibTeX 生成；提交前核对"正文引用顺序 = 参考文献编号顺序"（OSA 要求首引为 [1]）。
- 自引与综述引用适度；引用数据/软件按期刊政策（APS 支持 DOI 数据引用）。

## 5. Cover Letter 模板（通用）

```markdown
Dear Editor,

We are submitting our manuscript, "[Title]", for consideration as a [Article/Letter/Review] in [Journal].

[2-3 句：研究问题与背景]

[2-3 句：方法与主要发现]

[2-3 句：意义与为何适合该刊——跨学科意义、与期刊范围的契合]

We confirm this manuscript is original, has not been published elsewhere, and is not under consideration by another journal. All authors approve the submission and declare no competing interests.

Suggested reviewers: [Name, Institution, Email] × 3-5（可选）
Excluded reviewers: [Name, 理由]（可选）

Sincerely,
[Corresponding author name]
[Affiliation, Email]
```

- Nature/Scientific Reports 要求 cover letter 明确：为何适合该刊、建议/排除审稿人、是否与编辑有前期讨论。
- 推荐审稿人与投稿系统填写的审稿人保持一致。

## 6. 投稿前自检清单（通用）

- [ ] 目标期刊与文章类型确认（决定模板与限制）
- [ ] 官方模板获取并按要求填写
- [ ] 字数/页数/展示项在限制内
- [ ] 摘要符合字数与"无引用"规则
- [ ] 参考文献格式与完整性（首引 [1]，编号顺序）
- [ ] 编译全流程通过（含 bibtex），无 error
- [ ] 提交打包方式正确（OSA=.tar；Nature=.bbl）
- [ ] Cover letter、数据可用性声明（Nature 必填）、利益冲突声明齐全
- [ ] ORCID 填写；通讯作者唯一（OSA）

## 7. LLM 使用政策（重要）

- **Nature Portfolio**：LLM 不满足作者标准；若使用 LLM 辅助写作，须在 Methods（或合适位置）说明。
- **APS / OSA**：各出版方对 AI 工具使用有明确政策（通常允许辅助语言润色，但作者须对内容负责、不能列为作者）——投稿前查阅目标期刊最新政策，如实声明。

> 中文提醒：各出版方政策会更新——以投稿时目标期刊官网 Author Guidelines 为准，本 Skill 只提供通用框架。
