# Independent LLM-judge protocol (paper subsection source)

For the LaTeX rewrite of evaluation. Facts below are from the frozen 2026-08-29 report and the live scoring/slate code. Do not re-read Python to write the subsection. Do not call this protocol G-Eval. Do not report it as a human reader study or as proof of authorship, security, or general naturalness.

**Cite the 244-pair table exactly as in the frozen report** (section "Frozen 244-pair result table" below). Viewer copy and later qualitative notes add extra numbers (human-arm means, tell counts, bootstrap stories). Those are not in the frozen report. Do not mix them into the paper table.

---

## What this protocol is

A fixed-text, post-clustered, five-criterion evaluation of already-generated cover comments. A language model scores blinded slates. It is not a new capacity experiment, not an intention-to-treat reliability table, and not a replacement for the source comparison run's generation/recovery accounting.

Source: `stego-side-wing/docs/reports/2026-08-29-independent-llm-judge-results.md` (scope). Paper glossary: `project_paper/CONTEXT.md` ("LLM judge").

The five criteria reuse the same 244 pairs. They are not 2,928 independent generated samples. Source: frozen report.

Operational name in code and artifacts is "Codex judge" (`codex_judgments/`, `score_codex_judgments.py`) even when the backend is Claude. The frozen published run used Codex Luna, not Claude.

---

## Not G-Eval (and not the other older judges)

G-Eval is a different, older quality path. Do not use the name for this subsection.

| | Independent LLM judge (this protocol) | G-Eval (older) |
| --- | --- | --- |
| Runner | `scripts/run_codex_judge.py` + campaign `run_codex_judge_campaign.py` | `scripts/run_paired_quality_judge.py --metric geval` |
| Scoring | `scripts/score_codex_judgments.py`, `src/services/judge_scoring_service.py` | `scripts/score_paired_quality_judgments.py` |
| Prompt | five `*_v1.txt` files (standout, weak_link, suspicion, attribution, register) | `config/evaluation_prompts/geval_v1.txt` |
| Criteria | identification / ranking / suspicion AUROC / thread pick / register overall | coherence, relevance, fluency, factual_consistency, overall (each 1-5) |
| Input | thread slates plus candidate; no matched human reference text in the prompt | thread context, matched human reference, candidate |
| Default model (current code) | Claude CLI `sonnet` (Sonnet 5). Frozen run was Codex `gpt-5.6-luna` | LM Studio `google/gemma-3-12b` |
| Where it appears | 2026-08-29 independent judge report; `/zlg-comparison` default | 2026-07-26/27 sample audits; `quality_judgments.geval` in older comparison summaries |

G-Eval prompt instructs an "exacting evaluator" and returns `{"scores": {coherence, relevance, fluency, factual_consistency, overall}, "rationale"}`. It says "Do not reward payload capacity." Source: `geval_v1.txt`; `run_paired_quality_judge.py`.

The 2026-07 historical audits that say "ZLG led on unadjusted G-Eval" are that older path, on a different 304-pair / 47-cluster sample. Source: `stego-side-wing/.agents/method-and-zlg-benchmark.md`.

Other scripts that are also not this protocol: `run_human_likeness_judge.py` (pairwise A/B, Gemma), `run_thread_quality_judge.py` (thread_relevance / writing_quality), `run_suspiciousness_judge.py` (3-way `suspicious_index`). Ignore them in the paper subsection.

---

## Frozen evaluation set

Source comparison:

`metrics/zlg_comparison_runs/zlg_lucid_fresh_6x_20260815/comparison_dataset/paired_rows.jsonl`

Judge dataset:

`metrics/zlg_comparison_runs/zlg_lucid_fresh_6x_20260815_independent_unique_judge`

Viewer default run id is `zlg_lucid_fresh_6x_20260815_independent_unique_judge`. Source: `stego-results-viewer/src/app/zlg-comparison/_lib/data.ts`.

Selection rule, implemented in `scripts/build_independent_judge_subset.py` `select_rows`:

1. Keep only complete pairs that have both `our_method` and `zlg`.
2. Count ZLG `stegotext` strings across those complete pairs.
3. Walk complete pairs in sorted `pair_id` order.
4. Take the first pair for each `post_id` whose ZLG text occurs exactly once in the whole source pool.
5. Exclude a post entirely if it has no unique-ZLG pair.

