# Updated packet verification record

October 8, 2026. Research-only. This record separates executed checks from
pending work; it does not supply human acceptance or engineering validation.
The prospective [protocol](PROTOCOL.md) and [method review](method-review.md)
preceded this version's historical sample selection.

## State and runtime

Dedicated worktree `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`,
branch `research/sherlock-wtc7-investigation`, HEAD
`ca1c223335c20905d6608eb15c676f88cbfac734`. Existing unrelated research changes
were preserved. All work here remains local and uncommitted; main/raw/legal
files and the frozen material-claim index were not edited.

Commands below run from this directory unless specified. `P` denotes
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`;
commands actually used that full executable and `-B`. No bytecode writes are
needed. Shell calls used `login:false` and an explicit workdir.

## Declaration and original preservation

Repository intake ran (`a9fa71`). Main AGENTS, WORKFLOW, START-HERE and CHARTER
were checked against their known hashes (`75ae3a`); user-supplied current-main
controls outrank the older worktree instructions. Required skill/reference
and relevant old protocol/code/report reads preceded edits.

Method review examined protocol SHA
`b07d4319a3d675a20f0fa8a368855631999f93673db37b820b7e3d2a583ff273`.
Its clarification was applied before historical selection: CE IDs are stable
quantile-slot labels, not stable source coordinates. Frozen execution protocol:
`c3081a9ca870d0b67ddee5cec2d7dc4d346db137711baf1dbdc39af3bc362651`.
No sampling rule, input or acceptance threshold changed.

The old packet/viewer preservation snapshot (`02814a`) is:

| Original file | SHA256 |
| --- | --- |
| review.html | `7bee34510477e5b911f84ba3dd2380a447d46b86e2ab58389edca34053c6b2c6` |
| review.mjs | `509142c1cd0ddecfd864aa904de31b16773076305026c60de793621920ba7082` |
| serve_review.py | `6c1913c83a38ff6f1cd5ae1a2c8037f0fa7312a12501ed3d947bf364fd33c541` |
| render_packet.py | `514425a36d5b2327ced15c97f7603e1eba208c4d2e57983789076a0f43e6b68a` |
| HUMAN-REVIEW.md | `76db6bde6f12ecbace9f0ce45adb93be24c92613278aadb8b37331e493455133` |
| packet01.json and packet02.json | `cb0f9da2f36e384eeeb046528696bba4f379fc8419f393a18ae2f809b05829cc` |
| viewer-data01.mjs and viewer-data02.mjs | `9fbb8fb4c5c27832a39fa6b9c729fd18aef52350799efa89f09050d5d1823bff` |

These original files are in the sibling `envelope-packet-2026-10-08` directory,
not aliases for the new packet.

## Producer tests and retained failures

`P -B -m unittest -v test_packet` initially passed 18 synthetic tests
(`4097ac`). The same command in the old packet directory passed its unchanged
11 selection/mapping tests (`a5cd10`).

The first `P -B packet.py 01` failed while resolving dependencies, before
selection or saving (`68ad41`): the initial consumer incorrectly interpreted
the F7 receipt's directory-relative input map as graph-root-relative. No
historical result was produced by that attempt. The repair explicitly resolves
the old packet map against the graph root and the F7 receipt map against its
own directory before normalizing output keys. Two synthetic owner/drift tests
were added. All 20 new producer tests then passed (`0c72a6`). This was a local
implementation error, not missing evidence or an altered scientific protocol.

The next same-command run reached exclusive save and received `PermissionError`
because the investigation worktree lies outside default writable roots
(`c8bb29`). Scoped escalation of the same command saved run 01 (`fa3b25`);
`P -B packet.py 02` saved the separate execution (`801560`). Original files
were not overwritten. Both results are 230,511 bytes and have SHA256:
`ceadeebf040913d5654c20bce5d55dca5ae2b7e4d6612821818f67af6024fb1c`.
`cmp packet01.json packet02.json` returned 0 (`73f097`).

Execution source pins (`79d099`):

- packet.py: `48015d31f451d838ec4b3438e329edd3938a81507c25d537d9c877a88b3f23fe`.
- test_packet.py: `fbb3fe8ae0ac106fc201aef15a2d1bf468c7d692ccf11e3bf864a5d8c6f89be7`.

All 260 declared input pins were checked again by a root Ruby SHA256/byte-count
loop (`efe93a`), including before/after map equality. This is an integrity
check, not a new source annotation. A separate projection of the saved F7 slots
(`2603d0`) counted 191 total native mappings and retained the third F7 slot's
missing peer spring candidate. Every real human response remains null.

## Full closure failure and dependency-only repair

The separate historical checker rejected the candidate (`351243`, exit 1),
before receipt save: 264 required inputs versus 260 listed. Its read-only
diagnostic (`400d55`) and root's independent key comparison (`eb79ce`) agree:
the old packet's checker, checker tests, envelope arithmetic and arithmetic
tests were absent; no listed pin had changed. Therefore the earlier listed-pin
integrity check is not complete closure verification.

[DEPENDENCY-REPAIR.md](DEPENDENCY-REPAIR.md) was declared and separately
reviewed before execution. The unchanged first producer/tests and both failed
candidate packets are preserved. `packet_v2.py` pins and replays that exact
producer, then extends the full old receipt closure with explicit owner
resolution. No source path global is patched. The output adds those four
missing pins plus the three repair controls and two failed candidates, totaling
269. Only inputs and inputs_after may change.

`P -B -m unittest -v test_packet test_packet_v2` passed 24 tests (`c49eff`).
Reviewed execution hashes (`b9f218`):

- DEPENDENCY-REPAIR.md: `0f60d4b0592840fcdce8f40cebb5e94b9fab8d76c73fb1683c9a9260a0af4770`.
- packet_v2.py: `92d52738b35072912bc6d9a00f3d97f52922e3f00d87bf691d1d1ee49ea61bb1`.
- test_packet_v2.py: `d05dede03d4feafcfac4167becd47383b57992d7695611bdbc64f93d551fa7c4`.

Scoped exclusive executions `P -B packet_v2.py 01` (`333f0c`) and
`P -B packet_v2.py 02` (`86563d`) returned 0. Both corrected results are
233,479 bytes, SHA256
`d2c75d2a399d495d88f270181259c71893c8025c68e542c150a57c60a91b6c83`.
Root's Ruby byte/object comparison (`8ce456`) verified identical corrected
outputs and exact equality of every non-input field with the preserved failed
candidate. This is a versioned repair, not silent rehashing of old output.

## Presentation candidate history

The first renderer refused a stale protocol pin before saving (`83b575`);
file absence was checked (`da4ad5`). The corrected protocol was fully reread
and its hash checked (`592605`, `eed8f4`), then the renderer pin and its HTML's
stable-label wording were intentionally corrected. This did not alter the
packet. Initial Python tests encountered nine loopback-bind permission errors
after thirteen passes (`d42ccb`); scoped retry passed all 22 (`cb125c`). Final
candidate tests passed 22 Python (`99d5df`) and 15 Node (`8b55eb`); these were
synthetic checks, not source acceptance.

Before the closure failure was communicated, two candidate presentation files
had been saved exclusively (`845a19`, `1055ee`): viewer-data01.mjs and
viewer-data02.mjs, each 140,546 bytes, SHA256
`40f8c0fc372fac83f0a1644efb2fd16830f13b54fcc56ffed2c934ef7d3ee723`.
They bind the rejected candidate and remain preserved history. No candidate
server was launched or presented for actual review. The corrected presentation
uses separate explicit filenames and the corrected packet hash, as recorded
below.

## Repaired independent verification

The separate v2 checker passed and saved [independent-check-v2.json](independent-check-v2.json):
99,877 bytes, SHA256
`2711ea2717eb4049c5ceb9143d85adde173289ebeffd3fec3c47638094686553`.
It requires exactly 269 producer pins, individually rejects all 269 omissions,
checks all 42 selections / 84 entries / 191 native mappings / 84 displacement
hulls / 13 image headers, and retains all 39 non-F7 slots exactly. Its 275
before/after pins are unchanged. No duplicate-footprint flags occur. It also
requires exact non-input-field equality with both rejected candidates and
retains their original four missing pins rather than retrospectively passing
them. The code imports only frozen independent reconstruction helpers, not
either producer; prior F7 annotation/checker authorship is disclosed.

Separate-agent exact command, using the same bundled Python 3.12.14 (`cdb464`):

```sh
P -B independent_check_v2.py --run1 packet-v2-01.json --run2 packet-v2-02.json --expected-sha d2c75d2a399d495d88f270181259c71893c8025c68e542c150a57c60a91b6c83 --save-receipt
```

The first execution completed checks but failed at save with PermissionError
(`c42b09` session23413 → `ebc67d`). The identical scoped retry saved successfully
(`1172ec` session72597 → `9dda5c`); readback `29a927` checked the final receipt.
The original independent-check.json remains absent. Root read both checker
generations and replayed the full v2 result through a byte comparison:

```sh
set -o pipefail
P -B independent_check_v2.py --expected-sha d2c75d2a399d495d88f270181259c71893c8025c68e542c150a57c60a91b6c83 | cmp - independent-check-v2.json
```

Root replay `0f75b8` session50641 → `ed25f9` returned 0, with no new receipt
write. Root's `P -B -m unittest -v test_packet test_packet_v2
test_independent_check test_independent_check_v2` passed 70 tests (`639653`);
the separate agent had passed its 46 checker tests (`c3b88d`). These repeated
checks are not independent observations of the source or generating curves.

## Presentation test follow through

Root prematurely included test_presentation_v2 before that file had been
completed: 22 existing tests passed and one import failed (`2db4b3`). This is
an execution-order error, not a failed implemented test or missing dependency.
After the test file was completed, root's same combined command passed all
34 (`73e5a8`), including the synthetic repaired-packet server's 17 routes.
The separate agent's first repair test had one expected-header-label error
(`b69359`); the assertion was corrected to the existing interface's literal
header, with all 12 repair tests passing (`4827db`). No scientific criterion
or UI behavior was changed to pass that test.

```sh
P -B -m unittest -v test_render_packet test_serve_review test_presentation_v2
node --test test_review.mjs
```

Root Node tests passed 15/15 (`21c20e`), using Node v22.16.0 (`e8e099`).
Python HTTP tests used scoped permission for ephemeral loopback binding;
fixtures stayed synthetic and temporary. Leaf symlinks are rejected; an
unchanged asset reachable through a parent-directory symlink remains allowed
by the inherited handler, while changed bytes are rejected. This is a stated
handler limit, not a general sandbox or hostile-filesystem security guarantee.

Root's post-repair integrity check found all 269 input pins unchanged and the
material index still at `e9aac5145a7d0b631474ece1d4b8082ba0f9a53ee0a5daaaf1a531dd9b009ff8`
(`522afd`). Worktree tracked whitespace check returned 0 (`8095d2`).

## Corrected presentation and live-browser checks

The separate agent's corrected renders (`349db7`, `c40c1f`) each produced
140,546 bytes, SHA256
`5fc35ee26eb2ad7ee655e083996cd779fadc5b92fe66182ec129ef56e2e0b93f`:
viewer-data-v2-01.mjs and viewer-data-v2-02.mjs. Sixteen control pins were
unchanged before and after both runs. The projection differs from the
preserved candidate only in its packet_sha256 field. Reviewed code pins:

- render_packet_v2.py: `746241d7019f44d920b0c8be866b505ba467b27a7da0bcbceceacbd8c3298636`.
- serve_review_v2.py: `c2fcb2fc13bd7a85e66d7132a11223e8e05e6ea75c8eeaae142350bfeba1c6d8`.
- test_presentation_v2.py: `ad2a4caf3d549b262923823a313bad5c4dc3e25825cf09067a4d9783c1bceec7`.

Root launched `P -B serve_review_v2.py --port 0` with scoped loopback permission
(`b4db7f`, session 66007). It printed http://127.0.0.1:62409/, corrected packet
ID/version/full hash and 17 explicit read-only asset routes. No candidate
server was substituted. The existing browser connection opened a separate tab,
leaving earlier review tabs alone.

Actual browser actions and DOM checks, preserved in the tool transcript:

- Selected all 42 real CE slots without changing any human field. Counted 84
  intended entries and 191 proposed native-image instances. The first immediate
  pass caught four CE-F3Q1 images before load completion (0×0 at that instant);
  this was retained, not called a pass. A second complete pass, reading the
  rendered DOM after each selection, found all 191 loaded with positive native
  dimensions and all 191 coordinate readouts ready. All real statuses stayed
  uninspected in both passes.
- Expanded the original-page and twelve-native-strip panels. All thirteen
  images loaded: page 1700×2200, Im0–Im5 741×88, Im6–Im11 745×92. CE-F7Q3
  displays its absent peer spring mapping and dash-only peer-spring scenarios;
  CE-F4Q1 explicitly retains its excluded-boundary warning.
- Synthetic control only: at 100%, 200% and 400%, the centered click reported
  (320,180), while display dimensions scaled from 1280×720 to 2560×1440 and
  5120×2880. Right/down keys reported (321,180) then (321,181); Escape cleared
  the point without changing a human response. These bounded checks do not
  establish a universal pointer error bound or historical annotation accuracy.
- Toggled outlines off and on, confirming corresponding hidden/displayed
  overlays. Entered explicitly synthetic status/scope/notes; the output kept
  them under SYNTHETIC UI TEST — NOT HUMAN EVIDENCE while all 84 CE rows stayed
  uninspected. Cleared the synthetic response and verified its absence.
- Checked packet ID, version and the full corrected hash in the visible header
  and copyable table. Clipboard transfer itself was not exercised. The browser
  copies the server-bound identity; it does not independently authenticate
  packet bytes. Root inspected a screenshot for readable layout only, not
  curve ownership or human acceptance.
- Left the page at CE-F7Q1, 200%, outlines on, no synthetic response and all
  84 real entries uninspected. Session-local notes are not durable submissions.

A separate actual-HTTP read (`604d54`) fetched all 17 live routes with
urllib.request.urlopen and compared SHA256 against serve_review_v2.routes().
All returned 200 and matching bytes; all 16 presentation controls remained
unchanged before/after. The full route byte counts and hashes are in that
receipt. This live check is separate from the earlier synthetic HTTP tests.

No source images, packet proposals or code were edited during browser QA.
None of these checks supplies a human observation or scientific acceptance.

## Final preservation and handoff

Root's final Ruby JSON/Digest check (`5f97f5`, exit 0) verified all 269 producer
and 275 checker pins against actual bytes, both before/after maps, both corrected
packet and presentation repeats, the unchanged non-input candidate payload,
the saved independent receipt hash, all nine original packet/viewer preservation
pins listed above, and the unchanged material index. A separate check
(`0f5efb`, exit 0) found the four main authority controls unchanged. No new
main/legal record or accepted-engine state was written.

`git diff --check` in the investigation worktree returned 0 (`7046cd`). A
separate Ruby scan of the six unit Markdown files checked 17 local relative
file links and trailing whitespace (`c54ce5`, exit 0): none missing or
whitespace-flagged. It checks file existence, not every Markdown anchor or the
entire repository. An earlier multi-file documentation patch had an unmatched
validation context and made no changes; the corrected patch applied normally.

The separate review's dated closeout addendum is in [method-review.md](method-review.md).
That prior-informed reviewer evaluates text and saved artifacts; it is not an
independent human source reading or a claim to have repeated root's live UI
actions. No code or scientific payload changed during documentation closeout.
The working-tree status (`055d86`) confirms local modifications and an untracked
new unit; nothing was committed, pushed or merged in this unit.

The handoff is the corrected local viewer plus [HUMAN-REVIEW.md](HUMAN-REVIEW.md),
not acceptance. All 84 real entries remain uninspected. A partial F7 response
does not satisfy the other 39 slots, original actual-D sample, source/support
qualifications or the full investigation charter. The full goal remains active
and incomplete. Sherlock feedback is deduplicated locally under SFB-005, not
sent to an archived task or claimed acknowledged. No Faraday engine admission,
new physical metric or cause ranking follows.
