# Independent source/claim review

2026-09-20 UTC. Text/metadata only; no new external call, media acquisition,
playback, image display, or execution of retrieved scripts. Only this note is
edited. Main authority, charter and initial protocol pins were rechecked in
`publisher-search.md`; the prospective six-open root extension was read fully.
This is research review, not historical authentication, legal promotion,
human acceptance, or an exhaustive public-source search.

## Initial review through the target-folder page

The source chain has advanced beyond my earlier publisher-lane retrieval gap:
the saved archived catalog actually lists the exact target folder. It does
**not** yet prove that any particular constituent file contains Window Shot,
is an original camera recording, or is a continuous/unedited chronology.
Constituent-file traversal and the eventual root report remain pending at
this review stage; this is not a final negative finding.

### Checks performed

- Independently computed byte counts and SHA-256 for the eight source files
  below. Parsed oEmbed JSON directly and the first/only assignments of
  `ytInitialPlayerResponse` and `ytInitialData` with Python's JSON decoder,
  not JavaScript evaluation. Asserted the oEmbed embed URL's video ID, player
  ID, title, author, and declared 430-second length. Title and author agree
  across both responses. Player `shortDescription` and the attributed
  description under `videoSecondaryInfoRenderer` match exactly (303 characters).
- Host metadata has ID `tZlENw_xuXU`, title `WTC7 9/11 Footage, NIST video
  enhanced`, author `WTC911demolition`, playability `OK`, non-live status,
  and matching upload/publish values `2014-09-26T23:44:01-07:00`. These establish
  what the host metadata says, not measured runtime, successful playback,
  original resolution, capture time, source ownership, or original-DVD identity.
- Parsed both IC911 HTML bodies for relevant text and all href-bearing
  anchors (372 Building 7; 156 Point 8). Building 7 line 878 links the exact
  YouTube ID. The separate leaning-shot entry has `24:49`; Window Shot does
  not. Full target naming includes both identifiers; the live index uses an
  en dash while the preserved old index/catalog uses a hyphen.
- Point 8 line 963's actual href is the archived SFolder link, not its
  displayed direct 911datasets URL. It describes the **other** folder
  `42A0120 - G25D31`; its quoted 3.82-GB size must not be transferred.
- Independently inspected all non-script/style text and extracted anchors
  of the four saved wiki pages through `wayback-target-folder.html`. The
  other-folder VIDEO_TS page line 81 points to parent `AWBCBPAERAX5G6AGBT7WTRV7WCXVEHHG`;
  that parent line 81 points to Release 25 `KRK27BSPI3B2VATLZYYTUCLZQBRVLP4I`.
  Release-page line 111 lists target `42A0122 - G25D33` as
  `5D64ZEBE7BYMSXL3KVSMELPWEKMNUKGE`. Its body confirms the full path and
  reciprocal Release 25 parent, and line 111 lists VIDEO_TS child
  `V2PCNLNHLTN5SBZOC5CA5HX2IF7HQ5CT`.
- Programmatic assertions passed: Release 25 contains 59 unique full folder
  labels and 59 unique SFolder IDs, with G25D integers exactly 1–59, plus
  `7Clips.zip` (SFile `YBENHJ4ONIRBOD5TWJN4I3MWWPMUF5LN`). Five 42A prefixes
  repeat across distinct G25D labels: 42A0118, 42A0125, 42A0128, 42A0131,
  42A0141. A 42A prefix alone is not a unique key. This is a count of this
  returned listing, not proof of an exhaustive original production.

### Active claim limits / corrections to preserve

1. The uploader admits color/resolution processing and describes replay,
   fast-forward and rewind material. The attribution of earlier replay-loop
   editing to NIST is explicitly qualified by “it seems.” Preserve it as an
   uploader allegation, not an agency editing finding. No constituent
   filename, checksum, release receipt, or new independent source is supplied;
   the description points back to the old index. The strongest alternative
   is a processed derivative whose earlier editing history remains unknown.
2. The wiki is direct evidence of its archived catalog assertions, not direct
   evidence of camera origin, NIST production authenticity, footage content,
   source-clock identity, causation, temperature, or continuity. Its footer's
   Public Domain notice does not establish rights in linked recordings.
