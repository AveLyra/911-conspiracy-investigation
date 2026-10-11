# Verification record

October 8, 2026. Research-only. Commands below ran in this directory unless
otherwise stated. Let P denote
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Root and raster runs: Python 3.12.14; Pillow 12.3.0; JPEG library 6.2;
Node v22.16.0. The separate packet checker's save used Homebrew Python 3.14.0
at `/opt/homebrew/bin/python3`, not the bundled runtime. Root's 3.12.14 replay
matches that receipt exactly; these execution environments remain distinct.
The raster results pin the Python executable and Pillow imaging binary;
this does not pin every shared library or certify the machine.

## Preserved outputs

| Artifact | Bytes each | SHA256 |
|---|---:|---|
| packet01.json / packet02.json | 211388 | `cb0f9da2f36e384eeeb046528696bba4f379fc8419f393a18ae2f809b05829cc` |
| independent-check.json | 79651 | `cc822cf3cb0214f9e3901a0d554af922363383518a18418b034bcde132d0760d` |
| raster-challenge01.json / raster-challenge02.json | 387949 | `5c2a47be28c134eee6b9eaf142353b10aa3f9f09ba31ec6d3da4b9ddcbb434c5` |
| viewer-data01.mjs / viewer-data02.mjs | 135023 | `9fbb8fb4c5c27832a39fa6b9c729fd18aef52350799efa89f09050d5d1823bff` |

Protocol SHA256 is
`ffa2fc84231d2b19dedfc6be7272460f05a980cdf6c5c6d8f15c36a66e8baaa9`.
It was declared and separately reviewed before selection/results. Four
pre-freeze clarifications retained distinct reading records, open boundaries,
length-only merging and source-footprint duplicate definitions. A failed
patch-context attempt made no change. No later protocol or source annotation
was modified to obtain these results.

## Execution and root replay

- `P -B packet.py 01` and `P -B packet.py 02`: two separate exclusive saves,
  both exit 0; receipts cf1b85 and 4e7c81. Both outputs have all 222 input pins
  before/after. Root freshly rebuilt with `packet.encode(packet.build())` and
  compared exact bytes against both outputs (6ea4a6, exit 0).
- `P -B render_packet.py 01` and `02`: exclusive presentation saves, both exit
  0 (7622eb). Root freshly rebuilt `render_packet.build()` and compared both
  outputs exactly in 6ea4a6. The server also reconstructs and verifies the
  wrapper against the frozen packet at startup.
- `P -B -m unittest -v test_packet.py test_envelope_math.py test_raster_challenge.py test_independent_check.py`:
  **63 tests pass** (928bf0 / a1fc5d). Counts are 11 selection/mapping, 19 exact
  arithmetic, 15 raster challenges, 18 independent checker/oracle tests.
- `P -B -m unittest -v test_serve_review.py`: **17 tests pass** in root's
  approved loopback run (a4b7bf). Tests mutate only temporary synthetic
  fixtures. Real packet/source assets are only read.
- `node --test test_review.mjs`: **7 tests pass** after the trace-color and
  scenario-state presentation additions (b7322a). Final presentation changes
  are rechecked at closeout below.
- `PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py --expected-sha cb0f9da2f36e384eeeb046528696bba4f379fc8419f393a18ae2f809b05829cc --save-receipt`:
  separate agent's exclusive receipt save, exit 0 (a4febd). Root freshly
  re-ran the complete verification and matched receipt object and bytes
  exactly (2c0fac). All 222 required-pin omission checks reject the mutation.
- `P -B raster_challenge.py --output raster-challenge01.json` and `02`:
  separate executions exit 0 (4fa939, bb8fd5), exact byte equality and all ten
  before/after pins checked. Root `P -B raster_challenge.py --check raster-challenge01.json`
  rebuilds the full result and matches exactly (5c3509 / 745157).
- Root's separate read-only inline Python inspection (271ba7) imports no
  producer helper: decodes/checks every encoded image hash, byte count,
  dimension and decoded hash; independently totals all 1,024 record outcomes;
  verifies all six equal encoded pairs; and checks the quartic extrema/sample
  zeros and the 1/8-column gap algebra. It shares Pillow, not an independent
  decoder. This is an integrity/algebra check, not a second synthetic renderer.

Exact root receipt replay:

```sh
P -B -c 'import independent_check as c; p=c.HERE/"independent-check.json"; r=c.verify(c.HERE/"packet01.json",c.HERE/"packet02.json","cb0f9da2f36e384eeeb046528696bba4f379fc8419f393a18ae2f809b05829cc"); assert r==c.load(p); assert c.encoded(r)==p.read_bytes(); print(c.pin(p))'
```

P above is notation: substitute the stated absolute executable, not an
assumed shell variable. Producer, checker, mathematical module and test pins
are retained inside the results/receipt. Root independently rehashed all 22
current code/protocol/result/presentation files in 271ba7; scientific output
hashes match the freezes. The [presentation receipt](presentation-verification.json)
records final UI pins, bounded test coverage and the local preview.

## Independent review coverage

The packet checker imports no producer/admission/selection/mapping helper.
It selects from original elementary segment cumulative lengths, independently
checks all four scenario states, transforms all four rectangle corners,
inverts through endpoint interpolation, compares duplicate footprints
pairwise, and parses image dimensions from JPEG/PNG headers without Pillow.
It checks the entire required dependency closure, not merely the producer's
listed subset. Schema/protocol were inspected; this is prior-informed,
shared-input computational review, not blind source reading or expert opinion.

