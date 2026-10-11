// Synthetic metadata and synthetic display rectangles only. No image is read,
// decoded or opened; none of these entries is a human or historical observation.
import assert from "node:assert/strict";
import { test } from "node:test";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { validateBox, validateResponse, formatResponses } from "./response.mjs";
import { initializeReview } from "./review.mjs";

const r1 = readFileSync(new URL("../../comparator-r1-replication/coordinate.js", import.meta.url));
assert.equal(createHash("sha256").update(r1).digest("hex"), "38cc0cd9b0947e05072ec8656c58e4fc4ca95d968bd1a903af26afe43db0b05b");
const prefix = r1.subarray(0, 2524);
assert.equal(createHash("sha256").update(prefix).digest("hex"), "9cff4290fc41e27126b36402818b1ecb55057e003f819ecbe8cef53281d2e2c4");
const core = await import(`data:text/javascript;base64,${prefix.toString("base64")}`);
const meta = (ordinal, synthetic, width, height) => ({
  ordinal, synthetic, width, height, url: synthetic ? "/synthetic-control.png" : `/fixture-${ordinal}.png`,
  mode: synthetic ? "RGB" : "L", bytes: 123, sha256: "a".repeat(64),
  stored_pts: null, best_effort_timestamp: 17,
  stored_pts_seconds_exact: null, best_effort_seconds_exact: "17/30",
});
// Ordinals 10/20 are arbitrary synthetic metadata fixtures, not selected source ordinals.
const assets = { control: meta(null, true, 1280, 720),
  "10": meta(10, false, 704, 480), "20": meta(20, false, 704, 480) };
const box = { xmin: 2, ymin: 3, xmax: 5, ymax: 8 };
const entered = (status = "localizable", patch = {}) => ({
  inspected: true, status, box: status === "localizable" ? { ...box } : null,
  note: "Synthetic fixture only — adjoining contours or a stated limitation.", ...patch,
});
const formatted = (rows = new Map(), source = assets) =>
  JSON.parse(formatResponses(rows, source, [10, 20], "b".repeat(64), "c".repeat(64)));

