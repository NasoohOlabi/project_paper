#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BUILD_DIR="$SCRIPT_DIR/build"
mkdir -p "$BUILD_DIR"

export BIBINPUTS="$SCRIPT_DIR/../common/references${BIBINPUTS:+:$BIBINPUTS}"
export BSTINPUTS="$SCRIPT_DIR/../common${BSTINPUTS:+:$BSTINPUTS}"

latexmk -cd -xelatex -interaction=nonstopmode -file-line-error \
  "-outdir=$BUILD_DIR" "$SCRIPT_DIR/main.tex"
