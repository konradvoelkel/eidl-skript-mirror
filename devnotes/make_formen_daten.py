#!/usr/bin/env python3
"""Erzeugt `formen-stichprobengroesse.json` für die Abbildung `vl11-stichprobengroesse`.

Aufruf aus dem Projektverzeichnis (braucht torch, also die **Default-Gruppe**):

    uv run devnotes/make_formen_daten.py

**Warum ein eigenes Skript und eine Datei dazwischen?** `make_figures.py` läuft mit
`--only-group figures`, und in dieser Gruppe steckt bewusst kein torch (siehe
`../CLAUDE.md`). Ein Netz lässt sich dort nicht trainieren. Die Rechnung läuft deshalb
hier, einmal, und legt ihr Ergebnis als **versionierte** JSON ab; gezeichnet wird daraus
mit der angehefteten matplotlib-Fassung wie jede andere Abbildung auch. Nebenbei kostet
das Zeichnen dann keine zwei Minuten mehr, sondern Millisekunden.

Gegenprobe: zweimal laufen lassen, die JSON muss byte-gleich sein.

Was gerechnet wird: Ein MLP klassifiziert 32x32-Graustufenbilder in „Dreieck“ und
„Quadrat“. Die Bilder kommen nicht aus einem Ordner, sondern aus einer **Verteilung**,
die in `formen.py` vollständig angegeben ist (dort ohne torch, weil `make_figures.py`
dieselbe Verteilung für die Beispielbilder braucht) — wir können also beliebig oft daraus
ziehen. Alle Läufe bekommen dasselbe Budget (gleich viele Gradientenschritte, gleich viele gesehene
Beispiele, dieselbe Initialisierung, derselbe Optimierer); der einzige Unterschied ist,
aus wie vielen *verschiedenen* Bildern diese Beispiele stammen.

Die Flächen der Formen sind vorgegeben und für beide Klassen gleich verteilt. Ohne das
wäre „Tinte zählen“ schon die halbe Antwort: Ein Dreieck und ein Quadrat gleicher Fläche
unterscheiden sich im Umfang um 14 % (4,56·sqrt(A) gegen 4·sqrt(A)). Wie gut die
Abkürzungen nach dieser Vorkehrung noch tragen, misst das Skript mit und legt es in die
JSON — die Zahlen stehen im Kapitel.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np
import torch
from formen import ShapeConfig, sample_batch, shape_stream
from sklearn.linear_model import LogisticRegression
from torch import nn
from torch.utils.data import (
    DataLoader,
    Dataset,
    IterableDataset,
    RandomSampler,
    get_worker_info,
)

WURZEL = Path(__file__).resolve().parent.parent
ZIEL = Path(__file__).resolve().parent / "formen-stichprobengroesse.json"

SCHRITTE, BATCH, LR = 3000, 128, 1e-3
GROESSEN = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]
KURVEN = [64, 256, 1024, 4096]          # davon zeigt die linke Hälfte der Abbildung den Verlauf
WORKERS = 4
# Fünf Wiederholungen je Punkt, berichtet wird der Median. Mit einem einzigen Seed ist
# die Kurve nicht monoton (N=16384 fiel unter N=8192), und eine Abbildung, die eine
# Aussage über Stichprobengrößen macht, darf nicht an der Ziehung hängen. Dieselbe
# Vorkehrung wie bei der Double-Descent-Abbildung, dort mit 200 Datensätzen.
REPS = 5
SEED = 0

# Für den Abschnitt in Kapitel 10: Die Demo dort zeigt `Adam`, und das Kapitel behauptet,
# dass `SGD` dasselbe Netz nicht in 3000 Schritten dorthin bringt. Also nachmessen —
# derselbe Strom, dasselbe Budget, dieselben Initialisierungen, nur der Optimierer
# wechselt. Drei Wiederholungen reichen, weil hier keine Kurve gezeichnet wird, sondern
# ein Satz im Text davon abhängt.
# `None` ist der Weg durch die Voreinstellung von `trainiere` — die Adam-Zeile misst damit
# genau den Code, den alle anderen Läufe oben benutzen.
OPTIMIERER = [("adam_1e-3", None),
              ("sgd_1e-2", lambda p: torch.optim.SGD(p, lr=1e-2)),
              ("sgd_1e-1", lambda p: torch.optim.SGD(p, lr=1e-1))]
REPS_OPT = 3


# ---------------------------------------------------------------- Daten für PyTorch

class FormenIterable(IterableDataset):
    """Der unendliche Strom. Jeder Worker bekommt seinen eigenen Seed.

    Ohne die Abfrage von `get_worker_info()` zieht jeder Worker-Prozess dieselbe Folge,
    und mit `num_workers=4` sieht das Netz jeden Batch viermal — der Loss sinkt trotzdem,
    nur die effektive Datenmenge ist ein Viertel.
    """

    def __init__(self, cfg: ShapeConfig, seed: int = 0):
        self.cfg, self.seed = cfg, seed

    def __iter__(self):
        info = get_worker_info()
        wid = 0 if info is None else info.id
        for x, y in shape_stream(self.cfg, self.seed + 9973 * wid):
            yield torch.from_numpy(np.ascontiguousarray(x)), int(y)


class FormenFest(Dataset):
    """Einmal gezogen, dann fest — der Datensatz für „viele Epochen auf wenig Daten“."""

    def __init__(self, cfg: ShapeConfig, n: int, seed: int):
        x, y = sample_batch(cfg, np.random.default_rng(seed), n)
        self.x, self.y = torch.from_numpy(x), torch.from_numpy(y)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, i):
        return self.x[i], int(self.y[i])


# ---------------------------------------------------------------- Netz und Training

def mlp(breite=(256, 128), size=32):
    schichten, davor = [nn.Flatten()], size * size
    for b in breite:
        schichten += [nn.Linear(davor, b), nn.ReLU()]
        davor = b
    return nn.Sequential(*schichten, nn.Linear(davor, 2))


@torch.no_grad()
def genauigkeit(modell, x, y, batch=4096):
    modell.eval()
    richtig = sum((modell(x[i:i + batch]).argmax(1) == y[i:i + batch]).sum().item()
                  for i in range(0, len(y), batch))
    modell.train()
    return richtig / len(y)


def trainiere(quelle, init_state, x_test, y_test, x_train=None, y_train=None,
              opt_fabrik=None):
    """Ein Lauf. x_train=None heißt: unendlicher Strom.

    Dann gibt es keine Trainingsmenge, auf der sich die Lücke messen ließe — jedes
    Beispiel wird genau einmal gesehen, Trainings- und Testverteilung sind dieselbe.
    """
    modell = mlp()
    modell.load_state_dict(init_state)
    opt = (opt_fabrik(modell.parameters()) if opt_fabrik
           else torch.optim.Adam(modell.parameters(), lr=LR))
    lf = nn.CrossEntropyLoss()
    verlauf = {"schritt": [], "test_acc": [], "train_acc": []}
    for schritt, (xb, yb) in enumerate(quelle, start=1):
        opt.zero_grad()
        lf(modell(xb), yb).backward()
        opt.step()
        if schritt == 1 or schritt % 100 == 0:
            verlauf["schritt"].append(schritt)
            verlauf["test_acc"].append(genauigkeit(modell, x_test, y_test))
            verlauf["train_acc"].append(
                None if x_train is None else genauigkeit(modell, x_train, y_train))
        if schritt >= SCHRITTE:
            break
    return verlauf


def median_ueber_reps(name, laeufe_roh):
    """Punktweiser Median der Wiederholungen, dazu die Einzelwerte am Ende."""
    schritt = laeufe_roh[0]["schritt"]
    hat_train = laeufe_roh[0]["train_acc"][0] is not None

    def med(schluessel):
        if schluessel == "train_acc" and not hat_train:
            return None
        spalten = np.array([lauf[schluessel] for lauf in laeufe_roh], dtype=float)
        return [round(v, 4) for v in np.median(spalten, axis=0)]

    test, train = med("test_acc"), med("train_acc")
    final = sorted(round(lauf["test_acc"][-1], 4) for lauf in laeufe_roh)
    print(f"  {name:28s} Test {test[-1]:.3f}  [{final[0]:.3f}–{final[-1]:.3f}]   Train "
          f"{'  --      --   ' if train is None else f'{train[-1]:.3f}   {train[-1] - test[-1]:+.3f}'}")
    return {"schritt": schritt, "test_acc": test, "train_acc": train,
            "test_final_je_rep": final}


# ---------------------------------------------------------------- Abkürzungen messen

def abkuerzungen(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    """Wie weit kommt man ohne die Form? Trennt die Aufgabe von ihren Artefakten."""
    kontrast = np.abs(x - np.median(x.reshape(len(x), -1), axis=1)[:, None, None])
    tinte = kontrast.sum(axis=(1, 2))[:, None]
    hell = x.mean(axis=(1, 2))[:, None]
    maske = kontrast > 0.15
    hoehe, breite = maske.any(axis=2).sum(1), maske.any(axis=1).sum(1)
    bbox = np.stack([hoehe, breite, hoehe * breite], axis=1).astype(float)
    fuellgrad = (maske.sum(axis=(1, 2)) / np.maximum(hoehe * breite, 1))[:, None]

    n = len(y)
    tr, te = slice(0, n // 2), slice(n // 2, None)

    def fit(merkmale):
        m = LogisticRegression(max_iter=2000).fit(merkmale[tr], y[tr])
        return round(float(m.score(merkmale[te], y[te])), 3)

    return {
        "tinte": fit(tinte),
        "helligkeit": fit(hell),
        "bbox": fit(bbox),
        "fuellgrad": fit(fuellgrad),
        "alle_vier": fit(np.hstack([tinte, hell, bbox, fuellgrad])),
        "linear_auf_pixeln": fit(x.reshape(n, -1)),
    }


# ---------------------------------------------------------------- Lauf

def main() -> None:
    cfg = ShapeConfig()
    torch.manual_seed(SEED)
    torch.use_deterministic_algorithms(True)

    xt, yt = sample_batch(cfg, np.random.default_rng(99_999), 10_000)
    x_test, y_test = torch.from_numpy(xt), torch.from_numpy(yt)

    print("Abkürzungen (50 % = Raten):")
    kurz = abkuerzungen(xt, yt)
    for k, v in kurz.items():
        print(f"  {k:20s} {v:.3f}")

    anzahl = sum(p.numel() for p in mlp().parameters())
    print(f"\nMLP 1024-256-128-2, {anzahl:,} Parameter; Budget je Lauf "
          f"{SCHRITTE} x {BATCH} = {SCHRITTE * BATCH:,} gesehene Beispiele; "
          f"{REPS} Wiederholungen, berichtet wird der Median")

    # Je Wiederholung eine andere Initialisierung und eine andere Ziehung, aber für alle
    # Stichprobengrößen dieselben — sonst vergleicht die Abbildung zwei Dinge auf einmal.
    inits = []
    for r in range(REPS):
        torch.manual_seed(SEED + r)
        inits.append(mlp().state_dict())

    t0 = time.time()
    laeufe = []
    for n in GROESSEN:
        roh = []
        for r in range(REPS):
            ds = FormenFest(cfg, n, seed=1234 + 101 * r)
            # **Mit Zurücklegen**, und zwar für jedes N gleich. Mit `shuffle=True` wäre die
            # Batchgröße bei N=64 auf 64 begrenzt, und dieser eine Lauf sähe halb so viele
            # Beispiele wie die anderen -- dann vergliche die Abbildung zwei Dinge auf
            # einmal. So zieht jeder Lauf dieselben SCHRITTE x BATCH Beispiele i.i.d. aus
            # seiner Menge, genau wie der Strom aus der Verteilung; die Trägermenge ist die
            # einzige Variable.
            loader = DataLoader(ds, batch_size=BATCH, sampler=RandomSampler(
                ds, replacement=True, num_samples=SCHRITTE * BATCH))
            roh.append(trainiere(loader, inits[r], x_test, y_test, ds.x, ds.y))
        laeufe.append({"n": n, "epochen": round(SCHRITTE * BATCH / n, 1),
                       **median_ueber_reps(f"N={n} ({SCHRITTE * BATCH / n:.0f} Epochen)", roh)})

    # Der unendliche Strom: jedes Beispiel genau einmal, „eine Epoche“, die nie endet.
    # Die Worker sind hier kein Luxus — das Ziehen kostet mehr als der Gradientenschritt.
    roh = []
    for r in range(REPS):
        loader = DataLoader(FormenIterable(cfg, seed=7 + 13 * r), batch_size=BATCH,
                            num_workers=WORKERS)
        roh.append(trainiere(loader, inits[r], x_test, y_test))
    laeufe.append({"n": None, "epochen": 1.0,
                   **median_ueber_reps(f"Strom (1 Epoche, {WORKERS} Worker)", roh)})
    print(f"\n{REPS * (len(GROESSEN) + 1)} Läufe in {time.time() - t0:.0f}s")

    # Dieselben Seeds wie oben: Die Adam-Zeile muss die ersten drei Wiederholungen des
    # Stroms exakt wiederholen — eine billige Gegenprobe, dass die Fabrik nichts
    # verschiebt.
    print(f"\nOptimierer am Strom, Median aus {REPS_OPT} Wiederholungen:")
    optimierer = {}
    for name, fabrik in OPTIMIERER:
        werte = []
        for r in range(REPS_OPT):
            loader = DataLoader(FormenIterable(cfg, seed=7 + 13 * r), batch_size=BATCH,
                                num_workers=WORKERS)
            lauf = trainiere(loader, inits[r], x_test, y_test, opt_fabrik=fabrik)
            werte.append(round(lauf["test_acc"][-1], 4))
        optimierer[name] = {"test_final": round(float(np.median(werte)), 4),
                            "je_rep": sorted(werte)}
        print(f"  {name:12s} {optimierer[name]['test_final']:.3f}   {werte}")

    ZIEL.write_text(json.dumps({
        "erzeugt_von": "devnotes/make_formen_daten.py",
        "config": asdict(cfg),
        "parameter": anzahl,
        "schritte": SCHRITTE,
        "reps": REPS,
        "batch": BATCH,
        "lr": LR,
        "test_n": len(yt),
        "kurven": KURVEN,
        "abkuerzungen": kurz,
        "laeufe": laeufe,
        "reps_opt": REPS_OPT,
        "optimierer": optimierer,
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\ngeschrieben: {ZIEL.relative_to(WURZEL)}")


if __name__ == "__main__":
    main()
