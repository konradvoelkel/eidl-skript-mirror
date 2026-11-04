#!/usr/bin/env python3
"""Die Metadaten der Vorlesungsaufzeichnungen in der Mediathek prüfen und erzeugen.

    uv run --no-project devnotes/mediathek_seo.py            # prüfen, Vorschläge zeigen
    uv run --no-project devnotes/mediathek_seo.py --offline   # ohne Netz, nur Vorschläge
    uv run --no-project devnotes/mediathek_seo.py --vl 4       # nur eine Vorlesung

Warum es das gibt (2026-11-04)
------------------------------
Die HHU-Mediathek hat im Formular eines Mediums fünf Felder, die in der Seite als
Meta-Tags landen: `media[meta_title]`, `media[meta_description]`, `media[meta_keywords]`,
`media[meta_author]`, `media[meta_copyright]`. Bei VL 1 bis VL 4 sind **alle fünf leer**;
die Seite füllt die Lücke dann aus der Beschreibung. Das sieht man ihr an: in
`<meta name="description">` stehen die HTML-Tags der Beschreibung mit, escaped als
`&lt;p&gt;`, also beginnt der Suchtreffer-Text mit „<p>“.

Dazu kommt der **Umlaut-Fallstrick**, den Konrad bei jedem Upload von Hand ausbügelt: Der
Vorschlag der Mediathek für „SEO URL Titel“ (`media[slug]`) *löscht* Umlaute statt sie zu
umschreiben — aus „Einführung“ würde „einfhrung“. Bei VL 1 bis 4 steht überall korrekt
„einfuehrung“, der Griff sitzt also; geprüft wurde er nie. Dieselbe Löschung passiert
ungefragt in der `video:description` des Sitemaps („berblick ber die Vorlesung erste
N herungen“) — das ist Sache der Mediathek, nicht unsere, und mit einem Feld nicht zu
heilen; hier wird es nur gemeldet.

Die Datenquelle sind die Kapitel selbst, nichts wird erfunden: Jedes Kapitel, das eine
Aufzeichnung verlinkt, hat im Frontmatter ein `description:` von 80 bis 155 Zeichen
(Regel seit 2026-11-03, geprüft von `devnotes/check_doku.py`). Genau das ist eine
Meta-Beschreibung. Der Titel des Videos wird live gelesen, nie geraten, und daraus wird
der Slug berechnet, den die Mediathek haben *müßte*.

Was geprüft wird
----------------
1. Der Slug im Kapitel-Link ist der, den die Seite selbst als `og:url` nennt.
2. Der Slug ist die korrekte Umschrift des Videotitels (fängt „einfhrung“ und ein
   falsches Semester im Titel).
3. Der Titel nennt das Semester dieses Durchgangs (SEMESTER unten).
4. `<meta name="description">` enthält keine escapeten HTML-Tags, d.h. das Feld
   `meta_description` ist gefüllt.
5. Autor und Copyright stehen in der Seite.
Exit-Code 1, wenn etwas davon nicht stimmt.

Eintragen muß man die Vorschläge von Hand im Formular (`/media/edit/key/<hash>`); dieses
Skript schreibt nichts, es liest nur.

Was die fünf Felder wirklich tun (an VL 1 gemessen, 2026-11-04)
---------------------------------------------------------------
Kopf der Seite vorher und nachher verglichen, 49 gegen 51 Tags:

- `meta_description` **ist der Ertrag.** `<meta name="description">` enthielt vorher die
  Beschreibung samt escapeten HTML-Tags (der Text begann mit „<p>“), jetzt genau den
  gesetzten Satz. Die Seite wurde dadurch 412 Bytes kleiner.
- `meta_author` und `meta_copyright` erzeugen zwei Tags, die vorher ganz fehlten.
- `meta_keywords` **ersetzt** die Hausliste, es ergänzt sie nicht (siehe STICHWORTE_FEST).
- `meta_title` landet nur in `<meta name="title">`, und zwar mit dem Zusatz
  „ - Medien - HHU Mediathek“ dahinter. **Der echte `<title>` bleibt unberührt**, er kommt
  weiter aus `media[title]`; `og:title` ebenfalls. Suchmaschinen lesen `meta name="title"`
  nicht -- der Hebel auf die Überschrift im Suchergebnis ist also der Videotitel selbst,
  nicht dieses Feld. Es wird trotzdem gefüllt, damit das Feld nicht leer aussieht.
"""

