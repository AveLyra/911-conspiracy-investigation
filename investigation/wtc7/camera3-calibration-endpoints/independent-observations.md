# Independent Camera 3 calibration-endpoint observations

September 12, 2026. Research-only computational AI observation under the [protocol](PROTOCOL.md) and investigation charter. These descriptions were saved before reading any root observation note, inferred endpoint labels or future report from this unit. Shared saved coordinates, seven candidate floor pairs, prior case imagery and prior calibration reviews were already known. This is separate annotation, not a clean holdout, human review or historical authentication.

## Independent result

The upper saved query location meets the building's repeated horizontal facade pattern below the large dark rectangular upper-facade feature. It is not a roof/parapet outline or a uniquely resolved architectural corner. I cannot identify its precise stripe phase as a floor slab, window top or window bottom from these images.

The lower saved query location is at or just inside the bright foreground structure's left-side occluding edge. The target facade continues visibly immediately to its left, but the query location does not give me a clean, unoccluded second target-window/floor marker. Treating the two saved endpoints as two identified corresponding window tops would therefore exceed my independent observation. The foreground edge and target stripe can coincide in projection without being the same material feature or depth.

The visible repetitive facade pattern over approximately this span is compatible with roughly **14-16 band-to-band intervals**, with about 15 a plausible visual count. That is a subjective row-count envelope, not an exact endpoint-to-endpoint floor count, fitted spacing, metric estimate or independent confirmation of the supplied 58.293 m. Absolute floor labels remain unresolved. I do not choose any of the seven dimensional pairs or infer a count of failed stories.

## Fixed query locations and display mapping

Saved image coordinates, not newly estimated feature coordinates:

- Upper tape endpoint: `(414.3770672546858, 196.24035281146615)`.
- Lower tape endpoint: `(416.95700110253586, 390.7276736493937)`.

The native images are 720 x 480 grayscale. The supplied crop is the half-open native rectangle `[300,80,510,425)`, enlarged exactly 3x nearest-neighbor to 630 x 1035. Its origin-relative coordinate mapping is `(x_c,y_c) = (3(x-300),3(y-80))`; this locates the queries near `(343.13,348.72)` and `(350.87,932.18)` in the crop. For an integer source pixel, the enlarged evidence is its corresponding 3 x 3 block, not a newly resolved subpixel. These display positions derive from supplied coordinates, not independent landmarks.

The envelopes below instead describe my subjective native-coordinate association region around the visible feature at each query. They are not confidence intervals, estimates of saved-coordinate error, or uncertainty on historical material position. An extended stripe is not localized in x as a unique point; the x ranges identify the inspected neighborhood only.

## Frame-by-frame observations

| Diagnostic index and encoded time | Upper query: independent appearance / association envelope | Lower query: independent appearance / association envelope | Repetition and correspondence limits |
|---|---|---|---|
| 138; PTS 9200 at 1/1000 s = 9.2 s | Repeated slanted-in-image light/dark facade bands below the dark rectangular upper feature. Query is near a pale inter-row stripe / adjoining darker-row boundary, not the external roofline. Inspected association region `x=410..420, y=193..201`; exact top/bottom/slab phase ambiguous. | Near the bright foreground structure's left vertical edge, with target banding immediately to the left. Inspected edge/occlusion region `x=414..420, y=387..396`. Underlying target marker at the exact query is unavailable/ambiguous; no clean window corner localized. | Roughly 14-16 repetitive intervals over this vertical neighborhood; about 15 plausible when tracing similar stripe phases. Lower endpoint's occlusion and upper stripe-phase ambiguity prevent a unique direct count. |
| 141; PTS 9400 at 1/1000 s = 9.4 s | Same type of banded-facade neighborhood is visible at the query. Independently inspected association region `x=410..420, y=193..201`; precise stripe boundary remains blurred/ambiguous. | Bright foreground occluding edge remains at the lower query, target bands visible to its left. Independently inspected region `x=414..420, y=387..396`; no separately identifiable target-window top at the query. | Again approximately 14-16 repetitive intervals, not a new independent dimensional observation. Fine changes in blur/intensity do not resolve the phase or occluded endpoint. |
| 168; PTS 11200 at 1/1000 s = 11.2 s | Upper banded facade is still recognizable at the fixed query. Independently inspected association region `x=410..420, y=193..201`; cannot promote a light/dark transition into a named floor level. | Lower query remains at the bright foreground/target-facade overlap neighborhood. Independently inspected region `x=414..420, y=387..396`; target endpoint identity stays unavailable/ambiguous. | Similar approximate 14-16 interval count. Changed smoke/upper imagery supplies no absolute floor numbering or hidden endpoint. No physical motion/onset conclusion is made from similar association envelopes. |

