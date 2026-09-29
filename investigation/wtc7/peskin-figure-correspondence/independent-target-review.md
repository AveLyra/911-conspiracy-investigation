# Independent target-image regions and matching limits

2026-09-13. Prospective region suggestions within a retrospective same-source
comparison. These choices were made after reading the admitted prior screening
account, but **before viewing any additional candidate video frames or current
matching results**. This is not a verified correspondence, clock correction,
fire measurement or original-exposure identification.

## Actual coverage and pins

Read current main AGENTS/WORKFLOW/START-HERE, the complete investigation CHARTER,
this unit's protocol, and main `fire-originals/peskin/PROTOCOL.md`, `report.md`
and `validation.md`. Evidence-falsification and PDF safeguards were applied.
Read only the two selected asset entries and physical-page-278 placement entry
in the reviewed provenance key; no other asset images, video frames, archive,
raw model, source video, source metadata headers or held packet were opened.

Exactly three complete images were visually inspected: the full report page
context, then both full native-size target JPEGs. No crop, enhancement, new
render, matching computation or video decode occurred. Source-byte hashes were
checked before and after viewing; they match the saved selected-key pins.

| Input, relative to main `research/sherlock-wtc7-investigation/` unless stated | SHA256 / identity |
|---|---|
| Worktree `peskin-figure-correspondence/PROTOCOL.md` | `e445a976b664e6d2bd8c619d415cf0c1eb0ccc4866743082231b34f0a0f00537` |
| `fire-originals/peskin/PROTOCOL.md` | `9de07a527b8a7de017063ee647b0617343401f44ddf2b813571b56fb2fc19789` |
| `fire-originals/peskin/report.md` | `84e2b851f396c47efce61955418479fe51dae2a477595051d90b37e0ab357fd0` |
| `fire-originals/peskin/validation.md` | `35daf2e70f0de2584fe22b8668c0928c87584cdfeb5d3a150b055f0e234dcb4b` |
| `fire-annotation/assets/run-01/reviewed-provenance-key.json` | `c0361c5a3ae52c2663a6772db6078824b4b123e59d8e50d2e24b26d85855afa3`; selected entries only |
| `fire-originals/peskin/derivatives/ncstar-context-278.png` | `7cbb61686d3efb782ccc8dacf194792238fec2ed7e9f5c66af555fd0a180ab85`; 935 x 1210 full-page RGB PNG |
| `fire-annotation/assets/run-01/images/A-370a6ef2789a.jpg` (T148) | `8afb62b6dce6e4618075c66576ef9fdf88295d636427893dc36064afb37a1253`; 124,078 bytes; 720 x 478 RGB JPEG |
| `fire-annotation/assets/run-01/images/A-e43e4088a4a2.jpg` (T149) | `6129afd898a56282579832595715ef2e1093b55d299b693810ac05c72af53469`; 117,263 bytes; 720 x 478 RGB JPEG |

The full page identifies T148 as upper-placed Figure 5-148 and T149 as
lower-placed Figure 5-149, printed p.234 / physical 278. Both captions state
image intensities were adjusted and column/floor numbers added. Their reported
clocks are source assertions; the actual caption, page text and overlay labels
are not independent match evidence. The JPEGs are extracted PDF image
codestreams, not original camera frames or the PDF's on-disk ciphertext.

Prior PDF pin from the read validation/key is
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
This arm viewed the saved complete page derivative and did not reread/re-render
the entire PDF. The prior video/source pins and screening coverage were read,
not independently re-decoded or rehashed here.

## Coordinate and selection convention

All boxes below are **target-JPEG coordinates**, with origin at upper left,
x rightward and y downward; `[x0,y0,x1,y1)` is half-open, integer-pixel bounded.
They are exact proposed box definitions, manually selected from the complete
720 x 478 views, not subpixel landmark measurements. They do not use report-
page points or the 935 x 1210 context coordinates. No aspect-ratio correction
has been applied. Outer three-pixel strips on all four target edges are excluded.

These are independent candidate masks for parent method selection, not a
requirement to accept an uninformative patch. Preserve this version if a later
method adopts different boxes. A future candidate-dependent modification must
be declared and retain the earlier choice and reason.

## Overlay and non-scene exclusions

Exclude the following generous guard rectangles from every registration or
dynamic-content score. Do not use their outlines, OCR, positions, color or
anti-aliasing as scene landmarks.