import argparse
import pathlib
import re
import sys
import urllib.request

SEMESTER = "2026/27"
AUTOR = "Konrad Völkel"
EINRICHTUNG = "Heinrich-Heine-Universität Düsseldorf"
COPYRIGHT = "CC BY-ND 4.0, " + EINRICHTUNG   # nur als Rückfall, wenn die Seite nichts sagt


def kurz_lizenz(text):
    """Aus "Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)"
    das Kürzel in der Klammer machen; ohne Klammer den Text selbst."""
    m = re.search(r"\(([^)]+)\)\s*$", text.strip())
    return m.group(1) if m else text.strip()
# Das Feld ERSETZT die Hausliste der Mediathek ("eidl26 HHU,Mediathek,Video,Vorlesung,
# Vorlesungen,Heinrich-Heine,Universität,Düsseldorf,Vorlesungsaufzeichnung") vollständig --
# am 2026-11-04 an VL 1 gemessen. Deshalb stehen der Tag und die Hausbegriffe hier mit
# drin, sonst verliert die Seite sie.
STICHWORTE_FEST = ["Deep Learning", "Vorlesung", "Vorlesungsaufzeichnung", "eidl26",
                   "HHU", "Heinrich-Heine-Universität Düsseldorf", "Informatik"]
SKRIPT = "https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de/"

WURZEL = pathlib.Path(__file__).resolve().parent.parent
LINK = re.compile(
    r"\[Vorlesungsaufzeichnung VL (\d+): ([^\]]+)\]"
    r"\((https://media\.hhu\.de/video/([a-z0-9-]+)/([0-9a-f]{32}))\)"
)

# Die Mediathek löscht Umlaute im Slug-Vorschlag; richtig ist die Umschrift.
UMSCHRIFT = {
    "ä": "ae", "ö": "oe", "ü": "ue", "Ä": "ae", "Ö": "oe", "Ü": "ue", "ß": "ss",
}


def slug_aus_titel(titel):
    """Den Slug bilden, den die Mediathek bei korrekter Umschrift hätte.

    Abgelesen an VL 1 bis 3, nicht erfunden: Umlaute umschreiben, alles Übrige außer
    Buchstaben, Ziffern und Leerzeichen fallen lassen (aus „2026/27“ wird „202627“, der
    Doppelpunkt nach der VL-Nummer verschwindet), dann Leerzeichen zu Bindestrichen.
    """
    t = "".join(UMSCHRIFT.get(c, c) for c in titel).lower()
    t = re.sub(r"[^a-z0-9 ]+", "", t)
    return re.sub(r"\s+", "-", t.strip())


def frontmatter(pfad):
    text = pfad.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    kopf = text.split("---", 2)[1]
    felder = {}
    for zeile in kopf.splitlines():
        m = re.match(r'(\w+):\s*"?(.*?)"?\s*$', zeile)
        if m:
            felder[m.group(1)] = m.group(2)
    return felder


def videos_aus_kapiteln():
    """Alle Aufzeichnungen finden, die ein Kapitel verlinkt: VL -> Daten."""
    gefunden = {}
    for pfad in sorted(WURZEL.glob("part-*/*.md")):
        for nr, label, url, slug, key in LINK.findall(pfad.read_text(encoding="utf-8")):
            v = gefunden.setdefault(int(nr), {
                "label": label, "url": url, "slug": slug, "key": key, "kapitel": [],
            })
            if v["key"] != key:
                print("WARNUNG: VL %s wird mit zwei verschiedenen Videos verlinkt" % nr)
            fm = frontmatter(pfad)
            v["kapitel"].append({
                "pfad": pfad.relative_to(WURZEL).as_posix(),
                "titel": fm.get("title", ""),
                "beschreibung": fm.get("description", ""),
            })
    return gefunden


