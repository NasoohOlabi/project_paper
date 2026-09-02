# Where the English paper disagrees with the live implementation

Question: section by section, where does the English paper misstate, overclaim, or omit something the live `stego-side-wing` implementation does?

Primary axis: paper claim vs live code. Human Writer Notes (intended Alice/Bob story) and `method-and-zlg-benchmark.md` are used as the intended method story, not as a second implementation.

## Sources

- Paper: `project_paper/stego_paper/sections/{abstract,introduction,background,related_work,methodology,implementation,evaluation,conclusion}.tex`
- Sender: `stego-side-wing/src/workflows/pipelines/stego.py`
- Receiver: `stego-side-wing/src/workflows/pipelines/receiver.py`
- Decode: `stego-side-wing/src/workflows/pipelines/decode.py`
- Codec: `stego-side-wing/src/workflows/utils/stego_codec.py`
- Sampler: `stego-side-wing/src/workflows/utils/context_sampler.py`, `infrastructure/config.py`
- Method note: `stego-side-wing/.agents/method-and-zlg-benchmark.md`
- Intended story: `project_paper/AGENTS.md` Human Writer Notes
- Numbers: `stego-side-wing/docs/reports/2026-07-30-context-weighted-v2-zlg-benchmark.md`, `docs/reports/2026-08-08-current-research-state.md`, `docs/reports/2026-08-29-independent-llm-judge-results.md`

## Highest-severity first

These are the mismatches that would make a reader misunderstand the live system. Details and quotes follow by section.

| Issue | Severity | Paper location | Live code |
| --- | --- | --- | --- |
| Default `encode()` uses physical widths + modulo aliasing, not the lossless recoverable path | **wrong** | methodology channel-widths | `stego.py` → `codec_augment_post`; recoverable path is multi-frame only |
| Receiver does not enforce \(T_{sync}\) | **wrong** (body contradicts itself; caption still claims enforcement) | methodology temporal window; decode step 1 | `receiver.py` `build_pre_sender_post` only removes the sender comment |
| Decode discriminator runs at encode temperature 0.7, not temperature 0 | **wrong** | implementation model config; figure prompt | `decode.py` `get_workflow_stego_llm_temperature()` |
| Default sampler is `post_level_v1`; context-weighted is opt-in. Decode of Layer 2 under v2 needs the observed parent first | **omission** / **overclaim** of a shared post-level Angle list | methodology Layer 2 and Decoding | `config.py` default; `receiver.rebuild_context(selected_parent_id=...)` |
| Default receiver is audit-assisted when `sender_audit` is on the artifact | **overclaim** of no side-channel | introduction contribution 2 | `receiver.run` reads compressed bits and expected angle from audit |
| Live `encode()` retries, then **sharpens** on last attempt; paper says regenerate unchanged | **omission** | methodology verification | `stego.py` `_sharpen_until_accepted` |
| Multi-frame receiver needs `ordered_frame_refs`; it does not discover frames from the public thread | **omission** | methodology multi-frame | `receiver.run_multi_frame` |
| Search term count, search backend, and URL fetch are not the fixed Google/crawl4ai/12–20 story | **wrong** / **overclaim** | methodology search | capacity cap 8 on balanced; HTTP-first; DuckDuckGo/Bing fallbacks |
| Evaluation mixes the 2026-07-30 run with a rewritten ZLG failure taxonomy, omits the 2026-08-29 judge, and uses rescaled BERTScore the source report does not print | **stale-number** / **wrong** | evaluation, abstract, conclusion | July 30 report vs `evaluation.tex` |

---

## Abstract

### A1. Recovery is described as depending on a supplied snapshot, which is closer to the code than the methodology later is

> “The receiver rebuilds supplied pre-publication context and recovers the selected choices; exact recovery depends on shared operational parameters, synchronized inputs, and the supplied snapshot boundary.”

**Severity:** none on the snapshot wording (this is the honest live contract). Contrast with methodology decode step 1, which then claims the receiver itself applies \(t_{publish}-T_{sync}\).

**Code:** `ReceiverPipeline.run` locates the sender comment, clones the post with that comment removed (`build_pre_sender_post`), and rebuilds. There is no timestamp cutoff.

