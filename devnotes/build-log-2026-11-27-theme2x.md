# Umstieg auf Site-Template 2.1.1 — Protokoll vom 2026-11-27

Der Plan dazu steht in `plan-theme-2x.md` und lag seit dem 2026-11-18 unbeschlossen da; die
Zahlen, die ihm fehlten, kamen am Vormittag dieses Tages dazu
(`build-log-2026-11-27-js.md`: 38 % weniger JavaScript je Seite, das Krypto-Polyfill weg,
netto −312.508 B). Konrad hat danach entschieden: machen, und jetzt. Gearbeitet wurde auf
dem Zweig `theme-2x`; der `pages`-Job baut nur aus dem Default-Branch, die ausgelieferte
Seite ist davon also unberührt, bis jemand zusammenführt.

**Der Plan hat gehalten, wo er etwas behauptete, und drei Dinge nicht gesehen.** Die drei
stehen unten unter „Was der Plan nicht wußte" — alle drei hätten still danebengehen können,
und zwei davon hätten Bytes gekostet, die dieses Repo seit Wochen einsammelt.

## Was gemacht wurde, der Reihe nach

**1. Das Archiv.** `_site/vendor/book-theme.zip` ist jetzt das Release-Asset von
`myst-to-react@2.1.1` (23.487.865 B,
SHA-256 `9104dd5e…10128a`). Es hat **keine Wurzelebene**; `install_template.py` erkennt
beide Formen an `template.yml` — liegt es im Archiv ganz oben, wird das Entpackte selbst
zum Ziel, sonst die eine Ebene darunter.

**2. Die Patch-Schicht.** Zwei Änderungen, und beide so klein, wie der Plan sie
vorhergesagt hat:

* `tolerant()` läßt offen, welches Anführungszeichen gemeint ist (2.x schreibt
  Zeichenketten in Backticks). Angewandt auf `BEDIENUNG`, `STRUKTUR` und den Kastenkopf,
  **nicht** auf die Prüftexte: Die suchen den deutschen Text, und den schreiben wir immer
  doppelt gequotet.
* `server_buendel()` und `browser_buendel()` finden beide Layouts
  (`build/index.js` + `public/build/**` gegen `renderer/server/index.js` +
  `renderer/client/**`).

Gemessen nach dem ersten Lauf gegen 2.1.1: Kastennamen in 2 Bündeln, 37 Bedienungsmuster,
`eidl:kasten-div-note` 1×, `eidl:kasten-div-props` 2×, `eidl:kasten-titel-id` 1× — je
einmal im Server- und einmal in den Browser-Bündeln, wie die Invariante es verlangt. Der
zweite Lauf ist Leerlauf. `server/server/index.js` bleibt unangetastet, mit Begründung im
Docstring.

**3. Die Adressen.** Neu: `tools/artefakt.py`. Es **erkennt am Verzeichnis**, ob die
Dateien unter `build/` (1.4.x) oder `_public/` (2.x) liegen, und liefert Ordnernamen,
Pfad, Adressteil und eine Zerlegung für Zeichenketten. Umgestellt sind `head_meta.py` (3
Stellen), `webp.py` (4), `llms_txt.py`, `stable_card.py` (4), `hydration.py` und
`publish_urls.py` — letzteres stand nicht in der Liste des Plans, siehe unten.

