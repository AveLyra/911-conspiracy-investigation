# Native-coordinate review tool scope

2026-09-24. Added after the user's explicit report that their viewer cannot
show reliable pixel coordinates. That reply is **not** a human mapping pass.
This small read-only tool addresses that concrete usability blocker; it does
not replace Sherlock, accept findings, or change frozen annotations.

Serve only the six already-admitted PNGs, one synthetic control PNG, one HTML
page and its coordinate script. Bind only 127.0.0.1, use exact path allowlists,
check asset identities, refuse different Host/Origin, and support no uploads,
directory browsing or write endpoints. No external scripts/assets, analytics,
storage, clipboard transfer or export. Selection remains in page memory only.
The server is not authentication against other processes on the same computer.
Source-sensitive files are not routes. Tests must exercise refusals as well
as success; this is not a complete security certification.

Display an original-image coordinate readout derived from the image's current
rendered rectangle and natural dimensions, not uncorrected screen coordinates.
Use native integer pixel indices, origin upper-left, floor for hit location,
and clear distinction between hover and locked point. Pixel-center marker
placement, scaling, scrolling, keyboard one-pixel movement, boundary handling,
frame changes/loading/error state and no-saving behavior must be tested.
The viewer must never claim a clicked pixel is an authenticated material point.

Browser QA uses the synthetic figure for coordinate assertions. Loading the six
historical assets and reading their DOM dimensions/metadata tests the tool,
not the feature measurements; no new historical annotations or arithmetic is
authorized. Any historical screenshot/view used solely for UI layout checking
must be logged as such, not silently added to the frozen observation coverage.
No historical screenshot is planned: keep visual QA on the synthetic figure.

Pure-function tests must cover fit, native and doubled display scales, offsets,
scroll positions, limits and pixel-center mapping. Then check actual clicks,
readout/marker state, zoom, scrolling, frame changes and keyboard movement in
the native in-app browser. The page is delivered only after those relevant
checks, with actual residual limitations. Application tests do not constitute
the user's human review or validate historical coordinates. The exact source
figures and human-review question remain the same.
