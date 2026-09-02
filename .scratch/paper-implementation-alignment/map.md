# Bring the paper in line with the live implementation

Label: wayfinder:map

## Destination

The English paper, then the Arabic twin, describes the live `stego-side-wing` selection-channel method as it actually runs: a reader can follow how bits become a Reddit-style reply, and the evaluation reports the real tests including the independent LLM judge, with brief calculation notes and tables that match frozen artifacts rather than the stale 304-pair audit alone.

## Notes

- Domain: academic paper. English in `stego_paper/` is the source of truth; `stego_paper_ar/` must stay factually aligned after English lands.
- Skills every session should consult: unslop; `project_paper/AGENTS.md` (read-only knowledge-base rule, preferred translations, Human Writer Notes Alice/Bob walkthrough); `stego-side-wing/.agents/method-and-zlg-benchmark.md` before quoting any comparison number; `project_paper/CONTEXT.md` for terms.
- Execution is in scope. After research tickets close, later tickets edit the LaTeX. This map is not a spec handoff.
- Nasouh asked not to be grilled unless a decision is actually blocked. Facts come from code and frozen reports.
- Review paragraphs one at a time. No jargon pile-up. No invented numbers. No verification-plan documents.
- "LG" in the original brief is treated as the evaluation and benchmarking writeup: it needs a full rewrite, not a patch of Table 1.
- Do not modify `stego-side-wing`, the viewer, or ZLG to make the paper easier. The paper follows the code.
- The `project_paper/knowledge-base` directory named in AGENTS.md is not present in this checkout; use sibling repos and frozen reports instead. Do not create one.

## Decisions so far

- [How the two-layer embedding actually works](issues/01-how-embedding-works.md): reported runs are single-frame `encode` plus audit-assisted decode; lossless widths and parent-then-angles planning are the multi-frame path, not those tables. Detail: [research note](research/01-how-embedding-works.md).
- [How each reported metric is calculated](issues/02-how-metrics-are-calculated.md): historical table is SOO then post-clustered channel width vs a matched 16-bit ZLG payload; live runner uses a different capacity definition and already computes the LLM-judge and divergence metrics the paper omits. Detail: [research note](research/02-how-metrics-are-calculated.md).
- [Where the paper disagrees with the code](issues/04-where-the-paper-disagrees-with-the-code.md): default encode is physical widths plus modulo; \(T_{sync}\) is operational not enforced; decode is temperature 0.7 plus audit override; evaluation mixes July 30 cells with a later ZLG failure story. Detail: [research note](research/04-where-the-paper-disagrees-with-the-code.md).
- [Paragraph quality of the English paper](issues/06-paragraph-quality-of-the-english-paper.md): keep the Alice/Bob opening; teach reply target and Angle before compression; replace evaluation rather than polish Table 1. Detail: [research note](research/06-paragraph-quality-of-the-english-paper.md).
- [Rewrite the embedding explanation](issues/07-rewrite-the-embedding-explanation.md): methodology now leads with the two visible choices; compression and multi-frame sit after; implementation matches live temperatures and the 80k Angle batch cap.
- [How the independent LLM-judge evaluation works](issues/05-how-the-llm-judge-works.md): Codex Luna, 244 unique-output pairs, five criteria; only register has a claimed paired sign test (p=0.00374). Not G-Eval. Detail: [research note](research/05-how-the-llm-judge-works.md).
- [Which result numbers the paper should cite](issues/03-which-numbers-the-paper-should-cite.md): two dated artifacts, 08-29 judge plus 07-30 historical table; drop the rescaled BERTScore and BLEU-median cells. Detail: [research note](research/03-which-numbers-the-paper-should-cite.md).
- [Rewrite evaluation and results](issues/08-rewrite-evaluation-and-results.md): evaluation leads with the 244-pair LLM-judge table; historical 304-pair table kept and labeled; MISSING overlap cells removed.
- [Unslop remaining English sections](issues/09-unslop-remaining-english-sections.md): introduction and background no longer present token sampling as this method; related work points at evaluation instead of restating MATTR.
- [Sync the Arabic paper](issues/10-sync-the-arabic-paper.md): Arabic methodology, implementation, evaluation, background, and related-work pointers now match the English facts and numbers. Locked abstract untouched.

## Not yet specified

- Whether figures need redraws, or only captions and surrounding prose.

## Out of scope

- New experiments or re-running the GPU benchmark.
- Code changes in `stego-side-wing`, `stego-results-viewer`, or `zero-shot-GLS`.
- Writing into a knowledge base.
- Committing or pushing unless Nasouh asks.
