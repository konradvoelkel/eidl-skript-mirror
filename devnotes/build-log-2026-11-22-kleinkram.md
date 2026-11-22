# Die Einzelposten aus §13 des dritten Audits, 2026-11-22

Punkt 7 der Arbeitsliste (`seo-audit-2026-11-18.md`, §18, dort die Posten 10 bis 12 und 16)
plus zwei Befunde aus §13, die noch offen standen. Fünf von sechs sind erledigt, einer ist
eine Entscheidung und bleibt liegen.

Gemessen wurde am lokalen Artefakt: `myst build --html`, dann die Schrittfolge des
`pages`-Jobs gegen eine Kopie, Browsermessungen mit Chromium aus dem
Playwright-Zwischenspeicher. Die ausgelieferte Site war an diesem Tag nicht erreichbar
(`gitlab.cs.uni-duesseldorf.de` und der Pages-Host wiesen Verbindungen auf 80 und 443 ab).

## 1. Der Kapitellink über eine 302 — und eine falsche Begründung

`/gradientenabstieg/` verlinkte `/hintergrundwissen-analysis#zweite-ableitungen-die-hesse-matrix`,
also ohne Schrägstrich. `tools/trailing_slash.py` ließ das stehen, weil
`fehlt_schraegstrich()` den ganzen Wert in der Kapitelliste suchte und ein Fragment ihn
dort nicht finden ließ. In der Tabelle des Docstrings stand als Begründung, `/kapitel#abschnitt`
liefere schon 200 — **das ist falsch**: Der Browser schneidet das Fragment ab, der Server
sieht den Pfad ohne Schrägstrich. Für die Query gilt dasselbe.

Jetzt trennt `mit_schraegstrich()` am ersten `#` oder `?`, prüft den Pfadteil und setzt den
Schrägstrich **vor** den Rest. Zehn Einheitsproben gegengerechnet, darunter die vier Fälle,
die unangetastet bleiben müssen (kein Kapitel, Datei mit Punkt, absolute Adresse,
Großbuchstabe) und die zwei, die schon richtig sind (`/kapitel/`, `/kapitel/#a`). Im
Artefakt steht der Link nun in Markup und Hydrations-Nutzlast mit Schrägstrich, und
`--check` zählt über alle 33 Seiten keinen Kapitellink ohne.

## 2. Die vier fehlenden Bild-Tags

`og:image:alt`, `og:image:width`, `og:image:height` und `twitter:image:alt` fehlten auf
allen 33 Seiten. `tools/head_meta.py` trägt sie nach; alle vier stehen jetzt auf 33 von 33
Seiten.

**Das Maß wird aus der Datei gelesen, nicht geschrieben.** 1200×630 wäre die Karte — aber
`vet_card()` darf eine Abbildung als Karte stehen lassen, wenn sie groß genug ist, und dann
wäre die Angabe falsch. Gezählt: Heute tragen 33 von 33 Seiten die Karte, der Fall tritt
also gerade nicht ein; das Skript rechnet trotzdem je Seite aus der Bilddatei.

Der Alt-Text beschreibt die Karte und wiederholt den Titel nicht — der steht als `og:title`
daneben, und dieselbe Regel gilt im Buch für jede Abbildung. Für den Fall, daß doch eine
Abbildung als Karte steht, holt `bild_alt()` deren Alt-Text aus dem Markup derselben Datei;
findet es keinen, bleibt das Tag weg.

## 3. Roher LaTeX-Quelltext in den Suchausschnitten

MyST legt in `myst.search.json` den Text jeder Überschrift samt Abschnitt ab — Mathematik
darin **ohne** die `$`-Zeichen, die sie als Mathematik auswiesen. Gezählt: **180 von 722
Eintragen** mit mindestens einem Backslash.

Neuer Schritt `tools/suchindex.py`. Er übersetzt mit der Tabelle aus `inject_jsonld.py`
plus einer eigenen und streift ab, was er nicht kennt. **Warum nicht laut gescheitert wie
beim Glossar:** Über den ganzen Index gemessen kennt die Glossartabelle **98 verschiedene
Befehle nicht**, in 1957 Vorkommen — `\mathbb` (256), `\in` (142), `\to` und `\partial` (je
107), dazu `\begin{pmatrix}`-Umgebungen. Ein lauter Abbruch hätte den Deploy an jedem neuen
Formelzeichen aufgehalten, und das für einen Suchausschnitt.

