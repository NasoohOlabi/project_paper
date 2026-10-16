# Research structure comparison with the reference thesis

Date: 16 October 2026. Manuscript reviewed: Arabic version at commit `135d6b6`. This report recommends changes; it does not change the paper or its abstracts.

## Review progress

The findings below describe the reviewed commit. Subsequent author-approved edits correct the Arabic chapter map, distinguish development-only reconstruction validation from deployed behavior, revise the contributions to separate black-box operation from shared-list coordination, define API in both languages, and broaden the second Arabic research question to cover sender generation, receiver extraction, and failure causes. These edits address parts of the scope and framing findings; the remaining recommendations still require individual review.

The author's terminology correction applies throughout the Arabic paper and to all future revisions arising from this report: translate experimental **run/runs** as **تجربة/تجارب**, or **اختبار/اختبارات** for a specific validation check. Do not use **تشغيلات/التشغيلات**. Technical expressions such as **نظام التشغيل** and **زمن التشغيل** retain their meaning. The Arabic writing guide records this rule, and existing research-run wording has been revised across the Arabic chapters. English “run” and recorded artifact identifiers remain unchanged.

Development validation and message-extraction experiments are separate forms of evidence. The recommendations do not require processing every dataset post twice or adding repeated processing to deployment. Any claim about a successful validation must be supported by its records.

## Main finding

The paper has the main research components already: motivation, problem, objectives, research questions, contributions, related work, methodology, implementation, experiments, limitations, and future work. It does not need to acquire the reference thesis's chapter count or length.

The main weakness is the connection between those components. The reference repeatedly explains **what question a design choice addresses, how it is tested, and what the result allows the author to conclude**. Our manuscript contains much of that information, but distributes it across general descriptions, dated experiments, and repeated qualifications. Readers have to reconstruct the research argument themselves.

The highest-value revision would connect the existing evidence to explicit questions, distinguish the evaluated configurations, and show one complete implementation example. Adding paragraphs indiscriminately would make the manuscript longer without resolving those problems.

## Scope and evidence

The comparison uses the supplied [reference thesis](<Example Previous Papers.pdf>), an Arabic HIAST doctoral thesis on a syntactic-semantic representation of software requirements, and the current Arabic LaTeX sources. The reference is scanned, so relevant passages were read from rendered pages. This is a targeted structural reading, not a technical audit of every reference-thesis claim or a review of university regulations.

Reference pages below use **printed page numbers**. For the cited main-body pages, add 28 to obtain the PDF viewer page. Thus reference p. 102 is PDF page 130. Manuscript sources are identified by filename, section, and line where useful; line numbers describe the reviewed commit.

Evidence labels distinguish different kinds of recommendation:

- **Correction:** the current manuscript contains a concrete navigation or consistency problem.
- **Presentation gap:** the information is absent from the exposition, too compressed, or scattered. Existing records may be sufficient to fix it.
- **Evidence gap:** stronger conclusions require additional analysis or experiments. Writing alone cannot close it.
- **Optional:** useful only if it supports the intended claims and audience.

The reference supplies examples of research practice. It does not establish that its particular datasets, annotation procedures, learning algorithms, or validation splits should be copied into a steganography study.

## What the reference does that is worth transferring

