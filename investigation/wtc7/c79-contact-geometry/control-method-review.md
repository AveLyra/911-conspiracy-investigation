# Explicit contact controls and geometric-method limits

Research only, September 13, 2026. This independent numeric-source and
primary-manual review does not initialize contact, run a solver, establish
surviving restraint, validate NIST's model, rank collapse causes, or promote
research into the legal record. The [unit protocol](PROTOCOL.md) and original
[charter](../CHARTER.md) control. Current main AGENTS/WORKFLOW/START-HERE, the
latest STATUS handoff and the preserved [earlier 47-page manual review](../c79-restraint-audit/contact-method-review.md)
were read; later local Sherlock scope initialization is not accepted evidence.

## Extraction and reproducibility receipt

[extract_controls.py](extract_controls.py) is a new, independently written,
numeric-only reader. It does not import earlier source-reader helpers. The
previous CID1/2 arrays were read before implementation for the expressly
authorized card-position comparison; the new global-control extraction reads
the raw admitted streams. This is not a blind source-discovery exercise.

[control-extraction01.json](control-extraction01.json) retains all selected
numeric rows, eight positional values including nulls, numeric lexemes,
physical source lines, raw-row hashes, keyword/header hashes, source identity,
before/after dependency pins and complete decompressed EOF receipts. Headings,
comments and arbitrary unsupported keyword spellings are never emitted.
Numeric source text is data, never executable instructions.

| Artifact | SHA-256 |
| --- | --- |
| extract_controls.py | f970de77c746133d5935209e2294e9e623127b17e417a756d88a9ba2e2dd8826 |
| control-extraction01.json | dfcca53944ba6772dc65922d5c0083ae5bdec191950f8eb0157d79ffbb6deec8 |
| PROTOCOL.md as executed | b18a519ba88e7d61d331d821232e269c3e3f9a5e690a3e25e3e108e1e70df1ea |
| Prior contacts-root01.json | 04193c154495a37e7603e72ad32668ee28383ff9471b4baeee7f93b257c56859 |
| Prior contact-method-review.md | b720e2330f46efc75e527db2aa3154147e36fa0210eee4eecb6597d3a128bb55 |

The scan completed at exit 0: 6.209 seconds, 27,525,120 bytes peak RSS on
macOS/Python 3.12.14. It read all three streams: 11,292,839 physical lines,
567,415,336 decompressed bytes. Each compressed size/hash and decompressed
size/line/hash matched the admitted prior receipt; before/after source,
protocol, manual, prior-result and prior-method pins passed. Original source
files remain unchanged.

| Source | Compressed bytes | Compressed SHA-256 | Decompressed bytes / lines |
| --- | ---: | --- | ---: |
| SRC-119 | 70,199 | 2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7 | 508,372 / 7,905 |
| SRC-120 | 23,162,693 | c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59 | 232,959,541 / 4,088,491 |
| SRC-121 | 47,520,888 | f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d | 333,947,423 / 7,196,443 |

The result has one CONTROL_CONTACT, six headed CONTACT blocks (36 numeric
rows), zero plain PART_CONTACT and zero unsupported related variants under
the declared lexical coverage. Exactly all 12 selected CID1/2 numeric rows
and their line locators match the frozen prior extraction. This agrees with
previous source extraction for those rows, not with historical solver state.
The new global block has not received a second independent parser comparison
in this review.

Thirteen synthetic controls passed: zero/null distinction, numeric lexeme
preservation, blank card, fixed-width slots, rejection of arbitrary text,
excess free fields, nonfinite values and inline comments, recognition of
unsupported related variants, ID-before-OFFSET heading separation, blank-row
position, source-string suppression and synthetic EOF. Fixtures are explicit
in the script. Syntax parsing passed. A separate attempted existing-output
write was refused before source scanning, and its hash remained unchanged.
There was no failed source computation. No UI/browser test applies.

This parser recognizes the three supplied CONTACT spellings, plain
CONTROL_CONTACT and PART_CONTACT. Other related variants are hashed, not
interpreted. It supports comma-separated or fixed ten-column numeric rows,
not arbitrary LS-DYNA input syntax, symbolic numeric substitutions, source
macros or inline-comment interpretation. It preserves extra numeric cards
as unreviewed instead of assigning a guessed schema. An EOF inventory is not
proof the historical program read, accepted or activated every block, or that
an uninspected include contains no relevant controls. No include is followed.

The actual command used bundled Python at
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
with `-B extract_controls.py --out control-extraction01.json`, using absolute
script/output paths. Reproduction requires a fresh output name in this unit;
existing output replacement is refused. Script writes require the scoped
sibling-worktree approval. No source execution, network, held help, raw/main/
legal edit, geometry computation, outreach, commit, push or Faraday run occurred.

## Explicit global control values

