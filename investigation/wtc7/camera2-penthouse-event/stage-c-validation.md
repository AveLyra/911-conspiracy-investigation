# Stage C execution and verification

Research-only fixed display sensitivity test. Governing [declaration](STAGE-C.md)
SHA-256 `7a1bf712a8d1b5dc629395e2c704afda1cce93068db386f0125e460663b2554d`.
No new decode, source acquisition, original-camera authentication, physical
calibration or solver run. Passing pixel checks is not visual event acceptance.

## Before historical rendering

The independent method review identified three protocol risks, corrected before
rendering: crop context is a condition, not an assumption; a qualifying new
post-state must have its actual next two frames inside the continuous run;
three frames establish a local transition, not final disappearance across gaps
or possible reappearance. The earlier declaration hash is superseded only as
a pre-render draft; Stage B freezes remain unchanged.

Root read the complete final producer and test code. The driver author ran two
successful 28-test synthetic passes; its initial sandbox refusal and exact
attempt history remain in [launch-history.md](stage-c-driver-controls01/launch-history.md).
Root's **separate final-code rerun** used this command from the research worktree:

```
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 research/sherlock-wtc7-investigation/camera2-penthouse-event/test_stage_c_display.py --out stage-c-driver-controls-root01
```

Actual result: **28 tests, zero failures/errors, exit 0**, 3.583 seconds. This
includes five inherited pure-crop controls and 23 producer controls, not 28
independent historical observations. Fresh synthetic outputs are separate from
historical outputs. The controls cover exact mapping, selected rows/PTS,
geometry, pins, animated PNG/render metadata, warnings, changed inputs/code,
output confinement/collisions, failure retention and paired synthetic renders.

Final producer SHA-256:
`a5f932d13ffd2e8f137e5702a547cb89ab73498b58ace81359751dbb0d91892a`.
Tests SHA-256:
`ae75b7eebdab55498857814317d88259ccef9b9525d5e490bbe01959f78af015`.

Root independently implemented a byte-row oracle in
[stage_c_pixel_check.py](stage_c_pixel_check.py), without importing the producer
or calling crop/resize. A separate reviewer found and helped correct animated/
render-metadata and hash-versus-parsed-byte risks. The checker now hashes and
decodes the same captured PNG bytes and hashes/parses the same selection and
receipt buffers, and checks identities again after the traversal. Final checker
SHA-256 `dee8adcbadfb9c4ff7da6ba72e51843a20f8b4b88efde1a6ef99b1f25a0d532f`.

Root's final `stage_c_pixel_check.py --test` execution: **12 tests passed,
exit 0**, 0.019 seconds. It includes actual multiframe PNG and transparency
negative controls, wrong-pixel rejection even with updated hashes, bad types,
dimensions/pins and duplicate-run rejection. Earlier 6/10/12-test development
runs and the reviewer's 12-test run are not additional unique controls.
The final selection-buffer correction was tested in root's final 12-test run.

## Actual historical displays and independent check

After the controls passed, root ran the final producer twice with
`--out stage-c-run01` and then `--out stage-c-run02`, using the same Python
environment/bytecode setting as above. **Both exit 0**, each reporting
`complete`, 71 selected frames and 142 PNGs. Neither run recorded warnings or
a failure receipt. No existing output was overwritten.

Root then ran `stage_c_pixel_check.py` without `--test`. Actual result:
**exit 0, pass-pixels-metadata-only**, 71 source frames, 284 output PNG instances,
142 matching image pairs. Every native pixel and every enlarged 4×4 block
matches integer row slices/repetition from the original preserved luminance.
Dimensions, single-frame format, rendering metadata, encoded and luminance
hashes, ordered source joins, exact PTS and declared/frozen inputs passed.

| Run | Receipt SHA-256 | Receipt bytes |
|---|---|---:|
| stage-c-run01 | 30f7e34c346b1ccdc52a1be5a1b1aac2eaadb8800ff3e702ee84e5e5d2e0552a | 197369 |
| stage-c-run02 | 36b3107ba51c777d259836ee2929a4aed73b7d993db99b5669157f2f36dcb6e3 | 197369 |

The checker shares Pillow's PNG decoder with the producer; it is a separately
written mapping/oracle check, not a second PNG implementation. It does not
authenticate the converted recording or the observer's component identities.

Root separately executed a read-only inventory traversal, **exit 0**. Per run:
157 receipt-listed products (142 PNGs plus 15 snapshot/metadata files), plus
the receipt itself; exact directory membership; no failure.json; empty warning
list; every product's bytes/hash correct; all **79 input** and **seven runtime**
identities unchanged and equal to their before/after files; all **ten snapshots**
equal the current corresponding code/declarations/frozen inputs. The four Stage
B freezes and original selection remain pinned to their prior hashes.

