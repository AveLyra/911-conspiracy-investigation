# Acquisition and validation record

2026-09-20 UTC. Research-only worktree, branch
research/sherlock-wtc7-investigation, HEAD e8d83d7. Expected pre-existing dirty
research preserved. No commit or push. Root rechecked goal (active), branch,
status, controls, skills and the prior declared DEM-04 handoff.

## Actual requests

Before the local protocol: web open of the declared university landing page
succeeded (69 returned lines); following its link13 returned403. No PDF was
obtained. Independent reviewer was assigned landing page and held lead only,
without root's substantive report; its read is not a second event witness.

Local temporary directory: /private/tmp/cather-pound-source.PgFv2C.
Client: curl8.7.1, x86_64-apple-darwin25.0, SecureTransport,
LibreSSL3.3.6, zlib1.2.12, nghttp2/1.68.1. Each invocation used:

```
curl --location --max-time 45 --proto '=https' --proto-redir '=https' \
  --dump-header <exact-output>.headers --output <exact-output>.body \
  --write-out 'http_code=%{http_code}\nurl_effective=%{url_effective}\nsize_download=%{size_download}\ncontent_type=%{content_type}\n' <declared-URL>
```

The two URLs are frozen in [PROTOCOL.md](PROTOCOL.md). No credentials,
custom user agent, cookie replay, challenge solving or alternate URL used.

| Attempt | Result | Preserved evidence |
|---|---|---|
| Sandboxed landing | exit6; DNS resolution failed; HTTP000, zero downloaded bytes | empty landing.headers; body not created |
| Sandboxed thesis | exit6; DNS resolution failed; HTTP000, zero downloaded bytes | empty thesis.headers; body not created |
| Approved public landing | exit0; HTTP200; 40,666 bytes; text/html; same effective URL | landing-public.body and headers; response date07:52:02 GMT |
| Approved public thesis | exit0; HTTP403; 5,666 bytes; text/html; same effective URL | thesis-public.body and headers; response date07:52:07 GMT |

DNS failures were local transport failures, not university refusals. The
approved public requests were the declared ordinary retrieval, not a change
of target or access-control bypass. Curl exit0 is successful HTTP transport,
not successful thesis acquisition. The403 header identifies a challenge;
no challenge was solved or replayed. Raw response headers can contain transient
server-generated cookies: retain locally, do not transmit as feedback.

All six created response files were preserved without overwrite using cp -n
in [source/](source/). The integrity manifest records the captured bytes,
not the historical authenticity or correctness of the source. No PDF renderer,
PDF text extractor, video decoder, numerical solver or timing analysis ran.
This unit does not trigger the PDF skill's full-page reading stage.

## Inspection and failures

Root inspected the landing page's title/author/date/citation and complete
abstract in the captured HTML, including the positive sensor/model claims.
Repeated metadata copies within that page are one source. The webpage's
publication metadata disagrees with the old held manifest's2018 label; main
manifest bytes remain unchanged. No conclusion that the thesis lacks internal
measurements is warranted without its full content.

Some combined onboarding/status outputs were truncated. Controls had been
fully read before this continuation; targeted current handoff, metadata and
source lines were subsequently retrieved. No complete fresh reading of the
entire long status/index was claimed from a truncated output.

## Final checks and review disposition

The [independent review](independent-review.md) preserved its prior source-scope
findings before reading root's report; subsequently it checked all six source
hashes, exact file set, sizes and whitelisted HTTP fields. No material
scientific overclaim was found. Root read that review completely and separately
reran shasum -a256 -c, the six byte sizes and HTTP/date/content-type/challenge
fields: all six hashes passed, sizes total49,301 bytes, statuses200/403 matched.
These checks reproduce receipt integrity, not the historical measurements or
the original download process. Original command outcomes are root's recorded
tool observations; the reviewer did not independently witness those processes.

The reviewer correctly identified protocol wording ambiguity: after observing
the web403, the protocol explicitly allowed an ordinary public-client attempt,
but also said not to retry a denied route. The public-client request therefore
repeated the same denied URL through a different ordinary client. It was not
an access-control bypass; nevertheless a blanket claim of no repeated denied
URL would be false. Preserve the original protocol and this clarification.
No further requests to that route occurred or are authorized by this unit.

Two narrow validation-discovery commands failed because this checkout has no
tools/ directory. In the first command an && chain stopped at that lookup, so
its following checksum check did not run. Root then ran the source integrity
checks separately and successfully. A first multi-file index patch failed on
an incorrect expected README heading; a subsequent read verified neither
index had changed, and the corrected patch succeeded. No failed check is
counted as a pass.

Root's six-link check of the initial three unit Markdown files passed;
git diff --check passed for the two edited research indexes. Main control
hashes remain unchanged. The current status's stale statement that lateral
geometry was prospective was corrected to its already-completed bounded
status. Existing WIP and all earlier study outputs remain preserved. No code,
solver, video/PDF analysis, canonical promotion, filing, transmission, commit
or push occurred. This unit closes only the declared source route.
