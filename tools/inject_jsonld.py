#!/usr/bin/env python3
"""Die JSON-LD-Beschreibung des Buchs und jedes Kapitels in das gebaute HTML schreiben.

    python3 tools/inject_jsonld.py <site-url> <html-verzeichnis>

Nach `tools/publish_urls.py` und `tools/head_meta.py` laufen lassen: Beide Werte, die
hier aus der Seite zurückgelesen werden -- die absolute Karten-URL und der Kapiteltitel
--, stammen von dort. MyST emittiert keine strukturierten Daten, und der Block kann nicht
im Markdown stehen: eine `{raw} html`-Direktive landete im PDF-Export.

Portiert aus ds-en `tools/inject_jsonld.py` (2026-10-19). Was anders ist, steht unten
unter „Was hier anders ist als in ds-en".


Ein Buch, 29 Kapitel, ein Autor
--------------------------------

Ein Kapitel bekommt kein zweites `Book`. Es bekommt ein
`["Chapter","LearningResource"]` mit eigenem `@id` (`.../<slug>/#chapter`) und einem
`isPartOf` auf den einen Buchknoten, der einen festen `@id` hat. Der Autor ist derselbe
Zug eine Ebene tiefer: Die `Person` wird einmal ausgeschrieben, auf der Landingpage, mit
`@id` `.../#author`, und jedes Kapitel verweist auf diesen `@id`, statt Namen,
Profile und Zugehörigkeit 29-mal zu wiederholen.

Der `author` eines Kapitels ist bewusst der nackte `{"@id": …}`-Verweis, ohne `@type`
und `name` daneben: Google liest ein Dokument zur Zeit, auf einer Kapitelseite behauptet
der Verweis also eine Identität und sonst nichts; die Eigenschaften sind einen Abruf der
Landingpage entfernt.

Nicht behauptet wird `Course` samt `hasCourseInstance` und `provider`. Das Skript
*gehört* zu einer Lehrveranstaltung der HHU, aber diese Seite ist nicht deren
Anmeldeseite -- das läuft über ILIAS. Die Zugehörigkeit des Autors stimmt und bleibt.


Drei Werke, ein Autor
---------------------

Im Oktober 2026 antwortete ChatGPT auf die Frage, wie viele Vorlesungsskripte Konrad
Völkel geschrieben habe, es könne „keine verlässliche Gesamtzahl" bestätigen -- und hängte
an dieses Buch ein fremdes Bild. Die einzige Quelle für die Zahl war ein Absatz in Prosa
auf der Landingpage **einer** der drei Ausgaben; dieses Buch sagte maschinenlesbar gar
nichts, weder über sich noch über seinen Autor (ds-en `SEO-NOTES.md` §21).

Deshalb trägt die Landingpage einen `@graph`: den Buchknoten und die beiden anderen Werke
aus `tools/sibling-works.json`, jedes ein `["Book","LearningResource"]`, dessen `author`
derselbe `{"@id": …}`-Verweis ist. Mehr wird über sie nicht behauptet, als ihre eigene
`myst.yml` hergibt -- Titel, Sprache, Lizenz, Art und Niveau --, weil diese Seite nicht
ihr Herausgeber ist.

Eine `Person` hat in schema.org keine Eigenschaft „Werke", deshalb wird das von der Seite
der Werke gesagt und nicht von der des Autors. Deshalb auch keine `ItemList`: Eine Liste
von dreien ist eine Behauptung über den Inhalt einer Seite, drei Knoten mit demselben
`author` eine Behauptung über die Welt -- und gemeint ist die zweite.


Die `@id`s und die zwei Adressen dieser Seite
----------------------------------------------

Diese Seite ist unter zwei Adressen erreichbar: Die lesbare Namensraum-URL
`https://voelkel.pages.cs.uni-duesseldorf.de/eidl-skript/` antwortet mit **308** auf
`https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de/` -- GitLabs „unique domain" ist
in diesem Projekt eingeschaltet (in `eipy-skript` auch, in `ds-skript` nicht).

**Konrad hat das am 2026-10-19 entschieden: Der generierte Host ist der kanonische.**
Ein Canonical, der weiterleitet, ist keiner. Also nennt alles den generierten Host --
`canonical`, `og:url`, jede `<loc>`, `url` **und der `@id`**. Der `@id` steht deshalb als
`__SITE__/#work` in der Vorlage und nicht als feste Zeichenkette: Er kann dann nicht von
`SITE_ORIGIN` abdriften.

Die erste Fassung dieses Repos hielt den `@id` auf der lesbaren URL fest, weil ds-ens
`sibling-works.json` ihn so behauptete. Das war dieselbe Spaltung von der anderen Seite:
`eipy-skript` leitete seinen `@id` vom generierten Host ab, dieses Repo schrieb die
lesbare URL hart hinein, und der Graph beschrieb zwei Werke statt eines. ds-en,
ds-skript, eipy-skript und `konradvoelkel.com` sind seither alle auf die generierten
Hosts umgestellt (ds-en `SEO-NOTES.md` §21a).

**Der Preis, und er gehört genannt:** Der Bezeichner ist jetzt ein undurchsichtiger
Hostname, den GitLab vergibt. Wird „unique domain" je abgeschaltet, wandern alle diese
Dateien mit -- in vier Repositorien. Die lesbare Adresse bleibt als `sameAs` am
Buchknoten stehen, damit die zweite Schreibweise nicht verlorengeht.

Das Datum kommt aus `git log`, nicht von der Uhr
--------------------------------------------------

`dateModified` je Kapitel ist der Zeitstempel des letzten Commits, der die **Quelldatei**
berührt hat; das Datum des Buchs ist das neueste davon, nicht das der Landingpage -- die
beschriebene Entität ist das Werk als Ganzes, und ein heute überarbeitetes Kapitel macht
das Buch heute geändert.

Keine Rückfallebene auf die Bauzeit: Ein Bau am Dienstag macht ein Kapitel vom September
nicht frisch, und ein Datum, das das behauptet, ist schlechter als keines -- derselbe
Fehlertyp wie die Sitemap, die auf `localhost` zeigte. Liefert git nichts, bricht das
Skript ab.

Ein **flacher Klon** wird vorher abgewiesen, und zwar direkt statt über ein fehlendes
Ergebnis: Gegen einen Commit ohne Eltern meldet git *jede* Datei als von ihm geändert,
`git log -1 -- <datei>` antwortet also für alle 30 -- mit dem Zeitstempel von HEAD. Das
Skript liefe glatt durch, und jede Seite behauptete, im Moment des Deploys geändert
worden zu sein. Deshalb `GIT_DEPTH: "0"` im `pages`-Job.


Der Kapitelname ohne den Buchtitel
-----------------------------------

MyST setzt in `<title>` und `og:title` jeder Kapitelseite den Projekttitel als Suffix:
„Backpropagation - Einführung in Deep Learning". Als `name` eines `Chapter`-Knotens und
als Brotkrume ist das falsch -- das Kapitel heißt „Backpropagation", das Buch steht schon
in `isPartOf` daneben. Der Suffix wird deshalb hier abgeschnitten, und zwar **nur für die
strukturierten Daten**.

ds-en kürzt ihn auch im `<title>` selbst (dessen Abschnitt 1, samt Eingriff in die
Hydrations-Nutzlast); ds-skript hat das bewusst nicht portiert, weil die Messung, die es
dort rechtfertigte, für einen kürzeren Suffix deutlich milder ausfällt. Das bleibt hier
ebenso: Die sichtbaren Titel bleiben unberührt, und der Suffix wird aus dem `<title>` der
Landingpage gelesen statt hart geschrieben -- ein Umbenennen in myst.yml trägt sich damit
von selbst durch.


Was hier anders ist als in ds-en
---------------------------------

* **Kein `freshness.py`.** Dort schreibt ein eigenes Skript `article:modified_time` in
  jeden Kopf und `<lastmod>` in jeden Sitemap-Eintrag, und dieses liest das Datum von
  dort zurück. Portiert ist nur der Teil, den die strukturierten Daten brauchen; die
  sichtbaren Daten und `<lastmod>` stehen als offener Punkt in `devnotes/TODO.md`.
* **Der `@id` des Buchs ist fest**, siehe oben.
* **Die Zuordnung Datei zu Slug** kommt aus `config.json`: `toc` nennt die Quelldateien
  in Lesereihenfolge, `pages` die Slugs in derselben Reihenfolge, und die Kapitel dieses
  Buchs heißen anders als ihre Dateien (`part-lernen/09-backpropagation.md` wird
  `/backpropagation/`). Beide Listen werden gegeneinander gezählt und gegen die gebauten
  Verzeichnisse geprüft, statt den Slug aus dem Dateinamen zu raten.


Zweimal laufen
--------------

Je Seite idempotent: Eine Seite, die schon einen `ld+json`-Block trägt, wird
übersprungen. Die Nachbedingungen laufen trotzdem über alle 30 Seiten -- genau ein Block
je Seite, jedes `isPartOf` auf dem `@id` des Buchs, jede Position wie im Inhaltsverzeichnis
--, damit auch ein Lauf, der nichts geschrieben hat, Markup auffallen lässt, das MyST
unter uns verschoben hat.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
VORLAGE = Path(__file__).resolve().parent / "structured-data.json"
GESCHWISTER = Path(__file__).resolve().parent / "sibling-works.json"


def _git(args: list[str]) -> subprocess.CompletedProcess:
    # check=False: Der Rückgabewert wird hier ausgewertet -- „git kennt diese Datei
    # nicht" ist etwas anderes als „git ist gescheitert", und die zwei zu
    # verwechseln schickt bei einem Rechteproblem in die falsche Richtung.
    return subprocess.run(["git", "-C", str(WURZEL), *args],
                          capture_output=True, text=True, check=False)


def flachen_klon_abweisen() -> None:
    if _git(["rev-parse", "--is-shallow-repository"]).stdout.strip() == "true":
        raise SystemExit(
            "✗ flacher Klon: git meldete für jede Datei das Datum von HEAD, und jede\n"
            "  Seite behauptete, im Moment des Deploys geändert worden zu sein.\n"
            '  Der Job braucht GIT_DEPTH: "0".'
        )


def git_datum(datei: str) -> str:
    res = _git(["log", "-1", "--format=%cI", "--", datei])
    if res.returncode != 0:
        raise SystemExit(f"✗ git scheiterte an {datei}: {res.stderr.strip()}")
    stamp = res.stdout.strip()
    if not stamp:
        raise SystemExit(
            f"✗ git kennt keinen Commit für {datei}. Ist die Datei neu und noch nicht\n"
            "  eingecheckt? Geraten wird hier nicht."
        )
    return stamp


def meta(doc: str, kind: str, name: str) -> str | None:
    """Der Inhalt eines <meta>, HTML-entschärft, oder None.

    Entschärft, weil der Wert in JSON wandert, wo `&#x27;` sechs Zeichen sind und kein
    Apostroph.
    """
    m = re.search(rf'<meta {kind}="{re.escape(name)}" content="([^"]*)"', doc)
    return html.unescape(m.group(1)) if m else None


def toc_seiten(projekt: dict) -> list[tuple[str, str, str | None]]:
    """(Slug, Quelldatei, Teiltitel) je Seite in Lesereihenfolge; Landingpage: Slug "".

    `toc` kennt die Dateien, `pages` die Slugs -- und die Kapitel dieses Buchs heißen
    anders als ihre Dateien. Beide Listen stehen in derselben Reihenfolge; das wird
    gezählt statt angenommen.
    """
    dateien: list[tuple[str, str | None]] = []

    def walk(entries, teil: str | None) -> None:
        for e in entries:
            if "file" in e:
                dateien.append((e["file"], teil))
            if e.get("children"):
                walk(e["children"], e.get("title", teil))

    walk(projekt["toc"], None)
    if not dateien:
        raise SystemExit("✗ das toc in config.json nennt keine Dateien")

    slugs = [e["slug"] for e in projekt.get("pages", []) if "slug" in e]
    if len(slugs) != len(dateien) - 1:
        raise SystemExit(
            f"✗ config.json nennt {len(dateien)} toc-Dateien und {len(slugs)} Slugs; "
            "die Zuordnung Datei zu Slug ist nicht mehr die Reihenfolge"
        )
    # Der erste toc-Eintrag ist die Landingpage; sie wird aus dem Wurzelpfad geliefert.
    out = [("", dateien[0][0], None)]
    out += [(slug, datei, teil) for slug, (datei, teil) in zip(slugs, dateien[1:])]
    return out


def buch_knoten(site: str) -> dict:
    return json.loads(VORLAGE.read_text(encoding="utf-8").replace("__SITE__", site))


def geschwister_knoten(site: str, buch: dict) -> list[dict]:
    knoten = json.loads(GESCHWISTER.read_text(encoding="utf-8").replace("__SITE__", site))
    for n in knoten:
        # Der Verweis muss innerhalb desselben Dokuments auflösen, sonst sagt der Graph
        # dreimal „irgendein Autor" statt dreimal „dieser Autor".
        if n["author"]["@id"] != buch["author"]["@id"]:
            raise SystemExit(
                f"✗ {GESCHWISTER.name}: {n['name']} nennt {n['author']['@id']}, "
                f"nicht den Autor des Buchs {buch['author']['@id']}"
            )
        if n["@id"] == buch["@id"]:
            raise SystemExit(f"✗ {GESCHWISTER.name}: {n['name']} benutzt den @id des Buchs")
    return knoten


def ohne_suffix(name: str, suffix: str | None) -> str:
    """Den Projekttitel-Suffix abschneiden, den MyST an jeden Kapiteltitel hängt."""
    if suffix and name.endswith(suffix):
        return name[: -len(suffix)].strip()
    return name


def kapitel_graph(site: str, slug: str, position: int, datum: str, doc: str,
                  buch: dict, suffix: str | None) -> dict:
    url = f"{site}/{slug}/"
    name = ohne_suffix(meta(doc, "property", "og:title"), suffix)
    kapitel = {
        "@type": ["Chapter", "LearningResource"],
        "@id": f"{url}#chapter",
        "url": url,
        "name": name,
        "description": meta(doc, "property", "og:description"),
        "isPartOf": {"@id": buch["@id"]},
        "position": position,
        # Aus dem Buchknoten, nicht wiederholt: Eine Stelle sagt, dass das Buch deutsch,
        # frei und CC BY-SA ist, und ein Kapitel kann davon nicht abdriften.
        "inLanguage": buch["inLanguage"],
        "isAccessibleForFree": buch["isAccessibleForFree"],
        "license": buch["license"],
        "author": {"@id": buch["author"]["@id"]},
        "dateModified": datum,
    }
    # Zwei Glieder, nicht drei: Für einen Teil („Grundlagen") gibt es keine Seite, und
    # ein ListItem ohne `item` lehnt Googles Rich Results Test ab -- dann wird gar keine
    # Brotkrume gezeichnet. Die Hierarchie steht ohnehin in `isPartOf` und `position`.
    brotkrumen = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": buch["name"], "item": f"{site}/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": url},
        ],
    }
    return {"@context": "https://schema.org", "@graph": [kapitel, brotkrumen]}


def landing_graph(site: str, doc: str, buch: dict, datum: str) -> dict:
    karte = re.search(r'<meta property="og:image" content="([^"]+)"', doc)
    if not karte:
        raise SystemExit("✗ die Landingpage hat kein og:image, auf das die "
                         "strukturierten Daten zeigen könnten")
    if not karte.group(1).startswith("http"):
        raise SystemExit(f"✗ die Landingpage hat ein relatives og:image: "
                         f"{karte.group(1)} -- lief tools/publish_urls.py vorher?")
    buch["image"] = karte.group(1)
    buch["dateModified"] = datum
    # Der Kontext wandert an den Graphen; ein Knoten darin mit eigenem Kontext ist
    # zulässig und Lärm.
    buch.pop("@context", None)
    return {"@context": "https://schema.org",
            "@graph": [buch, *geschwister_knoten(site, buch)]}


def block(payload: dict) -> str:
    """ensure_ascii, damit die Nutzlast jede Kodierungsüberraschung übersteht; "</" wird
    getrennt, weil ein wörtliches </script> das Element früh schlösse."""
    text = json.dumps(payload, ensure_ascii=True, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">{text}</script>'


def pruefen(site: str, root: Path, seiten: list[tuple[str, str, str | None]],
            buch: dict, suffix: str | None) -> int:
    for position, (slug, _, _) in enumerate(seiten, 1):
        ziel = root / "index.html" if not slug else root / slug / "index.html"
        doc = ziel.read_text(encoding="utf-8")
        bloecke = re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                             doc, re.S)
        if len(bloecke) != 1:
            print(f"✗ {ziel} trägt {len(bloecke)} ld+json-Blöcke, erwartet genau einen")
            return 1
        try:
            payload = json.loads(bloecke[0].replace("<\\/", "</"))
        except ValueError as exc:
            print(f"✗ {ziel} trägt ld+json, das nicht parst: {exc}")
            return 1
        graph = payload.get("@graph", [payload])

        if not slug:
            gefunden = next((n for n in graph if n.get("@id") == buch["@id"]), None)
            if not gefunden:
                print(f"✗ der Graph der Landingpage hat keinen Knoten {buch['@id']}")
                return 1
            andere = [n for n in graph if n is not gefunden]
            erwartet = geschwister_knoten(site, buch)
            if len(andere) != len(erwartet):
                print(f"✗ die Landingpage nennt {len(andere)} weitere Werke, "
                      f"{GESCHWISTER.name} führt {len(erwartet)}")
                return 1
            for n in andere:
                if n.get("author", {}).get("@id") != buch["author"]["@id"]:
                    print(f"✗ {n.get('name')} ist nicht {buch['author']['@id']} "
                          "zugeschrieben")
                    return 1
            buch["dateModified"] = gefunden.get("dateModified", "?")
            continue

        knoten = {
            tuple(n["@type"]) if isinstance(n["@type"], list) else n["@type"]: n
            for n in graph
        }
        kapitel = knoten.get(("Chapter", "LearningResource"))
        if not kapitel:
            print(f"✗ {ziel} hat keinen Chapter-Knoten")
            return 1
        if kapitel["isPartOf"]["@id"] != buch["@id"]:
            print(f"✗ {ziel} gehört zu {kapitel['isPartOf']['@id']}, nicht {buch['@id']}")
            return 1
        if kapitel["author"]["@id"] != buch["author"]["@id"]:
            print(f"✗ {ziel} nennt {kapitel['author']['@id']}, nicht den Autor des Buchs")
            return 1
        if kapitel["position"] != position:
            print(f"✗ {ziel} sagt Position {kapitel['position']}, "
                  f"das Inhaltsverzeichnis sagt {position}")
            return 1
        if "BreadcrumbList" not in knoten:
            print(f"✗ {ziel} hat keine BreadcrumbList")
            return 1
        for feld in ("name", "description", "dateModified"):
            if not kapitel.get(feld):
                print(f"✗ {ziel} hat ein leeres {feld} -- lief head_meta.py vorher?")
                return 1
        if suffix and kapitel["name"].endswith(suffix):
            print(f"✗ {ziel} trägt den Buchtitel noch im Kapitelnamen: "
                  f"{kapitel['name']!r}")
            return 1
    return 0


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    site, root = sys.argv[1].rstrip("/"), Path(sys.argv[2])
    if not (root / "index.html").exists():
        print(f"✗ {root / 'index.html'} fehlt; nach dem HTML-Bau laufen lassen")
        return 1

    flachen_klon_abweisen()
    projekt = json.loads((root / "config.json").read_text(encoding="utf-8"))["projects"][0]
    seiten = toc_seiten(projekt)
    buch = buch_knoten(site)

    daten = {slug: git_datum(datei) for slug, datei, _ in seiten}
    buch_datum = max(daten.values())

    # Der Suffix, den MyST an jeden Kapiteltitel hängt -- aus dem <title> der
    # Landingpage gelesen, der *der* Projekttitel ist, nicht hart geschrieben.
    m_titel = re.search(r"<title[^>]*>(.*?)</title>",
                        (root / "index.html").read_text(encoding="utf-8"), re.S | re.I)
    suffix = f" - {html.unescape(m_titel.group(1).strip())}" if m_titel else None

    geschrieben = uebersprungen = 0
    for position, (slug, _, _) in enumerate(seiten, 1):
        ziel = root / "index.html" if not slug else root / slug / "index.html"
        if not ziel.exists():
            print(f"✗ {ziel} fehlt; config.json und der Bau widersprechen sich")
            return 1
        doc = ziel.read_text(encoding="utf-8")
        if "application/ld+json" in doc:
            uebersprungen += 1
            continue

        if not slug:
            payload = landing_graph(site, doc, buch, buch_datum)
        else:
            if not meta(doc, "property", "og:title"):
                print(f"✗ {ziel} hat kein og:title, das das Kapitel benennen könnte")
                return 1
            if not meta(doc, "property", "og:description"):
                print(f"✗ {ziel} hat kein og:description")
                return 1
            payload = kapitel_graph(site, slug, position, daten[slug], doc, buch,
                                    suffix)

        if "</head>" not in doc:
            print(f"✗ {ziel} hat kein </head>")
            return 1
        ziel.write_text(doc.replace("</head>", block(payload) + "</head>", 1),
                        encoding="utf-8")
        geschrieben += 1

    if rc := pruefen(site, root, seiten, buch, suffix):
        return rc
    print(f"✓ strukturierte Daten auf {len(seiten)} Seiten: {geschrieben} geschrieben, "
          f"{uebersprungen} hatten schon einen Block; ein Buch ({buch['@id']}), "
          f"{len(seiten) - 1} Kapitel, {len(geschwister_knoten(site, buch))} weitere "
          f"Werke desselben Autors ({buch['author']['@id']}), "
          f"Stand {buch.get('dateModified', '?')[:10]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
