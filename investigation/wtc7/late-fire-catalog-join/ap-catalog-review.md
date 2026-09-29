# AP Archive 314927: bounded public-catalog review

2026-09-19. Research-only source-identity note by Codex agent `/root/ap_catalog_source`. This lane is independent of root's CBS/Internet Archive and NIST-release investigation; it supplies no independent visual review of those lanes. Worktree: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`; branch `research/sherlock-wtc7-investigation`; intake HEAD `e8d83d7`. Main AGENTS.md, WORKFLOW.md, START-HERE.md, the unchanged investigation CHARTER.md and this directory's PROTOCOL.md control.

## Result and evidentiary ceiling

**The historical search lead `314927` remains unresolved. The present public AP search accepts the exact number but returns zero results. No primary AP item title, item identifier, date, shotlist, source credit, rights statement, preview or media file was identified for it.**

The actual route was [AP Archive's legacy homepage](https://www.aparchive.com/), which the web tool reported redirecting to [AP's current archive page](https://newsroom.ap.org/archive). The current page has a public `Search videos...` field. Entering `314927` and pressing Return produced [the exact public keyword-search result](https://newsroom.ap.org/editorial-photos-videos/search?query=314927&mediaType=video&st=keyword): the heading contained the query, the page showed `0 results`, and it stated `Your search returned zero results`. The date control was `Anytime`; the media type was video; AI Search was not enabled. The page still offered `Sign in`; no sign-in was attempted.

This is a directly observed result of one current public search route, **not** a finding that AP lacks the item, that the identifier never existed, or that an authenticated/legacy catalog would also return no match. In particular, the observed route labels its mode `st=keyword`; this review did not establish whether legacy numeric identifiers are indexed in that public mode. Migration, differing catalog access and an incorrect or stale secondary identifier remain unresolved alternatives.

No WTC 7 preview was viewed, no media bytes were downloaded, and no fire, scene, continuity, duration, event-time or cause finding follows from this result. A generic Vimeo AP Archive promotional embed was present in the landing-page accessibility tree; it was not inspected as evidence and was not the target item.

## Lead provenance checked locally

Read `late-fire-video-lineage/source-leads.md` and the actual preserved secondary HTML at `/Users/admin/docs/911/research/wtc7-video-comparison/sources/911conspiracy-tv-7-WTC-2020-07-01.html`, lines 499–512. Section `Window Shot (Unknown, FOX)` gives the number as a search instruction on aparchive.com, rather than an item permalink. Its assertion concerns a longer version; it supplies no AP item title, date, shotlist, duration, original camera identifier or AP-specific rights field. The surrounding text explicitly describes the claimed fire event's time as unknown. Its causal terminology is not adopted.

The current search result for [International Center for 9/11 Justice's Building 7 Collapse Archive](https://ic911.org/building-7-collapse/) repeated the number and the same AP/broadcaster/collection narrative. Only the web search result excerpt was inspected; that page was not opened in this lane. This repetition is not independent confirmation of the AP catalog identity, source chain or depicted sequence. The preserved HTML and the newer index may share a source; this lane did not determine their editorial history.

## Complete public-query and navigation ledger

All attempts below occurred on 2026-09-19. The search tool used its normal web index. No unrelated result page was opened, and no search-result snippet was treated as an AP item record. The first four queries were submitted in one call and the last two in a second call; those calls returned aggregated results rather than an individually labeled response for each query.

| Order | Actual query or requested URL | Inspected response / result |
|---|---|---|
| Q1 | `site.aparchive.com "314927"` | First aggregated web-search response supplied no identified primary AP target page. Returned unrelated exact-number/topic hits were not inspected beyond the result output. |
| Q2 | `site.apnews.com "314927"` | Same first aggregated response; no identified primary target. AP News is not assumed equivalent to AP's archive catalog. |
| Q3 | `"AP Archive" "314927"` | Same first aggregated response; no identified primary target. |
| Q4 | `site.aparchive.com "World Trade Center" "Window" "2001"` | Same first aggregated response; no identified primary target. This was one catalog-focused metadata query, not an expanded general event investigation. |
| Q5 | `"314927" "WTC"` | Second aggregated web-search response included the IC911 index excerpt described above, plus unrelated hits. No primary AP target was returned. |
| Q6 | `"314927" "AP" "2001"` | Same second aggregated response; no primary AP target identified. No further web-search query was run. |
| N1 | `https://www.aparchive.com/` | Web open reported a redirect to `https://newsroom.ap.org/archive`, title `Newsroom`, content type text/html, and zero extracted text lines. That text-extraction limit did not establish a login barrier or page absence. |
| N2 | `https://newsroom.ap.org/archive` | Opened directly in the Codex in-app browser. Initially loading; later accessibility state showed `AP Archive`, title `Archival Photos & Video Footage Licensing \| Associated Press`, the public video-search field, and sign-in/contact controls. No login, contact submission or rights agreement was performed. |
| N3 | Public UI search text `314927` | Set the visible video-search field and pressed Return. Initial accessibility results still showed loading. Subsequent DOM inspection showed the completed zero-result page. The final URL was `https://newsroom.ap.org/editorial-photos-videos/search?query=314927&mediaType=video&st=keyword`. |

The initial loading observations are retained here as transitional states, not counted as failed catalog searches. Only the completed N3 response supplies the negative result. The web tool's empty N1 text and the browser's successful N2 UI are compatible: the browser exposed content that the text extractor did not.

No HTTP status code was exposed by these browser observations; none is inferred. No raw AP HTML, catalog response bytes or browser export was saved in this lane. This note records inspected tool/UI observations and exact navigation; it is not a byte-preserved AP source artifact. Root may independently reopen the final URL to check the current result. A later change would require a dated follow-up, not alteration of this observation.

## Admission state and claim audit

| Layer / claim | Status and support | Strongest alternative or disconfirming evidence | Grade |
|---|---|---|---|
| The preserved index supplies an exact AP search lead | Direct local text observation at the file and lines above | The index is secondary, and a numeral in an instruction is not itself authenticated AP metadata | A for existence of the lead text only |
| The current public AP keyword search for 314927 returns zero results | Direct browser DOM observation at N3 | Legacy numeric identifiers may not be searchable in this interface; the zero result cannot resolve historical availability | A for this route's observed response only |
| AP 314927 is a longer copy of the target Window Shot sequence | Asserted in the secondary index, unverified here | The exact public query does not presently identify an item; the number could be stale, mistyped, inaccessible or unindexed | D: materially underdetermined |
| This is an authenticated original or a continuous longer source | No primary item or video acquired/viewed | Even a later AP match could be a syndicated or edited compilation rather than the original recording | E as a presently supported conclusion; not a finding of falsity |
| AP metadata establishes capture time or causal significance | No relevant metadata obtained | Catalog publication/event dates, broadcast times and player positions would not alone authenticate camera time or mechanism | E as a presently supported conclusion |

| Admission milestone | Result |
|---|---|
| Public catalog route located | Yes: archive landing page and exact query URL |
| Primary item link located | No |
| Item-level title / ID / date / shotlist / source / rights inspected | No; all remain unknown for this lead |
| File identity established or bytes acquired | No |
| Target preview actually viewed | No |
| Scene counterpart supported by this lane | No |
| Continuity established | No |
| Historical recording time authenticated | No |

The strongest adverse evidence found is the completed exact-number public query's failure to locate an item. It weakens a claim of a currently resolvable public catalog match. It does not discriminate between a bad lead and incomplete public indexing. Conversely, a verified legacy-to-current ID crosswalk and matching item shotlist would materially improve the lead, while a catalog item showing different footage would defeat this proposed join. No visual contradiction or confirming frame correspondence was found because no target media was inspected.

## Smallest next source and boundary

The next missing source is an **AP-issued item-level catalog record or legacy/current identifier crosswalk for historical identifier 314927**, with its exact title, item/permalink identity, catalog date fields, source/credit, shotlist and available public preview. The specific public entry point is the N3 result above; it does not currently expose such a record. A new directly located legacy permalink or a publicly documented AP ID search route would be a bounded next retrieval. A permissioned AP account, staff request or licensing transaction was not attempted and requires the separate authority applicable to that action.

Do not invent a legacy story URL, map the number to a guessed filename, transfer another clip's title to it, or use AP's site-wide copyright footer as the target item's rights metadata. The declared six initial web queries and the linked AP-page exploration are complete. Further route expansion belongs to root's scope decision; no global catalog exhaustion is claimed.

## Inspection scope and verification

Applied the repo-orchestrator, evidence-falsification-auditor and source-of-truth-guardian skills. Read their relevant references, main repository controls, the charter and this task's protocol. `python3 /Users/admin/.codex/skills/repo-orchestrator/scripts/repo_intake.py` ran successfully in the assigned worktree and reported the expected branch and many pre-existing edits/untracked research directories. They were left untouched by this lane.

Actual source inspection was limited to the local source-lead note, preserved HTML lines 499–512, the six web-search outputs, AP redirect metadata, the AP landing/search accessibility state, the completed result DOM and its final URL/title. This lane did not inspect root's current media selection or other agents' visual conclusions. No raw evidence, legal spine, prior frozen note or summary was edited; only this research note was added. No login, fee, outreach, upload, sensitive query, contact form, media acquisition, software import, evidence promotion, commit or push occurred. Note-content and whitespace checks and its hash are reported in the agent's return message; they establish file integrity, not source authenticity or a successful footage join.
