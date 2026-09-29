# Execution and verification record

2026-09-20 UTC. [Report](report.md). This validates bounded source handling and
synthetic mathematics, not historical video calibration or the quoted interval.

## State and scope

Worktree `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch
`research/sherlock-wtc7-investigation`, HEAD `e8d83d7`. Existing tracked and
untracked WIP preserved; no commit/push, source mutation, main/canonical/legal
edit, solver, upload, outreach or accepted Sherlock/Faraday claim.

Main controls/full charter were read in preceding work and freshly pinned
unchanged at this unit's start; current causal synthesis read in full. The
evidence-audit, source-of-truth, PDF and development-verification skills govern
provenance and testing. Context-distiller governs the status handoff. This
does not substitute software checks for scientific acceptance.

## Full-page render and separate readings

Actual producer command from the worktree:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/lateral-geometry-audit/render.py
```

Terminal session 65844 ended with exit 0. PyMuPDF 1.27.2.2 / MuPDF 1.27.2,
eight full pages at 150 dpi, zero saved warnings. Seven PNGs are 1275 x 1650;
physical page 322 is landscape 1650 x 1275. Source, code, original protocol
and Python executable were pinned before/after. Module versions are recorded,
not a hash of the entire installed dependency environment. The source PDF is
read-only. This route avoids, but does not repair, the previously recorded
Poppler font-configuration problem in a different audit.

Root and the separate reader each displayed all eight complete pages once,
with no failed/repeated/truncated image display. Both found complete readable
pages, not precision-measurement quality historical frames. Root additionally
read page 324's extracted text; the second reader read all eight text files.
Neither performed new image-coordinate measurements. Each froze a standalone
note before interpretations were exchanged. A harmless `identity,+a fixed`
typo in the root note is corrected explicitly in MATH-PROTOCOL.md without
changing the frozen note.

Root read-only integrity check exited 0: all four pinned input files matched;
all 17 receipt-listed products rehashed; the exact render directory contained
those products plus the receipt (18 files); all eight PNGs decoded with their
declared dimensions; all eight saved warning strings were empty. Two source
AST parses passed, and both source-reading freezes matched their notices.
The separate reader also independently checked source/protocol/eight PNG pins.

## Synthetic arithmetic

MATH-PROTOCOL.md was saved before numerical implementation/execution. It fixes
six matrix cases, two ideal cameras, nine points, singular/negative-error and
zero-width controls. No after-result sweep expansion or historical parameter
fitting occurred.

