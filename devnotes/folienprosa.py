r"""Prosa aus den Beamer-Quellen holen — das Gegenstück zu `prosa_zeilen()` für `.tex`.

Damit lassen sich die Prüfungen des Sprachdurchgangs (`sprachpruefliste.py`,
`grammatikpruefung.py`) auf `slides/*.tex` anwenden. Benutzt von
`devnotes/folienpruefliste.py`; als Bibliothek gedacht, nicht als Kommandozeile.

Was herausgenommen wird: LaTeX-Kommentare, `lstlisting`/`verbatim`/`tikzpicture`,
Mathematik, Bild- und Paketmakros. Was **behalten** wird: der Text in `\frametitle`,
`\emph`, `\textbf`, `\item` und — der größte Posten — in `\note{}`. Die Notizen sind
Prosa in derselben Stimme; sie stehen nur nicht an der Wand, sondern auf dem zweiten
Schirm.

Drei Fallen, die beim Bau des Extraktors je eine Ladung Falschmeldungen erzeugt haben
und die man nicht zweimal finden muss:

* **`\textbf{Training}:` wird zu „Training :“**, wenn man nach dem Auflösen eines
  Textmakros stur ein Leerzeichen einfügt. Das ergab 79 Treffer „Leerzeichen vor
  Satzzeichen“, alle falsch — und mitten im Wort („Gradienten\emph{ab}stieg“)
  entsteht so „Gradientenab stieg“. Deshalb wird nie eines eingefügt.
* **`\begin{tabular}{@{}rll@{}}`** — das Spaltenformat ist kein Text und hat
  verschachtelte Klammern, an denen ein `[^}]*`-Muster scheitert.
* **`\\Einführung`** (Zeilenumbruch direkt vor einem Wort) liest der Makro-Parser als
  Makro `\Einf`, weil `[a-zA-Z]+` keine Umlaute kennt; übrig bleibt „ührung“. Das ist
  der Grund, warum `header.tex` und Konfigurationszeilen gar nicht erst geprüft werden.

Mehrzeilige `$…$` erkennt der Extraktor nicht — Mathematik über zwei Zeilen liefert
Bruchstücke wie `dZ`, `dw`. Das ist bekannt und in Kauf genommen: Es erzeugt ein paar
unbekannte Wörter, aber keine falschen Typografie-Befunde.
"""
import re

PLATZ = "\ue000"  # wie in sprachpruefliste.py: ein Zeichen, erzeugt keine Lücke

# Makros, deren Argument Prosa ist und die aufgelöst werden
TEXT = ("emph", "textbf", "textit", "underline", "alert", "frametitle",
        "framesubtitle", "title", "date", "author", "institute", "note",
        "item", "textsc", "footnote", "caption")
# Makros, deren Argument Code oder Adresse ist: Platzhalter
CODE = ("texttt", "url", "path", "lstinline", "href")
# Makros ohne Textargument, die ganz verschwinden (samt optionalem [..] und {..})
WEG = ("setcounter", "addtocounter", "includegraphics", "graphicspath", "input", "usepackage", "documentclass",
       "setbeameroption", "setbeamertemplate", "setlength", "newcommand",
       "renewcommand", "label", "hypersetup", "titlepage", "tableofcontents",
       "lstset", "definecolor", "hspace", "vspace", "raisebox", "colorbox")


def _kommentar_weg(z: str) -> str:
    m = re.search(r"(?<!\\)%", z)
    return z[: m.start()] if m else z


def _arg(s: str, i: int) -> tuple[str, int]:
    """Inhalt der Klammergruppe ab s[i]=='{' plus Index dahinter."""
    tiefe, j = 0, i
    while j < len(s):
        if s[j] == "{" and (j == 0 or s[j - 1] != "\\"):
            tiefe += 1
        elif s[j] == "}" and s[j - 1] != "\\":
            tiefe -= 1
            if tiefe == 0:
                return s[i + 1 : j], j + 1
        j += 1
    return s[i + 1 :], len(s)


