#!/usr/bin/env python3
"""Den Hinweiskasten „Site not loading correctly?“ aus den gebauten Seiten nehmen.

    python3 tools/no_css_dialog.py <html-verzeichnis>
    python3 tools/no_css_dialog.py <html-verzeichnis> --check

Das Theme legt in jede Seite ein `<dialog id="myst-no-css">` mit dem Text

    Site not loading correctly? This may be due to an incorrect BASE_URL
    configuration. See the MyST Documentation for reference.

und einem Skript, das den Dialog öffnet, falls die CSS-Variable `--has-styling` fehlt.
Für Leser ist er unsichtbar, solange das Stylesheet lädt — **im Text der Seite steht er
trotzdem, und zwar als erstes**. Wer die Seite als Text liest (Vorschau-Dienste,
Suchmaschinen-Schnipsel, die Textextraktion von Sprachmodell-Crawlern, Screenreader im
Durchlauf), bekommt eine Fehlermeldung über eine kaputte Deploy-Konfiguration als
Einstieg in ein Vorlesungsskript (Befund Konrad, 2026-11-04).

Hier liefert das Stylesheet `tools/vendor_assets.py` aus dem eigenen Verzeichnis aus, und
`tools/check_css_assets.py` prüft im selben Job, dass jede eingebundene Datei existiert.
Der Dialog wäre also ein Warnschild für einen Fehler, den der Bau schon verhindert.
**Was wir dafür aufgeben:** Sollte das Stylesheet in der Auslieferung doch einmal fehlen,
sieht der Leser unformatiertes HTML ohne Erklärung. Das ist der Preis, und er ist bewusst.

Das Skript zählt, was es entfernt, und scheitert, wenn es **nichts** findet: Benennt ein
mystmd-Update den Dialog um, soll das auffallen und nicht still durchlaufen (die Regel
„ein Schritt meldet die Zahl, auf die er gewirkt hat“ aus PLAYBOOK §3.10).
"""

import argparse
import pathlib
import re
import sys

DIALOG = re.compile(r'<dialog\s+id="myst-no-css".*?</dialog>', re.S)


def seiten(wurzel):
    return sorted(pathlib.Path(wurzel).rglob("*.html"))


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("verzeichnis")
    p.add_argument("--check", action="store_true",
                   help="nur prüfen, ob der Kasten weg ist (Exit 1, wenn nicht)")
    args = p.parse_args()

    dateien = seiten(args.verzeichnis)
    if not dateien:
        print("Keine HTML-Datei unter %s" % args.verzeichnis)
        return 1

    if args.check:
        uebrig = [f for f in dateien
                  if DIALOG.search(f.read_text(encoding="utf-8", errors="replace"))]
        if uebrig:
            print("no_css_dialog --check: Kasten noch in %d von %d Seiten, z. B. %s"
                  % (len(uebrig), len(dateien), uebrig[0]))
            return 1
        print("no_css_dialog --check: in allen %d Seiten weg" % len(dateien))
        return 0

    geaendert = 0
    for f in dateien:
        s = f.read_text(encoding="utf-8", errors="replace")
        neu, n = DIALOG.subn("", s)
        if n:
            f.write_text(neu, encoding="utf-8")
            geaendert += 1
    if not geaendert:
        print("no_css_dialog: in keiner der %d Seiten gefunden -- heisst der Kasten noch "
              "'myst-no-css'? (mystmd-Update?)" % len(dateien))
        return 1
    print("no_css_dialog: aus %d von %d Seiten entfernt" % (geaendert, len(dateien)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
