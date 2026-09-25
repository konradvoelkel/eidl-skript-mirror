# Durchsicht der Beamer-Decks VL 1–15 (2026-09-25)

Geprüft wurden die 15 gebauten PDFs in `slides/` (276 Folien) und ihre `.tex`-Quellen: Rendering
(Kontaktbögen aller Folien), Textdichte (Wörter pro Folie aus `pdftotext`), fachliche Korrektheit
der Formeln und Fakten, Abgleich mit Skript, `kurs-2026-27.md` und den Blättern, Bildanzahl, sowie
die Ablaufpläne in den Titelnotizen.

**Umgesetzt am 2026-09-25 (Entscheidung Konrad):** A1 (Schrift), A2 (Titel), A3 (Item-Labels),
und die Blatt-Referenzen aus A6 sind jetzt nummernfrei („Übungsblatt“, „eine Übungsaufgabe“), damit
sie stabil bleiben, wenn Blätter getauscht werden. Dazu die Codezeile in VL 3 (Abschnitt C) und ein
Glob-Fehler in `build.sh`. Alle 15 Decks bauen ohne Schriftwarnungen und ohne zu volle Rahmen auf
Folien; die verbliebenen `Overfull \hbox` in den Logs stammen aus den Ablaufplan-Tabellen in den
Titelnotizen. Offen: A4, A5, die Termin-Punkte in A6, B, C, D.

**Kurzfassung.** Textdichte und Dramaturgie sind gut (max. 69 Wörter pro Folie inkl. Fußzeile,
Median ≈ 28; jede Sitzung hat Rückblick, Kern, Take-Home, Blatt). Es gibt aber vier systemische
Probleme, die jedes Deck betreffen (Schriftbild, Titel unter dem Logo, abgeschnittene Item-Labels,
falsche Foliennummern in den Ablaufplänen), eine Handvoll fachlicher Unschärfen auf einzelnen
Folien und drei Decks, die Blätter oder Termine falsch beschreiben. Bilder fehlen vor allem in
VL 10, 13 und 15.

## A. Systemisch (alle Decks)

### A1. Schriftbild: Serifen statt Source Sans Pro, aufrechte Mathe-Buchstaben — **erledigt 2026-09-25**

Alle Decks (auch die Modulvorstellung vom Juli) rendern den Fließtext in Latin Modern Roman
(Serifen), Mathe-Buchstaben aufrecht (`f(x) = w · x + b` ohne Kursive) und Operatoren wie
`ln`, `odds`, `logit`, `tanh`, `ReLU`, `sm` serifenlos, also drei Schriftbilder in einer Formel.

Ursache: das Theme (`/usr/share/texmf/tex/latex/beamer/themes/hhubeamer/beamerthemehhubeamer.sty`,
Zeile 4) lädt `\RequirePackage[scaled=0.9]{helvet}`, also die Type-1-Familie `phv`. Unter
LuaTeX mit `fontspec` gibt es `phv` in der TU-Kodierung nicht, das Log meldet in jedem Deck
`Font shape 'TU/phv/m/n' undefined ... defaults substituted`. Der Header setzt zwar
`\setmainfont{Source Sans Pro}`, aber Beamer setzt in der *Sans*-Familie, und die bleibt `phv`.
Die Mathe-Fonts verbiegt Beamers Standard-Fonttheme zusätzlich Richtung serifenlos, was mit dem
Fallback zusammen die aufrechten Buchstaben ergibt.

Fix (getestet an VL 2, Schriftwarnungen weg, Textschrift Source Sans Pro, Mathe Latin Modern
Math kursiv, Tabellenköpfe fett): im Header direkt nach `\usetheme{hhubeamer}`

```latex
\usefonttheme{professionalfonts}
\ifLuaTeX
  \setsansfont[Ligatures=TeX]{Source Sans Pro}
\fi
```

`\setmainfont` kann bleiben (wirkt nur auf `\rmfamily`). Wer die Mathe ebenfalls serifenlos will,
nimmt stattdessen `unicode-math` mit einer Sans-Mathe-Schrift; die Kombination Source Sans Pro
plus Latin Modern Math ist aber üblich und lesbar.

