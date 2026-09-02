# Rewrite evaluation and results

Type: task
Status: resolved
Blocked by: 02, 03, 05

## Question

Replace the evaluation section with a full account of testing and benchmarking: how each metric is calculated (briefly), the independent LLM-judge criteria and table, and the other frozen metrics (capacity, reliability, perplexity, divergence, overlap, length) with honest denominators and caveats.

This is the rewrite the original brief called for. Do not leave the 304-pair table as the only results display. Update abstract, introduction contributions, and conclusion so they cite the same numbers. English only in this ticket.

## Answer

Evaluation now leads with the 2026-08-29 LLM-judge table, then 2026-08-15 ITT/capacity, then the 2026-07-30 historical table. Dropped the MISSING rescaled BERTScore and BLEU-median cells. Abstract, contributions, conclusion, and the related-work pointers to evaluation cite the same two artifacts.

Edited: `stego_paper/sections/evaluation.tex`, `abstract.tex`, `introduction.tex`, `conclusion.tex`, `related_work.tex` (evaluation pointers only), `main.tex` preprint date.
