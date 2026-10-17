# Figure prompt: the evaluation roadmap

The figure tells the reader why the experiments belong together. A comment must first fit its conversation; carrying an entire message adds a recovery requirement; independent reception adds context reconstruction. The arrows connect research questions. They do not pool samples, imply a historical sequence, or claim that every experimental stage succeeded.

## Placement and delivery

Status: the author-generated English and Arabic images are inserted in both papers. Each appears in **Evaluation → Experimental setup along the evaluation path**, after its opening explanation and before the configuration table. The prompts below retain the design brief for future revisions.

- English asset: `stego_paper/figures/evaluation_roadmap_en.png`
- Arabic asset: `stego_paper_ar/figures/evaluation_roadmap_ar.png`
- Use the matching language prompt below. Generate the two versions separately, preserving the same geometry, colors, and meaning. A lossless PNG at least 3200 pixels wide is suitable. Keep generous margins; intended print width is about 15 cm.
- Caption, English: “Evaluation organized by the question each experiment answers. Comment quality, complete-message recovery, and independent context reconstruction require different evidence. Supporting checks help locate failures; samples and configurations remain experiment-specific.”
- Caption, Arabic: «تنظيم التقييم بحسب السؤال الذي تجيب عنه كل تجربة. تتطلب جودة التعليق واستخراج الرسالة كاملة وإعادة بناء السياق بصورة مستقلة أدلة مختلفة. وتساعد الاختبارات المساندة على تحديد أسباب الإخفاق، مع بقاء العينات والإعدادات خاصة بكل تجربة.»

## English generation prompt

Create a publication-quality academic roadmap diagram for a linguistic steganography paper. This is a conceptual research map, not a performance chart or software architecture diagram. White background; crisp dark navy text and outlines; restrained pale blue fills; one muted teal accent. Flat vector-like appearance, no gradients, shadows, decorative illustrations, logos, or photographic elements. Wide landscape canvas, roughly 1.8:1, at least 3200 pixels wide. It must remain readable at 15 cm print width. Use a clean sans-serif font with generous spacing. All visible text must be copied exactly from the labels below. Do not invent extra labels, numbers, percentages, model names, dates, or claims of improvement.

At the top, place the title: “From a fitting comment to a recovered message”.

Across the central area place three equally sized cards, reading LEFT TO RIGHT. Each card has a large question at its top, two compact experiment labels in its middle, and a small clearly separated footer describing what is being examined. Use thin arrows between the cards, with an arrowhead at the next card. These arrows express the next research question, not a data pipeline. Do not use green ticks, red crosses, upward-trending graphs, or visual indicators that suggest all tests passed.

LEFT CARD:
Question: “Does the comment fit?”
Middle labels on separate lines: “Baseline comparison” and “Prompt ablation”
Footer: “Comment quality”

CENTER CARD:
Question: “Can the whole message be recovered?”
Middle labels on separate lines: “Source excerpts” and “Independent payloads”
Footer: “Prepared context”

RIGHT CARD:
Question: “Can the receiver rebuild the context?”
Middle labels on separate lines: “Independent archive inputs” and “Sender-policy comparison”
Footer: “Reconstructed context”

Below the cards, draw one thin, visually subordinate support band. Its heading is “Supporting checks”. Inside it place three equally spaced short labels, separated by small dots or vertical rules: “List agreement”, “Capacity planning”, “Transport integrity”. This band supports interpreting the experiments, not a fourth stage. Do not draw new data-flow arrows or extra boxes from it.

At the bottom place the small note: “See the text for samples and settings.”

Ensure balanced card heights and enough space for question line breaks. Keep all text horizontal. Preserve the central distinction between prepared context and independently reconstructed context. The diagram should look calm, precise, and suitable for a thesis, with the questions more prominent than the experiment labels and the support band less prominent than the three cards.

## Arabic generation prompt

Create the Arabic companion of an academic evaluation-roadmap diagram for a linguistic steganography thesis. White background; thin dark navy outlines; black or dark navy Arabic text; restrained pale blue fills; one muted teal accent. Flat vector-like style, no gradients, shadows, decorative illustrations, logos, or photographic elements. Wide landscape canvas, roughly 1.8:1, at least 3200 pixels wide. Intended print width is about 15 cm, so use large, properly joined Arabic letters and generous spacing. Copy every visible Arabic label below exactly. Do not translate or paraphrase it. Do not add English translations, dates, model names, sample counts, percentages, or claims of improvement.

At the top, place the title: «من تعليق ملائم إلى رسالة مستخرجة».

Use three equally sized central cards, reading RIGHT TO LEFT. Each has a large question, two compact experiment labels, and a separate small footer. Put a thin arrow from the RIGHT card to the CENTER card and another from the CENTER card to the LEFT card. The arrowhead must touch the destination side. These arrows connect questions in the research argument, not experimental data or consecutive steps on one sample. No success ticks, failure crosses, upward-trending graphs, or other symbols suggesting that all tests passed.

RIGHT CARD:
Question: «هل يلائم التعليق سياقه؟»
Middle labels on separate lines: «مقارنة بالطريقة المرجعية» and «مقارنة تعليمات الكتابة»
Footer: «جودة التعليق»

CENTER CARD:
Question: «هل تُستخرج الرسالة كاملة؟»
Middle labels on separate lines: «مقتطفات المصادر» and «حمولات مستقلة»
Footer: «سياق مُعد مسبقًا»

LEFT CARD:
Question: «هل يعيد المُستقبِل بناء السياق؟»
Middle labels on separate lines: «مدخلات مستقلة من الأرشيف» and «مقارنة سياسات المُرسِل»
Footer: «سياق يعاد بناؤه»

Below the cards, draw one thin support band, visually less prominent than the cards. Heading: «اختبارات مساندة». Inside the band, reading right to left, place three equally spaced labels separated by small dots or vertical rules: «تطابق القوائم»، «تخطيط السعة»، «سلامة النقل». It is a supporting band, not a fourth research stage. Do not add data-flow arrows or extra boxes from it.

At the bottom place the small note: «العينات والإعدادات موضحة في النص».

Keep the two versions geometrically consistent by mirroring the order of the three cards. Balance question line breaks and card heights. Keep text horizontal, right aligned within its label area, with correct Arabic punctuation and joined letters. Questions should be more prominent than experiment names. The distinction between a prepared context and one rebuilt by the receiver must be visible at first glance.

## Checks when the image is returned

Inspect every label, especially Arabic letter joining and diacritics, arrow destinations, and readability at print width. Confirm that no numerical result, model identity, invented experiment, or success claim was added. Insert only the verified matching-language image, rebuild both papers, and check its placement and caption. Exact settings belong in the adjacent table, so the image stays readable and does not duplicate it.
