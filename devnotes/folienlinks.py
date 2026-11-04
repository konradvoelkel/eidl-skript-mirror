#!/usr/bin/env python3
"""Die Foliensätze in den Kapiteln verlinken — mit Seitenbereich.

    uv run devnotes/folienlinks.py            # Vorschlag zeigen
    uv run devnotes/folienlinks.py --schreiben  # in die Kapitel eintragen
    uv run devnotes/folienlinks.py --check    # stimmen die Bereiche noch?

Warum (2026-11-04)
------------------
Seit die Decks im CI gebaut und als `/folien/vl01.pdf` … `/folien/vl15.pdf` veröffentlicht
werden, kann das Skript sie verlinken — und zwar **seitengenau**: `#page=N` ist Teil der
PDF Open Parameters und funktioniert in Chrome, Firefox und Edge (am 2026-11-04 am
ausgelieferten PDF gemessen). Der Link steht dort, wo auch die Aufzeichnung steht, direkt
unter der Kapitelüberschrift.

Woher die Seitenzahlen kommen
-----------------------------
**Nicht geraten.** Zwei Quellen, in dieser Reihenfolge:

1. Der Folientitel je Seite (`pdftotext -f N -l N`) wird gegen die `##`-Überschriften des
   Kapitels gehalten. Deckt eine Sitzung zwei Kapitel ab, ist die Grenze die erste Seite,
   deren Titel zu einer Überschrift des zweiten Kapitels passt. Das löst elf der fünfzehn
   Decks von selbst.
2. Für die vier übrigen steht die Grenze in GRENZEN unten — abgelesen aus dem Ablaufplan in
   der Titelnotiz des Decks („Folien 12--14 & Tensor $\\approx$ Array“) und am Folientitel
   gegengeprüft. Diese vier Zeilen sind die einzige Handarbeit; ändert sich ein Deck
   wesentlich, meldet `--check`, dass der Titel an der Grenze nicht mehr passt.

Die Zuordnung Sitzung → Kapitel kommt aus der Tabelle in `../kurs-2026-27.md`, nicht aus
einer zweiten Liste. Ein Kapitel kann in zwei Sitzungen vorkommen (Backpropagation in VL 6
und VL 13, Anwendungsbeispiele in VL 14 und VL 15); dann nennt die Zeile beide.
"""

import argparse
import glob
import io
import json
import pathlib
import re
import subprocess
import sys
import unicodedata

WURZEL = pathlib.Path(__file__).resolve().parent.parent
# **Vollstaendige Adresse, nicht `/folien/...`.** Eine absolute Pfadangabe funktioniert im
# HTML, wird aber im PDF-Export zu einem Link ohne Host und damit tot -- und das Skript
# wird gedruckt und als PDF weitergegeben. Dieselbe Entscheidung wie bei den
# Aufzeichnungslinks, die auch voll ausgeschrieben sind.
SITE = "https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de/"
# Erkannt wird die Zeile an ihrem Inhalt, nicht an einer Marke: mystmd laesst rohes
# HTML fallen oder gibt es escaped aus (am 2026-11-04 gemessen), ein
# `<!-- ... -->` koennte also als Text auf der Seite landen.
MARKE = "/folien/vl"

# Grenzen, die der Titelvergleich nicht findet: Sitzung -> {Kapitelindex: erste Seite}.
# Quelle ist der Ablaufplan in der Titelnotiz des jeweiligen Decks.
GRENZEN = {
    3:  {1: 12},   # "Folien 12--14 & Tensor = Array"
    12: {1: 9},    # "Folien 9--10 & Zehn Wege, ein LLM zu nutzen"
    14: {1: 14},   # Folie 14 ist "Anwendung 1: hAInrich"
    15: {1: 13},   # Folie 13 ist "Vibecoding"
}


def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c)).replace("ß", "ss")
    return [w for w in re.sub(r"[^a-z0-9 ]+", " ", t).split() if w]


def seiten_titel(pdf):
    kopf = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    n = int(kopf.split("Pages:")[1].split()[0])
    out = {}
    for p in range(1, n + 1):
        z = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", pdf, "-"],
                           capture_output=True, text=True).stdout.strip().splitlines()
        out[p] = z[0].strip() if z else ""
    return n, out


def kurs_plan():
    s = (WURZEL / "kurs-2026-27.md").read_text(encoding="utf-8")
    plan = {}
    for z in s.splitlines():
        if re.match(r"^\| *\d+ *\|", z):
            sp = [x.strip() for x in z.strip("|").split("|")]
            plan[int(sp[0])] = re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", sp[1])
    return plan


