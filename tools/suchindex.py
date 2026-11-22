#!/usr/bin/env python3
"""Rohen LaTeX-Quelltext aus den Suchausschnitten nehmen.

    python3 tools/suchindex.py <html-verzeichnis>
    python3 tools/suchindex.py --check <html-verzeichnis>

Im `pages`-Job hinter den Schritten laufen lassen, die HTML anfassen, und **vor**
`precompress.py` -- es schreibt `myst.search.json` neu.


Warum es dieses Skript gibt
---------------------------

Die Suche des Themes liest `myst.search.json`, und MyST legt dort den Text jeder
Ueberschrift samt ihrem Abschnitt ab. Mathematik kommt darin vor -- aber **ohne** die
`$`-Zeichen, die sie als Mathematik auswiesen. Im Suchtreffer steht deshalb der
LaTeX-Quelltext im Klartext. Im dritten SEO-Audit (§13, 2026-11-18) zeigten mindestens
4 der 18 Treffer zu "Kreuzentropie" Dinge wie
`L_{\\text{BCE}}(x, y; w) = -\\frac1N` oder `D_{KL}(q \\Vert p)`; gezaehlt am Artefakt
vom 2026-11-22: **180 von 722 Eintraegen** mit mindestens einem Backslash.

Dieselbe Fehlerklasse wie bei den Alt-Texten (2026-11-17) und beim `DefinedTermSet`
(§5): Ein Text, der fuer die Anzeige gedacht ist, wird aus dem Quelltext gebildet,
ohne ihn zu uebersetzen.


Warum uebersetzt und nicht laut gescheitert wird
------------------------------------------------

`tools/inject_jsonld.py` macht es beim Glossar umgekehrt: Dort scheitert
`mathe_klartext()` laut an einem unbekannten Befehl, weil 69 Begriffe ueberschaubar sind
und eine falsche Definition schlimmer waere als ein roter Build. Hier geht das nicht.
Gemessen am 2026-11-22 ueber den ganzen Index: **98 verschiedene Befehle**, die die
Tabelle dort nicht kennt, in 1957 Vorkommen -- `\\mathbb` (256), `\\in` (142), `\\to`
(107), `\\partial` (107), dazu `\\begin{pmatrix}`-Umgebungen und `\\left`/`\\right`.
Ein lauter Abbruch haette den Deploy an jedem neuen Formelzeichen aufgehalten, und das
fuer einen Suchausschnitt.

Angefasst wird nur ein Feld, das einen Backslash traegt. Das ist die Bedingung dafuer,
dass ein zweiter Lauf nichts mehr tut -- aus `\\{0, 1\\}` wird `{0, 1}`, und genau diese
Klammern wuerde ein weiterer Lauf wieder abstreifen; Prosa mit geschweiften Klammern
bleibt so ebenfalls unangetastet.

Dieses Skript uebersetzt deshalb, was es kennt, und **streift den Rest ab**: Der
Backslash-Befehl fliegt heraus, die Klammern fallen weg, Leerraum wird zusammengezogen.
Die Nachbedingung ist nicht "alles richtig uebersetzt", sondern **kein Backslash mehr im
Index** -- das ist pruefbar, und es ist genau der Befund aus dem Audit. Wer einen
haeufigen Befehl haesslich abgestreift findet, traegt ihn in `ERSATZ` nach.

Die Tabelle aus `inject_jsonld.py` wird importiert und nicht kopiert: Was dort fuer das
Glossar gilt, gilt hier auch, und zwei Tabellen wuerden auseinanderlaufen.
"""

import argparse
import json
import pathlib
import re
import sys

from inject_jsonld import MATHE_ERSATZ

# Geschweifte Klammern, die am Ende **nicht** mit den LaTeX-Klammern wegfallen sollen:
# `\{` und `\}` sind eine Menge im Text. Sie werden bis zum Schluss geparkt.
PLATZ_AUF, PLATZ_ZU = "\x00", "\x01"

