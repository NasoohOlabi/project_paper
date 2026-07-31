#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"
latexmk -xelatex -interaction=nonstopmode -file-line-error main_ar.tex