def _makros(s: str) -> str:
    """Textmakros auflösen, Code- und Wegmakros ersetzen. Iterativ wegen Verschachtelung."""
    for _ in range(12):
        neu = []
        i, geaendert = 0, False
        while i < len(s):
            m = re.match(r"\\([a-zA-Z]+)\*?", s[i:])
            if not m:
                neu.append(s[i]); i += 1; continue
            name, ende = m.group(1), i + m.end()
            # optionale Argumente überspringen
            while ende < len(s) and s[ende] == "[":
                k = s.find("]", ende)
                if k < 0: break
                ende = k + 1
            if name in TEXT:
                if ende < len(s) and s[ende] == "{":
                    inhalt, nach = _arg(s, ende)
                    # Kein Leerzeichen einfügen: Die Quelle hat ihre Abstände außerhalb
                    # der Klammern schon. Sonst wird „\textbf{Training}:“ zu „Training :“
                    # und „Gradienten\emph{ab}stieg“ zu „Gradientenab stieg“.
                    neu.append(inhalt); i = nach
                else:
                    neu.append(" "); i = ende
                geaendert = True
            elif name in CODE:
                # \href{ziel}{text}: Ziel weg, Text behalten
                if name == "href" and ende < len(s) and s[ende] == "{":
                    _, nach = _arg(s, ende)
                    if nach < len(s) and s[nach] == "{":
                        inhalt, nach2 = _arg(s, nach)
                        neu.append(inhalt + " "); i = nach2; geaendert = True; continue
                    neu.append(PLATZ); i = nach; geaendert = True; continue
                if ende < len(s) and s[ende] == "{":
                    _, nach = _arg(s, ende); i = nach
                else:
                    i = ende
                neu.append(PLATZ); geaendert = True
            elif name in WEG:
                while ende < len(s) and s[ende] == "{":
                    _, ende = _arg(s, ende)
                neu.append(" "); i = ende; geaendert = True
            else:
                neu.append(" "); i = ende; geaendert = True   # Formatiermakro
            continue
        s = "".join(neu)
        if not geaendert:
            break
    return s


def prosa_zeilen_tex(text: str) -> list[str]:
    """Zeilenweise Prosa; Zeilennummern bleiben erhalten."""
    zeilen = [_kommentar_weg(z) for z in text.split("\n")]
    raus, in_code, in_mathe = [], False, False
    for z in zeilen:
        if re.search(r"\\begin\{(lstlisting|verbatim|minted|tikzpicture)\}", z):
            in_code = True; raus.append(""); continue
        if re.search(r"\\end\{(lstlisting|verbatim|minted|tikzpicture)\}", z):
            in_code = False; raus.append(""); continue
        if in_code:
            raus.append(""); continue
        s = z
        # Mehrzeilige $…$: ungerade Anzahl $ heißt, die Mathematik läuft weiter. Ohne das
        # liefert eine über zwei Zeilen gesetzte Formel Bruchstücke wie „dZ“ und „dw“.
        if in_mathe:
            zu = re.search(r"(?<!\\)\$", s)
            if zu is None:
                raus.append(PLATZ); continue
            s = PLATZ + s[zu.end():]
            in_mathe = False          # ohne das frisst jede Folgezeile ihren Anfang
        if len(re.findall(r"(?<!\\)\$", s)) % 2:
            s = s[: s.rfind("$")] + PLATZ
            in_mathe = True
        s = re.sub(r"\$\$.*?\$\$", PLATZ, s)
        s = re.sub(r"(?<!\\)\$[^$]*\$", PLATZ, s)
        s = re.sub(r"\\\[.*?\\\]", PLATZ, s)
        s = re.sub(r"\\\(.*?\\\)", PLATZ, s)
        # \begin{tabular}{@{}rll@{}} — das Spaltenformat ist kein Text
        s = re.sub(r"\\begin\{(tabular|array|column)\*?\}(\[[^\]]*\])?\s*\{(?:[^{}]|\{[^{}]*\})*\}", " ", s)
        s = re.sub(r"\\begin\{[a-zA-Z*]+\}(\[[^\]]*\])?(\{[^}]*\})*", " ", s)
        s = re.sub(r"\\end\{[a-zA-Z*]+\}", " ", s)
        # Zeilenumbruch \\ zuerst: sonst liest _makros „\\Einführung“ als Makro \Einf,
        # weil [a-zA-Z]+ keine Umlaute kennt, und „ührung“ bleibt als Wort übrig.
        s = re.sub(r"\\\\\*?(\[[^\]]*\])?", " ", s)
        s = _makros(s)
        s = s.replace("---", " – ").replace("--", " – ")   # als Strich lesbar machen
        s = re.sub(r"\\[\\,;:!>]|\\\s", " ", s)            # \\, \, \; …
        s = s.replace("~", " ").replace("&", " ")
        s = re.sub(r"[{}]", " ", s)
        s = re.sub(r"\[\s*-?[\d.]+\s*(pt|em|ex|mm|cm|in|bp)\s*\]", " ", s)  # \\[2pt]
        s = re.sub(r"[ \t]+", " ", s)
        raus.append(s.strip())
    return raus