ERSATZ = [
    # Umgebungen und Grossklammern -- nur Geruest, kein Inhalt.
    (re.compile(r"\\(?:begin|end)\{[^}]*\}"), " "),
    (re.compile(r"\\(?:left|right|bigl|bigr|Bigl|Bigr|big|Big|biggl|biggr)\b"), ""),
    (re.compile(r"\\\\"), " "),
    (re.compile(r"\\\{"), PLATZ_AUF),
    (re.compile(r"\\\}"), PLATZ_ZU),
    # Mengen und Raeume
    (re.compile(r"\\mathbb\{R\}"), "\u211d"),
    (re.compile(r"\\mathbb\{N\}"), "\u2115"),
    (re.compile(r"\\mathbb\{Z\}"), "\u2124"),
    (re.compile(r"\\mathbb\{E\}"), "\U0001d53c"),
    (re.compile(r"\\mathbb\{([^}]*)\}"), r"\1"),
    (re.compile(r"\\math(?:cal|bf|rm|sf|it|frak)\{([^}]*)\}"), r"\1"),
    (re.compile(r"\\mathrel\{([^}]*)\}"), r"\1"),
    # Relationen und Operatoren
    (re.compile(r"\\hat="), "\u2259"),
    (re.compile(r"\\(?:notin)\b"), "\u2209"),
    (re.compile(r"\\in\b"), "\u2208"),
    (re.compile(r"\\(?:to|rightarrow)\b"), "\u2192"),
    (re.compile(r"\\mapsto\b"), "\u21a6"),
    (re.compile(r"\\Rightarrow\b"), "\u21d2"),
    (re.compile(r"\\(?:leq|le)\b"), "\u2264"),
    (re.compile(r"\\(?:geq|ge)\b"), "\u2265"),
    (re.compile(r"\\(?:neq|ne)\b"), "\u2260"),
    (re.compile(r"\\gg\b"), "\u226b"),
    (re.compile(r"\\approx\b"), "\u2248"),
    (re.compile(r"\\propto\b"), "\u221d"),
    (re.compile(r"\\pm\b"), "\u00b1"),
    (re.compile(r"\\times\b"), "\u00d7"),
    (re.compile(r"\\otimes\b"), "\u2297"),
    (re.compile(r"\\odot\b"), "\u2299"),
    (re.compile(r"\\oplus\b"), "\u2295"),
    (re.compile(r"\\ast\b"), "\u2217"),
    (re.compile(r"\\circ\b"), "\u2218"),
    (re.compile(r"\\(?:vee|lor)\b"), "\u2228"),
    (re.compile(r"\\(?:wedge|land)\b"), "\u2227"),
    (re.compile(r"\\cup\b"), "\u222a"),
    (re.compile(r"\\cap\b"), "\u2229"),
    (re.compile(r"\\subseteq\b"), "\u2286"),
    (re.compile(r"\\subset\b"), "\u2282"),
    (re.compile(r"\\partial\b"), "\u2202"),
    (re.compile(r"\\nabla\b"), "\u2207"),
    (re.compile(r"\\infty\b"), "\u221e"),
    (re.compile(r"\\prod_"), "\u220f_"),
    (re.compile(r"\\int_"), "\u222b_"),
    (re.compile(r"\\langle\b"), "\u27e8"),
    (re.compile(r"\\rangle\b"), "\u27e9"),
    (re.compile(r"\\(?:lVert|rVert|Vert)\b"), "\u2016"),
    (re.compile(r"\\lceil\b"), "\u2308"),
    (re.compile(r"\\rceil\b"), "\u2309"),
    (re.compile(r"\\top\b"), "\u1d40"),
    (re.compile(r"\\colon\b"), ":"),
    (re.compile(r"\\(?:dots|ldots|cdots)\b"), "\u2026"),
    # Funktionsnamen bleiben Namen.
    (re.compile(r"\\(log|exp|sin|cos|tan|tanh|sinh|cosh|det|dim|deg|arg|sup|inf|lim|"
                r"argmax|argmin|softmax|mod|gcd)\b"), r"\1"),
    (re.compile(r"\\sqrt\{([^{}]*)\}"), "\u221a(\\1)"),
    (re.compile(r"\\binom\{([^{}]*)\}\{([^{}]*)\}"), "(\\1 \u00fcber \\2)"),
    (re.compile(r"\\hat\{([^{}]*)\}"), "\\1\u0302"),
    (re.compile(r"\\tilde\{([^{}]*)\}"), "\\1\u0303"),
    (re.compile(r"\\(?:bar|overline)\{([^{}]*)\}"), "\\1\u0304"),
    (re.compile(r"\\vec\{([^{}]*)\}"), "\\1\u20d7"),
    # Griechisch, soweit das Buch es benutzt (die Tabelle aus inject_jsonld.py bringt
    # sigma, tau, rho, mu, lambda und varepsilon mit).
    (re.compile(r"\\alpha\b"), "\u03b1"),
    (re.compile(r"\\beta\b"), "\u03b2"),
    (re.compile(r"\\gamma\b"), "\u03b3"),
    (re.compile(r"\\delta\b"), "\u03b4"),
    (re.compile(r"\\epsilon\b"), "\u03b5"),
    (re.compile(r"\\zeta\b"), "\u03b6"),
    (re.compile(r"\\eta\b"), "\u03b7"),
    (re.compile(r"\\theta\b"), "\u03b8"),
    (re.compile(r"\\kappa\b"), "\u03ba"),
    (re.compile(r"\\nu\b"), "\u03bd"),
    (re.compile(r"\\xi\b"), "\u03be"),
    (re.compile(r"\\pi\b"), "\u03c0"),
    (re.compile(r"\\(?:varphi|phi)\b"), "\u03c6"),
    (re.compile(r"\\chi\b"), "\u03c7"),
    (re.compile(r"\\psi\b"), "\u03c8"),
    (re.compile(r"\\omega\b"), "\u03c9"),
    (re.compile(r"\\Gamma\b"), "\u0393"),
    (re.compile(r"\\Delta\b"), "\u0394"),
    (re.compile(r"\\Theta\b"), "\u0398"),
    (re.compile(r"\\Lambda\b"), "\u039b"),
    (re.compile(r"\\Sigma\b"), "\u03a3"),
    (re.compile(r"\\Phi\b"), "\u03a6"),
    (re.compile(r"\\Omega\b"), "\u03a9"),
    # Abstaende und Platzhalter
    (re.compile(r"\\(?:qquad|quad|hspace|,|;|:|!| )"), " "),
    (re.compile(r"\\nonumber\b|\\notag\b|\\limits\b|\\displaystyle\b"), ""),
]

