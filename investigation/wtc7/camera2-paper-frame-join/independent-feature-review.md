# Independent Camera 2 source-feature review

Status: frozen first pass, 2026-09-19T14:35:17Z. Research annotation proposal only. The reviewer is a separate agent pass, not an independent human expert. Scope is the four Figure 4 roofline labels and native frames 6593 and 6841; no trajectory, timing alignment, acceleration, symmetry, structural-cause inference, fresh decode, or additional native frame inspection.

The strongest visual joins are the paper's WC lower step-foot and NW outer right facade corner. EC has a plausible lower left step-foot in frame 6841 but no distinctly exposed corresponding point in 6593. NE remains a smoke-softened region in both fixed frames. The caption's cardinal names are source assignments, not an independently authenticated orientation or architectural map.

## Coverage and independence

Read the main repository workflow/navigation controls, supplied current repository instructions, worktree controls, investigation charter, evidence-falsification-auditor skill, and PDF skill. Read selection metadata only for file identity and the two declared frame records. No old target coordinates, native overlays, target panels, root annotations, or other agents' numerical findings were read before this freeze.

Viewed the entire PDF/printed page 13 at 150 dpi, including heading, section 3.1, Figure 4, six-color caption, the statement that the east penthouse had already collapsed in the pictured source image, and the continuation about NCSTAR 1-9 Figure 5-9. Also viewed the complete embedded Figure 4 raster (Image76.jpg, 863 x 638) and both complete native PNGs (640 x 480). The latter show surrounding buildings, smoke and image borders as well as WTC 7. No native image crop or interpolation was used. PDF text extraction additionally exposed pages 14 and 15 for page-number identification; their timing claims were not used to select coordinates or infer a source frame.

## Frozen proposal

Native coordinates use the upper-left origin, x right/y down. Bounds are subjective inclusive [xmin, ymin, xmax, ymax] boxes, not statistical confidence intervals. A region has no accepted point; do not turn its midpoint into a measurement. All centers are integer visual estimates.

| Paper label | Frame 6593 | Frame 6841 | Image feature and limit |
|---|---|---|---|
| NE / neon green | Region [299,145,320,164]; no center | Region [301,146,319,161]; no center | Left end of lower roofline is softened by smoke; a unique material corner is unresolved. The higher rooftop silhouette would substitute another feature. |
| EC / blue | Region [341,144,359,159]; no center | Center [352,151], bounds [348,148,356,155] | Lower left step-foot is distinguishable only in the latter fixed frame. It is a projected junction, not an authenticated material connection. |
| WC / orange | Center [425,154], bounds [422,151,429,158] | Center [425,154], same bounds | Lower right step-foot. The upper rooftop corner, assigned a separate light-blue marker by the paper, is a different feature. |
| NW / red | Center [454,156], bounds [452,153,457,160] | Center [454,156], same bounds | Outer right lower-roofline/facade corner, the strongest material-corner candidate. Cardinal orientation remains source-assigned. |

Equal rounded coordinates across two frames do not establish zero motion. These are tentative feature annotations, not a motion dataset or a demonstration of continuous visibility.

In the embedded source raster the visual marker centers are approximately NE [435,209], EC [504,209], WC [637,216], and NW [689,217]. These locate the markers themselves. Colored ring/cross pixels overwrite the source image and do not reveal the authors' exact Tracker selection. The rings identify neighborhoods containing plausible intended features; neither their centers nor their enclosed areas prove the true tracked material point. EC is below/left of the dark-green north-screen-wall marker, and WC is below the light-blue west-penthouse marker. Substituting the upper steps for those lower roofline labels would conflate features that the source itself separates.

## Claim ceilings and strongest objections

The repeated surrounding image arrangement supports a qualitative comparison of feature neighborhoods. No image registration was fitted and no native source frame was assigned to Figure 4. Similarity, smoke configuration, crop, or an assumed elapsed time cannot identify the paper's native frame. Frame 6593 is a fixed comparison baseline, not native-camera authenticity evidence.

The strongest objection to treating these as material tracks is projection: a lower roofline can meet the visible side of a rooftop structure in the image without that meeting being one persistent physical point. EC is especially vulnerable because the corresponding lower junction is not distinctly exposed in frame 6593. A screen-wall side, penthouse side, silhouette boundary, or occlusion can change apparent junction position. NW has the clearest apparent material corner, but independent geometry and higher-resolution unmarked source/project data remain necessary to authenticate the physical designation and exact tracked coordinate.

The native PNG hashes establish consistency with the selected local bytes. They do not establish historical video authenticity. The selection manifest records video hash 84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730; the video itself was not rehashed or decoded in this pass.

## Input pins and actual verification

| Input | SHA-256 |
|---|---|
| Chandler-Walter-Szamboti 2023 PDF | cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394 |
| Native f006593.png | 39bcb70c16ccc468133edf92b3a9dc9ea43edbc5692d82d8adcfc08cc22903a8 |
| Native f006841.png | a6c380c7aa74a8cecebe3577d679cdcf5fb26638522f9ad50fac839359a80f2c |
| Native selection.json | dda0cb2e9f17240562e2aafa9443f05df0c2047fd93d8a4e643233cf53e3175e |
| Extracted embedded Image76.jpg | b86c6900c3a1be5be83e206238f60bde11e2b71668b961ec8573abd3dc35220d |
| Full page-13 150-dpi render | 9d94e60afb2399dee3078c1593ded20bd1de52291f7a9294e1361ba16f9bc6ae |

`shasum -a 256` was run on all six files above. Native PNG hashes match the corresponding `selection.json` entries; the PDF matches the task-supplied pin. `jq` selected records 6593 and 6841, reporting source PTS 659301 and 684101 with time base 1/2997. `pdfinfo` reported 51 pages, unencrypted, 612 x 792 points. Bundled `pypdf` confirmed Figure 4 at PDF page 13 and extracted its embedded image without resampling. `pdftoppm -f 13 -l 13 -r 150 -singlefile -png` exited 0; it emitted fontconfig configuration/cache warnings. Complete visual inspection found legible page text and the intact figure/caption. `pdftotext` was unavailable (exit 127), so text extraction used bundled `pypdf`; no unavailable check is represented as passed.

The paper and native images remain unchanged. Temporary PDF review derivatives are under `/private/tmp/camera2-independent-Kw7CfA/`. Exact source paths and metadata are in `independent-feature-proposal.json`.

Next step: compare this frozen pass with the root's independently frozen pass. Address discrepancies on these same two native frames first; declare any proposed extra frames and the ambiguity they would test before viewing them.
