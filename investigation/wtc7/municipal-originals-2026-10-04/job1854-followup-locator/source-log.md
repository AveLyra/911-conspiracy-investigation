# Job 1854 follow-up lookup execution record

Research branch research/sherlock-wtc7-investigation, HEAD
ca1c223335c20905d6608eb15c676f88cbfac734. October 4, 2026 America/New_York
(acquisition/check receipts extend into October 5 UTC). Intentional WIP is
preserved. Main control hashes matched the previously read versions (649e14,
exit 0); the complete main charter was reread (2d3d14, exit 0). Repository
intake completed 31708c/17942 to d5cf8b, exit 0.

## Frozen request scope and acquisition

Protocol SHA256:
4d80c5e158fb35be8bd569ecd6ea4824bd860275bd54c36b1332353b4e4ff37d.
Query-map SHA256:
4304b2197346f6bfb6d8b7daefc855ee9e1833b097e62813cbba323f96e3ada0.
Both were pinned at fd0511, before requests. Independent pre-request method
review found no blocker and retained the keyword/OCR coverage limits.

The public City portal web-reader open returned an HTML shell, not document
content. The first sandbox control request (2a29d7) failed DNS, exit 6,
HTTP000 and zero response bytes. This was not a server refusal. Its terminal
receipt is the failed-attempt record; no complete failed-attempt log bundle
was saved. An empty scratch-only sandbox header file remains.

A scoped network approval then allowed precisely the ten frozen public POST
requests. No private payload, credentials or cookies were supplied. Actual
command pattern, expanded only over the ten declared labels:

```sh
curl -q --proto '=https' --connect-timeout 20 --max-time 60 \
  --max-filesize 10485760 --fail --silent --show-error \
  --header 'Content-Type: application/json' \
  --data-binary @LABEL-request.json \
  --dump-header SCRATCH/LABEL.headers \
  --output SCRATCH/LABEL-response.json \
  --write-out 'http=%{http_code} bytes=%{size_download} content_type=%{content_type} redirects=%{num_redirects}\n' \
  https://sept11documents.cityofnewyork.us/api/v2/search
```

Stdout/stderr went to the matching transport/stderr files. The serial loop
stopped on any nonzero curl exit. Initial receipt b505e8, handle54481, terminal
d28070 exit0 recorded all ten individual curl exits0. Every saved transport
records HTTP200, JSON media type and zero redirects. No pagination or query
changes occurred. Scratch: /private/tmp/wtc7-job1854-locator.c4IvYO.

Forty successful-acquisition files were copied non-overwriting into this unit:
214f7a, handle90065, terminal b550dd exit0. Independent
[preservation checks](preservation-check.md) verify all forty byte pairs,
ten exact request contracts and twenty JSON integrity pins. Responses total
236,764 bytes. Preserved four-field transport logs do not independently prove
actual timeout enforcement or curl exits; terminal receipts establish the
operator's observed process exits.

Raw headers contain server-issued session cookies. The preservation checker
unnecessarily printed them once in a local tool result, then switched to
allowlisted checks. No cookie was replayed. The raw headers remain unchanged
and local-only; this unit's .gitignore excludes *.headers. They are not approved
for publication or push. No values are reproduced in this note or feedback.

## Strict contract failure

The reused scalar/property contract remains in
../test-acceptance-locator/check_metadata.py, SHA256
d561ee20e778bd0111103b3352f251396f618f2be2a23ad172ad96efb7ac6d7a.
The new strict adapter SHA256 is
6f51bfda7c4cf6508ab0095240bbbba3b935d8f23f0bae957bc36f42f8986b72.

Root's20 synthetic strict tests passed (1fe4b1, exit0). The actual historical
run, 24f118 exit1, stopped because the first affected row lacked folder_name.
No strict output was frozen or admitted: its redirected scratch output was
empty. The subsequent raw-field inspection (c22ee2, exit0) found eight missing
folder-name occurrences. This is failed fixed-contract acceptance, not an
archive content finding or a reason to synthesize labels.

## Separate diagnostic extraction

