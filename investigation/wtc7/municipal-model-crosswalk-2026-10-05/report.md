# Municipal structural references and released model locations

October 5, 2026. Research only. Completed bounded crosswalk under the
[fixed scope](SCOPE.md); no new primary-source reading or simulation.

Four column labels in the April 1998 municipal comments—70, 71, 73 and 74—
resolve through explicit diagnostic references to parts in the released model.
That supplies concrete model locations for a further comparison. It does
**not** identify the first-floor notched beams, establish a physical floor in
the model, or show whether the documented alterations were represented.

The narrower result matters in both directions. The released model is not
wholly unlocatable: named column regions, geometry bounds and material
references can be inspected. Conversely, finding those columns is not a test
of the altered beam, reinforcement, trench or connection. No model omission,
capacity defect, accurate historical reconstruction or collapse-cause ranking
is established by this crosswalk.

## Documentary connections and their limits

The [drawing review](drawing-locators.md) records exact pages, dates, prefixes
and source roles from the existing municipal readings. Those readings retain
their display and legibility limitations; this text crosswalk does not repair
them. The [municipal synthesis](../municipal-originals-2026-10-04/synthesis.md)
remains the full documentary assessment.

| Target | Supported connection | Disposition and missing link |
|---|---|---|
| April tank and slab-opening comments | 173529 p6 names tank location between column lines70/73 rather than64/67; p10 names70/71/73/74. The separate May index lists first-floor S-1 and seventh-floor S-2 with May13,1998 dates. | **Location leads and model-label matches.** Comments are proposed corrections, not surveyed or installed locations. The actual May13 S-1 and response/revision record are not supplied by that index. The April column group is not silently assigned to the October notches. |
| S-S-1 first-floor penetration plan | 166828 p4, October15,1998, Re:S-1, refers the indicated notched beams to SKS-S-2 and names a companion trench sketch. | **Actual drawing held; exact altered-member join unresolved.** Complete leaders, beam endpoints and grid identity were not reliably recovered in prior readings. Repeated S-1 does not alone prove identity with the May13 sheet. |
| SKS-S-2 first-floor notch detail | 166828 p5, October16, shows reinforcement plates on both sides and a weld callout. S-S-1 expressly references it. | **Plan-to-detail connection supported; model geometry unresolved.** The full existing section and affected-member identities are unverified. The sketch log's S-S-2 versus actual SKS-S-2 prefix remains explicit; tentative dimensions are not model inputs. |
| October S-TS-7 | 166828 p6, October15, sections11/11A, first-floor trench area, work-with SKS-S-1; slab restoration and replacement of cut top reinforcement are explicit. | **Section/reference connection supported; global member mapping unresolved.** Re:FS-7 versus Re:TS-7 is a retained reading disagreement. Partial W6 labels do not give full section identities. |
| December S-TS-7 | 167874 p1 retains the title/base date/section arrangement and is marked Revised12/3/98. It adds an overlap clause to the prominent restoration note. | **Version relationship supported; detailed geometry and adopted revision unresolved.** The overlap reading remains1′0″ versus1′6″. October already requires restoration; no zero-overlap condition is inferred. |
| Seventh-floor CO23 | 171807 p1 is a December1 fax referring to requested seventh-floor beam-penetration sketches as likely CO23 backup; 167170/171802 identify the November3,1998 submission and express cost approval subject to audit. | **Reference and commercial approval held; governing sketch not supplied.** No beam/grid/model join. The first-floor drawings cannot substitute for the separate seventh-floor sketch. |
| CO40 trench reinforcement | The same approval letter identifies the December21,1998 submission and a three-inch welded-rebar overlap. | **Approved described work; joint and floor unresolved.** No exact drawing/member/joint identifier joins it to S-TS-7. The different numbers are a reconciliation question, not a demonstrated same-joint contradiction. |

The unnumbered September opening fragment likewise lacks a secure floor,
member and parent-sheet identity. Its grid tokens23/24/25 do not identify
CO23. Other projects at floors38/39 and one variously listed at30/31 have useful
beam spans but different project records. The30/31 discipline-table discrepancy
remains unresolved; none is borrowed as the OEM sketches' missing geometry.
The drawing review preserves those alternative locators rather than mistaking
similar labels for a match.

No tested drawing-to-model correspondence reaches a demonstrated
contradiction. The principal outstanding results are **unresolved**, not
proved absent or outside the entire historical model's coverage.

