import test from "node:test";
import assert from "node:assert/strict";
import {startDiagnostics, isControl, rectangle, LIMIT} from "./diagnostics.mjs";

function fixture() {
  class Element {
    constructor(id = "") {
      this.id = id; this.disabled = false; this.hidden = false;
      this.style = {}; this.children = []; this.textContent = ""; this.value = "";
      this.bounds = {x: 10.25, y: -4.5, left: 10.25, top: -4.5,
        right: 650.25, bottom: 355.5, width: 640, height: 360};
    }
    getBoundingClientRect() { return {...this.bounds}; }
    setAttribute(key, value) { this[key] = value; }
    appendChild(child) { this.children.push(child); }
    closest() { return this; }
  }
  const nodes = new Map(["native-image", "frame", "viewport", "marker", "readout",
    "box-readout", "inspected", "judgment", "note", "record-row", "clear-row",
    "response-text"].map(k => [k, new Element(k)]));
  const listeners = new Map(), timers = new Map();
  const doc = {body: new Element("body"), getElementById: id => nodes.get(id),
    createElement: () => new Element(),
    addEventListener(type, fn, capture) {
      assert.equal(capture, true);
      listeners.set(type, [...(listeners.get(type) || []), fn]);
    },
    removeEventListener(type, fn, capture) {
      assert.equal(capture, true);
      listeners.set(type, (listeners.get(type) || []).filter(x => x !== fn));
    }};
  let ticks = 0, timerId = 0, observe;
  const win = {location: {href: "http://127.0.0.1:1234/", origin: "http://127.0.0.1:1234"},
    innerWidth: 1200, innerHeight: 900, devicePixelRatio: 2,
    scrollX: 4, scrollY: 9, performance: {now: () => ++ticks},
    setTimeout(fn, delay) { assert.equal(delay, 0); timers.set(++timerId, fn); return timerId; },
    clearTimeout(id) { timers.delete(id); },
    MutationObserver: class { constructor(fn) { observe = fn; } observe() {} disconnect() {} }};
  Object.assign(nodes.get("native-image"), {src: "/control.png", complete: true,
    naturalWidth: 1280, naturalHeight: 720});
  Object.assign(nodes.get("viewport"), {scrollLeft: 21, scrollTop: 33});
  nodes.get("frame").value = "control";
  nodes.get("marker").hidden = true;
  const emit = (type, additions = {}) => {
    const event = {type, target: nodes.get("native-image"), clientX: 260.75, clientY: 85.25,
      isTrusted: false, pointerType: "mouse", pointerId: 2, timeStamp: 101.2,
      preventDefault() { this.prevented = true; },
      stopImmediatePropagation() { this.stopped = true; }, ...additions};
    for (const listener of [...(listeners.get(type) || [])]) {
      listener(event); if (event.stopped) break;
    }
    return event;
  };
  const flush = () => {
    for (const [id, fn] of [...timers]) { timers.delete(id); fn(); }
  };
  return {doc, win, nodes, emit, flush, timers, mutate: () => observe()};
}

test("capture is copied immediately; post-dispatch snapshot runs in separate task", () => {
  const f = fixture(), logger = startDiagnostics({document: f.doc, window: f.win});
  f.emit("click"); const row = logger.state.events[0];
  assert.equal(row.status, "pending"); assert.equal(row.after, null);
  assert.equal(row.event.isTrusted, false);
  assert.deepEqual(row.capture.pageScroll, [4, 9]);
  assert.deepEqual(row.capture.regionScroll, [21, 33]);
  assert.deepEqual(row.capture.viewport, [1200, 900]); assert.equal(row.capture.dpr, 2);
  f.nodes.get("readout").textContent = "LOCKED: x 500, y 179";
  f.nodes.get("native-image").bounds.top = 10;
  f.flush();
  assert.equal(row.capture.imageRect.top, -4.5);
  assert.equal(row.after.imageRect.top, 10);
  assert.equal(row.after.readout, "LOCKED: x 500, y 179");
  assert.equal(row.after.status, "completed"); assert.equal(row.status, "completed");
});

