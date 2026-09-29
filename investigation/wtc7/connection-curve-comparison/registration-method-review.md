# Registration controls and bounded method review

2026-09-27. Working research. Owner `/root/curve_method`, reused prior-informed
AI reviewer and earlier curve-arithmetic author. This is not actual human
review, historical curve identification, engineering approval or a calibration
result. Only this note, `registration_controls.py` and
`registration-controls01.json` are owned by this job.

## Scope and freeze order

Read the complete `REGISTRATION-STAGE.md`, `NUMERICAL-PROTOCOL.md`,
`HUMAN-REVIEW-GATE.md` and `technical-preparation.md`; current main CHARTER and
controls were read in the preceding readiness task and their unchanged hashes
checked. Evidence-falsification and source-of-truth skills and their references
were read for that task; the development-verification skill was read for this
implementation. These preserve source/gate boundaries and require actual
verification rather than treating plausible formulas as verified software.

The synthetic code and successful receipt were frozen and reported to root
**before** reading either new candidate registration. After that freeze I read
the complete root registration below. The separate reader's new registration
was not yet present at that point. I did not read viewer implementation, open
historical images, decode a JPEG, obtain curve ordinates, compute graph/model
discrepancies, run a solver, acquire a source or edit the pending five-family
matrix. No file in main, an older frozen record or another owner's files changed.

The code is independently implemented for this bounded task and does not
import the viewer or other registration programs. It is **not** an independent
historical source. Its test expectations are hand-authored by the implementation
author; a passing suite and repeat are not a separately authored oracle or a
human mapping check. Root has been given the full code and runnable command
for separate review/replay; this note does not assert that those happened.

## Exact geometric contract

Only a positive, axis-aligned image CTM `[a,0,0,d,e,f]` is supported. Rotations,
reflections, shears and nonpositive dimensions are rejected, not approximately
handled. For image dimensions `W,H`, image-edge coordinates use upper-left
origin and the continuous domain `[0,W] × [0,H]`:

```text
PDF X = e + a*u/W
PDF Y = f + d*(1-v/H)
u = W*(X-e)/a
v = H*(1-(Y-f)/d)
```

Pixel indices instead stop at `W-1,H-1`. An indexed pixel is a cell footprint,
not a zero-area sample at an edge or center. Exact `Fraction` arithmetic avoids
float roundoff in the synthetic calculations. API numbers must be integers or
Fractions; booleans, strings, floats/NaN/infinity and malformed/reversed inputs
are refused. This exact toy arithmetic does not claim historical CTMs have
infinite source precision.

For an unrotated page box `[x0,y0,x1,y1]` rendered at `Rw,Rh`, the render cell
`i,j` maps to the appropriate `dx=(x1-x0)/Rw`, `dy=(y1-y0)/Rh` footprint with
the y axis inverted. A supplied nonnegative extra render-pixel radius expands
the entire footprint. The radius is an explicit caller allowance, **not an
estimated error distribution**. An envelope beyond the page is rejected rather
than silently clipped. This intentionally narrow edge policy may require a
separate explicit clipped-status policy for future boundary selections.

Each strip uses its own CTM and dimensions. All intersecting strips are
returned. Since uncertainty envelopes are closed sets, an exact seam contact
is retained with `boundary_only=true`; it does not supply nonzero support or
an additional native pixel. Overlapping candidates are not resolved by their
order. Every candidate is marked visibility-unverified: geometry does not
apply PDF clipping, overpainting or model/legend identification.

## Synthetic controls actually run

Twenty named `unittest` cases passed. Individual cases contain additional
subtests; they are not claimed as twenty independent validation datasets.

