# Arabic-to-English revision coverage

The approved Arabic revisions are the source for this port. English wording follows the same method rather than literal Arabic phrasing. Both abstracts are unchanged.

| Author note or subsequent choice | Arabic artifact | English artifact | Result |
| --- | --- | --- | --- |
| Add terminology and a table of terms | `stego_paper_ar/sections/terminology.tex` | `stego_paper/sections/terminology.tex` | Both include the same twelve core concepts and definitions. |
| Use black-box terminology and the approved opening | Methodology opening | Methodology opening | Arabic uses the approved sentence; English uses black-box linguistic steganography without repeating the internal-probability explanation. |
| Explain system requirements, parameter groups, and workflow first | Methodology 5.1 | Methodology 5.1 | Helper and writer roles, six parameter groups, and six processing stages match. |
| Define the helper's setting once | Methodology 5.1 | Methodology 5.1 | A displayed `temperature = 0` equation introduces the fixed helper configuration; reproducibility remains conditional on identical inputs and services. |
| Present the final method instead of development history | Methodology and figure captions | Methodology and figure captions | Month-specific implementation narratives removed; experimental limits retained. |
| Explain OPPRESSION before our adaptation and cite it | Methodology 5.2 and related work | Methodology 5.2 and related work | Shared documents, document pointers, tree nodes, source changes, and persistent/ephemeral modes are explained and cited. |
| Explain search phrases and general retrieval | Methodology 5.2 | Methodology 5.2 | Queries derive from title/body; twelve queries are not twelve prompts; top ten results replace API pagination details. Local PDF restrictions and provider fallbacks are omitted. |
| Explain source texts and their mapping to topics | Methodology 5.2 | Methodology 5.2 | Post, comments, and web texts form D; per-text extraction and shared ordering yield A under the same equation. |
| Explain the topic-list name and record fields | Methodology 5.2 and terminology | Methodology 5.2 and terminology | Quote, description, category, source reference, and index are distinguished from the compression dictionary. |
| Replace the old search figure with the approved compact collection diagram | Figure 3, `source_text_collection_ar.png` | Figure 3, `source_text_collection_en.pdf` | Equivalent inputs and data flow; English is a reproducible vector figure. |
| Add the approved mapping diagram and concrete example | Figure 4, `source_to_topics_ar.png` | Figure 4, `source_to_topics_en.pdf` | Same repair-versus-replacement example and four record fields. |
| Rename the comments snapshot/dump everywhere | Arabic sections and Markdown guidance | English sections and shared guidance | Arabic uses the approved comments-copy term; English uses "copy of the post's comments". Timing is explained separately. |
| Explain why the comment copy is needed before its timing | Methodology 5.3 | Methodology 5.3 | New comments, processing time, cutoff, deadline, and edits/deletions are explained in matching order. |
| Use an ordered list rather than embedding sub-subsections | Methodology 5.4 | Methodology 5.4 | Reply-location and topic choices form a two-item list; internal section references point to 5.4. |
| Use the final binary-choice diagram | Figure 6, `two_layer_embedding_ar.png` | Figure 6, `two_layer_embedding_en.pdf` | 10 selects Comment 2; 01 selects Repair cost; both feed the writer with context. |
| Keep writing guidance and figure prompts current | `ARABIC_WRITING_GUIDELINES.md`, translation guidance, and Arabic figure briefs | `PAPER_WRITING_GUIDELINES.md`, native English figure sources | Rules and exact approved Arabic labels retained; the English diagrams are authored directly in LaTeX. |

## Scope and provenance

The discussion about domain similarity and compression was a question, not an approved paper edit. It is not added to either version as a new claim. The discussion of figure placement was also exploratory; no broad layout rewrite is included. The new explanatory diagrams stay close to their introductions.

`refs/task-checkpoints/bilingual-notes-before` records the complete workspace before the English port, including pre-existing edits. The bilingual commit includes the revised methodology, terminology, diagram assets, citation-bearing related-work passage, and guidance. Main-file terminology inputs and the evaluation terminology edits are staged separately from unrelated pre-existing edits in those files. Other research changes remain in the working tree.

## Rebuilding

The 16 October author-approved reconstruction-validation explanation is included in both evaluation chapters under `sec:reconstruction-validation`. It distinguishes development-only repeated processing from deployed sender/receiver behavior and from message-extraction experiments. The Arabic introduction now gives a brief pointer instead of the rejected blanket statement about untested reconstruction. Both abstracts remain unchanged.

Run `python scripts/build_bilingual_notes.py` from the repository root. It compiles the five vector figures, builds both papers, compares methodology label sets, and rejects unresolved references. Logs and the build summary are under `build/bilingual-notes/`. The figures are also checked visually in the built pages; successful compilation alone is not a layout check.

## Review

The author-approved second Arabic research question now asks about sender generation, receiver extraction, and causes of failure. Experimental run/runs is rendered throughout the Arabic chapters as تجربة/تجارب, or اختبار/اختبارات for a specific check, following the Arabic guide. This is an Arabic wording rule; English run and technical expressions such as نظام التشغيل remain valid. Neither abstract required a change.

Reviewed inline. The Git checkpoint preserves the earlier workspace. The change does not turn audit-assisted results into independent receiver results. English figures have different drawing geometry from the Arabic raster figures but the same inputs, output structures, examples, and selections.
