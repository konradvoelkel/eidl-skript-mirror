#!/bin/sh
# Baut ein Deck (oder alle) und meldet Seitenzahl und zu volle Rahmen.
set -e

# Logverzeichnis unter TMPDIR. Hier stand bis zum 2026-09-30 ein fester Pfad in das
# Scratchpad einer Coding-Sitzung (/tmp/claude-1000). Den gibt es auf keiner anderen
# Maschine, und dann scheitert jede Umleitung: Das Skript meldet fuer jedes Deck FEHLER,
# baut nichts und endet trotzdem mit 0.
LOGDIR="${TMPDIR:-/tmp}/eidl-slides"
mkdir -p "$LOGDIR"

[ $# -eq 0 ] && set -- *VL*.tex   # Default in "${@:-...}" würde nicht globben
status=0
for f in "$@"; do
  log="$LOGDIR/$(basename "$f" .tex).log"
  latexmk -lualatex -interaction=nonstopmode -halt-on-error "$f" > "$log" 2>&1 \
    || { echo "FEHLER: $f"; grep -E '^!' "$log" | head -3; status=1; continue; }
  pdf="${f%.tex}.pdf"
  pages=$(pdfinfo "$pdf" | awk '/^Pages/{print $2}')
  vbox=$(grep -c 'Overfull \\vbox' "$log" || true)
  echo "ok  $(basename "$f" .tex): $pages Seiten, $vbox zu volle Rahmen"
done
# Exit-Code statt nur einer Zeile auf stdout: Ein Bau, der scheitert, soll auch fuer den
# Aufrufer scheitern. Logs liegen in "$LOGDIR".
exit $status
