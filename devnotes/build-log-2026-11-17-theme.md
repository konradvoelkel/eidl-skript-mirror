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
