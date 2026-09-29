# Collapse Reconstruction Workbench

**Status:** Evidence/provenance core implemented; not an expert report  
**Working name:** Collapse Reconstruction Workbench (CRW)  
**First pilot:** WTC 7 multi-camera, audio, and structural-model audit

## Purpose

CRW is a reproducible, physics-guided system for testing which families of collapse mechanisms are compatible with recorded observations. It is not a video classifier and does not produce a binary “fire” or “demolition” verdict.

The system's central output is deliberately narrower:

> Given preserved evidence, explicit uncertainty, a parameterized mechanism, and a forward model, identify which parameter regions reproduce the observations, which fail, and which remain observationally indistinguishable.

That framing is necessary because collapse reconstruction is an inverse problem. Different hidden failure histories can generate similar exterior motion, and no algorithm can recover interior events that were never recorded.

## Implemented vertical slice (`CRW-001`–`CRW-005`)

The local Python package now provides:

- JSON-Schema validation with object paths in error messages;
- immutable, SHA-256 content-addressed ingest and deduplication;
- integrity verification that detects missing or altered bytes;
- lossless CSV-manifest import with explicit local/remote/missing/hash-mismatch status;
- deterministic audio-extraction and PNG frame-sequence derivatives using `ffmpeg`;
- immutable derivative records containing parent IDs, commands, tool versions, environment details, and output hashes; and
- reproduction of registered derivatives with byte-for-byte hash comparison.

This slice does not authenticate source media, measure collapse motion, classify causes, run structural simulations, or promote any result into the litigation fact record.

### Install and test

Python 3.10 or later is required. `ffmpeg` is required only for media derivative commands and their integration test.

```bash
cd research/collapse-reconstruction-workbench
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[test]'
.venv/bin/crw --help
.venv/bin/python -m pytest
```

### Core commands

Use an evidence store outside tracked source. The examples below use `/path/to/crw-evidence-store`; the tool never defaults to a repository media directory.

```bash
crw schema validate examples/synthetic-evidence.json --schema evidence-object

crw evidence ingest /path/to/input.mp4 \
  --store /path/to/crw-evidence-store \
  --id EVD-EXAMPLE-001 \
  --event-id EVT-EXAMPLE-001 \
  --role access_copy \
  --authenticity-status unknown \
  --preservation-tier platform_access \
  --limitation "Example only; provenance has not been authenticated."

crw evidence verify --store /path/to/crw-evidence-store

crw manifest import \
  ../wtc7-video-comparison/source-manifest.csv \
  ../wtc7-video-comparison/media/video-acquisition-manifest.csv \
  --output reports/seed-manifest-reconciliation.json

crw derivative audio \
  --store /path/to/crw-evidence-store \
  --parent-id EVD-EXAMPLE-001 \
  --id DRV-EXAMPLE-AUDIO-001

crw derivative frames \
  --store /path/to/crw-evidence-store \
  --parent-id EVD-EXAMPLE-001 \
  --id DRV-EXAMPLE-FRAMES-001

crw derivative reproduce \
  --store /path/to/crw-evidence-store \
  --id DRV-EXAMPLE-FRAMES-001
```

Frame sequences are stored as deterministic ZIP archives of numbered PNG files. The archive is a derivative, not a timing map: presentation timestamps, duplicate frames, dropped frames, and edits remain work for `CRW-006`.

### Store layout and immutability limits

The store uses `blobs/sha256/<prefix>/<digest>` for bytes and `records/<ID>.json` for immutable metadata. New files are made read-only and records are never intentionally replaced. Filesystem permissions are not a hostile-user security boundary; use snapshots, write-once storage, or controlled custody procedures where stronger guarantees are required. `crw evidence verify` is the detection control.

## Blueprint package

| File | Purpose |
|---|---|
| [`SYSTEM-BLUEPRINT.md`](SYSTEM-BLUEPRINT.md) | Architecture, inference method, components, trust boundaries, and implementation shape |
| [`DATA-CONTRACTS.md`](DATA-CONTRACTS.md) | Evidence, observation, model-run, provenance, and uncertainty contracts |
| [`PILOT-ROADMAP.md`](PILOT-ROADMAP.md) | Phased WTC 7 pilot, validation gates, roles, compute, and completion criteria |
| [`schemas/evidence-object.schema.json`](schemas/evidence-object.schema.json) | Machine-readable evidence/provenance object |
| [`schemas/observation.schema.json`](schemas/observation.schema.json) | Machine-readable measured-observation object |
| [`schemas/scenario-run.schema.json`](schemas/scenario-run.schema.json) | Machine-readable simulation/run record |
| [`examples/`](examples/) | Synthetic, non-evidentiary fixtures demonstrating the three contracts |

## Design commitments

1. **Preserve before analyzing.** Original acquired bytes are immutable, hashed, and separated from derivatives.
2. **Measurements precede explanations.** Tracks, timings, audio events, and uncertainties are stored without embedding a causal label.
3. **AI assists measurement and search.** It does not decide the cause.
4. **Every hypothesis runs forward.** A proposed mechanism must generate predicted observables from the actual camera and microphone geometry.
5. **Uncertainty is first-class.** Camera calibration, synchronization, measurement, physical parameters, and model discrepancy are represented separately.
6. **Comparator labels require independent foundation.** A spectacular video is not a “known demolition” control without reliable method documentation.
7. **Holdouts are event-level.** Clips of the same event cannot be divided between training and testing.
8. **Likelihood and priors stay separate.** The system reports physical fit without silently importing institutional, logistical, or motive assumptions.
9. **Negative results remain visible.** Failed runs, rejected tracks, and analyst disagreements are retained.
10. **Reproduction is a deliverable.** A result is incomplete without source hashes, code version, parameters, environment, and regenerable outputs.

## Existing seed evidence

The initial evidence layer already exists in [`../wtc7-video-comparison/`](../wtc7-video-comparison/):

- three secondary-hosted camera-analysis files;
- two archived broadcast segments;
- separately preserved video/audio streams of the 27 Angles compilation;
- separately preserved video/audio streams of a confirmed explosive-implosion control;
- file-level acquisition metadata and SHA-256 hashes;
- an audio-screening script, figures, and limitations audit;
- a mechanism feature matrix; and
- primary-report and alternative-analysis source manifests.

These objects are pilot inputs, not training labels and not authenticated originals.

## Recommended first build

Build the **measurement and evidence core** before any structural inverse solver:

1. content-addressed evidence ingestion;
2. derivative and provenance graph;
3. frame-accurate timestamp maps;
4. camera calibration and stabilization;
5. multi-point tracking with uncertainty;
6. audio-event candidates with propagation-time ranges;
7. synchronized observation timeline; and
8. a report that can be reproduced from hashes and configuration.

That first system would already improve the evidentiary record. The structural simulation and Bayesian comparison layer should begin only after the observation pipeline passes the validation gates in the roadmap.

## Repository boundary

Keep CRW outputs under `research/` unless a proposition is deliberately promoted through the repository's fact-promotion process. A model-fit result is an analysis artifact, not a procedural fact or pleading allegation. Engineering conclusions require qualified expert review.