3. Preserve actual archived hrefs: obtained pages expose differing capture
   timestamps/host forms (`20170424205404`, `20170424115907`,
   `20170424103806`, `20170424115904`; with/without `www`). Their IDs and paths
   join, but a common original request timestamp must not be substituted for
   all returned-page link contexts. Saved bodies alone do not independently
   verify root's reported transport flags, curl status, effective URLs, or
   HTTP redirect chain.

No material contradiction was found between the checked sources and the
initial `root-search.md` interpretation (SHA-256
`dcba9cf24b7e510d967f0ec5e52279ffc1d8b53f5a53361d60e7dd966862e982`).
That ledger snapshot still marked open 10 pending; later pages were examined
as subsequently supplied sources, not silently attributed to that version.

## Independently computed source pins

All paths below are under this unit's `sources/`.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| youtube-oembed.json | 817 | `d73e1a0d4a99791386b5c1f1c5a4e5c61a16da5e022d50e9e5bfb7ca16c0a462` |
| youtube-watch.html | 1189397 | `e6944e7146ef30ac0fb1ca09306c7caddb2e94aa8488b1f76bc819c1283931b6` |
| ic911-building7.html | 549409 | `da33035e9e8ce9d95bca6d3697f9fe99e8625ad74fee3b2cd5164cef84794eaf` |
| ic911-wtc7-8.html | 498149 | `dd8c4444fac75104381d469660655c5595b119b8f6d09ab1bc37d8e1cc9cf857` |
| wayback-other-folder.html | 29819 | `8dd8759c036a557a7cc544586fd0c563cd26faa0aa9f37bc8f6078ac552d908a` |
| wayback-other-parent.html | 28840 | `0a9a25590d70909d463c0fb32e5ff77f3d18aefdb684f25607ba77a2cd645bf9` |
| wayback-release25.html | 39921 | `2edad9b809fb14cfd2627255cd3e4012e468336e08a9a89defc8a8d0137612ea` |
| wayback-target-folder.html | 28840 | `a47cfdcb90d146cbe72484067941cc800a9c2b6b0d74a0950c0f667184e85a4c` |

Reproducible local method: `wc -c sources/*`, `shasum -a 256 sources/*`,
Python standard-library `HTMLParser` (omit script/style text; retain href,
anchor text and `getpos()` line), and `json.JSONDecoder().raw_decode` after
the two named assignment markers. Match full folder labels with
`42A\d+ - G25D\d+`, then compare ID/name sets and G25D integer sequence.
The described parser/assertion runs returned exit 0. Source scripts were
not executed, and no network verification was repeated.

## Follow-up: target VIDEO_TS listing

The subsequently saved `sources/wayback-target-videots.html` is 30036 bytes,
SHA-256 `2925c7288b97935407d270c3045e56a960dcf2a8506dc1e32cafd4c8e0c94567`.
I parsed all non-script/style text and all 97 anchors, then asserted uniqueness
of all eight listed file names and eight corresponding SFile links. The body
gives the exact target path ending `42A0122 - G25D33/VIDEO_TS` and reciprocal
parent `5D64ZEBE7BYMSXL3KVSMELPWEKMNUKGE`. All eight file anchors are on local
line 112 with prefix
`/web/20170424205354/http://www.911datasets.org/index.php/SFile:`.

| Filename | SFile ID |
| --- | --- |
| VIDEO_TS.BUP | `YNBS65YTR5ZNON6BPO3BIMP4YZMQRR5I` |
| VIDEO_TS.IFO | `F6O5LQX7QTAZD5IY43MXQQUL3JGPULSQ` |
| VIDEO_TS.VOB | `UEKD5I4ACLGEA7WCMZZHANNNFZSOSMAZ` |
| VTS_01_0.BUP | `TESMB6BJGI3G5MOZUYR5TKNFWELX66LR` |
| VTS_01_0.IFO | `4XUJGX4GL474RXJ3HXOBIYKBKG4AO5J2` |
| VTS_01_1.VOB | `W3UYIIVYDLXD7AUBDCPMEYX7L74N6JRY` |
| VTS_01_2.VOB | `B5F6OLNOMMZPUDDARF3QIT62BCVZJXAC` |
| VTS_01_3.VOB | `GNKALFTXU3LVPSPQVRM3GALVZ6FCMDQC` |

