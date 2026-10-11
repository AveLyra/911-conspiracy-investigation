// Pure session-draft validation. This does not authenticate a human or accept evidence.
export const STATUSES = Object.freeze([
  "notinspected", "localizable", "ambiguous", "obscured", "notlocated", "outside",
]);

const exactKeys = (value, keys) => value !== null && typeof value === "object" &&
  !Array.isArray(value) && Object.keys(value).length === keys.length &&
  keys.every((key) => Object.hasOwn(value, key));

function requireValue(condition, message) {
  if (!condition) throw new TypeError(message);
}

export function validateBox(box, width, height) {
  requireValue(Number.isSafeInteger(width) && width > 0 &&
    Number.isSafeInteger(height) && height > 0, "Invalid native dimensions.");
  requireValue(exactKeys(box, ["xmin", "ymin", "xmax", "ymax"]),
    "A complete box needs xmin, ymin, xmax and ymax.");
  const { xmin, ymin, xmax, ymax } = box;
  requireValue([xmin, ymin, xmax, ymax].every(Number.isSafeInteger),
    "Box endpoints must be integer native pixel-cell indices.");
  requireValue(xmin >= 0 && ymin >= 0 && xmax < width && ymax < height &&
    xmax >= 0 && ymax >= 0 && xmin < width && ymin < height, "Box is outside the image.");
  requireValue(xmin <= xmax && ymin <= ymax,
    "Reversed endpoints rejected; choose upper-left first, lower-right second.");
  return { xmin, ymin, xmax, ymax };
}

export function validateResponse(row, asset) {
  requireValue(exactKeys(row, ["inspected", "status", "box", "note"]),
    "A row needs only inspected, status, box and note.");
  requireValue(row.inspected === true, "Explicit inspection confirmation is required.");
  requireValue(STATUSES.includes(row.status) && row.status !== "notinspected",
    "Choose an entered status; not inspected is not a response.");
  requireValue(typeof row.note === "string" && row.note.trim().length > 0,
    "An explanatory note is required for every entered status, including localizable.");
  let box = null;
  if (row.status === "localizable") {
    box = validateBox(row.box, asset.width, asset.height);
  } else if (row.status === "ambiguous" && row.box !== null) {
    box = validateBox(row.box, asset.width, asset.height);
  } else {
    requireValue(row.box === null, "This status requires a null box; clear the pending box.");
  }
  return { inspected: true, status: row.status, box, note: row.note.trim() };
}

// Metadata comes from the pinned packet, never from an entered row. Nullable
// timestamp fields are preserved verbatim; no clock is inferred or substituted.
export function formatResponses(rows, assets, frameOrder, sourceHash, protocolHash) {
  requireValue(rows instanceof Map, "Session rows must be a Map.");
  requireValue(Array.isArray(frameOrder) && new Set(frameOrder).size === frameOrder.length,
    "Frame order must contain unique ordinals.");
  const allowed = new Set(["control", ...frameOrder.map(String)]);
  for (const key of rows.keys()) requireValue(allowed.has(key), "Unknown session row.");
  function entry(key, synthetic) {
    const asset = assets[key];
    requireValue(asset && asset.synthetic === synthetic, "Synthetic/historical asset mismatch.");
    requireValue(synthetic ? asset.ordinal === null :
      Number.isSafeInteger(asset.ordinal) && String(asset.ordinal) === key, "Asset ordinal mismatch.");
    const response = rows.has(key) ? validateResponse(rows.get(key), asset) :
      { inspected: false, status: "notinspected", box: null, note: null };
    return {
      ordinal: asset.ordinal, synthetic, image_sha256: asset.sha256,
      width: asset.width, height: asset.height, mode: asset.mode,
      stored_pts: asset.stored_pts, best_effort_timestamp: asset.best_effort_timestamp,
      stored_pts_seconds_exact: asset.stored_pts_seconds_exact,
      best_effort_seconds_exact: asset.best_effort_seconds_exact,
      ...response,
    };
  }
  return JSON.stringify({
    packet: "DistantView six-frame human localization feasibility pilot",
    state: "Session-only draft; not saved, submitted, verified or accepted",
    human_identity: "Not authenticated by this interface; a checkbox is not identity proof",
    source_sha256: sourceHash, protocol_sha256: protocolHash,
    coordinate_convention: "Zero-based native pixel cells; inclusive xmin,ymin,xmax,ymax; no inferred center",
    timestamp_limit: "Stored and best-effort fields are nullable metadata, not an adopted capture clock",
    historical_responses: frameOrder.map((ordinal) => entry(String(ordinal), false)),
    synthetic_control_response: rows.has("control") ? entry("control", true) : null,
    limit: "Subjective plausible-position boxes are not confidence intervals or proof of a fixed material point. Only an actual user reply can become a preserved human observation.",
  }, null, 2);
}
