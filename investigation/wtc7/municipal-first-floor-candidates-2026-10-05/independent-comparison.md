# Independent held-record comparison

Working research, October 5, 2026. This separate comparison began only after both
complete new-source reading freezes were reported. It does not alter the frozen
initial observations or make repeated source material an independent witness.

## Preconditions and actual representation

My new-source reading: 29,253 bytes, SHA-256
`d4e190aa3411a7e0cc42c6dac2e7ec15852596c19b1f80724dded3dc1e6ed023`.
Receipt 06ae68, exit 0, 1.741 s, verified the unchanged 7,751-byte initial prefix,
protocol and both PDF pins, final newline and no trailing whitespace. Root
reported its own frozen 15,671-byte record SHA-256
`3104215f8674d31b071b40862ba59d453611659c5505b5e8160774bd37702c18`,
29 initial views and zero repeats. I did not read that record or root findings
before either this comparison or my initial freeze. The process notifications
are attributed reports, not my independent audit of root tool chronology.

The protocol was reread in full (ab9b77, exit 0), confirming exactly two held
views. The held PDF and PNG files were hashed without PDF parsing or content
extraction; PNG dimensions came only from the IHDR bytes (20938a, exit 0,
2.986 s). Base path:
`../municipal-originals-2026-10-04/followup/`.

| Input | Bytes | Saved dimensions | SHA-256 |
| --- | --- | --- | --- |
| NYC-WTC_000173199.pdf | 333388 | — | `37b65cb843cd81716df26af8780627e27bed6d0557eb4b3419945ef742495903` |
| render/173199-1.png | 85462 | 1287 × 1724 | `0801d39df1b19903c6bbe469d7f96ea90ac547571394e5468932c9b01a048f62` |
| render/173199-5.png | 143765 | 1287 × 1726 | `01821bed2c8209a0bd12de3a85c1a874a8c509cf5d65552c4dab266f5d025907` |

Actual read pattern, once for page 1 followed by once for page 5:

```javascript
const r = await tools.view_image({path: absoluteHeldPngPath, detail: "original"});
text({requested: "original", returned: r.detail, forwarded: "original"});
image(r.image_url, "original");
```

Both calls returned original detail and no explicit resize notice. The stored
pixel dimensions do not prove native-pixel display. Exactly two held full-page
views, zero repeats/new rendering/crops/OCR/extraction/enhancement/measurements.
No 166828 S-S-1 image, other earlier image, root source note or synthesis was read.
No confidentiality marking was observed; contacts, names and signatures are
omitted from this narrative.

## Page-specific observations and comparison

**Held 173199 physical page 1, Bates 173199:** SHCA addendum cover/transmittal
with some upper project/date text obscured by a superimposed address/routing
block. The readable body calls the addendum a contract document modifying
specifications and drawings dated May 4, 1998; revisions are according to the
attached drawing/specification lists, and only items in bold italics are issued
under Addendum 1. A received stamp reads May 20, 1998; a separate handwritten
FYI notation carries May 21, 1998. Receipt/routing dates are not sheet issue or
as-built dates. The cover does not itself supply an actual structural plan,
prove that every listed drawing was newly issued, or identify a modified member.

**Held 173199 physical page 5, Bates 173203, printed list page 3:** SHCA,
Mayor's Office of Emergency Management, 7 WTC, project 5576A, May 15, 1998,
“List of Drawings—Addendum #1.” The bold-italic-only issuance legend is explicit.
The structural rows are S-1 first floor, S-2 seventh floor, S-3 twenty-third
floor, S-4 roof part and S-5 sections, all carrying May 13, 1998. They appear in
ordinary rather than the bold-italic issuance style exemplified lower down by
AV-E1 dated May 15. S-1 reads “1ST FLOOR FARMING PLAN”; the other framing/farming
titles retain the source's apparent spelling rather than supplying actual plans.
The page also contains AV and telecommunications lists for other subject matter.

