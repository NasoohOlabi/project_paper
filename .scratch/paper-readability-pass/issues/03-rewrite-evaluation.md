# Rewrite evaluation as testing and benchmarking

Type: task
Status: resolved
Blocked by: 01, 02

## Question

Rewrite `stego_paper/sections/evaluation.tex` so it is a testing and benchmarking section, not a caveats stack. Keep the frozen numbers. Lead with how the comparison was run. Teach each metric in one short paragraph before the table that uses it. Keep both dated tables. Update abstract, introduction contributions, and conclusion only if their sentences still sound like the old memo.

English only in this ticket.

## Answer

English evaluation now teaches capacity, success rates, GPT-2, lexical quality, word count, BERTScore, and the five judge criteria before the tables. LUCID `max_retries=1` is named. Dual ZLG failure accounting is a footnote. Self-consistency and the naturalness gate are named once, not ranked. Abstract, introduction, conclusion, and two related-work pointers dropped "audit-assisted" / ITT where they were leftover memo voice.

Edited: `stego_paper/sections/evaluation.tex`, `abstract.tex`, `introduction.tex`, `conclusion.tex`, `related_work.tex` (two sentences).
