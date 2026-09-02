# Which numbers the paper should cite

Question: which frozen artifacts are canonical for the evaluation tables, and which `evaluation.tex` figures (627/554/304, 15.14 vs 16.00 bits, GPT-2 68.15 vs 53.70, and the rest) remain valid as a historical configuration comparison?

Rule used here: copy digits from a frozen report or JSON as written. If a value is not in those artifacts, it is **MISSING**. No new rounding, no subset re-aggregation.

## Verdict

The evaluation rewrite should print **two dated comparisons**, not one 304-pair table.

1. **Current fixed-text quality comparison** — the 2026-08-29 independent LLM-judge result on 244 unique-ZLG pairs drawn from the 2026-08-15 LUCID vs ZLG run. Canonical writeup: `stego-side-wing/docs/reports/2026-08-29-independent-llm-judge-results.md`. Canonical numbers: that report’s table strings, or the exact counts/floats in `zlg_lucid_fresh_6x_20260815_independent_unique_judge/comparison_dataset/`.
2. **Historical configuration comparison** — the 2026-07-29/30 `context_weighted_v2` vs ZLG run (627 attempted / 554 succeeded / 304 paired). Canonical writeup: `stego-side-wing/docs/reports/2026-07-30-context-weighted-v2-zlg-benchmark.md`. Failure-denominator correction for the same run: `stego-side-wing/docs/results/zlg-benchmark-failure-taxonomy-20260731.md`.

`evaluation.tex` today is the 07-30 run plus the 07-31 harness correction, with extra BERTScore / 5-gram / BLEU-median cells that are **MISSING** from every frozen report and JSON still on disk.

Do not use the 2026-07-26/27 47-post audit (`18.66` vs `76.70`, GPT-2 `91.52` vs `34.66`) as this paper’s main paired table. That is an earlier run (`zlg_demo_20260712_v6_200`). Its run directory is gone; its frozen numeric sidecar is `stego-side-wing/docs/reports/data/zlg-sample-audit-2026-07-27.json`.

Do not conflate the two **244** counts. The 07-30 run has **244 / 304** unique our-method stegotexts. The 08-29 judge set has **244 pairs from 244 posts**. Same integer, different objects.

---

## 1. Canonical artifacts (ranked)

| Role | Path | Still on disk? |
| --- | --- | --- |
| Current judge writeup | `stego-side-wing/docs/reports/2026-08-29-independent-llm-judge-results.md` | yes |
| Judge scoring JSON | `stego-side-wing/metrics/zlg_comparison_runs/zlg_lucid_fresh_6x_20260815_independent_unique_judge/comparison_dataset/codex_judge_summary.json` | yes |
| Judge judgments / tasks | same folder, `codex_judgments/{standout,weak_link,suspicion,attribution,register}_{tasks,judgments,answer_key,progress}.jsonl` | yes |
| Judge subset rows + selection manifest | `.../independent_unique_judge/comparison_dataset/paired_rows.jsonl`, `subset_manifest.json` | yes |
| Selection code | `stego-side-wing/scripts/build_independent_judge_subset.py` | yes |
| Source comparison freeze used by the judge | `stego-side-wing/metrics/zlg_comparison_runs/zlg_lucid_fresh_6x_20260815/comparison_dataset/paired_rows.jsonl` and `summary.json` | yes |
| Source ZLG lane (later, larger than the pairing freeze) | `.../zlg_lucid_fresh_6x_20260815/summary.json`, `results.jsonl` | yes |
| LUCID generation ITT for that campaign | `stego-side-wing/metrics/evaluation_campaigns/lucid_fresh_6x_20260815/combined_summary.json` | yes |
| Historical 627/554/304 writeup | `stego-side-wing/docs/reports/2026-07-30-context-weighted-v2-zlg-benchmark.md` | yes |
| Same-run ZLG failure recode (554→460) | `stego-side-wing/docs/results/zlg-benchmark-failure-taxonomy-20260731.md` | yes |
| Earlier 47-post metric audit | `stego-side-wing/docs/reports/zlg-benchmark-audit-2026-07-26.md` | yes |
| Earlier 47-post sample/capacity correction | `stego-side-wing/docs/reports/zlg-sample-audit-2026-07-27.md` + `docs/reports/data/zlg-sample-audit-2026-07-27.json` | yes (JSON); **run dir gone** |
| Status note | `stego-side-wing/docs/reports/2026-08-08-current-research-state.md` | yes; **partially stale** (see §4) |
| Original 07-30 comparison JSON | `metrics/zlg_comparison_runs/zlg_batch_scale300/` | **GONE** |
| Reconstructed scale300 summary | `metrics/e2e_runs/scale300_combined_summary.json` | yes, but it is a 2026-08-07 reconstruction from the *recalibrated* results file (`total_succeeded_samples`: 442, `skipped_missing_output_files`: 112). **Not** the source of 15.14 / 68.15. |
| Recalibrated ZLG-only rerun | `metrics/zlg_comparison_runs/zlg_batch_scale300_recalibrated/` | yes; 389 paired posts in its `comparison_dataset/summary.json`; **not** paired with the 08-15 LUCID campaign; **skip_model_metrics** true |

