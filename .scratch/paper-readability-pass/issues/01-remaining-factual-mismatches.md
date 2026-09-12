# Remaining factual mismatches

Type: research
Status: resolved
Blocked by:

## Question

After the alignment map closed, does any English section still disagree with `stego-side-wing` or with the frozen 2026-08-29 / 2026-08-15 / 2026-07-30 artifacts? List remaining mismatches with file:line. If none, say so.

## Answer

Headline method and frozen table cells match. Remaining issues for the rewrite: LUCID used `max_retries=1` against a profile default of 6; word-count tokenizer in both printed tables is `[A-Za-z0-9']+`; freeze also stores self-consistency, a naturalness gate, and repetition, which should be named once and not ranked.

Detail: [research note](../research/01-remaining-factual-mismatches.md).

## Comments

Claimed by this session. Findings from [Audit paper vs code](148f826a-0126-4d82-b4de-4e8da922a711).
