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
   Lösungsvorschläge, keine Unicode-Pfeile im Fließtext. Und Literatur ist anklickbar: kein
   `et al.` und kein `arXiv:…` ohne Link in derselben Zeile, und jedes Werk, das ein Kapitel
   über DOI oder arXiv verlinkt, steht auch in dessen „Weiterlesen“-Box, und DOI-Links gehen
   über `hdl.handle.net`, nicht über `doi.org` (seit 2026-11-02). Und jede Seite außer
   der Landingpage hat ein eigenes `description:` von 80 bis 155 Zeichen (seit 2026-11-03).

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
    if dropdowns != 9:
        fehler.append(
            f"CLAUDE.md nennt neun `dropdown`-Boxen, im Buch sind es {dropdowns} — "
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

    # Literatur (2026-11-02): Im Transformer-Kapitel stand ein Verweis auf einen Artikel, der
    # weder anklickbar war noch in "Weiterlesen" auftauchte -- und so ging es rund 50 Werken
    # im ganzen Buch. Zwei Prüfungen, beide bewusst grob: eine Zeile, die "et al." oder
    # "arXiv:" nennt, enthält auch einen Link; und jede DOI- oder arXiv-Adresse eines Kapitels
    # steht auch in dessen Weiterlesen-Box. Was keine dieser Formen hat ("Gage 1994"), fängt
    # das nicht -- dafür gilt die Regel in CLAUDE.md, Abschnitt "Literatur".
    for p in kapitel:
        text = p.read_text(encoding="utf-8")
        ohne_code = re.sub(r"```.*?```", "", text, flags=re.S)
        for nr, zeile in enumerate(ohne_code.splitlines(), 1):
            ohne_links = re.sub(r"\[[^\]]*\]\([^)]*\)", "", zeile)
            if ("et al." in ohne_links or re.search(r"arXiv:\d", ohne_links)) and "](" not in zeile:
                if zeile.lstrip().startswith(("#", ":::")):
                    continue  # Überschriften und Direktiven-Köpfe tragen keine Links
                fehler.append(f"{p.name}: Literaturverweis ohne Link: „{zeile.strip()[:70]}…“")
        box = re.search(r":::\{admonition\} Weiterlesen\n(.*?)\n:::", ohne_code, re.S)
        box_text = box.group(1) if box else ""
        for url in sorted(set(re.findall(r"https://(?:hdl\.handle\.net|arxiv\.org/abs)/[^)\s]+", ohne_code))):
            if url not in box_text:
                fehler.append(f"{p.name}: {url} steht im Text, aber nicht in „Weiterlesen“")
        # Kein doi.org: mystmd macht aus jedem Link dorthin ein Zitat, holt die Metadaten beim
        # Bauen aus dem Netz und ersetzt im PDF den Linktext durch "Autor [Jahr]" samt
        # angehängter Literaturliste -- ohne Netz steht "?" da (2026-11-02: 24 Stellen lokal,
        # drei Seiten mehr in der CI). hdl.handle.net löst dieselbe DOI auf, unberührt.
        for treffer in sorted(set(re.findall(r"https?://(?:dx\.|www\.)?doi\.org/[^)\s]+", ohne_code))):
            fehler.append(f"{p.name}: {treffer} -- DOI-Links als https://hdl.handle.net/<DOI>, siehe CLAUDE.md „Literatur“")

    # ── 5b. Aufzeichnungen: Linkzeile und Player-Widget nennen dieselbe Adresse ──
    # Jede Zeile „[Vorlesungsaufzeichnung …](…)“ bekommt darunter den eingeklappten Player
    # (widgets/mediathek.mjs). Die Adresse steht damit zweimal da; wird eine nachgetragen oder
    # korrigiert, muss die andere mit -- sonst spielt der Player ein anderes Video als der Link.
    LINKZEILE = re.compile(r"^\[Vorlesungsaufzeichnung[^\]]*\]\((https://media\.hhu\.de/video/[^)]+)\)$", re.M)
    PLAYER = re.compile(r"^:::\{anywidget\} \.\./widgets/mediathek\.mjs\n\{url: '([^']+)'\}\n:::$", re.M)
    for p in kapitel:
        text = p.read_text(encoding="utf-8")
        links = [(m.end(), m.group(1)) for m in LINKZEILE.finditer(text)]
        player = [(m.start(), m.group(1)) for m in PLAYER.finditer(text)]
        if text.count("widgets/mediathek.mjs") != len(player):
            fehler.append(f"{p.name}: Player-Widget nicht in der Form {{url: '…'}} -- so prüft niemand die Adresse")
        for ende, adresse in links:
            folgt = [a for start, a in player if 0 < start - ende <= 2]
            if not folgt:
                fehler.append(f"{p.name}: unter der Aufzeichnungszeile fehlt der Player (widgets/mediathek.mjs)")
            elif folgt[0] != adresse:
                fehler.append(f"{p.name}: Player spielt {folgt[0]}, die Linkzeile darüber nennt {adresse}")
        if len(player) > len(links):
            fehler.append(f"{p.name}: Player-Widget ohne Aufzeichnungszeile darüber")

    # ── 5c. Jede Seite außer der Landingpage hat eine eigene Beschreibung ─────────
    # Bis zum 2026-11-03 trug keine einzige Seite ein `description:`; alle 32 erbten die
    # des Projekts aus myst.yml, als Meta-Description, og:description und im JSON-LD je
    # Kapitel -- als Suchergebnis 32-mal derselbe Satz (SEO-Audit, wichtigster inhaltlicher
    # Befund). Die Landingpage behält die des Buchs. 155 Zeichen, weil Google ab etwa da
    # abschneidet; eine Untergrenze fängt ein vergessenes halbes Stichwort.
    beschreibungen: dict[str, str] = {}
    for p in buchdateien:
        if p.name == "index.md":
            continue
        kopf = re.match(r"---\n(.*?)\n---\n", p.read_text(encoding="utf-8"), re.S)
        m = re.search(r'(?m)^description:\s*"([^"]*)"\s*$', kopf.group(1)) if kopf else None
        if not m:
            fehler.append(f"{p.name}: kein `description:` im Frontmatter -- dann erbt die Seite die des Buchs")
            continue
        d = m.group(1)
        if not 80 <= len(d) <= 155:
            fehler.append(f"{p.name}: description hat {len(d)} Zeichen, erwartet 80 bis 155")
        if d in beschreibungen:
            fehler.append(f"{p.name}: dieselbe description wie {beschreibungen[d]}")
        beschreibungen.setdefault(d, p.name)
        for zeichen in ("—", "→"):
            if zeichen in d:
                fehler.append(f"{p.name}: „{zeichen}“ in der description (Gedankenstrich ist „–“)")

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

    # ── 7. Die ausgegebenen Uebungsblaetter ─────────────────────────────────────
    # `blaetter/` ist der einzige Ort im Repo, an dem ein Uebungsblatt liegt, und das Repo
    # ist oeffentlich. Zwei Dinge muessen deshalb stimmen: dort liegt **nur** das Blatt,
    # nie eine Loesungsfassung (die TeX-Quellen enthalten sie, der Wrapper schaltet sie
    # ein), und die Seite `uebungsblaetter.md` verlinkt genau die Dateien, die da sind --
    # sonst steht ein Blatt unverlinkt im Netz oder ein Link zeigt ins Leere.
    ordner = WURZEL / "blaetter"
    if ordner.exists():
        dateien = sorted(p.name for p in ordner.iterdir() if p.is_file())
        for name in dateien:
            if re.search(r"loesung|lösung|solution", name, re.I):
                fehler.append(f"blaetter/{name}: Loesungsfassung im oeffentlichen Repo")
            elif not re.fullmatch(r"blatt\d\d\.pdf", name):
                fehler.append(f"blaetter/{name}: erwartet wird blattNN.pdf")
        seite = WURZEL / "uebungsblaetter.md"
        if not seite.exists():
            fehler.append("blaetter/ ist da, aber uebungsblaetter.md fehlt")
        else:
            verlinkt = set(re.findall(r"blaetter/(blatt\d\d\.pdf)", seite.read_text(encoding="utf-8")))
            for name in dateien:
                if name.endswith(".pdf") and name not in verlinkt:
                    fehler.append(f"blaetter/{name} ist nicht in uebungsblaetter.md verlinkt")
            for name in sorted(verlinkt - set(dateien)):
                fehler.append(f"uebungsblaetter.md verlinkt {name}, die Datei fehlt")

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
