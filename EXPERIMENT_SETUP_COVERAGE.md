# Experiment setup and evaluation roadmap

## Reader-facing changes

The bilingual `sections/experiment_setup.tex` appears after the dataset and outcome overviews, before baseline rationale. Its research story moves from comment quality and prompt components to complete-message extraction with prepared context, then to independent archive preparation. This connects questions rather than inventing one chronological experiment or treating overlapping samples as independent replications.

The configuration table separates the initial comparison, fixed comment-quality comparison, prompt screen, source-excerpt recovery, independent-payload development, and archive studies. Supporting preparation, capacity, reply-chain, and offline transport checks keep their own conditions in the existing overview. The prose identifies generation, topic identification, and quality judging as separate roles; two total attempts mean one retry. Historical settings are not replaced by current defaults.

## Evidence and scope

`python scripts/build_experiment_setup_evidence.py` reads saved artifacts and emits `common/data/experiment_setup_evidence.json` with SHA256 source identities and selected settings. It changes neither backend artifacts nor SLR sources and makes no model/API calls.

- The source-excerpt manifest supplies anchored writing at temperature 0.7, six retries after the first attempt, a twelve-carrier command limit, Qwen 3.5 9B identity, and the RTX 5060 Ti device-memory record.
- The independent-payload manifest requests GPT-6 Luna with low reasoning, eight-byte payloads, twenty carriers, and one retry. The earlier diagnosis records unavailable effective CLI temperature; do not infer zero or 0.7.
- Archive policy manifests separately pin writer/identifier temperatures 0.7/0, twenty carriers, and the Qwen Q4_K_M runtime with a 16,384-token loaded context. Their quality freeze pins GPT-OSS 20B at zero. The table distinguishes these later panels from the earlier anchored/G5 comparison.
- The comment-quality campaign's saved generation settings name Qwen 3.5 9B and the natural writing package; the baseline summary records its own Qwen GGUF identity. The source experiment's effective one-retry setting is retained from the established campaign account, rather than confusing the saved balanced-profile default of six with the invocation limit. Judge metadata identifies GPT-5.6 Luna with high reasoning.
- The original initial-comparison table and prompt-screen manifests do not establish complete historical generator/runtime identities. The table marks that exact scope of missing metadata. No matching quantization or hardware identity is projected backward from the archive panels.
- Preparation, generating candidates, validating candidates, selecting accepted replies, and receiving carriers have different computational costs. Shared-state experiments exclude fresh acquisition; summed model-call durations are not declared total elapsed latency.

Exact artifact paths and hashes are in the generated JSON, outside the manuscript. The existing prompt-ablation, recovery, archive, and baseline evidence records retain the underlying result provenance. The original result-table values are preserved.

## Roadmap image

`EXPERIMENT_ROADMAP_FIGURE_PROMPT.md` contains complete standalone English and Arabic generation prompts. Its three main questions are whether the comment fits, whether the whole message can be recovered, and whether the receiver can rebuild the context. A subordinate band identifies list agreement, capacity planning, and transport integrity as supporting checks. It carries no numerical results or model settings.

The author supplied and approved both generated images. They are copied unchanged to `stego_paper/figures/evaluation_roadmap_en.png` and `stego_paper_ar/figures/evaluation_roadmap_ar.png`. Both LaTeX files include the matching image directly, with a caption, introductory reference, and label `fig:evaluation-roadmap`, before the configuration table. Arabic reads right to left and English left to right. No artwork step remains pending.

## SLR integration

See `SLR_SELECTION_EVIDENCE.md` for the documented search protocol and exact extraction-ID/citation-key mapping. The companion evidence script confirms the 31 completed CSV records match both application-study tables. The manuscript uses the existing `olabi2026slr` unpublished entry, retains primary-study citations, and summarizes relevant findings without turning this paper into another full review. The broader draft's conflicting 32/33/34 totals and unsupported shared-dataset percentage are not imported. Both abstracts and all SLR source files remain unchanged.

## Completed checks

The image-inclusive papers compile successfully: English 60 pages, Arabic 93 pages. No citations or references are unresolved. The source-settings and bilingual 31-study checks passed in the text revision, as did the baseline-coverage and experiment-label checks. Four checked baseline/judge result tables retain their numeric values; neither abstract has a diff. The earlier SLR and setup pages were visually checked, with table placement corrected to follow their introductions. After adding the author-approved images, English PDF pages 38–40 and Arabic PDF pages 58–60 were rendered and inspected. Figure 10 is readable in each language, its caption is intact, and it precedes the configuration table. Arabic's figure is on printed page 57. The copied image bytes match the supplied originals.
