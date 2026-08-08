# Arabic scientific terminology audit — 2026-08-08

This is a terminology review of the Arabic manuscript. It uses the paper's own glossary, the project writing rules, and Arabic steganography literature terminology. The protected human-authored Arabic abstract was not edited.

## Recommended canonical terms

| English concept | Recommended Arabic | Review decision |
|---|---|---|
| steganography | إخفاء المعلومات | Preferred over transliteration; established in Arabic technical usage. |
| linguistic steganography | الإخفاء اللغوي للمعلومات | Precise and consistent with the paper title/domain. |
| information hiding | إخفاء المعلومات | Use when discussing the broader field; do not confuse it with encryption. |
| embedding | التضمين | Use for the act/process of placing the payload in a carrier or selection channel. |
| extraction/recovery | الاستخراج / الاسترجاع | Use `الاستخراج` for extracting a carrier/message and `الاسترجاع` for recovering decoded payload; define both where they first diverge. |
| decoding | فك الترميز | Correct for mapping observed choices back to bits/indexes. |
| imperceptibility | اللامحسوسية | Preferred project term; distinguish perceptual, statistical, and cognitive imperceptibility. |
| black-box | الصندوق الأسود | Standard technical metaphor; keep the English abbreviation only when needed. |
| white-box | الصندوق الأبيض | Standard counterpart to black-box access. |
| semantic | دلالي | Correct adjective for meaning-level selection. |
| contextual / context-aware | مدرك للسياق | Required by `project_paper/AGENTS.md`; do not replace with an improvised synonym. |
| selection channel | قناة الانتقاء | More precise than “قناة الاختيار” for a channel whose states are selected from a finite set. Define it once. |
| reply target / parent comment | هدف الرد / التعليق الأب | Use “التعليق الأب” for the graph/tree relation and “هدف الرد” for the selected carrier location. |
| angle | زاوية | Retain as the paper’s named data object; define it as a semantic framing or line of inquiry, not a geometric angle. |
| tangent | مماس موضوعي / اتجاه موضوعي | Use “مماس موضوعي” only if the data object is explicitly called tangent; otherwise “اتجاه موضوعي” is clearer Arabic prose. Do not alternate without definition. |
| payload | حمولة | Standard in communication/security contexts; clarify that it is the secret bitstream. |
| capacity | سعة | Use “السعة القابلة للاسترجاع” for verified capacity, not merely physical index width. |
| bits per word/comment | بتات لكل كلمة/تعليق | Keep the unit explicit; do not translate `bpw` as a generic “معدل”. |
| shortlist | قائمة مختصرة للمرشحين | More precise than a literal “قائمة قصيرة”. |
| semantic similarity | تشابه دلالي | Standard NLP term. |
| deterministic | حتمي | Reserve for stages whose inputs, model/backend, and configuration are fixed; do not call the whole decoder حتمي. |
| audit-assisted | مدعوم بالتدقيق | Correct for recovery using sender metadata or audit artifacts. |
| temporal window | نافذة زمنية | Use with “حد زمني” for the cutoff operation. |
| hallucination | هلوسة | Established AI term; define it as unsupported or context-inconsistent generation. |
| steganalysis | تحليل الإخفاء / كشف الإخفاء | Use “تحليل الإخفاء” for the research discipline and “كشف الإخفاء” for a detection task. |

## Consistency issues to resolve in a future Arabic revision

1. The manuscript alternates between “الزاوية” and descriptions of “tangent.” Keep “زاوية” as the named object and define its fields as category, source quote, and اتجاه/مماس موضوعي.
2. “الاسترجاع” and “فك الترميز” are related but not interchangeable: recovery is the outcome; decoding is the mapping operation.
3. “حتمي” must be limited to deterministic preprocessing and explicitly fixed decoder configurations. The semantic shortlist/discriminator stage is configurable and is not inherently deterministic.
4. “السعة القابلة للاسترجاع” must exclude unused states when a choice count is not a power of two. This is a scientific accounting rule, not a stylistic preference.
5. “المقارنة المزدوجة” is understandable but “مقارنة مقترنة” is more conventional in statistical writing when each observation is paired across methods. Define the chosen term once and use it consistently.
6. “المعيار” can imply a gold-standard benchmark. For the historical artifact, use “مقارنة إعداد مدققة” or “أثر تدقيقي تاريخي” and explicitly state that it is not a current decision-grade result.

## Protected text

`stego_paper_ar/sections/abstract.tex` contains an explicit human-authored-text protection notice requiring three separate confirmations before any edit. No change was made there.