Frozen counts from the report (use these, do not recompute):

- Source pool: 1,608 pairs from 339 posts.
- Selected set: 244 pairs from 244 posts (488 generated texts).
- Text uniqueness in the selected set: 244 / 244 for our method and 244 / 244 for ZLG.
- 95 posts without a unique ZLG output were excluded.

The result is about the unique-output subset, not the full 1,608-pair source run. Source: frozen report, interpretation limits.

Manifest key written by the subset script: `selection: first_pair_per_post_with_globally_unique_zlg_stegotext`.

---

## Task inventory

Five metrics. Campaign order: standout, weak_link, suspicion, attribution, register. Source: `run_codex_judge.py` `METRICS`; `run_codex_judge_campaign.py`.

On the frozen 244-pair set, every pair produced every task type (all posts passed eligibility). Task counts:

| Metric | Tasks per pair | Arms | Frozen tasks |
| --- | ---: | --- | ---: |
| standout | 2 | our_method, zlg (separate slates) | 488 |
| weak_link | 1 | paired (human + our_method + zlg in one slate) | 244 |
| suspicion | 3 | our_method, zlg, human | 732 |
| attribution | 3 | our_method, zlg, human | 732 |
| register | 3 | our_method, zlg, human | 732 |
| **Total** | **12** | | **2,928** |

Frozen execution: 2,928 / 2,928 completed, 0 task errors. Pilot audit passed with full valid coverage for all five criteria. Source: frozen report.

Eligibility before emission (`run_codex_judge.py` `_tasks`). Pair must contain both control and treatment methods.

- standout: cleaned comments >= 9
- weak_link, suspicion, register: at least one cleaned comment
- attribution: corpus size >= 4 posts and the post has cleaned comments

Comment cleaning (`judge_slate_service.py` `_clean_comments`, `_walk`, `_valid`):

- Walk each comment dict's `body` and nested `replies`.
- Collapse whitespace (`" ".join(body.split())`).
- Drop if lowercase body is `[deleted]` or `[removed]`.
- Drop if character length < 15 (after collapse).
- Drop if word count > 200 (`len(text.split())`).
- Dedupe preserving order (`dict.fromkeys`).

---

## Judge model and provenance

**Frozen published run.** Codex Luna, high reasoning effort. Per-task prompt/schema hashes, model provenance, and JSONL responses live under `comparison_dataset/codex_judgments/`. Source: frozen report.

Code identity for that backend: `--backend codex`, default model `gpt-5.6-luna`, default `--reasoning-effort high`, and `--ignore-user-config` on Codex. Source: `codex_judge_client.py` `DEFAULT_MODELS`; `run_codex_judge.py`.

**Current code default for future runs.** Claude CLI alias `sonnet` (Sonnet 5), still high reasoning. The frozen report says this default change does not rewrite or mix with the completed Codex result. Paper must describe the Codex Luna run, not the later Claude default.

Each judgment row stores: `judge_backend`, `judge_model`, `reasoning_effort`, `codex_cli_version`, `judge_prompt_sha256`, `output_schema_sha256`, `usage`. Source: `score_codex_judgments.py` `_merge`; `run_codex_judge.py` `_run`.

Execution `task_id` is SHA-256 of

`{metric}:{pair_id}:{method}:{prompt_hash}:{schema_hash}:{backend}:{model}:{reasoning_effort}`

Changing prompt, schema, backend, model, or effort creates a distinct cache. Source: `run_codex_judge.py` `_task_id`.

Scoring artifact provenance blob (`codex_judge_summary.json`):

- `tasks_are_seeded`: true (slate RNG is deterministic)
- `reasoning_models_are_not_deterministic`: true (the judge model is not)
- `inference_unit`: `post_id`
- `cluster_bootstrap_iterations`: 10000

That last key is a leftover. `cluster_bootstrap_ci` exists in `judge_scoring_service.py` but `score_codex_judgments.py` never calls it. `mcnemar_exact` in the same module is also unused by this protocol. **Do not report bootstrap confidence intervals or McNemar tests for these five criteria.** They are not in the scoring artifact.

Pilot gate (`audit_codex_judge_pilot.py`): coverage >= 0.95 and dominant predicted index share < 0.8 per metric. Campaign runs a 50-pair pilot, audits, then the full set. Source: `run_codex_judge_campaign.py`; operations note `docs/operations/codex-judge-progress.md`.

