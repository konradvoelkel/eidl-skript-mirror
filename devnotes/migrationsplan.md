# Migrationsplan EiDL 2025/26 → 2026/27

Stand: 2026-09-20 (Historie; offene Punkte stehen nur in `TODO.md`)

## Ausgangslage

- Die Folien aus 2025/26 liegen nur als Google-Slides-Exporte (PDF) vor, siehe `../from_2025/slides/`.
- Übungsblätter (LaTeX, `../from_2025/exercises/`) und Klausuren (LaTeX, `../from_2025/exam/`) sind vollständig als Quelltext vorhanden.
- Das neue Modul-Vorstellungsdeck (`../slides/`) ist bereits im üblichen LaTeX-Beamer-Stil (hhubeamer, Source Sans Pro).

## Migrationspfad

1. **Skript aufsetzen** (dieses Projekt, MyST wie `eipy-skript`) und die Inhalte der 15 Vorlesungen in Reihenfolge festhalten.
   Erledigt als automatische Transkription der Folien (Folie für Folie, `<!-- Folie N -->`-Marker), erzeugt durch
   ein Skript aus den PDFs. Formeln (Unicode-Mathe aus Google Slides) und Abbildungen müssen von Hand nachgezogen werden.
2. **Inhalt überarbeiten**: Text in eigene Worte bringen, Formeln in LaTeX setzen, Abbildungen ersetzen/neu erzeugen (matplotlib),
   Redundanzen aus inkrementellen Folien (Overlays) zusammenfassen. Dabei sicherstellen, dass alles enthalten ist, was
   Übungsblätter und Klausur-Aufgabenschatz voraussetzen (siehe Tabelle unten).
   *Stand 2026-09-17: Alle 15 Kapitel liegen als erste Prosafassung mit LaTeX-Formeln vor (Formeln, die in den
   Google-Slides Bilder waren, wurden aus den gerenderten Folien rekonstruiert). Noch offen: Abbildungen – die Stellen
   sind als `<!-- TODO Abbildung -->` markiert, fachliche Durchsicht der Ergänzungen,
   die über die Folien hinausgehen (z.B. Perzeptron-Konvergenzsatz in VL 02, Attention-Formel in VL 09,
   Momentum/Adam-Formeln in VL 15).*
3. **Übungsblätter** anpassen (`part-exercises/`, bereits per pandoc konvertiert; Abgabetermine noch aus 2025).
4. **Danach** neue Beamer-Decks aus dem Skript ableiten (Entscheidung 2026-09-20: aus dem Skript, nicht aus den Slides 2025), Themenfolge laut `kurs-2026-27.md`, Header aus `../slides/Einführung in Deep Learning 2026 header.tex`.

## Zuordnung Vorlesung ↔ Kapitel ↔ Übungsblatt ↔ Klausur

Seit dem Umbau am 2026-09-17 sind die Kapitel inhaltlich geschnitten (Dateinamen ohne VL-Nummer); am 2026-09-18
wurden überfrachtete Kapitel nochmals geteilt (26 Kapitel), am 2026-09-20 kam „Loss-Funktionen und Maximum Likelihood“
als Split von „Gradientenabstieg“ hinzu, jetzt **27 Kapitel (01–27)**. Die Zuordnung Vorlesungswoche → Kapitel steht
als Tabelle in `kurs-2026-27.md` (nicht im Buch; seit 2026-09-20 aus dem Ist der Aufzeichnungen 2025 abgeleitet), der
Abgleich mit dem Klausur-Aufgabenschatz in `klausur-abdeckung.md`. Die Aufzeichnungen 2025/26 selbst sind ausgewertet
in `../transcripts/` und `diskussion-vorlesung-vs-skript.md`. Übungsblätter (2025): 00/01 → Perzeptron (Lin. Algebra),
02 → Perzeptron, 03 → Gradientenabstieg (schwache Ableitungen), 04/05 → Logistische Regression,
06/08 → Autoencoder, 07 → Backpropagation, 09 → VAE, 10 → CNNs, 11 → LLMs benutzen.

Klausurformat 2025/26: 6 Aufgaben, 55 Punkte, 90 Minuten, keine Hilfsmittel; Aufgabentypen laut
`../from_2025/exam/exam2025-eidl-aufgabenschatz.tex`: (1) Multiple Choice W/F, (2) Anwendungskonzept,
(3) Code-Verständnis, (4) Backpropagation & Update, (5) gruppierte Multiple Choice, jeweils in Sets A–D.
Entwürfe für 2026 (englisch, amsart): `exam2026-eidl-exam-1.tex`, `exam2026-eidl-exam-2.tex`.

## Offene Punkte / Ideen

→ Alle in `TODO.md`. Die folgenden Notizen sind die ursprünglichen vom 2026-09-17/18 und nur noch Historie.

