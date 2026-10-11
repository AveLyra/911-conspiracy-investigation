# Named drawing query receipts

October 4, 2026. Preserved public metadata, not primary-page interpretation.
Protocol SHA256 `9369d79f07726b7b46570d734a828158d6d8fe95c0596414c3dd41285f6534cc`
was saved before searches. Main control hashes rechecked `b54dac`, exit 0,
and matched their previously read versions. The immediately preceding user
coordinate reply was a no-progress confirmation, not a blocker. This unit
executes an available new locator test after completing the folder comparison.

## Held catalog and web context

The exact held catalog is `../folder-document-locator/folders.json`, SHA256
`cf3afa33cc58a0f2a9d48e6fbac57cdd8bb060b046cf5373d261d37bb976b704`.
It has 4205 rows, capture September 11, 2026, and the six-column structure
checked by the saved parser. The protocol's phrase "prior unit" means this
named locator, not the intervening PDF-reading unit; that path clarification
was supplied to the independent reviewer before its catalog inspection.

The other fixed locator is main `research/WTC7_archive_leads_2026-09-16.md`,
SHA256 `01f7419ec36c6686ac154c6f6e05e3309d90704069957119cfc9efb8160bc3ea`.
Actual command (`d20db3`, exit 0):

```sh
rg -n -i 'SKP[ -]*[34]|S[ -]*TS[ -]*7' <held-folders.json> <main-archive-leads.md>
```

Both named input paths were explicit in execution. Only catalog physical line
4097 and memo line 84 matched, both the 167873 cover. The catalog row's
one-based data ordinal is 4075, distinct from physical line number 4097.
No off-source match occurred. A web-reader open of
https://sept11documents.cityofnewyork.us/ returned the public portal shell,
zero readable text lines (`turn749view0`), not a document-content result.

## Public requests

Four `*-request.json` files were saved before execution. Each asks the known
read-only POST search route `https://sept11documents.cityofnewyork.us/api/v2/search`
for count 50, no content sample, and eleven explicit metadata properties.
Payloads contain only public source labels and sheet numbers. No credentials,
cookies, private case text, redirects or source uploads were used.

Scratch directory from `mktemp -d`:
`/private/tmp/wtc7-drawing-locator.bTnvMw`. Each command used:

```sh
curl -q --proto '=https' --connect-timeout 20 --max-time 60 \
  --max-filesize 10485760 --fail --silent --show-error \
  --header 'Content-Type: application/json' --data-binary @<saved-request.json> \
  --output <scratch-response.json> \
  --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects}\n' \
  https://sept11documents.cityofnewyork.us/api/v2/search
```

The four sandbox attempts terminated exit 6, could not resolve the host,
HTTP 000 and zero downloaded bytes: SKP-3 `861e9a`, SKP-4 `b8223d`, S-TS-7
`0cfdb4`, control `949f03`. These are local DNS failures, not HTTP refusals
or completed City queries. The exact commands were then approved for network
execution. Each produced one HTTP response: all 200, application/json;charset=utf-8,
zero redirects and terminal exit 0. No server-denied request was retried.

| Query | Terminal receipt | Response bytes | SHA256 |
|---|---|---:|---|
| SKP-3 | a6c1b9 | 22502 | a13e7e290cd0e625db4502ec4197389c1c549b138b48502c2daebc00c62a3a26 |
| SKP-4 | da11a7 | 21189 | e4848f93061aaf339bdfb006fce212f95805298ba24fe60e8e1d2fbcb6be9a0b |
| S-TS-7 | 629908 | 10553 | 639d3c9f00b00acbdf613525c3ffa27b6f2e3190a1b566269a003d59424b41c7 |
| Control | 63f688 | 8451 | fdf92a229791be47e9ca997939bc9df8f9543fa4eb7764c3bb3c1770a52ae57b |

