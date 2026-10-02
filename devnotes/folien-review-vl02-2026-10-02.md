# Durchsicht des VL-2-Decks (2026-10-02)

Geprüft wurde `slides/Einführung in Deep Learning 2026 VL 02 Neuron und Perzeptron.tex` nach
der Prüfliste in `~/Sciebo/hhu/PLAYBOOK-folien.md` §3: Bau von Null, Kontaktbogen,
Notizenfassung, Ablaufplan gegen die Frame-Reihenfolge, Ansagen gegen `kurs-2026-27.md` und das
Blatt, Fakten gegen die Kapitel 02 und 03, Dialogmuster gegen
`transcripts/vl02-perzeptron-2025/notiz.md`. Alle Befunde sind am selben Tag umgesetzt.

**Ausgangslage:** 20 Folien, 0 zu volle Rahmen, Notizenfassung vollständig (der Header-Fix
vom Vormittag), Ablaufplan stimmte (Befund A4 vom 25.09. galt für VL 2 nicht), Termine
richtig. Nachgerechnet und richtig: Abstandsbeispiel mit $w=(3,4)$, Sigmoid-Werte auf
Folie 9, die drei Fälle, $w^{(k)}\cdot x$ auf Folie 15, die Linearitätsrechnung auf
Folie 19, Novikoffs Schranke, die Shape von `nn.Linear`.

## A. Fachlich

| | Befund | Umsetzung |
|---|---|---|
| **A1** | **σ gegen τ.** Kapitel 02 legt fest: τ ist die beliebige Aktivierungsfunktion, σ immer die logistische. Folie 3 (`y = σ(ζ)`, Notiz „σ ist eine Schwellenwertfunktion“) und Folie 18 (`h = σ(Wx+b)`) brachen das, Folie 17 hatte τ. Wurzel: `make_figures.py` beschriftete `vl01-neuron.png` mit σ – das Bild steht im Kapitel, in VL 1 (Folie 20) und in VL 2 | Ein Zeichen in `make_figures.py`, Bild neu erzeugt (`images/vl01-neuron.png`), Folien 3 und 18 auf τ, Notiz zu Folie 3 nennt die Konvention |
| **A2** | **Fünf Fragen, drei Antworten.** Folie 12 fragt; Zielgröße und Hyperparameter standen nur in Notizen, die Initialisierung nirgends (Kapitel 03 hat sie, 2025 wurde danach gefragt) | Neue Folie 21 „Die fünf Antworten für das Perzeptron“ vor dem Übungsblatt, zugleich die Take-Home-Folie; Initialisierung in der Notiz zu Folie 16 |
| **A3** | **XOR versprochen, nicht eingelöst.** Folie 11 zeigt das Gegenbeispiel, die Auflösung stand nur in der Notiz zu Folie 18 (Playbook §2.8) | Neue Folie 19 „XOR, aufgelöst“ mit `vl07-xor-region.png` (OR, NAND, UND – das Bild gab es schon für VL 7) und den drei Perzeptron-Formeln |
| **A4** | **Der Bias wird nie explizit gelernt**; 2025 gab es die Update-Zeile mit Type-Check, das Blatt braucht b | Zeile auf Folie 14: $b_{\text{neu}} = b + \rho\,(y-f(x))$ mit $x_0 = 1$, Type-Check in der Notiz |
| **A5** | Fragen aus 2025 ohne Vorbereitung im Deck: MLP gegen neuronales Netz, Nullvektor als Start, rückblickend perfekte Lernrate | Je ein Absatz in den Notizen zu Folie 18, 16 und 13 |

## B. Form und Kleinkram

| | Befund | Umsetzung |
|---|---|---|
| **B1** | Folie 16: vier Panels bei 0.8 der Breite, Fehlerraten in den Paneltiteln unlesbar | Neue Funktion `vl02_perceptron_updates_folie()` in `make_figures.py`: zwei Panels (Start, nach drei Epochen), gleiche Daten und Lernrate; das Buch behält die vier Stufen. Bei 0.9 der Breite lief der Rahmen 21 pt über, 0.7 passt |
| **B2** | Ablaufplan: Zeile 75–82 nannte für Folie 16 nur das verallgemeinerte Perzeptron | Zeile umbenannt; die zwei neuen Folien eingetragen, Summe bleibt 90 Minuten |
| **B3** | Folie 20, Notiz: „Der verlinkte Code ist Ugly Code“ setzt einen Link auf dem Blatt voraus, den die 2025er Markdown-Fassung nicht hat; das Blatt nennt Iris, die Folie nicht | Notiz mit Vorbehalt („falls das Blatt den Link noch hat, vorher am TeX-Blatt nachsehen“), Punkte um Iris und „Fehler auf Train und Test zählen“ ergänzt; Prüfpunkt in `TODO.md` |
| **B4** | `kurs-2026-27.md`: „Hugging Face nur als Ausblick“, im Deck ein halber Satz | Ein Satz in der Notiz zur letzten Folie |
| **B5** | Folie 2, Notiz: „Kapitel 1 im Skript“ – eine Kapitelnummer | Kapiteltitel |

## Gegenprobe nach dem Umbau

| | vorher | nachher |
|---|---|---|
| VL 2 | 20 Folien | 22 Folien (XOR aufgelöst, fünf Antworten) |
| zu volle Rahmen | 0 | 0 (nach der Breitenkorrektur, siehe B1) |
| Notizenfassung | kein `\vbox` | kein `\vbox` |
| VL 1 (neu gebaut, τ-Abbildung) | 25 Folien | 25 Folien |
| `folienpruefliste.py` | 0 / 0 | 0 / 0 |
| `myst build --html` (Abbildung im Kapitel) | ohne Warnungen | ohne Warnungen |

## Was daraus ins Playbook ging

Eine Notationsregel im Buch gilt auch für den Abbildungsgenerator: `make_figures.py` trug die
alte Notation, und das Bild wanderte in Kapitel und zwei Decks. Steht jetzt in
`~/Sciebo/hhu/PLAYBOOK-folien.md` §2.11. Dazu der Befund, dass §2.8 (Frage auf der Folie,
Antwort in einem Medium) in einem Deck dreimal zuschlug – die Prüfliste bleibt, wie sie ist.
