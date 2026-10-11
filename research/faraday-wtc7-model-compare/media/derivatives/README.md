# NIST WTC 7 collapse-model Ogg derivative

- Public file record: <https://commons.wikimedia.org/wiki/File:NIST_WTC_7_collapse_model_with_debris_impact_damage.ogv>
- Downloaded: 2026-10-02 from the file link exposed by that Commons record.
- Local filename: `NIST_WTC_7_collapse_model_with_debris_impact_damage.ogv`
- SHA-256: `d926028f5ad980e3f1126071c834ffc85d3d5c4976e68cf2f7a9a543ed424193`
- Local probe: Ogg/Theora, 464 × 338, 25 fps, 24.880 s, 3,693,005 bytes (`ffprobe`).

This is a Commons-hosted derivative. The matching hash confirms that the
retrieved bytes match the candidate hash already recorded in the exploratory
review; it does not authenticate the file as a native or master NIST export.
The Commons description reports that the animation contains two concatenated
clips. Treat it as a candidate visual reference only, not as a source of
validated physical measurements.

## Provenance check (2026-10-02)

The Commons record attributes its two constituent clips to an old NIST index
and the files `CU animation.flv` (“Collapse Initiation -- Physics Based
Model”) and `whole building animation.flv` (“WTC 7 Collapse with Debris
Impact Damage – Physics Based Model”). On 2026-10-02, the index and both file
URLs linked from that record returned 404. NIST's current [WTC investigation
media repository](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations)
confirms that it has a general category for investigation-generated computer
simulations, but its landing page does not identify this exact Ogg file or
provide a matching download.

**Inference and limit:** the Commons record supplies a specific, plausible
NIST source trail, but the exact-byte chain to a currently accessible NIST
master/original was not independently confirmed. A stale or migrated URL is
an ordinary alternative explanation for the 404s; the dead links alone do
not establish fabrication, intentional removal, or any cause of the video's
unavailability.

### Internet Archive capture of the CU-animation URL

The Internet Archive CDX index lists a capture of the Commons-linked CU
animation URL at `20110427193523`, with recorded status `200`. Retrieving that
timestamp's identity replay on 2026-10-02 returned an HTML document, not an
FLV: the response header reports the capture time as 2011-04-27 19:35:23 UTC,
and the document title is “National Institute of Standards and Technology
Error Page.” The replay body was 13,113 bytes with SHA-256
`27c355ac556ac27556a08b871be9a5336f321de931fcfb540562b2632c48a98a`.

