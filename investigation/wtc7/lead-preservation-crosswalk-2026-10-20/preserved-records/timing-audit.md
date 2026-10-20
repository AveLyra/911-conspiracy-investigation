# WTC 7 animation versions and timing: preserved discrepancies

October 16, 2026. Public-source research, not a collapse-cause finding or a court
filing. New observations are distinguished from rechecked earlier findings.
Existing reports, captured bytes, conflicting values and history are unchanged.

## What this adds

The strongest new source-visible discrepancy is **Figure 12–68's caption versus
its own panel clocks**. The strongest new validation qualification is that the
FAQ's equal 12.9-second intervals do not represent two directly observed
interior-failure timestamps. The animation work adds a reproducible, recursive
binary comparison of the preserved player files—not the missing video payloads.

None of these findings establishes deliberate editing, fabrication, demolition,
or concealment. They identify specific records and assumptions to test. An
innocent editorial or player-maintenance explanation remains possible; it is
not adopted as the established explanation.

### 1. New: Figure 12–68 contains incompatible timing descriptions

[NCSTAR 1-9](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf#page=659),
printed 593 / PDF page 659, gives:

| Location on the same figure | Relative times (s) | Parenthetical times (s) | Subtracted clock offset (s) |
| --- | --- | --- | --- |
| Three panel labels | 6.2; 7.4; 8.5 | 19.5; 20.7; 21.8 | 13.3 for each pair |
| Caption endpoints | 5.5 to 7.8 | 21.5 to 23.8 | 16.0 for both endpoints |

Thus the caption's relative endpoints are 0.7 s earlier than the displayed
endpoint labels, while its parenthetical endpoints are 2.0 s later. These are
different discrepancies from the previously reported one-second label conflict
on printed 591–592. They cannot all be made the same clock merely by subtracting
one common reference. No preferred value is selected.

On that same page, Figure 12–69's panels and caption do agree with a 13.3 s
offset: 10.8 (24.1), 13.5 (26.8), 15.5 (28.8). That comparison preserves a
nearby internally consistent control. The two figures' captions also give
negative endpoints for **resultant lateral displacement**, whereas the displayed
legends show zero to positive 0.5 m. This extends, rather than replaces, the
earlier caption/legend observations on printed 592. It does not determine a
direction of physical motion from a resultant magnitude.

**Why interesting:** a frame-to-run/time/display-variable crosswalk is necessary
before treating these figures or an animation derived from them as quantitative
validation. A copied caption or reference-label error could account for the
conflict. No source manuscript, native output or rendering log was acquired to
test that explanation, and no solver defect follows from the caption alone.

### 2. New qualification: the FAQ's 12.9-second equality has a proxy endpoint

[NIST's FAQ, Q25](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation)
says measured and predicted intervals from floor failures around Column 79 to
initial north-face roofline motion were both 12.9 s. The numbers in
[NCSTAR 1A](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861610#page=85),
printed 42–44 / Table 3–1, do yield:

- Observation column: `6.9 − (approximately −6.0) = approximately 12.9 s`.
- Debris-model column: `6.3 − (−6.6) = 12.9 s` using the printed precision.

But §3.5.1 describes the observed early event as exterior east-west vibration
(reported amplitude ±2 in.), not a direct view of the hidden floor failures.
The causal identification of that vibration with interior cascading failure is
an inference being corroborated. The east-penthouse descent is also deliberately
set to zero to align the comparison. Treating the interval equality as two
independently measured interior-to-exterior failure histories would overstate it.

**What holds and what does not:** the arithmetic agreement is real at the
published precision. It is not a falsified subtraction, proof of fitting, a
statistical goodness-of-fit test, or evidence that the inferred floor failures
did not occur. NIST itself discloses in §3.5 that some photographic observations
were used to direct simulations; that disclosure weighs against claiming an
undisclosed use of every visual input. This audit does not establish which
additional observables were held out from model development.

NIST also expressly limits later-stage fidelity in §3.5.2: uncertainties grow
after global collapse starts, and it describes movement after the depicted kink
as beyond the model's reliable physics. That acknowledgment is important contrary
evidence to an accusation that NIST promised an accurate reconstruction of every
late frame. It does not remove the need to identify which earlier predictions
were independently validated or explain inconsistent printed frame clocks.

**Records that could discriminate:** original vibration/video measurements,
event-identification and synchronization worksheets, uncertainties, calibration
records, validation criteria and the particular run histories compared. No new
historical video timing is claimed here.

### 3. Rechecked: other event times do not all match

The same Table 3–1 supplies these signed differences, computed from its printed
numbers as **model minus reported observation**:

| Named observable | With debris damage (s) | Without debris damage (s) |
| --- | --- | --- |
| East penthouse below roofline | +0.4; +0.7 | +0.3; +0.6 |
| Initial north-face roofline motion, eastern section | −0.6 | +2.9 |
| East end of screenwall below roofline | −1.2; −0.8 | +0.2; +0.7 |
| West penthouse below roofline | −2.4; −2.0 | +1.3; +1.6 |

Paired entries denote **different views of a model**, not separate statistical
replications, an uncertainty interval or two independently timed observations.
The west-penthouse comparison remains 9.3 s reported versus 6.9/7.3 s in the
debris model. It has not been replaced by our own measurement. Bracketing an
observed value with different damage scenarios is not the same as a single
validated run predicting it accurately. Conversely, these residuals alone do
not establish that either scenario is impossible.

The FAQ describes exterior-drop onset as within approximately half a second;
the printed debris-model table difference is 0.6 s. Preserve both descriptions:
the qualifier and unknown timing uncertainty prevent treating the 0.1 s excess
over half a second as a demonstrated material falsehood. Printed 42 also gives
modeled floor-cascade onset as −6.5 s, while the table gives −6.6 s. That small
prose/table difference is retained, without selecting one or diagnosing its cause.

The previously documented `3.2 (17.5)` label implies 14.3 s, while five adjacent
pairs and the stated no-debris reference imply 13.3 s. The surrounding prose
also calls 17.5 s 4.2 s after the reference. The present arithmetic retains all
of them; it does not repair the label.

### 4. New binary detail: animation players changed, missing videos remain missing

The four held SWFs were freshly hash-checked against the earlier acquisition
record and parsed without executing ActionScript. Both root and nested sprite
tag streams were inspected. [Full output](swf-structure-run01.json) and
[paired comparisons](comparisons-run01.json) preserve byte offsets and hashes.

| Field | August 29 capture pair | September 7 capture pair |
| --- | --- | --- |
| SWF version | 9 | 8 |
| Header frame rate | 12 | 30 |
| Canvas from signed RECT bounds, pixels | **355 × 300** | **464 × 368** |
| Declared root frames / root ShowFrame tags | 1 / 1 | 1 / 1 |
| Root tags | 61 | 130 |
| Recursive standard VideoFrame tags | **0** | **0** |
| DefineVideoStream tags | 0 | **2, each declaring 160 × 120 and zero frames** |
| Identical corresponding root payloads within CU/whole pair | **59 of 61** | **129 of 130** |

The canvas, recursive scan, video declarations and positional payload comparison
are new detail beyond the earlier top-level wrapper review. The 12/30 rate
change, version change and media filenames were already reported.

In August, only the DoABC payload and tag 76 payload differ between CU and
whole-building players at corresponding root positions. In September, only one
DoAction payload differs. This is a byte-comparison result, not a semantic
disassembly or proof that only a filename changed. The August ABC string pools
also name the separately referenced **`SkinUnderPlayStopSeekCaptionVol.swf`**,
an additional exact asset locator. Names for seek, source, duration and autoplay
are present; their presence alone does not establish active runtime settings.

**Important separation:** wrapper canvas size is not necessarily video-raster
size. Wrapper header rate is not established as the external FLV's frame rate,
presentation speed or structural-simulation clock. The zero-frame declarations
do not prove zero-duration video. No standard VideoFrame payload was found in
the inspected root/sprite hierarchies; opaque or unknown tag contents and full
ActionScript semantics were not validated. Neither the FLV contents nor the
rendering behavior has been reconstructed here.

Ordinary player re-export, changed Flash compatibility or controls could
produce wrapper changes without changing animation frames. Substituted external
content is another untested hypothesis, not positively indicated by these
player bytes. Discriminating evidence is the exact external FLVs, wrapper/skin
assets, HTTP/publication version records, source run and render/export manifest.
The archive capture dates are acquisition/index labels, not proven edit dates.

The Adobe-authored specification was located at a public mirror, but direct
retrieval returned 403 and the browser fetch failed. This limitation is recorded
in the source manifest. The parser is inspectable and synthetically tested;
it is not certified against a complete independently acquired specification or
validated in a Flash runtime. See the [Library of Congress format
record](https://www.loc.gov/preservation/digital/formats/fdd/fdd000629.shtml)
and [identified specification mirror](https://www.mobilefish.com/download/flash/swf_file_format_spec_v9.pdf).

### 5. New source-pinned records lead: NIST identifies a video intake database

The freshly captured FAQ Q26 states that an NBC copy already lacked the
penthouse segment when received, was copied without NIST editing, and that
videos were logged in a database with restricted investigator access. Those are
specific public agency representations, not proof of their opposite.

The corresponding existing database entry, intake identifier, original NBC
receipt/copy, derivative/export records and preservation checks are a concrete
source-chain lead. A checksum may or may not have been maintained: do not invent
one or assume a byte-for-byte copy claim promises one. **No contrary NBC original
or discrepant database record was found by this audit.** This historical camera
footage is distinct from the modeled animation and must not be conflated with it.

### 6. New acquisition: the player-skin path has matching archive-index labels

Three new exact-path public CDX requests succeeded on October 16. The video-path
responses reproduce the earlier 2011 classifications and add a fresh acquisition
record. The newly probed skin path supplies an additional asset comparison:

| Asset | 2011 capture dates returned | Status / MIME labels | CDX length values |
| --- | --- | --- | --- |
| `CU animation.flv` | April 27; May 12; July 4 | 200 / text/html | 4107; 4107; 4107 |
| `whole building animation.flv` | April 27; May 12; July 4 | 200 / text/html | 4112; 4113; 4113 |
| `SkinUnderPlayStopSeekCaptionVol.swf` | April 27; May 12; July 4 | 200 / text/html | 4117; 4117; 4121 |

All nine rows report the same CDX digest label:
`5QS37AMPA6EYJE6CM34M2AJWR5PWXQSX`. This is an **index-reported association
across a player asset and both named video assets**, not a new payload hash or
proof that the corresponding archived response bodies are byte-identical.
The actual response JSON values, request URLs, acquisition UTC times and response
hashes are preserved in [archive-index-probes-2026-10-16.json](archive-index-probes-2026-10-16.json).
The video queries also returned later 2016/2025 HTML/redirect entries; none of
these returned rows identifies a recovered FLV payload.

Common fallback/error handling is a testable possibility, not an adopted cause.
These CDX lengths are not assumed to count the same representation as the old
13,113-byte browser-decoded replay entities. No archived ARC/WARC record or fresh
identity-replay body was retrieved in this check. The earlier access failures
and index/replay discrepancies remain preserved; present index access does not
retroactively change those observations or establish why the payloads are absent.

## Potential legal relevance: concrete records, not global impeachment

These are generic public records-law observations, not a proposed pleading,
private litigation strategy, narrowed request, discovery concession or outgoing
request. Scientific verification and FOIA compliance are different questions.

| Finding or representation | Potentially useful existing records | Necessary limitation |
| --- | --- | --- |
| Caption/panel and clock conflicts | Figure-to-case/time crosswalk, rendering scripts, source plots and applicable corrections | A publication defect is not itself a false search declaration or invalid exemption. |
| Proxy endpoint, forced reference and event residuals | Original timing/validation worksheets, run IDs, holdout/calibration criteria and retained uncertainty analysis | Tests the precision and scope of a validation claim; it does not require FOIA to create a new analysis. |
| Changed wrappers and exact external asset names | Publication inventory, asset/version mapping and export records | Request scope and agency possession/control must be established; unavailable archive replays do not prove agency deletion. |
| FAQ says originals were preserved and logged | Existing intake/database/export/preservation records for a specifically identified video | A challenge to that representation needs a concrete contrary record; none is supplied here. |
| FAQ Q7 invokes validation to explain safety-sensitive withholding | Existing validation documentation and a record-specific explanation of the claimed connection | Disputing validation is not sufficient by itself to defeat a statutory public-safety withholding. |

The strongest general legal route is a **specific evidentiary contradiction or
positive lead bearing on search, record classification, withheld categories or
segregability**, not an assertion that any model disagreement makes all agency
representations untrustworthy. For example, [Shapiro v. DOJ, No. 18-5123
(D.C. Cir. 2019), pp. 4–6](https://www.govinfo.gov/content/pkg/USCOURTS-caDC-18-05123/pdf/USCOURTS-caDC-18-05123-0.pdf)
required nonconclusory explanations for particular records previously identified
as responsive and for claimed destruction. It allowed supplemental evidence on
remand; it did not establish that every preliminary search hit must be released.
That decision concerns the FBI and is an analogy, not a holding about these NIST
files or automatically controlling in every jurisdiction.

Contrary authority is substantial. [Quick v. Commerce, 775 F. Supp. 2d 174
(D.D.C. 2011), pp. 7–10](https://www.govinfo.gov/content/pkg/USCOURTS-dcd-1_09-cv-02064/pdf/USCOURTS-dcd-1_09-cv-02064-0.pdf)
upheld NIST's search, Exemption 3 withholding and segregability analysis on its
record, as well as noting concessions. Calling it merely an unopposed case
would omit its merits rulings. [Cole v. Copan, No. 19-cv-1182, ECF 20
(D.D.C. Nov. 30, 2020), pp. 7–16](https://law.justia.com/cases/federal/district-courts/district-of-columbia/dcdce/1:2019cv01182/206571/20/)
upheld NIST's interpretation of a Column 79 input-data/analyses request, search,
withholding and segregability; the court also rejected requiring creation of new
screenshots. That opinion is court-authored text at a third-party mirror. Neither
decision can simply be discarded because later research questions the model.

[15 U.S.C. §7306(d)](https://www.law.cornell.edu/uscode/text/15/7306) protects
information subject to the statutory public-safety finding. A questionable
caption does not eliminate that law. Conversely, the law and these decisions
do not scientifically validate every rendering, authenticate every circulating
copy or establish that every separate publication/provenance record falls within
the same withholding rationale. Those record-specific questions remain open.

## Preserved earlier leads and boundaries

The [earlier animation review](../../../research/faraday-wtc7-model-compare/review/animation-version-comparison-2026-10-04.md),
[AVI header audit](../../../research/faraday-wtc7-model-compare/review/avi-container-stream-header-audit-2026-10-04.md),
[CDX/replay discrepancy](../wayback-replay-capture-2026-10-09/cdx-replay-layer-discrepancy-2026-10-10.md)
and [prior clock/caption review](../causal-chain-synthesis/stable-control-2026-10-05/report.md)
remain preserved, including their caveats. The old report's characterization of
archive HTML as an original NIST error page is not newly authenticated here;
the later replay-layer limitation must travel with it. That is a limitation of
our earlier account, not evidence of NIST misconduct.

No AVI-header discrepancy, Ogg boundary candidate, archive index/replay conflict,
or animation-source caption difference is adjudicated by this run. The old
8.48/8.76-second exploratory alignment is not retuned or promoted to validation.
No actual FLV, original WARC response, native solver result, independent video
trajectory, witness evidence, or evidence linking a person to wrongdoing was
acquired. These gaps limit conclusions; they are not themselves operation evidence.

## Verification and provenance

See [protocol](PROTOCOL.md), [literal timing transcription](timing-observations.json),
[source manifest](sources.json), [execution and review](VERIFICATION.md),
[static parser](audit_swf.py), [arithmetic/comparison code](compare_records.py),
and [current FAQ capture](nist-faq-capture-2026-10-16.json).
Two repeated executions produced byte-identical parser outputs and
byte-identical comparison outputs. Sixteen tests passed, including synthetic
malformed-input/nested-video controls and arithmetic/preservation checks. These
are reproducibility checks on this audit, not a rerun of NIST's building model.
