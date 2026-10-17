# Evidence for the literature-review provenance

Read-only inspection of `D:/Master/SLR draft`; no source files in that repository were changed. This report supports a brief explanation in the bilingual project paper, not a replacement SLR methodology section.

## Main finding

The project paper's 31-study set has a concrete extraction basis: **all 31 dated records in the supplied SLR CSV correspond to the 31 distinct citation keys enumerated in the project paper's application table**. The CSV also contains seven undated records without completed extraction. The dated records span 2020–2025: 2, 1, 2, 5, 14, and 7 studies respectively. Thus the project's existing 10 earlier / 21 later split is supported.

Do not describe 31 as the final total of the supplied SLR manuscript. Its current prose and tables disagree about that total. Describe this paper as drawing on the **31 extracted studies used in its synthesis**, from the author's broader SLR.

## Search and selection protocol actually documented

All paths in this subsection are under `D:/Master/SLR draft/`.

| Evidence | Source |
| --- | --- |
| Review planned around publication state, applications, evaluation, external knowledge, and limitations | `sections/research_method.tex:12–21` |
| Search string: `(steganography OR watermark OR "Information Hiding") AND ("Large Language Model" OR LLM OR BERT OR LAMA OR GPT)` | `sections/research_method.tex:24–29` |
| ACM Digital Library, IEEE Digital Library, ScienceDirect, Scopus, and SpringerLink; backward reference snowballing | `sections/research_method.tex:29` |
| Full text, English, from 2018, peer-reviewed journals/conferences/workshops; relevant LLM-related information hiding; empirical, review, or theoretical contributions | `sections/research_method.tex:34–42` |
| Duplicate/incomplete/irrelevant/non-English exclusions; generally excludes non-peer-reviewed sources | `sections/research_method.tex:45–52` |
| 1,043 initial candidates, split 346 + 61 + 209 + 151 + 276 across the five sources | `sections/research_method.tex:55–56` |
| Parsifal deduplication, followed by title/abstract/full-text screening; 58 after title/abstract screening | `sections/research_method.tex:58` |
| Data extraction covers bibliography, model/access/method/code, datasets, context representation/use, evaluation, strengths/weaknesses | `sections/research_method.tex:60–72` |

The manuscript describes the protocol, but this inspection did not locate a complete per-candidate screening audit, the actual search execution dates, or a recoverable duplicate-removal count. Do not invent those details or claim an independently reproduced exhaustive search. The misspelling `LAMA` is in the recorded query; do not silently report a different executed query. A short manuscript insertion need not reproduce the string at all.

## Count reconciliation and membership

| Artifact | Count actually present | Implication |
| --- | --- | --- |
| `data/SLR - SLR-Deep.csv:2–152` | 31 dated/extracted records | Matches project synthesis membership |
| Same CSV, lines 153–159 | 7 undated/pending records | Excluded from the 31-study denominator |
| `draft.tex:30`, `sections/research_method.tex:58`, `sections/results.tex:4`, `sections/conclusion.tex:3` | 34 claimed accepted studies | Inconsistent with current extraction CSV |
| `sections/rq1_literature_state.tex:5,23` | 32; publication table has 8 in 2025 | Current CSV has 7 in 2025 |
| `sections/rq1_literature_state.tex:32–50` | Model-family table uses denominator 34 | Do not transfer its percentages into project31 |
| `sections/rq2_applications.tex:21–31` | 33 distinct citations | Different membership and several questionable category assignments; not a replacement for project table |
| `sections/threats.tex:12` | 6 pending | Current CSV has 7, including RS-Stega |
| `accepted_papers_buckets.md:3` | Says 34, lists a later selection spanning 2025–2026 | A separate selection artifact; not the project's extracted31 corpus |

The SLR's 33-key application table adds `chen2025cdea`, `ou2025multigranularity`, and `math9212829` relative to the project31, but omits `hao2025robust`. Its inclusion of a survey (`math9212829`) in a primary-method category and assignments such as ALiSa to black-box writing mean it should not be copied wholesale.

Exact mapping from the extraction CSV to project citation keys (CSV physical starting line in parentheses):

