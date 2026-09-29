# Independent primary-PDF schema review

2026-09-20 UTC / 2026-09-19 America/New_York. Frozen before reading root's later PDF interpretation. Public-record document review only, not physical verification, human acceptance, legal drafting or a catalog-content identification.

## Finding

The inspected pages verify a **June 2004, Volume 4 progress-report example** of NIST's VideoList tape/copy and clip-timing records. They do **not** supply a CBS-Net Dub5 to numbered WTCI mapping. CBS is named among providers on printed H-3; the illustrated database rows concern a different individual-source example. Tape IDs visible in that example cannot be converted into WTCI filename numbers without a linking record.

The pages also support an important qualification: clips could be divided at natural recording changes **or** by the system's file-size limit within a continuous recording. Timing calculations have conditions involving a known reference time, continuous or real-time material, exclusion of replays where stated, and suitable metadata. The existence of those tools does not show that the current CBS access copies were timed, split or preserved in a particular way.

## Scope and source integrity actually checked

Read READ-SCOPE-04.md and the PDF skill completely. Followed the skill's read-only full-page visual review, using the six supplied 110dpi page PNGs individually through `view_image(detail="original")`. No new render, crop, image processing, download or source edit was made. Root/other later PDF interpretations were not read before saving this note. I have prior familiarity with the preceding search-index schema lead; this is not a blind discovery claim.

Source: `sources/nistspecialpublication1000-5v4.pdf`, acquired from the exact declared public NIST URL `https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1000-5v4.pdf` by root. I independently ran a local size check and SHA-256 calculation: **18,342,113 bytes**, SHA-256 **19281ca238382466a4a0029784d4789fb78cf4d8e4785ac49370c01f9aa94433**, matching the supplied acquisition identity. The 224-page container count and 110dpi render parameters are root-supplied metadata, not separately recalculated by this observer. A byte hash establishes local identity, not truth of the report's historical statements.

All six pages were viewed in full, including page headings, captions and footers. Only these six page images were visually inspected; this note does not claim a whole-document negative search. The images are working render derivatives of a preserved public document, not additional historical observations.

| Supplied filename under sources/ | PDF page | Visible locator | SHA-256 of inspected PNG |
|---|---:|---|---|
| sp1000-5v4-cover-001.png | 1 | Cover | 12ed2b1875d1f732c406e49c7bba71722e288eb75037f24be574a3f625d7ae36 |
| sp1000-5v4-schema-145.png | 145 | H-3; H.1.3, H.2, H.2.1 | 841ccd93c3e41a36a24ce254fe32f8eced8daf1369c3f7c737bc9e0b3607474b |
| sp1000-5v4-schema-146.png | 146 | H-4; H.2.2, H.2.3 | 158d05d07bfcb8dce6ddca28ee8c7601eaca8f95b895aa292dd5872018563723 |
| sp1000-5v4-schema-147.png | 147 | H-5; Figure H-1 | c44853021fa77269bee7d9f06aedfeee1e7d0e98db19de724de5f2e738e89ac7 |
| sp1000-5v4-schema-148.png | 148 | H-6; Table H-1 | bce58e8e69ece54085e13b482ab7d64dd492edec81c113e54747d3d66fdb2e55 |
| sp1000-5v4-timing-156.png | 156 | H-14; Video Tools; Figure H-5 | ba79f9bb3ded176f7af9ff705b2f7d61bc6f5f1d9c83a2e42c350cfb94d5d088 |

Personal names, an example recording location, database example clip names and screenshot taskbar/computer paths are unnecessary to this finding and are not retranscribed here. Their appearance in a public report does not make them relevant to the source join.

## Edition and document role

The cover identifies **NIST Special Publication 1000-5**, dated **June 2004**, titled *Progress Report on the Federal Building and Fire Safety Investigation of the World Trade Center Disaster*. It says **Volume 4**, containing **Appendices G, H, and I**. The reviewed appendix pages carry an interim-report heading about WTC fires based on image analysis. This is not the later final NCSTAR1-5A edition or a current 2026 catalog export.

Printed H-3 describes the then-current collection, names CBS among network/local providers, and distinguishes broadcast recordings from material recorded but not broadcast. It explicitly recognizes incompleteness in identified/collected visual material, while expressing NIST's view that its collection was sufficient for its investigation. That is an institutional statement in the progress report; it neither proves complete collection nor identifies the exact CBS tape now sought.

## VideoList fields and example relationships