test("pointerdown/up/click remain separately ordered and bounded", () => {
  const f = fixture(), logger = startDiagnostics({document: f.doc, window: f.win});
  for (const type of ["pointerdown", "pointerup", "click"]) f.emit(type);
  assert.deepEqual(logger.state.events.map(x => x.event.type), ["pointerdown", "pointerup", "click"]);
  assert.deepEqual(logger.state.events.map(x => x.sequence), [1, 2, 3]);
  f.flush(); assert.equal(logger.state.completed, 3);
});

test("reserve cap applies before queued tasks; no replacement/discard", () => {
  const f = fixture(), logger = startDiagnostics({document: f.doc, window: f.win});
  for (let i = 0; i < 130; i++) f.emit("click", {clientX: i});
  assert.equal(logger.state.reserved, LIMIT); assert.equal(logger.state.events.length, LIMIT);
  assert.equal(logger.state.stopped, true); assert.equal(f.timers.size, LIMIT);
  assert.equal(logger.state.events[0].event.clientX, 0);
  assert.equal(logger.state.events[99].event.clientX, 99);
  f.flush(); assert.equal(logger.state.completed, LIMIT);
});

test("historical selection, route, missing/hidden/unready or wrong-sized image cannot log", () => {
  const changes = [
    f => f.nodes.get("frame").value = "274",
    f => f.nodes.get("native-image").src = "/frames/274.png",
    f => f.nodes.get("native-image").src = "http://other.test/control.png",
    f => f.nodes.get("native-image").src = "/control.png?query",
    f => f.nodes.get("native-image").src = "/control.png#fragment",
    f => f.nodes.get("native-image").naturalWidth = 704,
    f => f.nodes.get("native-image").naturalHeight = 480,
    f => f.nodes.get("native-image").hidden = true,
    f => f.nodes.get("native-image").complete = false,
    f => f.nodes.delete("native-image")
  ];
  for (const change of changes) {
    const f = fixture(), logger = startDiagnostics({document: f.doc, window: f.win});
    change(f); assert.equal(isControl(f.doc, f.win), false);
    f.emit("click"); assert.equal(logger.state.reserved, 0);
  }
});

test("non-control after dispatch is explicitly withheld, not historical logging", () => {
  const f = fixture(), logger = startDiagnostics({document: f.doc, window: f.win});
  f.emit("click"); f.nodes.get("native-image").src = "/frames/274.png"; f.flush();
  assert.deepEqual(logger.state.events[0].after, {status: "withheld_noncontrol"});
});

test("response/selection guards stop propagation and restore disabled controls", () => {
  const f = fixture(), logger = startDiagnostics({document: f.doc, window: f.win});
  for (const id of ["record-row", "clear-row", "inspected", "judgment", "note", "response-text", "frame"]) {
    assert.equal(f.nodes.get(id).disabled, true);
    const event = f.emit("click", {target: f.nodes.get(id)});
    assert.equal(event.prevented, true); assert.equal(event.stopped, true);
  }
  f.nodes.get("frame").value = "274";
  f.emit("change", {target: f.nodes.get("frame")});
  assert.equal(f.nodes.get("frame").value, "control");
  f.nodes.get("record-row").disabled = false; f.mutate();
  assert.equal(f.nodes.get("record-row").disabled, true);
  assert.equal(logger.state.events.length, 0);
});

test("destroy cancels pending tasks without inventing completed output", () => {
  const f = fixture(), logger = startDiagnostics({document: f.doc, window: f.win});
  f.emit("click"); logger.destroy(); f.flush(); f.emit("click");
  assert.equal(logger.state.events.length, 1);
  assert.equal(logger.state.events[0].status, "pending");
  assert.equal(logger.state.completed, 0);
});

test("nulls preserve unavailable pointer fields; rectangle retains fractional/negative origins", () => {
  const f = fixture(), logger = startDiagnostics({document: f.doc, window: f.win});
  f.emit("click", {pointerType: undefined, pointerId: undefined, clientX: NaN});
  const event = logger.state.events[0].event;
  assert.equal(event.pointerType, null); assert.equal(event.pointerId, null);
  assert.equal(event.clientX, null);
  assert.equal(rectangle(f.nodes.get("native-image")).top, -4.5);
});
