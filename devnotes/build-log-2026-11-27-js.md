# Wohin das JavaScript geht, Theme 1.4.1 gegen 2.1.1 — Messung vom 2026-11-27

Punkt 8 der Arbeitsliste des dritten SEO-Audits (`seo-audit-2026-11-18.md`, §11): „Den
schon gebauten 2.1.1-Bau mit PSI vermessen und die JS-Größen in `plan-theme-2x.md`
nachtragen." Der Plan für Theme 2.x beschreibt bis heute jede Änderung am Artefakt, aber
**keine einzige Byte-Zahl** — und das Audit nennt die Größe des JavaScripts als einen der
beiden Gründe, aus denen über 2.x überhaupt nachzudenken ist.

## Warum nicht PSI, und was stattdessen

PSI misst nur öffentliche Adressen. Der 2.1.1-Bau liegt lokal, und er darf auch nicht nach
`main`: Der `pages`-Job baut aus `main`, und ein halber Umstieg liefert eine englische
Oberfläche mit `<aside>`-Kästen aus (`plan-theme-2x.md` §9). Gemessen wurde deshalb
dasselbe mit einem anderen Instrument — Chrome 158.0.8127.88 über das DevTools-Protokoll,
beide Artefakte über einen lokalen Server, ungenutzte Bytes nach **derselben Regel, die
Lighthouse rechnet**: `Profiler.startPreciseCoverage` mit `detailed`, und von außen nach
innen aufgetragen, weil der äußere Bereich eines Moduls immer läuft. Eine Vereinigung der
Bereiche mit `count>0` ergäbe fast überall 100 % — das war der erste Versuch und er war
falsch.

**Das Instrument ist an den PSI-Zahlen geeicht.** Für 1.4.1, dieselben vier Seiten:

| | Audit vom 18.11., aus PSI | hier gemessen |
|---|---|---|
| JavaScript der Startseite, brotli | 859 kB | **859.481 B** |
| davon die drei größten Chunks | 697 kB | **696.920 B** |
| `chunk-7FWBVTMU` ungenutzt | 98,3 % | **98,3 %** |
| `chunk-LS4ALTVG` ungenutzt | 80–82 % | 84,8 % |
| `chunk-WGW5MSUV` ungenutzt | 76 % | 77,2 % |

Die ersten drei Zeilen treffen auf das Kilobyte, die beiden letzten auf zwei bis drei
Punkte. Was unten über 2.1.1 steht, ist mit demselben Werkzeug gemessen wie diese Spalte.

## Methode

Derselbe Baum, dieselbe Fassung, nur das Theme getauscht: mystmd 1.13.0, Node 24.22.3,
Inhaltsstand `310d0f5`. Das Archiv von 2.1.1 kommt aus dem Release-Asset
(`myst-to-react@2.1.1`, 23.487.865 B,
SHA-256 `9104dd5eb5f94726cdc46e750dfcaab8332cfe55d40e91ce9db65e25d010128a`) und wurde ohne
`install_template.py` direkt in den Template-Cache gelegt, weil das Skript eine Wurzelebene
verlangt und 2.1.1 keine hat. Je Theme ein `myst build --html`, dann vier Seiten
(Startseite, `/glossar/`, `/rnn/`, `/transformer/`) mit Abdeckungsmessung, danach brotli
Stufe 11 über jede angeforderte JS-Datei — Stufe 11, weil `tools/precompress.py` im
`pages`-Job genau diese Stufe fährt.

Drei Einschränkungen, die bei jeder Zahl unten mitzulesen sind:

* **`thebe-core.min.js` (1.308.332 B, brotli 282.459 B) wird lokal von beiden Themes
  geladen und ist unten überall herausgerechnet**, weil `tools/thebe_gate.py` es im
  `pages`-Job entfernt und sein Muster in 2.1.1 unverändert greift (gemessen am 18.11.).
  Die Zahlen unten sind also die der ausgelieferten Seite, nicht die des lokalen Baus.
* **Die übrige `pages`-Kette lief nicht**, auf keiner der beiden Seiten. Verglichen werden
  rohe Artefakte.
* **1.4.1 ist gepatcht, 2.1.1 nicht.** Die Patch-Schicht wiegt **525 B** über 1.000 Dateien
  (18.806.248 B gegen 18.806.773 B), sie fällt gegen die Unterschiede unten nicht auf.

