# Independent saved-keyframe source review

September 12, 2026. Bounded computational AI source/numeric-state review under [KEYFRAME-ADDENDUM.md](KEYFRAME-ADDENDUM.md), the investigation charter and privacy/preservation controls. This addendum was declared **after initial fits were inspected by main**. It is a post-result source follow-up, not prospective confirmation of independent measurement. Only this new review is authored; no source, checker, export, original observation or fit is changed.

## Result and claim ceiling

**The numeric membership result is independently confirmed.** Each of the two original PointMass sibling objects has an explicit, nonempty saved `keyFrames` array with exactly 71 unique indices: `138,141,...,348`. Each set/list exactly matches that object's own saved `framedata` indices. There are zero saved positions outside the key set and zero keys outside those positions. These values and the derived membership/fallback statuses match [keyframes01.json](keyframes01.json).

This supports the narrow statement that **this captured saved state does not label any of these 71 positions as a non-key interpolation gap**. It does not prove manual marking, separate independent measurement of each point, faithful original camera exposures, absence of interpolation earlier in the project's history, correct feature identity, historical annotation precision or physical accuracy.

| Generic track | Explicit nonempty keys | Numeric indices | Saved non-key positions | Extra keys |
|---|---|---|---:|---:|
| track01 | yes | 71; 138 through 348, step 3 | 0 | 0 |
| track02 | yes | 71; 138 through 348, step 3 | 0 | 0 |

The observed small residuals prompted this check; they are not used to validate these source-state conclusions or to infer a marking procedure. No fitted values were inspected in this review.

## Tagged source semantics actually checked

Read the preserved `tracker-6.1.2-PointMass.java` at lines **705-728, 1174-1332 and 2933-2960**. The additional lines after 1315 complete the interpolation function and show its return; no whole-program audit or historical executable equivalence is claimed.

- `autoMarkAt` calls the superclass method and adds the frame number to `keyFrames`. Its comment and the interpolation comments explicitly include manually **or automatically** marked steps. Automatic marking is therefore a concrete alternative to the inference “all keys means all manual.”
- The interpolation methods traverse selected clip steps between key positions and generate/change intermediate x/y by a linear fraction of the step-number range when autofill is active. The shown branch can delete existing intermediate steps when autofill is off. This establishes an available program pathway, not that it was used on this historical project.
- The loader clears the key set, imports a nonempty saved numeric key array when present, and otherwise adds all existing non-null positions as keys. Thus missing/empty metadata would not justify a historical claim of no interpolation. The current two arrays are explicit and nonempty, so that missing/empty fallback is not selected **if this inspected loader path is used**. It remains possible for an earlier history or a different loading/marking process to have produced the current all-key state; no such history is demonstrated here.

Source comments and code distinguish key/non-key behavior, but key membership is not an audit trail of how, when or by whom a coordinate was obtained. Reading a tagged source file does not reproduce the author's original binary, engine state or session history.

## Independent numeric-only check

The independent read-only helper did not import or run `check_keyframes.py`. It:

1. Read the exact 65,128-byte known-hash project; required SHA-256 `955d1c2d00d7c287f4f235063eb603a0080cf0941595a5419aa7c94726c1a41c`, bounded its size, and rejected DTD/entity declarations before parsing inert XML.
2. Selected exactly two PointMass sibling objects by the fixed class/path. For each, required one array-valued `keyFrames` field containing one string child. It accepted only the full ASCII grammar `\{\s*[0-9]{1,3}(?:\s*,\s*[0-9]{1,3})*\s*\}`, then converted its comma-separated numeric tokens to integers in memory. No raw list string, arbitrary XML field/name, private path or source coordinate value was displayed.
3. Required every key in 0..441, unique and increasing. Independently read only the numeric bracketed indices of that object's `framedata` children, not their x/y contents; required exactly `list(range(138,349,3))`. Compared those indices with the parsed keys and the saved result's two numeric arrays/counts/difference lists. Both matched exactly.
4. Rehashed the original project afterward and confirmed it unchanged. Only counts, first/last/step, generic track IDs, expected hashes and derived check outcomes were emitted.

The helper used bundled **Python 3.12.14** and exited 0. The original project XML was never emitted or executed. This pass did not open the 71-point coordinate export or original arbitrary track names. The numeric difference-list comparison is to the actual captured `framedata` index lists and the saved keyframe result, not a repetition of the producer's membership calculation imported as trusted code.

## Failed-checker recovery and retained failure

The addendum records that the initial indexed-int parser exited 1 with `unexpected_integer_array_shape`, before exporting keyframe values. A shape-only follow-up then identified the braced integer-list serialization, followed by a prospective normalization amendment. That earlier attempt remains a failure, not a successful extraction retrospectively relabeled.

I read the complete current checker and reversed **only** the documented normalization block in memory:

- Locate its unique line `            children=list(arr)\n`.
- Remove through and including the unique later line `            for pos,entry in enumerate(children):\n`.
- Replace that span with `            for pos,entry in enumerate(arr):\n`, preserving all other bytes exactly.

The current checker has **3,969 bytes**. The reconstructed checker has **3,382 bytes** and SHA-256 **`52caaf25b5e00e9c46b155ba60df5fd546c27d1a0ec3dbd1c8492fe41caca02b`**, exactly the recorded failed-checker identity. Nothing was written over either source or current checker. The reconstructed checker was **not executed**; this verifies exact byte recoverability, not a new replay of the original process. The current raw array's string child would fail the old indexed-int type gate, independently corroborating the declared format mismatch without exposing its text.

This is a representation adaptation, not evidence of missing scientific data or changed historical coordinates. The numeric-only normalization is compatible with the observed serialized values; it does not recover a historical marking history.

## Exact input pins and coverage

| Input | Bytes | SHA-256 |
|---|---:|---|
| `KEYFRAME-ADDENDUM.md`, fully read | 3010 | `b10094afe4004fd2a0da2b55a555256adf793ae344904ecfabe220f4d7bfda42` |
| `check_keyframes.py`, fully read, not executed | 3969 | `91329cbac3cec654c4534d9f8128a9d3c42d303c2439a5a7c73e6286f495668f` |
| `keyframes01.json`, numeric result and pins read | 3573 | `1c7b63983bbd2d3e7b075b2d743d32612f09f63a1eb1736b7824ef6b245e1793` |
| Original public project, restricted numeric-field traversal only | 65128 | `955d1c2d00d7c287f4f235063eb603a0080cf0941595a5419aa7c94726c1a41c` |
| Tagged PointMass source, specified ranges only | 105716 | `e382d1287948e6bb7ca5e72af902e42a88cc5a1828d0786696815116558d5d6f` |

First three paths are under `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-conditional-trajectories/`. The read-only project is `/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/nested/Camera3-test_Camera3-test.trk`. The read-only tagged source is `/Users/admin/docs/911/research/sherlock-wtc7-investigation/tracker-clock-semantics/sources/tracker-6.1.2-PointMass.java`.

The evidence-audit skill required preserving the all-key positive result, the failed representation assumption, automatic-marking/fallback alternatives and historical limits together. The source-of-truth skill kept captured numeric state distinct from original authorship/history and protected all frozen records. No new image viewing, decode, fit, project application, private metadata disclosure, external/source retrieval, model/case access, causal inference, human approval or authority promotion occurred. This finite source follow-up is complete.
