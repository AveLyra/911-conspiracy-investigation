// Synthetic coordinate bookkeeping only; no historical images/positions read.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';

const source = await readFile(new URL('../../comparator-r1-replication/coordinate.js', import.meta.url));
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
assert.equal(sha(source), '38cc0cd9b0947e05072ec8656c58e4fc4ca95d968bd1a903af26afe43db0b05b');
const prefix = source.subarray(0, 2524);
assert.equal(sha(prefix), '9cff4290fc41e27126b36402818b1ecb55057e003f819ecbe8cef53281d2e2c4');
const { pointerToPixel: hit, pixelCenter: center, nudgePixel: nudge } =
  await import(`data:text/javascript;base64,${prefix.toString('base64')}`);

for (const [width, height] of [[704, 480], [1280, 720]]) {
  for (const scale of [0.375, 1, 2]) {
    test(`${width}x${height} at ${scale}: every pixel-center round trip, fractional scrolled origin`, () => {
      const rect = { left: -317.25, top: -93.125, width: width * scale, height: height * scale };
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const expected = { x, y };
          const p = center(expected, rect, width, height);
          assert.deepEqual(hit(p.clientX, p.clientY, rect, width, height), expected);
        }
      }
      assert.deepEqual(hit(rect.left, rect.top, rect, width, height), { x: 0, y: 0 });
      assert.equal(hit(rect.left + rect.width, rect.top, rect, width, height), null);
      assert.equal(hit(rect.left, rect.top + rect.height, rect, width, height), null);
      assert.equal(hit(rect.left - 0.001, rect.top, rect, width, height), null);
      assert.equal(hit(rect.left, rect.top - 0.001, rect, width, height), null);
      assert.deepEqual(hit(rect.left + rect.width - 0.001, rect.top + rect.height - 0.001,
        rect, width, height), { x: width - 1, y: height - 1 });
      // Border/padding clicks outside this image-only rectangle must be excluded.
      assert.equal(hit(rect.left + rect.width + 1, rect.top + 1, rect, width, height), null);
    });
  }
  test(`${width}x${height}: interior floor boundary and keyboard clamp`, () => {
    const rect = { left: 31.25, top: 12.5, width, height };
    assert.deepEqual(hit(41.25, 32.5, rect, width, height), { x: 10, y: 20 });
    assert.deepEqual(hit(41.25 - 0.001, 32.5 - 0.001, rect, width, height), { x: 9, y: 19 });
    assert.deepEqual(nudge({ x: 0, y: 0 }, 'ArrowLeft', width, height), { x: 0, y: 0 });
    assert.deepEqual(nudge({ x: 0, y: 0 }, 'ArrowUp', width, height), { x: 0, y: 0 });
    assert.deepEqual(nudge({ x: width - 1, y: height - 1 }, 'ArrowRight', width, height),
      { x: width - 1, y: height - 1 });
    assert.deepEqual(nudge({ x: width - 1, y: height - 1 }, 'ArrowDown', width, height),
      { x: width - 1, y: height - 1 });
    assert.deepEqual(nudge({ x: 10, y: 20 }, 'ArrowRight', width, height), { x: 11, y: 20 });
    assert.deepEqual(nudge({ x: 10, y: 20 }, 'ArrowDown', width, height), { x: 10, y: 21 });
    assert.equal(nudge({ x: 10, y: 20 }, 'Escape', width, height), null);
  });
}

test('invalid inputs never become coordinates', () => {
  const rect = { left: 0, top: 0, width: 704, height: 480 };
  for (const [width, height] of [[0, 480], [704, -1], [704.5, 480], [NaN, 480], ['704', 480]]) {
    assert.equal(hit(1, 1, rect, width, height), null);
    assert.equal(center({ x: 0, y: 0 }, rect, width, height), null);
    assert.equal(nudge({ x: 0, y: 0 }, 'ArrowRight', width, height), null);
  }
  for (const bad of [null, {}, { ...rect, width: 0 }, { ...rect, top: Infinity },
    { ...rect, left: NaN }, { ...rect, height: -1 }]) {
    assert.equal(hit(1, 1, bad, 704, 480), null);
    assert.equal(center({ x: 0, y: 0 }, bad, 704, 480), null);
  }
  for (const p of [null, { x: -1, y: 0 }, { x: 704, y: 0 }, { x: 1.5, y: 0 }, { x: 0, y: 480 }]) {
    assert.equal(center(p, rect, 704, 480), null);
    assert.equal(nudge(p, 'ArrowRight', 704, 480), null);
  }
  assert.equal(hit(NaN, 1, rect, 704, 480), null);
  assert.equal(hit(1, Infinity, rect, 704, 480), null);
});