`.agents/method-and-zlg-benchmark.md` still names the 07-26 47-post audit as “the current historical audit” and quotes corrected capacity **18.66** bits/comment. That file is operational guidance. It is not the source of `evaluation.tex`, and it is not the 08-29 judge result.

---

## 2. LUCID vs ZLG dataset behind the 2026-08-29 judge

From `2026-08-29-independent-llm-judge-results.md` and `subset_manifest.json` (SHA matches the source file):

| Item | Value | Source |
| --- | --- | --- |
| Source comparison dataset | `metrics/zlg_comparison_runs/zlg_lucid_fresh_6x_20260815/comparison_dataset/paired_rows.jsonl` | 08-29 report; manifest `source_sha256` |
| Source SHA-256 | `20a0538717c4f86844393f1d0ae1e862cb22aede6cf6ce70d2551014efe5fc67` | `subset_manifest.json`; recomputed hash of that `paired_rows.jsonl` matches |
| Judge dataset | `metrics/zlg_comparison_runs/zlg_lucid_fresh_6x_20260815_independent_unique_judge` | 08-29 report |
| Selection id | `first_pair_per_post_with_globally_unique_zlg_stegotext` | `subset_manifest.json`; implemented in `build_independent_judge_subset.py` |
| Source pool | 1608 pairs from 339 posts | 08-29 report; `summary.json` `paired_posts` 1608; `independence_diagnostics.independent_clusters` 339 |
| Selected set | 244 pairs from 244 posts (488 generated texts) | 08-29 report; manifest `selected_pairs` 244, `selected_posts` 244, `dataset_posts` 244 |
| Excluded | 95 posts with no unique ZLG output | 08-29 report; recomputed from source `paired_rows.jsonl`: 339 − 244 = 95 |
| Comparison mode on source pairs | `capacity_matched` on all 1608 ZLG rows | source `paired_rows.jsonl` |
| Model metrics on source pairs | `perplexity_gpt2`, `kl_*`, `jsd_*`, `bleu`, `rouge*`, `bertscore_*` are JSON `null` on all 3216 rows | source `paired_rows.jsonl`; `summary.json` `skip_model_metrics`: true, `skip_reference_metrics`: true |
| Judge model for the completed run | Codex Luna, high reasoning effort; 2928 / 2928 tasks, 0 task errors | 08-29 report; judgments carry `judge_backend` `codex`, `judge_model` `gpt-5.6-luna`, `reasoning_effort` `high` |
| Pilot | `pilot_audit.json` `healthy`: true; coverage 1.0 and 0 errors on all five criteria | `codex_judgments/pilot_audit.json` |

The five criteria reuse those 244 pairs. They are not 2928 independent generated samples (08-29 report). Task counts in the JSONL files: standout 488, weak_link 244, suspicion 732, attribution 732, register 732. Sum **2928**.

