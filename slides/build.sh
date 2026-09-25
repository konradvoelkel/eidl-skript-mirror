#!/bin/sh
# Baut ein Deck (oder alle) und meldet Seitenzahl und zu volle Rahmen.
set -e
for f in "${@:-*VL*.tex}"; do
  latexmk -lualatex -interaction=nonstopmode -halt-on-error "$f" > "/tmp/claude-1000/$(basename "$f" .tex).log" 2>&1 \
    || { echo "FEHLER: $f"; grep -E '^!' "/tmp/claude-1000/$(basename "$f" .tex).log" | head -3; continue; }
  pdf="${f%.tex}.pdf"
  pages=$(pdfinfo "$pdf" | awk '/^Pages/{print $2}')
  vbox=$(grep -c 'Overfull \\vbox' "/tmp/claude-1000/$(basename "$f" .tex).log" || true)
  echo "ok  $(basename "$f" .tex): $pages Seiten, $vbox zu volle Rahmen"
done
