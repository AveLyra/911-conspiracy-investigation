"use strict";
// Synthetic display geometry only. No historical files or image pixels read.
const assert = require("node:assert/strict");
const { readFileSync } = require("node:fs");
const { join } = require("node:path");
const { test } = require("node:test");

const code = readFileSync(join(__dirname, "coordinate.js"), "utf8");
const moduleReady = import(`data:text/javascript;base64,${Buffer.from(code).toString("base64")}`);
const W = 1280, H = 720;
const rect = (left, top, width, height) => ({ left, top, width, height });

test("floor mapping at 100%, including independent fractional x/y cells", async () => {
  const { pointerToPixel: map } = await moduleReady;
  assert.deepEqual(map(10.75, 20.99, rect(0, 0, W, H), W, H), { x: 10, y: 20 });
  assert.deepEqual(map(42, 57, rect(30, 40, W, H), W, H), { x: 12, y: 17 });
});

test("fit-to-width and fit-to-height geometries", async () => {
  const { pointerToPixel: map } = await moduleReady;
  assert.deepEqual(map(260.2, 200.4, rect(10, 20, 640, 360), W, H), { x: 500, y: 360 });
  assert.deepEqual(map(180, 110, rect(20, 20, 320, 180), W, H), { x: 640, y: 360 });
});

test("200% uses two CSS pixels per native pixel", async () => {
  const { pointerToPixel: map } = await moduleReady;
  assert.deepEqual(map(31.9, 63.9, rect(10, 20, W * 2, H * 2), W, H), { x: 10, y: 21 });
});

test("fractional offsets and scales", async () => {
  const { pointerToPixel: map } = await moduleReady;
  assert.deepEqual(map(21.375, 31.125, rect(10.125, 20.375, 960, 540), W, H), { x: 15, y: 14 });
});

test("scrolling and negative image rectangle origins require no extra scroll addition", async () => {
  const { pointerToPixel: map } = await moduleReady;
  assert.deepEqual(map(20.5, 30.5, rect(-500, -200, W, H), W, H), { x: 520, y: 230 });
  assert.deepEqual(map(20.5, 30.5, rect(-500, -200, W * 2, H * 2), W, H), { x: 260, y: 115 });
});

test("upper/left included, right/bottom excluded, last interior pixel retained", async () => {
  const { pointerToPixel: map } = await moduleReady;
  const area = rect(10, 20, 640, 360);
  assert.deepEqual(map(10, 20, area, W, H), { x: 0, y: 0 });
  assert.deepEqual(map(649.999, 379.999, area, W, H), { x: 1279, y: 719 });
  for (const [x, y] of [[650, 20], [10, 380], [9.999, 20], [10, 19.999], [-1, -1], [1000, 1000]]) {
    assert.equal(map(x, y, area, W, H), null);
  }
});

test("invalid native dimensions and malformed rectangles are rejected", async () => {
  const { pointerToPixel: map, pixelCenter, nudgePixel } = await moduleReady;
  for (const bad of [0, -1, 1.5, NaN, Infinity, true, "1280", undefined]) {
    assert.equal(map(1, 1, rect(0, 0, W, H), bad, H), null);
    assert.equal(map(1, 1, rect(0, 0, W, H), W, bad), null);
    assert.equal(pixelCenter({ x: 0, y: 0 }, rect(0, 0, W, H), bad, H), null);
    assert.equal(nudgePixel({ x: 0, y: 0 }, "ArrowRight", W, bad), null);
  }
  for (const bad of [null, {}, rect(NaN, 0, W, H), rect(0, Infinity, W, H),
    rect(0, 0, 0, H), rect(0, 0, W, -1), rect(0, 0, true, H),
    rect(Number.MAX_VALUE, 0, Number.MAX_VALUE, H)]) {
    assert.equal(map(1, 1, bad, W, H), null);
    assert.equal(pixelCenter({ x: 0, y: 0 }, bad, W, H), null);
  }
  for (const value of [NaN, Infinity, -Infinity, true, "1", undefined]) {
    assert.equal(map(value, 1, rect(0, 0, W, H), W, H), null);
    assert.equal(map(1, value, rect(0, 0, W, H), W, H), null);
  }
});

test("marker centers at pixel plus one half and round-trips across fit/1x/2x/scroll", async () => {
  const { pointerToPixel: map, pixelCenter } = await moduleReady;
  assert.deepEqual(pixelCenter({ x: 0, y: 0 }, rect(0, 0, W, H), W, H), { clientX: 0.5, clientY: 0.5 });
  assert.deepEqual(pixelCenter({ x: 1279, y: 719 }, rect(10, 20, 2560, 1440), W, H), { clientX: 2569, clientY: 1459 });
  for (const area of [rect(0, 0, W, H), rect(10.125, 20.375, 640, 360),
    rect(-1200.25, -900.5, 2560, 1440), rect(2.7, 19.3, 853.2, 479.925)]) {
    for (const point of [{ x: 0, y: 0 }, { x: 1279, y: 719 }, { x: 581, y: 140 }, { x: 300, y: 600 }]) {
      const center = pixelCenter(point, area, W, H);
      assert.deepEqual(map(center.clientX, center.clientY, area, W, H), point);
    }
  }
});

test("nudging moves exactly one native pixel regardless of display scale", async () => {
  const { nudgePixel: nudge } = await moduleReady;
  const start = { x: 200, y: 300 };
  assert.deepEqual(nudge(start, "ArrowLeft", W, H), { x: 199, y: 300 });
  assert.deepEqual(nudge(start, "ArrowRight", W, H), { x: 201, y: 300 });
  assert.deepEqual(nudge(start, "ArrowUp", W, H), { x: 200, y: 299 });
  assert.deepEqual(nudge(start, "ArrowDown", W, H), { x: 200, y: 301 });
  assert.deepEqual(start, { x: 200, y: 300 });
});

test("nudge clamps at all edges, and rejects invalid pixels and keys", async () => {
  const { nudgePixel: nudge, pixelCenter } = await moduleReady;
  assert.deepEqual(nudge({ x: 0, y: 0 }, "ArrowLeft", W, H), { x: 0, y: 0 });
  assert.deepEqual(nudge({ x: 0, y: 0 }, "ArrowUp", W, H), { x: 0, y: 0 });
  assert.deepEqual(nudge({ x: 1279, y: 719 }, "ArrowRight", W, H), { x: 1279, y: 719 });
  assert.deepEqual(nudge({ x: 1279, y: 719 }, "ArrowDown", W, H), { x: 1279, y: 719 });
  for (const bad of [null, {}, { x: -1, y: 0 }, { x: 1280, y: 0 }, { x: 0, y: 720 },
    { x: 0.5, y: 0 }, { x: true, y: 0 }, { x: 0, y: NaN }]) {
    assert.equal(nudge(bad, "ArrowRight", W, H), null);
    assert.equal(pixelCenter(bad, rect(0, 0, W, H), W, H), null);
  }
  for (const key of ["Escape", "PageDown", "toString", "", null]) {
    assert.equal(nudge({ x: 1, y: 1 }, key, W, H), null);
  }
});