### A2. Lange Folientitel laufen unter das HHU-Logo — **erledigt 2026-09-25**

Das Theme begrenzt die Titelbreite nicht; ab etwa 45 Zeichen kollidiert der Titel mit dem Logo.
Betroffen:

* VL 1, Folie 18: „Lesetext: How AMD May Get Across the CUDA Moat“ (Log: Overfull hbox, sichtbar
  abgeschnitten unter dem Logo).
* VL 2, Folie 7: „Geometrie: w steht senkrecht auf der Trenngeraden“ (berührt das Logo).
* VL 10, Folie 9: „Zwischenfrage: Wie misst man Übersetzungsqualität?“ (läuft unter das Logo).

Gekürzt auf „Lesetext: AMD und der CUDA-Graben“ (Originaltitel jetzt als Zeile auf der Folie),
„w steht senkrecht auf der Trenngeraden“, „Wie misst man Übersetzungsqualität?“. Zusätzlich
überschreibt der Header die Frametitle-Vorlage des Themes mit einer Kopie, die dem tikz-Knoten
`text width=12.4cm` gibt: ein künftig zu langer Titel bricht vor dem Logo um, statt darunter zu
laufen. (Das Theme setzt die Vorlage `hhubeamer` vor jedem Frame neu, deshalb muss die Kopie
denselben Namen tragen; `\defbeamertemplate` verweigert die Neudefinition, daher wird das interne
Makro vorher gelöscht — siehe Kommentar im Header.)

### A3. `\item[...]` mit langen Labels wird links abgeschnitten — **erledigt 2026-09-25**

Beamers `itemize` setzt das Label rechtsbündig in eine schmale Box; lange Labels ragen links über
den Folienrand hinaus. Sichtbar abgeschnitten:

* VL 2, Folie 14 „Drei Fälle“: aus `y = 1, f(x) = 0` wird „, f(x) = 0“.
* VL 3, Folie 5 „Computer Vision“ und Folie 6 „NLP“: die Task-Namen sind bis auf die letzten
  Buchstaben weg („stimation“, „ssification“, „mentation“).

Die Jahreszahlen in VL 1 (Folien 19, 21, 22) und `top-k` in VL 14 (Folie 9) sind kurz genug. Die
drei Folien sind auf `description` umgestellt (mit dem längsten Label als Breitenvorgabe); die
Labels erscheinen jetzt vollständig, rechtsbündig in HHU-Blau.

### A4. Ablaufpläne in den Titelnotizen: Foliennummern stimmen in 10 Decks nicht

Die Tabellen „Minuten → Folien“ verweisen auf Nummern, die es im Deck so nicht gibt (die Pläne
wurden offenbar vor der letzten Straffung geschrieben). Abgleich `\frametitle`-Reihenfolge gegen
Planzeilen:

| Deck | Befund |
|---|---|
| VL 1 | Plan: Folie 7 = Semesterplan, 8 = Definition. Im Deck ist 7 die Definition, 8 der Plan. Die Deck-Reihenfolge ist gewollt (Notiz auf 7: „hier beginnt der Semesterplan“), also die beiden Planzeilen tauschen. |
| VL 3 | Ab Folie 7 um eins verschoben (Plan zählt 19 Folien, Deck hat 18). |
| VL 4 | Folie 5 (S-Form basteln) ist im Plan in „2–4“ subsumiert, „5–7“ meint 6–7; Rest stimmt. |
| VL 5 | Ab Folie 5 um eins verschoben (Plan 22, Deck 21). |
| VL 6 | Ab Folie 15 um eins verschoben (Plan 18, Deck 17): „Das Muster“ ist 14, nicht 15. |
| VL 7 | Ab Folie 16 um eins verschoben, diesmal in die andere Richtung (Plan 20, Deck 21): `xy` ist 16, Universalität 17–19, Take-Home 20, Blatt 21. |
| VL 10 | Ab Folie 6 um eins verschoben (Plan 18, Deck 17). |
| VL 12 | Ab Folie 10 um eins bis zwei verschoben (Plan 17, Deck 15): VRAM ist 10, Ollama 11, Embeddings 12, Verteilung 13, JSON 14, Blatt 15. |
| VL 14 | Ab Folie 12 verschoben (Plan 19, Deck 17): Latent Space Oddity ist 12, Anwendungen 14–16, Rezept 17. |
| VL 15 | Ab Folie 8 verschoben (Plan 16, Deck 14): drei Ansätze 8, Loss 9, Dark Knowledge 10, Born Again 11, DistilBERT 12, Vibecoding 13, Abschied 14. |
| VL 2, 8, 9, 11, 13 | stimmen. |

