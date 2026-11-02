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

Danach setzt es **deutsche Kastennamen** ein (seit 2026-11-02): Das Template schreibt in
den Kopf jedes `{prf:…}`-Kastens das `kind` mit großem Anfangsbuchstaben, also „Example 1“,
„Theorem 2“. Dieselbe Stelle steht zweimal im Template, im Bündel fürs Server-Rendering
(`build/index.js`) und in dem für den Browser (`public/build/_shared/…`); beide werden
gepatcht, sonst schreibt der Browser beim Hydrieren das Englische zurück. Gesucht wird nach
Struktur, nicht nach den minifizierten Namen; findet sich die Stelle nicht genau einmal je
Bündel, endet das Skript mit Fehler — dann hat sich das Template bewegt. Das PDF repariert
`devnotes/patch_myst_tex.py`.

Aufruf (vor `myst build`):

    python _site/vendor/install_template.py
"""

from __future__ import annotations

import re
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

# Deutsche Namen der prf-Kästen; was hier fehlt, behält den englischen Namen.
KASTENNAMEN = {
    "proof": "Beweis", "theorem": "Satz", "lemma": "Lemma", "definition": "Definition",
    "example": "Beispiel", "remark": "Bemerkung", "corollary": "Folgerung",
    "proposition": "Proposition", "axiom": "Axiom", "conjecture": "Vermutung",
    "observation": "Beobachtung", "algorithm": "Algorithmus", "exercise": "Aufgabe",
}
KOPF = re.compile(r'kind:(\w+)\((\w)\),children:\[\1\(\2\)," ",(\w)\]')
GEPATCHT = "/*eidl:kastennamen*/"


def kastennamen_eindeutschen() -> int:
    """Ersetzt im Kopf der prf-Kästen `Gross(kind)` durch den deutschen Namen."""
    tabelle = "{" + ",".join(f'{k}:"{v}"' for k, v in KASTENNAMEN.items()) + "}"
    buendel = [ZIEL / "build" / "index.js", *sorted((ZIEL / "public" / "build" / "_shared").glob("*.js"))]
    gefunden = 0
    for pfad in buendel:
        text = pfad.read_text(encoding="utf-8", errors="surrogateescape")
        if GEPATCHT in text:
            gefunden += 1
            continue
        treffer = KOPF.findall(text)
        if not treffer:
            continue
        if len(treffer) != 1:
            print(f"FEHLER: {len(treffer)} Kastenköpfe in {pfad.name}, erwartet 1", file=sys.stderr)
            return 1
        gross, k, nr = treffer[0]
        alt = f'kind:{gross}({k}),children:[{gross}({k})," ",{nr}]'
        neu = f'kind:{gross}({k}),children:[{GEPATCHT}({tabelle}[{k}]||{gross}({k}))," ",{nr}]'
        pfad.write_text(text.replace(alt, neu), encoding="utf-8", errors="surrogateescape")
        print(f"Kastennamen eingedeutscht: {pfad.relative_to(WURZEL)}")
        gefunden += 1
    if gefunden != 2:
        print(f"FEHLER: Kastenkopf in {gefunden} statt 2 Bündeln gefunden — Template bewegt?", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    if not ARCHIV.is_file():
        print(f"FEHLER: {ARCHIV.relative_to(WURZEL)} fehlt", file=sys.stderr)
        return 1

    if (ZIEL / MARKER).is_file():
        print(f"Template liegt schon in {ZIEL.relative_to(WURZEL)}.")
        return kastennamen_eindeutschen()

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
    return kastennamen_eindeutschen()


if __name__ == "__main__":
    raise SystemExit(main())
