# Stable case source check execution record

Research only. Root first verified current branch/HEAD/status, read the existing
material/run and released-file audits, and requested a separate read-only
feasibility check. Both checks identify the already documented absent paired
states/results in the inspected packages, not a new absence finding. Main
SC10 and held extracted pages supplied prior familiarity. No new inventory
scan, decompression, native model execution or source acquisition was performed.

## Source and preparation

Source PDF: main `authority/nist/wtc7/ncstar-1-9.pdf`, SHA256
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
Scope SHA256:
`4e0df05f2393974f13e49f29d0bf67418231bece6d85d110ab00826514a19548`.
Renderer: `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`,
version26.05.0, SHA256
`de772e88ab9977ccde25def9b403bf42675d75f5dd82b19fbd7d8123ad183159`.

The first render invoked `pdftoppm -f 655 -l 658 -r 180 -png SOURCE ncstar-1-9`
in this output directory without an explicit font configuration. Session38887
was confirmed running and polled on the same handle, not restarted on timeout.
It returned terminal exit1 (`2b5889`): default font configuration/cache errors
and inability to write the first PNG. Tool logs were truncated by volume;
no claim of a complete stderr capture or exact warning count is made.
The directory check `7f8ab2`, exit0, confirmed that only SCOPE.md existed, with
no PNG to preserve or inspect. No historical source page was viewed in this
failed preparation. This is a tool/setup failure, not a source-content result.

Before any views, a local fonts.conf was added with system font directories
and the fresh private cache `/private/tmp/wtc7-stable-fonts.CxdDxt`.
One exact render retry is planned with the same four pages, resolution and
renderer, an explicit FONTCONFIG_FILE, output prefix `run02`, and ordinary
approval for writing this worktree directory. This transparently extends the
scope's one-render preparation after zero images were produced; source/page
selection and reader/view budgets are unchanged. No system configuration or
dependency installation is changed. A further failure must be reported before
another approach; no silent retry loop.

## Actual retry and source integrity

The declared retry completed before any page view. Actual command:

```sh
FONTCONFIG_FILE=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/causal-chain-synthesis/stable-control-2026-10-05/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 655 -l 658 -r 180 -png /Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/causal-chain-synthesis/stable-control-2026-10-05/run02
```

The write used normal approval for the dedicated worktree. Tool result
`902506` returned session16060; the same handle's `da0371` poll was still
running with no output; `fc6d1b` returned terminal exit0 with no diagnostics.
No process remained live at the later closeout. This records tool-returned
results, not a separately saved complete renderer transcript. There was no
further render attempt or independent raster reproduction.

The font configuration hash is
`ead26c91871c7eeb298d0de661e96cf38ecac71b47ec12df22d20443d7259a9a`.
Post-render checks `0f1c86` and `81d023`, both exit0, confirmed the source and
PNG identities. A later independent-from-render, read-only byte/header check
`ffbfc4`, exit0, reverified all four files and the unchanged source, scope,
font configuration and two frozen notes. It did not decode or display pixels.

| Physical page | PNG | Bytes | Header dimensions | SHA256 |
|---:|---|---:|---|---|
| 655 | run02-655.png | 1341967 | 1530 × 1980 | `0c9671ba4990bde6d42aa85fe44f41c1437a6177bf579143c5902b016f66ef4a` |
| 656 | run02-656.png | 1226843 | 1530 × 1980 | `d0431588c062ea967be6b6f1406b1019086facfc7db9286b5a70cec0039b6c65` |
| 657 | run02-657.png | 553720 | 1530 × 1980 | `f6e48d8bdb5c1ee5499563bc6c8a06957125e3e853dabc05341521a9c430257d` |
| 658 | run02-658.png | 2153547 | 1530 × 1980 | `22b09f032a2824181af998b2bad9a9dccfb0144db61b693dbf2f329f489e0e8f` |

The renderer's executable hash also still matched at closeout (`2451f0`,
exit0). Hashes establish identity of these captured artifacts, not the
historical accuracy of the simulations depicted in them.

