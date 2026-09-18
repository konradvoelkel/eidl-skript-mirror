# Notebooks aus der Vorlesung 2025/26

Diese Notebooks sind **nicht Teil des Buchs** (TOC-Eintrag in `myst.yml` auskommentiert). Ihr Inhalt
ist am 2026-09-18 in die Kapitel übernommen worden – Code, Ergebnisse und Erklärungen stehen jetzt dort:

| Notebook | jetzt in | Status |
|---|---|---|
| `VL_11_backprop.ipynb` | Kapitel „Autograd und Berechnungsgraph“ | vollständig übernommen |
| `nn-by-hand.ipynb` | Kapitel „Netze von Hand bauen“ (Abbildungen via `devnotes/make_figures.py`) | vollständig übernommen |
| `VL_10_convolutions.ipynb` | Kapitel „Faltung und CNNs“ (Abbildung `images/vl10-pallino-conv.png` aus dem Output) | vollständig übernommen |
| `VL_11_llamacpp.ipynb` | Kapitel „LLMs benutzen“ | vollständig übernommen |
| `latent-classifier.ipynb` | Blatt 11 (Download auf der Blatt-Seite), Beschreibung in „LLMs benutzen“ | **bleibt** – Studierende führen es aus |

Sie bleiben hier als Referenz und zum lokalen Ausführen; die eingecheckten Outputs sind die aus der Vorlesung.

```bash
uv sync            # installiert torch, transformers, llama-cpp-python usw. (groß!)
uv run jupyter lab notebooks/
```

Daten: `ASML.csv` (Yahoo Finance, Schlusskurse) und `pallino.jpg` für die Faltung;
`qwen2.5-0.5b-instruct-q4_k_m.gguf` (491 MB, **nicht im Repo**) für llama.cpp von
https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF laden oder `ollama pull qwen2.5:0.5b`.
