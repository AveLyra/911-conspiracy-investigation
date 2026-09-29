# Metric-motion audit validation

Research-only work under [PROTOCOL.md](PROTOCOL.md), in
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch
`research/sherlock-wtc7-investigation`, based on
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`. Source dependencies in
`/Users/admin/docs/911` were read only. This validates the stated source
checks and synthetic mathematics, not historical acceleration or model physics.

## Scope and preserved declarations

- Charter SHA-256: `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
- Protocol: `2ef59293a4e7994929964878ace70cef3569b4b689008e7ef85c66dc1e00e800`.
- [inputs.json](inputs.json): `6885b06d38a6ed1b3b55d6188df49c1c91caaa3460fb08b80740ec76dc8fb8f1`.
- [calculate.py](calculate.py): `bc59b8a9e6510a0e8a493636dff96907a500c047536c235e7840fb72bb09e3d0`.

The protocol and synthetic producer/inputs were not altered after execution.
The additional source check is a disclosed follow-up to an already seen
calibration lead, not a preregistered independent holdout. It tests internal
configuration arithmetic and three explicitly transcribed floor pairs; it
does not fit or select a physical trajectory.

## Synthetic calculation and independent reproduction

Both `run01` and `run02` contain exactly seven files: six listed products and
their receipt. All corresponding files are byte-identical. The common receipt
SHA-256 is `d2839376f40177f8c09875e328f9f66dced562cf5d7135a7d5a7c86c86e22c41`.
There are 26 examples: 15 affine scale/clock combinations, five projective
examples, two nonlinear clocks, two offsets and two circular calibrations.
Six producer controls cover exact recovery, projective sign reversal,
nonlinear clock recovery and invalid inverse domains.

The two producer commands ran sequentially in **one shell invocation**. Each
printed completion with six controls and 26 examples; the combined observed
exit was 0. Separately captured producer exit statuses are not claimed.
The yielded command completed through its original handle; it was not
restarted because an observation timed out.

The separate reviewer derived the formulas before reading the producer's
results. Its exact rational second-order Taylor-series implementation does
not import the producer. Nine finite oracle check groups include affine and
nonlinear projection/clock witnesses, inverse recovery, constant offsets,
negative orientation, circularity and explicit invalid domains. These are
not nine historical tests. The early oracle implementation and result remain
preserved; no failed numeric example was removed.

The completed [verify_metric.py](verify_metric.py), SHA-256
`5be3a9c620fe01d362b212e24c58ac91624f00fbd2fa6a8964ae4540702aa8d2`,
reconstructs every rational and decimal field in all 26 examples and verifies
the complete two-run inventories, snapshots and runtime pins. The reviewer
and root each executed it with observed exit 0. Root had read the entire
verifier before its run. See [math-review.md](math-review.md).

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/metric-motion-audit/verify_metric.py --runs run01 run02 --out research/sherlock-wtc7-investigation/metric-motion-audit/independent-root01.json
```

[independent-root01.json](independent-root01.json), SHA-256
`7afdf2f6aec2084e5b60a88c5926788be297d8cba0b490f79be452fe0a159785`,
equals the reviewer's `independent-runs01.json` after removing only each
recorded command. This equality was independently rechecked by the later
source/configuration checker. Runtime for these calculations is Python 3.13.7.

## Primary-source and configuration coverage

During this bounded unit, root visually inspected ten complete NCSTAR 1-9
physical PDF pages: **306, 307, 308, 666, 667, 668, 669, 746, 749, 750**.
They establish camera descriptions, dimensional attribution, fit procedure
and the different vibration-marker purpose. All twenty corresponding existing
PNG/text products match their prior lineage hashes. The original NCSTAR 1-9
hash remains unchanged. No new render is claimed; no new NCSTAR 1A page
inspection is claimed.

Root and the separate calibration-source reviewer each viewed the complete
floor-spacing page and all five complete lab-instruction pages. These six
pages add to root's ten NIST pages, for **16 distinct primary PDF pages** in
the unit. Both calibration PDFs and all six existing PNGs match
`camera3-provenance/reading-products.json`. Existing renders are not
independent sources or new original-media viewing.

The [calibration-source review](calibration-source-review.md) additionally
checked PDF page counts and all 48 printed floor/Roof rows, including all
1,128 unordered pairs. Seven pairs have the assigned tape length at printed
precision; its embedded reproducible calculation was executed with exit 0.
Root independently verified three explicit examples and the exact unit
conversion, not a second full 1,128-pair enumeration. Both reviewers' prior
familiarity and computational, non-human status remain explicit.

The earlier [clock/source review](clock-source-review.md) pins 36 inputs and
checks all **8,717 existing frame-map rows**. Its original zero-new-image/page
coverage remains unchanged; the later six-page review is additive. It checks
28 selected scalars and five array summaries against the public TRK as inert
XML, rejecting DTD/entities and not emitting author-machine path fields.
Seven tagged Java files were read at its specified ranges, not as a full
runtime reproduction. Media were not newly rehashed or decoded in that pass.

Root's new [verify_sources.py](verify_sources.py), SHA-256
`75cb3e2a60ee542b4d56f1d568fa1a1306abe4883224c8406553245e04c1e4e7`,
checks all 36 pinned input rows, the NIST PDF, twenty NIST derivatives, two
calibration PDFs and six calibration page images: **65 hash checks, all pass**.
This is 65 checks, not necessarily 65 distinct files. Its new Decimal/rational
calculation independently reconstructs the tape distance, scale and three
nonunique floor spans from explicitly sourced values. It does not parse
the original TRK or locate any video endpoints.

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/metric-motion-audit/verify_sources.py --out source-check-root01.json
```

