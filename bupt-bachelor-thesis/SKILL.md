---
name: bupt-bachelor-thesis
description: Create, adapt, or compile LaTeX thesis projects using a bundled Beijing University of Posts and Telecommunications (BUPT) undergraduate bachelor thesis template. Use when the user asks to write a BUPT bachelor thesis, 北邮本科毕设论文, 北京邮电大学毕业设计, convert content into the BUPT undergraduate thesis LaTeX format, initialize a thesis from the bundled template, add chapters/abstract/references/figures/tables, or troubleshoot compilation of main.tex.
---

# BUPT Bachelor Thesis

Use this skill when a user wants work based on the BUPT undergraduate bachelor thesis LaTeX template. The template is bundled inside this skill directory, so no remote clone is needed.

## Asset Location

All paths below are **relative to this skill directory** (`<skill_dir>/`). Resolve the skill's own location at runtime (e.g. via `Path(__file__)` for scripts, or by copying the skill folder into the assistant's skills directory); never hardcode an absolute path.

- Bundled template: `assets/template/`
- Main entry: `main.tex`
- Metadata: `main.cfg`
- Abstracts and keywords: `abstract.cfg`
- Bibliography: `ref.bib`
- Figures: `pictures/`
- Administrative PDFs and Word sources: `docs/`
- Template style and bibliography style: `BUPTthesisbachelor.sty`, `buptbachelor.bst`

Copy `assets/template/` into the user's requested output directory before modifying it. Do not edit the skill asset in place.

## Standard Workflow

1. Copy the template directory into the user's target directory:

   ```bash
   rsync -a <skill_dir>/assets/template/ <target-dir>/
   ```

   Replace `<skill_dir>` with the absolute path of this skill (for example, `<assistant-skills-dir>/bupt-bachelor-thesis`). Never assume a specific user home or a specific assistant's skills layout.

2. Replace thesis metadata in `main.cfg`:
   - `\thesistitle`
   - `\thesistitleen`
   - `\thankwords`

3. Replace abstracts and keywords in `abstract.cfg`:
   - `\abstractzh`
   - `\abszhkeyone` through `\abszhkeyfive`
   - `\abstracten`
   - `\absenkeyone` through `\absenkeyfive`

4. Replace example body content in `main.tex`:
   - Keep the document preamble, cover/task/score/statement PDF inclusion, abstract inclusion, table of contents, bibliography, thanks, and appendix structure unless the user asks otherwise.
   - Replace sample `\chapter`, `\section`, figures, tables, algorithms, and appendices with the user's thesis content.
   - Use `\chapter{...}`, `\section{...}`, `\subsection{...}` for structure.

5. Add figures and code:
   - Put thesis figures under `pictures/` or a subfolder such as `pictures/chip/`.
   - Use the template figure helper:

     ```tex
     \buptfigure[width=0.70\textwidth]{pictures/example}{图题}{fig:example}
     ```

   - Use the template table helper:

     ```tex
     \begin{bupttable}{表题}{tab:example}
       \begin{tabular}{lll}
       ...
       \end{tabular}
     \end{bupttable}
     ```

6. Put BibTeX entries in `ref.bib`, then cite them with `\cite{key}`.

7. Compile from the thesis project root:

   ```bash
   xelatex -interaction=nonstopmode -file-line-error main.tex
   bibtex main
   xelatex -interaction=nonstopmode -file-line-error main.tex
   xelatex -interaction=nonstopmode -file-line-error main.tex
   ```

## Common Fixes

- If `Times New Roman` is missing on Linux, either install Microsoft fonts or patch the template style to use `Tinos`:

  ```tex
  \setmainfont[Mapping=tex-text]{Tinos}
  ```

- If Fandol CJK fonts fail, prefer explicit system CJK fonts in `BUPTthesisbachelor.sty`:

  ```tex
  \usepackage[fontset=none]{ctex}
  \setCJKmainfont{Noto Serif CJK SC}
  \setCJKsansfont{Noto Sans CJK SC}
  \setCJKmonofont{Noto Sans Mono CJK SC}
  ```

- If compilation stops at a `?` prompt, exit with `X`; rerun with `-interaction=nonstopmode` to avoid interactive hangs.
- If references appear as question marks, run the full four-step compile sequence.
- If `docs/*.pdf` files are missing, either restore them from the bundled template or remove/comment the corresponding `\includepdf` lines in `main.tex`.

## Output Expectations

- The compiled thesis PDF is `main.pdf` in the thesis project root.
- Avoid overwriting the user's existing project without checking whether the target directory already contains a thesis.
- Keep generated thesis source self-contained: copied template files, figures, `ref.bib`, and any code listings should live under the target directory.
