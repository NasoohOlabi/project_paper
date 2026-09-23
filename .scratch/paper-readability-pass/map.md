# Make the paper readable without going stale

Label: wayfinder:map

## Destination

A reader who is not steeped in the repo can follow how bits become a Reddit-style comment, then read a testing section that teaches the LLM-judge criteria, prints that table, and briefly says how every other printed metric is computed. English is the source of truth. Arabic is updated after English lands. Frozen numbers do not move. The prose is unslopped.

## Notes

- Domain: academic paper. English in `stego_paper/` first; `stego_paper_ar/` after.
- Skills every session should consult: unslop; `project_paper/AGENTS.md`; `project_paper/CONTEXT.md`; `stego-side-wing/.agents/method-and-zlg-benchmark.md` before quoting a comparison number.
- Execution is in scope. Later tickets edit LaTeX. This is not a spec handoff.
- Nasouh asked not to be grilled unless a decision is actually blocked. Facts come from code and frozen reports.
- Review paragraphs one at a time. No jargon pile-up. No invented numbers. No verification-plan documents. Do not modify `AGENTS.md`.
- A prior map, [Bring the paper in line with the live implementation](../paper-implementation-alignment/map.md), already put the two dated artifacts and the two-layer method into the English and Arabic files. This map does not redo that research. It makes the writeup followable.
- "LG" in the brief is the evaluation and benchmarking section.
- Do not modify `stego-side-wing`, the viewer, or ZLG. Do not run new GPU experiments. Do not commit unless Nasouh asks.

## Decisions so far

- [Remaining factual mismatches](issues/01-remaining-factual-mismatches.md): tables match the freeze; remaining gaps are omitted freeze fields, LUCID `max_retries=1`, and a wrong word-count tokenizer claim. Detail: [research note](research/01-remaining-factual-mismatches.md).
- [What a followable evaluation section must do](issues/02-evaluation-as-a-testing-section.md): teach metrics first, then the two dated tables, then caveats; define lexical quality; demote freeze bookkeeping. Detail: [research note](research/02-evaluation-as-a-testing-section.md).
- [Rewrite evaluation as testing and benchmarking](issues/03-rewrite-evaluation.md): English evaluation teaches each printed metric, then the two dated tables; LUCID retry override and freeze-native extras are named once.

## Not yet specified

- Figure caption wording after later methodology edits: keep the TikZ drawings unless a caption still names the wrong pipeline.

## Out of scope

- New experiments or re-running the GPU benchmark.
- Code changes in `stego-side-wing`, `stego-results-viewer`, or `zero-shot-GLS`.
- Writing into a knowledge base.
- Committing or pushing unless Nasouh asks.
- Re-deciding which frozen artifacts to cite: that is already answered in [Which result numbers the paper should cite](../paper-implementation-alignment/issues/03-which-numbers-the-paper-should-cite.md).
