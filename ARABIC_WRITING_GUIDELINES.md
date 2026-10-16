# Arabic Writing Guidelines

Use this guide when drafting or revising the Arabic version of the paper. It records the author's confirmed preferences; it is not a substitute for checking the technical meaning against the English source.

Shared method and citation rules are also recorded in [PAPER_WRITING_GUIDELINES.md](PAPER_WRITING_GUIDELINES.md). Port substantive method changes to both languages.

For every author correction, follow **Scope and application of author feedback** in that shared guide. Arabic terminology and general style choices apply throughout the Arabic paper, including captions, appendices, and visible figure text; a sentence-specific rewrite remains local. Apply confirmed broad rules immediately and ask when their scope is genuinely ambiguous.

## Style

- **NEVER USE «نقاش» OR ITS DERIVATIVES IN THE ARABIC PAPER.** Choose **تعليقات** for comments or comment threads, **دردشة** for chat, and **تواصل** for communication or contact, according to context. For a social-media exchange, use **محادثة**.
- Write clear, natural academic Arabic. Prefer idiomatic phrasing over word-for-word translation, especially for computer science terminology.
- State the technical idea directly. Avoid vague metaphors, strained expressions, and wording that sounds like translated English.
- Keep sentences easy to follow. Name the actor when it matters: use **المُرسِل** and **المُستقبِل** for sender and receiver.
- Use the paper's actual concepts. For example, say **موضوع التعليق** for the comment's topic; do not replace it with an angle, tangent, or generic prompt.
- When a phrase is unclear or can be translated in more than one way, give the author several complete alternatives and explain briefly what each means. Do not silently settle on a paraphrase.
- Preserve the paper's claims and scope. Do not add defensive disclaimers that do not help explain the method or findings.
- Do not mention internal project codenames in the paper. Name the proposed method or the technical component instead.
- Do not begin a paragraph with **لكن**. Establish the point directly and explain any qualification in context.
- Explain success-rate counts in plain language: count all attempted samples, including failures; calculate quality and judge scores on accepted generations. Avoid **مقام** and **قصد المعالجة** as shorthand for these populations.
- Rewrite implementation and evaluation paragraphs from their technical meaning, following the same clear exposition as the approved methodology. Explain the purpose, then the procedure, then settings and results. Do not turn them into translated development logs.
- Add Arabic diacritics selectively when they resolve ambiguity or improve reading, as in **مَوْضِعِ الرَّدِّ** and **مَوْضُوعِ التَّعْلِيقِ**.

- Use **نسخة من تعليقات المنشور** consistently for a comments snapshot or dump in prose, headings, terminology tables, captions, and figure prompts. Timing is implicit; describe the cutoff separately when explaining synchronization. For snapshots of web documents, use **نسخة من الوثائق** or **نسخة من محتوى الوثيقة**, according to context.

## Methodology exposition

- Present the final approach in the present tense. Do not narrate development history, month-specific changes, previous defaults, or implementation milestones in the methodology. Put differences between evaluated configurations in the implementation or evaluation chapter when they affect the findings.
- Explain the problem and purpose before introducing its mechanism or parameters. Introduce changing comments before snapshotting and changing web documents before persistent and ephemeral sources.
- Open the methodology with system components, parameter groups, and an ordered overview of the workflow. Keep configuration distinct from the payload-dependent choices.
- Define the helper model once with the displayed equation `\mathrm{temperature}=0`. Thereafter use **النموذج المساعد الحتمي**. This name describes the target configuration; do not claim that the parameter alone guarantees reproducibility.
- Describe the general method before implementation choices. Omit API argument names, provider fallbacks caused by budget limits, local-model format restrictions, and batching details from the methodology.
- Cite OPPRESSION with `\cite{zillien2024oppression}` whenever naming it or attributing a mechanism to it in prose, tables, or captions. Keep headings free of citations and cite the opening sentence beneath them. Use the existing bibliography entry and the spelling **OPPRESSION**.
- Attribute only the source paper's actual mechanisms to OPPRESSION. Explain our simplified adaptation separately, and distinguish the source-document list, the comment-topic list, and the compression dictionary.
- Use **منشور** for a social-media post and **قائمة موضوعات التعليق** for the ordered tangent list. Explain its quote, topic, category, and source fields.
- In the two-choice embedding section, use one ordered list rather than sub-subsections. State each figure's scope explicitly in its introduction and caption.

