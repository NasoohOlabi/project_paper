# How the two-layer embedding actually works

Type: research
Status: resolved
Blocked by:

## Question

What does the live sender do, step by step, to turn a payload into a published reply, and what does the live receiver do to get the bits back?

Cover: payload protection and compression; comment-target selection; Angle list construction (including context-weighted vs post-level); bit widths (physical vs recoverable); synthesis and the decode-verification retry; receiver reconstruction, shortlist, and discriminator; multi-frame only if the pipelines actually use it in the reported runs. Cite pipeline modules, codec functions, and prompts. Flag every place the current methodology.tex disagrees with the code.

## Answer

Reported runs use single-frame `StegoPipeline.encode`: protect (default `plain`), dictionary-compress, spend bits on a DFS parent index then an Angle index, generate three candidate replies, and keep a text only if strict decode hits the chosen Angle. Multi-frame and parent-conditioned rebuild at encode time exist in code and are not what the tables measured. Decode is MiniLM top-20 plus lexical rerank plus a temperature-0.7 `idx: N` prompt; reported e2e recovery is audit-assisted on the sender’s already-angled post.

Detail: [How embedding works](../research/01-how-embedding-works.md).
