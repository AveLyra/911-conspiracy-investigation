# Security filing source coverage and acquisition record

October 8, 2026. [Scope](SCOPE.md) controls this finite WP5 question.
Main charter SHA256:
`54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
Worktree branch `research/sherlock-wtc7-investigation`, HEAD
`ca1c223335c20905d6608eb15c676f88cbfac734`; pre-existing WIP remains.

## Selection and search record

The initial operations below are recorded retrospectively from the preceding
session's tool observations, not a preserved search-engine result archive.
Search snippets were locators, not final claim evidence. Four of six allowed
public queries were used:

1. `site.sec.gov/Archives/edgar Stratesec "World Trade Center"`
2. `site.sec.gov/Archives/edgar Securacom "World Trade Center"`
3. `Stratesec Inc 2000 10-K CIK`, restricted to `sec.gov`.
4. `Securacom 1997 S-1 333 registration`, restricted to `sec.gov`.

The company directory and a proxy filing index identified CIK 1037453. The
proxy body was not inspected. The four selected substantive filing slots were
the September 11, 1997 S-1/A, the 1999 and 2000 annual reports, and the June 2001
quarterly report. Three bodies were accessed as partial web-reader windows;
the 1997 slot remained inaccessible and was not replaced by a fifth filing.
Repeated windows and indexes are not new filings or independent corroboration.

The SEC submissions-JSON route failed. Two secinfo locators for the earlier
S-1 and selected amendment returned JavaScript/sign-in/human-challenge pages;
no filing body, login or bypass followed. The selected 1997 SEC directory
timed out; constructed index and old-style accession text were inaccessible.
These are route results, not proof of global unavailability or concealment.

1997 attempted accession: `0000950133-97-003231` under CIK 1037453.
The selected September 1997 date remains locator metadata, not a verified body.
No direct-download attempt was made for it. No secondary allegation or
association was adopted from search results.

## Selected source identity

| Research ID | SEC accession and period | Date evidence | Captured representation |
|---|---|---|---|
| SEC99 | 0000925328-00-000015; annual period 1999-12-31 | SEC index records filing 2000-03-30 and form 10-K405. | Windows from the complete-submission `.txt` URL; not the complete submission bytes. |
| SEC00 | 0000925328-01-000006; annual period 2000-12-31 | SEC index records filing 2001-04-02 and form 10KSB40. | Windows from primary document `0000925328-01-000006-0001.txt`. |
| SECQ | 0000925328-01-500029; quarter ending 2001-06-30 | Body cover gives the period. Directory shows 2001-08-14 modification dates; the filing index failed, so that directory date is not upgraded to independently verified filing metadata. | Windows from `fm10q601.txt`; SGML type is 10-Q, while the printed cover says 10-QSB. |

All three body URLs and the two index URLs are retained verbatim in
`web-projection-01.json` through `web-projection-06.json`. The report links the
bodies directly. Original company assertions are one source family.

There is an explicit date discrepancy: SEC00's index says April 2, 2001;
SECQ lines 275–276 describe the preceding annual report as filed March 30,
2001. Both assertions remain preserved. The index is the source for the date
column above; the disagreement is not resolved by silently normalizing either
text and does not establish a security-project chronology or deliberate error.

## What was preserved and what failed

The root web reader displayed primary SEC content before direct preservation
attempts. Each of three direct `curl` attempts then returned HTTP 403, exit 22,
and 4,819 bytes of HTML. The `.response` files are those error bodies; paired
`.headers` files retain the response status. They are not filings. There was
no user-agent substitution, retry, proxy, credential or alternate-client bypass.
The review continued only from already available reader representations.

The three commands used the exact corresponding report URL with:

```text
curl --fail-with-body --location --proto '=https' --connect-timeout 15
     --max-time 45 --max-filesize 10485760
     --user-agent 'Research source preservation'
     --dump-header <source>.headers --output <source>.response
     --write-out '\nstatus=%{http_code} bytes=%{size_download} url=%{url_effective}\n'
     <exact SEC body URL>
```

Existence guards prevented overwriting saved responses. Tool receipts were
`74582e`, `b4a5c2`, and `702d74` for SEC99, SEC00, and SECQ respectively.
Headers date these attempts October 8, 2026 UTC. The local hashes identify
captured error bytes, not missing original bytes.

The six JSON files preserve exact available tool-return strings in their
`output` fields, including provider formatting and the requested locations.
They were saved after first source inspection, using the in-session returned
strings rather than recreating article text from memory. This is a weaker,
retrospective preservation step, not compliance with original-byte preservation
before interpretation. Their hashes do not authenticate SEC originals.
The provider may render/collapse line labels; a minimum/maximum line range is
not proof that every intervening line was supplied.

| Projection | Retained source windows or locator results |
|---|---|
| 01 | SEC00 lines 0–179; SEC99 552–698; SECQ 244–408. |
| 02 | SEC00 155–317 and 307–466; SECQ 437–602. |
| 03 | SEC99 660–767 and 212–317; SEC00 566–676; SECQ 0–126. |
| 04 | SEC99 312–456 and 437–584; SECQ 358–503; index/directory identity results without expanded lines. |
| 05 | Expanded annual indexes and quarterly directory metadata. |
| 06 | Literal `World Trade` locator results for SEC99/SEC00; no match returned for SECQ. Locator coverage is not a full-body reading or absence test. |

The substantive reading covers the relevant services/client, backlog, dispute
and MD&A passages in these windows. It is not an audit of every financial
statement, exhibit or prior filing. Root also viewed some earlier windows
before these captures; no final finding depends solely on an uncaptured window.
No unnamed settlement or company-wide financial figure is attributed to WTC7.

## Separate reading and authority boundary

The separate reader's initial direct web requests for all three body URLs
failed (provider references `turn852view0`–`turn852view2`). No body was read in
that attempt, and no independent acquisition is claimed. The subsequent
bounded review uses the same locally preserved projections; it can independently
check interpretation, but cannot repair the acquisition or historical
corroboration limits. See [review.md](review.md).

No additional external search was used on resumption. Cached-source windows
completed the already selected passage context. No new filing, outreach,
payment, private data, formal case fact, pleading, engine/bridge acceptance,
commit, push or publication was authorized or performed.

The source question can receive a bounded disposition; complete original
preservation and WTC7-specific attribution remain unmet. The full goal remains
active. [Validation](validation.md) records actual local checks separately
from scientific or historical verification.
