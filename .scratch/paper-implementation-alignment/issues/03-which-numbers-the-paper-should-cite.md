# Which result numbers the paper should cite

Type: research
Status: resolved
Blocked by:

## Question

Which frozen artifacts are the canonical sources for tables in the paper, and which numbers from `evaluation.tex` (the 627/554/304 historical audit, 15.14 vs 16.00 bits, GPT-2 68.15 vs 53.70, and so on) are still valid to keep as a historical configuration comparison?

Identify the LUCID vs ZLG comparison dataset behind the 2026-08-29 independent LLM-judge result, the ITT reliability numbers for that source run, uniqueness/selection rules, and any later reports that supersede `2026-08-08-current-research-state.md`. List every table cell the evaluation rewrite should print, with the file it comes from. Do not invent rounded values.

## Answer

Print two dated comparisons. Current quality: the 2026-08-29 Codex Luna judge on 244 unique-ZLG pairs from `zlg_lucid_fresh_6x_20260815`. Source-run ITT sits beside it (LUCID 2543/4044, ZLG freeze 1610/1711 accepted and 1603 decode-verified). Historical configuration: 2026-07-30 627/554/304 with 15.14 vs 16.00 bits and GPT-2 68.15 vs 53.70, plus the 07-31 460/66.1% recode. Drop BERTScore 0.083/0.154, F1 0.068/0.114, 5-gram 5.9%/0.3%, and BLEU medians 1.46 vs 1.59: they are MISSING from every frozen report. The two 244 counts are different objects.

Detail: [Which result numbers the paper should cite](../research/03-which-numbers-the-paper-should-cite.md).