---

## 3. Uniqueness / selection rules

From `build_independent_judge_subset.py` `select_rows`:

1. Group rows by `pair_id`. Keep a pair only if both `our_method` and `zlg` exist.
2. Count ZLG `stegotext` frequencies **globally** over complete pairs.
3. Walk complete pairs in **sorted `pair_id` order**.
4. Keep the first pair whose `post_id` is unused **and** whose ZLG text has global count 1.
5. Emit both method rows for those pair ids.

Source-pool uniqueness (recomputed from the frozen source `paired_rows.jsonl`, matching the 08-29 prose):

| Arm | Rows | Unique `stegotext` |
| --- | ---: | ---: |
| our_method | 1608 | 1606 |
| zlg | 1608 | 1236 |

ZLG texts with count > 1: 101 distinct strings, covering 473 rows.

`summary.json` `independence_diagnostics.unique_our_method_texts` is **1606**. `diversity_guard.minimum_unique_ratio` is **0.0** (diagnostic, not a hard fail). One post fails perfect uniqueness: `1n3dmol`, 6 samples, `unique_ratio` `0.6666666666666666`. `failing_post_ids` is `[]` because the threshold was 0.0.

Selected-set uniqueness (08-29 report, confirmed on judge `paired_rows.jsonl`): **244 / 244** our method, **244 / 244** ZLG.

The 08-29 note’s reporting limits still apply: this evaluand is the unique-ZLG-output subset, one pair per post; judge scores are not a reader study; do not mix judge denominators with ITT denominators.

---

## 4. ITT reliability for that source run

Three nested denominators. Do not add them.

### 4a. LUCID generation (campaign that fed ZLG)

File: `metrics/evaluation_campaigns/lucid_fresh_6x_20260815/combined_summary.json`

| Field | Value |
| --- | ---: |
| `requested` | 4044 |
| `succeeded` | 2543 |
| `failed` | 1501 |
| unique success posts | 517 |
| unique fail posts | 405 |
| union posts | 674 |
| success reuse max | 6 |
| `recovery_source` on all 2543 successes | `audit_assisted_compressed_full` |
| `used_compressed_full` | true on all 2543 |

`failure_code` on the 1501 failures:

| Code | Count |
| --- | ---: |
| `generation_failure` | 846 |
| `receiver_angle_mismatch` | 613 |
| `stego_invalid_json` | 42 |

Receiver recovery among recorded successes is 100% by construction of `entries`. It is **not** blind full-payload recovery: every success used audit-assisted compressed bits.

### 4b. ZLG lane freeze that the 1608-pair dataset was built from

File: `metrics/zlg_comparison_runs/zlg_lucid_fresh_6x_20260815/comparison_dataset/summary.json` → `zlg_attempt_reliability`

This is the ITT block that belongs with the judge’s source `paired_rows.jsonl`.

| Field | Value |
| --- | --- |
| `rows_in_run` | 1711 |
| `harness_skipped` | 0 |
| `attempted` | 1711 |
| `accepted` | 1610 |
| `decode_verified` | 1603 |
| `acceptance_rate` | 0.9409701928696669 |
| `decode_verified_rate` | 0.9368790181180596 |
| `effective_payload_bits_per_attempt` | 13.073056691992987 |
| `conditional_payload_bits_per_verified_success` | 13.953836556456643 |
| `failed_attempts_count_as_zero_bits` | true |
| `failure_stage_counts.quality_gate` | 96 |
| `failure_stage_counts.leakage_check` | 5 |

Paired ZLG rows in that same freeze: **1608**. Of those, `decode_ok` is true on **1603** and false on **5**. All 1608 still have `recovery_source` `pure_channel_hide_reveal_verified`. Do not invent a story that closes the 1610 vs 1608 vs 1603 gap; print the fields as stored.

Our-method paired rows in that freeze: 1608, `decode_ok` true, `recovery_source` `audit_assisted_compressed_full`.

### 4c. Later completed ZLG `results.jsonl` (same run directory, **not** the pairing freeze)

