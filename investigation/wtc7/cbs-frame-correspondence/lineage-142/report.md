# Figure 5-142 lineage check finds an embedded tape and timecode lead

2026-10-04. **The held Clip 7 AVI contains a tape-name field reading
`Vince Demetri CBS` and start-timecode text `00;03;12;26`.** These were not
exposed by the ordinary video probe or saved catalogue response. This narrows
the next source search; it does not authenticate the original tape, establish
wall-clock time, select an exact source exposure, or reconstruct NIST's image
processing. The full investigation remains active and research-only.

## What the held bytes establish

The [complete metadata inventory](metadata.json) records the three unchanged
source hashes, probe output, 24 RIFF headers, 866 retained metadata payload
bytes, JPEG header metadata and selected PDF metadata. The following text is
the prefix **before the first NUL byte**, not the entirety of each field.
The complete payloads, including uninterpreted binary tails, are preserved in
the inventory. Offsets are zero-based file byte positions.

| AVI field | Payload offset | Stored text prefix | Scoped interpretation |
| --- | ---: | --- | --- |
| `Tdat/tc_O` | 140334520 | `00;03;12;26` | Start-timecode value, subject to the qualifications below. |
| `Tdat/tc_A` | 140334546 | `00;03;12;26` | Alternate-timecode value; repetition is not independent corroboration. |
| `Tdat/rn_O` | 140334572 | `Vince Demetri CBS` | Tape-name metadata, not authenticated camera custody. |
| `Tdat/rn_A` | 140334620 | `Vince Demetri CBS` | Alternate tape-name metadata. |
| `Cdat/cmnt` | 140334680 | Describes window flames/smoke, falling debris and a corner chunk. | An unattributed embedded description, not a second witness or new physical observation. |