### A2. Historical attempt counts are kept, but they mix two accounting stories

> “554 of 627 project-side attempts succeeded, while the baseline lane was invoked on 460 attempts and accepted and decode-verified 304.”

**Severity:** **stale-number** (accounting mix).

**Report:** `2026-07-30-context-weighted-v2-zlg-benchmark.md` reports ZLG attempted on all 554 successes and accepted 304 (54.9%). The 460 / 66.1% denominator (dropping 94 cover-extraction failures from ZLG’s trial count) is the later overhaul taxonomy (`docs/results/zlg-overhaul-handoff-20260731.md`), not the July 30 table the rest of the paper’s metrics come from. The abstract is internally consistent with `evaluation.tex`’s rewritten denominator, but not with the frozen July 30 “Total attempted 554” table.

### A3. Compression, protection modes, and context-weighted pools are omitted at abstract level

The commented previous abstract named dictionary compression and two-layer indices. The live abstract does not. That is acceptable for a high-level abstract **if** the main text is accurate; it is not, so the abstract currently under-describes the channel the evaluation actually used (`context_weighted_v2`).

**Severity:** **omission** (low if methodology is fixed; high while methodology still reads as a single shared Angle list).

---

## Introduction

### I1. “No side-channel metadata exchange”

> “A deterministic reconstruction pipeline (thread + reproducible research) that enables sender/receiver parity without white-box model access or side-channel metadata exchange.”

**Severity:** **overclaim**.

**Code:** `ReceiverPipeline.run` (`receiver.py` ~812–851) pulls `sender_audit` from the post JSON and, unless the caller passes something else:

- uses `_compressed_full_from_audit` as `compressed_full` (recovery source `audit_assisted_compressed_full`);
- uses `selected_angle_index` from the audit as `expected_angle_index`;
- in non-strict mode, **overrides** a disagreeing semantic decode with the audit index (`authoritative_idx = expected_angle_index`).

`get_workflow_decode_strict_default()` is **False** on the `balanced` profile used in the reported run. Blind public-thread recovery is a mode, not the default implemented `run()`.

Human Writer Notes assume Bob reconstructs from the public thread plus shared search/LLM settings, not from a sender audit blob.

### I2. Token / white-box leftover is only in the figure prompt, not the published caption

The figure prompt for `fig:token-vs-intent` still says “often needs white-box logits”. The published caption is conceptual and does not claim the authors’ method uses logits.

**Severity:** **omission** if the PDF figure still shows that badge; not a LaTeX-body error.

### I3. Two-layer story matches the intended method; it does not say the live default encode is aliased

> “bits map to (i) the index of the reply target … and (ii) the index of a context-conditioned Angle”

**Severity:** **omission**. The introduction presents an injective selection channel. Live `StegoPipeline.encode` consumes physical bit widths via `codec_augment_post`, which modulo-folds out-of-range indices (`stego_codec.embed_in_comment_selection` / `embed_in_angle_selection`). The injective “lossless” writer is `augment_post_with_recoverable_selection_bits`, used by `stego_multiframe.py`, not by `encode()`.

`method-and-zlg-benchmark.md` already warns not to count aliased patterns as useful payload. The paper’s introduction does not.

---

## Background

### B1. Formal model is token-level steganographic sampling

> “At each generation step, rather than sampling freely from the language model's conditional distribution \(p_{LM}\), the embedding function \(f_{emb}\) **restricts or modifies** the token selection process”

**Severity:** **omission** (leftover white-box / token-sampling language). This paragraph defines *the field’s* generative methods, not this system. It is easy to read as the paper’s own embedding function, especially because the next subsection says this trade-off “directly motivates the black-box design adopted in Section methodology.” The live method does not modify next-token sampling; it selects a parent and an Angle, then calls a black-box LLM.

### B2. No live-implementation disagreement beyond that framing

Background does not describe \(T_{sync}\), compression modes, or the decode contract. No code contradiction specific to this section besides the sampling language above.

---

## Related work

### R1. Token-gap sidestep is true for the channel, overstated as a complete decode contract

> “Because this work embeds payload through reply targeting and angle selection rather than through raw token identity … it sidesteps the detokenization-retokenization gap entirely: the sender and receiver only need to agree on which discrete angle or reply target was selected”

