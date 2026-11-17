# Umstieg auf das Site-Template 2.x — Arbeitsplan

Stand 2026-11-18. Gemessen an **2.1.1** (`myst-templates/book-theme@main`, Commit
`4c368fe4` vom 2026-11-17) gegen das hier benutzte **1.4.1**. Alles unten ist an den
Bündeln und an einem wirklichen Bau nachgemessen; wo etwas offen ist, steht es als offen
da.

**Dieser Plan ist nicht beschlossen.** Er beschreibt, was zu tun wäre, und in welcher
Reihenfolge. Es gibt keinen Zwang: Das Template liegt als ZIP im Repo, mystmd lädt nichts
nach, und 1.4.1 läuft.

## 0. Was schon erfüllt ist

* **mystmd ≥ 1.12** — 2.x braucht die Render-Schiene aus mystmd 1.11.0 und eine
  `template.yml`, die `multiple: true` benutzt (Option `redirects`), und das kennt erst
  1.12.0. Dieses Repo steht seit dem 2026-11-17 auf **1.13.0**, lokal wie im Image.
* **Node ≥ 22** — das Image bringt Node 26 mit, lokal läuft 22.22.3.
* **Es baut.** Mit 1.13.0 und ohne jede Anpassung hat 2.1.1 am 2026-11-18 durchgebaut:
  33 Seiten, Rückgabewert 0, keine Warnung. Das ist der Ausgangspunkt, nicht das Ziel —
  gepatcht war dabei nichts, die Oberfläche stand also auf Englisch und die Kästen auf
  `<aside>`.

## 1. Das Archiv (klein)

**Befund.** Das Release-Asset von 2.1.1 ist 23,5 MB (1.4.1: 12,7 MB) und hat **keine
Wurzelebene**: `renderer/`, `server/`, `public/`, `template.yml`, `package.json` und
`.env.prod` liegen direkt im Archiv. `install_template.py` verlangt heute genau ein
Wurzelverzeichnis und bricht sonst ab.

**Zu tun.**

1. In `_site/vendor/install_template.py` das Auspacken so ändern, dass **beide** Formen
   gehen: genau ein Wurzelverzeichnis (wie bisher) **oder** die Dateien direkt im Archiv.
   Erkennungsmerkmal ist `template.yml` — liegt es im Archiv ganz oben, wird das Archiv
   selbst zum Ziel entpackt, sonst die eine Ebene darunter.
2. Die Herkunftstabelle in `_site/vendor/README.md` auf das 2.1.1-Release-Asset und
   seinen SHA-256 setzen (Adresse wie gehabt, nur die Fassung tauschen).

**Fertig, wenn** `install_template.py` das Archiv auspackt und `template.yml` am
erwarteten Ort liegt.

## 2. Die Patch-Schicht (die gute Nachricht)

**Befund — und er widerlegt, was am 2026-11-17 in `CLAUDE.md` stand.** Der Bündler von 2.x
schreibt Zeichenketten in **Backticks** statt in doppelte Anführungszeichen; Attributnamen
bleiben doppelt gequotet (`"aria-label":` `` `Table of Contents` ``). Mehr ist es nicht.
Läßt man im Muster offen, welches Anführungszeichen gemeint ist, greifen gegen
`renderer/`:

| Liste | 1.4.1 | 2.1.1 |
|---|---|---|
| `BEDIENUNG`, 37 Muster | 37 | **37**, Server- und Browser-Bündel gleich oft |
| `STRUKTUR` (`aside` zu `div`) | 3 | **3** |
| `KOPF` (Kastenname aus dem `kind`) | 1 | **1** |
| `thebe_gate.py`, `COMPONENT` | 1 | **1**, unverändert — das Muster hat keine Anführungszeichen |

Die Zahl **35**, die im Nachtrag vom 2026-11-18 zuerst stand, war ein Fehler der Messung
und nicht des Themes: Zwei Einträge der Liste sind reguläre Ausdrücke (`"No results
found\."` und die `sr-only`-Stelle), und mein Messskript hatte sie als wörtliche
Zeichenketten escaped. `bedienung_eindeutschen()` compiliert **jeden** Eintrag als Regex.

**Zu tun.**

