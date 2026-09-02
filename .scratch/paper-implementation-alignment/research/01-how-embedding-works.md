# How embedding works: live sender and receiver

Status: findings for wayfinder ticket `01-how-embedding-works`
Primary question: what the live sender does, step by step, to turn a payload into a published reply, and what the live receiver does to get the bits back.

“Live” here means the Python pipelines in `stego-side-wing`, not the historical n8n graphs they still name. The code does **not** post to Reddit. “Publish” means: accept a visible comment body and persist it as a local artifact (or, on the multi-frame path, splice it into an in-memory comment tree).

---

## 1. Two encode paths, one reported path

There are two sender entry points:

| Path | Entry | Used by the reported LUCID/ZLG workload runs? |
| --- | --- | --- |
| Single-frame | `StegoPipeline.encode` in `stego-side-wing/src/workflows/pipelines/stego.py` | **Yes.** `scripts/run_actual_workload_e2e.py` (`_run_sample`) calls `stego.encode`. LUCID campaign scripts wrap that runner (`run_lucid_evaluation_campaign.py`). |
| Multi-frame | `StegoPipeline.encode_payload_frames` → `stego_multiframe.plan_payload_frames` / `plan_payload_frames_contextual` | **No, not in the reported evaluation artifacts.** Wired by `scripts/run_publication_benchmark.py` and `scripts/run_multi_frame_*.py`. As of `docs/reports/zlg-sample-audit-2026-07-27.md`, `metrics/benchmark/runs/` was still empty and the publication runner had never been executed. |

`stego-side-wing/.agents/method-and-zlg-benchmark.md` describes the intended research-grade comparison as `run_publication_benchmark.py` (multi-frame). That is the protocol, not a completed reported run.

Default sampler if `WORKFLOW_CONTEXT_SAMPLER` is unset: `post_level_v1` (`infrastructure/config.py` `get_workflow_context_sampler`). Reported LUCID angle prep set `context_weighted_v2` (`docs/reports/2026-08-08-current-research-state.md`). That flag changes **angle-input sampling** at gen-angles time. It does **not** switch `encode()` onto the two-stage parent-then-angles planner. That planner lives only on `plan_payload_frames` (`docs/plans/context-weighted-v2-zlg-benchmark-status.md` §5).

Default encoding profile if unset: `balanced` (`config.py` `DEFAULT_WORKFLOW_ENCODING_PROFILE` / `WORKFLOW_ENCODING_PROFILES["balanced"]`): `payload_transform=plain`, `stego_prompt_style=natural`, `stego_sample_angle_count=1`, `stego_default_max_retries=6`, `decode_semantic_top_n=20`, `stego_llm_temperature=0.7`, `decode_strict_default=False`.

---

## 2. Shared codec (both parties call the same module)

`stego-side-wing/src/workflows/utils/stego_codec.py` is the bit-layer contract. Pipelines orchestrate; they should not fork a second compressor.

Relevant functions:

- `protect_payload` / `unprotect_payload`
- `build_dictionary` / `compress_payload` / `decompress_after_embed_prefix`
- `embed_in_comment_selection` / `embed_in_angle_selection` / `augment_post`
- `get_bit_width`, `_recoverable_width`, `selection_channel_capacity_report`
- `augment_post_with_recoverable_selection_bits` (lossless / multi-frame)
- `recover_payload_with_compressed_full` (audit-assisted)
- `recover_payload_bruteforce_comment_bits` (pure selection-channel)
- `build_multi_frame_stream` / `parse_multi_frame_stream` (Elias-gamma header)

Invisible-Unicode helpers (`extract_invisible_payload`, `strip_invisible_payload`) are read-only leftovers. There is no write-side invisible carrier (`stego_codec.py` comment at the invisible helpers).

---

## 3. Sender: single-frame live path (`StegoPipeline.encode`)

This is what `process_post`, `run_actual_workload_e2e`, and the LUCID 500-style runs actually drive.

Prerequisite: the post already has a non-empty `angles` list (`encode` raises otherwise). Angle generation is a **prior** stage (`GenAnglesPipeline`), not a step inside `encode`.

