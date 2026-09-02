# Paragraph quality of the English paper

Ticket: `issues/06-paragraph-quality-of-the-english-paper.md`
Scope: voice and readability of `stego_paper/sections/*.tex`. No LaTeX edits. No new scientific claims.
Sources: the eight English section files, plus the target-voice notes in `project_paper/AGENTS.md` (Human Writer Notes) and the glossary in `project_paper/CONTEXT.md`. Unslop pattern numbers refer to the scan list in the unslop skill, applied as a scan only.

Word counts below include figure-prompt comments that never reach the PDF. Related work is still the longest reader-facing section. Methodology is the one a reader has to survive in order to learn how bits become a reply.

| File | Lines | Words |
| --- | --- | --- |
| `related_work.tex` | 329 | 5317 |
| `methodology.tex` | 324 | 4292 |
| `background.tex` | 40 | 1288 |
| `evaluation.tex` | 44 | 823 |
| `implementation.tex` | 56 | 809 |
| `introduction.tex` | 53 | 797 |
| `abstract.tex` | 5 | 373 |
| `conclusion.tex` | 6 | 190 |

## Target voice for methodology

Later rewrite tickets should treat `project_paper/AGENTS.md` Human Writer Notes as the methodology voice, not the current System Architecture register.

That note is an Alice/Bob walkthrough: both have accounts on a threaded platform (Reddit as the case), Alice’s agent finds a post, builds a shared document list (post, comments, search results), maps those documents to Angles with a shared LLM at temperature 0, then embeds in two layers (which comment to reply to, which Angle to talk about), generates a visible reply, checks that Bob can recover the Angle, and only then publishes after an agreed duration so Bob can rebuild the same snapshot. Compression is an aside for text payloads, not the thing the reader learns first.

The glossary in `CONTEXT.md` agrees: say *reply target*, not *spatial embedding*; say *Angle* and *tangent* with those meanings; say *stego comment*, not *covertext* as the default term. Several methodology headings currently violate that glossary on purpose of sounding more technical.

## Structural issues (not style)

Two layout problems will keep producing bad paragraphs even if individual sentences get cleaned.

**Methodology teaches the codec before the channel.** After a clear Alice/Bob opening (`methodology.tex` L4–9), the section spends Operational Requirements, Search Determinism, Temporal Window, then the entire Payload Preparation & Compression block (HMAC modes, zlib, session dictionary, backward DP, token layout table) *before* Layer 1 and Layer 2. Multi-frame (Elias-gamma headers, circular slot planner, context-weighted sampler) then sits between channel widths and the synthesis/verify loop. A reader who came to learn “how does a comment hide bits?” hits a compressor and a transport planner first. Human Writer Notes put compression last and in one sentence. Ticket 07 should keep compression and multi-frame only at the level the reported runs need, and walk Alice hiding a short message before any DP.

**Evaluation is a stale 304-pair audit with no LLM judge.** `evaluation.tex` reports one historical configuration comparison (627 project attempts, 554 successes, baseline invoked on 460, 304 decode-verified pairs, 100 post clusters). Grep over `stego_paper/` finds no `LLM judge`, no independent judge protocol, no named qualitative criteria. The section reads like a defensive memo about what the old table is *not* (not decision-grade, not blind recovery, not a security advantage). That honesty is useful. It is not an evaluation writeup. Ticket 08 has to replace this section, not polish Table 1. Related work’s “Evaluation Practices in the Literature” (`related_work.tex` L98–222) will then duplicate whatever the new evaluation explains, which the map already flags.

Related work is a third structural drag: 31-study survey tone, stacked tables, and a closing “research direction” that restates the contribution. Ticket 09 should cut or point, not re-survey, once evaluation exists.

## Abstract

**Already works.** The security non-claim is plain and correctly scoped: the method avoids invisible control characters and does not claim token-level or information-theoretic security (`abstract.tex` L5).

**Worst offenders**

