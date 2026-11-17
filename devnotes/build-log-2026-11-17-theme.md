# Site-Template von 1.3.1 auf 1.4.1 (2026-11-17)

Anlass war eine Frage, keine Störung: Gibt es upstream in mystmd oder im Theme etwas, das
dieses Buch übernehmen könnte? Die Durchsicht der Primärquellen (35 gemergte PRs in
`jupyter-book/mystmd` seit 1.11.0, 29 in `jupyter-book/myst-theme`) hat zwei Antworten
gegeben, und die zweite war die unerwartete.

## Was upstream *nicht* passiert ist

Zu keinem der Punkte, die dieses Repo Patches kosten, gibt es eine Behebung:
`admonitions.tsx` rendert weiter `<aside>`, `Root.tsx` schreibt `<html lang="en">` hart,
die Kastennamen sind englische Literale in `proof.tsx`, `root.tsx` importiert
`thebe-core.css` unbedingt und hängt Font Awesome und `mpl_widget.css` in jede Seite,
KaTeX kommt vom CDN, und an der Stelle des Canonical steht in `meta.ts` ein `// TODO`.
Lokalisierung ist seit Januar 2023 ein offenes Sammelticket (`mystmd#166`); `#2628`,
derselbe Fall für französische Bücher, wurde im Juni als Duplikat geschlossen.
`myst-to-tex` ist seit dem 2025-12-05 funktional unangetastet, `devnotes/patch_myst_tex.py`
bleibt also nötig und würde bei einem mystmd-Upgrade nicht auslösen.

## Was passiert ist: das Theme ist zwei Generationen weiter

`myst-templates/book-theme@main` ist seit dem Stand dieses Repos fünfmal neu gebaut
worden — v1.4.0 und v1.4.1 am 2026-09-21, v2.0.0 am 2026-11-10 und 11-12, **v2.1.1 am
2026-11-17 um 15:33 UTC**, also am Tag dieser Durchsicht. mystmd heftet das Theme nicht an;
geschützt ist dieses Repo allein dadurch, dass `install_template.py` das mitgelieferte
Archiv vor dem Bau in den Template-Cache legt und mystmd dann nichts nachlädt.

Genommen wurde **1.4.1**, nicht 2.1.1. 1.4.1 behält das Dateilayout exakt
(`build/index.js`, `public/build/_shared/*`, `thebe-core.css` als eigene Datei); 2.x
ändert es vollständig und entwertet damit die 38 Anker in `install_template.py` sowie den
Ansatz von `tools/dead_css.py` und `tools/thebe_gate.py` (Einzelheiten in
`_site/vendor/README.md`).

## Gemessen, nicht angenommen

* `install_template.py` setzt **alle 38 Ersetzungen** (Kastennamen, Bedienung, Kastenelement),
  Rückgabewert 0.
* `myst build --html`: **0 Warnungen**.
* Die lokale `pages`-Kette läuft vollständig grün durch, einschließlich aller `--check`-Läufe.
* `hydration.py --check-rendered`: 4 Seiten halten nach der Hydration Sprache, Canonical,
  `og:url`, `ld+json` und Titel und tragen den `myst-no-css`-Kasten nicht mehr.
* `<aside>` im Artefakt: 0 — der Kastenpatch greift auch in 1.4.1.
* Die Admonitions sind **pixelgleich**: die gerechneten Farben von Kante, Fläche, Kopf und
  Symbol stimmen in hell und dunkel für jede Art überein. Dass 1.4.1 `{seealso}` upstream
  von Grün auf Blau umfärbt, ist hier unsichtbar, weil Abschnitt 4 von
  `_site/custom-style.css` die Farben ohnehin selbst setzt.
* Ein Nebenbefund aus der Kette: `head_meta` meldet jetzt **40 entfernte Bild-Preloads**
  (vorher 0). Das Theme legt seit 1.4.x Preload-Links für Abbildungen an; der Schritt, der
  sie wegnimmt, war schon da und greift erst jetzt.

## Was sich sichtbar ändert: die 47 `{prf:…}`-Kästen

Das ist die einzige Stelle, an der 1.4.1 das Aussehen dieses Buchs verändert, und sie
musste nachgezogen werden. In 1.4.1 gilt `border-l-4` immer (vorher nur im Dunkelmodus),
und der Titel bekommt eine Farbe nach `kind`: Definition blau `rgb(37,99,235)`, Beispiel
grün `rgb(22,163,74)`. Beide Farben stehen nicht in der Palette dieses Buchs — und das
Grün hat auf Weiß **3,30:1**, für Text also unter den 4,5:1 der Stufe AA. Vorher war der
Titel schwarz mit 17,93:1.