### 3.1 Payload protection

`encode` reads `get_workflow_payload_transform()` and `get_workflow_encoding_secret()`, then:

```text
embedded_payload = protect_payload(payload, transform, secret)
```

(`stego.py` `StegoPipeline.encode`)

`protect_payload` (`stego_codec.py`):

- `plain` (balanced default): identity.
- `hmac_xor_v1`: 16-byte nonce, HMAC-SHA256 keystream XOR, 16-byte truncated MAC, `swsec1.` + three URL-safe Base64 fields.
- `secure_compact_v2`: zlib-compress first, same cipher under label `swsec2`, one Base64 blob.

The transform is recorded on `sender_audit["payload_transform"]`.

### 3.2 Compression (session dictionary + DP parse)

`encode` calls `_augment_post` → `codec_augment_post` → `augment_post(payload, post)`.

`augment_post`:

1. `build_dictionary(post)` → `build_post_text_dictionary` in `workflows/utils/text_utils.py`.
2. `compress_payload(protected_payload, dictionary)`.

Dictionary order, unrestricted (`build_post_text_dictionary_entries`): post body (`selftext` or `text`), then each `search_results` text (or snippet), then every comment `body` in flattened DFS order (`flatten_comments`). Codec capacity capping is **off by default**: `get_workflow_codec_dictionary_limits_enabled` defaults to `False`. So the compressor usually sees the full unranked source order. That is a **different** dictionary from the angle-generation dictionary (see §5).

`compress_payload`:

- Always considers a UTF-8 bitstream (`to_binary_utf8`).
- Builds a backward DP over payload characters. Literal tokens: flag `0`, length field `encode_int(len, MAX_LITERAL_LEN)` with `MAX_LITERAL_LEN=250` so `W(250)=8` bits, then UTF-8 bytes. Length is in **characters**; the decoder later reads 8-bit groups until that many Unicode chars appear (`_read_utf8_n_chars`).
- Dictionary references only for matches of length **> 2** (`if match_len > 2`). Token: flag `1`, dict index, offset in that document, match length. Widths use `get_bit_width` (`ceil(log2(m+1))` for `m>0`).
- Emits `"0"+utf8` (standard) unless the dictionary parse is **strictly shorter**. Worst-case expansion is one mode bit.

The compressed string is **not** required to fit in one comment’s selection channel. Leftover bits are counted as `remainingBitsUnembedded` and warned; they are not dropped, but they are also not carried by the visible selection. Recovery of the full string then needs the audit copy (`compressed`) or brute-force padding search.

### 3.3 Layer 1: comment-target selection

`_selection_embedding_fields` consumes the **front** of the compressed bitstream:

1. `embed_in_comment_selection(bits, post)`
2. `embed_in_angle_selection(remaining, nested_angles)`

`flatten_comments` is pre-order DFS: visit a node, then walk `replies` (`text_utils.flatten_comments`).

Choice count `C = n+1` (`comment_selection_choice_count`): index `0` = reply to the post; indices `1..n` = the flattened comments. Physical width `w1 = get_bit_width(n) = W(n)`. The encoder takes `w1` bits (`take_bits`, pad with zeros if short), interprets as an integer, and if the integer is `> n` reduces modulo `n+1` (`embed_in_comment_selection`).

If index `> 0`, it builds `pickedCommentChain` by walking parents (`_picked_comment_chain`). That chain is later rendered into the synthesis prompt.

**Physical vs recoverable.** Recoverable comment width is `_recoverable_width(C) = floor(log2(C))` when `C>1`. When `C` is not a power of two, several physical bit patterns alias to the same parent. `encode()` **does not** restrict to the recoverable width. The injective path is `augment_post_with_recoverable_selection_bits`, used by the multi-frame planner (`stego_multiframe.planned_frame`), not by `encode()`.

### 3.4 Layer 2: angle selection (on the post’s existing angle list)