- ~~Im Vorstellungsdeck 2026 ist die geplante Reihenfolge leicht anders als 2025: Logistische Regression und SGD/Backprop
  *vor* PyTorch. Entscheiden, ob Kapitel 03 (PyTorch) nach hinten wandert.~~ Reihenfolge bleibt wie 2025 (Plan in `kurs-2026-27.md`, 2026-09-20).
- ~~VL 08 war 2025 mit 85 Folien überladen (AE-Varianten + VAE + word2vec + NLP); ggf. word2vec/NLP in Kapitel 09 verschieben.~~ Im Skript sind das jetzt eigene Kapitel (Autoencoder, VAE, word2vec); die Folienverteilung ist Thema von Schritt 4.
- ~~VL 06 endet bereits mit Autoencoder-Einführung, VL 07 beginnt mit „handgemachten Netzen" (Universalität) – Kapitelgrenzen neu ziehen.~~ Erledigt (Kapitelsplits 2026-09-18).
- Lehrbuchbezug: Prince, *Understanding Deep Learning* (Kapitel pro Thema referenzieren), Deisenroth et al. für Mathe-Grundlagen.
- ~~Notebooks (`notebooks/`) laufen noch nicht im Build.~~ Inhalte am 2026-09-18 in die Kapitel übernommen, Notebooks aus dem Buch genommen (siehe `notebooks/README.md`).
- Englische Übungsblätter (`sheetNN.tex`) sind nicht konvertiert; bei Bedarf gleicher Weg über pandoc.

## Google-Slides-Quellen (Drive-Ordner `1blU81WO_aaZRyH02UFrwk4AamOyWT-sv`)

Die Drive-Textexporte sind schlechter als `pdftotext` (Mathe-Symbole als Mojibake, Formeln sind Bilder und fehlen ganz,
keine Notizen) – die Transkription in den Kapiteln basiert daher auf den PDFs. Links zum Nachschlagen:

| VL 2025/26 | Google Slides |
|---|---|
| 1 Überblick, Perzeptron | https://docs.google.com/presentation/d/1EMOQ_P6TWf3eksBuEAv5l7z-1ul8VWU1Q4CpORdW3eg |
| 2 Perzeptron, Vortrainierte Modelle | https://docs.google.com/presentation/d/1V0-Acn_TwPNy_6bThHWX_lkIkZ750XqIiT_gbCChShA |
| 3 PyTorch Basics, Tensoren | https://docs.google.com/presentation/d/16u4n4JTcAE98KwneaoQ2z2M1C93laxtwZDrXCdxMYzg |
| 4 Logistische Regression | https://docs.google.com/presentation/d/1nrnlpvMElMnvgAeg2O3JIdFrvPQ8LADlXmmXKrXPom0 |
| 5 SGD | https://docs.google.com/presentation/d/1psfkmt_W95qPiGZcu5-5zBp6WRZBTSQzsPWI1zGrlLo |
| 6 Backprop | https://docs.google.com/presentation/d/1HBOY-MczMD2-a4jeBXXWtjTCxxk-Vla7H_TnoheaV1c |
| 7 Autoencoder | https://docs.google.com/presentation/d/1QbSPcKxY9bJiMIhtvYRSm2OuI2nvUydTj1VLvJfeW6o |
| 8 Latent Space und VAE | https://docs.google.com/presentation/d/1M9DZqUgNPWyu3RbnhMedtnebT2eATjLNoKxJsBrPZyY |
| 9 Representation Learning | https://docs.google.com/presentation/d/14pO2CKBvnK8m_7yz7dvDZ0z0QHQH0UUVn9cYYZ8lKmM |
| 10 Convolution (CNN) | https://docs.google.com/presentation/d/1CcntCr6ylo_dlewNQc3-UBpk3--pNpP2aKCoupQBl2g |
| 11 LLMs benutzen | https://docs.google.com/presentation/d/1uMJKcqCZoxKZhYLMY6lGtu0tX820mIdOpGetN5zdMPU |
| 12 GANs | https://docs.google.com/presentation/d/1IQ5WJb15ZLUZgmHJsKY7bd0Odpf_uePO3oUKwwyKxUM |
| 13 Latent Spaces und Anwendungen | https://docs.google.com/presentation/d/1zrs-bgHQGRvMHfNi_DWm642VVjwHLNbIwHeZ6ibLzw0 |
| 14 Destillation | https://docs.google.com/presentation/d/1gJFnzR3GaPkEWp98jj6idrNHZ4prxU6mdtlarvdTjWw |
| 15 Märchenstunde | https://docs.google.com/presentation/d/1tu3Mp6eaooEZ1nBJJhXSbQ8s4ZhJrDk9mcFj0BcEa2k |

Ältere Iterationen im selben Ordner: 2024/25 VL 1–12 (u.a. „VL 12: Transformer", 2025 in VL 9/11 aufgegangen)
und 2023/24 VL 1–13 (u.a. „VL 13: Finale"); einige davon wurden noch im Dez. 2025 bearbeitet.
