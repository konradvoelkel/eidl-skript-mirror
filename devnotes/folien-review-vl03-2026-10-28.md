# Durchsicht des VL-3-Decks (2026-10-28)

Geprüft wurde `slides/Einführung in Deep Learning 2026 VL 03 Vortrainierte Modelle und
Tensoren.tex` nach der Prüfliste in `~/Sciebo/hhu/PLAYBOOK-folien.md` §3: Bau von Null,
Notizenfassung, Ablaufplan gegen die Frame-Reihenfolge, Ansagen gegen `kurs-2026-27.md` und
die ILIAS-Run-Datei, Fakten gegen die Kapitel „Vortrainierte Modelle verwenden“ und
„Tensoren“, Dialogmuster gegen `transcripts/vl03-pytorch-tensoren-2025/notiz.md`. Am
Vorlesungstag selbst, drei Stunden vor der Sitzung; alle Befunde sind sofort umgesetzt.

**Ausgangslage:** 18 Folien, 0 zu volle Rahmen, Notizenfassung vollständig, Termine richtig
(`\date{28.10.2026}`, „Nächste Woche: logistische Regression“ = Woche 4 laut Run-Datei, die
Übungsblatt-Folie beschreibt Blatt 3). Nachgeprüft und richtig: die Querverweise VL 9
(word2vec), VL 10 (Transformer, BPE) und VL 15 (Destillation) gegen `kurs-2026-27.md`;
$784 = 28 \cdot 28$; $\dim(V \otimes W) = n \cdot m$; die Konvention „erste Achse ist der
Batch“; `torch.from_numpy` teilt den Speicher.

## A. Fachlich

