# Independent TECOREP engineering-source reading

September 20, 2026 UTC. Research-only computational source review under
[PROTOCOL.md](PROTOCOL.md). Saved before reading root's new source-review note
or receiving its substantive findings. I previously located and read the two
participant HTML accounts in the source-lead task; that prior knowledge is
disclosed. This is a separate reading of the same participant publication,
not blind review, an independent historical witness or licensed engineering
validation. English descriptions below are my paraphrases of Japanese text,
assisted by the publication's English captions, not certified translations.

## Sources, actual coverage and integrity

The article is *140m の超高層ホテルにおけるテコレップシステムの適用*,
*Report of Taisei Technology Center*, No.46 (2013), article06. The overview
supplies the English title *A New Demolition System for a High-rise Hotel
"TECOREP SYSTEM"*. Authors are Hideki Ichihara, Makoto Kayashima, Manabu Ogura,
Takenobu Koga and Kiyoshi Yajima; the supplied affiliations are Taisei technical
development, structural design, construction-site and building-technology units.

| Admitted source | Exact identity | Coverage |
|---|---|---|
| [Official overview](https://www.taisei.co.jp/giken/report/2013_46/intro/C046_006.pdf), preserved as `C046_006-intro.pdf` | 1,817,040 bytes; SHA-256 `8ce337aaa3099a3b9a390d4f540a8306500d21961f382d3997aa7ffba9cd53ed` | Entire sole PDF page, including title, images, award table, three sections, affiliations and footer article06. |
| [Official full article](https://www.taisei.co.jp/giken/report/2013_46/paper/A046_006.pdf), preserved as `A046_006-paper.pdf` | 1,878,298 bytes; SHA-256 `a6a6fb65396ebf8ac4f7e147e40f08a178cbd89fabf97b90a1c4448352aaf4c8` | All eight PDF pages, printed06-1 through06-8; every section, Table1-2, Fig.1-8, Photo1-13, captions, author affiliations, awards and references. |

Actual visual coverage: **nine complete readable pages, nine displays, no
repeats or failed displays by this reviewer**. Used only the admitted MuPDF
render of the overview and `A046_006-mupdf-page01.png` through `page08.png`,
in page order. The earlier incomplete Poppler overview render was not viewed
or used by me. Root's acquisition/rendering log was read for provenance and
its excluded failures, not counted as my own execution.

PyMuPDF1.27.2.2 text extraction assisted reading; it did not replace page
inspection. Several diagram labels are small at the supplied resolution, so
no member-design inference depends on an uncertain tiny label. Headings,
captions and the decisive mechanics are readable in the complete pages and
surrounding text. The saved article HTML was checked for its explicit overview
and full-report links; its abstract is the same source family, not additional
corroboration. No source was browsed, acquired or downloaded by this reviewer.

Independent read-only checks ran with
`PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3`:
both admitted PDF byte counts/hashes and page counts passed; in-memory MuPDF
rendering at150dpi/RGB/no-alpha exactly matched the pixels in all nine supplied
PNG pages; no MuPDF warning text was emitted. Both PDF hashes were rechecked
unchanged after inspection. This verifies rendering/integrity, not the truth
of execution claims. No derived image or raw source was written.

Render SHA-256 identities checked during this review:

| Page | SHA-256 |
|---|---|
| Intro1 | `244c98828893f9d6069d1ea114107d79664c76a9dcb6d44bcbc4ff0483bcb25d` |
| Paper1 /06-1 | `3b8b94d9acb64805a4945beafde4cb03c3757aac702817f025d60c51bc3e6dc6` |
| Paper2 /06-2 | `ed06952fc14edde07be4800a60dc7868d274a451ee172d630408cab967e25a19` |
| Paper3 /06-3 | `795416c516a9e20323d0f4137490737a3eb90d7b9d99fb66963c774d6ec6934d` |
| Paper4 /06-4 | `eef270e3a666e118124ccfe5b570680903553cf3b54f5db0494aba1cb7819674` |
| Paper5 /06-5 | `42fa38a90cf9b422599d3bb9b8bd1072979934c04b7c22cb6cc7cccf2c9b57f6` |
| Paper6 /06-6 | `087c43f1c67759439fdc4feec16cd4923fe894a1f44d77a790d0dcbea21aa2ce` |
| Paper7 /06-7 | `5196e29a6d40ddad036e9bb01148aa78935130b582fd7b31993a06ac5094cb2a` |
| Paper8 /06-8 | `615e00872872d4a2566c7388c1c08e19049b0f3b39cddfeae3bb7ab4f2ef4bfa` |

## What the source establishes at its documentary level

The full paper is a participant engineering account of an executed staged
removal, with project-specific temporary works, reported construction dates,
mechanical explanations and site photographs. It is materially stronger than
a prospective demolition schedule or a method inferred from a distant video.
It still does not expose a complete independently checkable execution record.

| Topic and source pin | Source statement / depiction | Interpretation and ceiling |
|---|---|---|
| Building,06-1 §1/Table1/Photo1 | 138.9m; steel above ground, SRC below; 39 above-ground floors, one penthouse level and two basements; hotel use, closed March2011; 67,750m² total floor area. | Retain that level convention. Do not use the generic label steel high-rise as evidence of matched WTC7 load paths, connections, floor system, protection or damage. |
| General system,06-1 §2.1 through06-3 §2.3/Fig.1/Fig.4 | An upper enclosure reuses roof framing, carries handling equipment and is lowered as upper floors are dismantled. The general discussion allows one or two floors between lowerings. | A description of supported staged dismantling, not a whole-building fall. The general sequence and the overview's one-floor wording are not the precise cycle used at this hotel. |
| Deliberate reinforcement,06-4 §3.2/Fig.5-6 and06-5 | Retained roof/penthouse framing is reinforced with added diagonals; temporary columns, supported machinery floors, cranes and a surrounding screen are installed. | Preparation and temporary load paths are affirmative parts of this method. The cap is a modified construction system, not the untouched original roof naturally descending. No as-built member-capacity reproduction was performed. |
| Initial load transfer,06-3 §2.3/Fig.4 and06-7 §3.5 | The cap's load is moved from existing perimeter columns to temporary supports; hydraulic equipment is checked, and load, displacement and temporary-column strain are monitored. | The existing gravity system is deliberately supplemented/reconfigured. A claim of monitored support transfer is present; actual synchronized sensor records, calibrations and acceptance limits are not supplied. |
| Lowering mechanism,06-5 to06-6 §3.3/Fig.7/Photo3 | Alternating bearing/support arrangements maintain support while hydraulic strand-jack action lowers the temporary cap. | The mechanism describes controlled support exchange and descent, not an interval of unrestrained falling. This is a documentary mechanical distinction, not my verification of every executed stroke or support reaction. |
| Actual removal unit,06-5 §3.2;06-7 §3.5/Photo10 | Two upper floors are removed per ordinary cycle, with a lower screened safety floor; machinery performs crushing/dismantling. A typical two-floor cycle is eight days, also expressed as four days per floor. | Neither two floors per day nor one whole building drop. The first lowering is an adjustment and the terminal operations differ; do not multiply every reported lowering by two floors or impose uniform cycle timing. |
| Material handling,06-1 §2.1;06-4 to06-6 Fig.5-6/§3.2 | Dismantled materials are moved horizontally and lowered separately; lower levels provide sorting/handling areas. | Sequential removal changes the remaining structure and mass. Cap displacement cannot be treated as the center-of-mass trajectory of the original intact building. |

The paper reports a total cap weight of1,500ton on15 temporary columns and an
approximately100ton axial load per column (06-4 Fig.5;06-5 §3.2). The simple
division1,500/15=100 was independently checked. It is an average accounting
relation in the source's units, not evidence of identical measured reactions
or a demonstrated safety margin. The equipment photograph's rated capacity
must not be converted into a factor of safety using only this average.

## Execution and completion: do not collapse different milestones

The project account supplies retrospective dates missing from the earlier
HTML lead (06-3 §3.1/Table2,06-4 continuation,06-7 §3.5):

- Interior/asbestos work began in September2011; structural work began in
  June2012. Temporary system preparation occupied June-October2012.
- First jack-down is dated November13,2012. The paper reports17 lowerings
  in total and dates the final one May18,2013.
- The detailed final sequence distinguishes the **16th** lowering, when the
  exterior screen/scaffold reached ground, from the **17th**, when the roof
  structure was lowered inside the now self-supporting screen. The brief
  §3.1 ground-contact summary should not overwrite that component distinction;
  a separate date for the first screen-ground contact is not supplied.
- Equipment, temporary works and retained roof structure were then dismantled.
  The authors report completion of the work in **early July2013**, not the
  earlier HTML page's planned June2013 end and not simply May18.

These are author-reported execution dates, not an independently checked
completion certificate. The paper also reports21months overall and13months
for the structural-demolition scope; its §3.5 active method description starts
in November2012. These period labels include different phases. Do not present
any one as the duration of uninterrupted lowering or silently reconcile all
aggregate month counts into exact elapsed-day measurements.

The article documents interior/asbestos work, initial top/temporary preparation,
ordinary mechanical floor removal, special terminal lowerings and final
temporary-system/roof dismantling. Those are different phases within the
reported project. It does not furnish an exhaustive daily method inventory
for every residual or below-ground element. No explosive stage is reported for
this hotel; that is not an independently audited assertion of no explosives
anywhere in every phase. The broader concluding reference to overseas blasting
(06-8 §5) is a comparison with other methods, not an admission of blasting here.

## Evidence classes, validation and strongest overclaim risks

1. **Execution report versus independent validation.** The detailed narrative,
   drawings and project photographs support **B** for the attributed staged
   method/application claim. They are one participant source family. Corporate
   awards and a second reader do not establish independent structural safety,
   universal applicability or an independently authenticated execution history.
2. **Support and instrument claims versus raw measurements.** The text names
   performance checks and monitored quantities. It provides no usable load-time,
   displacement-time or strain-time arrays, complete instrument uncertainties,
   reaction distributions or independently repeatable safety calculation. Those
   stronger quantitative conclusions remain **D** in this review.
3. **Environmental analysis versus measured field outcomes.** The noise/dust
   comparisons are expressly labeled simulations (06-2 Fig.2-3). The stated
   20dB reduction and anticipated90%-plus dust suppression must not become my
   audited field measurements, an absolute-silence claim, or an acoustic test
   of a different demolition. Full numerical input/validation data are absent.
4. **Reported images versus calibrated historical motion.** Photo11 (06-8)
   has displacement labels ending at6.4m but no elapsed-time axis. Photo12 is
   a series of external views, not a continuous authenticated recording.
   Photo13's English caption explicitly calls it a **simulation of before and
   during demolition**. Do not count its composite appearance as another
   observed state, independent witness or calibrated trajectory. No acceleration,
   free-fall interval, footage authenticity or synchronization follows.
5. **One/two floors and exceptional cycles.** The overview's simplified
   one-floor wording is qualified by the full paper's general one-or-two-floor
   allowance and actual two-floor hotel cycle. Early/late operations are
   exceptional. A uniform17-times-two-floor reconstruction would exceed the
   record.
6. **Representativeness.** This is one purposively selected top-down example,
   not the definition of all demolition. Its slow supported work neither
   excludes a faster intentional-removal mechanism elsewhere nor supplies
   evidence that WTC7 used such a mechanism. A shared downward-moving roof
   outline cannot identify shared initiation or support mechanics.

The strongest contrary possibility is that the participant account simplifies
execution, omits contingencies or compresses different phase definitions.
Independent completion records, temporary-works/as-executed drawings and raw
monitoring logs could qualify or contradict those details. The paper's limits
do not justify discarding the positive documentary evidence that this staged
method was actually applied.

## Disposition and smallest next requirement

The source supports documentary coverage of a top-down high-rise removal
method with controlled temporary support and machine dismantling. It is an
unmatched mechanism example, not a WTC7 fire/intervention control or a cause
likelihood. Broad structural labels are available; detailed permanent load
paths, floor/connection properties, gravity loads, original condition/fire
protection, damage, execution variations, raw monitoring and original camera
records remain unverified.

For this bounded source-reading unit, stop at the attributed method account
and those limits. The smallest prerequisite for a stronger support-performance
claim is a project-specific as-executed support/monitoring record with actual
loads and displacement history; a motion comparison additionally needs
authenticated timing and camera records. The article's four references were
read as references only and not chased. No outreach, solver, media acquisition,
legal promotion or accepted Sherlock/Faraday state change is authorized by
this review. The only file written by this reviewer is this note.
