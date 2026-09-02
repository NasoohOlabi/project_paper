# How each reported metric is calculated

Primary sources are the live runners and scoring modules, not the paper prose.
Two evaluation pipelines exist and **do not share one capacity or word-count definition**.

| Pipeline | What it is | Entry points |
| --- | --- | --- |
| Historical paired audit (current `evaluation.tex` table) | 304 accepted pairs, then post-clustered over 100 posts | `scripts/build_zlg_method_comparison_dataset.py`, `scripts/run_paired_reference_metrics.py`, `scripts/recompute_paired_bertscore.py` |
| Publication runner (live protocol) | Frozen-manifest, one attempt per post per method | `scripts/run_publication_benchmark.py`, `scripts/analyze_publication_results.py` |
| Codex LLM judge | Five blinded criteria on a comparison dataset | `src/services/judge_slate_service.py`, `scripts/score_codex_judgments.py`, `stego-results-viewer/.../llm-judge.ts` |
| Standalone CLIs | Corpus PPL / KL over `output-results/` | `scripts/avg_perplexity.py`, `scripts/avg_kld.py` |

`scripts/avg_er.py` is **not** an embedding-rate formula. It averages `len(stegoText)` in characters.

Post-clustered means: within each `post_id`, take the arithmetic mean of that method's samples, then mean those post-level values. Independent unit is the source post, not the row. Sign tests and Holm correction are applied to those post-level deltas.

---

## Compact table