| Research function | Evidence in the reference | Current manuscript | Difference that matters |
| --- | --- | --- | --- |
| Turn a broad problem into smaller questions | Sections 3.4.1 and 4.3.3–4.4.2, printed pp. 32 and 61–65 | Introduction has three research questions; methodology explains the stages | Questions exist, but the later experiments are not consistently presented as answers to those questions. |
| Explain why the proposed representation or mechanism is needed | Sections 4.2–4.4, pp. 58–65; sections 6.2–6.3, pp. 118–124 | Methodology gives purpose-first explanations, equations, and diagrams | Much improved already. Some implementation choices still appear as settings without a clear account of whether they are defaults, constraints, or experimentally chosen values. |
| Make the procedure inspectable | Section 5.4, pp. 93–102: overall diagram, decomposition into subproblems, definitions, pseudocode, and an illustrative output table | Methodology has diagrams and component examples; implementation lists five stages and describes the codec | The missing device is a continuous example showing the same message through preparation, choices, writing, and extraction. Another overview diagram would add less. |
| Define the experimental construct before measuring it | Section 4.5, p. 66 defines the intended semantic relation and connects tests to questions | Terminology and evaluation distinguish quality, available bits, sender acceptance, and extraction | These distinctions exist, but the paper needs a more visible mapping from each claimed property to its actual measure. |
| Justify data selection and preparation | Sections 4.5.1 and 5.5.1, pp. 66–70 and 105: source choice, annotation, cleaning, and coverage | Judge subset selection and archive eligibility are explained; historical source-population description is less consolidated | A reader can understand the filtering of some experiments more easily than the origin and coverage of the full set of source posts. |
| Separate design tuning from evaluation | Sections 4.5 and 4.6, pp. 70 and 86–87; section 7.3, p. 143 | Development versus previously unused archive posts is explicit; earlier and later runs have different roles | The distinction is present for the archive study but is not equally visible across the whole evaluation chapter. |
| Explain comparison alternatives and their relevance | Section 4.5.3, p. 80; section 5.5.5, p. 112; section 7.4, p. 144 | Related work compares mechanisms, and evaluation uses the official ZLG baseline | Precedent, quality comparator, and fair extraction comparator are different roles. The paper should state which role each comparison actually serves. |
| Answer questions after reporting results | Section 4.5 discussion, pp. 84–85, explicitly returns to numbered questions | Results and qualifications appear throughout chapter 7 | A short question-by-question synthesis is missing. |
| Explain limitations as threats to particular conclusions | Sections 4.6, 5.6, and 6.5, pp. 85–87, 113–114, and 138 | There are substantial limitations in methodology, evaluation, and conclusion | The improvement is organization by affected claim and mitigation, not adding more generic disclaimers. |
| Close by contributions and practical implications | Section 8.1, pp. 155–159 | Conclusion summarizes results, then places several completed studies under future work | The conclusion should distinguish completed contributions, remaining limitations, and genuinely future work more cleanly. |

## Prioritized findings

### P0. Correct the manuscript's internal map and scope statements

**Type: correction. No new experiment required.**

The introduction's final subsection still assigns related work to chapter 3, methodology to 4, implementation to 5, evaluation to 6, and conclusion to 7. The actual input order includes terminology as chapter 3, making those chapters 4, 5, 6, 7, and 8. This is a concrete instance of a structural change not being propagated throughout the manuscript. See `stego_paper_ar/sections/introduction.tex`, subsection «مخطط الرسالة», and `stego_paper_ar/main_ar.tex`.

Some broad statements in the introduction and conclusion also describe the evidence as if it were limited to the older sender-assisted comparisons. Later archive experiments independently reconstruct the conversation-only list under a narrower local simulation. Neither description should erase the other. Qualify claims by experiment: historical comparisons, shared-preparation extraction, and archive reconstruction are different evidence levels. See `introduction.tex:31`, its contributions list, `conclusion.tex:15`, and `fresh_archive.tex:5–9`.

The introduction describes the topic list as coming from a domain dataset, whereas methodology 5.2 explicitly defines the source-text list using the post, comments, and domain documents. Clarify whether the introduction is a generalization or an outdated configuration description. Do not silently replace it without checking the intended method. See `introduction.tex`, «هدف البحث وحدوده», and `methodology.tex`, «قائمة النصوص المصدرية».

The reference's chapter map and local section introductions make it easier to locate the promised explanation. Correcting our map has higher priority than adding a chapter.

One related summary also needs reconciliation: `related_work.tex:346` calls the July quantity extractable capacity, while chapter 7 carefully distinguishes the available selection budget from independently extracted useful bits. Align the summary with the actual measure. When discussing compression limits, distinguish the 250-character bound in methodology from the 255-byte chunks of the other representation in implementation; these need explicit units and representation names, not an assumed contradiction.

### P1. Connect the research questions to the experiments and answers

**Type: presentation gap, with a possible framing update.**

The three introduction questions focus on the design, sender-assisted outcomes, and judged quality. Later independent-receiver and archive studies address an additional question that is not equally visible in that framing. The paper should either broaden the relevant question or introduce a clearly subordinate question about extraction under stated shared-input conditions.

Add a compact mapping near the beginning of chapter 7:

| Question | Relevant experiment | Measured outcome | Answer supported | Remaining limit |
| --- | --- | --- | --- | --- |
| How do the two choices carry bits? | Method specification and codec checks | Invertible choices and exact reconstruction under fixed inputs | Design-level answer | Does not establish linguistic identification reliability |
| How reliably does the implemented sender produce accepted text? | Historical generation runs | Accepted attempts and failure categories | Configuration-specific feasibility | Sender acceptance differs from later receiver success |
| How do accepted comments compare in contextual quality? | Five judge tasks | Task-specific scores on the selected paired subset | Mixed results by task | Model judgments, selected sample, no security conclusion |
| Under which tested conditions can the receiver extract a complete message? | Shared-preparation and archive experiments | Exact complete-message extraction across all assigned attempts | Restricted empirical answer | No full live-platform/web reconstruction claim |

