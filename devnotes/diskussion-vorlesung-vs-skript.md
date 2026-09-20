# Diskussion: Was die Aufzeichnungen 2025/26 über das Skript sagen

**Status: abgeschlossen.** Konrad hat am 2026-09-20 zu allen acht Fragen entschieden, die Entscheidungen sind am selben
Tag umgesetzt (Details in `TODO.md`, Abschnitt „Erledigt 2026-09-20“). Kapitel werden unten mit Namen genannt, weil die
Nummern seit dem Split am 2026-09-20 (neues Kapitel „Loss-Funktionen und Maximum Likelihood“, 27 statt 26) anders sind.

| Frage | Entscheidung | Umsetzung |
|---|---|---|
| 1 VL-Tabelle | Nach dem Ist 2025 als guter Plan für WiSe 2026/27 umbauen | `kurs-2026-27.md`, neue Tabelle mit Anmerkungen; „Optimierer“ und „Adversarial Attacks“ sind Reserve |
| 2 Kernmomente | Beweise und Argumente, die der Dozent als zentral bezeichnet, ins Skript | Ein-Sample-Beweis (Perzeptron trainieren), Batch-Bild (Tensoren), VAE gegen PCA/EM (VAE), „früh aufhören“ (GANs). Dialogmuster bleiben draußen → Dozentennotizen zu den Decks, siehe `TODO.md` |
| 3 Vertiefungen | Sichtbar markieren | Aufklappbare Boxen „Vertiefung: …“: Konvergenzsatz, Cauchy-Schwarz, Spur-Trick, Message-Passing-Formel, Wasserstein-Dualität, FGSM |
| 4 Browser-Werkzeuge | Verlinken und benutzen, solange sie leben | Boxen „Ausprobieren“ mit dem, was 2025 gezeigt wurde: Playground, Loss Landscape Explorer, GAN Lab |
| 5 Folien | Aus dem Skript neu generieren | Festgehalten in `TODO.md`, Abschnitt Beamer-Folien |
| 6 Übungstipps | In die Blätter, wo die Studierenden sie sehen | Boxen „Hinweise“ in Blatt 1 bis 6 und 11, mit den Ansagen aus 2025; die Abschnitte „Tipps zu Übungsblatt N“ in den Kapiteln sind weg |
| 7 Klausuransagen | Keine weiteren übernehmen | nichts |
| 8 Offene Versprechen | CUDA/ROCm beantworten; wav2vec nicht weiter; Zeitreihen später | Antwortbox in „Was ist Deep Learning?“; wav2vec entfällt im Plan; Zeitreihen in `TODO.md` zurückgestellt |

Dazu, ohne eigene Frage: alle Snippets aus `vorschlag-grundlagen.md` sind eingebaut.

---

Der ursprüngliche Diskussionstext folgt unverändert, als Begründung der Entscheidungen.

Stand: 2026-09-20. Grundlage sind die 15 Sitzungsnotizen in `transcripts/*/notiz.md` und der
`transcripts/abschlussbericht.md`, abgeglichen mit `TODO.md`, `vorschlag-grundlagen.md` und dem
damaligen Kapitelschnitt (26 Kapitel). Zum Zeitpunkt des Schreibens war kein Punkt umgesetzt; der Stand danach steht oben. Jeder Abschnitt endet mit einer
Entscheidungsfrage; die Vorschläge sind bewusst zugespitzt, damit man widersprechen kann.

Zwei Vorbemerkungen, die alles Weitere relativieren:

1. Das Skript ist aus den Folien gebaut. Die Folien sind aber nur der Teil der Vorlesung, der
   ohnehin schriftlich war. Was die Sitzungen tragen, ist überwiegend nicht auf den Folien:
   Tafelbeweise, Hörsaaldialoge, Browser-Werkzeuge, Anekdoten, Warnungen. Die Frage ist also nicht
   nur „was fehlt im Skript“, sondern „was davon gehört überhaupt in ein Skript“.
2. Das Skript ist semesterunabhängig und thematisch geschnitten, die Vorlesung lief wöchentlich
   und hat sich fast jede Woche verschoben. Ein Teil der Abweichungen ist deshalb kein Mangel des
   Skripts, sondern ein Argument gegen die VL-Tabelle in `kurs-2026-27.md`.

---

## 1. Die Verschiebungskette ist der wichtigste Befund, und er betrifft nicht das Skript