test("ordered inclusive boxes accept a cell and full bounds without adding a center", () => {
  for (const b of [box, { xmin: 0, ymin: 0, xmax: 0, ymax: 0 },
    { xmin: 0, ymin: 0, xmax: 703, ymax: 479 }]) {
    const got = validateBox(b, 704, 480);
    assert.deepEqual(got, b); assert.notEqual(got, b);
    assert.equal(Object.hasOwn(got, "center"), false);
  }
});
test("box rejects reversed endpoints independently on each axis", () => {
  assert.throws(() => validateBox({ ...box, xmin: 6 }, 704, 480), /Reversed/);
  assert.throws(() => validateBox({ ...box, ymin: 9 }, 704, 480), /Reversed/);
});
test("box rejects absent, partial, extra, noninteger and out-of-bounds data", () => {
  for (const b of [null, undefined, {}, [], { xmin: 1, ymin: 2 }, { ...box, center: 4 },
    ...[true, "2", 2.5, NaN, Infinity].map((xmin) => ({ ...box, xmin })),
    { ...box, xmin: -1 }, { ...box, ymin: -1 }, { ...box, xmax: 704 }, { ...box, ymax: 480 }]) {
    assert.throws(() => validateBox(b, 704, 480));
  }
});
test("invalid dimensions are rejected by box validation", () => {
  for (const value of [0, -1, true, "704", Infinity, NaN, 1.5]) {
    assert.throws(() => validateBox(box, value, 480));
    assert.throws(() => validateBox(box, 704, value));
  }
});
test("localizable requires explicit true inspection, a full box and explanatory note", () => {
  assert.deepEqual(validateResponse(entered(), assets[10]), entered());
  for (const value of [false, undefined, null, 1, "true", {}, []]) {
    assert.throws(() => validateResponse(entered("localizable", { inspected: value }), assets[10]), /confirmation/);
  }
  for (const value of [null, undefined, {}, { xmin: 1 }]) {
    assert.throws(() => validateResponse(entered("localizable", { box: value }), assets[10]));
  }
});
test("every entered status requires a note; no status defaults to acceptance", () => {
  for (const status of ["localizable", "ambiguous", "obscured", "notlocated", "outside"]) {
    for (const note of ["", "   ", null, 17, undefined]) {
      assert.throws(() => validateResponse(entered(status, { note }), assets[10]), /note/);
    }
    assert.equal(validateResponse(entered(status), assets[10]).status, status);
  }
  for (const status of ["notinspected", "accepted", "", undefined, "V"]) {
    assert.throws(() => validateResponse(entered("localizable", { status }), assets[10]));
  }
});
test("ambiguous permits explicit null or a valid box, never partial or omitted box", () => {
  assert.equal(validateResponse(entered("ambiguous"), assets[10]).box, null);
  assert.deepEqual(validateResponse(entered("ambiguous", { box }), assets[10]).box, box);
  for (const value of [undefined, {}, { xmin: 0 }]) {
    assert.throws(() => validateResponse(entered("ambiguous", { box: value }), assets[10]));
  }
});
test("obscured, notlocated and outside prohibit all boxes", () => {
  for (const status of ["obscured", "notlocated", "outside"]) {
    assert.equal(validateResponse(entered(status), assets[10]).box, null);
    assert.throws(() => validateResponse(entered(status, { box }), assets[10]), /null box/);
  }
});
test("extra forged identity or acceptance fields and missing row keys are rejected", () => {
  for (const key of ["human", "accepted", "synthetic", "ordinal", "source_sha256"]) {
    assert.throws(() => validateResponse({ ...entered(), [key]: true }, assets[10]));
  }
  const partial = entered(); delete partial.inspected;
  assert.throws(() => validateResponse(partial, assets[10]));
});
test("empty session formats all required rows as uninspected with no answer", () => {
  const got = formatted();
  assert.deepEqual(got.historical_responses.map((r) => r.ordinal), [10, 20]);
  for (const row of got.historical_responses) {
    assert.equal(row.inspected, false); assert.equal(row.status, "notinspected");
    assert.equal(row.box, null); assert.equal(row.note, null);
  }
  assert.equal(got.synthetic_control_response, null);
  assert.match(got.state, /not saved/i); assert.match(got.human_identity, /Not authenticated/);
});
test("synthetic practice remains separate and does not fill historical rows", () => {
  const got = formatted(new Map([["control", entered()]]));
  assert.equal(got.synthetic_control_response.synthetic, true);
  assert.equal(got.synthetic_control_response.ordinal, null);
  assert.ok(got.historical_responses.every((r) => !r.inspected && r.box === null));
});
test("metadata retains independent nulls and exact strings without clock substitution", () => {
  const got = formatted(new Map([["10", entered("notlocated")]])).historical_responses[0];
  assert.equal(got.stored_pts, null); assert.equal(got.best_effort_timestamp, 17);
  assert.equal(got.stored_pts_seconds_exact, null); assert.equal(got.best_effort_seconds_exact, "17/30");
  assert.equal(got.synthetic, false); assert.equal(got.ordinal, 10);
});
test("formatter rejects malformed rows, unknown keys, duplicate order and kind spoofing", () => {
  assert.throws(() => formatted(new Map([["10", entered("ambiguous", { inspected: "true" })]])));
  assert.throws(() => formatted(new Map([["99", entered()]])));
  assert.throws(() => formatted({}));
  assert.throws(() => formatResponses(new Map(), assets, [10, 10], "x", "y"));
  assert.throws(() => formatted(new Map(), { ...assets, "10": { ...assets[10], synthetic: true } }));
  assert.throws(() => formatted(new Map(), { ...assets, "10": { ...assets[10], ordinal: 20 } }));
});
test("validation and formatting do not mutate caller boxes or manufacture acceptance", () => {
  const row = entered(); const original = JSON.stringify(row);
  const valid = validateResponse(row, assets[10]); valid.box.xmin = 1;
  const got = formatted(new Map([["10", row]]));
  assert.equal(JSON.stringify(row), original);
  assert.equal(Object.hasOwn(got.historical_responses[0], "accepted"), false);
});

