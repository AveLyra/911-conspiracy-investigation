# A90 landline rerecordings: disclosed silence removal, differing time scopes and an index without receipts

November 1, 2026. Existing B129 / PD01–PD04 / FAA01–FAA04. Two previously catalog-only public records were acquired and read in full. This advances the source/copy and delivery-record inquiry; native audio, correction/receipt and later administrative outcomes remain open.

**The October 10, 2003 memorandum explicitly reports using “skip silence” to shorten rerecordings.** Its opening paragraph describes `0800–1200 local`, while the certification describes source data received `1200–1605 UTC`. Those stated intervals span four hours and four hours five minutes. Preserve both descriptions and their distinct labels. No actual audio gap, suppressed speech, elapsed-clock error or amount of removed material has been measured.

The associated four-page index supplies useful tab names. **It does not supply a delivery acknowledgment or identify each recording.** Its AAL11 and UAL175 tab letters differ, so joining records by letter alone would produce wrong associations. Repeated content labels also must not be silently deduplicated or counted as independent corroboration.

## Sources and reading scope

| Official released source | Acquisition, entity and SHA-256 | Actually read |
| --- | --- | --- |
| [A90-71 / NARA7599620](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/e-Other/5-A90-71-Memo-with-Re-Recordings.pdf) | 2026-11-01T20:30:50.234004+00:00; HTTP200; 40,254 bytes; `1a744e43b7a36e21cf01cd572acb18c73cc89a133fc5357604da0393fcdf1a66` | All1physical page, including scope, processing/certification and attachment footer |
| [A90-87 / NARA7599635](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/e-Other/5-A90-87-Index-of-Data-Provided-9-11-Commission.pdf) | 2026-11-01T20:30:50.237343+00:00; HTTP200; 101,936 bytes; `16c09e7d0b3d404d362d047e95c82773cf2dcc1aacedc6b19b53046ac602b1e9` | All4physical pages; all90visible table rows transcribed |

Download URLs came from the actual public catalog links. Each response entity and acquisition receipt is preserved unchanged, separately from research/public derivatives. These are official released scans, not independently authenticated native originals or signature/custody chains. The hash pins the bytes examined; it does not establish historical truth.