## Pre-exchange visual freezes

Root's actual viewing record: [scope](root-stage-c-scope.md), **71 distinct
images /71 displays**, no repeats or failures, all complete 660×480 enlarged
images in declared ascending order. No native crops separately displayed.
Root saved its two files before receiving the observer's findings:

- root-stage-c.md: `b2a7a5e935fdb9f2761d2141e5669e0e7e652fb7dca89a76f75ebb7c4272308f`.
- root-stage-c-scope.md: `c12ccd24b72dd8f04350baa765ac32ebedddc6cf5c0f16d512b36d6442fc6280`.

The observer completed and froze its records before receiving root findings:

- observer-stage-c.md: `a898e437cf544ed3ed0cda5926a4808725690c34c05c91bedaa9cc7f26edb569`.
- observer-stage-c-scope.md: `0b74d813694fc15a1bc315915e233facaf852f2e4811f7a5708c31aaaf2ab6d6`.

Root freshly rehashed all four Stage C files, confirmed both freezes and then
authorized exchange. All hashes matched. Root read both observer files fully;
the observer subsequently read both root files and supplied a post-exchange
comparison without new images or file changes. Observer coverage is 71 distinct
complete images, 75 successful displays including four repeats. One wholly
truncated ten-image request was excluded and then reopened successfully. The
observer's scope also preserves a wrong-path and an empty-selection arithmetic
attempt before its corrected exact-row check; neither affected source files.

Both reviewers see a continuing image feature through6978 and neither identifies
a qualifying component-specific crossing. The observer's optional6978 arithmetic
and root's decision not to extend the component-specific accepted bound are
compatible conditional treatments, not conflicting visual observations. The
post-exchange review expressly preserves that distinction and the old bound's
conditional status. No expert-human or independent-source confirmation follows.

Root independently ran a read-only Python3.13.7/Fraction check against the
pinned selection JSON: asserted exactly indices6714,6717,6958,6978,7013 and each
PTS×timebase identity; checked both old6958 differences and both new6978
differences. **Exit 0/PASS**. New differences are26399/2997 and26099/2997 seconds
(8.808475141808476 and8.708375041708376). These numbers verify arithmetic only;
the late-component attribution remains unaccepted. Neither supplies an upper
endpoint, a first-crossing time or an authenticated historical-clock interval.

## Independent root-text review before exchange

The producer author separately read only the declaration and root's two frozen
Stage C Markdown files, with no historical image review or observer findings.
It identified one narrow referent ambiguity: root's phrase “6959 the first
absent frame” must mean the first frame **without a visible bump**, not the first
frame without the intended penthouse component. A different corner could supply
the bump after that component has disappeared. The synthesis must state that
distinction expressly; the original freeze is preserved. No other material
text/protocol conflict was found in that limited review. This is not a third
visual confirmation or a physical component-identity finding.

A documentation append initially addressed a nonexistent path (omitted the
research prefix); it failed without writing. The corrected scoped append
succeeded. This did not affect any image, frozen annotation or execution.

## Final synthesis review and continuation

After exchange, the same text reviewer read the new synthesis and observer's
frozen annotation. It found no material text defect: the bump referent is
corrected, conditional6978 arithmetic is retained without adopting component
identity, both observations and the hard stop are preserved. This review was
text only, without images or writes. Root's exact metadata check is separate.

The existing STATUS.md/research README now route to Stage C and the bounded
15-image CBS–Peskin window-fire association plan. A separate read-only lead
reviewer selected those existing inputs; root read the CBS and Peskin reports
and independently checked all15PNG byte hashes/paths, exit0. No image has yet
been viewed for that next test; manifest locator joins and visual work remain
pending. Generic display-integrity feedback extends existing SFB-002/SFB-004
locally only. No archived-task send/reopen, accepted-engine or legal mutation.

State: branch `research/sherlock-wtc7-investigation`, HEAD `e8d83d7`; intentional
WIP/unrelated changes preserved. No commit/push. All bounded Stage C processes
and visual passes are terminal. The comprehensive investigation remains active.

Final documentation checks actually run from the research worktree:

- `git diff --check`: exit0, no output.
- `python3 /Users/admin/docs/911/tools/validate_record.py --strict`: exit0,
  `OK (headers + issue↔fact links + citation tags)`.
- Read-only explicit Markdown traversal: exit0/PASS, eight new protocol/
  annotation/scope/report/validation/next-plan files, 16 local links, nine
  declaration/freeze hashes, no trailing whitespace or conflict markers.
- Final synthesis SHA-256:
  `d3cc7ab9935ff811b0f5c3f2c605b34fdae7fad50baeef4c24009471d2c31e8d`.

These are record/document checks, not physical validation. The final append
does not alter any freeze, source, program or synthesis hash.
