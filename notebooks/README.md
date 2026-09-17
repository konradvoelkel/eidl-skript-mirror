# Notebooks aus der Vorlesung

Übernommen aus dem WiSe 2025/26. Die Notebooks werden beim Build des Skripts **nicht ausgeführt**;
die eingecheckten Outputs sind die aus der Vorlesung. Zum lokalen Ausführen:

```bash
uv sync            # installiert torch, transformers, llama-cpp-python usw. (groß!)
uv run jupyter lab notebooks/
```

| Notebook | Kapitel | Daten |
|---|---|---|
| `nn-by-hand.ipynb` | Aktivierungsfunktionen und Universalität | – |
| `VL_10_convolutions.ipynb` | Faltung und CNNs | `ASML.csv` (Yahoo Finance, Schlusskurse), `pallino.jpg` (beide hier im Ordner) |
| `VL_11_backprop.ipynb` | Backpropagation | – |
| `VL_11_llamacpp.ipynb` | LLMs benutzen | `qwen2.5-0.5b-instruct-q4_k_m.gguf` (491 MB, **nicht im Repo**; von https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF laden oder `ollama pull qwen2.5:0.5b`) |
| `latent-classifier.ipynb` | LLMs benutzen / Blatt 11 | lädt BERT über `transformers` |

Die Kopie von `latent-classifier.ipynb` in `from_2025/exercises/` ist quelltextidentisch (geprüft 2026-09-17).