## Actual reading and freeze sequence

Root and `/root/media_reconciliation` each viewed exactly these four full
pages, in order, once. Both used original-detail image loading/forwarding.
Both recorded **zero repeats**, with no crops, enhancement, pixel measurement,
additional primary pages, new extraction, or historical-video playback.
The image return size was 1530 × 1980; this is not certification of the
user interface's display scale. Both readers used the same derivatives.

The complete root record was saved and hashed before peer findings exchange:
`4ccf029a7fe6481705bfc3489650d3c659d077a40c1e0a2fbccb52e6ca41ee08`.
The complete second-reader record likewise froze first:
`89e53eb57dfc1245701efe62c5c5b1ff33113293133da5ffa6c27fd0c9a8a2d2`.
The observer's recorded clarification of the page657 figure-reference sentence
occurred before that full freeze; it is disclosed in the notes. Neither
record is edited to resolve a later difference. Root re-read both complete
notes at closeout; `1d5d1f` and `ffbfc4` verified their unchanged hashes.

The readings agree on the reported damage control, residual local failure,
stable captions, separate no-debris section, missing end criterion, unresolved
temperature pairing and one-second time-label discrepancy. Two qualifications
remain explicit in the report: the elapsed-time subtraction assumes a shared
global clock, and the observer could clearly read the upper positive lateral
legend but not every leading lower-legend character. Root's lower-legend
reading is not silently upgraded to joint clear agreement.

These are separately frozen AI readings of one author/source family. Neither
reader is blind to the reported outcome; the later critic is also the second
source reader. They supply neither independent historical corroboration nor
human/expert approval nor independent solver verification.

## Label arithmetic and supplementary source checks

Root's initial decimal-label subtraction (`cbe9d7`, exit0) was followed by
exact integer-hundredth arithmetic in `ffbfc4`, exit0. The latter avoids
floating-point display issues and prints results only; it writes no files:

```ruby
stable = [[-324, 1276], [-380, 1220]]
raise unless stable.map { |relative, absolute| absolute - relative } == [1600, 1600]
raise unless stable.map { |relative, absolute| absolute - 850 } == [426, 370]
no_debris = [[-580, 750], [-380, 950], [-130, 1200], [70, 1400], [230, 1560], [320, 1750]]
raise unless no_debris.map { |relative, absolute| absolute - relative } == [1330, 1330, 1330, 1330, 1330, 1430]
raise unless 1750 - 1330 == 420
```

This verifies arithmetic on transcribed labels, not the correct native frame
time, physical timing or a new simulation. The observer independently noted
the subtraction inconsistency in its pre-exchange notes; the two root command
implementations are not independent investigators.

After root's notes froze, root read the complete existing errata-review report
as a secondary edition check, then reread it at closeout (`07d19d`, exit0).
No new errata PDF view, website check or source acquisition occurred. Its
complete listed corrections do not include printed589–592 timing/sign fields.
That does not exclude a correction elsewhere or a later edition. This ancillary
report check does not expand the four-page primary selection.

The separate existing-input feasibility review by `/root/integration_scope`
read current inventory fields and completed release reports. It found no
newly located executable pair or native results; no new body search, model
run or files were produced. In particular, the earlier header-only scan gap
had already been superseded by full non-PNG body reads and curve searches.
It is not an open task to repeat. The June short ANSYS driver is not a
replacement for the missing LS-DYNA case. The report preserves these as
package-specific findings, not universal absence claims.

Support pins checked with `shasum -a 256` (`2451f0`, exit0):