1. The live abstract is one 160-word sentence-stack that names the method, then immediately dumps 554/627 and 304/460 (`abstract.tex` L5). **Diagnosis:** an abstract that leads with audit accounting before a reader knows what Alice does. **Direction:** two or three short sentences on the selection channel in Alice/Bob terms, then one sentence of results once ticket 08 has numbers worth citing. Keep the non-claim.

2. Commented prior abstract (`abstract.tex` L4) is more complete (transform, compression, two layers, verify loop) and also denser. **Diagnosis:** the “previous version” is a workflow dump, the live version is a hedge dump. **Direction:** take the *order* of the old version (corpus, two selections, visible reply, verify, receive) and the *restraint* of the live version (no token-security claim). Do not restore both at full length.

Unslop hits: bold *black-box* in the first clause (#15); *selection channel* is the right term, not slop.

## Introduction

**Already works.** The last sentence of paragraph 2 is the paper’s best motivation line: a comment that is fluent but off-topic is conspicuous (`introduction.tex` L6). Keep that observation. Contributions bullets 1–3 name the real pieces (two-layer selection, shared reconstruction, verify-before-publish).

**Worst offenders**

1. Opening paragraph (`introduction.tex` L4). **Diagnosis:** textbook throat-clearing plus unslop #1/#7: *ostensibly innocuous textual carriers*, *primarily predicated on*, *catalyzed a paradigm shift*, *de novo text generation*, *theoretically achieve high levels of statistical imperceptibility*. **Direction:** one short field sentence (hide a message in ordinary text), one sentence on why synonym tricks fail, one sentence that LLMs now generate the cover instead of editing it. Drop *paradigm shift*.

2. Contribution setup (`introduction.tex` L8). **Diagnosis:** *To address these challenges* (#23 filler) + *elevates the embedding domain* (#1/#26) + synonym cycling among *lexical level*, *semantic level*, *conversational decisions*, *selection channel*, *decodable witness* (#11). The (i)/(ii) mapping in the same paragraph is the actual method and is fine. **Direction:** keep the two-index mapping. Cut *elevates*. Say the visible reply is how Bob sees which Angle was chosen, not a *decodable witness* brand.

3. Contributions bullet 4 (`introduction.tex` L52). **Diagnosis:** the introduction ends on a historical-audit disclaimer instead of a result. **Direction:** after ticket 08, cite the live evaluation (including the LLM judge if that is what the frozen artifacts contain). Until then, do not invent a fourth contribution.

Unslop hits: *serves as* twice (#8); false range *from the lexical level to the semantic level* (#12); title-case section is fine as a section title, the problem is the prose.

## Background

**Already works.** Prisoners’ Problem sentence (`background.tex` L6) is the right Alice/Bob seed. Hallucination paragraph (`background.tex` L14) is concrete: fluent but ungrounded text is a security leak here, not only a quality bug. PSIC explanation (`background.tex` L16–18) is readable and earns its keep because the paper uses that tension later.

**Worst offenders**

1. Opening (`background.tex` L4). **Diagnosis:** forced triad encryption / privacy / concealing (#10), then bold **Steganography** and **Imperceptibility** as if the reader needs a glossary shout (#15). **Direction:** one sentence: this paper is about hiding that communication is happening, not about encrypting the bytes.

2. Formal embedding paragraph (`background.tex` L10). **Diagnosis:** $f_{emb}$, $p_{LM}$, $q$, *steganographic sampling* stacked in one block. That is the literature’s token-sampling model. It is not how *this* method works, and a reader will carry those symbols into methodology. **Direction:** keep one paragraph that token-level methods bias next-token sampling, with the Zhang citation. Drop the cryptographic-mapping diction. CONTEXT.md already says to avoid *steganographic sampling* for this method.

3. LLM primer (`background.tex` L23). **Diagnosis:** Wikipedia-grade Transformer recap (*billions of parameters*, *nuanced linguistic mimicry*). **Direction:** two sentences: an LLM predicts the next token from a prefix; that is why token-level stego can ride sampling, and why this paper does not.

4. White-box vs black-box (`background.tex` L30). **Diagnosis:** promotional rule of three *better text quality, faster generation speeds, and minimal local resource requirements* (#4/#10), *leveraging* (#31), then the converse paragraph that restates the same trade-off. **Direction:** black-box means API-only, no logits. White-box means the sampler can see probabilities. That is the whole distinction this paper needs.

5. Survey blurbs for LLM-Stega, Co-Stega, zero-shot (`background.tex` L32–36). **Diagnosis:** related-work paragraphs living in background, each ending in a fluency/capacity sales clause. **Direction:** one sentence each, or move names into related work and keep background as concepts only.

Unslop hits: boldface on almost every term (#15); *leverage* (#7/#31); title-case subsection headings (#17).

## Related work

This section is where survey-paper English takes over. Many citations are real. The prose around them is the problem. Do not treat the 31-study counts as facts to re-litigate here; the issue is that the reader cannot see the paper’s own method through the survey machinery.

**Already works.** Opening survey triad (`related_work.tex` L4) is a usable map of Majeed / Setiadi / Wang. Watermarking-as-boundary paragraph (`related_work.tex` L72) is clear. Perplexity caveats (`related_work.tex` L105) are specific (length, tokenizer, repetition). Anything/thing tokenization example (`related_work.tex` L306) is the rare concrete picture in this file. The last sentence of that subsection, that this work sidesteps token identity by selecting a reply target and an Angle, is the right bridge into methodology.

**Worst offenders**

1. Gap paragraph (`related_work.tex` L6). **Diagnosis:** *valuable coverage*, *Crucially*, *methodological gap*, *sophisticated CTG frameworks*, *leverage prompt learning*, plus an em-dash definition of *contextual compatibility*. Reads as a thesis-proposal for a survey, not a related-work open. **Direction:** “Prior surveys do not treat fit-to-thread as the main criterion. We do, because that is the channel.” Stop there. Do not announce that no systematic review exists unless the paper is that review.

2. Stegomalware closer (`related_work.tex` L8). **Diagnosis:** *Defensive strategies must evolve accordingly* (#6 formulaic challenge) and *Current research must confront* (#5 vague attribution). **Direction:** delete, or one cited sentence if a specific paper is in the bibliography.

3. Application-domain paragraph (`related_work.tex` L70). **Diagnosis:** one paragraph tries to name generation, rewriting, LLM-Stega, DeepStego, Co-Stega, Hi-Stega, and emotional control. **Direction:** split by family, or keep the table (`tab:app_distribution`) and cut the prose inventory.

4. Capacity-metrics block (`related_work.tex` L113–164). **Diagnosis:** inline-header list of BPT/BPW/ER/UR (#16) plus a five-row “bias categories” table that restates PSIC. This is encyclopedia, and it will collide with the new evaluation’s metric notes. **Direction:** after ticket 08, keep only what a reader needs to interpret *this* paper’s numbers. Point at evaluation for how you compute PPL, KL/JSD, capacity.

5. PSIC revisited (`related_work.tex` L288). **Diagnosis:** *high-entropy chaos*, *camouflaging signals within legitimate statistical noise* (#1/#26). Yang 2020 is a real citation. The metaphor is not. **Direction:** restate PSIC in the same plain terms already used in `background.tex` L16–18. Do not restage it as a thriller.

6. Critical unresolved challenges (`related_work.tex` L318–322). **Diagnosis:** generic gap list (theory, attacks, eval, governance, non-English, deployment) plus *arms race* in the previous subsection (`related_work.tex` L316). **Direction:** keep only gaps this paper actually touches (threaded context, black-box access, evaluation inconsistency).

7. Closing research-direction (`related_work.tex` L327–329). **Diagnosis:** *field in transition* (#1), *not only about X; it also depends* (#9), then a restatement of the contribution. **Direction:** one paragraph: the nearest precedents are context-aware systems (Co-Stega, Hi-Stega); this paper uses context as the payload channel, not as extra fluency. Cut the sermon.

Unslop hits throughout: em dashes (#13), title-case headings (#17), *Furthermore* / *Consequently* (#7), bold method names in running text (#15), rule-of-three metric axes.

## Methodology

The opening is already in the Human Writer Notes voice. Almost everything after System Architecture fights that voice.

**Already works (keep, maybe tighten)**

- Alice/Bob scenario (`methodology.tex` L4–9). Short sentences. Reddit as the case. Transfer to other platforms left as unevaluated. This is the template for the rest of the section.
- Search-term pipeline after the *cornerstone* opener (`methodology.tex` L58, from the second sentence). Counts and backends are concrete: 12–20 queries, `temperature=0`, `first=1`, `count=10`, batches of three, hashes.
- Honest $T_{sync}$ caveat (`methodology.tex` L94): the current receiver does not itself enforce the cutoff. Keep that. It is implementation-true and rare in this file.
- Session-dictionary order (`methodology.tex` L140, the positional-index warning). One of the few compressor sentences a non-specialist can use.
- Layer 1 steps (`methodology.tex` L239–241). Flatten, index, 0 means reply to the post. That is the channel.
- Recoverable vs physical widths (`methodology.tex` L255–259), once. The idea is necessary. The problem is that Layer 1, Layer 2, and this subsection all teach it.
- Verify loop (`methodology.tex` L279–280): if decode fails, resynthesize at nonzero temperature, capped retries. Matches Human Writer Notes.

**Worst offenders**

1. System Architecture (`methodology.tex` L45). **Diagnosis:** immediately undoes the opening. *leverages*, *spatial location*, *thematic subject*, *perceptual naturalness*, *high-level conversational actions*. CONTEXT.md says not to use *spatial embedding* in reader-facing prose. **Direction:** delete the subsection. The opening already said Alice writes a comment. Next sentence can be: bits choose the reply target, then the Angle.

2. Operational Requirements list (`methodology.tex` L48–53). **Diagnosis:** title-case bold labels (#16/#17) for things the Alice/Bob story already implied. **Direction:** four short sentences in the walkthrough (accounts, shared search settings, shared T=0 model, agreed duration). No spec sheet.

3. Temporal Window opener (`methodology.tex` L89). **Diagnosis:** *visualize an identical state of the conversation tree*, *This synchronization mechanism is operationalized to address the processing latency inherent in the sender's agent*. Human Writer Notes say: Alice needs time to work, comments that arrive meanwhile would desync Bob. **Direction:** use that. Then keep the $t_{publish} - T_{sync}$ rule.

4. Protection Transform (`methodology.tex` L130–137). **Diagnosis:** `hmac_xor_v1` / `secure_compact_v2` with HMAC counters, labels `swsec1`/`swsec2`, Base64 shapes. Human Writer Notes never mention this. A reader learning embedding does not need cipher construction. **Direction:** one sentence that an optional protection transform can wrap the payload, with the mode recorded so both sides invert the same one. Move field layout to implementation or an appendix.

5. Bit-Cost Optimal Parse (`methodology.tex` L142–166). **Diagnosis:** $W(m)$, $L_{max}$, backward DP, candidate-set exactness. Real codec, wrong altitude for “how embedding works.” **Direction:** “If the payload is text, a dictionary built from the thread and search docs can shrink it; otherwise it is sent as UTF-8 plus a one-bit flag.” Point to implementation for the DP.

6. Layer titles and one-liners (`methodology.tex` L237, L246). **Diagnosis:** *architectural placement of the steganographic contribution* and *communicative intent* rename reply target and Angle. **Direction:** “Layer 1: which comment we reply to.” “Layer 2: which Angle we talk about.”

7. Channel-widths surplus paragraph (`methodology.tex` L261). **Diagnosis:** self-delimiting units, compressor mode flag, unembedded surplus, audit-assisted recovery, and a forward pointer to multi-frame, all in one block. **Direction:** split. One sentence that leftover bits do not fit in one comment. Multi-frame only if the reported runs actually use it.

8. Multi-Frame Transport (`methodology.tex` L263–273). **Diagnosis:** Elias-gamma, circular $F$ search, zero-padding, post-level vs context-weighted sampler, before the reader has seen a single generated comment. **Direction:** if the evaluation run is single-frame, say longer payloads need more replies and stop. If multi-frame is in the reported artifacts, give Alice sending two comments, then one short note that the planner exists.

9. Synthesis opener (`methodology.tex` L276). **Diagnosis:** *Following the selection of the target context and selected Angle, the sender initiates the cover text synthesis process.* Empty. **Direction:** “A nonzero-temperature LLM writes a few candidate replies from the post, the parent chain, the Angle, and the research excerpts.” The bullet already says that.

10. Decode (`methodology.tex` L314–323). **Diagnosis:** Layer 2 is narrated as a three-step API (reconstruct, shortlist, discriminator) while Layer 1 is a trailing clause. Human Writer Notes: Bob already sees which comment was posted; he shortlists ~50 nearest tangents and asks a T=0 prompt which Angle it is. **Direction:** tell it in that order. Mention that decode settings are configurable (already at L323) without the *inherently deterministic* hedging pile.

Unslop hits: *cornerstone* (#1/#26), *Ensuring that* (#3), em dashes in codec prose (#13), title-case headings (#17), *Recursive Refinement* as a name for “retry” (#11).

## Implementation

**Already works.** Opening stage order (`implementation.tex` L4): data load, research, angle generation, synthesis, decode. Model-role bullets (`implementation.tex` L53–55) match the method: T=0 for reconstruction, nonzero T for synthesis, T=0 discriminator for decode.

**Worst offenders**

1. Architectural Components (`implementation.tex` L6–12). **Diagnosis:** *The system is operationalized through a series of deterministic pipeline stages* is filler, then the bullets repeat methodology. **Direction:** keep only what methodology will not keep after ticket 07 (30k/150k splits, fallback prompt, on-disk hashes).

2. Codec Module paragraph (`implementation.tex` L16). **Diagnosis:** restates the compression contract (*pure functions*, *exact inverses*, *why the pipelines themselves are restricted to I/O*). Fine as implementation, deadly as a second copy if methodology still contains the DP. **Direction:** one subsection after methodology has been cut down. Do not teach $W$ twice.

Unslop hits: title-case headings (#17); inline-header bold stage names (#16).

## Evaluation

Voice problem is secondary. The section is the wrong document.

**Already works (keep as caveats, not as the section)**

- Opening refusal to rank the methods (`evaluation.tex` L4).
- Attempt accounting in `evaluation.tex` L13 (627 / 554 / 94 extraction failures / 460 / 304), which is careful about denominators.
- Failure split (`evaluation.tex` L38) and uniqueness/reuse caveats (`evaluation.tex` L42–44).

**Worst offenders**

1. The section as a whole (`evaluation.tex` L1–44). **Diagnosis:** a historical 304-pair audit memo. No LLM judge, no independent qualitative table, no calculation notes for the metrics the map lists (reliability, divergence, overlap, length beyond the one table). The prose spends its energy on what the table is not. **Direction:** ticket 08 replaces this. New shape: how each reported metric is computed (short), the LLM-judge criteria and table if the frozen artifacts have them, then capacity/reliability/PPL/divergence/overlap/length with the same denominators. Reuse the honesty about audit-assisted recovery and post clustering. Do not keep Table 1 as the only results display.

2. Capacity Analysis (`evaluation.tex` L8–9). **Diagnosis:** formula first, no example. **Direction:** “A thread with 8 reply targets and 32 Angles carries 3+5 bits in one comment.” Then the floors.

3. Trade-off paragraph (`evaluation.tex` L34). **Diagnosis:** readable, but it only interprets the old table (ZLG capacity and PPL, our MATTR and length). **Direction:** after new results exist, interpret those. Do not rewrite this paragraph to claim a win.

No LLM-judge mention anywhere in `stego_paper/`. That is a missing section, not a missing adjective.

## Conclusion

**Already works.** Paragraph 2 (`conclusion.tex` L6) restates the audited numbers and the non-superiority caveat without puffery. Once ticket 08 changes the numbers, this paragraph has to change with them. Until then it is consistent with `evaluation.tex`.

**Worst offender**

1. Paragraph 1 (`conclusion.tex` L4). **Diagnosis:** *redefines the embedding domain as a selection channel* (#1), then a compressed restatement of intro. **Direction:** three sentences in the Human Writer Notes voice: bits choose a reply and an Angle; an LLM writes the comment; capacity is whatever the thread and Angle list uniquely decode. Same facts, lower diction.

## Unslop scan (paper only, no rewrites)

Hits are concentrated in introduction, background, related work, and methodology’s architecture/codec blocks. Evaluation and the methodology opening are mostly clean of the vocabulary list and fail for other reasons (wrong document, wrong order).

| Pattern | Where it shows up |
| --- | --- |
| 1 Puffery | *paradigm shift*, *elevates the embedding domain*, *cornerstone*, *field in transition*, *redefines the embedding domain*, *high-entropy chaos* |
| 3 Superficial -ing | *Ensuring that both Alice and Bob* (`methodology.tex` L58) |
| 4 Promotional | black-box *better / faster / minimal* triad (`background.tex` L30) |
| 5 Vague attribution | *Current research must confront* (`related_work.tex` L8) |
| 6 Formulaic challenge | *Defensive strategies must evolve accordingly* (`related_work.tex` L8) |
| 7 AI vocabulary | *leverage/leveraging*, *Crucially*, *sophisticated*, *enhance*, *Furthermore*, *Consequently* |
| 8 Fancy "is" | *serves as a conspicuous anomaly*, *serves as a decodable witness* |
| 9 Not just X but Y | *security is not only about distributional proximity* (`related_work.tex` L329) |
| 10 Rule of three | intro/background metric triads; black-box benefits; related-work survey axes |
| 11 Synonym cycling | spatial / intent / semantic / communicative / architectural for the same two choices |
| 12 False range | *from the lexical level to the semantic level* |
| 13 Em dash | codec and related-work prose (LaTeX `---` and `---`) |
| 15 Boldface | background and related-work term shouting |
| 16 Inline-header lists | capacity metrics, implementation stages, operational requirements |
| 17 Title-case headings | most `\subsection` titles in methodology, implementation, evaluation |
| 23 Filler | *To address these challenges*, *To ensure that*, *The system is operationalized* |
| 26 Abstract metaphors | *cornerstone*, *architectural placement*, *embedding domain*, *chaos* / *noise* |
| 28 Dense sentences | intro L8, related work L6 and L70, methodology L45 and L261, hmac item L134 |
| 31 Fancy synonym | *leverage* for *use* |

Patterns not really present: decorative emoji, chatbot closers, sycophancy, curly quotes as a voice problem.

## What later tickets should not do

- Do not rewrite the Alice/Bob opening of methodology. Extend it.
- Do not invent an LLM-judge result in evaluation while “unslopping” sentences. Ticket 08 owns those facts.
- Do not keep teaching HMAC, Elias-gamma, and the compression DP in the same pass that teaches reply targeting. That is how the current methodology became long relative to how a reader learns embedding.
- Do not treat related work’s evaluation-practices subsection as sacred once the paper’s own evaluation explains PPL, divergence, and capacity.
- Terminology: follow `CONTEXT.md`. Reply target, Angle, tangent, stego comment, recoverable capacity, temporal window, blind vs audit-assisted recovery, LLM judge. Stop saying *spatial embedding* and *decodable witness* in running prose.
