// Synthetic-control-only instrumentation. No storage, transport or clipboard.
export const LIMIT = 100;
const TYPES = ["pointerdown", "pointerup", "click"];
const BLOCKED = new Set(["frame", "inspected", "judgment", "note",
  "record-row", "clear-row", "response-text"]);
const finite = value => Number.isFinite(value) ? value : null;

export function rectangle(element) {
  const r = element.getBoundingClientRect();
  return Object.fromEntries(["x", "y", "left", "top", "right", "bottom", "width", "height"]
    .map(key => [key, finite(r[key])]));
}

export function isControl(doc, win) {
  const image = doc.getElementById("native-image");
  if (!image || doc.getElementById("frame")?.value !== "control" ||
      image.hidden || !image.complete || image.naturalWidth !== 1280 ||
      image.naturalHeight !== 720) return false;
  try {
    const source = new URL(image.currentSrc || image.src, win.location.href);
    return source.origin === win.location.origin && source.pathname === "/control.png" &&
      source.search === "" && source.hash === "";
  } catch { return false; }
}

function geometry(doc, win) {
  const image = doc.getElementById("native-image"), region = doc.getElementById("viewport");
  const visual = win.visualViewport;
  return {
    selected: doc.getElementById("frame").value,
    naturalWidth: image.naturalWidth, naturalHeight: image.naturalHeight,
    imageRect: rectangle(image),
    pageScroll: [finite(win.scrollX), finite(win.scrollY)],
    regionScroll: [finite(region.scrollLeft), finite(region.scrollTop)],
    viewport: [finite(win.innerWidth), finite(win.innerHeight)],
    visualViewport: visual ? Object.fromEntries(["width", "height", "offsetLeft", "offsetTop",
      "pageLeft", "pageTop", "scale"].map(k => [k, finite(visual[k])])) : null,
    dpr: finite(win.devicePixelRatio), performanceNow: finite(win.performance.now())
  };
}

export function startDiagnostics({document: doc, window: win}) {
  const state = {schema: "synthetic-pointer-diagnostic-v1",
    scope: "synthetic control only; not human or historical observations",
    limit: LIMIT, reserved: 0, completed: 0, stopped: false, events: []};
  const panel = doc.createElement("section"), heading = doc.createElement("h2");
  const status = doc.createElement("p"), output = doc.createElement("textarea");
  panel.id = "diagnostics-panel"; panel.className = "panel";
  panel.style.height = "390px"; panel.style.boxSizing = "border-box";
  heading.textContent = "Synthetic pointer diagnostic — no draft recording";
  status.id = "diagnostics-status";
  output.id = "diagnostics-json"; output.readOnly = true; output.spellcheck = false;
  output.setAttribute("aria-label", "Bounded synthetic diagnostic JSON");
  output.style.height = "275px"; output.style.resize = "none";
  for (const item of [heading, status, output]) panel.appendChild(item);
  doc.body.appendChild(panel);
  let destroyed = false;
  const timers = new Set();
  const publish = () => {
    status.textContent = state.stopped ?
      `CAP REACHED: ${state.reserved}/100 events; ${state.completed} completed. Logging stopped.` :
      `${state.reserved}/100 events; ${state.completed} completed; ${state.reserved - state.completed} pending.`;
    output.value = JSON.stringify(state, null, 2);
  };
  function lockControls() {
    for (const id of BLOCKED) {
      const element = doc.getElementById(id);
      if (element && !element.disabled) element.disabled = true;
    }
  }
  function guard(event) {
    // Capture prevents the unchanged controller's response/change listeners.
    const id = event.target?.closest?.("[id]")?.id || event.target?.id;
    if (!BLOCKED.has(id)) return;
    event.preventDefault(); event.stopImmediatePropagation();
    if (id === "frame") doc.getElementById("frame").value = "control";
  }
  function capture(event) {
    if (destroyed || state.stopped || !isControl(doc, win)) return;
    const row = {
      sequence: ++state.reserved, status: "pending",
      event: {type: event.type, isTrusted: event.isTrusted === true,
        pointerType: typeof event.pointerType === "string" ? event.pointerType : null,
        pointerId: finite(event.pointerId), clientX: finite(event.clientX),
        clientY: finite(event.clientY), timeStamp: finite(event.timeStamp),
        targetId: event.target?.id || null},
      capture: geometry(doc, win), after: null
    };
    state.events.push(row);
    if (state.reserved === LIMIT) {
      state.stopped = true;
      for (const type of TYPES) doc.removeEventListener(type, capture, true);
    }
    publish();
    // A separate task follows event dispatch. A microtask is insufficient:
    // browsers may checkpoint microtasks between event listeners.
    const timer = win.setTimeout(() => {
      timers.delete(timer);
      if (destroyed) return;
      row.after = isControl(doc, win) ? {
        status: "completed", ...geometry(doc, win),
        readout: doc.getElementById("readout").textContent,
        boxReadout: doc.getElementById("box-readout").textContent,
        marker: {hidden: doc.getElementById("marker").hidden,
          rect: rectangle(doc.getElementById("marker"))}
      } : {status: "withheld_noncontrol"};
      row.status = "completed"; ++state.completed; publish();
    }, 0);
    timers.add(timer);
  }
  lockControls();
  // The original controller updates disabled flags on pointer/load events.
  const observer = new win.MutationObserver(lockControls);
  observer.observe(doc.body, {subtree: true, attributes: true, attributeFilter: ["disabled"]});
  for (const type of ["click", "change", "keydown"]) doc.addEventListener(type, guard, true);
  for (const type of TYPES) doc.addEventListener(type, capture, true);
  publish();
  return {state, destroy() {
    destroyed = true; observer.disconnect();
    for (const type of ["click", "change", "keydown"]) doc.removeEventListener(type, guard, true);
    for (const type of TYPES) doc.removeEventListener(type, capture, true);
    for (const timer of timers) win.clearTimeout(timer);
    timers.clear();
  }};
}

if (typeof document !== "undefined") startDiagnostics({document, window});