**Beobachtung.** Zehn von fünfzehn Sitzungen beginnen mit dem Rest der vorigen oder enden mit
einem Vorgriff auf die nächste. Die größten Brüche: VL 1 erreicht das Perzeptron nicht; VL 3 trägt
eine halbe Stunde Hugging Face aus VL 2 und greift 18 Minuten auf VL 4 vor; VL 4 greift 12 Minuten
auf VL 5 vor; VL 6 schafft von drei Themen eines; VL 10 beginnt mit 22 Minuten Transformer; VL 12
mit 18 Minuten LLM-Notebook. Die Tipps zu Blatt 1 und Blatt 6 wurden nie gezeigt.

**Was das für das Skript heißt.** Nichts direkt. Es heißt aber etwas für die VL-Tabelle, die den
Plan von 2025 fast unverändert übernimmt. Die Tabelle setzt zum Beispiel für VL 6 wieder drei
Kapitel an (Backpropagation, Aktivierungsfunktionen, Autoencoder-Idee), obwohl 2025 in 94 Minuten
nur Backpropagation geschafft wurde. Für VL 9 stehen Graphen, RNN und Transformer, obwohl der
Transformer 2025 nach 7 Minuten abbrach.

**Vorschlag.** Die VL-Tabelle nicht aus dem Plan 2025, sondern aus dem Ist 2025 ableiten, und dann
bewusst entscheiden, was gestrichen wird, damit die Kette abreißt. Konkret:

- VL 1 ist eine Orientierungssitzung, ohne Perzeptron. Kapitel „Neuron und Perzeptron“ gehört ganz in VL 2.
- VL 2 trägt Kapitel „Neuron und Perzeptron“ und „Das Perzeptron trainieren“ und nur den Ausblick auf Hugging Face. Kapitel „Vortrainierte Modelle“ komplett in VL 3.
- VL 3 bekommt Kapitel „Vortrainierte Modelle“ und „Tensoren“, ohne Vorgriff auf die logistische Regression. Die Odds und die
  S-Form beginnen erst in VL 4, wo sie 2025 ohnehin wiederholt wurden.
- VL 6 bekommt nur Kapitel „Backpropagation“. Aktivierungsfunktionen und Netze von Hand in VL 7,
  Autoencoder beginnt erst in VL 7 zweite Hälfte oder VL 8.
- VL 9 ohne Transformer, VL 10 mit Transformer vor der Faltung, oder Faltung vor
  Transformer und den Transformer in VL 11 statt der Wiederholung.

**Gegenargument.** Die Vorgriffe waren teils Absicht („das nächste Mal wiederholen wir das“) und
haben als Spirale funktioniert; VL 4 ging mit der Wiederholung der Odds flüssig los. Der Preis war
die Zeit in VL 3 und VL 5, in denen der Stoff nach 60 bis 75 Minuten durch war.

**Entscheidung:** Tabelle nach Ist umbauen, oder den Plan behalten und im Skript je Kapitel
markieren, was bei Zeitnot wegfällt?

---

## 2. Was in den Sitzungen den Unterschied machte, steht nicht im Skript

Die Notizen benennen je Sitzung den Moment, den der Dozent selbst als zentral bezeichnet oder der
den Dialog getragen hat. Auffällig oft ist das etwas, das *nicht* auf den Folien stand und deshalb
auch nicht im Skript steht. Sortiert nach Gewicht:

| Sitzung | Kernmoment laut Notiz | Im Skript? |
|---|---|---|
| VL 2 | Tafelbeweis, dass die Perzeptronregel für ein einzelnes Sample funktioniert (Winkel, Bilinearität). Vom Dozenten als das Wichtigste der Sitzung bezeichnet | Nein. Kapitel „Das Perzeptron trainieren“ hat einen Satz „schiebt die Hyperebene in Richtung des Punkts“ und nennt den Konvergenzsatz. Der Ein-Sample-Beweis fehlt |
| VL 2, 3, 4 | „Type-Check“ als Argumentationsmuster: aus den Typen in der Formel folgt, dass r ein Skalar und b reell sein muss | Nein, nirgends |
| VL 3 | Tafeleinschübe zu Tensoren: liegende Vektoren als Dualraum, Skalare hin und her schieben, Reshape mit 80 Zahlen, „der dritte Index stapelt Matrizen, das ist der Batch“ | Teilweise (`reshape`-Antwort laut TODO). Das Batch-Bild fehlt |
| VL 5 | Das Minus vor dem Gradienten kommt erst durch einen Einwand aus dem Hörsaal; die Frage „wo steckt Zufall“ wird 20 Minuten offen gehalten und dann aufgelöst (Startvektor, Daten, Reihenfolge) | Das Minus ja; die Zufalls-Klammer nein |
| VL 5 | Loss Landscape Explorer und TensorFlow Playground, 23 Minuten, mit XOR von Hand und Universalität über Treppenfunktionen | Ein Link in „Gradientenabstieg“ und ein Satz in „Backpropagation“. Das Playground-XOR ist die einzige Übung, die in VL 5, 6 und 7 als „hoffentlich gemacht“ vorausgesetzt wurde |
| VL 7 | Hörsaal schlägt Aktivierungsfunktionen vor (Heaviside, 1 minus x, f selbst), jeder Vorschlag wird am Gegenbeispiel Eingabe 100 geprüft | Nein. Kapitel „Netze von Hand“ gibt die Lösungen, nicht die Fehlversuche |
| VL 8 | „Mu und Sigma sind erfundene Parameter des Encoders; ein linearer AE ohne Sigmoid ist PCA; der VAE gibt jedem Punkt eine eigene Verteilung statt fünf Cluster“ als Antwort auf zwei Hörsaalfragen | PCA-Bezug nein, EM-Gegenüberstellung nein |
| VL 9 | wav2vec-Brainstorming bis Contrastive Learning; der Dozent sagt selbst, das sei eine Klausurfrage, sobald es eine Übung dazu gibt | Nein |
| VL 12 | Regel „früh aufhören“ aus dem GAN Lab, Loss-Kurve des Tutorials als Dialog gelesen | GAN Lab ist verlinkt, die Regel nicht |
| VL 13 | Der Anwendungsteil als Spiel: Hörsaal schlägt jeden Schritt vor, Folie bestätigt. Schrittfolge: was haben wir, kein großes Modell, Vektor je Frage, Nachbarsuche, vom String zum Vektor, Güte messen | Kapitel „Anwendungsbeispiele“ zeigt nur das Ergebnis |
| VL 14 | Suche gegen Regression als roter Faden, mit dem Bild „Gebirge mit Zäunen“ | Suche und Regression ja, das Bild nein |
| VL 15 | Fragestunde: UMAP-Voraussetzungen, Singularitäten, topologische Regularisierung, orthogonale Updates | Nein, und laut Ansage nicht klausurrelevant |

**Vorschlag.** Drei Sorten auseinanderhalten:

- **Beweise und Argumente**, die der Dozent selbst als zentral bezeichnet, gehören ins Skript:
  der Ein-Sample-Beweis (VL 2), das Batch-Bild (VL 3), der PCA-Bezug des linearen Autoencoders
  (VL 8, kommt in VL 14 wieder), die Regel „früh aufhören“ (VL 12). Das sind vier Absätze.
- **Dialogmuster** (Type-Check, Gegenbeispiel Eingabe 100, das Spiel in VL 13, die offene
  Zufallsfrage) gehören nicht ins Skript, sondern in Dozentennotizen zu den Beamer-Decks
  (Schritt 4 des Migrationsplans). Ein Skript, das die Fehlversuche mitliefert, nimmt der
  Vorlesung die Pointe.
- **Browser-Werkzeuge** (Playground, Loss Landscape Explorer, GAN Lab): siehe Abschnitt 4.

**Gegenargument.** `vorschlag-grundlagen.md` fügt schon 2200 Wörter hinzu. Jeder weitere Absatz
konkurriert damit. Der Ein-Sample-Beweis ist aber genau die Lücke, die Snippet 2 (Abstand zur
Hyperebene) und 5B (Gradient p minus y) dort umkreisen, ohne sie zu schließen; er wäre der
Anschluss zwischen beiden.

**Entscheidung:** Welche der vier Absätze kommen ins Skript, und wo landen die Dozentennotizen?

---

## 3. Das Skript ist an mehreren Stellen dichter als die Vorlesung je war

Umgekehrt listen die Notizen unter „im Material, aber nicht in der Sitzung“ Dinge, die in keiner
der 15 Sitzungen vorkamen, obwohl das Kapitel dran war:

- Kapitel „Neuron und Perzeptron“ und „Das Perzeptron trainieren“: McCulloch-Pitts formal, Definition linear trennbar, XOR-Konstruktion mit zwei
  Perzeptrons, Konvergenzsatz. XOR kam erst in VL 7 von Hand.
