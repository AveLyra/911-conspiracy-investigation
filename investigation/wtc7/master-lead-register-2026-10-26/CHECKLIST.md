# Requirements, preservation and unresolved work

Scope: integrate the already-published operational-record and bank/phone studies into an additive edition of the public master; do not adjudicate their conflicts or promote research into case facts. Dependencies are fixed public commits ddd475b4 (134-entry baseline) and 838af603 (published operational/integration package, including the bb9e9c5d bank study). The acceptance criteria below are checked by verify_master.py.

| User requirement | Outcome/location | Verification and unresolved issue |
| --- | --- | --- |
| Include operational findings | M135–M142 / RF001–RF008, MASTER-LIST.md and register.json | Original RF objects and research sections retained exactly; historical recollections remain qualified |
| Include bank/phone findings | M143–M152 / BP01–BP10 | Original BP objects, full excerpts, page/Bates references and open tests retained exactly |
| Preserve earlier master | Unchanged M001–M134 records; preceding body preserved except relative-link relocation | All 14 earlier package blobs unchanged; inherited claims not freshly re-audited |
| Preserve source links and provenance | Source catalogs, primary hashes, fixed commit and one-based report-line locators | Copy/source identity does not authenticate every factual assertion; external sources not freshly fetched. Exact excerpt spans are recorded separately from heading/separator-inclusive entry spans |
| Preserve conflicting records | Full excerpts include $1,558 signs, $4,000–$8,000/$9,900, April 19/20, 22/27, CBR/cell, chronology/language/copy-locator differences | Causes remain unresolved; dates/units/scopes are not normalized |
| Preserve contrary/confirming evidence | Existing contrary-findings section; coincidence account; narrow carrier confirmation at M150 / BP08; judicial qualifications | Not a selection containing only incriminating observations |
| Carry unresolved questions | Exact targets-v2 in OPEN-TARGETS.json and register.json; all five BR and ten BPR IDs | Receipt/teller/February 4 carrier originals, earlier interviews, CIA routing, informant payment and full notebook/expert exhibits remain open |
| Keep different payment tracks distinct | Master introduction, M141 and M151 | Apartment-payment 1A attachments do not supply the $100,000 informant voucher |
| Avoid duplicate-evidence inflation | 152 overlapping entries; RF/BP crosswalk and dependence statements | Repeated reports, aliases, mirrors and analysis rows are not independent witnesses/calls |
| Preserve originals and public scope | New directory and additive navigation file only; protected-file pins in SCOPE.json | No raw PDF/media, personal account/contact data, correspondence, credentials or private case material added |
| Revision accountability | TEXT-CHANGES.diff compares the new full master with its immediate predecessor; other new Markdown compared to /dev/null | Earlier source-package status remains unchanged; PDF/layout checks are separate and not applicable |
| Commit/push as AveLyra | Check exact public repository, authenticated account and new author/committer before push | VERIFICATION.json is precommit integrity evidence, not a claim of completed remote verification |

No outreach, fee, private-repository push, source repair, force-push or history rewrite is part of this update. A failure to locate an original is not proof of destruction, concealment or wrongdoing. No independent probability or final causal conclusion is assigned.

The candidate checks found packaging issues: bank entry spans included a separator outside an exact excerpt, the final excerpt has no terminal newline, and preserved relative links needed three byte-exact public dependencies. The corrected candidate records exact excerpt spans and includes those dependencies. Source text and its original line-range fields were not edited; failed candidate/check records remain preserved locally. These were integration issues, not anomalies in the historical evidence.
