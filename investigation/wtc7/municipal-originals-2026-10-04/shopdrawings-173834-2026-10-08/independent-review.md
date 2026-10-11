# Independent stopped-disposition review

October 8, 2026 local / October 9 UTC. Research-only, separate AI review of
shared saved records. No material discrepancy found within this review's scope.

## Result and limits

The frozen diagnostic's `documents["NYC-WTC_000173834"]` agrees with the
manifest: title/key 173834, reported end Bates 173835, page_count string "2",
pdf_size 289072, query membership ["penn"], source WTC 7 and box 7DCAS. Its folder
is the OEM/7 World Trade Center Job1854 shop-drawing collection. The saved
diagnostic marks this row strict_valid true, missing [], strict_error null.
These are catalog statements, not acquired-PDF validation. The earlier 171835
message transcription is not supported by this row and is correctly distinguished
from a source inconsistency.

Selected population: one document/two reported pages/289072 reported bytes.
Acquired and reviewed population: zero documents/zero pages/zero bytes.
The manifest has no source file/hash, derivatives or observation records and
does not claim completed content coverage, sensitivity clearance or engine
acceptance. This is a stopped disposition under the protocol, not a completed
source reading or a content nonmatch.

The two saved attempt rows agree with execution.md:

| Attempt | Initial receipt / handle | Terminal receipt | Recorded result |
| --- | --- | --- | --- |
| 1 | c16fc8 / 40414 | b9d474 | curl 28; HTTP null; 0 bytes; 20.002508 s |
| 2 | 37f9c7 / 1905 | c6b46d | curl 28; HTTP null; 0 bytes; 20.005128 s |

Execution records same-handle polling and HTTP000; the manifest uses null,
not an HTTP refusal status. The saved command matches the exact public URL,
configuration-disabled curl, HTTPS-only protocol, 20 s connect/45 s total/10 MiB
limits and no redirect-follow flag. The later terminal section resolves the
earlier prospective retry paragraph; it should remain preserved chronology.

I independently confirmed current local absence, including broken-symlink
absence, at both exact PDF paths:

- This unit's `NYC-WTC_000173834.pdf`.
- `/private/tmp/wtc7-shop173834.ktiFnA/NYC-WTC_000173834.pdf`.

Before this review was added, the unit contained only PROTOCOL.md,
source-manifest.json, report.md and execution.md. The scratch directory
contained only fonts.conf and an empty font-cache directory. No source PDF,
page image or observation note was present in these bounded inventories.

Those checks do **not** independently re-observe the original tool/network
events or prove the remote server's condition. I did not rerun curl, poll or
restart a session, search alternative routes, inspect any source PDF, render,
OCR, view images, or open gated records. Saved statements and present local
absence cannot prove source unavailability everywhere or why either timeout
occurred. Ordinary connection/service/network failures remain possible;
withholding, concealment, document contents, equipment identity, installation,
operation and cause receive no evidentiary support from these failures.

The report maintains these ceilings. No source-page sensitivity review or
technical rerender was possible, and none is credited. A later legitimately
obtained exact copy could enable the predeclared content test; this review
neither acquires nor authorizes retrying it. The CO016/control-identity question
and full investigation remain incomplete.

## Method, commands and actual receipts

Main AGENTS.md, WORKFLOW.md, START-HERE.md and main investigation CHARTER.md
controlled. I also read worktree AGENTS.md and the complete
evidence-falsification-auditor/source-of-truth-guardian skills and their named
reference checklists. The skills enforced the split between catalog claims,
recorded transport events, directly checked local absence and historical
inference. No authority or accepted-state change was made.

Complete unit text reads: bf62f8 (protocol/manifest), 09472b (report/execution).
A read-only inline `python3 -B -` command located only the exact diagnostic
record and listed bounded paths (8292b6, exit 0). No new metadata query was run.

Independently authored inline `python3 -B -` command 9c76dd exited 0 in
0.038403625 s with 40 explicit assertions. The full submitted command is retained
in the tool history. It used pathlib/hashlib/json/os/shlex, no existing checker,
and checked:

- Four supplied unit snapshot hashes plus declared diagnostic/CO016-report pins.
- Duplicate-key/nonfinite-rejecting JSON parsing, the exact diagnostic fields,
  manifest path/hash bindings and populations.
- The exact two attempt dictionaries, their receipt/session/elapsed references
  in execution.md, and static parsing of the saved curl command without running it.
- Both PDF paths using os.path.lexists; bounded directory inventories, absence of
  media/notes, and absence of unexpected scratch content.
- Before/after SHA256 stability for all 15 read or pin-checked inputs and unchanged
  directory inventories.

All 40 assertions passed; no corrective edit to an input was needed. These are
consistency/integrity assertions, not 40 historical observations. The prior
CO016 report was hash-checked only, not substantively rereviewed. I did not
recheck the global material index or reproduce earlier peer preflight receipts.

The execution pin below binds the **pre-closeout snapshot** reviewed here.
Root may append a closeout after this review freezes; its reviewed prefix must
be preserved rather than represented as an unchanged full-file hash.

## Input pins

All 15 below were stable across the check. Relative paths resolve from this
unit. Control/skill pins are review-time identities, not acquisition records.
Only this independent-review.md was written; existing inputs remain untouched.

| Path | Bytes | SHA256 |
| --- | ---: | --- |
| `PROTOCOL.md` | 5565 | `cbfcc9aee04042b5687c525f64f11887baa3e0405983ac811cc5de6813589d05` |
| `source-manifest.json` | 1682 | `0aa0ede1d09ad85d6f506858257f644e12dc068a1e9b0bd19d050c2e303b4d03` |
| `report.md` | 3234 | `8a1bf76cffa92b99c6f97f90863162358797a33d1faa040bf4614ba3032d56ff` |
| `execution.md` | 4011 | `e1e0b0c7cbcf0a49f2dc88d4339f86db6978cba092ca258903c8e39e36155e18` |
| `../job1854-followup-locator/root-diagnostic.json` | 114859 | `c6a80ecc100e77cc3d387e17fa032e8c4032e4e13cb761d20bffd6eaed51e7d8` |
| `../co016-control-review-2026-10-08/report.md` | 6626 | `72668adddad033022356c84b35d2291dc473d6c43953e3a4da2974d3cd5a6900` |
| `/Users/admin/docs/911/AGENTS.md` | 15240 | `934437bfc0ddbe522cc73461819593706d12c0644cb306d263d9f1fe3914a857` |
| `/Users/admin/docs/911/WORKFLOW.md` | 5868 | `17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a` |
| `/Users/admin/docs/911/START-HERE.md` | 6383 | `b291da2b9ab3f1a8e9e69ff5a5d930c689ff2d45a6b2ce06a521e76295fbd560` |
| `/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md` | 24068 | `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd` |
| `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/AGENTS.md` | 3256 | `0632c96247e3f9764e5046a8d5af6247733fb5c2a095c196e4347f89165e490a` |
| `/Users/admin/.codex/skills/evidence-falsification-auditor/SKILL.md` | 4215 | `7894e7c6150319ec9591ec39ee1d11c3687f37deaf494d8a7c97b515f29c48a2` |
| `/Users/admin/.codex/skills/evidence-falsification-auditor/references/claim-ledger-template.md` | 566 | `daf05820e54f7b6aa622e60b8406505a9d838ea4b5e8bdff6d265af60f6d402c` |
| `/Users/admin/.codex/skills/source-of-truth-guardian/SKILL.md` | 4218 | `d283182d3b1f493001ad8952102ff70ebf4d7d0575cbfa1891a38df80e313ab5` |
| `/Users/admin/.codex/skills/source-of-truth-guardian/references/audit-checklist.md` | 841 | `b17b3fef9af6199f6efb0c7fc4ba772c2504cb76a28b4d0eecc4dfc0b8a78450` |