Printed H-4, H.2.2, describes VideoList as a Microsoft Access database written for this application. Incoming videos receive unique identifying numbers; recorded information includes duration, network/broadcast date where applicable, physical format/storage, original-versus-copy status, source, digitization, embedded timecode and notes. The text also says mini-DV copies are individually logged. This is a described workflow, not proof that every eventual public file preserves every field.

Figure H-1 on H-5 visibly separates a top-level **Videos** form from its **Tapes** rows:

| Form portion | Visible fields relevant here |
|---|---|
| Videos | Video title; Network; Broadcast_date; Duration(min); Subject; Notes |
| Tapes | Tape ID; Tape name; Copy; Format; Duration; Location; Source; Derived from; Batch; Clips; Timecode |

The displayed tape rows include IDs **32, 51, 60 and 77**. The visible Copy values are respectively **3, 4, 1 and 2**. Formats show mini-DV for the first three and Hi-8 for77. Rows32,51 and77 visibly show **60** in the Derived from column; row60 shows **0** there. The example thus gives direct documentary evidence of separately numbered tape/copy rows and an explicit derivation field. The meaning of zero as a database sentinel is not defined on the inspected page; do not silently equate it with a validated original master. I did not transcribe tiny checkbox states because they are unnecessary to the requested mapping and do not establish database rules.

Figure H-1 is captioned as an **example** entry sheet. Its individual-source title and Network value do not identify CBS-Net Dub5. Neither the plain numeric Tape ID field nor the example's row numbering establishes equivalence to a numbered WTCI filename, a source chronology, or an original-camera identifier. The underlying table/relational export would be needed to establish the actual requested join.

The prose below Figure H-1 describes separate photographic and video-clip catalogs, chosen attributes, and thumbnail display. It points to Table H-1 for photographs and Table H-2 for video. **The page supplied as PDF148/H-6 is Table H-1 for photographic assets**, not a videotape inventory or the video-attribute table. That page includes file-reference/category/name, photographer/receipt/source, usage/copyright, shot location, recorded date/time uncertainty, direction and building-face fields. It defines fields and entry choices; it does not contain populated CBS/Dub5-to-WTCI rows. I did not inspect Table H-2 in this six-page pass and do not infer its full contents from Table H-1.

## What the clip-splitting passage actually establishes

Printed H-4, H.2.2, describes digitizing analog sources or copying already digital material, logging mini-DV copies, and transferring selected material to hard disk. It then describes these distinct boundaries:

1. Natural recording changes can arise from stopping/restarting a camera or switching among cameras, such as in a newscast. The report describes treating those changes as individual-video endpoints.
2. An Adobe Premiere-controlled process records the selected boundaries in a clip file, which can also hold notes, and then generates video data files.
3. The described AVI-handling system has a **1gigabyte** maximum video file size, corresponding in the report to slightly more than **4.5minutes**. Longer continuous segments are split into roughly that length. The report also gives search/catalog convenience as a reason for such splitting.

Thus, a clip boundary need not mean a camera interruption, and continuity cannot be inferred merely because two titles have successive numbers. The passage does not prescribe the modern Drive naming scheme, map Dub5 14/15, prove those short access copies were size-limit splits, or override their observed endpoint mismatch. The report's statement about preserving digital information in AVI is a workflow assertion; this review did not verify losslessness or provenance of any particular encoding/copy.

## Timing text and conditions

Printed H-14 under **Video Tools** describes importing an Adobe Premiere clip file into VideoList and connecting a known real-event time to its mini-DV position. For a broadcast recording filmed in real time, the text says one known point can time its clips **except replays**. The selected clips to be calculated exclude replays; a marking/selecting step is described. The text also says the tool can time a continuous recording divided into multiple clips.

Figure H-5 visibly contains Tape_Name, Tape_ID and Tape Length(min), a DV Reference Time paired with Actual Time in hour/minute/second/frame fields, calculation/report controls, and a clip table with Clip Name, DV Time In, DV Time Out, Actual Time In, Actual Time Out, Duration and Notes. The example Tape_ID is **32**, linking the illustrated timing sheet to one of the Figure H-1 example rows. That is a relationship inside this example, not the requested CBS/WTCI crosswalk. No example clock values are promoted to facts about the present CBS files.

The paragraph below Figure H-5 adds a separate conditional route: **for mini-DV video that contains metadata**, CatDV extracts clock times at clip-in and clip-out positions; those values enable timing from one reference time. The existence of those fields/tools does not authenticate a camera clock, show which current files retain the metadata, establish that a segment was genuinely continuous/real-time, or prove that any selected CBS clip received the procedure. A reference event and the applicable continuity/metadata conditions must be independently supported for the particular material.