The separate arithmetic oracle enumerates direct physical scalar ordinates
and complete shared axis states for 16 synthetic panel/domain/axis cases;
it does not call producer difference/integration helpers for expected values.
The raster challenge received a second analytic review of the C1 quartic,
its extrema and zero derivative at its compact-support endpoints, and the
unsampled gap. That reviewer reran 15 tests but did not rerun the full build.
Root did rerun that build. Prior manual trial results are inherited and
unchanged, not newly scored by this challenge.

## Browser and server verification

Native Codex in-app browser, fixed loopback origin, no external requests.
The server uses the preserved read-only handler SHA256
`1ea233c4fa8074298f9791a305fa46f0b1ac3151ce00ce48c8edd7e99de48142`.

- All 42 CE views were selected; all 180 native image instances loaded; all
  four alternative-state labels were present; every real response remained
  uninspected. Ten boundary slots and three empty F7 slots matched the packet.
- The unchanged full-page image loaded at 1700 by 2200, with four locators
  for F3Q1. This is rendering verification, not acceptance of those locators.
- At 200% and, after presentation additions, 400% synthetic zoom, the pointer
  locked native (320,180); Right moved it to (321,180). Escape cleared it.
  The synthetic response stayed separately labeled; clear removed it without
  changing the 84 historical states. Copy reported success. At 100% the overlay
  toggle hid all overlays. Returning to 200%, next/previous navigation and
  full-page expansion worked. No warning/error browser logs were returned.
- Final UI wording names panel, bolt count, color, style, all reader scenarios
  and fragment IDs. The final small usability correction clears a stale
  “Copied” notice when the table changes; it does not change packet data.
- HTTP tests cover exact GET bytes/MIME/length, bodyless HEAD, restrictive
  headers, foreign Host/Origin rejection (403), unlisted/query/traversal paths
  (404), unsupported write methods (501), and per-request changed/deleted/
  leaf-symlink asset rejection (409). No source-code, JSON packet, directory
  browsing or arbitrary filesystem route is exposed.
- Bounded limitation: ancestor-directory symlinks are not rejected solely
  because they are symlinks. The explicit test establishes that a changed
  redirected target still fails its content hash. This is not a full security
  audit or protection against arbitrary same-user code modification.

An initial AX root-scroll action encountered a detached-element error; no
response was recorded. Screenshot-grounded scrolling recovered it. A scroll
position query preceded completion of a scroll; the subsequent screenshot and
fresh geometry were used for the successful pointer checks, not stale values.
No historical response was simulated. Synthetic clipboard/table content is
not an attributable human review.

Final closeout repeated all 42 views / 180 image mappings with every scenario
label visible and all 84 real entries uninspected after the last UI change.
Copy succeeded; clearing the synthetic response also cleared the stale copy
notice. Final seven JavaScript tests pass (42ec39). The saved preview shows
F3Q1 with no accepted responses. The same-origin server was restarted with
final pins (48769d), session 56853, at `http://127.0.0.1:61594/`; this is an
ephemeral local session, not permanent hosting. No warning/error browser logs
were returned. Actual inspection/acceptance remains absent.

## Retained execution limits and failures

Initial un-escalated server bind, independent receipt save, raster save and
HTTP fixture tests encountered sandbox permissions. Scoped approved retries
succeeded without changing scientific criteria. The HTTP suite's first
blocked run had eight passes and nine pre-execution socket errors; it was not
a clean run. Exclusive saves preserved all existing outputs. A pre-save
raster declaration-string typo was corrected before frozen outputs; no scene,
threshold, halo or outcome-dependent selection changed.

Source integrity, arithmetic, UI behavior, actual human inspection and
physical validation are separate gates. This unit supplies only the first
three within the coverage stated here. No original-curve enclosure guarantee,
historical discrepancy, accepted support, collapse reconstruction, engineering
opinion, engine acceptance, legal result or charter completion follows.

## Final closeout integrity checks

The read-only closeout command (faab3a / 64b024) rechecked all seven
presentation/handler pins, the saved screenshot hash, exact replay of the
independent receipt, 13 local links in the four new review documents, and all
17 server assets at startup. All those assertions passed; human acceptance
remained false. Its final shell loop stopped with exit 1 at the first
`git diff --no-index --check /dev/null` invocation, before checking the rest
of its file list. This was not recorded as a successful complete command.

Each of the ten new presentation/review files was then checked separately
with `git diff --no-index --check /dev/null FILE`: all ten returned exit 1
with empty diagnostics (e017e0 through 9c2a51), the no-index difference
status, not a whitespace finding. The scoped tracked-document check
`git diff --check -- research/README.md research/sherlock-wtc7-investigation/STATUS.md research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md research/sherlock-wtc7-investigation/connection-curve-comparison/technical-preparation.md`
ran from the worktree root and exited 0 (45048e). These checks cover this
unit's named files, not all unrelated worktree changes. The same server
session 56853 remained running (443e3e).

After the initial critical-review snapshot, the report gained a link to that
review and replaced its pending-review disposition with the qualified final
disposition. This closeout record was appended. Frozen protocol, scientific
outputs, source annotations, presentation assets and all acceptance states
were unchanged. The critical review retains its original snapshot hashes;
any follow-up snapshot is identified separately there.