SKP-4 handle 82679 was polled to terminal completion, not restarted.
Scratch file mtimes (`8b90d8`, exit 0) were October 4, 2026, 16:16:40-41
America/New_York (UTC-04:00); these are acquisition-file times, not historical
document dates. Approved `cp -n` preservation of four responses completed
`71c241`, exit 0. Original payload/response hashes are in checked-metadata.json.

## Root parsing

An initial schema inspection of the control response completed `e0e2e8`,
exit 0 after polling handle 85203. It supplied the actual resultset/property
structure. The read-only `check_metadata.py` was then saved with strict
JSON-key/property checks and metadata validation, not downloaded/executed code.

First execution failed at the Python-int-only byte-count assertion (`225123`,
exit 1). A bounded diagnostic (`702ae9`, exit 0) showed `pdf_size.value.num`
was represented as whole-valued floats in all returned entries, including
40327.0 for the known cover. The repair accepts int or float only if finite,
positive and exactly integral; raw source values remain unchanged. This is
a representation correction, not relaxed byte-count semantics. No other
failed checks were bypassed and no response was refetched.

Corrected command:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/drawing-locator/check_metadata.py
```

Run from the investigation worktree, it completed `1355a0`, exit 0 after
polling handle 96347. Full stdout was parsed as JSON and preserved unchanged
as `checked-metadata.json` with a final newline. It reports four matching
query echoes (only empty user_context stripped), unique properties/scalars,
positive integral byte counts, valid document IDs/title pairs, WTC 7 source
identity, matching repeated properties, and the expected known-cover control.
All four result sets report no next/previous page and NO_MORE_RESULTS.
The returned 29 occurrences reduce to 16 IDs and 47 reported pages. No
actual PDF page count, drawing contents or archive-wide recall is verified.

## Reproduction and independent check

Root reran the corrected parser through `cmp - checked-metadata.json` with
pipeline failure propagation; output was byte-identical. Four additional
`cmp` checks confirmed the preserved responses equal the scratch acquisition
bytes (`58ef0b`, exit 0). Protocol, checker and derived output pins were:

- Protocol: `9369d79f07726b7b46570d734a828158d6d8fe95c0596414c3dd41285f6534cc`.
- Checker: `1ac8bb366e0c8b2dd61dddcd7674a45760d73d5b5e01f7933860accdadfb5133`.
- Checked output: `43ab678e3e54683ae69096a7a35ff500fb4b47312762d2192e3716a66f99a720`.

The independent reviewer froze `metadata-review.md` before reading root's
parser/output/report, SHA256
`73713f7626297091eedc90d2de5a0a8087f66a98afa62dd8cbc63474c8f6bcf4`.
Its separate jq-based checks agree on 29 occurrences, sixteen IDs, repeated
property equality and reported query termination. It additionally checked
all sixteen exact source/box/folder joins against the held catalog without
equating aggregate folder counts with individual PDFs. Root read the whole
receipt (`7b8a17`, exit 0). Its transport-status limitations are preserved:
this was independent parsing of saved responses, not another network query,
source-content reading or historical authentication.

Root checked the two new unit reports/logs, protocol and parser for trailing
whitespace and thirteen local links (`b254bd`, exit 0); all passed before the
later review link was added. `git diff --check` also passed (`696b9d`, exit 0).
Research navigation now points to actual content candidates rather than the
completed proposal-copy review. Branch/HEAD rechecked `6a9075`, exit 0:
`research/sherlock-wtc7-investigation`, `ca1c223335c20905d6608eb15c676f88cbfac734`.
No staging, commit or push occurred. Existing SFB-005 catalog/source-family
and typed-parser fixtures cover these workflow risks; no separate inspected
Sherlock defect is claimed. Archived-task routing remains unchanged.

After freezing, the peer compared its findings with root's saved output;
all five equality checks passed (`d4810b`, exit 0). It found no material
overstatement in the report/source log before the independent-completion
paragraphs were added. Its phrase "separate authorization and admission"
means a separately declared content scope/admission, not renewed user
permission for public retrieval already authorized by the goal. The original
frozen peer wording is preserved; this is its subsequent clarification.
