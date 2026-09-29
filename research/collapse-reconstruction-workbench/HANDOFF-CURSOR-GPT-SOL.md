# Cursor / GPT-SOL handoff: Collapse Reconstruction Workbench

## State

- Repository: `/Users/admin/docs/911`
- Branch: `main`
- HEAD at handoff: `7be4d08` (`WIP: Answer analysis, EXH-012 ID, and NIST UPS service record`)
- Working tree: substantially dirty with pre-existing case/research edits and new WTC 7 research material. Do not reset, clean, or overwrite unrelated changes.
- CRW status: blueprint and schemas exist; implementation has not begun.

## User objective

Build a self-directed, reproducible system for testing WTC 7 collapse-mechanism hypotheses against preserved video/audio observations and structural models. The immediate objective is a low-cost pilot, not a definitive cause verdict or a litigation-ready expert opinion.

The user asked whether LS-DYNA costs can be avoided and whether an adequate solver can be built quickly with GPT assistance. The adopted answer is: use an established free/open solver where possible; build measurement, provenance, experiment, and audit tooling around it; do not claim that a new solver written in hours is equivalent to mature nonlinear explicit-dynamics software.

## Durable decisions

1. CRW is a falsification-oriented research workbench, not a video classifier and not a binary “fire versus demolition” detector.
2. Separate measured observations, physical assumptions, model outputs, and institutional/legal claims.
3. Preserve source bytes and hashes before analysis. Every derivative needs a parent hash, command/configuration, tool version, and output hash.
4. Begin with evidence/provenance and measurement. Structural inverse modeling comes only after observation validation.
5. Use event-level holdouts and predeclared scoring. Never train and test on clips from the same event.
6. Maintain competing mechanism families, including simultaneous support loss, propagating interior failure, exterior-first failure, fire-induced progressive failure, and other explicitly parameterized scenarios.
7. Report compatibility regions, sensitivities, failed runs, and non-identifiability. Do not convert a visual match into causal proof.
8. A mature free solver is preferable to inventing a solver. OpenRadioss is the primary no-license-fee candidate; it is AGPL-3.0 and accepts some LS-DYNA-format inputs, but keyword compatibility does not imply numerical equivalence.
9. Ansys LS-DYNA Student is a possible educational sandbox, not an assumed litigation/research license. Current official limits include educational-only terms, 128K nodes/elements, and up to four HPC cores; verify terms before use.
10. A model that reproduces exterior motion after prescribing a support-loss history tests consequence compatibility, not the historical cause of that support loss.

## Work completed

Existing CRW files:

- `README.md` — purpose, design commitments, seed evidence, and recommended first build.
- `SYSTEM-BLUEPRINT.md` — architecture, evidence vault, media measurement, structural model, forward simulation, inference, and trust boundaries.
- `DATA-CONTRACTS.md` — evidence, observation, scenario-run, provenance, and uncertainty contracts.
- `PILOT-ROADMAP.md` — phases G0–G6, a 90-day minimum pilot, and implementation backlog `CRW-001`–`CRW-010`.
- `schemas/*.json` — machine-readable contracts.
- `examples/*.json` — synthetic fixtures only; not evidentiary facts.

Seed media/research package:

- `research/wtc7-video-comparison/` contains preserved access copies, hashes, source manifests, audio screening, figures, and limitations notes. Treat it as pilot input, not authenticated original footage or a labeled training corpus.

## Recommended next task for Cursor

Implement only the first vertical slice: `CRW-001` through `CRW-005` from `PILOT-ROADMAP.md`.

### Read first

1. This handoff.
2. `research/collapse-reconstruction-workbench/README.md`.
3. `research/collapse-reconstruction-workbench/DATA-CONTRACTS.md`.
4. `research/collapse-reconstruction-workbench/PILOT-ROADMAP.md`.
5. Existing manifests and README files under `research/wtc7-video-comparison/`.
6. Repository instructions (`README.md`, relevant `AGENTS.md` if present, and source-of-truth/evidence rules).

### Scope

- Create a small Python package/CLI under the CRW directory (or a clearly documented adjacent `tools/` location).
- Add commands for schema validation, immutable evidence ingest, hash verification, and derivative registration.
- Use a content-addressed evidence store outside tracked source when appropriate; never copy or mutate original media unnecessarily.
- Import existing source/acquisition manifests without silently changing fields.
- Provide unit tests using the synthetic fixtures and temporary directories.
- Record environment/tool versions and exact commands in provenance records.
- Do not implement a finite-element solver, AI causal classifier, Bayesian posterior, or legal pleading in this slice.

### Acceptance criteria

- A clean checkout can run the CLI help and test suite.
- Valid synthetic fixtures pass JSON-Schema validation; malformed fixtures fail with useful paths.
- Re-ingesting identical bytes deduplicates by SHA-256; attempted overwrite fails.
- Verification detects deliberate byte alteration.
- At least one audio extraction and one frame-sequence derivative can be reproduced from recorded parent hash plus command/configuration.
- Existing manifests reconcile with an explicit report of missing/unavailable paths; no evidence is promoted to `facts/` or pleadings.
- Tests and limitations are documented. Do not imply that an unrun full-scale simulation has been reproduced.

## Solver and cost notes for later phases

- Incremental software cost can be zero using OpenRadioss and existing Python tooling, subject to its AGPL obligations and local compute.
- Student LS-DYNA can support learning and small component experiments if the use complies with its terms; it cannot reproduce NIST’s full-scale mesh under the published size limit.
- Narrow analytical/reduced models can be written in hours or days, but mature contact, buckling, fracture, thermal, and large-deformation behavior requires validation over weeks to months.
- Do not budget a full engineering team until a small benchmark establishes runtime, mesh needs, and the value of the missing inputs.

## Unresolved questions

- Which source files, NIST model packages, custom routines, and version-specific dependencies can be lawfully obtained and executed?
- Which cameras have sufficient calibration, frame timing, and unobstructed geometry for quantitative tracking?
- Which comparison/demolition controls have documented method and reliable provenance?
- Which physical parameters are identifiable from the available observations rather than merely adjustable?
- What external engineering review is needed before any result is characterized as expert evidence?

## Authority and caution

Repository research remains research unless deliberately promoted through the repository’s fact-promotion process. Preserve alternative interpretations and failed tests. Cursor should ask before making broad repository reorganizations or modifying pleading/fact files.

Useful primary references:

- [NIST WTC 7 investigation FAQ](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation)
- [NIST ASCE paper / structural methodology](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=902588)
- [OpenRadioss source and license](https://github.com/OpenRadioss/OpenRadioss)
- [Ansys LS-DYNA Student terms and limits](https://ansys.synopsys.com/academic/students/ansys-ls-dyna-student)

