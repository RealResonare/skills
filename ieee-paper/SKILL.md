---
name: ieee-paper
description: IEEE 论文写作 playbook：IEEEtran 模板获取与使用（期刊 Transactions/Letters + 会议双模式）、格式速查、IEEE 数字引用、PDF eXpress 与投稿流程。用于"写/改/投 IEEE 期刊或会议论文"类任务。
---

# ieee-paper — IEEE 论文写作 playbook

> **English Quick Start**
>
> This skill prepares manuscripts for **IEEE journals** (Transactions, Letters, Access) and **IEEE conferences** using the official IEEEtran LaTeX class. It covers: template acquisition (official paths only), the two document-class modes (journal vs conference), IEEE formatting rules (two-column, 10pt Times, US Letter, numbered references), and the submission workflows (PDF eXpress for conferences, ScholarOne for journals).
> Core loop: **确认目标（期刊/会议 + 文章类型） → 获取官方 IEEEtran 模板 → 按模式写作 → IEEE 格式与引用检查 → 编译 PDF（字体嵌入） → 提交**.
> Hard rules: always use the official IEEEtran template (never a modified third-party one); conference papers must NOT add headers/footers/page numbers; verify PDF via IEEE PDF eXpress for conferences; state UNVERIFIED for anything not checked against the target venue's Call for Papers / Author Guidelines.

## Purpose

This skill ensures IEEE manuscripts are formatted and submitted correctly, avoiding the two most common desk-rejection causes: wrong template variant (conference vs journal) and unembedded fonts failing PDF eXpress. It provides format cheat-sheets for both modes, reference/citation rules, and the complete submission workflows (EDAS/CMT/EasyChair for conferences; ScholarOne for journals).

> **模板说明**：IEEEtran 是 Michael Shell 编写的开源 LaTeX 类（CTAN 发布，`IEEEtran.cls` + `IEEEtran.bst`），可自由使用。由于本 Skill 无法内置该类文件（网络获取受限），提供**官方获取路径**与**符合格式的可编译骨架**；正式投稿必须使用官方模板。不要在第三方论坛下载"山寨"模板——PDF eXpress 会拒收。

## When to Invoke

Invoke whenever the user wants to:

- Write/format a manuscript for an **IEEE journal** (IEEE Transactions on ..., IEEE Letters, IEEE Access, etc.).
- Write/format a manuscript for an **IEEE conference** (ICASSP, ICRA, IROS, CVPR/IEEE-CS venues, etc.).
- Check a manuscript against IEEE format requirements, prepare submission files, or generate an IEEE-style bibliography.
- Fix IEEE submission issues (PDF eXpress rejection, font embedding, wrong template).

Do **not** invoke for APS/Nature/OSA journals (see `journal-paper`) or theses/books (see `latex-book`).

## Unified Pipeline (Mandatory Order)

| # | Step | Gate / Rule |
|---|---|---|
| 1 | **Confirm target** | Journal vs conference; article type (regular paper/letter/technote; conference paper). This decides the documentclass mode. Ask if unclear. |
| 2 | **Get official template** | Use IEEE Template Selector (`template-selector.ieee.org`) for the exact journal, or IEEE Author Center, or Overleaf "IEEE" official templates, or CTAN `IEEEtran` package. Never use third-party modified templates. |
| 3 | **Set document class** | `\documentclass[journal]{IEEEtran}` for journals; `\documentclass[conference]{IEEEtran}` for conferences; `technote` for correspondence; `peerreview`/`peerreviewca` for anonymous review. See `references/ieee-format.md`. |
| 4 | **Write & format** | Follow IEEE structure (Abstract, Index Terms, Introduction, ... References), author block, figures/tables/equations per `references/ieee-format.md`. Keep within page limits. |
| 5 | **References** | IEEE numbered citation style, `IEEEtran.bst` with BibTeX. First citation is [1]. See `references/ieee-format.md` §References. |
| 6 | **Compile & verify PDF** | pdflatex; ensure all fonts embedded; conference camera-ready: certify via **IEEE PDF eXpress** with the conference ID. See `references/submission.md`. |
| 7 | **Submit** | Conference: EDAS/CMT/EasyChair/HotCRP (PDF first; source at camera-ready). Journal: ScholarOne Manuscripts (PDF + source). Complete IEEE eCopyright form. |
| 8 | **Deliver** | Manuscript source + PDF + submission checklist (PASS/FAIL/NOT VERIFIED) + assumptions. |

## Core Rules (Non-Negotiable)

1. **Only official templates.** Never use third-party modified IEEE templates; PDF eXpress / production will reject them.
2. **Conference vs journal mode matters.** Using the wrong variant is a top desk-rejection cause. Conferences: `conference` option; journals: `journal` option (or the journal's custom template via Template Selector).
3. **Conference papers: no headers, footers, or page numbers added by the author.** The publisher adds them at production.
4. **Fonts must be embedded** in the PDF. Unembedded fonts are the #1 PDF eXpress rejection reason.
5. **Respect page limits** (journal main text often ≤14 pages; conference typically 4–8 pages per CfP) and the paper size (US Letter unless the venue explicitly allows A4).
6. **IEEE numbered citations**, first citation [1], `IEEEtran.bst`.
7. **State UNVERIFIED** for anything not checked against the target venue's Call for Papers / journal's Instructions for Authors.

## References

| File | Content |
|---|---|
| `references/ieee-format.md` | IEEEtran modes & documentclass options, author block, abstract/index terms, figures/tables/equations, references (IEEE style) |
| `references/submission.md` | Submission workflows: PDF eXpress certification, conference systems (EDAS/CMT/EasyChair), ScholarOne journals, eCopyright, checklists |
| `references/skeleton.md` | Minimal compilable IEEE-style skeleton (journal & conference variants) with instructions to swap in the official template |

## Output Contract

Every deliverable must include:

1. **Manuscript source** in IEEEtran structure (or the official template), with the skeleton adapted.
2. **Compiled PDF** (when compilation possible) with compile log; font-embedding check result.
3. **Format checklist**: mode correct, page limit, paper size, abstract/index terms, citation style — PASS/FAIL/NOT VERIFIED.
4. **Submission guidance**: which system (EDAS/CMT/ScholarOne), whether PDF eXpress certification is needed.
5. **Assumptions**: venue chosen, page limit assumed, anything needing user confirmation.
