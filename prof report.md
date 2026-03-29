### Method Metrics Summary

| Category | Metric | Baseline / Context | Mean Value | Range (Min / Max) |
| :--- | :--- | :--- | :--- | :--- |
| **Perplexity** | PPL (GPT-2) | 571 Stego Strings | **≈ 92.3** | 14.2 – 3580.0 |
| **Divergence** | KL Divergence | Matched Primary Post | **≈ 6.88** | — |
| | KL Divergence | Global Comment Corpus | **≈ 4.14** | — |
| | JSD | Matched Primary Post | **≈ 0.54** | — |
| | JSD | Global Comment Corpus | **≈ 0.54** | — |

---

### Explanation of Calculations

* **Perplexity (PPL):**
    Perplexity is a standard NLP measure used to evaluate the quality of a language model. It is calculated as the average per-word log-probability: $2^{-\frac{1}{n} \sum_{i=1}^{n} \log_2 P(x_i|x_{<i})}$. Roughly, it represents the number of equally likely choices the model believes it has for the next token. A **lower PPL** indicates the text is more natural and predictable, while a **higher PPL** indicates surprising or awkward continuations. The extreme max of ~3580 in your data likely stems from a few "pathological" samples that are highly unnatural to GPT-2.

* **Kullback–Leibler (KL) Divergence:**
    KL divergence measures the statistical difference between two probability distributions, such as a cover carrier ($P_C$) and a stego carrier ($P_S$). The calculation $\sum_w p_{\text{stego}}(w) \log \frac{p_{\text{stego}}(w)}{p_{\text{baseline}}(w)}$ quantifies the "information loss" or divergence between your stego word unigrams and the baseline. A **lower KL value** indicates higher statistical imperceptibility. Your finding that KL is lower for the global corpus than for matched primary posts suggests the stego text statistically drifts toward **generic wording** rather than maintaining thread-specific vocabulary.

* **Jensen–Shannon Divergence (JSD):**
    JSD is a symmetric version of KL divergence that provides a normalized measure of similarity between distributions. It is defined as: $DJS(P_C || P_S) = \frac{1}{2} D_{KL}(P_C || \frac{P_C + P_S}{2}) + \frac{1}{2} D_{KL}(P_S || \frac{P_C + P_S}{2})$. In steganography, JSD is often used to establish an upper bound on how easily an adversary can distinguish stego text from the true language distribution.

* **Laplace Smoothing:**
    The use of `smoothing_alpha = 1e-6` is a technique to handle words that appear in the stego text but not in the baseline distribution (and vice versa) to avoid mathematical errors (like division by zero) during KL and JSD calculations.

### Comparison of Method Metrics to Source Values

The following table compares your experimental results (Mean Values) to representative data points extracted from the provided sources.

| Metric | Your Method (Mean) | Source Reference Value | Source & Context |
| :--- | :--- | :--- | :--- |
| **Perplexity (PPL)** | **92.3** | **134.11** (Human Mean) | **VAE-Stega**: IMDB training corpus baseline. |
| | | **20.92** (RNN-Stega) | **VAE-Stega**: RNN baseline at 1.0 bpw. |
| | | **165.76** (LLM-Stega) | **LLM-Stega**: Black-box generation using GPT-4. |
| | | **42.23** (Discop) | **Discop**: Stego text quality using GPT-2. |
| **KL Divergence** | **4.14 – 6.88** | **19.51** (RNN-Stega) | **VAE-Stega**: RNN baseline on IMDB. |
| | | **0.045** (Meteor) | **Meteor**: High-entropy English text sampling. |
| | | **0.00** (Discop) | **Discop**: Perfectly secure "distribution copies". |
| **JSD** | **0.54** | **14.48** (RNN-Stega) | **VAE-Stega**: RNN baseline on IMDB. |
| | | **0.18** (Zero-shot) | **Zero-shot**: LLM in-context learning ($17.9 \times 10^{-2}$). |

---

### Analysis of the Comparison

* **Perplexity (PPL) Alignment**: Your mean PPL of **92.3** is significantly lower (more natural) than human text averages reported in the **VAE-Stega** source (**134.11**). It sits between the highly optimized but statistically detectable RNN models (**~20-30 PPL**) and newer black-box LLM methods like **LLM-Stega** (**165.76 PPL**). This suggests your method produces text that is predictable to GPT-2 while remaining within a "realistic" range for human communication.

* **Divergence Gaps (KLD/JSD)**:
  * Your KL Divergence (**4.14 – 6.88**) is considerably lower than the **RNN-Stega** baseline (**19.51**), which indicate a much higher level of statistical imperceptibility than older recurrent models.
  * However, your values are higher than "provably secure" methods like **Meteor** (**0.045**) or **Discop** (**0.00**). This is likely because your calculation is based on **word unigrams**, whereas methods like Discop maintain the exact model distribution at the token level to achieve zero divergence.
  * Your JSD of **0.54** is higher than the **Zero-shot** method (**0.18**), suggesting that your stego text has a more distinct statistical signature compared to models using in-context learning with LLMs.

* **Statistical Drift**: Your observation that KL Divergence is lower to the **Global Corpus** (**4.14**) than to the **Matched Post** (**6.88**) mirrors the "Psic Effect" described in the sources. This effect demonstrates that as stego text quality is optimized, it often drifts away from specific contextual distributions (the matched post) and toward more generic, background linguistic patterns (the global corpus).
