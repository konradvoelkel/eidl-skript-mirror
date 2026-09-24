# Code-Beispiele und externe Links, geprüft am 2026-09-24

Alle 24 Python-Blöcke aus den sieben Kapiteln mit Code wurden ausgeführt, nicht nur die vier aus
`TODO.md`. Umgebung: `uv sync` in ein Venv auf der zweiten SSD
(`UV_PROJECT_ENVIRONMENT=/media/konrad/xtraspace/eidl-venv`), Python 3.13, torch 2.14.0+cu130,
transformers 5.17, **CPU** (siehe „Umgebung“ unten). Die extrahierten Blöcke liegen in
`/tmp/.../codecheck/` und sind nicht eingecheckt.

## Was lief, was nicht

| Kapitel | Blöcke | Ergebnis |
|---|---|---|
| 04 Vortrainierte Modelle | 3 | Übersetzung läuft und liefert **exakt** den abgedruckten Satz. Brauchte `sacremoses` (fehlte in `pyproject.toml`). Blöcke 2/3 sind CUDA-Varianten – Block 2 (`.to("cuda")`) scheitert hier am Treiber, Block 3 (device-agnostisch) ist genau die Antwort darauf. |
| 06 Logistische Regression | 4 | Läuft, sobald es Daten gibt. `x`, `y`, `np` waren im Kapitel **nirgends definiert** → Beispieldaten ergänzt. Training: MSE 390 → 0.75 in 100 Epochen. |
| 10 Autograd | 6 | `import torch` fehlte im ersten Block → ergänzt. Danach stimmen **alle** abgedruckten Ausgaben: `<PowBackward0>`, `<AddBackward0>`, `((<MulBackward0>, 0), (<AccumulateGrad>, 0))`, `tensor(42.) tensor(14.)`, `None`, `tensor([6.])`. |
| 14 Autoencoder | 2 | Läuft (MNIST-Download, 15 Epochen CPU ≈ 3 min), aber **lernt fast nichts**: MSE 0.2308 → 0.2284. Imports, `device` und `IMAGESIZE` fehlten und standen zudem nach der Klasse, die sie benutzt → ergänzt und nach vorn gezogen. Offene Entscheidung, siehe unten. |
| 18 RNN | 1 | Läuft (definiert nur das Modell). `h_n, c_n` werden bewusst nicht benutzt, der Text erklärt das. |
| 20 Faltung und CNNs | 5 | Läuft. `data` (Schlusskurse) war undefiniert → Zeile mit `ASML.csv` ergänzt. Die Shape-Rechnung des CNN stimmt: 28×28 → `(1, 10)`, `16*4*4 = 256`. `pallino.jpg` liegt als `notebooks/pallino.jpg` im Repo (beim Prüflauf mit einem Ersatzbild getestet); der Codekommentar nennt jetzt den Pfad. |
| 21 LLMs benutzen | 3 | Alle drei laufen. Embedding: `(896,)`, Norm 296.8 („~300“ ✓). Strukturierte Ausgabe: `name='Sabine' age=29 occupation='doctor' location='Munich'` – exakt wie abgedruckt. llama.cpp: läuft mit `qwen2.5-0.5b-instruct-q4_k_m.gguf`, Vokabulargröße `(151936,)` ✓, die Top-5 weichen leicht ab → Kommentar aktualisiert. Brauchte `ollama` und `pydantic` (fehlten in `pyproject.toml`). |

## Gemessene Werte, die im Text standen

* Kapitel 21, nächste Tokens nach „The color of the sky is“:
  alt `' changing' 12.1%, ' always' 6.5%, ' blue' 3.9%, ' determined' 3.0%, ' very' 3.0%`, `' red' 0.74%` –
  jetzt gemessen `' changing' 10.3%, ' always' 6.7%, ' blue' 4.0%, ' a' 3.2%, ' determined' 3.0%`, `' red' 0.72%`
  (Qwen2.5-0.5B-Instruct Q4_K_M, llama-cpp-python 0.3.35). Die Aussage des Beispiels bleibt dieselbe,
  die Zahlen im Kommentar sind nachgezogen.
* Kapitel 14, Autoencoder nach 15 Epochen: SGD `lr=1e-2` → **0.2284**, SGD `lr=1e-1` → 0.0719,
  Adam `lr=1e-3` → 0.0188.

## Offene Entscheidung

Das Autoencoder-Training im Kapitel ist mit `optim.SGD(lr=1e-2)` und 15 Epochen so eingestellt, dass
praktisch nichts passiert – wer es nachbaut, sieht Matsch. Direkt danach kommt die Tricks-Liste
(„mehr Epochen“, „Lernrate anpassen“, „Adam statt SGD“), die genau das aufräumt. Entweder das im Text
explizit sagen, oder gleich Adam zeigen und SGD als Kontrast. Steht als Entscheidung in `TODO.md`.

## Umgebung

`uv sync` zieht den **cu130**-Build von torch; der Treiber auf diesem Rechner ist 12.9, deshalb ist
`torch.cuda.is_available()` False und alles lief auf der CPU. Für Demos im Hörsaal vorher Treiber
aktualisieren oder einen passenden torch-Build pinnen. Der Venv liegt bewusst auf
`/media/konrad/xtraspace` (torch + CUDA-Pakete brauchen ~10 GB), die Testdaten (MNIST, GGUF) unter
`/media/konrad/xtraspace/eidl-codecheck-data`.

## Externe Links

Alle 67 `http(s)`-Links aus den Kapiteln durchgeprüft (curl, Redirects verfolgt):

* **65 × 200**, darunter die vier Werkzeuge aus dem Semesterplan: TensorFlow Playground, Loss Landscape
  Explorer, GAN Lab, Ollama.
* **1 × tot:** `muhark.github.io/.../word2vec-from-scratch` (404) – ersetzt durch das offizielle
  PyTorch-Tutorial „Word Embeddings: Encoding Lexical Semantics“ (der Kaggle- und der d2l.ai-Link
  daneben leben weiter).
* **1 × 403 nur für curl:** der HPCwire-Artikel in Kapitel 01; im Browser ist die Seite normal da
  (Bot-Schutz). Kein Handlungsbedarf.