This is a suggested organizing device, not a proposed new result. End the evaluation with explicit answers using the existing evidence. The transferable pattern is the reference's return to its questions on pp. 84–85, rather than its exact number of questions.

### P1. Give the reader one complete worked implementation example

**Type: presentation gap.**

The paper already has a source-to-topic example, binary-choice illustration, sender/receiver diagram, and detailed examples of judge tasks. The earlier shape comparison should not be read as saying that examples are absent.

What is missing is continuity: one message followed through all the necessary representations. Use one clearly labeled illustrative example in chapter 6, or one recorded example if its artifacts support every step:

1. Public post and the relevant copy of its comments.
2. A small source-text list and the resulting indexed topic records.
3. Original message bytes and the selected payload representation.
4. Bit groups selecting the reply location and topic.
5. Generated comment, sender check, and acceptance or retry.
6. Receiver inputs, identified choices, reconstructed bits, integrity check, and final message.

If several comments are needed, show a short frame table and account for control bits and padding. Do not imply that a small invented example is a successful experimental run.

Reference pp. 93–102 combine definitions, stages, pseudocode, and outputs; pp. 118–124 carry one representation problem through diagrams and formal steps. Their useful lesson is traceability between representations.

### P1. Make chapter 6 describe the actual program's boundaries

**Type: presentation gap.**

Implementation 6.1 gives five stage descriptions, while 6.2 explains the common bit-processing module and 6.3 describes model settings. This covers the main flow, but leaves a reader assembling the concrete interfaces.

Add a compact table with each stage's input, output, producer/consumer, and persistence rule. Distinguish what the sender saves for analysis from what the receiver legitimately receives. Include list ordering, source references, configuration identity, and the behavior when an input is missing or a check fails. A file-by-file code tour is unnecessary.

A short sender procedure and receiver procedure could make termination and failure behavior explicit. Reuse chapter 5's explanation instead of copying it. The reference's explicit input/output pseudocode on p. 102 is a useful model for this purpose.

### P1. Introduce the experimental families before the dated results

**Type: presentation gap.**

Chapter 7 already contains an evidence-level table. Keep it. Its later position means the reader encounters several different meanings of success before seeing the whole map.

Move or adapt the overview to the start of evaluation and organize its rows by purpose: historical generation, paired quality, capacity planning, shared-preparation extraction, and independent archive reconstruction. For each row state the source population, payload type, receiver inputs, model/configuration, outcome, and reason for running the experiment. Dates remain useful provenance inside that structure.

This avoids treating the experiments as interchangeable or as an unexplained development diary. The reference introduces its experimental purpose before dataset and metric detail on p. 66, and its case study motivates the downstream task before reporting results on pp. 139–144.

### P1. Consolidate dataset provenance and sampling decisions

**Type: presentation gap; missing source information must be obtained from records.**

The judge subset is described carefully in `evaluation.tex:65–74`. Archive eligibility, community composition, and payload construction are explicit in `fresh_archive.tex:23–25`. Those are strengths.

The remaining need is a dataset overview across experiments. Explain the origin and collection period of source posts, eligibility/exclusions, comment selection and ordering, text language, repeated posts between studies, and why the tested communities suit the research question. Show how the initial population becomes attempted, accepted, paired, and judged samples. Do not combine counts from different campaigns into one funnel.

Reference pp. 66–70 and 105 explain both data choice and preparation. Transfer that explanatory function, not its human annotation protocol. Agreement between human annotators matters only if our own labels or claims depend on human annotation.

### P1. Explain design choices at the level of evidence actually available

**Type: presentation gap; sensitivity claims would require evidence.**

The manuscript specifies settings such as the topic limit, shortlist size, retry limits, generation settings, and frame budgets. What is less clear is how each was chosen.

Classify the important values as a protocol requirement, implementation/resource limit, inherited default, development choice, or experimentally compared value. Reconcile the reported 32-topic cap with the receiver description of a pool of up to 120 topics by identifying their scopes. See `methodology.tex:128`, its receiver procedure around line 217, and `implementation.tex:77–84`.

The reference explicitly separates representation choices, parameter comparisons, and later testing on pp. 70–72 and 86–87. Our paper should likewise avoid making a default sound optimal. Where no sensitivity study exists, say how the value was selected and leave robustness to that choice unestablished.

### P1. Explain baseline suitability and comparison fairness

**Type: presentation gap for rationale; evidence gap for stronger rankings.**

