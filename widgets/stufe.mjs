// Eine Stufe aus zwei Sigmoid-Neuronen: n(x) = v1·σ(w1·x + b1) + v2·σ(w2·x + b2), mit Reglern
// für Gewicht w, Bias b und Ausgabegewicht v je Neuron. Oben die beiden Neuronen einzeln,
// unten ihre Summe, auf Wunsch mit der Stufe aus der Abbildung als Ziel. Eingebunden im
// Kapitel „Universelle Approximation“ über {anywidget}; im PDF steht statt dessen die
// Abbildung vl11-step-from-sigmoids.png. Keine Abhängigkeiten.
//
// Absichtlich auf [0, 1] wie die Abbildung und nicht auf [1, 2] wie die Übung: Das Widget soll
// die Konstruktion zeigen, nicht die Aufgabe lösen.
//
// Modell (JSON5 im Direktivenrumpf): {n1: [w, b, v], n2: [w, b, v]}

const NS = "http://www.w3.org/2000/svg";
const XB = [0, 1];
const B = 520; // Breite der Zeichenfläche (viewBox)
const HO = 120; // Höhe des oberen Panels (die Neuronen, Werte in [0, 1])
const HU = 200; // Höhe des unteren Panels (die Summe)
const YU = [-1, 2]; // Wertebereich unten
const LUECKE = 34;
const RAND = 8;
// Ziel wie in der Abbildung: Höhe 0,8 auf [0,3; 0,6]
const ZIEL = { links: 0.3, rechts: 0.6, hoehe: 0.8 };
const REGLER = {
  w: { min: -200, max: 200, schritt: 1 },
  b: { min: -200, max: 200, schritt: 1 },
  v: { min: -2, max: 2, schritt: 0.05 },
};

const FARBEN = {
  hell: { n1: "#006AB3", n2: "#EE7F00", summe: "#003964", ziel: "#8CB110", gitter: "#e3e3e3" },
  dunkel: { n1: "#5aa9e6", n2: "#ffa040", summe: "#e8e8e8", ziel: "#a8d42a", gitter: "#3a3a3a" },
};

const zahl = (x, stellen = 2) =>
  (Math.abs(x) < 0.5 * 10 ** -stellen ? 0 : x).toLocaleString("de-DE", {
    minimumFractionDigits: stellen,
    maximumFractionDigits: stellen,
  });
const sigma = (z) => 1 / (1 + Math.exp(-z));

function el(tag, attrs = {}, parent) {
  const e = document.createElementNS(NS, tag);
  for (const [k, val] of Object.entries(attrs)) e.setAttribute(k, val);
  if (parent) parent.appendChild(e);
  return e;
}