Nachbedingung ist deshalb nicht „richtig übersetzt“, sondern **kein Backslash mehr im
Index**. Beispiel aus `/gans#gan-training`:

* vorher: `\min_G \max_D \; V(D, G) = \mathbb{E}_{x \sim p_{\text{data}}}\bigl[\log D(x)\bigr] + …`
* nachher: `min_G max_D V(D, G) = 𝔼_x ~ p_data[log D(x)] + 𝔼_z ~ N(0, I)[log(1 - D(G(z)))]`

Angefaßt wird nur ein Feld, das einen Backslash trägt, und das ist die Bedingung für einen
wirkungslosen zweiten Lauf: Aus `\{0, 1\}` wird `{0, 1}`, und genau diese Klammern würde ein
weiterer Durchgang wieder abstreifen. Gegenprobe: erster Lauf 180 Felder, zweiter Lauf 0,
`--check` grün.

## 4. Der Suchknopf, mobil

Gemessen bei 390 px Breite im Browser: Suchknopf **42 × 40 px**, der Befund aus dem Audit
vom 15.11. also bestätigt. Eine Schranke in `_site/custom-style.css` unterhalb von `sm`
(640 px) hebt ihn auf **44 × 44**, nachgemessen. Darüber wird aus dem Knopf die breite
Suchleiste, dort stellt sich die Frage nicht.

Mitgemessen und **nicht** geändert, weil nicht beanstandet: Menüknopf 40 × 40,
Hell-Dunkel-Knopf 32 × 32, Gliederungsschalter 24 × 24. Alle drei liegen über der
AA-Schwelle (2.5.8, 24 × 24) und unter der Zielgröße (2.5.5, 44 × 44).

## 5. CLS auf der Destillations-Seite: die Ursache sind die KaTeX-Schriften