`embed_in_angle_selection` flattens `post["angles"]` (nested groups allowed) via `flatten_angle_groups`, assigning sequential `idx`. Physical width `w2 = get_bit_width(A-1) = W(A-1)`. Index is taken from the next `w2` bits and wrapped `idx %= A` if needed. Recoverable width is `floor(log2(A))`.

`selectedAngle` is the chosen dict (with `idx`). `TangentsDB` is the full flattened list. `totalAnglesSelectedFirst` is `[selected, ...rest]` and is the pool later sampled for generation.

On this path the angle list is **whatever was already on the post**. `encode()` does not regenerate angles after choosing a parent. Context-weighted parent-conditioned codebooks are **not** applied here.

### 3.5 Sample construction and research excerpt

`_build_samples`:

- Takes the first `get_workflow_stego_sample_angle_count()` angles from `totalAnglesSelectedFirst` (balanced default: **1**).
- `needle_finder_batch` matches each angle’s `source_quote` against `post["search_results"]` (`BackendAPIAdapter.needle_finder_batch` → semantic `find_best_match`).
- Attaches `best_match` onto each sample.

### 3.6 Optional extractive shortcut (not the balanced live default)

If `WORKFLOW_STEGO_GENERATION_MODE` is `extractive_zero_kld` or `hybrid_extract`, `_encode_extractive_zero_kld` may copy existing thread text instead of generating. Balanced profile uses `stego_generation_mode="model"`, so this is skipped.

### 3.7 Synthesis

`StegoCandidateEngine.generate_groups` calls `_generate_stego_texts` once per sample.

Prompt construction: `StegoPipeline._build_prompt` → `stego_encode_prompts_for_style(prompt_style)` in `workflows/utils/workflow_llm_prompts.py`.

Balanced `natural` style uses `config/workflow_llm_prompts.json` `stego_encode` (same text as `_DEFAULT_STEGO_ENCODE_SYSTEM` / `_DEFAULT_STEGO_ENCODE_USER`):

- System: stay in character as a Redditor; output **one JSON array of exactly three** non-empty 1–2 sentence strings; thread is source of truth; angle is a hidden routing hint; do not announce labels.
- User interpolates `{best_match}`, `{target_category}`, `{target_tangent}`, `{target_source_quote}`, `{title}`, `{author}`, `{selftext}`, `{chain_section}`.

Other styles (`anchored`, `guided_natural`, `barb`) are code-level variants in `stego_encode_prompts_for_style`. `natural_then_anchor_retry` uses guided_natural on attempt 0 and anchored after (`_prompt_style_for_attempt`). `natural_sharpened` still generates with `natural`.

LLM: model id `qwen/qwen3.5-9b` (`STEGO_LLM_MODEL` = `DECODE_LLM_MODEL`), temperature `get_workflow_stego_llm_temperature()` (0.7 on balanced). Parser requires exactly three strings (`STEGO_LLM_JSON_STRING_COUNT = 3`), as a top-level array or under `texts`/`comments`/`items`/`output`.

### 3.8 Decode-verification retry (and sharpen)

For each attempt `0 .. max_retries` (balanced default max_retries **6**, so **7** synthesis attempts):

1. Generate candidate groups.
2. `StegoCandidateEngine.evaluate` (`stego_candidates.py`):
   - For each candidate text, `DecodePipeline.decode(..., strict_mode=True)`, then if that fails `strict_mode=False`.
   - `contextuality_gate` (`stego_contextuality.py`) must pass.
   - **Accepted** only if strict decode index equals `selectedAngle.idx` **and** the gate passes.
   - Few-shots passed into decode are **other sample groups**, not the other two strings in the same JSON array. With `sample_angle_count=1` the few-shot list is empty.
3. On success, return that visible text (`_encode_success_result`).
4. On failure: if style is `natural_sharpened` **or** retries are exhausted, `_sharpen_until_accepted` revises up to three “promising” candidates with `get_prompts().lucid_revision` (`_revise_candidate_text_contextually`). The revision prompt asks for JSON `{"text": "..."}`. The revised text is re-evaluated the same way.
5. Otherwise increment `retry_count` and regenerate at the same embedding (same parent, same angle, temperature > 0).

