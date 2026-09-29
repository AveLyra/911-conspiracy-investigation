# Column 79 contact geometry: bounded primary-source crosswalk

Research-only independent source review, September 13, 2026. This note follows
the previously uninspected lexical leads; it is new coverage, not a claim that
the preceding restraint audit had already read them. The charter and current
unit protocol control. Main, raw/canonical/legal records, admitted PDFs and the
prior source review remain unchanged. No released numerical payload, code,
geometry output, manual method or solver result was inspected by this arm.

## Result and claim boundary

The pages supply useful **published ANSYS model mappings**, but no authenticated
join to released PID179 coordinates:

- Figure 11-9 orients an ANSYS 16-story plan with north upward, a Y glyph upward
  and an X glyph rightward. Reading that glyph with the north arrow supports
  an eastward X / northward Y orientation **for the illustrated ANSYS plan**.
  This is a figure-based interpretation, not explicit prose authenticating the
  released LS-DYNA coordinate frame. Physical542/printed476.
- The ANSYS boundary-condition description expressly distinguishes global
  x/y lateral displacement from global z vertical displacement. It supplies
  no origin, signed Z direction, absolute elevations or transfer transform.
  Physical550/printed484, section11.2.7.
- The seated-connection subsection and Figure11-15 specifically name Column79
  and identify connection components and local x/z directions. They distinguish
  bolt/weld failure, subsequent contact, and eventual walk-off/loss of vertical
  support. Physical548-549/printed482-483. This is not an element/part-ID crosswalk
  or an initialized contact-pair record for the released global model.

**No floor-to-Z table, coordinate origin, released unit convention or physical
member-to-effective-PID179 join was found in these 16 fully inspected pages.**
This is a bounded nonfinding, not a statement that no such record exists in
the reports or elsewhere. No floor identity or unit is assigned by numerical
resemblance, a schematic dimension, a model label or a figure's apparent shape.

## Controls, preserved bytes and exact coverage

Main AGENTS.md, WORKFLOW.md and START-HERE.md were read. The worktree charter,
latest STATUS C79 handoff, prior source review and current unit protocol were
read as controls/prior knowledge, not independent physical evidence. Pins:

- `CHARTER.md`: SHA-256
  `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
- `c79-contact-geometry/PROTOCOL.md`: SHA-256
  `b18a519ba88e7d61d331d821232e269c3e3f9a5e690a3e25e3e108e1e70df1ea`.
- Prior `c79-restraint-audit/source-review.md`: SHA-256
  `13151e5174b402d7d37557a37f47560cfeeca54b785ee1f220ac44c5aa8d0218`.

| Existing primary PDF | Rechecked source integrity | New complete visual coverage in this pass |
|---|---|---|
| `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf` | NIST NCSTAR1-9, 2008; 52,766,002 bytes; 797 pages; SHA-256 `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` | Physical333-334 = printed289-290; 337 =293; 339 =295; 542-551 =476-485 |
| `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf` | NIST NCSTAR1-9A, 2008; 26,952,697 bytes; 173 pages; SHA-256 `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4` | Physical49-50 = printedxlvi-xlvii |

The original selection was 1-9 physical333/337/339/543-550 and 1-9A49: 12 pages.
Four immediate extensions were declared during review: 1-9 physical334 completes
333's sentence; 542 supplies the fin-connection introduction immediately before
Figure11-10 and includes the useful plan; 551 completes the structural-load list
and shows its referenced figure; 1-9A50 completes49's no-impact-run prose. No
single physical-to-printed offset applies across the combined report or front
matter; the printed numbers above were checked on the actual pages.

Full-page renders, including headings, captions, diagrams, legends and footers,
were inspected at `/private/tmp/c79-crosswalk-review.D7bsAY/`:
`ncstar1-9-333.png`, `-334.png`, `-337.png`, `-339.png`, `-542.png` through
`-551.png`, and `ncstar1-9a-049.png`, `-050.png`. All 16 pages were rendered
with the bundled Poppler 26.05.0 at 140 dpi; both render batches completed exit 0.
The bundled Python 3.12.14/pypdf 6.10.0 supported bounded marking checks.

Both PDFs have encryption flags but were readable with ordinary local tools
without supplying a password. No decrypted/re-exported PDF was made. The only
selected-page lexical marking candidate was `signature` on1-9 physical333.
A first contextual classifier did not resolve it; expanded engineering-context
checks and the complete page view established that it referred to an audio
signature, not a signature block. No restrictive marking was observed in the
16 complete technical-page views. This is not blanket clearance of other pages.

## Page-level findings and limitations

| Physical / printed page | Actual subject and positive information | Crosswalk limit |
|---|---|---|
| 1-9 333-334 /289-290 | Section5.7.5 concerns audio characteristics and synchronization of video soundtracks; section5.7.6/Table5-3 summarizes visual collapse observations. The word `coordinate` is not a spatial-coordinate definition. | No model frame, origin, elevation table or released-ID join. The audio/visual merits were not independently tested here. |
| 1-9 337 /293 | Chapter6 sections6.1-6.2 discuss emergency-response context/data gathering. Coordination refers to agencies and response. | Named occupancy floors and geographic location are not numerical floor elevations or a mesh frame. |
| 1-9 339 /295 | Floor-warden/evacuation organization and emergency activity. | The coordinate-related lead concerns human coordination, not geometry. |
| 1-9 542 /476 | Figure11-9, area in which connection failures were modeled; ANSYS16-story plan, north arrow, X/Y glyph and labels C73/C76/C78. The surrounding prose distinguishes local-failure ANSYS modeling from continuation in a47-story LS-DYNA model. | Positive illustrated ANSYS orientation and named-column locations, but no origin, coordinate values, particular floor elevation, released node/element/PID identity or cross-model transform. |
| 1-9 543-545 /477-479 | Figures11-10/11-11/11-12: fin, knife and header connection analytical models; local x/z arrows and ANSYS beam/break/contact roles. | Local element directions cannot silently become global geographic directions. These other connection types are not interchangeable with the C79 seated connection. |
| 1-9 545-546 /479-480 | SWC connection subsection and Figure11-13; seat/web-clip mechanisms, switching/control/contact elements and walk-off. | SWC travel/model details do not establish C79's connection properties or released cards. |
| 1-9 546-548 /480-482 | Exterior seated-connection subsection and Figure11-14; north/south/east exterior connection distinctions, slip/contact/restraint/walk-off modeling. | Exterior-column flange restraint and exterior walk-off distances must not be assigned to C79. |
| 1-9 548-549 /482-483 | C79/C81 seated-connection subsection and Figure11-15. The C79 model has local x along the illustrated member away from the column and local z upward; the C81 girder is stated to join at a different angle. Top-clip, seat, bolt, weld, rigid/elastic beam, slip, contact and control roles are labeled. | A specific physical connection type is identified, but no release-specific element namespace, part number, floor placement or force/state history is supplied. The local frame cannot be merged with the plan frame without a member orientation join. |
| 1-9 549-550 /483-484 | Shear-stud model/Figure11-16 separates break-element shear failure from slab-to-beam contact and continuing gravity transfer. Sections11.2.6-11.2.7 identify substructuring and ANSYS boundary conditions; global z is vertical, x/y lateral. | Contact surviving a modeled connection failure is a represented mechanism, not proof of any released interface's actual state or capacity. “Elevation View” means a side-view drawing, not an absolute-elevation datum. |
| 1-9 551 /485 | Figure11-17 design-load criteria and continuation of structural loading. | Floor labels in a loading schedule do not supply floor-to-Z positions. No load arithmetic or input verification was performed. |
| 1-9A 49-50 /xlvi-xlvii | Executive-summary TableE-2 separates observations from analysis, with observed Column79 buckling marked N/A. It distinguishes the3.5h noninitiating model case, the no-impact case and the prescribed-column-removal case. | The floor-elevation lexical hit is qualitative discussion of buckling locations, not an elevation table. Separate model runs are not historical observations or a coordinate-transfer record. |

### C79-specific mechanism: retain the source's qualifications

Physical548's C79/C81 subsection describes top-clip tension failure or bolt
shear followed by walk-off; it also repeats a narrower bolt-shear-then-walk-off
description. Its final paragraph specifies seat-bolt shear, top-clip bolt shear
or weld failure, and actual beam walk-off before loss of support. Thus neither
the broad phrase about prerequisite bolt/weld failure nor the shorter sequence
should be turned into a claim that every bolt and every weld must fail, or that
the first bolt failure instantly eliminates all bearing/contact resistance.

The same page describes node-to-node beam/column contact with an initial gap,
slotted holes at the top clip and standard holes at the bottom seat. It gives
model walk-off travel as 6.25 in along the beam axis and 5.5 in lateral to the beam;
axial walk-off used a control element, whereas lateral walk-off was monitored
during analysis. These are source-reported ANSYS connection assumptions, not
adopted tolerances for geometric selection in released LS-DYNA data. Neither
the printed inch dimensions nor “Elevation View” establishes those data's units.

Figure11-15 states that it is based on fabrication shop drawings (Frankel1985).
That attribution is evidence about NIST's stated source, not a claim that this
review inspected the original drawings or that a drawing authenticates the
released mesh, its damage state or the historical execution.

## Evidence grade, counterevidence and next bridge

Grade A applies to what these pinned pages explicitly publish: the ANSYS global
vertical/lateral roles, labeled local connection axes/components, separated
failure/contact mechanisms and distinction between observation and analysis.
The plan's eastward-X/northward-Y interpretation is a strong but figure-based
inference within that illustrated ANSYS frame. Its applicability to the released
model, absolute elevations/origin/units and PID179 identity remain underdetermined.

The prior review's independently read LS-DYNA result prose establishes +Y north,
-Y south and X east-west at 1-9A physical139/147. It was **not reread as new coverage
here**. Agreement with the ANSYS plan is useful consistency evidence, not a
release-to-run transformation or an independent physical witness. The narrow
remaining +X issue concerns the global/released join; the newly inspected
ANSYS glyph must not be omitted merely to preserve an older generic gap claim.

The strongest counterevidence to complete-disconnection reasoning is the
explicit distinction between connector failure and continued contact/bearing.
The strongest limit on an adequate-restraint claim is that the schematics give
no run-specific engaged pairing, remaining stiffness, directional reaction or
capacity for the target state. The 3.5 h noninitiating case is preserved as a
different model outcome; it does not identify the historical damage state.
Neither an unresolved crosswalk nor published buckling demonstrates wrongdoing,
concealment or a particular collapse cause.

The decisive bridge is a traceable physical-member/floor-to-effective-node/
element/part mapping, with coordinate origin, units, signed axes and any
ANSYS-to-LS-DYNA/release transform. It must then connect the C44-C79 seats and
C79-C76 west attachment from the prior report-state review to exact seat/clip/
bolt/contact surfaces and the relevant run's surviving state. This source arm
does not presume the numeric arm's candidate set succeeds or fails that join.

All 12 initially unfollowed leads have now received full-page review. Further
unfollowed context includes Chapter2 (referenced on550 for foundation context),
the underlying fabrication drawings, the broader model-construction/transfer
record, and diagrams/terminology not caught by the prior lexical queries.
Physical551's newly starting thermal-load subsection continues on552; that
continuation was not followed because no thermal-load conclusion is made here.
No whole-report absence finding or claim of exhaustive source retrieval is made.

Source-of-truth and evidence-audit skills kept these findings in this working
research note, with explicit publication/inference/transfer boundaries; the PDF
skill required full-page views and the four logged context extensions. No new
network search, external transfer, held-source access, modern manual expansion,
solver, legal/canonical promotion, integration edit, commit or push occurred.
