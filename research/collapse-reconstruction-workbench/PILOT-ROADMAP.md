# WTC 7 pilot roadmap

## Pilot objective

Build and validate the observation/inference foundation needed to compare explicit WTC 7 mechanism families. The pilot should improve measurement and reveal identifiability limits before attempting a definitive full-building reconstruction.

## Pilot questions

1. Can independent analysts reproduce multi-point façade displacement and uncertainty from the available cameras?
2. Can all candidate audio events be placed on a common source-time axis with defensible ranges?
3. Which observable features discriminate widespread support loss from a visibly propagating exterior failure?
4. Can a simple support-loss model reproduce the free-fall interval while also matching rotation, lateral displacement and precursor timing?
5. Which released or withheld structural files would most reduce uncertainty in a full-model audit?

## Phase 0 — charter and frozen protocol

**Estimated effort:** 1–2 weeks

Deliverables:

- frozen pilot questions and hypothesis-family definitions;
- observation list and measurement protocol;
- comparator inclusion criteria;
- train/calibration/holdout rules;
- predeclared scoring and uncertainty rules;
- repository and publication boundaries; and
- expert-role and conflict disclosures.

Exit gate G0: protocol is versioned before new causal comparisons are run.

## Phase 1 — evidence and provenance core

**Estimated effort:** 3–6 weeks

Use the existing [`../wtc7-video-comparison/`](../wtc7-video-comparison/) package as the seed collection.

Build:

- content-addressed ingestion;
- schema validation;
- immutable evidence and derivative identifiers;
- acquisition/custody event log;
- technical metadata extraction;
- parent/derivative graph;
- duplicate and near-duplicate detection; and
- integrity verification command.

Deliverables:

- all current media and source documents registered;
- current CSV manifests imported without losing fields;
- a provenance graph showing compilation, source and derivative relationships; and
- a missing-source inventory.

Exit gate G1: every analysis input resolves to preserved bytes, a hash, and a complete derivation path.

## Phase 2 — synchronized observation pipeline

**Estimated effort:** 6–12 weeks

Build:

- frame timestamp and edit maps;
- interlace/frame-duplication diagnostics;
- camera stabilization;
- initial camera pose and lens calibration;
- multi-point and line tracking;
- manual-review interface or structured annotation files;
- audio transient candidates and edit detection;
- clock-offset graph and acoustic propagation intervals; and
- uncertainty propagation into displacement and timing series.

Initial WTC 7 measurements:

- center roofline and both visible roof corners;
- east/west roof structures and façade kink;
- lateral displacement and rotation;
- window/dust onset regions;
- visible-obstruction masks; and
- all candidate audio events in the preserved sources.

Exit gate G2:

- two analysts independently reproduce selected tracks within predeclared tolerance;
- results remain stable across reasonable stabilization and smoothing choices;
- every plotted acceleration links to raw coordinates and uncertainty; and
- broadcast/file/source times remain explicitly distinct.

## Phase 3 — comparator benchmark

**Estimated effort:** 6–12 weeks, overlapping Phase 2

Acquire multiple documented examples in each relevant category. Do not use the current Hertz video as the sole explosive control.

Build:

- event-level corpus registry;
- source-quality and structural-comparability scoring;
- the same video/audio measurement pipeline used for WTC 7;
- feature-specific error models; and
- event-level blind holdouts.

Required tests:

- Can the pipeline detect a charge-train pattern in held-out confirmed implosions?
- How often do speech, vehicles, edit clicks, impacts and structural fracture trigger the same detector?
- How specific are coherent descent, free fall, dust onset and façade deformation across known causes?
- Does performance collapse when news graphics, filenames and event labels are removed?

Exit gate G3: measurement error and false-positive behavior are reported on held-out events; no clip from a held-out event was used in development.

## Phase 4 — WTC 7 geometry and reduced models

**Estimated effort:** 3–6 months

Build:

- normalized structural graph from drawings and published model descriptions;
- camera-aligned exterior geometry;
- gravity/load-path checks;
- connection and column subassembly models;
- L0 kinematic support-loss model;
- L1 reduced progressive-failure model; and
- synthetic camera renderer.

Experiments:

- simultaneous versus propagating support loss;
- interior-first versus exterior-first loss;
- east-to-west progression rates;
- sensitivity to lateral restraint and façade continuity;
- onset timing needed to produce the measured free-fall interval;
- compatibility with measured lateral movement, rotation and precursor events; and
- predictions for observations not used in fitting.

Exit gate G4: at least one camera or tracked feature is reserved for out-of-fit prediction; model families are rejected or retained using frozen criteria.

## Phase 5 — released/produced finite-element model ingestion

**Estimated effort:** 6–18 months after receipt of executable-quality packages

Build:

- ANSYS and LS-DYNA package inventory and dependency resolver;
- version/unit/custom-routine audit;
- model-transfer and damage-handoff inspection;
- execution sandbox;
- reference-output comparison; and
- parameter-perturbation and sensitivity harness.

Order of operations:

1. preserve and inventory exact bytes;
2. resolve dependencies without editing originals;
3. reproduce published/reference outputs;
4. explain any reproduction gap;
5. freeze baseline;
6. perturb one assumption family at a time;
7. build verified emulators for expensive regions; and
8. compare synthetic observables with all cameras.

Priority sensitivity families:

- connection stiffness and failure limits;
- thermal expansion and temperature mapping;
- restraint and composite action;
- initial debris damage;
- damping/contact/erosion rules;
- instantaneous versus time-resolved damage transfer;
- 3.5-hour versus 4.0-hour state transition; and
- omitted nonstructural stiffness.

