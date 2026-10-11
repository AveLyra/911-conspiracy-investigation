# Excerpt C visual coverage and sound correspondence

The full 25-second excerpt is now covered by preserved frames and visual screening. The approximate bang and dialogue markers are no longer outside the reviewed picture interval. At both nominal coordinates, the picture shows a large cloud among foreground buildings; it does not reveal a uniquely identifiable source for the reported sound. This closes a coverage gap, not the question of sound attribution or collapse cause.

## What is visible

Times below are coordinates in the uploaded compilation, not authenticated historical times. Excerpt C starts at track 430 seconds. The user's local markers remain approximate, with no numerical uncertainty interval supplied.

| Excerpt coordinate | Picture evidence | What it does not establish |
|---|---|---|
| 0 to just before 5 seconds | Wide elevated urban view. A substantial gray/brown cloud is already present behind foreground buildings. | An unobstructed initiation sequence or the cloud's independently authenticated source. |
| 5 seconds | Abrupt replacement by a closer cloud/building shot, between source frames 13049 and 13050. This shares the nominal coordinate of the reported start of white-noise-like sound. | Exact sound-onset coincidence, an edit-generated sound, or deliberate manipulation. |
| 11.866667 seconds | Another abrupt scene replacement, between frames 13255 and 13256, into a downward-looking cloud view. Early shake, blur and horizontal comb-like artifacts are visible. | The original elapsed time between shots or microphone synchronization. |
| About 13 seconds, reported bang | Nominal frame 13290, track 443 seconds, shows cloud behind lower foreground buildings and partly hidden by a dark high-rise at right. | A visible charge, a specific structural failure, or a unique physical source for the bang. |
| About 17 seconds, reported dialogue | Nominal frame 13410, track 447 seconds, remains within the cloud/foreground-building shot. | A visible speaker or an independently timed relationship between speech and collapse. |

The later shot continues through the end of the reviewed interval with cloud expansion and camera reframing. Neither reviewer recognized an unambiguous building roofline descent or resolved structural failure in this screening. Cloud and foreground obstructions can hide structural movement; this is not a finding that nothing moved. Camera tilt moves several visible buildings together on screen and must not be mistaken for structural displacement.

The bang marker is nominally about 1.1 seconds after the second picture cut. That arithmetic does not establish a physical sound delay: the user's timing is rough and original sound/picture synchronization remains unverified. A genuine collapse-related sound, another physical source, and an edited-recording origin remain unresolved alternatives. The excerpt must not be summarized as silence.

## Methods and verification

The [frozen protocol](protocol.json) extends the old half-open interval `[434,443)` to `[430,455)` without changing the old results. It acknowledges prior familiarity. The held video-only access copy is VID-WTC7-006, SHA-256 `1ea6063dac3847ee01969987bcee66991056d85ad61839ec301fb888a4456d87`. The audio report derives from a separately acquired soundtrack; matching compilation coordinates do not authenticate an original camera clock.

Each of two fresh runs saved 750 full-raster RGB PNGs: source indices 12900–13649, with exact presentation times equal to index/30. Source timestamps, dimensions and decoder output were checked. No interpolation, stabilization, crop, autoscaling or autorotation was used. RGB conversion is not colorimetric calibration. The same existing extraction functions first passed six synthetic assertions, including a nonzero timestamp fixture and missing-bin rejection. Both runs recorded Python 3.12.14, Pillow 12.3.0 and NumPy 2.3.5, along with source, implementation, protocol and binary hashes.

Both reviewers inspected all 25 labeled sheets, covering all 750 frames at 320×180 preview scale. Both also inspected the 25 fixed integer-second frames at the compilation's 1280×720 raster, plus both sides of each candidate cut: 29 presentations and 28 unique native frames. This is not native-detail inspection of all 750 frames, nor proof of original-camera resolution.

Root's [overview notes](root-overview-notes.json) and [native notes](root-native-notes.json) were frozen before receiving the separate reviewer's interpretation. The [independent review](independent-review.json) agreed on both cuts and the visibility limits. This is separate computational annotation of shared evidence, not blind review, independent historical corroboration, human acceptance or expert certification.

Actual execution in this directory:

- Bundled Python with `-B extract_full_c.py run01` and `run02`: both exit 0. The first sandboxed launch was denied permission to create the worktree output directory; a scoped authorized retry succeeded. No partial frame run preceded it.
- `verify.py`: exit 0, 1,692 checks passed. All historical PNGs, selected timing maps and overview sheets agree across runs; all 270 overlapping frames agree with the old audit. Of 828 paired products, only the two synthetic video containers differ in bytes. Their selected pixels and timing maps agree; container-byte cause was not diagnosed.
- `independent_check.py`: the reviewer ran its preserved body separately; root then reran the saved file with `python3 -B`, exit 0. It checked actual PNG bytes, geometry, exact rational times, fixed selection, all old overlaps and the current source hash without importing the extraction implementation.
- Existing-output refusal passed and preserved every existing run01 file. [Verification details](verification.json) and the two run receipts retain the checks. Counts measure check coverage, not scientific confidence.

## Consequence and next test

The image coverage blocker for C is resolved at the declared screening level. Sound identity, original synchronization, recording sensitivity and a complete accepted sound-event inventory are not resolved. The next discriminating source task is to locate and compare a longer continuous version of the camera segment around the reported bang, with its own soundtrack and provenance. More pixel inspection of the same obscured excerpt cannot supply that missing source relationship.

No causal ranking, accepted Sherlock finding, legal record, source media, prior audit, or user-only decision changed. This remains local research; no commit, push or transmission occurred.