- Kapitel „Gradientenabstieg“: Kettenregel mit Jacobi-Matrix, Cauchy-Schwarz, Hinge-Loss, Normalgleichungen als Name.
- Kapitel „Backpropagation“: Spur-Trick, Delta-Muster, Aufwand als doppelte Inferenz. Der Induktionsteil bekam in
  VL 13 sechs Minuten, die Fließtextfolie wurde ausdrücklich zum Zuhauselesen übersprungen.
- Kapitel „Graphen“ bis „Transformer“: Message-Passing-Formel, RNN-Formel mit W, U, V, LSTM-Gates namentlich,
  BLEU-Definition, Attention-Formel. In der Sitzung lief alles über Bilder und Adjazenzmatrix.
- Kapitel „Faltung und CNNs“: Ausgabegrößen-Formel, Parameter Sharing, Translationsäquivarianz, formale 2D-Definition
  (in der Sitzung „ausdrücklich nur mündlich“).
- Kapitel „GANs“: Minimax-Formel, Wasserstein-Mathematik, StyleGAN mit Mapping-Netz.
- Kapitel „Optimierer“ und „Adversarial Attacks“: Momentum- und Adam-Formeln, FGSM.

Dazu kommt die TODO-Liste „Fachliche Durchsicht“, die genau diese Stellen als „über die Folien
hinausgehend“ führt.

**Zwei Lesarten.**

- *Das Skript ergänzt, was die Vorlesung mündlich lässt.* Dann ist das gut so, und die Vorlesung
  darf mündlich bleiben. Der Klausurabgleich stützt das: die Klausur fragt Translationsäquivarianz,
  Parameter Sharing, 1x1-Faltung, Reparametrisierung, alles Dinge, die 2025 nur im Skript stünden.
- *Das Skript hebt den Kurs auf ein Niveau, das die Vorlesung nicht einlöst.* Wer nach VL 9 die
  Attention-Formel im Skript liest, hat sie nie erklärt bekommen. Die Klausur 2025 hat sie nicht
  gefragt (Klausurabgleich: „Softmax summiert zu 1“ ist das Transformer-Item).

**Vorschlag.** Die Liste in TODO „Fachliche Durchsicht“ in zwei Spalten teilen: (a) im Skript
und Vorlesung 2026 vorgesehen, (b) nur im Skript, als Vertiefung markiert (Admonition „Für
Neugierige“ oder ein Abschnitt am Kapitelende). Kandidaten für (b): Konvergenzsatz, Cauchy-Schwarz,
Spur-Trick, Message-Passing-Formel, Wasserstein-Mathematik, FGSM. Kandidaten für (a), weil sie in
der Klausur vorkommen oder 2025 mündlich behandelt wurden: Ausgabegrößen-Formel, Parameter Sharing,
Reparametrisierung, Minimax als Formel (VL 12 kam sie nur über das Tutorial).

**Entscheidung:** Vertiefungen sichtbar markieren, oder das Skript bewusst als Obermenge lassen?

---

## 4. Live-Coding gibt es nicht, aber Browser-Werkzeuge tragen ein Zehntel der Zeit

**Beobachtung.** Im ganzen Kurs entstehen unter zehn Minuten Code live. Notebooks werden gezeigt,
nicht geschrieben (VL 10, 11, 12). Dafür laufen rund 110 Minuten in Browser-Werkzeugen: ILIAS-Umfrage
(VL 1), Loss Landscape Explorer und TensorFlow Playground (VL 5, 23 Minuten), nanoGPT, conv_arithmetic
und Harleys MNIST-CNN (VL 10, 20 Minuten), Ollama im Terminal (VL 11), GAN Lab, thispersondoesnotexist
und das PyTorch-Tutorial (VL 12, 22 Minuten), Gemini-Vibecoding (VL 14, 25 Minuten).

**Was das für das Skript heißt.** Das Skript hat die Notebooks in Prosa übernommen (gut, weil sie
ohnehin nur gezeigt wurden). Die Browser-Werkzeuge sind aber Links am Rand, obwohl sie in der
Sitzung das Konzept getragen haben: das Playground-XOR ist die einzige durchgehende Übung von VL 5
bis VL 7, das GAN Lab liefert die Regel „früh aufhören“, der Loss Landscape Explorer die
Diskussion zu Lernrate, Neuinitialisierung und Abbruch.

**Vorschlag.** Je Werkzeug eine Box „Ausprobieren“ mit dem, was 2025 daran gezeigt wurde: beim
Playground die Aufgabe, XOR mit sechs Gewichten von Hand zu lösen, und die Beobachtungen zu
redundanten Neuronen und krummen Gewichten; beim Loss Landscape Explorer drei Lernraten und was
passiert; beim GAN Lab der lineare Datensatz, der ins lokale Minimum läuft. Das ersetzt keine
Übungsaufgabe, gibt dem Link aber einen Zweck.

