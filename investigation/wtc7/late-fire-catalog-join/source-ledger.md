# Catalog queries and acquisition record

Research-only, 2026-09-19 (UTC date of acquisition). This is a retrospective
record of actual requests/observations, not a claim that every response was
byte-preserved. Primary records and secondary pointers remain distinct.
The full pins and independent identity checks are in
[independent-source-review.md](independent-source-review.md).

## Root public-web search ledger

Queries were submitted in batches; returned snippets are not authenticated
item records. Where the combined output was truncated, no claim is made to
have inspected every returned hit. Only the opened/inspected routes below
enter this unit's source conclusions.

| Query | Useful result / limit |
|---|---|
| `"CBS-Net Dub5 14"` | Dailymotion title match at https://www.dailymotion.com/video/xf4hhw; secondary uploader description, no video inspected. |
| `"42A0122" "G25D33"` | Secondary IC911 index, no primary exact MPEG identity. |
| `site.nist.gov "Cumulus" "video" repository` | No exact clip join in inspected returned results. |
| `"NIST" "WTC" "repository" site:nist.gov` (domain filter nist.gov) | Official NIST repository landing page located. |
| `"CBS-Net Dub5 15"` | No primary exact file identity in the inspected web-search response; later resolved by scoped catalog navigation. |
| `"42A0122" archive.org` | Secondary pointers; no exact file acquired. |
| `"CBS-Net-NIST-Dub5" archive.org` | No exact primary join in inspected returned results. |
| `"42A0122" "NIST"` | Secondary index material; no exact MPEG filename established. |
| `"CBS-Net Dub6 44"` | Secondary index; primary identity subsequently resolved through Drive. |
| `site.ffmpeg.org "guess_layout_max"` | Official FFmpeg documentation for the input option used in the separately declared FRAME-PLAN. |
| `site.ffmpeg.org "select" "showinfo" "copyts" documentation` | Official FFmpeg documentation. No imported executable/source script. |

AP's six public queries, public search route and completed zero-result state
are recorded separately in [ap-catalog-review.md](ap-catalog-review.md).
Root read that entire note; root did not independently reopen the AP UI.

## Opened routes and actual access

- https://archive.org/details/cbs200109111856-1938?start=2322 and the same
  item without a query returned InternalError through the web text tool.
  https://archive.org/metadata/cbs200109111856-1938 also failed in that tool,
  but a bounded public HTTPS request successfully returned HTTP200 and
  15,348 bytes to `sources/ia-cbs-metadata.json`. Final URL unchanged.
  No IA video bytes acquired or viewed; metadata describes stream/loan-only
  broadcast-archive access. A tool route failure is not item absence.
- http://911datasets.org/index.php/Release_14_-_NIST_Cumulus_Video_Database
  returned InternalError in the web tool. No content acquired by that route.
- https://ic911.org/building-7-collapse/ was opened as a secondary index.
  Its Window Shot section repeats the named CBS/AP/IA leads in the preserved
  2020 index. This is not independent camera corroboration. A different
  `24:49` reference on the current page belongs to NBC Leaning Cam, not this
  Window Shot lead; it is not assigned here.
- https://www.dailymotion.com/video/xf4hhw yielded page metadata only.
  A clicked IC911 link to https://www.youtube.com/watch?v=tZlENw_xuXU returned
  InternalError. No playback/acquisition or source-content conclusion.
- https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations
  was read in the web tool and preserved separately by bounded HTTPS request:
  HTTP200, final URL unchanged, 101,629 bytes. The text rendition omitted
  usable folder anchors; inspecting the preserved HTML revealed them.
- The two exact NIST proxy URLs for Organized Photos and Video Clips and
  Original Video from Tapes returned InternalError in the web text tool.
  Opening the identified Organized link in the in-app browser succeeded and
  redirected to https://drive.google.com/drive/folders/17lDS4YslnUaOHv-x2CEhWLVzmceNllk1.
  The Original Video from Tapes folder
  `12vUikS9WpbovdIWwLAIqI7rSKDE4WMRQ` was not explored. Do not attach its
  category label to these Organized-category acquisitions.

The two raw HTTPS text requests used location following limited to three
redirects, HTTPS-only redirects, 45-second timeout and 8,388,608-byte cap.
Transport headers are retained locally in ignored `*-local-only` files, not
published or used as historical evidence. Their contents were not dumped.

## Scoped connector route

See [listing-request-receipt.md](listing-request-receipt.md) for the exact
retrospectively reconstructed query and two listing request payloads. Root
fetch, scoped folder search, listings and four exact metadata responses are
preserved under `sources/`. No global search of unrelated personal Drive
files was performed. NIST's public link supplied the initial folder ID.

The four exact metadata records establish the current target identities:

| Target | ID | Catalog bytes | Local acquisition |
|---|---|---:|---|
| CBS-Net Dub5 14.avi | 1cero39dWDYw60oQ4LUaw_Uk939KdBAKP | 73206324 | Not acquired |
| CBS-Net Dub5 15.avi | 1j6wE4s-bmFHqMMnmJZ1yqajsUKPeNfAN | 60183924 | Acquired, HTTP200, exact expected size |
| CBS-Net Dub6 45.avi | 1jKJ0OdPswfyuuDxUVRxDazgK020ngJka | 234785572 | Not acquired |
| CBS-Net Dub6 44.avi | 1hNNuWhtzaJVMJPY1GjVcE3iSe-OH6qyR | 104308572 | Acquired, HTTP200, exact expected size |

Each item URL is `https://drive.google.com/file/d/<ID>/view?usp=drivesdk`.
The four requested metadata field lists are preserved in the request receipt;
several fields were omitted from normalized responses. Null parent/checksum
output does not establish provider absence. Local SHA-256 values are pins for
our byte streams, not comparisons against an independently provided hash.

For the two acquired items, the connector fetch arguments used that exact item
URL, `download_raw_file:true` and `include_base64:false`. Returned file URIs
were materialized with bounded HTTPS requests (55-second timeout; 65,000,000
and 110,000,000-byte caps respectively), not guessed media URLs. Both returned
HTTP200, with sizes in the table. Preserve these local identities:

- `sources/cbs-net-dub5-15.avi`, SHA-256
  `8a4e3e02105d65140c2a3dc0bc95af0d907866de85353d5c9f498636aea79781`.
- `sources/cbs-net-dub6-44.avi`, SHA-256
  `c3a19c895f5bcacdb473745641dbbd500982219a6de57726920125477a12f90c`.

Acquisition is ordinary public-source preservation under the charter, not a
workaround for a display restriction. No conversion occurred before saving
these AVI byte streams. Decoder errors subsequently found in Dub6 44 do not
invalidate byte-count/hash identity, but do limit image-fidelity acceptance.

## Browser and operational qualifications

Root inspected a paused public Drive preview of Dub5 15, then its title and
public-link status. This was not full playback. The existing browser profile
was already signed in; no new login, permission grant or account-wide search
was performed. A single visible Download-button click had no confirmed
outcome. A subsequent exact-name file search encountered a Downloads permission
denial; no broad escalation or claim of download absence followed. Acquisitions
above instead have their own explicit connector/file-byte records.

The first raw-file connector response was unnecessarily echoed to internal
tool output with its transient retrieval URL. It was not copied into a source
file or this record; subsequent output omitted that URL. Do not repeat or
publish transient credentials. This was an operational logging mistake, not a
finding about source authenticity. No case document was uploaded or sent.

No fee, outreach, contact submission, new account, archive bypass, external
publication, commit, push or legal-record promotion occurred. Retrieved notices
were treated as source content, never as instructions granting authority.
