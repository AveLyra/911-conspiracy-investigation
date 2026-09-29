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

function initializeReview() {
  const WIDTH = 1280, HEIGHT = 720;
  const SOURCE_HASH = "8560cd686a18c8fcc16fe802691e0f17f117c713b4cd1862017af24d391ce5a2";
  const frames = Object.freeze({
    control: { url: "/control.png", bytes: 11216, hash: "f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48" },
    "239": { url: "/frames/239.png", ordinal: "0001", pts: "239239", seconds: "239239/30000", bytes: 881140, hash: "9f8d2878a69952da6d4a1e31f3a58415c9271c19e95160b28674692f5fb0439f" },
    "434": { url: "/frames/434.png", ordinal: "0196", pts: "434434", seconds: "217217/15000", bytes: 922606, hash: "cbd2078df347521154157ae7c3b637585d3196cd3b1d1398ccc19be00cacacc5" },
    "441": { url: "/frames/441.png", ordinal: "0203", pts: "441441", seconds: "147147/10000", bytes: 927384, hash: "13c3d28ee22e129de4de3030cb2d9543079518b766f01487bf43694cdbf0f95f" },
    "442": { url: "/frames/442.png", ordinal: "0204", pts: "442442", seconds: "221221/15000", bytes: 928276, hash: "62f63c6b6f912cc4d5f859175dbd7b8da987dc6a440bd0f17366b803c02bea68" },
    "443": { url: "/frames/443.png", ordinal: "0205", pts: "443443", seconds: "443443/30000", bytes: 927885, hash: "d64ec51cf17c6df8254446b642cef0542612e509245539b010c1bc8d473f80b3" },
    "444": { url: "/frames/444.png", ordinal: "0206", pts: "444444", seconds: "37037/2500", bytes: 927123, hash: "4679ce4d4e6634ac5721e36abc328ff11e75fa8eb57e468f6d390cf8c2200491" },
  });
  const byId = (id) => document.getElementById(id);
  const viewport = byId("viewport"), stage = byId("stage"), marker = byId("marker");
  const selector = byId("frame"), readout = byId("readout"), status = byId("load-status");
  let image = byId("native-image"), ready = false, point = null, locked = false;
  let zoom = "fit", loadGeneration = 0;

  function showPoint() {
    marker.hidden = true;
    if (!ready) {
      readout.textContent = "Coordinates unavailable: image not ready.";
      return;
    }
    if (!point) {
      readout.textContent = "No point — hover over the image or click to lock.";
      return;
    }
    const center = pixelCenter(point, image.getBoundingClientRect(), WIDTH, HEIGHT);
    if (!center) return;
    const base = stage.getBoundingClientRect();
    marker.style.left = `${center.clientX - base.left}px`;
    marker.style.top = `${center.clientY - base.top}px`;
    marker.hidden = false;
    readout.textContent = `${locked ? "LOCKED" : "HOVER"} — x: ${point.x}, y: ${point.y} (native pixel)`;
  }

  function clearPoint() {
    point = null;
    locked = false;
    showPoint();
  }

  function sizeImage() {
    const width = zoom === "fit"
      ? Math.max(1, Math.min(WIDTH, viewport.clientWidth, viewport.clientHeight * WIDTH / HEIGHT))
      : WIDTH * Number(zoom);
    stage.style.width = `${width}px`;
    if (!locked) point = null; // A previous hover need not describe a resized image.
    showPoint();
  }

  function loadFrame() {
    const generation = ++loadGeneration;
    const key = selector.value;
    if (!Object.hasOwn(frames, key)) return;
    const item = frames[key];
    ready = false;
    clearPoint();
    status.dataset.error = "false";
    status.textContent = "Loading image; coordinates disabled…";
    byId("kind").textContent = key === "control" ? "Synthetic control — not historical evidence" : "Historical comparator access-copy derivative";
    byId("index").textContent = key === "control" ? "Not applicable" : `${key} (zero-based source) / ${item.ordinal} (one-based output)`;
    byId("clock").textContent = key === "control" ? "Not applicable" : `PTS ${item.pts}; time base 1/30000; exact seconds ${item.seconds}`;
    byId("dimensions").textContent = `${item.bytes} bytes / 1280 × 720`;
    byId("hash").textContent = item.hash;
    byId("source-hash").textContent = key === "control" ? "Not applicable — synthetic fixture" : SOURCE_HASH;
    const next = new Image();
    next.id = "native-image";
    next.alt = key === "control" ? "Synthetic coordinate-control shapes A, B and C" : `Complete native comparator frame ${key}`;
    next.draggable = false;
    next.hidden = true;
    next.onload = () => {
      if (generation !== loadGeneration) return;
      if (next.naturalWidth !== WIDTH || next.naturalHeight !== HEIGHT) {
        status.dataset.error = "true";
        status.textContent = "Image rejected: native dimensions are not exactly 1280 × 720. Coordinates remain disabled.";
        return;
      }
      ready = true;
      next.hidden = false;
      status.textContent = "Image loaded: 1280 × 720 native pixels. Coordinates enabled; nothing is saved.";
      sizeImage();
    };
    next.onerror = () => {
      if (generation !== loadGeneration) return;
      status.dataset.error = "true";
      status.textContent = "Image load failed. Coordinates remain disabled. Select another image to retry.";
    };
    image.replaceWith(next);
    image = next;
    viewport.scrollLeft = 0;
    viewport.scrollTop = 0;
    sizeImage();
    next.src = item.url; // Only the seven literal allowlisted URLs above.
  }

  function pointer(event) {
    return ready ? pointerToPixel(event.clientX, event.clientY,
      image.getBoundingClientRect(), image.naturalWidth, image.naturalHeight) : null;
  }
  stage.addEventListener("pointermove", (event) => {
    if (!ready || locked) return;
    point = pointer(event);
    showPoint();
  });
  stage.addEventListener("pointerleave", () => {
    if (!locked) clearPoint();
  });
  stage.addEventListener("click", (event) => {
    const selected = pointer(event);
    if (!selected) return;
    point = selected;
    locked = true;
    viewport.focus({ preventScroll: true });
    showPoint();
  });
  viewport.addEventListener("keydown", (event) => {
    if (!ready || !locked) return;
    const moved = nudgePixel(point, event.key, WIDTH, HEIGHT);
    if (!moved) return;
    event.preventDefault();
    point = moved;
    showPoint();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") { event.preventDefault(); clearPoint(); }
  });
  viewport.addEventListener("scroll", () => { if (!locked) clearPoint(); });
  byId("clear").addEventListener("click", clearPoint);
  selector.addEventListener("change", loadFrame);
  for (const button of document.querySelectorAll("[data-zoom]")) {
    button.addEventListener("click", () => {
      zoom = button.dataset.zoom;
      for (const peer of document.querySelectorAll("[data-zoom]")) {
        peer.setAttribute("aria-pressed", String(peer === button));
      }
      sizeImage();
    });
  }
  new ResizeObserver(sizeImage).observe(viewport);
  loadFrame();
}

if (typeof document !== "undefined") initializeReview();
