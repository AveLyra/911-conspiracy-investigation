# Collected-steel video: complete source preserved, candidate chains still open

October 27, 2026. Steel B188/H005 in the active five-track original-record plan. This supplements the [earlier steel-photo study](https://github.com/AveLyra/911-conspiracy-investigation/blob/7fdee56fbc807ef5d7f5eeda85f7ad0b24935a33/investigation/broader-evidence/steel-photo-roots-2026-10-27/README.md); it does not change the FEMA/NIST attribution records or identify a WTC7 specimen.

**We acquired the complete current public archive file “WTC Tape 3.mov,” preserved its bytes, inspected its metadata and selected native frames, and repeated the video-frame count.** This provides an additional source for tracing steel inspection and labeling. No W14A/B or C12 attribution chain was completed.

## Source and preservation

[NIST's archive entry](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations) links the [Collected Steel repository](https://googledrive.nist.gov/folders/1mO5PPh1ZyZafGUtWrzqhiaDwzTqyEPG-). Its Video folder lists seven movies. This unit acquired only the smallest, [WTC Tape 3.mov](https://drive.google.com/file/d/1UkHot_5JcamIUEYnbtLSw8NgBdI7MeeY/view), ID **1UkHot_5JcamIUEYnbtLSw8NgBdI7MeeY**.

- Complete response: **468,978,020 bytes**, matching the catalog size.
- SHA-256: **a74ade3e8cbdf0df5976b67c60ee0a211937440e90d4a29bc211cdfc13057dcd**.
- [Acquisition date, source chain and qualifications](SOURCE.json).

The connector declined the movie because its size exceeded its 256MiB transfer limit. An ordinary anonymous public download, including the normal warning that Google could not virus-scan a file this large, succeeded. No sign-in, private browser cookie or restricted-access bypass was used. The earlier connector failure is preserved locally; it was a tooling limit, not evidence of removal or withholding.

The archive association identifies the current published entity. It does not establish an unbroken chain back to an original camera tape, recording date or physical specimen. Media originals and all derived frames/captures remain on the verified Intel store. They are not in this public package: NIST's repository notice warns that some media may have third-party copyrights, and no particular redistribution basis was established here. This package publishes original research notes, links, hashes, metadata and code.

## SV01–SV02 — What was actually tested

FFprobe reports a 640×480 Cinepak video stream, **2997/200 frames per second** (14.985), **426.993327 seconds** and **6,399 stored frame entries**. The full video count returned **6,399 decoded entries**, with empty warning output in that pass. Stereo 44.1kHz signed 16-bit big-endian PCM audio is described in metadata; audio content and synchronization were not inspected. [Metadata](FILE-METADATA.json) · [Decoded count](DECODED-FRAME-COUNT.json) · [Tool versions](TOOLS.json).

Sixteen native raster frames were extracted using `select='not(mod(n,450))+eq(n,3597)'`. [Their input indices, reported presentation timestamps and hashes](EXTRACTED-FRAMES.json) are preserved. Four were individually viewed in this unit: frames001,009,010 and016. Eight separate browser-preview positions were sampled earlier; they are a different display/derivative scope. No continuous visual census or audio review is claimed. Browser-seek labels and initial preview images must not be treated as exact native-frame or camera-event timestamps.

A matching stored/decoded count shows that this current video can be decoded to the reported number of entries. It does not prove that no original tape material was omitted, that frames are independent images, that the file was never edited, or that any building attribution is correct.

## SV03 — A directly visible preservation-related marking

Native input frame **3597**, extracted as frame009 at reported presentation time **240.04004s**, shows **“SAVE”** written on a steel member. Frame010 also shows the marking. The identifier preceding it was not confidently joined to an inventory entry in this unit; its original visual appearance is retained locally. We do not silently choose an M/N alias or transfer the N8 control identification from the previous study.

This is evidence of a visible marking in the published footage. Who wrote it, when, which retention instruction it reflected, what subsequently happened to the member and its original building remain unverified. It is not a signed preservation decision, custody receipt or WTC7 identification. Deformation, holes, separations and surface appearance visible in sampled frames do not determine a historical failure mechanism.

## SV04 — Keep the date fields and their meanings separate

| Object / field reported by the tools | Preserved value |
|---|---|
| Movie-format creation_time |2010-05-24T18:06:04.000000Z|
| Video-stream creation_time |2010-05-24T18:06:04.000000Z|
| Audio-stream creation_time |2010-05-24T18:06:07.000000Z|
| Drive catalog created_time |2019-11-26T06:39:26.268Z|
| Drive catalog modified_time |2019-11-26T06:39:26.268Z|

These observations are not interchangeable. Apple's primary specifications describe [movie-header creation time](https://developer.apple.com/documentation/quicktime-file-format/movie_header_atom/creation_time) and [track-header creation time](https://developer.apple.com/documentation/quicktime-file-format/track_header_atom/creation_time) as creation information for the corresponding atoms/headers, with a 1904 epoch and UTC preferred. The format definitions do not authenticate when this footage was filmed or explain how these particular values were produced. Stream tags are FFprobe observations here; raw atom byte offsets were not independently parsed.

The three-second difference between reported reported video/audio creation tags is **not a measured three-second audio delay**. No audio/event alignment test was performed. Conversion, packaging, copied tags or clock issues are untested possibilities; none is adopted as the explanation. Camera/tape logs and encoding/export records would discriminate between them. Do not count these different object fields as independent corroboration of wrongdoing.

## SV05 — Remaining original-record work

The January 30, 2002 W14A/B photographs 63–73 and January 21, 2002 C12a/b series 40–45 are not authenticated by this video acquisition. Preserve the earlier split precisely: W14B 63–67 and W14A 68–73; the combined range is only a locator convenience. The corresponding originals/indices, camera or negative provenance, intake/alias/coupon/transfer records, attribution worksheets and actual DOC-NIST-2013-001311 request/response remain needed. The prior field-attributed WTC7 versus later unidentified classifications remain unchanged and unresolved.

This unit's exact-identifier searches located the already known FOIA-log entry, not the substantive response. A targeted Miscellaneous Photos metadata search returned no result; folder-listing/pagination limits remain, so this is not an archive absence test. The other six videos, unsampled frames and audio are unreviewed. A source-native tape/catalog-to-specimen crosswalk is the next necessary join. The source and its limitations may strengthen or weaken a later attribution claim; no specific historical cause or concealment is established here.

## Reproduce and accountability

`python3 verify_source.py /path/to/movie.mov` hashes the entire provided entity and repeats the video-frame count using ffprobe. It performs no download and publishes no media. Use the source URL above and the pinned SHA-256 to distinguish this entity from a variant. Preserve any different entity separately rather than overwriting it.

CHECKLIST.json records the point-by-point scope, outcomes and open requirements. REPORT.diff is the final new-report addition against an empty predecessor; REPORT-REVISION.diff compares the final report with its preserved first draft. The first draft mistakenly called the combined63–73range W14A before giving the correct split; this was our drafting error, corrected to W14A/B, not a discrepancy in the underlying source. The earlier draft and its first-addition diff remain in drafts/. Older studies and source records are unchanged. Acquisition, manual reading, source integrity, historical authentication and publication are separate milestones. No private case records, personal mailbox access, third-party contact, new request, fee or private push is part of this unit. The five-track goal remains incomplete.