| Existing support artifact | SHA256 |
|---|---|
| Main errata-review report | `7a3165b482c558b12a89bd2791ddcfa8b2ba456c51d05358a9b64ac25389105f` |
| Main released-input report | `1d0b1d3031d7ee5b8baa87459c166fb5460954cc96e864a45199a52365483f9e` |
| Main released-input inventory.json | `391b13a37df24c9b2c987d0e1d03bf27513bd718fa3fecd168a95f614104dbf3` |
| material-run-crosswalk/report.md | `a9afca6aa6221db2f96bb0d2720cadb7094532105f5e86661fb591b9315babcf` |
| curve-release-search/report.md | `e186fc2fe9d532809f58f13459a54fed72ee4117244c29d0c54752de8b6b3ca8` |
| October5 reconciliation report | `a9000b3ab0d8374dddd554a7a8e2d97da314d27ce444d9f23da5dcc5109ade41` |

The completed reconciliation and its pinned causal-chain source report were
not edited. Current branch is `research/sherlock-wtc7-investigation`, HEAD
`ca1c223335c20905d6608eb15c676f88cbfac734` (`fdbf06`/`f61293`, exit0).

## Review and closeout in progress

The repeated coordinate-input turn only confirmed an already incorporated
result; it added no new scientific evidence. This continuation resumes the
previously unfinished source check without more primary views. The draft
submitted for source-reader critique has SHA256
`54c24f064c0117819e308673cd10cb311dce2d3bf03be3f3dc41748b9d54a49e`.
Final review disposition, output pins and navigation checks will be appended
after they actually complete. Scope, primary sources and frozen readings are
preserved; no model/engine run, legal promotion, outreach, transfer, staging,
commit or push is authorized by this closeout.

## Completed closeout

The [disclosed source-reader review](review.md) is complete, SHA256
`71eb85ee9dc4912052528cf57ac31e758f2f99e2fc3767c44a8abcc1ceed51ac`.
Root read its complete initial/revised disposition and final execution-record
append (`fefb34` and `4dd2f2`, exit0). Both requested corrections were applied:
conditional shared-clock wording and attribution of the lower-legend reading.
The reviewer also checked the added layer-specific A/C/D grades and dependency
link, then the actual execution chronology. No unresolved substantive
correction remains within that disclosed review's scope. This is not acceptance
by a human or a structural engineer.

The final report SHA256 is
`a68ac77d127922548e4e5e9a058d53b9e42ab8f994e0ff9b8d7857540559a9a6`.
A read-only Ruby check (`f8ffc8`, exit0) replaced only the final administrative
completion footer in memory with its reviewed predecessor and recovered the
reviewed `4d662d...` hash exactly. Thus the final report has no substantive
change after that review. The check also confirmed the exact final review
hash, no trailing whitespace in all six unit Markdown files (including
untracked files), and all14 local Markdown target paths. Target existence
does not verify headings/anchors, rendered layout or scientific correctness.

Actual repository whitespace check:

```sh
git diff --check -- research/README.md research/sherlock-wtc7-investigation/STATUS.md research/sherlock-wtc7-investigation/causal-chain-synthesis/stable-control-2026-10-05
```

It returned exit0 (`881ffa`). That Git command does not cover untracked
contents by itself; the explicit six-file check above supplies that coverage.
Root read back both changed navigation sections (`ff6c07`/`bbbc3c`, exit0).
`8911a8`, exit0, confirmed all three current-section navigation targets and
that the earlier causal-chain synthesis still matches the reconciliation's
B05 byte count and hash
`d0736961744b47e3dcf5cad2675a0dbff7cda9f912da02baf0a881772270d6a5`.
The October5 reconciliation itself also retained its previously checked hash.

The app returned `queued` for opening the final report. That is not verified
rendering or proof the user viewed it. No browser/display validation of this
Markdown was performed. The final scoped status check (`327968`, exit0)
shows two modified navigation files and this untracked unit. Existing other
WIP is preserved; no staging, commit or push occurred.

This finite four-page source check is complete: fixed coverage, preserved
inputs and failures, two frozen attributed readings, corrected comparison,
exact label arithmetic, critical review, and a concrete paired-case dependency
proposal. It is progress toward WP3/Q06/Q10, not reproduction of either model
or completion of the broad investigation. The native pair remains unavailable
within the inspected packages; no generic rescan or guessed-input run follows.
Other scientific and human-review workstreams remain active and incomplete.
