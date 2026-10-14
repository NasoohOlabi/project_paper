"""Build the English note figures and both language versions of the paper."""

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "bilingual-notes"
FIGURES = (
    "source_text_collection_en",
    "source_to_topics_en",
    "two_layer_embedding_en",
    "temporal_sync_method",
    "verify_decode_method",
)


def run_build(source: Path, output: Path, log: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(
        LC_ALL="C",
        LANG="C",
        BIBINPUTS=str(ROOT / "common" / "references") + ";",
        BSTINPUTS=str(ROOT / "common") + ";",
    )
    with log.open("w", encoding="utf-8") as stream:
        result = subprocess.run(
            [
                "latexmk", "-cd", "-xelatex", "-interaction=nonstopmode",
                "-file-line-error", f"-outdir={output}", str(source),
            ],
            env=env, stdout=stream, stderr=subprocess.STDOUT, check=False,
        )
    if result.returncode:
        raise RuntimeError(f"Build failed: {source}; see {log}")


def build_paper(language: str) -> dict:
    folder, basename = (
        ("stego_paper", "main") if language == "en"
        else ("stego_paper_ar", "main_ar")
    )
    source = ROOT / folder / f"{basename}.tex"
    output = ROOT / folder / "build"
    run_build(source, output, OUTPUT / f"paper-{language}.log")
    log = (output / f"{basename}.log").read_text(encoding="utf-8", errors="replace")
    unresolved = [line for line in log.splitlines() if re.search(
        r"(?:Reference|Citation).*undefined|undefined (?:references|citations)", line
    )]
    if unresolved:
        raise RuntimeError(f"Unresolved references in {language}: {unresolved}")
    return {"language": language, "pdf": str(output / f"{basename}.pdf"),
            "build": "passed", "unresolved_references": unresolved}


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    method_paths = [ROOT / folder / "sections" / "methodology.tex"
                    for folder in ("stego_paper", "stego_paper_ar")]
    methods = [path.read_text(encoding="utf-8") for path in method_paths]
    label_sets = [set(re.findall(r"\\label\{([^}]+)\}", text)) for text in methods]
    if label_sets[0] != label_sets[1]:
        raise RuntimeError(f"Methodology labels differ: {label_sets[0] ^ label_sets[1]}")
    for path, text in zip(method_paths, methods):
        if "\\subsubsection" in text or "fig:research-pipeline" in text:
            raise RuntimeError(f"Old methodology structure remains in {path}")
    for name in FIGURES:
        source = ROOT / "stego_paper" / "figures" / f"{name}.tex"
        run_build(source, OUTPUT / name, OUTPUT / f"{name}.log")
        shutil.copy2(OUTPUT / name / f"{name}.pdf", source.with_suffix(".pdf"))
    with ThreadPoolExecutor(max_workers=2) as executor:
        papers = list(executor.map(build_paper, ("en", "ar")))
    report = {"methodology_labels": "match", "figures": list(FIGURES), "papers": papers}
    (OUTPUT / "build-summary.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
