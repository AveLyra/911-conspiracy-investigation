// Pure coordinate helpers plus a guarded read-only browser UI.
// Importing without a document runs no UI; nothing is stored or accepted.
const finite = (value) => typeof value === "number" && Number.isFinite(value);

function dimensions(width, height) {
  return Number.isSafeInteger(width) && width > 0 &&
    Number.isSafeInteger(height) && height > 0;
}

function validRect(rect) {
  return rect && [rect.left, rect.top, rect.width, rect.height].every(finite) &&
    rect.width > 0 && rect.height > 0 &&
    finite(rect.left + rect.width) && finite(rect.top + rect.height) &&
    rect.left + rect.width > rect.left && rect.top + rect.height > rect.top;
}

function validPixel(point, width, height) {
  return dimensions(width, height) && point &&
    Number.isInteger(point.x) && Number.isInteger(point.y) &&
    point.x >= 0 && point.x < width && point.y >= 0 && point.y < height;
}

// client coordinates and getBoundingClientRect share the viewport origin.
// Thus scrolling (including negative rect origins) needs no added scroll offset.
// An image must have no border or padding: its rect is the displayed pixel area.
export function pointerToPixel(clientX, clientY, rect, width, height) {
  if (!dimensions(width, height) || !validRect(rect) ||
      !finite(clientX) || !finite(clientY)) return null;
  if (clientX < rect.left || clientY < rect.top ||
      clientX >= rect.left + rect.width || clientY >= rect.top + rect.height) {
    return null;
  }
  // The min protects the last in-bounds cell from final floating-point rounding.
  return {
    x: Math.min(width - 1, Math.floor((clientX - rect.left) / rect.width * width)),
    y: Math.min(height - 1, Math.floor((clientY - rect.top) / rect.height * height)),
  };
}

// The marker is centered on the selected pixel cell, not its upper-left edge.
export function pixelCenter(point, rect, width, height) {
  if (!validPixel(point, width, height) || !validRect(rect)) return null;
  return {
    clientX: rect.left + ((point.x + 0.5) / width) * rect.width,
    clientY: rect.top + ((point.y + 0.5) / height) * rect.height,
  };
}

export function nudgePixel(point, key, width, height) {
  if (!validPixel(point, width, height)) return null;
  const moves = {
    ArrowLeft: [-1, 0], ArrowRight: [1, 0],
    ArrowUp: [0, -1], ArrowDown: [0, 1],
  };
  if (!Object.hasOwn(moves, key)) return null;
  const [dx, dy] = moves[key];
  return {
    x: Math.max(0, Math.min(width - 1, point.x + dx)),
    y: Math.max(0, Math.min(height - 1, point.y + dy)),
  };
}