**Severity:** **overclaim** of agreement. Live Layer-2 agreement is a **semantic shortlist + LLM at temperature 0.7**, plus optional audit override — not a discrete index the receiver can read off the text. Layer 1 *is* discrete (parent of the published comment). Layer 2 is not.

### R2. Comparison paragraph omits audit-assisted recovery

> “In the tested configuration, the baseline had higher recoverable capacity and lower GPT-2 perplexity … The comparison is conditional on accepted outputs … it does not establish a security advantage”

**Severity:** **omission**. Evaluation later admits project-side rows used audit-assisted compressed-bitstring recovery. This related-work close does not. A reader can take “recoverable capacity” as blind receiver capacity.

### R3. No other live-pipeline claims

Tables and survey counts are literature synthesis, not implementation claims. Out of scope for this ticket except where they preview the authors’ method.

---

## Methodology

This section carries most of the implementation disagreements.

### M1. Temporal window: intended story vs live receiver (and vs the paper’s own caveat)

**LaTeX (operationalized as if implemented):**

> “Upon identifying the stego-contribution published at \(t_{publish}\), Bob filters the thread's historical state to include only those comments established prior to \(t_{publish} - T_{sync}\).”

**LaTeX (later, correct):**

> “The current receiver removes the sender comment and rebuilds from the supplied post, but does not itself enforce this timestamp cutoff”

**Caption (still claims enforcement):**

> “Bob's reconstructed thread state matches Alice's by agreeing on \(T_{sync}\) and filtering comments relative to \(t_{publish}\).”

**Severity:** **wrong** in the enumerated protocol and caption; the caveat is accurate.

**Code:** `build_pre_sender_post` / `build_pre_sender_post_all` only drop sender comments by id/author. `created_utc` is copied onto multi-frame observations, never used as a cutoff. No `T_sync` symbol exists in `src/workflows`.

**Human Writer Notes:** the duration *is* the intended method (“the receiver can simply take a snapshot … filter the comment by their creation date to the stegotext creation date minus the agreed duration”). The paper’s caveat matches the code; the protocol list and figure caption still tell the intended story as if it were implemented.

### M2. Search stage: 12–20 queries, Google only, crawl4ai, comments omitted

> “A search-term generator first extracts 12--20 unique queries from the post title, body, and URL … Each query is then executed through the Google Custom Search backend with a fixed request shape (`first=1`, `count=10`) … fetched in batches of three. Content extraction uses a crawl4ai-based adapter”

**Severity:** **wrong** / **overclaim**.

| Claim | Live |
| --- | --- |
| 12–20 queries | Prompt *asks* for “Minimum 12 queries (aim for 15-20)” (`workflow_llm_prompts.py`). Balanced/mid capacity then **trims to 8** (`WORKFLOW_CAPACITY_TIER_RESEARCH_MAX_TERMS = (4, 8, 12)`; evaluation used `balanced`). |
| Title, body, URL only | Matches `GenSearchTermsPipeline` (no comment bodies). Human Writer Notes wanted terms from “the post and comment section”; paper and code both omit comments. |
| Google Custom Search only | `ResearchPipeline._web_search_google_or_bing` tries Google, then DuckDuckGo, Yahoo News, Google News RSS, Bing News RSS, Bing. |
| Batches of three | Default fetch concurrency is 3 (`DEFAULT_WORKFLOW_RESEARCH_FETCH_CONCURRENCY`). This part is true. |
| crawl4ai adapter | `get_workflow_url_fetch_http_first()` defaults **on**; crawl4ai is the fallback after plain HTTP extraction (`content_acquisition/scraper.py`). |

### M3. Protection modes: mostly right; wire prefixes omitted

> “`hmac_xor_v1`: … Nonce, ciphertext, and tag are each Base64-encoded (URL-safe) and joined with dots into one string.”
> “`secure_compact_v2`: … the three raw fields are concatenated as bytes before Base64 encoding”

**Severity:** **omission**.

**Code:** outputs are `swsec1.<nonce>.<ct>.<mac>` and `swsec2.<b64(nonce||ct||mac)>` (`SECURE_PAYLOAD_V1_PREFIX` / `V2_PREFIX`). HMAC labels `swsec1` / `swsec2` match. Default transform on `balanced` is `plain`, which the paper does call the default.