**Gegenargument.** Web-Werkzeuge sterben. Der Loss Landscape Explorer und das GAN Lab sind
Forschungsprototypen. Eine Box, die auf ein totes Werkzeug zeigt, ist schlimmer als ein Link.

**Entscheidung:** Boxen schreiben, oder die Werkzeuge in die Beamer-Decks verlagern und im Skript
nur verlinken?

---

## 5. Unstimmigkeiten, die 2025 im Hörsaal entstanden sind

Diese Punkte sind klein, aber sie haben Zeit gekostet oder zu falschen Aussagen geführt:

| Stelle | Was passierte | Skript | Handlung |
|---|---|---|---|
| Softmax-Folie VL 4 | Dozent hält Formel für falsch (fehlendes Minus), VL 5 beginnt mit Nachtrag an der Tafel | Formel ohne Minus, korrekt | Folie 2026 mit einem Halbsatz „kein Minus, das ist Absicht“ versehen; Kapitel „Logistische Regression“ könnte den Fall K gleich 2 als Probe zeigen |
| Sparse-AE-Code VL 8 | Penalty wird im gezeigten Code nicht zum Loss addiert, live bemerkt | Kapitel „Autoencoder“ zeigt Code-Funktion; prüfen, ob der Fehler übernommen wurde | Code in 13 gegen den Loss prüfen |
| VAE-Loss-Begründung VL 8 | Sitzung: Sigma explodiert. Skript: Sigma geht gegen null | Beide richtig, je eine Hälfte | Kapitel „VAE“ beide Richtungen nennen |
| Encoder-Sigmoid VL 7 | Sitzung mit Sigmoid am Encoder-Ende, Skript ohne | Abweichung | Entscheiden, Begründung „wegen späterem Sampeln“ aus der Sitzung übernehmen oder streichen |
| BLEU VL 9 | Folie arithmetisch, Skript geometrisch | Skript richtig | Folie angleichen |
| Notebook VL 10 | `padding=1` mit falschem Kommentar, Kapitel nutzt `padding=2` | Skript richtig | Notebook angleichen (bleibt als Referenz) |
| Wasserstein VL 12 | Folie und Sitzung: Werte in [0,1]; Skript: reelle Zahl | Skript richtig | Folie angleichen |
| Top-k und Softmax VL 13 | Vergleichszeichen verdreht, Minus fehlt | Skript richtig | Folien angleichen |
| Interpolationsformel VL 7 | Dozent warnt, die Formel aus Gemini sei falsch gewesen | Kapitel „Netze von Hand“ hat die korrigierte Formel? | Bei der fachlichen Durchsicht die Interpolation in 11 nachrechnen |

Fünf der neun Punkte sind Folienfehler, die das Skript schon richtig hat. Das spricht dafür, die
Beamer-Decks 2026 aus dem Skript zu speisen (TODO, Entscheidung „Folien aus MyST oder von Hand“)
und nicht aus den Google-Slides 2025.

---

## 6. Übungsblätter: was die Vorlesung dazu wirklich gesagt hat

Die Notizen sammeln alle Übungsansagen. Die Bilanz ist dünn: Tipps zu Blatt 1 nie, zu Blatt 5
nie (nur auf der Folie), zu Blatt 6 nie, zu Blatt 9 nie. Gesagt wurde:

- Blatt 2: Perzeptronregel direkt, nicht das verallgemeinerte Perzeptron; 2D-Daten scattern;
  mehrere Epochen; `make_blobs` zuerst; der verlinkte Code ist „Ugly Code“.
- Blatt 3: Betragsfunktion ist banal, aber wichtig; die umdefinierte Vorzeichenfunktion ist auch
  eine schwache Ableitung; Integrale ignorieren.
- Blatt 4: Loss-Kurve beobachten, zum Debuggen alle Daten ins Training und keinen Train-Test-Split.
- Blatt 11: Code Zeile für Zeile verstehen, BERT Mini gegen Medium vergleichen.
- Übungsblatt-Hinweis VL 10: mit der Vorlesungsformel falten, nicht mit der PyTorch-Variante.

