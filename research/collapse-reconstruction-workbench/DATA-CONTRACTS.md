# CRW data contracts

## 1. Contract philosophy

CRW separates five layers that are often improperly blended:

| Layer | Example | May contain causal interpretation? |
|---|---|---|
| Evidence | Exact video bytes or a solver deck | No |
| Derivative | Deinterlaced proxy or extracted audio | No |
| Observation | Tracked roof coordinate with covariance | No |
| Scenario prediction | Simulated coordinate from a specified run | Only through declared scenario parameters |
| Assessment | Compatibility, sensitivity or exclusion result | Yes, with provenance to all lower layers |

A statement cannot skip layers. For example, “this resembles demolition” cannot become an observation; it must be decomposed into measurable features and compared against documented controls.

## 2. Identifiers

Recommended prefixes:

| Object | Prefix | Example |
|---|---|---|
| Event | `EVT-` | `EVT-WTC7-20010911` |
| Evidence | `EVD-` | `EVD-WTC7-CAM03-ACCESS-001` |
| Derivative | `DRV-` | `DRV-WTC7-CAM03-FRAMES-001` |
| Observation | `OBS-` | `OBS-WTC7-NORTH-ROOF-Y-001` |
| Structural model | `MDL-` | `MDL-WTC7-NIST-LSDYNA-001` |
| Hypothesis family | `HYP-` | `HYP-FIRE-PROGRESSIVE` |
| Scenario run | `RUN-` | `RUN-WTC7-FIRE-000042` |
| Assessment | `ASM-` | `ASM-WTC7-TRACKS-0007` |

Identifiers never encode truth status. Revisions create new objects linked with `supersedes`; they do not mutate an earlier object's meaning.

## 3. Evidence contract

The machine contract is [`schemas/evidence-object.schema.json`](schemas/evidence-object.schema.json).

Required concepts:

- immutable ID, local path, SHA-256, byte count and acquisition time;
- source/capture date distinguished from acquisition date;
- source page and retrieval route;
- exact role: preserved source, access derivative, comparator, produced model, or analysis derivative;
- custody and authenticity status as claims with source attribution;
- technical media/model metadata;
- parent relationships and transformations; and
- limitations and redistribution status.

An evidence object may be admissible, inadmissible, authenticated, disputed, or unknown without changing its bytes or identifier.

## 4. Derivative/provenance contract

A derivative is an evidence object with one or more lineage entries:

```json
{
  "parent_id": "EVD-WTC7-CAM03-ACCESS-001",
  "relation": "decoded_from",
  "transformation": {
    "tool": "ffmpeg",
    "version": "recorded-at-runtime",
    "configuration_uri": "configs/decode-lossless.json",
    "operator": "pipeline",
    "created_at": "2026-09-02T20:00:00Z"
  }
}
```

Manual edits require an annotation or mask object; they are never hidden inside an overwritten media file.

## 5. Observation contract

The machine contract is [`schemas/observation.schema.json`](schemas/observation.schema.json).

An observation must identify:

- all supporting evidence and derivative IDs;
- event time or interval and the clock used;
- spatial coordinate frame;
- feature type and value/series;
- units;
- measurement method and implementation version;
- uncertainty components;
- occlusion and completeness;
- reviewer status; and
- alternative interpretations or confounders.

### Uncertainty decomposition

Do not store only a total ± value. Preserve components:

```text
measurement noise
camera calibration
lens distortion
camera motion/stabilization
clock synchronization
frame timestamp uncertainty
feature-definition disagreement
source edit or provenance uncertainty
```

Components may be combined for a particular analysis, but the original decomposition remains available.

### Time model

Every time value has:

- `clock_id`;
- source presentation timestamp or sample index;
- mapped event time;
- mapping method;
- offset distribution; and
- propagation delay where acoustic observations are involved.

This prevents a broadcast timestamp, video-file offset, camera clock and source-event time from being treated as the same quantity.

### Missingness