### M4. Compression DP is largely accurate; codec dictionary is not the Angle sampler

The token grammar, 250-char literal cap, 3-char minimum match, mode flag, and “capacity profile disabled by default” for the **codec** dictionary match `compress_payload` / `get_workflow_codec_dictionary_limits_enabled()` (default False).

**Severity:** **omission**. Under `context_weighted_v2`, **Angle inputs** are parent-conditioned (`build_context_dictionary_bundle`), but **payload compression** still uses `build_post_text_dictionary` (post-level order). The paper’s session-dictionary subsection never says those two dictionaries can differ.

### M5. Default encode is not the lossless path the paper describes

> “The *lossless* embedding path enforces this in two steps: it restricts each field's input to its recoverable width, then re-encodes that value at the full physical width before writing it.”
> “Capacity claims in Section evaluation use these recoverable widths.”

**Severity:** **wrong** for the live sender; **ok** as an accounting statement for the table.

**Code:**

- `StegoPipeline.encode` → `_augment_post` → `codec_augment_post` → physical `get_bit_width` + modulo (`embed_in_comment_selection`, `embed_in_angle_selection`).
- `augment_post_with_recoverable_selection_bits` is what the paper describes; `stego_multiframe.py` uses it. The single-comment path used for the 627/554 run is `encode()`, not multi-frame.

Remaining compressed bits are reported as unembedded and, in `ReceiverPipeline.decode_payload`, recovered via audit-assisted `recover_payload_with_compressed_full` when the audit bitstring is present. That matches the paper’s later sentence about surplus bits, but contradicts the claim that the embedding path itself is injective.

### M6. Context-weighted Angle pools: true for the reported run, not the default, and not the main decode recipe

> “The description above assumes a static Angle pool shared by all frames (the `post-level` sampler). Under the *context-weighted* sampler — the mode used to produce the results reported in Section evaluation — the Angle pool instead depends on which parent comment was selected”

**Severity:** **omission** in Layer 2 / Decoding; the multi-frame paragraph is the only place this is stated.

**Code:**

- Default: `WORKFLOW_CONTEXT_SAMPLER` unset → `post_level_v1` (`config.py`).
- Reported run did set `context_weighted_v2` (July 30 report).
- Receiver: `rebuild_context(..., selected_parent_id=located.parent_id)` then `GenAnglesPipeline.preview_post(..., selected_parent_id=...)`. Layer 2’s codebook is rebuilt **after** observing Layer 1. The Decoding subsection still says both parties “reproduce the same ordered Angle list” from the filtered snapshot alone.

### M7. Verification loop: “rerun without modification” omits sharpening, prompt-style switching, and retry counts

> “If the simulation fails to recover the intended Angle, the sender re-executes synthesis without changing the embedding parameters. … The retry loop is capped by a fixed attempt budget.”

Figure prompt: “Synthesize 3 JSON comments (T=0.7)” and “max 5 attempts”.

**Severity:** **omission** / **stale-number** for the budget.

**Code:**

- Three JSON strings: matches the encode system prompt.
- Temperature 0.7: matches `STEGO_CYCLE_LLM_TEMPERATURE`.
- Retry budget: `balanced` profile `stego_default_max_retries=6`; helper default 4; not 5.
- On failure, `encode` may switch prompt style (`natural_then_anchor_retry` → `guided_natural` then `anchored`) and, on the last attempt (or always for `natural_sharpened`), call `_sharpen_until_accepted` (LUCID revision path). Paper: regenerate only.

Human Writer Notes: “if the decode fails I simply rerun the encode without any modification”. The paper follows the intended story; the live pipeline no longer does only that.

### M8. Decode contract: prompt, shortlist, temperature, lexical rerank, audit override

> “A semantic similarity model shortlists the top-\(N\) Angles”
> “Identify the specific Angle from the provided candidates... return the index only.”
> “If the discriminator returns a 1-based rank rather than a raw index, the pipeline maps the rank back to the shortlist; otherwise it falls back to the top semantic match. The decode temperature and shortlist size are configurable, so this stage is not inherently deterministic.”

**Severity:** **wrong** on the default temperature implied by the figure and Implementation; **omission** of the real decoder.

