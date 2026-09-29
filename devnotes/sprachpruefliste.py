#!/usr/bin/env python3
"""Atome für den Sprachdurchgang: Typografie, Satzlänge, Rechtschreibung.

Das Gegenstück zu `pruefliste_durchsicht.py`, nur für die andere Achse. Die fachliche
Durchsicht hat gefragt „stimmt es?“; dieses Skript fragt „steht es richtig da?“ und
liefert die *prüfbaren* Atome — es urteilt nicht, es zählt und listet mit Fundort.

    uv run devnotes/sprachpruefliste.py --uebersicht
    uv run devnotes/sprachpruefliste.py 06 --out <scratchpad>/sprache-06.md
    uv run devnotes/sprachpruefliste.py --alle --out <scratchpad>/sprache-alle.md
    uv run devnotes/sprachpruefliste.py --woerter        # nur die Rechtschreibliste

**Ausgabe in den Scratchpad, nicht ins Repo** — wie beim Prüflistenskript.

Was geprüft wird und was nicht
------------------------------
Geprüft wird nur **Prosa**: Codeblöcke, Inline-Code, Mathematik (`$…$` und `$$…$$`),
Directive-Zeilen (`:::{…}`, `:width:`), URLs und HTML-Kommentare werden vorher
herausgenommen und durch einen Platzhalter ersetzt. Ohne das ertrinkt jede Prüfung in
Falschmeldungen — das Buch besteht zu einem Fünftel aus Formeln und Code.

Die Rechtschreibprüfung läuft in vier Stufen, weil `aspell` allein auf deutschem
Fachtext unbrauchbar ist (1711 Treffer beim ersten Lauf, fast alle richtig):

1. `aspell --lang=de_DE-neu --run-together` (deutsche Komposita)
2. eigene Kompositum-Zerlegung: Wort in zwei bekannte Teile trennbar (mit Fugen-s)?
3. Filter gegen `aspell --lang=en_US` — das Buch zitiert englische Abstracts wörtlich
4. Filter gegen `devnotes/sprachpruefliste-woerter.txt`, die Projektwortliste

Nach Stufe 3 blieben am 2026-09-29 noch 494 verschiedene Wörter übrig; die Wortliste
ist dafür da, diese Zahl über die Durchgänge hinweg zu senken. **Ein Wort kommt erst in
die Liste, wenn jemand es angesehen hat.**
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
WORTLISTE = Path(__file__).resolve().parent / "sprachpruefliste-woerter.txt"
PLATZ = ""  # Platzhalter für Code/Mathe: ein Wortzeichen, erzeugt keine Lücken

# Lateinische Buchstaben mit Diakritika gehören ins Wortmuster: sonst zerfällt ein
# zitierter Name wie „Buciluă“ in „Bucilu“ und „Řehůřeks“ in „eks“ — beides Wörter,
# die es im Buch nicht gibt, die aber jede Rechtschreibliste anführen. Ausgenommen
# sind U+00D7 (×) und U+00F7 (÷), die in den Bereichen liegen, aber keine Buchstaben sind.
WORTZEICHEN = "A-Za-z\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u024f"

LANGER_SATZ = 35  # Wörter; darüber wird gelistet, nicht bewertet


# --------------------------------------------------------------------------- Dateien
def kapitel_dateien() -> list[Path]:
    """Alle Buchdateien in der Reihenfolge des Inhaltsverzeichnisses."""
    dateien = sorted(
        p for teil in ("part-grundlagen", "part-lernen",
                       "part-representation-learning", "part-architekturen-anwendungen")
        for p in (WURZEL / teil).glob("*.md")
    )
    return dateien + [WURZEL / "glossar.md", WURZEL / "index.md"]


def waehle(muster: str | None) -> list[Path]:
    if muster is None:
        return kapitel_dateien()
    treffer = [p for p in kapitel_dateien() if p.name.startswith(muster)]
    if not treffer:
        sys.exit(f"Kein Kapitel zu „{muster}“ — erwartet z.B. 06 oder glossar.")
    return treffer


# ----------------------------------------------------------------------------- Prosa
def ist_adresse(text: str) -> bool:
    """Ist dieser Linktext selbst eine Adresse oder ein Dateiname, keine Prosa?"""
    t = text.strip()
    if not t or " " in t:
        return False
    return bool(re.match(r"(?i)^(https?://|www\.)", t)
                or re.match(r"(?i)^[\w~.-]+\.[a-z]{2,}(/|$)", t))


def prosa_zeilen(text: str) -> list[str]:
    """Zeilenweise Prosa; Code, Mathe und Directives werden zu Platzhaltern.

    Zeilenweise, damit jeder Befund eine Zeilennummer behält. Mehrzeilige Blöcke
    (```…``` und $$…$$) werden über einen Zustandsautomaten erkannt.
    """
    zeilen = text.split("\n")
    raus: list[str] = []
    in_code = in_mathe = False
    in_front = zeilen[:1] == ["---"]
    for i, z in enumerate(zeilen):
        if in_front:
            raus.append("")
            if i > 0 and z.strip() == "---":
                in_front = False
            continue
        if z.lstrip().startswith("```"):
            in_code = not in_code
            raus.append("")
            continue
        if in_code:
            raus.append("")
            continue
        if z.strip() == "$$":
            in_mathe = not in_mathe
            raus.append("")
            continue
        if in_mathe:
            raus.append("")
            continue
        s = z
        s = re.sub(r"^:::+\{[^}]*\}.*$", "", s)      # :::{admonition} …
        s = re.sub(r"^:::+\s*$", "", s)              # schließendes :::
        s = re.sub(r"^:[a-z-]+:.*$", "", s)          # :width:, :class: …
        s = re.sub(r"<!--.*?-->", " ", s)
        s = re.sub(r"\$\$.*?\$\$", PLATZ, s)         # einzeiliges $$…$$
        s = re.sub(r"(?<!\$)\$[^$]+\$(?!\$)", PLATZ, s)
        s = re.sub(r"`[^`]+`", PLATZ, s)
        # Linktext behalten, Ziel weg — aber ein Linktext, der selbst eine Adresse ist
        # („[web.stanford.edu/~jurafsky/slp3/](…)“), wird Platzhalter. Sonst überlebt er
        # die URL-Regel darunter (die braucht ein Schema) und zerfällt in „web“,
        # „stanford“, „edu“, „jurafsky“ — Treffer, die keine Prosa sind.
        s = re.sub(r"\[([^\]]*)\]\([^)]*\)",
                   lambda m: PLATZ if ist_adresse(m.group(1)) else m.group(1), s)
        s = re.sub(r"https?://\S+", PLATZ, s)
        raus.append(s)
    return raus


def saetze(zeilen: list[str]) -> list[tuple[int, str]]:
    """(Zeilennummer, Satz). Absätze werden zusammengezogen, Listenpunkte einzeln."""
    ergebnis: list[tuple[int, str]] = []
    puffer, start = [], 0
    def leeren() -> None:
        if not puffer:
            return
        text = " ".join(puffer)
        for m in re.finditer(r"[^.!?]+(?:[.!?]+|$)", text):
            s = m.group(0).strip()
            if s:
                ergebnis.append((start, s))
        puffer.clear()
    for nr, z in enumerate(zeilen, 1):
        if not z.strip() or re.match(r"^\s*#", z):
            leeren()
            continue
        if not puffer:
            start = nr
        puffer.append(z.strip())
    leeren()
    return ergebnis


# ------------------------------------------------------------------------- Typografie
PRUEFUNGEN = [
    ("gerades Anführungszeichen (deutsch sind „ und “)", r'"'),
    ("Geviertstrich — (im Buch sonst der Halbgeviertstrich –)", r"—"),
    ("Bindestrich zwischen Leerzeichen (als Gedankenstrich gehört – hin)", r"(?<= )-(?= )"),
    ("doppeltes Leerzeichen", r"(?<=\S)  +(?=\S)"),
    ("Leerzeichen vor Satzzeichen", r" [,.;:!?](?=\s|$)"),
    ("drei Punkte als … statt ...", r"\.\.\."),
    # „die die“ und „das das“ sind in deutschen Relativsätzen richtig — deshalb
    # nur Wörter ab drei Zeichen, die keine Artikel/Relativpronomen sind.
    ("Wortdoppelung", r"\b(?!die|das|der|den|dem|und|ist|sie)(\w{3,})\s+\1\b"),
    ("Mehrfaches Ausrufe- oder Fragezeichen", r"[!?]{2,}"),
]

ABKUERZUNGEN = [r"z\.\s?B\.", r"d\.\s?h\.", r"u\.\s?a\.", r"i\.\s?d\.\s?R\.",
                r"bzw\.", r"vgl\.", r"ggf\.", r"etc\.", r"usw\."]


def typografie(zeilen: list[str]) -> list[tuple[str, int, str]]:
    funde = []
    for name, muster in PRUEFUNGEN:
        for nr, z in enumerate(zeilen, 1):
            # Tabellenzeilen haben ihre eigene Zeichensetzung: „| · | ? |“ ist kein
            # Leerzeichen vor einem Satzzeichen, sondern eine leere Zelle.
            if z.lstrip().startswith("|") and "Satzzeichen" in name:
                continue
            for m in re.finditer(muster, z):
                a, b = max(0, m.start() - 30), min(len(z), m.end() + 30)
                funde.append((name, nr, z[a:b].replace(PLATZ, "·").strip()))
    return funde


def abkuerzungen(zeilen: list[str]) -> Counter:
    text = "\n".join(zeilen)
    return Counter(
        m.group(0) for muster in ABKUERZUNGEN for m in re.finditer(muster, text)
    )


# ---------------------------------------------------------------- Rechtschreibung
def aspell(woerter: list[str], sprache: str, komposita: bool = False) -> set[str]:
    """Die Teilmenge von `woerter`, die aspell NICHT kennt."""
    if not woerter:
        return set()
    befehl = ["aspell", f"--lang={sprache}", "--encoding=utf-8"]
    if komposita:
        befehl += ["--run-together", "--run-together-limit=3", "--run-together-min=3"]
    befehl.append("list")
    try:
        p = subprocess.run(befehl, input="\n".join(woerter),
                           capture_output=True, text=True, check=True)
    except FileNotFoundError:
        sys.exit("aspell fehlt. Debian/Ubuntu: apt install aspell aspell-de")
    except subprocess.CalledProcessError as e:
        sys.exit(f"aspell scheiterte: {e.stderr.strip()}")
    return set(p.stdout.split())


def projektwortliste() -> set[str]:
    if not WORTLISTE.exists():
        return set()
    return {
        z.split("#")[0].strip()
        for z in WORTLISTE.read_text(encoding="utf-8").splitlines()
        if z.split("#")[0].strip()
    }


def zerlegbar(wort: str, bekannt: set[str]) -> bool:
    """Deutsches Kompositum aus zwei bekannten Teilen, mit oder ohne Fugen-s?"""
    for i in range(4, len(wort) - 3):
        kopf, rumpf = wort[:i], wort[i:]
        if kopf.capitalize() not in bekannt and kopf not in bekannt:
            continue
        kandidaten = [rumpf, rumpf.capitalize()]
        if rumpf[:1] == "s":
            kandidaten += [rumpf[1:], rumpf[1:].capitalize()]
        if any(k in bekannt for k in kandidaten if k):
            return True
    return False


def rechtschreibung(zeilen_je_datei: dict[str, list[str]]) -> dict[str, list[tuple[str, int]]]:
    """{Wort: [(Datei, Zeile), …]} für alles, was nach vier Stufen übrig bleibt."""
    vorkommen: dict[str, list[tuple[str, int]]] = {}
    for name, zeilen in zeilen_je_datei.items():
        for nr, z in enumerate(zeilen, 1):
            # Ohne Bindestrich im Muster: aspell trennt „ASML-Aktienkurs“ ebenfalls in
            # zwei Token, und beide Seiten müssen dieselben Wörter sehen.
            # „$i$-te Komponente“: eine kleingeschriebene Endung direkt hinter Mathe
            # oder Code ist eine Flexionsendung am Symbol, kein eigenes Wort.
            z = re.sub(PLATZ + r"-[a-zäöüß]+", PLATZ, z)
            for m in re.finditer(f"[{WORTZEICHEN}]+", z.replace(PLATZ, " ")):
                vorkommen.setdefault(m.group(0), []).append((name, nr))
    woerter = sorted(vorkommen)

    unbekannt = aspell(woerter, "de_DE-neu", komposita=True)
    if not unbekannt:
        return {}

    # Stufe 2: Kompositum-Zerlegung. Erst alle denkbaren Teile sammeln, dann in EINEM
    # aspell-Lauf prüfen — sonst dauert es Minuten statt Sekunden.
    teile: set[str] = set()
    for w in unbekannt:
        for i in range(4, len(w) - 3):
            teile.update({w[:i], w[:i].capitalize(), w[i:], w[i:].capitalize()})
            if w[i:i + 1] == "s":
                teile.update({w[i + 1:], w[i + 1:].capitalize()})
    teile = {t for t in teile if len(t) >= 4}
    bekannte_teile = teile - aspell(sorted(teile), "de_DE-neu")
    unbekannt = {w for w in unbekannt if not zerlegbar(w, bekannte_teile)}

    # Stufe 3: englische Wörter (das Buch zitiert Abstracts wörtlich)
    unbekannt &= aspell(sorted(unbekannt), "en_US")

    # Stufe 4: Projektwortliste
    unbekannt -= projektwortliste()

    return {w: vorkommen[w] for w in sorted(unbekannt) if w in vorkommen}


# ----------------------------------------------------------------------- Ausgabe
def kapitelbericht(pfad: Path) -> str:
    text = pfad.read_text(encoding="utf-8")
    zeilen = prosa_zeilen(text)
    sz = saetze(zeilen)
    woerter = sum(len(s.split()) for _, s in sz)
    lang = sorted(((len(s.split()), nr, s) for nr, s in sz), reverse=True)
    lang = [x for x in lang if x[0] >= LANGER_SATZ]
    typ = typografie(zeilen)
    abk = abkuerzungen(zeilen)
    rs = rechtschreibung({pfad.name: zeilen})

    rel = pfad.relative_to(WURZEL)
    aus = [f"\n## {rel}\n",
           f"{woerter} Wörter Prosa · {len(sz)} Sätze · "
           f"{len(typ)} Typografie-Treffer · {len(lang)} lange Sätze · "
           f"{len(rs)} Wörter für die Rechtschreibliste\n"]

    if typ:
        aus.append(f"\n### Typografie ({len(typ)})\n")
        for name in dict.fromkeys(n for n, _, _ in typ):
            treffer = [(nr, k) for n, nr, k in typ if n == name]
            aus.append(f"\n**{name}** ({len(treffer)})\n")
            for nr, k in treffer[:25]:
                aus.append(f"- [ ] Z. {nr}: …{k}…")
            if len(treffer) > 25:
                aus.append(f"- … und {len(treffer) - 25} weitere")

    if abk:
        aus.append("\n### Abkürzungen — auf *Einheitlichkeit* prüfen, nicht auf Richtigkeit\n")
        for a, n in sorted(abk.items()):
            aus.append(f"- {a} — {n}×")

    if lang:
        aus.append(f"\n### Sätze ab {LANGER_SATZ} Wörtern ({len(lang)})\n")
        aus.append("Lang ist kein Fehler. Aber jeder dieser Sätze ist einmal zu lesen mit "
                   "der Frage, ob er noch trägt.\n")
        for n, nr, s in lang[:20]:
            aus.append(f"- [ ] Z. {nr} ({n} Wörter): {s[:110].replace(PLATZ, '·')}…")
        if len(lang) > 20:
            aus.append(f"- … und {len(lang) - 20} weitere")

    if rs:
        aus.append(f"\n### Rechtschreibung: unbekannte Wörter ({len(rs)})\n")
        aus.append("Richtig? Dann in `devnotes/sprachpruefliste-woerter.txt`. "
                   "Falsch? Dann ein Befund.\n")
        for w, orte in rs.items():
            o = ", ".join(f"Z. {nr}" for _, nr in orte[:4])
            mehr = f" (+{len(orte) - 4})" if len(orte) > 4 else ""
            aus.append(f"- [ ] `{w}` — {o}{mehr}")
    return "\n".join(aus)


def uebersicht(dateien: list[Path]) -> str:
    kopf = ("| Datei | Wörter | Sätze | Typografie | lange Sätze | RS-Wörter |\n"
            "|---|---|---|---|---|---|")
    zeilen_aus = [kopf]
    summe = [0, 0, 0, 0]
    alle_zeilen = {}
    for p in dateien:
        z = prosa_zeilen(p.read_text(encoding="utf-8"))
        alle_zeilen[p.name] = z
        sz = saetze(z)
        w = sum(len(s.split()) for _, s in sz)
        t = len(typografie(z))
        l = sum(1 for _, s in sz if len(s.split()) >= LANGER_SATZ)
        zeilen_aus.append(f"| {p.name} | {w} | {len(sz)} | {t} | {l} | |")
        summe = [summe[0] + w, summe[1] + len(sz), summe[2] + t, summe[3] + l]
    rs = rechtschreibung(alle_zeilen)
    zeilen_aus.append(f"| **{len(dateien)} Dateien** | **{summe[0]}** | **{summe[1]}** | "
                      f"**{summe[2]}** | **{summe[3]}** | **{len(rs)}** |")
    zeilen_aus.append("\nDie Spalte RS-Wörter ist *gemeinsam* über alle Dateien gezählt "
                      "(ein Wort, das in fünf Kapiteln steht, ist ein Eintrag).")
    return "\n".join(zeilen_aus)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kapitel", nargs="?", help="Präfix, z.B. 06 oder glossar")
    ap.add_argument("--alle", action="store_true", help="alle Dateien einzeln")
    ap.add_argument("--uebersicht", action="store_true", help="nur die Tabelle")
    ap.add_argument("--woerter", action="store_true",
                    help="nur die Rechtschreibliste über das ganze Buch")
    ap.add_argument("--out", type=Path, help="Zieldatei (sonst nach stdout)")
    a = ap.parse_args()

    dateien = waehle(a.kapitel) if a.kapitel else kapitel_dateien()

    if a.uebersicht:
        text = uebersicht(dateien)
    elif a.woerter:
        rs = rechtschreibung({p.name: prosa_zeilen(p.read_text(encoding="utf-8"))
                              for p in dateien})
        text = "\n".join(
            f"{w}\t{', '.join(f'{d}:{nr}' for d, nr in orte[:3])}"
            f"{' (+%d)' % (len(orte) - 3) if len(orte) > 3 else ''}"
            for w, orte in rs.items()) or "(keine unbekannten Wörter)"
        text = f"# {len(rs)} unbekannte Wörter\n\n" + text
    else:
        text = uebersicht(dateien) + "\n" + "\n".join(kapitelbericht(p) for p in dateien)

    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(text + "\n", encoding="utf-8")
        print(f"{a.out} geschrieben ({len(dateien)} Datei(en)).")
    else:
        print(text)


if __name__ == "__main__":
    main()
