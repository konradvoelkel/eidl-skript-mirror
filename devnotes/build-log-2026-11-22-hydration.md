# Wird der Kopf überhaupt noch ersetzt? Messung vom 2026-11-22

Punkt 6 der Arbeitsliste des dritten SEO-Audits (`seo-audit-2026-11-18.md`, §18): In
`CLAUDE.md`, im Docstring von `tools/hydration.py` und in `erledigt.md` steht seit dem
2026-11-15, daß React hier mit den Fehlern #418 und #423 abbricht und dabei
`documentElement` samt `<head>` **ersetzt** — weshalb der Wächter an `document` hängt und
Kopf und Wurzelelement bei jedem Lauf frisch nachschlägt. Anlaß des Zweifels: #423 trat in
15 Läufen nicht mehr auf, nur #418, und drei Stylesheets standen nach der Hydration doppelt
im Kopf. Die Frage war also nicht, ob die Angaben verschwinden, sondern **ob sie noch auf
dem beschriebenen Weg verschwinden.**

## Methode

Zwei Kopien von `_build/html`, beide durch die Schrittfolge des `pages`-Jobs geschickt
(`dead_css`, `vendor_assets`, `check_css_assets`, `thebe_gate`, `publish_urls`,
`head_meta`, `inject_jsonld`, `freshness`, `llms_txt`, `zitierzeile`, `stable_card`,
`image_dims`, `outline_reserve`, `trailing_slash`, `no_css_dialog`, `webp`), dazu die
Schriften und die `__BASE__`-Ersetzung aus dem `myst-build`-Job. Die eine Kopie bekommt
danach `tools/hydration.py`, die andere **nicht**.

Gemessen wird im echten Browser, nicht am Artefakt: `tools/hydration.py --check-rendered`
über sechs Seiten, dazu eine eigene Sonde für die vollständige Inventur des Kopfes
(Chromium aus dem Playwright-Zwischenspeicher, `load` plus 7 s Wartezeit, Konsolenfehler
mitgeschrieben). Fassungen: mystmd 1.13.0, `@myst-theme/book` 1.4.1, lokaler Stand vom
2026-11-22.

Gemessen ist damit das **lokale Artefakt**, nicht die ausgelieferte Site: Am Tag der
Messung antworteten `gitlab.cs.uni-duesseldorf.de` und der Pages-Host auf 80 und 443 mit
„Connection refused“ (ICMP und SSH dagegen durch).

## Ergebnis

| | ausgeliefert | ohne Wächter, nach der Hydration | mit Wächter |
|---|---|---|---|
| `<html lang>`                                    | `de`       | **`de`**        | `de` |
| `<title>` der Startseite                         | mit Zusatz | **ohne Zusatz** | mit Zusatz |
| `rel="canonical"`                                | 1          | **0**           | 1 |
| `og:url`, `og:site_name`, `og:type`, `og:locale` | da         | **weg** (3 statt 7 `og:*`) | da |
| `og:image`                                       | absolut    | **wurzelrelativ** | absolut |
| `twitter:card`                                   | 1          | **0**           | 1 |
| `link rel="alternate" type="text/markdown"`      | 1          | **0**           | 1 |
| `article:modified_time`                          | 1          | **0**           | 1 |
| `ld+json`                                        | 1          | **1, Typen intakt** | 1 |
| `style id="bildmasse"`, `id="gliederungsplatz"`  | da         | **da**          | da |
| `<dialog id="myst-no-css">`                      | weg        | **wieder da**   | weg |
| React-Fehler in der Konsole                      | —          | **keine, 0 Konsolenfehler** | keine |

## Was daraus folgt

**Der Kopf wird nicht mehr ersetzt.** `lang="de"` überlebt, der `ld+json`-Block überlebt
samt seinen Typen (`Book,LearningResource` auf der Startseite,
`Chapter,LearningResource` plus `BreadcrumbList` im Kapitel), und die zwei Stylesheets, die
die Schritte in `tools/` anlegen, stehen nach der Hydration noch da — alles **ohne**
Wächter. Keine der sechs Seiten meldet noch einen React-Fehler; die Konsole bleibt leer.
Ein Abbruch mit #423, der `documentElement` neu rendert, kann das nicht sein, denn dann
wäre `lang` wieder `en` und der `ld+json`-Block weg.

**Der Wächter bleibt trotzdem nötig.** Was verschwindet, sind genau die `<meta>`- und
`<link>`-Tags, die React im Kopf selbst verwaltet: Canonical, die vier `og:*` aus
`head_meta.py`, `twitter:card`, der Markdown-`alternate`, `article:modified_time` und der
Titelzusatz der Startseite; `og:image` fällt auf die wurzelrelative Adresse zurück, und den
`myst-no-css`-Kasten legt das Theme neu an. Ohne Wächter trifft das jede Seite — in der
Messung sechs von sechs.

**Für die Dokumentation heißt das:** Die Begründung „#418 und #423, der Knoten wird
getauscht und nicht mutiert“ beschreibt den Zustand vom 2026-11-15 und nicht den von heute.
Der Wächter hängt weiter an `document` und schlägt Kopf und Wurzel frisch nach; das ist
jetzt Vorsorge und nicht mehr Notwendigkeit. Entfernt wird nichts: Die Vorsorge kostet
nichts, und ein Theme-Update kann den alten Zustand zurückbringen.

## Offen

* **Woher die Umstellung kommt, ist nicht gemessen.** Am 2026-11-17 sind Theme (1.3.1 auf
  1.4.1) und mystmd (1.11.0 auf 1.13.0) zusammen gehoben worden; welche der beiden
  Bewegungen den Abbruch behoben hat, sagt diese Messung nicht. Zu trennen wäre das nur
  über einen Lauf mit der alten Fassung je Seite.
* **Die ausgelieferte Site ist nicht gegengeprüft.** Sobald der Pages-Host wieder antwortet,
  gehört dieselbe Inventur an eine echte Adresse — das Artefakt ist bytegleich, die
  Auslieferung bringt aber Kompression und Zwischenspeicherung dazu.
