#!/usr/bin/env python3
"""Stand und zitierfähige Adresse in die Herkunftszeile jeder Seite, die eine hat.

    python3 tools/zitierzeile.py <site-url> <html-verzeichnis> [--check]

**Nach `tools/llms_txt.py`** laufen lassen und vor `tools/precompress.py`: Die
Markdown-Auslieferung muss schon da sein, damit die Zeile auch dort steht, und jede
Änderung nach der Vorkompression liefert allen Lesern die alte `.br` aus.

## Warum das Skript da ist

Jedes Kapitel endet seit dem 2026-11-17 mit einer Herkunftszeile: Werktitel, Gattung,
Autor, Lizenz und der Link auf „Über dieses Skript". Was darin **fehlte**, hat das dritte
SEO-Audit gefunden (2026-11-18, §8): kein Jahr, keine zitierfähige Adresse, und auf keiner
der 33 Seiten überhaupt ein sichtbares Datum. Für eine Dozentin, die ein Kapitel in ihrem
Material nennen will, und für eine Antwortmaschine, die eine Quelle datieren soll, ist
genau das der entscheidende Baustein -- und beides stand bis dahin nur eine Seite weiter
auf `/readme/`.

## Warum beim Veröffentlichen und nicht in der Quelle

Konrads Entscheidung vom 2026-11-18, und sie hat zwei Gründe, die beide zwingend sind:

* **Die Adresse darf nicht in die Quelle.** `CLAUDE.md` („Querverweise") verbietet
  absolute URLs auf die eigene Pages-Domain im Buch, und zwar aus gutem Grund: Der Host
  trägt eine von GitLab vergebene Zufallskennung (`131e30`), die bei einer Neuanlage des
  Projekts wechselt. 31 Kapitel mit einer eingebrannten Adresse wären 31 Stellen, die dann
  falsch sind.
* **Das Datum soll sich nicht von Hand pflegen lassen müssen.** Es steht in der Historie:
  `tools/freshness.py` liest es schon je Seite aus `git log` der Quelldatei, für
  `article:modified_time` und `<lastmod>`. Dieses Skript benutzt **dieselbe** Funktion und
  nicht eine zweite Rechnung -- zwei Datumsquellen wären zwei Wahrheiten.

Preis der Entscheidung, und er ist bewusst in Kauf genommen: **Im PDF steht die Zeile ohne
Datum und ohne Adresse**, weil dort kein Veröffentlichungsschritt läuft. Das PDF hat dafür
seine eigenen Metadaten.

## Wo gepatcht wird, und warum an genau diesen Stellen

Die Zeile ist **Fließtext**, kein Kopf-Tag -- und genau darum reicht das Markup nicht. Das
Theme rendert den Rumpf nach der Hydration aus der Nutzlast neu (React #418/#423, siehe
`tools/hydration.py`); was nur im Markup steht, ist nach dem ersten Frame weg. Dasselbe
hat `tools/webp.py` für die Bildadressen und `tools/trailing_slash.py` für die
Kapitellinks gelernt. Gepatcht wird deshalb:

* `<slug>/index.html` -- **zweimal** je Seite: im Markup und in `window.__remixContext`.
  Der Ankertext steht in der Nutzlast als *ein* Textknoten (nachgemessen am 2026-11-18),
  deshalb genügt eine Zeichenketten-Ersetzung über das ganze Dokument.
* `<slug>.json` -- die Seiten-JSON, aus der das Theme bei einer Navigation im Client
  rendert. Dieselbe Begründung wie in `trailing_slash.py`.
* `<slug>.md` und `<slug>/index.md` -- die Markdown-Auslieferung. Das ist die Fläche, die
  Antwortmaschinen lesen, also die eigentliche Zielgruppe dieses Befunds.
* `llms-full.txt` -- abschnittsweise, getrennt an den `URL: `-Zeilen.

**Nicht** gepatcht wird:

* die Startseite und `/readme/` -- die eine *ist* das Werk, die andere erklärt es; beide
  tragen die Herkunftszeile gar nicht.
* `myst.search.json`, der Suchindex: Datum und Adresse in jedem Suchausschnitt wären Lärm.
* die gehashten Markdown-Kopien im Dateiordner -- das ist der Quelltext zum Herunterladen,
  und der trägt die Adresse aus demselben Grund nicht wie die Quelle selbst.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import freshness  # noqa: E402  -- dieselbe Datumsquelle, siehe Docstring

ANKER = "frei unter CC BY-SA 4.0. "
MARKE = "Zitierbar als "

MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"]


def deutsches_datum(iso: str) -> str:
    """`2026-11-18T00:45:57+01:00` zu `18. November 2026`.

    Ohne `locale`: Das Image des `pages`-Jobs ist Alpine, und dort fehlt `de_DE`. Eine
    Monatstabelle ist langweilig und funktioniert überall.
    """
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", iso)
    if not m:
        raise SystemExit(f"✗ unerwartetes Datum aus git: {iso!r}")
    jahr, monat, tag = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if not 1 <= monat <= 12:
        raise SystemExit(f"✗ Monat {monat} aus {iso!r}")
    return f"{tag}. {MONATE[monat - 1]} {jahr}"


def ersatz(url: str, datum: str) -> str:
    return f"frei unter CC BY-SA 4.0, Stand {datum}. {MARKE}{url}. "


def patche(pfad: Path, url: str, datum: str, erwartet: int) -> int:
    """Ersetzt den Anker in einer Datei. Gibt die Zahl der Ersetzungen zurück."""
    text = pfad.read_text(encoding="utf-8")
    if MARKE in text:
        return -1  # schon gepatcht
    n = text.count(ANKER)
    if n != erwartet:
        raise SystemExit(
            f"✗ {pfad}: {n}x {ANKER!r}, erwartet {erwartet}x -- "
            f"Herkunftszeile geändert oder Theme bewegt?"
        )
    pfad.write_text(text.replace(ANKER, ersatz(url, datum)), encoding="utf-8")
    return n


def abschnitte(text: str) -> list[tuple[str, int, int]]:
    """(url, anfang, ende) je Seitenabschnitt von `llms-full.txt`."""
    marken = [(m.group(1), m.start()) for m in re.finditer(r"^URL: (\S+)$", text, re.M)]
    out = []
    for i, (url, start) in enumerate(marken):
        ende = marken[i + 1][1] if i + 1 < len(marken) else len(text)
        out.append((url, start, ende))
    return out


def llms_full(pfad: Path, je_url: dict[str, str]) -> int:
    """Abschnittsweise patchen: der Anker im Kopf der Datei bleibt unberührt."""
    text = pfad.read_text(encoding="utf-8")
    if MARKE in text:
        return -1
    stuecke, letzte, n = [], 0, 0
    for url, start, ende in abschnitte(text):
        stuecke.append(text[letzte:start])
        teil = text[start:ende]
        datum = je_url.get(url.rstrip("/") + "/")
        if datum and teil.count(ANKER) == 1:
            teil = teil.replace(ANKER, ersatz(url.rstrip("/") + "/", datum))
            n += 1
        stuecke.append(teil)
        letzte = ende
    stuecke.append(text[letzte:])
    pfad.write_text("".join(stuecke), encoding="utf-8")
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", help="Adresse der Site, ohne Schrägstrich am Ende")
    ap.add_argument("html", type=Path, help="das gebaute Verzeichnis")
    ap.add_argument("--check", action="store_true", help="nur nachprüfen, nichts ändern")
    args = ap.parse_args()
    site = args.site.rstrip("/")
    root: Path = args.html

    seiten = freshness.pages(root)
    je_url: dict[str, str] = {}
    getan = uebersprungen = 0
    fehlend: list[str] = []

    for slug, ziel, iso in seiten:
        if not slug or not ziel.exists():
            continue
        if ANKER not in ziel.read_text(encoding="utf-8") and MARKE not in ziel.read_text(encoding="utf-8"):
            continue  # Startseite und /readme/ tragen die Zeile nicht
        url = f"{site}/{slug}/"
        datum = deutsches_datum(iso)
        je_url[url] = datum

        kandidaten = [(ziel, 2), (root / f"{slug}.json", 1),
                      (root / f"{slug}.md", 1), (root / slug / "index.md", 1)]
        if args.check:
            # **Gezaehlt, nicht nur gesucht.** Eine Prüfung, die „steht die Marke
            # irgendwo" fragt, besteht auch dann, wenn nur eine der beiden Stellen im
            # HTML gepatcht ist -- und genau die zweite, die Nutzlast, entscheidet nach
            # der Hydration. Am 2026-11-18 beim Negativtest aufgefallen: Eine von Hand
            # zurückgedrehte Markup-Stelle blieb unentdeckt.
            for pfad, erwartet in kandidaten:
                if not pfad.exists():
                    continue
                t = pfad.read_text(encoding="utf-8")
                if (t.count(MARKE) != erwartet or ANKER in t
                        or t.count(url) < erwartet or datum not in t):
                    fehlend.append(
                        f"{pfad.relative_to(root)} ({t.count(MARKE)}x Marke, "
                        f"{t.count(ANKER)}x unveränderter Anker, erwartet {erwartet}x)")
            continue
        for pfad, erwartet in kandidaten:
            if not pfad.exists():
                continue
            n = patche(pfad, url, datum, erwartet)
            if n == -1:
                uebersprungen += 1
            else:
                getan += n

    voll = root / "llms-full.txt"
    if voll.exists():
        if args.check:
            t = voll.read_text(encoding="utf-8")
            if t.count(MARKE) != len(je_url):
                fehlend.append(f"llms-full.txt ({t.count(MARKE)} von {len(je_url)})")
        else:
            n = llms_full(voll, je_url)
            if n == -1:
                uebersprungen += 1
            elif n != len(je_url):
                print(f"✗ llms-full.txt: {n} Abschnitte gepatcht, {len(je_url)} erwartet")
                return 1
            else:
                getan += n

    if args.check:
        if fehlend:
            print(f"✗ Zitierzeile fehlt oder ist falsch in {len(fehlend)} Datei(en):")
            for f in fehlend[:10]:
                print(f"    {f}")
            return 1
        print(f"✓ Zitierzeile auf {len(je_url)} Seiten, in HTML, Seiten-JSON, Markdown "
              f"und llms-full.txt")
        return 0

    if not je_url:
        print("✗ keine Seite mit Herkunftszeile gefunden -- Text geändert?")
        return 1
    print(f"✓ Stand und Adresse in die Herkunftszeile von {len(je_url)} Seiten: "
          f"{getan} Ersetzungen"
          + (f", {uebersprungen} Dateien waren schon gepatcht" if uebersprungen else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
