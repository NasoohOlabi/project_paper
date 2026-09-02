# How each reported metric is calculated

Type: research
Status: resolved
Blocked by:

## Question

For every metric the paper might report, what is the exact formula, the code path, the direction (higher/lower better), and the denominator?

Must include: recoverable capacity / bits per comment; generation success and exact recovery (intention-to-treat vs successful-output-only); GPT-2 perplexity; KL/JSD; MATTR and any rescaling; word count; BLEU/ROUGE/BERTScore; LLM-judge criteria (standout, weakest-text, suspicion AUROC, thread attribution, register-fit); synthetic detection if present; passive-detector ROC-AUC if present. Note metrics the paper currently claims but the runners no longer compute, and metrics the runners compute that the paper omits.

## Answer

Two pipelines, two quantities. The current paper table is successful-output-only and then post-clustered over 100 posts from the historical 304-pair builder. Our "bits/comment" is lossless channel width, not blind recovered payload. ZLG's 16.00 is a matched 2-byte payload. The live publication runner counts exact recovered bits of an 8-hex-char secret, dropped MATTR/BLEU/ROUGE/BERTScore, and computes KL/JSD, Codex J1–J5, M2 detection, and grouped ROC-AUC, which the paper currently omits.

Full formulas, code paths, directions, and denominators: [How each reported metric is calculated](../research/02-how-metrics-are-calculated.md).
