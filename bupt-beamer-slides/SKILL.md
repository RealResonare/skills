---
name: bupt-beamer-slides
description: Create, adapt, and compile BUPT-style Beamer/LaTeX presentations using a bundled Beijing University of Posts and Telecommunications (BUPT) slide template. Use when the user asks for 北邮 Beamer, BUPT LaTeX PPT, slides from a paper/report/thesis, course presentation slides, or help initializing/troubleshooting a Beamer project.
---

# BUPT Beamer Slides

Use this skill to create or edit Chinese Beamer presentations with the bundled BUPT visual style.

## Asset Location

All paths below are **relative to this skill directory** (`<skill_dir>/`). Resolve the skill's own location at runtime (e.g. via `Path(__file__)` for scripts, or by copying the skill folder into the assistant's skills directory); never hardcode an absolute path.

- Template directory: `assets/template/`
- Main entry: `slide.tex`
- Theme file: `BUPT.sty`
- Bibliography stub: `ref.bib`
- Images: `pic/BUPT_logo.png`, `pic/dtmf.pdf`
- Project initializer: `scripts/init_bupt_beamer.py`

## Standard Workflow

1. Initialize a new slide project when needed:

   ```bash
   python <skill_dir>/scripts/init_bupt_beamer.py <target-dir>
   ```

   Replace `<skill_dir>` with the absolute path of this skill. Use `--force` only when the user wants existing template files overwritten.

2. Edit `<target-dir>/slide.tex`:
   - Keep `\documentclass{beamer}` for 4:3 slides.
   - Use `\documentclass[aspectratio=169]{beamer}` for 16:9 classroom/projector slides when appropriate.
   - Keep `\usepackage{BUPT}` and `BUPT.sty` in the same directory as `slide.tex`.
   - Update `\title`, `\subtitle`, `\author`, `\institute`, and `\date`.

3. Convert paper/report/thesis content into slide structure:
   - Prefer 8–14 content slides for a typical course or thesis presentation.
   - Use one idea per frame.
   - Use equations sparingly; split derivations across frames.
   - A generally useful technical presentation order (adapt to the user's topic):
     1. 课题背景 / 研究意义
     2. 相关工作 / 现状分析
     3. 方法 / 模型 / 算法
     4. 关键实现细节
     5. 实验 / 结果与分析
     6. 结论与展望
   - Ask the user for the actual topic outline when the source material is not explicit; do not assume a fixed project.

4. Reuse existing project figures:
   - Copy required PNG/PDF files into `pic/` or reference them with relative paths.
   - Use `\includegraphics[width=...]`.

5. Compile from the slide project root:

   ```bash
   xelatex -interaction=nonstopmode -file-line-error slide.tex
   xelatex -interaction=nonstopmode -file-line-error slide.tex
   ```

   If using BibTeX:

   ```bash
   xelatex -interaction=nonstopmode -file-line-error slide.tex
   bibtex slide
   xelatex -interaction=nonstopmode -file-line-error slide.tex
   xelatex -interaction=nonstopmode -file-line-error slide.tex
   ```

## Template Notes

- The bundled template uses XeLaTeX and explicit Noto CJK/Tinos fonts to avoid default Fandol warnings.
- Required apt packages normally include `texlive-xetex`, `texlive-latex-recommended`, `texlive-latex-extra`, `texlive-lang-chinese`, `fonts-noto-cjk`, `fonts-noto-core`, and `fonts-tinos`.
- `pstricks` is loaded by the template but can be removed from `slide.tex` if unused.
- The default theme uses BUPT blue `#3434b4`, smoothbars navigation, title page logo, section outline frames, and numbered captions.

## Validation

After edits, always run at least:

```bash
xelatex -interaction=nonstopmode -file-line-error slide.tex
xelatex -interaction=nonstopmode -file-line-error slide.tex
```

Check that:
- `slide.pdf` exists.
- There are no `LaTeX Error`, `Package ... Error`, `Undefined control sequence`, or unresolved citation/reference warnings.
- Text does not overflow frames; split dense frames rather than shrinking all text.