Die Frame-Listen zum Nachsetzen stehen im Anhang.

### A5. Notizen-Fassung: Titelnotiz läuft über die Notizseite hinaus

Mit `show notes on second screen=right` passt die Titelnotiz (Ablaufplan-Tabelle plus Absätze)
nicht auf die Notizseite; in VL 1 bricht der Text mitten im Satz „Wenn die Zeit knapp wird …“ ab,
die Kürzungsreihenfolge ist im Vortrag also unsichtbar. Beamer paginiert Notizen nicht. Getestet
und ausreichend: nach der `\setbeameroption`-Zeile

```latex
\setbeamertemplate{note page}[plain]
\setbeamerfont{note page}{size=\scriptsize}
```

Damit passt die komplette VL-1-Titelnotiz auf eine Seite. Die drei `Overfull \hbox` im Log von
VL 1 (Zeile 44) stammen ebenfalls aus dieser Tabelle, nicht aus den Folien.

### A6. Blätter und Termine, die nicht zum Plan passen — **Blatt-Nummern entfernt 2026-09-25**

Alle Verweise auf Übungsblätter sind jetzt nummernfrei („Übungsblatt“, „das nächste Blatt“, „eine
Übungsaufgabe“); die Folien „Blatt N“ am Ende heißen „Übungsblatt“, „Zur Übung“ oder „Bis nächste
Woche“. Damit sind die drei Fehlzuordnungen unten (VL 6/13 → Blatt 7, VL 11 → Fälligkeit, VL 1 →
Inhalt) im Text nicht mehr falsch, aber die Reihenfolge-Frage (Blatt 6 vor VL 8, Blatt 10 vor VL 11)
bleibt eine Entscheidung für die Blätter. VL 11 sagt jetzt „das laufende Blatt ist nächsten Mittwoch
fällig“, VL 1 nennt den Inhalt des ersten Blatts richtig (lineare Algebra und NumPy), die Zulassung
heißt „8 bestandene Blätter“. Ursprünglicher Befund:

* **VL 6, Folie 17 „Blatt 6“** beschreibt „Ein Rechenbeispiel wie Beispiel 4, von Hand, klausurrelevant“.
  Das ist der Inhalt von **Blatt 7** (`eidl2026blatt07.md`: zwei ReLU-Layer, Backpropagation
  manuell). Blatt 6 ist der Autoencoder-Quelltext zum Fragenstellen. Nur „Bitte ohne generative
  KI“ passt zu Blatt 6. VL 7 (Notiz Folie 21) sagt es richtig: „Blatt 7 ist die
  Backpropagation-Rechnung“. Ebenso falsch: VL 13, Notiz Folie 16 („Rechenbeispiel von Blatt 6“).
  Falls die Blätter 6/7 getauscht werden sollen (offene Entscheidung in `TODO.md`), stimmt VL 6
  und VL 7 muss geändert werden; so oder so passt derzeit eins von beiden nicht.
* **VL 11** (06.01.): Notiz Folie 2 und Ablaufplan sagen „Blatt 10 ist heute fällig“, Notiz
  Folie 16 „für heute gilt Blatt 10 als abgegeben“. Blatt 10 ist laut `kurs-2026-27.md` erst am
  **13.01.** fällig (VL 10, Folie 17 sagt das auch). Außerdem heißt die letzte Folie „Blatt 11“,
  obwohl in dieser Woche kein Blatt herauskommt.
