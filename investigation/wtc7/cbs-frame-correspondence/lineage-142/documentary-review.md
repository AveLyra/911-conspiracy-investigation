# Figure 5-142 / Clip 7 documentary lineage review

2026-10-04 UTC. **The inspected report/catalogue records do not supply the exact
tape-to-still derivation. Root's separate embedded-metadata inventory now adds
specific tape-name and timecode leads.** The original bounded non-recovery must
not be generalized to mean that the held AVI contains no such metadata.
The exact Figure 5-142 exposure/field and processing link remain unresolved.

## Scope and evidence layers

This reviewer read the current main AGENTS.md, WORKFLOW.md, START-HERE.md and
investigation charter, STATUS.md's current/CBS orientation, the completed
Clip 7 report, the exact Figure 5-142 attribution, its two named page-text
contexts, stage4 metadata/acquisition records, their catalogue pointers and
the directly relevant human/geometry records. The evidence-falsification and
source-of-truth skills governed the distinction between source statements,
saved catalogue metadata, derived source matching and physical findings.

The source-specific inventory was read-only. This final save adds only this
document. No media/image viewing, audio, raw-AVI read, decoding, network request,
matcher, test suite, source/result edit, legal/main change or outgoing Sherlock
message was performed by this reviewer. No authority or human gate is changed.

After that inventory, this reviewer read root's [report](report.md) and
[metadata.json](metadata.json). The new embedded-field findings below are
**attributed to root's raw-byte inventory and its separately reported check**,
not an independent raw-byte examination by this reviewer. Root's Adobe field
interpretation is likewise attributed: this reviewer did not retrieve or
independently inspect the Adobe specification. Reading root's saved probe output
is not a new probe. This review makes no claim that root's metadata probe was
proven to perform zero internal decoding; the report expressly records that
limitation.

## Positive documentary findings

1. **Report location, interval and processing disclosure.** The physical-page272
   caption identifies the lower northeast corner viewed from West Broadway /
   Barclay Street, between 3:55 and 4:04 p.m.; it discloses intensity adjustment
   and added floor/column labels. These are attributed report statements, not
   independently authenticated clock or processing parameters.
   [Page272 text, lines4–7](../../fire-coverage-batch3/assets/run01/context/P-8338c00a97d8.txt).
2. **Relative sequence, not an extraction locator.** Physical page271, lines18–22,
   calls Figure5-142 a frame from a clip recorded roughly two minutes after
   Figure5-141, and says flames in window8-42A were visible during the short
   clip although not readily apparent in the still. This warns against treating
   every video-derived assertion as independently demonstrated by the printed
   still. No tape number, source timecode, frame number or field is supplied.
   [Page271 text](../../fire-coverage-batch3/assets/run01/context/P-ebeb74127e68.txt).
3. **An explicit unresolved alternative.** Page272, lines18–23, leaves the lower
   plume unresolved between transported smoke and a fire on Floors5–6. It does
   not demonstrate fire on those floors merely from that plume. Its statements
   about intense flames elsewhere are report interpretations, not this reviewer's
   new observations or a calibrated heat measurement.
4. **Published-image identity.** The
   [attribution record](../../fire-coverage-batch3/source-attributions.json),
   lines5902–6037, identifies CBS credit, asset A-7c7cc22dc34c, physical page272 /
   printed228, PDF object2850/0 and the 706×457, 151488-byte JPEG. Its recorded
   PDF-to-JPEG derivation does not by itself connect a camera exposure to the
   processed, annotated report still. A raw PDF image codestream is not a
   camera-raw or unannotated source still.
5. **Held-copy identity.** Stage4's
   [acquisition record](../../cbs-vince-source-screen/stage4/acquisition.json),
   lines30–88, joins provider ID `1CnLqGzglKNyLeNwTrXBR1kxHdogB96wh`, literal title
   `Vince Demetri Clip 7.avi`, 140334936 bytes and received-copy SHA256
   `a2aefd37d58a7f2e7cea73c8d06114ec941e2178d1a4ddc9419649dd9936487b`.
   It records a complete first attempt, not original-camera custody.

## Exact catalogue links and their strengths

