# Column 79: published directional restraint states

Research-only independent source review, September 13, 2026. The investigation
charter and this unit's protocol control. No released geometry, code, numerical
crosswalk/output, solver or source-supplied program was inspected or executed in
this source arm. This note does not authenticate part 179 as a physical column,
reconstruct a historical run, quantify restraint stiffness or rank collapse
causes. Main, canonical/legal files and preserved PDFs remain unchanged.
The inspected `PROTOCOL.md` hash was
`b7bcdf096a31ffca12a5c25f0f34cf2cc3247018502c9d6320a315f90f61d72d`.

## Result

**The published account is not complete simultaneous disconnection in every
direction.** At Column 79's modeled buckling initiation, NIST reports retained
north-side girders at Floors 8-12 and 14 that might resist northward movement,
although their erection bolts had failed. At Floor 14 it additionally reports
an attached girder to the west, between Columns 79 and 76. Neither statement
supplies a directional force-displacement law. NCSTAR 1-9 physical639/printed573;
NCSTAR 1-9A physical130/printed79.

The figures also show lower and upper support classes that a blanket
"unbraced between floors" paraphrase would erase. In particular, their red
"No support" circles at Floors 8-12 coexist with an explicit north-only lateral
restraint/vertical-support annotation. The text's **possible** resistance, the
figure's affirmative annotation and its generic color legend must be retained
together, not silently harmonized into zero stiffness or intact bilateral
connections.

A useful but incomplete coordinate convention is documented: in the published
LS-DYNA global results, **+Y is north and -Y is south** (1-9A physical139/printed88);
**X is east-west** (physical147/printed96). The inspected sources do not establish
the +X sign, coordinate origin, an exact floor-to-Z table or the identity and
transform linking those displayed model coordinates to released part 179.

## Preserved sources and actual coverage

| Primary PDF, existing local authority copy | Integrity and edition | Complete pages visually read in this pass |
|---|---|---|
| `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf` | 52,766,002 bytes; 797 pages; SHA-256 `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`; NIST NCSTAR 1-9, 2008 report | Physical638-641 = printed572-575 |
| `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf` | 26,952,697 bytes; 173 pages; SHA-256 `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`; NIST NCSTAR 1-9A, 2008 report | Physical80,110,130,132,139,147,158,172 = printed29,59,79,81,88,96,107,121 |

The initial selection was 1-9 physical639-641 and 1-9A physical130. Extensions
were made explicitly: 1-9 physical638 completes the sentence and timing context
that continue onto639; 1-9A physical132 supplies the Figure4-17 expressly cited
on130; the other six pages were selected from bounded axis/elevation lexical
leads. Those extensions were not prospectively selected at the unit's start.
All 12 pages were viewed completely, including headings, captions, legends,
axes, footnotes and continuing prose. Page640 is landscape; its complete page,
not just the column image, was inspected.

The source files have PDF encryption flags (`pypdf.is_encrypted=True`) but were
readable by the ordinary local PDF tools without supplying a password. No
decrypted/re-exported PDF was created. Selected-page marking checks found no
restrictive candidates, and none were observed on the full technical-page
views; this is bounded inspection, not blanket clearance of unreviewed pages.

Full renders are preserved in `/private/tmp/c79-source-review.37aZHJ/` as
`ncstar1-9-638.png` through `ncstar1-9-641.png`, and
`ncstar1-9a-080.png`, `-110.png`, `-130.png`, `-132.png`, `-139.png`,
`-147.png`, `-158.png`, `-172.png`. Bundled pypdf/Poppler were used; render
commands completed with exit0. Hashes were checked against the existing bytes,
not used as proof of historical executable/input identity.

## Floor/direction matrix at the reported Column 79 initiation state

State time is **-1.3 (14.7) s**, using NIST's collapse-reference (calculation-
reference) syntax. Figure12-44, 1-9 physical641/printed575, and the Column 79
panel of Figure4-17, 1-9A physical132/printed81, agree on the following colors.
They are publications of model states, not instrumented historical observations.

