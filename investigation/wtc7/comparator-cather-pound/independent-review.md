# DEM-04 independent source-scope and receipt review

2026-09-20 UTC. Research-only AI review; not an engineering expert opinion,
independent event witness, full-thesis review, or reproduction of historical
measurements. This note preserves the reviewer's earlier frozen scope finding
and separately audits the subsequently supplied report and captured responses.
Only this new note was written. No network requests or PDF inspection occurred
during this audit.

## Authority, coverage, and reviewed versions

Main AGENTS.md, WORKFLOW.md, START-HERE.md and the complete investigation
CHARTER.md control; their hashes remain those of the previously read controls.
The worktree AGENTS.md and START-HERE.md were also read, and the main charter
was reread completely. The source-of-truth-guardian and
evidence-falsification-auditor skills were read and applied: captured bytes
remain evidence, this note remains exploratory, and attributed source claims
are not promoted into reproduced measurements or canonical case facts.

Completely read: PROTOCOL.md, report.md, execution.md, and
source/inventory.sha256. Independently inspected captured HTML lines 305–367,
including the complete abstract, and only whitelisted public header fields.
The HTML was read as source text, not rendered as a browser page. No cookies
were printed or transmitted by this audit.

Reviewed SHA-256 pins:

- PROTOCOL.md: `29082c94836b4378a2a537b956cfd1e52896c41310a869bfcca44b1b069577c8`
- report.md: `0b8064e68fcd0b643ff58b583e9886c4525f84b1992fb7ae15be7c8a5ecede07`
- execution.md: `61437f1c76f643ca9c10f4ea672c0483857cc8caf2705ed3c1d361720de1c9a0`
- source/inventory.sha256: `4f0a5a2011f538c5eefe60cf6bd43248010445b63ed4772a08763e28342283ad`

Later root revisions, if any, require their own explicit disposition; these
pins identify the versions actually reviewed here.

## Preserved independent conclusions and report comparison

The earlier independent reading covered the official university landing page's
complete metadata/abstract and the held DEM-04 source-manifest/WP0 entries,
before reading root's substantive report. The exact title is *Full Scale
13-Story Building Implosion and Collapse: Effects on Adjacent Structures*,
Kanchan Devkota, MS thesis, May 2019. The event date is December 22, 2017.
The held 2018 label is unsupported by this edition's metadata; the shortened
catalog title omits the important adjacent-structure emphasis.

The abstract attributes empirical nearby-structure/free-field acceleration
measurements and sacrificial sensors in the demolished buildings. It separately
describes numerical models of neighboring structures. Internal, synchronized
failure-propagation histories with usable uncertainty are not demonstrated by
the abstract. Their absence from the thesis cannot be inferred without reading
it. Structural-system, geometry, deliberate preparation, sensor-target, and
air/ground transmission differences limit comparator transfer.

The report faithfully preserves those conclusions. It appropriately separates
reported experimental work and reported model results from independent
authentication or reproduction. It does not turn sacrificial sensor presence
into usable internal timing, adjacent-model agreement into demolished-building
validation, or HTTP denial into concealment. No material scientific overclaim
was found in the reviewed report. Its December 2017 date is less precise than
the available day-level metadata, but not incorrect.

WP0's no-located-artifact status remains bounded to its declared selection;
the prior catalog did not prove global unavailability. DEM-04/DEM-05 evidence
overlap was unresolved, so this record does not establish another independent
event-level sample. No WTC7 causal ranking is derived here.

## Actual integrity and response checks

From source/, the following command returned exit 0 and six `OK` results:

```sh
shasum -a 256 -c inventory.sha256
```

Exact sizes were independently obtained with:

```sh
stat -f '%N %z bytes' landing-public.body landing-public.headers landing.headers thesis-public.body thesis-public.headers thesis.headers
```

| Captured file | Bytes |
|---|---:|
| landing-public.body | 40,666 |
| landing-public.headers | 844 |
| landing.headers | 0 |
| thesis-public.body | 5,666 |
| thesis-public.headers | 2,125 |
| thesis.headers | 0 |

The header check command returned exit 0:

```sh
rg -n -i '^(HTTP/|content-type:|content-length:)' landing-public.headers thesis-public.headers
```

Observed: landing HTTP/2 200 and thesis-route HTTP/2 403; both declare
`text/html; charset=UTF-8`. The thesis response declares content-length 5666,
matching its captured body. These are HTML responses, not an acquired PDF.

This additional whitelisted check returned exit 0:

```sh
rg -n -i '^(date:|cf-mitigated:)' landing-public.headers thesis-public.headers
```

It found response dates September 20, 2026, 07:52:02 GMT and 07:52:07 GMT,
respectively, and `cf-mitigated: challenge` for the thesis response. No
challenge was interacted with in this audit.

An additional read-only Ruby check enumerated source/ excluding the inventory
itself and compared that set with the six inventory entries: exact match;
all six regular files; none symlinks. It also read only the first eight thesis
body bytes, hex `3c21444f43545950` (an HTML DOCTYPE prefix). The actual command
was:

```sh
ruby -rjson -e 'names=File.readlines("inventory.sha256").map{|x|x.split(/\s+/,2)[1].strip}; actual=Dir.children(".").reject{|x|x=="inventory.sha256"}.sort; puts JSON.pretty_generate({manifest_entries:names.length,exact_file_set:actual==names.sort,files:actual.map{|x| {name:x,regular_file:File.file?(x),symlink:File.symlink?(x),bytes:File.size(x)}},thesis_first_8_bytes_hex:File.binread("thesis-public.body",8).unpack1("H*")}); abort "unexpected source file set" unless actual==names.sort'
```

Result: exit 0, six entries, exact_file_set true. No source-body script was
executed. The same inventory check is rerun after saving this note.

## Receipt limits and protocol wording issue

The saved bytes independently establish the current integrity, ordinary-request
HTTP statuses, content types, and sizes. They do not independently establish
the original process exit codes, DNS diagnostics, client version, or effective
URL: those are root's execution account, not a process this reviewer witnessed.
The two empty headers alone cannot prove why the earlier invocations failed.
This is a receipt limitation, not evidence that the account is false.

One procedural wording ambiguity should remain explicit. The protocol records
an earlier web-link 403 and then authorizes one ordinary public retrieval,
while also saying “Do not retry a denied route.” Execution records the web
request and a later ordinary request to the same thesis URL, both denied.
Thus the later request is the first declared ordinary-client attempt, but not
the first request to that denied URL. A closure clarification should acknowledge
this transport-specific exception/ambiguity rather than claim no repetition
of the denied URL occurred. No access-control bypass is evidenced by the
reviewed record, and no further request is warranted under this protocol.

The narrow next opportunity remains a lawfully supplied thesis or separately
authorized ordinary route, followed by prospective complete-page review.
This audit itself establishes no new timing constraint and does not reopen
acquisition or claim completion of the comparator study or full charter.
