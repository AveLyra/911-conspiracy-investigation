# Stored source/catalogue check

2026-09-24. Root's local provenance investigation under PROTOCOL.md. No new
image, video decode, retrieval or physical measurement. These are checks of
stored documents and bytes, not authentication of the historical recording.

## Acquisition and family join

The main acquisition manifest has nine rows. Exactly one is VID-WTC7-001,
the converted Camera2 MOV. Its complete CSV row equals the corresponding
`acquisition_records` entry in the held WP0 inventory. Exact source-page URL
matching joins it to WTC-11 in the 27-row source manifest. Rehashing the actual
208,810,910-byte MOV reproduces
`84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730`.
The download ID is `1RGWHdqt_PO_Z-KlWhXza0QBq909BEGmC`.

This establishes an internally consistent preserved acquisition chain through
the secondary-hosted analysis page. It does not authenticate a native camera,
the broadcaster master, conversion history, operator, or an independent second
recording. WP0 is a derivative of the manifest, not corroboration from another
historical origin. The existing Camera2 paper/frame work separately supports
the publication/download association, not the physical source of a light.

## Camera identification: attribution versus evidence

The preserved 2020 video-index HTML's `NBC_Leaning_Cam` section, lines 257–270,
associates the view with CBS-Net Dub5 24 and CBS-Net Dub6 48. It attributes the
camera to NBC atop the GE Building at 30 Rockefeller Center, and calls the CBS
credit mistaken. Those are **the index author's assertions**, not findings
adopted in this unit. The section names no foreground upright or light device.
No precise scene triangulation has been performed.

The held NIST NCSTAR 1-9 PDF, printed pp. 261–264 (PDF pages 305–308), was read
as complete extracted text. Table 5-2 describes Camera2 as high on a building
near midtown Manhattan, due north of WTC7, with higher magnification than
Camera1. Figure 5-183's caption places Cameras1/2 approximately 5–7 km away.
These are NIST's stated camera attributes, not independently surveyed positions.
They neither name the foreground upright nor verify the specific Rockefeller
attribution. The extracted text does not establish the attribution on a raster
credit embedded in Figure 5-185; no new image was opened to read that credit.
The caption expressly says its intensity levels were adjusted.

Thus a collection/broadcast credit, camera operator, filming location, depicted
object and later hosting service are separate identities. Neither agreement
with a broad northward location nor a conflicting credit proves alteration,
concealment, an emitter or a cause of collapse.

## Concrete copy leads, not acquired counterparts

| Held source assertion | Exact lead | Current verified status |
|---|---|---|
| Older index, line 269 | CBS-Net Dub5 24; CBS-Net Dub6 48 | Alternate clip labels. The latter occurs in the held converted MOV name; a label does not prove native-byte identity. |
| Same section, line 265 | `bbc200109111736-1818?start=160` | Claimed BBC rebroadcast counterpart; not the held earlier `bbc200109111654-1736` access file. No corresponding footage was acquired or checked here. |
| Same section, line 265 | `nbc200109111651-1733` | Claimed pre-collapse view at varying zoom. Not an authenticated exact candidate-frame counterpart. |
| Same section, line 269 | Release25 `42A0122 - G25D33`, at `24:49` | Exact folder and eight names positively appear in held archived directory pages; candidate content and clock remain unverified. The time belongs to the leaning-camera entry, not the separately listed Window Shot. |
| Restored IC911 Building7 page, lines 734–739 | Same location/clip/DVD assertions | Restored/repeated index lineage, not a second independent source. |

The archived VIDEO_TS listing contains VIDEO_TS.BUP, VIDEO_TS.IFO, VIDEO_TS.VOB,
VTS_01_0.BUP, VTS_01_0.IFO and VTS_01_1/2/3.VOB. Root inspected the listing's
content and the reciprocal folder label, not DVD bytes. The preceding
[source locator](../release25-source-locator/report.md) and
[copy locator](../release25-copy-locator/report.md) preserve the failed file
requests and later rate-limit stop. Those searches were not rerun here, and
their past failures are not represented as fresh attempts or source absence.

## Finite local filename coverage