Related work already distinguishes the nearest mechanisms, including the keyword-based precedent and the compression component. Evaluation already discloses token-assisted extraction for ZLG and sender-assisted reconstruction for older project-side results. Do not remove those distinctions.

What is missing is a short explanation of why ZLG answers the particular comparison question despite its different channel and access assumptions. State which inputs and resources are shared, which differ, and which outcomes are genuinely comparable. The reference explains alternatives and dimensions of comparison on pp. 80, 112, and 144.

A broader fair extraction or security ranking would require new matched evidence. A closer black-box comparator is worth considering if such a ranking becomes a claimed contribution; it is not automatically a prerequisite for reporting the current restricted comparisons.

### P2. Separate a plausible mechanism explanation from a demonstrated effect

**Type: evidence gap, conditional on the claims retained.**

The archive comparison already varies retry budget and concise selection, and the reply-chain probe investigates a concrete mismatch. The paper therefore does not lack all component-level investigation.

However, the complete benefit of web-derived topics, reply-location selection, sender verification, or compression is not isolated by an otherwise matched comparison of each component. If the paper claims that one of these improves contextual fit or reliability, consider a targeted component comparison. Otherwise narrow the claim to the design rationale and observed configuration results.

This corresponds to the reference's parameter/component questions and comparisons on pp. 66, 70–72, and 84–85. It does not justify a large new experiment matrix merely to imitate the reference.

### P2. Consolidate assumptions, measurement validity, and generalization

**Type: presentation gap, with clearly bounded evidence gaps.**

The paper already discusses comment timing, changing sources, shared inputs, extraction conditions, judge limitations, editing, and untested security. A blanket claim that it lacks assumptions or limitations would be incorrect.

Make those limits easier to use. A compact assumptions and observation table in methodology can distinguish what both parties know, what an observer sees, which inputs are supplied in each experiment, and what is secret. A short validity subsection can then identify the conclusion affected by each issue, the mitigation used, and what remains unknown.

For example: unique-output filtering affects the quality sample; multiple comments per post affect independence; a model judge affects the interpretation of naturalness; source excerpts affect compression coverage; small development groups and early stopping affect reliability estimates. Much of this already appears in chapter 7 and can be reorganized without new data.

The reference explicitly separates method limitations, dataset validity, parameter selection, and evaluation-task validity on pp. 85–87 and 113–114. Our domain-specific observation assumptions are an adaptation to steganography, not a section copied from that thesis. A formal security proof is not required to describe the tested limits honestly.

### P2. Provide a compact reproducibility description

**Type: presentation gap; report unrecorded values as unavailable.**

Exact judge prompts are already in the appendix. Model settings and some runtime/call counts are reported. What remains scattered is the configuration needed to understand or repeat each experiment: model identifier/version, role, generation controls, topic construction mode, retry interpretation, payload type, execution environment, and artifact identifiers.

Add a setup table and, where available, references to the generation/topic-identification prompts or their versioned specifications. Explain the otherwise opaque G5 variant before relying on its result. For cost claims distinguish preparation, generation, checking, and reception; do not extrapolate an end-to-end latency from a run that reuses prepared inputs.

This is a reader-facing research description, not a request to expose credentials, add deployment instructions, or list every local API argument.

### P2. State how the related-work evidence was selected

**Type: presentation gap; the level of detail depends on the review claim.**

Chapter 4 derives counts and percentages from 31 studies, but does not give a comparably visible account of how that set was assembled. The reference explains its review method, questions, selection rationale, and validity in §§3.3–3.4 and 3.9, pp. 30–32 and 55.

Add a short description of the search/source scope, inclusion criteria, time cutoff, and how studies were classified, or identify the existing review record that supplies this information. Explain whether this is a structured selection for related work or a systematic review. A related-work chapter need not become a second full review study, but its numerical summaries should have a traceable basis. Do not invent a search protocol after the fact or import counts from a different review corpus.

### P2. Reorganize the conclusion around contributions and actual future work

**Type: presentation gap.**

The subsection «آفاق البحث المستقبلية» currently begins with completed October and archive results. Move those results into the contribution/findings synthesis. Reserve future work for unresolved tasks and explain which present result motivates each one.

End with a compact account of what the method demonstrates, what the evidence says about its practicality, and what remains untested. The reference follows a contribution-by-contribution account before future directions on pp. 155–159. Our conclusion can adopt that logic without expanding to six pages.

## Suggested revision order