Five whole-page 2600-pixel images were read. Physical page numbers below are one-based. A90-87 physical1–2 are printed1of2/2of2; physical3 and4 are separate flight indexes each printed1of1. [SOURCE-PINS.json](SOURCE-PINS.json) records the exact inputs. [INDEX-ROWS.json](INDEX-ROWS.json) preserves all row labels and duplicates; only layout whitespace is simplified. No new OCR, hidden-layer extraction, redaction recovery, audio acquisition/listening/decoding, source editing or native clock fit occurred. Prior [A90-67/report context](https://github.com/AveLyra/911-conspiracy-investigation/blob/73cccf17d825861ba62161cd631454446bed550c/investigation/broader-evidence/faa-a90-original-copy-trail-2026-11-01/README.md) is reused, not a new acquisition or independent corroboration.

## What A90-71 actually reports

[A90-71 physical1](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/e-Other/5-A90-71-Memo-with-Re-Recordings.pdf#page=1), header and four body/footer locations:

| Location | Preserved assertion | What remains unverified |
| --- | --- | --- |
| Header/from/to | October10,2003; Manager,BostonTRACON,A90-1 → Manager,Evaluations and Investigation Staff,AAT-20 | Actual dispatch and recipient acknowledgment |
| Opening scope paragraph | Certified rerecordings attached from all landlines in TMU, OSIC and OS positions, September11,2001, `0800 to1200 local` | Actual channels, contents, enclosure completeness and which local-clock convention applies |
| Processing paragraph | “skip silence” was used; the memo describes skipping periods where nothing was said and compressing tape length | Actual settings, thresholds, time announcements and whether every relevant utterance survived processing |
| Certification paragraph | Data derived from Digital Voice Recording System data received September11,2001, `1200 UTC`–`1605 UTC` | Native export identity, source/date/timecode/coverage/correction history |
| Attachments footer | `TMU–1 tape`; `OSIC–2 tapes`; `OS–tape`, with no numeral visible for OS | A complete numeric attachment total and actual items received |

The two explicit numerals sum to **three**, plus an OS line with no visible numeric count. That is **not a verified three-tape total**. The singular word tape makes one OS tape, and therefore four overall, a plausible reading; it remains an inference rather than an explicit complete numeric manifest or proof of receipt. Three named position categories are not necessarily three channels. The one-page PDF contains the memorandum; no audio enclosure was acquired in this batch. That does not prove an enclosure was missing from the actual dispatch or from another released item.

The disclosed processing matters for reconstruction: playback elapsed time of a silence-shortened derivative cannot simply be treated as elapsed historical wall-clock time. That methodological implication is conditional on identifying an actual file as a descendant of these rerecordings. We have not identified or tested such a file here. The memo's explanation is affirmative contrary evidence to treating every shortened pause as covert splicing; it also does not independently prove that only silence was removed or that every utterance was preserved.

**Required discriminating records/tests:** continuous original/channel exports, each certified-copy identifier, preparation/export logs and silence settings, retained time announcements/timecode, custody and actual enclosures. A later comparison should map each surviving speech interval to the original, report skipped intervals and uncertainty, and anchor clocks independently. No such experiment has been performed in this unit.

## Time descriptions: preserve the five-minute span difference

Both descriptions refer to September11,2001, but the text labels their clocks and scopes differently:

| Description | Printed endpoints and clock label | Arithmetic within that description |
| --- | --- | --- |
| Opening paragraph's attached-copy scope | `0800`–`1200`, **local** | 240 minutes |
| Certification's source-data-received scope | `1200`–`1605`, **UTC** | 245 minutes |

The difference between those stated spans is **five minutes**. No timezone assumption is needed to subtract endpoints within each same-day description. If one hypothesizes that both pairs describe exactly the same boundaries under one constant clock offset, the starts require a numeric offset of240minutes and the ends245minutes. That conditional hypothesis does not make both endpoint pairs exactly equal. It does **not** measure clock drift, a five-minute gap, the silence-removal amount, or a concealed interval.

Untested possibilities include a nominal requested window versus a longer actual source-data boundary, extra lead-in/out, drafting error, or genuinely different described coverage. None is adopted. Native copy/export records, contemporaneous instructions and the recordings could distinguish them. Do not relabel local as a specific timezone, substitute a preferred endpoint, normalize1605to1600, or apply an offset to other evidence.

## Comparison with October8A90-67

[The held October8memorandum](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/4-UAL-175/e-Other/4-A90-67-Memo-Certifying-Re-recording.pdf#page=1) reports a certified ID/SL rerecording for `1209–1228 UTC`; broader DATs held at BostonTRACON but then unreproducible due to equipment problems; and a certification based on `DVRS` data received. October10A90-71 names **TMU/OSIC/OS landlines**, a different scope, and spells out **Digital Voice Recording System** as its source.

These are two dated source accounts. Same facility, two-day proximity, similar signatures or the shared acronym do not prove that the same original was used, the DAT problem was repaired, or the October8statement was false. Conversely, the later reported ability to make some rerecordings cannot establish that all source media were readable. Both assertions and their distinctions remain; copy-generation history, equipment records and native identifiers are missing. The earlier source and published assessment remain unchanged.

## What the four-page A90-87 index supplies

[Physical1–2](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/e-Other/5-A90-87-Index-of-Data-Provided-9-11-Commission.pdf#page=1): BostonTRACON(A90), numbered **TAB1–65**, with65visible rows. Physical1has1–36;physical2has37–65. It includes advisories, directives, GENOT/NOTAM entries, logs, procedures, security, press and stress-related material. These are index labels; no underlying item contents were acquired from a title alone.

[Physical3](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/e-Other/5-A90-87-Index-of-Data-Provided-9-11-Commission.pdf#page=3): BostonTRACON AccidentPackage–**AAL11**, **A–M**,13category rows. [Physical4](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/e-Other/5-A90-87-Index-of-Data-Provided-9-11-Commission.pdf#page=4): BostonTRACON **UAL175**, **A–L**,12category rows. This totals **90index rows across three scopes**, not90documents, tapes, pages, independent pieces of evidence or successfully delivered items. TABnumbers are a package-organizing namespace, not the NARA folder suffix in A90-87.

| Category or letter | AAL11 physical3 | UAL175 physical4 | Join implication |
| --- | --- | --- | --- |
| H | ATCSCC East Area Log | FOIA Freedom of Information Act | Same letter has different content |
| I | Fax Transmission Verification Reports | Headquarters Guidance and Communications | Same letter has different content |
| Headquarters Guidance and Communications | J | I | Same category has different letters |
| Flight Progress Strips | K | J | Same category has different letters |
| Certified Re-recordings | L | K | Same category has different letters |
| RADAR Data | M | L | Same category has different letters |

The two flight indexes share11literal category labels. AAL11 additionally lists ATCSCCEastAreaLog and FaxTransmissionVerificationReports; UAL175 additionally lists FOIAFreedomofInformationAct. That is a bounded difference in index descriptions, not proof one investigation lacked other records or one packet was defective. A listed fax-verification category is a concrete retrieval lead, not itself a retrieved transmission report or proof of these particular audio deliveries.

Eight content labels recur within the65numbered rows, which have55distinct literal labels after layout-space transcription. Examples: `Genot1/36` at10/13, `NOTAM1/0989` at33/35/36/39, and `ORDER7110.65M` at44/46. Keep each row and tab. The same title could refer to copies, acknowledgments, distinct versions or different enclosures; those are untested possibilities. No item bytes have been joined or deduplicated. Source spelling such as `Procudures General` at57 remains in the row data; it is not a substantive suspicious finding.

**What the index does not prove:** the four pages have no signed recipient acknowledgment, delivery date, tape barcode/serial/hash, copy-to-original crosswalk, per-recording channel/time list or enclosure receipt. Its catalog title says data provided, but a catalog description cannot independently certify each item was sent and received. Nor does the absence of those fields on an index establish that proof of delivery never existed. This source improves package navigation while leaving the receipt and native-content tests open.

## Outstanding inputs and publication limits

[OPEN-TODOS.md](OPEN-TODOS.md) preserves actual audio/copy manifests, blank OS count, source/copy boundary definitions, silence settings, original-to-rerecording joins, index-to-item mapping, signed delivery/receipt and applicable procedures as distinct dependencies. A90-74/98/99remain catalog-only targets from the earlier review. Available public work can continue there or in the telephone and steel original-record queues without rerunning these completed five page readings.

The actual corrected May2003QFR and acknowledgment, signed action/no-action determination, and separate OIGrecommendation response/implementation/closure remain unacquired. AAT-20routing, a2003audio memorandum, and an index do not substitute for those outcomes. All5work-plan tracks/18substantive criteria remain open/partial, with technical evaluation and independent-audit ownership unchanged. Existing Keyton/zero-duration mirrors and completed decoder tests retain their actual acquired/performed status; native provenance/routing/configuration/clock questions remain open.

[OBSERVATIONS.json](OBSERVATIONS.json) separates source reports, arithmetic, interpretations and unperformed tests. [verify.py](verify.py) checks declared bytes and reproduces the endpoint/row-label accounting; that does not establish native authenticity, speech retention, historical cause or acceptance of the substantive goal. [CHECKLIST.md](CHECKLIST.md) and [REVISION.diff](REVISION.diff) preserve requirements and exact new text. Original sources and prior publications remain unchanged. No outreach, fee, request, mailbox/private-case use, litigation edit, deletion, private push or history rewrite occurred.
