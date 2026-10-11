// Separate computational checker. No producer imports, browser, server or writes.
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { isDeepStrictEqual } from 'node:util';

export const TOLERANCE = 1e-9;
export const PINS = Object.freeze({
  protocol: 'c1b27cc20a7ed57498f9398743cd9bf46491030071b9ad4bbb9c58d9b5b39e9c',
  manifest: '1c6b76f665ae63f43a722139317ba5890a9f1c7e25511f094a6f6fa4184e4bb6',
  core: '9cff4290fc41e27126b36402818b1ecb55057e003f819ecbe8cef53281d2e2c4',
  control: 'f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48',
});
export const SCHEDULE = Object.freeze([
  ['fit-01', 'fit', 500, 178], ['fit-02', 'fit', 500, 179],
  ['fit-03', 'fit', 500, 180], ['fit-04', 'fit', 500, 181],
  ['fit-05', 'fit', 600, 200], ['fit-06', 'fit', 500, 100],
  ['native-01', '1', 500, 180], ['native-02', '1', 600, 200],
  ['native-03', '1', 500, 100], ['double-01', '2', 500, 100],
  ['double-02', '2', 100, 50], ['double-03', '2', 200, 100],
].map(Object.freeze));
const ORDINALS = [274, 300, 342, 365, 388, 411];
const RECT_KEYS = ['left', 'top', 'width', 'height', 'right', 'bottom', 'x', 'y'];
const VISUAL_KEYS = ['width', 'height', 'offsetLeft', 'offsetTop', 'pageLeft', 'pageTop', 'scale'];
const finite = value => typeof value === 'number' && Number.isFinite(value);
const close = (a, b) => Math.abs(a - b) <= TOLERANCE;
function need(condition, message) { if (!condition) throw new Error(message); }
function keys(value, wanted, label) {
  need(value !== null && typeof value === 'object' && !Array.isArray(value), `${label}: object required`);
  need(isDeepStrictEqual(Object.keys(value).sort(), [...wanted].sort()), `${label}: schema keys differ`);
}
function pair(value, label, positive = false) {
  need(Array.isArray(value) && value.length === 2 && value.every(finite), `${label}: finite pair required`);
  if (positive) need(value.every(v => v > 0), `${label}: positive pair required`);
}
function point(value, label) {
  keys(value, ['x', 'y'], label);
  need(finite(value.x) && finite(value.y), `${label}: finite coordinates required`);
}
export function rectangle(value, label = 'rectangle') {
  keys(value, RECT_KEYS, label);
  need(RECT_KEYS.every(key => finite(value[key])), `${label}: nonfinite component`);
  need(value.width > 0 && value.height > 0, `${label}: positive dimensions required`);
  need(close(value.x, value.left) && close(value.y, value.top) &&
    close(value.right, value.left + value.width) && close(value.bottom, value.top + value.height),
    `${label}: inconsistent rectangle`);
  need(value.right > value.left && value.bottom > value.top, `${label}: collapsed rectangle`);
  return value;
}

