# Control record acquisition and verification

October 8, 2026 local / October 9 UTC. Research worktree, branch
research/sherlock-wtc7-investigation, HEAD ca1c223335c20905d6608eb15c676f88cbfac734.
Current intake 1585b6 showed existing unrelated work; none is replaced.

Protocol was saved and hashed before requests: e37fe180397f5e57d8c8fbfc2af5c5fcdd39042c82242abd170b6b264d71942f
(376af8). Root metadata assertions a2279f and separate jq assertions 17564b
matched the two exact rows, three pages and 146675 bytes. The other six rows
in the saved break_glass response are not silently included. The diagnostic's
other missing-folder failures remain unchanged.

Scratch directory: /private/tmp/wtc7-co016-20261008.LWyZwn.
System curl8.7.1 (cce85e); bundled Poppler26.05.0 (a2f875), runtime bundle
26.1007.11041. Requests use curl -q, --proto '=https', --connect-timeout20,
--max-time45, --max-filesize10485760, --fail --silent --show-error, no redirect
following, credentials, cookie replay or private payload. Exact URLs are the
protocol's content prefix plus its two filenames. Output paths must not exist.
Only allowlisted transport fields are emitted; raw headers are not retained.

The first GET (8352d5, exit0) returned HTTP200/application/pdf,89091bytes,
zero redirects, elapsed0.537160s. The second GET (2f9287, session53596) was
polled on that same handle; b90e26 establishes terminal curl exit28 after
20.008823s connection timeout, HTTP000/zero bytes. No second PDF exists.
This was an actual transport failure, not an observation timeout or a remote
access denial. UTC clock checks bound these attempts between02:34:27 and
02:35:19 onOctober9; do not treat these as document creation dates.

Before any source image viewing, one identical retry of171909 is now declared.
It permits at most one successful download of that file, consistent with the
protocol. No alternative host/tool, changed credentials, guessed URL, automatic
retry loop or widened file set is allowed. A second failure ends that route in
this unit and remains an explicit incomplete source. No document content was
used to decide this transport-only retry.

The initial combined admission diagnostic (f7503a) stopped at the absent second
file before emitting its aggregate result; that is not a passing two-file check.
The one-file diagnostic (2bd0ee) passed the first PDF's magic, exact89091bytes,
two pages, no encryption and no catalog AcroForm/OpenAction/AA. SHA256:
4e10972135a0d9e24a61da9560cd554a4b5f6e66087aeee109ba041ad4fd2ca6.
Local pypdf text triage returned1224/998characters on pages1/2 and zero matches
for its explicit confidentiality/private-identifier categories. No extracted
text was emitted or saved. This is limited triage, not sensitivity clearance;
newly apparent sensitive content will stop substantive reading.

## Retry and source representation

The declared identical retry (f238c8, session38615) was polled on its same live
handle. Terminal receipt3f5678 records curl exit28,20.006215s connection timeout,
HTTP000/zero bytes. There is still no171909 body. This route stops here; the
missing reported page is not a negative content result or evidence of withholding.

For171905 the actual full-page rendering command was:

```sh
FONTCONFIG_FILE=/private/tmp/wtc7-co016-20261008.LWyZwn/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 2 -png -scale-to 2400 NYC-WTC_000171905.pdf NYC-WTC_000171905
```

It exited0 with no diagnostics (36ffda). The locally authored font configuration
uses system/library fonts and a private scratch cache, not a global change.
No historical image edits, cropping, enhancement or substantive OCR occurred.
Root viewed both full page images at original detail and saved each page note
before advancing. Zero repeat views or delayed note saves. No explicit
confidentiality marking was observed; ordinary business contacts, signature
and source-machine path are not reproduced in the analytic notes.

Root notes froze before peer exchange (41530b), SHA256
8ff803c4a66ddda44f6840e8e98e0d856dbdd24682425f02ecd5637977bd7174.
The source PDF, two page images and fonts.conf were copied non-overwriting
into this unit (6c2725). Root byte comparison (e43e52) confirms all four copies
equal the scratch originals. Pins:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| NYC-WTC_000171905.pdf | 89091 | 4e10972135a0d9e24a61da9560cd554a4b5f6e66087aeee109ba041ad4fd2ca6 |
| NYC-WTC_000171905-1.png | 120265 | 3c966e459dac95876a423fc5c23b799fe7574a137ca0927e77588b98d03f2d75 |
| NYC-WTC_000171905-2.png | 98315 | ae767d63f79b21869c981566eae8443c98b36c4063d3672003ae2d9bfb4258e2 |
| fonts.conf | 227 | 4d7cf05f6ca79c9cb870cd5927df09305d0add4fc6e83cdb203f7df7e6b4b023 |

Second reading, separate derivative verification and final review remain to
be recorded. The finite population is still two documents/three reported
pages, with only one document/two pages acquired; no acceptance criterion is
silently reduced to the successful download.

## Paired reading and review closeout

