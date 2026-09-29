# Critical consistency review of the sampled-sequence report

2026-09-19/20. Bounded textual/artifact review only. **I implemented this
unit's helper and tests and wrote helper-review.md. This is not an independent
code audit.** I did not view additional images, decode footage, retrieve media,
rerun the numerical review, or alter any frozen observation/source record.
Only this note was written. Evidence-falsification/source-of-truth review
distinguishes recorded observations, computations, attribution and inference.

## Result

No substantive inconsistency was found between the central bounded report
finding and the two visual records: the inspected endpoints fail the proposed
seamless join; neither numbered filenames nor common-looking surroundings
establish temporal adjacency, historical ordering or an unedited camera record.
This statement assesses consistency of the recorded observations, not a new
visual opinion. The strongest alternative—separately selected excerpts with
missing movement, replay or reordering—is expressly preserved in the report.

The report correctly discloses both deviations instead of using later records
to erase them. Four precise wording corrections identified below were addressed
in root's revised report, reread completely at the end of this review. None
changes the main finding or authorizes additional processing.

## Exact concerns and corrections

References are to report.md snapshot SHA-256
`336960ec70998c7b11a6e30b9217f26cdc1d4f031c5ff67a63c2bdf9a92a0f4d`.
The concerns remain below as review history, not as unresolved objections to
the revised snapshot `60c0e41b445eb2a28dadafab66b4362f5c30e524268a0639fe11bada57703fa9`.

1. **Common inputs versus authenticated source family (line 40).** “AI review
   of the same source family” could be read as establishing a common original
   camera/tape origin. The frozen records instead leave common origin and
   original chronology unresolved. The intended caution against duplicate
   corroboration is correct, but should use the narrower verified relationship:
   “All narrative scene observations are AI reviews of the same two acquired
   files; independent camera origins have not been established.” Strongest
   competing reading: “source family” means only the current CBS catalog group;
   that is reasonable but unnecessarily ambiguous in this provenance inquiry.
2. **Encoded time versus historical clock (table line 36).** “Exact source
   clock remains unverified” is ambiguous because source PTS/time bases have
   been checked. Replace with “historical camera/event clock remains
   unauthenticated.” This preserves the real limitation without casting doubt
   on the verified encoded locators.
3. **No proof of clock independence (table line 37).** “Independent clocks
   cannot be concatenated” should be “separately zeroed media timestamps cannot
   be joined into an event clock without an authenticated timing bridge.” The
   actual relationship of original camera clocks is unknown; independent
   zero points in these containers are not proof of independent cameras.
4. **Selected products versus decoded inventory (lines 64–65, minor).** “Each
   decode26 selected14 frames and38 selected15 frames” blurs decoding with
   selection. The retained inventory covers 578 and 475 frames; each run
   produces 26 and 38 selected PNGs. Suggested replacement: “Each run produces
   26 selected Dub5 14 PNGs and 38 selected Dub5 15 PNGs at native 720×480.”

## Priority issues checked and not found overstated

- **Root freeze deviation:** report items 1 and the root record agree that
  the observer summary arrived after 50 images but before root's remaining
  14 views and saved record. The root's claimed earlier boundary/index135
  recognition is explicitly not supported by a separately frozen file. The
  complete root pass must remain post-exchange, not blinded replication.
  I did not independently witness/reconstruct the view/message history.
- **Producer-review timing:** report item 2 distinguishes pre-run root
  code/test review and root-preflight from my helper-review note received
  after run01. The latter cannot retroactively satisfy FRAME-PLAN's promised
  written-review timing or constitute independent producer-code review.
  The frozen plan stays as history; the deviation is not silently rewritten.
- **Still identity:** index135 is only a qualitative comparison candidate.
  The report and observer explicitly withhold exact Figure5-157/158 identity;
  no registration, exhaustive frame search or quantitative match is claimed.
