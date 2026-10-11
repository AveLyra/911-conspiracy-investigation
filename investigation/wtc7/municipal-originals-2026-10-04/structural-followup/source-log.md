# Structural record acquisition and review receipt

October 4, 2026. Research only. Current worktree intake completed (`18cfa0`,
exit0, original handle30440 polled without restart), branch
research/sherlock-wtc7-investigation, HEAD ca1c2233. Main AGENTS, WORKFLOW,
START-HERE and full-charter hashes matched previously read controls (`e8b8af`,
exit0). Relevant skills were read again. Existing intentional WIP was preserved.
Previous turn was progress, not a wait or repeated blocker.

The prospective [protocol](PROTOCOL.md) froze before requests at SHA256
`34c26009cfec63e0fd1ce4b22680e4a82f092435ae6774ea1f690af3392892a2`
(`9beb10`, exit0). Independent method reading found no material issue before
document review (`e44ea7`/`2e6c3b`, exit0). Exact URLs came from the main
September16 catalog memo, not guessed adjacent identifiers.

## Direct retrieval

Capture window:14:08:46-14:09:37 UTC. Exactly one GET per target, concurrently
dispatched, with curl's user configuration disabled and no redirect/retry:

```sh
curl -q --silent --show-error --proto '=https' --no-location --retry 0 \
  --connect-timeout 10 --max-time 40 --max-filesize 10485760 \
  --output /private/tmp/wtc7-structural-followup.m6nJi3/<ID>.response \
  --write-out '{"http_code":"%{http_code}","url_effective":"%{url_effective}","content_type":"%{content_type}","size_download":%{size_download}}\n' \
  https://sept11documents.cityofnewyork.us/apps/content/September11_MD/<ID>.pdf
```

Literal IDs: NYC-WTC_000171807 and NYC-WTC_000173900. Both original handles
39678/44716 were polled to terminal exit0; no request was restarted. Each
effective URL matched the requested URL. No cookies, credentials or response
headers were captured. Runtime was the curl8.7.1 used in the preceding unit.

| Held source | Response and terminal receipt | SHA256 |
| --- | --- | --- |
| [NYC-WTC_000171807.pdf](NYC-WTC_000171807.pdf) | HTTP200, application/pdf,35750bytes; `9323fc`, exit0 | `1c0753e27edd92e4bc4dde5389f1b1a291bf3ee113a1600b47e73bc373816ab4` |
| [NYC-WTC_000173900.pdf](NYC-WTC_000173900.pdf) | HTTP200, application/pdf,107823bytes; `d2109c`, exit0 | `6dac8359d2f3c9ea98721c1b69f55038838d6755ea806d114cd55ff0b81d86df` |

`file` and `shasum` checked the responses (`28ff16`, exit0). `pdfinfo`
confirmed1/2pages, PDF1.5, unencrypted and no forms/JavaScript
(`920955`/`8cbfae`, exit0). ABBYY/iText/Nuix processing metadata and August12,
2026 modification dates do not authenticate historical creation or first
release. Approved `cp -n` preserved both PDF copies (`08b746`, exit0).

## Rendering and permission timeout

Temporary render directory created (`fc168a`, exit0). Full-page commands:

```sh
pdftoppm -f 1 -l 1 -r 150 -png /private/tmp/wtc7-structural-followup.m6nJi3/NYC-WTC_000171807.response /private/tmp/wtc7-structural-followup.m6nJi3/render/171807
pdftoppm -f 1 -l 2 -r 150 -png /private/tmp/wtc7-structural-followup.m6nJi3/NYC-WTC_000173900.response /private/tmp/wtc7-structural-followup.m6nJi3/render/173900
```

Same bundled Poppler26.05.0. Both handles86841/27623 reached terminal exit0
(`7a86f3`/`f26606`); no renderer warnings. The three expected outputs were
enumerated/hashed (`2afaf3`, exit0). Their later preserved hashes matched
(`bf232b`, exit0):

| PNG in render | SHA256 |
| --- | --- |
| 171807-1.png | `968cf1c81dd9f5dc0a25cd1464d54820c409d019b6958695caaf5e903da426a8` |
| 173900-1.png | `c4b522152823ef70480ec38e1d9c3c9cf5db98e8d6339e8acf9a098a84cb0ed0` |
| 173900-2.png | `1acae7ef30423d43103c6d8b9e026dba1c743bc0909a4a5127aa92ce8f34f769` |

