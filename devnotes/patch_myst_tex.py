#!/usr/bin/env python3
"""Repariert drei Fehler im LaTeX-Export von mystmd.

Beide treffen **nur** das PDF; im HTML ist nichts davon zu sehen. Beide sind
idempotent gepatcht, und beide scheitern laut, wenn die Stelle nach einem
Versionssprung nicht mehr da ist — dann hat mystmd sich bewegt, und jemand sieht
nach, ob der Fehler oben behoben ist (dann kann der betreffende Patch weg).

## 1. Leerzeichen vor jedem Bindestrich in Codeblöcken

MyST schreibt den Inhalt von Codeblöcken mit `state.text(nodeN.value, true)` in die
`.tex` — das zweite Argument heißt `mathMode`. Der Inhalt wird also als **Mathematik**
escaped, und dabei setzt MyST vor jeden Bindestrich ein Leerzeichen:

    Quelle:   pip install torch torchvision --index-url https://…/cu129
    erzeugt:  pip install torch torchvision - -index -url https://…/cu129
    Quelle:   nvidia-smi
    erzeugt:  nvidia -smi

Im Lauf vom 2026-09-20 waren es hier 49 Stellen in 18 Kapiteldateien — Befehle, die
nicht funktionieren, wenn man sie abtippt, und Modellnamen wie `facebook/wmt19-en-de`,
die falsch dastehen.

Die betroffene Stelle sitzt im **gemeinsamen `code`-Handler** von myst-to-tex, also vor
der Verzweigung nach `verbatim`, `lstlisting` und `minted`: Der Fehler trifft jeden
`code_style`. Nachgewiesen mit mystmd 1.10.1 und 1.11.0 (dieses Repo wie eipy-skript);
minimal reproduzierbar mit einem Codeblock, der `a-b` enthält. Nur der Bindestrich ist
betroffen, die übrigen ASCII-Sonderzeichen gehen unverändert durch.

Die Reparatur schreibt den Wert unescaped in die Verbatim-Umgebung, wo er hingehört:

    state.text(nodeN.value, true)  ->  state.write(nodeN.value)

**`nodeN` ist ein minifizierter Name und wandert**: In mystmd 1.10.1 und 1.11.0 hieß die
Variable `node3`, in 1.13.0 heißt sie `node4`, ohne dass sich an der Stelle inhaltlich
etwas geändert hätte. Dieser Patch sucht deshalb als einziger mit einem **regulären
Ausdruck** statt mit einer festen Zeichenkette; Anker, Fenster und die Forderung nach
genau einem Treffer bleiben, der Patch scheitert also weiterhin laut, wenn mystmd die
Stelle wirklich bewegt. Am 2026-11-17 gefunden, als 1.13.0 geprüft wurde: Acht der neun
Ersetzungen griffen, diese eine nicht — und zwar nur wegen des Namens.

## 2. `?“` wird zu `?¿` — die TeX-Ligatur schlägt zu

MyST übersetzt das schließende deutsche Anführungszeichen `“` (U+201C) in die
TeX-Schreibweise ``` `` ```. Das Glyph stimmt — aber direkt hinter einem Fragezeichen
bildet XeLaTeX daraus die Ligatur ``?` `` = `¿`:

    Quelle:   … nie „Geht das mit neuronalen Netzen?“ (Antwort: JA) …
    im PDF:   … nie „Geht das mit neuronalen Netzen¿‘ (Antwort: JA) …

Dasselbe mit `!“` (ergibt `¡`). In diesem Buch neunmal, gefunden 2026-09-27 beim Lesen
des eigenen PDF. Die Reparatur klammert die Ersetzung ein — `{``}` statt ``` `` ``` —,
dann kann keine Ligatur über die Klammergrenze entstehen; das Anführungszeichen selbst
bleibt unverändert. Dasselbe für das einfache `‘`.

## 3. Kästen heißen „Example“ und „Theorem“

mystmd legt die Umgebungen für `{prf:…}`-Kästen mit festen englischen Namen an
(`\\newtheorem{example}{Example}[section]` in `renderThmDefinitions`), unabhängig von der
Sprache des Dokuments; babel übersetzt nur `proof` („Beweis“), weil das amsthm-eigene
`\\proofname` ist. In diesem Buch standen so 15-mal „Example“ und 4-mal „Theorem“ im PDF,
gemeldet am 2026-11-02. Die Reparatur ersetzt die Namen in genau dieser Liste; die
Umgebungsnamen (`example`, `theorem`) bleiben, also auch jedes `\\label` und jeder Verweis.
Das HTML hat dasselbe Problem an anderer Stelle, im Site-Template; das repariert
`_site/vendor/install_template.py`.

## Aufruf (idempotent)

    python3 devnotes/patch_myst_tex.py              # sucht das Bundle selbst
    python3 devnotes/patch_myst_tex.py <pfad.cjs>   # oder gezielt

Gegenproben im gebauten PDF:

    pdftotext exports/eidl-skript.pdf - | grep -c ' -[a-zA-Z-]'   # Befehle
    pdftotext exports/eidl-skript.pdf - | grep -c '¿\\|¡'          # Anführungszeichen
    pdftotext exports/eidl-skript.pdf - | grep -cE '^(Example|Theorem) [0-9]'  # Kastennamen
"""