Actual producer command from the worktree:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/lateral-geometry-audit/geometry.py
```

Scoped worktree write permission was used. Exit 0; create-only math01.json.
Exact Fraction forward/inverse and zero-width checks pass for all six cases;
singular and negative-error inputs reject; all 18 pinhole plane-distance
identities and six fixed-horizontal-position vertical tracks pass. The three
pinned inputs were unchanged. Root subsequently reran `calculate()` in memory
and exactly matched every stored case, projection and control. Separate calls
to both producers' `main()` rejected their already-existing outputs with
FileExistsError; receipt/result hashes remained unchanged. These are focused
deterministic checks, not a comprehensive library test suite.

The [independent review](independent-math-review.md) derives extrema through
four residual-box vertices using exact Gauss-Jordan elimination, rather than
importing root's inverse-radius formula. Its six-case/24-vertex/18-projection
oracle was frozen before reading the producer. Root subsequently replayed the
entire independent calculation in memory and exactly matched its saved result;
compared all six input/center/interval/zero-test records and all 18 projections
across methods; rehashed both codes/results and the oracle's two input pins;
and verified its existing-output guard without changing the frozen JSON.
Every check exited 0. The distinct case-4 zero-north witness is (1/5,0), not
the origin. This is independent implementation, not independent historical data.

The oracle's first invocation failed at its output write with sandbox
PermissionError, creating no JSON. The unchanged-code scoped retry exited 0.
The separate review preserves both attempts; root does not describe the first
attempt as a successful saved run or a numerical-method failure. One report
update patch failed on a mismatched context line without changing the file;
inspection and the corrected patch succeeded. No acceptance criterion changed.

Several large combined text/status/feedback inspection outputs were truncated
by the tool budget. They were navigation reads, not full source-page coverage
or completed independent review. The entire selected protocol, frozen notes,
new calculation source and all eight full-page image displays were separately
available/read; no clipped tool text is being promoted to full-file review.
No fresh browser/UI or network test was needed for local PDF reading and
standard-library synthetic arithmetic.

A separate text-only critic read the report (pre-correction SHA256
`b1a0ecae3af3cd8a3aabc306ae7cec09e9dd89681231136746cca64c5e1c9978`),
both protocols and both frozen reading notes. Two requested corrections were
adopted: qualify the projection equations/straight-line principle with the
ideal central-camera and lens-distortion assumptions; say a shared historical
feasible-set test is required, not that it has been completed. The critic
found no material objection to the central evidentiary limits, while reserving
independent arithmetic language until the numerical oracle completes. This
was not a third historical-image reading or numerical reproduction.

The completed oracle review (SHA256
`92d2a11bb98233b657fb6058ee8d72d42394abfafe8a949208ff11d3bcaeb889`)
also compares all 24 vertices, interval centers/radii and 18 keyed projections;
replays both programs; and finds no numerical defect or interpretation overclaim
within its scope. Its primary-page review is explicitly absent. Root read the
post-freeze account and verified its final hash. The then-current report it checked had
SHA256 `644f64a01d37a87181f84c674205551cb4ff7c83fbfc3b5e84060006f6aae67f`.
The final report replaces the pending-oracle sentence with the completed
agreement and validation link, without changing equations or results; its
SHA256 is `34d8d60632151611eb36ff81be68511411560a3e0b5bc2514b9d58a7f15f3d68`.

Final focused checks: seven Markdown files' 11 local links resolve; all three
Python files parse; `git diff --check -- research/README.md
research/sherlock-wtc7-investigation/STATUS.md` exits 0. The initial wording
check mistakenly flagged the deliberately quoted frozen-note typo in this
validation record as live prose. After distinguishing that preserved quotation
from the report text, the corrected check exits 0; no scientific text or input
was changed to force a pass. Status and research index now distinguish this
completed bounded audit from the proposed acceleration-transition calculation.

## Fixed pins

| Artifact | SHA256 |
|---|---|
|PROTOCOL.md|`7f38d2e4f7b6295b238772aa91d53ad21c4afc3f7cfd7d8f2c1c95844f180417`|
|render.py|`7d25baaab6f89ad7ad609e04436c1937d231174be4653b3d0bacc097e542f11a`|
|render01/receipt.json|`d63eed304ab1cb1acf5bde5d50db57e2ac3e276e36090f6506522207ab2f365e`|
|root-reading.md|`7fda81cfa9f20596faddabcb6a8822468fbd18e7e45ecb553233d2ec9484a109`|
|independent-reading.md|`2fbeb927a00e717abc743d51c227091a405489009f9cb0febde7c0a9b5d684d5`|
|MATH-PROTOCOL.md|`58d49fe3d792b34ce323882b2f10f97d2e5500cfe62666b9a83005e7645828f2`|
|geometry.py|`526dd122642561b792e097df56bf3c46955f504820419fbac8d02b86f27c06ed`|
|math01.json|`1ad3d659f3a65fb8fe68787de29a0e27e1d315ce71b592fc2751a564606a8aea`|
|independent-math.py|`6235e4e34885770666640b95fa8d043b661dbb1dee091846a336cce1d1ad0d97`|
|independent-math01.json|`6df36e503f0c038e3a4f7870eb55be6abd09bdf3193f3f64571af4a2de6c185d`|

Hashes establish identity, not physical truth. Missing historical inputs and
the exact selected-page scope are stated in the report. A separate-source,
expert or raw-media validation is not claimed. No new generic Sherlock issue
is sent: provenance/calibration and source-versus-run distinctions already
have local feedback entries, and the destination task remains archived with
routing unresolved. A queued requirement is not a verified product defect/fix.