A read-only recursive inventory selected only `.mp4`, `.mov`, `.avi`, `.wmv`,
`.mpg`, `.mpeg`, `.vob`, `.ifo`, `.bup` and `.m4a` files within three roots:

- Main `research/wtc7-video-comparison/media`: nine files.
- Worktree `research/sherlock-wtc7-investigation/late-fire-catalog-join`: three files.
- Worktree `research/sherlock-wtc7-investigation/cbs-vms-content-check`: one file.

Case-insensitive basename patterns were `dub[ _-]*5[ _-]*24`,
`dub[ _-]*6[ _-]*48`, `bbc200109111736|BBC.*1736.*1818`, and
`42A0122|G25D33`. Only the known converted MOV matched (Dub6 48). None of the
other patterns matched those 13 basenames. This does not search embedded
archives, renamed media, video contents, all main/worktree holdings or the
Internet. In particular, compilations and other broadcast files can contain
unidentified excerpts despite different names. The alternate-media lane
separately inventories the named held kit; it must not be counted in these
13 files or silently inferred absent.

## Reproduction, pins and failures

Commands: `rg --files`, scoped `rg -n -i`, complete relevant `sed -n` sections,
`shasum -a 256`, `pdfinfo`, and stdout-only bundled Python3.12.14 using
`pathlib`, `csv`, `json`, `hashlib`, `re` and `pypdf`.
The CSV/inventory/hash assertions exited 0 with
`PASS_MAIN_ACQUISITION_WP0_WTC11_JOIN`. PDF locator output checked page heads/
tails for PDF pages 301–312, then extracted all text of pages 305–308. This is
text-only review, not validation of image/layout content or all 797 pages.

Two initial path queries used the wrong checkout for existing holdings and
reported missing directories. Correct absolute main/worktree locations were
then inspected. Those errors are not negative source evidence. `pdftotext`
was absent from PATH; its attempted extraction failed. The bundled pypdf
read-only fallback succeeded without changing the PDF. No authoring, render,
installation or re-export took place.

| Input (main unless marked worktree) | Bytes | SHA-256 |
|---|---:|---|
| video acquisition CSV | 5733 | `5f39f34f6ba978ff8e030c632ab49c54950faaaf2fb3654ccd5cdc14bdfee6dc` |
| video source CSV | 10158 | `6d3fe8322ee8c914500086d7add9f5886eb291e22ebf8456d17a0cb5b7fb5521` |
| WP0 inventory | 110958 | `a67e202166dce46842668e290d3bc9fdc50890420ef58f481c99fb75a5a4d7a1` |
| older source-index HTML | 66211 | `1d01d8ffce7358095c7aaf605d9f6dd91c69ab1eaa5440afb19ab2402dd33a2a` |
| NCSTAR 1-9 PDF | 52766002 | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` |
| worktree target-folder HTML | 28840 | `a47cfdcb90d146cbe72484067941cc800a9c2b6b0d74a0950c0f667184e85a4c` |
| worktree target-VIDEO_TS HTML | 30036 | `2925c7288b97935407d270c3045e56a960dcf2a8506dc1e32cafd4c8e0c94567` |
| worktree restored Building7 HTML | 549409 | `da33035e9e8ce9d95bca6d3697f9fe99e8625ad74fee3b2cd5164cef84794eaf` |

The main paths are `research/wtc7-video-comparison/{source-manifest.csv,
media/video-acquisition-manifest.csv,sources/911conspiracy-tv-7-WTC-2020-07-01.html}`,
`research/sherlock-wtc7-investigation/wp0/inventory.json`, and
`authority/nist/wtc7/ncstar-1-9.pdf`. Worktree HTMLs are under
`../release25-source-locator/sources/`, named `wayback-target-folder.html`,
`wayback-target-videots.html`, and `ic911-building7.html`.

## Evidentiary disposition

Acquisition and catalogue identities are established only as recorded above
(A at the document/byte layer). Rockefeller/NBC attribution remains a specific
secondary lead (C/D pending corroboration); exact light-source identity and
independent candidate-frame corroboration are not established (D). Even an
authenticated filming location would not, by itself, locate a light in depth.
No new cause ordering or finding about intent follows.