Nachgezogen in `_site/custom-style.css`, und zwar **ohne `!important`**: Theme 1.4.0 legt
rund siebzig Farben als CSS-Variablen offen, `.border-myst-info` löst zu
`var(--myst-color-info)` auf. Ein Satz Werte an `.myst-proof` genügt also — `info` ist die
Definition, `theorem` der Satz und die Proposition, `success` das Beispiel, `proof` bleibt
grau. Gemessen danach, auf dem jeweiligen Grund:

| | hell | dunkel |
|---|---|---|
| Definition, Satz (Marke) | 5,74:1 | 7,57:1 |
| Beispiel (HHU-Grün, abgedunkelt) | 5,94:1 | 7,00:1 |
| Beweis (grau) | 7,56:1 | 6,89:1 |

Das ist zugleich ein Vorgriff: Abschnitt 4 schreibt mit 34 `!important` gegen die
Tailwind-Utilities von 1.3.1 an. Mit den Variablen von 1.4.0 ließe sich das umbauen — ein
eigener Vorgang, hier nicht angefasst.

## Nicht geprüft

Das PDF. Es hängt am tex-Template und nicht am Site-Template; gebaut wurde es in diesem
Durchgang nicht.

---

# Nachtrag am selben Tag: mystmd 1.11.0 auf 1.13.0

Aus derselben Durchsicht. 1.12.0 erschien am 2026-10-26, 1.13.0 am 2026-11-12; zwischen
1.11.0 und heute wurden 35 PRs gemergt.

## Was es bringt, und was es kostet

Der Ertrag ist bescheiden und löst kein Problem, das dieses Buch hat: drei Behebungen
quadratischen Speicherwachstums bei großen Site-Builds (33 Seiten sind nicht groß),
`error_rules` mit Schlüsseln, ein Fix für Groß-/Kleinschreibung bei Querverweisen,
`multiple` für Template-Optionen. Gemacht wurde es trotzdem, weil die Anheftung sonst
stillschweigend veraltet und der Sprung später teurer wird.

Die Fassung steht an zwei Stellen: `pyproject.toml`/`uv.lock` für die Arbeit am Buch und
`Dockerfile` für die CI, wo mystmd global installiert und anschließend gepatcht wird.
Beide sind gehoben. Ein Push auf den Default-Branch baut das Image **automatisch** neu:
`build-image` hat eine `changes`-Regel auf `Dockerfile` und `devnotes/patch_myst_tex.py`,
beide sind in diesem Commit, und die Stufe `image` läuft vor `build`.

## Der eine echte Fund: ein minifizierter Name wandert

`patch_myst_tex.py` scheiterte gegen 1.13.0 — acht der neun Ersetzungen griffen, die für
die Bindestriche in Codeblöcken nicht:

    FEHLER [Bindestriche in Codeblöcken]: 'state.text(node3.value, true)' steht 0x im
    Fenster hinter dem Anker, erwartet genau 1x

Im Bündel von 1.13.0 steht an derselben Stelle `state.text(node4.value, true)`. Der Fehler
ist also **nicht** behoben, der Minifizierer hat nur die Variable umbenannt — was zu dem
Befund passt, dass `myst-to-tex` seit dem 2025-12-05 funktional unangetastet ist. Dieser
Patch sucht deshalb jetzt als einziger mit einem regulären Ausdruck; Anker, Fenster und
die Forderung nach genau einem Treffer bleiben, er scheitert also weiterhin laut, wenn
mystmd die Stelle wirklich bewegt. Gegen 1.11.0 wie gegen 1.13.0 geprüft, in beiden
Richtungen idempotent.

## Gemessen

* `myst build --html`: **0 Warnungen**.
* `myst build --pdf`: **152 Seiten** lokal — dieselbe Zahl wie unter 1.11.0, und damit die
  dritte Fassung in Folge ohne Satzunterschied. 0 LaTeX-Fehler, 0 fehlende Glyphen.
* Die Gegenproben im PDF: 0 zerrissene Langoptionen (`- -`), 0 `nvidia -smi`, dafür
  `--index-url` und `nvidia-smi` korrekt; 0 Ligaturen `¿`/`¡`; 0 englische Kastennamen.
* Suchindex und Querverweise **gleich**: 718 Einträge, 358 Adressen, 33 Seiten im `xref`,
  vorher wie nachher.
* Die lokale `pages`-Kette samt aller `--check` grün; `hydration.py --check-rendered` hält.

## Der Bruch, der keiner war

1.13.0 führt `searchable` an TOC-Einträgen ein: Versteckte Seiten sind nicht mehr
standardmäßig durchsuchbar. Verdächtig war `kurs-2026-27.md`, das bewusst außerhalb des
TOC steht — es wird aber gar nicht gebaut und stand auch unter 1.11.0 nicht im Suchindex.
Für dieses Buch ändert sich dadurch nichts.

Node ≥ 22 ist seit 1.12.0 Pflicht; das Image bringt Node 26 mit, lokal läuft 22.22.3.

## Nebenbefund

