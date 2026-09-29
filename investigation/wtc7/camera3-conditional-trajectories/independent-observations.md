# Independent sampled association of the saved Camera 3 tracks

September 12, 2026. Computational AI viewing under the [protocol](PROTOCOL.md) and investigation charter. Frozen before reading root's observation note, the exported point arrays or any fitted result. No original track names, raw TRK/private fields or gravity comparisons were used. Prior event, source and calibration familiarity is acknowledged; this is not a clean holdout or human/expert review.

## Result

**track01 (cyan)** is visually associated with the image-right outer top/side corner of the large banded background building in all eight samples. It is a more distinctive two-edge intersection than track02. In the final sample, a small part of that upper-right outline is still visible above the bright foreground obstruction. These samples support the intended image-feature association; they do not verify one unchanged material point throughout the intervening 71-mark series, establish a cardinal corner/name, or turn the corner into a centre of mass.

**track02 (yellow)** is associated with the image-left portion of the same building's upper rim, initially just image-right of the raised rectangular roof feature. It is not placed at the top corner of that raised feature. The local higher-roof context changes substantially in later samples, while the query remains near the main upper outline. A point on that outline is not necessarily a distinctive material landmark: I cannot distinguish a consistently tracked material point from an outline intersection near a chosen image column using these samples alone. At frame 348 the yellow query is in a smoke-softened, foreground-adjacent outline region; its exact target-edge association is ambiguous.

Both generic track IDs should remain. The observations do not support relabeling them using original names, treating them as stationary references, interpreting their separation as rigid-body geometry, or claiming whole-building symmetry from two point histories.

## Per-frame observation record

For each frame, I viewed the entire unmarked native image before the matching saved-query overlay. “Visible” below describes an image-outline association, not independently validated material continuity. The nominal time column is the protocol's assigned `(frame-138)/15` clock; it is not an exposure-time or collapse-onset determination.

| Zero-based frame / nominal seconds | track01, cyan | track02, yellow |
|---|---|---|
| 138 / 0 | Visible outer upper-right silhouette corner, where the slanted top meets the nearly vertical image-right side. Query lies at that corner neighborhood. | Visible upper-rim neighborhood near the lower/right vicinity of the raised rectangular roof feature. Query is on the main rim, not the raised feature's top. Architectural component and unique material anchor unverified. |
| 168 / 2 | Same type of visible top/side corner association. No new exact landmark position is independently measured here. | Main upper-rim neighborhood remains visible near the query. The neighboring raised feature provides context, not proof that the query belongs to that feature. |
| 198 / 4 | Corner remains visibly associated with cyan query. | Main rim near the query is visible, but the nearby raised roof profile has changed from the initial rectangular appearance. This does not establish that the yellow query tracks the changing raised feature or that its material correspondence has failed; it makes such an assignment unsafe without a definition. |
| 228 / 6 | Visible upper-right outline corner; association retained at sampled level. | Query is near the upper rim/shallow change in its profile. The formerly prominent raised rectangle is no longer clearly present in this neighborhood. General roof-outline association remains visible; unique baseline-material identity is unresolved. |
| 258 / 8 | Corner visible, with a clear contrast against sky. | Upper outline at the query is visible, but no isolated corner or persistent small material marker is resolved there. A fixed-column/outline-intersection interpretation remains possible. |
| 288 / 10 | Same kind of visible outer top/side intersection. | Query remains close to the upper outline; material identity remains uncertain for the same reason as frame 258. No statement of pixel stationarity follows from similar apparent query placement. |
| 318 / 12 | Visible upper-right corner on the now lower and differently shaped upper facade outline. This is an image appearance/displacement observation, not acceleration or onset. | Query lies near a lowered, more curved/shallow upper-outline region. A roof-edge association is visible, but it is not a clearly isolated continuation of a particular original corner. Deformation and changing silhouette limit correspondence. |
| 348 / 14 | Small upper-right target corner/edge remains visible above the bright foreground. Query is consistent with that remaining outline, although little adjacent facade context survives. | Query lies in a blurred/smoke-softened left upper-outline vicinity immediately adjacent to foreground overlap. A clean exact target landmark is not resolved; association is **ambiguous**, and continuing material identity is not assessable from this sample. Do not silently count it as a validated visible material marker or declare a precise disappearance. |

The sampled images support a stronger distinctive-corner association for track01 than for track02. They do not support calling track02 a penthouse-top track or assigning either point an architectural/cardinal name from the saved application's labels. A changed nearby roof feature is not automatically the feature represented by the query.

## What these samples can and cannot screen

Eight frames were fixed prospectively at every tenth saved mark: 138, 168, 198, 228, 258, 288, 318 and 348. They are **8 of 71** marked indices, not complete point-by-point visual verification. No other 63 marked positions or intervening video frames were newly viewed. The late track02 limitation is a sampled association result; it does not identify the first ambiguous frame or exact loss-of-visibility time.

A fit window may include source coordinates even when physical feature identity is unresolved. Preserve those calculations as a reconstruction of the supplied numbers, but flag the distinction when interpreting them. For track02, the unverified material-point definition applies even where a rim is plainly visible; windows containing frame 348 have the additional directly sampled ambiguity. For track01, good sample associations do not certify all intervening points or fixed projection.