`U` means the individual directional contribution is not resolved by these
pages; it does **not** mean absent. `NG0` means the retained north-south girder
is expressly reported not to resist that movement direction; it is not an
independently measured zero for every possible load path. "No support shown"
is a diagram classification, not a numerical contact/stiffness result.

| Floor | Figure color/class | Northward movement | Eastward movement | Southward movement | Westward movement / west member | Other reported support detail |
|---|---|---|---|---|---|---|
| 2 | Green / full | U | U | U | U | Full schematic support; directional values not supplied |
| 3 | Green / full | U | U | U | U | Full schematic support; directional values not supplied |
| 4 | Yellow / partial | U | U | U | U | Partial class is not decomposed by direction |
| 5 | Yellow / partial | U | U | U | U | Partial class; floor debris accumulated here in the model |
| 6 | Red / no support | No support shown | Loss asserted in span | Loss asserted in span | Loss asserted in span | No north-only exception identified here |
| 7 | Red / no support | No support shown | Loss asserted in span | Loss asserted in span | Loss asserted in span | No north-only exception identified here |
| 8 | Red / no support, with north-only annotation | Possible resistance | NG0 | NG0 | NG0 | North girder still seated; vertical support annotated |
| 9 | Red / no support, with north-only annotation | Possible resistance | NG0 | NG0 | NG0 | North girder still seated; vertical support annotated |
| 10 | Red / no support, with north-only annotation | Possible resistance | NG0 | NG0 | NG0 | North girder still seated; vertical support annotated |
| 11 | Red / no support, with north-only annotation | Possible resistance | NG0 | NG0 | NG0 | North girder still seated; vertical support annotated |
| 12 | Red / no support, with north-only annotation | Possible resistance | NG0 | NG0 | NG0 | North girder still seated; vertical support annotated |
| 13 | Red / no support | No support shown | Loss asserted in span | Loss asserted in span | Loss asserted in span | Not included in the retained north-girder list |
| 14 | Yellow / partial | Possible resistance from north girder | NG0; total law U | NG0; total law U | Attached west girder gives reported restraint **from west**; law U | North seat has not walked off; west girder is C79-C76 |
| 15 | Green / full | U | U | U | U | Full schematic support; directional values not supplied |
| 16 | Green / full | U | U | U | U | Full schematic support; directional values not supplied |
| 17 | Green / full | U | U | U | U | Full schematic support; directional values not supplied |
| 18 | Green / full | U | U | U | U | Full schematic support; directional values not supplied |

Floors outside the figure's 2-18 extent are not assigned states in this matrix.
The matrix does not convert a qualitative "full" symbol into independently
specified four-direction springs, a yellow symbol into half capacity, or a red
symbol into a deleted architectural member.

### Exact qualifications behind the matrix

- **1-9 physical638-639, printed572-573:** the sentence spanning these pages
  calls Column79 laterally unsupported east-west and south between Floors5
  and14. It then states that north-direction support remained at Floors8-12
  and14 because the girders had not walked off their seats even though the
  erection bolts had failed. It says the resulting connections *possibly*
  prevented northward displacement, but not east, west or south displacement.
  The Floor14 west-girder attachment is an express additional qualification.
  The broad span wording is not a license to discard the partial endpoint
  classes at Floors5/14 or the residual north contact.
- **1-9A physical130/printed79:** identifies the north-south girder as spanning
  Columns44 and79. The phrase that these girders had "no lateral restraint"
  after bolt failure is immediately qualified by possible resistance to
  northward Column79 motion. Thus bolt restraint and possible contact/bearing
  resistance cannot be equated. The text reports easterly Column79 buckling.
- **Floor14 direction caution:** “to the west,” “from the west,” and an
  attached C79-C76 girder establish member location plus reported restraint.
  They do not by themselves establish a one-sided westward-only law, zero
  eastward force, bilateral stiffness, tensile capacity or a restraint magnitude.
