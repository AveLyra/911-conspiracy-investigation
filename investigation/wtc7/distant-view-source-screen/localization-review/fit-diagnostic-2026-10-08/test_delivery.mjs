// Constructed software fixtures only. No browser events, images or observations.
import test from 'node:test';
import assert from 'node:assert/strict';
import { boundaryOracle, rectangle, SCHEDULE, verifyCases, validateManifest,
  readPinnedInputs, verifyPin, sha256 } from './verify_delivery.mjs';

const { manifest } = readPinnedInputs();
const clone = value => structuredClone(value);
const rect = (left, top, width, height) => ({ left, top, width, height,
  right: left + width, bottom: top + height, x: left, y: top });
const readout = (x, y) => `LOCKED: x ${x}, y ${y} (native pixel cell; not a recorded box)`;
function draft() {
  return { packet: 'DistantView six-frame human localization feasibility pilot',
    state: 'Session-only draft; not saved, submitted, verified or accepted',
    human_identity: 'Not authenticated by this interface; a checkbox is not identity proof',
    source_sha256: manifest.source_sha256, protocol_sha256: manifest.protocol_sha256,
    coordinate_convention: 'Zero-based native pixel cells; inclusive xmin,ymin,xmax,ymax; no inferred center',
    timestamp_limit: 'Stored and best-effort fields are nullable metadata, not an adopted capture clock',
    historical_responses: manifest.frame_order.map(ordinal => {
      const a = manifest.assets[String(ordinal)];
      return { ordinal, synthetic: false, image_sha256: a.sha256, width: a.width, height: a.height,
        mode: a.mode, stored_pts: a.stored_pts, best_effort_timestamp: a.best_effort_timestamp,
        stored_pts_seconds_exact: a.stored_pts_seconds_exact, best_effort_seconds_exact: a.best_effort_seconds_exact,
        inspected: false, status: 'notinspected', box: null, note: null };
    }), synthetic_control_response: null,
    limit: 'Subjective plausible-position boxes are not confidence intervals or proof of a fixed material point. Only an actual user reply can become a preserved human observation.' };
}
function fixture() {
  return { schema: 'synthetic-delivery-cases-v1', cases: SCHEDULE.map(([id, zoom, x, y], index) => {
    const scale = zoom === 'fit' ? .375 : Number(zoom), imageRect = rect(31.25, 12.6, 1280 * scale, 720 * scale);
    const geometry = { imageRect, pageScroll: [0, 0], regionScroll: [0, 0], viewport: [3000, 2000], dpr: 2 };
    const visualViewport = { width: 3000, height: 2000, offsetLeft: 0, offsetTop: 0, pageLeft: 0, pageTop: 0, scale: 1 };
    const requested = { x: imageRect.left + (x + .5) * scale, y: imageRect.top + (y + .5) * scale };
    const display = readout(x, y);
    return { id, zoom, intended: { x, y }, requested,
      before: { ...clone(geometry), viewportRect: rect(20, 0, 2800, 1600), naturalWidth: 1280, naturalHeight: 720,
        eventCount: 3 * index },
      events: ['pointerdown', 'pointerup', 'click'].map((type, n) => ({
        sequence: 3 * index + n + 1, status: 'completed',
        event: { type, isTrusted: true, pointerType: 'mouse', pointerId: 1,
          clientX: requested.x, clientY: requested.y, timeStamp: 100 * index + n, targetId: 'native-image' },
        capture: { selected: 'control', naturalWidth: 1280, naturalHeight: 720,
          ...clone(geometry), visualViewport: clone(visualViewport), performanceNow: 100 * index + n + .1 },
        after: { status: 'completed', selected: 'control', naturalWidth: 1280, naturalHeight: 720,
          readout: display, boxReadout: 'No pending box.',
          marker: { hidden: false, rect: rect(requested.x - 6, requested.y - 6, 12, 12) },
          ...clone(geometry), visualViewport: clone(visualViewport), performanceNow: 100 * index + n + .2 },
      })),
      after: { readout: display,
        draftCount: '0 / 6 historical session-draft rows; no separate synthetic practice row. Not saved or accepted.',
        draft: draft() },
    };
  }) };
}