File: `metrics/zlg_comparison_runs/zlg_lucid_fresh_6x_20260815/summary.json` and `results.jsonl`

| Field | Value |
| --- | ---: |
| `processed_entries` / `rows_total` | 2543 |
| `accepted` | 2340 |
| `failed` | 203 |
| `comparison_mode` | `capacity_matched` |
| `failure_stage` `none` | 2340 |
| `hide_request` | 184 |
| `quality_gate` | 13 |
| `harness_extract` | 6 |
| `updated_at_utc` | `2026-08-16T16:34:42.268011+00:00` |
| ZLG `/health` `git_commit` | `e87a1d9` |
| model | `Qwen3.5-9B-Q4_K_M.gguf` |

`params_used` on all **2340** accepted rows is exactly one EGS tuple: `mode=huffman`, `threshold=0.01`, `temperature=0.7`, `temperature_alpha=1.0`, `max_bpw=2`. The 203 failed rows have empty `params_used`.

This 2543-row ZLG file is the full campaign’s comparison attempts. The judge did **not** use it. `1711 + 832 = 2543`: the pairing freeze stopped earlier. If the rewrite cites 2340/2543, label it as the completed ZLG lane, not as the 1608-pair judge source.

Accepted rows also store a server `ppl` field. That is **not** GPT-2 perplexity. `paired_rows.jsonl` `perplexity_gpt2` is null.

---

## 5. Reports that supersede `2026-08-08-current-research-state.md`

| Document | Date | Relation to 08-08 |
| --- | --- | --- |
| `2026-08-03-current-research-state.md` | 2026-08-03 | **Superseded by 08-08** as the “authoritative current-state note”. |
| `2026-08-08-current-research-state.md` | 2026-08-08, later patched | Still the only file that *calls itself* the current-state note. Its 08-29 subsection points at the judge result and says that result **supplements rather than replaces** a frozen symmetric capacity-matched benchmark. |
| `2026-08-29-independent-llm-judge-results.md` | 2026-08-29 | **Later, and canonical for the judge table.** It does not replace ITT accounting. |

Stale sentences still sitting in 08-08:

- “Latest completed recalibrated unpaired ZLG artifact remains `zlg_batch_scale300_recalibrated`.” A later **paired** freeze exists: `zlg_lucid_fresh_6x_20260815`.
- LUCID freeze / contaminated `datasets/news_researched` applies to `LUCID_tangents_db_v1_balanced_500`. The 08-15 campaign is a different, later generation artifact. 08-08’s next-action item to grow `tangents_db_v1_fresh` is not itself a results table.

No later markdown in `docs/reports/` after 2026-08-29.

`docs/plans/context-weighted-v2-zlg-benchmark-status.md` (updated 2026-08-03) still says no paired LUCID-vs-ZLG claim is authorized. That plan is older than the 08-15 paired freeze and the 08-29 judge.

---

## 6. What `evaluation.tex` currently prints, and what stays

`evaluation.tex` is the **07-30 run**, not the 07-26 47-post audit, and not the 08-15/08-29 judge.

### Keep as historical configuration comparison (copy from 07-30 / 07-31)

From `2026-07-30-context-weighted-v2-zlg-benchmark.md` unless noted.