This is **not** “rerun encode with no other change” only. The Human Writer Notes describe only the temperature retry. The live pipeline also has a contextuality gate and a lucid revision pass.

`process_post` then, on success, writes an n8n-shaped JSON via `backend.save_object_local(..., step="final-step")`. It never calls a Reddit API.

---

## 4. Angle list construction (before encode)

`GenAnglesPipeline.preview_post` (`workflows/pipelines/gen_angles.py`).

### 4.1 Input dictionary: post-level vs context-weighted

`build_dictionary_bundle_for_post`:

- `post_level_v1` (code default): `build_post_text_dictionary_bundle(post, apply_capacity_profile=True)`. Mid profile caps/reorders search-result and comment blocks (`apply_post_text_dictionary_capacity`: rank, then round-robin with the post body up to `angles_max_input_blocks`).
- `context_weighted_v2`: `build_context_dictionary_bundle(post, selected_parent_id, ContextSamplerConfig)` in `workflows/utils/context_sampler.py`.
  - Always includes the post body.
  - If a parent id is set: that comment, up to `max_ancestors` ancestors, then siblings, children, global fallback, interleaved with research by `comment_weight:research_weight` (defaults 3:1).
  - Research is `rank_frozen_research` against a query built from title, body, selected comment, and ancestors.
  - If `selected_parent_id` is omitted (angle batch prep): parent is the post itself, so “siblings” are top-level comments. The pool is still **not** the exhaustive post-level order.

Reported LUCID angle artifacts used this sampler (`docs/reports/2026-08-08-current-research-state.md`). Prep scripts call `preview_post` **without** a per-encode parent, so the codebook is frozen once per post, not rebuilt after Layer 1.

### 4.2 LLM extraction (temperature 0)

Primary path: `backend.analyze_angles(dictionary, max_results=raw_target)` → `services/angles_service.py` `analyze_angles` → `content_acquisition/angles/angle_runner.py` at `TEMPERATURE = 0` (`workflows/utils/angles_llm_config.py`). Prompts: `src/content_acquisition/angles/systemPrompt.txt` and `userPrompt.txt` (extract `source_quote`, `tangent`, `category`; at least 15 objects). Fallback LLM path (`_generate_angles_llm`) uses `get_prompts().gen_angles` from `workflow_llm_prompts.json`, also temperature 0.

Then `_finalize_angles`: optional TangentsDB builder (`v1` or `lucid`), optional naturalness gate, dedupe, cap to `get_workflow_angles_max_output()` (mid default **32**).

Each retained angle is `{source_quote, tangent, category}` plus optional `source_document`. Flattened `idx` is assigned later at embed time, not here.

---

## 5. Receiver: live pipeline (`ReceiverPipeline.run`)

This is the full reconstruction contract in `workflows/pipelines/receiver.py`. It is **not** what the reported e2e runner calls (see §7).

### 5.1 Locate the carrier

`locate_sender_stego_comment(post, sender_user_id)`: flatten comments, keep those whose `author` or `author_id` matches and whose body is non-empty, return the **first**. Multiple matches log a warning and still take the first.

### 5.2 Pre-sender snapshot

`build_pre_sender_post`: clone the post and delete that comment subtree by id. **No** `t_publish - T_sync` filter exists in this module (confirmed by repo-wide search: `T_sync` is not implemented in Python). The paper already notes that cutoff is an operational duty of the caller.

### 5.3 Rebuild context

`rebuild_context`:

1. `DataLoadPipeline.preview_post` (URL/selftext fetch; fails without selftext).
2. `ResearchPipeline.preview_post` (see §6).
3. `GenAnglesPipeline.preview_post`. If sampler is `context_weighted_v2`, passes `selected_parent_id` from the located comment’s `parent_id`. Otherwise post-level.

Optional drift check against `sender_audit` hashes (dictionary, angles, selected URLs). If `fail_on_context_drift` (default True) and hashes disagree, `run` returns failure at stage `context_drift` without decoding.

### 5.4 Shortlist + discriminator (Layer 2)

`decode_payload` → `DecodePipeline.decode` (`workflows/pipelines/decode.py`).