1. In `install_template.py` eine Hilfsfunktion, die ein Muster toleranter macht:
   jedes `"` darf auch `` ` `` oder `'` sein. Sie wird auf `BEDIENUNG`, `STRUKTUR` und
   `KOPF` angewandt, **nicht** auf die Prüftexte (`pruef`), denn die sollen den
   deutschen Text wörtlich finden.
2. Die Bündelpfade umstellen:
   * Server: `build/index.js` wird `renderer/server/index.js`
   * Browser: `public/build/**/*.js` wird `renderer/client/**/*.js`
   * Beide Formen erkennen, damit das Skript auch ein 1.4.1-Archiv noch behandelt —
     oder bewusst nur noch 2.x, dann aber mit klarer Fehlermeldung.
3. **Entscheiden, was mit `server/server/index.js` geschieht.** Das ist der Express-Teil
   für `myst start`; keines unserer Muster kommt darin vor (gemessen: 0 Treffer). Für
   `myst build --html` ist er ohne Belang. Vorschlag: nicht anfassen und das im Docstring
   begründen.
4. Die Invariante „gleich oft im Server- und im Browser-Bündel" bleibt — sie hält in
   2.1.1 für alle 37 Muster.

**Fertig, wenn** `install_template.py` gegen 2.1.1 ohne Fehler durchläuft und alle 41
Ersetzungen meldet.

## 3. Die Adressen im Artefakt (der eigentliche Brocken)

**Befund.** Das ist die wirkliche Änderung. Im Artefakt von 2.1.1 liegen

* die Abbildungen unter **`_public/`** (`/_public/vl06-…png`), nicht unter `build/`;
* das Stylesheet unter **`_assets/root-XUxrsvCL.css`** (237 kB), nicht unter
  `build/_assets/app-*.css`;
* `robots.txt` und `sitemap.xml` unverändert in der Wurzel.

Fünf Skripte setzen die alte Adresse an zwölf Stellen voraus:

| Skript | Stellen | was dort steht |
|---|---|---|
| `tools/head_meta.py` | 7 | Pfad einer Bild-URL im Artefakt, Ersetzen zu kleiner Vorschaubilder durch die Karte |
| `tools/webp.py` | 3 | die beiden `srcset`-Adressen und der Prüfausdruck für `@1x` |
| `tools/llms_txt.py` | 1 | die Adresse, unter der eine Abbildung in der Markdown-Fassung steht |
| `tools/stable_card.py` | 1 | die Prüfung, dass die Karte unter ihrem stabilen Namen liegt |
| `tools/hydration.py` | 1 | nur im Docstring, kein Code |

**Zu tun.**

1. Einen **gemeinsamen Ort für die Adresse** schaffen, statt sie zwölfmal zu
   wiederholen. Vorschlag: ein kleines Modul `tools/artefakt.py` mit einer Funktion, die
   am gebauten Verzeichnis **erkennt**, wie es aufgebaut ist (gibt es `build/` oder
   `_public/`?), und beide Namen zurückgibt. Erkennen statt konfigurieren, damit ein
   Rückschritt auf 1.4.1 nichts kostet und der `pages`-Job nicht wissen muss, welches
   Theme gerade gebaut hat.
2. Die fünf Skripte darauf umstellen. `hydration.py` braucht nur eine Zeile Prosa.
3. **Achtung bei `webp.py`:** Es ordnet Bilddateien über den SHA-256 ihres Inhalts zu und
   ist von Verzeichnisnamen unabhängig — betroffen sind nur die drei Stellen, an denen
   die `srcset`-Adresse *gebaut* wird. Die Mehrfachkopien je Abbildung gibt es in 2.1.1
   genauso (drei Kopien von `vl06-two-neurons` unter verschiedenen Hashnamen).

**Fertig, wenn** `--check` von `publish_urls.py`, `image_dims.py`, `webp.py`,
`stable_card.py` und `llms_txt.py` am 2.1.1-Artefakt grün ist.

## 4. `dead_css.py` — hier geht wirklich etwas verloren

**Befund.** Von den drei Stylesheets, die das Skript heute aus jeder Seite nimmt, bleiben
zwei: Font Awesome 4.7.0 und `mpl_widget` hängen unverändert als CDN-`<link>` in jeder
Seite (je einmal im Server- und im Browser-Bündel, wie in 1.4.1). **`thebe-core.css` ist
kein eingebundenes Stylesheet mehr**: Die Datei liegt noch im Baum, verwiesen wird nicht
mehr darauf, und ihre Regeln stecken im Hauptstylesheet, das dadurch von 155 kB auf
237 kB wächst.