| Control | Declared truth / tested failure mode |
|---|---|
| Known CTM corners and interior | Both directions give independently hand-specified coordinates. |
| Upper-left y convention | A point near the PDF top maps to native row2, not18. |
| Cell edges versus center | A full source cell and its center remain distinct. |
| Differently scaled last strip | Identical 100×20 dimensions with PDF heights10 versus8 give native v12 versus10 at the same admitted point; uniform-height substitution is detectably wrong. This is synthetic, not a fit to Im5. |
| Render quantization | The first 200-dpi cell on a 612×792 page has exact PDF footprint `[0,19791/25,9/25,792]`. A translated-page fixture is also checked. |
| Quantization plus assessed radius | A half-pixel expansion enlarges both bounds; it is not confused with the center alone. |
| Seam crossing | Both strip candidates and their respective native envelopes survive. |
| Exact seam boundary | Zero-height intersection is retained but labeled boundary-only. |
| Overlapping footprints | Both candidates survive; no inferred unique owner. |
| Outside footprint | Empty candidate list, not an extrapolated native coordinate. |
| Invalid values and geometry | Nonfinite/boolean/float input, malformed CTM, shear, zero/negative dimensions, empty/reversed rectangles, duplicate names and out-of-range points are refused. |
| Conservative support | Explicit clear/same-identity/visible/adjacent declaration can pass; crossing, occlusion, ordinary dash gap, clipping, overprint or unknown status cannot. |
| Unknown identity / visibility | Remain unsupported, not converted into a larger numerical error bar. Different labels and nonadjacent samples also fail admission. |
| Known synthetic raster localization | Directly constructed RGB marks at three known cells are found exhaustively after exact3× replication; inverse envelopes cover exactly their original cells. |
| Larger render | Subcell footprints can get smaller while native source dimensions remain unchanged; no finer source resolution follows. |

The raster fixture is built only in memory: 17×9 RGB, three categorically
colored marks at cells(0,0), (16,8), (7,4), replicated to51×27 with direct row
construction independently of the coordinate transform. Exhaustive byte scans
recover exactly nine rendered cells per mark (27 total), and the union of
inverse footprints equals each known source cell. No raster is displayed or
saved. Source RGB SHA256:
`ac769c5465cbc2c12016507f6997085476c480ad0c93a125c35374d387e3dc28`;
replicated RGB SHA256:
`6c510b9034a4cf8e0a4dd20e8352d1d2eda8486e49e3e6832fd8dd7675cd4822`.

This tests simple known-pixel localization and inverse registration, **not**
JPEG decoding/artifacts, antialiasing, PDF rendering/compositing, real line
width, color confusion, dashed-line recovery, a human click, a browser pointer
mapping or historical image-based uncertainty. The support function operates
on explicit trusted declarations; it cannot prove those declarations true or
detect an unreported crossing inside a segment. It is a conservative policy
guard, not an image classifier or a complete supported-branch constructor.

## Commands, actual outputs and failure preservation

