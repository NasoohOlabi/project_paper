$ErrorActionPreference = 'Stop'

$PaperRoot = Split-Path -Parent $PSScriptRoot
$SourceFile = Join-Path $PaperRoot 'stego_paper\main.tex'
$OutputDir = Join-Path $PaperRoot 'stego_paper\build'

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$env:BIBINPUTS = "$(Join-Path $PaperRoot 'common\references');$env:BIBINPUTS"
& latexmk -cd -xelatex -interaction=nonstopmode -file-line-error `
  "-outdir=$OutputDir" $SourceFile
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
