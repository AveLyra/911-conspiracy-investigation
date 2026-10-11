# Header and arithmetic method references

Read before the eight-file header collection, 2026-10-04. These are public
technical definitions, not evidence authenticating the historical recordings.

- [Microsoft AVIStreamHeader](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/api/avifmt/ns-avifmt-avistreamheader)
  supplies the field order and semantics: video `dwRate/dwScale` is samples per
  second, `dwLength` is stream length in its units, and `dwStart` is a start delay.
  Collector compares scale/rate/start/length with saved probe output and requires
  zero start before conditional source-label gap calculations. No new probe is
  run. Retrieved page contained the specification body despite an access notice.
- [FFmpeg 7.1 timecode.c](https://ffmpeg.org/doxygen/7.1/timecode_8c_source.html)
  component initialization, lines232–249, supplies the nominal-frame minus
  dropped-label arithmetic: for nominal30, subtract two labels for each elapsed
  minute except each tenth minute. String parsing at lines253–265 is a different
  interface requiring initial colon separators; this investigation does **not**
  claim it parses the all-semicolon native text. Strict ASCII syntax, ranges and
  rejection of omitted labels are our explicit parser rules. No FFmpeg
  installation or invocation is performed by this unit; this is a reading of published source,
  not an exact-source pin to the local7.1.1 binary. Initial www and raw-GitHub
  source retrievals failed; the non-www documentation above returned source.
- The [previous field-semantics review](../lineage-142/report.md) and its
  [documentary review](../lineage-142/documentary-review.md) record the
  Adobe XMP Part3 RIFF mapping (`tc_O`, `tc_A`, `rn_O`, `rn_A`) and mirror/edition
  limitations. No inference of original-camera authorship, integrity or elapsed
  historical time follows from the mappings.

Source pages were read through the browsing tool. Their live remote contents
are not byte-pinned by this file; freezing this note pins our declared method
and citations, not a preserved external publication. No case-sensitive payload
was sent to a service for these format lookups.
