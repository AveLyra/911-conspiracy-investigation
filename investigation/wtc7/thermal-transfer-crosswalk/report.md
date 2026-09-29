# Thermal-load dataflow and released-script crosswalk

The released June files provide substantial, organized temperature-loading
material. This audit has **not identified the implementation that generated
the September LS-DYNA nodal-temperature input**. The distinction matters:
having the destination temperatures is not the same as being able to reproduce
their derivation, their spatial mapping or the handling of repeated nodes.

NIST's published account also corrects an overly narrow search premise. It
describes separate thermal-load data sets for ANSYS and LS-DYNA, as well as a
separate transfer of structural damage. It does not establish that LS-DYNA
temperatures were exported from a completed ANSYS structural-response
solution. Its stated interpolation between thermal load steps is temporal,
not a demonstrated spatial mapping rule for the LS-DYNA mesh.[^1]

This is research-only WP3/Q02/Q06/Q10 work. It establishes neither an incorrect
temperature field nor a validated fire-to-collapse sequence. It supplies no
new causal ranking, intent finding or legal conclusion. The controlling
[charter](/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md)
and preserved source records remain unchanged.

## Published dataflow

| Stage | Primary-source support | Scope of the support |
|---|---|---|
| FDS fire environment to structural heating | NCSTAR 1-9, printed 389 / PDF 455, §10.1 | The Fire Structure Interface links the fire and thermal calculations. Described gas-field averaging is not an LS-DYNA node-selection algorithm. |
| Thermal state to ANSYS structural loads | NCSTAR 1-9, printed 391 / PDF 457, §10.3.1 | Thermal loads were prepared at 12 half-hour instants. ANSYS interpolated between successive load steps. This describes prescribed loading, not measured steel temperatures. |
| Thermal state to LS-DYNA loads | Same page and section | A second thermal-load data set was generated for LS-DYNA. The passage does not identify its generator, source files, spatial selection or repeated-row convention. |
| ANSYS structural damage to LS-DYNA | NCSTAR 1-9, printed 457 / PDF 523, §11.1; separate primary-method review | Structural damage is another transferred quantity. That branch must not be silently substituted for the thermal-data branch. |

The complete-page root checks cover PDF 455,457,523 and 524; the separate
[primary-method review](method-source-review.md) records its additional text
coverage, source hashes and six targeted public-source searches. The public
sources describe a methodology, not authenticated execution of the released
files.[^1]

The referenced tower predecessor is more explicit about a spatial method:
NCSTAR 1-5G §4.7.2 identifies structural coordinates, opens the thermal solution
at the needed time, uses the closest thermal nodes for temperatures or
gradients, and writes ANSYS-compatible body loads. The core-column procedure
is described in §7.6. These are WTC 1/2 thermal-to-ANSYS procedures—not proof
that the WTC 7 LS-DYNA input used identical selection, tie-breaking, component
boundaries or output ordering. Complete pages120–121 and 168 were independently
viewed for this crosswalk.[^2]

## Released-file coverage

The frozen [protocol](PROTOCOL.md) selected the three APDL files from the
hash-pinned June manifest and every non-PNG regular member of the thermal ZIP.
All were read to EOF and hashed without executing source commands or extracting
members to their embedded paths. The original archive and all three APDL
hashes were checked again after processing.[^3]

| Coverage item | Result |
|---|---:|
| Thermal ZIP entries | 25,639:25,634 regular files and 5 directories |
| PNG bodies excluded | 272 |
| Non-PNG archive bodies read | 25,362 |
| Separate APDL bodies read | 3 |
| Total bytes read from those bodies | 477,970,521 |
| Bodies admitted to lexical interpretation | 25,364 |
| All-NUL body excluded from interpretation | 1;328 bytes, aliasZIP15109 |
| Physical LF lines, including the NUL body | 7,731,417 |

The interpreted subset contains **2,435,737 literal BF statements with TEMP
at the declared argument position** and **5,240,592 BFE/TEMP statements**.
These are statement counts across supplied files and variants, not unique
nodes, times, model temperatures, executed operations or independent tests.
Together with the public methods and linked input-file structure, they
support the inference that this is ANSYS-compatible temperature-loading
material. That is a positive role finding, not a claim that every file's
possible behavior is understood.[^3]

