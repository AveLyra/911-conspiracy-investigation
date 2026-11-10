# October 2001 WTC permit coordination and steel-haul draft

Public research copy. [Source URLs, locators and SHA-256](SOURCE-PINS.json).

**Scope.** Public records acquisition for the steel-preservation and custody track. Compare the two NYC DEP release packets carrying the October 16 daily report and identify additional records needed to trace steel loads. Both PDFs were retrieved directly from the City on November 5, 2026. The source pins give release IDs, exact page and text-line locators, byte counts and SHA-256.

## Observations

1. **Meeting requested.** Both October 16 daily-report copies carry the same heading, “FEMA requests meeting regarding permits and the demolition of WTC.” The email excerpt says the sender was trying to schedule a meeting. The stated agenda was to identify agency review processes, determine primary responsibility for each permit and address SEQR/NEPA requirements early. Both scans show “Wednesday t 2 pm.” The text supplies neither an exact meeting date nor confirmation that it took place. Its October 2001 context is post-attack work. [Short packet, PDF p. 1](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000154446.pdf#page=1) · [Long packet, PDF p. 1](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000154452.pdf#page=1)
2. **Two release versions.** The shorter release has four pages. The longer one has 15 pages and adds enclosures, including a two-page health order marked “DRAFT #4 - October 15, 2001.” Both daily-report copies refer to an attached draft executive order pertaining to incident command at PDF p. 2. The separately titled health draft in the longer packet has a different stated subject. Preserve both references separately. The packet does not establish that the executive order referenced on p. 2 is the health draft on pp. 6–7. [Short packet, PDF p. 2](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000154446.pdf#page=2) · [Long packet, PDF p. 2](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000154452.pdf#page=2) · [Health draft, PDF p. 6](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000154452.pdf#page=6)
3. **Proposed flatbed exception.** The health draft calls for spray-washing vehicles leaving the site at access-point wash stations. It calls for otherwise-open debris cargo to be covered, with an exception for flatbeds hauling structural steel and building components. Those flatbeds could go uncovered under the proposed text, subject to thorough wet washing before departure. The draft assigns posting and distribution to the health and police departments. The displayed date and execution area is blank. No issued counterpart was located in the bounded search. [Health draft, PDF pp. 6–7](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000154452.pdf#page=7)

## Conflicting readings preserved

| Locator | Short packet embedded text | Long packet embedded text | Scan observations |
| --- | --- | --- | --- |
| p. 1, line 28 | `project review board members` | `project review hoard members` | Both show `project review board members`. |
| p. 2, lines 14 and 12, respectively | `NYPD requests DEP to extend` | `NYPD requests DPIP to attend` | Both show `NYPD requests DEP to attend`. This is the separate counter-terrorism meeting. |

These are differences across the released embedded text and scan layers. No substantive difference was identified in the two scanned FEMA agenda passages inspected. The two passages are copies of the same daily-report entry and count as one source report of a request.

## What this adds to the custody search

The draft gives specific exit-control terms and potential custodians for follow-up. If an issued version retained the provision, dated distribution or wash-station records could establish when it applied. Joining an actual vehicle exit record to a load ticket and a receiving-yard receipt could establish a movement. The draft itself identifies no individual load, building of origin, route, receiver, retention instruction or completed wash. It supplies no test of whether a particular WTC 7 piece was washed or what any wash changed. The proposed wash rule and earlier DEP routing reports address separate links in the chain. [Earlier routing comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/eefbdc3c134599b89ad3942590aedc37777667f4/investigation/broader-evidence/steel-nyc-debris-routing-daily-reports-2026-11-05/README.md)

## Open TODOs

- [ ] Find the actual FEMA meeting invitation, agenda or minutes and any agency permit matrix, issued permits and site scope. Use the October 16 daily-report heading and the originating email as retrieval keys.
- [ ] Find the executed health order, effective date and posting or distribution record. Compare the wash and steel-flatbed terms against draft #4. Separately locate the incident-command executive-order draft referenced on p. 2.
- [ ] Find exit-point logs, carrier load tickets and receiving-yard records. A date, load or truck ID and matched receipt would support a load-level join. No such join was performed.
- [ ] Retain the unacquired December 19 DDC Incident Plan and December 21 daily safety report on the existing queue. Neither document was located in the bounded exact-title searches. [December command report and dependencies](https://github.com/AveLyra/911-conspiracy-investigation/blob/b81709e9af732cbde6b1142729e7f3c19e1d336c/investigation/broader-evidence/steel-nyc-december-command-reports-2026-11-05/README.md)

**Method and limits.** Acquired two City PDFs. Screened embedded text across both packets. Visually checked the targeted p. 1 and p. 2 text, the health draft heading, its exit-control clauses and its date/execution area. Text-line references in the source pins use PyMuPDF 1.27.2.2, `page.get_text(sort=True).splitlines()`, with one-based lines including blanks. Searched exact phrases for the health order and the FEMA agenda through public web indexes, including the independent City release index. The bounded search did not establish whether a final order or permit records exist in other files. The attachment comparison does not address historical collapse cause.