## Arabic figures and image-generation prompts

Apply these rules to every future Arabic diagram prompt, figure label, and caption. Use the terminology table below as the source of wording choices.

- Specify every visible Arabic label verbatim in the generation prompt. Ask the image model to copy it exactly with joined Arabic letters, rather than translate the English instructions.
- Use short, natural labels in figures. **تعليقات المنشور** names the comment input; explain its time cutoff in the prose or caption. Use **نسخة من تعليقات المنشور** when the figure specifically describes the collected copy.
- Use **قائمة النصوص** in compact figures for the formally defined **قائمة النصوص المصدرية**. Use **نصوص من الويب** for collected web text; keep **وثائق المجال** when discussing the documents as sources in the prose.
- Give each figure one purpose. Separate source collection, mapping texts to topics, and selecting reply locations and topics. Put configuration counts and API details in the text when needed.
- For mapping, show extraction from each text followed by collection and ordering. One source may yield several topics. Keep the source-text list, comment-topic list, and compression dictionary distinct.
- Use one concrete illustrative topic record with **اقتباس**, **موضوع التعليق**, **فئة**, and **مرجع المصدر**. The quotation inspires the topic; it is not a required phrase in the generated comment. Label invented examples **مثال توضيحي**, and use a source-list reference rather than a fabricated citation.
- Draw comments as an independently collected input. Use arrows for the actual data flow and show arrowheads at every destination. Read the layout right to left, while keeping binary strings and indices left to right in separate cells.
- Before handing over a prompt, check every visible label against this guide, verify the example's meaning and binary selections, and remove placeholder text. After generation, inspect Arabic spelling, letter joining, arrow direction, and readability at the intended print size before inserting the image.

## Preferred terminology

| Concept | Preferred Arabic |
| --- | --- |
| context-aware | مدرك للسياق |
| linguistic steganography | الإخفاء اللغوي |
| black-box steganography | الإخفاء اللغوي وفق نهج الصندوق الأسود; retain the English equivalent in the terminology table rather than repeating it in running prose |
| social-media post | منشور |
| post title and body | عنوان المنشور ونصه |
| post comments, figure input | تعليقات المنشور |
| search queries | عبارات البحث; استعلامات البحث remains appropriate in technical prose |
| collected web texts, figure label | نصوص من الويب |
| source-text list | قائمة النصوص المصدرية; shorten to قائمة النصوص in compact figures |
| comment-topic list | قائمة موضوعات التعليق |
| comments snapshot / dump | نسخة من تعليقات المنشور; timing is implicit in the term and explained separately in the synchronization procedure |
| helper model | النموذج المساعد; use النموذج المساعد الحتمي when its fixed generation setting matters |
| writer model | نموذج الكتابة |
| shared configuration | إعداد مشترك |
| experimental run / runs | تجربة / تجارب؛ ويُستخدم اختبار / اختبارات عندما يكون المقصود فحصًا محددًا. لا تُستخدم «تشغيلات» أو «التشغيلات»، ولا «تشغيل» للدلالة على تجربة بحثية. تبقى «نظام التشغيل» و«زمن التشغيل» صحيحتين عند وصف نظام الحاسوب أو تنفيذ البرنامج، وكذلك «معاملات التشغيل المشتركة» في سياق الإعدادات. |
| application programming interface | يُستخدم API في النص، ويُعرَّف في فصل المصطلحات بأنه واجهة برمجة التطبيقات. عند وصف الاستدعاء البرمجي، قل «عبر API» بدل «عبر واجهته المتاحة». لا تستبدل به واجهة المستخدم حين يكون المقصود UI. |
| cache | يُكتب cache بالإنجليزية عند الحاجة إلى ذكره في التنفيذ؛ لا يُترجم إلى «مخازن مؤقتة». لا يُقدَّم بوصفه مكوّنًا لازمًا للمنهجية. |
| source reference | مرجع المصدر |
| prompt | يُكتب prompt بالإنجليزية كما هو، ولا يُترجم إلى «طلب» أو «موجّه» عند وصف مدخلات نموذج اللغة. |
| fine-tuning (AI) | يُكتب fine-tuning بالإنجليزية ولا يُترجم إلى «الضبط الدقيق». عند الحاجة، يُشرح بأنه مواصلة تدريب نموذج مدرّب مسبقًا على بيانات المهمة أو المجال. |
| zero-shot | الإخفاء اللغوي التوليدي دون تدريب مخصص; explain the contrast with fine-tuning rather than leaving the English label unexplained |
| embedding (information) | تضمين |
| compatibility / fit | توافق; for the evaluation metric selected by the author, **ملاءمة السياق** |
| sender / receiver | المُرسِل / المُستقبِل |
| Extracting a hidden message | استخراج الرسالة or فك التضمين, according to the operation |
| reply location | مَوْضِع الرَّدّ |
| comment topic | مَوْضُوع التَّعْلِيق |
| entropy | الإنتروبيا |
| imperceptibility | خفاء الرسالة المضمَّنة |