1. Flatten rebuilt angles (`flatten_nested_angles`).
2. `backend.semantic_search(stego_text, angles, n=semantic_pool_n)` with `semantic_pool_n = min(A, max(top_n, 120))`. Implementation: SentenceTransformer `all-MiniLM-L6-v2`, **cosine** similarity (`services/semantic_service.py` `semantic_search`).
3. Map hits back to canonical indices; take the first `decode_semantic_top_n` mapped hits (balanced default **20**).
4. Lexical rerank: `combined = semantic + 0.25 * lexical_overlap` (`_rerank_decode_candidates`). Human Writer Notes’ “top N~50” is stale; live default is 20.
5. Discriminator prompt from `config/workflow_llm_prompts.json` `stego_decode`:
   - System: choose exactly one object from `{candidates_json}`; each has canonical 0-based `idx`; output a single line `idx: N`.
   - User: few-shots (receiver `run`/`decode_payload` pass **none**, so `[]`) + `### INPUT TEXT:` + the stego body.
6. LLM: **same** `qwen/qwen3.5-9b` and **same** `get_workflow_stego_llm_temperature()` as encode (0.7 on balanced), not temperature 0. Up to `decode_llm_max_tries` (5) transport retries.
7. Parse (`_extract_decode_index`): prefer `idx:` / JSON `"idx"` / last-line digits; then last allowed digit; then 1-based **rank** into the shortlist (`rank_fallback`); if nothing parses, fall back to the top semantic candidate.

Strict vs not:

- Sender verification requires a **strict** parse mode (`json_idx` / `labeled` / `last_line`). Rank fallback and semantic fallback are rejected for acceptance.
- `ReceiverPipeline.run` default `strict_decode` follows `get_workflow_decode_strict_default()` (**False** on balanced).
- If `expected_angle_index` from sender audit disagrees with the discriminator: log; in strict mode raise; in non-strict mode **the audit index becomes authoritative** (`decode_payload`). That is not a pure channel decode.

### 5.5 Recover bits and invert protection

Layer 1 is the observed parent of the sender comment (`comment_selection_index`). Layer 2 is the (possibly audit-overridden) angle index.

If `compressed_full` is supplied — `run` will take `sender_audit.compression.compressed` when the caller did not pass one — `recover_payload_with_compressed_full`:

- Check that the compressed string’s angle-bit slice decodes to the observed index (`angle_bits_decode_to_index`).
- Decompress **the entire** compressed string (`decompress_after_embed_prefix`), not only the `w1+w2` prefix. This is **audit-assisted** recovery (`recovery_source = audit_assisted_compressed_full`).

Else `recover_payload_bruteforce_comment_bits`: guess all `2^{w1}` comment prefixes, angle-bit aliases, and up to `max_padding_bits` (default 256) trailing zeros; keep the shortest round-trip through `compress_payload`. Marked in-code as unsuitable for large payloads.

Then `_decode_configured_payload` → `unprotect_payload`.

---

## 6. Research stage (shared by sender prep and receiver rebuild)

`ResearchPipeline.preview_post` (`workflows/pipelines/research.py`) plus `GenSearchTermsPipeline` (`gen_search_terms.py`).

- Search-term LLM at **temperature 0**. Prompt: `workflow_llm_prompts.json` `gen_search_terms` (minimum 12, aim 15–20 unique queries). User templates fill **title, URL, and post body only** — not the comment section (`GenSearchTermsPipeline._build_prompt`). That disagrees with the Human Writer Notes, not with `methodology.tex`.
- After generation, `_apply_terms_capacity` trims to `get_workflow_research_max_terms()`. Mid/balanced cap is **8** (`WORKFLOW_CAPACITY_TIER_RESEARCH_MAX_TERMS = (4, 8, 12)`). The prompt’s “12–20” is not what the mid profile keeps.
- Each kept term: Google (with Bing fallback) `first=1`, `count=10` (`research.py` `_web_search_google_or_bing` call site).
- Drop missing links, `*.pdf`, duplicate URLs; stop at `get_workflow_research_max_selected_urls()` (mid **24**).
- Fetch surviving URLs in batches of `get_workflow_research_fetch_concurrency()` (default **3**).

