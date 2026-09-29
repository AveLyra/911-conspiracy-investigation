# Root search ledger — Release25 literal locator

Research only. Retrieval date: September 20, 2026 UTC. Read with PROTOCOL.md.
The six queries below exhausted the root query allowance. Results were returned
in batches; a result is not assigned to an individual query where the tool did
not expose that association. Search snippets are leads, not inspected recordings.

## Queries (6/6)

First batch:

1. `"42A0122" "G25D33"`
2. `"tZlENw_xuXU"`
3. `"Release 25" "NIST" video`

Returned relevant leads included the current IC911 Building 7 collection
<https://ic911.org/building-7-collapse/> and South Tower collection
<https://ic911.org/south-tower-collapse/>. Both mention the target folder;
neither search result supplies an actual directory listing. Other results
identified different folders, including 42A0108–G25D18, 42A0119–G25D3 and
42A0120–G25D31. Those were not silently substituted for the target folder.

A secondary page about the last of those different folders mentioned
`Copy of Video_List.mdb`:
<https://baracuteycubano.blogspot.com/2018/09/video-de-mark-lagangacbs-news-con.html>.
The page was not opened; the filename is only a search-result lead.
Another result was <https://www.consensus911.org/point-wtc7-8/>; the publisher
lane handles its release-navigation context separately.

A public discussion supplied observed, but not yet inspected, Archive links:
<https://www.reddit.com/r/911archive/comments/1t4mcyh/where_can_i_find_an_uncompressed_version_of/>
→ <https://archive.org/details/vts-01-1_20260507>,
<https://archive.org/details/@alan-smithee?query=nist>,
<https://archive.org/details/abc-dub-1-30> and
<https://archive.org/details/cbs-net-dub-1-03>.
These are other-item/navigation leads, not a demonstrated target match. No
technical claim in that discussion is accepted as established by its posting.

Second batch:

4. `"42A0122"`
5. `"G25D33" site:archive.org`

Returned substantially the same IC911 leads and an irrelevant identifier
collision. No exact Archive item was identified by this batch. This is not
an exhaustive absence finding.

Final query:

6. `G25D33 NIST video download`

Returned unrelated NIST digital-video/TRECVID material. The results appear
to relax the literal identifier; none was opened. No inference about the
existence of the release follows from that result.

## Page/metadata attempts (running ledger)

1. Web open <https://www.youtube.com/watch?v=tZlENw_xuXU> failed with internal
   fetch error. It did not establish deletion or unavailability of the video.
2. Web open YouTube oEmbed endpoint, with that exact watch URL and
   `format=json`, failed with cache-miss/internal error.
3. Web open <https://ic911.org/building-7-collapse/> returned its text. Relevant
   entries repeat the old index: the leaning shot gets the 24:49 marker;
   the window shot does not. The publisher lane independently checks the
   archive's declared derivation, not the recording itself.
4. Anonymous curl of
   `https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DtZlENw_xuXU&format=json`
   succeeded (exit 0): `sources/youtube-oembed.json`, 817 bytes,
   SHA-256 `d73e1a0d4a99791386b5c1f1c5a4e5c61a16da5e022d50e9e5bfb7ca16c0a462`.
   Host metadata gives title `WTC7 9/11 Footage, NIST video enhanced` and
   uploader `WTC911demolition`. Neither title nor uploader authenticates the
   source; the word “enhanced” raises a processing-history question.
5. Anonymous curl of the IC911 page succeeded (exit 0), preserving
   `sources/ic911-building7.html`, 549409 bytes,
   SHA-256 `da33035e9e8ce9d95bca6d3697f9fe99e8625ad74fee3b2cd5164cef84794eaf`.
6. Anonymous curl of the exact YouTube watch page succeeded (exit 0). The
   captured HTML is omitted from this public copy because it contains embedded
   Google client-key material; original size and SHA-256 are preserved in
   `sources/youtube-watch-source-note.md`. Metadata inspection only; no media
   download or playback. A local Python
   `json.JSONDecoder().raw_decode` of the first `ytInitialPlayerResponse`
   assignment found ID `tZlENw_xuXU`, the same title/author as oEmbed,
   `lengthSeconds: "430"`, `isLiveContent: false`, and playability status
   `OK`. Its microformat publish date was `2014-09-26T23:44:01-07:00`.
   This is host-declared duration/date, not a measured running time or
   historical capture time. The page's `ytInitialData` attributed-description
   text agrees with the player's description.

   The uploader describes excerpts from a NIST DVD, acknowledges their own
   color/resolution changes, reports replay/fast-forward/rewind content and
   tentatively attributes prior replay-loop editing to NIST investigators.
   That attribution is expressly uncertain in the description and is not
   adopted here. The description points back to the same old video index;
   it supplies no constituent source filename, folder hash or release receipt.
   Acknowledged processing makes this a locator lead, not a calibrated color,
   continuous-duration or speed reference. No content match was performed.
7. Anonymous curl of
   `https://ic911.org/consensus-panel/consensus-points/point-wtc7-8/`
   succeeded (exit 0), preserving `sources/ic911-wtc7-8.html`, 498149 bytes,
   SHA-256 `dd8c4444fac75104381d469660655c5595b119b8f6d09ab1bc37d8e1cc9cf857`.
   HTMLParser found 156 href-bearing anchors; the SFolder anchor's actual
   href was
   `https://web.archive.org/web/20170424205404/http:/911datasets.org/index.php/SFolder:3IAGVZVIFRCYCZVEEMC4QG2NSIE3UGAF`.
   Its differently named folder is release-navigation context only.
