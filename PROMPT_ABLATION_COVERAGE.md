# Prompt ablation and G5 evidence

The author recalled testing multiple embedding prompts and requested an account if backed by evidence. Before this revision, the paper mentioned G5 only in the six-post archive comparison; it did not explain the larger prompt-development study.

## Verified primary material

Backend-relative saved runs:

- `metrics/experiments/wren/g0_g3/g0_g3_live_20260919`: four conditions on 48 posts, 192 post/condition assignments.
- `metrics/experiments/wren/g4_g5_barb/g4_g5_barb_screen48_20260919`: three additional conditions on the same 48 posts, 144 assignments.
- `metrics/experiments/wren/g0_g3_j1/j1_screen48_20260919`: 149 valid standout judgments.
- `metrics/experiments/wren/g4_g5_barb/j1_screen48_20260919`: 87 valid standout judgments.

`scripts/build_prompt_ablation_evidence.py` reads both manifests and all 336 attempt records, checks uniqueness and the common 48-post set, verifies identical selected parent/topic identities across conditions, joins all 236 tasks and judgments, and checks the judged carrier against the accepted generated text and inserted candidate. It also checks that the 48 posts form four strata of 12 within the original 244-post judge set. Sources and SHA256 values are in `common/data/prompt_ablation_evidence.json`; both languages consume generated rows and values from the companion TeX file. No model calls were made for this revision.

Reproduce from the paper repository:

```powershell
python scripts/build_prompt_ablation_evidence.py
python scripts/build_dataset_overlap_evidence.py
```

## Conditions and endpoint

G0/G1 retain reflective and subject/action/emotion instructions, without/with a target topic. G2/G3 request one local conversational act, without/with a target. G4 adds three fixed human-style examples to G2; G5 adds them to G3. A seventh, argumentative condition retains the target but asks for a pointed thread-specific reply. This is an exploratory prompt/component screen. Target-bearing conditions also invoke sender validation, whereas no-target controls do not; the target-presence contrast includes this acceptance difference.

Crucially, `_finish_arm` in `scripts/run_wren_g0_g3_pilot.py` sets `accepted_exact` from `evaluate_candidate_groups(...).succeeded`. It does not run a full independent payload extraction. Historical summary keys named `exact_recovery_n` therefore count topic-validated candidates in this screen. The paper labels this endpoint **topic verified**. No-target controls have an inapplicable check, not a 0% payload-recovery result.

| Condition | Produced /48 | Topic verified /48 | Detected / judged |
| --- | ---: | ---: | ---: |
| G0 | 48 | n/a | 12/48 |
| G1 | 46 | 24 | 12/24 |
| G2 | 48 | n/a | 12/48 |
| G3 | 46 | 29 | 15/29 |
| G4 | 44 | n/a | 2/44 |
| G5 | 41 | 28 | 10/28 |
| Argumentative | 39 | 15 | 11/15 |

The selected source posts have known historical outcomes; this is development, not an untouched confirmation sample. Judge denominators are available control texts or accepted target-bearing texts. They are not the 48 assignments for every condition. The saved judge metadata names GPT-5.6 Luna with high reasoning. The primary generation manifests record selection and conditions, but do not themselves constitute a full frozen generator/runtime identity; the paper does not claim byte-identical rerun conditions or optimal prompt selection.

## Interpretation and exclusions

G3 and G5 both have accepted comments on 21 posts. Each is detected on eight of these posts. Thus comparing 15/29 with 10/28 alone cannot isolate a benefit of adding examples. G1 and G3 share 19 judged posts (eight versus nine detections); G1 and G5 share 17 (eight versus five). These are descriptive intersections, not additional independent samples or confirmatory hypothesis tests.

The trace-enabled rerun `g0_g3_traced_screen48_20260920` records 28 verified G1 cases and 33 G3 cases; it is separate from the primary 24/29 counts. Earlier partial/first-draft snapshots and their 176-task judgment set are also not the accepted-text 149-task primary set. The paper's table does not pool or replace these generations. Other editing, parent-codebook, acceptance-policy, and judge-format diagnostics in the development directory are outside this focused prompt account.

The later six-post archive experiment has a different endpoint and context preparation: complete-message recovery, with four primary anchored successes and no G5 complete recoveries. Its generation/validation and acquisition failures do not establish inferior prose quality. The two stages are explained together without equating 28 topic-valid G5 comments with 28 independently recovered messages or treating 0/6 as a refutation of every use of G5.

## Paper placement

`sections/prompt_ablation.tex` in both languages explains the design, sampling, endpoint, results, common accepted subset, and connection to the archive follow-up. The dataset and endpoint overview tables now include this previously omitted study as a tenth evidence group; it remains nested in the original judge posts. The archive section points back to the definition of G5. Existing baseline, recovery, and judge results are preserved.

## Verification

Both papers compile successfully (English: 57 pages; Arabic: 88 pages), with no unresolved citations or references. The new subsection and updated dataset/endpoint tables were rendered and checked visually in both languages. The evidence builder validates all 336 assignments and 236 accepted-text/judgment joins. Existing baseline coverage and experiment-label checks pass; the four previously checked result tables retain their numeric values. Both abstracts remain unchanged.
