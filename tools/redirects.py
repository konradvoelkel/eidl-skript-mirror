#!/usr/bin/env python3
"""Versuch, aus der `302` ohne Schrägstrich eine `301` zu machen.

    python3 tools/redirects.py <html-verzeichnis> [--check]

Im `pages`-Job **nach** `publish_urls.py` laufen lassen: Die Liste der Adressen kommt aus
der fertigen `sitemap.xml`.

Worum es geht
-------------
`https://…/autoencoder` ohne Schrägstrich beantwortet GitLab Pages mit **302** auf
`…/autoencoder/`. Das ist dokumentiertes Verhalten und kein Defekt dieser Seite -- GitLabs
Dokumentation zeigt unter „Resolving ambiguous URLs" für `/data` genau
„302 Found: redirecting to /data/" --, aber eine *temporäre* Weiterleitung behauptet, die
Quelle bleibe die eigentliche Adresse, und das ist das Gegenteil dessen, was der Canonical
sagt. Dazu passt die eine Dublette, die sich nicht aus einem alten Crawl erklärt:
`perzeptron-trainieren` nennt den Canonical **mit** Schrägstrich, Google wählt die Variante
**ohne** (SEO-Audit 2026-11-18, §18.1).

Innerhalb der Seite ist das längst erledigt: `tools/trailing_slash.py` bringt jeden internen
Link auf die Form mit Schrägstrich. Übrig bleibt, wer von außen auf die kurze Form zeigt --
und der Crawler, der sie dann so behandelt, wie eine `302` es sagt.

Was dieses Skript versucht, und was offen ist
----------------------------------------------
GitLab Pages liest eine Datei `_redirects` im Wurzelverzeichnis des Artefakts; `301` ist
dort erlaubt und sogar die Vorgabe, wenn kein Code dasteht (Grenzen: 64 kB und 1.000
Regeln, hier 32 Zeilen). **Ob eine solche Regel vor der eingebauten Weiterleitung greift,
sagt die Dokumentation nicht.** Sie sagt nur „Files take priority over redirects. If a file
exists on disk, GitLab Pages serves the file instead of your redirect" -- das betrifft
Dateien, nicht die Auflösung mehrdeutiger Adressen. Erzwingen wie bei Netlify (`301!`)
unterstützt GitLab ausdrücklich nicht; genau darum geht das offene Issue
gitlab-org/gitlab#565802, und gitlab-pages#418 meldet die `302` seit Jahren als
SEO-Problem.

Der Versuch kostet nichts und kann nichts kaputt machen: Das Ziel jeder Regel ist genau die
Adresse, auf die die eingebaute Weiterleitung ohnehin zeigt. Greift die Regel, wird aus der
`302` eine `301`; greift sie nicht, liegt eine Datei im Artefakt, die niemand liest.

**Gemessen wird nach dem Deploy**, nicht hier:

    curl -sS -o /dev/null -w '%{http_code}\\n' https://…/autoencoder

`301` heißt, es hat geklappt. Bleibt es bei `302`, gehört dieses Skript wieder heraus --
dann ist die Frage endgültig beantwortet und die Antwort lautet nein.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

DATEI = "_redirects"
KOPF = (
    "# Erzeugt von tools/redirects.py -- nicht von Hand ändern.\n"
    "# Aus der eingebauten 302 ohne Schrägstrich eine 301 machen; ob das greift,\n"
    "# steht im Docstring des Skripts.\n"
)


def pfade(html: pathlib.Path) -> list[str]:
    """Die Pfade aus der Sitemap, ohne die Wurzel, jeweils ohne Schrägstrich am Ende."""
    sitemap = html / "sitemap.xml"
    if not sitemap.is_file():
        sys.exit(f"FEHLER: {sitemap} gibt es nicht -- nach publish_urls.py laufen lassen")
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap.read_text(encoding="utf-8"))
    out = []
    for u in locs:
        pfad = re.sub(r"^https?://[^/]+", "", u)
        if not pfad.endswith("/") or pfad == "/":
            continue            # die Wurzel hat keine kurze Form
        kurz = pfad.rstrip("/")
        if (html / kurz.lstrip("/")).is_file():
            continue            # da liegt eine Datei, die Regel wäre wirkungslos
        out.append(kurz)
    return sorted(set(out))


def inhalt(kurz: list[str]) -> str:
    return KOPF + "".join(f"{k} {k}/ 301\n" for k in kurz)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("html", type=pathlib.Path)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    kurz = pfade(args.html)
    if not kurz:
        sys.exit("FEHLER: keine Kapitelpfade in der Sitemap gefunden")
    ziel = args.html / DATEI
    soll = inhalt(kurz)

    if args.check:
        if not ziel.is_file():
            print(f"✗ {DATEI} fehlt im Artefakt")
            return 1
        if ziel.read_text(encoding="utf-8") != soll:
            print(f"✗ {DATEI} stimmt nicht mit der Sitemap überein")
            return 1
        if len(soll.encode()) > 64 * 1024 or len(kurz) > 1000:
            print(f"✗ {DATEI} über der Grenze von GitLab Pages (64 kB, 1.000 Regeln)")
            return 1
        print(f"✓ {DATEI}: {len(kurz)} Regeln, passend zur Sitemap")
        return 0

    ziel.write_text(soll, encoding="utf-8")
    print(f"✓ {DATEI} geschrieben: {len(kurz)} Regeln auf die Form mit Schrägstrich")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
