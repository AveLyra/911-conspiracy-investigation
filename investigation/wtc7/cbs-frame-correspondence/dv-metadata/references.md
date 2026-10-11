# Primary format references and inference limits

Read2026-10-04. Four version-tagged FFmpeg n7.1 source files are preserved in
`sources/` with their original license notices. The pre-execution freeze records
their bytes/hashes. These implementation sources establish a specific supported
layout and possible rewriting behavior, not a complete standards certification
or the software used in the historical acquisition chain.

Capture check: three saved files exactly equal the complete retrieved text.
The saved `dv_profile.c` is the complete code/notice text minus one terminal
empty-line LF (13428 versus13429 characters). Exact prefix equality and this
one-byte difference were checked; two attempted EOF-blank-line patches did not
restore that byte. Its frozen hash identifies this disclosed local derivative,
not a byte-identical upstream response. No format definition changed.

| Primary source | Inspected portion and use |
| --- | --- |
| [libavcodec/dv.h](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.1/libavcodec/dv.h) | DV section and pack-type enums; timecode0x13, audio date/time0x52/53, video date/time0x62/63. |
| [libavcodec/dv_profile.c](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.1/libavcodec/dv_profile.c) | First `dv_profiles` entry:120000 bytes,10 sequences,1 channel,720x480 and nominal1001/30000 frame period. The existing AVI time bases are separate and are not overwritten. |
| [libavcodec/dvenc.c](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.1/libavcodec/dvenc.c) | `dv_write_dif_id`, `dv_write_ssyb_id`, `dv_format_frame`:150 DIF blocks/sequence,80 bytes/block; header,2 subcode,3 VAUX,9 groups of audio plus15 video. Preserve SSYB IDs without treating this generator's numbering as a universal validity rule. |
| [libavformat/dvenc.c](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.1/libavformat/dvenc.c) | `dv_write_pack`, `dv_inject_audio`, `dv_inject_metadata`, `dv_assemble_frame`, `dv_init_mux`:pack offsets; the muxer can write new timecode and recording dates from creation metadata into copied frames. Its written original-mode flag does not authenticate original camera provenance. |

The [MediaArea temporal-metadata case study](https://mediaarea.net/DVAnalyzer/dv-metadata)
also documents a compilation workflow retaining camera metadata and explains
that rendering can instead lose it. Thus editing does not invariably remove
these fields; their absence does not prove deliberate deletion. This is an
illustrative workflow, not an identification of how the held files were made.

The first inventory deliberately does **not** interpret recording calendars,
time zones, date-century pivots, unknown components, transmitting/source-control
flags, drop-frame arithmetic or edit-point semantics. All660 five-byte slots
per frame and the surrounding retained controls remain available for a separately
verified interpretation. A matching first byte is a raw candidate, not a usable
clock. No first/majority-value selection, timestamp interpolation or timecode
continuity is used to authenticate recording history.

The metadata layout preserves9570 bytes/frame: ten copies of480 initial control
bytes plus nine groups of8 audio control bytes and45 video-ID bytes. Adding the
saved frame-chunk offset to a slot's frame-relative offset reproduces its source
position. The caller establishes complete frame extent; the extractor cannot
detect missing bytes confined to picture regions it deliberately does not read.

Public retrieval sent only generic source URLs, not case data. Initial shell
DNS resolution failed; the permitted network route retrieved the tagged source
text. A web attempt at a tagged MediaInfo source returned an internal error;
no missing-source or format conclusion is drawn from that failure. No external
decoder was installed or executed. The separate method review's movable-master
MediaInfo observations are cautions, not dependencies of this raw extractor.
