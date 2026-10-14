# Diagram prompts for the Arabic methodology

Read [ARABIC_WRITING_GUIDELINES.md](../ARABIC_WRITING_GUIDELINES.md) before writing or revising any Arabic figure prompt. Use the exact visible labels specified below. Technical symbols and binary values read left to right; the diagram reads right to left.

## Figure 3: collecting the source texts

Status: inserted in the Arabic paper using `figures/source_text_collection_ar.png`. This prompt records the intended design for future revisions.

Placement: Section 5.2, after the description of the source-text list and before its mapping equation. Section 5.3 explains how the parties prepare **نسخة من تعليقات المنشور**, including its time cutoff. Use that Arabic phrase whenever naming a comments snapshot or dump.

Caption: «جمع نص المنشور وتعليقاته والنصوص الناتجة عن البحث في قائمة مرتبة يستخدمها الطرفان لبناء موضوعات التعليق.»

Generation prompt:

> Create a compact academic diagram for an Arabic thesis. Use a white background, thin dark blue lines, black Arabic labels, and a right-to-left layout. Render exactly five labelled nodes. Place «عنوان المنشور ونصه» on the right. Its upper branch goes to «عبارات البحث», then to «نصوص من الويب», then to «قائمة النصوص» on the left. A separate direct arrow goes from «عنوان المنشور ونصه» to «قائمة النصوص». Below, place «تعليقات المنشور» as an independent input, with one arrow to «قائمة النصوص». Every arrow must have a visible arrowhead at its destination. Depict the output as a small stack of documents. Use a balanced two-row composition and large labels readable at 15 cm print width. Copy the five Arabic labels exactly. Show only these nodes and arrows; leave timing, ordering rules, models, and numerical settings to the caption and prose.

## Source texts mapped to comment topics

Status: inserted in the Arabic paper using `figures/source_to_topics_ar.png`.

Placement: Section 5.2, after «شكل موضوع التعليق والقائمة المرتبة».

Caption: «تحويل قائمة النصوص إلى قائمة مرتبة من موضوعات التعليق وفق إعداد مشترك. يوضح المثال اقتباسًا والفكرة المستمدة منه وفئتها ومصدرها.»

Generation prompt:

> Create a compact academic diagram for an Arabic thesis, with white background, thin dark blue outlines, restrained pale blue highlights, and large Arabic labels readable at 15 cm print width. Read the flow right to left. Begin with a single input list labelled «قائمة النصوص», showing rows «النص 0», «النص 1», and «…». Each row represents one text with its source reference. Draw an arrow to «استخراج موضوعات التعليق» and then to «جمع الموضوعات وترتيبها». The output is a list labelled «قائمة موضوعات التعليق», with indexed rows 0, 1, 2, … . The same extraction procedure is applied to each source text and can produce several topics; the mapping is not one topic per source. Above the extraction and ordering stages, place a small box «إعداد مشترك», with dashed arrows to both stages. Keep the source-collection branches out of this figure because Figure 3 already explains them. Below the output, enlarge one illustrative topic card connected to row 0. Use exactly these four field/value pairs: «اقتباس» — «تكلفة إصلاح الجهاز تقترب من سعر جهاز جديد.»; «موضوع التعليق» — «مقارنة إصلاح الجهاز باستبداله»; «فئة» — «مقارنة»; «مرجع المصدر» — «النص 0». Add the short note «مثال توضيحي» above this card. This is an invented teaching example, not a quotation attributed to a real source. The topic is inspired by the quotation and is not a copy of it. Render every Arabic label and example exactly as provided, with properly joined letters. Keep indices separate from Arabic text. Show only the main flow, the shared-setting box, and the one example card; leave record schemas and parameter details to the prose.

## Two lists carrying binary choices

Status: inserted in the Arabic paper using `figures/two_layer_embedding_ar.png`.

Placement: Section 5.4, replacing the previous two-layer figure.

Caption: «تختار المجموعة الأولى من البتات موضع الرد، وتختار المجموعة التالية موضوع التعليق. يكتب النموذج تعليقًا ملائمًا اعتمادًا على الاختيارين.»

Generation prompt:

> Create a compact academic diagram for an Arabic thesis on white, with thin dark blue outlines, restrained pale blue highlights, and large labels readable at 15 cm print width. Use a right-to-left composition, but preserve left-to-right binary digits. At the top show «بتات الحمولة» with two separate groups “10” and “01”. Label the groups «موضع الرد» and «موضوع التعليق» respectively. Connect the first group to a table labelled «قائمة مواضع الرد», whose four rows pair “00” with «المنشور», “01” with «التعليق 1», “10” with «التعليق 2», and “11” with «التعليق 3». Highlight only the row “10 / التعليق 2”. Connect the second group to «قائمة موضوعات التعليق», whose four rows pair “00” with «إصلاح الجهاز أم استبداله», “01” with «تكلفة الإصلاح», “10” with «عمر الجهاز», and “11” with «توفر قطع الغيار». Highlight only “01 / تكلفة الإصلاح”. These are illustrative topics. Connect the selected rows from both lists and a separate input «سياق المحادثة» to «نموذج الكتابة», then to «التعليق الحامل». Place the note «مثال توضيحي: بتان لكل قائمة» below the two tables. Copy all Arabic labels exactly, keep binary values in their own column, and show a clear arrowhead at every destination. Include only these lists, selections, context, writer, and output.