**Code (`decode.py`):**

- Semantic pool is `min(len(angles), max(top_n, 120))`, then truncated to `decode_semantic_top_n` (default **20**, not Human Writer’s “N~50”).
- Candidates are **reranked** with lexical overlap (`semantic + 0.25 * lexical`) before the LLM sees them. Paper never mentions this.
- Discriminator prompt asks for `idx: <integer>` of the canonical global index, not “the index only” in the paper’s paraphrase.
- LLM temperature is `get_workflow_stego_llm_temperature()` (**0.7**), same as encode. Methodology text admits configurability; Implementation still says temperature 0.
- Rank fallback and top-semantic fallback exist as described.
- `expected_angle_index` from audit can replace the semantic result in non-strict mode — not mentioned in this subsection.

### M9. Decode step 1 still claims the temporal cutoff

> “The receiver locates the candidate stego comment, removes it from the thread, applies the temporal cutoff (\(t_{publish} - T_{sync}\)), and reruns deterministic preprocessing”

**Severity:** **wrong**. Same as M1. This paragraph was not updated when the caveat was added above.

### M10. Multi-frame header vs leftover framed-bit codec; discovery

Elias-gamma count + length, empty compression dictionary, zero padding, reject on count/padding mismatch: **matches** `build_multi_frame_stream` / `parse_multi_frame_stream` / `_prepare_multi_frame_payload_bits`.

**Severity:** **omission**.

- Live `run_multi_frame` requires caller-supplied `ordered_frame_refs` (post_id, comment_id). The public thread does not name which comments are frames or their order.
- `frame_payload_bits` / `FRAME_MAGIC` / CRC32 still exist in `stego_codec.py` but are **not** the live multi-frame path. The paper correctly describes Elias-gamma; it should not be confused with the unused framed-bit helper. Invisible-Unicode extractors also remain as read-only legacy (`extract_invisible_payload`); the paper is right that the current channel does not write them.

### M11. Sender location is “first matching author comment”, not a unique agreed duration

**Severity:** **omission**. `locate_sender_stego_comment` returns the first non-empty comment whose author matches `sender_user_id`, and logs if there are several. The intended duration window is what would disambiguate late comments; the live locator does not.

---

## Implementation

### P1. “A series of deterministic pipeline stages” including stego and decode

> “The system is operationalized through a series of deterministic pipeline stages.”
> Caption: “each stage is deterministic and replayable where required for sender--receiver parity.”

The opening paragraph of the section is more careful (“synthesis and semantic decoding remain configurable”). The bullet list and caption are not.

**Severity:** **overclaim**.

### P2. Angle chunking 30k / 150k

> “Long inputs are split into 30k-character segments and batched up to 150k characters.”

**Severity:** **wrong**.

**Code:** `MAX_CHARS_PER_TEXT = 30_000` is right. Default batch cap is **80_000** (`_effective_max_chars_per_prompt()`, unless `ANGLES_MAX_CHARS_PER_PROMPT` is set). Not 150k.

### P3. Discriminative prompt at temperature 0

> “Semantic matching and decode: … a deterministic discriminative identification prompt (e.g., `temperature=0`)”

**Severity:** **wrong**. Decode uses the shared stego-cycle temperature 0.7 (`llm_temperatures.py`, `decode.py` line with `get_workflow_stego_llm_temperature()`).

### P4. Codec contract paragraph is accurate for the bit layer; it is not the whole decode contract

The shared `stego_codec.py` for compression, \(W\), and physical vs recoverable widths is correctly described. Pipelines are **not** “limited to I/O, caching, and orchestration”: they own parent-conditioned angle regen, semantic search, LLM decode, audit override, and sharpening.

**Severity:** **overclaim** of the module boundary.

### P5. Live modes omitted

Implementation does not mention:

- `WORKFLOW_CONTEXT_SAMPLER` (`post_level_v1` vs `context_weighted_v2`);
- encoding profiles (`balanced` / `robustness` / `capacity` / `security`);
- `extractive_zero_kld` generation;
- TangentsDB / LUCID critic-revision (`WORKFLOW_TANGENT_DB_BUILDER`, default `legacy`);
- HTTP-first URL fetch;
- search fallbacks.

