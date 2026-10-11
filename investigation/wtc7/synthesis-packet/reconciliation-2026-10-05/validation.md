# Reconciliation verification and limits

October 5, 2026. This record verifies the finite [scope](SCOPE.md), not the
whole investigation, historical authenticity or any collapse mechanism.

## Authority and state

Worktree: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
Branch: `research/sherlock-wtc7-investigation`; starting HEAD
`ca1c223335c20905d6608eb15c676f88cbfac734`. Intentional existing WIP remains.
Main legal records, older reports, raw sources, original annotations, accepted
engine state and the held NIST/UAF matrix remain outside the write scope.
No staging, commit, push, new acquisition, source-image view, listening,
measurement, decode, solver, engine call or external message in this unit.

The original scope/manifest preparation made a finite selection, not a new
physical result. The intervening user-coordinate reply merely reconfirmed an
existing result and is classified as no new goal progress; it is not another
human experiment. This continuation advances the goal by completing the
material-claim/dependency reconciliation and review, not by reclassifying that
confirmation as new science. Whole-goal completion remains unproven.

Scope SHA256: `9676311bd4113ca6b146eedf90941053fbae02e72dba63d9edb1fcd568dc6f62`.
Manifest SHA256: `30f291d43f241ddc8a1c50f73112f9ec31f371e9b73564141b2a5424158e26d9`.
The manifest's 35 rows are 14 baseline reports, 11 additions and 10 controls;
these are not 35 independent historical sources. The main historical packet's
32-report inventory is not relabeled as a current census.

## Read coverage and independent roles

Root read every A01–A11 report, both complete component reconciliations, the
October 4 assessment, the eight-link ledger and the D1–D9 table. Baseline
structural/common-observable details not newly reread in full remain attributed
to the pinned earlier assessment/component work, not a fresh audit of every
primary source. Root also read source/capability receipts for the selected
media checks. There was no new municipal page reading by root in this unit.
Truncated combined outputs were not treated as complete; selected missing
report sections were read in bounded later calls.

The documentary reader fully read A02–A10 and B04, relevant B03 dependencies
and narrow linked receipts. Its note records 13 relevant input checks,
23 selected source/receipt pins, seven reproduced derivative model joins and
four saved public-query population counts. It did not repeat archive queries,
native model extraction, source rendering or the historical experiment.

The media reader fully read A01/A11, B02 and C03, with relevant assessment
passages. Its saved check records seven input/control pins, source/map/frame
joins, two observation freezes, audio source/window joins, null events and
bridge receipt/log outcomes. It did not see new historical images or hear audio.

The later assembled critic authored the media component. Its review is separate
from root/documentary synthesis, but is not independent review of its own
component. Root independently reread the spot/audio reports and performed the
fresh media identity/status checks below. Those checks do not substitute for
another visual/audio interpretation or qualified engineering review.
Earlier attempts to dispatch a fresh critic and reactivate another reviewer
hit the agent-thread limit; the already active media reader performed the
disclosed assembled review. No unavailable fresh review is claimed.

## Actual root checks

| Tool receipt and actual command family | Result and scope |
|---|---|
| `662a78`, read-only Ruby using JSON, file size and SHA256 | All 35 frozen path/size/hash pairs match; 14 baseline, 11 additions, 10 controls. Manifest hash matches its freeze. No source parsing beyond JSON or new scientific execution. |
| `57c80c`, read-only Ruby using JSON and SHA256 | All seven PNG container hashes/sizes match; exact selected indices 255–261 and PTS 17000/17066/17133/17200/17266/17333/17400 match; WMV source pin matches. Container/receipt checks, not fresh pixel decoding or clock authentication. |
| Same `57c80c` | Four held WAV hashes match the source check; four windows, total98s, zero listening passes and `events:null` verified. Native bridge receipt exit3, all collection/pass/fail/skip counts zero and cases empty. No historical listening or bridge test executed. |
| Same `57c80c`, `shasum -a 256 -c comparison-inputs.sha256` from the October4 audit directory | All 14 original baseline pins pass. This verifies the original selection as well as the new manifest, not agreement with conclusions. |
| `3dbf46`, read-only Ruby parsing the component's P/R tables and hashing their files | All 23 documentary support pins independently rehashed by root; HEAD confirmed unchanged. This is not a new PDF content reading. |
| `957be1`, read-only Ruby local-link, whitespace, input-pin and row-label checks | 44 local link occurrences resolve across five Markdown files; no trailing whitespace; 35 inputs unchanged; all11 additions, Q01–Q10, eight links and D1–D9 labels present. Row labels do not verify scientific substance. |

The frozen-input identity check is reproducible without importing research code:

```ruby
require 'json'
require 'digest'
m = JSON.parse(File.read(ARGV.fetch(0)))
m.fetch('inputs').each do |r|
  p = r.fetch('path')
  abort("mismatch #{r.fetch('id')}") unless
    File.size(p) == r.fetch('bytes') &&
    Digest::SHA256.file(p).hexdigest == r.fetch('sha256')
end
puts "PASS #{m.fetch('inputs').length} frozen byte-size/SHA pairs"
```

Supply this directory's `inputs.json`; inspect the IDs/roles rather than
interpreting the row count as evidence strength. The script reads files only.

## Failures and qualifications retained

An initial attempt to add SCOPE failed because its parent directory was absent;
the exact directory was created through approved execution and the patch then
succeeded. An early map query assumed an array where the schema uses an object;
the schema was read before correction. These were preparation failures, not
historical evidence. No input or scientific threshold changed to make a pass.

The media reviewer records a similar initial products-array navigation error;
the documentary reviewer records a jq cardinality-expression error masked by
a later successful shell command and a malformed transcribed checksum. Their
successful subsequent checks and exact limits are in their preserved notes.
Do not count the initial shell exits as all-check passes.

Root's `3d1d2e` receipt projection queried nonexistent `selected_frames`,
`outputs` and `source` keys and returned null. That was a navigation assumption,
not missing historical fields. Root inspected the actual `indices`, `frames`
and `inputs` schema before the successful `57c80c` check. This null must not be
conflated with the deliberate null/unheard audio event state.

In the intervening coordinate confirmation, a Ruby `filter_map` call failed
under the installed version (`2d1307`). The compatible read-only `map.compact`
check (`452980`) matched all18 reported points, the frozen human-record hash
and all10 human-arm displacement intervals. No comparator file changed. That
check reconfirms the existing y-only tolerance, not a new x/radial error model.

An initial `rg` lookup in `957be1` used the wrong relative base and found no
requested files; that failure is not a completed text search despite the later
Ruby check's successful shell exit. The corrected base in `0d001d` returned the
relevant stable/failing-state passages. A first multi-file closeout patch had
an unmatched context and failed; `ccc0d6` confirmed both target hashes unchanged
before the corrected patch. No partial change or lost source was assumed away.

## Review and closeout

The [assembled review](critical-review.md), SHA256
`9bc48dfa5efce7c6d47a8b6effae488b2a2280eba0de24dcb866eab608944747`,
found no remaining material correction after the CO23 phrase was repaired.
The critic checked all35 inputs, exact11/10/8/9 row coverage and44 local links
(`318264`, exit0), then verified that reversing only the documentary phrase
restores its pre-correction hash (`ecf01a`, exit0). Root read the complete review
(`e6b2ee`, exit0). These are separate AI checks with the involvement limits above,
not another historical source, blinded adjudication or professional acceptance.

The correction changes “also requested December1” to “requested sketches
referenced in the December 1 fax.” It avoids inventing the date or act of the
request. Documentary hash before:
`e9b417e995d41e8727d4b67ef9e3453ad8c11e8ecd039b94d5970a261f8ab097`;
after: `e68384efc3b0b5c8ed0d299b688ff453d519d640df84f05e664995166e2dbeb0`.
No raw record or earlier interpretation was overwritten. The reviewed root
report hash is `7a8eab5d8d5858408124c091d7537f5c4da7cac540e9a86e62c1e2aa5700afbe`;
its subsequent change only replaces the final pending-review paragraph with
actual review status. The reviewed validation hash was
`20cca2a71de0ea0f6b12be2944a20ff3ddcc35bd9a47ad478fbac8d0e508e057`;
this closeout is later administrative documentation, not a second review claim.

Root updated the existing STATUS and research navigation rather than creating
a competing authority. `e4808b`, exit0, confirmed `git diff --check` and read
back the new status. The displayed tracked diff includes extensive earlier
WIP and must not be attributed to this unit alone. A prior presence probe
(`d0caf6`) found the critical file not yet saved; it did not establish a failed
review. The later complete read establishes the saved review's actual outcome.

A source hash, populated Q/D row or successful text check is not proof its
scientific question is solved. No frozen inputs, main/raw/legal records or
accepted engine state were edited by this unit. The full goal remains active;
its completion criteria were not narrowed to this reconciliation.

Final read-only check `7ed2fb`, exit0, verified 52 local link occurrences,
whitespace in all six Markdown files and all35 unchanged frozen inputs. Reversing
only the root report's administrative closeout paragraph reproduced its exact
reviewed hash, confirming unchanged scientific text. Current report SHA256:
`a9000b3ab0d8374dddd554a7a8e2d97da314d27ce444d9f23da5dcc5109ade41`.
This verification paragraph and the disclosed reviewer-dispatch limitation are
later log additions, not new scientific claims or a fresh review snapshot.