Hashes of terms and results are recorded for replay.

---

## 7. What the reported LUCID runs actually decode

`scripts/run_actual_workload_e2e.py` `_run_receiver_decode` does **not** call `ReceiverPipeline.run`.

It calls `receiver.decode_payload` with:

- `rebuilt_post=post` and `pre_sender_post=post` — the **sender’s already-angled post**, no data-load / research / gen-angles rebuild;
- `compressed_full` taken from the encode embedding;
- `strict_mode=False`;
- `expected_angle_index` from the encode result.

Payloads are short ASCII tags: `actual-e2e:{run_id}:{profile}:{sample_idx:04d}:{post_id}` (`_payload_for`). They typically fit in one frame’s physical prefix only with leftover compressed bits stored in the audit.

So the reported ITT numbers are **audit-assisted, pre-rebuilt-context** recoveries after a single-frame `encode()`, not blind `ReceiverPipeline.run()` over a live thread snapshot.

---

## 8. Multi-frame (implemented; not the reported-run protocol)

Only summarize because reported evaluation does not use it.

Sender (`encode_payload_frames`):

1. `protect_payload`, then `compress_payload(..., dictionary=[])` — empty dict forces **standard** mode (`"0"+utf8`). No session dictionary across posts.
2. `build_multi_frame_stream`: Elias-gamma(`F`) + Elias-gamma(payload bit length) + payload bits.
3. Slot size = **recoverable** capacity (`selection_channel_capacity_report`). Search smallest `F` whose first `F` slots cover the stream. Last slot zero-padded.
4. `post_level_v1`: `plan_payload_frames` + `augment_post_with_recoverable_selection_bits`.
5. `context_weighted_v2`: `plan_payload_frames_contextual` — take recoverable **parent** bits, resolve parent, `gen_angles.preview_post(..., selected_parent_id=parent)`, then size the angle field. This is the only encode path that rebuilds the codebook after Layer 1.
6. Each frame: `encode_binary_selection_bits` (skips protect/compress; diagnostic audit flags), then `append_comment_to_tree`.

Receiver `run_multi_frame`: caller-supplied `ordered_frame_refs`; per frame rebuild (all sender comments stripped); decode angle; `recoverable_frame_bit_candidates_from_observations`; concatenate; `parse_multi_frame_stream` (declared `F` must match; padding must be zeros); `from_binary_utf8` after the leading `0`; unprotect.

---

## 9. Human Writer Notes vs live code

`project_paper/AGENTS.md` Human Writer Notes:

| Note | Live code |
| --- | --- |
| Alice/Bob, Reddit-style thread, two layers (parent then angle), generate, verify, publish after an agreed delay | Architecture matches. Delay/`T_sync` is not enforced in `ReceiverPipeline`. Publish is a local artifact write. |
| Search terms from post **and comment section** | Terms from title, body, URL only (`gen_search_terms.py`). |
| Shared LLM T=0 for angles | True for gen-angles and search terms. False for encode and decode discriminator (0.7). |
| Prompt `GKmFzs1YuxtNztna.json` for angles | Live primary prompts are `content_acquisition/angles/{systemPrompt,userPrompt}.txt`. |
| Decode: top N~50 then n8n Decode prompt | Top **20** cosine + lexical rerank; `stego_decode` templates; `idx: N`. |
| If decode fails, rerun encode unmodified (T>0) | Also contextuality gate + lucid revision after the retry budget (or every attempt if `natural_sharpened`). |
| Compression instead of UTF-8/base64 | True as an optional DP dictionary parse; standard UTF-8 is the fallback and the multi-frame-only mode. |

---

## 10. Where `methodology.tex` disagrees with the code

Line numbers refer to `project_paper/stego_paper/sections/methodology.tex`.

### Agrees (keep)

