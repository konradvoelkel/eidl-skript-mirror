#!/usr/bin/env python3
"""Jede Seite und jeden Sitemap-Eintrag mit dem Datum ihrer letzten Änderung versehen.

    python3 tools/freshness.py <html-verzeichnis> [--check]

Nach dem Bau auf `public/` laufen zu lassen.

Port aus ds-skript, am 2026-11-03 für eidl angepasst: die Zuordnung Datei zu Slug (siehe
`pages()`), und `--stamp-source` (das sichtbare Datum auf der Landingpage) ist hier nicht
verdrahtet. `inject_jsonld.py` liest sein `dateModified` hier weiter selbst aus `git log`
derselben Quelldateien, die beiden Angaben haben also eine Herkunft. Der Text unten ist
der von ds-skript; in eidl stand am 2026-11-03 ebenfalls `<lastmod>` in null von 32
Einträgen.

Warum überhaupt
---------------
Dieses Buch wird laufend gepflegt, aber **keine einzige Seite sagte das** (gemessen am
Live-Stand 2026-10-16: kein Datum im `<head>`, keins im Text, `<lastmod>` in null von 32
Sitemap-Einträgen). Für AI-Antwortsysteme ist Aktualität eines der stärksten
Auswahlsignale — wir haben sie und haben sie verschenkt.

Woher das Datum kommt
---------------------
Aus `git log` der *Quelldatei*, nicht aus der Bauzeit. Ein Bau am Dienstag macht ein
Kapitel von 2024 nicht frisch; ein Datum, das das behauptet, wäre schlechter als gar
keins. Deshalb gibt es hier auch **keine Rückfallebene auf die Uhr**: liefert git für
eine Datei nichts, bricht das Skript ab, statt etwas Plausibles zu erfinden.

Das heißt, der Job braucht eine **vollständige Historie**. GitLab klont standardmäßig
flach (`GIT_DEPTH: 20`); eine Datei, die seit zwanzig Commits unberührt ist, hat dann
keinen Eintrag. `variables: GIT_DEPTH: "0"` im Job ist deshalb Pflicht, und die
Fehlermeldung unten sagt das auch.

Nicht enthalten: ein *sichtbares* Datum auf der Seite. Das Theme rendert den Seitenkopf
aus einem eingebetteten JSON-Block neu, eine ins Markup geschriebene Zeile wäre nach der
Hydration wieder weg. Der saubere Weg dafür ist `date:` im Frontmatter — eine
Quelltextänderung, und die wartet auf Zuruf.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = '<meta property="article:modified_time" content="{date}"/>'


def toc_files(toc) -> list[str]:
    """Alle Dateien der Inhaltsübersicht, in Lesereihenfolge."""
    out: list[str] = []
    for entry in toc:
        if "file" in entry:
            out.append(entry["file"])
        for child in entry.get("children", []):
            out.extend(toc_files([child]))
    return out


def project(html: Path) -> dict:
    """Der Projektblock aus der gebauten config.json.

    Bewusst nicht aus myst.yml: der `pages`-Job läuft auf python:3.13-alpine ohne
    PyYAML, und config.json enthält dieselben Angaben als reines JSON.
    """
    cfg = json.loads((html / "config.json").read_text(encoding="utf-8"))
    return cfg["projects"][0]


def _git(args: list[str]) -> subprocess.CompletedProcess:
    """git aufrufen und „git ist gar nicht da" an *einer* Stelle beantworten.

    Beide Aufrufer brauchen das, und refuse_shallow() läuft zuerst: ohne diesen Helfer
    stirbt ein fehlendes git dort mit einem nackten FileNotFoundError, der nichts
    Brauchbares nennt. Genau dieser Ausfall war `5b7818b` — python:3.13-alpine bringt
    kein git mit. Die Faktorisierung ist aus `ds-en` übernommen, das sie beim Portieren
    gefunden hat.
    """
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    except FileNotFoundError:
        raise SystemExit(
            "✗ git ist nicht installiert, also ist aus der Historie kein Datum zu lesen.\n"
            "  Welcher Griff hilft, haengt am Image des Jobs -- die Meldung nannte hier\n"
            "  bis zum 2026-10-16 nur Alpine und schickte damit beim Ausfall von\n"
            "  build-web in das falsche Image:\n"
            "    python:3.13-alpine (pages, hreflang-map): apk add --no-cache git\n"
            "    $CI_REGISTRY_IMAGE (build-web, build-pdf): git gehoert ins Dockerfile,\n"
            "      dann baut build-image es mit; nachinstallieren je Job waere doppelt."
        )


def refuse_shallow() -> None:
    """Abbrechen, wenn der Klon flach ist — bevor ein einziges Datum gelesen wird.

    Diese Prüfung kommt aus `ds-en` zurück und schliesst ein Loch im hiesigen Entwurf.
    Die Annahme war: bei einem flachen Klon liefert `git log` für eine unberührte Datei
    *nichts*, und dann bricht git_date() ab. Das stimmt für GitLabs `GIT_DEPTH: 20`.

    Es stimmt **nicht** für Tiefe 1. Gegen einen Commit ohne Eltern meldet git *jede*
    Datei als von ihm geändert, `git log -1 -- <datei>` antwortet also für alle 32 — mit
    dem Zeitstempel von HEAD. Das Skript läuft glatt durch und meldet Erfolg. ds-en hat
    das an einem `git clone --depth 1` nachgemessen: alle 30 Seiten auf die Sekunde des
    Deploy-Commits datiert, wo die echten Daten über drei Tage streuen.

    Das ist genau das Bauzeit-Datum, dessen Verhinderung der Zweck dieser Datei ist —
    erreicht über den einen Weg, den der Wächter nicht abdeckte, und stumm, weil die
    Ausgabe wie ein korrekter Lauf aussieht. Also wird die Tiefe direkt behauptet statt
    aus einer fehlenden Antwort geschlossen.
    """
    if _git(["rev-parse", "--is-shallow-repository"]).stdout.strip() == "true":
        raise SystemExit(
            "✗ das ist ein flacher Klon. git würde für jede Datei das Datum von HEAD\n"
            "  melden, und jede Seite behauptete, im Moment des Deploys geändert worden\n"
            "  zu sein. Der Job braucht\n"
            '    variables:\n      GIT_DEPTH: "0"\n'
            "  Erfunden wird hier nichts."
        )


def git_date(name: str) -> str:
    """ISO-8601-Datum des letzten Commits, der diese Datei angefasst hat."""
    res = _git(["log", "-1", "--format=%cI", "--", name])
    if res.returncode != 0:
        # Ein Fehler von git ist etwas anderes als "git kennt diese Datei nicht", und die
        # beiden zu verwechseln kostete beim Bauen eine halbe Stunde Fehlersuche: bei einem
        # Rechteproblem meldete das Skript "flacher Klon" und schickte in die falsche Richtung.
        raise SystemExit(f"✗ git scheiterte fuer {name}:\n  {res.stderr.strip()}")
    date = res.stdout.strip()
    if not date:
        raise SystemExit(
            f"✗ git kennt kein Datum für {name}.\n"
            f"  Bei einem flachen Klon ist das der Normalfall. Der Job braucht\n"
            f"  variables:\n    GIT_DEPTH: \"0\"\n"
            f"  Erfunden wird hier nichts."
        )
    return date


def pages(html: Path) -> list[tuple[str, Path, str]]:
    """(slug, index.html, datum) je Seite. Der erste toc-Eintrag ist die Startseite.

    Die Startseite bekommt nicht ihr eigenes git-Datum, sondern das **jüngste aller
    Seiten**. Sie ist das Titelblatt des Buchs, nicht ein Kapitel: `inject_jsonld.py`
    liest ihr `article:modified_time` als `dateModified` des Werks zurück, und das Werk
    hat sich geändert, sobald irgendein Kapitel sich geändert hat. Ohne diese Ausnahme
    veraltete die Angabe, sobald monatelang nur Kapitel angefasst werden.
    """
    refuse_shallow()
    proj = project(html)
    files = toc_files(proj["toc"])
    # In eidl heißen die Kapitel anders als ihre Dateien (08-gradientenabstieg.md wird
    # /gradientenabstieg/), anders als in ds-skript, wo der Dateiname der Slug ist. Den
    # Slug liefert `pages` in config.json, in derselben Reihenfolge wie `toc` -- dieselbe
    # Zuordnung wie in inject_jsonld.py, und wie dort gezählt statt angenommen.
    slugs = [e["slug"] for e in proj.get("pages", []) if "slug" in e]
    if len(slugs) != len(files) - 1:
        raise SystemExit(f"✗ config.json nennt {len(files)} toc-Dateien und {len(slugs)} "
                         "Slugs; die Zuordnung Datei zu Slug ist nicht mehr die Reihenfolge")
    out = []
    for n, name in enumerate(files):
        slug = "" if n == 0 else slugs[n - 1]
        target = html / "index.html" if n == 0 else html / slug / "index.html"
        if not target.exists():
            raise SystemExit(f"✗ {target} fehlt; toc und Bau sind sich uneinig")
        out.append((slug, target, git_date(name)))
    if out:
        newest = max(date for _, _, date in out)
        out[0] = (out[0][0], out[0][1], newest)
    return out


def book_date(html: Path) -> str:
    """Das jüngste Seitendatum — das Datum des Werks als Ganzes."""
    return max(date for _, _, date in pages(html))


def stamp_html(entries) -> int:
    done = 0
    for _, target, date in entries:
        page = target.read_text(encoding="utf-8")
        if "article:modified_time" in page:
            continue
        target.write_text(page.replace("</head>", META.format(date=date) + "</head>", 1),
                          encoding="utf-8")
        done += 1
    return done


def stamp_sitemap(html: Path, entries) -> int:
    """<lastmod> in jeden <url>-Block schreiben, zugeordnet über den letzten Pfadteil.

    Über den Pfad und nicht über die volle URL, damit der Schritt unabhängig davon ist,
    ob die Origin-Ersetzung im Job vorher oder nachher läuft.
    """
    path = html / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")
    if "<lastmod>" in xml:
        return 0
    by_slug = {slug: date for slug, _, date in entries}
    hits = 0

    def add(match: re.Match) -> str:
        nonlocal hits
        block, loc = match.group(0), match.group(1)
        slug = loc.rstrip("/").rsplit("/", 1)[-1]
        date = by_slug.get(slug if slug in by_slug else "")
        if date is None:
            return block
        hits += 1
        return block.replace("</loc>", f"</loc><lastmod>{date}</lastmod>", 1)

    path.write_text(re.sub(r"<url>\s*<loc>([^<]+)</loc>", add, xml), encoding="utf-8")
    return hits


def stamp_source() -> int:
    """Das Datum der Ausgabe in den Frontmatter der Landingpage schreiben.

    Das ist die *sichtbare* Hälfte, und sie steht bewusst nur auf dieser einen Seite.
    MyST 1.10.1 rendert ein Projekt-Datum aus `myst.yml` auf allen 32 Seiten gleich
    (am 2026-10-16 gemessen), und 16 davon hätten damit ein Datum behauptet, das ihr
    Quelltext nicht hergibt. Auf dem Titelblatt dagegen ist „Stand der Ausgabe" genau die
    richtige Aussage, und es ist derselbe Wert, den die Seite als `article:modified_time`
    und als `dateModified` des Werks ohnehin trägt.

    Mitzuwissen: Das Theme formatiert hart englisch („October 16, 2026"). `language: de`
    ändert daran nichts (geprüft), und eine deutsche Zeichenkette wirft MyST still weg
    (`"date":""`). Das ist der Preis dieser Zeile, bewusst bezahlt.

    Läuft **vor** dem Bau und schreibt in den Quelltext; das Ergebnis wird nicht
    eingecheckt. Lokal ohne diesen Schritt zu bauen heisst nur: kein Datum auf der Seite.
    """
    import yaml  # absichtlich lokal: der pages-Job hat kein PyYAML und braucht es nicht

    refuse_shallow()
    cfg = yaml.safe_load((ROOT / "myst.yml").read_text(encoding="utf-8"))
    files = toc_files(cfg["project"]["toc"])
    date = max(git_date(f) for f in files)[:10]  # nur der Tag; die Uhrzeit wäre Lärm

    landing = ROOT / files[0]
    text = landing.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SystemExit(f"✗ {landing.name} hat keinen Frontmatter")
    end = text.find("\n---", 4)
    if end < 0:
        raise SystemExit(f"✗ {landing.name}: Frontmatter nicht abgeschlossen")

    head, rest = text[:end], text[end:]
    if re.search(r"(?m)^date:", head):
        head = re.sub(r"(?m)^date:.*$", f"date: {date}", head)
    else:
        head = head.rstrip("\n") + f"\ndate: {date}"
    landing.write_text(head + rest, encoding="utf-8")
    print(f"✓ {landing.name}: Stand der Ausgabe auf {date} gesetzt")
    return 0


def main() -> int:
    if "--stamp-source" in sys.argv:
        return stamp_source()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    html = Path(args[0])
    entries = pages(html)

    if "--check" in sys.argv:
        pages_without = [str(t) for _, t, _ in entries
                         if "article:modified_time" not in t.read_text(encoding="utf-8")]
        stamps = (html / "sitemap.xml").read_text(encoding="utf-8").count("<lastmod>")
        if pages_without or stamps != len(entries):
            print(f"✗ {len(pages_without)} Seiten ohne Datum, "
                  f"{stamps} von {len(entries)} Sitemap-Einträgen mit <lastmod>")
            for p in pages_without[:5]:
                print(f"    {p}")
            return 1
        print(f"✓ {len(entries)} Seiten mit Datum, {stamps} Sitemap-Einträge mit <lastmod>")
        return 0

    n_html, n_map = stamp_html(entries), stamp_sitemap(html, entries)
    print(f"✓ {n_html} Seiten datiert, {n_map} Sitemap-Einträge mit <lastmod>; "
          f"jüngste Änderung {book_date(html)[:10]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