// Independent ordered-cell membership, not inverse scaling/floor or production code.
function axisCell(position, origin, extent, count) {
  if (position < origin || position >= origin + extent) return null;
  for (let index = 0; index < count; index++) {
    const lower = origin + extent * (index / count);
    const upper = index + 1 === count ? origin + extent : origin + extent * ((index + 1) / count);
    if (position >= lower && position < upper) return index;
  }
  throw new Error('Oracle: no cell contains in-bounds coordinate');
}
export function boundaryOracle(position, rect, width = 1280, height = 720) {
  point(position, 'oracle position'); rectangle(rect, 'oracle rectangle');
  need(Number.isSafeInteger(width) && width > 0 && Number.isSafeInteger(height) && height > 0,
    'Oracle: invalid dimensions');
  const x = axisCell(position.x, rect.left, rect.width, width);
  const y = axisCell(position.y, rect.top, rect.height, height);
  return x === null || y === null ? null : { x, y };
}
function intendedCenter(intended, rect) {
  const x0 = rect.left + rect.width * (intended.x / 1280);
  const x1 = rect.left + rect.width * ((intended.x + 1) / 1280);
  const y0 = rect.top + rect.height * (intended.y / 720);
  const y1 = rect.top + rect.height * ((intended.y + 1) / 720);
  return { x: x0 + (x1 - x0) / 2, y: y0 + (y1 - y0) / 2 };
}
function inside(position, rect) {
  return position.x >= rect.left && position.x < rect.right &&
    position.y >= rect.top && position.y < rect.bottom;
}
function validateGeometry(value, label) {
  rectangle(value.imageRect, `${label}.imageRect`);
  pair(value.pageScroll, `${label}.pageScroll`);
  pair(value.regionScroll, `${label}.regionScroll`);
  pair(value.viewport, `${label}.viewport`, true);
  need(finite(value.dpr) && value.dpr > 0, `${label}.dpr: positive finite value required`);
  if (Object.hasOwn(value, 'visualViewport') && value.visualViewport !== null) {
    keys(value.visualViewport, VISUAL_KEYS, `${label}.visualViewport`);
    need(VISUAL_KEYS.every(key => finite(value.visualViewport[key])) &&
      ['width', 'height', 'scale'].every(key => value.visualViewport[key] > 0),
      `${label}.visualViewport: invalid geometry`);
  }
}
function geometryDifferences(a, b) {
  const changes = [];
  for (const key of RECT_KEYS) if (!close(a.imageRect[key], b.imageRect[key])) changes.push(`imageRect.${key}`);
  for (const key of ['pageScroll', 'regionScroll', 'viewport']) {
    for (let i = 0; i < 2; i++) if (!close(a[key][i], b[key][i])) changes.push(`${key}[${i}]`);
  }
  if (!close(a.dpr, b.dpr)) changes.push('dpr');
  if (Object.hasOwn(a, 'visualViewport') && Object.hasOwn(b, 'visualViewport')) {
    if (a.visualViewport === null || b.visualViewport === null) {
      if (a.visualViewport !== b.visualViewport) changes.push('visualViewport.availability');
    } else {
      for (const key of VISUAL_KEYS) {
        if (!close(a.visualViewport[key], b.visualViewport[key])) changes.push(`visualViewport.${key}`);
      }
    }
  }
  return changes;
}
function locked(readout, label) {
  need(typeof readout === 'string', `${label}: string required`);
  const match = /^LOCKED: x (\d+), y (\d+) \(native pixel cell; not a recorded box\)$/.exec(readout);
  need(match !== null, `${label}: exact LOCKED readout required`);
  const answer = { x: Number(match[1]), y: Number(match[2]) };
  need(answer.x < 1280 && answer.y < 720, `${label}: outside synthetic image`);
  return answer;
}
export function validateManifest(manifest) {
  need(isDeepStrictEqual(manifest.frame_order, ORDINALS), 'Manifest: frame order mismatch');
  need(manifest.source_sha256 === 'a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e',
    'Manifest: source pin mismatch');
  need(manifest.protocol_sha256 === '1846d0e0cc532009e7941608ef39af3444fb01b365c670a19a08325af6c5046d',
    'Manifest: original protocol pin mismatch');
  need(manifest.assets?.control?.sha256 === PINS.control && manifest.assets.control.synthetic === true &&
    manifest.assets.control.width === 1280 && manifest.assets.control.height === 720,
    'Manifest: synthetic control identity mismatch');
  for (const ordinal of ORDINALS) {
    const asset = manifest.assets[String(ordinal)];
    need(asset?.ordinal === ordinal && asset.synthetic === false && asset.width === 704 && asset.height === 480,
      'Manifest: historical asset identity mismatch');
  }
}
function emptyDraft(after, manifest, label) {
  keys(after, ['readout', 'draftCount', 'draft'], label);
  need(after.draftCount === '0 / 6 historical session-draft rows; no separate synthetic practice row. Not saved or accepted.',
    `${label}: draft count changed`);
  const draft = after.draft;
  keys(draft, ['packet', 'state', 'human_identity', 'source_sha256', 'protocol_sha256',
    'coordinate_convention', 'timestamp_limit', 'historical_responses', 'synthetic_control_response', 'limit'], `${label}.draft`);
  need(draft.source_sha256 === manifest.source_sha256 && draft.protocol_sha256 === manifest.protocol_sha256,
    `${label}: draft identity mismatch`);
  need(draft.packet === 'DistantView six-frame human localization feasibility pilot' &&
    draft.state === 'Session-only draft; not saved, submitted, verified or accepted' &&
    draft.human_identity === 'Not authenticated by this interface; a checkbox is not identity proof',
    `${label}: draft scope changed`);
  need(draft.coordinate_convention === 'Zero-based native pixel cells; inclusive xmin,ymin,xmax,ymax; no inferred center' &&
    draft.timestamp_limit === 'Stored and best-effort fields are nullable metadata, not an adopted capture clock' &&
    draft.limit === 'Subjective plausible-position boxes are not confidence intervals or proof of a fixed material point. Only an actual user reply can become a preserved human observation.',
    `${label}: draft qualifications changed`);
  need(draft.synthetic_control_response === null, `${label}: synthetic draft was recorded`);
  need(Array.isArray(draft.historical_responses) && draft.historical_responses.length === 6,
    `${label}: historical roster mismatch`);
  const metadata = ['ordinal', 'synthetic', 'width', 'height', 'mode', 'stored_pts', 'best_effort_timestamp',
    'stored_pts_seconds_exact', 'best_effort_seconds_exact'];
  for (let i = 0; i < ORDINALS.length; i++) {
    const row = draft.historical_responses[i], asset = manifest.assets[String(ORDINALS[i])];
    keys(row, [...metadata, 'image_sha256', 'inspected', 'status', 'box', 'note'], `${label}.row${i}`);
    for (const name of metadata) need(isDeepStrictEqual(row[name], asset[name]), `${label}: row metadata mismatch ${name}`);
    need(row.image_sha256 === asset.sha256, `${label}: row image pin mismatch`);
    need(row.inspected === false && row.status === 'notinspected' && row.box === null && row.note === null,
      `${label}: historical response is not empty`);
  }
}