- Black-box, two-layer selection channel; no token-sampling / invisible Unicode as the live write path (`stego_codec.py`, `method-and-zlg-benchmark.md`).
- Research chain shape: T=0 terms, Google `first=1`/`count=10`, drop PDFs and dupes, fetch concurrency 3, integrity hashes (`research.py`).
- `T_sync` is an agreed operational filter; the receiver module does not apply it (tex already says so, ~L94).
- Protection modes `plain` / `hmac_xor_v1` / `secure_compact_v2` match `protect_payload`.
- Compression DP, literal cap 250 chars, matches >2 chars, mode flag `0`/`1`, `W(m)=ceil(log2(m+1))` match `compress_payload` / `get_bit_width`.
- Layer 1: DFS flatten, index 0 = post reply (`embed_in_comment_selection`).
- Physical vs recoverable widths, and that modulo aliasing makes extra physical patterns non-invertible (`_recoverable_width`, wrap in embed functions).
- Multi-frame **code**: empty-dict standard compression, Elias-gamma `F` + length, recoverable slot sizes, context-weighted two-stage planner (`stego_multiframe.py`).
- Synthesis: non-zero T, JSON list of three strings, verify before commit (`_generate_stego_texts`, `StegoCandidateEngine.evaluate`).
- Discriminator: cosine shortlist then LLM; rank-to-shortlist and top-embedding fallback exist in **non-strict** `DecodePipeline.decode`.

### Disagrees or overclaims (fix in the rewrite)

1. **Lossless embedding is not the live single-frame path.** Tex §channel-widths (~L259): “The lossless embedding path enforces this in two steps: it restricts each field's input to its recoverable width, then re-encodes that value at the full physical width.” That is `augment_post_with_recoverable_selection_bits`, used by **multi-frame planning**. `StegoPipeline.encode` → `augment_post` uses **physical** `W(n)` / `W(A-1)` and modulo wrap.

2. **Context-weighted two-stage encode is not what produced the reported LUCID numbers.** Tex §multiframe (~L273): “Under the context-weighted sampler — the mode used to produce the results reported in Section evaluation — the Angle pool instead depends on which parent comment was selected, so the planner works in two stages per frame.” The two-stage planner is `plan_payload_frames_contextual`, only on `encode_payload_frames`. Reported runs call `encode()` on a precomputed angle list (`run_actual_workload_e2e.py`; `docs/plans/context-weighted-v2-zlg-benchmark-status.md` §5). Prep may have used `context_weighted_v2` **once per post**, usually with no selected parent.

3. **Multi-frame is not the reported evaluation protocol.** Tex presents it as the way longer payloads (and evaluation) work. Reported LUCID 500 / TangentsDB 500 used single-frame `encode` + audit-assisted `decode_payload`. `run_publication_benchmark.py` has not produced a frozen reported run (`zlg-sample-audit-2026-07-27.md`).

4. **Search-term count 12–20 is the prompt, not the mid-profile keep set.** Tex ~L58. After T=0 generation, mid capacity keeps **8** terms (`get_workflow_research_max_terms`). High profile keeps 12.

5. **Decode discriminator is not T=0.** Figure prompt (~L295) and “deterministic identification prompt” (~L318) vs `DecodePipeline.decode` using `get_workflow_stego_llm_temperature()` (0.7). Tex later (~L323) admits the stage is configurable / not inherently deterministic — that later sentence is the accurate one; the figure and “deterministic” wording are not.

6. **Retry story is incomplete and the attempt count is wrong.** Tex ~L280 and figure “max 5 attempts”: balanced `stego_default_max_retries=6` (7 loops). Live path also requires `contextuality_gate` and may **revise** text (`lucid_revision`) rather than only resampling. Sender acceptance is **strict** decode, not the relaxed receiver default.

7. **Receiver reconstruction as described is `run()`, not the reported decoder.** Tex ~L316 “locates the comment, removes it, applies temporal cutoff, reruns preprocessing.” `run()` locates and removes, does **not** apply the cutoff, then rebuilds. Reported e2e skips `run()` entirely and reuses the sender post plus `compressed_full`.

8. **Audit override of the angle index is omitted.** Non-strict `decode_payload` can replace the discriminator index with `sender_audit.selected_angle_index`. Reported e2e passes that expected index.

