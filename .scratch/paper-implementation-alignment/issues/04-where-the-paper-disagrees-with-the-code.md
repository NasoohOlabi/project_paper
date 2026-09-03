# Where the paper disagrees with the code

Type: research
Status: resolved
Blocked by:

## Question

Section by section (`abstract`, `introduction`, `background`, `related_work`, `methodology`, `implementation`, `evaluation`, `conclusion`), where does the English paper misstate, overclaim, or omit something the live implementation does?

Prioritize the embedding story, decode contract, temporal window enforcement, compression and protection modes, context-weighted Angle pools, audit-assisted vs blind recovery, and any leftover white-box or token-sampling language. Quote the LaTeX claim and the code or report that contradicts it.

## Answer

Live `encode()` still writes physical widths with modulo aliasing; the injective recoverable writer is multi-frame only. The receiver drops the sender comment and does not apply \(T_{sync}\). Decode runs at temperature 0.7 with a top-20 shortlist and lexical rerank, and it will take the sender audit when present. Context-weighted Angle pools are the reported run, not the default. Evaluation mixes the July 30 metric cells with a later ZLG failure taxonomy and omits the 2026-08-29 judge.

Detail: [Where the paper disagrees with the code](../research/04-where-the-paper-disagrees-with-the-code.md).