Observed exit 0; [source-check-root01.json](source-check-root01.json) SHA-256
`b3cb0bf523c5a267b2f3541de410b82f5c4c7f14dbe2a22c1bddb44c267bd1bd`.
The scale residual is approximately `7.35e-16` pixels per assigned metre;
58.293 m converts exactly to 765/4 ft. This is configuration/source arithmetic,
not an independently measured physical scale.

## Failures, review and limits

No numerical calculation failed in the current metric unit. Preserve these
workflow limitations instead of rewriting them as scientific results:

- An initial guessed Tracker-semantics report path did not exist; its actual
  Markdown path was then read. Some combined reads exceeded the display
  budget; required passages were recovered through scoped reads. A wrong
  sanitized-JSON key produced a `jq` error before the correct key was used.
- One skill path was incorrectly guessed; the declared catalog path was then
  read. A shell group's final success is not evidence that every earlier
  command within it succeeded.
- The intervening supplementary-production reminder changed no scientific
  result. Its metadata-only delegate stopped without completing that check;
  it is not an independent intake verification. Existing inventory/lead
  records controlled that acknowledgment.
- Final report review is recorded separately in [final-math-review.md](final-math-review.md)
  and [final-source-review.md](final-source-review.md). Exact reviewed hashes,
  corrections and final acceptance must be read there, not inferred from the
  existence of this file.

Both final reviews now pass for report SHA-256
`cdf5218c9b32ef76c4b7859b5e9c4acfa7405f9ead14fe7330fdc66855941e86`.
The initial report hash remains in each review. Three mathematical precision
edits clarified twice-differentiable functions/nonzero clock rate, distinct
regression units and the signed camera-to-target baseline component; the
source review clarified “floor intervals.” The mathematical reviewer reversed
only these four changes in memory and recovered the original full-report
hash. Root read both completed reviews, including their additive final
dispositions. None certifies a new historical measurement or human review.

Final integration checked eleven selected Markdown documents and 178 local
link targets: none missing, with 104 resolving to unchanged original-repository
dependencies absent from the sparse checkout. No trailing whitespace or
conflict markers were found. All three current Python files parsed, and
scoped tracked `git diff --check` passed. These are scoped documentation/code
checks, not canonical-record validation or review of unrelated worktree edits.
The repository's canonical record validator was not run in this sparse
research-only unit; no canonical record files were changed. All calculation
and bounded-review handles are terminal; no process is presumed live from
its receipt alone.

All results remain research-only. No historical fit, source retiming, target
reannotation, new decode, structural solver execution, production/held-packet
inspection, outreach, external upload, Faraday bridge use, case import,
human approval, canonical fact promotion, filing, commit or push occurred.
Sparse-checkout link validation may resolve unchanged dependencies in the
original read-only repository; that is not a complete standalone checkout.
Source, evidence and development-verification safeguards distinguish
reproducibility from physical validation. Broader WP2 and the full goal remain
incomplete; the next source-raster endpoint test is stated in the report.
