#!/usr/bin/env python3
"""Legt das mitgelieferte Site-Template dort ab, wo `myst build` es erwartet.

Hintergrund: MyST laedt das Site-Template bei jedem Lauf von
`https://github.com/myst-templates/book-theme/archive/refs/heads/main.zip`
nach — von einem *Branch*, nicht von einem Tag. Damit ist das Aussehen der Seite
eine unversionierte Abhaengigkeit an fremdem `main`, und jeder Netzausfall bricht
den Build (so am 2026-09-24/25 dreimal in Folge).

`site.template` kann in `myst.yml` **keinen** lokalen Pfad aufnehmen: Der Wert wird
als Template-*Name* gegen api.mystmd.org aufgeloest, und `file://`-URLs lehnt
node-fetch ab. Was funktioniert, ist das Verzeichnis vorzubelegen, in dem MyST das
Template zwischenspeichert — dann laedt es nichts nachher.

Genau das tut dieses Skript. Es ist idempotent und braucht kein Netz.

Aufruf (vor `myst build`):

    python _site/vendor/install_template.py
"""

from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent.parent
ARCHIV = WURZEL / "_site" / "vendor" / "book-theme.zip"
ZIEL = WURZEL / "_build" / "templates" / "site" / "myst" / "book-theme"

# Woran man erkennt, dass MyST das Template als vorhanden ansieht. Liegt eine
# dieser Dateien eine Ebene zu tief (im `book-theme-main/` des Archivs), laedt
# MyST trotzdem neu — deshalb wird der Wrapper beim Entpacken entfernt.
MARKER = "template.yml"


def main() -> int:
    if not ARCHIV.is_file():
        print(f"FEHLER: {ARCHIV.relative_to(WURZEL)} fehlt", file=sys.stderr)
        return 1

    if (ZIEL / MARKER).is_file():
        print(f"Template liegt schon in {ZIEL.relative_to(WURZEL)} — nichts zu tun.")
        return 0

    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    if ZIEL.exists():
        shutil.rmtree(ZIEL)

    # In einen Nachbarordner entpacken und dann die eine Wrapper-Ebene
    # (`book-theme-main/`) zum Zielnamen machen.
    roh = ZIEL.parent / "_entpackt"
    if roh.exists():
        shutil.rmtree(roh)
    with zipfile.ZipFile(ARCHIV) as archiv:
        archiv.extractall(roh)

    inhalt = [p for p in roh.iterdir() if p.is_dir()]
    if len(inhalt) != 1:
        print(
            f"FEHLER: erwartet genau ein Wurzelverzeichnis im Archiv, "
            f"gefunden: {[p.name for p in inhalt]}",
            file=sys.stderr,
        )
        return 1

    inhalt[0].rename(ZIEL)
    shutil.rmtree(roh)

    if not (ZIEL / MARKER).is_file():
        print(f"FEHLER: {MARKER} fehlt nach dem Entpacken", file=sys.stderr)
        return 1

    print(f"Template entpackt nach {ZIEL.relative_to(WURZEL)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