# Was danach noch mit Backslash anfaengt, fliegt heraus -- siehe Docstring.
REST = re.compile(r"\\[A-Za-z]+\*?|\\.")


def klartext(s: str) -> str:
    """Ein Textfeld des Index ohne LaTeX-Quelltext."""
    for muster, ersatz in MATHE_ERSATZ + ERSATZ:
        s = muster.sub(ersatz, s)
    s = REST.sub("", s)
    s = s.replace("{", "").replace("}", "")
    s = s.replace(PLATZ_AUF, "{").replace(PLATZ_ZU, "}")
    # Zusammengezogen wird nur innerhalb einer Zeile: Die Ausschnitte tragen Absaetze als
    # "\n\n", und die trennen Ueberschrift und Abschnitt in der Trefferanzeige.
    s = re.sub(r"[ \t]{2,}", " ", s)
    return re.sub(r" +([,.;:)\u2026])", r"\1", s)


def felder(record: dict):
    """Die Textfelder eines Eintrags, als (Behaelter, Schluessel)."""
    for k, v in record.items():
        if isinstance(v, str) and k != "url":
            yield record, k
    h = record.get("hierarchy")
    if isinstance(h, dict):
        for k, v in h.items():
            if isinstance(v, str):
                yield h, k


def index(root: pathlib.Path) -> pathlib.Path:
    f = root / "myst.search.json"
    if not f.exists():
        sys.exit(f"FEHLER: {f} existiert nicht -- nach dem HTML-Bau laufen lassen")
    return f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html_dir")
    ap.add_argument("--check", action="store_true", help="nur nachmessen, nichts schreiben")
    args = ap.parse_args()

    f = index(pathlib.Path(args.html_dir))
    data = json.loads(f.read_text(encoding="utf-8"))
    records = data.get("records")
    if not isinstance(records, list) or not records:
        sys.exit(f"FEHLER: {f} hat keine Liste 'records' -- hat MyST das Format geaendert?")

    betroffen = n_felder = 0
    for r in records:
        geaendert = False
        for behaelter, k in felder(r):
            # Nur Felder mit Backslash, und das ist keine Abkuerzung, sondern die
            # Bedingung dafuer, dass ein zweiter Lauf nichts mehr tut: `\{0, 1\}` wird
            # zu `{0, 1}`, und diese Klammern wuerde der Lauf danach wieder abstreifen.
            # Prosa mit geschweiften Klammern bleibt damit ebenfalls unangetastet.
            if "\\" not in behaelter[k]:
                continue
            neu = klartext(behaelter[k])
            if neu != behaelter[k]:
                behaelter[k] = neu
                n_felder += 1
                geaendert = True
        betroffen += geaendert

    # Nachbedingung: kein Backslash mehr, und zwar am Ergebnis gesucht statt dem Lauf
    # geglaubt. Ein zweiter Lauf aendert null und muss trotzdem gruen sein.
    for r in records:
        for behaelter, k in felder(r):
            if "\\" in behaelter[k]:
                sys.exit(f"FEHLER: {f} hat in {r.get('url')} ({k}) weiter einen Backslash: "
                         f"{behaelter[k][:80]!r}")

    if args.check:
        if betroffen:
            sys.exit(f"FEHLER: {f} traegt in {betroffen} von {len(records)} Eintraegen noch "
                     "LaTeX-Quelltext -- ist tools/suchindex.py gelaufen?")
        print(f"✓ suchindex: {len(records)} Eintraege, kein LaTeX-Quelltext")
        return 0

    f.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    print(f"suchindex: {len(records)} Eintraege, {betroffen} bereinigt, {n_felder} Felder")
    return 0


if __name__ == "__main__":
    sys.exit(main())
