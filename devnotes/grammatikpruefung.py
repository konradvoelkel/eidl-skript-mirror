#!/usr/bin/env python3
"""Grammatik- und Kohärenzprüfung der Prosa mit LanguageTool (Antwort auf D5).

Das dritte Werkzeug des Sprachdurchgangs, neben `sprachpruefliste.py` (Typografie,
Satzlänge, Rechtschreibung) und `check_doku.py`. Es beantwortet die eine Frage, die
`aspell` prinzipiell nicht beantworten kann: **Passt es grammatisch zusammen, und
schreibt das Buch dasselbe Wort überall gleich?**

    uv run --no-project --with language-tool-python devnotes/grammatikpruefung.py
    …                                                 --alle      # ungefiltert
    …                                                 --datei 16  # ein Kapitel

Voraussetzungen und warum es nicht in `pyproject.toml` steht
------------------------------------------------------------
LanguageTool ist Java und lädt beim ersten Lauf ~260 MB. Das Buch braucht davon nichts
zum Bauen — die Regel „Das Image installiert kein einziges Python-Paket“ gilt weiter.
Deshalb **ephemer** aufrufen (`uv run --no-project --with …`), nicht als Abhängigkeit
eintragen. Den Download legt man mit `LTP_PATH` dorthin, wo Platz ist:

    export LTP_PATH=/media/konrad/xtraspace/languagetool

Was gefiltert wird und warum
----------------------------
Ungefiltert meldete LanguageTool am 2026-09-29 über das ganze Buch **1 930 Treffer, von
denen 6 echt waren**. Der Rest ist strukturell erklärbar und kommt garantiert wieder:

* `GERMAN_SPELLER_RULE` (1 681) — Fachvokabular. Das macht `sprachpruefliste.py` besser,
  weil es die Projektwortliste kennt.
* `DE_CASE` (98) — LanguageTool sieht Markdown nicht: `**Weg 2, Embeddings.** Ein Text …`
  liest es als *einen* Satz und will „ein“ klein.
* `UPPERCASE_SENTENCE_START` (34) — ein Satz, der nach einer abgesetzten Formel
  weitergeht, ist richtig so.
* `F_ANSTATT_PH` (12) — will „Graf“ statt „Graph“; im Fach falsch.
* `EMPFOHLENE_GETRENNTSCHREIBUNG` (7) — will „nicht linear“ statt „nichtlinear“; ebenso.

`PRODUKTIV` unten ist deshalb die Liste der Regeln, die im Buch tatsächlich etwas
gefunden haben. **Wer eine Regel herausnimmt, weil sie einmal danebenlag, nimmt sie für
immer heraus** — lieber den Einzelfall prüfen und hier einen Kommentar hinterlassen.

Ein Fallstrick, der Zeit kostet
-------------------------------
Satz für Satz prüfen dauert zu lange (2 721 Aufrufe, nach zehn Minuten abgebrochen).
Dieses Skript schickt **eine Anfrage je Datei** über die verkettete Prosa und rechnet die
Trefferoffsets per `bisect` auf Zeilennummern zurück. Das läuft in gut zwei Minuten.
"""
from __future__ import annotations

import argparse
import bisect
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sprachpruefliste import PLATZ, kapitel_dateien, prosa_zeilen, waehle  # noqa: E402

# Die Regeln, die am 2026-09-29 im Buch etwas Echtes gefunden haben. Siehe Docstring.
PRODUKTIV = {
    "DE_COMPOUND_COHERENCY",     # fand E3, E4, E5 — beide Schreibweisen je für sich richtig
    "STATT_DESSEN",              # fand R6
    "ALS_ERSTES",                # fand R7
    "DER_KORPUS",                # fand R8
    "KOMMA_VOR_UND_ODER",        # führte zu D6
    "ZUSAMMENGESETZTE_VERBEN",
    "EMPFOHLENE_ZUSAMMENSCHREIBUNG",
    "COMPOUND_INFINITIV_RULE",
    "DE_VERBAGREEMENT",
    "KOMMA_STATT_PUNKT",
    "MONTAGS",                   # fand R12 in kurs-2026-27.md
    "VIELZAHL_PLUS_SINGULAR",    # fand R13 ebenda
}


def pruefe(dateien: list[Path], alle: bool) -> int:
    try:
        import language_tool_python as lt
    except ImportError:
        sys.exit("language_tool_python fehlt. Aufruf:\n"
                 "  uv run --no-project --with language-tool-python "
                 "devnotes/grammatikpruefung.py")
    tool = lt.LanguageTool("de-DE")
    treffer = 0
    try:
        for p in dateien:
            # Mathe und Code als „X“: im deutschen Satz steht dort fast immer ein Symbol.
            zeilen = [z.replace(PLATZ, "X") for z in prosa_zeilen(p.read_text(encoding="utf-8"))]
            text = "\n".join(zeilen)
            start, akk = [], 0
            for z in zeilen:
                start.append(akk)
                akk += len(z) + 1
            for m in tool.check(text):
                if not alle and m.rule_id not in PRODUKTIV:
                    continue
                treffer += 1
                nr = bisect.bisect_right(start, m.offset)
                print(f"- [ ] {p.name}:{nr}  [{m.rule_id}] -> {m.replacements[:3]}")
                print(f"      {re.sub(r'\\s+', ' ', m.context).strip()[:150]}")
    finally:
        tool.close()
    return treffer


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--datei", metavar="KAPITEL", help="nur dieses Kapitel, z.B. 16 oder glossar")
    ap.add_argument("--alle", action="store_true",
                    help="ungefiltert — erwarte über 1900 Treffer, fast alle falsch")
    a = ap.parse_args()
    dateien = waehle(a.datei) if a.datei else kapitel_dateien()
    n = pruefe(dateien, a.alle)
    print(f"\n{n} Treffer in {len(dateien)} Datei(en)"
          f"{'' if a.alle else f', gefiltert auf {len(PRODUKTIV)} Regeln'}.")
    if not a.alle:
        print("Ungefiltert: --alle. Jeder Treffer ist zu prüfen, nicht zu glauben.")


if __name__ == "__main__":
    main()
