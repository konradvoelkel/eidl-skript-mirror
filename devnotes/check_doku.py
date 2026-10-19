#!/usr/bin/env python3
"""Prüft, ob die Dokumentation noch stimmt — Pfade, Zahlen, Konventionen.

Doku altert schneller als Code, weil sie niemand baut. Am 2026-09-27 stand in `CLAUDE.md`
eine `--min-pages`-Zahl von vor dem Herausnehmen der Übungsblätter, ein Verweis auf eine
Datei, die es nicht mehr gab, und eine empfohlene Gegenprobe, die selbst fehlerhaft war —
alles drei ohne dass irgendetwas rot geworden wäre. Dieses Skript macht daraus eine Prüfung.

Es liest die drei Dokumentationsdateien (`CLAUDE.md`, `devnotes/TODO.md`,
`devnotes/README.md`) und vergleicht, was sie behaupten, mit dem Repo:

1. **Pfade.** Jeder in Backticks genannte Pfad existiert (Ausnahmen unten sind benannt).
2. **Zahlen.** Kapitel, Übungsabschnitte, `dropdown`-Boxen, Seitenzahl des gebauten PDF.
3. **`--min-pages`** in CLAUDE.md und in `.gitlab-ci.yml` stimmen überein.
4. **Vollständigkeit.** Jede Datei in `devnotes/` steht in dessen `README.md` und umgekehrt,
   und `TODO.md` enthält nur offene Punkte (die Historie steht in `erledigt.md`).
5. **Die Regeln, die im Buch gelten:** keine Verweise auf nummerierte Übungsblätter, keine
   Lösungsvorschläge, keine Unicode-Pfeile im Fließtext.

Aufruf:

    uv run devnotes/check_doku.py

Endet mit Exit-Code 1 und einer Liste, wenn etwas nicht stimmt. Was sich bewusst geändert
hat, wird hier nachgezogen — die Ausnahmen stehen als Konstante am Kopf, nicht verstreut.

**Was es nicht prüft:** Pfade in den Kapiteltexten. Dort wird mit Markdown-Links verwiesen,
und kaputte Links meldet der HTML-Build selbst (`Cross-reference target not found`). Und es
prüft nicht, ob die Doku *sinnvoll* ist — nur, ob sie noch stimmt.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
DOKU = ("CLAUDE.md", "devnotes/TODO.md", "devnotes/README.md")

# Pfade, die absichtlich nicht existieren: Artefakte der CI, historische Namen in
# „Erledigt"-Einträgen, Platzhalter, Pfade in anderen Repos.
PFAD_AUSNAHMEN = {
    "public/",
    "public/eidl-skript.pdf",
    "part-exercises/",
    "exam2026-eidl-exam-1/2.tex",
    "_tex/plain_latex-hhu/",
    "~/Sciebo/hhu/eidl-25/exercises/blattNN-solution/",
    "ds2-26/ilias/",
    "devnotes/build_skript_from_2025.py",
    "devnotes/restructure.py",
    "git show 946600f:devnotes/restructure.py",
}


def fehler_sammeln() -> list[str]:
    fehler: list[str] = []

    # ── 1. Pfade ────────────────────────────────────────────────────────────────
    for name in DOKU:
        inhalt = (WURZEL / name).read_text(encoding="utf-8")
        basis = (WURZEL / name).parent
        for k in sorted(set(re.findall(r"`([~./A-Za-z0-9_\-]+/[A-Za-z0-9_\-./]*)`", inhalt))):
            if k in PFAD_AUSNAHMEN:
                continue
            if k.startswith("~"):
                p = Path(os.path.expanduser(k))
            elif k.startswith("/"):
                p = Path(k)
            elif k.startswith("../"):
                p = basis / k  # Verweise aus devnotes/ heraus
            else:
                p = WURZEL / k  # sonst relativ zur Repo-Wurzel
            if not p.exists():
                fehler.append(f"{name}: Pfad `{k}` existiert nicht ({p})")

    # ── 2. Zahlen ───────────────────────────────────────────────────────────────
    kapitel = sorted(
        p
        for teil in ("part-grundlagen", "part-lernen", "part-representation-learning",
                     "part-architekturen-anwendungen")
        for p in (WURZEL / teil).glob("*.md")
    )
    uebungen = [p for p in kapitel if "\n## Übung\n" in p.read_text(encoding="utf-8")]
    dropdowns = sum(
        p.read_text(encoding="utf-8").count("dropdown") for p in kapitel
    )

    claude = (WURZEL / "CLAUDE.md").read_text(encoding="utf-8")
    todo = (WURZEL / "devnotes/TODO.md").read_text(encoding="utf-8")

    def behauptet(text: str, muster: str, name: str, ist: int) -> None:
        m = re.search(muster, text)
        if not m:
            fehler.append(f"{name}: Behauptung nicht gefunden (Muster {muster!r})")
        elif int(m.group(1)) != ist:
            fehler.append(f"{name}: behauptet {m.group(1)}, tatsächlich {ist}")

    behauptet(claude, r"(\d+) der 29 Kapitel haben einen", "CLAUDE.md/Übungsabschnitte", len(uebungen))
    behauptet(todo, r"(\d+) Übungsabschnitte", "TODO.md/Übungsabschnitte", len(uebungen))
    if dropdowns != 7:
        fehler.append(
            f"CLAUDE.md nennt sieben `dropdown`-Boxen, im Buch sind es {dropdowns} — "
            "und `dropdown` versteckt im PDF nichts, also nachsehen, was da offen steht"
        )
    if len(kapitel) != 29:
        fehler.append(f"Doku spricht von 29 Kapiteln, gefunden: {len(kapitel)}")

    # ── 3. --min-pages hier und in der CI ───────────────────────────────────────
    ci = (WURZEL / ".gitlab-ci.yml").read_text(encoding="utf-8")
    m_doku = re.search(r"--min-pages (\d+)", claude)
    m_ci = re.search(r"--min-pages (\d+)", ci)
    if not (m_doku and m_ci):
        fehler.append("--min-pages nicht in CLAUDE.md und/oder .gitlab-ci.yml gefunden")
    elif m_doku.group(1) != m_ci.group(1):
        fehler.append(
            f"--min-pages: CLAUDE.md sagt {m_doku.group(1)}, .gitlab-ci.yml sagt {m_ci.group(1)}"
        )

    # ── 4. devnotes/ und sein Index ─────────────────────────────────────────────
    index = (WURZEL / "devnotes/README.md").read_text(encoding="utf-8")
    vorhanden = {p.name for p in (WURZEL / "devnotes").iterdir() if p.suffix in (".py", ".md")}
    vorhanden.discard("README.md")
    genannt = set(re.findall(r"`([A-Za-z0-9_\-]+\.(?:py|md))`", index))
    for f in sorted(vorhanden - genannt):
        fehler.append(f"devnotes/README.md: `{f}` liegt da, steht aber nicht im Index")
    for f in sorted(genannt - vorhanden - {"README.md"}):
        if f not in {"build_skript_from_2025.py", "restructure.py"}:  # historisch erwähnt
            fehler.append(f"devnotes/README.md: `{f}` steht im Index, existiert aber nicht")

    # ── 4b. TODO.md enthaelt nur Offenes ────────────────────────────────────────
    # Am 2026-09-27 standen dort 65 erledigte gegen 24 offene Punkte. Die Historie ist nach
    # erledigt.md gewandert; wer sie zurueckwandern laesst, macht die Liste wieder unlesbar.
    erledigt_in_todo = len(re.findall(r"(?m)^- \[x\]", todo))
    if erledigt_in_todo:
        fehler.append(
            f"devnotes/TODO.md: {erledigt_in_todo} erledigte Punkte — die gehoeren nach "
            "devnotes/erledigt.md, damit die Liste die Frage „was ist zu tun\" beantwortet"
        )

    # ── 5. Regeln, die im Buch gelten ───────────────────────────────────────────
    buchdateien = kapitel + [WURZEL / n for n in ("index.md", "README.md", "glossar.md")]
    for p in buchdateien:
        text = p.read_text(encoding="utf-8")
        for treffer in re.findall(r"(?:Übungs)?[Bb]latt ?\d+", text):
            fehler.append(f"{p.name}: Verweis auf ein nummeriertes Übungsblatt („{treffer}“)")
        if "Lösungsvorschlag" in text:
            fehler.append(f"{p.name}: enthält einen Lösungsvorschlag — das Repo ist öffentlich")
        for pfeil in ("→", "←", "⇒", "↦"):
            if pfeil in re.sub(r"```.*?```", "", text, flags=re.S):
                fehler.append(f"{p.name}: Unicode-Pfeil „{pfeil}“ im Fließtext (bricht den PDF-Lauf)")

    # ── 6. Das gebaute PDF, falls vorhanden ─────────────────────────────────────
    pdf = WURZEL / "exports/eidl-skript.pdf"
    if pdf.is_file():
        lauf = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=False)
        m = re.search(r"^Pages:\s+(\d+)", lauf.stdout, re.M)
        if m:
            seiten = int(m.group(1))
            behauptet(claude, r"PDF \*\*(\d+) Seiten", "CLAUDE.md/Seitenzahl", seiten)
            behauptet(todo, r"\*\*29 Kapitel plus Glossar, (\d+) Seiten", "TODO.md/Seitenzahl", seiten)
            untergrenze = int(m_ci.group(1)) if m_ci else 0
            if seiten < untergrenze:
                fehler.append(f"PDF hat {seiten} Seiten, unter der CI-Untergrenze {untergrenze}")
    else:
        print("Hinweis: kein gebautes PDF in exports/ — Seitenzahlen ungeprüft.")

    return fehler


def main() -> int:
    fehler = fehler_sammeln()
    if fehler:
        print(f"{len(fehler)} Beanstandung(en):", file=sys.stderr)
        for f in fehler:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("Dokumentation stimmt mit dem Repo überein.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