* **VL 1, Folie 23**: „Blatt 1 ab heute, Mathe“ und Notiz „erst Blatt 2 programmiert“. Blatt 1
  hat neben Lineare Algebra auch „Implementierung in Numpy“ (Aufgaben 5–9) und „Visualisierung mit
  Matplotlib“ (Aufgabe 10).
* **Reihenfolge Blatt 10 / VL 11**: Blatt 10 (Faltung, 1D-Signal) wird am 16.12. in der
  RNN/Transformer-Sitzung ausgegeben, die Faltungsvorlesung ist am 06.01. Dasselbe Muster wie bei
  Blatt 6 vor VL 8 (in `TODO.md` vermerkt); hier ist es noch nicht vermerkt.
* VL 1, Folie 2 „Zulassung: 8 von 11 Blättern“: `kurs-2026-27.md` spricht von 10–12 Blättern
  und 8 bestandenen; ob die Probeklausur als zwölftes Blatt mitzählt, sollte die Folie nicht
  offenlassen.

## B. Fachlich (einzelne Folien)

* **VL 5, Folie 15 „Zurück zum Perzeptron“**: `L_Perc = Σ max(0, −y_i⟨w,x_i⟩)` setzt stillschweigend
  `y_i ∈ {−1, +1}` voraus; in VL 2 (Folie 5, 13) ist `Y ∈ {0,1}` und die Regel `w + r(y − f(x))x`.
  Ohne einen Halbsatz „hier y ∈ {±1}“ ist „Für N = 1: w ± ρx“ nicht nachvollziehbar. Das Skript
  (Kapitel 08, Abschnitt „Zurück zum Perzeptron“) hat dieselbe Lücke.
* **VL 7, Folie 9 „OR“**: „Ansatz x + y? Nein: f(1,1) = 2“, dann „oder besser ReLU(x) + ReLU(y)“.
  Aber `ReLU(1) + ReLU(1) = 2` ebenfalls, und mit der auf Folie 8 (Notiz) festgelegten
  Interpretation „x ≥ 1 heißt TRUE“ ist 2 in Ordnung. Das Skript (Kapitel 12) argumentiert
  anders: nach dem Wechsel der Interpretation ist `x + y` akzeptabel, ReLU ist „noch besser, weil
  es Negatives sauber abschneidet“ (`f(−2, 1) = −1` wäre FALSE, `ReLU(−2) + ReLU(1) = 1` ist TRUE).
  Die Folie sollte das echte Gegenbeispiel zeigen, sonst findet der Hörsaal den Widerspruch.
* **VL 9, Folie 7 „Der KL-Term, geschlossen“**: „Das ist genau der negative ELBO aus Data Science“
  steht unter der KL-Formel. Im Skript (Kapitel 15) bezieht sich der Satz auf die *gesamte*
  Loss-Funktion (Rekonstruktion + KL). Auf Folie 6 verschieben.
* **VL 6, Folie 6**: `∂y_pred/∂w_1 = ⟨w_2, σ'(⟨w_1,x⟩) x⟩` ist ein Skalarprodukt, der Gradient nach
  dem Vektor `w_1` aber ein Vektor. Bei zwei skalaren Neuronen (so das Bild) ist es einfach
  `w_2 σ'(⟨w_1,x⟩) x`. Aus dem Skript übernommen (Kapitel 09, „Beispielsetup 1“), dort dieselbe
  Unschärfe.
* **VL 14, Folie 17 „Das Rezept“**: fünf Punkte; das Skript (Kapitel 24) hat sechs, Punkt 6 „Was
  kann schiefgehen?“ (Datenschutz, Kosten, Verteilungsverschiebung, Bias) fehlt. Gerade für den
  Klausur-Aufgabentyp „Anwendungskonzept“ ist der Punkt wichtig.
* **VL 8, Folie 6 „Autoencoder gegen PCA“**: Das Bild titelt „MSE PCA 0,0385, AE 0,0354“, die
  AE-Zeile sieht nicht besser aus als die PCA-Zeile; die Notiz verspricht „deutlich bessere
  Rekonstruktion“. Entweder das Bild mit einem länger bzw. nichtlinear trainierten AE neu
  erzeugen (`devnotes/make_figures.py`) oder die Aussage abschwächen („gleich gut bei k = 4;
  der Vorteil kommt bei gekrümmten Strukturen“).