These are three separately viewed frames. Equal reported envelopes reflect the same coarse visibility/localization limit after each inspection; they are not a claim of pixel equality, immobile camera, exact feature continuity or equal physical position. The recorded per-frame pixel hashes are different.

For the tentative repetition count, I traced the repeated light/dark facade bands through the visible strip just left of the lower foreground obstruction, roughly native x=400..410, and related their slanted image courses to the query neighborhoods. The apparent stripe phase at the top, the lowest partly obscured stripe and the short lateral extrapolation each permit an off-by-one choice. This is why a range is retained. A facade cycle is not automatically one architectural story; the association requires the dimensional/image join rather than the supplied tape value as a counting rule.

## Competing assignments and useful inference

1. **Corresponding facade features about fifteen regular intervals apart.** The repetitive pattern and near-fifteen visual count are positive evidence for this candidate, consistent with the lab's intended method. The lower feature could continue behind the foreground obstruction and have been placed by extending a visible band. These images do not establish that extension, the endpoint phase, exact count or absolute floor labels. Consistent window offsets could cancel, but their equality is not observed here.
2. **Unlike phases, a foreground boundary, or an off-by-one row selection.** This remains live because the upper marker is not a unique architectural level and the lower query meets an occlusion boundary rather than a clean target marker. It is not evidence of manipulation or proof that the assigned scale is wrong. Resolving a band to the left of an obstruction is not equivalent to resolving its hidden material endpoint at the query.

I would admit the assigned scale as an explicitly conditional configuration and the near-fifteen repetitive span as qualified image support. I would not call the tape physically validated, select 30-45 or another numbered pair, or compute an acceleration from this source join. A source-linked higher-quality calibration frame or drawing/image annotation that distinguishes both selected feature phases, floor numbering and the foreground overlap is the precise remaining discriminator. Another unlabelled enlarged copy would not create the missing resolution or architectural identity.

## Source-to-project review before image release

The sanitized saved project names only the safe basename `Camera3.wmv`, saves video frame count 442, start frame 138, step size 3 and step count 102. Both separately listed PointMass arrays have 71 marked indices and contain all three selected indices. The tape is recorded as fixed. This supports the declared selection but does not mean all selected or fixed query positions are physically identified.

The prior run02 diagnostic receipt and map agree on the source hash and a 442-frame sequence. Its full raw grayscale result is 152,755,200 bytes with SHA-256 `1244ddf86418a17a1f4140c979268d33a5964a098da4fd6fd7817499bcb60b6b`. The prior three warning indices are 37/55/63, not these three selections. The old clean-decode rejection and diagnostic-only admission limit remain intact; an unflagged frame is not certified pristine.

The new receipt attributes identical current hashes to the public outer and nested/videos copies and reports full raw/per-frame agreement with that prior diagnostic. Duplicate-copy identity plus the saved basename/frame count supports present-file correspondence, not a reproduction of the historical Tracker raster, decoder or time state. I did not reopen or emit the original TRK's personal path fields and did not rehash the video copies myself in this pass.

