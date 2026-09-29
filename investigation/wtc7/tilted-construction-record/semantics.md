# Held-code semantics for the construction-record locator

2026-09-24. Bounded source-code review, completed without opening omitted raw TRK fields or inspecting new locator results. Research only. The complete [protocol](PROTOCOL.md), including its pre-execution clarification, was read and pinned at `47d55648820416cb92d35d562335a6332a8eff490c9a3e861ecda3a54cd6e030`. Main AGENTS, WORKFLOW, START-HERE and the investigation charter control. The frozen [method follow-up](../tilted-point-frame-audit/method-followup.md) supplies the question, not an answer inferred from metadata.

## Result and ownership

The strongest directly established text locator is **root TrackerPanel `description`**. Runtime per-track descriptions also exist, but their exact serialization field remains unverified because the held PointMass loader delegates common track state to an uninspected `TTrack.Loader`. A direct-track `description` is a reasonable locator candidate; it must not be described as a fully traced serializer contract yet.

Neither an ordinary PointMass record nor saved key membership is a complete construction/editing history. The code distinguishes software state from an analyst's choice of physical or geometric observable. A free-form description, if later safely inspected, would be a source assertion, not validation that its method was used correctly.

All exact serializer interpretations below are conditional on the **inspected source bytes**, previously attributed to Tracker 6.1.2. This review does not authenticate the historical executable, libraries, runtime defaults or saved file's complete editing history. Source citations use literal line numbers in the pinned files below.

## Direct primary support

| Field or behavior | Owner / function and exact lines | Supported interpretation and limit |
| --- | --- | --- |
| `description` | `TrackerPanel.getDescription/setDescription`, 581–597; `TrackerPanel.Loader.loadObject`, 3828–3832; `saveObject`, 4104–4109 | Panel-level free-form notes. Setter substitutes an empty string for null. Writer emits `description` only if `description.trim()` is nonempty; loader sets it only for a non-null retrieved value. Could contain a technical rule, but code imposes no method schema. |
| `hide_description` | TrackerPanel loader 3829; writer 4105–4106; `onLoaded`, 5147–5153 | UI behavior controlling automatic notes display. It is not an editing-history flag or evidence of concealment. This source-code identification does not expand the protocol's plaintext-name/value allowlist. |
| Runtime track descriptions | `TrackerPanel.onLoaded`, 5147–5151, calls `track.getDescription()` | Establishes that descriptions can belong to tracks as well as the panel. Does not establish the XML key, emission conditions or loader defaults for those descriptions. |
| Common track serialization | `PointMass.Loader.saveObject`, 2826–2831; `loadObject`, 2874–2877 | Explicit delegation to `XML.getLoader(TTrack.class)`. That missing base-loader implementation is a substantive coverage limit, not a license to infer its fields from familiar names. |
| PointMass-specific saved fields | `PointMass.Loader.saveObject`, 2826–2865 | Writes `mass`; conditional `velocity_color`, `velocity_footprint`, `acceleration_color`, `acceleration_footprint`; nondependent `framedata`; and `keyFrames`. Those are not an explicit per-row marking recipe. Common delegated state remains separate. |
| `framedata`, dependence | PointMass writer 2847–2856; loader 2908–2935 | This writer saves positions when `!p.isDependent()`. With an authenticated matching writer, saved positions would support that state at serialization, not independent human measurement or absence of prior geometric construction. The inherited predicate's implementation is not in the inspected source. |
| Per-frame `x`, `y` | `PointMass.FrameData`, 3355–3368; `FrameDataLoader.saveObject/loadObject`, 3374–3393 | This inspected frame record holds position values only. It does not save a per-point annotator, original feature definition, editing timestamp, uncertainty or construction recipe. This is not a claim about every other project container. |
| `keyFrames` | PointMass writer 2858–2865; loader 2937–2951; `autoMarkAt`, 713–717 | Automatic marking adds keys. If loaded keys are missing or empty, this loader treats all existing steps as keys. Key membership cannot establish manual marking; missing keys cannot establish absence of prior marking. |
| Autofill runtime state | PointMass field default, 394; `isAutofill`, 1035–1036; `setAutoFill`, 1044–1064 | Runtime result combines `Tracker.enableAutofill` and the track flag. The PointMass-specific loader does not explicitly save/load a field called `autofill`; delegated base behavior is uninspected. A missing XML field cannot establish that interpolation was never used. |
| Interpolation | `PointMass.markAllInterpolatedSteps`, 1182–1213; overloads at 1222–1268 and 1279–1317 | The inspected pathway interpolates between selected-frame keys; it can create/move intermediate positions and, when disabled, remove gap steps. This is possible software behavior, not identification of the method that created a particular historical row. |
| Automatic target description | `PointMass.getTargetDescription`, 1330–1337 | Returns the generic localized position-name resource. It is not an analyst-authored statement of which building feature was tracked. |
| AutoTracker runtime owner | `TrackerPanel.getAutoTracker`, 3352–3359 | A panel can lazily create an AutoTracker. The inspected panel/PointMass-specific writers contain no explicit AutoTracker-state serialization, but uninspected delegated/child code prevents a global absence conclusion. |
| Undo/edit capability | `PointMass.createStep`, 535–538; interpolation routines 1185–1212 and 1228–1267 | Creates pre-edit XML snapshots and posts undo edits. This establishes editing capability, not a persisted audit trail. No explicit undo/history field appears in the two inspected save methods. Undo implementation and other persistence routes remain uninspected. |

The direct root `tracks` collection is saved at TrackerPanel 4140–4141 and loaded at 3965–3984. This supports keeping root ownership distinct from each direct track object's fields rather than treating any descendant `description` match as a track note.