October 8 local / October 9 UTC, following the provisional entry above. The
second reader completed both pages in order with one full-page view each and
immediate notes, then froze observer-observations.md (9274ca; size check 4b34ed):
SHA256 c6854e2300b099f7582ea41486940badb8536ff6a3ee58e64a5ddcd2ddb91f1a.
Root read the entire frozen peer record at dd41d9 after both records had frozen.
The peer then compared the root notes at ab77f6; both note hashes remained
unchanged at 44a94d. No repeat image views or revised observations followed.
The readers agree on the material content. Their fax-hour disagreement, 08
versus 09 with minute 21, is retained without either hour entering chronology.
These are prior-informed AI readings of one source, not independent witnesses
or actual human/expert acceptance.

The separate technical verification is saved in technical-verification.md,
SHA256 62af6d3659623a3ad3d16d4239b8755b2c9de73a74a0ef4718b8e38eec565b8a.
Root read it completely at 8bbf9b and again on resumption at bceddd. Its checks
cover the exact roster, four copied files, PDF structure, manifest and a fresh
rerender in /private/tmp/wtc7-co016-independent.H2iga1. Rerender receipt 07c381
exited 0 with no diagnostics; comparison 721b0e found both PNGs identical in
encoded bytes and decoded RGB pixels. The same Poppler implementation was used:
this verifies local repeatability, not historical authenticity or an independent
rendering engine. The checker did not read page content or repeat downloads.

The independent interpretive review is critical-review.md, SHA256
bffca1a6b40f0042b1e109ae182c015d1edc311772ab17baa4637424970ec265.
It finds no material interpretive blocker in report.md at SHA256
72668adddad033022356c84b35d2291dc473d6c43953e3a4da2974d3cd5a6900.
Root read the complete review on resumption (2a7cee). No substantive repair
was requested or made. The review explicitly distinguishes unresolved equipment
identity from a demonstrated nonmatch, design assertions from installation,
cost concerns from wrongdoing, and admitted-page completion from the incomplete
selected population. It is a document-to-document AI review, not another source
view, historical authentication or engineering opinion.

The review pins the prior source-log snapshot, which ends immediately before
this new heading; it does not purport to have reviewed these later closeout
entries. Frozen protocol, notes, report, manifest and review records are not
rewritten. The earlier metadata-only CO016 label in test-chain-review.md remains
preserved history; the dated STATUS/navigation update points to this new result.

Resumption intake 8f2072 confirmed branch research/sherlock-wtc7-investigation
and the same HEAD, with extensive pre-existing research WIP preserved. Main
controls and the version 3 material index rehashed unchanged at fad60b; the
index remains a frozen earlier snapshot, not a silently updated current claim
for this letter. No main/legal/source-spine or accepted-engine change occurred.
The preceding source-retrieval goal work was progress; the intervening acoustic
answer did not add a measurement. This closeout completes review and navigation
of that new evidence, not the full investigation. The second PDF remains unread
after two terminal transport failures; no third attempt is authorized by this
unit. The exact equipment/circuit link and dated field test remain the next
substantive discriminators. No new software pain point arose beyond already
recorded provenance/partial-coverage controls, and no feedback was transmitted.

## Final integration checks and retained diagnostic failure

Before the closeout append, the technical reviewer revalidated eight reviewed
snapshots, source/manifest coverage, absent 171909 in both checked directories,
and unchanged bytes across 14 checked files: shasum receipt 0b8691, read-only
Node assertions a12438 and reader-heading check 55c112. This describes that
pre-append snapshot, not the later full source-log bytes.

Root's initial integration command at 11a377 failed its source-log prefix
comparison because the checker appended an extra newline to an already
newline-terminated prefix. The command also ran git diff --check afterward,
so its aggregate shell exit 0 did not mean the Ruby assertion passed. The
visible RuntimeError is retained as a failed diagnostic. The isolated byte
check at 738520 confirmed that the exact 5026-byte prefix has the reviewed
79ab0074... hash, while the extra-newline string does not. No source, original
log entry or expected hash was altered to obtain a pass.

Corrected Ruby assertions, run alone at e6ee95 (exit 0), verified all eight
reviewed snapshots with the old log checked as its exact preserved prefix,
all three source/derivative hashes and sizes, manifest coverage and false
acceptance flags, both zero-byte timeout records, absence of the second PDF,
manifest/review/index pins, seven Markdown files' whitespace, and eleven local
unit/navigation links. The separate scoped git diff --check at 128f8d exited 0
without diagnostics. These are integrity and documentation checks, not another
source observation or scientific acceptance.

The diagnostic mistake yielded a generic extension to the existing SFB-004/
SFB-005 feedback, not a newly alleged Sherlock defect. Synthetic test 5542ff
(exit 0) verifies literal append-prefix equality, inequality after an extra
newline, and the difference between an unguarded failing-first/successful-last
shell sequence (status 0) and guarded execution (status 1). Preserve individual
operation results and raw byte boundaries. The deduplicated note remains
local at the unchanged archived-destination boundary, not sent or fixed.

Separately, a read-only inference audit found that the current acoustic update,
claim index and causal-chain synthesis already distinguish conventional-blast
predictions from quieter thermochemical hypotheses. Root checked the material
passages at 18a608. The user's reported bang is retained; silence and thermal
intervention are not established. No duplicate memo, new acoustic measurement,
source retrieval, acceptance or cause ranking follows from that wording check.