## Crosswalk disposition and what changes

The earlier search-index excerpt's narrow claim about a VideoList example and identity/derivation fields is now supported by direct visual inspection of the exact primary report page. The prior bounded search note remains preserved as the earlier record of an unverified excerpt; this review supplies the new verification layer without changing it.

On the **six pages actually inspected**, there is no explicit CBS/CBS-Net Dub5 to numbered WTCI mapping. CBS appears only in the provider discussion relevant to this task; the populated figure is a different example. This finding does not assert that no mapping exists elsewhere in the224-page document, another report, a database export, or the public catalog. It also does not prove which tape any WTCI file contains.

The precise remaining record is an actual source/tape/copy or clip row that connects the CBS-Net Dub5 label to its preserved tape identifier and then to the public WTCI item. An export retaining Tape ID, Tape name, Source, Derived from and clip associations would be more useful than guessing from filenames. No new retrieval or media inspection was performed in this review, and no legal or causal conclusion follows from this schema verification.

## Addendum: separately supplied six-page expansion

2026-09-20 UTC. The initial six-page note above was saved and hashed **before** root sent the additional-page assignment. Its first **11,645 bytes** remain unchanged, initial SHA-256 **898f3296d12883258191c9dafac7923ce3e20e38353f9275e5a6bb3d8463c98b**. Root reported that its own initial six-page observations had been saved, but sent no substantive PDF conclusions. I did not read root's observations before this addendum. The newly supplied page selection itself is declared provenance, not a claim of complete selection independence.

I then inspected the following six complete PNGs individually at original detail. This expands actual coverage to **12 pages total: PDF1,145–148,150–156**. PDF149 and the rest of the document were not visually inspected by this observer. No global text search, additional render, crop, download or physical-media interpretation was performed. The screenshots embedded in the report were examined for schema/label layout; their thumbnail content was not analyzed as new event evidence.

| Supplied filename under sources/ | PDF page | Visible locator | SHA-256 of inspected PNG |
|---|---:|---|---|
| sp1000-5v4-attributes-150.png | 150 | H-8; photographic table continuation; H.3 and H.3.1 | 0d0ca642bf2df6563c5f949c70053ebd46ca0ef08b60d5845f06c40bae861fe5 |
| sp1000-5v4-attributes-151.png | 151 | H-9; Table H-2, video assets | c0c0ae7729b98464e2215ba1e30709648c6af6eb8c6bb2b31a01efece3cb35cf |
| sp1000-5v4-attributes-152.png | 152 | H-10; video table continuation | 7bf11ed54a2a05d8297fc90646bb912f6cd2418fd22d8a0b57097c757822dcab |
| sp1000-5v4-attributes-153.png | 153 | H-11; video table continuation | 16dc69995502e4a9519128d11c1e41e36bc32d14ad48d72ff8937c25e6f5a2b9 |
| sp1000-5v4-attributes-154.png | 154 | H-12; Figures H-2 and H-3 | ec3bb9e3bdb8ebf3d451ce657fa14870bb312f0c2373fa2f83bf96ce9d5025cc |
| sp1000-5v4-attributes-155.png | 155 | H-13; Photograph Tools and Figure H-4 | 65484b5f5fd02d8e80092662d30a3208ad1de96d5215dcecff0b065d669e398a |

### Actual video fields, distinct from photographic fields

Table H-2 is directly headed as the attributes for **video assets** on H-9 and continues through H-11. Its displayed organization is attribute, definition and entry choice; it is a schema/definition table, not populated source rows.