Additional **container leads**, not established marking rules: `drawing_scenes`/`drawings_visible` are saved at 4147–4151 and loaded at 3985–4002; legacy `drawings` is loaded at 3993–4002. `views` is saved at 4175–4180 and `datatool_tabs` at 4210–4234. Their child schemas were not inspected here. Plot/fit expressions, generic variable descriptions and graphical annotations must not automatically be classified as position-selection methods. Root `author`/`contact` are separately loaded at 3834–3836 and saved at 4111–4116; their values are unnecessary to this question and were not read.

## Missing/empty-state and search cautions

- Root description absence is compatible with omission of empty or trim-whitespace notes by this writer. It does not prove no method existed, no note was ever written, or no differently owned field contains one. A current empty field is not a record of earlier emptiness.
- Missing `hide_description` is compatible with the writer emitting it only when true; absence is not a secrecy test. No project value was inspected here.
- The sanitized export's `autofill`/`dependent` numeric allowlist and substring searches are investigator-defined probes, **not** proof those names are serialized by this revision. A zero matching-name count bounds only that declared name search.
- Keep missing, absent text, empty, whitespace-only, nonempty, duplicate, and structured properties separate. The protocol's parsed text/tail ledger does not recover original lexical spelling, comments or processing instructions.
- A nonempty hashed description proves a stored nonempty value at a locator, not relevance, harmlessness, plaintext disclosure permission or correctness. Unknown names may contain useful information even if the stem scan misses them.
- The known PM05 nonkey prefix cannot be assigned to the between-surviving-keys interpolation pathway from current keys alone. Neither the absence nor presence of an autofill-like property would, by itself, resolve the earlier marking/edit history.
- A hash identifies held bytes. Matching an expected version label does not authenticate the executable that wrote the project. No source-code absence is promoted to a historical absence finding.

## Actual read and search coverage

Working directory: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`. No new source download, archive-interior inspection, raw TRK field inspection, project execution, media decode/view, historical calculation, or locator-source execution occurred in this lane.

Primary directory: `/Users/admin/docs/911/research/sherlock-wtc7-investigation/tracker-clock-semantics/sources/`.

- `tracker-6.1.2-TrackerPanel.java`: complete bounded ranges 570–605, 2660–2735, 3338–3367, 3713–3850, 3945–4243 and 5137–5166 were read; whole-file `rg -n` queries located description, save/load, dependence, AutoTracker, Undo/history and metadata references. Snippet search is not claimed as a complete full-file reading.
- `tracker-6.1.2-PointMass.java`: complete bounded ranges 380–407, 490–590, 690–732, 1025–1108, 1175–1344, 2800–2958 and 3335–3397 were read; whole-file `rg -n` queries located the corresponding field/function references.
- Existing sanitized exporter `tilted-camera-source-join/project-export.py`: lines 1–190 and 224–305 read; its reviewed schema and `project-export-review.md`/`source-semantics-review.md` were consulted. The exporter was **not imported or executed** in this lane.
- The previous frozen `tilted-point-frame-audit/method-followup.md` was read fully; no observation record was changed or used to infer new metadata contents.

Representative actual code-reading commands used `nl -ba PATH | sed -n 'START,ENDp'`, with the paths and exact ranges above, and `rg -n` on those two Java files. Current code pins were checked using `shasum -a 256` before documenting their semantics. The complete ignored-inclusive missing-source filename query was:

```sh
rg --files --hidden --no-ignore -g '!**/.git/**' -g '*TTrack*' -g '*AutoTracker*' -g '*Undo*' -g '*ParticleModel*' -g '*DynamicParticle*' /Users/admin/docs/911/research research
```

The standalone query returned **exit 1 with no matching paths**. It covered only filenames in main/worktree research, including ignored/hidden files, not archive interiors or the wider machine. An earlier listing included a nonexistent worktree `tracker-clock-semantics/sources` directory and returned exit 2; the actual primary sources are under main, as specified above. That path error is not a source-absence finding. Combined tool output that truncated a small charter segment was followed by a bounded reread of the omitted range. No failure was treated as a successful source search.

## Full source and dependency pins

| Artifact | SHA-256 |
| --- | --- |
| `tracker-6.1.2-TrackerPanel.java` | `f9c9a9adc83b3dea6f233cbe8c1e1a0a190dd10231073c2f61c3435c5d130893` |
| `tracker-6.1.2-PointMass.java` | `e382d1287948e6bb7ca5e72af902e42a88cc5a1828d0786696815116558d5d6f` |
| `tilted-camera-source-join/project-export.py` | `872d37a02cbbad8c8e80e2f40068e0f8e0606411c4494173bf7f3c9f24b36181` |
| `tilted-camera-source-join/project-export-review.md` | `bf3cf0b544ac9317908b4425247a05ca1edd168c3c19294708728afb1e793173` |
| `tilted-camera-source-join/source-semantics-review.md` | `f2a62ac0826e64b60f59aede09c00ff703c1c1a48c549d4f7d42be41ff50b2e1` |
| `tilted-point-frame-audit/method-followup.md` | `6561c386c6228416e6c308a69d21e0f9ce20856ef5468202380e7e7caceb29a1` |
| Current unit `PROTOCOL.md` | `47d55648820416cb92d35d562335a6332a8eff490c9a3e861ecda3a54cd6e030` |

The missing base-loader, AutoTracker and Undo implementations remain explicit coverage gaps. Their absence here does not block a privacy-preserving literal field inventory under the protocol; it limits the semantic conclusions that inventory can support. The evidence-audit/source-of-truth safeguards keep current saved state, possible software behavior, historical procedure and scientific validation distinct.
