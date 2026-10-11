# NBC candidate media acquisition

Both named public candidates were acquired on October 9, 2026, with byte counts
matching the fresh catalog metadata. The original downloads are preserved
unchanged. This resolves their local acquisition problem, not the origin of
Excerpt C's reported bang or a collapse mechanism.

| Source | Bytes | Encoded duration | Picture and sound streams |
| --- | ---: | ---: | --- |
| [collapse wtc.mpg](sources/collapse%20wtc.mpg) | 2,703,430 | 9.864 s | 320x240 MPEG-1 video; stereo 48 kHz MP2 audio |
| [wtc5.mpeg.mpg](sources/wtc5.mpeg.mpg) | 99,297,340 | 354.916667 s | 320x240 MPEG-1 video; stereo 48 kHz MP2 audio |

Durations and stream properties are ffprobe results, not authenticated filming
times. Both report average frame rate 30/1 and a separate r_frame_rate of 60/1;
the saved frame-selection timestamps avoid treating those labels as a verified
camera cadence. Decoded counts are 295 and 10,648 frames respectively.

The [manifest](manifest.json) records public source/download links, exact SHA-256
hashes, sizes, route limits and source lineage. The successful download links
were read from the public Drive pages; no credentials, sharing changes, or
temporary bearer links were used. The earlier connector-only failure is not
rewritten. A new connector attempt again returned only a reference, whereas
ordinary public downloads produced actual local bytes.

## Initial content screen

The [small contact sheet](inspection/small-contact.png) shows a collapse/dust
plume followed by a scene change to debris-covered escalators. The
[large contact sheet](inspection/large-contact.png) shows damaged interiors
and debris in all twelve selected frames. Neither set reproduces the three
checked C third-shot reference pictures. The
[observations](inspection/observations.json) identify those references and
the comparison limits.

This was twelve uniformly index-spaced frames per file, not a continuous visual
review or an exhaustive exclusion of a short matching scene. Neither filename
is sufficient building attribution. The existence of encoded audio is not proof
of an original camera soundtrack; no audio listening, event classification,
loudness comparison or acoustic timing test was performed here.

## Decoder and preservation checks

Both complete video/audio decode commands returned exit 0. The small file's
decode log is empty. The large file emitted **damaged texture, unavailable motion
vectors and corrupt decoded-frame warnings**. Exit 0 therefore does not certify
an error-free source. Contact extraction repeated those warnings and also noted
an unavailable accelerated color conversion; all diagnostics are retained.
No repair, transcoding or concealment was applied to the stored source files.

The first contact command failed on filter escaping; its diagnostic remains
separate from the corrected run. A preliminary wrong-directory probe also
failed before inspecting media. Neither failure is presented as a successful
source check. Metadata supplied no provider checksum, so matching catalog size
and repeatable local hashes do not establish complete historical authenticity.

## Reproducing the inspection

Use ffmpeg/ffprobe 7.1.1. From this directory, the probe and full-decode operations
for either source are:

```sh
ffprobe -v warning -show_format -show_streams -of json 'sources/collapse wtc.mpg'
ffmpeg -hide_banner -nostdin -v warning -i 'sources/collapse wtc.mpg' -map '0:v?' -map '0:a?' -f null -
ffprobe -v warning -select_streams v:0 -show_frames -show_entries frame=best_effort_timestamp_time -of json 'sources/collapse wtc.mpg'
```

Substitute `sources/wtc5.mpeg.mpg` for the second file. Keep each command's exit
status and stderr independently. The [sample map](inspection/sampling.json)
uses `round((N-1)*i/11)` for i=0 through 11 on the decoded video frame list.
Each sheet contains those twelve unchanged-size frames in row-major order.
For example, the exact small-file selection/filter is:

```text
select=eq(n\,0)+eq(n\,27)+eq(n\,53)+eq(n\,80)+eq(n\,107)+eq(n\,134)+eq(n\,160)+eq(n\,187)+eq(n\,214)+eq(n\,241)+eq(n\,267)+eq(n\,294),tile=4x3:nb_frames=12
```

Use that filter with `-frames:v 1 -fps_mode vfr -update 1` to generate a new
PNG at a nonexisting output path. The large-file indices are in the same
sample map. Color conversion is a viewing derivative, not calibration.

## Research and Git boundaries

The [prospective scope](PROTOCOL.md) and [manifest](manifest.json) govern this
small acquisition packet. Source videos and contact sheets are Git LFS objects;
metadata, diagnostics and notes are ordinary Git text. The destination branch
is `research/nbc-media-acquisition-2026-10-09` in the existing private
`roryscot/911` repository, based on an already-published commit. No merge to
main, parent-goal change, legal-record promotion, accepted Sherlock/Faraday
finding or substituted human review is included.

The next scientific step, if pursued, is a denser, prospectively specified
source-correspondence screen, followed by separate soundtrack provenance and
timing work. A visual match alone would not identify an explosive sound.
