# Municipal retrieval source record

2026-10-04. Research only. Source/control checks and worktree intake found
the same investigation branch and ca1c2233 HEAD with intentional existing WIP.
Main AGENTS, workflow, start page and full charter remain controlling; charter
SHA256 `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
Both main September16 municipal memos were read completely, including their
prior failed-access and no-local-original qualifications. No catalogue scan
was repeated. Their locators are not acquired documents or verified contents.

## Web reader attempt

Original protocol saved/hashed before retrieval (`43a6fe`, exit0). At
13:28:44–13:29:10UTC, one call opened exactly the two declared PDF URLs.

| Target | Tool return | What was actually obtained |
| --- | --- | --- |
| NYC-WTC_000153903 | `turn742view0`, Internal Error, URL not accessible via this tool | One error line, no PDF/text/metadata/server status. |
| NYC-WTC_000173529 | `turn742view1`, Internal Error, URL not accessible via this tool | One error line, no PDF/text/metadata/server status. |

No originals acquired or read. These are tool access failures, not a confirmed
HTTP refusal, no-records response or finding that a City record is absent.
The first protocol's contingent byte-acquisition condition did not occur.
The separately declared direct route preserves, rather than erases, this
limitation. No tool retry, guessed URL or alternative source was used.

## Separate direct route and acquired bytes

[DIRECT-RETRIEVAL.md](DIRECT-RETRIEVAL.md) was saved before requests, SHA256
`ac22ba4f37a88cfb87b85ae172b0ce44a7367e858b92a7af93d43c189ae10105`
(`60ee67`, exit0). Independent prospective review found no material correction;
this was a new bounded route, not execution of the original untriggered condition.

At13:31:26–13:31:49UTC, exactly one direct GET per target succeeded. curl8.7.1
(x86_64-apple-darwin25.0; libcurl8.7.1, SecureTransport/LibreSSL3.3.6) was
invoked with `-q --silent --show-error --proto '=https' --no-location --retry 0
--connect-timeout 10 --max-time 40 --max-filesize 10485760 --output <response>
--write-out <status/effective-URL/type/size JSON> <exact URL>`. `-q` disabled
user curl configuration; no credentials or cookie/header capture was used.
The two commands ran concurrently, not as retries. Approved network execution
was limited to these public inbound files and literal URLs.

| Target and preserved file | Direct result | SHA256 |
| --- | --- | --- |
| [NYC-WTC_000153903.pdf](NYC-WTC_000153903.pdf) | `a316ad`, exit0; HTTP200; same effective official URL; application/pdf;12,357bytes | `87daf254c97f818598eab7de77481048079c69b300338a5c7734719acb0b985d` |
| [NYC-WTC_000173529.pdf](NYC-WTC_000173529.pdf) | `50b10c`, exit0; HTTP200; same effective official URL; application/pdf;533,823bytes | `143af40af3270048ef8b9afc501342f40341c2dc6b9256394396682900e1c2c6` |

Bodies initially went to a fresh private temporary directory as `.response`
files. `file` identified PDF1.5 with1/10pages (`31b8e0`, exit0); hashes were
recorded (`cb1fed`, exit0). `pdfinfo` independently reported the same counts,
sizes, unencrypted files, no JavaScript or forms (`e28281`/`0f3cc9`, exit0).
These are file properties, not a security audit or historical authentication.
Creator/producer identify ABBYY/Nuix processing; August8/12,2026 modification
metadata is not a1998/2002 creation, receipt or release date.

The exact source copies were preserved locally without overwrite through two
approved copy commands (`1b8f06`/`2da1c1`, exit0). Their hashes matched the
temporary responses (`7ffaa0`, exit0). No redirects, challenges, retries,
mirrors or additional URLs were used. The accessible files correct only the
earlier tool-route limitation, not the historical record's authenticity.

## Complete page derivation and reading scope

The system exposed bundled `pdfinfo`/`pdftoppm`; `command -v` returned1 because
`pdftotext` was absent (`5c20d0`). No text-extraction command was run and no
package was installed. `pdftoppm -h` identified Poppler26.05.0 (`74e035`, exit0).
Rendering used `pdftoppm -f 1 -l 1 -r 150 -png <153903-response> <153903-prefix>`
and the same command with `-l 10` for173529. Both original live handles were
polled to terminal exit0 (`1c6b81`/`d29f0d`); no warning text was returned.
No interrupted output was treated as complete and neither job was restarted.

The eleven PNGs were copied unchanged into `render/` (`afc37c`, exit0).
Their physical-page mapping is literal:153903-1 is page1;173529-01 through-10
are pages1–10. Full-page150dpi rendering, no cropping/rotation/enhancement or
synthetic substitute. The fixed output hashes (`6aa1dc`, exit0) are:

| Image in render | SHA256 |
| --- | --- |
| 153903-1.png | `8a83a742bf5ae93b2828ed718e878596ca6dd65ce51242c44028420163e0496a` |
| 173529-01.png | `079b9a2e2eda9fd7f920c12956b3484d95f49e92d12cc75801a831e2857dc044` |
| 173529-02.png | `7ccc0cc1a2c6a76195a13c6186fa8fccd3672029903ccce910fd0dbca05f2091` |
| 173529-03.png | `4efa4c8a3ab4e083b6a3cee33c60d1f1c11f4f7840998c39a0b6dfcdae8c8ff2` |
| 173529-04.png | `c54c2f10f2063a3e209fb3e5b39f6ecd0e051b4623d29701eb6a25ca8b15d983` |
| 173529-05.png | `772db94a4f3311b339bedc089f2feec2a3c068abc9d0921da4940d609964e1e9` |
| 173529-06.png | `6d9ffbbb5796601761871d9e11849d1b6870eff014d9e41ae07a0b0220e037ea` |
| 173529-07.png | `11e9cfee707fa1727901393680a94679c5eb861e53bfc8e6231c0abc3236152f` |
| 173529-08.png | `6118c9b1259fb5cf57f6142e404204fd41617dd88f46e8e023dca0b690b736cb` |
| 173529-09.png | `6a8b00c44e9d3ae39c19b379bda01990c2e5546e27b9c72d93d6dcd00c1a2996` |
| 173529-10.png | `bee9e26a1527fc229db3b7cb63a7504b9af52be9e82fbf20cc76b18b65b1ba92` |

Root read all11 complete pages once at original detail and froze
[root-observations.md](root-observations.md), SHA256
`1a7a6ce7a10765fcc47503e7c8c497f61eb27245235765814eb5e8e433b909c3`
(`b6f068`, exit0), before receiving the second reader's findings. The actual
page stamps agree with the requested targets. Visual uncertainty in marginal
stamps, fax headers, a column identifier and clipped form edges is retained.
Historical signatures/contact details and author-machine paths are not copied
into outgoing text or software feedback. The second reader is independently
reviewing exactly these admitted local pages; its findings are not presumed.

Acquisition totals: two failed web opens, then two separately declared direct
GETs, two PDFs,11pages, no additional source or group member. No whole-folder,
FOIL-production, historical-original custody, first-release or2001 installed-
state validation follows from this successful preservation.

## Completed review and continuation

The separate reader completed all eleven pages and froze [review.md](review.md)
at SHA256 `6e0ae6c36b1f5bfcf0a2f0329c82d4036e11d9d2881ac82144633cf935777c3f`.
Both readers' initial notes were frozen before substantive exchange. Root
then read the complete independent review. Cross-review narrowed root's
"before later construction" to "at the plan-review stage": later construction
chronology is not established here. The original reading is preserved.

An independent [derivative check](derivative-check.md), SHA256
`d3ed230d1d649ecc8693c0fc69940c3920444acf4eca2960c0f2ca628f15563a`,
rendered both held PDFs once with the same Poppler version and compared every
PNG. Both terminal statuses were zero, no renderer warnings were returned,
and all eleven outputs were byte-identical to the saved images. Root read
that complete receipt (`6c82a5`, exit0). Its source-log pin describes the earlier
snapshot before this additive completion entry, not the updated log.

The user's repeated coordinates were independently checked in the intervening
turn and already matched the completed comparator arm; that was not new goal
progress. This continuation resumed the municipal synthesis and then acquired
the separately declared [followup](followup/PROTOCOL.md); those new records
are not retroactively included in the original two-target scope.

The first combined report/log patch failed because an expected log context
line did not exist. A read-only existence check (`4203ef`, exit1) confirmed no
report had been created. The corrected report-only patch succeeded. No raw
source, protocol or frozen reading was changed by either attempt.

Separate complete text review of the draft report (`28042c`, exit0; draft
SHA256 `e5240de590838fcad5f6f487a94d63c786aa290f29d81e0894fc37d73149674a`)
found no causal/as-built inflation, but asked that the uncertain column
identifier be placed with its p.10 S-3 comment, not the S-1 tank-location row.
Root applied that pinpoint clarification. The reviewer did not revalidate
the linked fuel-system analysis or derivative audit. Four frozen protocol/
reading pins were freshly confirmed unchanged (`e9ecea`, exit0).

Generic access-state and catalog-content lessons recur under existing SFB-005
feedback, not new defect claims. No disclosure is made while the designated
task's archived-destination routing remains unresolved. Main legal sources,
earlier municipal lead memos and unrelated WIP remain unchanged.

Final read-only verification (`python3 -B -`, receipt `95ef96`, exit0) checked
thirteen frozen files across both units (four PDFs, three prospective controls,
four initial reading records and two derivative receipts), all nineteen PNG
hashes against their source-log tables with exact file-set membership, all
thirty-eight local links in the unit Markdown, and final new-Markdown whitespace.
All passed. This was an integrity/navigation check, not source interpretation,
human acceptance or historical authentication. `git diff --check --
research/README.md research/sherlock-wtc7-investigation/STATUS.md
research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md
research/sherlock-wtc7-investigation/municipal-originals-2026-10-04` returned0
(`326461`). The additional Python check covered untracked Markdown that Git's
diff check does not inspect.

Final report SHA256: `e5274f088935d459a4ff733b5560517af1feb4544d00413f2173a45c1e2d828a`.
Follow-up report SHA256: `ae94174aa04498144d439c75e44eb869dbe1284d7ad40104add60a43ef141e54`.
These pins follow the explicitly documented peer corrections and final wording
cleanup. The current STATUS and research map now distinguish completed source
tasks from the next two located structural-response candidates. `git status
--short` (`ddbc6e`, exit0) retained the existing intentional WIP plus this unit;
no staging, commit, push or main-repository edit occurred. Full goal remains
active and incomplete, with scientific, documentary and human gates separate.