* **VL 3, Notiz Folie 15**: „ℝ⁴ ⊗ ℝ¹⁰ ≅ ℝ⁴⁰, also `a.reshape(-1, 2)`“ und zwei Sätze später „das
  Beispiel mit achtzig Zahlen“; 40 oder 80.
* **VL 12, Notiz Folie 10**: „Llama2-7B ist etwa 8,6 GB groß“ passt zu keiner gängigen Fassung
  (fp16 ≈ 13,5 GB, Q4 ≈ 3,8 GB in Ollama, Q8 ≈ 7,2 GB). Prüfen oder streichen.
* **VL 8, Folie 7**: Notiz zählt „vier Tasks“, die Folie zeigt drei Wörter.
* Kleinkram, Geschmackssache: VL 7, Folie 19 nennt Pinkus für schmale tiefe Netze (das ist
  Kidger–Lyons bzw. Hanin; Pinkus 1999 ist die Breiten-Universalität) und lässt bei Yarotsky den
  log-Faktor bei der Gewichtszahl weg; VL 10, Folie 9 „BLEU (2001)“ (Paper ACL 2002, Report
  2001); VL 1, Folie 22 „2021 Diffusionsmodelle“ (DDPM ist 2020).

Alles andere Nachgerechnete stimmt: Abstandsformel und Zahlenbeispiel (VL 2), Entropieableitung,
Sigmoid-Identitäten, Softmax ohne Minus, `e^89 = inf` in float32 (VL 4), Münzwurf-Likelihood,
`dL/dz = p − y` (VL 5), δ-Rekursion und `∇_{W_k}E = δ_k z_kᵀ` (VL 6), `Q(x)` an allen
Stützstellen, Polarisationsidentität (VL 7), KL in geschlossener Form (VL 9), Attention,
BPE-Vokabulargröße (VL 10), Ausgabegrößen 28→24→12→8→4 (VL 11), Autograd-Zahlen 42/14/6 (VL 12),
Minimax (VL 13), Temperatur (VL 14), `T²`-Faktor, DistilBERT-Zahlen (VL 15).

## C. Bilder und Layout

Bilder pro Deck (`\includegraphics`): VL 1: 8, VL 2: 3, VL 3: 0 (3 Listings), VL 4: 4, VL 5: 3,
VL 6: 1, VL 7: 8, VL 8: 5, VL 9: 6, VL 10: 1, VL 11: 3, VL 12: 0 (9 Listings), VL 13: 1,
VL 14: 4, VL 15: 0.

Wo ein Bild fehlt und leicht zu haben wäre (eigene Skizze, kein Lizenzproblem):

* **VL 10**: Transformer-Block (Attention, MLP, Residual, LayerNorm) zu Folie 11, und eine
  LSTM-/GRU-Zelle zu Folie 6. Neun reine Textfolien am Stück (9–17) für die wichtigste Architektur
  des Kurses.
* **VL 15**: kein einziges Bild. Ein Lehrer-Schüler-Schema mit weichen Wahrscheinlichkeiten zu
  Folie 9/10 („Dark Knowledge“) trägt die Take-Home-Message.
* **VL 13**: Ab Folie 5 nur Text; die Induktion (Folien 13–15) ruft nach einer DAG-Skizze.
* **VL 6**: Beispiel 4 als Berechnungsgraph mit den δ-Pfeilen rückwärts (Folie 14 ist die, „die
  hängen bleiben soll“).
* **VL 3**: das Batch-Bild `(32, 3, 28, 28)` als gestapelte Matrizen (Folie 16); die TODO nennt es
  als Vorlesungsstoff, ein Bild gibt es in `images/` nicht.

Zu klein oder unleserlich auf dem Beamer:

* VL 1, Folie 21: die drei Teaser-Bilder bei `height=0.22\textheight` sind Briefmarken, darunter
  ist die halbe Folie leer.