Adobe's *XMP Specification Part 3*, 2020, section 2.3.2.1/Table 22 maps these
four `Tdat` tags to start/alternate timecode and tape/alternate-tape name.
The next page states that native values use UTF-8 and this AVI metadata lacks
a native-change digest. This supports field interpretation, not the truth or
date of the stored values. [Adobe-authored specification, mirrored copy,
printed pages 55–56](https://dl.photoprism.app/pdf/specifications/20120101-Adobe_XMP_Specification_Part_3.pdf).

The mapping was checked in the full extracted document text. Adobe's
[official specifications page](https://developer.adobe.com/xmp/docs/xmp-specifications/)
links its own repository copy, but the browser retrieval of that raw PDF failed
on its content type; a legacy Adobe URL was also inaccessible. The mirror's
filename contains 2012, whereas the inspected document identifies 2020. A
screenshot request did not provide a complete two-page visual check. No claim
of byte identity between mirror and Adobe-hosted copies is made.

The fields are editable metadata in an access copy. The binary tails are not
interpreted, and the prefixes are not converted to frame numbers, elapsed
seconds or local time. No drop-frame/rate convention, original recording date,
camera clock, uninterrupted tape cadence or edit-list linkage is established.
In particular, `00;03;12;26` is **not** an independently measured time of day.
It is a useful retrieval key even while those questions remain unresolved.

## The report image and publication metadata

Physical PDF page 272, resource `/Im0`, resolves to object 2850/0. It is a
706×457 `/DCTDecode` image. Both root and the separate checker verified that
the raw encoded stream is exactly the held 151488-byte JPEG, SHA256
`68c9d384ac3b1099361f255f80a74d387073d67500089099765f4f0cf030215a`.
This independently confirms the PDF-to-JPEG extraction, not camera-to-report
provenance.

Pillow's inspected JPEG header has an Adobe APP14 marker and no EXIF entries.
No original tape/frame/export recipe appears in that inspected header. This
is not a complete post-scan JPEG forensic search or proof that no relevant
sidecar, project or original still exists. The selected PDF image dictionary
does not contain its own metadata pointer.

The PDF document info/XMP identifies a Word-derived title, PScript5.dll and
Acrobat Distiller, with creation/modification fields in 2009/2011. Those are
document-level metadata, not the date of the video exposure or proof of a
particular adjustment to the figure. No broader PDF-object or revision-history
scan was performed. Publication software and intensity adjustment are not
evidence of fabrication by themselves.

## Source context and the strongest alternative

The [documentary review](documentary-review.md) checks the saved catalogue
chain and original report context. The catalogue exposes the held object and
folder labels but does not supply the original tape-to-still edit chain.
Requested fields omitted by the connector remain unknown at the provider;
2019 catalogue timestamps are not 2001 recording times.

The [page 271 text](../../fire-coverage-batch3/assets/run01/context/P-ebeb74127e68.txt)
attributes Figure 5-142 to a clip roughly two minutes after Figure 5-141 and
says some window flames described from the moving clip are not readily
apparent in the still. The [page 272 caption and discussion](../../fire-coverage-batch3/assets/run01/context/P-8338c00a97d8.txt)
disclose adjusted intensities and added architectural labels. They also
explicitly leave a lower plume unresolved between transported smoke and a
fire on Floors 5–6. These are source claims and admissions of uncertainty,
not newly verified fire/window states.

The strongest ordinary explanation for the incomplete bridge is a publication
workflow that produced an adjusted/annotated still while the later access-copy
catalogue retained only some production metadata. The recovered tape/timecode
fields make that a more specific possibility; they do not verify the workflow.
A retained original or export project might show faithful processing, material
alteration, or a different exposure. No such outcome is assumed here.

## Evidence assessment and next test

| Claim | Layer and strength | What would materially change it |
| --- | --- | --- |
| The held AVI contains the listed field prefixes at the listed offsets. | Observed bytes, A for this acquired copy; two direct checks agree. | A wrong file/hash, offset, header or transcription would overturn it. |
| The fields function as tape-name and timecode metadata. | Source-supported interpretation, B; published mapping matches the field names. | A contrary applicable format/version definition or source-project interpretation. |
| These identify an authentic original recording clock and the exact Figure 5-142 exposure. | Not established, D. | Original/capture records, timebase/edit continuity and a still-generation linkage. |
| The extracted JPEG faithfully preserves the PDF's image stream. | Derived identity, A within the exact three pinned artifacts. | A byte mismatch or incorrect page/object association. |
| The processing exaggerated fire or proves intentional deception. | Unsupported by this unit. | A controlled source-to-output comparison demonstrating a material alteration, with its physical and intentional implications tested separately. |

The next local test should use the recovered **tape-name/timecode pair** as a
source-lineage key: inspect already held sibling AVI headers and directly
linked catalogue/production records for corresponding entries and internally
consistent relative ordering. Declare that finite population and interpretation
before reading results. Do not add this start value to frames 538/539 and call
the result a verified tape timecode without rate/edit-continuity evidence.
The highest-value missing documentary link remains an existing Figure 5-142
worksheet/database entry/export project connecting source asset, frame/field
and crop/resize/intensity steps, ideally retaining the unannotated still.
This identifies the useful record; it does not assert its existence or authorize
outreach.

Exact exposure identity is not a universal prerequisite for a bounded qualitative
fire observation. Such an observation needs defensible location, visible region,
resolution, timing uncertainty and treatment of processing/occlusion alternatives.
Claims of a particular pane state or mismatch to model inputs require tighter
joins. The [142-N12 human entry](../../nist-acoustic-detectability/window-state-human-review-user-2026-09-29.md)
remains unmarked as inspected. No new human acceptance, calibrated heat/steel
temperature, window-state finding or collapse-cause ranking follows here.

## Execution and limitations

See [execution record](execution.md) and the
[separate metadata review](metadata-review.md) for exact checks.
The evidence-audit workflow preserved an oversized first capture and corrected
an index-skipping bug instead of treating truncated output as a complete record.
The reviewer also caught a protocol overstatement: ordinary ffprobe can decode
internally while discovering stream information. These runs produced metadata
only, with no frame/audio outputs or new historical image views, but they were
**not proven zero-decoding runs**. The original plan remains unchanged and the
deviation is documented. Independent direct byte checks support the positive
metadata findings without relying on that probing behavior.

The fixed AVI tree contains no misplaced movie/audio leaf outside the skipped
movie list. The collector is not a validated general-purpose forensic parser;
its generic leaf handling must not be used to claim header-only behavior on
arbitrary files. DV packs, hidden/post-scan metadata, unknown binary tails and
all possible PDF revisions were not investigated. Those omissions limit
negative conclusions, not the directly checked positive fields.
The six controls do not test the depth/record/payload ceilings, and the
30-second timeout governs external commands only, not the entire Python/PDF
inspection. The actual fixed tree and observed output sizes bound this run;
neither the tests nor the timeout certify arbitrary-input resource safety.

No raw evidence, original annotations, prior comparison outputs, main/legal
records or authority boundaries changed. No files were committed, pushed,
uploaded or sent to Sherlock. The feedback routing issue remains separate
from this completed local unit.
