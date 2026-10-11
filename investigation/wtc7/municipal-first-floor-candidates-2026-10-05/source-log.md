# Drawing candidate acquisition and reading receipts

October 5, 2026. Research only. Main AGENTS, WORKFLOW, START-HERE and complete
charter retain their previously verified hashes (b0c00f, exit0). Intake96186
reached terminal d1dbcc, exit0: existing research branch/ca1c2233 and intentional
WIP. No investigation edits on main. The previous goal turn completed new
source-location evidence and final reviews; this is further progress, not a wait.

## Prospective scope and acquisition

PROTOCOL.md froze before requests at
`60a2b129cf6d67b5b8204a6756ff7919c86a63fd4e06d3761c8215404aaf23f2`
(208083, exit0). The two exact URLs and fixed29-page expected coverage are in
that protocol. Scratch ed5b3e, exit0:
`/private/tmp/wtc7-plan-candidates.nzCgwO`.

One web-reader open per URL returned tool-inaccessible errors (turn761view0,
turn761view1), no source text or pages. These are tool limitations, not verified
server refusals. Approved direct HTTPS captures each succeeded first attempt:

```sh
curl -q --proto '=https' --connect-timeout 20 --max-time 60 \
  --max-filesize 10485760 --fail --silent --show-error \
  --output <scratch-PDF> \
  --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects}\n' \
  <exact-protocol-URL>
```

| ID | Receipt and exit | HTTP / type / redirects | Bytes | PDF pages | SHA256 |
|---|---|---|---:|---:|---|
| 173192 | 03f4b9 /0 | 200 /application/pdf /0 | 253273 | 4 | 6e3433d6addbb43c79625ae6b7564fd8d353dbde1d55ff45997323167e598ad1 |
| 169180 | 14c815 /0 | 200 /application/pdf /0 | 4451736 | 25 | e7c938b689f9e4d0c2a1146349a637dde7edccdd384d7bfc8dc5ccd0d473c513 |

Admission e643d6, exit0, checked PDF magic, sizes matching source-index metadata,
actual page counts, no encryption and no root AcroForm/OpenAction/AA flags.
These basic checks are not exhaustive security or historical-authenticity tests.
Captured completion mtimes were05:39:48.126325 and05:39:53.861389UTC, respectively;
file mtimes are not independent server timing or original document issue dates.
Approved cp-n ec23b6, exit0, preserved both captures without overwriting sources.
No credentials, cookies, confidential payload, redirects, neighboring guesses or
other source acquisitions occurred.

## Representation

Configured bundled runtime was refreshed; Poppler26.05.0 verified in208083.
fonts.conf was created with apply_patch and names a separately created private
cache plus the two system font directories. The directory's existence does not
itself prove fontconfig used it. Both source renders use FONTCONFIG_FILE pointing
to that exact config, complete-page PNG, scale-to2400 and separate stderr files.
No additional post-render interpolation is performed; ordinary renderer scaling
and image-delivery resampling remain disclosed. This is the method review's
clarification of the protocol's no-interpolation wording, not a native-pixel claim.

Commands used the bundled override/pdftoppm binary with these arguments:

```sh
pdftoppm -f 1 -l 4 -png -scale-to 2400 <173192-PDF> <scratch>/173192
pdftoppm -f 1 -l 25 -png -scale-to 2400 <169180-PDF> <scratch>/169180
```

The actual calls used absolute source/config/destination paths and separate
stderr redirects. First command4107cd/handle55037 reached75c22c, exit0, no stdout;
stderr is empty. Second058a03/handle26344 was still live atad838c; its terminal
receipt must be recorded before claiming complete derivation. Approved2c5cc5,
exit0, preserved the first four renders, config and empty first diagnostics.

## Reading versions

