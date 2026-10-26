#!/bin/sh
set -eu

if [ "$#" -lt 1 ]; then
  echo "usage: render path/to/sheet.tex|dir|glob [...]" >&2
  exit 1
fi

mkdir -p /work/.cache /work/template/fonts

found=0

for input in "$@"; do
  if [ -d "$input" ]; then
    set -- "$input"/*.tex
    for file in "$@"; do
      [ -e "$file" ] || continue
      found=1
      latexmk -interaction=nonstopmode -pdf -lualatex "$file"
    done
  else
    for file in $input; do
      [ -e "$file" ] || continue
      found=1
      latexmk -interaction=nonstopmode -pdf -lualatex "$file"
    done
  fi
done

if [ "$found" -eq 0 ]; then
  echo "no .tex files found" >&2
  exit 1
fi

