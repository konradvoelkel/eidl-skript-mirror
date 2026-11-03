// Player der HHU-Mediathek, eingeklappt unter der Linkzeile „Vorlesungsaufzeichnung …“ eines
// Kapitels. Erst ein Klick lädt den Player – wer nur liest, lädt nichts von media.hhu.de. Mit
// Kapitelraster (chapters=true) und derselben Startzeit wie der Link. Im PDF fehlt das Widget,
// dort steht die Linkzeile allein. Keine Abhängigkeiten.
//
// Modell (JSON5 im Direktivenrumpf): {url: '<dieselbe Adresse wie in der Linkzeile darüber>'}.
// devnotes/check_doku.py prüft, dass beide übereinstimmen.

const EINBETTEN = "https://media.hhu.de/media/embed";

function render({ model, el: wurzel }) {
  const url = new URL(model.get("url"));
  const key = url.pathname.split("/").filter(Boolean).pop();
  const t = url.searchParams.get("t");
  const quelle = new URL(EINBETTEN);
  for (const [k, v] of Object.entries({ key, autoplay: "false", chapters: "true", related: "false", responsive: "true" })) {
    quelle.searchParams.set(k, v);
  }
  if (t) quelle.searchParams.set("t", t);

  const box = document.createElement("div");
  box.className = "mediathek";
  const stil = document.createElement("style");
  stil.textContent = `
    .mediathek { font-family: inherit; color: inherit; margin: 0.5rem 0 1rem; }
    .mediathek details { border: 1px solid rgba(127,127,127,0.35); border-radius: 6px; }
    .mediathek summary { cursor: pointer; padding: 0.35rem 0.8rem; list-style: none; }
    .mediathek summary::-webkit-details-marker { display: none; }
    .mediathek summary::before { content: "▶"; display: inline-block; margin-right: 0.5rem;
      font-size: 0.8em; transition: transform 0.15s; }
    .mediathek details[open] summary::before { transform: rotate(90deg); }
    .mediathek summary:hover { background: rgba(127,127,127,0.1); }
    .mediathek .klein { opacity: 0.7; font-size: 0.85em; }
    /* 720 × 745 ist das Format, das die Mediathek für den Player mit Kapitelraster vorschlägt */
    .mediathek iframe { display: block; width: 100%; aspect-ratio: 720 / 745; border: 0;
      border-top: 1px solid rgba(127,127,127,0.35); }
  `;
  box.appendChild(stil);

  const details = document.createElement("details");
  const summary = document.createElement("summary");
  summary.innerHTML = `Aufzeichnung hier abspielen${t ? ` ab ${Math.floor(Number(t) / 60)}:${String(Number(t) % 60).padStart(2, "0")}` : ""} <span class="klein">(lädt den Player der HHU-Mediathek)</span>`;
  details.appendChild(summary);
  details.addEventListener("toggle", () => {
    if (!details.open || details.querySelector("iframe")) return;
    const f = document.createElement("iframe");
    f.src = quelle.href;
    f.title = "Vorlesungsaufzeichnung, Player der HHU-Mediathek";
    f.allow = "fullscreen; picture-in-picture";
    f.allowFullscreen = true;
    details.appendChild(f);
  });
  box.appendChild(details);

  wurzel.appendChild(box);
  return () => box.remove();
}

export default { render };