Root viewed the first four complete pages in one permitted batch, with original
detail passed to both loader and forwarding. No explicit resampling notice was
returned; this is not native-display certification. The index-only observation
prefix froze before any second-packet view:3293bytes, SHA256
`ca894ecb6d8f354b470e3fc39f60c1cf290e929a49a3252224eabd1e989a4da6`
(7f5e14, exit0). No larger repeat, crop, OCR or old-source view occurred in that
first batch. The independent reader had not seen root's findings. Remaining
reading, comparison and review receipts will be appended when actually completed.

## Terminal rendering and complete root reading

The second render above reached terminal1e2899, exit0; its stderr was empty
(4a5555). Approved6816e8, exit0, preserved all25 second-packet PNGs and its
diagnostics. No renderer was restarted after yielding. Root's81c24b, exit0,
then compared all34 scratch/preserved pairs byte-for-byte: two PDFs,29 PNGs,
one font config and two empty diagnostic files. All matched. PNG dimensions
have maximum2400; that checks the saved files, not display delivery or source
historical truth. The independent derivative reproduction is still pending.

Root saved ascending notes before each following batch, including pages21–24
before page25. The complete new-source record froze in c35533, exit0:
15671bytes, SHA256
`3104215f8674d31b071b40862ba59d453611659c5505b5e8160774bd37702c18`.
The3293-byte index prefix still hashes to its earlier ca894e… value. Root used
29 complete initial views, zero larger repeats, no OCR/crop/enhancement and no
new-source geometric measurements. Original-detail requests were passed at both
stages with no explicit resize notices; native delivery is not certified.
No peer observations or held173199 comparison views were consulted before
this full freeze. Await the peer's corresponding freeze before comparison.

Independent initial-image reproduction completed: all29 same-name PNGs match
in complete bytes and dimensions after two terminal exit0 processes, with
both PDF pins unchanged and empty stdout/stderr. The checker keeps coverage
open for any peer-requested repeats. Root's624e05, exit0, independently checked
all29 rows in derivative-review.md against both preserved and separately
rendered files, and checked the root observation table's exact ordered4+25
page/Bates coverage and unchanged full-freeze pin. These are derivative and
coverage checks, not independent source authentication or content agreement.

Before any held comparison image view,81f1da, exit0, verified the old PDF and
both named comparison PNGs against the earlier source log:

| Held item | Bytes | Dimensions | SHA256 |
|---|---:|---|---|
| NYC-WTC_000173199.pdf |333388| PDF |37b65cb843cd81716df26af8780627e27bed6d0557eb4b3419945ef742495903|
| followup/render/173199-1.png |85462|1287x1724|0801d39df1b19903c6bbe469d7f96ea90ac547571394e5468932c9b01a048f62|
| followup/render/173199-5.png |143765|1287x1726|01821bed2c8209a0bd12de3a85c1a874a8c509cf5d65552c4dab266f5d025907|

This preflight read bytes and image headers only, not comparison-page content.
Those two previously rendered pages are outside the29-new-image rerender set.

## Independent freezes, comparison and synthesis

The independent reader completed exactly29 initial views and zero repeats;
its complete observations froze at29253bytes/SHA256
`d4e190aa3411a7e0cc42c6dac2e7ec15852596c19b1f80724dded3dc1e6ed023`
(06ae68, exit0), retaining the7751-byte initial index prefix
`7f7b86716729a28518c5e23f70e447f6324c459e8295d930ffe1d5a2686d0076`.
The reader discloses one compaction after packet2 p4 before saving that batch,
and one failed append context corrected before p9; no intervening source views
or exchange of findings. All pages and uncertainty remain recorded.

Only after both full freezes, root viewed held173199 p1 then p5 once each.
Root's separate comparison froze at2610bytes/SHA256
`1555040df22f4875e21d58b1e7db0244c55bf845da26da2baaf426b5ac06e177`
(aa45a1, exit0). Peer likewise viewed only those two held pages, then froze its
comparison's first6061bytes at
`fa229d67cf3598ab70fe8356e02ab7cb499fd0715f89e8db23a1b1bcd2fe2858`
(82ad6f, exit0). Both requested original detail at loading and forwarding,
with no explicit resize notices. No new view of166828, crop, OCR, measurement
or expanded old-source budget occurred. Reconciliation is appended to the
peer comparison; initial prefixes and both complete reading files stay frozen.