for (const [width, height] of [[704, 480], [1280, 720]]) {
  test(`exact reused helpers: ${width}×${height}, fit/100%/200%, scroll/offset/borders/centers`, () => {
    for (const scale of [.4375, 1, 2]) {
      const rect = { left: -117.25, top: 23.375, width: width * scale, height: height * scale };
      for (const point of [{ x: 0, y: 0 }, { x: width - 1, y: height - 1 }, { x: 16, y: 29 }]) {
        const center = core.pixelCenter(point, rect, width, height);
        assert.deepEqual(core.pointerToPixel(center.clientX, center.clientY, rect, width, height), point);
      }
      assert.deepEqual(core.pointerToPixel(rect.left, rect.top, rect, width, height), { x: 0, y: 0 });
      assert.equal(core.pointerToPixel(rect.left + rect.width, rect.top, rect, width, height), null);
      assert.equal(core.pointerToPixel(rect.left, rect.top + rect.height, rect, width, height), null);
      assert.equal(core.pointerToPixel(rect.left - .01, rect.top, rect, width, height), null);
      assert.equal(core.pointerToPixel(rect.left, rect.top - .01, rect, width, height), null);
    }
    assert.deepEqual(core.nudgePixel({ x: 16, y: 29 }, "ArrowRight", width, height), { x: 17, y: 29 });
    assert.deepEqual(core.nudgePixel({ x: 0, y: 0 }, "ArrowLeft", width, height), { x: 0, y: 0 });
  });
}

// Minimal event/geometry fixture, not a browser or human. Real browser QA remains separate.
class Element {
  constructor(id = "") {
    this.id = id; this.listeners = new Map(); this.children = []; this.dataset = {}; this.style = {};
    this.value = ""; this.checked = false; this.hidden = false; this.disabled = false; this.textContent = "";
    this.clientWidth = 640; this.clientHeight = 360;
    this.rect = { left: 10.25, top: 20.375, width: 640, height: 360 };
  }
  addEventListener(name, fn) { if (!this.listeners.has(name)) this.listeners.set(name, new Set()); this.listeners.get(name).add(fn); }
  removeEventListener(name, fn) { this.listeners.get(name)?.delete(fn); }
  fire(name, fields = {}) { const event = { preventDefault() { this.prevented = true; }, ...fields }; for (const fn of this.listeners.get(name) || []) fn(event); return event; }
  getBoundingClientRect() { return this.rect; }
  focus() { this.focused = true; }
  setAttribute(name, value) { this[name] = value; }
  appendChild(node) { this.children.push(node); }
  replaceChildren() { this.children = []; }
  replaceWith(next) { this.replacement = next; }
}
function fixture() {
  const ids = ["viewport", "stage", "marker", "frame", "load-status", "readout", "box-readout",
    "inspected", "judgment", "note", "feedback", "record-row", "start-box", "use-endpoint", "native-image",
    "response-text", "draft-count", "kind", "index", "dimensions", "clock", "hash", "source-hash",
    "protocol-hash", "clear-point", "clear-box", "clear-row"];
  const elements = Object.fromEntries(ids.map((id) => [id, new Element(id)]));
  const zooms = ["fit", "1", "2"].map((value) => { const e = new Element(); e.dataset.zoom = value; return e; });
  const doc = new Element();
  doc.getElementById = (id) => elements[id]; doc.querySelectorAll = () => zooms;
  doc.createElement = () => new Element();
  const images = [], observers = [];
  class Image extends Element { constructor() { super(); images.push(this); } }
  class ResizeObserver {
    constructor(callback) { this.callback = callback; observers.push(this); }
    observe() {} disconnect() { this.disconnected = true; }
  }
  const controller = initializeReview({ document: doc, Image, ResizeObserver, assets, frameOrder: [10, 20], core,
    sourceHash: "b".repeat(64), protocolHash: "c".repeat(64) });
  const load = (width = 1280, height = 720) => {
    const image = images.at(-1); image.naturalWidth = width; image.naturalHeight = height; image.onload(); return image;
  };
  const change = (key) => { elements.frame.value = key; elements.frame.fire("change"); };
  const click = (x, y) => {
    const asset = assets[elements.frame.value];
    const p = core.pixelCenter({ x, y }, images.at(-1).rect, asset.width, asset.height);
    elements.stage.fire("click", { clientX: p.clientX, clientY: p.clientY });
  };
  const draft = () => JSON.parse(elements["response-text"].value);
  const record = (status) => {
    elements.inspected.checked = true; elements.judgment.value = status;
    elements.note.value = "Synthetic UI fixture only."; elements["record-row"].fire("click");
  };
  return { e: elements, doc, images, observers, zooms, controller, load, change, click, draft, record };
}