def seite_lesen(url):
    kopf = {"User-Agent": "mediathek_seo.py (eidl-skript, Pruefung der eigenen Videos)"}
    with urllib.request.urlopen(urllib.request.Request(url, headers=kopf), timeout=30) as r:
        html = r.read().decode("utf-8", "replace")
    head = html.split("</head>")[0]

    def meta(name, attr="name"):
        m = re.search(r'<meta[^>]+%s=["\']%s["\'][^>]*>' % (attr, re.escape(name)), head, re.I)
        if not m:
            return None
        c = re.search(r'content=["\'](.*?)["\']', m.group(0), re.S)
        return c.group(1).strip() if c else ""

    t = re.search(r"<title>(.*?)</title>", head, re.S)
    # Die Lizenz steht nur im Seitenkörper, nicht im Kopf. Sie wird gelesen und nicht
    # angenommen: am 2026-11-04 trugen VL 1 und VL 2 "CC BY-SA 3.0 DE", VL 3 und VL 4
    # "CC BY-ND 4.0" -- zwei Lizenzen in einer Reihe. Ein `meta_copyright` aus einer
    # Konstante hätte auf zwei Videos etwas behauptet, was das Lizenzfeld widerlegt.
    lic = re.search(r"(Creative Commons [^<]{5,90}?)\s*<", html)
    return {
        "lizenz": lic.group(1).strip() if lic else "",
        "seitentitel": t.group(1).strip() if t else "",
        "videotitel": meta("og:title", "property") or meta("og:title") or "",
        "og_url": meta("og:url", "property") or meta("og:url") or "",
        "description": meta("description"),
        "keywords": meta("keywords"),
        "author": meta("author"),
        "copyright": meta("copyright"),
    }


def vorschlag(nr, v, videotitel, lizenz=""):
    """Die fünf Formularfelder vorschlagen -- aus dem Kapitel, nicht aus der Luft."""
    kap = v["kapitel"][0]
    thema = v["label"]
    # Google schneidet den Titel bei etwa 60 Zeichen ab; bei langen Themen (VL 3:
    # „Vortrainierte Modelle“) kommt deshalb die kurze Form, sonst die ausgeschriebene.
    meta_title = "VL %d %s – Einführung in Deep Learning (HHU)" % (nr, thema)
    if len(meta_title) > 60:
        meta_title = "VL %d %s – Deep Learning, HHU" % (nr, thema)
    stichworte = [thema] + [k["titel"] for k in v["kapitel"]] + STICHWORTE_FEST
    gesehen, liste = set(), []
    for s in stichworte:
        if s and s.lower() not in gesehen:
            gesehen.add(s.lower())
            liste.append(s)
    return {
        "meta_title": meta_title,
        "meta_description": kap["beschreibung"],
        "meta_keywords": ", ".join(liste),
        "meta_author": AUTOR,
        "meta_copyright": "%s, %s" % (kurz_lizenz(lizenz), EINRICHTUNG) if lizenz else COPYRIGHT,
        "_quelle": kap["pfad"],
        "_weitere": [k["beschreibung"] for k in v["kapitel"][1:]],
    }