Root read all433 lines of the peer observations in three consecutive ranges
(8ff1f8, c2509c,870fd1; exit0), then its comparison/reconciliation (55e465,
exit0). Root'sc8b1ee, exit0, checked the peer whole-observation pin, unchanged
protocol and the closed derivative review:
`8011fee4a29e2a60c64b01f33448819adb4fd60df209f1ed074571d44d30fec5`.
Both readers' final larger-repeat sets are empty, closing29-new-raster coverage.

Report first synthesis froze at52c259adb7072df3521f0acf5e18e7e402a2c9cd3df8df67acf3afc1cb233a87
(cf6b7e, exit0). The independent reader recommended clarifying that the service
record reports some performed work; what is missing is evidence closing the
remaining relay work, not service evidence altogether. Root adopted that
correction and added the independent comparison link, producing
`4e8588712b43075edc2488aa46a6c0699e2983d5f1b797f6c02044774d1c44e5`
(d78c58, exit0). Fine-token differences are reported, not silently overwritten.
Separate synthesis critique and closing verification remain to be recorded.

Main instruction/charter pins still match (87c160, exit0). Tracked navigation
diff whitespace check passed (f1949f, exit0). Branch remains
research/sherlock-wtc7-investigation and HEADca1c223335c20905d6608eb15c676f88cbfac734
(0ccb41/122a0a, exit0); no stage, commit, push or main/legal edits.

## Completed reviews

Independent comparison/reconciliation final13217bytes/SHA256
`f4eb8f2dfc71ab72fc6b1b5bd60179bb9eedbbf836cef0ea40044ff269c907f8`
retains its original6061-byte prefix and frozen observations (f22238, exit0).
The reader verified the service correction and all nine then-current report
links (89f1b7, exit0). Root read the final appendix (aaf04f, exit0) and checked
seven complete unit pins, whitespace and three frozen prefixes (0bfa60, exit0).

Final logic reviewer read both complete source records/comparisons and the
corrected4e8588… scientific report, finding no further blocking correction.
The separately saved final-review.md pins its reviewed inputs and records the
complete-read commands. Its SHA256 is
`f7935dd43afcd3746d475400596332ed6a9476acc640d79a7e1622b8b7ef44ca`.
Root's first attempt to open that not-yet-saved file failed (2c3275, exit1);
this was a timing error, not a missing historical record or completed read.
After the actual save/pin arrived, root read it completely (10d92d, exit0).
The report's review-status footer and navigation updates followed; scientific
text is unchanged from the10433-byte reviewed prefix.

Root separately rechecked the earlier public-search result pin (3cae7c, exit0)
and the single168526 metadata row (0430a8, exit0): s1_first membership,
one reported page,43286bytes, multi-floor CO56 folder label. This verifies the
next candidate's saved metadata, not its still-unread content or relevance.
No new query, acquisition or expanded next-task execution occurred.

## Closing checks

70df50, exit0: all nine complete source/protocol/reading/comparison/review pins
match; all four frozen prefixes (including the reviewed scientific report)
match; all ten final report links resolve; all nine unit Markdown files have
final newlines and no trailing whitespace. Final report11229bytes/SHA256
`38928bd56392ab7dcdfb045bde56d8b964cc14aed1caf8c38955bc31947a0a20`.
Tracked navigation diff check also passed (ed7b9e, exit0). This closing paragraph
was appended after those checks; it does not change any pinned source or report.
Current finite unit completed, comprehensive goal active/incomplete. No new
authority, human approval, engine activation, legal promotion or external send.
