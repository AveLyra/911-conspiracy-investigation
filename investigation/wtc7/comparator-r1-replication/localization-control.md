# Prospective display-coordinate control

2026-09-24. Declared after both historical candidate records were frozen, but
before creating or viewing this synthetic fixture. Neither historical record
may be changed based on this test. It tests only coarse native-display
coordinate reading, not real-camera blur, material-point identity, uncertainty
calibration, reference stationarity or physical motion.

Create one deterministic 1280×720 RGB figure on a plain background with three
separated geometric shapes labeled A, B and C. Each queried point is the
top-left outer corner of its labeled shape. A rooflike polygon and two simple
rectangles provide different heights. No historical imagery, extracted pixels,
labels, or values are used. The builder retains exact known integer corners;
no coordinates/ruler/grid are displayed on the fixture itself.

Root authors the builder and therefore knows the answers; root cannot serve
as a truth-blind reader. /root/curve_render reads this note but **not** the
builder or truth data before its control annotation freeze. It views the
fixture once at original detail and saves a subjective inclusive y envelope
for A/B/C using the same display-reading method as its historical candidates.
Nulls and failures must remain. The prospective pass rule is that all three
ranges contain the corresponding known corner y, with width (high minus low)
no greater than 24 native pixels. A wider/null/missed range fails this bounded
control; no retuning or replacement fixture is permitted in this pass.

After freezing, root compares all three with the builder truth. A separate
checker verifies figure dimensions and exact corner geometry/pixels from the
builder and reruns the truth-versus-annotation calculation. Preserve the entire
fixture, annotation, actual outcomes and any failure. Passing this easy fixture
is only a successful coarse-coordinate control for this one reader/display;
it does not establish that the real-frame envelopes have calibrated coverage
or that both readers are independently accurate. Actual human mapping review
remains required before historical arithmetic or a reproduction verdict.
