---
name: publisher-templates
description: Elsevier/ACM 论文写作 playbook：elsarticle/acmart 模板选择与使用、格式速查、引用样式、Editorial Manager/TAPS 投稿流程。用于"写/改/投 Elsevier 或 ACM 期刊会议论文"类任务。
---

# publisher-templates — Elsevier/ACM 论文写作 playbook

> **English Quick Start**
>
> This skill prepares manuscripts for **Elsevier** journals (elsarticle / cas classes) and **ACM** journals & conferences (acmart class). It covers: choosing the right document class and options, per-publisher formatting rules, reference styles, and the distinct submission workflows — **Editorial Manager (Elsevier)** and **TAPS (ACM)** — including the file-structure and classification rules that cause most submission failures.
> Core loop: **确认目标出版方与期刊/会议 → 选择文档类与选项 → 写作 → 引用与格式检查 → 编译 → 按系统要求打包提交**.
> Hard rules: never invent class options or publisher policies (verify against Guide for Authors / authors.acm.org); follow each submission system's file rules (Elsevier: no subfolders, .bib as "Manuscript"; ACM: TAPS approved-package list); state UNVERIFIED for anything not checked.

## Purpose

This skill prevents the most common Elsevier/ACM submission failures, which are almost never about LaTeX code itself but about **system-specific file rules**: Elsevier's Editorial Manager rejects subfolders and misclassified files; ACM's TAPS rejects non-approved LaTeX packages. It provides template/option cheat-sheets, reference styles, and step-by-step submission workflows for both publishers.

> **模板说明**：`elsarticle.cls` / `cas-sc.cls` / `cas-dc.cls`（Elsevier）与 `acmart.cls`（ACM）均为出版社官方/CTAN 宏包。本 Skill 提供官方获取指引与格式速查，不内置版权类文件；正式投稿使用官方模板，禁止修改类文件。

## When to Invoke

Invoke whenever the user wants to:

- Write/format a manuscript for an **Elsevier** journal (elsarticle or CAS workflow journals).
- Write/format a manuscript for an **ACM** conference (sigconf/sigplan) or journal (acmsmall/acmlarge/acmtog).
- Prepare submission files for **Editorial Manager** (Elsevier) or **TAPS** (ACM).
- Check references/citations (Elsevier numbered/Harvard; ACM numeric) or fix submission errors.

Do **not** invoke for APS/Nature/OSA (see `journal-paper`), IEEE (see `ieee-paper`), theses (see `latex-book`), or slides (see `bupt-beamer-slides`).

## Unified Pipeline (Mandatory Order)

| # | Step | Gate / Rule |
|---|---|---|
| 1 | **Confirm target** | Publisher (Elsevier vs ACM) + specific journal/conference + article type. Determines document class and options. Ask if unclear. |
| 2 | **Get official template** | Elsevier: `elsarticle.zip` from the LaTeX instructions page or Overleaf "Elsevier" templates. ACM: `acmart` (v2.18+) from authors.acm.org / portalparts / Overleaf, or TeX Live. Never modify the class files. |
| 3 | **Set document class** | Elsevier: `\documentclass[preprint,12pt]{elsarticle}` for submission; cas-sc/cas-dc for CAS journals. ACM: `[sigconf]`/`[sigplan]` (conference) or `[acmsmall]`/`[acmlarge]`/`[acmtog]` (journal); `[manuscript,review,anonymous]` for review. See references. |
| 4 | **Write & format** | Follow publisher structure (frontmatter, abstract, highlights/graphical abstract if required, sections). Keep to page/word limits. |
| 5 | **References** | Elsevier: `elsarticle-num` / `elsarticle-harv` / `elsarticle-num-names` per journal. ACM: `ACM-Reference-Format` (BibTeX) or biblatex acmnumeric/acmauthoryear. |
| 6 | **Compile & verify** | pdflatex sequence with BibTeX. Fix all errors — note Overleaf may produce a PDF despite errors while Editorial Manager only gives an error log. |
| 7 | **Package & submit** | Elsevier: flatten all files to one folder, remove paths, upload .bib as "Manuscript". ACM: review phase single-column `manuscript` PDF; camera-ready switch to `[sigconf]` + TAPS-compatible packages + CCS codes + `\Description{}`. |
| 8 | **Deliver** | Source + PDF + submission checklist (PASS/FAIL/NOT VERIFIED) + assumptions. |

## Core Rules (Non-Negotiable)

1. **Never modify the official class files** (`elsarticle.cls`, `acmart.cls`); use options instead.
2. **Elsevier Editorial Manager**: no subfolders; remove all paths from `\includegraphics`/`\bibliography`; classify `.bib`/`.bbl`/`.bst`/`.sty`/`.cls` as **"Manuscript"** (not Supplemental); figures as "Figure". File names: no special chars, one period only.
3. **Elsevier initial submission**: use `preprint` mode (single-column) even if the journal publishes two-column; `final`/`1p`/`3p`/`5p` are camera-ready only.
4. **ACM two-phase workflow**: review = `[manuscript,review,anonymous]{acmart}` single-column; camera-ready = `[sigconf]{acmart}` two-column. `\setcopyright{none}` until the rights form is done.
5. **ACM TAPS**: only approved LaTeX packages; every figure needs `\Description{}`; CCS concepts (from the CCS generator) required; no custom `\newcommand` (refrain).
6. **Respect limits** and the journal/conference Guide for Authors / CfP.
7. **State UNVERIFIED** for anything not checked against current publisher guidelines.

## References

| File | Content |
|---|---|
| `references/elsevier.md` | elsarticle/cas classes & options, frontmatter, reference styles, Editorial Manager submission rules & error fixes |
| `references/acm.md` | acmart variants (sigconf/sigplan/acmsmall/acmlarge/acmtog), two-phase workflow, TAPS rules, CCS & accessibility |

## Output Contract

Every deliverable must include:

1. **Manuscript source** in the official class structure, with correct documentclass options.
2. **Compiled PDF** (when possible) + compile log summary.
3. **Submission checklist**: document class correct, file flattening done, item-type classification, package approval (ACM), reference style — PASS/FAIL/NOT VERIFIED.
4. **Submission guidance**: Editorial Manager item types / TAPS requirements.
5. **Assumptions**: target venue chosen, limits assumed, anything needing user confirmation.