The sole block is SRC-121, keyword line 4, numeric lines 5 and 6. Manual
physical 472–476 / printed 8.24–8.28 gives the schema and qualifications.

| Source line | Exact field/value sequence |
| --- | --- |
| 5 | SLSFAC=.1; RWPNAL=0; ISLCHK=1; SHLTHK=0; PENOPT=1; THKCHG=0; ORIEN=1; ENMASS=0 |
| 6 | USRSTR=0; USRFRC=0; NSBCS=10; INTERM=0; XPENE=4; SSTHK=0; ECDT=0; TIEDPRJ=0 |

There are no optional global Cards 3–6 in that block. Their absence is not
an explicit array of zeros. No PART keyword containing CONTACT was found
by this bounded related-keyword scan of these three streams.

- SLSFAC=.1 is an explicit global penalty scale, not a complete spring law.
  PENOPT=1 selects the documented minimum of the master/slave stiffness
  values for applicable formulations (474); the actual constituent values
  and applicability are separate.
- ISLCHK=1 is the manual's no-checking selection (474), not an affirmative
  report that there were no initial penetrations.
- ORIEN=1 is automatic orientation for automated part input only (475).
  These selected master faces are explicit segments, so this setting does
  not establish their automatic reorientation. Preserve supplied order.
- SHLTHK=0 cannot be promoted to "no thickness anywhere": physical 474
  lists classes where thickness offsets are always included; physical 403
  says the global SHLTHK option is ignored for its named automatic classes.
  Tied attachment's thickness criterion must be considered separately.
- TIEDPRJ=0 is the documented eliminate-gap/projection selection for the
  named base tied types (476). That paragraph alone does not demonstrate
  identical behavior for plain OFFSET. The explicit variant distinction on
  363–364 remains controlling; no actual node projection was measured here.
- THKCHG, SSTHK, ENMASS, ECDT and XPENE have contact-class/state-dependent
  meanings (474–476). Their literal zeros are not evidence of member
  disconnection, zero mass, zero surviving contact or unlimited penetration.

## Selected contacts: exact local settings and qualifications

CID1: SRC-121 keyword 6,426,410, heading 6,426,411, numeric rows
6,426,412–6,426,417. It is TIED_SHELL_EDGE_TO_SURFACE_ID_OFFSET.
CID2: keyword 6,532,025, heading 6,532,026, numeric rows
6,532,027–6,532,032. It is TIED_SURFACE_TO_SURFACE_ID_OFFSET.

| Position | CID1 | CID2 |
| --- | --- | --- |
| Card 1: SSID, MSID, SSTYP, MSTYP, SBOXID, MBOXID, SPR, MPR | 1,1,4,0,null,null,0,0 | 2,3,0,0,null,null,0,0 |
| Card 2: FS,FD,DC,VC,VDC,PENCHK,BT,DT | eight explicit zeros | eight explicit zeros |
| Card 3: SFS,SFM,SST,MST,SFST,SFMT,FSF,VSF | eight explicit zeros | eight explicit zeros |
| Optional A: SOFT,SOFSCL,LCIDAB,MAXPAR,SBOPT,DEPTH,BSORT,FRCFRQ | eight explicit zeros | eight explicit zeros |
| Optional B: PENMAX,THKOPT,SHLTHK,SNLOG,ISYM,I2D3D,SLDTHK,SLDSTF | eight explicit zeros | eight explicit zeros |
| Optional C: IGAP,IGNORE,DPRFAC,DTSTIF,unused5,unused6,FLANGL,unused8 | 0,1,null,null,null,null,null,null | same |

The Card1 spatial-filter fields are blank, not explicit zero or a discovered
nonzero box filter. The ID heading is correctly separated despite ID not
being the final suffix (363–367). These variants do not require one of the
type-specific Card4 forms listed on 366; their six following rows map to
main Cards1–3 and optional A/B/C. The full raw-row hashes are retained.

1. **Time gating:** physical 374 expressly maps BT=0 to an inactive birth-
   time condition and DT=0 to 1E20. Thus these zeros do not switch off the
   contacts at time zero. Time eligibility still is not realized tying.
2. **Thickness and scale:** physical 375 lists element thickness as the
   SST/MST defaults and unity for SFS/SFM/SFST/SFMT/FSF/VSF. The selected
   literal fields are zero. This page does not spell out every explicit-
   zero conversion; retain the distinction between stated defaults and
   demonstrated effective values. Neither zero thickness/stiffness nor
   authenticated unity factors follow from this extraction. No negative
   SST/MST special attachment-tolerance override is specified.
3. **SOFT/MAXPAR:** explicit SOFT=0 selects the manual's penalty option
   (394). SOFT2-specific alternatives on 396 are not selected by these
   cards. Physical 395 explicitly maps MAXPAR=0 to 1.025 for most contacts
   and lists 1.006 for tied-shell-edge OFFSET. These are stronger version-
   manual grounds than an invented universal search factor; they still
   do not authenticate the historical build or its initialized pairing.
