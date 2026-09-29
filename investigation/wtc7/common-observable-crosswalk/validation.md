# Verification and review record

2026-09-20. Research-only source comparison. This records actual checks, not
physical verification, historical authenticity, engineering sign-off, legal
clearance or accepted Sherlock/Faraday state.

## Frozen coverage and source pins

Root completed all twenty full-page readings specified by [protocol](PROTOCOL.md).
The separate NIST and UAF readers each completed their ten. All three notes
were saved before substantive exchange; prior source knowledge was declared.
No new rendering, crop, video decode, fitting, retiming, network request or
solver occurred in this unit. The reused pages' rendering qualifications are
retained in the notes; byte equality does not erase earlier warning history.

Read-only `python3 -B` using hashlib/json matched the following four source PDF
hashes and twenty selected PNGs against existing receipts before the root read.
Result: `primary_pdf_pins: 4`, `selected_png_pins: 20`, `status: match`,
`new_render_or_physical_verification: false`. Source paths for the NIST PDFs
are under `/Users/admin/docs/911/authority/nist/wtc7/`; UAF is under the
research worktree's `uaf-final-method-audit/source/`.

| PDF | SHA-256 |
|---|---|
| ncstar-1a.pdf | `03c801bc1338533b54c6a64a66f074165c9429a59df11e2f58a19f5da91aef09` |
| ncstar-1-9a.pdf | `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4` |
| ncstar-1-9.pdf | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` |
| uaf-final-2020.pdf | `f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa` |

Five PNG pins came from [Camera2 validation](../camera2-penthouse-event/validation.md);
five from the [lateral receipt](../lateral-geometry-audit/render01/receipt.json);
ten from the [UAF receipt](../uaf-final-method-audit/render01/receipt.json).
The readers separately checked their admitted sources and derivatives as
described in their frozen notes. No duplicate render replay is claimed.

| Frozen artifact | SHA-256 before exchange |
|---|---|
| root-notes.md | `fcea96ed40ea52a8591151f6235e4e4e37035c21dc01d057d33d077e07de83ef` |
| nist-notes.md | `113d5596456a918873c1030c6fadaf8b3b339b87fde1634e165f17a0ab4a93ec` |
| uaf-notes.md | `f366303c0f188b991697a584e83aebad497f20592a24e101f4ab8208a0668ff0` |
| draft-alignment.md | `c852c2d4c9fc1d476c9eeae18bd59b00969ec70e3332cccb8161427e3a058438` |

The alignment reader checked the three Faraday drafts and prior Luna
Faraday section, not historical imagery or a present ledger. Its five source
hashes were unchanged. The draft-alignment artifact is a proposal review,
not a fifth physical source or an engine mutation.

## Corrections after exchange

1. The NIST reader caught root's conversion of “last seen at 8.0 ± 0.1 s” into
   exact disappearance. The joint report now preserves last-seen status, the
   subsequent 8.1 s image and view-dependent parapet occlusion. Root's original
   wording remains frozen as the audit trail, not the adopted finding.
2. The UAF reader narrowed root's blanket “not independent measurements or
   unused validation data.” The joint report says those targets are **not
   independently reproduced here or established as unused validation data**.
   UAF describes its own video review as well as NIST/FEMA; exact derivation
   of each target was not recovered. The reader also required explicit eastern
   roofline versus northwest-corner separation, now prominent in the table.

Neither correction changes the source bytes. No material disagreement remains
between the three readings within this fixed scope; that is interpretive
agreement, not additional independent historical evidence. The separate final
text review is preserved in [review.md](review.md), SHA-256
`8fabcf1d7d5701f8df1c2d525c3ca9bdc7dacb649887218156b255135bb79b44`.
It found no material overclaim or numerical error in report snapshot
`07a86920fbb65ee4d97e7b72bd5f353ffc55e09985ef98c3c7d4b11dd6aff59f`.
Its two prospective refinements were incorporated afterward: separate the
function's implementation role from calibration history, and define first
versus final roofline passage. The next-task wording also now explicitly says
local native-file availability is unverified. Frozen notes/review unchanged.

## Final document checks

Root's read-only `python3 -B` command used hashlib/json/regular expressions and
Decimal. Exit 0: all four frozen artifact pins, four primary PDF hashes,
twenty reused PNG hashes and four main instruction/charter pins matched; all
eight Markdown files then present passed final-newline, trailing-whitespace
and conflict-marker checks; all eighteen then-present local links resolved.
There were no remote links to open. All six published-time subtractions passed
exact Decimal assertions. The separate critic used Fraction and checked those
six plus the two displayed 16-second clock differences (eight assertions),
without claiming the clock origins authenticated.

`git diff --check -- research/README.md research/sherlock-wtc7-investigation/STATUS.md`
exited 0. Branch and HEAD readbacks matched
`research/sherlock-wtc7-investigation` /
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`. Scoped status shows the two navigation
files modified and this new directory untracked; broader intentional WIP is
preserved, not staged or cleaned. Checks after the prospective text refinements
are recorded separately below; the earlier reviewed hash is not silently
replaced with the final one.

Post-refinement check: report SHA-256 is
`952628e3fbb405f2a9f05af09546f876a567a5c9975da21442de7a74c26e6024`.
The critic read the changed crossing/next-task passages and confirmed both
suggestions resolved, with frozen review unchanged. Root's final read-only
Python check exited 0: eight Markdown files, nineteen local links, six
artifact pins (final report, frozen review and four frozen reading/alignment
notes), and three new navigation links passed. Scoped `git diff --check`
again exited 0. This paragraph records those checks without claiming a new
scientific test; it is not part of the critic's earlier frozen snapshot.

## Execution qualifications

- An initial recursive navigation listing matched too many paths and was
  truncated; no complete inventory claim rests on it. Targeted existing
  receipt/path checks supplied the selected source set.
- A guessed old root-source-note path did not exist. The correct earlier
  `root-definitions.md` was used only for pin/context lookup; no full reread
  of that old file is claimed.
- A four-image presentation of NIST physical323–324/UAF105–106 exceeded
  available context. It was not counted. All four were later successfully
  presented and reviewed in two-image batches; the other pages were reviewed
  completely. This was a display/context limitation, not source corruption.
- A broad status/navigation output was truncated. Top-level navigation was
  recovered through focused ranges. The guessed investigation-level README
  did not exist; actual navigation is `research/README.md`. No absent-file
  finding was extrapolated beyond those paths.

No new distinct Sherlock pain point was identified beyond existing SFB-004/005
event, dependency and case-role fixtures. No duplicate feedback added; archived
destination remains unresolved and no message was sent there. Original Luna
artifacts, primary sources, existing measurement freezes, legal records and
accepted-engine state were not edited. No commit, push, merge, publication,
fee, outreach or new sensitive disclosure.
