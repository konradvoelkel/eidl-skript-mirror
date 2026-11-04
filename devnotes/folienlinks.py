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

**Verlinkt wird nur, was freigegeben ist.** `../slides/freigegeben.txt` sagt, welche Decks
veroeffentlicht werden duerfen; dieselbe Datei liest der `pages`-Job. Ein Deck, das dort
fehlt, wird gebaut (ein Fehler soll laut sein), aber nicht ausgeliefert -- und bekommt
deshalb auch keine Zeile im Kapitel. `--schreiben` nimmt eine Zeile wieder heraus, deren
Deck aus der Freigabe faellt.

Die Zuordnung Sitzung → Kapitel kommt aus der Tabelle in `../kurs-2026-27.md`, nicht aus
einer zweiten Liste. Ein Kapitel kann in zwei Sitzungen vorkommen (Backpropagation in VL 6
und VL 13, Anwendungsbeispiele in VL 14 und VL 15); dann nennt die Zeile beide.

**Ausnahme, solange der Plan den Decks voraus ist:** `DECK_STAND` unten. Ein Folienlink muss
auf das zeigen, was im Deck steht; ist eine Sitzung im Plan schon umgeschnitten und das Deck
noch nicht, gilt für sie die Liste dort. Jede Zeile verschwindet mit dem Umschnitt ihres
Decks, dann kommt wieder alles aus dem Plan.

Was `--check` prüft: dass jedes Kapitel der Tabelle eine Folienzeile hat, dass jede Grenze
gefunden wurde, **und dass die eingetragene Zeile noch zu den Bereichen passt**. Das Dritte
hat bis zum 2026-11-04 gefehlt – ein geänderter Plan hat die Links still falsch werden
lassen, und rot wurde nur die nicht gefundene Grenze.
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


def freigegeben():
    """Die Nummern der Decks, die veroeffentlicht und verlinkt werden duerfen.

    Steht in `../slides/freigegeben.txt`, eine Nummer je Zeile, `#` ist Kommentar.
    Dieselbe Datei liest der `pages`-Job; ein Deck, das dort fehlt, wird gebaut, aber
    nicht ausgeliefert -- und darf deshalb auch aus keinem Kapitel verlinkt sein, sonst
    zeigt der Link auf eine Adresse, die es nicht gibt.
    """
    datei = WURZEL / "slides" / "freigegeben.txt"
    if not datei.exists():
        raise SystemExit("slides/freigegeben.txt fehlt -- ohne sie ist unklar, "
                         "welche Decks veroeffentlicht sind.")
    nummern = set()
    for z in datei.read_text(encoding="utf-8").splitlines():
        z = z.split("#", 1)[0].strip()
        if z:
            nummern.add(int(z))
    return nummern
# **Vollstaendige Adresse, nicht `/folien/...`.** Eine absolute Pfadangabe funktioniert im
# HTML, wird aber im PDF-Export zu einem Link ohne Host und damit tot -- und das Skript
# wird gedruckt und als PDF weitergegeben. Dieselbe Entscheidung wie bei den
# Aufzeichnungslinks, die auch voll ausgeschrieben sind.
SITE = "https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de/"
# Erkannt wird die Zeile an ihrem Inhalt, nicht an einer Marke: mystmd laesst rohes
# HTML fallen oder gibt es escaped aus (am 2026-11-04 gemessen), ein
# `<!-- ... -->` koennte also als Text auf der Seite landen.
MARKE = "/folien/vl"

# Sitzungen, deren Deck noch nach dem **alten** Schnitt gebaut ist (Stand 2026-11-04).
# Der Plan in `../kurs-2026-27.md` ist den Decks voraus: VL 9 und VL 12 bis 14 sind dort am
# 2026-11-04 neu geschnitten worden (Graphen aus VL 9 nach VL 14, latente Raeume als Sitzung
# nach der Pause, Autograd und die Backprop-Induktion zusammen hinter die GANs), die Decks
# folgen erst -- Deck 9 vor dem 09.12., die anderen in der Weihnachtspause (offener Punkt in
# `TODO.md`, Abschnitt "Beamer-Folien").
#
# Bis dahin gilt fuer diese Sitzungen die Liste hier, denn ein Folienlink muss auf das zeigen,
# was im Deck **steht**, nicht auf das, was der Plan vorsieht. Sonst schickt das Kapitel
# "Latente Raeume geometrisch" den Leser auf Deck 12, wo Autograd steht.
#
# **Jede Zeile verschwindet mit dem Umschnitt ihres Decks.** Ist die Liste leer, kommt wieder
# alles aus dem Plan, so wie es gedacht ist.
DECK_STAND = {
    # VL 9 ist am 2026-11-04 gekürzt und steht wieder auf dem Plan: Die fünf Graphen-Rahmen
    # liegen auf `../slides/parkplatz-vl14-graphen.tex`, bis Deck 14 umgeschnitten wird.
    12: ["part-lernen/10-autograd-berechnungsgraph.md",
         "part-architekturen-anwendungen/23-llms-benutzen.md"],
    13: ["part-architekturen-anwendungen/22-gans.md",
         "part-lernen/09-backpropagation.md"],
    14: ["part-representation-learning/17-latente-raeume-geometrisch.md",
         "part-architekturen-anwendungen/24-anwendungsbeispiele.md"],
}

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