def einzeln(url):
    """Eine Adresse allein prüfen: Titel, Slug, Semester, Meta-Felder -- ohne Vorschlag.

    Für den Fall, der am 2026-11-04 mit VL 4 auftrat: das Video liegt schon in der
    Mediathek, die Kapitelzeile und das Player-Widget kommen erst, wenn Untertitel,
    Kapitelmarken und Vorschaubild fertig sind. Bis dahin findet `videos_aus_kapiteln`
    es nicht, und der Titel soll trotzdem geprüft sein.
    """
    m = re.match(r"https://media\.hhu\.de/video/([a-z0-9-]+)/([0-9a-f]{32})", url)
    if not m:
        print("Das ist keine media.hhu.de-Videoadresse: " + url)
        return 1
    slug = m.group(1)
    live = seite_lesen(url)
    print("Titel : " + live["videotitel"])
    print("Slug  : " + slug)
    befunde = []
    soll = slug_aus_titel(live["videotitel"])
    if soll != slug:
        befunde.append("Slug ist '%s', aus dem Titel folgt '%s'" % (slug, soll))
    if SEMESTER not in live["videotitel"]:
        befunde.append("Titel nennt nicht %s" % SEMESTER)
    d = live["description"] or ""
    if "&lt;" in d or d.lstrip().startswith("<p"):
        befunde.append("meta description enthaelt HTML-Tags (Feld meta_description leer)")
    for feld in ("author", "copyright"):
        if not live[feld]:
            befunde.append("meta %s fehlt in der Seite" % feld)
    for b in befunde:
        print("BEFUND: " + b)
    if not befunde:
        print("Keine Befunde.")
    return 1 if befunde else 0


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--vl", type=int, help="nur diese Vorlesung")
    p.add_argument("--offline", action="store_true", help="nicht ins Netz, nur Vorschläge")
    p.add_argument("--url", help="eine Mediathek-Adresse direkt prüfen (ohne Kapitel, "
                                 "für einen frischen Upload, dessen Kapitelzeile noch fehlt)")
    args = p.parse_args()

    if args.url:
        return einzeln(args.url)

    videos = videos_aus_kapiteln()
    if not videos:
        print("Keine Aufzeichnung in den Kapiteln verlinkt.")
        return 1
    befunde = []
    lizenzen = {}
    for nr in sorted(videos):
        if args.vl and nr != args.vl:
            continue
        v = videos[nr]
        print("=" * 78)
        print("VL %d: %s" % (nr, v["label"]))
        print("  Kapitel  : " + ", ".join(k["pfad"] for k in v["kapitel"]))
        print("  Slug     : " + v["slug"])
        live = None
        if not args.offline:
            try:
                live = seite_lesen(v["url"])
            except Exception as e:
                befunde.append("VL %d: Seite nicht lesbar (%s)" % (nr, e))
                print("  FEHLER   : %s" % e)
        if live:
            print("  Titel    : " + live["videotitel"])
            soll = slug_aus_titel(live["videotitel"])
            if soll != v["slug"]:
                befunde.append("VL %d: Slug ist '%s', aus dem Titel folgt '%s'"
                               % (nr, v["slug"], soll))
                print("  BEFUND   : Slug weicht vom Titel ab, erwartet '%s'" % soll)
            og_slug = live["og_url"].rstrip("/").split("/")[-2] if live["og_url"] else ""
            if og_slug and og_slug != v["slug"]:
                befunde.append("VL %d: Kapitel verlinkt '%s', die Seite nennt '%s'"
                               % (nr, v["slug"], og_slug))
            if SEMESTER not in live["videotitel"]:
                befunde.append("VL %d: Titel nennt nicht %s ('%s')"
                               % (nr, SEMESTER, live["videotitel"]))
                print("  BEFUND   : Semester im Titel ist nicht %s" % SEMESTER)
            d = live["description"] or ""
            if "&lt;" in d or d.lstrip().startswith("<p"):
                befunde.append("VL %d: meta description enthaelt HTML-Tags "
                               "(Feld meta_description leer)" % nr)
                print("  BEFUND   : meta description kommt aus der Beschreibung samt Tags")
            for feld in ("author", "copyright"):
                if not live[feld]:
                    befunde.append("VL %d: meta %s fehlt in der Seite" % (nr, feld))
        vor = vorschlag(nr, v, live["videotitel"] if live else "",
                        live["lizenz"] if live else "")
        if live:
            lizenzen.setdefault(live["lizenz"], []).append("VL %d" % nr)
        print("  -- Vorschlag (Quelle %s) --" % vor["_quelle"])
        for feld in ("meta_title", "meta_description", "meta_keywords",
                     "meta_author", "meta_copyright"):
            print("  %-16s (%3d) %s" % (feld, len(vor[feld]), vor[feld]))
        for w in vor["_weitere"]:
            print("  (Alternative aus dem zweiten Kapitel: %s)" % w)

    print("=" * 78)
    if len(lizenzen) > 1:
        befunde.append("Die Reihe traegt mehr als eine Lizenz: "
                       + "; ".join("%s -> %s" % (", ".join(v), k or "keine Angabe")
                                   for k, v in lizenzen.items()))
    if befunde:
        print("%d Befund(e):" % len(befunde))
        for b in befunde:
            print("  - " + b)
        return 1
    print("Keine Befunde.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