**Beobachtung dazu.** Der Blatt-4-Tipp („ohne Train-Test-Split debuggen“) widerspricht scheinbar
VL 1 und ist genau die Art Hinweis, die im Skript fehlt. `vorschlag-grundlagen.md` Snippet 6
(logistische Regression hört nie auf) und Snippet 11 (`nan`-Loss) zielen in dieselbe Richtung.

**Vorschlag.** Die „Tipps zu Übungsblatt N“-Abschnitte im Skript gegen diese Liste abgleichen.
Wo die Vorlesung 2025 etwas gesagt hat, das im Skript-Tipp fehlt (Blatt 2 „Ugly Code“, Blatt 3
Vorzeichenfunktion, Blatt 4 Debug-Regel), ergänzen. Wo das Skript Tipps hat, die nie gesagt
wurden (Blatt 1, 5, 6, 9), prüfen, ob sie in der Übung statt in der Vorlesung gehören.

**Entscheidung:** Tipps als Skript-Abschnitt lassen, oder in die Blätter selbst verschieben, wo
die Studierenden sie beim Bearbeiten sehen?

---

## 7. Klausur: was angesagt wurde, und was das Skript daraus macht

Ansagen 2025: „beim Ableiten immer sagen, wonach“ (VL 5, „in jeder Klausur ein Fehler“); ein
Rechenbeispiel wie Beispiel 4 aus VL 6 kann drankommen; Training des Empfehlungssystems ist
mögliche Klausurfrage (VL 13); Klausur prüft, was in den Übungen geübt wurde (VL 10); VL 15 nicht
klausurrelevant; alte Klausur auf ILIAS.

**Abgleich.** `klausur-abdeckung.md` prüft Begriffe, nicht diese Ansagen. Zwei Lücken:

- „Wonach wird abgeleitet“ ist Snippet 7 in `vorschlag-grundlagen.md`. Die Klausurwarnung aus
  VL 5 wäre der Aufhänger dafür, im Skript und im Blatt.
- Das Empfehlungssystem steht in Kapitel „Anwendungsbeispiele“ als Beispiel, aber die Trainingsfrage, die als
  Klausurfrage angekündigt wurde, ist dort nicht ausformuliert. Der TODO-Punkt „Rezept
  Anwendungskonzept“ ist genau diese Lücke.

**Entscheidung:** Die Klausuransagen aus den Notizen in `klausur-abdeckung.md` aufnehmen?

---

## 8. Was die Vorlesung verspricht und dann nicht liefert

Drei Ankündigungen aus den Sitzungen blieben offen und stehen auch nicht im Skript:

- VL 1: CUDA gegen ROCm als „Hausaufgabe“. Kapitel „Was ist Deep Learning?“ stellt die Frage, beantwortet sie nicht.
- VL 9: „ich brauche eine bessere Übungsaufgabe zu wav2vec, bevor ich das als Klausuraufgabe
  stellen kann.“ Es gibt keine.
- VL 14: Anregung Aktienkurse mitgenommen, VL 15 macht nichts damit; Zeitreihen bleiben unbehandelt,
  obwohl `ASML.csv` im Notebook-Ordner liegt und Kapitel „RNNs“ RNNs erklärt.

**Vorschlag.** Die ersten beiden als kleine Übungsaufgaben (Blatt 1 und Blatt 9) statt als
offene Fragen. Die dritte ist ein Argument, Kapitel „RNNs“ mit einem Zeitreihen-Beispiel an ASML zu
schließen, oder das Versprechen 2026 nicht mehr zu geben.

---

## 9. Was nicht geändert werden sollte

Damit die Diskussion nicht nur Änderungen sammelt:

- Der thematische Schnitt ohne VL-Nummern hat sich bewährt. Die Verschiebungskette 2025 zeigt,
  dass VL-Nummern in Kapitelnamen nach zwei Wochen falsch gewesen wären.
- Die Notebooks in Prosa zu übernehmen war richtig: 2025 wurden sie ohnehin nur vorgelesen.
- Kapitel „Anwendungsbeispiele“ als Dialog-Ergebnis zu lassen ist richtig, solange das Spiel im Hörsaal erhalten
  bleibt. Wer das Skript vorher liest, spielt schlechter mit; das ist 2025 bewusst so gemacht
  worden („wer hat die Folien vorab gelesen?“).
- Kapitel „Optimierer“ und „Adversarial Attacks“ dürfen dünn bleiben. VL 15 war nicht klausurrelevant, und die Fragestunde
  war stark, weil sie nicht vorbereitet war.

---

## Zusammenfassung der Entscheidungen

Siehe die Tabelle am Anfang des Dokuments.