| Claim | Value | Keep? | File |
| --- | --- | --- | --- |
| Our attempts / successes | 627 attempted, 554 succeeded (88.4%) | yes | 07-30 §4 |
| Our failures | 73; `receiver_angle_mismatch` 70; `generation_failure` 3 | yes | 07-30 §4 |
| ZLG fed from | all 554 successes, `capacity_matched` | yes | 07-30 §4 |
| ZLG accepted (original denominator) | 304 (54.9% of 554) | yes, as the original accounting | 07-30 §4 |
| ZLG failed (original taxonomy) | 250 = quality_gate 134 + cover-extract 94 + prompt_leakage 22 | yes, as the original taxonomy | 07-30 §4 |
| Cover-extract concentration | 94 failures from 21 posts | yes | 07-30 §4 |
| Research pool / reuse | 167 posts; 35 used 10 times; 154/167 produced ≥1 success | yes | 07-30 §5 |
| Unique our-method texts among 304 pairs | 244/304 (80.3%); 100 unique posts | yes | 07-30 §5 |
| Post-clustered inference unit | 100 posts | yes | 07-30 §6 |
| Angle cap | 32 entries; `floor(log2(32))=5` bits | yes | 07-30 §6 |
| EGS tuple on all 304 accepted ZLG rows | threshold=0.01, temperature=0.7, alpha=1.0, max_bpw=2 | yes | 07-30 §2 bug 5, §7 |
| Project recovery | audit-assisted compressed bitstring | yes | 07-30 §8 / evaluation.tex; 07-27 audit for the *other* run uses the same recovery_source name |
| Corrected ZLG denominator | 460 invocations, 304 accepted (66.1%); 94 harness skips excluded | yes, as the 07-31 recode of the **same** run | 07-31 “Corrected figures” |
| Genuine ZLG failures after recode | 156 = quality_gate 133 + leakage 22 + HTTP 500 1 | yes | 07-31 taxonomy table |

`evaluation.tex` already mixes both accountings in one paragraph (554/54.9% language in 07-30 vs 460/66.1%/133/1 in 07-31). Keep both, labeled, rather than collapsing them.

### Historical paired table cells — copy these strings from 07-30 §6

Post-clustered means over 100 posts. The `zlg_batch_scale300` JSON that produced them is **gone**. Do not unround.

| Metric | Our method | ZLG | Sign test (Holm-adj. p) | Extra from 07-30 |
| --- | ---: | ---: | --- | --- |
| Recoverable capacity (bits/comment) | 15.14 | 16.00 | p < 0.001 | ZLG higher (66/100 posts, 26 ties) |
| GPT-2 perplexity | 68.15 | 53.70 | p = 0.0001 | ZLG lower (73/100 posts) |
| Lexical quality index (0–100) | 99.36 | 98.45 | p = 0.0015 | Ours higher (58/100 posts) |
| Word count | 22.4 | 17.3 | p < 0.001 | Ours longer (77/100 posts) |
| BERTScore F1 | 0.842 | 0.848 | — | “Comparable”; **no Holm p** in 07-30 |

`evaluation.tex` relabels the lexical-quality index as “MATTR (rescaled 0–100)” and claims it “reduces exactly to \(55\cdot\mathrm{MATTR}+45\)”. The 07-30 report names it **Lexical quality index (0–100)**. The v2 weights (in the 08-15 `summary.json` `lexical_quality_index` block, same formula family) are 0.55 MATTR + 0.30 bigram non-repetition + 0.15 length sanity. Whether those last two terms were identically 1.0 on every 07-30 row is **MISSING** (JSON gone). Do not print “MATTR” as if it were a raw MATTR column unless that reduction is found in a frozen artifact.

### Drop or mark MISSING from `evaluation.tex`

These strings appear only in `project_paper/stego_paper/sections/evaluation.tex` (and the Arabic twin / conclusion echoes). They are **not** in 07-30, 07-31, 07-26, 07-27, 08-08, 08-29, or any remaining `summary.json`.

| Cell / claim | `evaluation.tex` | Frozen source |
| --- | --- | --- |
| BERTScore Precision | 0.083 vs 0.154; Holm \(p\approx 0.0045\) | **MISSING** |
| BERTScore F1 (rescaled) | 0.068 vs 0.114; Holm \(p=0.12\) | **MISSING** (07-30 F1 is 0.842 vs 0.848, unrescaled) |
| “BERTScore is baseline-rescaled” | caption + prose | **MISSING** as a defined transform in reports |
| 5-gram overlap with BLEU reference | “about 5.9% of ZLG rows” vs 0.3% ours | **MISSING** |
| BLEU medians | 1.46 versus 1.59 | **MISSING** |
| 100 clusters on the 07-26 audit | evaluation opening can be read as 07-26 | 07-26 is **47** clusters, not 100 |

