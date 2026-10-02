# Paper builds

The repository contains two independent document roots:

- `stego_paper/main.tex` — English paper
- `stego_paper_ar/main_ar.tex` — Arabic paper

Both use XeLaTeX through `latexmk`. In Cursor, open either `main.tex` and run
the **LaTeX Workshop: Build** command. The shared workspace recipe writes
auxiliary files and the PDF into that paper's local `build/` directory.

For PowerShell builds from this directory:

```powershell
.\scripts\build-en.ps1
.\scripts\build-ar.ps1
```

Shared figures, TikZ sources, bibliography, and class/style files live under
`common/`. The translated section files remain separate under the two paper
directories.

## Method terminology

Refer to our method as "the proposed method" or "our method" in English and
«الطريقة المقترحة» or «طريقتنا» in Arabic. Do not include internal implementation
code names in either paper, including titles, figures, tables, captions, or abstracts.
