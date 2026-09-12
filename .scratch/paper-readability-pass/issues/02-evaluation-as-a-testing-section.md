# What a followable evaluation section must do

Type: research
Status: resolved
Blocked by:

## Question

`evaluation.tex` already contains the LLM-judge table and the historical table. It still reads like an audit memo. What paragraph-level shape should the rewrite take so a reader learns: (1) how we tested, (2) how each printed metric is calculated, (3) the five judge criteria, (4) the two dated result tables, (5) what we are not claiming? Name the jargon to drop or define once.

## Answer

Teach first, then tables, then caveats. Opening names the two runs in ordinary English. Each printed metric gets a short what / how / where / limit block, including the lexical-quality index the current file never defines. Judge criteria keep standout and weakest almost as they are; AUROC is explained as “more suspicious than a human comment” before the statistic. Dual ZLG failure accounting is a footnote or is cut. Frozen numbers do not move.

Detail: [research note](../research/02-evaluation-as-a-testing-section.md).

## Comments

Claimed by this session. Findings from [Assess paper prose quality](504ebe99-fee2-466d-b3fc-c7482ca95ba6).