| CSV ID | Project citation key | CSV line |
| --- | --- | --- |
| 25 | `hao2025robust` | 2 |
| 43 | `wang2025contrastive` | 3 |
| 44 | `kuznetsov2025deepstego` | 4 |
| 45 | `shi2025emotionally` | 5 |
| 47 | `wozniak2025multicriteria` | 6 |
| 48 | `lin2025positionagnostic` | 7 |
| 50 | `chen2025activetwo` | 8 |
| 3 | `liao2024co` | 9 |
| 6 | `wu2024generative` | 10 |
| 8 | `lin2024zero` | 21 |
| 9 | `qi2024provably` | 29 |
| 10 | `ji2024principled` | 33 |
| 11 | `ding2023context` | 42 |
| 12 | `munyer2024deeptextmark` | 51 |
| 13 | `wang2023hi` | 57 |
| 15 | `steinebach2024natural` | 64 |
| 19 | `li2024imperceptible` | 67 |
| 20 | `li2024semantic` | 74 |
| 21 | `xu2024beyond` | 77 |
| 23 | `zhang2024controllable` | 78 |
| 24 | `pang2024fremax` | 84 |
| 4 | `ding2023joint` | 87 |
| 5 | `ding2023discop` | 98 |
| 16 | `qiang2023natural` | 109 |
| 17 | `li2023rewriting` | 110 |
| 22 | `xiang2023cpg` | 115 |
| 2 | `zheng2022general` | 118 |
| 18 | `yi2022alisa` | 125 |
| 7 | `kaptchuk2021meteor` | 133 |
| 1 | `yang2020vae` | 139 |
| 14 | `zhang2020linguistic` | 148 |

CSV records contain embedded newlines; use `csv.DictReader`, not physical-line counting, to count studies. All 31 keys above exactly equal the union of citations inside `stego_paper/sections/related_work.tex`'s `tab:app_distribution` table. The Arabic table mirrors that bounded synthesis.

## Findings worth briefly connecting to this project

1. **Access and context differ between methods.** The SLR describes generative, rewriting, black-box, and context-aware approaches (`sections/rq1_literature_state.tex:7`; `sections/discussion.tex:6–8`). This supports separating practical access requirements from claimed novelty and explains why superficially similar methods are not interchangeable baselines.
2. **Contextual fit requires more than fluent standalone text.** Retrieval, semantic control, examples, and other contextual resources recur in the review (`sections/conclusion.tex:7`; `sections/rq4_knowledge_integration.tex:106–136`). This motivates reply/context fit criteria in our evaluation, without proving our implementation is superior.
3. **Capacity, language quality, detectability, and recovery need separate evidence.** Different datasets, tokenization, models, formulas, and attacks limit cross-paper rankings (`sections/threats.tex:8`; `sections/discussion.tex:24–26`; `sections/conclusion.tex:5–9`). This supports the project's staged evaluation and explicit baseline conditions.

Avoid importing unsupported quantitative generalizations. For example, `sections/rq3_evaluation_metrics.tex:210–213` says 20% shared datasets, 25% human assessment, and 60% missing attack tests, whereas its own detailed table reports one human-evaluation study (`:233`) and several differently defined robustness categories (`:243–245`). Those figures require record-level recoding, not a new denominator alone. The project's existing detailed claims should be described as its extraction/classification results; “20% shared datasets” has no visible enumeration in the supplied artifacts and is safest omitted or rewritten qualitatively.

## Suggested brief insertion scope

Place a compact provenance paragraph at the beginning of Related Work, followed by one short bridge from the review findings to this paper's design/evaluation. Retain individual primary-study citations throughout; identify the broader SLR as the author's review/draft, with honest unpublished bibliographic status if cited. Do not add another SLR-sized methods section or a PRISMA figure to this implementation paper.

English content: “This section draws on our systematic literature review of LLM-based linguistic steganography. The review searched five digital libraries and supplemented database retrieval with backward snowballing; studies were screened by title, abstract, and full text, and extracted by method, model access, context use, and evaluation. The synthesis here uses the 31 studies with completed extraction records, published in 2020–2025. Watermarking studies serve as adjacent evidence and are distinguished from covert payload transmission.”

Arabic content: «يستند هذا القسم إلى مراجعتنا المنهجية لأبحاث الإخفاء اللغوي باستخدام النماذج اللغوية الكبيرة. شملت المراجعة البحث في خمس مكتبات رقمية، وفحص مراجع الدراسات المختارة للعثور على أعمال إضافية، ثم فرز الدراسات بحسب العنوان والملخص والنص الكامل. وجُمعت بيانات كل دراسة عن آلية العمل، ونوع الوصول إلى النموذج، واستخدام السياق، وأساليب التقييم. ويعتمد العرض هنا على 31 دراسة اكتملت بيانات تحليلها، ونُشرت بين عامَي 2020 و2025، مع التمييز بين نقل الرسائل السرية وأعمال العلامات المائية ذات الصلة.»

No publication-date labels for manuscript versions are needed. The 2020–2025 span describes the literature, not a software/experiment version.