The three diagnostic PTS values are 9.2, 9.4 and 11.2 seconds on that encoded diagnostic clock. Saved analysis start time zero must not replace these times, nor may present PTS be relabeled as the historical application's engine/exposure clock. The three images cover an early selected interval, not the earliest physical onset or the whole event.

## Actual viewing, independent checks and pins

Viewed all **3 native frames plus 3 complete unmarked crops**, individually at original supplied sizes: `run01/frame-0138.png`, `frame-0141.png`, `frame-0168.png` and `run01/crop-0138.png`, `crop-0141.png`, `crop-0168.png`. No other new image was viewed. I read the protocol, current charter/privacy rules, applicable evidence/source skills, the prior WMV diagnostic report, selected receipt/map fields and sanitized settings. No root observation/label/report from this unit was opened before saving this file.

I independently rehashed all six PNG files against the new receipt; confirmed native `L` mode/720 x 480 and crop `L` mode/630 x 1035; matched each selected native pixel hash to both new receipt and prior map; matched the three inherited PTS/time-base/rational-second records; and checked every crop pixel against the declared native crop's 3x nearest-neighbor mapping in memory. All these bounded checks passed. This did not run the video decoder or independently recheck all 442 fresh frames; that full-sequence result remains attributed to root's receipt. No image or check artifact was written.

Current input pins:

| File / scope | SHA-256 |
|---|---|
| This unit `PROTOCOL.md` | `8c23c82af39edf6cc1ff6627e3c70e38728b599c830b41865ec457d3f7950981` |
| This unit `run01/receipt.json` | `8ae034a788f93a8c8c80704c4fe4b675105065be2a28567e9c4c21cf47a83219` |
| Original public `camera3-provenance/kit-inventory/run-v1/saved-tracker-settings.json` | `ccfd9c4de098539680caf9f296eb5ea784ade27497d860a32284285e577cefeb` |
| Original public `camera3-recording-comparison/wmv-diagnostic/run02/receipt.json` | `11bb4f4d44031621322b068648647f4e0c437f61510d3b4e6d380e8fc62cc227` |
| Original public same run `default-frames.json` | `8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2` |
| Public WMV source/alias, attributed to both receipts, not newly rehashed here | `48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722` |

Original public relative paths above are rooted at `/Users/admin/docs/911/research/sherlock-wtc7-investigation/`. This unit is rooted at `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-calibration-endpoints/`.

| Index | Native PNG SHA-256 | Crop PNG SHA-256 | Native grayscale pixel SHA-256 |
|---|---|---|---|
| 138 | `8d16b44ea88ac210579b1c7b8c67ba202a400009f63d4cb9a80fa294f85b5abb` | `6b0cbb98a951fadf36aaed274e0edafeb773e1ef6d6b8afdf8eb8777118a2792` | `5c91a1376ac74ff0b015d13984ee6618f61ba37ebdb696136192d339b257e972` |
| 141 | `01aa019a70e8eabb429e527ef86e466a5a8e81db627ec611604d80755e3fff92` | `fe14e9601dfe8259ae0609164e05eb94b2cf29b6ce5752d7deb5360199459e51` | `0fd466995d6160fff8281db29aac3f887ea425d25f7e01bf026d31bbcf105d09` |
| 168 | `e53a02c70cbe9107a3042fab4dbdf3fbd20a809ee49480d3b8b6c76f2f07434d` | `c28914fcf01f6e948058cdf8d45bec0834b41c8775a939967d8f345b6c219b77` | `fc3d6c167692d66dbaea5799e71504ce40f1ea1bab8fac039a2e3d4eb0870e53` |

Root's retained extraction receipt reports Python 3.13.7/Pillow 12.0.0. My separate in-memory metadata/PNG checks used the bundled Python **3.12.14**; these are different executions and are not described as the same runtime. No raw diagnostic log was opened. Only this new independent observation file is authored; no original source, frozen record or root procedure is changed. The evidence skill prompted competing feature assignments and distinct uncertainty types; the source skill prevented diagnostic image identity from becoming historical/physical authentication. No authority promotion or cause ranking changes.
