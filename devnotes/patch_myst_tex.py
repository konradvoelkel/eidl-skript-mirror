#!/usr/bin/env python3
"""Repariert zwei Fehler im LaTeX-Export von mystmd.

Beide treffen **nur** das PDF; im HTML ist nichts davon zu sehen. Beide sind
idempotent gepatcht, und beide scheitern laut, wenn die Stelle nach einem
Versionssprung nicht mehr da ist — dann hat mystmd sich bewegt, und jemand sieht
nach, ob der Fehler oben behoben ist (dann kann der betreffende Patch weg).

## 1. Leerzeichen vor jedem Bindestrich in Codeblöcken

MyST schreibt den Inhalt von Codeblöcken mit `state.text(node3.value, true)` in die
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
`code_style`. Nachgewiesen mit mystmd 1.10.1 (dieses Repo) und 1.11.0 (eipy-skript);
minimal reproduzierbar mit einem Codeblock, der `a-b` enthält. Nur der Bindestrich ist
betroffen, die übrigen ASCII-Sonderzeichen gehen unverändert durch.

Die Reparatur schreibt den Wert unescaped in die Verbatim-Umgebung, wo er hingehört:

    state.text(node3.value, true)  ->  state.write(node3.value)

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

## Aufruf (idempotent)

    python3 devnotes/patch_myst_tex.py              # sucht das Bundle selbst
    python3 devnotes/patch_myst_tex.py <pfad.cjs>   # oder gezielt

Gegenproben im gebauten PDF:

    pdftotext exports/eidl-skript.pdf - | grep -c ' -[a-zA-Z-]'   # Befehle
    pdftotext exports/eidl-skript.pdf - | grep -c '¿\\|¡'          # Anführungszeichen
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path

# Anker: die Zeile, die den minted-Fall im `code`-Handler aufbaut. Sie steht im Bundle
# auch dann, wenn das Projekt `verbatim` exportiert — der Handler ist derselbe. Direkt
# dahinter folgt die zu patchende Stelle; `state.text(…, true)` kommt im Bundle noch ein
# zweites Mal vor (Inline-Mathematik), und die ist richtig.
PATCHES = (
    (
        "Bindestriche in Codeblöcken",
        "begin{minted}[breaklines]",
        600,
        "state.text(node3.value, true)",
        "state.write(node3.value)",
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


def patche(pfad: Path) -> int:
    text = pfad.read_text(encoding="utf-8")
    fehler = 0
    geaendert = False

    for name, anker, fenstergroesse, alt, neu in PATCHES:
        if anker not in text:
            print(
                f"FEHLER [{name}]: Anker {anker!r} fehlt in {pfad} — andere mystmd-Version?",
                file=sys.stderr,
            )
            fehler += 1
            continue
        start = text.index(anker)
        fenster = text[start : start + fenstergroesse]
        if neu in fenster and alt not in fenster:
            print(f"{pfad.name} [{name}]: bereits gepatcht")
            continue
        if fenster.count(alt) != 1:
            print(
                f"FEHLER [{name}]: {alt!r} steht {fenster.count(alt)}x im Fenster hinter "
                "dem Anker, erwartet genau 1x — bitte von Hand nachsehen",
                file=sys.stderr,
            )
            fehler += 1
            continue
        text = text[:start] + fenster.replace(alt, neu, 1) + text[start + fenstergroesse :]
        geaendert = True
        print(f"{pfad.name} [{name}]: gepatcht ({alt} -> {neu})")

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
