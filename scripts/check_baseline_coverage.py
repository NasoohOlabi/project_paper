"""Check that both papers retain the reviewed baseline-comparison topics.

This checks coverage anchors, not the truth of the surrounding scientific claims.
Evidence and interpretation are recorded in BASELINE_COMPARISON_COVERAGE.md.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANCHORS = {
    "evaluation.tex": (
        "sec:baseline-choice",
        "par:baseline-model-access",
        "par:baseline-model-scale",
        "par:baseline-capacity",
        "par:baseline-retries",
        "par:baseline-receiver-inputs",
        "par:baseline-domain-vocabulary",
        "fig:zlg-prompt-standout",
    ),
    "conclusion.tex": ("par:baseline-interpretation", "par:cross-post-extension"),
}
errors = []
for language in ("stego_paper", "stego_paper_ar"):
    for filename, anchors in ANCHORS.items():
        path = ROOT / language / "sections" / filename
        text = path.read_text(encoding="utf-8")
        for anchor in anchors:
            count = text.count(f"\\label{{{anchor}}}")
            if count != 1:
                errors.append(f"{path.relative_to(ROOT)}: {anchor}: expected once, found {count}")
for error in errors:
    print(error)
print(f"Baseline coverage anchors: {len(errors)} error(s). Scientific review is still required.")
raise SystemExit(bool(errors))
