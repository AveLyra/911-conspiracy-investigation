# HBI acquisition execution record

September 20, 2026 UTC. Research only. The one acquisition permitted by the
[frozen protocol](PROTOCOL.md) has ended in failure. No video, image, audio,
media fragment or platform metadata sidecar was acquired. Source admission,
derivative production and the proposed paired visual study were not run.

## Before the historical attempt

The protocol was frozen before acquisition or viewing. Independent code review
identified four implicit defaults; [prospective controls](ACQUISITION-CONTROLS.md)
required explicit routing/environment, actual downloader runtime/package pins,
warning-only file fixups and refusal of unavailable fragments. Root inspected
the relevant installed option/implementation definitions before execution.
This was preservation engineering, not evidence of historical tampering.

Wrapper versions and failures remain distinguishable:

- Initial, never used for historical retrieval: SHA-256
  `a14161bc9a79734e479c274762f3d246105a087a6b74ef7b9b46235dabed8022`.
  Harmless nonzero/timeout/existing-output controls passed in
  `/private/tmp/hbi-acquisition-controls-9functmm`.
- First repaired, never used for historical retrieval: SHA-256
  `f681ed90144fdd04b6e2c28ad80cf01eb1e2f3690fed5e13c12cf394a0fcb095`.
  Its required-member check wrongly expected `extractor/youtube.py` instead
  of the installed YouTube package. Root's final-control attempt failed
  before child tests; `/private/tmp/hbi-final-controls-pe41ehyc` remained
  empty. The independent reviewer also found this error. A later command's
  success in the same shell return did not erase that failed check.
- Final: SHA-256
  `50676c016235530b9b1373623224d97a7cf7b6fb8929ba9abcd60e9b83ef7526`.
  Required members corrected; fresh independent pre-execution review passed.
  No historical invocation used a superseded version.

Final-code harmless controls were executed by root, not independently rerun
by the reviewer. In `/private/tmp/hbi-final-controls2-t4_3bdak`, an exit-3
child retained separate 12-byte stdout/stderr and a two-second child was
terminated at a 0.25-second timeout, returning timeout/exit-9 with diagnostics
preserved. The first environment assertion failed because macOS added
`__CF_USER_TEXT_ENCODING`. A keys-only diagnostic established that difference;
no value was printed and no wrapper change was made to hide it. In
`/private/tmp/hbi-env-refusal-b7xbxqqs`, the corrected expected-key check passed
with no proxy/PYTHONPATH/PYTHONHOME inheritance; an existing acquisition
directory was refused and left empty. These are separate control runs, not a
single all-path certification.

Five synthetic cases using the installed `match_filter_func` passed: accept
the selected nonlive 18-second item; reject a wrong ID, live item, 31-second
item and missing duration. They made no network requests. The exact filter
was `id = '83cFWPY07dI' & duration <= 30 & !is_live`. The original version and
control failures are preserved here rather than described as clean first runs.

## Single historical invocation and terminal result

Working directory: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
Actual command, approved for the scoped ordinary public retrieval:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 research/sherlock-wtc7-investigation/comparator-hbi-motion/acquire.py
```

The exact downloader argv, child environment and complete pins are in
[start.json](acquisition01/start.json) and [receipt.json](acquisition01/receipt.json).
Installed downloader: 2025.06.09; actual shebang Python: 3.13.9. The wrapper
used a separate Python 3.13.7. All six pinned files and 1,111 package Python
source files were unchanged. This is not transitive-library or loaded-code
attestation.

Recorded interval: **05:32:19.975017–05:32:22.431100 UTC**, 2.456083 seconds.
The process returned **exit 1**, with no timeout or exception-class entry.
The execution service initially yielded session 7655; the subsequent poll
returned terminal exit 1. No process is awaiting another poll or retry.
One invocation does not mean one HTTP request.

The destination contains exactly four regular files: start record, receipt,
354-byte stdout and 288-byte stderr. Receipt-listed product hashes reconcile;
the receipt does not list its own subsequently written hash. The independent
[review](independent-review.md) preserves exact sizes/hashes and a reproducible
read-only check. There is no video, info-JSON, partial media or fragment.

All diagnostics were assessed: six stdout lines describe requested-item
context and extractor fetch progress; stderr has one missing-URL/forced-SABR
format warning and one terminal page-reload error. An initial keyword scan
that found no matching category was not treated as clean diagnostics; a
sanitized message read and independent complete classification followed.
Raw logs remain local and were not copied to another service.

This proves failure of this pinned attempt, not removal, authentication denial,
unavailability, concealment or any historical collapse mechanism. A client/
platform compatibility issue is plausible but not established. No retry,
software update, alternate recording, authentication or workaround followed.

## Documentary work and stopping point

Root and a separate reader checked the held ASI/Vimeo HTML, not new live-site
responses. The [source review](source-review.md) distinguishes exact title/ID
embedding from a cross-document named-operation inference. Its conditional
wording about an “access copy” is prospective: **this unit holds a recording
lead, not a newly acquired copy**. Earlier channel/duration assertions remain
inherited; no returned metadata upgraded them.

The excluded reactor PDF was neither inspected nor hashed. No decoder, image
display, audio analysis or visual comparison ran in this unit. The one-attempt
route is closed; the larger investigation remains active. Any isolated newer-
client attempt requires a new prospective scope, official dependency review
and fresh controls; it must not overwrite or retroactively extend this unit.
