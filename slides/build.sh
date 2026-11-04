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

  # Gezaehlt wird im LaTeX-Log neben der .tex, NICHT in der Ausgabe von latexmk oben.
  # Grund (2026-11-04): Ist das PDF schon aktuell, startet latexmk LaTeX gar nicht erst --
  # dann steht in seiner Ausgabe kein einziges "Overfull", und das Skript meldete "0 zu
  # volle Rahmen" fuer ein PDF, das einen zu vollen Rahmen hatte. Falsches Gruen ist
  # schlimmer als keine Zahl. Das LaTeX-Log dagegen stammt aus dem Lauf, der das
  # vorhandene PDF erzeugt hat.
  # Dass es wirklich dazu gehoert, wird an der Bytezahl geprueft, die LaTeX selbst
  # hineinschreibt ("(22 pages, 1865916 bytes)."): nicht an Zeitstempeln, denn dash kennt
  # `test -ot` nicht, und nicht an der Seitenzahl allein, die sich bei einer Aenderung oft
  # gar nicht aendert. Die Zeile "Output written on ..." selbst taugt nicht als Anker --
  # LaTeX bricht sie mitten im Dateinamen um.
  # Fehlt das Log, hilft `touch` auf die .tex NICHT: latexmk vergleicht Pruefsummen, nicht
  # Zeitstempel, und ueberspringt den Lauf trotzdem. Nur `latexmk -g` baut erzwungen neu.
  # (Und keine Backticks in die Meldung unten -- die Shell fuehrt sie aus; so hat dieses
  # Skript am 2026-11-04 bei jedem Deck ein ratloses `touch` aufgerufen.)
  # Und die Zeile wird VOR dem Vergleich entfaltet. LaTeX bricht das Log hart bei 79
  # Zeichen um, und wo der Umbruch landet, haengt an der Laenge des Dateinamens: bei VL 08
  # mitten in "pages", bei VL 11 hinter der Klammer, bei VL 13 mitten in der Bytezahl
  # ("1" / "539457"). Zeilenweise gesucht, fand der Vergleich dort nichts und meldete
  # "nicht geprueft" fuer drei einwandfreie Decks (2026-11-04).
  texlog="${f%.tex}.log"
  logbytes=""
  [ -f "$texlog" ] && logbytes=$(tr -d '\n' < "$texlog" | sed -n \
    's/.*(\([0-9]\{1,\}\) pages\{0,1\}, \([0-9]\{1,\}\) bytes)\..*/\2/p')
  if [ -z "$logbytes" ] || [ "$logbytes" != "$(wc -c < "$pdf" | tr -d ' ')" ]; then
    echo "ok  $(basename "$f" .tex): $pages Seiten, Rahmen NICHT geprueft (LaTeX-Log fehlt oder passt nicht zum PDF; mit latexmk -g erzwingen)"
    continue
  fi
  # Nur \vbox, wie gehabt: die drei \hbox je Deck kommen aus der Ablaufplan-Tabelle in der
  # Titelnotiz und sind bekanntes Rauschen (PLAYBOOK-folien §2.4).
  vbox=$(grep -c 'Overfull \\vbox' "$texlog" || true)
  echo "ok  $(basename "$f" .tex): $pages Seiten, $vbox zu volle Rahmen"
done
# Exit-Code statt nur einer Zeile auf stdout: Ein Bau, der scheitert, soll auch fuer den
# Aufrufer scheitern. Logs liegen in "$LOGDIR".
exit $status