Missing and negative observations are distinct:

- `not_visible`: geometry was occluded or outside the frame;
- `not_recorded`: source does not contain the interval or channel;
- `not_detected`: method searched a qualified recording and found no event above a declared threshold;
- `unknown`: evidence is insufficient to assign another state.

“Not visible” must never be converted to “did not occur.”

## 6. Structural-model contract

Each imported model package records:

- original package evidence IDs and hashes;
- asserted author and model purpose;
- solver family, exact version and precision;
- complete include/dependency graph;
- unit system;
- geometry/member/connection counts;
- material and failure cards;
- contact, damping, timestep, mass scaling and erosion settings;
- initial and transferred damage;
- temperature histories and mapping rules;
- custom routines or macros;
- unsupported or unresolved dependencies;
- import warnings; and
- reproduction status.

Reproduction statuses:

| Status | Meaning |
|---|---|
| `bytes_preserved` | Package stored and hashed only |
| `parsed_partial` | Some content normalized; unresolved objects remain |
| `parsed_complete` | All execution-relevant content accounted for |
| `executed` | Solver completed under recorded environment |
| `output_matched` | Declared reference outputs reproduced within tolerance |
| `audited` | Sensitivity and independent review completed |

## 7. Scenario-run contract

The machine contract is [`schemas/scenario-run.schema.json`](schemas/scenario-run.schema.json).

Every run identifies:

- hypothesis family;
- base structural model;
- changed parameters and their rationale;
- source of every parameter bound;
- execution environment and random/deterministic state;
- solver quality metrics;
- output objects;
- synthetic-observation objects; and
- comparison metrics.

Runs are immutable. A rerun with corrected settings receives a new ID and links to the superseded run.

## 8. Fit and assessment contract

Assessments must report residuals by observation, not just an aggregate score. At minimum:

- displacement residuals by point and camera;
- timing residuals by event;
- rotation/deformation residuals;
- audio-event compatibility after propagation correction;
- structural-energy and numerical-quality diagnostics;
- observations excluded from the comparison and why;
- model-discrepancy assumptions; and
- sensitivity of the conclusion to weighting and uncertainty choices.

Allowed conclusion vocabulary:

- `incompatible_with_declared_bounds`;
- `compatible_in_parameter_region`;
- `better_fit_than_named_alternative_under_same_metric`;
- `not_identifiable_from_current_observations`; and
- `not_tested`.

Avoid “proved,” “debunked,” and “AI confidence” unless a separately defined statistical proposition warrants those terms.

## 9. Comparator contract

Each comparator event requires:

- independent cause/method foundation;
- building type, height, structural system and geometry summary;
- preparation and damage history when applicable;
- camera/microphone locations or their uncertainty;
- native/best-available source status;
- all clips grouped under one event ID;
- train/calibration/holdout partition assigned at event level; and
- reasons the event is or is not comparable to the target.

Controls calibrate specific features. A reinforced-concrete implosion may be a useful audio positive control while being a poor structural-dynamics analogue.

## 10. Review and promotion

Review states are `machine_proposed`, `analyst_measured`, `second_reviewed`, `expert_reviewed`, `disputed`, and `superseded`.

No CRW assessment becomes a repository fact merely because it is reproducible. Promotion requires the repository's existing source, relevance, and expert-review safeguards.

## 11. Semantic invariants beyond JSON Schema

JSON Schema validates object shape. Application validators must additionally enforce:

- stored byte count and SHA-256 match the referenced file;
- referenced IDs exist and event IDs agree where required;
- provenance and `supersedes` graphs are acyclic;
- source and event intervals have start values no later than end values;
- acoustic propagation delay is applied exactly once;
- coordinate transformations resolve through a complete calibration chain;
- units are dimensionally compatible before values are combined;
- `not_detected` observations include the searched interval, threshold and qualified source;
- run output hashes resolve and failed runs cannot enter a fit assessment as successful; and
- immutable objects cannot be edited in place.