def bereiche():
    """Je Sitzung: [(Kapitelpfad, Kapiteltitel, von, bis, Titel der Startfolie)]."""
    plan, alles = kurs_plan(), {}
    for nr, kapitel in sorted(plan.items()):
        pdfs = glob.glob(str(WURZEL / "slides" / ("*VL %02d *.pdf" % nr)))
        if not pdfs:
            continue
        n, titel = seiten_titel(pdfs[0])
        heads = []
        for t, pfad in kapitel:
            txt = (WURZEL / pfad).read_text(encoding="utf-8")
            heads.append([norm(t)] + [norm(h) for h in re.findall(r"^#{2,3} (.+)$", txt, re.M)])
        grenzen = [2]
        for k in range(1, len(kapitel)):
            hand = GRENZEN.get(nr, {}).get(k)
            if hand:
                grenzen.append(hand)
                continue
            treffer = None
            for p in range(grenzen[-1] + 1, n + 1):
                nt = set(norm(titel[p]))
                if not nt:
                    continue
                if any(h and (set(h) <= nt or (len(nt) > 1 and nt <= set(h))) for h in heads[k]):
                    treffer = p
                    break
            grenzen.append(treffer or 0)
        zeilen = []
        for k, (t, pfad) in enumerate(kapitel):
            von = grenzen[k]
            bis = (grenzen[k + 1] - 1) if k + 1 < len(grenzen) and grenzen[k + 1] else n
            zeilen.append((pfad, t, von, bis, titel.get(von, "")))
        alles[nr] = zeilen
    return alles


def zeile_fuer(kapitelpfad, alles):
    """Die Markdown-Zeile für ein Kapitel (kann zwei Sitzungen nennen)."""
    teile = []
    for nr in sorted(alles):
        for pfad, _t, von, bis, _s in alles[nr]:
            if pfad == kapitelpfad and von:
                spanne = "S. %d" % von if von == bis else "S. %d–%d" % (von, bis)
                teile.append("[Folien VL %d, %s](%sfolien/vl%02d.pdf#page=%d)" % (nr, spanne, SITE, nr, von))
    return " · ".join(teile) if teile else None


def eintragen(pfad, zeile):
    """Die Zeile unter die `#`-Überschrift setzen -- hinter Aufzeichnung und Player,
    wenn es sie gibt, sonst direkt darunter. Idempotent über die Marke."""
    p = WURZEL / pfad
    s = p.read_text(encoding="utf-8")
    if MARKE in s:
        s = re.sub(r"^\[Folien VL .*$", zeile, s, count=1, flags=re.M)
        p.write_text(s, encoding="utf-8")
        return "aktualisiert"
    m = re.search(r"^# .+\n", s, re.M)
    if not m:
        return "keine Überschrift"
    rest = s[m.end():]
    # hinter dem Player-Block, falls vorhanden
    pl = re.match(r"\n\[Vorlesungsaufzeichnung[^\n]*\n\n:::\{anywidget\}[^\n]*\n[^\n]*\n:::\n", rest)
    stelle = m.end() + (pl.end() if pl else 0)
    rest = s[stelle:].lstrip("\n")
    s = s[:stelle] + "\n" + zeile + "\n\n" + rest
    p.write_text(s, encoding="utf-8")
    return "eingefügt"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--schreiben", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    alles = bereiche()
    if not alles:
        print("Keine Decks gebaut -- erst slides/build.sh laufen lassen.")
        return 1

    offen = []
    for nr in sorted(alles):
        for pfad, t, von, bis, start in alles[nr]:
            if not von:
                offen.append("VL %d: Grenze fuer '%s' nicht gefunden" % (nr, t))
            print("VL %2d  %-40s S. %3s-%-3s  ab Folie: %s"
                  % (nr, t[:40], von or "?", bis, start[:38]))

    kapitel = sorted({pfad for nr in alles for pfad, *_ in alles[nr]})
    print("-" * 78)
    for pfad in kapitel:
        z = zeile_fuer(pfad, alles)
        if not z:
            continue
        if args.schreiben:
            print("%-52s %s" % (pfad, eintragen(pfad, z)))
        else:
            vorhanden = MARKE in (WURZEL / pfad).read_text(encoding="utf-8")
            print("%-52s %s" % (pfad, "steht schon" if vorhanden else "neu"))
            print("    " + z)

    if args.check:
        fehlt = [p for p in kapitel if MARKE not in (WURZEL / p).read_text(encoding="utf-8")]
        if fehlt or offen:
            for f in fehlt:
                print("FEHLT: %s hat keine Folienzeile" % f)
            for o in offen:
                print("OFFEN: " + o)
            return 1
        print("Alle %d Kapitel mit Deck haben ihre Folienzeile." % len(kapitel))
    if offen:
        for o in offen:
            print("OFFEN: " + o)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