- **1-9A physical80/printed29, STC subsection:** describes seats/stiffeners,
  clips and four construction-restraint bolts for the north side of Column79.
  It says the model used shell seat/clip plates tied to column and discrete
  bolt elements, with the same bolt properties/contact strategy as the STP
  connections. This is positive documentation of separate bolt and bearing/
  contact mechanisms, not a mapping of every released ID or its failed state.
- **1-9A physical110/printed59:** damage application to seated connections is
  described as removing discrete elements corresponding to failed bolts and
  applying specified seat/clip damage. The displayed Figure3-58 instead
  illustrates shear-connection damage levels; it must not silently supply an
  exact seated-connection state or a residual-contact law for Column79.

## Time, picture and counterevidence limits

1. **Model time is not event time without the reported alignment.** 1-9
   physical638 defines collapse-reference zero by the observed east-penthouse
   roofline kink and places the modeled kink at calculation16.0s. The reported
   pre-kink Column79 buckling follows from that analysis/alignment, not a direct
   historical observation of the interior column. The same page explicitly
   calls the following sequence events observed *in the analysis*.
2. **Different snapshots are not interchangeable.** Figure12-42 is labeled
   -6.5 (9.5)s. Figure12-43's cutaway is -0.5 (15.5)s, whereas Figure12-44
   supplies the Column79 initiation state at -1.3 (14.7)s. Figure4-17 presents
   Columns79,80,81 at their own different initiation times. It is not a
   simultaneous three-column restraint census. Figure12-43 plots resultant
   lateral displacements at selected floors and average vertical stress at
   Floor8, not every member's directional reaction history.
3. **Display removal is not structural deletion.** 1-9 physical638 and 1-9A
   physical132 explain that exterior and some tenant framing were removed
   from the views for visibility. Their resultant lateral displacement
   contours show absolute magnitudes and cannot establish motion sign;
   graphics may saturate at the chosen range. Apparent visual absence or
   contour color alone therefore cannot recover element deletion or force.
4. **A published nonbuckling case is retained.** 1-9 physical639 says an
   otherwise similarly loaded analysis using ANSYS damage at3.5h instead of
   4.0h did not buckle the interior columns. This is counterevidence to a
   blanket claim that every modeled southeast damage state necessarily
   triggered buckling, but does not independently reproduce either run or
   establish which state was historically correct.
5. **Alternative numerical runs are not independent historical witnesses.**
   The coordinate/elevation search also reached 1-9A physical158/172, which
   discuss the run without debris impact and, on172, prescribed removal of
   a Column79 segment between Floors11-13. These pages do not supply a
   coordinate/elevation table. The prescribed-removal result is not used to
   prove the fire-to-restraint-loss step. The no-impact run remains a distinct
   model case, not the Figure12-44 state automatically transferred to another run.

## Bounded coordinate/member crosswalk finding

The positive primary mappings are **physical column names** C44-C79 for the
retained north girder, C79-C76 for the Floor14 west girder, and the labeled floor
states above. The global-results prose assigns Y to north-south with its sign
and X to east-west. Neither a figure's axis glyph nor a named original drawing
establishes that released part179 uses the identical frame, origin, units,
elevations or whole-column scope. No release-specific join was sought in raw
payloads here, and the input arm's result is not assumed.

Lexical discovery returned page numbers only, before selecting full pages:

- In all173 pages of 1-9A, `coordinate` had no hit; `axis/axes` hit80;
  global/XYZ-direction patterns hit139/147; floor-elevation patterns
  hit49/110/158/172; Figure4-17 hit15/130/132. Page49 and the navigation-only
  hit15 were not substantively reviewed in this pass.