Der Befund aus dem Audit vom 17.11. (desktop 0,103, „Quelle jetzt bekannt: ein `P` und ein
`DIV.flex.my-5.group`") ist lokal reproduziert — und die Quelle ist eine andere als
vermutet. Vier Läufe je Fall, 1366 px, Abrufe einzeln blockiert:

| Fall | CLS, Median |
|---|---|
| alles wie ausgeliefert | **0,0760** |
| ohne Inter | 0,0657 |
| ohne JetBrains Mono | 0,0760 |
| **ohne die KaTeX-Schriften** | **0,0000** |
| ohne das KaTeX-Stylesheet | 0,0000 |

Es sind also nicht die Hausschriften — für die sorgen die metrikgleichen Ersatzschriften
vom 2026-10-22 — sondern die Schriften von KaTeX. Sie werden erst entdeckt, wenn das
Stylesheet geholt, geparst und eine Glyphe gebraucht ist, auf dieser Seite nach 326 ms, und
dann ruckt jeder Absatz mit Inline-Mathematik. Die Höhe der Formelblöcke ändert sich dabei
**nicht** (24 und 49 px vor und nach dem Tausch); es sind die Zeilenumbrüche im Fließtext.

Behebung: `tools/head_meta.py` lädt die KaTeX-Schriften vor — **je Seite genau die, die
ihre Formeln brauchen.** Mit den zwei häufigsten sinkt das CLS auf 0,0219, mit allen fünf,
die diese Seite holt, auf 0,0000.

Welche eine Seite braucht, steht in ihrem Markup: Die Zuordnung Klasse zu Datei steht in
`_site/vendor/katex/katex.min.css` (`.katex .mathbb{font-family:KaTeX_AMS}` und so weiter)
und ist abgeschrieben, nicht geraten. **Gegen den Browser geprüft** an fünf Seiten:

| Seite | Chromium holt | Vorhersage |
|---|---|---|
| `/destillation/` | AMS, Caligraphic, Main-Regular, Math-Italic, Size1 | gleich |
| `/backpropagation/` | dieselben plus Size2, Size3 | gleich |
| `/glossar/` | Caligraphic, Main-Regular, Math-Italic, Size1 | gleich |
| `/anwendungsbeispiele/` | keine | keine |
| `/tensoren/` | AMS, Main-Regular, Math-Italic, Size2 | **eine mehr** (Size1) |

Die eine Abweichung ist erklärt: Die Formel mit der großen Klammer steckt dort in einem
eingeklappten `dropdown` und wird erst beim Aufklappen gebraucht. Die Vorhersage ist damit
eine Obermenge und nie zu klein — zu klein wäre der Fehler, der das Ruckeln zurückbrächte.

**Die Falle dabei:** `size1` allein ist KaTeX' Skalierungsklasse und steht auf fast jeder
Formel; die Größen-Schrift hängt an **zwei** Klassen am selben Knoten (`delimsizing size1`).
Wer das verwechselt, lädt auf fast jeder Seite drei Dateien zu viel. Die erste Fassung der
Tabelle tat genau das, und die Gegenprobe gegen den Browser hat es gezeigt.

Nach dem Umbau, desktop: Destillations-Seite, Startseite, `/faltung-cnn/` und
`/universelle-approximation/` je **0,0000**. Mobil bleibt die Destillations-Seite bei
**0,0139** — vorher derselbe Wert, dort liegt also eine andere, kleinere Quelle; bei 390 px
rollt die Formel waagerecht statt den Text umzubrechen.

**Gegenprobe, ob der Preload etwas kostet**: LCP derselben Seite unter gedrosselter
Verbindung (1,6 Mbit/s, 150 ms RTT, vier Läufe) vorher **27.886 ms**, nachher **27.864 ms**
— im Rauschen, die Preloads holen dieselben Dateien nur früher. Die absolute Zahl ist eine
Eigenschaft der Drosselung und des 859-kB-Bündels, keine Aussage über die ausgelieferte
Site; das LCP-Element ist der Einleitungsabsatz (§10 des Audits) und hängt an Inter, nicht
an den Formelschriften.

## Offen geblieben

**Die zehn Titel über 60 Zeichen** (§18 Punkt 16). Gemessen am Artefakt vom 2026-11-22,
Spanne 61 bis 71 Zeichen:

| Zeichen | Seite | Titel |
|---|---|---|
| 71 | `/faltung-cnn/` | Faltung und Convolutional Neural Networks - Einführung in Deep Learning |
| 68 | `/loss-funktionen-maximum-likelihood/` | Loss-Funktionen und Maximum Likelihood - … |
| 65 | `/representation-learning-graphen/` | Representation Learning und Graphen - … |
| 63 | `/hintergrundwissen-lineare-algebra/` | Hintergrundwissen Lineare Algebra - … |
| 63 | `/adversarial-attacks-polysemie/` | Adversarial Attacks und Polysemie - … |
| 62 | `/optimierer/` | Optimierer: Momentum, Adam, Muon - … |
| 62 | `/` | Einführung in Deep Learning — Vorlesungsskript, HHU Düsseldorf |
| 61 | `/vortrainierte-modelle/` | Vortrainierte Modelle verwenden - … |
| 61 | `/glossar/` | Glossar zur Klausurvorbereitung - … |
| 61 | `/gans/` | Generative Adversarial Networks - … |

Die Ursache ist in allen Fällen der Zusatz „ - Einführung in Deep Learning“, 30 Zeichen,
den das Theme an jeden Kapiteltitel hängt. Das ist eine Entscheidung und kein Defekt, und
es gibt drei Wege: den Zusatz auf langen Seiten weglassen (abgeschnitten wird er in der
Trefferliste ohnehin), ihn buchweit kürzen (kostet Wiedererkennung), oder die Kapiteltitel
kürzen — was zugleich die Suchwortlücken schließen würde, die §13 nennt (`/gans/` ohne
„GAN“, `/faltung-cnn/` ohne „CNN“), aber die Überschriften im Buch ändert. Deshalb liegt
das bei Konrad.