| Target | Label/content | Exclusion boxes |
|---|---|---|
| T148 | Red column labels | `[251,82,289,112)`, `[408,87,447,118)`, `[537,95,575,124)` |
| T148 | Right floor-number labels, top to bottom | `[602,43,648,79)`, `[604,132,636,169)`, `[603,219,635,255)`, `[603,303,634,340)`, `[600,398,634,433)` |
| T148 | Bottom copyright strip | `[0,444,260,478)` |
| T149 | Red column labels | `[272,92,311,121)`, `[423,99,462,131)`, `[535,103,574,131)` |
| T149 | Right floor-number labels, top to bottom | `[611,53,656,89)`, `[612,133,658,170)`, `[612,214,658,250)`, `[613,295,658,331)`, `[615,366,660,406)`, `[613,451,643,478)` |
| T149 | Bottom copyright strip | `[0,449,264,478)` |

The masks are padded proposals, not a complete segmentation of all JPEG ringing.
Before any consequential score, parent should visually verify overlay coverage
in the exact native target. If a resampling kernel reads outside a mask, guard
support must expand according to its declared radius, not bleed labels back in.
Page margins, captions and body text are outside both JPEGs and are never used.

T149's saturated foreground patch `[3,237,65,339)` and bright right-edge object
`[683,210,717,266)` are additional exclusions from photometric registration:
they may change with clipping, reflection, reframing or object motion. This
does not classify those features as fire or identify the bright object's cause.

## Static structural suggestions, with plane and quality separated

The strongest crisp structure is on foreground buildings, not the hazy WTC 7
plane. A single transform optimized mainly on foreground pixels must not
certify alignment of the background fire frontage. Track foreground alignment
as a separate diagnostic; evaluate the WTC 7 window-band geometry explicitly.
Zoom/pan/parallax can produce different apparent shifts at different depths.

| ID | Box | Intended structural content | Quality / limitation |
|---|---|---|---|
| T148-S1 | `[12,15,235,270)` | Left foreground facade's light/dark bands and terminal vertical edge | Strong geometry, but repeated bands and a different depth plane; not a WTC 7-only registration mask |
| T148-S2 | `[8,278,233,437)` | Left foreground diagonal parapet/setback and its junction with facade | More distinctive than a single window cell; perspective/occlusion context only |
| T148-S3 | `[660,164,713,214)` | Right foreground projecting ledge/balcony boundary | Independent foreground-plane check; do not let brick repetition alone select a frame |
| T148-S4 | `[672,287,713,332)` | Second right foreground white ledge and edge | Separate vertical-position check, excluding nearby floor label |
| T148-W1 | `[296,123,377,175)` | Faint upper background facade/window-band texture, away from the small bright patch | Low confidence/low contrast; may fail a texture or uniqueness gate |
| T148-W2 | `[340,295,380,338)` | Lower background window-divider neighborhood | Tentative structural edge amid haze; not a smoke-free intensity template |
| T148-W3 | `[426,294,456,339)` | Another lower-row window-divider neighborhood | Same haze qualification; single-row aliases remain |
| T148-W4 | `[523,295,556,339)` | Right part of the lower background window row | Weak edge information, not a verified unique mullion identity |
| T149-S1 | `[12,77,159,218)` | Left foreground upper setback/roof boundary | Distinct corner shape, but separate depth and broad low-texture surfaces |
| T149-S2 | `[80,166,278,244)` | Left foreground projecting horizontal ledge and its end | Strong corner/edge arrangement; foreground-only diagnostic |
| T149-S3 | `[71,343,258,435)` | Lower left foreground diagonal edge and bands | Checks a second vertical level without copyright strip; repeated geometry remains |
| T149-S4 | `[661,91,713,143)` | Right foreground brick/white-ledge junction | Useful cross-image layout check, not a historical-time marker |
| T149-W1 | `[164,125,580,173)` | Upper background window band across several openings | Stronger target-plane candidate than T148; repeated-grid aliases and haze still matter |
| T149-W2 | `[281,204,580,247)` | Second background window band above the bright flame row | Adds separated vertical structure; no resolved flame here does not mean invariant pixel intensity |

Apply the overlay/edge exclusions even when a suggested static box overlaps
one. Do not score each box as an independent camera or observation. Window
band/divider labels above describe image neighborhoods, not independently
authenticated floor/column designations. T148 may simply lack enough reliable
background-plane structure for a unique transform; rejecting that inference is
preferable to accepting a foreground-driven fit. The box suggestions do not
claim that all their pixels are temporally static.