Structured output is schema-validated (`codex_judge_client.py` `_schema_valid`). One retry (`max_attempts=2`).

---

## Shared slate machinery

Slates are built in `src/services/judge_slate_service.py`. Prompts are filled by replacing `{field}` tokens in `config/evaluation_prompts/{metric}_v1.txt`. JSON shape is `config/evaluation_prompts/schemas/{metric}_v1.schema.json`.

**Seeding.** `random.Random` with seed = integer from the first 8 hex characters of SHA-256(`{metric}:{post_id}:{pair_id}`). Same pair and metric always rebuild the same slate. Suspicion and register use different metric names in the seed, so they can hold out different human comments even though both call `build_pointwise`.

**Blinding.** Public task files omit `answer`. Prompts never name the method. Scoring uses the `answer` object stored on the judgment row itself, not a re-join of `{metric}_answer_key.jsonl`.

**Control/treatment names.** Builders internally use `our_method` and `zlg`. The runner remaps those labels to `--control-method` / `--treatment-method` (defaults unchanged). Frozen table columns are "Our method" and "ZLG".

---

## The five criteria

Chance rates below are implied by slate size. Python does not compute them. The viewer hardcodes the strings in `stego-results-viewer/src/app/zlg-comparison/_lib/judge-copy.ts`. They are the correct combinatorial baselines.

### J1 standout detection

**Ask.** Identify the one machine-generated comment in a 10-comment thread. Instruction: judge conversational fit, specificity, stance, register, and habits; do not use length or polish as a cue.

**Prompt / schema.** `standout_v1.txt`, `standout_v1.schema.json`. Returns `inserted_index` (1-10), `confidence` (0-100), `runner_up_index` (1-10), `evidence`.

**Slate** (`build_standout`). Seeded RNG samples 9 cleaned human comments (eligibility already requires >= 9), draws one insert slot in `0..9`, then for each of our method and ZLG copies those distractors and inserts that method's `stegotext` at the same slot. Prompt fields: subreddit, post title, post body, numbered comments 1-10. Hidden answer: `inserted_index = slot + 1`. Two tasks per pair. The two methods never share one slate. They share distractors and slot.

All ten comments come from the same post. J1 does not mix threads.

**Table number.** Among standout rows for that method with both `result` and `answer`, fraction where `result.inserted_index === answer.inserted_index`. Viewer helper `rate(rows, "standout", method, "inserted_index")`, shown as percent to 1 decimal. Scoring script does not store an accuracy key for standout, only `valid_judgments` / `tasks`.

**Direction.** Lower is better (harder to pick out of the lineup).

**Chance.** 10% (1 of 10).

**Frozen denominator.** 244 / 244 tasks per method.

**Frozen result.** Our method 126 / 244 (51.6%). ZLG 69 / 244 (28.3%).

**Sign test.** None in the scoring artifact.

### J2 weakest text picked

**Ask.** Rank three replies from most human-plausible (1) to least (3), then name the weakest. Ignore length and ordering.

**Prompt / schema.** `weak_link_v1.txt`, `weak_link_v1.schema.json`. Returns `weakest_index` (1-3), `ranking` (permutation of 1-3), `evidence`.

**Slate** (`build_weak_link`). One task per pair, `method: "paired"`. Seeded RNG holds out one human comment, shuffles `(human, our_method stegotext, zlg stegotext)` into `candidate_1..3`, and shows up to five other thread comments as context plus post title/body. Hidden answer: `methods` = shuffled method names in candidate order.

**Table number.** Among all weak-link rows with `result` and `answer`, fraction where `answer.methods[result.weakest_index - 1] === method`. Viewer helper `pickedRate`. The three percentages divide the same 244 slates and sum to 100%. Scoring script has no weak-link accuracy key.

**Direction.** Lower is better.

**Chance.** 33% (1 of 3). Human control sits in every slate.

**Frozen denominator.** 244 shared slates, not 244 per method.

**Frozen result.** Our method 71 / 244 (29.1%). ZLG 116 / 244 (47.5%). Human control 57 / 244 (23.4%). The human count is in the frozen report interpretation column. Include it.

**Sign test.** None in the scoring artifact. Descriptive only.

### J3 suspicion AUROC vs human