8. Web open of that exact Wayback href failed as inaccessible via the tool.
9. Anonymous curl of the same href succeeded (exit 0), preserving
   `sources/wayback-other-folder.html`, 29819 bytes,
   SHA-256 `8dd8759c036a557a7cc544586fd0c563cd26faa0aa9f37bc8f6078ac552d908a`.
   The archived wiki body identifies the different folder's VIDEO_TS directory
   under Release_25/Release 25/42A0120 - G25D31, with DVD filenames and parent
   `SFolder:AWBCBPAERAX5G6AGBT7WTRV7WCXVEHHG`. This is actual catalog content,
   but not yet the target inventory. All non-script/style text and hrefs in
   this 29819-byte snapshot were inspected locally. No torrent was fetched
   or used, despite the wiki's folder-category label referring to BitTorrent.
10. Anonymous curl of its observed parent href,
    `https://web.archive.org/web/20170424205404/http://911datasets.org/index.php/SFolder:AWBCBPAERAX5G6AGBT7WTRV7WCXVEHHG`,
    succeeded (exit 0): `sources/wayback-other-parent.html`, 28840 bytes,
    SHA-256 `0a9a25590d70909d463c0fb32e5ff77f3d18aefdb684f25607ba77a2cd645bf9`.
    All non-script/style body text was inspected. It names the neighboring
    folder and links Release 25 at
    `https://web.archive.org/web/20170424115907/http://www.911datasets.org/index.php/SFolder:KRK27BSPI3B2VATLZYYTUCLZQBRVLP4I`.
    The changed capture timestamp/hostname is from its actual href; it was
    not a guessed target identifier. Curl followed HTTPS redirects, but no
    final-response header/URL receipt was saved for these ten attempts.
11. Following the prospectively declared extension, anonymous curl of the
    exact Release 25 href in row10 succeeded (exit 0):
    `sources/wayback-release25.html`, 39921 bytes,
    SHA-256 `2edad9b809fb14cfd2627255cd3e4012e468336e08a9a89defc8a8d0137612ea`.
    The full non-script/style text lists59 named DVD folders and `7Clips.zip`.
    Exact target label `42A0122 - G25D33` links
    `https://web.archive.org/web/20170424103806/http://www.911datasets.org/index.php/SFolder:5D64ZEBE7BYMSXL3KVSMELPWEKMNUKGE`.
    Repeated42A prefixes elsewhere show why both parts of the folder label
    matter; this count is the saved directory, not an authenticated NIST
    production completeness finding.
12. Anonymous curl of that observed exact target href succeeded (exit 0):
    `sources/wayback-target-folder.html`, 28840 bytes,
    SHA-256 `a47cfdcb90d146cbe72484067941cc800a9c2b6b0d74a0950c0f667184e85a4c`.
    The complete non-script/style text names the target's full path and
    links its VIDEO_TS directory at
    `https://web.archive.org/web/20170424115904/http://www.911datasets.org/index.php/SFolder:V2PCNLNHLTN5SBZOC5CA5HX2IF7HQ5CT`.
13. Anonymous curl of that exact VIDEO_TS href succeeded (exit 0):
    `sources/wayback-target-videots.html`, 30036 bytes,
    SHA-256 `2925c7288b97935407d270c3045e56a960dcf2a8506dc1e32cafd4c8e0c94567`.
    Its complete non-script/style text lists eight constituent filenames;
    see report.md for the exact filename/identifier crosswalk. The three
    title-segment entries expose the URLs requested in rows14–16 below.
14. Anonymous curl of
    `https://web.archive.org/web/20170424205354/http://www.911datasets.org/index.php/SFile:W3UYIIVYDLXD7AUBDCPMEYX7L74N6JRY`
    (listed `VTS_01_1.VOB`) failed, exit56, reporting HTTP404. No response
    body, size or content checksum was obtained.
15. Anonymous curl of
    `https://web.archive.org/web/20170424205354/http://www.911datasets.org/index.php/SFile:B5F6OLNOMMZPUDDARF3QIT62BCVZJXAC`
    (listed `VTS_01_2.VOB`) failed, exit56, reporting HTTP404. Same limit.
16. Anonymous curl of
    `https://web.archive.org/web/20170424205354/http://www.911datasets.org/index.php/SFile:GNKALFTXU3LVPSPQVRM3GALVZ6FCMDQC`
    (listed `VTS_01_3.VOB`) failed, exit56, reporting HTTP404. Same limit.

Rows14–16 ran in parallel, all within the declared extension. Their failed
routes do not establish absence of the source files, of other archived
captures, or of current public copies. No fabricated metadata values or
inferred byte sizes replace these missing file-detail records.

Transport for successful curl routes disabled user curl configuration and
used HTTPS-only redirects, a 25-second timeout and a fixed byte ceiling.
No login, account content, private case payload, upload or outreach was used.
No retrieved instruction is treated as task authority.

Final root count: **6 queries / 16 page-or-metadata attempts**.
Initial root page allowance exhausted. PROTOCOL.md now prospectively allows
six more observed catalog-link opens, justified by this actual directory chain.
Each failed or repeated transport route counts. No additional query or media
download is covered by that extension. No metadata opens remain in this unit.
Root had six failed routes (1,2,8,14,15,16) and ten successful page/metadata
responses (one parsed web response plus nine saved source bodies). Publisher
lane coverage is separate: four queries/eight opens, three failed. Combined
unit coverage: ten queries/24 opens, nine failed. No new media was downloaded,
decoded, displayed or played in either lane.
