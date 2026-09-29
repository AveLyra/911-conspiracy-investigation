# Post-result derivative-clock diagnostic

2026-09-19. This is an explicitly **post-result** extension, not part of the original protocol. Original run01/run02 and the independent rational oracle remain frozen. The original nominal-0.4-second test has11 rounding-incompatible residuals among161 supported velocities, all positive0.035–0.045 m/s at negative velocities. Independent arithmetic reproduces that pattern. No error has been corrected in the paper or original analysis.

Before testing alternatives, root inspected the already-preserved Camera2 access-copy metadata and freshly rehashed/probed the held file. `VID-WTC7-001` is208,810,910 bytes, SHA-256 `84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730`. Fresh `ffprobe` and the saved `timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/streams.json` agree: nominal `r_frame_rate=30000/1001`, average `2997/100`, time base `1/2997`. Saved metadata SHA-256 `d54e30ca5e8bece9ba61769e3916741caa14ea3f4b4c0b6dc7757685ec50daa1`. The earlier timing audit documents nonuniform presentation intervals; neither rate supplies an authenticated exposure clock.

## Hypothesis and fixed test

A source nominal0.2-second tracking step could represent six frames near30fps while computed velocities use a slightly longer duration. That would reduce magnitudes for negative velocities, matching the observed residual sign. **Six-frame selection and use of either listed rate are hypotheses, not documented author settings.** The paper-specific frame/table join remains unverified.

Test exactly three centered spans:12/30 =0.4s (original);12/(30000/1001) =0.4004s;12/(2997/100) =400/999s. Do not optimize an arbitrary denominator. For every original supported row and every candidate, compare `(y_next-y_previous)/span` with printed v and use the exact rounding bound `0.010/span +0.005`. Save all483 row-candidate results, exact fractions, failures and counts. The original unsupported NW endpoint remains unsupported. A synthetic linear-position test at each span must recover its true velocity, and an explicit beyond-bound perturbation must fail.

Do not rerun or rescale the98 prior fits under this diagnostic. Do not claim joint feasibility of all hidden rounded variables, absence of filtering, native frame timing, corrected acceleration, or identification of the historical Tracker settings. A candidate that accounts for every individual residual would show a concrete ordinary explanation for this particular mismatch; it would not authenticate the measurements or establish the overall collapse mechanism. A candidate failure is retained, not tuned away.

Independent exact recalculation must verify every row and decision. Both the pre-extension failures and the post-extension result stay visible in the report. No new raw-video decoding/tracking, source alteration, solver, main edit or disclosure is authorized.