`check_pdf_build.py` läuft lokal nicht durch, weil `exports/` außer dem Buch noch ein
Foliendeck und elf Übungsblätter enthält — der Prüfer erwartet dort genau ein PDF. In der
CI ist das Verzeichnis sauber. Die Zahlen oben sind deshalb von Hand aus `pdfinfo` und
`pdftotext` gelesen.

---

# Nachtrag 2026-11-18: Theme 2.1.1 ausgemessen, nicht übernommen

Gemessen, weil der Befund von gestern — „2.1.1 würde die Patch-Schicht entwerten" — aus
einer Durchsicht der Quellen stammte und nicht aus einem Versuch. Er ist in seinem Kern
**falsch**, und das ist die Nachricht dieses Nachtrags.

## Die Anker überleben

Der Bündler von 2.x schreibt Zeichenketten in **Backticks** statt in doppelte
Anführungszeichen: aus `"Skip to article content"` wird `` `Skip to article content` ``.
Die Attributnamen bleiben doppelt gequotet (`"aria-label":`), nur die Werte wechseln. Weil
die 37 Muster in `install_template.py` das Anführungszeichen mitschreiben, greift keines —
die **Zeichenketten selbst stehen aber alle noch da** (`Skip to article content` 1×,
`Site not loading correctly` 1×, `Copy code to clipboard` 1×, `myst-admonition` 8×).

Gegen eine **ungepatchte** 1.4.1 als Kontrolle gemessen, mit einem Anführungszeichen, das
auch ein Backtick sein darf (`["'`]`):

| | 1.4.1 (Kontrolle) | 2.1.1 `renderer/server` |
|---|---|---|
| BEDIENUNG, 37 Muster | 29 greifen | **35** greifen |
| STRUKTUR (`aside` zu `div`) | 3 | **3** |
| KOPF (Kastenname aus dem `kind`) | 1 | **1** |

Zwei Muster bleiben übrig: `"No results found."` und `"sr-only",children:"Downloads"}`.
Die sind einzeln nachzusehen, nicht neu zu erfinden. Dass 2.1.1 **mehr** Treffer hat als
die 1.4.1-Kontrolle, liegt daran, dass dort einige Muster nur im Browser-Bündel standen.

## Was wirklich anders ist: die Adressen im Artefakt

Mit mystmd 1.13.0 **baut** 2.1.1 auf Anhieb — 33 Seiten, Rückgabewert 0, ohne jede
Anpassung. Das Artefakt sieht aber anders aus:

* Abbildungen liegen unter **`/_public/…`** statt unter `/build/…`.
* Das Stylesheet heißt **`/_assets/root-XUxrsvCL.css`** statt `/build/_assets/app-*.css`.
* Fünf Skripte in `tools/` setzen `build/` an 13 Stellen voraus: `head_meta.py` (7),
  `webp.py` (3), `hydration.py`, `llms_txt.py`, `stable_card.py` (je 1).

Dazu zwei Kleinigkeiten am Archiv: Es hat **keine Wurzelebene** (`renderer/`, `server/`,
`public/`, `template.yml` liegen direkt darin), womit die Prüfung „genau ein
Wurzelverzeichnis" in `install_template.py` scheitert; und es ist mit 23,5 MB fast doppelt
so groß wie das von 1.4.1.

## Die eine echte Einbuße

`thebe-core.css` ist in 2.1.1 **kein eingebundenes Stylesheet mehr**. Die Datei liegt zwar
noch im Baum, verwiesen wird aber nicht mehr darauf; ihre Regeln stecken im
Hauptstylesheet, das dadurch von 155 kB auf 237 kB wächst. Der Schnitt, den
`tools/dead_css.py` heute macht — 87 kB `<link>` weg, auf jeder der 33 Seiten —, ist so
nicht mehr zu haben. Font Awesome, `mpl_widget` und KaTeX hängen dagegen unverändert als
CDN-`<link>` in jeder Seite; diese drei Ziele von `dead_css.py` und `vendor_assets.py`
bleiben.

## Was das für eine Übernahme heißt

Kein Umbau, aber ein Tagwerk, und es liegt an zwei Stellen: `install_template.py` (ein
tolerantes Anführungszeichen, das Auspacken ohne Wurzelebene, zwei Muster nachsehen) und
die Adressannahme `build/` in den fünf Skripten. Dazu eine Entscheidung zu `thebe_gate.py`
und `dead_css.py`, die ohne den `thebe-core`-Link einen Teil ihres Zwecks verlieren.

**Nicht gemessen**: ob die *gepatchte* 2.1.1 richtig rendert, die `pages`-Kette, die
Hydration, das Aussehen. Das PDF ist nicht betroffen, es hängt am tex-Template.

Übernommen wurde nichts; der Arbeitsbaum steht wieder auf 1.4.1 (nachgeprüft: Theme 1.4.1
im Cache, 0 `<aside>`, Bildpfade unter `/build/`).