| | Befund | Umsetzung |
|---|---|---|
| **A1** | **Der Ablaufplan rechnet mit 19 Seiten, das Deck hatte 18** – ab „Folien 5–7 Task-Rundgang“ war jede Zeile um eins verschoben (Playbook §2.6). Die fehlende Folie ist belegt: Folie 4 nennt sechs Task-Familien, die Notiz klammert Audio, Tabular und RL aus – **Multimodal** blieb angekündigt und ungezeigt (§2.8) | Neue Folie 7 „Multimodal“ mit den vier Tasks aus der Kapiteltabelle (Image-to-Text, Visual QA, Document QA, Feature Extraction). Danach stimmt der Ablaufplan Zeile für Zeile, ohne ihn anzufassen |
| **A2** | **Hugging Face gehört bald Nvidia, das Deck wusste nichts davon.** Das Kapitel führt den Kauf vom September 2026 (12,93 Mrd. \$, Abschluss erste Hälfte 2027 erwartet), die Folie nannte nur die Bewertung von 2023 (Playbook §2.11: was im Kapitel korrigiert wurde, gehört auch ins Deck) | Vierter Bullet auf Folie 3 (Konrads Ansage), Notiz mit Datum, Summe, Vorbehalt und der Einordnung |
| **A3** | **Die Reshape-Auflösung in der Notiz war halbiert.** Sie nannte $\mathbb{R}^4 \otimes \mathbb{R}^{10} \cong \mathbb{R}^{40}$ und im nächsten Satz „das Beispiel mit achtzig Zahlen“ – der dritte Faktor $\mathbb{R}^2$ aus dem Kapitel fehlte, und damit die Herkunft der 2 in `reshape(-1, 2)` | Notiz nennt jetzt $a \in \mathbb{R}^4 \otimes \mathbb{R}^{10} \otimes \mathbb{R}^2$ (achtzig Zahlen) und `a.reshape(-1, 2) == a.reshape(40, 2)`, wie im Kapitel |
| **A4** | **„fast alle Layer“ ohne das „fast“.** Die Notiz zum Batch-Bild übernahm die Einschränkung aus dem Kapitel, nicht aber die Ausnahme | RNN-Fall in die Notiz: `nn.RNN`/`LSTM`/`GRU`/`Transformer` erwarten `(seq, batch, feature)`, `batch_first=True` stellt die Regel her; dazu $(N, C, H, W)$ als Antwort auf die naheliegende Rückfrage |
| **A5** | Folie 9 hieß „Das Muster hinter **allen** Hub-Modellen“ und zeigte „Text → Zahlen → Zahlen → Text“ – falsch für Bild- und Audiomodelle (Konrads Befund) | Titel „Das Muster hinter jedem Hub-Modell“, Zeile jetzt „Daten → Zahlen → Zahlen → Daten“, dazu eine kleine Zeile und ein Notizabsatz: bei Bild und Audio heißt der erste Schritt Prozessor (`AutoProcessor`, `FeatureExtractor`) |
| **A6** | **Der Code auf Folie 8 lief nicht** (Konrads Ansage: „sind wir uns sicher, dass Folie 8 die Wahrheit erzählt?“). Nachgefahren mit genau dem Befehl der Folie: `FSMTTokenizer` bricht mit `ImportError: You need to install sacremoses` ab -- `transformers[torch]` zieht das Paket nicht mit. Die Installationsfolie und **das Kapitel** hatten denselben Mangel | `sacremoses` auf Folie 8, wo das Beispiel steht; auf der Installationsfolie 11 ausdrücklich **nicht** (Konrad: „da will ich das nicht sehen") -- die Folie zeigt den allgemeinen Weg, nicht die Eigenheit eines Modells. Notiz auf Folie 8 erklärt es. Im Kapitel `04-vortrainierte-modelle.md` ein Satz vor dem Beispiel |
| **A7** | **Folie 17 benutzte 32 für zwei verschiedene Dinge** und erklärte dadurch nichts (Konrads Rückfrage: „wenn ich batchsize 16 habe bei 32 Bildern, wie ist dann der Shape?“). „32 Datenpunkte“ liest sich als Größe des Datensatzes, gemeint war die Batchgröße | Folie zeigt jetzt `(784,)` → `(16, 784)` → `(16, 28, 28)` → `(16, 3, 28, 28)`, dazu die Zeile „32 Bilder bei `batch_size=16`: zwei Tensoren `(16, 28, 28)`“. Notiz: letzter Batch darf kleiner sein, `drop_last`. Derselbe Satz im Kapitel `05-tensoren.md` |
| **A8** | Der Zusatz „Achtung: anders als bei NumPy“ (Konrads Ansage, von ihm selbst zurückgezogen: „mein Vorschlag war auch doof“) stimmte so nicht: Zeilen als Datenpunkte sind in NumPy und scikit-learn genauso | Zusatz raus; statt dessen steht der **wahre** Unterschied sichtbar auf der Folie, die Kanalachse: PIL, matplotlib `(H, W, C)` gegen PyTorch `(N, C, H, W)` |
| **A9** | **Die vierte der vier Fragen blieb ohne Folie** (Konrads Befund: „was speichert ein PyTorch-Tensor zusätzlich zum NumPy-Array? das muss doch hier gesagt werden“). Das Kapitel nennt `dtype`, GPU-Speicher und `grad`; auf den Folien stand davon nur, dass `from_numpy` den Speicher teilt | Neue Folie 14 „Was ein Torch-Tensor mehr hat“: Tabelle NumPy gegen PyTorch über `dtype`/`shape`, `device`, `requires_grad`, `grad`, `grad_fn`. Notiz mit dem nachgefahrenen Zweizeiler (`w.grad` ist `None`, `y.grad_fn` ein `SumBackward0`, nach `backward()` steht `tensor([3.])` drin) und den Zeigern auf VL 5, 6 und 12. **Ablaufplan mitgezogen**: 50--58 Folien 12--14, danach 15--17, 18--19, 20 |

## B. Form und Kleinkram

| | Befund | Umsetzung |
|---|---|---|
| **B1** | Folie 2: „und die Datenstruktur dahinter“ (Konrads Ansage) | Satz endet nach „trainiert haben“ |
| **B2** | Folie 8 zeigte Code, aber nicht, was er ausgibt; der übersetzte Satz stand nur in der Dozentennotiz (Konrads Ansage) | Ausgabezeile unter das Listing, in `\footnotesize`, damit der Rahmen nicht überläuft |
| **B3** | Folie 8: Das Listing hatte eine elfte, leere Zeile – das eingerückte `\end{lstlisting}` (Konrads Ansage) | `\end{lstlisting}` auf Spalte 0. **Dieselbe Einrückung steht in den Listings auf Folie 10 und 11 und in anderen Decks** – dort noch nicht angefasst, siehe unten |
| **B4** | Folie 8: kein Weg zum Ausprobieren ohne Installation (Konrads Ansage) | Zweites Listing `uv run --with 'transformers[torch]' uebersetzen.py`, Notiz erklärt die Wegwerf-Umgebung und verweist auf Folie 11 |
| **B5** | Fünf Wörter sind der Rechtschreibprüfung unbekannt: `ViLT`, `LayoutLM` (Folie 7), `venv`, `FSMT` (Notizen), `uv` (Zwischenüberschriften Folie 11) | Alle fünf mit Begründung in `sprachpruefliste-woerter-folien.txt` |
| **B6** | Folie 3: Die beiden Adressen waren toter Text, Konrad will im Hörsaal hineinklicken; zur Dollarsumme fehlte die Einordnung in Euro | `\href` auf beide URLs, in der Markenfarbe; geprüft sind zwei `/URI`-Annotationen im PDF. „(ca. 11,6 Mrd. €)“ hinter die Dollarsumme, gerechnet mit dem EZB-Referenzkurs vom 2026-10-27 (1 € = 1,1150 \$) |
| **B7** | Folie 9: „Tokenizer Modell Tokenizer“ stand als eigene Zeile unter dem Pfeildiagramm, die Zuordnung zu den Pfeilen war nicht zu sehen (Konrads Ansage) | Beides in eine `tabular` mit sieben Spalten: Wörter und Pfeile oben, die Beschriftungen darunter genau unter ihrem Pfeil. Dafür `\LARGE` statt `\Huge` und `tabcolsep` auf 4pt, sonst lief „Daten“ rechts aus dem Rahmen |
| **B8** | Letzte Folie: „Die Integrale dürfen Sie ignorieren“ klang endgültiger als gemeint (Konrads Ansage) | „... beim ersten Lesen ignorieren“ |

## Gegenprobe nach dem Umbau

| | vorher | nachher |
| Seiten | 18 | 20 (Multimodal, Torch-Tensor) |
| zu volle Rahmen | 0 | 0 (nach `\footnotesize` auf Folie 8, siehe B2) |
| Notizenfassung | kein `\vbox` | kein `\vbox` |
| Ablaufplan gegen `frametitle` | ab Zeile „5–7“ um eins verschoben | stimmt Zeile für Zeile |
| `folienpruefliste.py --deck 03` | 0 Typografie / 0 unbekannte Wörter | 0 / 0 (fünf Wörter neu in der Folienwortliste) |
| Log: `Font shape`, Silbentrennung | 0 | 0 |

## Der Lauf, der Folie 8 belegt

Am 2026-10-28 in `/media/konrad/xtraspace/tmp/vl03-wmt19-test/` ausgeführt, mit genau dem
Skript und dem Befehl der Folie (`HF_HOME` auf die zweite Platte, 1,1 GB Modell):

```
uv run --with 'transformers[torch]' --with sacremoses uebersetzen.py
Ich bin mir nicht sicher, ob Deep Learning wirklich etwas für mich ist.
```

Der Satz auf der Folie stimmt also wörtlich, Zeichen für Zeichen -- und die Zeile darunter
stimmt erst seit diesem Lauf, siehe A6. Der erste Versuch, ohne `sacremoses`, endete nach
dem Download von torch und Modell im `ImportError`. **Die Lehre, die ins Playbook gehört:
Ein Codebeispiel auf einer Folie ist nicht geprüft, solange es nicht einmal mit der
Installationszeile derselben Folie gelaufen ist.** Beides stand hier seit 2025 nebeneinander
und war beides für sich plausibel.

## Woher der `sacremoses`-Fehler kommt (Konrads Rückfrage)

Der naheliegende Verdacht war, dass das 2023 längst behoben sei --
`huggingface/api-inference-community` [#240](https://github.com/huggingface/api-inference-community/pull/240),
gemerged am 2023-04-24, Betreff „this fix issue loading a FSMTTokenizer". Der PR ändert aber
**genau eine Datei**, `docker_images/sentence_transformers/requirements.txt`, und darin eine
Zeile: `sacremoses==0.0.53`. Das ist das Docker-Image der **gehosteten Inference-API**, also
das Widget auf der Modellseite. Auf eine lokale Installation wirkt es nicht.

Der Fehler kommt aus `transformers` selbst und ist kein Versehen, sondern Absicht:
`models/fsmt/tokenization_fsmt.py` importiert `sacremoses` erst im Konstruktor und wirft
sonst den `ImportError` (Zeilen 174--180 in 5.21.0). In den Metadaten steht `sacremoses` nur
unter den Extras `testing`, `deepspeed-testing` und `dev` -- es gibt **kein** Nutzer-Extra,
das es mitbringt, also muss man es nennen.

**Und 2025 lief es doch?** Es lief nie ohne das Paket -- es ist nur nie aufgefallen. Die
Metadaten aller Fassungen von 4.30 (2023) bis 5.21 nennen `sacremoses` ausschließlich in den
Extras `testing`, `deepspeed-testing` und `dev`; `pip install 'transformers[torch]'` hat es
also auch letztes Jahr nicht mitgebracht. Und `tokenization_fsmt.py` trägt den try/except
Wort für Wort schon in v4.30.2, v4.46.3 und v4.56.2. Das 2025er Deck
(`~/Sciebo/hhu/eidl-25/slides/… VL 03_ PyTorch Basics, Tensoren.pdf`, Folien 21 und 23) zeigt
denselben Code und dieselbe unvollständige Installationszeile.

Der Grund, warum es bei uns trotzdem funktionierte, steht in diesem Repo: `pyproject.toml`
führt seit dem 2026-09-24 (`95b1c9b`, „Code-Beispiele ausgeführt und repariert") die Zeile
`"sacremoses",  # Tokenizer von facebook/wmt19-en-de (Kapitel „Vortrainierte Modelle")`.
Der Fehler ist damals beim Ausführen der Kapitelbeispiele schon einmal gefunden und für die
**Projektumgebung** behoben worden -- in den Kapiteltext und auf die Folie hat er es nicht
geschafft. Wer `uv run` im Repo aufruft, merkt nichts; wer der Folie folgt, läuft hinein.

Gemessen am 2026-10-28: transformers 5.21.0, huggingface\_hub 2.3.0, torch 2.14.1+cu130.
Nebenbei, zur Frage, warum die Abhängigkeit nicht deklariert ist: `transformers` hat die
Maschinerie dafür (`is_sacremoses_available`, `SACREMOSES_IMPORT_ERROR`, `requires_backends`
in `utils/import_utils.py`), aber weder FSMT noch XLM benutzen sie -- beide Dateien haben
einen handgeschriebenen `try: import sacremoses`, und beide werfen denselben Text, der
`XLMTokenizer` nennt. In `tokenization_fsmt.py` steht damit der falsche Klassenname in der
Fehlermeldung; deshalb führt die Suche danach auch in XLM- und Inference-API-Fäden statt zu
FSMT. Die Abhängigkeit existiert also nur als Zeichenkette in einem Konstruktor, nicht in den
Metadaten.

**Eine Version zu pinnen hilft hier nichts**, am wenigsten bei `huggingface_hub` -- das ist
nicht das Paket, das importiert. Wer pinnen will, pinnt ohnehin schon: Der Weg „Mit uv" auf
Folie 11 schreibt `uv.lock`, und damit sind alle Fassungen fest.

## Belege für die neuen Namen

Die vier Modellnamen auf der Multimodal-Folie sind nicht erfunden, sondern am 2026-10-28
geprüft: `Salesforce/blip-image-captioning-base` und `impira/layoutlm-document-qa` stehen auf
den Task-Seiten `huggingface.co/tasks/image-to-text` bzw. `.../document-question-answering`;
`dandelin/vilt-b32-finetuned-vqa` und `openai/clip-vit-base-patch32` antworten mit 200. Die
Task-Namen selbst stehen in der Tabelle in `part-grundlagen/04-vortrainierte-modelle.md`.

## In ILIAS

Hochgeladen am 2026-10-28 um 11:40 als **neue Datei** in den Ordner „Vorlesungsfolien"
(`fold_2215461`), wie es der Workflow vorsieht -- nicht als neue Version des 2025er Decks.
Neue id `file_2228081`, 20 Seiten, 1.519.488 Bytes; der ausgelieferte Download hat dieselbe
Bytezahl und dieselbe SHA-256
(`53aff6bba1158e362e45273c1d62194a74cc7830fea503989c4acf362a362dec`) wie die lokale Datei.

In der Wochentabelle ist „Folien VL 3" jetzt verlinkt: Zelle Zeile 3, Spalte 4 im
Datentabellen-Editor, Inhalt `[iln file="2228081"]Folien VL 3[/iln]`. Vor dem Setzen geprüft,
dass der eine TinyMCE wirklich in dieser Zelle steht und den alten Inhalt zeigt -- die Falle
aus der README, an der am 2026-09-24 fünf Zellen verrutscht sind. In der Run-Datei ist
`slides-03` nachgetragen und aus `unlinked_object_keys` heraus; `live_check.py` gegen den
Abzug `out/live/2026-10-28-course-nach-upload.txt` meldet nur noch die zwei bekannten
„Lösungshinweise"-Punkte.

## Was offen bleibt

* **Die eingerückten `\end{lstlisting}` (B3) stehen in weiteren Decks.** Hier ist nur Folie 8
  geändert, weil kurz vor der Sitzung. Ein Durchgang über alle Decks gehört in die nächste
  Foliensitzung – und, wenn er sich bestätigt, die Regel ins Playbook.
* **Die zwei Sätze im Kapitel sind geändert, aber nicht veröffentlicht.** `sacremoses` vor dem
  WMT19-Beispiel und der Absatz „für Bild und Audio heißt es Prozessor“ stehen in
  `part-grundlagen/04-vortrainierte-modelle.md`; gebaut, gepusht und auf der Pages-Seite
  nachgesehen ist das noch nicht.
* Von den vier Fragen auf Folie 12 hat jetzt die vierte ihre eigene Folie (A9); die ersten
  drei bleiben mündlich. Das ist in Ordnung -- es sind Definitionsfragen, die vierte war
  die, an der das Kapitel hängt.
* Das Kapitel „Tensoren“ nennt `dtype`, GPU-Speicher und `grad` in einem Satz, aber weder
  `requires_grad` noch `grad_fn`. Die Folie ist dort jetzt genauer als das Buch -- beim
  nächsten Durchgang durch das Kapitel angleichen.