| Link | Saved support and limit |
| --- | --- |
| Organized Photos and Video Clips `17lDS4YslnUaOHv-x2CEhWLVzmceNllk1` → VideoClips `1mKqRTrMFX4VDnxW_-VU3pByhfqqs1uwn` | `late-fire-catalog-join/sources/nist-organized-root.connector.json`, line9 nested listing and lines10–16 outer identity. Listing-context membership; VideoClips' own parent field is null. |
| VideoClips → Vince Dementri CBS WTC7 `1EjgG0oRrJ6VGrVG304qKDAUmKd80n5Rg` | `late-fire-catalog-join/sources/nist-cbs-folder-search.connector.json`, lines163–176, explicitly supplies the VideoClips parent ID. The reconstructed `listing-request-receipt.md`, lines13–20, records the parent-filtered search. |
| Vince folder → Vince Demetri Clip 7.avi `1CnLqGzglKNyLeNwTrXBR1kxHdogB96wh` | `nist-acoustic-detectability/cbs-folder-metadata-2026-09-28.json`, lines49–57 exact folder-listing request and lines116–129 Clip7 row. Request-context membership, not an explicit child-parent field. |

The parent rows were checked separately by a bounded text-only helper and by
this reviewer; that is another reading of the same saved captures, not an
independently retrieved catalogue. The folder's **Dementri**, file's **Demetri**
and embedded tape-name spelling are preserved rather than silently normalized
into authenticated personal identity. The reconstructed request receipt is not
a provider-native request log. Its official-landing statement was not newly
verified in this task.

Stage4 [metadata-refresh.json](../../cbs-vince-source-screen/stage4/metadata-refresh.json),
lines8–36, requested description/video metadata/checksum/parent fields but
returned a normalized object without several of them. Earlier folder metadata
explicitly warns about normalization omissions. **Missing or null captured
fields do not establish absence at the provider.** The returned 2019 catalogue
timestamps are not authenticated September2001 recording times. Clip number,
folder name and report similarity do not establish tape continuity or a source
exposure identity.

## Update: embedded leads from root's separate inventory

Root's pinned metadata inventory and report now record the following prefixes
before the first NUL byte. The offsets below are the report's zero-based
**payload** offsets; the metadata JSON's RIFF record offsets are eight bytes
earlier. Full payloads, including uninterpreted binary tails, remain preserved.

| Field | Reported payload offset | Leading text / attributed meaning |
| --- | ---: | --- |
| Tdat/tc_O | 140334520 | `00;03;12;26`; root identifies a start-timecode field using the Adobe mapping. |
| Tdat/tc_A | 140334546 | `00;03;12;26`; alternate-timecode field. |
| Tdat/rn_O | 140334572 | `Vince Demetri CBS`; tape-name field. |
| Tdat/rn_A | 140334620 | `Vince Demetri CBS`; alternate tape-name field. |

Root also records a Cdat/cmnt description of flame/smoke/debris content. It is
unattributed embedded description, not independently observed physical evidence.
Repeated original/alternate values are not independent corroboration.

This is a material advance beyond the catalogue/page-text inventory: a
**specific retrieval key exists in the held access-copy metadata**. It remains
editable metadata, not authenticated original tape ownership, camera custody,
exposure time or a Figure5-142 still-generation record. No original rate,
drop-frame convention, edit continuity or frame/field linkage was established
by this documentary review. Do not add source index538/539 to that text and
present the result as verified tape timecode or local time of day.

The earlier non-recovery statement remains valid only as: “The inspected
catalogue and report records did not supply the exact source-timecode/tape-to-
still bridge.” It would now be inaccurate to say that no tape-name/timecode
lead exists in the held material.

## Ordinary explanation, discriminator and useful observation

The strongest ordinary explanation is a publication/access-copy workflow:
an intensity-adjusted and annotated still was published, while a later
catalogue exposed selected file-level fields and the access copy retained
some production metadata. The disclosed processing and normalized-field
limits support considering that explanation; the recovered embedded fields
make it more specific. The exact workflow remains unverified. This does not
prove faithful processing, material exaggeration, withholding or intent.

The highest-value exact documentary link is **any existing Figure5-142
production worksheet, visual-evidence database entry or export project** tying
the source asset/tape-name/timecode lead to the selected frame/field and
crop/resize/field/intensity processing, preferably with the unannotated still.
This identifies useful content, not a claim that such a record necessarily
exists or permission for outreach. A separately declared finite sibling-header
comparison could test the new lead's internal ordering; it cannot authenticate
historical custody merely through consistent editable tags.

Exact exposure identity is **not a universal prerequisite** for a bounded
qualitative fire observation. A claim confined to visible flame-like content
in a specified held view needs defensible source/location, observable region,
adequate resolution, stated timing uncertainty and consideration of processing,
reflection and obscuration. A coarser claim may remain useful when neighboring
candidate frames cannot be distinguished. It does not require all original
model files or a complete image-edit recipe merely to describe that view.

