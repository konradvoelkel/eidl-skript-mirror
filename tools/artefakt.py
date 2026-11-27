#!/usr/bin/env python3
"""Wo im gebauten Artefakt die mitkopierten Dateien liegen -- einmal, nicht zwölfmal.

Theme 1.4.x legt Abbildungen, Karte und Stylesheets unter **`build/`** ab
(`/build/vl06-two-neurons-3f2a….png`), Theme 2.x unter **`_public/`**. Fünf Skripte in
`tools/` bauen oder lesen diese Adresse an dreizehn Stellen; vor diesem Modul stand
`"/build/"` dreizehnmal wörtlich im Code, und ein Themenwechsel hätte jede Stelle einzeln
gefunden werden müssen.

**Erkannt, nicht konfiguriert.** Der `pages`-Job muß nicht wissen, welches Theme gebaut
hat, und ein Rückschritt auf 1.4.1 kostet keine Zeile: Welcher Ordner es ist, steht am
Artefakt selbst. Für reine Zeichenkettenarbeit genügt `spalte()`, das beide Namen
akzeptiert und deshalb ohne das Verzeichnis auskommt.

Nicht hier drin: der Ort des **Stylesheets** (`build/_assets/app-<hash>.css` gegen
`_assets/root-<hash>.css`). Den sucht `tools/dead_css.py` über seine eigenen Muster, und
`tools/check_css_assets.py` löst auf, was darin steht -- beide hängen am Inhalt des
`<link>`-Tags und nicht an einem geratenen Pfad.
"""

from __future__ import annotations

import pathlib
import re
import sys

#: Die Ordnernamen, unter denen die beiden Themegenerationen ihre Dateien ablegen.
ORDNER = ("build", "_public")

#: Dieselben Namen als Adressteil. Beide zugleich, damit eine Zeichenkette ohne
#: Kenntnis des Verzeichnisses zerlegt werden kann.
RX = re.compile(r"/(" + "|".join(ORDNER) + r")/")


def ordner(wurzel: pathlib.Path) -> str:
    """Der Name des Dateiordners dieses Artefakts, am Verzeichnis erkannt."""
    for name in ORDNER:
        if (wurzel / name).is_dir():
            return name
    sys.exit(f"FEHLER: in {wurzel} liegt weder {' noch '.join(ORDNER)} — "
             f"kein gebautes Artefakt, oder das Theme hat den Ordner umbenannt")


def pfad(wurzel: pathlib.Path) -> pathlib.Path:
    """Der Dateiordner als Pfad."""
    return wurzel / ordner(wurzel)


def praefix(wurzel: pathlib.Path) -> str:
    """Der Dateiordner als Adressteil, mit Schrägstrichen: `/build/` oder `/_public/`."""
    return f"/{ordner(wurzel)}/"


def spalte(url: str) -> tuple[str, str, str] | None:
    """Eine Artefakt-Adresse am Dateiordner zerlegen, am **letzten** Vorkommen.

    Gibt `(davor, ordnername, danach)` oder `None`, wenn die Adresse nicht in den
    Dateiordner zeigt. Am letzten Vorkommen, weil die Adresse absolut sein kann und der
    Basispfad der Seite selbst `build` heißen könnte.

    >>> spalte("https://example.org/buch/build/karte.png")
    ('https://example.org/buch', 'build', 'karte.png')
    >>> spalte("/_public/vl06.webp")
    ('', '_public', 'vl06.webp')
    >>> spalte("/images/vl06.png") is None
    True
    """
    letzte = None
    for m in RX.finditer(url):
        letzte = m
    if letzte is None:
        return None
    return url[:letzte.start()], letzte.group(1), url[letzte.end():]


if __name__ == "__main__":
    import doctest

    fehler = doctest.testmod().failed
    if len(sys.argv) > 1:
        wurzel = pathlib.Path(sys.argv[1])
        print(f"Dateiordner: {ordner(wurzel)} ({pfad(wurzel)})")
    raise SystemExit(1 if fehler else 0)