**Ask.** Score the reviewed comment from 0 (genuine human) to 100 (machine-generated or edited). Do not treat bluntness, mistakes, or poor punctuation as evidence. Optional tell labels from a closed list: `generic_could_fit_any_thread`, `ignores_thread_specifics`, `register_mismatch`, `unnatural_phrasing`, `repetition`, `over_hedged`, `over_polished`, `contradicts_thread_facts`, `none`.

**Prompt / schema.** `suspicion_v1.txt`, `suspicion_v1.schema.json`. Returns `suspicion` (0-100), `tells`, `evidence`.

**Slate** (`build_pointwise`). Three tasks per pair sharing the post and the same five context comments: our method, ZLG, and one random held-out human comment. Hidden answer: `{human: true/false}`. The table does not use that boolean.

**Table number is not the mean of `suspicion`.** It is AUROC of that method's scores against the human-arm scores, stored in `codex_judge_summary.json` as `suspicion.auroc.{our_method,zlg}`.

Mann-Whitney / Wilcoxon form in `judge_scoring_service.py` `auroc`:

```
wins = sum( 1 if p > n else 0.5 if p == n else 0
            for p in method_scores for n in human_scores )
AUROC = wins / (|method_scores| * |human_scores|)
```

On a complete frozen run that is 244 x 244 pairwise comparisons per method, not 244 cluster means.

**Direction.** Lower AUROC is closer to the human distribution / chance.

**Chance.** 0.5.

**Frozen result.** Our method 0.661. ZLG 0.650. Print three decimals, as the frozen report does. The viewer display rounds to two decimals. The paper follows the report.

**Paired sign test (not a test of AUROC).** `post_cluster_summary` on non-human raw `suspicion` scores, one cluster per `post_id`. Frozen report: "no clear post-cluster difference (p=0.385)". That p-value is the two-sided sign test on paired raw scores (our method minus ZLG per post), **not** a test of the 0.011 AUROC gap. No AUROC confidence interval is stored. Source: frozen report; `score_codex_judgments.py` `_summary`; viewer limit text in `judge-copy.ts` (the distinction is real; the extra bootstrap story in that file is not in the scoring artifact).

### J4 thread attribution accuracy

**Ask.** Given one comment and four thread blurbs, choose the thread the comment belongs to, even if uncertain.

**Prompt / schema.** `attribution_v1.txt`, `attribution_v1.schema.json`. Returns `thread_index` (1-4), `confidence` (0-100), `evidence`.

**Slate** (`build_attribution`). Seeded RNG draws 3 other posts from the judge corpus (prefer same subreddit if at least 3 same-subreddit alternatives exist; otherwise any other posts), appends the true post, shuffles. Fields for i=1..4: `sub_i`, `title_i`, `snippet_i` (post body truncated to 700 characters). Same four-thread slate for our method, ZLG, and a random human comment. Hidden answer: 1-based `thread_index` of the true post. Three tasks per pair.

**Table number.** Per-method fraction where `result.thread_index === answer.thread_index`. Viewer `rate(..., "attribution", method, "thread_index")`. Scoring script also writes `summary.attribution.accuracy[method]`, excluding the human arm.

**Direction.** Higher indicates stronger thread-specific linkage.

**Chance.** 25% (1 of 4).

**Frozen denominator.** 244 / 244 per table column (our method and ZLG).

**Frozen result.** Our method 89.3%. ZLG 75.0%. Frozen report does not print a human-arm accuracy. Viewer computes one via the same `rate` helper. Do not add it to the paper table unless a later ticket cites a frozen source for it.

**Sign test.** None in the scoring artifact. Frozen report: "descriptive only here."

### J5 register-fit score (1-5)

**Ask.** Using five genuine subreddit comments as register examples, score the candidate's style only. Fields: `tone_formality`, `length_norm`, `mechanics`, `insider_knowledge`, `overall`. Each 1 (out of place) to 5 (indistinguishable).

**Prompt / schema.** `register_v1.txt`, `register_v1.schema.json`. All five integers required, plus `evidence`.

**Slate.** `build_register` delegates to `build_pointwise("register", ...)`. Same shape as J3 (three tasks per pair), independently seeded.