Use terminology consistently within the paper. Prefer established Arabic computer science terms, and verify a proposed term against its technical meaning before adopting it.

- Use Arabic guillemets **«...»** for quotations in Arabic prose, including quoted English strings; place English text inside the guillemets in `\EN{...}`, as in **«\EN{any}»**.

- Never use **اللامحسوسية** for *imperceptibility*. Use **خفاء الرسالة المضمَّنة** instead.

## Wording approved by the author

- **نقترح طريقة للإخفاء اللغوي وفق نهج الصندوق الأسود داخل محادثة عامة.**

- **منهجية للإخفاء اللغوي المدرك للسياق**
- **محادثات** rather than **النقاشات المتسلسلة**
- **وتحمل اختياراتُ مَوْضِعِ الرَّدِّ وَمَوْضُوعِ التَّعْلِيقِ بتاتَ الرسالة، ثم يصوغ المُرسِل تعليقًا عاديًا.**
- **نسخة من تعليقات المنشور** for the comments snapshot or dump; use **نسخة من تعليقات المنشور تُقدَّم إلى المُستقبِل** when describing supplied input
- **معاملات التشغيل المشتركة**
- **ملاءمة السياق** for the selected evaluation label
- **الطرائق المبكّرة** with shadda on ك
- Describe the two actors as **المُرسِل** and **المُستقبِل**. Avoid **استرجاع** and its derivatives throughout the Arabic paper. Describe the operation precisely as **استخراج الرسالة** or **فك التضمين** when appropriate; use the sender and receiver as the grammatical subjects when explaining what each party does. Do not imply successful recovery of a payload unless the receiver independently obtains it from the public conversation.
- Use **محادثة** or **محادثات** for a social-media exchange. Avoid literal translations such as **نقاش متسلسل** and **نقاشات متسلسلة**.

## Current sentence under review

The current draft says: **واللغة الطبيعية قليلة الإنتروبيا، لذا قد تمنح حتى الشذوذات الإحصائية الصغيرة كاشفًا ما يمسك به.** The English source says: “Natural language has little spare room, so even small statistical quirks can give a detector something to grab.” The second half is figurative in English and reads awkwardly as a literal Arabic translation.

Possible rewrites, pending the author's choice:

1. **ولأن اللغة الطبيعية منخفضة الإنتروبية، قد تكشف الانحرافات الإحصائية الطفيفة النصَّ المولَّد.** This uses the selected low-entropy framing and states the consequence directly.
2. **وتتميّز اللغة الطبيعية بانخفاض الإنتروبيا، لذلك قد تجعلها الانحرافات الإحصائية الطفيفة أسهلَ كشفًا.** This keeps the information-theoretic framing, if low entropy is the intended technical claim.
3. **وفي اللغة الطبيعية، قد تكفي انحرافات إحصائية طفيفة لكشف النص المولَّد.** This is shorter and direct, while omitting the causal explanation about spare room.

Selected: option 1, revised to use منخفضة الإنتروبية.

- Do not translate \\EN{Perplexity} as **حيرة**. In prose, describe low perplexity as fluency or naturalness (for example, **طليق** or **طبيعي**) when that matches the claim; retain the English metric name where a technical label is needed.

- Do not translate a social-media chat or thread as **السلسلة**. Use **المحادثة** for the exchange, or **سلسلة التعليقات** when the platform structure itself is meant.