The observed project number, date, addendum heading, structural identifiers,
floor roles, May 13 row dates and typography agree with the material index
features in newly read 173192 physical page 3 (Bates 173194). This supports a
repeated index/list relationship, not an independently sourced construction fact.
It is a visual field comparison, not proof that the whole PDFs or raster pixels
are byte-identical. My initial new-source note transcribed S-3 as “FRAMING” while
the held view appears to say “FARMING”; that fine lexical difference remains
unresolved without another prohibited revisit and has no bearing on whether an
actual plan or member geometry is supplied. The initial note is not rewritten
to manufacture exact agreement.

The cover and index together support reading the list as part of an Addendum 1
package with a base-drawing date and selective new issuance. They do **not**
establish that the S-1 row is the later S-S-1 sheet, that a May sheet was revised
in October, that SKS-S-2 is its detail, or that any particular beam/grid/member
was altered or installed. No October sheet or source image was viewed here;
the earlier October context remains prior context, not a new verified bridge.
173192 adds a separately held copy of the index lead but no underlying plan.
The 169180 packet's administrative pages add no such bridge either.

## Bounded disposition

The strongest useful lead is now more specifically described: an actual
project-5576A S-1 first-floor structural sheet with the May 13, 1998 row date,
plus a documentary revision/renumbering connection if it is to be related to
S-S-1. Neither newly admitted PDF nor these two held views supplies that sheet
or connection. This is not proof that the drawing is absent from the archive,
never issued, unapproved, unbuilt or omitted from a model. It does not justify
selecting a member by number or advancing an installed-condition/causal claim.
Any next acquisition needs its separately declared bounded source scope; the
current unit authorizes no automatic queue or expanded search.

Both permitted comparison views are complete and their reading set is closed.
This note was saved before accessing root source findings or synthesis.

## Post-freeze reconciliation — no new source views

The initial 6,061 bytes above froze as SHA-256
`fa229d67cf3598ab70fe8356e02ab7cb499fd0715f89e8db23a1b1bcd2fe2858`
(82ad6f, exit 0, 6.390 s). That check also confirmed my 29,253-byte initial
observations still matched their frozen pin. Only after that freeze did I read
root's complete observations and comparison. A stdout-only Python invocation
read each exact path, asserted its SHA-256 against the separately announced pin,
then printed the full Markdown: cda9c3, exit 0, 1.125 s. Both pins matched:

- root-observations.md: 15,671 bytes,
  `3104215f8674d31b071b40862ba59d453611659c5505b5e8160774bd37702c18`.
- root-comparison.md: 2,610 bytes,
  `1555040df22f4875e21d58b1e7db0244c55bf845da26da2baaf426b5ac06e177`.

The direct-reading method, two packet page counts, listed-versus-supplied drawing
distinction, original-detail limitations, zero repeats, two separately authorized
held views, bounded nonmatch and repeated-index relationship materially agree.
Neither reader identifies an actual first-floor structural plan, an express
S-1/S-S-1 revision bridge or a usable member map in this admitted population.
Both preserve favorable/compliance evidence and refrain from turning allegations,
blank forms or general inspection statements into event-day conditions.

The following differences are retained, not silently reconciled into exact quotes:

| Page/field | My frozen reading | Root frozen reading | Disposition |
| --- | --- | --- | --- |
| 173192 p3 / S-3 spelling | “FRAMING,” while some other rows were recorded “FARMING” | Framing used descriptively, explicit apparent “FARMING” retained for S-1 | Held 173199 p5 appears to use “FARMING” for plan rows. No new 173192 view; avoid claiming exact whole-list transcription equality. Material identifiers/floors/dates agree. |
| 169180 p5 / offense date | Not reliably resolved | Appears 8/25/99, explicitly uncertain | Do not select a date from the competing faint readings. |
| 169180 p11 / receipt day and directive | February 6, 1991; F.P. Dir. 3-60 | February 6 or 8, 1991; F.P. Dir. 5-60 | Treat exact day and directive digits as unresolved in synthesis. Agreement on 1991, floor 27, cutting-torch complaint and “No Cause” is sufficient for this scope. |
| 169180 p18 / Class E order wording | Broad system/alarm-operation paraphrase | Compliance/plan-submittal, circuit-diagram/floor/A-C-plan and approval language, itself qualified | My broad paraphrase must not become a finding of missing/inoperative equipment. Exact requirements are unresolved; both see an administrative order, no framing plan. |
| 169180 p20 / record requirement | Fire-alarm records | Fire-drill/inspection records, tentative | Use only “records requirement” absent a clearer separately scoped reading. No new violation event or compliance outcome inferred. |
| 169180 p23 / reinspection date | December 9, 1998 | Appears December 9, 1998; day qualified | Retain day uncertainty while preserving the agreed FP-12/FP-28 C.W. marks and dismissed recommendation, distinct from blank Bureau disposition. |