function render({ model, el: wurzel }) {
  const start = { n1: [...(model.get("n1") ?? [20, -4, 1])], n2: [...(model.get("n2") ?? [20, -14, 1])] };
  let p = { n1: [...start.n1], n2: [...start.n2] };
  let zielZeigen = true;

  const box = document.createElement("div");
  box.className = "stufe";
  const stil = document.createElement("style");
  stil.textContent = `
    .stufe { font-family: inherit; color: inherit; margin: 1rem 0; }
    .stufe svg { width: 100%; height: auto; display: block; }
    .stufe .gitter line { stroke: var(--gitter); stroke-width: 1; }
    .stufe .achsen line { stroke: currentColor; stroke-width: 1; opacity: 0.5; }
    .stufe .beschriftung { fill: currentColor; font-size: 15px; }
    .stufe .regler { display: grid; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
      gap: 0.4rem 1.5rem; margin-top: 0.6rem; }
    .stufe fieldset { border: 1px solid var(--gitter); border-radius: 6px; padding: 0.3rem 0.7rem 0.5rem; margin: 0; }
    .stufe legend { font-weight: 600; padding: 0 0.3rem; }
    .stufe label { display: grid; grid-template-columns: 1.6rem 1fr 3.6rem; align-items: center;
      gap: 0.5rem; font-variant-numeric: tabular-nums; }
    .stufe label span:last-child { text-align: right; }
    .stufe input[type=range] { width: 100%; accent-color: var(--akzent); }
    .stufe .leiste { display: flex; flex-wrap: wrap; gap: 0.5rem 1.2rem; align-items: center; margin-top: 0.6rem; }
    .stufe button { font: inherit; color: inherit; background: transparent; border: 1px solid currentColor;
      border-radius: 6px; padding: 0.2em 0.7em; cursor: pointer; }
    .stufe button:hover { background: rgba(127,127,127,0.15); }
    .stufe .stand { font-variant-numeric: tabular-nums; margin-top: 0.5rem; line-height: 1.6; }
    .stufe .hinweis { font-size: 0.85em; opacity: 0.75; margin-top: 0.4rem; }
  `;
  box.appendChild(stil);

  const H = HO + LUECKE + HU;
  const svg = el("svg", { viewBox: `0 0 ${B} ${H}`, role: "img" });
  box.appendChild(svg);
  const bx = (x) => RAND + ((x - XB[0]) / (XB[1] - XB[0])) * (B - 2 * RAND);
  const byO = (y) => HO - 6 - y * (HO - 22);
  const byU = (y) => HO + LUECKE + ((YU[1] - y) / (YU[1] - YU[0])) * HU;

  // Gitter und Achsen
  const gitter = el("g", { class: "gitter" }, svg);
  for (let k = 0; k <= 10; k++) {
    const x = bx(k / 10);
    el("line", { x1: x, y1: 14, x2: x, y2: HO }, gitter);
    el("line", { x1: x, y1: HO + LUECKE, x2: x, y2: H }, gitter);
  }
  for (const y of [-1, -0.5, 0.5, 1, 1.5, 2]) el("line", { x1: RAND, y1: byU(y), x2: B - RAND, y2: byU(y) }, gitter);
  el("line", { x1: RAND, y1: byO(1), x2: B - RAND, y2: byO(1) }, gitter);
  const achsen = el("g", { class: "achsen" }, svg);
  el("line", { x1: RAND, y1: byO(0), x2: B - RAND, y2: byO(0) }, achsen);
  el("line", { x1: RAND, y1: byU(0), x2: B - RAND, y2: byU(0) }, achsen);
  const text = (x, y, inhalt, anker = "start") => {
    const t = el("text", { x, y, class: "beschriftung", "text-anchor": anker }, svg);
    t.textContent = inhalt;
    return t;
  };
  text(RAND + 2, 11, "die beiden Neuronen σ(w·x + b), Werte in [0; 1]");
  text(RAND + 2, HO + LUECKE - 6, "Ausgabe n(x) = v₁·σ₁ + v₂·σ₂");
  for (const k of [0, 5, 10]) text(bx(k / 10), H - 3, zahl(k / 10, 1), k === 0 ? "start" : k === 10 ? "end" : "middle");
  for (const y of [1, 2, -1]) text(B - RAND - 2, byU(y) + 13, zahl(y, 0), "end");

  const zielPfad = el("path", { fill: "none", "stroke-width": 2, "stroke-dasharray": "6 4" }, svg);
  const kurve1 = el("path", { fill: "none", "stroke-width": 2.2 }, svg);
  const kurve2 = el("path", { fill: "none", "stroke-width": 2.2 }, svg);
  const summe = el("path", { fill: "none", "stroke-width": 2.8 }, svg);
  const marke1 = el("line", { "stroke-width": 1, "stroke-dasharray": "2 3" }, svg);
  const marke2 = el("line", { "stroke-width": 1, "stroke-dasharray": "2 3" }, svg);

  // Regler
  const reglerBox = document.createElement("div");
  reglerBox.className = "regler";
  box.appendChild(reglerBox);
  const anzeigen = {};
  const eingaben = {};
  for (const [n, titel] of [["n1", "Neuron 1"], ["n2", "Neuron 2"]]) {
    const fs = document.createElement("fieldset");
    fs.style.setProperty("--akzent", "currentColor");
    const lg = document.createElement("legend");
    lg.textContent = titel;
    fs.appendChild(lg);
    ["w", "b", "v"].forEach((name, i) => {
      const r = REGLER[name];
      const lab = document.createElement("label");
      const kurz = document.createElement("span");
      kurz.innerHTML = `<i>${name}</i><sub>${n[1]}</sub>`;
      const inp = document.createElement("input");
      Object.assign(inp, { type: "range", min: r.min, max: r.max, step: r.schritt, value: p[n][i] });
      inp.setAttribute("aria-label", `${name}${n[1]}, ${name === "w" ? "Gewicht" : name === "b" ? "Bias" : "Ausgabegewicht"} von ${titel}`);
      const wert = document.createElement("span");
      inp.addEventListener("input", () => { p[n][i] = Number(inp.value); zeichne(); });
      lab.append(kurz, inp, wert);
      fs.appendChild(lab);
      anzeigen[`${n}${name}`] = wert;
      eingaben[`${n}${name}`] = inp;
    });
    reglerBox.appendChild(fs);
  }

  const leiste = document.createElement("div");
  leiste.className = "leiste";
  const zurueck = document.createElement("button");
  zurueck.type = "button";
  zurueck.textContent = "Zurücksetzen";
  zurueck.addEventListener("click", () => {
    p = { n1: [...start.n1], n2: [...start.n2] };
    ["w", "b", "v"].forEach((name, i) => {
      eingaben[`n1${name}`].value = p.n1[i];
      eingaben[`n2${name}`].value = p.n2[i];
    });
    zeichne();
  });
  const zielWahl = document.createElement("label");
  zielWahl.style.display = "inline-flex";
  zielWahl.style.gap = "0.4rem";
  const zielBox = document.createElement("input");
  zielBox.type = "checkbox";
  zielBox.checked = zielZeigen;
  zielBox.addEventListener("change", () => { zielZeigen = zielBox.checked; zeichne(); });
  zielWahl.append(zielBox, document.createTextNode("Ziel zeigen: Stufe der Höhe 0,8 auf [0,3; 0,6]"));
  leiste.append(zurueck, zielWahl);
  box.appendChild(leiste);

  const stand = document.createElement("div");
  stand.className = "stand";
  stand.setAttribute("aria-live", "polite");
  box.appendChild(stand);
  const hinweis = document.createElement("div");
  hinweis.className = "hinweis";
  hinweis.textContent = "Jedes Neuron springt bei x = −b/w; je größer |w|, desto steiler. Das Vorzeichen von v entscheidet, ob die Stufe hoch- oder runtergeht.";
  box.appendChild(hinweis);

  function farben() {
    const fb = FARBEN[document.documentElement.classList.contains("dark") ? "dunkel" : "hell"];
    box.style.setProperty("--gitter", fb.gitter);
    kurve1.setAttribute("stroke", fb.n1);
    kurve2.setAttribute("stroke", fb.n2);
    marke1.setAttribute("stroke", fb.n1);
    marke2.setAttribute("stroke", fb.n2);
    summe.setAttribute("stroke", fb.summe);
    zielPfad.setAttribute("stroke", fb.ziel);
    const [f1, f2] = box.querySelectorAll("fieldset");
    f1.style.setProperty("--akzent", fb.n1);
    f2.style.setProperty("--akzent", fb.n2);
    f1.querySelector("legend").style.color = fb.n1;
    f2.querySelector("legend").style.color = fb.n2;
  }

  function zeichne() {
    farben();
    const N = 600;
    const xs = Array.from({ length: N + 1 }, (_, k) => XB[0] + (k / N) * (XB[1] - XB[0]));
    const s1 = xs.map((x) => sigma(p.n1[0] * x + p.n1[1]));
    const s2 = xs.map((x) => sigma(p.n2[0] * x + p.n2[1]));
    const n = xs.map((_, k) => p.n1[2] * s1[k] + p.n2[2] * s2[k]);
    // Werte außerhalb von YU an den Rand drücken, statt über das Panel hinaus zu malen
    const pfad = (ys, by) => ys.map((y, k) => `${k ? "L" : "M"}${bx(xs[k]).toFixed(1)},${by(Math.max(YU[0], Math.min(YU[1], y))).toFixed(1)}`).join("");
    kurve1.setAttribute("d", pfad(s1, byO));
    kurve2.setAttribute("d", pfad(s2, byO));
    summe.setAttribute("d", pfad(n, byU));

    const sprung = (q) => (q[0] !== 0 ? -q[1] / q[0] : NaN);
    for (const [m, q] of [[marke1, p.n1], [marke2, p.n2]]) {
      const s = sprung(q);
      const sichtbar = Number.isFinite(s) && s >= XB[0] && s <= XB[1];
      m.style.display = sichtbar ? "" : "none";
      if (sichtbar) {
        m.setAttribute("x1", bx(s)); m.setAttribute("x2", bx(s));
        m.setAttribute("y1", 14); m.setAttribute("y2", H - 14);
      }
    }

    let abweichung = 0;
    if (zielZeigen) {
      const z = (x) => (x >= ZIEL.links && x <= ZIEL.rechts ? ZIEL.hoehe : 0);
      zielPfad.setAttribute("d", `M${bx(0)},${byU(0)} H${bx(ZIEL.links)} V${byU(ZIEL.hoehe)} H${bx(ZIEL.rechts)} V${byU(0)} H${bx(1)}`);
      zielPfad.style.display = "";
      // mittlere absolute Abweichung über [0, 1]; die maximale ist an den Sprüngen immer ≈ 0,4
      abweichung = xs.reduce((a, x, k) => a + Math.abs(n[k] - z(x)), 0) / xs.length;
    } else {
      zielPfad.style.display = "none";
    }

    for (const n_ of ["n1", "n2"]) {
      anzeigen[`${n_}w`].textContent = zahl(p[n_][0], 0);
      anzeigen[`${n_}b`].textContent = zahl(p[n_][1], 0);
      anzeigen[`${n_}v`].textContent = zahl(p[n_][2]);
    }
    const term = (q) => `${zahl(q[2])}·σ(${zahl(q[0], 0)}·<i>x</i> ${q[1] < 0 ? "−" : "+"} ${zahl(Math.abs(q[1]), 0)})`;
    const stelle = (q) => (q[0] !== 0 ? zahl(-q[1] / q[0]) : "–");
    stand.innerHTML = `<i>n</i>(<i>x</i>) = ${term(p.n1)} ${p.n2[2] < 0 ? "−" : "+"} ${term([p.n2[0], p.n2[1], Math.abs(p.n2[2])])}<br>
      Sprungstellen −<i>b</i>/<i>w</i>: Neuron 1 bei ${stelle(p.n1)}, Neuron 2 bei ${stelle(p.n2)}
      ${zielZeigen ? `<br>mittlere Abweichung vom Ziel auf [0; 1]: ${zahl(abweichung, 3)}` : ""}`;
    svg.setAttribute("aria-label", `Graph von n(x) auf [0; 1]; Sprungstellen bei ${stelle(p.n1)} und ${stelle(p.n2)}`);
  }

  const beobachter = new MutationObserver(zeichne);
  beobachter.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });

  wurzel.appendChild(box);
  zeichne();
  return () => {
    beobachter.disconnect();
    box.remove();
  };
}

export default { render };
