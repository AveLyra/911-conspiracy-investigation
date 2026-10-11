# Synthetic delivery diagnostic execution

October 8, 2026 local / October 9 UTC. Research worktree branch
research/sherlock-wtc7-investigation, HEAD ca1c223335c20905d6608eb15c676f88cbfac734.
Current main AGENTS, WORKFLOW, START-HERE and CHARTER pins matched their
previously read versions (47d3a1). Original localization protocol, report,
human instructions, controller, core and tests were read before implementation.
The development-verification and native-browser skills control software QA;
evidence/source-preservation rules keep synthetic controls separate from human
observations and preserve the original unresolved miss.

Original viewer session 43737 was polled at 6a65ac and remained live. It was
not restarted. The existing native-browser connection listed its original
tab at http://127.0.0.1:55462/. Read-only DOM inspection confirmed synthetic
control selected, no point or box, six uninspected historical rows and no
synthetic practice draft. No historical image was selected or displayed by
this unit. Later diagnostic interaction will use a separate tab and server.

Before diagnostic implementation, root read the existing synthetic geometry:
1280 by 720 native; browser viewport 1280 by 720 CSS pixels, DPR 2;
image rectangle left20.1953125, top360.609375, width792.8828125,
height445.9921875. Page/region scroll were zero. This was an original-viewer
DOM observation, not a calibration of physical display or historical footage.

The protocol froze before the new code was written at 078aa3, SHA256
c1b27cc20a7ed57498f9398743cd9bf46491030071b9ad4bbb9c58d9b5b39e9c.
It fixes twelve synthetic intended cells and distinguishes mapping of delivered
input from accuracy of intended targeting. A separate reader demonstrated a
constructed rounded-input counterexample (9ed5c0); it was not an observed
browser event or reconstruction of the prior miss.

## Baseline regression and preservation

From the original localization-review directory, root ran:

```sh
node --test test_response.mjs test_mapping.mjs ../../comparator-r1-replication/test_coordinate.cjs ../../connection-curve-comparison/test_coordinate.mjs
node verify_packet.mjs
```

Launch 2eee88 returned session54205; same-handle result595c12 completed exit0.
All55 JavaScript cases passed. The separate packet check passed both six-file
packet copies, 660 predecessor pins, 17 packet-input pins, twelve declared
routes, exact helper bytes and nullable metadata. Its HTTP option was not used;
this run did not recheck live route bodies. These are preservation/regression
controls for the new diagnostic, not new scientific measurements.

Runtime check879f88 reports Node22.16.0 and bundled Python3.12.14. Its unrelated
git-status invocation used root-relative paths from the unit directory and
warned about a nonexistent nested path; it is not relied on. Correctly rooted
status75ddb7 confirmed the existing untracked localization tree. No existing
packet, historical response or accepted finding has been modified.

## Implementation, setup failures and final build

Execution continued into October9 local. The independent source/handler pins
are in the manifests; final code is not a modification of the original viewer.
Root reviewed the builder, server and logger. Root tests69d040 passed10 Python
and8 Node cases. Agent final tests8295a5 passed the same18 after a final server
guard preventing import-cache writes; source syntax also passed there.

The first two derivative packets were built and checked at33b33f. Server8250
started on50719 at55f55e. Root had acted on a ready/no-more-edits message while
the agent was adding only `import sys`, its explanatory comment and
`sys.dont_write_bytecode = True` to the server. The resulting source-pin race
was detected at9c1373; no original packet was affected. Packet01/02 retain the
old server pin b6eb347e70262a0aab69576a2f2bc2e76a2db7df9774e61db7801ec5a73c1cb4
(2502 bytes). `serve_diagnostic-pre-guard.py` was reconstructed by removing
those exact additions and verified against that pin at878580. This is a
matching reconstruction, not a contemporaneously captured backup.

No actual click was delivered on that first server. The attempted
`fitDiagTab.cua.click` failed because the selected native browser exposes AX,
not that API. The subsequent DOM observation showed zero logged events and
no point. Root read the current browser API documentation and used its real
`ax.click([x,y])` action for acquisition, not injected page events. Server8250
was deliberately stopped atd84114. No packet was overwritten.

After final source freeze, these actual commands all passed at9a653e:

```sh
python3 -B build_diagnostic.py build --out packet03
python3 -B build_diagnostic.py build --out packet04
python3 -B build_diagnostic.py check --out packet03
python3 -B build_diagnostic.py check --out packet04
```

The final server source SHA is
9a12fb74233e184e71d27d41bdfa72bbe8a0066f813e77a506e8899b0e90b990.
`python3 -B serve_diagnostic.py --packet packet03 --port 0` started session53124
on http://127.0.0.1:50885/ at5a574c. Diagnostic browser tab4 was separate from
original tab2. Packet03 and04 manifests both hash to
2e4130478c8248f3151e3d8af46a460113e480714af58f17267a7b528ce5de63.