- **Attribution and order:** item 3 corrects acquisition.md's “secondary
  asserted segment order.” The failed join is the investigation's candidate,
  not a verified claim attributed to NIST or a secondary author. Sample order
  within15 does not establish when the two report stills were captured.
- **Nondetection:** weaker/obscured orange appearances are not treated as
  extinction, a complete pulse or no fire; bright cloud is not automatically
  flame. Large unsampled intervals and the absence of a pre-onset baseline
  remain visible. No six-second or whole-building fire conclusion follows.
- **Coverage/acceptance:** 1,053 inventory rows and 64 PNGs per pass, 2,106
  rows and 128 repeated instances overall, agree with the declared artifacts.
  They are not independent historical observations. Scientific/human
  acceptance stays false. The unchanged no-strict-causal-ordering statement
  agrees with the preceding unit's report and is not represented as equal odds.

## Actual scope and checks

Read completely: report.md, root-sequence-freeze.md, observer-sequence.md,
independent-review.md (including its recorded command), PROTOCOL.md,
FRAME-PLAN.md, root-preflight.md, acquisition.md and helper-review.md. Read
both top-level run receipts; made only a targeted text check of causal-ranking
language in the preceding unit's report. This is not a full previous-unit
or Luna-wide reevaluation. Root's revision additionally clarified the secondary
lead; its statements were checked against the preserved HTML lines 499–513.
That text names 14 (fire event in 15) and 45 (fire event in 44), explicitly
calls event time unknown, and does not assert immediate file-boundary adjacency.
This does not authenticate the secondary author's fire/cause characterization.

Actual read-only commands: `cat`, numbered `sed` reads, `jq` projections,
`shasum -a 256`, and an in-memory Python JSON/Markdown-table comparison.
The latter exited 0: all 64 observer ordinal/index/rational-time locators match
run01 frame JSON; both runs' selections match the manifest; all eight retained
probe/decode statuses are zero; the four probe stderr streams are empty; the
four source receipts retain the descriptive-only admission and false human/
scientific acceptance. Declared totals are 128 product instances / 2,106
inventory rows, and the freeze-order arithmetic is 26+24=50, 38−24=14.
This check did not open PNGs, recompute their hashes or independently reproduce
the separate review's full inventory/RGB traversal. No failed check occurred.

## Reviewed snapshot pins

| Record | SHA-256 |
| --- | --- |
| report.md, initial reviewed snapshot | `336960ec70998c7b11a6e30b9217f26cdc1d4f031c5ff67a63c2bdf9a92a0f4d` |
| report.md, revised and reread snapshot | `60c0e41b445eb2a28dadafab66b4362f5c30e524268a0639fe11bada57703fa9` |
| root-sequence-freeze.md | `ffc850a24c5385c50f1d684bf1670f840cecbd307bc5d6977af4058acb39eeb0` |
| observer-sequence.md | `a193075371078b2c78c4afa90800e7fcaf054d8e518aaf5b7452903891a3e0bd` |
| independent-review.md | `8bc2a41dc295016653bed0e56306c4dc31733ba141f8d79eea8a788d40752f68` |
| PROTOCOL.md | `878822418fae5d60096bbc509e101025cdd23463f062ce6fb7e0eb25c9098ef9` |
| FRAME-PLAN.md | `4c2870ab8775dd4a8b33fdbd59d32fafc2940fb14d7cee6cc19df829ad476297` |
| root-preflight.md | `9c86d00e9d754862751eec6c8e8df7f6996f439cf44f88b4aaf4711966f60419` |
| helper-review.md | `443cb54c3584a92e367ec1d0e0014c0dc84937551eb8db2c2d059e06a13de8ed` |

Review disposition at this snapshot: central bounded conclusion and disclosed
deviations supported by the records read; the four wording concerns are
resolved within the reviewed report's context. No remaining substantive
objection found within this limited scope. No independent code, visual or
human clearance.