The root filename-shape classification places BF statements in member/core/
slno files, BFE statements in slab files, and the thermal archive's /INPUT
statements in floor/hour drivers. These names classify packaging; they do
not establish physical floor identity or historical invocation. Node-list
lines classified by numeric prefix were not fully field-validated as geometry.
No image-content or numerical temperature-magnitude finding follows here.

Neither of the two selected full literal markers—the LS-DYNA thermal keyword
or the known September thermal basename—was found in the interpreted
code/comment material. This does not rule out dynamically assembled text,
other names, external programs or omitted dependencies. No recognized format
record occurred in this corpus; independently reproduced synthetic format
edge cases remain documented rather than silently treated as a full parser
certification.[^3]

## Static file-reference follow-up

A separately declared [follow-up](DETAIL-PROTOCOL.md) reread1,864 selected
bodies totaling 469,040,000 bytes. It joined every inspected operation to its
original alias, physical line, segment and argument hash. It parses literal
fields without displaying arbitrary filenames, comments or arguments, and
never follows a source path.[^4]

| Literal operation | Count | Exact-name candidate result |
|---|---:|---|
| Thermal /INPUT with .int extension | 25,032 | Three basename candidates across the inventory, exactly one in the source member's archive parent. |
| Thermal /INPUT with .int extension | 96 | One basename candidate, in the same archive parent. |
| APDL /INPUT with .apdl extension | 8 | No exact basename/extension candidate in this selected inventory. Locations:APDL03 lines15,16,4275–4280. |
| /OUTPUT with .out extension | 1 | APDL03 line12; no matching supplied candidate. Its generated content is not established. |

No inspected call had percent-substitution syntax or an explicit path/directory
under the declared checks. These tests do not cover every possible indirect
language or environment mechanism. The25,128 same-parent input matches are
good evidence of internally organized thermal-file references. They are not
proof of the working directory, active case, selected branches, execution order
or a complete runnable case. The eight unmatched APDL calls corroborate a
specific static dependency gap; they do not establish that no corresponding
file exists under another name or outside this inventory.[^4]

The only recognized /OUTPUT occurrence has a literal .out extension, but an
extension does not determine output content. It cannot be labeled a proven
thermal exporter or dismissed as harmless logging without further evidence.
No spatial-coordinate join, source thermal-result read and LS-DYNA card-writing
chain has been established by the inspected calls.

## Remaining lexical limits

The initial root scan has 35 hashed unknown-token spellings,10,225 occurrences,
and 1,561 noncommand-unresolved segments. The targeted producer follow-up
classifies9,849 occurrences by an additional fixed generic vocabulary,
including geometry/selection tokens and nine MV starts in the extensionless
file. Thirty segments are syntactic parameter assignments:five from the
unknown-token bucket and 25 from the noncommand bucket. Expressions and MV
arguments were not executed or interpreted as historical actions.[^4]

At this revision,371 unknown-token occurrences and 1,536 first-line segments
remain unclassified by that producer. A proposed UTF-8 BOM explanation was
tested and **not supported**:zero selected bodies began with the exact
EFBBBF prefix. This preserves a failed diagnostic hypothesis, not an encoding
failure finding. Unclassified material is neither affirmative exporter evidence
nor permission to claim exporter absence. The independently reconstructed
[supplement](independent-supplement-review.md) confirms that the 371 occurrences
have full identifier-token syntax across 14 hash families. The 1,536 residual
segments are ASCII, 18 characters each, across 24 exact segment-hash families;
their meaning remains unresolved. These are version-specific producer
classifications and independently checked syntactic shapes, not a complete
language interpretation.[^4]