**Table number.** Arithmetic mean of numeric `result.overall` on register rows for that method. Viewer `meanScore(rows, method, "overall")`, `toFixed(3)`. Sub-scores are stored on each judgment (`codex_register_*` after merge) and **do not** enter the table cell.

**Direction.** Higher is better.

**Chance.** None. This is not an identification task.

**Frozen denominator.** 244 overall scores per table column. Sign-test rollup uses 244 paired post-cluster deltas.

**Frozen result.** Our method 3.193. ZLG 2.791. Our method higher by 0.402 post-cluster points; 106 wins, 67 losses, 71 ties; paired sign-test p=0.00374.

Human-arm mean 3.402 appears in viewer copy (`judge-copy.ts`) from `meanScore(..., "human", "overall")`. It is **not** in the frozen report table. Do not add it unless ticket 03 names a frozen source.

---

## Scoring formulas (copy into LaTeX)

### Identification rate (J1, J4)

For method m, metric k, key f (inserted_index or thread_index):

```
rate(m) = (# valid tasks for m where result[f] == answer[f]) / (# valid tasks for m)
```

Valid means the judgment has both `result` and `answer` and no error.

### Pick rate (J2)

```
picked(m) = (# weak-link tasks where answer.methods[result.weakest_index - 1] == m)
            / (# weak-link tasks with result and answer)
```

Denominator is the number of slates, shared by human, our method, and ZLG.

### AUROC (J3)

As above. Ties contribute 0.5. Chance is 0.5. Independent of post pairing. Human scores are the negative class, method scores the positive class, so AUROC here is "how well suspicion ranks method text above human text." Lower is better for stealth.

### Mean overall (J5)

```
mean(m) = arithmetic mean of result.overall over register tasks with method m
          and a numeric overall
```

### Post-cluster paired sign test (J3 raw scores and J5 overall)

`judge_scoring_service.py` `post_cluster_summary`:

1. Group numeric scores by `post_id` then method.
2. For each post that has both control (`our_method`) and treatment (`zlg`), delta = mean(control) - mean(treatment). On this frozen set there is one pair per post, so the cluster mean is the single score.
3. wins = count(delta > 0), losses = count(delta < 0), ties = count(delta == 0).
4. trials = wins + losses (ties dropped).
5. Two-sided exact sign test, binomial n = trials, p = 1/2:

```
p = min(1, 2 * sum_{i=0}^{min(wins, losses)} C(trials, i) / 2^{trials} )
```

Verified against the frozen register counts: wins=106, losses=67, ties=71, trials=173, p = 0.003737... which the report prints as 0.00374.

Control minus treatment is also stored as `our_minus_zlg_post_cluster_mean` when those names are used. Frozen register value: 0.402.

The scoring script computes this rollup for **suspicion and register only**. Frozen report presents register's test as the claimed significance result, and quotes suspicion's p=0.385 only as "no clear post-cluster difference." J1, J2, and J4 have no paired test in the artifact. Raw differences on those rows are descriptive.

### Holm adjustment

`holm_adjust` is applied to the list of `two_sided_sign_test_p` values from metrics that have a `post_cluster` block (suspicion and register, if both have been scored). Step-up: sort finite p-values, `adjusted = max(prior, min(1, p * (n - rank)))`.

The frozen report **does not quote Holm-adjusted p-values**. Print the unadjusted p=0.00374 and p=0.385 as the report does. If a later pass needs Holm, two tests with those p-values adjust to about 0.00748 (register) and 0.385 (suspicion). Register remains below 0.05. Do not invent Holm numbers in the paper unless the frozen summary JSON is cited.

---

## Frozen 244-pair result table

Copy these cells. Source: `stego-side-wing/docs/reports/2026-08-29-independent-llm-judge-results.md`, Results. All figures use the 244 selected post clusters.

| Criterion | Our method | ZLG | Interpretation |
| --- | ---: | ---: | --- |
| Standout detection | 126 / 244 (51.6%) | 69 / 244 (28.3%) | Lower is better; ZLG was less often identified in the 10-way slate. |
| Weakest text picked | 71 / 244 (29.1%) | 116 / 244 (47.5%) | Lower is better; the human control was picked 57 / 244 (23.4%). |
| Suspicion AUROC vs human | 0.661 | 0.650 | Lower is closer to chance/human; no clear post-cluster difference (p=0.385). |
| Thread attribution accuracy | 89.3% | 75.0% | Higher indicates stronger thread-specific linkage; descriptive only here. |
| Register-fit score (1-5) | 3.193 | 2.791 | Our method higher by 0.402 post-cluster points; 106 wins, 67 losses, 71 ties; paired sign-test p=0.00374. |