| Order | Revision | Work needed | Completion condition |
| --- | --- | --- | --- |
| 1 | Fix chapter map and scope of older claims | Editorial, checked against current experiment descriptions | Introduction, methods, evaluation, and conclusion refer to the same chapter structure and evidence levels. |
| 2 | Map questions to evidence and answers | Synthesis of existing content | Each research question has an identifiable answer with its limit; later extraction studies have an explicit purpose. |
| 3 | Add the continuous example and implementation interfaces | Exposition plus verified examples/artifacts | A reader can follow one message from inputs to receiver output and identify what each party receives. |
| 4 | Put experiment families, data, and configuration in overview tables | Consolidation and record lookup | Each result has an identifiable sample, payload, configuration, receiver-input condition, and outcome. |
| 5 | Explain design choices and baseline rationale | Editorial plus provenance checks | Defaults, tested choices, and protocol requirements are distinguished; comparisons state their scope. |
| 6 | Consolidate validity and rewrite conclusion structure | Reorganization | Every main claim is paired with its evidence and limits; future work contains future tasks. |
| 7 | Decide whether stronger claims justify new studies | Research decision | Run only studies needed to support retained claims; otherwise narrow the claims. |

Steps 1–6 mainly improve the paper's explanation. They cannot create missing experimental support. This review changes neither the manuscript nor the experiments.

## What not to add merely to match the reference

- Additional contribution chapters: the reference develops several linked contributions; our methodology/implementation/evaluation split can remain.
- Human annotator agreement statistics when there is no human annotation task. The relevant question here is the reliability and meaning of the actual judge procedure.
- Training/test folds borrowed from a supervised classification experiment. Use development/evaluation separation appropriate to the actual steganography tests.
- More background or related-work pages just to reach a thesis-sized document. Those chapters should prepare the reader for our choices.
- More implementation history in the methodology. Keep the final design clear and place experimental configuration differences where they explain the findings.
- A claim that the university requires any particular missing heading. That would need an actual institutional requirement, which this comparison does not establish.

## Source index

| ID | Source and location | Used for |
| --- | --- | --- |
| R1 | Reference §§3.3–3.4.1, printed pp. 30–32; §§3.8–3.10, pp. 54–55 | Review method, question decomposition, synthesis, and review validity. |
| R2 | Reference §§4.2–4.4, pp. 58–65 | Purpose, representation choices, procedure, and testable questions. |
| R3 | Reference §4.5, pp. 66–72, 80, 84–85 | Construct definition, data, annotation, parameter choices, baselines, and explicit answers. |
| R4 | Reference §§4.6–4.7, pp. 85–87 | Limitations, data validity, parameter tuning, and task validity. |
| R5 | Reference §5.4, pp. 93–102; §§5.5.1, 5.5.5, 5.6, pp. 105, 112–114 | Input/output decomposition, pseudocode, examples, preparation, comparison criteria, and threats. |
| R6 | Reference §§6.2–6.5, pp. 118–125 and 138 | Formal definitions, worked representations, algorithm steps, experiment questions, and downstream validation need. |
| R7 | Reference §§7.1–7.4, pp. 139–144 | Case-study motivation, dataset description, test protocols, and alternative methods. |
| R8 | Reference §§8.1–8.2, pp. 155–159 | Contribution-centered conclusion and distinct future work. |
| M1 | [Arabic introduction](stego_paper_ar/sections/introduction.tex) | Research framing, questions, contributions, topic-list summary, and outdated chapter map. |
| M2 | [Arabic methodology](stego_paper_ar/sections/methodology.tex), §§5.1–5.9 | Components, sources, timing, bit choices, verification, compression, multiple frames, and receiver conditions. |
| M3 | [Arabic implementation](stego_paper_ar/sections/implementation.tex), §§6.1–6.3 | Actual stage exposition, shared codec, and model settings. |
| M4 | [Arabic evaluation](stego_paper_ar/sections/evaluation.tex) | Metrics, judge sampling/tasks, historical comparisons, extraction studies, evidence table, and limits. |
| M5 | [Archive experiments](stego_paper_ar/sections/fresh_archive.tex), §7.7 | Independent acquisition, policies, sample composition, cost, and quality tradeoff. |
| M6 | [Arabic conclusion](stego_paper_ar/sections/conclusion.tex) | Contribution summary and completed results appearing under future work. |
| M7 | [Related work](stego_paper_ar/sections/related_work.tex), [terminology](stego_paper_ar/sections/terminology.tex), and [judge appendix](stego_paper_ar/sections/judge_supplement.tex) | Existing coverage that should be reused rather than classified as absent. |

The source comparison is based on the manuscript, not a fresh audit of backend behavior or raw experiment records. Proposed numerical examples, parameter rationales, and additional studies must be checked against those records before being added to the paper. The abstracts retain their separate authorization requirement.