4. **Optional B:** physical 397 limits THKOPT/SHLTHK to listed old contact
   types; SHLTHK is defined if and only if THKOPT=1. Do not apply all eight
   zeros as universal controls of the supplied plain ties. PENMAX is
   contact-class-specific, not a generic fracture threshold (397,405–407).
5. **Optional C:** physical 399 labels IGAP implicit-only, with listed
   choices1/2 and default1; it does not explicitly define IGAP input0 in
   that paragraph. IGNORE concerns CONTACT_AUTOMATIC options. Therefore
   the explicit IGNORE=1 in these plain tied-OFFSET cards cannot prove
   ignored penetrations or skipped projection. DPRFAC/DTSTIF concern
   SOFT2 or SOFT1/2 (399–400), not evidence of an unlisted active feature.
6. **Part overrides:** physical 1028–1036 permits reordered PART options
   but limits its CONTACT functionality to named automatic/single-surface
   classes. Physical 1031 conditions part FS/FD/DC/VC use on CONTACT FS=-1;
   OPTT is shell contact thickness, SFT automatic-contact thickness scaling,
   and SSF explicitly maps zero to unity (1035). No such block occurs in
   this scan; these rules must not be imported as hidden plain-tie settings.

## Judgment on the proposed later geometric sensitivity diagnostic

Evaluating all relevant slave nodes against each selected ordered master
face, retaining both quadrilateral triangulations, supplied-thickness low/
high scenarios and separate e=1,1.006,1.025 scenarios is defensible as a
**declared conditional geometric sensitivity analysis**, not as recreated
LS-DYNA pairing. No proximity analysis was performed in this review. The
following limits must accompany any later result:

- Physical 402–403 supplies the closeness form
  `delta=max(.60*(ts+tm), .05*min(master diagonals))`. It does not fully
  specify how heterogeneous nodal incidence and corner thickness become
  the effective ts/tm in this particular solver variant. Supplied min/max
  fields are test inputs, not proven effective-thickness bounds.
- No-shell or missing-thickness cases remain unknown. They must not be
  discarded as failed ties or assigned ts=0 merely to complete the formula.
  The manual's separate solid-node zero-thickness rule requires an actual
  solid-element interpretation, not absence of a shell incidence alone.
- Two triangulations test sensitivity to representing a warped quad by
  planar triangles. Their distances are not automatically rigorous upper/
  lower bounds on a solver's bilinear surface distance. Retain degeneracy,
  warpage, face order, normal/projection and boundary cases explicitly.
- MAXPAR describes a parametric segment search extension (395), not
  necessarily Euclidean dilation. A chosen implementation of e must be
  declared. Parametric extension or extrapolation can leave corner-value
  min/max bounds. Never call a box bound conservative for all solver
  behavior when it is conservative only for the declared surrogate.
- Preserve all qualifying faces and the multiplicity/no-candidate groups.
  A nearest-face winner would conceal genuine ambiguity. Passing a
  closeness test does not establish selected pairing, tie stiffness,
  restraint direction, later survival or architectural-member identity.

The highest-priority unresolved method dependencies are (1) effective nodal/
face thickness aggregation and explicit-zero treatment for this build;
(2) its exact parametric search/projection and competing-face rules for
these OFFSET variants; (3) initialization/warning or realized-pair records
and exact executable/run provenance; then (4) surviving materials, stiffness,
state and force histories for a residual-restraint calculation. Actual
global values and absence of PART_CONTACT in these streams narrow this list;
they do not make a generic "all controls unavailable" claim appropriate.

## Source-view record and inference ceiling

The admitted May2007 Version971 manual retains SHA-256
`f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d`.
This turn added 13 complete new page views: physical396–399 and1028–1036,
including tables, warnings and continuations. They were rendered to
`/private/tmp/c79-contact-controls.6scoor/p<page>.png` with bundled Poppler
26.05.0, scale1700, PNG, singlefile and the earlier pinned font configuration.
Physical374,375,402,403 were visually re-inspected from the prior renders.
Other relied-upon manual pages are in the preserved earlier47-page record;
they are not claimed as new views. Root separately handled ELEMENT_DISCRETE
758–759; this reviewer supplied only a bookmark locator and does not claim
those full-page views or the ground-node determination.

Directly established: explicit numeric controls and their source locators
within these streams. Source-supported interpretation: option-specific
schemas, stated defaults and applicability restrictions. Still underdetermined:
effective historical initialization and surviving physical restraint. The
strongest countercheck against an omitted-coupling claim is the declared
penalty-tie mechanism; the strongest countercheck against intact-restraint
claims is the unresolved transition from candidates to initialized and
surviving force paths. No scientific or legal ranking changes here.