- In all797 pages of 1-9, `coordinate` hit333/337/339, XYZ-axis/direction
  patterns hit543-550, and the chosen floor-elevation pattern had no hit.
  These lexical hits were not followed; the directly relevant global-axis
  prose was located in 1-9A. No absence claim is made for those unreviewed
  pages or for diagrams/terms the lexical patterns could miss.

This is a finite useful source pass, not an assertion that the reports contain
no further crosswalk. It produced no floor-to-Z or +X assignment and no public
physical-column-to-effective-PID join. All12 full pages and unfollowed leads are
listed so another reader can distinguish positive finding from search ceiling.

## Decisive next restraint-state records

The next bridge is specific: for the **C44-C79 north seats at Floors8-12/14**
and **C79-C76 west attachment at Floor14**, obtain or resolve the physical
member-to-effective part/element/node mapping, exact floor elevations and
coordinate transform. Then join those members to the actual run's surviving
seat/clip/bolt states and their deletion/failure times at initiation, contact
surface pairing/normals/gaps/friction, relevant tied/rigid constraints, and
material/connection force-displacement definitions. The lower partial supports
at Floors4/5 and upper full-support classes also need explicit state data if
they are used as stability boundaries.

Directional reactions and tangent restraint behavior, with their load/temperature
and deformation state, would test whether residual north contact and the west
attachment were engaged, lost, weak or sufficient for a proposed stability
model. A single zero reaction does not prove zero available stiffness; sharing
a node does not prove adequate restraint; different node IDs do not rule out
contact/tied/rigid transfer. No values are filled in here. The full column's
section/splice/imperfection and axial-load state would additionally be required
before a physically supported stability calculation, not just an Euler-length
ratio or a graphic count of apparently missing floors.

**Claim strength:** A for what the pinned report text/figures state; model-
dependent for the reported calculated states; unresolved for numerical residual
stiffness, release-to-run identity and historical realization. The strongest
positive evidence is NIST's own explicit retention of direction-dependent
support mechanisms. The strongest limit is the missing join from that narrative
and schematic state to a fully specified, traceable mechanical state. Neither
gap nor modeled buckling proves deliberate intervention or concealment.

No network retrieval, outreach, raw production access, manual/modern-command
documentation extension, transmission, solver, canonical promotion or integration
edit occurred. Current main controls, charter, unit protocol and source-of-truth,
evidence-falsification and PDF skills were read and applied by this reviewer.

## Final report source/inference disposition

September 13, 2026: **bounded source/inference clearance, with the requested
wording correction confirmed in the actual report.** The initial complete
221-line report reviewed had SHA-256
`89d23384b67307914b3da8e8ee1679b47e038ea6bd1d1e20b7aedb9e5e261db9`.
Its line203 referred to "these selected pairs" before actual pairing was
established. The complete current 254-line report, SHA-256
`6b57c44b9e6b194b019a8a362cb5242ab1f3b69ec679907389382e5593d59fda`,
was read; line235 now correctly says **"candidate pairings under these
definitions"**. The NIST source claims remain consistent with the reviewed
primary pages and this note's original source-review body (pre-addendum hash
`0542e28b36fb3188dc1855d04f36b73ca5aa7783fc964550b03512643394cc1c`).

The Floor14 member-location versus motion-direction distinction, timing and
cutaway qualifications, 3.5-hour nonbuckling counterevidence, published axis
conventions, bolt-versus-bearing mechanisms and source/model/historical grades
are retained appropriately. The report challenges both complete-isolation
inferences and unsupported claims of adequate or historically verified
restraint. No further substantive NIST-source correction was identified.

This disposition relies on the 12 complete primary pages listed above, not
new source acquisition or new PDF views. It **does not certify** released-input
numbers, direct/contact topology, candidate-deletion joins, numerical outputs
or their reproducibility, or the added Version971/manual-method interpretations.
Those remain the separate numeric and manual arms' responsibilities. The report,
raw sources and main/canonical/legal files were not edited by this reviewer;
only this disposition was appended to the existing source-review note.