Claims of an exact pane state at a particular time, alteration of the published
image or disagreement with specific model inputs need the corresponding tighter
place/time/processing/model joins. Exterior brightness does not measure steel
temperature or interior heat release; visible localized flames do not by
themselves establish the total interior fire extent. The
[human record](../../nist-acoustic-detectability/window-state-human-review-user-2026-09-29.md),
lines19–26 and40–45, still has **142-N12 not marked inspected**. Filled impression
fields do not create an inspected-pane finding. The
[geometry crosswalk](../../nist-acoustic-detectability/window-geometry-crosswalk-2026-09-28.md),
lines57–86, allows useful qualitative comparisons with matched scope, while
preserving Floor8/Floor12, exact-input and event-time distinctions. Actual-human
spot-check requirements for consequential automated measurement remain intact.

## Inspected file identities and actual checks

Paths below are relative to the investigation's `research/sherlock-wtc7-investigation/`
directory unless stated otherwise. The two page texts were read completely
with `nl -ba`; their `shasum -a 256` results match the source-attribution pins.
Relevant records were read with `cat`, `sed -n`, `nl -ba` and bounded `rg`
queries. No parser/test/matcher or new media extraction was run. This is not
an exhaustive archive search or a replay of the prior numerical comparison.

| Inspected material | SHA256 checked |
| --- | --- |
| cbs-frame-correspondence/dense-clip7/report.md | `984f3132fae5016cc01bdf2a68831b2147963fc0db9fd541e4aa908ce96ff470` |
| fire-coverage-batch3/source-attributions.json, Figure5-142 and named context entries | `c79c043fd6c0e87505481df94080f6d3a325c74f90e27f870a49f0b69a0cd20d` |
| fire-coverage-batch3/assets/run01/context/P-ebeb74127e68.txt, physical271 | `2772110710b61a13af806b2f77829bde1af0b2f570ecbc6c0df6edfe647f927b` |
| fire-coverage-batch3/assets/run01/context/P-8338c00a97d8.txt, physical272 | `f5a4c9ef7d07a1d153c7f208693eccb97d58542cf170498fe3a64102e5ab2735` |
| cbs-vince-source-screen/stage4/metadata-refresh.json, Clip7 entry | `b5a5d6bc0bf12a8079f96f5ecc0548d4c260beb0fcf06bde5be870508cb4a27e` |
| cbs-vince-source-screen/stage4/acquisition.json, Clip7 entry | `7ad550f1e6394c0e5e86984b2a63090a5f250c70735e838592fe8282ba2fb6a7` |
| nist-acoustic-detectability/cbs-folder-metadata-2026-09-28.json, request/folder/Clip7 entry | `44168a69f5b823f70e82f45cf06f8ff610c9388e39876ed0d8a60043d7554e1a` |
| late-fire-catalog-join/sources/nist-cbs-folder-search.connector.json, Vince entry | `64fb1e41b773e10da666899b32e6a42c6afd823dfb76b4a239c2b36a2dfa5be8` |
| late-fire-catalog-join/sources/nist-organized-root.connector.json, root/VideoClips entry | `93658f5427045ae96bd6dfd086427ca3093c9b2fed01c26a3e03ff214653a9ec` |
| late-fire-catalog-join/listing-request-receipt.md | `9919f84d826594809f0b2513ea21b3ad6772f0c420e5144ae0a8c0f162fe137f` |
| cbs-frame-correspondence/lineage-142/report.md, root snapshot read before this save | `6904ac731d4f1b553d2c8a7ddb447928e6048af2c9bd079e5231f04f1b93cf52` |
| cbs-frame-correspondence/lineage-142/metadata.json, root inventory read before this save | `b2e51a671177c0b5ea0b2784eb1894eaacb38c24208d37a2c20207d5689781fc` |

Navigation/direct-pointer text additionally inspected: cbs-vince-source-screen/
PROTOCOL.md lines1–29; nist-acoustic-detectability/window-clip-inventory-
2026-09-28.md's exact folder pointer; window-clip-inventory-independent.md
lines205–288; the human-response and geometry-crosswalk files named above.
No new integrity claim is made for unpinned navigation text. The stage4 input
file was included only in a bounded metadata-reference text search, not used
as independent camera provenance.

Actual page-text read/hash command completed exit0, tool chunk `04b7a1`;
source-record hash command completed exit0, `db6de3`. The final root report/
metadata read and hash command completed exit0, `2f1353`. These are saved-text
checks only. Historical media custody, exact still linkage and physical
inferences remain open; no new causal ranking or research-to-case promotion
is made.