9. **Full-payload recovery from one comment is audit-assisted by default.** Tex ~L261 is actually close (“relies on sender-side metadata”) but the surrounding evaluation claim should not read as blind selection-channel recovery. `ReceiverPipeline.run` itself prefers `compressed_full` from the audit when present.

10. **Two dictionaries are conflated.** Tex session dictionary (~L140) describes compressor order and says the capacity profile “is disabled by default.” True for **codec** `build_dictionary`. Angle generation on `post_level_v1` applies capacity **by default**. Context-weighted uses a parent-conditioned weighted schedule, not “post body, then search, then comments.”

11. **Discriminator prompt paraphrase is wrong.** Tex quote (~L320): *“Identify the specific Angle from the provided candidates... return the index only.”* Actual templates require `idx: N` and pass a JSON candidate list with canonical `idx` (`workflow_llm_prompts.py` `_DEFAULT_STEGO_DECODE_*` / `config/workflow_llm_prompts.json`).

12. **Few-shots.** Decode user template always has a few-shot slot. Receiver leaves it `[]`. Sender fills it only when `sample_angle_count > 1`. Balanced default is 1. Tex never mentions this; it should not invent a few-shot decode protocol.

13. **“Identical LLM (T=0) for angle reconstruction”** (operational requirements / figure) is right for **angles and search terms**, wrong if read as covering the Layer-2 discriminator.

14. **Figure “LLM synthesis (temperature=0.7)”** matches balanced encode. Do not also label decode T=0.7 as T=0 in the same figure.

---

## 11. Paper implications

### The embedding explanation must say

- Alice hides bits by **choosing a reply parent and an Angle**, then generating an ordinary visible reply. The payload is not in zero-width characters or in token-sampling bias.
- Before that, the payload may be protected (`plain` by default) and compressed with a thread/research dictionary; leftover compressed bits beyond `w1+w2` stay in sender metadata, not in the comment.
- Layer 1 numbering is a deterministic DFS flatten; 0 replies to the post.
- Layer 2 is an index into a shared Angle list `{category, source_quote, tangent}` built from a hashed research corpus plus thread text, with the Angle LLM at temperature 0.
- Physical width `ceil(log2(choices))` vs recoverable `floor(log2(choices))` must stay distinct. Capacity claims use recoverable widths (`method-and-zlg-benchmark.md`).
- The sender samples several candidate replies (three JSON strings per sample), locally decodes them with the **same** shortlist+discriminator used at receive time, and only publishes a candidate that **strict-decodes** to the selected Angle and passes the contextuality gate. On failure it retries at T>0 and may revise a near-miss (`lucid_revision`).
- The receiver’s Layer-2 decoder: MiniLM cosine shortlist (default 20), lexical rerank, then a T=0.7 `idx: N` prompt — not a T=0 deterministic oracle.
- What the **reported** LUCID numbers actually measured: single-frame `encode` + audit-assisted `decode_payload` on a pre-angled post, context-weighted used at **angle prep**, not the two-stage multi-frame planner.

### The embedding explanation must stop saying

- That the live encode path writes only recoverable/lossless selection bits (that is multi-frame planning).
- That reported evaluation used multi-frame transport or parent-conditioned Angle rebuild at encode time.
- That the discriminator runs at temperature 0, or that decode is “deterministic” in the same sense as angle generation.
- That failed verification only “reruns synthesis unchanged” for a budget of 5, with no gate and no revision.
- That the receiver in the reported runs rebuilds research+angles from a `T_sync`-filtered snapshot and recovers the payload from selection observations alone.
- That search-term generation keeps 12–20 queries under the balanced/mid profile, or that comments are an input to term generation.
- That a quoted “return the index only” prompt is the live decode contract.
- That compression’s session dictionary and the Angle-input sampler are the same object.
- That Alice’s agent posts to Reddit; the live sender writes a local stego artifact.

If the methodology keeps a multi-frame subsection, label it as an implemented protocol and planned publication-benchmark path, not as the pipeline behind the current LUCID/ZLG tables.