Root also more expressly linked contiguous pages 16–17 as a 1994 inspection
family, using the continued-form heading and matching categories. My note kept
page 16's absence of its own visible date and page 17's May 31, 1994 date separate.
These are compatible when the family linkage is stated as an inference, not an
independently printed date on page 16. Root's cautious operational/preincident
description of page 24 is compatible with my “computer/dispatch-style” label;
neither establishes that an actual alarm event occurred at an identified time.

No additional source image, PDF content, source acquisition or root synthesis
was used for this reconciliation. No frozen observation text was altered. These
remaining peripheral differences do not change the first-floor-plan disposition;
they limit any exact enforcement chronology or technical interpretation beyond
the declared question. Agreement between two prior-informed AI readers of the
same sources is not an independent historical witness, engineering acceptance or
validation of source authenticity.

Replay of the initial comparison freeze must hash exactly its first 6,061 bytes,
not this subsequently appended full file. The separate observations file retains
its whole-file frozen hash; its original index freeze is the first 7,751 bytes.

## Root synthesis review

After reconciliation, I read the complete 10,289-byte report.md at SHA-256
`52c259adb7072df3521f0acf5e18e7e402a2c9cd3df8df67acf3afc1cb233a87`
(9a2dc6, exit 0, 1.425 s). The central disposition matches the frozen readings;
the report retains the fine directive/day/spelling/order-wording differences,
positive compliance evidence, p21's faint entries, family-versus-whole-copy
distinction, and source/installed/model limits. It does not use a higher-resolution
repeat after exchange to make the readers agree. No material structural-plan
overclaim was found in this bounded source-transcription review.

One narrow wording clarification was sent to root: “the referenced card and
completed service are not supplied here” should mean that the referenced card
and **evidence closing the remaining relay work** are not supplied. Page 15 does
supply a report of some performed service; missing follow-through is the supported
limitation. This suggestion does not change the frozen observations.

The proposed one-page CO56 test is explicitly a future separately scoped content
test, not a result established by these source pages or an automatic queue. I
did not reacquire or independently recheck that candidate's metadata, replay
acquisition/renderer processes, inspect transport headers, audit root's full tool
history, or reassess the scientific/model status during this reader review.
Those report statements remain governed by their separate existing receipts.

Receipt c3bba3, exit 0, 4.030 s, verified all eight report local-file link targets
exist, the report pin remained unchanged at that check, this comparison's exact
6,061-byte initial prefix remained unchanged, and the whole initial observation
file still matched its frozen pin. Link existence is not substantive acceptance
of each linked file. No additional primary source view was performed.

Root then adopted the narrow service-record clarification and added the link to
this comparison. Receipt 89f1b7, exit 0, 1.940 s, verified the intentionally
revised report at 10,433 bytes and SHA-256
`4e8588712b43075edc2488aa46a6c0699e2983d5f1b797f6c02044774d1c44e5`.
The revised row expressly distinguishes reported performed service from absent
evidence closing the remaining relay work; the new comparison link exists, as
do all nine local report targets. This was an announced correction, not a failed
unexpected-pin check. The intermediate comparison freeze (05c791, exit 0) was
12,390 bytes / `e8164bbc493c0a52116431054052fdedf481017983784f4e6af6ef4b2c25159c`;
only this final verification paragraph is appended after it. No primary reread,
new source or change to either initial observation/comparison prefix occurred.
