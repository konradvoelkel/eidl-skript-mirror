#!/usr/bin/env python3
"""Die Quelltexte des Buchs als Markdown ausliefern und in llms.txt verzeichnen.

    python3 tools/llms_txt.py <site-url> <html-verzeichnis>

Port aus ds-skript (dort `tools/llms_txt.py`, 2026-11-03). Im `pages`-Job laufen zu
lassen, nachdem die Origin im Bau steht. Drei Dinge:

  * den Quelltext jedes Kapitels als Markdown nach `<slug>.md` und `<slug>/index.md`
    schreiben;
  * `<link rel="alternate" type="text/markdown">` in den `<head>` jeder Seite, damit ein
    Werkzeug, das das HTML hat, den Quelltext findet, ohne zu raten;
  * `/llms.txt` (kurzes Verzeichnis in Lesereihenfolge) und `/llms-full.txt` (das ganze
    Buch in einer Datei) schreiben.

**Zur Einordnung, damit später niemand mehr davon erwartet als drinsteht:** Google sagt
in seinem eigenen Leitfaden zur AI-Optimierung (2026-05-15), dass `llms.txt` für die
Google-Suche weder hilft noch schadet. Der Nutzen liegt bei anderen Systemen und vor
allem bei der **Markdown-Auslieferung** – ein Kapitel als 20 KB Markdown statt als 150 KB
HTML ist für jeden Abrufer das bessere Angebot.

Zwei Unterschiede zu ds-skript:

  * Die Slugs kommen aus `pages` in `config.json`, nicht aus dem Dateinamen
    (`08-gradientenabstieg.md` wird `/gradientenabstieg/`) – dieselbe Zuordnung wie in
    `freshness.py` und `inject_jsonld.py`, und wie dort gezählt statt angenommen.
  * Die Schwesterskripten im Kopf kommen aus `tools/sibling-works.json`, derselben
    Quelle wie im JSON-LD, damit die beiden Angaben nicht auseinanderlaufen.

Gelesen wird `config.json` aus dem Bau statt `myst.yml`: derselbe Inhalt als reines JSON,
und der `pages`-Job läuft auf python:3.13-alpine ohne PyYAML.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

KOPF = """# {title}

> {description}

Ein offenes Lehrbuch von {author} ({affiliation}), CC BY-SA 4.0, zur Vorlesung
„Einführung in Deep Learning“ im Bachelor Informatik. Es setzt Python mit NumPy und die
lineare Regression voraus und führt vom einzelnen Neuron über Gradientenabstieg und
Backpropagation bis zu Autoencodern, Transformern und großen Sprachmodellen; Formeln
werden durchgerechnet, Code steht in PyTorch.

Jedes Kapitel unten verweist auf seinen Markdown-Quelltext (MyST). Das ganze Buch in
einer Datei steht unter {site}/llms-full.txt, als PDF unter {site}/eidl-skript.pdf

## Über den Autor

{author} lehrt an der {affiliation}, in der Arbeitsgruppe Dialog Systems and Machine
Learning. Seine eigene Seite ist https://www.konradvoelkel.com/, seine ORCID ist
0000-0002-4144-4199. Von ihm stammen außerdem, ebenfalls frei unter CC BY-SA 4.0:

{geschwister}

Alle sind Vorlesungsskripten für ein Informatik-Bachelorstudium, von ihrem Autor selbst
veröffentlicht, keine Bücher eines Verlags. Die vollständige Liste, mit den PDF-Ausgaben
und den Vorlesungsaufzeichnungen, steht unter https://www.konradvoelkel.com/teaching/

## Kapitel
"""


def toc_files(toc) -> list[str]:
    out: list[str] = []
    for entry in toc:
        if "file" in entry:
            out.append(entry["file"])
        for child in entry.get("children", []):
            out.extend(toc_files([child]))
    return out


def frontmatter_split(text: str) -> tuple[dict, str]:
    """(Frontmatter als dict, Rest). Ein winziger Parser statt PyYAML: gebraucht wird
    genau `title:` auf oberster Ebene."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-", "#")):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip("\"'")
    return fm, text[end + 4:].lstrip("\n")


def geschwister() -> str:
    zeilen = []
    for w in json.loads((ROOT / "tools" / "sibling-works.json").read_text(encoding="utf-8")):
        zeile = f"- **{w['name']}**, auf Deutsch, unter {w['url']}"
        if "workTranslation" in w:
            zeile += f" – die englische Übersetzung steht unter {w['workTranslation']['url']}"
        zeilen.append(zeile)
    return "\n".join(zeilen)