* VL 4, Folie 18: Plot unter dem Code bei `0.46\textwidth` kaum lesbar.
* VL 5, Folie 12: das Tafelfoto ist grau und kontrastarm; als Skizze neu zeichnen oder mit
  Schwellwert schwärzen.
* VL 7, Folie 11: drei Panels bei `0.5\textwidth`, Achsen unlesbar.
* VL 8, Folie 5: `vl06-autoencoder-schema.png` hat überlappende Beschriftungen im Bild selbst
  („Input x ∈ ℝᴰ“, „latenter Vektor“, „Rekonstruktion x̂“ laufen ineinander); in `make_figures.py`
  Abstände vergrößern.
* VL 8, Folie 17: Denoising-Beispiel bei `0.5\textwidth`, Ziffern winzig.
* VL 9, Folie 19: Message-Passing-Grafik, Knotenlabels unlesbar; auf volle Breite.
* VL 11, Folie 8: Filterbeschriftungen unlesbar (Bild ist hoch, `height=0.62`).
* VL 14, Folie 5: Bolukbasi-Figur, kein Wort lesbar; `0.7\textwidth` oder Ausschnitt.

Sonstiges Layout:

* VL 3, Folie 9: die Zeile `device = torch.device("cuda") if ... else torch.device("cpu")` brach
  mitten in `torch.` um. **Erledigt:** jetzt `device = "cuda" if torch.cuda.is_available() else "cpu"`.
* Textdichte ist überall im grünen Bereich; die dichteste Folie ist der Semesterplan (VL 1,
  Folie 8, 69 Wörter inkl. Fußzeile), alle anderen unter 66.

## D. Didaktischer Gesamteindruck

* Die Struktur jeder Sitzung trägt: „Wo wir stehen“, Kern mit einer Formel pro Folie, Take-Home,
  Blatt. Die Dialogfolien (Quizfrage Testset, „Was macht reshape?“, „Wo steckt der Zufall?“,
  „Was lernt ein Netz eigentlich?“) sind genau richtig leer.
* Die Notizen sind der eigentliche Wert der Decks (Zeitbudgets, Fragen aus 2025, Stolperstellen).
  Deshalb lohnen A4 und A5: ohne stimmende Foliennummern und mit abgeschnittener Titelnotiz ist
  die Zweitschirm-Fassung im Hörsaal nicht verlässlich.
* Rückbezüge über VL-Nummern sind konsistent geprüft (VL 2 → VL 4/5/6, VL 3 → VL 9/10/15,
  VL 8 → VL 4/5, VL 14 → VL 7/9/12) und stimmen mit dem Plan überein.
* Was ich nicht prüfen konnte: die Dialogmuster gegen die Transkript-Notizen (nicht im Repo) und
  ob die Browser-Werkzeuge im Hörsaal-Netz laufen (laut TODO am 2026-09-24 geprüft).

## Vorschlag zur Reihenfolge für den Rest

1. A5 (Notizseite, zwei Zeilen im Header) — sobald die Zweitschirm-Fassung gebraucht wird.
2. B (VL 5, 7, 9, 14) — inhaltlich, vor dem Upload nach ILIAS.
3. C (Bildgrößen, fehlende Bilder) — je Deck fünf Minuten, Bilder für VL 10/13/15 länger.
4. A4 (Ablaufpläne) zuletzt, wenn die Folienreihenfolge steht.

## Anhang: Frame-Listen der Decks mit falschem Ablaufplan

Nummer:Titel, gekürzt.

