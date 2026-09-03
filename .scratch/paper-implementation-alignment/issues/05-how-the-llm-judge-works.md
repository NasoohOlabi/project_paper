# How the independent LLM-judge evaluation works

Type: research
Status: resolved
Blocked by:

## Question

What is the independent LLM-judge protocol in enough detail for a paper subsection: the five criteria, slate construction, judge model and provenance, scoring formulas, chance baselines, paired sign tests, and reporting limits?

Primary sources: `stego-side-wing/docs/reports/2026-08-29-independent-llm-judge-results.md`, `scripts/score_codex_judgments.py`, `src/services/judge_scoring_service.py`, judge prompt builders, and the viewer formulas in `stego-results-viewer/src/app/zlg-comparison/_lib/llm-judge.ts`. Distinguish this protocol from G-Eval if G-Eval is a different older path.

## Answer

This is a five-criterion Codex Luna judge on 244 unique-output pairs (2,928 tasks), not G-Eval. Cite the frozen table as-is: standout 51.6% vs 28.3%, weakest 29.1% vs 47.5% (human 23.4%), suspicion AUROC 0.661 vs 0.650 (sign-test p=0.385 on raw scores, not AUROC), attribution 89.3% vs 75.0% descriptive, register 3.193 vs 2.791 with paired sign-test p=0.00374. Chance baselines are 10% / 33% / 0.5 / 25% / none.

Detail: [How the independent LLM-judge evaluation works](../research/05-how-the-llm-judge-works.md).