Exit gate G5: baseline output matched within declared tolerances and all unresolved dependencies disclosed. “Parsed” is not “reproduced.”

## Phase 6 — inference, model criticism and external replication

**Estimated effort:** 6–12 months after G5

Build:

- multi-observation likelihoods with correlated error;
- model-discrepancy terms;
- history matching and simulation-based inference;
- global sensitivity and identifiability analysis;
- evidence-value ranking; and
- frozen, reproducible reports.

Independent teams receive source hashes, protocol, code, configurations and selected blinded scenarios. Disagreements are reported rather than averaged away.

Exit gate G6: an external team reproduces the principal measurements and at least one model-comparison result from a clean environment.

## Ninety-day minimum viable pilot

The first 90 days should not promise a collapse-cause verdict. It should deliver:

1. validated evidence/observation/scenario schemas;
2. ingestion of the current WTC 7 package;
3. immutable provenance graph and integrity command;
4. timestamp/edit maps for Cameras 2–4 and the 27 Angles access copy;
5. reproducible multi-point roof/façade tracks from at least two cameras;
6. synchronized event intervals with uncertainty;
7. current audio candidates classified only by signal morphology and provenance quality;
8. the Hertz control processed through the identical pipeline;
9. an L0 support-loss model rendered from one camera; and
10. a report identifying what is measured, inferred, unresolved, and most valuable to obtain next.

### Initial implementation backlog

| ID | Work item | Acceptance criterion |
|---|---|---|
| `CRW-001` | Create package/CLI skeleton and test harness | Clean environment runs `crw --help` and the test suite |
| `CRW-002` | Implement JSON-Schema validation | Valid fixtures pass; intentionally malformed objects fail with useful paths |
| `CRW-003` | Import existing source and acquisition manifests | Row counts, paths, hashes and limitations reconcile exactly |
| `CRW-004` | Build immutable ingest and integrity commands | Reingest deduplicates by hash; overwrite attempt fails; verification detects changed bytes |
| `CRW-005` | Register derivative provenance | One audio extraction and one frame sequence reproduce from recorded commands |
| `CRW-006` | Produce frame timestamp/edit maps | Variable rate, duplicate, dropped and hard-cut fixtures are correctly flagged |
| `CRW-007` | Define point/line annotation format | Two analysts can annotate the same fixture without overwriting each other |
| `CRW-008` | Implement calibration and tracking baseline | Synthetic camera fixture recovers known motion within frozen tolerance |
| `CRW-009` | Import the existing audio-window analysis | Source and derivative hashes, windows and event markers resolve through the provenance graph |
| `CRW-010` | Generate first evidence report | One command emits sources, observations, uncertainty and unresolved items from a clean checkout plus evidence store |
| `CRW-011` | Build L0 support-loss simulator | Known analytic free-fall and resisted-fall fixtures pass before WTC 7 fitting |
| `CRW-012` | Render L0 output through a calibrated camera | Synthetic track can be recovered by the same observation pipeline without privileged state access |

## Roles

Minimum serious team:

| Role | Primary responsibility |
|---|---|
| Technical lead / research engineer | Architecture, reproducibility and integration |
| Computer-vision engineer | Camera calibration, tracking, occlusion and uncertainty |
| Structural engineer | Load paths, connections, failure families and model review |
| Computational-mechanics specialist | Nonlinear FE adapters, execution and numerical quality |
| Acoustics specialist | Propagation, transient analysis and recording limitations |
| Evidence/data engineer | Provenance, custody, schemas and immutable storage |
| Independent reviewers | Blind tracks, protocol review and replication |

The MVP can begin with one research engineer plus part-time structural, vision and acoustics review. Full finite-element inference requires the specialist team.

## Compute and storage

### MVP

- workstation-class CPU/GPU;
- several terabytes of versioned local storage;
- content-addressed source vault and separate derivative cache;
- deterministic batch jobs; and
- no distributed infrastructure requirement.

### Full-model stage

- licensed solver environment where required;
- isolated high-memory CPU nodes;
- checkpointed multi-run scheduling;
- tens to hundreds of terabytes if full histories are retained;
- verified emulators to reduce full-run count; and
- immutable archival storage for decisive runs.

Compute scale must follow validated questions. A large parameter sweep cannot repair an uncalibrated camera or incomplete model package.

## Principal risks and controls

| Risk | Control |
|---|---|
| Non-identifiability | Report surviving mechanism families and value of additional evidence |
| Training-set bias | Include accidental, non-collapse and acoustic negative controls |
| Label leakage | Remove titles/graphics and split by event |
| False timing precision | Explicit clock and propagation distributions |
| Derivative mistaken for source | Immutable lineage and visible preservation tier |
| AI hallucination of occluded behavior | Prohibit generated content as observation |
| Overfitting one roofline track | Multiple cameras, points, lines and reserved predictions |
| Numerical artifact mistaken for physics | Energy/mass/contact diagnostics and mesh/timestep sensitivity |
| Proprietary model cannot execute | Preserve bytes, report dependency gap, maintain open reduced models |
| Investigator degrees of freedom | Freeze protocols and retain failed/rejected analyses |
| Advocacy capture | Disclose funding/roles; use blind review and external replication |

## Stop conditions

Pause escalation to full inverse modeling if:

- source provenance cannot support the claimed timing precision;
- camera geometry cannot constrain metric displacement;
- comparator holdouts show unacceptable false-positive behavior;
- model packages lack execution-critical dependencies;
- results are determined primarily by arbitrary weighting; or
- different plausible parameterizations remain observationally indistinguishable.

Stopping with a rigorous non-identifiability result is a successful scientific outcome.