Nearby but **different run** (do not substitute): `zlg-baseline-weaknesses-2026-07-27.md` has “Verbatim repeated 5-gram 8.2% vs 0.0%”; 07-26 BLEU means are 1.126 vs 1.187. Those are the 47-post demo run.

### Do not promote the 07-26/27 audit to the paper’s main table

If a footnote or related-work sentence needs that older audit, copy from the reports/JSON rather than from `evaluation.tex`:

| Metric | Ours | ZLG | File |
| --- | ---: | ---: | --- |
| Post-clustered recoverable capacity (comment channel only, as stored) | 10.66 | — | 07-26 table; JSON `capacity_audit.post_clustered_means.reported` = `10.659574468085106` |
| Corrected post-clustered recoverable capacity | 18.66 | 76.70 | 07-26 correction banner + 07-27; JSON recomputed mean `18.659574468085108`. **ZLG 76.70 is only in the 07-26 markdown**, not in the 07-27 JSON (`methods.zlg.embedded_bits.mean` is row-level `75.15789473684211`). |
| Failure-adjusted ZLG bits/attempt | n/a | 41.77 | 07-26 table (304/547 = 55.6%) |
| GPT-2 PPL, arithmetic post mean | 91.52 | 34.66 | 07-26 table (post-clustered). Row-level JSON means are `104.5423749879055` vs `36.06054257274159`. |
| Unique our-method texts | 47 / 304 | 304 / 304 | 07-27 table; JSON `unique_texts` 47 vs 304 |

The 07-26 run directory `metrics/zlg_comparison_runs/zlg_demo_20260712_v6_200` is **gone**.

---

## 7. Table cells the evaluation rewrite should print

Print counts as integers. Print floats as they appear in JSON, or as the already-rounded strings in a named report. Do not round JSON into a new display value.

### Table J — Independent LLM judge (canonical current quality table)

Denominator: 244 selected post clusters unless the row says otherwise. Source for display percents/one-decimal scores: 08-29 report table. Source for exact counts/floats: JSON/JSONL as listed.

| Criterion | Our method | ZLG | Other | Exact generating artifact |
| --- | --- | --- | --- | --- |
| Standout detection (lower better) | 126 / 244 | 69 / 244 | report also prints 51.6% and 28.3% | `standout_judgments.jsonl` (126 and 69 hits); 08-29 table for the percent strings |
| Weakest text picked (lower better) | 71 / 244 | 116 / 244 | human control 57 / 244; report 29.1%, 47.5%, 23.4% | `weak_link_judgments.jsonl`; 08-29 table |
| Suspicion AUROC vs human (lower closer to chance) | 0.6606758935769954 | 0.6497413329750067 | report prints 0.661 and 0.650; sign-test p=`0.38511100043646007` (report `p=0.385`) | `codex_judge_summary.json` `suspicion.auroc` and `suspicion.post_cluster.two_sided_sign_test_p` |
| Thread attribution accuracy (higher better) | 0.8934426229508197 | 0.75 | report prints 89.3% and 75.0%; counts 218 / 244 and 183 / 244 | `codex_judge_summary.json` `attribution.accuracy`; counts from `attribution_judgments.jsonl` |
| Register-fit `overall` 1–5 (higher better) | 3.192622950819672 | 2.790983606557377 | report prints 3.193 and 2.791 | arithmetic mean of `result.overall` on `register_judgments.jsonl` (not stored as a mean in `codex_judge_summary.json`) |
| Register post-cluster delta (ours − ZLG) | 0.4016393442622951 | — | report 0.402 | `codex_judge_summary.json` `register.post_cluster.our_minus_zlg_post_cluster_mean` |
| Register wins / losses / ties | 106 / 67 / 71 | — | paired sign-test p=`0.0037377190466882` (report `p=0.00374`) | `codex_judge_summary.json` `register.post_cluster` |
| Holm-adjusted primary p-values stored | 0.0074754380933764, 0.38511100043646007 | — | register Holm is 2× raw p | `codex_judge_summary.json` `holm_adjusted_primary_p_values` |
| Tasks completed | 2928 / 2928 | — | 0 task errors | 08-29 report; JSONL lengths |

