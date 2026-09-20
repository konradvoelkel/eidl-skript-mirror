# Grundlagen-Snippets: umgesetzt am 2026-09-20

Dieses Dokument war ein Vorschlag (Stand 2026-09-19) für stillschweigend vorausgesetzte Mathematik am Anfang des
Skripts. Konrad hat am 2026-09-20 alle zwölf Snippets freigegeben; sie sind eingebaut. Die ausformulierten Texte
stehen jetzt nur noch in den Kapiteln, nicht mehr hier, damit es keine zwei Fassungen gibt.

**Prinzip** (gilt weiter): Was das [Data-Science-Skript](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/)
schon erklärt, wird verlinkt und in ein bis zwei Sätzen erinnert, nicht neu erklärt. Neu geschrieben wird nur, was
dort fehlt oder erst im Zusammenspiel mit einem Neuron seine Bedeutung bekommt.

| Snippet | Wo es jetzt steht |
|---|---|
| 0 Rückverweise aufs DS-Skript | `README.md` (Satz unter „Inhaltliche Voraussetzungen“); Links in 06, 07, 08 und Blatt 1, 5 |
| 1 Notationsbox Datenpunkt/Feature/Stichprobe | „Was ist Deep Learning?“ (01), vor „Daten und erzeugende Verteilung“; Folgeänderung $x^{(i)}_j$ in „Gradientenabstieg“ (08) |
| 2 Vorzeichenbehafteter Abstand, Rolle von $\|w\|$ | „Neuron und Perzeptron“ (02), Abschnitt „Das Perzeptron“; Querverweis in „Logistische Regression“ (06) bei der Steilheit $k$ |
| 3 Zeilenbild von $Wx$ | „Neuron und Perzeptron“ (02), nach $h = \sigma(Wx + b)$ |
| 4 Überraschung und Entropie verlinken | „Logistische Regression“ (06), „Schon mal irgendwo gesehen?“ und bei `BCELoss` |
| 5A Maximum Likelihood → BCE | **neues Kapitel** „Loss-Funktionen und Maximum Likelihood“ (07) |
| 5B Gradient $p - y$, zurück zur Perzeptronregel | „Gradientenabstieg“ (08), „Und zurück zur logistischen Regression“ |
| 6 Linear trennbar: LogReg hört nie auf | „Loss-Funktionen und Maximum Likelihood“ (07), Warnbox am Ende; Hinweis auf Blatt 4 |
| 7 Ableiten nach $w$, nicht nach $x$ | „Loss-Funktionen und Maximum Likelihood“ (07), Box in „Optimieren mit Fehlerterm“ |
| 8 Summe über Pfade, numerische Probe | „Gradientenabstieg“ (08), Ende der Kettenregel-Erinnerung |
| 9 Loss als Mittelwert, Erwartungswert | „Gradientenabstieg“ (08), SGD-Abschnitt |
| 10 Feature-Skalierung | „Gradientenabstieg“ (08), „Der Algorithmus“ |
| 11 Numerik von $e^x$ und $\ln$ | „Logistische Regression“ (06), Warnbox vor dem Kapitelende |
| 12 Übungsaufgaben | Blatt 1 Aufgabe 4b, Blatt 3 Aufgabe 2b, Blatt 5 Aufgabe 1b (je mit Lösungsvorschlag); Blatt 5 Aufgabe 4 mit DS-Link |

**Split** (Variante 1 aus dem Vorschlag, umgesetzt): „Gradientenabstieg“ wurde geteilt in „Loss-Funktionen und
Maximum Likelihood“ (07: Rückblick, BCE und Perceptron Loss, Maximum Likelihood, Optimieren mit Fehlerterm, Warnung
zu trennbaren Daten) und „Gradientenabstieg“ (08: Kettenregel, Gradienten, Algorithmus, Perzeptron und logistische
Regression, Loss-Kurven, SGD). Alle folgenden Kapitel sind um eins hochnummeriert (08–26 → 09–27).

Offen aus diesem Vorschlag: nichts. Die fachliche Gegenprüfung der neuen Lösungsvorschläge steht in `TODO.md`.
