# IEEE Submission — 投稿流程

> **中文说明**：IEEE 会议与期刊投稿流程差异巨大——会议走第三方系统 + PDF eXpress 认证，期刊走 ScholarOne。本文件是完整投稿手册：PDF 生成与字体嵌入、各系统操作、eCopyright、清单。

## 1. 会议 vs 期刊投稿总览

| 环节 | 会议 (Conference) | 期刊 (Journal) |
|---|---|---|
| 初稿提交 | PDF（多数会议） | PDF + LaTeX 源文件 |
| 系统 | EDAS / CMT / EasyChair / HotCRP（按会议） | ScholarOne Manuscripts |
| PDF 认证 | **IEEE PDF eXpress**（camera-ready 必需） | 不需要（ScholarOne 自带转换） |
| 源文件 | camera-ready 阶段可能要求 | 初稿即要求 |
| 版权 | IEEE eCopyright 表单（录用后） | IEEE eCopyright 表单（录用后） |

## 2. IEEE PDF eXpress（会议必备）

1. 访问 pdf-express 站点，用**会议 ID** 注册（在会议官网获取）。
2. 上传 PDF → 系统检查：**字体嵌入**、页边距、图片分辨率、页码合规等。
3. 返回结果：
   - **Pass** → 获得认证 PDF（标注 "PDF eXpress" 水印）用于上传。
   - **Fail** → 查看具体错误（最常见：字体未嵌入）。
4. 修复字体未嵌入：
   - 用官方模板 + pdflatex 重新编译（pdflatex 默认嵌入字体）。
   - 检查：`pdffonts your.pdf`（Linux/macOS）应显示全部字体为 `embedded`。
   - 不要用 Word 默认导出（字体常未嵌入）或第三方转换工具。

```bash
# 检查 PDF 字体嵌入（全部应为 embedded）
pdffonts paper.pdf
```

## 3. 会议投稿系统

| 系统 | 特点 | 注意 |
|---|---|---|
| EDAS | IEEE 会议常用 | 文件名规范严格；按系统字段填写 |
| Microsoft CMT | 学术会议常用 | 支持 LaTeX 上传 |
| EasyChair | 通用 | 关注截止时间（时区！） |
| HotCRP | 理论/CS 会议 | 匿名评审常见 |

**通用规则**：
- 初稿只要 PDF（部分系统），camera-ready 阶段需 PDF + 源文件（.tex + 图 + .bbl 等）。
- 文件名不要含作者名（匿名评审）；用系统要求命名（如 `paper123.pdf`）。
- 截止时间注意系统时区（通常 AoE 或指定 UTC）。

## 4. 期刊投稿（ScholarOne Manuscripts）

1. 注册 ScholarOne（按期刊进入）。
2. 上传：PDF + LaTeX 源文件（.tex、图、.bib 或 .bbl、样式文件）。
3. 填写元数据：标题、摘要、关键词、作者（ORCID 必填）、基金信息、推荐审稿人。
4. 部分期刊（如 IEEE Access）要求 Word/LaTeX 源文件与 PDF 内容完全一致。
5. 双盲期刊：上传**匿名版**（删除作者信息、致谢、自引、文件名元数据），单列 title page 或按系统要求。

## 5. IEEE eCopyright 表单

- 录用后完成（会议 camera-ready 前、期刊录用后）。
- 填写：文章标题、作者、出版形式（期刊/会议）、OA 选项（可选开放获取，涉及 APC）。
- 完成后获得版权确认号，提交系统时需要。

## 6. 会议 Camera-Ready 清单

- [ ] 官方模板（与初稿一致的模板版本）
- [ ] PDF eXpress 认证通过（字体嵌入）
- [ ] 页数在限制内（按 CfP）
- [ ] 无作者添加的页眉/页脚/页码
- [ ] 图片分辨率 ≥300dpi（照片）/ 600dpi（线条图）
- [ ] 参考文献完整（IEEE 风格、DOI）
- [ ] 上传源文件（如系统要求）+ 认证 PDF
- [ ] eCopyright 完成

## 7. 期刊录用前清单

- [ ] 与目标期刊 Instructions for Authors 逐项核对
- [ ] 页数限制（正文 ≤14 页等）
- [ ] 摘要 ≤250 词（各刊不同）、Index Terms 齐全
- [ ] 参考文献 IEEE 风格 + 完整（低分辨率图、不完整引文是 camera-ready 高频返工项）
- [ ] 作者简介与照片（IEEE biography + photo）按模板
- [ ] 双盲要求处理（若适用）
- [ ] 数据/第三方素材许可声明（引用数据集许可、第三方图版权）

## 8. 常见问题速查

| 问题 | 处理 |
|---|---|
| PDF eXpress 拒：字体未嵌入 | 官方模板 + pdflatex 重编；`pdffonts` 验证 |
| PDF eXpress 拒：页边距溢出 | 检查纸张 US Letter（别用 A4）；别改模板边距 |
| 会议上传不了 LaTeX | 初稿通常只要 PDF；camera-ready 才要源文件 |
| 期刊系统转换 PDF 失败 | 检查 .bib/.bbl、图片路径、特殊字符（\include 多文件问题） |
| 匿名评审泄露身份 | 删文件名作者名、致谢、自引、PDF 元数据 |