Human-arm extras that exist in JSONL but are **not** in the 08-29 table: attribution human 184 / 244; register human mean `3.401639344262295`. Treat as **optional**; do not invent a report percent for them.

### Table R — ITT beside the judge (do not share Table J’s 244 denominator)

| Row | Value | File |
| --- | --- | --- |
| LUCID attempted / succeeded / failed | 4044 / 2543 / 1501 | `lucid_fresh_6x_20260815/combined_summary.json` |
| LUCID failure codes | generation_failure 846, receiver_angle_mismatch 613, stego_invalid_json 42 | same, `failures[].failure_code` |
| LUCID recovery on successes | 2543 / 2543 `audit_assisted_compressed_full` | same |
| ZLG freeze matching the 1608-pair source | attempted 1711, accepted 1610, decode_verified 1603; quality_gate 96; leakage_check 5; harness_skipped 0 | source `comparison_dataset/summary.json` `zlg_attempt_reliability` |
| Optional: completed ZLG lane | 2340 accepted / 2543 processed; hide_request 184, quality_gate 13, harness_extract 6 | run `summary.json` + `results.jsonl` |

### Table C — Source-run post-clustered capacity / length / lexical (08-15 freeze, 339 posts)

File: `zlg_lucid_fresh_6x_20260815/comparison_dataset/summary.json`. Inference unit `unique_post_id`. **No GPT-2, KL, JSD, BLEU, ROUGE, BERTScore** in this freeze (`skip_model_metrics` / `skip_reference_metrics` true; those fields are null in `paired_rows.jsonl`).

Clustered means (`methods_clustered_by_post`, n=339):

| Metric | Our method | ZLG |
| --- | ---: | ---: |
| `payload_bits_encoded_mean` | 13.418879056047198 | 13.900491642084562 |
| `payload_bits_encoded_median` | 13.0 | 16.0 |
| `total_embedded_bits_mean` | 13.418879056047198 | 13.933579154375614 |
| `word_count_mean` | 23.856342182890856 | 15.905850540806291 |
| `word_count_median` | 23.666666666666668 | 15.0 |
| `lexical_quality_index_mean` | 99.3734333676008 | 96.92804869596854 |
| `repetition_ratio_mean` | 0.031141486513594507 | 0.074115492272213 |
| `self_consistency_mean` | 0.46553374566058675 | 0.4626606774497086 |

Paired sign tests (`paired_statistics`, n=339 except self_consistency n=326):

| Metric | mean_delta (ZLG − ours) | ZLG greater / ours greater / ties | two_sided_sign_test_p | holm_adjusted_p |
| --- | ---: | --- | ---: | ---: |
| `payload_bits_encoded` | 0.48161258603736484 | 230 / 91 / 18 | 4.971379479121762e-15 | 1.4914138437365286e-14 |
| `total_embedded_bits` | 0.514700098328417 | 234 / 87 / 18 | 1.0512412482551553e-16 | 5.256206241275777e-16 |
| `word_count` | -7.950491642084563 | 31 / 307 / 1 | 2.909797843624482e-58 | 2.3278382748995856e-57 |
| `lexical_quality_index` | -2.445384671632252 | 75 / 250 / 14 | 3.858747300020063e-23 | 2.3152483800120374e-22 |
| `repetition_ratio` | 0.0429740057586185 | 257 / 77 / 5 | 8.758996272994631e-24 | 6.131297391096242e-23 |
| `self_consistency` | -0.002873068210878135 | 112 / 214 / 0 | 1.712727135938705e-08 | 1.712727135938705e-08 |

Row-level means exist under `methods` (n=1608) if a diagnostic row is needed; primary inference is the 339-post cluster block.