## Actual acquisition and computational review

All twelve prescribed cases completed in order. Each requested position was
computed from a fresh read-only DOM rectangle and each delivered triplet was
saved before advancing. The individual case JSONs and `browser-cases.json`
retain intentions, requests, events, selected cells and complete empty draft
snapshots. Five `browser-log-*.json` chunks retain the full42-event log,
including zoom triplets19–21 and31–33. `keyboard-observations.json` records the
four real arrow-key actions. No case was replaced or omitted.

Root's independent checker tests6f647b passed16 cases; actual checker run0ba1c7
passed all12 observed delivered mappings, with one retained intended miss and
no recorded geometry change. Its exact stdout is `verification-root.json`.
Separate reviewer results and reconciliation commands are in
`independent-review.md`; `verification-peer.json` is byte-identical to root.
Root read that complete review atb1cef4. There was no material correction to
the observed-result interpretation. Checker independence does not mean blind
sampling: schema alignment finished after the first root Fit observations,
but before the separate reviewer inspected actual data.

## Closeout checks and screenshot

Final root commands at8d6824, from this directory:

```sh
python3 -B -m unittest test_diagnostic.py
node --test test_diagnostics.mjs test_delivery.mjs
python3 -B build_diagnostic.py check --out packet03
python3 -B build_diagnostic.py check --out packet04
```

Results:10 Python tests and24 Node tests passed; both final packets matched
their exact derivation. Root reran the original baseline commands above at
26f99b (session10239), completed c73cce exit0:55 tests passed,660+17 pins and
both original packet copies unchanged. Its HTTP option remained unrun.

`node verify_closeout.mjs 50885` initially failed with sandbox EPERM at9c367d.
That was not a server refusal or successful HTTP check. The same read-only
command, after scoped escalation, passed at9a2209. Saved stdout is
`closeout-check.json`:14 input pins, seven identical files per final packet,
four unchanged original modules, one appended HTML tag, seven successful
allowlisted routes and seven refusal/HEAD cases with restrictive headers.
The checker imports no producer module. No public server or external request
was used for these tests.

After acquisition, one real page-scroll action moved pageY from0 to720 for a
readout screenshot; it did not select a point or add events. Final DOM values:
control selected; locked(200,100); no pending box;0/6 historical draft rows;
no synthetic draft;42/100 events,42 completed,0 pending; viewport1280x720.
The returned browser screenshot is JPEG, not PNG. A direct attempted write
into the worktree failed EPERM and produced no saved image. Root retained the
same screenshot bytes in memory, saved them exclusively in an authorized
mktemp directory, then used an approved `cp -n` to preserve them as
`synthetic-final-view.jpg` (28d61d). Source/destination SHA256 both equal
41c6615c0274c0b6e018007da1fc3546dccd3142f7ddd6a1f132718c17692a37.
No image transform was performed. Root visually inspected the screenshot;
it contains the synthetic fixture/readout and disabled response controls,
not historical footage. One tool-output forwarding mistake printed encoded
synthetic image data instead of rendering it; the subsequent correctly
forwarded image was inspected. That transport output is not measurement data.

Root sent Ctrl-C only to diagnostic session53124 atf4bfc1; its subsequent poll
reported unknown process ID. No exit code was returned in the stop receipt,
so none is asserted. Original session43737 was separately polled atbc6136 and
remained live. It was neither restarted nor stopped.

Fresh main control pins at6a1d36 match the initial pins. A mistaken relative
material-index hash path atb518f3 did not resolve; the corrected absolute-path
check c3728f returned the unchanged frozen index hash
e9aac5145a7d0b631474ece1d4b8082ba0f9a53ee0a5daaaf1a531dd9b009ff8.
Branch/HEAD remain as stated above. Existing dirty work is preserved. New
results, report, deduplicated local feedback and navigation are uncommitted;
no legal record, accepted-state promotion, transmission or push occurred.

Final separate wording review narrowed "the browser received identical
coordinates" to "the logged click events carried identical coordinates";
the saved observations do not identify the browser's internal input boundary.
The reviewer found no other material issue within that final wording check.
`lsof -nP -iTCP:50885 -sTCP:LISTEN` atff17c4 returned no listener (exit1).
Tracked navigation/feedback whitespace check63dcf8 passed. Its large aggregate
diff counts include extensive pre-existing WIP and are not this turn's change
counts; no consolidation or commit was attempted.

Final local read-only assertions039329 parsed26 JSON files, checked five text
files for trailing whitespace and resolved nine relative Markdown links.
Root/peer summaries match; the original packet manifest, frozen protocol and
saved screenshot retain their stated pins. The failed PNG write left no file.
These are artifact checks, not additional browser observations or physical tests.
