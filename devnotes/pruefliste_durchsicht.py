#!/usr/bin/env python3
"""Erzeugt die Prüfliste für die fachliche Durchsicht: die Atome, die nachzurechnen sind.

Alle anderen Prüfer in `devnotes/` prüfen alles **außer** dem Inhalt — `check_pdf_build.py`
den PDF-Lauf, `check_doku.py` die Doku, `check_ci_yaml.py` die CI. Eine fachliche Durchsicht
kann niemand automatisch prüfen; sie hat deshalb kein natürliches Ende und keinen Prüfer, der
rot wird. Was sich automatisieren lässt, ist die **Zählbarkeit**: hinterher muss
unterscheidbar sein, was nachgerechnet und was nur gelesen wurde.

Dieses Skript liest die Kapitel und zählt heraus, was eine prüfbare Behauptung ist:

* **Formelblöcke** (`$$ … $$`), numeriert und mit Vorschau — die Liste, die beim Nachrechnen
  abgehakt wird. 126 Stück im Buch, davon 60 in den Kapiteln 06, 08 und 09. (Wer `$$`-Zeilen
  zählt statt Blöcke, kommt auf das Doppelte.)
* **Zeilen mit einer interessanten Zahl** — Dezimalzahlen, Exponenten, Prozente, Jahre,
  Zahlen mit Einheit. Nackte kleine Ganzzahlen („Kapitel 3“, Tabellenspalten) bleiben
  draußen, sonst ist die Liste unbenutzbar.
* **Zeilen mit Bibliotheks- oder Versionsangabe** — die altern von selbst, und laut
  `CLAUDE.md` werden sie geprüft statt erinnert.
* **Jahreszahlen** getrennt von den übrigen Zahlen — die Kurzgeschichte in Kapitel 01
  besteht fast nur daraus, und ein falsches Jahr ist ein Befund wie ein falsches Vorzeichen.
* **Quellenangaben** (Jahr in Klammern, arXiv, DOI, die Begleitbücher UDL und MML).
* **Links**, intern und extern (Status prüft `check_links.py`, nicht dieses Skript).
* **Antwortproben** der Übungsabschnitte — jede ist eine nachrechenbare Behauptung.
* **Boxen** (`Vertiefung:`, `Weiterlesen`, Merkboxen) mit ihrer Klasse; `dropdown` wirkt im
  PDF nicht, offene Antworten fallen hier auf.

Die Reihenfolge ist die **Vorlesungsreihenfolge**, nicht die Dateireihenfolge: die Zuordnung
Kapitel zu VL wird aus der Wochentabelle in `kurs-2026-27.md` gelesen, damit sie nicht in
einer zweiten Fassung veraltet. Kapitel 10 (Autograd) gehört zu VL 12, nicht zu VL 10.

Aufruf:

    uv run devnotes/pruefliste_durchsicht.py                  # Übersicht und Prüfliste
    uv run devnotes/pruefliste_durchsicht.py --uebersicht     # nur die Fortschrittstabelle
    uv run devnotes/pruefliste_durchsicht.py 06 08 09         # nur diese Kapitel
    uv run devnotes/pruefliste_durchsicht.py 06 --out /tmp/kap06.md

Das Skript liest nur und schreibt nichts ins Repo. Seine Ausgabe ist ein Arbeitszettel, kein
Dokument: sie gehört in den Scratchpad, nicht in `devnotes/`. Was dabei gefunden wird, gehört
in `devnotes/durchsicht-2026-10.md`.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
TEILE = (
    "part-grundlagen",
    "part-lernen",
    "part-representation-learning",
    "part-architekturen-anwendungen",
)

# Zahlen, die eine Behauptung tragen. Nackte Ganzzahlen fehlen absichtlich („Kapitel 3“,
# Tabellenspalten) — sonst ist die Liste so lang, dass sie niemand abhakt.
ZAHL = re.compile(
    r"""\d+\{,\}\d+                      # 0{,}05 — deutsche Dezimalzahl in Mathe
      | \d+[.,]\d+                       # 0.05, 3,14
      | \b\d+\s?e\s?-?\d+\b              # 1e-3
      | \b\d+\s?%                        # 30 %
      | \b\d+\s?(?:Mal|mal|Bit|Byte|kB|MB|GB|TB|Pixel|Kanäle|Kanal|Neuronen|Schichten
                 |Dimensionen|Parameter|Sekunden|Minuten|Stunden|Epochen|Stellen|Klassen)\b
    """,
    re.X,
)
# Jahreszahlen stehen in einem eigenen Eimer: in Kapitel 01 ist die Kurzgeschichte des Feldes
# fast nichts anderes, und ein falsches Jahr ist ein Befund wie ein falsches Vorzeichen.
JAHR = re.compile(r"\b(?:1[89]|20)\d{2}\b")
BIBLIOTHEK_NAMEN = (
    "torch", "pytorch", "numpy", "scipy", "sklearn", "scikit-learn", "transformers",
    "gensim", "matplotlib", "tensorflow", "keras", "ollama", "nltk", "networkx",
    "torchvision", "pandas", "huggingface", "cuda", "rocm", "mps", "onnx",
)
VERSION = re.compile(r"\b\d+\.\d+(?:\.\d+)?\b")
# Quellenangabe: Jahr in Klammern, arXiv/DOI, oder die beiden Begleitbücher. Kursive
# Werktitel werden **nicht** gesucht — `**fett**` sieht für jede Kursiv-Regex wie `*kursiv*`
# aus, und dann steht der halbe Kapiteltext in der Liste.
QUELLE = re.compile(
    r"\((?:1[89]|20)\d{2}\)|arxiv\.org|doi\.org|\*UDL\*|\*MML\*|Prince|Deisenroth"
)
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)|<(https?://[^>\s]+)>")
BOX = re.compile(r"^:{3,}\{admonition\}\s*(.+)$")
KLASSE = re.compile(r"^:class:\s*(.+)$")


def zeilen_mit_art(text: str) -> list[tuple[int, str, str]]:
    """Jede Zeile mit ihrer Art: frontmatter, fence, math oder prosa.

    Ohne diese Trennung zählt man Zahlen aus Codeblöcken mit und übersieht, dass ein
    `$$`-Block über mehrere Zeilen geht.
    """
    art: list[tuple[int, str, str]] = []
    in_front = False
    in_fence = False
    in_math = False
    for nr, zeile in enumerate(text.splitlines(), start=1):
        blank = zeile.strip()
        if nr == 1 and blank == "---":
            in_front = True
            art.append((nr, "frontmatter", zeile))
            continue
        if in_front:
            art.append((nr, "frontmatter", zeile))
            if blank == "---":
                in_front = False
            continue
        if blank.startswith("```"):
            in_fence = not in_fence
            art.append((nr, "fence", zeile))
            continue
        if in_fence:
            art.append((nr, "fence", zeile))
            continue
        if blank == "$$":
            in_math = not in_math
            art.append((nr, "math", zeile))
            continue
        art.append((nr, "math" if in_math else "prosa", zeile))
    return art


def kuerzen(s: str, n: int = 78) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


class Kapitel:
    def __init__(self, pfad: Path, vl: str) -> None:
        self.pfad = pfad
        self.vl = vl
        self.text = pfad.read_text(encoding="utf-8")
        self.zeilen = zeilen_mit_art(self.text)
        m = re.search(r'^title:\s*"?(.*?)"?\s*$', self.text, re.M)
        self.titel = m.group(1) if m else pfad.stem
        self.nummer = pfad.stem.split("-", 1)[0]
        self.woerter = len(self.text.split())
        self._sammeln()

    def _sammeln(self) -> None:
        self.formeln: list[tuple[int, str]] = []
        self.zahlen: list[tuple[int, str]] = []
        self.jahre: list[tuple[int, str]] = []
        self.bibliothek: list[tuple[int, str]] = []
        self.quellen: list[tuple[int, str]] = []
        self.links: list[tuple[int, str]] = []
        self.antwortproben: list[tuple[int, str]] = []
        self.boxen: list[tuple[int, str, str]] = []
        self.codebloecke: list[tuple[int, str]] = []

        offen: int | None = None
        inhalt: list[str] = []
        for nr, art, zeile in self.zeilen:
            blank = zeile.strip()
            if art == "math":
                if blank == "$$":
                    if offen is None:
                        offen, inhalt = nr, []
                    else:
                        vorschau = next((z for z in inhalt if z.strip()), "")
                        self.formeln.append((offen, kuerzen(vorschau)))
                        offen = None
                else:
                    inhalt.append(zeile)
                continue
            if art == "fence":
                if blank.startswith("```") and len(blank) > 3:
                    self.codebloecke.append((nr, blank.lstrip("`")))
                continue
            if art == "frontmatter":
                continue

            ueberschrift = blank.startswith("#")
            if ZAHL.search(zeile) and not ueberschrift:
                self.zahlen.append((nr, kuerzen(zeile)))
            if JAHR.search(zeile) and not ueberschrift:
                self.jahre.append((nr, kuerzen(zeile)))
            low = zeile.lower()
            if any(n in low for n in BIBLIOTHEK_NAMEN) or VERSION.search(zeile):
                self.bibliothek.append((nr, kuerzen(zeile)))
            if QUELLE.search(zeile) and not ueberschrift:
                self.quellen.append((nr, kuerzen(zeile)))
            for treffer in LINK.finditer(zeile):
                self.links.append((nr, treffer.group(1) or treffer.group(2)))
            if blank.startswith("*Antwortprobe"):
                self.antwortproben.append((nr, kuerzen(blank, 110)))
            m = BOX.match(blank)
            if m:
                self.boxen.append((nr, m.group(1), ""))
            m = KLASSE.match(blank)
            if m and self.boxen:
                nr0, name, _ = self.boxen[-1]
                self.boxen[-1] = (nr0, name, m.group(1))

        self.hat_uebung = "\n## Übung\n" in self.text

    # ── Ausgabe ────────────────────────────────────────────────────────────────
    def pruefliste(self) -> str:
        rel = self.pfad.relative_to(WURZEL)
        z: list[str] = [
            f"## Kap. {self.nummer} — {self.titel}",
            "",
            f"`{rel}` · VL {self.vl} · {self.woerter} Wörter · "
            f"{len(self.formeln)} Formeln · {len(self.codebloecke)} Codeblöcke",
            "",
            "Achsen: **A1** stimmt es (nachrechnen, nicht nachlesen) · "
            "**A2** passt es zu Plan, Folien, Klausur · **A3** trägt es beim Lesen.",
            "",
        ]

        def block(titel: str, eintraege: list[str]) -> None:
            if not eintraege:
                return
            z.append(f"### {titel} ({len(eintraege)})")
            z.append("")
            z.extend(eintraege)
            z.append("")

        block(
            "A1 Formeln — nachgerechnet oder offen, nichts dazwischen",
            [f"- [ ] F{i} (Z. {nr}) `{v}`" for i, (nr, v) in enumerate(self.formeln, 1)],
        )
        block("A1 Zahlen", [f"- [ ] Z. {nr}: {v}" for nr, v in self.zahlen])
        block(
            "A1 Bibliothek und Versionen — prüfen statt erinnern",
            [f"- [ ] Z. {nr}: {v}" for nr, v in self.bibliothek],
        )
        block("A1 Jahre und historische Angaben", [f"- [ ] Z. {nr}: {v}" for nr, v in self.jahre])
        block("A1 Quellenangaben — Jahr und Wortlaut", [f"- [ ] Z. {nr}: {v}" for nr, v in self.quellen])
        block(
            "A1/A3 Antwortproben — jede einmal durchrechnen",
            [f"- [ ] Z. {nr}: {v}" for nr, v in self.antwortproben],
        )
        block(
            "A2/A3 Boxen — `dropdown` versteckt im PDF nichts",
            [f"- [ ] Z. {nr}: {name} (`{kl or 'ohne :class:'}`)" for nr, name, kl in self.boxen],
        )
        block("Links (Status prüft `check_links.py`)", [f"- Z. {nr}: {t}" for nr, t in self.links])
        z.append("### A2 Abgleich")
        z.append("")
        z.append(
            f"- [ ] gegen `kurs-2026-27.md`, Zeile für VL {self.vl} (Umfang, „kein Vorgriff auf …“)"
        )
        z.append("- [ ] gegen die Folien dieser VL in `slides/` und gegen `devnotes/klausur-abdeckung.md`")
        z.append("- [ ] gegen die Aufzeichnung in `transcripts/` (Divergenz ist ein Befund, kein Fehler)")
        z.append("")
        z.append("### A3 Lesen")
        z.append("")
        z.append("- [ ] Begriff benutzt, bevor er definiert ist?")
        z.append("- [ ] Notation wie in den Vorkapiteln (Symbolinventar im Befundbogen)?")
        z.append("- [ ] Querverweise führen dorthin, wo das Gesagte steht?")
        if self.hat_uebung:
            z.append("- [ ] Übung: in fünf bis fünfzehn Minuten mit Papier zu schaffen, Tipp trägt?")
        else:
            z.append("- [ ] kein Übungsabschnitt — absichtlich (04, 17, 21, 22) oder vergessen?")
        z.append("")
        return "\n".join(z)


def vl_zuordnung() -> dict[str, str]:
    """Kapitel zu VL-Nummer, gelesen aus der Wochentabelle in `kurs-2026-27.md`."""
    plan = (WURZEL / "kurs-2026-27.md").read_text(encoding="utf-8")
    zu: dict[str, list[str]] = {}
    for zeile in plan.splitlines():
        if not zeile.startswith("|"):
            continue
        spalten = [s.strip() for s in zeile.strip("|").split("|")]
        if len(spalten) < 2 or spalten[0] in ("VL", "---"):
            continue
        vl = spalten[0]
        for ziel in re.findall(r"\]\((part-[^)]+\.md)\)", spalten[1]):
            zu.setdefault(Path(ziel).name, []).append(vl)
    if not zu:
        sys.exit("kurs-2026-27.md: Wochentabelle nicht gefunden — hat sich die Form geändert?")
    return {name: "/".join(vls) for name, vls in zu.items()}


def kapitel_laden(auswahl: list[str]) -> list[Kapitel]:
    zu = vl_zuordnung()
    pfade = sorted(p for teil in TEILE for p in (WURZEL / teil).glob("*.md"))
    geladen = [Kapitel(p, zu.get(p.name, "—")) for p in pfade]
    for name in zu:
        if name not in {p.name for p in pfade}:
            print(f"Hinweis: `{name}` steht im Plan, liegt aber nicht in part-*/", file=sys.stderr)

    def schluessel(k: Kapitel) -> tuple[int, str]:
        erste = k.vl.split("/")[0]
        return (int(erste) if erste.isdigit() else 99, k.nummer)

    geladen.sort(key=schluessel)
    if auswahl:
        gewuenscht = {a.lstrip("0") or "0" for a in auswahl}
        geladen = [k for k in geladen if (k.nummer.lstrip("0") or "0") in gewuenscht]
        if not geladen:
            sys.exit(f"Kein Kapitel zu {auswahl} gefunden.")
    return geladen


def uebersicht(kapitel: list[Kapitel]) -> str:
    """Die Fortschrittstabelle für den Befundbogen — Spalten A1/A2/A3 bleiben leer.

    Sie werden von Hand gefüllt, und zwar mit einem Datum: „geprüft“ ohne Datum ist eine
    Absichtserklärung. Wenige Spalten absichtlich; Codeblöcke, Jahre und Quellen stehen in
    der Prüfliste des Kapitels, nicht hier.
    """
    z = [
        "| Kap | Titel | VL | Wörter | Formeln | Zahlen | Proben | A1 | A2 | A3 | Befunde |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for k in kapitel:
        z.append(
            f"| {k.nummer} | {k.titel} | {k.vl} | {k.woerter} | {len(k.formeln)} | "
            f"{len(k.zahlen)} | {len(k.antwortproben)} | | | | |"
        )
    summe = lambda f: sum(f(k) for k in kapitel)  # noqa: E731
    z.append(
        f"| | **{len(kapitel)} Kapitel** | | **{summe(lambda k: k.woerter)}** | "
        f"**{summe(lambda k: len(k.formeln))}** | **{summe(lambda k: len(k.zahlen))}** | "
        f"**{summe(lambda k: len(k.antwortproben))}** | | | | |"
    )
    return "\n".join(z)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("kapitel", nargs="*", help="Kapitelnummern, z. B. 06 08; ohne Angabe alle")
    p.add_argument("--uebersicht", action="store_true", help="nur die Fortschrittstabelle")
    p.add_argument("--out", type=Path, help="Ausgabe in eine Datei statt nach stdout")
    args = p.parse_args()

    geladen = kapitel_laden(args.kapitel)
    teile = [uebersicht(geladen)]
    if not args.uebersicht:
        teile.append("")
        teile.extend(k.pruefliste() for k in geladen)
    ausgabe = "\n".join(teile) + "\n"

    if args.out:
        args.out.write_text(ausgabe, encoding="utf-8")
        print(f"{args.out} geschrieben ({len(geladen)} Kapitel).")
    else:
        sys.stdout.write(ausgabe)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