## Das Ergebnis

Startseite, ohne `thebe-core`, brotli Stufe 11:

| 1.4.1 | roh | brotli | ungenutzt |
|---|---|---|---|
| `chunk-7FWBVTMU.js` — JupyterLab/Lumino | 1.321.541 | 279.745 | 98,3 % |
| `chunk-LS4ALTVG.js` — thebe, JupyterLite, MathJax, jQuery | 895.459 | 227.857 | 84,8 % |
| `chunk-WGW5MSUV.js` — **2,13 MB Krypto-Polyfill**, 55 kB Komponenten | 2.187.346 | 189.318 | 77,2 % |
| `chunk-KB7LMXDF.js` — React und ReactDOM | 193.283 | 51.759 | 64,0 % |
| 16 weitere Dateien | 385.376 | 110.802 | — |
| **Summe, 20 Dateien** | **4.983.005** | **859.481** | **82,6 %** |

| 2.1.1 | roh | brotli | ungenutzt |
|---|---|---|---|
| `dist-L0z2u8h2.js` — Lumino, JupyterLab, thebe, MathJax, jQuery in **einem** Chunk | 1.627.013 | 358.194 | 89,1 % |
| `jsx-runtime-CXMjD0lx.js` — React 19 und ReactDOM | 270.255 | 73.482 | 67,1 % |
| `root-BM0TnMvp.js` — die Komponenten des Themes | 171.973 | 44.361 | 54,6 % |
| `_-Dtrusp7j.js` — die Route | 92.339 | 24.676 | 58,4 % |
| 10 weitere Dateien | 97.010 | 29.557 | — |
| **Summe, 14 Dateien** | **2.258.590** | **530.270** | **81,7 %** |

Über alle vier Seiten, jeweils ohne `thebe-core`:

| Seite | roh 1.4.1 → 2.1.1 | brotli 1.4.1 → 2.1.1 | Dateien |
|---|---|---|---|
| Startseite | 4.983.005 → 2.258.590 B (−55 %) | 859.481 → 530.270 B (−38 %) | 20 → 14 |
| `/glossar/` | 4.982.545 → 2.258.232 B (−55 %) | 859.145 → 530.111 B (−38 %) | 20 → 14 |
| `/rnn/` | 5.010.575 → 2.285.593 B (−54 %) | 869.396 → 539.773 B (−38 %) | 22 → 16 |
| `/transformer/` | 4.982.545 → 2.258.232 B (−55 %) | 859.145 → 530.111 B (−38 %) | 20 → 14 |

Der Anteil des ungenutzten Codes bleibt, wo er war: 82,6 % gegen 81,7 %. Es wird nicht
weniger verschwendet — es wird **weniger geliefert**, und zwar 329.211 B brotli je Seite.

In der Rechenweise, in der Lighthouse ungenutztes JavaScript ausweist (Transferbytes mal
Anteil), sind das auf der Startseite **703 KiB gegen 418 KiB**, auf `/rnn/` 702 gegen
415 KiB. Das Audit nennt für dieselbe Seite 591 KiB; die 19 % Abstand nach oben sind
nicht geklärt — am nächstliegenden wäre, daß Lighthouse nur Dateien über einer Schwelle
aufführt, geprüft habe ich das nicht. Für den Vergleich der beiden Themes spielt es keine
Rolle, beide Spalten sind mit derselben Regel gerechnet.

### Das Krypto-Polyfill ist weg

Der auffälligste Posten aus §11 des Audits — 2,13 MB browserifiziertes `crypto-browserify`
in einem Lehrbuch ohne Anmeldung und ohne Formular — kommt in 2.1.1 nicht mehr vor.
Gemessen über alle 429 JS-Dateien des Artefakts: `crypto-browserify` 0,
`createHmac` 0, `pbkdf2` 0, `diffie-hellman` 0, `browserify-sign` 0, `readable-stream` 0.
`elliptic` steht 23-mal da, aber nicht als Bibliothek: Es sind `EllipticK` und
Verwandte in den Sprachdateien von Maxima und Mathematica und in plotly, und keine dieser
drei Dateien fordert die Seite an.
Das erklärt den Großteil der 2,72 MB, die roh wegfallen, und es ist ohne Gabelung des
Themes zu haben — die war im Audit der einzige genannte Weg dorthin.

### Der große Chunk hängt weiter statisch drin

