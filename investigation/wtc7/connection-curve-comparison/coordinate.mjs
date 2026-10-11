// Pure coordinate helpers and guarded read-only UI. R1 contract adapted for variable dimensions.
// R1 coordinate.js SHA: 38cc0cd9b0947e05072ec8656c58e4fc4ca95d968bd1a903af26afe43db0b05b.
const finite = (v) => typeof v === "number" && Number.isFinite(v);
const dimensions = (w, h) => Number.isSafeInteger(w) && w > 0 && Number.isSafeInteger(h) && h > 0;
const validRect = (r) => r && [r.left, r.top, r.width, r.height].every(finite) &&
  r.width > 0 && r.height > 0 && finite(r.left + r.width) && finite(r.top + r.height) &&
  r.left + r.width > r.left && r.top + r.height > r.top;
const validPixel = (p, w, h) => dimensions(w, h) && p && Number.isInteger(p.x) &&
  Number.isInteger(p.y) && p.x >= 0 && p.y >= 0 && p.x < w && p.y < h;

export function pointerToPixel(x, y, r, w, h) {
  if (!dimensions(w, h) || !validRect(r) || !finite(x) || !finite(y) ||
      x < r.left || y < r.top || x >= r.left + r.width || y >= r.top + r.height) return null;
  return { x: Math.min(w - 1, Math.floor((x - r.left) / r.width * w)),
    y: Math.min(h - 1, Math.floor((y - r.top) / r.height * h)) };
}
export function pixelCenter(p, r, w, h) {
  if (!validPixel(p, w, h) || !validRect(r)) return null;
  return { clientX: r.left + (p.x + .5) * (r.width / w),
    clientY: r.top + (p.y + .5) * (r.height / h) };
}
export function nudgePixel(p, key, w, h) {
  if (!validPixel(p, w, h)) return null;
  const moves = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] };
  if (!Object.hasOwn(moves, key)) return null;
  const [dx, dy] = moves[key];
  return { x: Math.max(0, Math.min(w - 1, p.x + dx)), y: Math.max(0, Math.min(h - 1, p.y + dy)) };
}

// Literal JSON shared by inspection/tests, not fetched and never writable through the UI.
export const ASSETS = {
  "control": {"url":"/control.png","width":1280,"height":720,"bytes":11216,"hash":"f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48"},
  "73": {"url":"/pages/073.png","width":1700,"height":2200,"bytes":497348,"hash":"471745c7181f5edd02d84ad80ea3d396d26571c3441863b5909f8200877dbc4b"},
  "74": {"url":"/pages/074.png","width":1700,"height":2200,"bytes":279563,"hash":"132859b7a2e3d5abb95f1411c7f111d6ec07c7c751ae2b1cd80954713a155856"},
  "75": {"url":"/pages/075.png","width":1700,"height":2200,"bytes":309181,"hash":"60f4b265ff9449de096a091bbea9b0d8350209cee2a388533ee5c11efa802b20"},
  "76": {"url":"/pages/076.png","width":1700,"height":2200,"bytes":943120,"hash":"0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6"},
  "77": {"url":"/pages/077.png","width":1700,"height":2200,"bytes":499256,"hash":"cd0a15b5fa18a352c79d418d439f95c69b29f3713ff1106f0d325f269a9affc6"},
  "117": {"url":"/pages/117.png","width":1700,"height":2200,"bytes":456303,"hash":"0f031fc21ba1639185ce134045ef6c6a4fcd8f814c4d0863b7e4e67e4b9f6e3d"}
};
export const CANDIDATES = {
  "F0":{"x":449,"y":829}, "Fright":{"x":1294,"y":829}, "Ftop":{"x":449,"y":224},
  "E0":{"x":473,"y":1669}, "Eright":{"x":1297,"y":1669}, "Etop":{"x":473,"y":1048}
};
export const ANCHORS = [
  {id:"F0",plot:"Force",feature:"left-bottom axis intersection",candidate:"F0",xRange:"446–452",yRange:"826–832"},
  {id:"FR",plot:"Force",feature:"right-bottom axis intersection",candidate:"Fright",xRange:"1291–1297",yRange:"826–832"},
  {id:"FT",plot:"Force",feature:"left-top axis intersection",candidate:"Ftop",xRange:"446–452",yRange:"221–227"},
  {id:"E0",plot:"Energy",feature:"left-bottom axis intersection",candidate:"E0",xRange:"470–476",yRange:"1666–1672"},
  {id:"ER",plot:"Energy",feature:"right-bottom axis intersection",candidate:"Eright",xRange:"1294–1300",yRange:"1666–1672"},
  {id:"ET",plot:"Energy",feature:"left-top axis intersection",candidate:"Etop",xRange:"470–476",yRange:"1045–1051"}
];