test("UI defaults to the synthetic control, loading disables actions, no answer is manufactured", () => {
  const f = fixture();
  assert.equal(f.images.length, 1); assert.equal(f.images[0].src, "/synthetic-control.png");
  assert.equal(f.e.frame.value, "control"); assert.equal(f.e.inspected.checked, false);
  assert.equal(f.e.judgment.value, "notinspected"); assert.equal(f.e["record-row"].disabled, true);
  f.record("ambiguous"); assert.equal(f.draft().synthetic_control_response, null);
  f.load(); assert.equal(f.e["record-row"].disabled, false); assert.equal(f.e.marker.hidden, true);
  f.controller.destroy();
});
test("hover, lock, one-pixel keyboard nudge, clear, scroll and resize remain distinct", () => {
  const f = fixture(); const image = f.load();
  const c = core.pixelCenter({ x: 30, y: 40 }, image.rect, 1280, 720);
  f.e.stage.fire("pointermove", { clientX: c.clientX, clientY: c.clientY });
  assert.match(f.e.readout.textContent, /HOVER: x 30, y 40/);
  f.e.viewport.fire("scroll"); assert.equal(f.e.marker.hidden, true);
  f.click(30, 40); assert.match(f.e.readout.textContent, /LOCKED: x 30, y 40/);
  assert.equal(f.e.viewport.fire("keydown", { key: "ArrowRight" }).prevented, true);
  assert.match(f.e.readout.textContent, /LOCKED: x 31, y 40/);
  for (const button of f.zooms) button.fire("click");
  assert.equal(f.e.stage.style.width, "2560px");
  f.observers[0].callback(); assert.match(f.e.readout.textContent, /LOCKED: x 31/);
  f.doc.fire("keydown", { key: "Escape" }); assert.equal(f.e.marker.hidden, true);
  f.controller.destroy();
});
test("two clicks create a pending ordered box only; explicit confirmation/note records synthetic practice", () => {
  const f = fixture(); f.load(); f.e["start-box"].fire("click");
  f.click(2, 3); assert.match(f.e["box-readout"].textContent, /FIRST ENDPOINT/);
  f.click(5, 8); assert.match(f.e["box-readout"].textContent, /PENDING BOX.*2,3,5,8/);
  assert.equal(f.draft().synthetic_control_response, null);
  f.e.judgment.value = "localizable"; f.e["record-row"].fire("click");
  assert.match(f.e.feedback.textContent, /confirmation/);
  f.record("localizable");
  assert.deepEqual(f.draft().synthetic_control_response.box, box);
  assert.ok(f.draft().historical_responses.every((r) => !r.inspected));
  f.controller.destroy();
});
test("reversed second endpoint remains pending and is never silently swapped or recorded", () => {
  const f = fixture(); f.load(); f.e["start-box"].fire("click");
  f.click(10, 10); f.click(9, 11);
  assert.match(f.e.feedback.textContent, /Reversed/);
  assert.match(f.e["box-readout"].textContent, /FIRST ENDPOINT/);
  f.record("ambiguous"); assert.match(f.e.feedback.textContent, /Complete or clear/);
  assert.equal(f.draft().synthetic_control_response, null);
  f.e["clear-box"].fire("click"); f.record("ambiguous");
  assert.equal(f.draft().synthetic_control_response.box, null);
  f.controller.destroy();
});
test("locked keyboard-refined points can supply both endpoints without auto-centering", () => {
  const f = fixture(); f.load(); f.click(2, 3); f.e["use-endpoint"].fire("click");
  f.e.viewport.fire("keydown", { key: "ArrowRight" });
  f.e.viewport.fire("keydown", { key: "ArrowDown" });
  f.e["use-endpoint"].fire("click"); f.record("localizable");
  assert.deepEqual(f.draft().synthetic_control_response.box, { xmin: 2, ymin: 3, xmax: 3, ymax: 4 });
  f.controller.destroy();
});
test("frame change clears all transient input but retains recorded rows without prefill", () => {
  const f = fixture(); f.load(); f.record("ambiguous"); f.click(12, 18);
  f.change("10");
  assert.equal(f.e.inspected.checked, false); assert.equal(f.e.judgment.value, "notinspected");
  assert.equal(f.e.note.value, ""); assert.equal(f.e.marker.hidden, true);
  assert.match(f.e["box-readout"].textContent, /No pending box/);
  assert.equal(f.e["record-row"].disabled, true);
  assert.equal(f.draft().synthetic_control_response.status, "ambiguous");
  f.load(704, 480); f.record("notlocated");
  assert.equal(f.draft().historical_responses[0].status, "notlocated");
  f.change("control"); f.load();
  assert.equal(f.e.judgment.value, "notinspected"); assert.equal(f.e.note.value, "");
  f.e["clear-row"].fire("click");
  assert.equal(f.draft().synthetic_control_response, null);
  assert.equal(f.draft().historical_responses[0].status, "notlocated");
  f.controller.destroy();
});
test("stale image events cannot unlock a replacement; bad dimensions and errors clear entry state", () => {
  const f = fixture(); const old = f.images[0]; f.change("10");
  old.naturalWidth = 1280; old.naturalHeight = 720; old.onload();
  assert.equal(f.e["record-row"].disabled, true);
  f.load(1280, 720); assert.match(f.e["load-status"].textContent, /rejected/);
  f.change("10"); const current = f.load(704, 480); f.click(10, 12);
  f.e.inspected.checked = true; f.e.judgment.value = "ambiguous"; f.e.note.value = "pending";
  current.onerror();
  assert.equal(f.e["record-row"].disabled, true); assert.equal(f.e.marker.hidden, true);
  assert.equal(f.e.inspected.checked, false); assert.equal(f.e.note.value, "");
  current.onload(); assert.equal(f.e["record-row"].disabled, true);
  f.controller.destroy();
});
test("invalid frame selection, excluded image edges, and disposed UI do not record or expose positions", () => {
  const f = fixture(); const image = f.load();
  f.e.stage.fire("click", { clientX: image.rect.left + image.rect.width, clientY: image.rect.top });
  assert.equal(f.e.marker.hidden, true);
  f.change("99"); assert.equal(f.images.length, 1); assert.equal(f.e["record-row"].disabled, true);
  assert.match(f.e["load-status"].textContent, /Unknown image/);
  f.controller.destroy(); assert.equal(f.observers[0].disconnected, true);
  f.e["record-row"].fire("click"); assert.equal(f.draft().synthetic_control_response, null);
});
test("HTML keeps image pixels free of border/padding and has no historical previews or export affordance", () => {
  const html = readFileSync(new URL("./review.html", import.meta.url), "utf8");
  assert.match(html, /#native-image \{[^}]*padding: 0; border: 0;/);
  assert.equal((html.match(/<img\b/g) || []).length, 1);
  assert.doesNotMatch(html, /<img[^>]*\bsrc=/);
  const js = readFileSync(new URL("./review.mjs", import.meta.url), "utf8");
  assert.doesNotMatch(js, /localStorage|sessionStorage|indexedDB|navigator\.clipboard|fetch\(|XMLHttpRequest|WebSocket|sendBeacon|createObjectURL/);
});