Das strukturelle Hindernis bleibt. `root-BM0TnMvp.js` enthält
`import{…}from"./dist-L0z2u8h2.js"`, und die Startseite lädt den Chunk über
`rel="modulepreload"` vor (14 Vorlademarken statt 19 in 1.4.1). Ein Tor nach dem Muster
von `tools/thebe_gate.py` ist damit auch in 2.1.1 nicht möglich: Dort greift es nur, weil
`thebe-core` **dynamisch** geladen wird. 358.194 B brotli, zu 89,1 % ungenutzt, stehen also
weiterhin im kritischen Pfad, und 2.x verschiebt diese Frage, statt sie zu beantworten.

### Was die Bilanz zurücknimmt

Nicht alles wird kleiner. Gegenrechnung je Seite, brotli:

| | 1.4.1 | 2.1.1 | Differenz |
|---|---|---|---|
| JavaScript | 859.481 | 530.270 | **−329.211** |
| Stylesheet | 16.684 (`app-*.css`, 155.290 B roh) | 28.219 (`root-*.css`, 237.475 B roh) | +11.535 |
| HTML der Startseite | 19.861 | 25.029 | +5.168 |
| **Summe** | | | **−312.508** |

Das Stylesheet wächst, weil `thebe-core.css` eingebacken ist — die 12.531 B brotli, die
`tools/dead_css.py` heute als `<link>` herausnimmt, sind in den 28.219 B schon drin. Die
Nutzlast der Hydration ist praktisch unverändert (`index.json` 38.858 gegen 38.856 B,
`rnn.json` 123.126 gegen 123.128 B); daß das HTML trotz 18.827 B weniger Rohgröße
komprimiert größer ausfällt, ist nicht erklärt.

### Die Zeit auf dem Hauptthread

Sechs Läufe je Theme und Seite, CPU auf ein Viertel gebremst, Median und Spanne in
Millisekunden:

| | Script | Style + Layout | Task | Langaufgaben |
|---|---|---|---|---|
| 1.4.1 Startseite | 1.566 [1.495–1.739] | 100 [94–125] | 1.816 [1.726–2.027] | 1.324 [1.278–1.469] |
| 2.1.1 Startseite | 1.413 [1.127–1.807] | 119 [90–168] | 1.727 [1.359–2.329] | 1.121 [939–1.538] |
| 1.4.1 `/rnn/` | 1.711 [1.579–1.769] | 296 [280–319] | 2.244 [2.096–2.357] | 1.466 [1.357–1.555] |
| 2.1.1 `/rnn/` | 1.349 [1.200–1.803] | 364 [282–544] | 2.027 [1.786–2.866] | 1.149 [981–1.559] |

Die Mediane zeigen in eine Richtung — auf `/rnn/` 21 % weniger Skriptzeit und 22 % weniger
Langaufgaben —, **die Spannen überlappen aber vollständig**, und 2.1.1 streut deutlich
breiter als 1.4.1. Mit sechs Läufen ist das ein Hinweis und kein Beleg; die methodische
Folgerung aus §11 des Audits gilt hier genauso. Woran man merken würde, daß es falsch ist:
Wenn zehn weitere Läufe die Mediane zusammenrücken lassen, war der Unterschied Rauschen,
und dann bringt der halbierte Download **keine** gewonnene Zeit mit.

Einen Punktwert von PSI gibt es aus diesem Durchgang nicht und kann es nicht geben. Was er
zusätzlich sagen würde, wäre bei einer zusammengefaßten Streuung von 7,9 Punkten (§11 des
Audits) ohnehin erst nach zehn Läufen eine Zahl.

## Nicht gemessen

Die *gepatchte* 2.1.1 (die Patch-Schicht wurde am 18.11. nur gezählt, nicht angewandt), die
`pages`-Kette, die Hydration, das Aussehen, das LCP in einem sichtbaren Fenster, Felddaten.
Das PDF ist nicht betroffen, es hängt am tex-Template.

## Was danach im Baum stand

Der Arbeitsbaum steht wieder auf 1.4.1: Theme 1.4.1 im Cache, `/build/` im Artefakt, 0
`<aside>` in `autoencoder/index.html`, `_build/html` neu gebaut (33 Seiten). Übernommen
wurde nichts, kein Skript und keine Fassung hat sich geändert — die Messung ist der ganze
Vorgang.