| Metric | Formula gist | Code | Higher/lower better | Denominator |
| --- | --- | --- | --- | --- |
| Recoverable capacity (our, historical) | \(\lfloor\log_2 C\rfloor+\lfloor\log_2 A\rfloor\) per comment; \(C=\#\text{comments}+1\), \(A=\#\text{flattened angles}\) | `stego_codec.selection_channel_capacity_report` → row `payload_bits_encoded`; clustered in `build_zlg_method_comparison_dataset._clustered_method_summary` | higher | SOO: accepted paired rows, then one mean per post. **Channel width, not verified recovered payload bits** |
| Recoverable capacity (ZLG, historical) | useful payload bits from hide (`payload_bytes_actual*8` fallback) | `build_zlg_method_comparison_dataset._zlg_capacity_fields` | higher | same SOO post-cluster; on the 304-pair run this is 16.00 exactly (2-byte payload) |
| Recoverable bits (publication) | our: `payload_bits_target` iff exact decode else 0; ZLG: UTF-8 bits of verified prefix | `run_publication_benchmark._our_accounting`, `zlg_comparison_service._verified_capacity_fields` | higher | `analyze_publication_results._capacity_summary`: **accepted rows only**; pooled BPW uses \(\sum\) bits / \(\sum\) words |
| Bits/word pooled | \(\sum\) useful bits / \(\sum\) words | `analyze_publication_results._capacity_summary` | higher | accepted rows; word regex `\b[\w'-]+\b` |
| Bits/word macro | mean of per-row bits/max(1, words) | `analyze_publication_results._method_summary` (`effective_recovered_bits_per_word`) | higher | accepted rows |
| Bits/token pooled | \(\sum\) bits / GPT-2 token count | `_capacity_summary` + `stego_metrics_service.count_model_tokens` | higher | accepted stegotexts, GPT-2 tokenizer |
| Generation success (historical, our) | successes / attempts | paper 554/627; dataset builder conditions pairs on ZLG `accepted` | higher | ITT our-method attempts (627), **not** post-clustered |
| Generation success (historical, ZLG) | accepted / invocations | `_zlg_attempt_reliability`; paper 304/460 | higher | ITT among rows that reached the server; **excludes** 94 `harness_extract` skips |
| Exact recovery (historical) | `decode_ok` among accepted ZLG; our rows are `audit_assisted_compressed_full` | builder `decode_ok`; our `recovery_source` | higher | ZLG: 304/304 accepted (SOO). Our paired rows do **not** prove blind full-payload recovery |
| Generation success (publication) | `accepted / attempted` | `run_publication_benchmark._summary` | higher | ITT: all requested posts |
| Verified recovery (publication, SOO) | `(accepted ∧ decode_ok) / accepted` | `_summary.verified_recovery_rate` | higher | accepted rows only |
| Exact recovery (publication, ITT) | `decode_ok / attempts` | `analyze_publication_results._method_summary.exact_recovery_rate` | higher | all attempts (failures count as 0) |
| GPT-2 perplexity | \(\exp(\sum \mathrm{NLL}/\sum \text{scored tokens})\) per text; report mean (and median/corpus) | `stego_metrics_service.compute_text_perplexity`; clustered via `perplexity_gpt2` | **lower** | SOO scored texts; paper table = post-clustered mean of per-text PPL (not token-weighted corpus PPL) |
| KL | \(\mathrm{KL}(P_{\text{stego}}\|Q_{\text{baseline}})\) in nats, add-\(\alpha\) unigrams | `stego_metrics_service.kl_divergence` | lower | usable stego samples with a non-empty baseline; \(\alpha=10^{-6}\) default |
| JSD | \(0.5\,\mathrm{KL}(P\|M)+0.5\,\mathrm{KL}(Q\|M)\), \(M=(P+Q)/2\) | `stego_metrics_service.js_divergence` | lower | same; bound \(\ln 2\) |
| MATTR | moving-average TTR, window 10 | `build_zlg_method_comparison_dataset._mattr` | higher (diversity) | tokens from `[A-Za-z0-9']+`; **not** in publication runner |
| LQI / paper “MATTR 0–100” | \(100(0.55\cdot\mathrm{MATTR}+0.30\cdot\text{bigram}+0.15\cdot\text{length})\) | `_lexical_quality_index`; clustered as `lexical_quality_index` | higher | SOO paired rows. On this run, other terms saturate so LQI \(=55\cdot\mathrm{MATTR}+45\) |
| Word count (historical / MATTR) | `#` of `[A-Za-z0-9']+` | `_quality` / `_tokens` | descriptive (ours longer) | SOO post-cluster |
| Word count (publication / ZLG frames) | `#` of `\b[\w'-]+\b` | `run_publication_benchmark._word_count`, `zlg_comparison_service._word_count` | descriptive | sum over frames; acceptance also uses this budget |
| BLEU | sacrebleu `sentence_bleu` score (0–100) | `paired_quality_metrics_service.score_reference_metrics` | higher as overlap proxy | one candidate vs first human comment; SOO |
| ROUGE-1/2/L | stemmed F-measure | same, `rouge_scorer.RougeScorer` | higher as overlap proxy | same reference |
| BERTScore P/R/F1 | `BERTScorer(..., rescale_with_baseline=True)` | `score_reference_metrics` / `score_bertscore_pairs` | higher as overlap proxy | same; paper table is **rescaled** (near 0), not raw ~0.84 |
| Self-consistency | mean cosine to other same-post outputs | `score_self_consistency` | **no preferred direction** | other same-post texts of that method |
| J1 standout | P(judge `inserted_index` = true slot) | slate `build_standout`; score `llm-judge.rate` | **lower** (stealth) | valid tasks **per method**; chance 1/10 |
| J2 weak-link | P(named `weakest_index` maps to that method) | `build_weak_link`; `llm-judge.pickedRate` | **lower** | **shared** slates (one per pair); chance 1/3; three rates sum to 1 |
| J3 suspicion AUROC | Mann–Whitney on suspicion scores vs human arm | `judge_scoring_service.auroc`; `score_codex_judgments._summary` | **lower** (closer to human) | valid pointwise scores; chance 0.5 |
| J4 thread attribution | P(`thread_index` matches answer) | `_summary` accuracy; `llm-judge.rate` | **higher** as topical fit; **above human is a tell** | valid tasks per method; chance 1/4 |
| J5 register-fit | mean of `overall` (1–5) | `_summary` + `post_cluster_summary`; viewer `meanScore` | higher | valid register judgments per method |
| G-Eval | mean of 1–5 fields | `score_paired_quality_judgments` | higher | rows with valid scores; paper omits |
| Thread-grounded factuality | judge 1–5 vs thread evidence | same + `thread_grounded_factuality_v1.txt` | higher | same |
| M1 human-likeness | pairwise win rate (1 our / 0 ZLG / 0.5 tie), post-clustered | `score_human_likeness_judgments.summarize` | higher our-score | valid pairwise judgments, then posts |
| M2 synthetic detection | P(judge picks the stego among 1 stego + 2 humans) | `score_suspiciousness_judgments.score` + `analyze_suspiciousness_results` | **lower** | accepted carriers with ≥2 human decoys; clustered by post |
| Passive-detector ROC-AUC | 5-fold grouped CV, char-4gram LLR, mean fold AUC | `analyze_passive_detector.analyze` | **lower** (0.5 = chance) | accepted rows; humans sampled from same post; grouped by `post_id` |

---

## 1. Recoverable capacity / bits per comment

### Our method: lossless selection-channel width

Physical index width (can include modulo aliases) is **not** what the paper should quote:

- `comment_selection_bit_width` → `get_bit_width(n_comments)` = \(\lceil\log_2(n+1)\rceil\) when \(n>1\)
- `angle_selection_bit_width` → `get_bit_width(n_angles-1)`

Lossless / recoverable width used for reporting:

```text
comment_choices C = len(flatten_comments) + 1   # +1 = reply-to-post
tangent_choices A = len(flatten_angle_groups(angles))
comment_recoverable = floor(log2(C)) if C > 1 else 0
tangent_recoverable = floor(log2(A)) if A > 1 else 0
recoverable_capacity_bits = comment_recoverable + tangent_recoverable
```

Code: `workflows/utils/stego_codec.py` — `_recoverable_width`, `selection_channel_capacity_report`, `recoverable_selection_channel_capacity`. Tests in `src/tests/test_stego_codec.py` (`test_capacity_report_tracks_dynamic_comment_and_tangent_counts`).

A 32-angle cap contributes at most \(\lfloor\log_2 32\rfloor=5\) angle bits. That is why the historical gap is ~15 vs 16, not a general ceiling.

**Historical table cell (15.14):** `build_zlg_method_comparison_dataset` writes `payload_bits_encoded = recoverable_capacity_bits` for our-method rows (`pure_channel_bits`). `_refresh_recoverable_capacity` overwrites legacy modulo-width `selection_bits` with that lossless figure. Clustered mean: `_clustered_method_summary` averages within post, then across posts.

This is **offered uniquely-decodable channel width per comment**, not “bits the receiver recovered from a secret string.” Those rows set `recovery_source = "audit_assisted_compressed_full"`. Do not present 15.14 as blind end-to-end payload recovery.

An older enrichment bug read the pre-angle dataset snapshot (`angles` missing), zeroed the tangent term, and under-reported ~10.66 bits. The corrected clustered figure for that older artifact is 18.66 bits/comment (`method-and-zlg-benchmark.md`; `zlg-sample-audit-2026-07-27.md`). The paper’s 15.14 is the later 32-angle-cap run, not that 18.66 figure.

### ZLG: useful payload bits

`_zlg_capacity_fields`: `payload_bits_encoded` from the hide record, else `payload_bytes_actual * 8`. Overhead is `total_embedded_bits - useful` (ZLG framing header is 16 bits: `zlg_comparison_service.FRAMING_HEADER_BITS`).

On the 304-pair `capacity_matched` run every accepted ZLG row carries 16 useful bits, so the post-clustered mean is exactly **16.00**. That is a matched 2-byte payload, not ZLG’s maximum (`max_bpw=2` is a generation constraint, `DEFAULT_MAX_BPW`).

### Publication runner (different quantity)

`run_publication_benchmark._payload` is 8 hex chars = 64 UTF-8 bits.

- Our, `capacity_matched`: `_our_accounting` sets `payload_bits_encoded = payload_bits_target` only if `ReceiverPipeline` returns the exact string; else 0. `accepted` also requires `word_count <= max_total_words`.
- Our, `max_capacity`: largest planned payload that still accepts (`_run_our_max_capacity`).
- ZLG, `capacity_matched`: `run_comparison_frames` / `_verified_capacity_fields`: useful bits = recovered UTF-8 prefix bytes × 8, only after hide/reveal `decode_ok`.
- Pooled BPW/BPT and utilization (`total_embedded / total_selection_capacity`) are computed **only on accepted rows** (`analyze_publication_results._capacity_summary`). Macro BPW uses `max(1, word_count)` per accepted row.

`capacity_matched` vs `max_capacity` must not be mixed when claiming fluency at equal payload (`method-and-zlg-benchmark.md`).

---

## 2. Generation success and exact recovery (ITT vs SOO)

Keep failed attempts. Do not drop them from reliability rates.

### Historical 304-pair accounting (what `evaluation.tex` narrates)

| Rate | Numbers | Denominator | Kind |
| --- | --- | --- | --- |
| Our generation | 554/627 = 88.4% | all our attempts | ITT |
| ZLG invoked | 460 of 554 | exclude 94 cover-extraction (`harness_extract`) failures | harness, not ZLG |
| ZLG accepted | 304/460 = 66.1% | invocations only | ITT among server calls |
| ZLG decode | 304/304 | accepted ZLG | SOO; all were hide/reveal verified |
| Paired metric table | 304 pairs → 100 posts | only accepted pairs | **SOO**, then post-cluster |

Code for the ZLG denominators: `_zlg_attempt_reliability` (`failed_attempts_count_as_zero_bits=True` for **effective** bits/attempt; the table’s 16.00 is **conditional** on verified success).

Our 73 failures: 70 angle mismatches + 3 generation failures (paper prose). That is ITT reliability, not the metric table.

### Publication runner

`_run_our_method.accepted` = encode succeeded **and** exact payload match **and** word budget. So for our method, `accepted` already implies `decode_ok`.

`run_publication_benchmark._summary`:

- `generation_success_rate = accepted / attempted` — ITT
- `verified_recovery_rate = (accepted ∧ decode_ok) / accepted` — SOO

`analyze_publication_results._method_summary` uses a **different** recovery denominator:

- `attempt_success_rate = accepted / attempted` — ITT
- `exact_recovery_rate = (# decode_ok) / attempted` — ITT (failures are zeros)

Quality (PPL, JSD) is scored only when `row["accepted"]` (`score_quality`). That is SOO.

Pilot expansion gate (`_summary`): both methods need generation success ≥ 0.80 and verified recovery ≥ 0.95.

---

## 3. GPT-2 perplexity

CLI: `avg_perplexity.py` → `run_perplexity_metrics`. Pair scoring: `run_single_post_metrics` → `compute_text_perplexity`.

Per text:

1. Tokenize with Hugging Face `gpt2`, no truncation.
2. Sliding windows: `perplexity_windows(seq_len, stride=512, max_length=n_positions)` so each token is the prediction target of exactly one window; earlier tokens in the window are context (`labels=-100`).
3. Hugging Face mean CE loss × number of scored positions (`_ppl_chunk_loss`). Full-width windows score `target_len-1` because of the causal shift.
4. \(\mathrm{PPL}=\exp(\text{total NLL}/\text{scored tokens})\). Sequences with `<2` tokens → NaN, dropped.

Aggregates in `run_perplexity_metrics`:

- `average_perplexity`: arithmetic mean of per-text PPL (right-tail sensitive)
- `median_perplexity`: marked `headline_statistic`
- `corpus_perplexity`: token-weighted \(\exp(\sum\mathrm{NLL}/\sum\text{tokens})\)

The paper’s 68.15 / 53.70 are **post-clustered means of per-text PPL**, not median or corpus PPL. `analyze_publication_results` also uses `_mean` of per-text values.

Direction: **lower** is more GPT-2-predictable, not “more human.”

---

## 4. KL / JSD

CLI: `avg_kld.py` → `run_divergence_metrics`. Pair path: `run_single_post_metrics` / `_kl_jsd_pair`.

Tokenization: `TOKEN_RE = [A-Za-z0-9']+`, lowercased (`tokenize`). Comment bodies: `_iter_comment_bodies` (nested replies, skip `[deleted]`/`[removed]`).

Additive smoothing (`_smoothed_prob`), default \(\alpha=10^{-6}\):

\[
\hat p(w)=\frac{c(w)+\alpha}{N+\alpha|V|},\quad V=\mathrm{supp}(P)\cup\mathrm{supp}(Q)
\]

- KL direction **KL(stego ‖ baseline)** (`kl_direction` in the report). Nats (`math.log`).
- JSD = \(0.5\mathrm{KL}(P\|M)+0.5\mathrm{KL}(Q\|M)\), \(M=0.5(P+Q)\). Upper bound \(\ln 2\).

Baselines:

1. Primary: matched-post comment unigrams
2. Secondary: global corpus of all dataset comments
3. Human control: length-matched held-out real comment vs the rest of its thread (`evaluate_human_control`, 10th–90th percentile window)

Headline in the standalone report: `jsd_gap_vs_human_control` (stego mean − human-control mean).

`analyze_publication_results` pairs **JSD**, not KL. The historical clustered stats include both `kl_matched_post` / `jsd_matched_post` and global counterparts. **`evaluation.tex` reports neither.**

Direction: lower = closer to that unigram baseline. Strongly length- and \(\alpha\)-confounded (`alpha_sensitivity`).

---

## 5. MATTR, LQI, and the paper’s 0–100 rescaling

Only the historical builder computes these (`_mattr`, `_quality`, `_lexical_quality_index`). **`run_publication_benchmark` / `analyze_publication_results` do not.**

MATTR, window `MATTR_WINDOW = 10`:

- If \(|t|\le 10\): TTR \(= |set|/|t|\)
- Else: mean of \(|set(t[i:i+10])|/10\) over every window

LQI v2 (`lexical_quality_v2`):

\[
\mathrm{LQI}=100\bigl(0.55\cdot\mathrm{MATTR}+0.30\cdot s_{\mathrm{bigram}}+0.15\cdot s_{\mathrm{length}}\bigr)
\]

- \(s_{\mathrm{bigram}}=1-\min(1,\max(0,m-1)/3)\) where \(m\) is max bigram count
- \(s_{\mathrm{length}}=w/5\) if \(w<5\); \(1\) if \(5\le w\le 120\); else \(\max(0,1-(w-120)/120)\)

Clustered inference uses **`lexical_quality_index`**, not raw MATTR (`_clustered_paired_stats`).

`evaluation.tex` relabels that cell “MATTR (rescaled 0–100)” with \(55\cdot\mathrm{MATTR}+45\). That identity holds **only when** \(s_{\mathrm{bigram}}=s_{\mathrm{length}}=1\) (no repeated bigram above 1, word count in [5,120]). The 99.36 / 98.45 cells in `docs/reports/2026-07-30-context-weighted-v2-zlg-benchmark.md` are the LQI row, later renamed. They are not an independent second quality win.

Direction: higher LQI = more diverse / less phrase-repetitive / length-sane. Exploratory handcrafted index (`_lexical_quality_metadata.status`).

---

## 6. Word count

Two regexes:

| Where | Regex | Function |
| --- | --- | --- |
| Historical quality / MATTR / paper 22.4 vs 17.3 | `[A-Za-z0-9']+` | `_tokens` / `_quality` → `word_count = len(toks)` |
| Publication + ZLG frame budget | `\b[\w'-]+\b` (Unicode) | `_word_count` in `run_publication_benchmark.py` and `zlg_comparison_service.py` |
| `avg_er.py` | `len(stegoText)` characters | not a word count |

Paper table uses the historical token count, post-clustered. Direction: descriptive; ours is longer, which confounds PPL, KL, and detectors.

---

## 7. BLEU / ROUGE / BERTScore

`paired_quality_metrics_service.score_reference_metrics`. Reference = **first flattened human comment body** (`_reference_and_context`). Empty candidate or reference → skipped (scores stay `None`, not zero).

- BLEU: `sacrebleu.sentence_bleu(candidate, [reference]).score` (0–100)
- ROUGE-1/2/L: `rouge_score` F-measure, `use_stemmer=True`
- BERTScore: `bert_score.BERTScorer`, `model_type="roberta-large"`, `lang="en"`, **`rescale_with_baseline=True`**

`recompute_paired_bertscore.py` exists because an earlier artifact stored **unrescaled** F1 (~0.84). The paper’s 0.083 / 0.154 Precision and 0.068 / 0.114 F1 are the rescaled scale (can be near 0 or negative).

ZLG cover sentences are drawn from the thread, so overlap with that first-comment reference is partly regurgitation (paper: 5.9% of ZLG rows share a 5-gram vs 0.3% ours). Mean BLEU is outlier-driven; medians closer.

`finite_quality_metric_keys` treats BLEU/ROUGE/BERTScore as higher-is-better **overlap proxies**, not naturalness.

Self-consistency (`score_self_consistency`): mean cosine (`all-MiniLM-L6-v2`) to other same-post outputs of the same method. Listed as a **diagnostic**, not higher-is-better (`diversity_metric_keys`).

Publication runner does **not** call this module. Enrichment: `run_paired_reference_metrics.py`.

---

## 8. LLM-judge criteria (Codex / viewer)

Slates: `src/services/judge_slate_service.py`. Prompts: `config/evaluation_prompts/{standout,weak_link,suspicion,attribution,register}_v1.txt`. Python numeric summary: `scripts/score_codex_judgments.py` + `src/services/judge_scoring_service.py`. Viewer (standout / weak-link, which the Python scorer does **not** aggregate): `stego-results-viewer/src/app/zlg-comparison/_lib/llm-judge.ts`. Direction copy: `judge-copy.ts`.

### J1 standout — lower better

Insert one method’s stegotext into 9 human distractors from the **same** post (`build_standout`). Our method and ZLG get **separate** 10-comment slates, same slot. Chance 10%.

\[
\text{detection rate}=\frac{\#\{\text{result.inserted\_index}=\text{answer.inserted\_index}\}}{\#\text{valid tasks for that method}}
\]

`llm-judge.rate(..., "inserted_index")`. `score_codex_judgments._summary` does not emit this rate.

### J2 weak-link — lower better

One shuffled triple: human, our, ZLG (`build_weak_link`). Judge returns `weakest_index` (1–3).

\[
\text{pick rate}(m)=\frac{\#\{\text{methods[weakest\_index}-1]=m\}}{\#\text{valid slates}}
\]

`llm-judge.pickedRate`. Shared denominator (one slate per pair). Chance 1/3. No paired sign test in the Python summary.

### J3 suspicion AUROC — lower better (closer to human)

Pointwise 0–100 suspicion (`build_pointwise("suspicion")`). AUROC:

```text
wins = Σ_p Σ_n  1[p>n] + 0.5·1[p=n]
AUROC = wins / (|P|·|N|)
```

`judge_scoring_service.auroc(method_scores, human_scores)`. Mann–Whitney with ties as 0.5. Chance 0.5. **Not** the mean of the 0–100 scores. `post_cluster_summary` still runs a sign test on raw suspicion for Holm.

### J4 thread attribution — higher as topical fit; beating the human arm is a liability

Four thread blurbs, one true (`build_attribution`). Accuracy = P(`result.thread_index == answer.thread_index`). Chance 25%. `_summary` and `llm-judge.rate(..., "thread_index")`.

### J5 register-fit — higher better

1–5 scores; table cell is **`overall` only** (not a composite of the four subscores). `post_cluster_summary` on `overall`; viewer `meanScore`. Human arm is the same model scoring real comments.

Holm in `score_codex_judgments`: applied to the list of `two_sided_sign_test_p` from metrics that produced a `post_cluster` block (suspicion + register), not to standout/weak-link/attribution accuracies.

---

## 9. Other quality judges (runners compute; paper omits)

**G-Eval** (`run_paired_quality_judge.py`, `geval_v1.txt`): 1–5 coherence, relevance, fluency, factual_consistency, overall. `_summarize` in `score_paired_quality_judgments.py`: row means and post-clustered sign test. Higher better.

**Thread-grounded factuality**: 1–5 vs supplied thread evidence only (`thread_grounded_factuality_v1.txt`). Not canonical FActScore.

**M3/M4 thread quality** (`score_thread_quality_judgments.py`): 1–5, post-clustered our−ZLG deltas.

**M1 pairwise human-likeness**: `score_human_likeness_judgments._score` maps winner to 1 / 0 / 0.5, then post-cluster mean. Higher our-score = more pairwise wins.

---

## 10. Synthetic detection (M2) — present in runners, not in `evaluation.tex`

Protocol is **not** J3.

`build_suspiciousness_tasks.build`: for each accepted carrier, shuffle `[stego, human1, human2]`. Judge picks `suspicious_index`. `score_suspiciousness_judgments.score` sets `correct` iff that index is the stego. Detection rate = P(correct). **Lower** is better.

`analyze_suspiciousness_results.analyze`: per-post mean detection rate, delta ZLG−ours, clustered sign test. Conditions on accepted generations.

This is a **fixed-protocol rate**. Do not merge it with passive-detector AUC.

---

## 11. Passive-detector ROC-AUC — present in runners, not in `evaluation.tex`

`scripts/analyze_passive_detector.py`.

- Features: character 4-grams on whitespace-normalized lowercase text (`_ngrams`)
- Score: mean per-ngram log-likelihood ratio, Laplace-smoothed, **divided by n-gram count** (length-invariant)
- Labels: stego=1 vs human texts from the same attempt (`human_texts`, capped to match stego count)
- Split: 5-fold CV **grouped by `post_id`** (no carrier leakage)
- `roc_auc` = mean of **per-fold** AUCs (scores are not pooled across folds)
- AUC: Wilcoxon with ties 0.5 (`_auc`)

Only `accepted` rows. Methods scored separately (`our_method`, `official_zgls`). **Lower** AUC = less separable from matched humans; 0.5 is chance. Residual length imbalance is stored (`mean_stego_chars` vs `mean_human_chars`).

---

## 12. Shared statistics (not metrics, but they define the paper’s *p*)

| Procedure | Formula gist | Code |
| --- | --- | --- |
| Two-sided exact sign test | \(2\sum_{i=0}^{\min(W,L)}\binom{n}{i}/2^n\), \(n=W+L\) (ties dropped) | `_sign_test_p_value`, `judge_scoring_service.post_cluster_summary`, `analyze_publication_results._sign_p` |
| Holm | sorted \(p\), running \(\max_j \min(1,(m-j)p_{(j)})\) | `_apply_holm_correction`, `judge_scoring_service.holm_adjust` |
| Cluster bootstrap 95% CI | resample post-deltas, seed 1337, 10k | `_bootstrap_mean_ci` / `_bootstrap` |

Historical Holm family in `_stats_from_complete_pairs` includes capacity, PPL, KL/JSD, word count, LQI, BLEU/ROUGE/BERTScore, self-consistency — a **large** family. A paper *p* quoted as Holm-adjusted is relative to that family, not to the five table rows alone.

---

## 13. What `evaluation.tex` claims vs what runners compute

### In the paper table / prose, from the **historical** builder

Reported: recoverable bits/comment, GPT-2 PPL, LQI-as-rescaled-MATTR, word count, BERTScore P/F1; BLEU/ROUGE discussed in prose; ITT attempt counts.

Source: `build_zlg_method_comparison_dataset.py` + BERTScore recompute. Frozen writeup of the cells: `stego-side-wing/docs/reports/2026-07-30-context-weighted-v2-zlg-benchmark.md` (LQI still named “lexical quality index” there).

### Paper claims that the **publication** runner no longer computes

These still exist on the historical dataset path, but `run_publication_benchmark.py` + `analyze_publication_results.py` will not reproduce them:

- MATTR / LQI / \(55\cdot\mathrm{MATTR}+45\)
- BLEU, ROUGE, BERTScore
- Self-consistency
- Naturalness-gate pass rates (`_shared_gate_fields`)
- G-Eval / thread-grounded factuality (separate judge scripts, not the publication loop)

If the evaluation rewrite is supposed to follow the **live** publication protocol, those table rows have no current runner output. If it stays a historical configuration comparison, they remain defined only for that 304-pair artifact.

### Runners compute, paper omits

- KL and JSD (matched-post, global, human-control gap) — `avg_kld.py`, `run_single_post_metrics`, publication `matched_post_jsd`
- Pooled / macro bits per word and bits per GPT-2 token; utilization %
- Latency
- Median and corpus (token-weighted) perplexity
- Codex J1–J5 (standout, weak-link, suspicion AUROC, attribution, register)
- M1 pairwise human-likeness; M2 three-way synthetic detection
- Passive-detector grouped ROC-AUC
- G-Eval and thread-grounded factuality
- Naturalness gate `quality_passed` (shared) vs ZLG `server_quality_passed`
- Robustness / attack recovery (`analyze_attack_recovery.py`) — mentioned as future work in the paper
- POLYCARRIER sample-layer rollups (`polycarrier_sample_metrics.py`) if multi-frame is reported

### Paper reliability figures the live publication `_summary` would not emit as-is

- 554/627 and 304/460 come from the asymmetric historical harness (ZLG only runs on our successes; 94 extraction skips). Publication runs both methods on every frozen post.
- Historical our “capacity” is channel width with audit-assisted recovery; publication counts exact recovered payload bits of an 8-hex-char secret.

### `avg_er.py`

Does not compute embedding rate. Average character length of `stegoText` in `output-results/`. Do not cite it as ER/BPW.

---

## 14. Direction cheat-sheet for the evaluation rewrite

**Lower better:** GPT-2 PPL, KL, JSD, J1 detection, J2 pick rate, J3 AUROC, M2 detection rate, passive ROC-AUC, synthetic-detection rate.

**Higher better:** recoverable useful bits, generation/recovery rates, MATTR/LQI, BLEU/ROUGE/BERTScore (as overlap only), J4 accuracy (with the human-arm caveat), J5 overall, G-Eval.

**No preferred direction / descriptive:** word count, self-consistency, J4 above the human arm (stealth liability).

**Denominator rule of thumb:** reliability rates should show ITT (attempts) and SOO (accepted) side by side; fluency/overlap/judge scores in the current paper table are SOO on accepted pairs, then post-clustered.