Der heutige Schnitt — 87 kB weniger auf jeder der 33 Seiten — ist so nicht mehr zu haben.

**Drei Möglichkeiten, in dieser Reihenfolge zu prüfen.**

1. **Die Regeln aus dem Hauptstylesheet schneiden.** Sie sind erkennbar (`.thebe-`,
   `.jp-`, `thebeoutputspin`). Ein Schnitt am gebauten CSS ist aber etwas anderes als das
   Weglassen eines `<link>`: Er muss bei jedem Theme-Update neu geprüft werden, und er
   kann Regeln treffen, die etwas anderes brauchen. Wenn, dann mit einer Gegenprobe, die
   die Seite vorher und nachher rendert und vergleicht.
2. **Es hinnehmen.** 82 kB mehr Stylesheet gegen 87 kB weniger Link ist in Summe ein
   Nullsummenspiel — nur eben als eine Datei statt zweier. Für die Ladezeit ist eine
   Datei weniger sogar besser; was bleibt, ist der Verlust an Kontrolle.
3. **Upstream fragen.** `#960` („move thebe to myst-theme") ist offen und wäre die Stelle,
   an der sich das ändern könnte.

**Vorschlag:** Möglichkeit 2 für den Umstieg, Möglichkeit 1 als eigener Vorgang danach.
`tools/dead_css.py` behält dann zwei Ziele statt dreier, und seine Nachbedingung („findet
der Lauf gar kein Ziel, scheitert er") wird auf zwei gesetzt.

**`thebe_gate.py` bleibt, wie es ist.** Sein Muster hängt an der Form des
`useThebeLoader`-Aufrufs und nicht an Anführungszeichen; es greift in 2.1.1 unverändert
einmal. Die 1,3 MB `thebe-core.min.js` bleiben also weiterhin draußen.

## 5. Die `pages`-Kette durchziehen

Erst wenn 1 bis 4 stehen, lohnt der ganze Durchlauf. In der Reihenfolge des Jobs, jeweils
mit `--check`:

1. `dead_css.py` (jetzt zwei Ziele), `vendor_assets.py`, `check_css_assets.py` — Letzteres
   löst jeden `url()` der eingebundenen Blätter auf und wird zeigen, ob das größere
   Hauptstylesheet neue Schriften oder Bilder mitbringt.
2. `thebe_gate.py` — Muster unverändert, sollte durchlaufen.
3. `publish_urls.py`, `head_meta.py`, `inject_jsonld.py`, `freshness.py` — hier hängt
   nichts an den Bündeln, aber `head_meta.py` an den Bildadressen (siehe 3).
4. `llms_txt.py`, `stable_card.py`, `image_dims.py`, `outline_reserve.py`,
   `trailing_slash.py`, `no_css_dialog.py`, `webp.py`, `hydration.py`, `precompress.py`.

**Besonders ansehen:**

* `no_css_dialog.py` — der Kasten steht in 2.1.1 unverändert im Markup (`myst-no-css`
  einmal im Server- und einmal im Browser-Bündel), das Skript sollte greifen.
* `outline_reserve.py` — die Gliederung setzt ihre `max-height` weiter inline; die
  Deckelung auf 128 px am Handy ist neu zu messen, nicht zu übernehmen.
* `trailing_slash.py` — 2.x schreibt die Seiten weiter als `<pfad>/index.html`, der 302
  für die Adresse ohne Schrägstrich bleibt also Sache des Servers.

## 6. Die Hydration neu messen

**Nicht übernehmen, messen.** 2.0.0 hebt React 18 auf **19** und ersetzt Remix durch React
Router 8; ob die Fehler #418/#423 damit verschwinden, sagt keine Release-Notiz, und
geprüft hat es hier niemand. Davon hängt viel ab: Wenn die Hydration gelingt, ist
`tools/hydration.py` womöglich überflüssig — und wenn sie anders scheitert, ist sein
Wächter womöglich wirkungslos.

```sh
uv run --no-project --with playwright python tools/hydration.py --check-rendered _build/html
```

Dazu die Sonde aus dem Audit vom 2026-11-15 wiederholen: Wird `document.documentElement`
ersetzt oder verändert? Steht der Canonical nach dem ersten Frame noch da?

**Und `webp.py` hängt mit dran:** Das `srcset` steht heute in Markup **und** Nutzlast,
weil React sonst nach der Hydration ein nacktes `<img>` baut. Rendert 2.x stabil, ist der
doppelte Eintrag unnötig; rendert es anders, muss er anders aussehen.

## 7. Das Aussehen vergleichen

Dieselbe Methode wie beim Sprung auf 1.4.1, sie hat dort funktioniert:

1. Beide Artefakte lokal ausliefern, dieselben vier Seiten in hell und dunkel ganzseitig
   aufnehmen, pixelweise vergleichen, die Bänder mit Abweichung ansehen.
2. Die gerechneten Farben von Kante, Fläche, Kopf und Symbol je Kastenart auslesen und
   gegen heute halten — unser CSS in `_site/custom-style.css` §4 und §4b setzt sie, aber
   es hängt an den Klassennamen `myst-admonition*` und `myst-proof*`.
3. **Neu in 2.x: Brotkrumen** über dem Seitentitel. Entweder mit `hide_breadcrumbs: true`
   abschalten oder eindeutschen — dann kommt ein Muster zu `BEDIENUNG` dazu
   (`"aria-label":"Breadcrumb"`), ebenso für „Announcement banner", „Dismiss
   announcement", „Open Contents".

## 8. Was 2.x mitbringt, das wir nehmen könnten

* **`redirects`** (`"quelle:ziel"`, mehrfach) — statische Umleitungen als
  `<meta http-equiv="refresh">`. Das wäre die Antwort auf umbenannte Kapitel; bisher gibt
  es dafür nichts, und die eine Umbenennung von 2026-11-04 (`latente-raeume` zu
  `latente-raeume-geometrisch`) läuft bis heute ins Leere.
* **`hide_breadcrumbs`**, **`outline_maxdepth`**, **`hide_search`** — neue Schalter.
* **`style`** — ein lokales CSS über die Template-Option statt über unseren eigenen Weg;
  nur ansehen, nicht umstellen.

## 9. Rückweg

Jederzeit: `_site/vendor/book-theme.zip` aus `main` zurückholen,
`_build/templates/site/myst/book-theme` löschen, `install_template.py` laufen lassen, neu
bauen. Am 2026-11-18 zweimal gemacht, beide Male sauber (Gegenprobe: Theme 1.4.1 im Cache,
0 `<aside>`, Bildpfade wieder unter `/build/`).

Solange der Umstieg nicht fertig ist, gehört er auf einen Zweig und nicht nach `main` —
der `pages`-Job baut aus `main`, und ein halber Umstieg liefert eine englische Oberfläche
mit `<aside>`-Kästen aus.

## 10. Was nicht betroffen ist

* **Das PDF.** Es hängt am tex-Template unter `templates/tex/eidl-skript`, nicht am
  Site-Template. Seitenzahl, `patch_myst_tex.py` und `check_pdf_build.py` bleiben
  unberührt.
* **Die Foliensätze.** Eigener Bau, eigenes Theme.
* **Die Inhalte.** Kein Kapitel, kein Frontmatter, kein `myst.yml`-Eintrag ändert sich —
  außer den Template-Optionen in 8, falls wir welche nehmen.

## 11. Reihenfolge und Aufwand

1. Archiv und `install_template.py` (1, 2) — ein halber Tag, gut prüfbar.
2. Adressen in den fünf Skripten (3) — ein halber Tag, der Großteil ist `head_meta.py`.
3. `dead_css.py` entscheiden (4) — eine Stunde, wenn Möglichkeit 2.
4. Kette und Prüfungen (5) — ein halber Tag, mit Überraschungen zu rechnen.
5. Hydration messen (6) — eine Stunde, kann einen eigenen Vorgang auslösen.
6. Aussehen vergleichen (7) — zwei Stunden.

**Nicht in der Vorlesungszeit anfangen**, und nicht in derselben Woche wie eine inhaltliche
Änderung: Sonst ist später nicht zu unterscheiden, was der Umstieg verursacht hat und was
der Inhalt.