Which helper feeds which cell (viewer, same numbers):

| Cell | Computed from | Helper / field |
| --- | --- | --- |
| J1 | loaded judgments | `rate(..., "inserted_index")` |
| J2 | loaded judgments | `pickedRate(...)` |
| J3 | `codex_judge_summary.json` | `suspicion.auroc.{our_method,zlg}` |
| J4 | loaded judgments | `rate(..., "thread_index")` |
| J5 | loaded judgments | `meanScore(..., "overall")` |

Source: `llm-judge-panel.tsx` `FullResults`; `llm-judge.ts`.

---

## Reporting limits (use in the paper)

From the frozen report, Interpretation limits. Keep all four.

1. Selection removes repeated ZLG covers and uses one pair per post. That addresses non-independence in an earlier raw judge workload, and it changes the evaluand to the unique-output subset.
2. Judge scores are model-based measures, not reader studies. They must not be reported as proof of human authorship, security, or general naturalness.
3. Capacity remains non-comparable across these systems without a separately frozen, capacity-matched experiment using real receiver verification.
4. Report failure and acceptance rates from the source comparison run alongside these conditional fixed-text judgments. Do not combine their denominators.

Additional limits that are true in code and belong in a short methods paragraph:

- The judge is not deterministic (`reasoning_models_are_not_deterministic`). Slates are seeded. Re-running the model can move answers.
- Only register has a claimed paired post-cluster significance test. J1/J2/J4 differences are descriptive. J3's p=0.385 is a sign test on raw suspicion scores, not on AUROC.
- Human-arm tasks exist for J2 (in-slate control, reported), J3 (AUROC reference distribution, not a table mean), J4 and J5 (scored, not in the frozen table).
- `CONTEXT.md` forbids calling this G-Eval, a human evaluation, or a naturalness proof.

---

## Docket secondary note, verified

`stego-results-viewer/docs/docket/research/what-each-criterion-measures.md` matches the code on prompts, slate builders, helpers, chance rates, and denominators. Safe to trust as a map. Two cautions for the paper agent:

- Its J5 note about a "human-anchor comparison follows below" is viewer UI copy. The frozen report has no human-arm register mean.
- Extra qualitative counts in `judge-copy.ts` (tell tallies, 3.402, 75.4% human attribution, polish-on-70-of-126, and so on) are justification-page analysis, not the scoring artifact. Out of scope for this protocol subsection unless another research ticket freeze-cites them.

---

## Source index

| Claim class | File |
| --- | --- |
| Frozen counts, table, Codex Luna, limits | `stego-side-wing/docs/reports/2026-08-29-independent-llm-judge-results.md` |
| Subset rule | `stego-side-wing/scripts/build_independent_judge_subset.py` |
| Task emission, hashes, campaign | `stego-side-wing/scripts/run_codex_judge.py`, `run_codex_judge_campaign.py` |
| Slates, cleaning, seeds | `stego-side-wing/src/services/judge_slate_service.py` |
| Prompts and schemas | `stego-side-wing/config/evaluation_prompts/{standout,weak_link,suspicion,attribution,register}_v1.txt` and `schemas/` |
| Merge, AUROC wiring, Holm list | `stego-side-wing/scripts/score_codex_judgments.py` |
| Sign test, AUROC, Holm formulas | `stego-side-wing/src/services/judge_scoring_service.py` |
| Model ids, schema validation | `stego-side-wing/src/services/codex_judge_client.py` |
| Viewer rate / pick / mean | `stego-results-viewer/src/app/zlg-comparison/_lib/llm-judge.ts` |
| Chance strings, extra (non-frozen) copy | `stego-results-viewer/src/app/zlg-comparison/_lib/judge-copy.ts` |
| Default run directory | `stego-results-viewer/src/app/zlg-comparison/_lib/data.ts` |
| G-Eval | `stego-side-wing/config/evaluation_prompts/geval_v1.txt`, `scripts/run_paired_quality_judge.py`, `scripts/score_paired_quality_judgments.py` |
| Glossary | `project_paper/CONTEXT.md` |