from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

# Anker: die Zeile, die den minted-Fall im `code`-Handler aufbaut. Sie steht im Bundle
# auch dann, wenn das Projekt `verbatim` exportiert — der Handler ist derselbe. Direkt
# dahinter folgt die zu patchende Stelle; `state.text(…, true)` kommt im Bundle noch ein
# zweites Mal vor (Inline-Mathematik), und die ist richtig.
#
# Vier Felder je Patch, bei Bedarf ein fünftes: Name, Anker, Fenstergröße, gesuchte
# Stelle, Ersatz — und, wo die gesuchte Stelle ein regulärer Ausdruck ist, die Form, an
# der „schon gepatcht“ zu erkennen ist. Ohne das sechste Feld ist das der Ersatz selbst.
PATCHES = (
    (
        "Bindestriche in Codeblöcken",
        "begin{minted}[breaklines]",
        600,
        re.compile(r"state\.text\((node\w*)\.value, true\)"),
        r"state.write(\1.value)",
        re.compile(r"state\.write\(node\w*\.value\)"),
    ),
    (
        "Anführungszeichen-Ligatur (doppelt)",
        "var textOnlyReplacements2",
        400,
        '"\\u201C": "``",',
        '"\\u201C": "{``}",',
    ),
    (
        "Anführungszeichen-Ligatur (einfach)",
        "var textOnlyReplacements2",
        400,
        '"\\u2018": "`",',
        '"\\u2018": "{`}",',
    ),
) + tuple(
    (f"Kastenname {en}", "renderThmDefinitions() {", 900, f"{{{en}}}", f"{{{de}}}")
    for en, de in (
        ("Theorem", "Satz"),
        ("Corollary", "Folgerung"),
        ("Example", "Beispiel"),
        ("Remark", "Bemerkung"),
        ("Conjecture", "Vermutung"),
        ("Observation", "Beobachtung"),
    )
)

KANDIDATEN = (
    "/usr/local/lib/node_modules/mystmd/dist/myst.cjs",
    ".venv/lib/python3.*/site-packages/mystmd_py/myst.cjs",
)


def finde_bundle() -> Path | None:
    for muster in KANDIDATEN:
        for treffer in sorted(glob.glob(muster)):
            return Path(treffer)
    return None


def zaehle(muster: str | re.Pattern[str], text: str) -> int:
    return len(muster.findall(text)) if isinstance(muster, re.Pattern) else text.count(muster)


def steckt_drin(muster: str | re.Pattern[str], text: str) -> bool:
    return bool(muster.search(text)) if isinstance(muster, re.Pattern) else muster in text


def ersetze(muster: str | re.Pattern[str], neu: str, text: str) -> str:
    if isinstance(muster, re.Pattern):
        return muster.sub(neu, text, count=1)
    return text.replace(muster, neu, 1)


def patche(pfad: Path) -> int:
    text = pfad.read_text(encoding="utf-8")
    fehler = 0
    geaendert = False

    for eintrag in PATCHES:
        name, anker, fenstergroesse, alt, neu = eintrag[:5]
        schon = eintrag[5] if len(eintrag) > 5 else neu
        if anker not in text:
            print(
                f"FEHLER [{name}]: Anker {anker!r} fehlt in {pfad} — andere mystmd-Version?",
                file=sys.stderr,
            )
            fehler += 1
            continue
        start = text.index(anker)
        fenster = text[start : start + fenstergroesse]
        if steckt_drin(schon, fenster) and not steckt_drin(alt, fenster):
            print(f"{pfad.name} [{name}]: bereits gepatcht")
            continue
        if zaehle(alt, fenster) != 1:
            print(
                f"FEHLER [{name}]: {alt!r} steht {zaehle(alt, fenster)}x im Fenster hinter "
                "dem Anker, erwartet genau 1x — bitte von Hand nachsehen",
                file=sys.stderr,
            )
            fehler += 1
            continue
        # Fuer die Meldung die wirklich gefundene Stelle zeigen, nicht das Muster.
        gefunden = alt.search(fenster).group(0) if isinstance(alt, re.Pattern) else alt
        ersetzt = ersetze(alt, neu, fenster)
        text = text[:start] + ersetzt + text[start + fenstergroesse :]
        geaendert = True
        gesetzt = ersetze(alt, neu, gefunden) if isinstance(alt, re.Pattern) else neu
        print(f"{pfad.name} [{name}]: gepatcht ({gefunden} -> {gesetzt})")

    if geaendert:
        pfad.write_text(text, encoding="utf-8")
    return 1 if fehler else 0


def main(argv: list[str]) -> int:
    pfad = Path(argv[0]) if argv else finde_bundle()
    if pfad is None or not pfad.is_file():
        print("FEHLER: kein mystmd-Bundle gefunden", file=sys.stderr)
        return 1
    return patche(pfad)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
