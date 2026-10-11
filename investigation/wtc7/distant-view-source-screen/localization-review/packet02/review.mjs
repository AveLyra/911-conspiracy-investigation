import { validateBox, validateResponse, formatResponses } from "./response.mjs";

// Inject only browser primitives and the pinned packet modules. Importing this
// module in Node performs no UI work; tests need no real image or browser.
export function initializeReview({ document: doc, Image: ImageClass,
  ResizeObserver: ResizeClass, assets, frameOrder, core, sourceHash, protocolHash }) {
  const byId = (id) => {
    const element = doc.getElementById(id);
    if (!element) throw new Error(`Missing review element: ${id}`);
    return element;
  };
  const viewport = byId("viewport"), stage = byId("stage"), marker = byId("marker");
  const selector = byId("frame"), loadStatus = byId("load-status");
  const readout = byId("readout"), boxReadout = byId("box-readout");
  const inspected = byId("inspected"), judgment = byId("judgment"), note = byId("note");
  const feedback = byId("feedback"), recordButton = byId("record-row");
  const startBoxButton = byId("start-box"), endpointButton = byId("use-endpoint");
  const rows = new Map(), listeners = [];
  const zoomButtons = [...doc.querySelectorAll("[data-zoom]")];
  let image = byId("native-image"), key = "control", ready = false;
  let point = null, locked = false, first = null, box = null, boxMode = false;
  let zoom = "fit", generation = 0, disposed = false;

  function listen(element, event, callback) {
    element.addEventListener(event, callback);
    listeners.push(() => element.removeEventListener(event, callback));
  }
  function say(message, error = false) {
    feedback.textContent = message;
    feedback.dataset.error = String(error);
  }
  function showPoint() {
    marker.hidden = true;
    recordButton.disabled = !ready;
    startBoxButton.disabled = !ready;
    endpointButton.disabled = !ready || !locked || !point || box !== null;
    boxReadout.textContent = box ?
      `PENDING BOX (not recorded): ${box.xmin},${box.ymin},${box.xmax},${box.ymax} inclusive` : first ?
      `PENDING FIRST ENDPOINT: ${first.x},${first.y}; choose the lower-right endpoint.` :
      boxMode ? "BOX MODE: choose the upper-left endpoint, then lower-right." : "No pending box.";
    if (!ready) { readout.textContent = "Coordinates unavailable: image not ready."; return; }
    if (!point) { readout.textContent = "No point — hover or click to lock; nothing is prefilled."; return; }
    const asset = assets[key];
    const center = core.pixelCenter(point, image.getBoundingClientRect(), asset.width, asset.height);
    if (!center) { readout.textContent = "Coordinates unavailable: display rectangle invalid."; return; }
    const base = stage.getBoundingClientRect();
    marker.style.left = `${center.clientX - base.left}px`;
    marker.style.top = `${center.clientY - base.top}px`;
    marker.hidden = false;
    readout.textContent = `${locked ? "LOCKED" : "HOVER"}: x ${point.x}, y ${point.y} (native pixel cell; not a recorded box)`;
  }
  function clearPoint() { point = null; locked = false; showPoint(); }
  function clearBox() { first = null; box = null; boxMode = false; showPoint(); }
  function resetEntry() {
    point = null; locked = false; first = null; box = null; boxMode = false;
    inspected.checked = false; judgment.value = "notinspected"; note.value = "";
    say(""); showPoint();
  }
  function showDraft() {
    byId("response-text").value = formatResponses(rows, assets, frameOrder, sourceHash, protocolHash);
    const count = frameOrder.filter((ordinal) => rows.has(String(ordinal))).length;
    byId("draft-count").textContent = `${count} / ${frameOrder.length} historical session-draft rows; ` +
      `${rows.has("control") ? "one" : "no"} separate synthetic practice row. Not saved or accepted.`;
  }
  function sizeImage() {
    if (disposed) return;
    const asset = assets[key];
    const width = zoom === "fit" ? Math.max(1, Math.min(asset.width,
      viewport.clientWidth, viewport.clientHeight * asset.width / asset.height)) : asset.width * Number(zoom);
    stage.style.width = `${width}px`;
    if (!locked) point = null;
    showPoint();
  }
  function loadFrame() {
    const token = ++generation;
    ready = false;
    resetEntry();
    image.hidden = true;
    const selected = selector.value;
    if (!Object.hasOwn(assets, selected) ||
        (selected !== "control" && !frameOrder.some((ordinal) => String(ordinal) === selected))) {
      loadStatus.dataset.error = "true";
      loadStatus.textContent = "Unknown image rejected; coordinates and recording disabled.";
      return;
    }
    key = selected;
    const asset = assets[key];
    loadStatus.dataset.error = "false";
    loadStatus.textContent = "Loading full image; coordinates and recording disabled…";
    byId("kind").textContent = asset.synthetic ?
      "SYNTHETIC CONTROL — coordinate bookkeeping practice only; never historical evidence" :
      "Historical access-copy derivative — awaiting actual human inspection";
    byId("index").textContent = asset.synthetic ? "Not applicable — synthetic" : `${asset.ordinal} (zero-based decoded source order)`;
    byId("dimensions").textContent = `${asset.width} × ${asset.height}; ${asset.mode}; ${asset.bytes} bytes`;
    const nullable = (value) => value === null ? "null (missing)" : String(value);
    byId("clock").textContent = asset.synthetic ? "Not applicable — synthetic" :
      `Stored PTS: ${nullable(asset.stored_pts)}; stored exact seconds: ${nullable(asset.stored_pts_seconds_exact)}; ` +
      `best-effort timestamp: ${nullable(asset.best_effort_timestamp)}; best-effort exact seconds: ${nullable(asset.best_effort_seconds_exact)}. Not a capture clock.`;
    byId("hash").textContent = asset.sha256;
    byId("source-hash").textContent = asset.synthetic ? "Not applicable — synthetic fixture" : sourceHash;
    byId("protocol-hash").textContent = protocolHash;
    const next = new ImageClass();
    next.id = "native-image";
    next.alt = asset.synthetic ? "Complete synthetic coordinate-control shapes" : `Complete native DistantView frame ${asset.ordinal}`;
    next.draggable = false;
    next.hidden = true;
    let failed = false;
    const reject = (message) => {
      failed = true; ready = false; next.hidden = true; resetEntry();
      loadStatus.dataset.error = "true";
      loadStatus.textContent = message;
    };
    next.onload = () => {
      if (disposed || token !== generation || failed) return;
      if (next.naturalWidth !== asset.width || next.naturalHeight !== asset.height) {
        reject("Image rejected: native dimensions do not match the pinned packet. Select an image to retry.");
        return;
      }
      ready = true; next.hidden = false;
      loadStatus.textContent = `Full image loaded (${asset.width} × ${asset.height}). Nothing is recorded until you explicitly record a draft row.`;
      sizeImage();
    };
    next.onerror = () => {
      if (disposed || token !== generation) return;
      reject("Image load failed. Coordinates and recording disabled; select an image to retry.");
    };
    image.replaceWith(next);
    image = next;
    viewport.scrollLeft = 0; viewport.scrollTop = 0;
    sizeImage();
    next.src = asset.url; // Only URLs supplied by the fixed generated asset module.
  }
  function pointer(event) {
    const asset = assets[key];
    return ready ? core.pointerToPixel(event.clientX, event.clientY,
      image.getBoundingClientRect(), asset.width, asset.height) : null;
  }
  function useEndpoint() {
    if (!ready || !locked || !point || box) return;
    if (!first) { first = { ...point }; say("First endpoint pending; choose the lower-right endpoint."); }
    else {
      try {
        box = validateBox({ xmin: first.x, ymin: first.y, xmax: point.x, ymax: point.y },
          assets[key].width, assets[key].height);
        boxMode = false;
        say("Box pending, not recorded. Choose a status, confirm inspection and explain your judgment.");
      } catch (error) { say(error.message, true); }
    }
    showPoint();
  }
  listen(stage, "pointermove", (event) => {
    if (!ready || locked) return;
    point = pointer(event); showPoint();
  });
  listen(stage, "pointerleave", () => { if (!locked) clearPoint(); });
  listen(stage, "click", (event) => {
    const selected = pointer(event);
    if (!selected) return;
    point = selected; locked = true;
    viewport.focus({ preventScroll: true });
    if (boxMode) useEndpoint();
    showPoint();
  });
  listen(viewport, "keydown", (event) => {
    if (!ready || !locked) return;
    const moved = core.nudgePixel(point, event.key, assets[key].width, assets[key].height);
    if (!moved) return;
    event.preventDefault(); point = moved; showPoint();
  });
  listen(doc, "keydown", (event) => {
    if (event.key === "Escape") { event.preventDefault(); clearPoint(); }
  });
  listen(viewport, "scroll", () => { if (!locked) clearPoint(); else showPoint(); });
  listen(byId("clear-point"), "click", clearPoint);
  listen(byId("clear-box"), "click", clearBox);
  listen(startBoxButton, "click", () => {
    if (!ready) return;
    first = null; box = null; boxMode = true; point = null; locked = false;
    say("Box mode: click upper-left, then lower-right. No endpoint is prefilled."); showPoint();
  });
  listen(endpointButton, "click", useEndpoint);
  listen(recordButton, "click", () => {
    try {
      if (!ready) throw new Error("Image is not ready; no row recorded.");
      if (first && !box) throw new Error("Complete or clear the pending first endpoint before recording.");
      const row = validateResponse({ inspected: inspected.checked, status: judgment.value,
        box: box ? { ...box } : null, note: note.value }, assets[key]);
      rows.set(key, row); showDraft();
      say(`${assets[key].synthetic ? "Synthetic practice" : `Frame ${key}`} session-only draft row recorded in memory; not saved or accepted.`);
    } catch (error) { say(error.message, true); }
  });
  listen(byId("clear-row"), "click", () => {
    rows.delete(key); resetEntry(); showDraft();
    say("Current session draft row cleared; no previously sent reply was changed.");
  });
  listen(selector, "change", loadFrame);
  for (const button of zoomButtons) listen(button, "click", () => {
    if (!["fit", "1", "2"].includes(button.dataset.zoom)) return;
    zoom = button.dataset.zoom;
    for (const peer of zoomButtons) peer.setAttribute("aria-pressed", String(peer === button));
    sizeImage();
  });
  selector.replaceChildren();
  for (const value of ["control", ...frameOrder.map(String)]) {
    const option = doc.createElement("option");
    option.value = value;
    option.textContent = value === "control" ? "Synthetic control (default)" : `Frame ${value}`;
    selector.appendChild(option);
  }
  selector.value = "control";
  const observer = new ResizeClass(sizeImage);
  observer.observe(viewport);
  showDraft(); loadFrame();
  return { destroy() {
    disposed = true; ++generation; ready = false;
    image.onload = null; image.onerror = null;
    for (const remove of listeners) remove();
    observer.disconnect(); resetEntry();
  } };
}

if (typeof document !== "undefined") {
  Promise.all([import("./coordinate-core.mjs"), import("./assets.mjs")])
    .then(([core, packet]) => initializeReview({ document, Image, ResizeObserver,
      core, assets: packet.ASSETS, frameOrder: packet.FRAME_ORDER,
      sourceHash: packet.SOURCE_HASH, protocolHash: packet.PROTOCOL_HASH }))
    .catch(() => {
      const status = document.getElementById("load-status");
      status.dataset.error = "true";
      status.textContent = "Local packet failed to initialize. No inspection or response has been recorded.";
    });
}