* **VL 1**: 1 Titel | 2 Organisatorisches | 3 Material | 4 Keine Angst vor | 5 Was wir zusammen lernen | 6 Eingangsumfrage | 7 Der Name ist erfreulich ehrlich | 8 Der grobe Plan | 9 Python Katastrophe | 10 Python perfekt | 11 Woher kommen die Daten | 12 Generatives Modell | 13 Supervised/Unsupervised | 14 Regression/Klassifikation | 15 Klassifikation als Regression | 16 Wie gut ist das Modell | 17 Quizfrage | 18 Lesetext | 19 bis 2010 | 20 1958 | 21 2010–2015 | 22 nach 2015 | 23 In die Praxis
* **VL 3**: 1 Titel | 2 Wo wir stehen | 3 Hugging Face | 4 Wonach sortiert | 5 Computer Vision | 6 NLP | 7 Übersetzen | 8 Muster | 9 GPU | 10 Installation | 11 Vier Fragen | 12 Tensor ≈ Array | 13 Tensorprodukt | 14 Dualraum | 15 Quizfrage | 16 Batch-Bild | 17 Warum wichtig | 18 Blatt 3
* **VL 4**: 1 Titel | 2 Wo wir stehen | 3 Lin. Regression zur Klassifikation | 4 Zweidimensional | 5 S-Form | 6 Odds | 7 Skala schief | 8 Logit | 9 Entropie | 10 Logistische Funktion | 11 Sigmoid/tanh | 12 Symmetrie | 13 invers | 14 Interpretation | 15 Log. Regression | 16 PyTorch linear | 17 Trainingsschleife | 18 logistisch | 19 Softmax | 20 Wann Softmax | 21 Numerik | 22 Blatt 4
* **VL 5**: 1 Titel | 2 Zwei Modelle | 3 Einheitliche Antwort | 4 BCE | 5 Maximum Likelihood | 6 Logarithmieren | 7 ML von Hand | 8 Wie minimiert man | 9 Approximativ | 10 Richtung | 11 Absteigen | 12 Ein Schritt | 13 Lernrate | 14 Explorer | 15 Perzeptron | 16 Log. Regression | 17 Drei Loss | 18 Skalieren | 19 Take-Home | 20 Zufall | 21 Bis nächste Woche
* **VL 6**: 1 Titel | 2 Ziel | 3 Was wir haben | 4 Setup 1 | 5 Zwei Bausteine | 6 Update-Regeln | 7 Mehr Dimensionen | 8 Eine Schicht | 9 Beispiel 4 | 10 Vorwärts | 11 Rückwärts Ausgabe | 12 Bekannt vom Neuron | 13 Eine Schicht zurück | 14 Das Muster | 15 PyTorch | 16 Kosten | 17 Blatt 6
* **VL 7**: 1 Titel | 2 Haben/Fehlt | 3 Funktionen lernen | 4 ReLU | 5 Warum ReLU | 6 Sterbende Neuronen | 7 Zwei Auswege | 8 NOT | 9 OR | 10 OR/NOR | 11 XOR | 12 Optimierer | 13 Arithmetik | 14 x² | 15 Interpolation | 16 xy | 17 Universell | 18 Stufe | 19 Präziser | 20 Take-Home | 21 Blatt 7
* **VL 10**: 1 Titel | 2 Sequenzen | 3 RNN | 4 Entfaltet | 5 Skip | 6 Gated | 7 LSTM Code | 8 Geschichte | 9 BLEU | 10 Attention | 11 Block | 12 Reihenfolge | 13 GPT | 14 BPE | 15 BERT | 16 ViT | 17 Winterpause
* **VL 12**: 1 Titel | 2 Zwei Hälften | 3 Kleines Netz | 4 Graph | 5 backward | 6 Optimizer | 7 Freezing | 8 Geteilte Gewichte | 9 Zehn Wege | 10 VRAM | 11 Ollama | 12 Embeddings | 13 Verteilung | 14 JSON | 15 Blatt 11
* **VL 14**: 1 Titel | 2 Wo wir stehen | 3 Arithmetik | 4 Richtungen | 5 Bolukbasi | 6 Interpolation | 7 Bildraum | 8 Diskret | 9 Vier Wege | 10 Temperatur | 11 AE/VAE/GAN | 12 Geometrie krumm | 13 Herausholen | 14 hAInrich | 15 E-Mails | 16 Empfehlung | 17 Rezept
* **VL 15**: 1 Titel | 2 Letzte Vorlesung | 3 Eine Funktion | 4 Ansatz 1 | 5 Ansatz 2 | 6 Suche/Regression | 7 Compression | 8 Drei Ansätze | 9 Loss | 10 Dark Knowledge | 11 Born Again | 12 DistilBERT | 13 Vibecoding | 14 Das war's