def kapiteltitel(pfad):
    """Der Titel aus dem Frontmatter -- fuer DECK_STAND, damit dort nur Pfade stehen."""
    s = (WURZEL / pfad).read_text(encoding="utf-8")
    m = re.search(r'^title: "?(.+?)"?$', s, re.M)
    return m.group(1) if m else pathlib.Path(pfad).stem


def kurs_plan():
    s = (WURZEL / "kurs-2026-27.md").read_text(encoding="utf-8")
    plan = {}
    for z in s.splitlines():
        if re.match(r"^\| *\d+ *\|", z):
            sp = [x.strip() for x in z.strip("|").split("|")]
            plan[int(sp[0])] = re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", sp[1])
    for nr in sorted(DECK_STAND):
        plan[nr] = [(kapiteltitel(pf), pf) for pf in DECK_STAND[nr]]
        print("Hinweis: Deck VL %d ist noch nach dem alten Schnitt gebaut, "
              "Bereiche aus DECK_STAND statt aus dem Plan." % nr)
    return plan


def bereiche():
    """Je Sitzung: [(Kapitelpfad, Kapiteltitel, von, bis, Titel der Startfolie)]."""
    plan, alles = kurs_plan(), {}
    frei = freigegeben()
    for nr, kapitel in sorted(plan.items()):
        if nr not in frei:
            continue   # nicht freigegeben: kein Link, siehe slides/freigegeben.txt
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


def entfernen(pfad):
    """Die Folienzeile samt Leerzeile herausnehmen -- für ein Kapitel, das in keiner
    Sitzung mehr vorkommt, weil sein Stoff aus dem Deck ausgezogen ist."""
    p = WURZEL / pfad
    s = p.read_text(encoding="utf-8")
    neu = re.sub(r"^\[Folien VL .*\n\n?", "", s, count=1, flags=re.M)
    if neu == s:
        return "nichts zu entfernen"
    p.write_text(neu, encoding="utf-8")
    return "entfernt"


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

    # Ueber *alle* Kapitel, nicht nur ueber die der Sitzungen: Ein Kapitel, dessen Stoff aus
    # einem Deck ausgezogen ist, kommt in keiner Sitzung mehr vor und behielte sonst still
    # seine alte Zeile -- einen Link auf Folien, die es nicht mehr gibt (2026-11-04, Graphen).
    kapitel = sorted(
        pf.relative_to(WURZEL).as_posix()
        for teil in ("part-grundlagen", "part-lernen", "part-representation-learning",
                     "part-architekturen-anwendungen")
        for pf in (WURZEL / teil).glob("*.md")
    )
    print("-" * 78)
    for pfad in kapitel:
        z = zeile_fuer(pfad, alles)
        vorhanden = MARKE in (WURZEL / pfad).read_text(encoding="utf-8")
        if not z and not vorhanden:
            continue
        if args.schreiben:
            print("%-52s %s" % (pfad, eintragen(pfad, z) if z else entfernen(pfad)))
        elif not z:
            print("%-52s %s" % (pfad, "Zeile übrig, gehört zu keiner Sitzung"))
        else:
            print("%-52s %s" % (pfad, "steht schon" if vorhanden else "neu"))
            print("    " + z)

    if args.check:
        # Drei Fragen, und die dritte ist die, die am 2026-11-04 gefehlt hat: Bis dahin
        # pruefte --check nur, *dass* eine Folienzeile da ist und dass jede Grenze gefunden
        # wurde -- nicht, ob die Zeile im Kapitel noch zu den Bereichen passt. Ein
        # umgeschnittenes Deck oder ein geaenderter Plan hat die Links also still falsch
        # werden lassen.
        fehlt, falsch, uebrig = [], [], []
        for pf in kapitel:
            s = (WURZEL / pf).read_text(encoding="utf-8")
            soll_da = zeile_fuer(pf, alles) is not None
            if MARKE not in s:
                if soll_da:
                    fehlt.append(pf)
                continue
            if not soll_da:
                uebrig.append(pf)
                continue
            ist = re.search(r"^\[Folien VL .*$", s, re.M)
            soll = zeile_fuer(pf, alles)
            if ist and soll and ist.group(0) != soll:
                falsch.append((pf, ist.group(0), soll))
        if fehlt or falsch or uebrig or offen:
            for f in fehlt:
                print("FEHLT: %s hat keine Folienzeile" % f)
            for u in uebrig:
                print("ÜBRIG: %s hat eine Folienzeile, kommt aber in keiner Sitzung vor" % u)
            for pf, ist, soll in falsch:
                print("FALSCH: %s" % pf)
                print("    steht: " + ist)
                print("    soll:  " + soll)
            for o in offen:
                print("OFFEN: " + o)
            print("\nMit `--schreiben` eintragen. Zeigt eine Zeile auf ein Deck, das den Stoff"
                  " gar nicht enthaelt,\ngehoert die Sitzung nach DECK_STAND, nicht in die Links.")
            return 1
        print("Alle %d Kapitel mit Deck haben ihre Folienzeile." % len(kapitel))
    if offen:
        for o in offen:
            print("OFFEN: " + o)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