Working directory:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison`.

1. `python3 -B registration_controls.py` — exit0;20 controls, no failures/errors;
   stdout only.
2. `python3 -B registration_controls.py --out registration-controls01.json` —
   first default-sandbox execution failed at exclusive file creation with
   `PermissionError: Operation not permitted`. This was a write-permission
   failure, not a failed arithmetic assertion. No receipt was created by it.
3. The same command, with normal `require_escalated` approval for the one
   dedicated-worktree receipt — exit0, exclusive-created the receipt;20 controls
   passed, no failures/errors. No alternate destination or overwrite was used.
4. `shasum -a 256 registration_controls.py registration-controls01.json` — exit0,
   pins below.
5. Read-only `python3 -B -c` replay used `subprocess.run(["python3","-B",
   "registration_controls.py"],capture_output=True,check=True)`, asserted empty
   stderr and exact stdout-byte equality with the saved receipt — exit0,
   `PASS: stdout replay exactly matches saved receipt; 20 controls`.

Runtime: Python3.14.0, executable
`/opt/homebrew/opt/python@3.14/bin/python3.14`; standard library only. The
receipt intentionally has no elapsed time/date, so same-runtime output is
deterministic. Different runtime/executable fields would require field-level
comparison, not a claim of byte equality. No browser test was performed by
this agent; the viewer's separate owner/root must test its own actual mapping.

| Artifact | SHA256 |
|---|---|
| registration_controls.py | `98873f48740f69499f509e1e1db5c425586d25811e83ae9c88c862db7e54bc54` |
| registration-controls01.json | `6fc33fd629226cb6033ba2839c3710dc7fefed129aef3008f442457024931b7f` |
| REGISTRATION-STAGE.md | `18e212edcf4950f370bd30119597b20f786015d61da03fe4aeb19b23125f004c` |
| NUMERICAL-PROTOCOL.md | `e03c47c1945b9eb9fd0a040d757d5f5f66bf76791ced8944323d3c92d1120df3` |
| HUMAN-REVIEW-GATE.md | `2e6f34d2e2d6d423c440c8a56b4a3c4796429d59f4d0baf0cf03609341a271ee` |
| technical-preparation.md | `a4d820f468dd80932f4144048eba545e70129f994c4b93e0f02f6a7f88e54550` |

Code checks the four local instruction pins before and after controls and
also its own bytes before/after. These guards were exercised on unchanged
inputs only; changed-pin, exclusive-create collision and symlink behavior
were not fault-injected. Do not label the output path guard a general security
certification. No new historical geometry/curve arrays are accepted by its CLI.

## Post-freeze root-registration review

After the controls freeze, read `registration-root.md`, parent-supplied frozen
SHA256 `ec66ae85a45a0169b7e8cc61698cc522e75cda2f2905f4c283f45f88de1f55a7`.
Its stated inverse mapping, render-cell convention, strip-specific Im5 warning
and source-resolution ceiling agree with the tested contract. Its interior
tick coordinates are explicitly predictions, not independent measurements;
its +/-3 rendered-pixel allowance is assessed, not empirically calibrated.
I did not inspect its images or independently remeasure any proposed anchor.

One concrete completion issue was sent to root: the assembled registration
must retain **all six anchors' full assessed-plus-cell PDF/native envelopes**,
including every candidate strip at a seam. Three center-coordinate examples
and correct formulas alone are not the complete interval registration called
for by REGISTRATION-STAGE. A supplementary numeric mapping can complete this
without changing the frozen observation or claiming new curve measurements.

The root note correctly refuses to use geometric containment as proof of
visibility, distinguishes clipping graphics-state scope from a page-wide
mask, and keeps underlying white-overpaint areas unavailable. These are
appropriate limits; the present controls do not themselves verify the actual
historical PDF graphics-state sequence or masks.

**Disposition at this freeze:** the narrow synthetic mapping/support controls
pass. Root registration's stated method is consistent at the text level,
subject to the full interval mapping completion above. Separate candidate
registration, comparison, viewer/browser verification, actual human review
and all selected curve-sample checks remain distinct. No historical tracing,
calibration-fidelity finding, work/dissipation identity or cause conclusion is
cleared by these controls. Main/raw/legal/engine and pending matrix boundaries
are unchanged.

### Subsequent root review/replay receipt

Root subsequently reported reading the complete controls and rerunning them
with the bundled Python3.12.14: all20 passed, with the entire resulting JSON
equal to the Python3.14.0 receipt except `python` and `executable`. Root also
reported independently deriving all six full envelopes before importing this
code and subsequently obtaining exact Fraction agreement with its functions.
These are explicitly parent-reported review/replay results; I have not
rerun that separate derivation or inspected a separately saved root receipt.
Root committed to include the full native intervals in the assembled
registration after the other reader freezes; a promised addition is not yet
an inspected completed artifact. None of those six assessed envelopes is
reported to cross a strip seam, but the generic seam controls remain needed.

My fresh `shasum -a 256` confirmed the actual frozen root-registration hash
quoted above and both unchanged code/receipt hashes. The method note before
this append was SHA256
`d2cb6e2894f14a5ad55db911f4aae0aadb547450e51a528e0c389e80ecd6e5f5`.
There is no remaining permission request from this completed control run;
the one receipt was actually saved. Scientific acceptance is different:
the actual-human gate and future historical curve-sample checks remain unmet.