**Severity:** **omission**. These are live knobs. The reported table is one (`context_weighted_v2` + `balanced`) configuration.

---

## Evaluation

Numbers below are checked against `docs/reports/2026-07-30-context-weighted-v2-zlg-benchmark.md` unless noted.

### E1. Capacity formula matches the method note; the run’s 15.14 vs 16.00 is the capacity-matched context-weighted table, not the 2026-07-26 18.66 vs 76.70 audit

> “For one recoverable frame, the selection-channel capacity is \(\lfloor\log_2 C\rfloor + \lfloor\log_2 A\rfloor\)”
> “In this benchmark the Angle list was capped at 32 entries, so the angle component contributed at most 5 recoverable bits per frame.”
> Table: 15.14 vs 16.00 bits/comment; PPL 68.15 vs 53.70; MATTR 99.36 vs 98.45; word count 22.4 vs 17.3

**Severity:** **none** for those cells vs the July 30 report. **stale-number** if a reader maps this table onto `zlg-benchmark-audit-2026-07-26.md` (18.66 vs 76.70, 47 posts, GPT-2 91.52 vs 34.66). The paper does say this is a historical configuration comparison; it should not be cited as the method note’s corrected 18.66 figure.

ZLG’s 16.00 is **capacity_matched**, not ZLG’s native token-channel capacity. The paper says this. Good.

### E2. ZLG failure taxonomy disagrees with the July 30 report

July 30 §4:

- ZLG attempted 554, accepted 304, failed 250
- 134 quality-gate, 94 cover-sentence extraction, 22 prompt-leakage
- Our method 73 failures = 70 `receiver_angle_mismatch` + 3 `generation_failure`

**Paper paired-results paragraph:**

> “the baseline was invoked on 460 … accepted 304 (66.1%) … Of the 156 genuine baseline failures, 133 were quality-gate rejections, 22 were prompt leakage, and one was a server fault.”

**Paper failure-analysis paragraph:**

> “the 250 rejected attempts consisted of 134 quality-gate failures, 94 failures caused by insufficient cover sentences, and 22 prompt-leakage detections.”

**Severity:** **wrong**.

- 133 vs 134, and a “server fault” that the July 30 report does not list.
- 66.1% / 460 is the overhaul rewrite; 54.9% / 554 is the frozen report. The paper uses both stories in one section (460 in the results paragraph, 250 = 134+94+22 in the failure paragraph).

Project-side 70 + 3 matches July 30. Keep those.

### E3. Audit-assisted vs blind recovery is disclosed here (good) and contradicts the introduction

> “The project-side paired rows used audit-assisted compressed-bitstring recovery, so they validate selection/angle artifacts rather than demonstrating blind recovery of the complete compressed payload.”

**Severity:** none as an evaluation caveat. It is the sentence the introduction and related-work close need.

**Code:** `recovery_source = "audit_assisted_compressed_full"` when `compressed_full` is supplied; the comparison dataset used that path (`zlg-sample-audit-2026-07-27.md` also recorded 304/304 audit-assisted on an earlier artifact).

### E4. BERTScore cells are not the July 30 report’s F1

July 30: BERTScore F1 0.842 vs 0.848 (unrescaled, “comparable”).

Paper table: Precision 0.083 vs 0.154, F1 0.068 vs 0.114, “BERTScore is baseline-rescaled.”

Current scorer does set `rescale_with_baseline=True` (`paired_quality_metrics_service.py`). Those small numbers can be a later recompute, but they are **not** in the July 30 report the rest of the table copies, and Precision Holm \(p\approx0.0045\) is not in that report either.

**Severity:** **stale-number** / mixed artifact. Ticket 03 should pin the file. Do not treat 0.083 / 0.154 as coming from the same frozen table as 15.14 / 68.15.

### E5. Independent LLM judge and later LUCID ITT runs are omitted

`2026-08-08-current-research-state.md`: LUCID context-weighted 381/500 (76.2% ITT); TangentsDB-v1 371/500 (contaminated research cache). `2026-08-29-independent-llm-judge-results.md`: 244 unique-post pairs, five judge criteria.

