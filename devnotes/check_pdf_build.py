#!/usr/bin/env python3
"""Prüft das Ergebnis von `myst build --pdf` — weil der Befehl selbst lügt.

Am 2026-09-25 endete `myst build --pdf` mit **Exit-Code 0**, obwohl LaTeX nach 104
Fehlern abgebrochen war und das PDF 226 statt 435 Seiten hatte: Der Rest des
Brownfield-Kapitels, ganz `part-appdev`, ganz `part-practical` und alle Übungsblätter
fehlten. Ein CI-Job, der nur `myst build --pdf` aufruft, hätte das nicht gemerkt.

Drei Prüfungen, von denen die dritte den Fall damals tatsächlich gefunden hat:

1. **Fehler im Log** — und zwar im richtigen Format. Latexmk läuft mit
   `-file-line-error`, Fehlerzeilen beginnen also mit `./datei.tex:419:` und **nicht**
   mit `! `. Ein `grep '^! '` meldet 0, wo 104 sind.
2. **Der Abbruch wegen Fehlerflut** (`That makes 100 errors`), der alles Weitere
   verschluckt.
3. **Die Seitenzahl** gegen eine Untergrenze, und Stichproben aus den *letzten*
   Kapiteln im extrahierten Text. Nur das fängt einen Abbruch, der sich sonst nirgends
   als Fehler zeigt.

Aufruf:

    python devnotes/check_pdf_build.py --min-pages 400 \\
        --expect Playground --expect Keyboard-Smasher
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent

# Fehlerzeile im -file-line-error-Format: ./datei.tex:419: Meldung
FEHLERZEILE = re.compile(r"^\./[^:]+\.tex:\d+: ", re.M)
ABBRUCH = "That makes 100 errors"
SEITEN = re.compile(r"Output written on .*?\((\d+) pages")

# "Missing character: There is no │ (U+2502) in font [lmmono10-regular]:"
# Das ist **keine** Warnung im harmlosen Sinn: Das Zeichen fehlt im PDF
# ersatzlos, LaTeX laeuft trotzdem mit Exit 0 durch, und im HTML sieht man
# nichts davon. So sind 820 fehlende Rahmen- und Emoji-Zeichen monatelang
# unbemerkt geblieben (Protokoll: devnotes/build-log-2026-09-26.md).
FEHLENDE_GLYPHE = re.compile(r"^Missing character: There is no (.) \(U\+([0-9A-F]+)\)", re.M)

# MyST meldet auf **stdout**, wenn es einen Knoten nicht nach LaTeX uebersetzen kann, und
# laesst ihn dann weg -- mit Exit 0 und ohne Spur im LaTeX-Log. In eipy war das ein
# `:::{iframe}`, der eine leere figure-Umgebung mit der Bildunterschrift "iframe"
# hinterliess (2026-09-27). Deshalb liest der Pruefer auf Wunsch auch das MyST-Protokoll.
VERSCHLUCKTER_KNOTEN = re.compile(r"Unhandled LaTeX conversion for node of \"([^\"]+)\"")

# Kein Fehler, sondern eine bewusste Entscheidung (Playbook 3.8d): Ohne `inkscape` rastert
# MyST SVG nach PNG. Wird gezaehlt und gemeldet, damit die Entscheidung sichtbar bleibt.
SVG_FALLBACK = re.compile(r"To convert .svg images to .pdf, you must install inkscape")


def neuestes_log() -> Path | None:
    kandidaten = sorted(
        WURZEL.glob("_build/temp/myst*/*.log"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return kandidaten[0] if kandidaten else None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pdf", type=Path, help="PDF; Vorgabe: die einzige in exports/")
    p.add_argument("--log", type=Path, help="LaTeX-Log; Vorgabe: das neueste unter _build/temp/")
    p.add_argument("--min-pages", type=int, default=1, help="erwartete Mindestseitenzahl")
    p.add_argument(
        "--tolerate",
        action="append",
        default=[],
        metavar="TEXT",
        help="Fehlerzeilen, die diesen Text enthalten, werden gezaehlt und gemeldet, "
        "aber nicht beanstandet. Nur fuer bekannte, kosmetische Umgebungsprobleme "
        "benutzen -- und mit Begruendung an der Aufrufstelle.",
    )
    p.add_argument(
        "--max-missing-glyphs",
        type=int,
        default=0,
        metavar="N",
        help="erlaubte Zahl fehlender Glyphen (`Missing character` im Log). "
        "Vorgabe 0: Ein Zeichen, fuer das keine Schrift eine Glyphe hat, fehlt im "
        "PDF ersatzlos -- ohne Fehler, ohne Warnung im HTML.",
    )
    p.add_argument(
        "--myst-log",
        type=Path,
        metavar="DATEI",
        help="Protokoll von `myst build --pdf` (via tee). Wird auf Knoten geprueft, die "
        "MyST nicht nach LaTeX uebersetzen konnte und deshalb weggelassen hat.",
    )
    p.add_argument(
        "--expect",
        action="append",
        default=[],
        metavar="TEXT",
        help="Text, der im PDF vorkommen muss (mehrfach angebbar); "
        "sinnvoll sind Stellen aus den *letzten* Kapiteln",
    )
    args = p.parse_args(argv)

    fehler: list[str] = []

    pdf = args.pdf
    if pdf is None:
        gefunden = sorted((WURZEL / "exports").glob("*.pdf"))
        if len(gefunden) != 1:
            print(
                f"FEHLER: erwarte genau ein PDF in exports/, gefunden: "
                f"{[g.name for g in gefunden]}",
                file=sys.stderr,
            )
            return 1
        pdf = gefunden[0]
    if not pdf.is_file():
        print(f"FEHLER: {pdf} fehlt", file=sys.stderr)
        return 1

    log = args.log or neuestes_log()
    if log is None or not log.is_file():
        print("FEHLER: kein LaTeX-Log unter _build/temp/ gefunden", file=sys.stderr)
        return 1

    text = log.read_text(encoding="utf-8", errors="replace")

    # Ganze Fehlerzeilen, damit --tolerate am Meldungstext greifen kann.
    fehlerzeilen = [
        z for z in text.splitlines() if FEHLERZEILE.match(z + "\n") or FEHLERZEILE.match(z)
    ]
    toleriert = [z for z in fehlerzeilen if any(t in z for t in args.tolerate)]
    echte = [z for z in fehlerzeilen if z not in toleriert]

    if toleriert:
        # Gezaehlt und gemeldet, nicht verschwiegen: Wer das liest, soll sehen,
        # dass hier etwas unter einer Ausnahme laeuft.
        muster = ", ".join(repr(t) for t in args.tolerate)
        print(f"toleriert: {len(toleriert)} Fehlerzeile(n) nach Muster {muster}")
    if echte:
        fehler.append(
            f"{len(echte)} LaTeX-Fehler im Log ({log.name}), z.B.: "
            + "; ".join(z.strip()[:90] for z in echte[:3])
        )
    glyphen = FEHLENDE_GLYPHE.findall(text)
    if glyphen:
        haeufig: dict[str, int] = {}
        for zeichen, codepoint in glyphen:
            haeufig[f"{zeichen} U+{codepoint}"] = haeufig.get(f"{zeichen} U+{codepoint}", 0) + 1
        aufzaehlung = ", ".join(
            f"{k} ({v}x)" for k, v in sorted(haeufig.items(), key=lambda kv: -kv[1])
        )
        meldung = f"{len(glyphen)} fehlende Glyphe(n) im PDF: {aufzaehlung}"
        if len(glyphen) > args.max_missing_glyphs:
            fehler.append(
                meldung + " — eine Schrift im Image kennt diese Zeichen nicht, "
                "sie fehlen im PDF ersatzlos"
            )
        else:
            print(f"toleriert: {meldung}")

    if args.myst_log:
        if not args.myst_log.is_file():
            fehler.append(f"MyST-Protokoll {args.myst_log} fehlt")
        else:
            myst_text = args.myst_log.read_text(encoding="utf-8", errors="replace")
            knoten = VERSCHLUCKTER_KNOTEN.findall(myst_text)
            if knoten:
                knotenliste = ", ".join(sorted({f"{k} ({knoten.count(k)}x)" for k in knoten}))
                fehler.append(
                    f"MyST hat {len(knoten)} Knoten nicht nach LaTeX uebersetzt und "
                    f"weggelassen: {knotenliste} — im PDF fehlt der Inhalt ersatzlos"
                )
            svg = len(SVG_FALLBACK.findall(myst_text))
            if svg:
                print(
                    f"Hinweis: {svg}x SVG nach PNG gerastert (kein inkscape im Image). "
                    "Bewusst so, siehe Playbook 3.8d."
                )

    if ABBRUCH in text:
        fehler.append(
            f"LaTeX hat wegen Fehlerflut abgebrochen ({ABBRUCH!r}) — "
            "alles nach der Fehlerstelle fehlt im PDF"
        )

    seiten = SEITEN.findall(text)
    if not seiten:
        fehler.append("keine Seitenzahl im Log gefunden ('Output written on ...')")
    else:
        gezaehlt = int(seiten[-1])
        print(f"Seiten: {gezaehlt}")
        if gezaehlt < args.min_pages:
            fehler.append(
                f"nur {gezaehlt} Seiten, erwartet mindestens {args.min_pages} — "
                "das ist das Anzeichen für einen abgebrochenen Lauf"
            )

    if args.expect:
        if shutil.which("pdftotext") is None:
            fehler.append(
                "pdftotext fehlt, die Stichproben konnten nicht geprüft werden "
                "(Paket poppler-utils)"
            )
        else:
            lauf = subprocess.run(
                ["pdftotext", str(pdf), "-"],
                capture_output=True,
                text=True,
                check=False,
            )
            inhalt = lauf.stdout
            for erwartet in args.expect:
                if erwartet not in inhalt:
                    fehler.append(
                        f"{erwartet!r} steht nicht im PDF — wahrscheinlich fehlen "
                        "die letzten Kapitel"
                    )
                else:
                    print(f"gefunden: {erwartet}")

    if fehler:
        print(f"\n{len(fehler)} Beanstandung(en):", file=sys.stderr)
        for f in fehler:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print(f"PDF in Ordnung: {pdf.relative_to(WURZEL)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
