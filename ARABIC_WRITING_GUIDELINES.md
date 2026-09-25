# Arabic Writing Guidelines

Use this guide when drafting or revising the Arabic version of the paper. It records the author's confirmed preferences; it is not a substitute for checking the technical meaning against the English source.

## Style

- Write clear, natural academic Arabic. Prefer idiomatic phrasing over word-for-word translation, especially for computer science terminology.
- State the technical idea directly. Avoid vague metaphors, strained expressions, and wording that sounds like translated English.
- Keep sentences easy to follow. Name the actor when it matters: use **المُرسِل** and **المُستقبِل** for sender and receiver.
- Use the paper's actual concepts. For example, say **موضوع التعليق** for the comment's topic; do not replace it with an angle, tangent, or generic prompt.
- When a phrase is unclear or can be translated in more than one way, give the author several complete alternatives and explain briefly what each means. Do not silently settle on a paraphrase.
- Preserve the paper's claims and scope. Do not add defensive disclaimers that do not help explain the method or findings.
- Add Arabic diacritics selectively when they resolve ambiguity or improve reading, as in **مَوْضِعِ الرَّدِّ** and **مَوْضُوعِ التَّعْلِيقِ**.

## Preferred terminology

| Concept | Preferred Arabic |
| --- | --- |
| context-aware | مدرك للسياق |
| fine-tuning (AI) | الضبط الدقيق، مع شرح أنه مواصلة تدريب نموذج مدرّب مسبقًا على بيانات المهمة أو المجال عند الحاجة |
| zero-shot | الإخفاء اللغوي التوليدي دون تدريب مخصص; explain the contrast with fine-tuning rather than leaving the English label unexplained |
| embedding (information) | تضمين |
| compatibility / fit | توافق; for the evaluation metric selected by the author, **ملاءمة السياق** |
| sender / receiver | المُرسِل / المُستقبِل |
| reply location | مَوْضِع الرَّدّ |
| comment topic | مَوْضُوع التَّعْلِيق |
| entropy | الإنتروبيا |

Use terminology consistently within the paper. Prefer established Arabic computer science terms, and verify a proposed term against its technical meaning before adopting it.

## Wording approved by the author

- **منهجية للإخفاء اللغوي المدرك للسياق**
- **محادثات** rather than **النقاشات المتسلسلة**
- **وتحمل اختياراتُ مَوْضِعِ الرَّدِّ وَمَوْضُوعِ التَّعْلِيقِ بتاتَ الرسالة، ثم يصوغ المُرسِل تعليقًا عاديًا.**
- **نسخة المحادثة المُقدَّمة إلى المُستقبِل**
- **معاملات التشغيل المشتركة**
- **ملاءمة السياق** for the selected evaluation label
- **الطرائق المبكّرة** with shadda on ك

## Current sentence under review

The current draft says: **واللغة الطبيعية قليلة الإنتروبيا، لذا قد تمنح حتى الشذوذات الإحصائية الصغيرة كاشفًا ما يمسك به.** The English source says: “Natural language has little spare room, so even small statistical quirks can give a detector something to grab.” The second half is figurative in English and reads awkwardly as a literal Arabic translation.

Possible rewrites, pending the author's choice:

1. **ولأن اللغة الطبيعية منخفضة الإنتروبية، قد تكشف الانحرافات الإحصائية الطفيفة النصَّ المولَّد.** This uses the selected low-entropy framing and states the consequence directly.
2. **وتتميّز اللغة الطبيعية بانخفاض الإنتروبيا، لذلك قد تجعلها الانحرافات الإحصائية الطفيفة أسهلَ كشفًا.** This keeps the information-theoretic framing, if low entropy is the intended technical claim.
3. **وفي اللغة الطبيعية، قد تكفي انحرافات إحصائية طفيفة لكشف النص المولَّد.** This is shorter and direct, while omitting the causal explanation about spare room.

Selected: option 1, revised to use منخفضة الإنتروبية.

- Do not translate \\EN{Perplexity} as **حيرة**. In prose, describe low perplexity as fluency or naturalness (for example, **طليق** or **طبيعي**) when that matches the claim; retain the English metric name where a technical label is needed.

- Do not translate a social-media chat or thread as **السلسلة**. Use **المحادثة** for the exchange, or **سلسلة التعليقات** when the platform structure itself is meant.