Other known language tokens such as SAVE/PARSAV/PARRES/*TREAD were counted but
not assigned I/O argument locators by the initial scanner; none occurred in
its recognized historical counts. Dynamic macros, abbreviations, language
state, external tools and runtime defaults remain outside this lexical audit.
The [inference review](inference-review.md) identifies these limits and shows
why matching counts cannot establish semantic or executable completeness.

## Scientific consequence and discriminating records

The earlier [thermal-assignment trace](../thermal-assignment-trace/report.md)
remains a finding about the released LS-DYNA input's row order and topology.
This crosswalk does not explain how its unequal repeated coefficients arose,
choose first/last/sum/average treatment, or authenticate the effective values
used by a historical solver. The closest-node tower procedure is a lead to
test, not a substitute for the missing WTC 7 mapping implementation.

The highest-value missing link is the actual implementation chain connecting
the source thermal state to the released LS-DYNA nodal records. A useful
crosswalk needs source-result identity and time, destination geometry/IDs,
coordinate and unit conventions, spatial selection and ties, component
selection, repeated-row generation/consolidation, serialization, and an
invocation/output match. Several routines could supply this chain; it need
not be one monolithic exporter. A named program without those joins would
still leave the relevant scientific question unresolved.

Two tests would materially change the result: reproducibly generate the
selected September thermal rows from authenticated upstream inputs using
the actual mapping code, and establish the applicable historical solver's
treatment of repeated assignments using versioned documentation or authorized
execution with its run evidence. Neither test was performed here. Their
absence does not establish faulty temperatures, intentional withholding,
deliberate intervention or the correctness of the fire account.

| Claim | Type / strength | Alternative or disconfirming test |
|---|---|---|
| The selected bytes contain the reported thermal statements and operations. | Observed/derived;A within the declared lexical scope. | A source-pin mismatch or independent locator/count disagreement would defeat this result. |
| The package supplies organized ANSYS-compatible temperature-loading material. | Inference;B, supported by syntax, candidate links and primary methods. | Actual implementation showing another use would narrow this role; the present inference does not assert exclusive function. |
| NIST's account distinguishes two thermal-load sets from structural damage transfer. | Attributed documentary observation;A. | A more specific source/run crosswalk could identify how the branches were implemented; the description alone does not. |
| The WTC 7 LS-DYNA temperature generator has not been identified in this finite pass. | Bounded investigation result;B, not a nonexistence finding. | Identified code, upstream-state linkage and reproduced output would change it. |
| A particular repeated-row rule or collapse cause follows from this audit. | Inference;E/unsupported here. | Requires additional implementation/run evidence and mechanism-specific physical tests. |

## Verification and sources

The two root source scans reproduce identical result objects. The independent
reader froze before seeing producer results and confirms all body hashes,
recognized thermal counts and 25,137 operation locators. Its original
comparison preserves differing argument-hash recipes, comment counters and
unknown-token buckets. A later, explicitly post-schema source check reconstructs
both argument-hash recipes and candidate fields for all 25,137 operations and
accounts for all 1,549 differing hash buckets at their source locators. It
resolves those comparison differences, not their complete language semantics;
the three comment-counter definition differences remain preserved. See
[verification review](verification-review.md) and the final
[validation record](validation.md) for exact pins, controls, retained failures,
follow-up coverage and residual disagreement. Independent code review is not
independent historical evidence or licensed engineering review.

[^1]: NIST. *Structural Fire Response and Probable Collapse Sequence of World Trade Center Building7*, NCSTAR 1-9, November 2008, §§10.1,10.3.1,11.1. [Official publication](https://www.nist.gov/publications/structural-fire-response-and-probable-collapse-sequence-world-trade-center-building-7); [local source](/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf). Inspected copy SHA-256`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`; complete source/coverage details in[method-source-review.md](method-source-review.md).

[^2]: NIST. *Fire Structure Interface and Thermal Response of the World Trade Center Towers*, NCSTAR 1-5G, September 2005, §§4.7.2 and 7.6, printed 76–77/124; physical PDF120–121/168. [Official PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-5g.pdf). Acquired copy SHA-256`f6aa637c05c4ff1ae2a6a5e9192471aa69e6e0aa97a4bbe5aa33afd68a3526ea`. This is a tower predecessor, not a WTC 7 exporter source listing.

[^3]: June production, three manifest-selected APDL files and thermal ZIP. [Pinned protocol](PROTOCOL.md), [root run01](run01.json), [root run02](run02.json), [independent checkpoint](independent01.json), [original comparison](independent-comparison01.json). Source hashes identify retained bytes, not production completeness or historical execution.

[^4]: [Targeted follow-up protocol](DETAIL-PROTOCOL.md), [details02](details02.json), [details03 including the negative BOM test](details03.json), [independent selected-source supplement](independent-supplement-review.md), and code/verification pins in[validation.md](validation.md). The producer follow-up is post-selection and shares the root lexer; the independent supplement imports only its own frozen scanner. Neither is another blinded discovery.
