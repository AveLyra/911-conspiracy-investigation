# Earlier audio-bearing copy check

October 7, 2026. Research continuation after the unresolved CD138 catalog
check. Preserve the preceding protocol, report and review as completed
history; this stage has not yet produced a source match.

## Question and scope

Can either exact earlier copy named by the preserved secondary index provide
longer matching pictures and original-associated continuous sound for excerpt
C? Targets are public YouTube IDs `SIbqaybkbWI` and `O0L5uyqIf0g`, plus the
older mirror page `http://www.11-septembre.com/web/terrorize.dk/911/wtc7dem2/index.html`.
Treat these as derivative publication leads, not camera masters. Root follows
the first ID; a separate reviewer follows the second ID and older page.

Use ordinary unauthenticated public access only. No cookies, account sessions,
login, access-control workaround, outreach, private searches or payment.
Allow at most four page opens and three exact-identifier searches per reviewer.
If the web text reader fails, one installed yt-dlp metadata attempt per exact
YouTube ID is allowed with ignored user configuration, no playlist, no media
download, no cache, bounded retries and timeouts. Output only title, ID,
description, duration, upload date, uploader, channel/page URL, availability
and live status; do not dump signed delivery URLs or whole info JSON.

Preserve successful allowlisted output and failures with commands and time.
Metadata success is not source authentication. A browser-reader failure or
missing search result does not prove the video is globally unavailable.

Before any media acquisition, add a prospective bounded plan specifying the
observed source, chosen available format, byte/duration limits, outputs and
inspection rules. No media acquisition under this initial scope. Do not
download merely to bypass preview/display restrictions.

## Acceptance and limits

A useful result is a retrievable source with specific provenance/continuity
claims to test, or a bounded failed-route record with the next exact locator.
No audio authenticity, physical event timing, sound classification, camera
identity, silence, deliberate manipulation or cause ranking follows from
page metadata. Any later image/sound comparison must preserve original bytes,
presentation times, edit boundaries and source-family dependence.

The first root web-text open of `SIbqaybkbWI` failed to fetch. It did not
retrieve a page stating that the video is deleted or private.

The first local metadata command failed with DNS resolution errors under
restricted network access and produced no metadata. Allow one exact retry
through the tool's approval mechanism; retain both outcomes. Do not interpret
the DNS failure as a source-side unavailability finding or install/update the
downloader merely in response to its generic error message.

## Direct public HTML route

The independent web reader normalized the older HTTP page to HTTPS before
failing; that is not a test of the literal HTTP route. Before retrieval,
allow root one direct unauthenticated HTTP(S) attempt for that exact page,
maximum three redirects, 30 seconds and 1 MiB, with a new exclusive output
path. Preserve the bytes/status if returned and inspect only as untrusted
source material. No browser session or cookies. This is source-page
preservation, not video acquisition or a display-restriction workaround.

The direct older-page request returned HTTP 404, with a 322-byte HTML body.
No redirect occurred. Preserve that source-side result separately from the
web reader's earlier failure. Before a further request, allow direct public
oEmbed JSON retrieval for the same two declared YouTube IDs, each limited to
64 KiB and 20 seconds, to distinguish reader/downloader failures from the
platform's metadata response. Stop on authentication or access restrictions;
do not change identities, sessions or clients to evade them. This is a
declared two-request extension, not part of the exhausted reader allowance.

## Pinned acquisition tool retry

Public oEmbed returned metadata for `SIbqaybkbWI`, confirming a live metadata
route for that ID; the mirror ID returned 403 and will not be retried through
alternative identities or authentication. The installed downloader is
2025.06.09, whereas the existing preservation method documents 2026.08.19
with SHA-256 `1fa6733c37ea6fb51c99ad8fe785e7b7e5f3246c9b980230329d4fb72ed8d4d6`.
The official public release page confirms that version exists and includes
YouTube extractor maintenance. This is a grounded tool-version diagnosis,
not an inference that the failed route means missing source evidence.

Allow acquisition of the official release's small Unix zipimport executable
and SHA2-256SUMS file, in a new temporary directory and preserved checksum
record respectively. Limits: 10 MiB for executable, 64 KiB for checksums,
30 seconds each, HTTPS only. Verify both the official checksum entry and the
previously recorded hash before execution; stop on mismatch. No system-wide
install, dependency update, authentication, browser state or plugin changes.
Run one metadata-only retry for the first ID, with the same safety settings,
and permit allowlisted format fields (ID, extension, dimensions, frame rate,
audio/video codecs, stated/estimated size) to plan any later bounded media
preservation. Do not print or retain delivery URLs. No media download yet.

## Early-copy media preservation and fixed screening

The pinned retry succeeded, returning a public 38-second video uploaded
2007-10-15, titled `wtc7 collapse (rare video)`, uploader `einsteen`. The
description says part of the collapse is missing; this is an uploader claim,
not authentication. A missing-JavaScript-runtime warning means the returned
format list may be incomplete. Do not call it the platform's highest quality.

Before acquisition, select the largest returned direct MP4 video stream,
format 133 (320 by 224, 30 fps, reported 758,909 bytes), and AAC audio format
140 (reported 611,813 bytes), in separate files without local remux or
transcoding. Purpose is preservation and source/scene correspondence, not a
display workaround. Download only this already metadata-public ID, maximum
10 MiB each, 90 seconds total, one retry, no overwrite or info-JSON export.
Stop on a source authentication/access restriction, unexpected ID, length
over 60 seconds, or size over the cap. Record actual source-byte hashes,
ffprobe streams, presentation timing and any acquisition warnings before
analysis. Raw files remain unchanged.

Initial screening is fixed to every integer second from zero through the
last complete second within the decoded video, using the nearest presented
frame at or after that time. Inspect the full image, not a hypothesis-selected
crop. Preserve frame indices and rational presentation times. First ask
whether distinctive stationary buildings and their occlusion relationships
match any of the three C segments; similar cloud alone is insufficient.
Record shot replacements, camera movement and missing view intervals. Do not
make a numerical cross-source clock join or acoustic-cause inference at this
screening stage. If more detail is needed, declare it separately before
choosing additional frames. No audio listening is claimed from image review.

## Preservation deviation and bounded correction

The first acquisition succeeded, but the downloader automatically invoked
FixupM4a. Thus `SIbqaybkbWI.f140.m4a` is a locally transformed container, not
the as-downloaded source bytes. Preserve it unchanged, with its 611,449-byte
size and hash; do not relabel it raw or discard the deviation. The first
video is 758,909 bytes and no video fixup was reported.

Before retry: acquire only format 140 again, with `--fixup never`, to a new
`SIbqaybkbWI.f140.unmodified.m4a` path under the same limits. Retain both
copies. Probe/hash them separately. A byte difference is expected if the
container was rewritten; compare full decoded PCM only to assess this local
transformation, not to authenticate historical audio or classify sounds.

ffprobe identifies the video as 320 by 224, square pixels, 30000/1001 fps,
time base 1/30000, start 0, duration 37.704333 seconds. Platform metadata's
30 fps and 38 seconds were rounded; the declared integer-second selection
must use actual frame PTS, not substitute exact 30 fps. Planned selections
remain targets 0 through 37 seconds. This records metadata/probe disagreement
before any image extraction rather than tuning after viewing content.