- [CDX capture listing](https://web.archive.org/cdx/search/cdx?url=www.nist.gov%2Fpublic_affairs%2Freleases%2Fwtc_videos%2FCU%20animation.flv&output=json&filter=statuscode%3A200&fl=timestamp%2Coriginal%2Cstatuscode%2Cdigest%2Clength)
- [2011 identity replay](https://web.archive.org/web/20110427193523id_/http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.flv)

This resolves the apparent `200` only for that archived capture: it is an
HTTP-successful error page, not a successful video retrieval. It establishes
that this URL yielded an NIST error page in this one 2011 snapshot. It does
not establish what the URL served in 2008, whether the animation existed at
another URL, or why the resource was unavailable by 2011.

The same check on the Commons-linked `whole building animation.flv` URL found
a CDX capture at `20110427194914`, also indexed with status `200`. Its 2026
identity replay was likewise an HTML “National Institute of Standards and
Technology Error Page,” 13,113 bytes, with the same replay-body SHA-256 as
the CU-animation capture above. Thus, both named URLs resolve in these 2011
archive captures to the same error-page body, not to video data.

- [Whole-building CDX capture listing](https://web.archive.org/cdx/search/cdx?url=www.nist.gov%2Fpublic_affairs%2Freleases%2Fwtc_videos%2Fwhole%20building%20animation.flv&output=json&filter=statuscode%3A200&fl=timestamp,original,statuscode,digest,length)
- [2011 whole-building identity replay](https://web.archive.org/web/20110427194914id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.flv)

This narrows the live provenance lead: by these April 2011 snapshots, neither
Commons-cited URL yielded its named animation. The identical error page could
reflect a shared web-server error template or asset-path problem. It does not
show that the files were never published, that the Commons copy is false, or
that either URL was deliberately disabled.

### Archived NIST index page (2008)

An Internet Archive capture of the NIST video index at
`20080823230025` preserves an NIST page dated August 21, 2008. The archived
HTML is 10,016 bytes (replay SHA-256
`4a3b01b863f020d21a5a964e84f52737183a962b42a908da8dd556a785f4b9ae`). It
contains two Flash embeds: `CU animation.swf`, captioned “Collapse Initiation
-- Physics Based Model,” and `whole building animation.swf`, captioned
“Visualization Model of WTC Collapse”; both are credited to NIST on that
page.

- [2008 archived NIST index page](https://web.archive.org/web/20080823230025id_/http://www.nist.gov/public_affairs/releases/wtc_videos/wtc_videos.html)
- [Wayback CDX capture listing](https://web.archive.org/cdx/search/cdx?url=www.nist.gov%2Fpublic_affairs%2Freleases%2Fwtc_videos%2Fwtc_videos.html&output=json&filter=statuscode%3A200&fl=timestamp,original,statuscode,digest,length)

**Provenance implication:** this is primary-page evidence that NIST publicly
listed two animations in 2008, with the stated names, captions, and credits.
It does not establish the contents or hashes of either embedded SWF, nor
prove which SWF (if either) was converted into the Commons Ogg. The archived
page's second caption (“Visualization Model of WTC Collapse”) also differs
from the Commons record's description for its `whole building animation.flv`
source (“WTC 7 Collapse with Debris Impact Damage – Physics Based Model”).
That discrepancy calls for checking the archived SWF/FLV assets and later
index versions before treating the files as identical; it is not evidence of
alteration or concealment by itself.

### Archived SWF captures retrieved (2026-10-03)

Wayback CDX records returned captures for the two SWF paths embedded in the
2008 NIST page. Identity replays of the August 29, 2008 captures returned
actual compressed Macromedia Flash version 9 files (`CWS` signature), not
error-page HTML. The archive replay headers report the captured origin's
content lengths, matching the local file lengths:

| Archived NIST path | Capture timestamp (UTC) | Local replay size | SHA-256 |
|---|---:|---:|---|
| `CU animation.swf` | 2008-08-29 10:02:16 | 84,654 bytes | `e067773201621de8dcc0851eeada92a61a02ec8490302af99fe676274c145f44` |
| `whole building animation.swf` | 2008-08-29 10:00:49 | 84,678 bytes | `9acbef93ef59f0103071b8ce580cee3beb8cdb6139a2ac16f15d864013c84f44` |

Identity replays of the September 7, 2008 records also returned Flash files,
but they are different binaries and report Flash version 8 rather than
version 9. Their replay headers give September 4 `Last-Modified` dates:

| Archived NIST path | Capture timestamp (UTC) | Local replay size | Flash version | SHA-256 |
|---|---:|---:|---:|---|
| `CU animation.swf` | 2008-09-07 01:30:11 | 52,070 bytes | 8 | `c3a00150f07f449d5a642879f2c294a186b3314cb2672134d708ecff85db8508` |
| `whole building animation.swf` | 2008-09-07 01:30:06 | 52,079 bytes | 8 | `1926c25114092d4c61a170ed8d1a2a04aa223f758421f75b35fdf6185e793074` |

The files are retained alongside the August 29 captures. The verified
signature/version, byte-length, and hash differences establish distinct
archived binaries at the same NIST paths by September 7; they do not reveal
whether the depicted structure, simulation inputs, or intended meaning
changed. A recompile/re-encoding is a plausible alternative to a substantive
model revision. Any stronger comparison requires inspecting the SWF contents
or comparing rendered frames under a reproducible player.

The captured files are retained under `archived-nist-swf/` with their capture
timestamps in the filenames. These are Internet Archive replay bytes from
captures of files served at NIST URLs, not independently acquired NIST
masters. Their archival existence corroborates the 2008 page's two embedded
SWFs; it does not establish that either is the Commons Ogg's source. The
CDX listings also contain later records with different digests for both
paths, so the archived files changed or were captured differently later;
which version, if any, corresponds to the Commons derivative remains open.

- [CU SWF capture](https://web.archive.org/web/20080829100216id_/http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.swf)
- [Whole-building SWF capture](https://web.archive.org/web/20080829100049id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.swf)
- [CU SWF September 7 capture](https://web.archive.org/web/20080907013011id_/http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.swf)
- [Whole-building SWF September 7 capture](https://web.archive.org/web/20080907013006id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.swf)

### SWF payload inspection and decoder limit (2026-10-03)

The CWS files were inflated by skipping the 8-byte SWF header and zlib-
decompressing the remainder, then scanning printable strings. Each CU SWF
contains the player/video-file name `CU animation.flv`; each whole-building
SWF contains `whole building animation.flv`. The SWFs are therefore Flash
player wrappers that reference separate FLV media, not self-contained video
files. This links the 2008 NIST page's SWF objects to the FLV pathnames
identified in the later Commons source metadata, but does not authenticate
the Commons Ogg as a transcode of those FLVs.

Local decoding test: FFmpeg 7.1.1's SWF demuxer treated each August 29 SWF
as a single 45 × 45 ARGB raw-video frame at 12 fps; decoding stopped after
one frame. For each September 7 SWF, FFmpeg identified two streams with
unknown codecs and zero dimensions, then failed because it found no output
stream. Thus this FFmpeg path does not render the animations; the 45 × 45
frame is not a meaningful visualization of the WTC 7 sequence. A compatible
Flash runtime or a matching FLV capture is needed for a content comparison.

This result narrows the provenance question without resolving it: the NIST
player wrappers name the same FLV paths that later Wayback captures return as
error pages. The Ogg could still be a derivative made while the FLVs were
available, but that relationship is not established by names alone.
- [CU SWF CDX records](https://web.archive.org/cdx/search/cdx?url=www.nist.gov%2Fpublic_affairs%2Freleases%2Fwtc_videos%2FCU%20animation.swf&output=json&filter=statuscode%3A200&fl=timestamp,original,statuscode,digest,length)
- [Whole-building SWF CDX records](https://web.archive.org/cdx/search/cdx?url=www.nist.gov%2Fpublic_affairs%2Freleases%2Fwtc_videos%2Fwhole%20building%20animation.swf&output=json&filter=statuscode%3A200&fl=timestamp,original,statuscode,digest,length)