**4. `dead_css.py`.** Zwei Ziele statt dreier, Möglichkeit 2 des Plans. Dazu zwei
Anpassungen, die der Plan nicht vorhersah: Die Muster für das `links()`-Array brauchen
dasselbe tolerante Anführungszeichen, und **das Array ist nach dem Räumen leer** — in
1.4.x blieb das Hauptstylesheet darin stehen. Die alte Nachbedingung („mindestens ein
Eintrag bleibt übrig") hätte den Schritt abbrechen lassen; sie lautet jetzt: Die Startseite
bindet weiterhin ein Stylesheet ein, das keines der Ziele ist. Damit `--check` und ein
zweiter Lauf das geräumte Array wiederfinden, trägt es den Marker `/*eidl:dead_css*/`.

**5. Die Kette.** Alle 19 Schritte des `pages`-Jobs laufen durch, alle 11 Prüfungen sind
grün (Protokoll unten). Dafür waren die drei Überraschungen zu beheben.

**6. Die Brotkrumen**, neu in 2.x über dem Seitentitel: eingedeutscht statt abgeschaltet
(`aria-label="Pfad"`, ein weiteres Muster in `BEDIENUNG`). Sie zeigen Teil und Kapitel —
auf `/faltung-cnn/` „Architekturen › CNNs". Abschalten wäre `hide_breadcrumbs: true` in
den Template-Optionen, eine Zeile.

## Was der Plan nicht wußte

### Die Hydrations-Nutzlast ist kein JSON mehr

Theme 2.x (React Router 8) schickt sie als **Turbo-Stream**: ein flaches Array in einem
`streamController.enqueue("…")`, in dem Objekte ihre Schlüssel und Werte über Indizes in
dasselbe Array nennen. Drei Schritte schreiben in die Nutzlast — `webp.py`
(`urlOptimized`), `head_meta.py` und `hydration.py` (die Karte) —, und alle drei hätten
**still nichts mehr getan**: Ihre Textersetzungen suchen `"url":"…"`, und dort stehen
Schlüssel und Wert nicht beieinander.

Was das kostet, ist gemessen und nicht geschätzt, an `/faltung-cnn/` im Browser:

| | ohne Nutzlast-Eintrag | mit |
|---|---|---|
| `<picture>` nach der Hydration | **0** von 5 | 5 von 5 |
| Abbildungen zweimal geladen | **2** | 0 |
| `og:image` nach der Hydration | `/_public/vl10-blur-edges-….webp` (relativ) | die Karte, absolut |

Die ausgelieferte 1.4.1 hält zur Kontrolle 5 von 5 `<picture>` und ihre Karte — der
Verlust wäre also ein Rückschritt gewesen, kein Gleichstand, und zwar genau an der Stelle,
an der am 2026-11-26 schon einmal 563 kB umsonst geladen wurden.

Neu ist deshalb `tools/turbostream.py`: dekodiert, gibt die Knoten heraus, hängt Neues
**am Ende an** (dann bleiben alle Indizes gültig) und schreibt zurück. Es escapet `<` als
`<` wie das Theme selbst, und es liest das Zeichenkettenliteral vollständig
(`"(?:[^"\\]|\\.)*"`) — ein ungieriges `".*?"` endete bei 20 von 33 Seiten mitten im
Literal, weil in der Nutzlast HTML steht und darin `\");` vorkommt. Dieser Fehler war
erst nach dem Schreiben sichtbar, und zwar an der eigenen Nachbedingung („keine lesbare
Nutzlast mehr").

### Der Platzhalter-Origin heißt nicht mehr `localhost`

2.x prerendert gegen `http://pre.render`. `publish_urls.py` ersetzte nur
`http://localhost:3000` und meldete zufrieden „0× ersetzt"; aufgefallen ist es an der
eigenen Nachbedingung, die 64 `<loc>` auf `http://pre.render/…` fand. Jetzt stehen beide
Platzhalter in einer Liste, und beide werden auch geprüft.

### `config.json` liegt nicht mehr im Artefakt

Theme 1.4.x legte es nach `_build/html`, 2.x nicht mehr; `inject_jsonld.py` liest daraus
das `toc` und die Slugs und brach ab. Der `myst-build`-Job kopiert es jetzt aus
`_build/site/` ins Artefakt und prüft, daß es angekommen ist.

## Die Kette, gemessen

Alle Schritte gegen eine Kopie des Artefakts, mit denselben Argumenten wie im
`pages`-Job (`BASE_URL` leer, `SITE_ORIGIN` die Pages-Adresse):

```
dead_css        66 <link> aus 33 Seiten und 2 Eintraege aus root-BM0TnMvp.js
vendor_assets   22 Dateien nach /vendor, 34 CDN-Referenzen in 581 Dateien (katex=34)
check_css_assets 3 eingebundene Stylesheets, 62 url()-Verweise, jeder aufloesbar
thebe_gate      _assets/dist-L0z2u8h2.js gated
publish_urls    33 <loc> mit Schraegstrich, 33 Canonicals
head_meta       33 Seiten, 132 Bild-Tags, 140 KaTeX-Schriften, 20 Karten ersetzt
inject_jsonld   Buch- und Kapitelknoten, Brotkrumen
llms_txt        33 Seiten als Markdown, llms-full.txt 479 KiB, 121 Bildadressen
zitierzeile     31 Seiten, 186 Ersetzungen
stable_card     social-card.png, 101 Verweise in 34 Dateien
image_dims      61 Abbildungen vermasst, 61 CSS-Regeln je Kopf
outline_reserve 32 Seiten mit Gliederung, 128 px
trailing_slash  632 hrefs im Markup, 395 in den Seiten-JSON
no_css_dialog   aus 33 von 33 Seiten
webp            527 Abbildungen, 41,73 MB weniger; 54 in zwei Groessen
                (98 Knoten der Nutzlast, 54 <picture>, 19 Preloads mit imagesrcset)
suchindex       724 Eintraege, 181 bereinigt
hydration       264 Tags und 98 bewahrte Knoten in den Waechtern
```

Und die elf `--check`-Läufe danach: alle grün, darunter `hydration --check` („Dokument
ganz, Nutzlast lesbar, Karte absolut") und `hydration --check-rendered`, das im Browser
nachsieht.

## Die Hydration, im Browser gemessen

Sechs Seiten, Chrome 158, 7 s nach `load`, gegen eine Kopie **ohne** Wächter und eine
**mit**:

* `documentElement` und `<head>` werden **nicht** ersetzt — wie unter 1.4.1 seit dem
  2026-11-22.
* React #418 tritt weiter auf, auf jeder Seite. Auch an der ausgelieferten 1.4.1 (Kontrolle
  am selben Tag).
* Ohne Wächter verloren: Canonical, 10 von 19 `<meta>`, alle Preloads, die `<picture>`,
  und der `myst-no-css`-Kasten kommt zurück. **Der Wächter bleibt nötig.**
* Mit Wächter: 15 von 19 `<meta>` — dieselben vier von React verwalteten Tags, die auch
  die ausgelieferte 1.4.1 verliert (dort gemessen: ebenfalls 19 auf 15). Canonical,
  `lang`, `ld+json`, Titel, Markdown-Verweis, `<picture>` und die absolute Karte stehen.
* Die drei Stylesheets stehen danach doppelt im Kopf; **keine fremde Herkunft kommt
  zurück** (null Anfragen nach außen, nachgezählt).

## Das Aussehen

Vier Seiten, hell und dunkel, Desktop und Handy, lokal gegen die ausgelieferte 1.4.1:

* Die **gerechneten Stile** sind identisch — Kästen (`myst-admonition*`, `myst-proof*`),
  ihre Kopfzeilen und Titel, Fließtext, Überschrift, Codeblöcke in Schriftgröße und
  Zeilenhöhe. Der einzige Unterschied in der ganzen Tabelle ist die Brotkrumenzeile, die
  es in 1.4.1 nicht gibt.
* **Pixelweise**: Die Seiten sind um 4 px versetzt (die Brotkrumen oben); mit diesem
  Versatz ist ein Band aus der Seitenmitte **byte-gleich**, über die ganze Seite bleiben
  1,5 % abweichende Pixel, und die liegen im Kopfbereich und an Stellen, an denen sich der
  Versatz um ein Pixel verschiebt. Die Seitenhöhe unterscheidet sich um 4 px auf 11.046.

## Nicht gemessen, nicht gemacht

* **Die Zeit.** Ob die halbierte Lieferung auch gewonnene Zeit ist, ist weiter offen: Die
  sechs Läufe vom Vormittag haben überlappende Spannen. Das gehört an die ausgelieferte
  Seite, nach dem Deploy, mit zehn PSI-Läufen je Seite.
* **Das PDF.** Hängt am tex-Template, nicht angefaßt.
* **Die Möglichkeit 1 aus `plan-theme-2x.md` §4** — die thebe-Regeln aus dem
  Hauptstylesheet schneiden. Eigener Vorgang, wenn überhaupt.
* **Der Deploy selbst.** Der Zweig ist nicht zusammengeführt; nichts davon ist live.
