---
name: journal-paper
description: 期刊论文写作 playbook：按 APS（REVTeX）/ Nature / OSA（Optica）期刊格式要求组织、排版、编译与提交 LaTeX 论文。用于"写/改/投 APS、Nature、OSA 期刊论文"类任务，提供格式速查与模板获取指引。
---

# journal-paper — 期刊论文写作 playbook

> **English Quick Start**
>
> This skill prepares scientific manuscripts for submission to **APS** (American Physical Society, REVTeX 4.2), **Nature** (Springer Nature template / Scientific Reports `wlscirep`), and **OSA / Optica** (Optica Publishing Group `optica-article`) journals. It covers: choosing the right template, structuring the manuscript per journal conventions, formatting references/citations, compiling with the correct engine, and packaging for submission.
> Core loop: **确认目标期刊与文章类型 → 获取官方模板 → 按期刊结构写作 → 参考文献与格式检查 → 编译验证 → 打包提交**.
> Hard rules: never fabricate journal policies or template commands (verify against the journal's author guidelines); always fetch the official template (do not invent .cls/.sty content); compile with the correct engine; check word/page limits before submission.

## Purpose

This skill ensures manuscripts are formatted **correctly for the target journal** before submission, avoiding desk rejection from formatting issues. It provides per-journal format cheat-sheets, template acquisition links (official sites / Overleaf), structural conventions, reference/citation rules, and compile & submission workflows.

> **版权说明**：APS/Nature/OSA 的官方 LaTeX 模板（REVTeX、sn-jnl.cls、wlscirep.cls、optica-article.cls 等）是出版社版权材料，本 Skill **不内置版权文件**，而是提供获取指引（官方下载页 / Overleaf 模板库）与格式要求速查。AI 生成手稿时应引用官方模板，不得凭空捏造模板内容。

## When to Invoke

Invoke whenever the user wants to:

- Write or format a manuscript for an **APS** journal (PRL, PRA–PRE, PRX, PRApplied, PRFluids, etc.).
- Write or format a manuscript for **Nature** / Nature Portfolio (incl. Scientific Reports).
- Write or format a manuscript for **OSA / Optica** journals (Optics Express, Optics Letters, Optica, JOSA A/B, Biomedical Optics Express, etc.).
- Check a manuscript against journal formatting requirements, or prepare submission files (tar/zip, .bbl, cover letter).

Do **not** invoke for books/theses (see `latex-book`, `bupt-bachelor-thesis`) or general slide decks (see `bupt-beamer-slides`).

## Unified Pipeline (Mandatory Order)

| # | Step | Gate / Rule |
|---|---|---|
| 1 | **Confirm target** | Journal + article type (Article/Letter/Review). This determines template, length limits, and structure. Ask if unclear; default per journal tables below. |
| 2 | **Get official template** | Fetch the official template: APS REVTeX from `journals.aps.org/revtex` or Overleaf; Nature from Springer Nature template page / Overleaf; OSA/Optica from Overleaf ("Universal manuscript template for Optica Publishing Group journals"). Do not invent .cls/.sty content. |
| 3 | **Write to structure** | Follow the journal's structure conventions (see references). Keep to word/display-item limits. |
| 4 | **References & citations** | Use the journal's citation style (all three use numerical). APS: natbib/BibTeX with `apsrev4-2.bst`; Nature: `.bbl` required (no `.bib` upload); OSA: full author names + titles + inclusive pages. |
| 5 | **Format & compile** | Compile with correct engine (REVTeX: pdflatex; OSA: pdflatex or xelatex per template; Nature: pdflatex). Run BibTeX sequence where needed. Fix all errors/warnings. |
| 6 | **Length & policy check** | Verify against word/page/display-item limits and author guidelines (abstract limits, no citations in abstract, etc.). See per-journal tables. |
| 7 | **Package & submit** | Package per journal: OSA = `.tar` (not .zip); Nature/SciRep = files incl. `.bbl`; APS = source files. Prepare cover letter and required statements. |
| 8 | **Deliver** | Manuscript source + compiled PDF + submission checklist (per-journal PASS/FAIL) + assumptions. |

## Core Rules (Non-Negotiable)

1. **Never fabricate journal policies or template commands.** Verify against the journal's current author guidelines. If unverified, state so.
2. **Always use the official template.** Do not write custom .cls/.sty from memory; fetch from official/Overleaf.
3. **Compile with the correct engine** and run the full compile sequence (including BibTeX) before claiming success.
4. **Respect limits**: word count, abstract limit, display items, references cap. Exceeding them risks desk rejection.
5. **No citations in the abstract** (Nature & OSA explicitly prohibit; APS abstracts should avoid them too).
6. **Check the submission format requirement**: OSA requires `.tar`; Nature/SciRep needs `.bbl` not `.bib`; APS accepts source + PDF.
7. **State UNVERIFIED** for anything not checked against the current journal guidelines.

## References

| File | Content |
|---|---|
| `references/aps-revtex.md` | APS: REVTeX 4.2 setup, journal options, structure, references, compile, submission |
| `references/nature.md` | Nature / Scientific Reports: templates, word limits, structure, references (.bbl), policies |
| `references/osa-optica.md` | OSA/Optica: optica-article setup, journal selection, abstract/ref rules, .tar submission |
| `references/writing-common.md` | Cross-journal writing conventions: title/abstract/figures/equations/citations, cover letter, LLM-use policy |

## Output Contract

Every deliverable must include:

1. **Manuscript source** (.tex + figures + .bib/.bbl) in the official template structure.
2. **Compiled PDF** (when compilation possible) with compile log summary.
3. **Per-journal checklist**: word count vs limit, display items vs limit, abstract compliance, reference format, submission packaging — PASS/FAIL/NOT VERIFIED.
4. **Submission package**: files arranged per journal requirements (tar for OSA, .bbl for Nature, etc.).
5. **Assumptions**: journal/type chosen, limits assumed, anything needing user confirmation.