The first approved-copy request did not execute: the automatic permission
review timed out (functions cell1042). The returned message expressly allowed
one retry; the identical no-overwrite copy then succeeded (`c5e54a`, exit0).
This is a permission-review timeout, not a server denial, failed rendering,
unsafe-content determination or duplicate acquisition. No output was copied
over a prior source. The independent reader was allowed to read the already
complete temporary renders while preservation was pending; their byte identity
is the same as the saved copies. No denied action was bypassed.

## Source interpretation scope

Root read all three complete pages once, no repeat/crop/OCR/measurement,
and froze [root-observations.md](root-observations.md), SHA256
`34034cd7a6d2f03aad34db9430e3359233f8b1f965988b08e3e5c23eed2a5808`
(`bf232b`, exit0), before receiving peer findings. The actual body/Bates
identities agree with the requested sources. Fine callout uncertainty was
retained rather than silently normalized. Historical contact details and
author paths are not proposed for outside disclosure. Independent reading,
derivative reproduction and synthesis review retain separate receipts.

The catalog/attachment completeness issue is already represented by SFB-005's
existing generic fixtures. This unit supplies another local example, not a
new Sherlock bug or duplicate issue. Archived-task routing remains unresolved;
no new payload or source material was sent. No main/legal edit, engine/bridge
action, outreach, fee, staging, commit or push occurred.

## Independent reading and cross review

The separate reading froze at SHA256
`f9058df2d766816f4b2e720b31f7271aab6c69a1c72af51aeec33bc5e8357d00`
(`b7ee55`, exit0), before receiving root's findings. The reader independently
checked both PDF and all three temporary-render pins (`d87712`, exit0), then
viewed all three complete pages once with no repeats. Root read the complete
[review](review.md) (`0be9ab`, exit0). After both freezes, the separate reader
read root's note (`6e6b74`, exit0) and checked that both frozen hashes were
unchanged (`dee2ff`, exit0). No material disagreement was found. Six complete
first-view displays in total are two readings of shared sources, not two
independent historical acquisitions or engineering validation.

The [derivative check](derivative-check.md) froze at SHA256
`7182fc77523f7afc11185690e789214fed6275d721518aa14bec51eec7180734`.
One independently executed render per held PDF reached exit0 without warnings;
all three generated PNGs matched the saved bytes and hashes. Root read the
complete receipt before marking this bounded source unit complete. Same-renderer
replication does not test a second implementation or historical authenticity.

The separate complete text review of the synthesis (`eb2446`, exit0; draft
SHA256 `dda7fd74c54e4378f4200d35527ce6058ce75c4a520019df52d571d53fd14097`)
found no material correction. It specifically checked conditional protection
wording, source/installation separation and the two distinct operations. The
reviewer did not validate the derivative receipt in that pass. Its frozen
reading remained unchanged (`58ad70`, exit0). The report's subsequent change
records the now-checked derivative completion; it does not change the findings.

## Final verification and handoff

Root read the complete derivative receipt (`228092`, exit0). The final
read-only `python3 -B -` check (`a21695`, exit0) verified six frozen inputs
(protocol, two reading records, derivative receipt and two PDFs), the three
PNG hashes and exact render-set membership against this log, fifteen local
document links, terminal newlines and absence of trailing whitespace in the
six unit Markdown files. These are scoped integrity/navigation checks, not
historical authentication. Final report SHA256:
`63f41c26b2b13b6df455825eab3056617d4ec861ebb2185a8fd9951edfafddcf`.

`git diff --check -- research/README.md
research/sherlock-wtc7-investigation/STATUS.md
research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/structural-followup`
returned0 (`046464`). Untracked unit Markdown was covered by the separate
Python whitespace check, not misrepresented as covered by Git diff.
The earlier combined diff/status command's live handle75684 was polled to
terminal exit0 (`c93614`), retaining existing WIP and the municipal subtree.
No stage, commit, push, main/legal change or new feedback transmission occurred.
Current STATUS/research map retire these two targets and name the exact located
enclosure framing-plan candidate172233 for the next prospective source join.
Full goal remains active; unresolved model, listening and human gates are not
treated as completed or as a universal investigation blocker.
