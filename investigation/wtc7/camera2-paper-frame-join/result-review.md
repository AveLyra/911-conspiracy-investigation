# Bounded result cross-review

2026-09-19. Computational review by the agent that produced the frozen independent feature proposal. This is a fresh arithmetic and wording check, not human clearance, a second independently blinded annotation, architectural authentication, or validation of the historical trajectories. No original file was changed. No additional image, thumbnail, video frame, or measurement was viewed or generated during this cross-review.

## Result

All eight comparison rows reproduce directly from the original root and independent JSONs. There are eight unique frame/label keys, five candidate-point pairs and three region-only pairs. All eight box intersections are nonempty. The five center differences and all normalized status/overlap values match both `verification01.json` and `verification02.json` exactly. I did not read or run `verify_join.py`.

| Frame | Label | Normalized class, both files | Independent minus root center | Computed box intersection [xmin,ymin,xmax,ymax] |
|---|---|---|---|---|
| 6593 | EC | Region | Not defined | [347,146,358,157] |
| 6593 | NE | Region | Not defined | [299,145,319,160] |
| 6593 | NW | Candidate | [-1,0] | [452,153,457,160] |
| 6593 | WC | Candidate | [1,0] | [422,151,428,158] |
| 6841 | EC | Candidate | [0,0] | [349,148,356,155] |
| 6841 | NE | Region | Not defined | [301,146,315,159] |
| 6841 | NW | Candidate | [-1,0] | [452,153,457,160] |
| 6841 | WC | Candidate | [1,0] | [422,151,428,158] |

The intersections are computational comparisons of subjective boxes, not improved error bounds. No union, midpoint, average center or consensus measurement was substituted into either proposal. Region rows retain null centers.

## Report and addendum review

The reviewed report correctly retains the root's exposure before its written freeze, the independent reviewer's earlier saved proposal, and the prohibition on counting agreement as a blinded replication. The addendum expressly acknowledges that formal protocol failure. This cannot be repaired by agreement or by this cross-review.

The report and addendum also preserve the complete embedded Figure 4 raster viewed by the independent reviewer in addition to the complete page render. That was extra rendering detail from the same source image, not another independent scene observation. Source-assigned compass names, uncertain material identities, projected-junction limits, and the lack of an exact Figure 4 native source frame remain explicit. The conclusions do not force four authenticated or continuously trackable material points.

I read `../camera2-target-trackability/targets-proposal.md` only after my first-pass proposal had been saved and hashed. It expressly defines T2 as the upper step endpoint [424,144], prohibits substituting the lower junction, and assigns no compass or physical-component identity. The present WC lower-foot candidate near [424-425,154] is about ten native pixels lower in the common baseline. The report's distinction is supported and does not falsely accuse the earlier study of treating T2 as WC. The T1-to-NW statement remains a neighborhood consistency statement, which is the appropriate limit. The report's later-frame statements about f6946/f6961 were not independently audited in this bounded review; the baseline-only proposal does not itself support those later statements.

Two precise editorial improvements would make the report more inspectable; neither changes the reproduced rows:

1. Replace `Their status classifications agree and all eight subjective boxes overlap.` with `Both proposals classify the same five rows as candidate points and the same three as regions; their detailed descriptive status strings differ. All eight subjective boxes overlap.` The arithmetic normalizes status by whether a center exists; it does not establish agreement of physical-feature type or confidence.
2. Link `verification01.json` and `verification02.json` separately where the report says `both verification runs`. The current link resolves only to run 01. The two output files have identical bytes, which is compatible with repeatability but is not evidence of independent code or visual validation.

For the later-frame historical statement, add a direct citation to the existing trackability report or result rows supporting the specific f6946/f6961 conclusion; do not imply that the linked baseline-only proposal contains those results. No additional historical measurement was requested or performed here.

## Alias and thumbnail prose limits

At the reviewed report hash, the alias paragraph explicitly said the metadata/thumbnail follow-up was pending. I treated it as pending, not as a completed negative search or a recovered-settings result. Subsequent integration of the settings receipt and thumbnail review is outside that report snapshot.

At root's bounded extension request, I read `thumbnail-review.md` as prose only. I did not view either thumbnail and therefore do not independently verify its image observations. The prose correctly says the images are 320 x 228 saved application screenshots, not native frames; it excludes reading plot/table values as measurements. Its source-relatedness conclusion is explicitly plausible rather than established, and it preserves the alternatives of related or differently processed footage and an illustrative project differing from the publication's actual analysis.

The thumbnail prose appropriately rejects byte inequality as sufficient to exclude related footage, while also rejecting automatic transfer of scale, timing, rotation, selections, source exposure sequence, or publication history from resemblance. Its proposed next test declares member/frame selection, static-scene anchors, provenance and ambiguity before further decode. I found no source/inference overstatement requiring a change in that prose. This is a review of the stated limits, not visual confirmation of the thumbnails or clearance to perform the proposed decode.

## Inputs and actual checks

| Reviewed file | SHA-256 at review |
|---|---|
| root-feature-proposal.json | 64691f300a697a459cc35af2417e46ed2fc76759567bec586892c49876e5a687 |
| independent-feature-proposal.json | b2ff33b771893a124f0ed6ce2f77bfb605d6c29c098d761e1c8b192db5612c8a |
| report.md, pending-alias draft | 91643a4f21c578ca5f551debde30ff3d875c0913082d00923c3d6b68c3bed44f |
| ADDENDUM-01.md | 5cb6e8c9dd32f244a0f98ea35dcefdc226976cf22b76d84d20bb34da1c1dec79 |
| verification01.json | bd69d3e98ae6a8aa924208456fe44d02721d67a20a0f35d8fff16ad9a0119a6d |
| verification02.json | bd69d3e98ae6a8aa924208456fe44d02721d67a20a0f35d8fff16ad9a0119a6d |
| older targets-proposal.md | 4dba7ccad1a54749f9543503905bdfc291b5fd3d8a69af55b50d3e9422c93d65 |
| thumbnail-review.md | dd2191313327f2ddbaab48b9229dd5ead74cb6252be4c115c0cc39e2ba48cbd3 |

`shasum -a 256` produced those input pins. A separately written `jq -n --slurpfile root ... --slurpfile independent ... --slurpfile run1 ... --slurpfile run2 ...` expression joined root `annotations` to independent `features[].observations[]` by frame and label. It selected independent `bounds // region`, formed the rectangle intersection with coordinatewise max of lower bounds and min of upper bounds, computed independent-minus-root centers only when both existed, and compared the resulting sorted rows to each recorded verification array. It exited 0 and returned row_count 8, unique_keys 8, candidate_count 5, region_count 3, run1_matches true and run2_matches true. No test failure was suppressed.

This independent arithmetic check does not repeat root's video/PNG/luma/PTS validation, authenticate the camera's history, or audit the settings review. The unchanged independent proposal hash confirms preservation of its pre-exposure first pass. The investigation and human-review prerequisites remain open.