const cleanCell = (value) => String(value ?? "").replace(/[\t\r\n]+/g, " ").trim();
export function formatReviewTSV(observations, labelNotes = "") {
  const lines = ["Anchor\tGraph location\tAI locator (page pixels)\tProposed x range\tProposed y range\tHuman status\tObserved x\tObserved y"];
  for (const anchor of ANCHORS) {
    const proposed = CANDIDATES[anchor.candidate];
    const answer = observations[anchor.id];
    lines.push([anchor.id, `${anchor.plot}: ${anchor.feature}`, `(${proposed.x}, ${proposed.y})`,
      anchor.xRange, anchor.yRange, answer?.status ?? "not checked",
      answer?.point?.x ?? "", answer?.point?.y ?? ""].map(cleanCell).join("\t"));
  }
  lines.push("", `Axis / legend notes\t${cleanCell(labelNotes)}`);
  return lines.join("\n");
}

export function initializeReview() {
  const byId = (id) => document.getElementById(id);
  const viewport = byId("viewport"), stage = byId("stage"), marker = byId("marker");
  const selector = byId("page"), readout = byId("readout"), status = byId("load-status");
  let image = byId("page-image"), item = ASSETS.control, ready = false, point = null;
  let locked = false, provenance = "", zoom = "fit", generation = 0;
  const observations = Object.create(null);
  let anchorIndex = 0;
  const anchorProgress = byId("anchor-progress"), reviewOutput = byId("review-output");

  function renderReview() {
    for (let i = 0; i < ANCHORS.length; i++) {
      const anchor = ANCHORS[i], answer = observations[anchor.id];
      byId(`row-${anchor.id}`).dataset.current = String(i === anchorIndex);
      byId(`answer-${anchor.id}`).textContent = answer?.point ? `(${answer.point.x}, ${answer.point.y})` : "—";
      byId(`state-${anchor.id}`).textContent = answer?.status === "unreadable" ? "Unreadable" :
        answer?.point ? "Observed by click" : "Not checked";
    }
    const anchor = ANCHORS[anchorIndex];
    anchorProgress.textContent = `Anchor ${anchorIndex + 1} of ${ANCHORS.length}: ${anchor.id} — ${anchor.plot}, ${anchor.feature}. Click the actual intersection, then use arrow keys if needed.`;
    reviewOutput.value = formatReviewTSV(observations, byId("label-notes").value);
    byId("previous-anchor").disabled = anchorIndex === 0;
    byId("next-anchor").disabled = anchorIndex === ANCHORS.length - 1;
  }

  function activateAnchor() {
    if (selector.value !== "76" || !ready) return;
    const anchor = ANCHORS[anchorIndex], answer = observations[anchor.id];
    setZoom("1");
    if (answer?.point) {
      point = { ...answer.point }; locked = true; provenance = "YOUR RECORDED OBSERVATION"; showPoint();
      const r = image.getBoundingClientRect();
      viewport.scrollLeft = (point.x + .5) * (r.width / item.width) - viewport.clientWidth / 2;
      viewport.scrollTop = (point.y + .5) * (r.height / item.height) - viewport.clientHeight / 2;
      viewport.focus({ preventScroll: true });
      viewport.scrollIntoView({ block: "center" });
    } else {
      markCandidate(anchor.candidate);
    }
  }

  function showPoint() {
    marker.hidden = true;
    if (!ready) { readout.textContent = "Coordinates unavailable: image not ready."; return; }
    if (!point) { readout.textContent = "No point — hover or click to lock; nothing is saved."; return; }
    const center = pixelCenter(point, image.getBoundingClientRect(), item.width, item.height);
    if (!center) return;
    const base = stage.getBoundingClientRect();
    marker.style.left = `${center.clientX - base.left}px`;
    marker.style.top = `${center.clientY - base.top}px`;
    marker.hidden = false;
    const unit = selector.value === "control" ? "synthetic image pixel" : "page-render pixel";
    readout.textContent = `${locked ? provenance : "HOVER"} — x: ${point.x}, y: ${point.y} (${unit}; not accepted)`;
  }
  function clearPoint() { point = null; locked = false; provenance = ""; showPoint(); }
  function sizeImage() {
    stage.style.width = `${zoom === "fit" ? Math.max(1, Math.min(item.width,
      viewport.clientWidth, viewport.clientHeight * item.width / item.height)) : item.width * Number(zoom)}px`;
    if (!locked) point = null;
    showPoint();
  }
  function setZoom(value) {
    zoom = value;
    for (const b of document.querySelectorAll("[data-zoom]")) {
      b.setAttribute("aria-pressed", String(b.dataset.zoom === value));
    }
    sizeImage();
  }
  function markCandidate(name) {
    point = { ...CANDIDATES[name] }; locked = true;
    provenance = `AI PROPOSED ${name} ±3 px each axis`;
    showPoint();
    const r = image.getBoundingClientRect();
    viewport.scrollLeft = (point.x + .5) * (r.width / item.width) - viewport.clientWidth / 2;
    viewport.scrollTop = (point.y + .5) * (r.height / item.height) - viewport.clientHeight / 2;
    viewport.focus({ preventScroll: true });
    viewport.scrollIntoView({ block: "center" });
  }
  function loadPage(candidate = null) {
    const current = ++generation;
    ready = false; clearPoint();
    image.hidden = true;
    const key = selector.value;
    if (!Object.hasOwn(ASSETS, key)) {
      status.dataset.error = "true"; status.textContent = "Unknown asset; coordinates disabled."; return;
    }
    item = ASSETS[key];
    status.dataset.error = "false"; status.textContent = "Loading; coordinates disabled…";
    byId("kind").textContent = key === "control" ? "Synthetic control — not evidence" :
      `NCSTAR 1-9A physical page ${key} / printed ${Number(key) - 51}; complete 200 dpi render`;
    byId("dimensions").textContent = `${item.width} × ${item.height}; RGB; ${item.bytes} bytes`;
    byId("hash").textContent = item.hash;
    byId("source-hash").textContent = key === "control" ? "Not applicable — synthetic fixture" :
      "cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4";
    const next = new Image(); next.id = "page-image"; next.hidden = true; next.draggable = false;
    next.alt = key === "control" ? "Complete synthetic coordinate-control shapes" : `Complete NCSTAR 1-9A physical page ${key}`;
    next.onload = () => {
      if (current !== generation) return;
      if (next.naturalWidth !== item.width || next.naturalHeight !== item.height) {
        status.dataset.error = "true";
        status.textContent = `Rejected: expected exactly ${item.width} × ${item.height}; coordinates disabled.`;
        return;
      }
      ready = true; next.hidden = false;
      status.textContent = `Loaded ${item.width} × ${item.height}; coordinates enabled; observations remain only in this page session.`;
      sizeImage();
      if (candidate !== null) markCandidate(candidate);
      else activateAnchor();
    };
    next.onerror = () => {
      if (current !== generation) return;
      ready = false; clearPoint(); status.dataset.error = "true";
      status.textContent = "Image load failed; coordinates disabled. Select an image to retry.";
    };
    image.replaceWith(next); image = next;
    viewport.scrollLeft = 0; viewport.scrollTop = 0;
    sizeImage(); next.src = item.url;
  }
  const pointer = (e) => ready ? pointerToPixel(e.clientX, e.clientY,
    image.getBoundingClientRect(), item.width, item.height) : null;
  stage.addEventListener("pointermove", (e) => { if (!ready || locked) return; point = pointer(e); showPoint(); });
  stage.addEventListener("pointerleave", () => { if (!locked) clearPoint(); });
  stage.addEventListener("click", (e) => {
    const selected = pointer(e); if (!selected) return;
    point = selected; locked = true; provenance = "CLICK LOCKED";
    if (selector.value === "76") observations[ANCHORS[anchorIndex].id] = {status:"observed", point:{...point}};
    renderReview();
    viewport.focus({ preventScroll: true }); showPoint();
  });
  viewport.addEventListener("keydown", (e) => {
    if (!ready || !locked) return;
    const moved = nudgePixel(point, e.key, item.width, item.height);
    if (!moved) return;
    e.preventDefault(); point = moved; provenance = "KEYBOARD ADJUSTED";
    if (selector.value === "76" && observations[ANCHORS[anchorIndex].id]?.status === "observed") {
      observations[ANCHORS[anchorIndex].id].point = {...point};
    }
    renderReview(); showPoint();
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { e.preventDefault(); clearPoint(); } });
  viewport.addEventListener("scroll", () => { if (!locked) clearPoint(); });
  byId("clear").addEventListener("click", clearPoint);
  selector.addEventListener("change", () => loadPage());
  byId("previous-anchor").addEventListener("click", () => {
    if (anchorIndex === 0) return;
    anchorIndex--; renderReview(); activateAnchor();
  });
  byId("next-anchor").addEventListener("click", () => {
    if (anchorIndex >= ANCHORS.length - 1) return;
    anchorIndex++; renderReview(); activateAnchor();
  });
  byId("mark-unreadable").addEventListener("click", () => {
    observations[ANCHORS[anchorIndex].id] = {status:"unreadable"};
    clearPoint();
    if (anchorIndex < ANCHORS.length - 1) anchorIndex++;
    renderReview(); activateAnchor();
  });
  byId("clear-answer").addEventListener("click", () => {
    delete observations[ANCHORS[anchorIndex].id]; clearPoint(); renderReview(); activateAnchor();
  });
  byId("hide-marker").addEventListener("click", clearPoint);
  byId("label-notes").addEventListener("input", renderReview);
  byId("copy-review").addEventListener("click", async () => {
    reviewOutput.value = formatReviewTSV(observations, byId("label-notes").value);
    try {
      await navigator.clipboard.writeText(reviewOutput.value);
      byId("copy-status").textContent = "Copied. Paste the table into chat when ready.";
    } catch {
      reviewOutput.focus(); reviewOutput.select();
      byId("copy-status").textContent = "Clipboard access is unavailable. The table is selected; copy it manually, then paste into chat.";
    }
  });
  for (const b of document.querySelectorAll("[data-zoom]")) b.addEventListener("click", () => setZoom(b.dataset.zoom));
  for (const b of document.querySelectorAll("[data-candidate]")) b.addEventListener("click", () => {
    const anchor = ANCHORS.find((entry) => entry.id === b.dataset.candidate);
    if (!anchor) return;
    anchorIndex = ANCHORS.indexOf(anchor); renderReview();
    selector.value = "76"; setZoom("1"); loadPage(anchor.candidate);
  });
  new ResizeObserver(sizeImage).observe(viewport);
  renderReview();
  loadPage();
}
if (typeof document !== "undefined") initializeReview();