**Severity:** **omission**. The map for this alignment work says evaluation must include the independent LLM judge. The English evaluation section currently does not. Related-work also claims the paper “report[s] naturalness, distributional divergence, and operational reliability jointly” while dropping KL/JSD, the judge, synthetic detection, and robustness — metrics the method note still lists.

### E6. Unique texts 244/304, 167 posts, 35 posts × 10 samples

These match July 30 §5. **Severity:** none.

---

## Conclusion

Repeats 627 / 554 / 460 / 304, 16.00 vs 15.14, 53.70 vs 68.15, MATTR 99.36 vs 98.45, and the audit-assisted / reuse caveats.

**Severity:** **stale-number** only insofar as it inherits E2’s 460-denominator mix. The “not decision-grade / not blind end-to-end superiority” close matches `method-and-zlg-benchmark.md`. It still does not mention that live `encode()` is not the lossless writer, that decode is not temperature 0, or that \(T_{sync}\) is not enforced.

---

## Human Writer Notes vs paper vs code (intended story)

These are not extra paper-vs-code bugs if both paper and code omit them; they are the method the paper is supposed to tell.

| Intended (AGENTS.md) | Paper | Live code |
| --- | --- | --- |
| Search terms from post **and comments** | Title, body, URL only | Title, body, URL only |
| Shared search engine **and sites** | Fixed Google CSE shape | Google then several fallbacks; HTTP-first fetch |
| Shared LLM temperature 0 for Angles | Yes | Angles temperature 0 (`ANGLES_TEMPERATURE`) |
| Decode: top N~50 closest tangents, then a prompt | top-\(N\), unspecified; figure “top 20” | default shortlist 20, pool up to 120, lexical rerank, then LLM |
| Failed encode → rerun unchanged (T>0) | Yes | Retry plus optional prompt switch and sharpen |
| Agreed duration; receiver filters by `created - T_sync` | Described, then caveated; caption still claims it | Not implemented |
| Text payload compression instead of raw UTF-8 | Full DP section | Implemented; default `plain` protection; dictionary mode only if shorter |

---

## Leftover white-box / token-sampling language (index)

| Location | Language | Verdict |
| --- | --- | --- |
| background embedding function / steganographic sampling | token restriction of \(p_{LM}\) | leftover field definition; do not let it describe this method |
| background / related_work white-box vs black-box | accurate as literature | OK |
| introduction figure prompt “white-box logits” | prior-work panel | OK if the figure is clearly “typical token methods” |
| related_work detokenization gap | “only need to agree on which discrete angle” | overclaim for Layer 2 |
| methodology / implementation | black-box + visible witness | matches the live carrier; decode is still a stochastic LLM |
| `stego_codec.py` invisible-payload helpers | not in the paper | correctly omitted from the write path; keep the paper from implying they were never in the repo |

---

## What the paper already gets right (do not “fix” these into errors)

- Two-layer selection channel (parent index + Angle index); visible text as witness; no invisible write path in current encode.
- Physical vs recoverable widths, and not counting modulo aliases as capacity — as **accounting**, this matches `selection_channel_capacity_report` / the method note.
- Surplus compressed bits need multi-frame or audit-assisted recovery.
- Evaluation used `context_weighted_v2`, angle cap 32, `balanced`, capacity-matched ZLG, post-clustered 100 posts, 244 unique our-method texts, 70 angle mismatches + 3 generation failures.
- Shared codec module for protect/compress/embed widths.
- Protection modes `plain` / `hmac_xor_v1` / `secure_compact_v2` exist as described, aside from the `swsec1.` / `swsec2.` prefixes.

---

## Suggested rewrite order (for later tickets; not edits)

1. Methodology decode + temporal window: one protocol (intended \(T_{sync}\)) vs one implemented receiver (supplied snapshot, no cutoff).
2. Embedding: default `encode()` is physical+modulo; recoverable writer is multi-frame; evaluation capacity is recoverable accounting, often audit-assisted.
3. Context-weighted as the reported run’s codebook rule, including parent-first regen; default remains `post_level_v1`.
4. Decode contract: shortlist 20, lexical rerank, `idx: N` at temperature 0.7, audit override when present.
5. Evaluation: one frozen artifact; one ZLG denominator; BERTScore from that same file; add or explicitly defer the 2026-08-29 judge.