This establishes actual catalog names under the literal target, not a
current direct media URL, bytes acquired, a media checksum independently
computed, or assignment of Window Shot to a particular VOB. The neighboring
VIDEO_TS directory contains nine names, including `VTS_01_4.VOB`; do not copy
that ninth file or its quoted size into the target inventory. Individual
file-page metadata and final report checks remain pending.

## Final catalog/source audit at reviewed report version

The traversal stage is now complete within the declared allowance. I read
the complete report and final root ledger, then independently compared their
material joins against the saved sources. Review pins:

- `report.md`: `7c026044d3c3b6a8b97683d938561efa45accdb70fc5970332611475ea3dac9f`.
- `root-search.md`: `3fb40b20210517da6fbf329ecc4adb06eef7720c174ea3ac882983e3c1aa827a`.
- Extended `PROTOCOL.md`: `4d87433c6d18259edc2b6ef47000614e4270108bfbb19f38bfb60ce3097b5df3`.

The final local assertion run (exit 0) rebuilt the eight filename/ID pairs
from the target directory's HTML anchors and compared the complete mapping
with the report's table: exact match. It independently resolved the actual
footnote href, four subsequent directory hrefs, and all three VOB-detail
hrefs with `urllib.parse.urljoin`, asserting that each exact URL appears in
the root ledger. It also recomputed all nine saved source sizes and SHA-256
values and confirmed each against that ledger. No ninth target file, copied
neighboring-folder size, guessed ID, fabricated media checksum, or reassigned
24:49 marker was found.

The ledgers reconcile to ten queries and 24 opens: root six/16 and publisher
four/eight, with six plus three reported failures. Nine root bodies are saved;
the extra successful root response was parsed web text. This is a ledger and
saved-source reconciliation, not a replay of root's external requests.
The three VOB-detail failures have no preserved response bodies; their exit
56 / reported HTTP 404 disposition remains dependent on root's recorded
execution account. No failure is upgraded to proof of an origin-server status,
missing media, withholding, or a globally exhausted archive. No listed DVD
bytes, sizes, content hashes, codec, playback order or duration were verified.

**Disposition:** no remaining material source/claim contradiction was found
within this text/metadata-only scope. The report correctly distinguishes a
located publisher inventory from acquired or content-matched footage and
does not adopt the uploader's tentative NIST-editing allegation. Its claims
about the restored index's dependence are also consistent with the prior
publisher-page review, not a new independent historical account. A correct
catalog could still describe copied, edited, differently sourced or
misidentified material; only source-file comparison and independent production
records can discriminate those alternatives.

Root announced a later clarification of its closing Luna-status sentence;
that change is not silently included in the report pin above. Later report
versions and forthcoming `validation.md` require their own version check.
No unrun mechanical validator, human/scientific acceptance, or new visual
review is claimed here. All original review entries remain preserved.

## Current-version disposition

Re-read the entire current `report.md`, 8232 bytes, SHA-256
`368334e0c23da89b0aa428693d67e2f8b90875fa5775675aedcf19f58d512b3e`,
and the available `validation.md`, 2767 bytes, SHA-256
`244ebd2f8ab057fcb0e942e14b569bfd6ece796f8b3c1527d7aaeb8667bf5729`.
The report's sole change from the previously reviewed version was verified,
not assumed: replacing its current phrase `Full goal and Luna follow-through
remain` with the prior phrase `Full goal and review of located Luna work
remain` reproduces the exact prior SHA-256 `7c026044…` recorded above.
That clarification leaves the source analysis unchanged and avoids implying
that a completed bounded Luna audit itself is unfinished.

No remaining material inconsistency was found in this version within the
declared text/metadata scope. The eight-file mapping, observed route chain,
source pins, differentiated time claims, processing disclosure and source
limitations remain as independently checked above. Historical content,
original-camera/DVD authenticity, media availability, and cause ranking
remain unverified; the text does not claim otherwise.

The inspected validation version explicitly left its final navigation/link/
whitespace rerun pending. I did not run or independently attest the reported
record-spine validator or root transport diagnostics, and do not import
forthcoming checks as passes. Later validation additions are not covered by
its pin here. This review is independent parsing and critical source/text
comparison, not an independent historical viewing or human/expert acceptance.