## Dynamic content, held out from fitting scene alignment

After a structural transform is fixed, these boxes can test prospective fire/
smoke correspondence. Preserve several spatially separated regions instead of
collapsing to one maximum-orange score. They are not temperature or flame-area
measurements. A small warm patch may have insufficient resolved shape for
unique matching even if it is genuinely scene content.

| ID | Box | Observed target content / caution |
|---|---|---|
| T148-D1 | `[388,143,417,169)` | Small isolated upper bright/warm patch; limited spatial information |
| T148-D2 | `[299,304,338,331)` | Lower cluster of small warm/bright points |
| T148-D3 | `[388,304,416,332)` | Weaker separated lower warm patch; ambiguous fine shape |
| T148-D4 | `[261,231,567,293)` | Broad pale haze/plume region above the lower window row; diffuse boundary and contrast dependence |
| T149-D1 | `[265,278,291,328)` | Bright left flame region adjoining the foreground edge; clipping/occlusion risk |
| T149-D2 | `[315,278,414,337)` | Central multiple bright flame forms |
| T149-D3 | `[447,278,568,342)` | Right flame forms and adjacent weaker red glow |
| T149-D4 | `[280,15,592,87)` | Upper diffuse haze/background region; weak temporal discrimination, not a definite smoke source attribution |

Keep D1-D3 out of structural fitting. D4 is a diagnostic region, not proof
that all haze elsewhere is absent: smoke can cross every nominal WTC 7 static
box. Do not treat D4 as an exhaustive smoke segmentation. If haze moves over a
window edge, retain the structural/dynamic contamination as a limitation and
compare edge geometry separately from intensity rather than silently relabeling
all such pixels static. Exact orange brightness or white clipping need not
survive NIST intensity adjustment and intermediate encodings.

## Method risks and required interpretation safeguards

1. **Repeated-grid ambiguity:** whole rows and separated structural levels are
   more discriminating than one window cell. Retain alternative integer-window
   and integer-floor shifts and check edge/corner layout, rather than assuming
   the highest correlation selected the correct bay or frame.
2. **Depth and crop:** left foreground setbacks/right brick edges can locate a
   similar view while the WTC 7 plane remains misregistered. Separate plane
   residuals and use the smallest adequate declared transform. Missing border
   pixels do not justify synthesizing content or a flexible warp.
3. **Blur/interlace/generation:** haze, soft edges and streaked small flame
   structures limit precision. Interlacing/field blending, motion blur, scaling,
   sharpening and JPEG artifacts are plausible generation risks, not newly
   established properties of the original camera. A baseline JPEG or progressive
   output container does not exclude an interlaced antecedent. Preserve adjacent
   or duplicate candidate frames and possible multi-field ambiguity.
4. **Aspect and intensity:** targets are 720 x 478; the prior access copy is
   1620 x 1080 stored with SAR 8:9 and display 4:3. Neither a presumed two-row
   crop nor uniform/axis-specific scaling is established by those numbers.
   Explicitly test declared geometric possibilities; do not infer physical
   angles, area, temperatures or a colorimetric correction.
5. **Independence of fit and test:** fitting on flames then citing their good
   match is circular. Fix geometry using declared structural choices and test
   dynamic regions afterward. Conversely, static alignment alone is weak frame-
   time evidence because neighboring frames may share identical geometry.
6. **Texture failure is a result:** flat/hazy regions must be permitted to fail
   the parent method's prospective information and ambiguity gates. This review
   supplies no numeric threshold and has tested no matcher. Keep failed masks
   and do not retrofit a clean-looking region after seeing a desired frame.
7. **Clock ceiling:** a best or even convincing scene-content match identifies
   at most an access-copy frame/candidate interval under its transforms. It does
   not authenticate recording cadence, original frame number, a historical clock,
   NIST's clock assignment or compilation continuity. The earlier same-family
   interpretation and text-known candidate interval are disclosed prior knowledge.

These suggestions should support synthetic controls for repeated-window aliases,
different foreground/background motion, changed dynamic content, photometric
adjustment, blur and uninformative patches before real scores are used. They
are prospective tests to implement elsewhere, not tests passed by this arm.

No new video pixels were inspected. No measured frame correspondence, numerical
score, source-relative separation, historical timing error, thermometry,
structural consequence or mechanism ranking is asserted. Only this research
note was created; existing files, main/legal records, tools and agent privileges
were unchanged, with no installation, outreach, transmission or bridge action.