## Exact model references recovered

The finite query selected explicit `column_diagnostics[].column_number`
values44,70,71,73,74,76,79 from the already checked
[member map](../model-member-map/report.md). The four new candidates came
from the April comments;44,76,79 were previously mapped controls. The selection
was declared before this query, but source reports and earlier mappings were
already known. It is not a blinded physical test.

The parser derives the column label from the diagnostic heading, then follows
its stated part-set identifier and that set's explicit part list. The query
does **not** manufacture a part number by adding100 to a column number.
Part identifiers then join to the supplied
[material crosswalk](../material-run-crosswalk/report.md).

| Column label | Diagnostic line | Part set and explicit part | Part numeric-card line | Material | Section | Shell records |
|---:|---:|---:|---:|---:|---:|---:|
| 44 | 369 | 144 | 3072 | 100 | 144 | 624 |
| 70 | 551 | 170 | 3410 | 99 | 170 | 800 |
| 71 | 558 | 171 | 3423 | 99 | 171 | 584 |
| 73 | 572 | 173 | 3449 | 99 | 173 | 952 |
| 74 | 579 | 174 | 3462 | 99 | 174 | 592 |
| 76 | 593 | 176 | 3488 | 99 | 176 | 944 |
| 79 | 614 | 179 | 3527 | 99 | 179 | 952 |

All selected diagnostic and part locators belong to the master source alias
SRC-121, `wtc7_global_8a_no-conn-matl.k.gz`. Numeric-card lines differ from
keyword lines and are not published report page numbers. Materials99 and100
have supplied definitions at keyword lines2486 and2496 respectively. Their
presence is not validation of the law, thermal history or historical run.

Each selected label occurs once in the83 diagnostic records. Each explicit
part resolves uniquely in the map, all-part references and used-part records;
its referenced material ID resolves uniquely in the effective material index.
Diagnostic bounds equal the referenced part bounds **within the member map**.
Part, section and material identifiers and element-family counts agree across
the member-map and material-crosswalk outputs; the latter does not independently
supply those geometry bounds. There are no missing selected parts.
The [independent check](inventory-check.md) preserves full key definitions,
numeric bounds, input hashes, canonical object digests and the replay command.
The [model review](model-locators.md) interprets available fields and limits.

### What the coordinates do not establish

The recorded bounds describe the whole referenced part, not a cross-section
plane intersection, individual connection or physical floor. No floor is
assigned from a regular Z spacing, a plane coordinate, an ID or a filename.
The absence of floor/drawing/revision field names in these two derivative
schemas is a bounded schema observation, not proof such information exists
nowhere in the released files or source documentation.

The existing include transformation and matching IDs also do not establish
geographic orientation, physical units, a floor-elevation datum, installed
condition, or equivalence between detailed master and outside representations.
The earlier [C79 detail audit](../c79-member-detail-crosswalk/report.md) already
shows why a column-part match does not identify a specific seat, clip or bolt.
This unit neither repairs missing materials elsewhere nor establishes native
solver execution, complete boundary conditions or historical run identity.

There are two more specific coverage cautions. The earlier
[input inventory](/Users/admin/docs/911/research/sherlock-wtc7-investigation/lsdyna-supplement-content-audit/report.md)
records literal seventh-floor mass titles in the discrete-mass include; those
are not a CO23 framing match. The
[structural source audit](/Users/admin/docs/911/research/sherlock-wtc7-investigation/structural-chain-source-audit.md),
SC06, attributes fixed column ends below second-floor framing and a fixed,
nondeformable substation to NIST's global model description. That makes lower
boundary treatment a concrete question, but does not establish that every
first-floor alteration is absent or physically irrelevant. These are existing
audit attributions, not newly authenticated primary-source findings. The global
LS-DYNA assembly is also distinct from the reported16-story ANSYS work.

The new regions have aggregate counts and bounds, not fresh per-element
exports in this unit. Existing C79 element/contact exports cover a different
selection. In particular, beam part IDs73/74 are not column labels73/74.
Neither number matching nor an earlier localized connection frame can fill
the missing municipal member and floor correspondence.

## What would discriminate next

The next local task is a **bounded legibility review of the already-held
S-S-1 plan,166828 p4**. It directly bears on the first-floor member join;
another trench-detail summary cannot supply the missing plan endpoints.
Declare that review before viewing, fix the existing source/raster identities,
correct the prior image-detail delivery mismatch, and record separate reader
results before exchange. The target is the complete notch-note leader,
affected beam endpoints/grid labels and Re:S-1 key—not a new reading of the
entire municipal collection or selection of convenient glyphs.