export function verifyCases(data, manifest) {
  validateManifest(manifest);
  keys(data, ['schema', 'cases'], 'data');
  need(data.schema === 'synthetic-delivery-cases-v1', 'Data schema mismatch');
  need(Array.isArray(data.cases) && data.cases.length === 12, 'Exactly 12 cases required');
  const results = [];
  let previousEventTime = -Infinity;
  let previousEndCount = 0;
  for (let index = 0; index < SCHEDULE.length; index++) {
    const item = data.cases[index], [id, zoom, x, y] = SCHEDULE[index];
    keys(item, ['id', 'zoom', 'intended', 'before', 'requested', 'events', 'after'], `case ${index}`);
    need(item.id === id && item.zoom === zoom && isDeepStrictEqual(item.intended, { x, y }), `Schedule mismatch at ${index}`);
    const before = item.before;
    keys(before, ['imageRect', 'viewportRect', 'naturalWidth', 'naturalHeight', 'viewport', 'dpr',
      'pageScroll', 'regionScroll', 'eventCount'], `${id}.before`);
    validateGeometry(before, `${id}.before`); rectangle(before.viewportRect, `${id}.viewportRect`);
    need(before.naturalWidth === 1280 && before.naturalHeight === 720, `${id}: wrong natural dimensions`);
    need(Number.isSafeInteger(before.eventCount) && before.eventCount >= previousEndCount &&
      before.eventCount <= 97, `${id}: prior event count invalid, overlapping or beyond cap`);
    const betweenCaseEvents = before.eventCount - previousEndCount;
    point(item.requested, `${id}.requested`);
    const center = intendedCenter(item.intended, before.imageRect);
    need(close(item.requested.x, center.x) && close(item.requested.y, center.y), `${id}: requested point is not intended center`);
    need(inside(item.requested, before.imageRect) && inside(item.requested, before.viewportRect) &&
      item.requested.x >= 0 && item.requested.y >= 0 && item.requested.x < before.viewport[0] &&
      item.requested.y < before.viewport[1], `${id}: request not visible inside recorded rectangles/viewport`);
    need(Array.isArray(item.events) && item.events.length === 3, `${id}: three events required`);
    const eventDifferences = [];
    for (let n = 0; n < 3; n++) {
      const entry = item.events[n], name = `${id}.event${n}`;
      keys(entry, ['sequence', 'status', 'event', 'capture', 'after'], name);
      need(entry.sequence === before.eventCount + n + 1 && entry.status === 'completed', `${name}: sequence/status mismatch`);
      keys(entry.event, ['type', 'isTrusted', 'pointerType', 'pointerId', 'clientX', 'clientY', 'timeStamp', 'targetId'], `${name}.event`);
      need(entry.event.type === ['pointerdown', 'pointerup', 'click'][n] && entry.event.isTrusted === true,
        `${name}: event type/trust mismatch`);
      need((entry.event.pointerType === null || typeof entry.event.pointerType === 'string') &&
        (entry.event.pointerId === null || Number.isSafeInteger(entry.event.pointerId)),
        `${name}: invalid nullable pointer identity`);
      need(entry.event.targetId === 'native-image', `${name}: non-image event target`);
      need([entry.event.clientX, entry.event.clientY, entry.event.timeStamp].every(finite) &&
        entry.event.timeStamp >= 0 && entry.event.timeStamp >= previousEventTime, `${name}: invalid event coordinates/time`);
      previousEventTime = entry.event.timeStamp;
      keys(entry.capture, ['selected', 'naturalWidth', 'naturalHeight', 'imageRect', 'pageScroll', 'regionScroll',
        'viewport', 'visualViewport', 'dpr', 'performanceNow'], `${name}.capture`);
      need(entry.capture.selected === 'control' && entry.capture.naturalWidth === 1280 &&
        entry.capture.naturalHeight === 720, `${name}: not synthetic control`);
      validateGeometry(entry.capture, `${name}.capture`);
      keys(entry.after, ['status', 'selected', 'naturalWidth', 'naturalHeight', 'readout', 'boxReadout', 'marker',
        'imageRect', 'pageScroll', 'regionScroll', 'viewport', 'visualViewport', 'dpr', 'performanceNow'], `${name}.after`);
      need(entry.after.status === 'completed', `${name}: incomplete after record`);
      need(entry.after.selected === 'control' && entry.after.naturalWidth === 1280 && entry.after.naturalHeight === 720,
        `${name}: after record not synthetic control`);
      validateGeometry(entry.after, `${name}.after`);
      need(finite(entry.capture.performanceNow) && entry.capture.performanceNow >= 0 &&
        finite(entry.after.performanceNow) && entry.after.performanceNow >= entry.capture.performanceNow,
        `${name}: invalid capture/after ordering`);
      need(typeof entry.after.readout === 'string' && entry.after.boxReadout === 'No pending box.',
        `${name}: missing readout or unexpected pending box`);
      keys(entry.after.marker, ['hidden', 'rect'], `${name}.marker`);
      need(typeof entry.after.marker.hidden === 'boolean', `${name}: invalid marker state`);
      if (entry.after.marker.rect !== null && !entry.after.marker.hidden) rectangle(entry.after.marker.rect, `${name}.marker.rect`);
      need(entry.after.marker.hidden || entry.after.marker.rect !== null, `${name}: visible marker missing rectangle`);
      eventDifferences.push({ type: entry.event.type,
        before_to_capture: geometryDifferences(before, entry.capture),
        capture_to_after: geometryDifferences(entry.capture, entry.after) });
    }
    const click = item.events[2], delivered = { x: click.event.clientX, y: click.event.clientY };
    const expected = boundaryOracle(delivered, click.capture.imageRect);
    need(expected !== null, `${id}: delivered click outside image`);
    const reported = locked(click.after.readout, `${id}.click.readout`);
    need(isDeepStrictEqual(reported, expected), `${id}: delivered-cell oracle disagrees with LOCKED readout`);
    need(!click.after.marker.hidden, `${id}: click marker hidden`);
    emptyDraft(item.after, manifest, `${id}.after`);
    need(item.after.readout === click.after.readout, `${id}: final readout differs from click record`);
    const stable = eventDifferences.every(row => row.before_to_capture.length === 0 && row.capture_to_after.length === 0);
    const intendedMatch = isDeepStrictEqual(item.intended, reported);
    const delta = { x: delivered.x - item.requested.x, y: delivered.y - item.requested.y };
    previousEndCount = before.eventCount + 3;
    results.push({ id, zoom, before_event_count: before.eventCount, intervening_logged_events_not_in_case: betweenCaseEvents,
      case_event_sequences: item.events.map(entry => entry.sequence),
      pointer_identity_as_recorded: item.events.map(entry => ({ type: entry.event.type,
        pointerType: entry.event.pointerType, pointerId: entry.event.pointerId })),
      intended: item.intended, requested: item.requested, delivered, reported,
      oracle: expected, requested_to_delivered_delta_css: delta,
      intended_to_reported_delta_cells: { x: reported.x - x, y: reported.y - y },
      intended_matches_reported: intendedMatch, geometry: stable ? 'stable' : 'changed',
      geometry_differences: eventDifferences,
      disposition: !stable ? 'changed_geometry_retains_attribution_ambiguity' : intendedMatch ?
        'intended_cell_reached' : 'delivered_point_explains_miss_with_stable_geometry_no_stack_layer_attribution' });
  }
  return { schema: 'independent-delivery-verification-v1', status: 'passed', cases_checked: results.length,
    completed_trusted_events_checked: 36, geometry_tolerance_css: TOLERANCE,
    intended_misses: results.filter(row => !row.intended_matches_reported).length,
    changed_geometry_cases: results.filter(row => row.geometry === 'changed').length,
    historical_response_rows_checked_empty: 72, synthetic_drafts_recorded: 0, cases: results,
    limits: ['Computational review of supplied browser records, not independent browser observation.',
      'No production controller, response module, coordinate helper or logger imported or executed.',
      'Visibility checks recorded rectangles/viewport; not occlusion by unrecorded overlays or scrollbar geometry.',
      'Pre-request visualViewport was not recorded; only capture-to-after visualViewport stability is checked. Null stays unknown.',
      'No original-event cause, stack rounding layer, human localization accuracy or fine-view guarantee established.',
      'Keyboard follow-through, logger guards/cap, server routes and full protected-input closure are outside this checker.'] };
}