| Part | Fields actually specified for video | Material qualification |
|---|---|---|
| Identity/organization, H-9 | Asset Reference; Categories; Record Name; Photographer; Content | Asset Reference locates a clip in the file system; Categories are typically source/photographer groupings; Record Name is the clip filename. These are not displayed numeric Tape ID-to-WTCI links. The printed video-table label is **Photographer**; I have not silently renamed it. |
| Rights/location, H-9 | Use Limited; Copyright; Copyright Agreement; Shot From | Usage/source-location descriptors do not authenticate a tape or recording. The photographic table's **Received from** and **Original Source** fields are not listed in this inspected video table; do not import them into Table H-2 by analogy. |
| Time, H-9 | Date Recorded; End Recording; Duration; Time Uncertainty(s) | Definitions specify the clip's beginning, end, minutes:seconds duration and uncertainty in recorded/end time. Entry choices are date/time, real number for duration and integer for uncertainty. Field definitions do not show that values exist or are accurate for the CBS clips. |
| View and visibility, H-9–H-10 | View Direction; WTC Faces; Distance; Building | Distance categories are defined by detail visible in windows, ability to count windows, or inability to count them. They are descriptive clarity categories, not a calibrated camera-to-building distance. |
| Event/content tags, H-10–H-11 | Plane strikes; WTC1/2/7 collapse; street; debris categories; Fireball; Thermal; Plume; Flames Visible; people; falling components; streamers; dripping; hanging floor; core; FDNY/NYPD; aircraft; Major Change | These are checkbox/tag definitions. The table's physical wording is NIST's category vocabulary, not a new independent observation, mechanism finding or an assignment of those tags to the current CBS source. |
| Analysis and notes, H-11 | Good for Analysis; Analyzed; Notes | The analysis flags refer to possible/performed window-by-window analysis. Video Notes has entry choice **Text** and includes how a clip was timed. No actual CBS timing note appears here. |

The H-9 Content choices include WTC9/11 footage, an untimed street-scene category, post-collapse debris-field material, construction, normal operation, animation, stills and interview. Their definitions show that the catalog could contain distinct material types. Selecting or illustrating a category would not by itself establish a clip's clock, continuity, original source or factual correctness. The Major Change group on H-11 includes fire/smoke changes and opened windows; these are descriptive tagging options, not measured thresholds or a mechanism test.

Table H-1 remains photographic. H-8 continues that table; Figure H-2 on H-12 is explicitly a photographic data-entry example. Figure H-3 on the same page is the separate video asset-screen example. Neither its position beside Figure H-2 nor overlapping labels makes the two schemas identical.

### Figure H-3 and label-reading limit

Figure H-3 shows a Cumulus video screen with a category tree at left and example asset thumbnails, names and recording-start/end dates/times. Network/source-like groups and numbered Dub-like labels are visible in the tree. Some lower labels appear to start with **WCBS** and include Dub numbers; their remaining tiny/truncated text is not safely transcribed from this supplied render. I do not convert those labels into a full CBS-Net Dub5 title or a WTCI number.

The example asset grid is a different individual-source example, not a CBS-Net Dub5 record. No corresponding Tape ID/Derived from values or WTCI identifier are displayed beside the potentially relevant category labels. Consequently, the screenshot establishes that such catalog groupings were illustrated, not that a specific current folder/title has been authenticated or joined to a numbered tape.

This addendum relied on visible labels and captions, not OCR for small text. Uncertain letters remain uncertain; no digit or source name was reconstructed from expected results. A higher-resolution source view would be needed for exact small-label transcription, and even a perfectly read category would still require a record-level identity link.

### Added timing and completeness context

H-8 says some collected photographs/videos were omitted from the two catalogs after being judged not directly relevant. Its then-current counts are **6,759 photographic assets** and **6,911 video assets**. These are counts in this June2004 report context, not counts of current public folders or unique cameras, and catalog omission does not show footage absence.

H.3/H.3.1 on H-8 emphasizes that accurate times were absent for much collected material. Embedded camera clocks usually needed correction, sometimes being wrong by days or years, although the report treats short-interval relative timing as useful. This supports retaining the distinction between a recorded clock and authenticated event time; it does not validate the timestamp of an arbitrary present-day derivative.

H-13 notes that analog recordings may occasionally carry imprinted time information, but generally need other timing methods. Its **Photograph Tools** discussion is conditional on a set sharing a common clock from the same digital camera and on an accurate reference time. CatDV reads available metadata; PhotoTiming uses a paired Exif/actual-time reference to calculate adjusted times. The illustrated **62second** offset is specific to that photographic example. It must not be transferred to the CBS videos or generalized as an investigation-wide correction.

This added context complements H-14's video/replay/continuity conditions preserved above. It does not remove them. VideoList and Cumulus are documented tools and schemas; the present task still needs the actual CBS source/tape/clip records and their provenance.

### Expanded disposition

No explicit CBS-Net Dub5-to-numbered-WTCI mapping is established on the **12 pages now actually viewed**. The expanded review confirms the actual video schema and the existence of illustrated source/dub categories, but it does not authenticate their connection to the current acquired CBS files or any WTCI item. The remaining crosswalk and particular-source timing/continuity questions are unresolved. The initial six-page observation record above is preserved rather than retroactively represented as having included these additional pages.
