# What a followable evaluation section must do

Source: [Assess paper prose quality](504ebe99-fee2-466d-b3fc-c7482ca95ba6)

## Verdict

`evaluation.tex` has the right bones and the right frozen numbers. It still reads as an audit memo. The rewrite teaches first, then tables, then caveats.

## Required shape (paragraph order)

1. **How we tested.** One plain opening: we compared our comments to ZLG on quality and on capacity/reliability, on two separate runs. Name the two tables in ordinary English. The “do not mix denominators” warning comes after the reader knows what each table is, not in sentence one.

2. **How each printed metric is calculated.** One short block per family, each in the same order: what it is, how it is computed, which table uses it, one limitation.
   - Recoverable capacity: toy example (8 reply targets + 32 Angles = 3+5 bits), then the floor-log formula. Physical/modulo stays in methodology, not here.
   - Success rates: say “we also count failed encodes” once. Do not lead with intention-to-treat. Define that term once if the table still needs it.
   - GPT-2 perplexity: how surprised GPT-2 is; lower is not “more human.” Formula after the sentence.
   - Lexical-quality index: define it here. The current file uses it in tables and never explains it.
   - Word count: which tokenizer, and that the two runs are not interchangeable.
   - BERTScore F1: historical table only, unrescaled, one line.
   - LLM judge: not G-Eval. We asked a model five blinded questions. Codex Luna / seeded slates can be one sentence, not the lead.

3. **Five judge criteria**, each: setup, chance, direction (higher/lower), then the number. Standout and weakest are already close. Suspicion AUROC needs “how often this arm looks more suspicious than a human comment” before Mann–Whitney. Attribution: we report the rate; no significance test. Register-fit: 1–5 mean plus the paired sign test in one sentence, drop “claimed.”

4. **Tables after teaching.** Judge table first. Then a short reliability paragraph: how often encode succeeded, and that recovery used sender audit files. Then the historical table with one configuration story. Dual ZLG failure accounting (54.9% vs 66.1%) belongs in a footnote or is cut.

5. **What we are not claiming.** Unique-ZLG subset, not a reader study, not blind Bob-on-Reddit, not a security ranking. Keep this short because the teaching blocks already carried the limits.

## Jargon

Drop from running prose, or define once then use the plain phrase: intention-to-treat, successful-output-only, decision-grade, post-clustered, Holm-adjusted, Mann–Whitney, slate (say lineup), audit-assisted (say sender-side metadata / not a public-thread decode), globally unique, freeze IDs as leads.

Keep as table labels only where the frozen report uses them.

## Out of this ticket

Methodology Layer-2 and bit-width teaching, and background/related-work slop, are later tickets. Do not flatten the 31-paper survey tables in the evaluation rewrite.