LINK = re.compile(r"\]\(([^)\s#:]+\.md)(#[^)\s]*)?\)")


def links_absolut(body: str, src: Path, seiten: dict[Path, str]) -> tuple[str, int]:
    """Relative Verweise auf Kapiteldateien (`../part-lernen/09-backpropagation.md`) zeigen
    auf der Seite ins Leere; sie werden zur Adresse der Kapitelseite. Unbekannte Ziele
    bleiben stehen und werden gezählt."""
    offen = 0

    def ersetze(m: re.Match) -> str:
        nonlocal offen
        ziel = (src.parent / m.group(1)).resolve()
        if ziel not in seiten:
            offen += 1
            return m.group(0)
        return f"]({seiten[ziel]}{m.group(2) or ''})"

    return LINK.sub(ersetze, body), offen


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    site, html = sys.argv[1].rstrip("/"), Path(sys.argv[2])

    project = json.loads((html / "config.json").read_text(encoding="utf-8"))["projects"][0]
    files = toc_files(project["toc"])
    slugs = [e["slug"] for e in project.get("pages", []) if "slug" in e]
    if len(slugs) != len(files) - 1:
        print(f"✗ config.json nennt {len(files)} toc-Dateien und {len(slugs)} Slugs; "
              "die Zuordnung Datei zu Slug ist nicht mehr die Reihenfolge")
        return 1
    author = project["authors"][0]["name"]
    aff_id = project["authors"][0]["affiliations"][0]
    affiliation = next((a["name"] for a in project.get("affiliations", []) if a.get("id") == aff_id), aff_id)

    seiten = {(ROOT / name).resolve(): f"{site}/" + ("" if n == 0 else f"{slugs[n - 1]}/")
              for n, name in enumerate(files)}
    index_lines, full_parts, unaufgeloest = [], [], 0

    for n, name in enumerate(files):
        src = ROOT / name
        if not src.exists():
            print(f"✗ {name} steht in der toc, aber nicht auf der Platte")
            return 1
        fm, body = frontmatter_split(src.read_text(encoding="utf-8"))
        title = fm.get("title") or src.stem
        body, offen = links_absolut(body, src, seiten)
        unaufgeloest += offen
        # Ein Kapitel, das seinen Titel schon als `#` trägt, bekommt ihn nicht doppelt.
        md_text = (body if body.startswith(f"# {title}\n") else f"# {title}\n\n{body}").rstrip() + "\n"

        if n == 0:
            page_url, md_rel, page_html = f"{site}/", "index.md", html / "index.html"
        else:
            slug = slugs[n - 1]
            page_url, md_rel = f"{site}/{slug}/", f"{slug}/index.md"
            page_html = html / slug / "index.html"
        if not page_html.exists():
            print(f"✗ {page_html} gibt es nicht; toc und Bau sind sich uneinig")
            return 1

        md_url = f"{site}/{md_rel}"
        out = html / md_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md_text, encoding="utf-8")
        # Eine zweite Kopie unter /<slug>.md, weil das die Form ist, die ein Werkzeug
        # zuerst rät.
        if n > 0:
            (html / f"{slugs[n - 1]}.md").write_text(md_text, encoding="utf-8")

        page = page_html.read_text(encoding="utf-8")
        if 'type="text/markdown"' not in page:
            tag = f'<link rel="alternate" type="text/markdown" href="{md_url}"/>'
            page_html.write_text(page.replace("</head>", tag + "</head>", 1), encoding="utf-8")

        index_lines.append(f"- [{title}]({md_url})" + (f": {fm['description']}" if fm.get("description") else ""))
        full_parts.append("=" * 80 + f"\nURL: {page_url}\nQUELLE: {md_url}\n" + "=" * 80 + f"\n\n{md_text}")

    kopf = KOPF.format(title=project["title"], description=project["description"], author=author,
                       affiliation=affiliation, site=site, geschwister=geschwister())
    (html / "llms.txt").write_text(kopf + "\n".join(index_lines) + "\n", encoding="utf-8")
    (html / "llms-full.txt").write_text(kopf + "\n".join(index_lines) + "\n\n" + "\n\n".join(full_parts),
                                        encoding="utf-8")

    if unaufgeloest:
        print(f"✗ {unaufgeloest} relative .md-Verweise ohne Kapitelseite; der HTML-Bau meldet sie als "
              "Cross-reference target not found")
        return 1
    size = (html / "llms-full.txt").stat().st_size
    print(f"✓ {len(files)} Seiten als Markdown, llms.txt verzeichnet, llms-full.txt {size // 1024} KiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