export const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
export function verifyPin(bytes, pin, label) { need(sha256(bytes) === pin, `${label}: SHA-256 mismatch`); }
export function readPinnedInputs() {
  const protocol = readFileSync(new URL('./PROTOCOL.md', import.meta.url));
  const manifestBytes = readFileSync(new URL('../packet02/manifest.json', import.meta.url));
  const core = readFileSync(new URL('../packet02/coordinate-core.mjs', import.meta.url));
  verifyPin(protocol, PINS.protocol, 'Diagnostic protocol');
  verifyPin(manifestBytes, PINS.manifest, 'Original packet manifest');
  verifyPin(core, PINS.core, 'Original mapping helper bytes');
  const manifest = JSON.parse(manifestBytes);
  validateManifest(manifest);
  return { manifest, pins: { protocol: { bytes: protocol.length, sha256: sha256(protocol) },
    original_manifest: { bytes: manifestBytes.length, sha256: sha256(manifestBytes) },
    original_core: { bytes: core.length, sha256: sha256(core) } } };
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    need(process.argv.length === 3, 'Usage: node verify_delivery.mjs browser-cases.json');
    const inputs = readPinnedInputs(), bytes = readFileSync(process.argv[2]);
    const summary = verifyCases(JSON.parse(bytes), inputs.manifest);
    const after = readPinnedInputs();
    need(isDeepStrictEqual(inputs.pins, after.pins), 'Pinned inputs changed during check');
    need(bytes.equals(readFileSync(process.argv[2])), 'Browser-case input changed during check');
    process.stdout.write(JSON.stringify({ ...summary, inputs: { ...inputs.pins,
      browser_cases: { bytes: bytes.length, sha256: sha256(bytes) },
      verifier: { sha256: sha256(readFileSync(fileURLToPath(import.meta.url))) } } }, null, 2) + '\n');
  } catch (error) {
    process.stderr.write(`Independent delivery verification failed: ${error.message}\n`);
    process.exitCode = 1;
  }
}