The saved-query crosses are analytical additions, not original marks, new point placements or uncertainty envelopes. The receipt defines cyan as track01 and yellow as track02, with nearest-integer queries under an integer-pixel-centre convention. I did not independently re-localize centres or assign numerical localization-error bars in this pass. The native images, not colored overlays, supply the scene evidence.

## Actual coverage and input identities

This pass viewed all **16** supplied complete 720 x 480 images: the eight `views01/frame-NNNN.png` native L-mode images and matching `views01/queries-NNNN.png` RGB query overlays. No crops, new images, raw TRK, point-array file, producer code, root observation note or fitted result were opened. Numeric exported-point hashes below are lineage metadata from the view receipt, not a claim that I reviewed their contents. The separate methods note reviews the declared procedure, not its execution.

All paths in this table are under `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-conditional-trajectories/` unless explicitly attributed.

| Input / role | SHA-256 |
|---|---|
| `PROTOCOL.md`, read fully | `d7fd79c3269155a06225346273aab4a6352c14c233beda4fa88989d244d3ec01` |
| `views01/receipt.json`, selected identity/convention/execution fields read | `2288efb20f0c7d7a94b8859f3a5b50483f0996d0dac4114f43ffaf3db9d24c3f` |
| Numeric point export, attributed to view receipt; contents not read | `f85e6f0ddbb55e3ef142a62e774237c69a59b9bbcbc31a92f93a37b9a9099df3` |
| Numeric export receipt, attributed; contents not read | `599911e494dc79f0cec5770a6caed44ddee1d9acb3fa64554db0e371bf86a16c` |
| Public WMV source, attributed to view receipt; no new source rehash by me | `48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722` |
| Prior WMV map, attributed to view receipt | `8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2` |

| Index | Native PNG SHA-256 | Query-overlay PNG SHA-256 |
|---|---|---|
| 138 | `8d16b44ea88ac210579b1c7b8c67ba202a400009f63d4cb9a80fa294f85b5abb` | `b6f14a6cc6c1a5ecc30ad3279ebbc7b7c2c98e8134a913ec195ed4ab9bcb4f9a` |
| 168 | `e53a02c70cbe9107a3042fab4dbdf3fbd20a809ee49480d3b8b6c76f2f07434d` | `93359263bb77d9cffd81183eb30256d05154ae542544c5c0c7f241fb8281488d` |
| 198 | `ad940b434d38c2ac0b46365a55f9035878ffc0dbd7c638dfd4023f58c78440bf` | `9d7803cf5cf404e2ce870d5136905a8b15081839ad1c7919b8391ecf900e9d87` |
| 228 | `57dd165587436b775dbbdc48c59dfb0e49b123ddc4ac02732f7c7c188482fd2d` | `3f1260bf4521b012b627fab1f15a9c994f72f7a3a895746d7a3a23e2fd45db4c` |
| 258 | `4fc10778ab5ca7d94719cf9880c26b6ce5e3f622ce4aca2d1fc3e749c246e571` | `7c42c68beacc1dc4701f90c4f5479dd0c66b7cf7d32ae019f874773797e1357f` |
| 288 | `4fbcf6c6423938ab5dac57d3c1530af34432aad31dad1c4c4e09768f46806536` | `058da7198e1761cd7ab401ef0809aafe46160c096da74cc80c4832c7e9b3190c` |
| 318 | `db89a5f83fa9ff3e45dd3c2132af7fb4d81288d8ac983bd9da789e64b2789d0b` | `ba33ca7edda01d0af8da8577d6eec980fef2323afe7c3733179f96912c4b0d6b` |
| 348 | `91e7cc04d40b343c4dadc85d0690fd583eb918a07aa4d661f0dbc2a8c24e4598` | `4093e31284e068345c3dab1234f329348aa57f5d8b1f65397962975eff35bc2e` |

I independently rehashed all 16 PNGs against the receipt, checked their dimensions and L/RGB modes, and checked all eight native grayscale pixel hashes against the receipt. All passed. Root's receipt separately reports full 442-frame raw/per-frame agreement, exit 0, 152,755,200 grayscale bytes and raw SHA-256 `1244ddf86418a17a1f4140c979268d33a5964a098da4fd6fd7817499bcb60b6b`, with three prior corruption-warning mentions. I did not rerun that decode or independently inspect the full raw stream. These remain diagnostic images, not clean/historical certification.

My read-only PNG checks used bundled Python 3.12.14; the view-generation receipt records Python 3.13.7/Pillow 12.0.0. An initial checker expected a `path` key and failed with `KeyError` before validating any product; the actual receipt uses a relative `name` key. After inspecting that schema, the corrected check passed. No source or receipt was changed and no failed check was counted as a pass.

Only this new independent observation note and the separately authorized short methods review are authored in this scope, in the dedicated worktree. Evidence/source rules keep query display, sampled feature association, material continuity, scale and physical interpretation separate. No human approval, new physical calibration, gravity result, force/cause ranking or legal promotion is claimed.
