# Independent C observations — frozen before comparison

Date: 2026-09-12. Status: exploratory image annotations in the investigation worktree; not a canonical case fact, expert report, architectural identification, or causal finding.

Protocol SHA-256: `d8adc5afa2e8f9b5d986b0d3042f8b420509478fc84dd5dfd7ea26016415c27e`.

Input receipt: `../camera3-late-reannotation/views01/receipt.json`; SHA-256 `8bf54e80ccb0eb823cd9a09fc45e285fa4a649c166aaf2b26d551c13782c3161`. The receipt hash matches the protocol. All 44 selected native/crop files passed SHA-256 comparison against the receipt's product entries before viewing. Hash agreement establishes integrity relative to that receipt, not historical authenticity.

I viewed every selected native and crop image through `view_image` with original detail. The 22 samples are frame 258 and frames 288 through 348 in steps of 3. Native images are 720×480; the supplied crop is [295,125,535,375), nearest-neighbor factor 3, with external native-coordinate rulers. No additional decode, crop, interpolation, enhancement, or source acquisition was performed.

The observable is C: the **lower-right** corner of the prominent dark upper-facade band, where its right termination meets its lower sloping edge. The overall building corner and the band's upper-right corner are different features. Coordinates are integer native pixel centers (x rightward; y downward). Bounds are inclusive, subjective localization ranges for the visible junction; they are not statistical confidence intervals. Placement and box width follow local visibility and transition width, without fitting or extrapolation.

Before this freeze I did not read root C annotations, earlier A/B coordinate arrays, fitted results, or geometry conclusions. This is an independent annotation pass by a separate computational observer on shared image derivatives. It is not an independent camera, historical holdout, human measurement, or structural expert review.

Coverage is 20 localized samples out of 22. Frames 345 and 348 are null because the original junction cannot be separated confidently from foreground occlusion. A remaining dark band segment does not establish that the original corner is visible. These nulls are part of the frozen observation set, not missing values to interpolate.

| Frame | x | y | Inclusive x bounds | Inclusive y bounds | Visibility / identity note |
|---:|---:|---:|:---:|:---:|---|
| 258 | 420 | 182 | [418, 422] | [180, 184] | Lower sloping edge and right termination of dark band both visible. Rounded contrast transition spans several native pixels; center is the visible lower-right junction, not the building edge. |
| 288 | 419 | 183 | [417, 422] | [181, 185] | Dark band right edge and lower oblique border recognizable. Lower-right junction is soft; placement includes the dark-to-gray transition width. |
| 291 | 419 | 183 | [417, 422] | [181, 185] | Same visible contrast junction. Lower band edge remains distinct from the lighter horizontal facade strip below; corner is slightly rounded. |
| 294 | 419 | 184 | [417, 422] | [182, 186] | Right termination is visible against lighter facade. Lower edge reaches it through a short blurred transition; no competing local corner selected. |
| 297 | 418 | 185 | [416, 421] | [183, 188] | Same band junction recognizable. Vertical termination is softened and lower boundary spreads into the facade stripe, motivating a slightly taller box. |
| 300 | 418 | 187 | [416, 421] | [185, 190] | Band lower-right corner remains recognizable; right boundary is diffuse but not obscured. Box covers the softened end of the lower oblique border. |
| 303 | 418 | 189 | [416, 421] | [187, 192] | Visible right termination meets the lower dark edge. Nearby facade texture below is not used as the feature; blur limits precise junction placement. |
| 306 | 418 | 192 | [416, 421] | [190, 195] | Lower-right band junction is still directly legible. Right-side contrast becomes hazier, so the box includes transition pixels on both sides. |
| 309 | 418 | 196 | [416, 422] | [193, 199] | Recognizable band endpoint with diffuse lower-right meeting region. Neither facade marks below nor the upper band corner are substituted. |
| 312 | 417 | 202 | [414, 420] | [200, 205] | Band lower-right junction remains distinguishable from adjacent lighter strip. Soft right termination and rounded corner justify a broader horizontal range. |
| 315 | 416 | 210 | [413, 419] | [207, 213] | Same contrast junction recognizable, with hazy pixels adjoining the vertical termination. The visible lower border supplies placement rather than a projected track. |
| 318 | 416 | 220 | [413, 419] | [217, 223] | Lower-right corner remains a recognizable dark-to-light contrast junction. Low local contrast broadens lower-edge placement; visible bright strip below is excluded. |
| 321 | 416 | 231 | [413, 419] | [229, 234] | Band endpoint remains recognizable despite haze. Right termination and bottom sloping edge meet in a short rounded region above the brighter facade strip. |
| 324 | 416 | 242 | [413, 419] | [239, 246] | Dark band's lower-right endpoint remains visible. Lower border is more diffuse vertically than right border; box includes the corner transition, not the separate light line below. |
| 327 | 416 | 255 | [413, 420] | [252, 259] | Recognizable same band termination with soft lower edge. Haze and reduced contrast broaden both coordinates while the corner can still be assigned without feature switching. |
| 330 | 416 | 271 | [413, 419] | [268, 274] | Lower-right junction remains visible, with blocky compression/blur along the band's lower edge. Bounding region follows the actual local transition. |
| 333 | 416 | 286 | [413, 419] | [283, 290] | Visible band termination remains identifiable. Lower edge is locally uneven and soft, so bounds encompass that meeting region rather than a single sharp pixel. |
| 336 | 416 | 303 | [413, 420] | [300, 307] | Recognizable lower-right contrast junction. Lower dark boundary spreads over several pixel rows; surrounding facade appears washed out, widening the vertical bounds. |
| 339 | 416 | 320 | [413, 420] | [317, 324] | Right termination and lower border are visible above the foreground tank. Haze and uneven lower edge limit precision but do not create a competing feature identity. |
| 342 | 416 | 337 | [413, 420] | [333, 341] | Last clearly separated lower-right junction above the foreground tank. Right termination and lower border are visible but blurred; vertical range includes the diffuse corner while staying on this band. |
| 345 | null | null | null | null | Lower-right band corner is not independently localizable: the right termination coincides with the foreground tank's left occluding edge, while haze softens the lower border. A visible band segment is insufficient to distinguish the original junction from the occlusion boundary; no continuation is inferred. |
| 348 | null | null | null | null | Same lower-right corner is obscured by foreground tank/building and haze. The remaining dark band segment reaches an occluding boundary and crop bottom, so the original edge intersection cannot be localized; no extrapolation. |

The direct observation is a recognizable image contrast junction in each non-null frame. The precise center and bounding choices remain observer judgments on blurred, compressed imagery. For localized samples the strongest alternative placement is another pixel within the same softened boundary region; for the two nulls, the apparent corner may instead be an occlusion boundary. Higher-quality source imagery or a reproducible disagreement locating a different visible boundary could weaken these placements.

The architectural identity and correspondence to a single physical material point remain unestablished. These annotations alone do not demonstrate rigidity, motion of the whole building, acceleration, support state, or collapse mechanism. Source images, existing annotations, other analysis files, and canonical/legal materials were left untouched. Only this Markdown record and its JSON counterpart were created.