Capacity formula note stored in that summary: our_method uses `floor(log2(comment_choices))+floor(log2(tangent_choices))`; ZLG displayed conditional mean is successful hides; `zlg_attempt_reliability` counts failures as zero bits.

**Do not** compute a new 244-subset capacity table from the judge `paired_rows.jsonl`. No frozen summary of that subset exists. The 08-29 note says capacity stays non-comparable without a separately frozen capacity-matched experiment using real receiver verification — and also says to report source-run failure/acceptance alongside the judge, which Table R and Table C already do.

### Table G — Shared analysis-time naturalness gate (08-15 freeze, 1608 rows/arm)

From `summary.json` `shared_naturalness_gate`:

| Arm | n | passed | pass_rate | failed rules |
| --- | ---: | ---: | ---: | --- |
| our_method | 1608 | 1603 | 0.9968905472636815 | too_short 5 |
| zlg | 1608 | 1509 | 0.9384328358208955 | degenerate_repetition 62, structural_artifact 39, too_short 10, bigram_repeat 1 |

Thresholds: `min_words` 8, `max_words` 60, `max_bigram_repeat_limit` 4, `repetition_ratio_limit` 0.28.

### Table H — Historical 07-30 paired results (configuration comparison)

Copy §6 of `2026-07-30-context-weighted-v2-zlg-benchmark.md` as Table C’s historical twin. Use the 07-30 BERTScore F1 **0.842 vs 0.848** if overlap is shown at all. Do not print 0.083 / 0.154 / 0.068 / 0.114.

Reliability prose for that table: 07-30 §4 plus 07-31 corrected 460 / 66.1% / 133 / 22 / 1.

---

## 8. Metrics the runners have that this freeze does not print

On the 08-15 source `paired_rows.jsonl` the columns exist but are null: `perplexity_gpt2`, `kl_matched_post`, `kl_global_corpus`, `jsd_matched_post`, `jsd_global_corpus`, `bleu`, `rouge1`, `rouge2`, `rougeL`, `bertscore_precision`, `bertscore_recall`, `bertscore_f1`.

`tangent_db_quality` in the 08-15 summary has `report_rows` 0 / `unique_posts` 0.

Synthetic detection rate, G-Eval, and passive-detector ROC-AUC from the 07-26 audit are **not** in the 08-15 freeze. They belong only to the 47-post historical audit if cited at all.

---

## 9. Abstract / introduction / conclusion sync

`abstract.tex` and `conclusion.tex` currently cite 554/627, 460, 304, 16.00 vs 15.14, 53.70 vs 68.15, MATTR 99.36 vs 98.45. Those stay valid **as the historical configuration comparison**, sourced from 07-30 + 07-31.

They do **not** yet cite the 08-29 judge table. Ticket 08 (`rewrite-evaluation-and-results`) asks to update abstract, contributions, and conclusion to the same numbers as the rewritten evaluation. After the rewrite, those sections should name both the 244-pair judge result and the 627/554/304 historical run, with the artifacts above as the owners of the digits.

---

## 10. MISSING register (do not fill)

- BERTScore Precision 0.083 vs 0.154 and Holm \(p\approx 0.0045\)
- BERTScore F1 0.068 vs 0.114 and Holm \(p=0.12\)
- BLEU medians 1.46 vs 1.59
- 5.9% vs 0.3% 5-gram overlap with the BLEU reference
- Unrounded JSON behind 07-30 table cells 15.14, 68.15, 22.4, 17.3 (`zlg_batch_scale300` gone)
- Proof that 07-30 lexical-quality index equals \(55\cdot\mathrm{MATTR}+45\) on every row
- GPT-2 / KL / JSD / BLEU / ROUGE / BERTScore for `zlg_lucid_fresh_6x_20260815`
- Frozen post-clustered capacity on the 244 judge subset
- A post-08-29 current-state note that retires the 08-08 “latest ZLG artifact is `zlg_batch_scale300_recalibrated`” sentence
- Blind (non-audit-assisted) full-payload recovery rate for LUCID on 08-15 (all 2543 successes are `audit_assisted_compressed_full`)
