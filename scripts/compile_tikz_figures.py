"""Compile TikZ standalones to PDF/PNG and copy into both paper trees."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIKZ_DIR = ROOT / "stego_paper" / "figures" / "tikz"
OUT_DIRS = [
    ROOT / "stego_paper" / "figures",
    ROOT / "stego_paper_ar" / "figures",
]

FIGURES = [
    "end_to_end_scenario",
    "research_pipeline_deterministic",
    "temporal_sync_window",
    "two_layer_embedding",
    "verify_and_decode_flow",
    "implementation_pipelines",
    "token_vs_intent_embedding",
    "payload_compression_dp",
]


def run(cmd: list[str], cwd: Path) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> int:
    TIKZ_DIR.mkdir(parents=True, exist_ok=True)
    for name in FIGURES:
        tex = TIKZ_DIR / f"{name}.tex"
        if not tex.exists():
            raise SystemExit(f"missing {tex}")
        run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                tex.name,
            ],
            TIKZ_DIR,
        )
        pdf = TIKZ_DIR / f"{name}.pdf"
        run(["pdftocairo", "-png", "-r", "220", "-singlefile", str(pdf), str(TIKZ_DIR / name)], TIKZ_DIR)
        png = TIKZ_DIR / f"{name}.png"
        for out in OUT_DIRS:
            out.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pdf, out / f"{name}.pdf")
            shutil.copy2(png, out / f"{name}.png")
            print(f"wrote {out / name}.pdf")
        for leftover in (f"{name}.aux", f"{name}.log"):
            path = TIKZ_DIR / leftover
            if path.exists():
                path.unlink()
    return 0


if __name__ == "__main__":
    sys.exit(main())
