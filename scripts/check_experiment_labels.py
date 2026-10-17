"""Flag calendar-based and author-rejected experiment labels in manuscript prose."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(
    r"\b(?:19|20)\d{2}[-_]\d{2}[-_]\d{2}\b|\b20\d{6}(?:T\d+Z)?\b|"
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b|"
    r"\b(?:يناير|فبراير|مارس|أبريل|مايو|يونيو|يوليو|أغسطس|سبتمبر|أكتوبر|نوفمبر|ديسمبر)\b|"
    r"الإعداد الأولي"
)
failures = []
for folder in ("stego_paper/sections", "stego_paper_ar/sections", "common/tikz"):
    for path in sorted((ROOT / folder).glob("*.tex")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            # Comments and reference keys are not visible version labels.
            prose = re.split(r"(?<!\\)%", line, maxsplit=1)[0]
            prose = re.sub(r"\\(?:cite\w*|label|ref|input|includegraphics)(?:\[[^]]*\])?\{[^}]*\}", "", prose)
            if PATTERN.search(prose):
                failures.append(f"{path.relative_to(ROOT)}:{number}: {line.strip()}")
for failure in failures:
    print(failure)
print(f"Experiment-label check: {len(failures)} potential violation(s).")
raise SystemExit(bool(failures))
