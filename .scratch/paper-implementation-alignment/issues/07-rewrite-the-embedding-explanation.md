# Rewrite the embedding explanation

Type: task
Status: resolved
Blocked by: 01, 04, 06

## Question

Rewrite the methodology embedding walkthrough so a reader can follow Alice hiding a short message and Bob recovering it, in the voice of the Human Writer Notes, matching the live pipelines, without puffery or token-sampling jargon.

Keep compression and multi-frame only at the level the code and reported runs actually need. Update implementation.tex where it duplicates or contradicts that walkthrough. English only in this ticket.

## Answer

Methodology now walks Alice through reply target then Angle before compression. Single-comment `encode()` is the reported path: physical widths plus modulo, three candidates, strict verify, optional revision. Multi-frame and parent-conditioned rebuild are labeled as implemented, not as the tables. Decode is MiniLM top-20, lexical rerank, temperature 0.7 `idx: N`, with audit-assisted recovery on the reported workloads. Implementation no longer calls decode temperature 0 or a 150k Angle batch cap.

Edited: `stego_paper/sections/methodology.tex`, `stego_paper/sections/implementation.tex`.
