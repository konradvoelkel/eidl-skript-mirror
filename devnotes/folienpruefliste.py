#!/usr/bin/env python3
r"""Sprachprüfung der Beamer-Folien: Typografie, Rechtschreibung, Striche.

Das Gegenstück zu `sprachpruefliste.py` für `slides/*.tex`. Die Prosa holt
`folienprosa.py` (dort stehen auch die Fallen des Extraktors).

    uv run devnotes/folienpruefliste.py
    uv run devnotes/folienpruefliste.py --woerter      # nur die Rechtschreibliste
    uv run devnotes/folienpruefliste.py --deck 05      # nur ein Deck

Warum die Folien eine **eigene** Wortliste haben
------------------------------------------------
`sprachpruefliste-woerter.txt` gehört zum Buch. Die Folien bringen eigenes Vokabular mit,
das im Buch nicht vorkommt (`Tafelanschriebe`, `Labelphase`, `Perspektivwechsel`, dazu die
Namen aus den Dozentennotizen). Kippt man das in die Buchliste, wird die Prüfung des Buchs
stumpfer, ohne dass die der Folien schärfer wird — dieselbe Überlegung wie in C1. Gelesen
werden **beide** Listen, eingetragen wird nur in `sprachpruefliste-woerter-folien.txt`.

Der Strich
----------
In LaTeX ist `--` der Halbgeviertstrich und `---` der Geviertstrich. `CLAUDE.md` legt den
Halbgeviertstrich als Gedankenstrich fest (D2), also ist jedes `---` in der Prosa ein
Befund. Am 2026-09-29 waren es 316 in 15 Decks. **Achtung, zwei Sorten Fehlalarm:** die
`% ------`-Trennkommentare und `# <---`-Pfeile in Codeblöcken. Beide werden übersprungen.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from folienprosa import PLATZ, prosa_zeilen_tex  # noqa: E402
import sprachpruefliste as sp  # noqa: E402

WURZEL = Path(__file__).resolve().parent.parent
FOLIEN = WURZEL / "slides"
WORTLISTE = Path(__file__).resolve().parent / "sprachpruefliste-woerter-folien.txt"

# `header.tex` ist Konfiguration, keine Prosa: `pdftitle={…}`, `keywordstyle={…}` liefern
# nur Fehlalarme, und der Zeilenumbruch `\\Wort` zerbricht dort Wörter.
KEINE_PROSA = ("header",)

# Bewusst *nicht* geprüft: doppelte Leerzeichen. TeX klappt sie selbst zusammen, in
# `.tex` können sie also kein Befund sein — anders als in Markdown, wo die Regel in
# `sprachpruefliste.py` zu Recht steht. Auch nicht geprüft: „Leerzeichen vor
# Satzzeichen“. Tabellen trennen mit `&`, und das erzeugt nur Fehlalarme.

PRUEFUNGEN = [
    ("gerades Anführungszeichen (deutsch sind „ und “)", r'"'),
    ("drei Punkte als … statt ...", r"\.\.\."),
    ("Wortdoppelung", r"\b(?!die|das|der|den|dem|und|ist|sie|von|im)(\w{3,})\s+\1\b"),
    ("mehrfaches Ausrufe- oder Fragezeichen", r"[!?]{2,}"),
    ("Unicode-Pfeil (MyST-Falle, hier nur Hygiene)", r"[→←↔⇒⇐]"),
]


def decks(muster: str | None) -> list[Path]:
    alle = [p for p in sorted(FOLIEN.glob("*.tex"))
            if not any(k in p.name for k in KEINE_PROSA)]
    if muster is None:
        return alle
    treffer = [p for p in alle if muster in p.name]
    if not treffer:
        sys.exit(f"Kein Deck zu „{muster}“ — erwartet z.B. 05 oder GANs.")
    return treffer


def kurz(p: Path) -> str:
    return p.name.split("2026 ")[-1].replace(".tex", "")


def geviertstriche(p: Path) -> list[tuple[int, str]]:
    """`---` in der Prosa: nicht in Kommentaren, nicht in Codeblöcken, keine Striche-Reihe."""
    raus, in_code = [], False
    for i, z in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        if re.search(r"\\begin\{(lstlisting|verbatim|minted)\}", z):
            in_code = True
        elif re.search(r"\\end\{(lstlisting|verbatim|minted)\}", z):
            in_code = False
        if in_code:
            continue
        m = re.search(r"(?<!\\)%", z)
        text = z[: m.start()] if m else z
        for t in re.finditer(r"(?<!-)---(?!-)", text):
            a = max(0, t.start() - 50)
            raus.append((i, text[a : t.end() + 40].strip()))
    return raus


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--deck", help="nur Decks, deren Name das enthält")
    ap.add_argument("--woerter", action="store_true", help="nur die Rechtschreibliste")
    a = ap.parse_args()
    ziel = decks(a.deck)

    zeilen_je = {kurz(p): prosa_zeilen_tex(p.read_text(encoding="utf-8")) for p in ziel}

    if not a.woerter:
        n = 0
        for p in ziel:
            befunde = [(i, k, "Geviertstrich --- (Gedankenstrich ist --, siehe D2)")
                       for i, k in geviertstriche(p)]
            for i, z in enumerate(zeilen_je[kurz(p)], 1):
                for titel, muster in PRUEFUNGEN:
                    for m in re.finditer(muster, z):
                        a0 = max(0, m.start() - 50)
                        befunde.append((i, z[a0 : m.end() + 40].replace(PLATZ, "·").strip(), titel))
            if befunde:
                print(f"\n## {kurz(p)}")
                for i, k, titel in sorted(befunde):
                    print(f"- [ ] Z.{i} [{titel}]\n      …{k}…")
                n += len(befunde)
        print(f"\n{n} Typografie-Befunde in {len(ziel)} Deck(s).")

    # Rechtschreibung: Buchliste UND Folienliste gelten
    eigene = set()
    if WORTLISTE.exists():
        eigene = {z.split("#")[0].strip()
                  for z in WORTLISTE.read_text(encoding="utf-8").splitlines()
                  if z.split("#")[0].strip()}
    rs = {w: o for w, o in sp.rechtschreibung(zeilen_je).items() if w not in eigene}
    print(f"\n{len(rs)} unbekannte Wörter (Buch- und Folienwortliste abgezogen)")
    for w, orte in rs.items():
        print(f"  {w:30} {', '.join(f'{d}:{n}' for d, n in orte[:3])}")
    if rs:
        print(f"\nGeprüft und richtig? Dann nach {WORTLISTE.name} — aber erst ansehen.")


if __name__ == "__main__":
    main()