[DIAGNOSTIC-CONTINUATION.md](DIAGNOSTIC-CONTINUATION.md) explicitly preserves the
failed protocol and narrows the result to a diagnostic inventory. Its SHA256:
4d3a9fe762050b37b8a4d1880d6ae69e3ed0d9120943765997451d4aa273d17c.
The unchanged strict checker still fails. The separate diagnostic recognizes
only the observed omitted-field case, leaves it absent, retains the raw
quarantined objects/ordinals, validates supplied ID/title/page/byte fields,
and stops on unknown malformed or conflicting records. It does not grant
full-contract acceptance.

Actual root commands, using bundled Python3.12.14, non-optimized:

```sh
python3 -B -m unittest -v test_metadata.py
python3 -B check_metadata.py
python3 -B -m unittest -v test_diagnostics.DiagnosticTests
python3 -B diagnose_metadata.py
```

Eight diagnostic tests passed (527c54/6314 to f81d50, exit0). Diagnostic run
d6f4d2 exited0 and was frozen before peer findings at b128ec:
c6a80ecc100e77cc3d387e17fa032e8c4032e4e13cb761d20bffd6eaed51e7d8.
The generated scratch JSON was copied non-overwriting (3ad911, exit0).
Diagnostic implementation SHA256:
98b7a748aa7abe4c8dd1b25c9cbe930a98f6cfc42e59fd373344a82e766540a2.

Root diagnostic summary read acf8c5/98146 to89fbd9 exit0 gives142 occurrences,
97 unique IDs,134 strict-valid occurrences/89 unique IDs and8 quarantined
occurrences/8 unique IDs,519 metadata-reported pages. A separate post-freeze
join (9be8bf, exit0) gives17 IDs shared with the preceding111-ID extraction
and80 new to that extraction. These are metadata counts, not independent
documents, acquired PDFs or read pages. The full municipal PDF holdings
remain40files/104physicalpages; this unit acquired no new PDF.

The prior frozen page notes were searched read-only (d6fcc9, exit0) to test
the keyword-nonmatch interpretation: both readers recorded transient testing
in the known report family, yet this unit's transient query did not return
any of its five IDs. The cause of that retrieval failure is not diagnosed.
The positive known-record control does not cure it. This counterexample bars
treating query nonmatches as absence of the described material.

## Independent reconciliation and final checks

The separate reader froze peer-metadata.json before root read it:
83f0e653c79ae85dd24f6f0a413cf8d1cfb0a89034a72e01e2a16acdbe8f1a45.
Its independently implemented peer_check.py has SHA256
ea297ebcb43a2f428b3adb0125080217b1b03e8296be9875fe9998acf984b3b0.
Root read the complete code at f55568, exit0 and checked the output hash at
1f13fd, exit0. The reader knew the omitted-field issue and the97-ID count from
coordination before its freeze; no numerical blindness is claimed. It did not
read root code/output before independently deriving its inventory.

Root's complete reconciliation (b81c4a, exit0) compared all97 IDs, every supplied
field and raw property object,142 membership/ordinal pairs, all ten coverage
rows, eight missing-field exceptions,21 input pins and aggregate totals.
All agreed. Query-occurrence page sums are779; unique-ID page sums are519;
neither is inspected-page coverage. Root's fresh peer-checker run parsed to
the identical frozen peer JSON structure; byte-format identity is not claimed.
Root separately reran its15 synthetic controls (cf637a, exit0); all passed.
See metadata-review.md for the independent source-derivation record.

The independent method reviewer separately ran20+22 strict synthetic cases,
8+9 diagnostic cases, exact diagnostic replay and retained strict-failure
confirmation; see method-review.md. Root replayed the frozen diagnostic,
confirmed continued strict failure, checked all ten header Git-ignore rules and
eight existing local prose links (99bf10/76535 to00194e, exit0).
The six-candidate/seven-page selection and four prose whitespace checks passed
b693b6, exit0. Repository git diff --check passed0ae486, exit0.

Final critical review of the then-current report/source log against the frozen
diagnostic and prior page notes found no substantive correction (a7573e to
9fd43e and9b63dc toa07edd, both exit0). It explicitly left independent extraction
pending at that checkpoint; the reconciliation above subsequently closes only
that step. A local prose patch failed an exact-context match and made no change;
the corrected patch updated these current-state paragraphs.

Current navigation and generic feedback are updated in the existing files.
The source-preservation and data-quality skills kept the original failure,
missingness and narrow derivative result separate. Local Markdown was read
and link-checked; no rendered Page/PDF/UI review is claimed. No source/legal
promotion, external feedback send, PDF content review, commit or push occurred.