The other reader's earlier larger view also did not recover the complete
member mapping. Correcting delivery does not create new source detail or
promise success; the proposed test addresses a known review limitation.

Acceptance is either a reproducible, uncertainty-qualified member/location
reading or an explicit unresolved result. No forced consensus or inferred
geometry follows if the scan cannot support it. A different reading must be
preserved as a new observation version, not overwrite the old one. The needed
next record if this fails is the applicable underlying first-floor S-1 with
its revision and grid/beam schedule; the May13 listing supplies a candidate
date, not a verified identity.

The seventh-floor branch has a different next record: CO23's November3
submission/sketch or the missing attachment to the December1 fax, with
its governing seventh-floor plan. CO40 needs its December21 scope and exact
joint/detail identity. No acquisition or pending public drawing-package
inspection is performed or newly cleared here.

Even a successful member reading would require an explicit drawing-to-model
coordinate and floor comparison before a historical omission claim. Conditional
tests may use disclosed assumptions and sensitivity ranges without complete
as-built proof; they must not report those assumptions as observed history.
The potential causal relevance still needs exposure, loads, connection
behavior and propagation testing, not simply more matching identifiers.

## Verification and research state

Drawing and model reviewers and a separate input checker prepared their
initial records without access to this synthesis. These are independent AI
implementations/reviews over shared records, not independent historical
witnesses, source authentication or professional engineering acceptance.

Root rechecked the unchanged main control/charter hashes and existing branch
state. A stdout-only bundled Python query (`6ce75c`, exit0) verified both
model input pins and all seven explicit label-to-set-to-part/reference/used/
material joins, selected geometry and material agreement. This replay followed
reading the checker's findings and is not blinded. A separate hash-only replay
(`b613e5`, exit0) verified the frozen scope/checker notes and all60 unique
path/size/SHA256 rows in the checker's input tables. No PDF contents were
reparsed. The checker retains its initial path-lookup and note-authoring
failures rather than reporting those attempts as passes.

Final critical review of draft `17ee467aa993e1fe89e5469db3450f9af63b9c19c1aeccb632ef3b3de7f1acf5`
required three pinpoint corrections: geometry equality is within the member
map, not an independent geometry reconstruction; the CO23 fax refers to
requested sketches rather than itself requesting them; and the other project's
30/31 floor discrepancy must remain visible. The prior larger-view limitation
was added to avoid promising that corrected delivery will resolve the scan.
Both substantive reviewers verified their changes in revision
`ba1bffd9824b925c2d2dda58f2703e4d929b39005b644af832c54adfb24db8ed`
(`50c360`→`5ecbdb` and `df9a72`, exit0). Neither found a remaining blocker in
its checked scope; this is not a fresh review of every primary input.

The independent checker compared the separately frozen model note with its
own results and this revised report (`00f60d`, exit0): all seven peer/root
join rows, geometry rows, keyword/card locators, shared pins, collection counts
and ten report links agree. Its earlier `a076ac` exited1 because it detected
the concurrent report revision before numerical checks ran; the confirmed
revision was reread before rerunning. That failed version check is retained.

Root additionally checked14 drawing-note and17 model-note source hashes,
four frozen scope/reviewer pins and31 local links across the unit (`b70aba`,
exit0). A final stdout-only Python comparison (`05282c`, exit0) reproduced
the report's seven numeric rows and checked section/material/count agreement
across outputs and bounds equality within the member map. These reuse shared
data and are not independent historical evidence. Earlier source-display
limitations, differing readings and missing joins remain substantive limits
despite the passing checks. Subsequent edits only close this review record
and propagate navigation, without changing those reviewed findings.

The preceding user-coordinate turn only reconfirmed existing measurements;
it did not advance the broader goal. This crosswalk adds new candidate model
locations and separates the next missing joins. The full charter remains
active and incomplete; no cause ranking or numerical probability changes.
Research worktree/branch remain at ca1c2233 with intentional uncommitted WIP.
Main/legal, preserved sources and frozen earlier observations are unchanged.
No new source acquisition/viewing, decompression, solver, engine activation,
outreach, fee, transfer, promotion, staging, commit or push occurred. Existing
Sherlock identity/version/join feedback covers this workflow; archived-task
routing and other scientific/human/permission gates remain unchanged.
