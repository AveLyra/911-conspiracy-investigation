# Primary definitions for the counter test

Read 2026-10-04. Sources below are version-tagged FFmpeg n7.1 implementation
definitions, not a complete purchased-standard certification or evidence of
the software used to create these access copies. Local copies preserve the
complete retrieved UTF-8 text and license notices; exact equality to all three
captured responses was checked before analysis. No fetched code is executed.

- [timecode.c](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.1/libavutil/timecode.c):
  `av_timecode_get_smpte`, `av_timecode_make_smpte_tc_string2`, and
  `av_timecode_init_from_components` define component masks, DF bit and ordinal
  adjustment. `bcd2uint` returns zero on invalid BCD; our explicit validation
  preserves invalidity instead. Its initialization function also is not a
  forensic range/omitted-label validator.
- [timecode.h](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.1/libavutil/timecode.h):
  the SMPTE ST 314M reference and bit map accompany the API. Extra bits have
  profile-dependent labels; the field argument may be arbitrary/polarity-related.
  This test retains those bits by position instead of inventing camera state.
- [libavformat/dv.c](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.1/libavformat/dv.c):
  `dv_extract_timecode` reads `AV_RB32(pack+1)`, uses the profile's rate, suppresses
  DF interpretation for PAL and skips field expansion. The held 120,000-byte,
  720×480, DSF-zero profile is the distinct 525/60 case used here.
- Held [DV muxer source](../dv-metadata/sources/ffmpeg-n7.1-libavformat-dvenc.c)
  shows `dv_write_pack` generating the packed counter and setting additional
  bits. A well-formed counter can therefore be software-generated; that does
  not identify the actual historical workflow. Held
  [profile source](../dv-metadata/sources/ffmpeg-n7.1-libavcodec-dv_profile.c)
  supplies the nominal DV frame period. Its previously disclosed one-terminal-LF
  normalization is unchanged and pinned, not relabelled an exact upstream copy.

The raw GitHub header initially returned a web-tool cache error; permitted curl
retrieved the full file. The documentation-page text finder also missed a symbol
that is present in the full raw demuxer source. Neither failed lookup establishes
absence. Only generic public URLs were transmitted. Creation of the scoped
worktree directory needed filesystem approval before source preservation;
the first failed patch created no source file. Existing source evidence is intact.

This is strict component/range/DF arithmetic validation. Subcode SSYB validity,
camera synchronization, original tape custody, dates/time zones and edit/export
mapping are not authenticated by it. The previous byte audit supplies input
integrity, not a new independent clock. A single continuous sequence could be
either original or regenerated; the test must retain that non-identifiability.