test('independent boundary membership handles fractional and negative origins', () => {
  for (const r of [rect(31.25, 12.6, 480, 270), rect(-317.25, -93.125, 1280, 720)]) {
    assert.deepEqual(boundaryOracle({ x: r.left, y: r.top }, r), { x: 0, y: 0 });
    assert.equal(boundaryOracle({ x: r.right, y: r.top }, r), null);
    assert.equal(boundaryOracle({ x: r.left, y: r.bottom }, r), null);
    assert.equal(boundaryOracle({ x: r.left - .001, y: r.top }, r), null);
    assert.deepEqual(boundaryOracle({ x: r.right - .001, y: r.bottom - .001 }, r), { x: 1279, y: 719 });
  }
  const r = rect(-20, -30, 1280, 720);
  assert.deepEqual(boundaryOracle({ x: -10, y: -10 }, r), { x: 10, y: 20 });
  assert.deepEqual(boundaryOracle({ x: -10.001, y: -10.001 }, r), { x: 9, y: 19 });
});
test('constructed rounding counterexample is preserved, not treated as mapping failure', () => {
  const data = fixture(), c = data.cases[2];
  assert.deepEqual(c.requested, { x: 218.9375, y: 80.2875 });
  for (const event of c.events) {
    event.event.clientX = Math.round(c.requested.x); event.event.clientY = Math.round(c.requested.y);
    event.after.readout = readout(500, 179);
  }
  c.after.readout = readout(500, 179);
  const result = verifyCases(data, manifest);
  assert.equal(result.intended_misses, 1); assert.equal(result.changed_geometry_cases, 0);
  assert.deepEqual(result.cases[2].reported, { x: 500, y: 179 });
  assert.deepEqual(result.cases[2].requested_to_delivered_delta_css, { x: .0625, y: -.2874999999999943 });
});
test('all frozen scheduled targets pass and repeated summaries are byte-identical', () => {
  const data = fixture(), original = JSON.stringify(data);
  const a = verifyCases(data, manifest), b = verifyCases(data, manifest);
  assert.equal(a.cases_checked, 12); assert.equal(a.intended_misses, 0);
  assert.equal(JSON.stringify(a), JSON.stringify(b)); assert.equal(JSON.stringify(data), original);
});
test('logged zoom-control gaps are retained without imposing a fictitious contiguous overall sequence', () => {
  const data = fixture();
  for (let i = 0; i < data.cases.length; i++) {
    const gap = i >= 9 ? 6 : i >= 6 ? 3 : 0;
    data.cases[i].before.eventCount += gap;
    for (const event of data.cases[i].events) event.sequence += gap;
  }
  const result = verifyCases(data, manifest);
  assert.equal(result.cases[6].intervening_logged_events_not_in_case, 3);
  assert.equal(result.cases[9].intervening_logged_events_not_in_case, 3);
  assert.deepEqual(result.cases[11].case_event_sequences, [40, 41, 42]);
});
test('changed geometry remains explicit and does not itself fail', () => {
  const data = fixture();
  for (const entry of data.cases[0].events) entry.after.pageScroll[1] = 3;
  const result = verifyCases(data, manifest);
  assert.equal(result.changed_geometry_cases, 1);
  assert.equal(result.cases[0].disposition, 'changed_geometry_retains_attribution_ambiguity');
});
test('capture rectangle, not prior or after rectangle, determines delivered cell', () => {
  const data = fixture(), c = data.cases[0];
  for (const e of c.events) {
    e.capture.imageRect = rect(e.capture.imageRect.left, e.capture.imageRect.top + .375, 480, 270);
    e.after.readout = readout(500, 177);
  }
  c.after.readout = readout(500, 177);
  const result = verifyCases(data, manifest);
  assert.equal(result.intended_misses, 1); assert.equal(result.changed_geometry_cases, 1);
});
test('geometry tolerance is fixed and reported', () => {
  const a = fixture(); a.cases[0].events[0].after.dpr += 5e-10;
  assert.equal(verifyCases(a, manifest).changed_geometry_cases, 0);
  a.cases[0].events[0].after.dpr += 2e-9;
  assert.equal(verifyCases(a, manifest).changed_geometry_cases, 1);
});
test('nullable visual viewport and changes are retained; invalid or noncontrol after state fails', () => {
  const data = fixture();
  for (const event of data.cases[0].events) {
    event.capture.visualViewport = null; event.after.visualViewport = null;
  }
  assert.equal(verifyCases(data, manifest).changed_geometry_cases, 0);
  data.cases[1].events[2].after.visualViewport.offsetTop = 1;
  const result = verifyCases(data, manifest);
  assert.equal(result.changed_geometry_cases, 1);
  assert.deepEqual(result.cases[1].geometry_differences[2].capture_to_after, ['visualViewport.offsetTop']);
  data.cases[2].events[2].after.visualViewport = null;
  assert.equal(verifyCases(data, manifest).changed_geometry_cases, 2);
  for (const mutate of [d => d.cases[0].events[2].after.selected = '274',
    d => d.cases[0].events[2].after.naturalWidth = 704,
    d => d.cases[0].events[2].capture.visualViewport.scale = 0,
    d => delete d.cases[0].events[2].capture.visualViewport,
    d => d.cases[0].events[2].after.visualViewport.offsetTop = null]) {
    const bad = fixture(); mutate(bad); assert.throws(() => verifyCases(bad, manifest));
  }
});
test('invalid oracle inputs and inconsistent rectangles fail closed', () => {
  for (const r of [null, {}, rect(0, 0, 0, 1), { ...rect(0, 0, 1, 1), right: 2 },
    { ...rect(0, 0, 1, 1), top: Infinity }]) assert.throws(() => rectangle(r));
  for (const p of [null, {}, { x: NaN, y: 0 }, { x: '1', y: 0 }])
    assert.throws(() => boundaryOracle(p, rect(0, 0, 1280, 720)));
  assert.throws(() => boundaryOracle({ x: 0, y: 0 }, rect(0, 0, 1, 1), 1.5, 1));
});
test('schedule/schema omissions, duplicates, substitutions and unknown fields fail', () => {
  for (const mutate of [d => d.cases.pop(), d => d.cases.reverse(), d => d.cases[1].id = d.cases[0].id,
    d => d.cases[0].zoom = '1', d => d.cases[0].intended.y++, d => d.schema = 'other',
    d => d.cases[0].extra = true, d => delete d.cases[0].before]) {
    const data = fixture(); mutate(data); assert.throws(() => verifyCases(data, manifest));
  }
});
test('wrong intended center and invisible request fail without substituting targets', () => {
  for (const mutate of [d => d.cases[0].requested.y += .01,
    d => d.cases[0].before.viewport = [100, 100],
    d => d.cases[0].before.viewportRect = rect(0, 0, 10, 10),
    d => d.cases[0].before.naturalWidth = 704]) {
    const data = fixture(); mutate(data); assert.throws(() => verifyCases(data, manifest));
  }
});
test('untrusted, missing, pending, misordered and wrong-target events fail', () => {
  for (const mutate of [d => d.cases[0].events.pop(), d => d.cases[0].events[2].event.isTrusted = false,
    d => d.cases[0].events[0].status = 'pending', d => d.cases[0].events[2].after.status = 'pending',
    d => d.cases[0].events.reverse(), d => d.cases[0].events[2].event.targetId = 'stage',
    d => d.cases[0].events[2].event.clientX = Infinity, d => d.cases[1].before.eventCount = 0,
    d => d.cases[0].events[2].capture.selected = '274', d => d.cases[0].events[2].event.timeStamp = -1]) {
    const data = fixture(); mutate(data); assert.throws(() => verifyCases(data, manifest));
  }
});
test('nullable pointer metadata stays unknown without weakening event trust checks', () => {
  const data = fixture();
  for (const event of data.cases[0].events) {
    event.event.pointerType = null; event.event.pointerId = null;
  }
  const result = verifyCases(data, manifest);
  assert.deepEqual(result.cases[0].pointer_identity_as_recorded,
    ['pointerdown', 'pointerup', 'click'].map(type => ({ type, pointerType: null, pointerId: null })));
  for (const [key, value] of [['pointerType', 1], ['pointerId', '1'], ['pointerId', 1.5]]) {
    const bad = fixture(); bad.cases[0].events[2].event[key] = value;
    assert.throws(() => verifyCases(bad, manifest), /nullable pointer identity/);
  }
  data.cases[0].events[2].event.isTrusted = false;
  assert.throws(() => verifyCases(data, manifest), /type\/trust mismatch/);
});
test('genuine selected-cell mismatch fails even with changed geometry', () => {
  for (const changed of [false, true]) {
    const data = fixture(); data.cases[0].events[2].after.readout = readout(500, 177);
    if (changed) data.cases[0].events[2].after.pageScroll[1] = 3;
    assert.throws(() => verifyCases(data, manifest), /oracle disagrees/);
  }
});
test('any historical answer, synthetic draft or identity/nullable-metadata change fails', () => {
  for (const mutate of [d => d.cases[0].after.draft.historical_responses[0].inspected = true,
    d => d.cases[0].after.draft.historical_responses[0].box = { xmin: 0, ymin: 0, xmax: 0, ymax: 0 },
    d => d.cases[0].after.draft.historical_responses[0].note = '',
    d => d.cases[0].after.draft.historical_responses[1].stored_pts = 0,
    d => d.cases[0].after.draft.historical_responses.reverse(),
    d => d.cases[0].after.draft.synthetic_control_response = {},
    d => d.cases[0].after.draft.protocol_sha256 = '0'.repeat(64),
    d => d.cases[0].after.draftCount = '1 historical row',
    d => d.cases[0].events[2].after.boxReadout = 'PENDING BOX']) {
    const data = fixture(); mutate(data); assert.throws(() => verifyCases(data, manifest));
  }
});
test('manifest identity and byte-pin mismatches fail', () => {
  for (const mutate of [m => m.frame_order.reverse(), m => m.source_sha256 = '0'.repeat(64),
    m => m.assets.control.width = 704, m => m.assets.control.sha256 = '0'.repeat(64),
    m => m.assets['274'].synthetic = true]) {
    const m = clone(manifest); mutate(m); assert.throws(() => validateManifest(m));
  }
  const bytes = Buffer.from('synthetic fixture');
  verifyPin(bytes, sha256(bytes), 'fixture');
  assert.throws(() => verifyPin(bytes, '0'.repeat(64), 'fixture'), /SHA-256 mismatch/);
});
