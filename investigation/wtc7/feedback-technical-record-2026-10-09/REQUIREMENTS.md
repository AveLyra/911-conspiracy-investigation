# Sherlock feedback technical requirements

This is the source-ordered technical transcription and coverage map for the frozen feedback snapshot. The JSON record is the editable source for this generated view. See README.md for scope, status, review limits and source privacy.

Source SHA-256: `e1c718bb928ba846deb0d527f69cda7ea00a8d888c2247a864b1d666b4204133`. Source lines: 2468.

## Earlier digest crosswalk

Topic membership is navigation, not proof that the earlier digest or recipient log retained every refinement.

| Digest item | Topic | Detailed units |
| --- | --- | --- |
| 01 | Acquisition and perceptual states | TR-L0022, TR-L0462, TR-L0485, TR-L0500, TR-L1391, TR-L1430, TR-L1449, TR-L1464, TR-L1492, TR-L1560, TR-L1889, TR-L2267, TR-L2328, TR-L2329, TR-L2341, TR-L2397, TR-L2399, TR-L2401 |
| 02 | Search scope and bounded extraction | TR-L0512, TR-L0523, TR-L0542, TR-L0554, TR-L0564, TR-L0687, TR-L0805, TR-L0822, TR-L0835, TR-L0847, TR-L0860, TR-L0873, TR-L0879, TR-L1391, TR-L1492, TR-L1507, TR-L1519, TR-L1531, TR-L1719, TR-L1815, TR-L1905, TR-L1959, TR-L2042, TR-L2267 |
| 03 | Catalog grain, representation and document roles | TR-L0485, TR-L0500, TR-L0512, TR-L0531, TR-L0542, TR-L0554, TR-L0564, TR-L0572, TR-L0582, TR-L0605, TR-L1449, TR-L1464, TR-L1492, TR-L1507, TR-L1519, TR-L1531, TR-L1560, TR-L1598, TR-L1649, TR-L1795, TR-L1797, TR-L1843, TR-L1905, TR-L2217, TR-L2267, TR-L2269, TR-L2331, TR-L2337, TR-L2342, TR-L2343, TR-L2350, TR-L2458 |
| 04 | Redact before display and disclosure | TR-L0022, TR-L0401, TR-L0460, TR-L0669, TR-L0697, TR-L0725, TR-L0761, TR-L0805, TR-L0995, TR-L1430, TR-L1442, TR-L1449, TR-L1476, TR-L1531, TR-L1560, TR-L1793, TR-L2277, TR-L2324, TR-L2329, TR-L2345, TR-L2347, TR-L2403, TR-L2468 |
| 05 | Exact bytes, parser contracts and path safety | TR-L0037, TR-L0052, TR-L0068, TR-L0149, TR-L0554, TR-L0669, TR-L0680, TR-L0687, TR-L0805, TR-L1365, TR-L1649, TR-L1719, TR-L1754, TR-L1799, TR-L1967, TR-L2271, TR-L2273, TR-L2277, TR-L2403 |
| 06 | Dependency closure, namespace and owner identity | TR-L0052, TR-L0068, TR-L0112, TR-L0149, TR-L0157, TR-L0166, TR-L0181, TR-L0234, TR-L0330, TR-L0367, TR-L0391, TR-L0660, TR-L1405, TR-L1464, TR-L1476, TR-L1614, TR-L1706, TR-L1719, TR-L1754, TR-L1799, TR-L2271, TR-L2273, TR-L2277, TR-L2351, TR-L2369, TR-L2397, TR-L2399, TR-L2401 |
| 07 | Preservation acquisition and runtime identity | TR-L0680, TR-L0714, TR-L0761, TR-L0805, TR-L1076, TR-L1096, TR-L1108, TR-L1231, TR-L1344, TR-L1359, TR-L1430, TR-L1877, TR-L1889, TR-L2000, TR-L2275, TR-L2328, TR-L2329, TR-L2330 |
| 08 | Failure capture and stage-specific admission | TR-L0037, TR-L0735, TR-L0822, TR-L0995, TR-L1006, TR-L1076, TR-L1108, TR-L1138, TR-L1231, TR-L1244, TR-L1252, TR-L1344, TR-L1359, TR-L1476, TR-L1544, TR-L1560, TR-L1580, TR-L1754, TR-L1905, TR-L1987, TR-L2151, TR-L2227, TR-L2231, TR-L2263, TR-L2330, TR-L2357, TR-L2383, TR-L2405 |
| 09 | Chunk completeness, storage and process supervision | TR-L0680, TR-L1138, TR-L1304, TR-L1967, TR-L1979, TR-L2000, TR-L2082, TR-L2330, TR-L2369, TR-L2383 |
| 10 | Immutable observations, review and errata | TR-L0068, TR-L0080, TR-L0135, TR-L0166, TR-L0174, TR-L0191, TR-L0200, TR-L0367, TR-L0436, TR-L0697, TR-L0774, TR-L1126, TR-L1152, TR-L1198, TR-L1217, TR-L1304, TR-L1374, TR-L1507, TR-L1544, TR-L1580, TR-L1815, TR-L2036, TR-L2042, TR-L2055, TR-L2194, TR-L2206, TR-L2285 |
| 11 | Native-coordinate human review | TR-L0174, TR-L0317, TR-L0436, TR-L1265, TR-L1283, TR-L1290, TR-L1304, TR-L1803, TR-L1829, TR-L2068, TR-L2233, TR-L2241 |
| 12 | Lossless annotation schemas and ownership | TR-L0089, TR-L0102, TR-L0112, TR-L0123, TR-L0135, TR-L0191, TR-L0200, TR-L0211, TR-L0223, TR-L0234, TR-L0272, TR-L0292, TR-L0330, TR-L0343, TR-L0353, TR-L0391, TR-L1815, TR-L1829, TR-L1852, TR-L2055, TR-L2170, TR-L2184, TR-L2194, TR-L2206, TR-L2237, TR-L2245, TR-L2247, TR-L2289, TR-L2305, TR-L2355 |
| 13 | Conditional support and correlated graphical uncertainty | TR-L0089, TR-L0102, TR-L0123, TR-L0191, TR-L0211, TR-L0249, TR-L0272, TR-L0281, TR-L0292, TR-L0317, TR-L0343, TR-L1062, TR-L2355 |
| 14 | Calibration, observables, fits and event censoring | TR-L1126, TR-L1322, TR-L1374, TR-L1391, TR-L1544, TR-L1580, TR-L1598, TR-L1679, TR-L1843, TR-L1852, TR-L1945, TR-L2042, TR-L2145, TR-L2147, TR-L2149, TR-L2168, TR-L2170, TR-L2184, TR-L2229, TR-L2233, TR-L2237, TR-L2239, TR-L2241, TR-L2243, TR-L2245, TR-L2247, TR-L2261, TR-L2327 |
| 15 | Clock provenance and exact extraction coverage | TR-L1544, TR-L1614, TR-L1679, TR-L1905, TR-L1921, TR-L1933, TR-L1945, TR-L2082, TR-L2145, TR-L2147, TR-L2149, TR-L2151, TR-L2153, TR-L2168, TR-L2227, TR-L2229, TR-L2231, TR-L2239, TR-L2243, TR-L2326, TR-L2327, TR-L2357, TR-L2361, TR-L2403, TR-L2405, TR-L2422 |
| 16 | Visual matching, exclusion and common support | TR-L0411, TR-L1614, TR-L1635, TR-L2011, TR-L2024, TR-L2082, TR-L2102, TR-L2117, TR-L2126, TR-L2233, TR-L2261, TR-L2357 |
| 17 | Audio, mixing, speech and correspondence | TR-L0462, TR-L1877, TR-L1889, TR-L2145, TR-L2147, TR-L2149, TR-L2153, TR-L2155 |
| 18 | Exact numerical decisions and complete checkers | TR-L0281, TR-L0292, TR-L0774, TR-L0955, TR-L0973, TR-L1044, TR-L1365, TR-L1614, TR-L1665, TR-L1679, TR-L1738, TR-L1801, TR-L2068, TR-L2235, TR-L2237, TR-L2239, TR-L2243, TR-L2245, TR-L2247, TR-L2437 |
| 19 | Models, quantities and validation scope | TR-L0308, TR-L0572, TR-L0590, TR-L0605, TR-L0619, TR-L0628, TR-L0637, TR-L0647, TR-L0660, TR-L0793, TR-L0891, TR-L0899, TR-L0924, TR-L0955, TR-L1015, TR-L1693, TR-L1706, TR-L1774, TR-L1793, TR-L1795, TR-L1799, TR-L1801, TR-L1803, TR-L1921, TR-L1979, TR-L2024, TR-L2229, TR-L2269, TR-L2271, TR-L2273, TR-L2281, TR-L2283, TR-L2285, TR-L2335, TR-L2337, TR-L2349, TR-L2397, TR-L2399, TR-L2401 |
| 20 | Experiments, force bounds and uncertainty semantics | TR-L0590, TR-L0619, TR-L0637, TR-L0647, TR-L0774, TR-L0793, TR-L0899, TR-L0913, TR-L0924, TR-L0955, TR-L1044, TR-L1062, TR-L1774, TR-L2335 |
| 21 | Independence, ground truth and review leakage | TR-L0052, TR-L0234, TR-L0317, TR-L0391, TR-L0401, TR-L0411, TR-L0436, TR-L0500, TR-L0697, TR-L0774, TR-L0899, TR-L0985, TR-L1374, TR-L1580, TR-L1598, TR-L1665, TR-L1679, TR-L1693, TR-L1706, TR-L1797, TR-L1945, TR-L2024, TR-L2036, TR-L2042, TR-L2102, TR-L2117, TR-L2194, TR-L2231, TR-L2233, TR-L2241, TR-L2281, TR-L2283, TR-L2285, TR-L2289, TR-L2305, TR-L2327, TR-L2342, TR-L2355, TR-L2361 |
| 22 | Documentary assertions and temporal attribution | TR-L0485, TR-L0564, TR-L0572, TR-L0582, TR-L0590, TR-L0628, TR-L0647, TR-L0985, TR-L1015, TR-L1031, TR-L1217, TR-L1774, TR-L1793, TR-L1795, TR-L1797, TR-L1815, TR-L2269, TR-L2305, TR-L2331, TR-L2342, TR-L2343, TR-L2350, TR-L2361, TR-L2458 |
| 23 | Replays, preflights and inert reconstruction | TR-L0068, TR-L0367, TR-L0379, TR-L0391, TR-L0735, TR-L1184, TR-L1774, TR-L1877, TR-L1959, TR-L1987, TR-L2000, TR-L2082, TR-L2155, TR-L2235, TR-L2261, TR-L2263, TR-L2275, TR-L2351, TR-L2401, TR-L2466 |
| 24 | Completion and claim-specific prerequisites | TR-L0135, TR-L0249, TR-L0260, TR-L0308, TR-L0436, TR-L0605, TR-L0697, TR-L0714, TR-L0774, TR-L0793, TR-L0937, TR-L1126, TR-L1598, TR-L1693, TR-L1706, TR-L2143, TR-L2145, TR-L2149, TR-L2452, TR-L2454 |
| 25 | External-engine export and enforcement boundaries | TR-L0725, TR-L0735, TR-L0751, TR-L0761, TR-L2351, TR-L2353, TR-L2460, TR-L2462, TR-L2464, TR-L2466, TR-L2468 |
| 26 | Feedback lifecycle and readiness reporting | TR-L0001, TR-L0005, TR-L0009, TR-L0080, TR-L0411, TR-L0430, TR-L0452, TR-L0460, TR-L0479, TR-L0697, TR-L0714, TR-L0735, TR-L0751, TR-L1861, TR-L1863, TR-L1865, TR-L1867, TR-L1869, TR-L1871, TR-L1873, TR-L1875, TR-L2141, TR-L2143, TR-L2249, TR-L2251, TR-L2253, TR-L2255, TR-L2257, TR-L2259, TR-L2265, TR-L2279, TR-L2287, TR-L2322, TR-L2324, TR-L2333, TR-L2339, TR-L2345, TR-L2347, TR-L2351, TR-L2353, TR-L2359, TR-L2363, TR-L2365, TR-L2367, TR-L2395, TR-L2448, TR-L2450, TR-L2452, TR-L2454, TR-L2456, TR-L2460, TR-L2462, TR-L2464, TR-L2466, TR-L2468 |
| 27 | Rendering, byte layers and display contracts | TR-L1096, TR-L1108, TR-L1152, TR-L1169, TR-L1175, TR-L1184, TR-L1252, TR-L1322, TR-L1344, TR-L1405, TR-L1649, TR-L1803, TR-L1843, TR-L2068, TR-L2151, TR-L2153, TR-L2168, TR-L2217, TR-L2227, TR-L2237, TR-L2241, TR-L2326, TR-L2343, TR-L2355, TR-L2357 |

## TR-L0001 Feedback-record purpose

Source lines 1–4; context. SFB mapping: none. Earlier digest topics: 26.

The source is an actionable, deduplicated software-feedback log encountered during an investigation. It is not a second product roadmap or a repository of case evidence.

Qualification: Context for the technical record, not a product implementation assertion.

Publication transformation: The investigation-charter link is omitted; the role distinction is retained.

## TR-L0005 Explicit routing and lifecycle distinctions

Source lines 5–8; requirement. SFB mapping: SFB-005. Earlier digest topics: 26.

Use the existing explicitly designated feedback destination. Do not create replacement tasks, external issues, or unsolicited implementation instructions by default. Keep authored, sent, delivery-confirmed and acknowledged states distinct from implemented and verified-fixed. Later confirmed delivery can supersede a current pending-routing label without rewriting earlier dated local-only history.

Acceptance checks

- A batch acknowledged by its designated recipient is not labeled implemented or verified fixed.
- A historical unsent entry remains preserved after a later authorized delivery.
- No new destination or implementation request is inferred from ordinary feedback routing.

Qualification: The source records a later authorized delivery and acknowledgment. This transcription does not independently certify its receipt or any product fix.

Publication transformation: Private destination title, task identifier, and exact delivery date are replaced by their routing roles.

## TR-L0009 Historical digest delivery and limits

Source lines 9–21; context. SFB mapping: SFB-001, SFB-002, SFB-003, SFB-004, SFB-005. Earlier digest topics: 26.

The source records a 27-item consolidated digest under the existing feedback families, preserving the resolved status of SFB-001. The raw log, case material, source identifiers, private paths and attachments were not sent; the requested action was logging and triage only. All 27 item IDs were accounted for in the recipient response: 24 acknowledged extensions and items 15, 16 and 27 reported already covered. The three coverage classifications were recipient dispositions, not independently verified implementation coverage. The failed reopen attempt was not represented as a successful unarchive; later direct-send evidence established delivery independently. A reported timing-sensitive full-suite failure followed by an isolated passing rerun did not certify the full suite or a feature fix. Source-history preservation and exact transmitted-payload checks do not establish semantic completeness of a digest.

Qualification: Historical delivery narrative is attributed to the source. Delivery and acknowledgment establish neither fix, retest, activation, case transfer nor scientific finding. Other source-handling and human-review gates remain unchanged.

Publication transformation: Exact timestamps, source and message hashes, byte sizes, receipt locations, private paths, task/turn/message identifiers and markup delimiters are omitted. No technical acceptance condition is removed.

## TR-L0022 Reference-only acquisition is not materialization

Source lines 22–36; requirement. SFB mapping: SFB-005. Earlier digest topics: 01, 04.

A native raw-file fetch can report success, stated size/MIME and a file_uri object containing an expiring download locator without creating a local file. Where the available tool set supplies no identified native materialization action, acquired-bytes must remain false until a supported transfer produces a checked local artifact. Do not expose reference values in diagnostics, infer source refusal from this local capability gap, or mark an unattempted second item failed. Provide a supported privacy-preserving reference-to-local-artifact path with size/hash checks and distinct referenced, materialized and admitted states.

Acceptance checks

- A dummy successful reference-only response leaves acquired-bytes=false.
- A supported completed transfer produces a checked local artifact before materialized/admitted transitions.
- Diagnostics omit reference values and preserve the unattempted state of a second item.

Qualification: Source describes an observed integration need, not a demonstrated Sherlock defect or tested product fix.

Publication transformation: Redundant dated local-routing and no-transmission boilerplate omitted; only the generic response shape is retained.

## TR-L0037 Literal byte boundaries and aggregate process status

Source lines 37–51; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 05, 08.

A prefix verifier must compare literal byte boundaries. Synthetic reproduction: append a heading to "x\n", split immediately before that heading, and compare the exact prefix with the original. Adding another newline to a prefix that already retains its final newline must fail. Separately, a failing first command followed by a successful final command must not become overall verified success. Retain each operation's result or propagate failure explicitly; do not relax expected hashes to make verification pass.

Acceptance checks

- The exact prefix of the synthetic newline-terminated input equals the original bytes.
- The added-newline variant fails the expected hash check.
- A failed operation cannot be masked by a later successful operation.

Qualification: The source reports locally reproduced checker/wrapper errors and a corrected real-byte check, not a demonstrated Sherlock defect or product fix.

Publication transformation: Redundant routing and date text omitted.

## TR-L0052 Reachable claim links and semantic locator roles

Source lines 52–67; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 05, 06, 21.

Complete ID rosters are insufficient if all evidence/transform edges are erased. Require applicable joins or field-specific consequential gaps, and test actual traversal reachability: counts alone are not coverage. Distinguish input, derivation and output locators; do not copy analysis-section locators onto upstream inputs. Modalities of one uploaded item must retain their shared origin without asserting original synchronization. Keep semantic content review separate from structural validation. Compare byte-normalized data/hashes and actual file state, not language string-encoding metadata, when diagnosing apparent changes.

Acceptance checks

- Erased or unreachable links fail even with complete ID counts.
- Synthetic inputs, derivations and outputs retain role-correct locators.
- Two modalities share an origin without an unsupported synchronization claim.
- Equal bytes represented with different string encodings do not trigger a false file-change finding.

Qualification: The source reports reproduced local workflow/checker issues and separate content-review findings, not inspected Sherlock defects or implemented fixes.

Publication transformation: Private execution context and redundant routing statements omitted.

## TR-L0068 Versioned preservation includes later reviewed additions

Source lines 68–79; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 05, 06, 10, 23.

A verifier bound to an initial baseline does not automatically protect later additions. For a synthetic baseline-plus-extension update, retain the complete latest reviewed objects and ordered additions, not only their IDs or original subset. Reject undeclared new rows and changed old qualifications or acceptance flags. Bracket the full delegated validation call with control-integrity checks. Byte-versus-encoding diagnostic differences must be resolved without modifying data merely to silence a warning.

Acceptance checks

- Mutating an earlier object, reordering protected additions, or changing an old acceptance flag fails.
- An undeclared new row fails even if original IDs remain.
- Control-integrity checks surround the complete delegated call.
- Synthetic wrapper controls and the selected-file check are reported separately.

Qualification: The source reports passing local mutation/reordering/flag fixtures and a separately executed selected-file check; this is not a demonstrated Sherlock defect or fix.

Publication transformation: Redundant dated routing text omitted.

## TR-L0080 Later reading receipts do not certify earlier truncated displays

Source lines 80–88; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 10, 26.

A later complete small-block observation may resolve an earlier truncated-read gap without retrospectively certifying rejected displays. Preserve the pinned partial snapshot, append attributable new reading receipts, and version any completed output or consumer binding. A new observation must not silently flip old completion or human-acceptance flags.

Acceptance checks

- Earlier partial snapshot and rejected-display status remain unchanged.
- New attributable reading receipt has a distinct observation/version linkage.
- Old completion and human-acceptance flags remain unchanged unless an explicitly versioned decision changes the relevant consumer.

Qualification: Observed local workflow requirement, not a demonstrated product defect or fix.

Publication transformation: Redundant routing and date statements omitted.

## TR-L0089 Core/fringe partitions remain distinct from outer-set agreement

Source lines 89–101; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 12, 13.

Two readers may select the same outer pixel set while assigning different cells to a confident core and tentative fringe. Preserve these classifications separately. Synthetic case: reader A core {1}, fringe {3}; reader B core {3}, fringe {1}. Outer-set equality is not complete agreement; row 2 must not be filled. Neither the intersection nor union is a calibrated original-source confidence bound. Use unambiguous names for agreement and disagreement counts.

Acceptance checks

- The synthetic outer sets are equal while core/fringe agreement remains false.
- No unselected row is interpolated into the annotation.
- Neither intersection nor union is labeled a calibrated source confidence bound.
- Agreement and disagreement counts are explicitly named.

Qualification: Priority is preventing scientific overclaim from reproducible annotation. Source describes an observed workflow need, not an inspected Sherlock defect.

Publication transformation: Redundant no-source-payload and routing text omitted.

## TR-L0102 Fragment membership is not inferred from contiguous geometry

Source lines 102–111; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 12, 13.

Two separately named pieces can have a contiguous combined row set without becoming one identified stroke. A single identifier without an optional membership map must remain distinguishable from missing attribution. Preserve original schemas and labels, reject automatic multi-piece fusion, and report geometry eligibility separately from source containment or acceptance.

Acceptance checks

- Contiguous separately identified pieces remain separate.
- A legitimate single-identifier schema with no optional map is not treated as missing attribution.
- Geometry eligibility does not imply source containment or acceptance.

Qualification: The source reports both forms exercised by local synthetic controls; no inspected Sherlock defect or fix is established.

Publication transformation: Redundant local routing text omitted.

## TR-L0112 Literal uncertainty labels and documented provenance aliases

Source lines 112–122; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 06, 12.

Preserve a reader's literal uncertainty vocabulary: fringe_only and identity_conflict are not interchangeable. Represent unknown fragment membership separately; a known-label fringe remains distinct from either unknown or conflicting attribution. Accept only documented pin/target schema aliases, reject contradictory aliases, and distinguish an originally declared source pin from a verifier's later additional pin. Check changed dependencies before comparing actual records.

Acceptance checks

- Different literal labels survive normalization.
- Unknown membership remains separate from known-label fringe.
- Undocumented or contradictory aliases fail.
- Original and verifier-added pins retain separate provenance.
- Changed dependency fixtures fail before real-record comparison.

Qualification: Source reports locally reproduced and exercised workflow needs, not a demonstrated Sherlock defect or delivered fix.

Publication transformation: Redundant routing and no-sensitive-payload text omitted.

## TR-L0123 Schema dispatch cannot silently drop list-valued membership

Source lines 123–134; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 12, 13.

An old normalizer may recognize a membership map under one coordinate schema while ignoring a list-valued membership field under another. In a synthetic two-piece record, unadapted classification admitted a single-fragment rectangle; an explicit copy-only adapter retained both memberships and excluded it. Dispatch only declared schemas, preserve all originals and membership unions, reject conflicting aliases, and prevent an unsupported field combination from silently weakening the single-fragment rule.

Acceptance checks

- Both synthetic memberships survive the copy-only adapter.
- The multi-piece record is excluded from a single-fragment rectangle classification.
- Unsupported field combinations and conflicting aliases fail rather than lose fields.

Qualification: Source reports a local-method hazard and tested adapter used by new local integration; it states no saved historical result was shown affected. No inspected Sherlock bug or product fix is established.

Publication transformation: Redundant date/routing language omitted.

## TR-L0135 Semantic qualifications survive additive inventory revision

Source lines 135–148; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 10, 12, 24.

An inventory can preserve all old measurements exactly while a rewritten summary drops a still-applicable limitation. Synthetic case: an older annotation batch has broad conflict references; a later batch has precise references; both remain in the combined dataset. Preserve each batch's qualifier and scope in current summaries. A newer schema does not retroactively repair older data. Review semantic changes alongside object/hash equality. If a lapse is found after output freeze, preserve that version and make an explicit narrowly checked narrative correction without changing numerical arrays.

Acceptance checks

- Combined summaries retain the older batch's limitation and the newer batch's different scope.
- Object/hash equality alone cannot clear a dropped qualifier.
- A post-freeze correction identifies its parent and leaves numerical arrays unchanged.

Qualification: Source describes a local authoring lapse caught by separate review, not a demonstrated Sherlock defect or product fix.

Publication transformation: Redundant routing/date statements omitted.

## TR-L0149 Canonicalize root and child consistently across path aliases

Source lines 149–156; requirement. SFB mapping: SFB-005. Earlier digest topics: 05, 06.

Resolving a child path but not its root may misconstruct a relative dependency key across an operating-system alias. Test canonical and aliased temporary roots and normalize both sides consistently. Retain strict allowed-path boundaries; do not widen them merely to make a test pass.

Acceptance checks

- Canonical and aliased temporary-root fixtures resolve the same allowed artifact.
- The same strict path boundary is enforced in both representations.

Qualification: Source reports a local synthetic failure repaired before historical output; no Sherlock implementation was inspected or changed.

Publication transformation: Actual paths and redundant transmission language are not included.

## TR-L0157 Resolve manifests against their individual owners

Source lines 157–165; requirement. SFB mapping: SFB-005. Earlier digest topics: 06.

Two manifests may declare different owners and therefore different relative-path bases. Resolve each map against its own owner before normalizing combined keys. Synthetic parent/child aliases must resolve to one unchanged artifact, and before/after byte drift must fail.

Acceptance checks

- A fixture with distinct declared owners resolves each map correctly before sample selection.
- Parent/child aliases converge on the same unchanged artifact.
- Before/after drift fails verification.

Qualification: Source reports a local consumer error that failed before sample selection and two passing regression checks, not an inspected Sherlock defect.

Publication transformation: Private paths and redundant date/routing text omitted.

## TR-L0166 Listed-pin success is not complete dependency closure

Source lines 166–173; requirement. SFB mapping: SFB-005. Earlier digest topics: 06, 10.

Checking every listed pin can still miss dependencies of an already pinned receipt. Independently reconstruct the required closure and reject an incomplete candidate before release. Preserve the candidate and its code; extend the complete receipt dependency map under a separate output identity, asserting every non-dependency scientific field unchanged. Do not relabel a successful listed-pin hash check as full closure.

Acceptance checks

- An independently reconstructed closure finds dependencies omitted from a pinned receipt map.
- The incomplete candidate fails before release and remains preserved.
- A repaired output has a distinct identity, complete closure, and unchanged non-dependency scientific fields.

Qualification: Source reports a local missed-closure failure and repair, not a Sherlock product fix.

Publication transformation: The incidental count of omitted dependencies is not needed to exercise the failure; artifact-specific context omitted.

## TR-L0174 Human responses bind to full packet identity

Source lines 174–180; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 10, 11.

Stable sample labels may identify different coordinates after a declared input extension. Bind display and copied human responses to the packet ID and full byte hash. Preserve the old packet and every uninspected state; prohibit automatic acceptance transfer based on label equality.

Acceptance checks

- A same-label/two-version synthetic packet does not inherit earlier human acceptance.
- Response binding includes packet ID and full hash, not only label.
- Old packet and uninspected states remain intact.

Qualification: Source proposes this generic product test; it is not a delivered fix or permission for case access.

Publication transformation: Redundant date/routing context omitted.

## TR-L0181 Pin caches must not skip recursive dependency expansion

Source lines 181–190; requirement. SFB mapping: SFB-005. Earlier digest topics: 06.

A wrapper may pre-pin a JSON input and then trigger an already-pinned early return in a recursive helper, silently skipping that file's dependencies. Synthetic case: pre-pin A and B where A declares B and B declares C; require complete dependency closure. C must be included and changed C bytes must fail despite A/B being cached. Keep traversal-expansion state separate from the byte-pin map.

Acceptance checks

- Pre-pinning A and B does not prevent discovery of C.
- Changed C bytes fail with unchanged cached A/B.
- Nested-map and script dependency cases are exercised.

Qualification: Source reports a local fix and passing nested-map/script regressions before historical output, not an inspected Sherlock defect or product fix.

Publication transformation: Redundant routing/date text omitted.

## TR-L0191 One visible band is not two independently identified series

Source lines 191–199; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 10, 12, 13.

An overplotted pair and one remaining series may look alike. Preserve unknown membership rather than duplicating one observation into apparent two-series agreement. Retain a later correction alongside the original reading, even where every checklist field had been filled.

Acceptance checks

- A synthetic ambiguous band remains of unknown membership rather than becoming two observations.
- Completeness of checklist fields does not prevent an explicit versioned correction.
- Original reading remains preserved alongside its correction.

Qualification: Observed annotation/inference risk, not a verified Sherlock defect or implementation approval.

Publication transformation: Redundant no-payload/routing language omitted.

## TR-L0200 Literal ink annotations and versioned cell-level errata

Source lines 200–210; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 10, 12.

A compact manual run may incorrectly include exactly white cells as tentative visible ink. Compare every selected cell to the preserved source; distinguish an explicit uncertainty envelope from an ink annotation; flag mismatches without silently editing the frozen reading. A versioned erratum must identify its parent, exact membership changes, unchanged remainder and post-exchange status. Keep the original freeze as history, not as a new independent reading. Repeatable correction does not validate remaining annotations.

Acceptance checks

- White-cell-as-ink synthetic misclassification is detected.
- The frozen reading is not silently changed.
- Erratum identifies parent, exact changes, unchanged remainder and exposure status.
- Correction neither becomes independent evidence nor certifies the remaining cells.

Qualification: Source reports a reproduced local transcription failure, not a new product-defect claim.

Publication transformation: Redundant date/routing text omitted.

## TR-L0211 Fringe-only boundary truncation

Source lines 211–222; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 12, 13.

A selected faint edge can touch a crop boundary while its confidently visible core lies outside the target. A nonempty core is not required for every truncated fragment. Permit a nonempty fringe-only identified boundary fragment, reject empty truncation and invented flags, and retain unknown outside-crop continuation separately from a true endpoint. If a validator limitation is repaired, do not rewrite earlier frozen outputs; record whether they were affected.

Acceptance checks

- Nonempty fringe-only identified boundary fragment passes the declared truncation representation.
- Empty truncation and invented truncation flags fail.
- Unknown continuation is not classified as an endpoint.
- Earlier frozen outputs remain preserved.

Qualification: Source reports a demonstrated local validator limitation and tested fixture, with prior frozen outputs stated unaffected; not an inspected Sherlock defect.

Publication transformation: Redundant date/routing text omitted.

## TR-L0223 Named reader roles cannot depend on dictionary order

Source lines 223–233; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 12.

Explicitly select named primary and secondary readers before forming directional differences; do not infer roles from dictionary insertion order. Reverse input mapping order in a synthetic test and require identical output, with primary-only and secondary-only cells still attributed to the correct reader.

Acceptance checks

- Reversed mapping insertion order yields identical role-correct results.
- Directional cell differences remain attached to named reader identities.

Qualification: Source reports a potential API-order weakness, a passing local adapter/control, and saved earlier runs using the expected order; those runs are not shown wrong. Not a verified Sherlock fix.

Publication transformation: Redundant routing/date text omitted.

## TR-L0234 Source-region keys, legitimate reading reuse and nonempty conflict references

Source lines 234–248; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 06, 12, 21.

Two source regions for one named series may share native coordinates while source images and transforms differ. Retain both region/source keys, reject swapping or collapsing them, and never infer a seam join from the shared series label. Overlap may reuse an actual prior reading only after exact source-cell equality and explicit coverage/receipt linkage; reused reading is not a second observation. A named but empty unassigned band cannot receive a valid conflict reference: require nonempty same-column material and a recorded reason while retaining empty records separately from missing records.

Acceptance checks

- Equal coordinates under different source/transform keys remain distinct.
- Swapped or collapsed region/source keys fail.
- Reading reuse requires source-cell equality plus receipt/coverage linkage and is counted once.
- A named empty band cannot supply conflict material.
- Empty and missing records remain distinct.

Qualification: Source reports passing local controls and no changes to original annotations. Priority is attribution and missingness integrity; not verified Sherlock defects or fixes.

Publication transformation: Redundant date/routing statements omitted.

## TR-L0249 Crop completion is not full-scope measurement admission

Source lines 249–259; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 13, 24.

Every item in a fixed crop roster can be finished while broader source-region obligations remain. Preserve separate states for qualitative inspection, literal footprint, justified measurement bounds, admitted support and actual human acceptance. Join completed crops to the original full-scope inventory, retain unmeasured and unresolved portions separately, and refuse to convert unknown common support into an empty domain. A context halo does not enlarge the target; overlapping older work is not new evidence.

Acceptance checks

- Completed crop roster is evaluated against original broader scope.
- Unmeasured and unresolved regions remain distinct.
- Unknown common support does not become empty support.
- Context halo and overlap do not enlarge measured scope or evidence count.

Qualification: Local workflow risk, not a demonstrated Sherlock defect.

Publication transformation: Redundant archived-routing context omitted.

## TR-L0260 Recovery batches need a decision-relevant prerequisite

Source lines 260–271; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 24.

Repeated successful recovery batches can postpone an actual measurement-admission decision even when the controlling protocol permits partial domains. Before another recovery batch, name the limiting condition and expected decision impact. More annotations do not establish completion, and accessible unmeasured regions must not be relabeled unreadable. Synthetic case: two completed local regions and one unresolved contact. The next action must assess admission of the existing regions or explain the specific prerequisite the next recovery resolves.

Acceptance checks

- The synthetic two-region/one-contact state produces an admission assessment or a named recovery prerequisite with expected decision impact.
- Accessible unmeasured material is not called unreadable.
- Annotation count alone cannot establish completion.

Qualification: Source states this transition was adopted locally, but the proposed product test was not implemented or run. Not a verified Sherlock defect.

Publication transformation: Redundant routing/date text omitted.

## TR-L0272 Cross-series ownership conflicts across all reader pairs

Source lines 272–280; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 12, 13.

Two different series, each read twice, may use overlapping source cells. Cover all four reader pairings, both confidence classes and unassigned material. Same row numbers in different columns must not intersect. Preserve every cross-series intersection as a candidate attribution conflict, not corroboration or permission to overwrite either original.

Acceptance checks

- All four reader pairings and both confidence classes are tested, including unassigned material.
- Same-row/different-column cells do not intersect.
- Cross-series intersections remain conflicts with both original annotations preserved.

Qualification: Source reports passing tests in a local comparison harness, not in Sherlock.

Publication transformation: Redundant routing and no-payload text omitted.

## TR-L0281 Conditional coordinate windows are not established curve support

Source lines 281–291; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 13, 18.

A visible dash cap may occupy a pixel without its generating path covering the entire column. A selected-cell enclosure does not establish an error bound for omitted halo. Preserve identity, full-column existence and enclosure assumptions separately; retain competing reader/axis alternatives. Marginal boxes sharing one calibration are neither independent errors nor automatic support. Arithmetic conversion checks exercise the conversion, not those assumptions.

Acceptance checks

- Identity, full-column existence, selected-cell enclosure and omitted-halo assumptions have separate status.
- Competing reader and axis alternatives remain visible.
- Shared-calibration marginal boxes cannot be treated as independent or automatically supported.

Qualification: Source reports local synthetic and complete arithmetic checks but not validation of the assumptions. Observed workflow need, not verified Sherlock defect.

Publication transformation: Redundant routing text omitted.

## TR-L0292 Joint support precedes uncertain coordinate mapping

Source lines 292–307; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 12, 13, 18.

Presence of both series somewhere does not establish overlapping comparison support. Compute overlap in shared source geometry before uncertain coordinate mapping. Two disjoint intervals shifted by one shared uncertain offset can have overlapping marginal hulls without ever intersecting together. Check cross-route ownership even within one reader: a tentative edge cell can occur in both series although each route's core/fringe sets are internally disjoint. Preserve original selections, flag shared cells, retain unaffected local intervals, and do not convert conditional coverage or an empty candidate set into accepted support or a zero curve.

Acceptance checks

- Disjoint shared-offset intervals remain jointly disjoint despite overlapping marginal hulls.
- Cross-route shared cells are detected within one reader as well as all four reader combinations.
- Original selections and unaffected intervals remain intact.
- Conditional coverage and empty candidates do not become admitted support or a zero curve.

Qualification: Source reports twenty local producer controls, 26 separate checker controls and full calculation replay passing; these synthetic local controls are not a Sherlock product test or verified fix.

Publication transformation: Redundant date/routing text omitted.

## TR-L0308 Claim-specific prerequisites do not expand silently

Source lines 308–316; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 24.

A prerequisite for full physical-system validation must not silently become a gate for a narrower published-graph comparison. Preserve separate claims and their actual dependencies in separate rows. Reject both automatic physical-system promotion from graph agreement and blanket withholding of graphical analysis pending a system-level test.

Acceptance checks

- Graph comparison and physical-system validation have separate claim/dependency rows.
- Graph agreement cannot validate the whole system.
- A system-level prerequisite cannot block a narrower graph comparison without a claim-specific dependency.

Qualification: Source describes a local report-wording issue corrected by review, not an inspected product bug or product fix.

Publication transformation: Redundant no-payload/delivery language omitted.

## TR-L0317 Conditional sample namespaces and finite-renderer ambiguity

Source lines 317–329; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 11, 13, 21.

Distinguish a conditional review sample from an originally required accepted-support sample. A length-quantile target may lie on an excluded shared endpoint even if adjacent intervals merge for length bookkeeping. Keep that target unresolved, retain missing primary coverage instead of substituting a peer, display every same-position alternative, and never treat a UI click as a human response. Separately, finite-renderer controls may have identical pixels with different subpixel support/extrema. Preserve that renderer-specific limitation without claiming historical error rates.

Acceptance checks

- Conditional and accepted-support samples use distinct namespaces.
- Excluded endpoint targets remain unresolved after interval merging.
- Missing primary coverage is not filled by peer substitution.
- All same-position alternatives are displayed.
- Automated UI clicks do not create human responses.
- Identical rendered pixels do not establish unique subpixel support or historical error rates.

Qualification: Source reports local controls exercised; observed workflow need, not an inspected Sherlock defect or product fix.

Publication transformation: Redundant routing/date statements omitted.

## TR-L0330 Route-specific conflicts and independently recorded helper pins

Source lines 330–342; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 06, 12.

A band tentatively belonging to route B must not make an unrelated empty route A conflicted. Require explicit candidate-route labels, including an explicitly supplied empty list; reciprocal same-column references; and nonempty material for conflict status. Missing labels must not silently default to empty. Preserve pre-fix code for exposed failures. Verify any separately recorded expansion-helper pin, not only files in the primary input map: changed helper bytes must fail even if frozen annotation bytes are unchanged.

Acceptance checks

- Route-B uncertainty does not create unrelated route-A conflict.
- Missing candidate labels fail rather than silently becoming an empty list.
- Conflict status requires nonempty same-column material and reciprocal references.
- Changed separately pinned helper bytes fail despite unchanged annotations.

Qualification: Source reports local synthetic failures and repaired passing checks with pre-fix code retained, not verified Sherlock defects or source-reading corrections.

Publication transformation: Redundant routing and date text omitted.

## TR-L0343 Aggregate band prose is weaker than machine-enforced fragment ownership

Source lines 343–352; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 12, 13.

Prose can assign two pieces of an aggregate uncertainty band to different candidate routes while both machine references target the entire band. Do not describe this as machine-enforced fragment ownership. Preserve the aggregate schema and notes, distinguish them from explicit member-level references, and prevent downstream support construction from silently assigning every band cell to each route. All-ink set comparisons may remain valid without the stronger identity claim.

Acceptance checks

- Aggregate references remain distinguishable from member-level ownership.
- Support construction cannot assign all aggregate-band cells to every candidate route.
- Valid all-ink comparisons are retained without upgrading their identity claim.

Qualification: Observed local encoding limit, not a verified Sherlock defect; original frozen observations remain unchanged.

Publication transformation: No substantive source content omitted.

## TR-L0353 Multiple disjoint uncertainty bands at one column

Source lines 353–366; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 12.

A validator/index must not assume only one uncertainty band per column. Synthetic example: at one x, band U selects row 1 for route A and band V selects row 4 for route B. Retain both originals under (x, band_id), preserve each reciprocal reference, union them only for an explicitly all-visible-ink comparison, reject cross-route references, and never overwrite by x alone. An explicit schema adapter may validate and translate local-ink status labels without rewriting originals or silently changing ownership.

Acceptance checks

- Both disjoint same-column bands survive indexing.
- Each band retains its correct reciprocal route reference.
- Wrong-route reference fails.
- Only an explicitly all-ink comparison unions the bands.
- Schema translation preserves original records and ownership.

Qualification: Source reports a demonstrated local validator/index limitation and new synthetic retention/rejection tests, not an inspected Sherlock defect or product fix.

Publication transformation: Redundant date/routing text omitted.

## TR-L0367 Replay commands require exact frozen scope

Source lines 367–378; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 06, 10, 23.

Saving an executable and script is insufficient if a required scope argument is omitted. Preserve a working command in an external receipt without rewriting the original output. Commands must reproduce the exact declared scope; partial code and outputs remain immutable when later scope is added. Expanded versions require distinct identities and complete dependency pins. Distinguish one-region from all-region replays and fail before reading inputs if required frozen scope is missing.

Acceptance checks

- Missing frozen-scope argument fails before input reads.
- One-region and all-region commands retain distinct declared scopes.
- Working receipt supplements rather than rewrites old output.
- Expanded replay has distinct identity and complete pins.

Qualification: Source reports a local receipt defect, not an inspected Sherlock product defect or verified product fix.

Publication transformation: Private executable, script and receipt locators omitted; generic requirements retained.

## TR-L0379 Independent inert reconstruction includes declared data updates

Source lines 379–390; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 23.

An independent checker that reads an initial configuration literal but ignores later explicit data-only updates can fail historical equality. Preserve that failure and implementation. A versioned correction must handle only declared data operations, retain list order and update semantics, reject unsupported mutations and pass synthetic fixtures before replay. Do not execute producer code or copy its result to manufacture independence. Synthetic example: a declared map, literal submap update and literal list append must all reconstruct; an unknown operation fails closed.

Acceptance checks

- Literal map, declared submap update and literal list append reconstruct with correct order and update semantics.
- Unknown mutation fails closed.
- The producer is not executed and its output is not copied as an allegedly independent reconstruction.
- Failure and pre-fix implementation remain preserved.

Qualification: Local reproducibility safeguard; it changes neither source observation nor establishes a verified Sherlock defect.

Publication transformation: Redundant routing/date language omitted.

## TR-L0391 Coverage-schema dispatch verifies complete source-cell unions

Source lines 391–400; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 06, 12, 21, 23.

A checker supporting direct column blocks may not support declared same-source shared rectangles. Preserve failed versions. A separate repair must check exact schema, source identity, typed bounds, referenced-context containment, receipts, complete source-cell union and equality. Counts or overlapping areas alone do not establish coverage; reject ambiguous schemas and gaps. Passing coverage checks verifies recorded coverage, not independently witnessed perception.

Acceptance checks

- Direct-column and declared shared-rectangle forms are explicitly dispatched.
- Wrong source, invalid typed bounds, containment failures, missing receipts, union gaps or ambiguous schemas fail.
- Equal counts or overlapping areas alone cannot pass coverage.
- Recorded coverage is not labeled independent perception.

Qualification: Source reports a repaired local full audit passing without annotation rewrites, not a verified Sherlock fix.

Publication transformation: Redundant routing context omitted.

## TR-L0401 Integrity metadata can defeat blinding

Source lines 401–410; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 04, 21.

A permitted integrity manifest may disclose truth-related filenames and equal hashes while the actual answer file is withheld. Minimal synthetic test: give a reader two unnamed candidate images plus a manifest containing alternative labels and hashes. A truth-withheld packet must use only its own allowlisted artifact manifest. Any exposure remains a blinding limitation; it cannot be relabeled independent discovery retroactively.

Acceptance checks

- Truth-withheld packet excludes answer-revealing labels/hash joins outside its allowlist.
- Synthetic manifest leakage is recorded as exposure.
- Exposure prevents a retrospective claim of independent discovery.

Qualification: Observed local workflow issue, not an inspected product defect.

Publication transformation: Redundant date/routing text omitted.

## TR-L0411 Shared exclusion rules make sensitivity runs correlated

Source lines 411–429; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 16, 21, 26.

An exploratory detector sweep can vary contrast thresholds while retaining one color exclusion; a continuous synthetic nonwhite band may then have identical artificial gaps in every run. Reproducibility and parameter agreement do not validate detected topology. Preserve shared preprocessing and exclusion dependencies in sensitivity/validation reporting and do not label correlated runs independent evidence. Minimal fixture: alternate pale and saturated colored pixels along an uninterrupted band, apply a fixed color cutoff with several contrast cutoffs, and retain known-continuous ground truth alongside broken detections. Preserve failed control, shared rule and narrowed claim; passing replay must not promote line identity or erase the control. Separately, a notLoaded task state alone does not establish archival status.

Acceptance checks

- All broken detections retain their shared color-exclusion dependency and known-continuous synthetic ground truth.
- Parameter agreement and repeatability do not certify topology or independence.
- Failed control and narrowed claim remain preserved after successful replay.
- notLoaded alone cannot establish archival status.

Qualification: Priority is a scientific-validity safeguard before consequential measurement. Source reports an observed workflow need, not a demonstrated Sherlock defect or implementation/fix.

Publication transformation: Private destination/current-read details and repeated routing history omitted; the reusable status-inference constraint is retained.

## TR-L0430 Historical routing lookup is not scientific progress

Source lines 430–435; context. SFB mapping: SFB-005. Earlier digest topics: 26.

The source records a paginated archived-destination lookup using the returned cursor and limiting surfaced metadata to the relevant destination. A lookup did not constitute send, unarchive, replacement or rerouting, nor scientific progress or feedback delivery.

Qualification: Historical operational receipt, not a new product acceptance requirement.

Publication transformation: Exact date, target identity/title, and operational page counts omitted.

## TR-L0436 Prospective outcome-independent human-sample selection

Source lines 436–451; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 10, 11, 21, 24.

A workflow that requires selected human checks must specify how samples are selected. Freeze an outcome-independent selection rule and complete target census before discrepancy results. Preserve unavailable targets, boundary ties, coincident native footprints and original failed selections rather than replacing them with convenient points. Retain source/registration version, actual inspected coverage and attributable response. Require deterministic replay from the frozen inventory. A passed spot-check is neither whole-source validation nor a calibrated confidence interval.

Acceptance checks

- Frozen outcome-independent rule deterministically replays the full target census.
- Unavailable targets, ties, coincident footprints and failed selections survive without convenient substitution.
- Source/registration version, inspected coverage and attributable human response are recorded.
- Passing a spot-check cannot yield whole-source or calibrated-interval claims.

Qualification: Priority is evidence integrity before consequential use. Source describes an observed method gap, not an inspected Sherlock defect or new issue family.

Publication transformation: Redundant date/routing/no-case-payload statements omitted.

## TR-L0452 Historical archival-state verification

Source lines 452–459; context. SFB mapping: SFB-005. Earlier digest topics: 26.

The source distinguished a loaded-state response from an actual archived-destination listing. An invalid listing-limit request was rejected; a corrected supported-limit request located the destination. No send, unarchive, replacement or implementation request followed from the lookup.

Qualification: Historical routing receipt. A display/loading status alone is not archival evidence.

Publication transformation: Date, exact task title/identifier and tool-specific request limits omitted as incidental routing context.

## TR-L0460 Feedback transition evidence and exact disclosure gate

Source lines 460–461; requirement. SFB mapping: SFB-005. Earlier digest topics: 04, 26.

Keep observed/proposed, sent, acknowledged/triaged, fix-reported and locally verified states distinct. Acknowledgment is not a fix. Include date, source/version when available, impact, safe reproduction and acceptance check. Before every send, apply the privacy rule to exact payload and destination. Case-sensitive and sensitive security details remain local pending specific approval; prefer a harmless synthetic example.

Acceptance checks

- Every claimed lifecycle transition has appropriate evidence.
- Acknowledgment cannot set fixed or verified status.
- Feedback includes dated scope, available source/version, impact, safe reproduction and acceptance criteria.
- Exact destination/payload privacy review occurs before transmission.

Qualification: Source states a feedback handling requirement; it does not authorize any new disclosure.

Publication transformation: No substantive requirement omitted.

## TR-L0462 Delivered audio is not necessarily perceptually accessible

Source lines 462–478; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 01, 17.

A valid synthetic speech file may pass generation and byte-delivery checks while the receiving interface explicitly omits audio because it lacks that modality. Auditory perception has not occurred. Retain separate file-ready, emitted, perceptually accessible, listened and human-reviewed states. Unsupported modality leaves events unknown, not an empty list interpreted as no events. Preserve the failed route, offer a local human-review packet, and do not loop without a capability change. Even a successful clean-speech control does not certify noisy-event detection or causal timing.

Acceptance checks

- Unsupported-modality response leaves perception/listening false and events unknown.
- Generation/delivery success cannot become auditory review.
- Failed route is retained with a local human-review alternative.
- Unchanged unsupported routes are not retried indefinitely.
- Clean-speech success does not certify noisy event detection or causal timing.

Qualification: Source reports an observed caller workflow limit, not an inspected Sherlock defect. Priority is preventing fabricated media review and enabling a genuine listening handoff.

Publication transformation: Real media, paths, interface-specific payloads and redundant routing/date statements omitted.

## TR-L0479 Historical paginated routing recheck

Source lines 479–484; context. SFB mapping: SFB-005. Earlier digest topics: 26.

A later paginated archived-destination listing located the designated destination. Archival status was attributed to that listing, not a notLoaded field. No send, unarchive or replacement was performed.

Qualification: Historical operational receipt; generic lifecycle distinction already retained in the requirement units.

Publication transformation: Exact date, destination title/identifier and page counts omitted.

## TR-L0485 Acquisition-route history and documentary roles

Source lines 485–499; requirement. SFB mapping: SFB-005. Earlier digest topics: 01, 03, 22.

Preserve a reader-only failure followed by a separately declared successful direct acquisition, without rewriting the failure or calling it server refusal. A later request may enclose earlier design comments: request, attachment, agency response, revision and installed-state acceptance remain separate roles. Reject promotion of a folder label to an instruction or a review comment to an unresolved historical defect. Distinguish a document's own date from earlier documents it modifies, and listed sheets from selected issued sheets or completed work.

Acceptance checks

- A failed reader route and later successful direct acquisition coexist with separate receipts.
- Request, enclosed comments, response, revision and installed-state acceptance remain distinct.
- Folder labels are not instructions and comments are not automatically unresolved defects.
- Document date and dates of modified predecessors remain separate.
- Listed, selected-issued and completed sheets/work remain separate states.

Qualification: Workflow source-role checks, not an inspected Sherlock bug or separate product issue.

Publication transformation: Source identities, actual dates and redundant routing language omitted.

## TR-L0500 Reader projection, acquisition error body and original differ

Source lines 500–511; requirement. SFB mapping: SFB-005. Earlier digest topics: 01, 03, 21.

A reader may display selected passages while direct acquisition returns an error body. Preserve the exact projection, requested windows and failed response as distinct artifact roles. Hashing either derivative does not hash the unavailable original. Synthetic case: partial text view, HTTP 403 HTML body, and a second reviewer limited to the shared view. Reject claims of original acquisition, whole-document coverage or independent corroboration; allow a separately labeled interpretation review.

Acceptance checks

- Projection, requested windows and failed response have separate artifact identity/coverage.
- Derivative hashes cannot be labeled original-source hashes.
- The limited second reviewer may provide interpretation review, not independent original-source corroboration.
- Original acquisition and whole-document coverage remain unestablished.

Qualification: Source identifies a P2 workflow need under SFB-005, not an inspected defect or implemented fixture.

Publication transformation: Actual source paths, identifiers, dates and routing statements omitted.

## TR-L0512 Prospective identifier normalization and count grain

Source lines 512–522; requirement. SFB mapping: SFB-005. Earlier digest topics: 02, 03.

A synthetic catalog may use A.B.C. while an initial literal query uses ABC. Preserve original zero/match coverage and a prospectively declared normalization pass separately. Report token, line, logical-record and source-family counts as different quantities. A known original can lack its drawing number in metadata: a metadata nonmatch is not original-record absence. Reject retroactive query rewriting and double-counting link labels/URLs.

Acceptance checks

- Literal and normalized searches retain separate declarations and coverage.
- Token, line, logical-record and source-family totals are not conflated.
- Known-original metadata nonmatch is retained as a counterexample to absence inference.
- Link label and target URL do not duplicate evidence counts.

Qualification: Reproducible local workflow need, not an inspected product defect.

Publication transformation: Only explicitly synthetic identifiers retained; redundant routing/date statements omitted.

## TR-L0523 Embedded token leads differ from exact identifiers

Source lines 523–530; requirement. SFB mapping: SFB-005. Earlier digest topics: 02.

A short token Q-1 may match inside A-Q-1 or Q-1.1. Preserve the complete original field and distinguish token leads from exact identifiers; exercise compound cases before selection. A known source under a generic nonmatching label remains a counterexample to content-absence inference.

Acceptance checks

- Q-1, A-Q-1 and Q-1.1 remain distinct exact identifiers despite token matches.
- Complete original field is preserved.
- Generic metadata nonmatch does not establish missing content.

Qualification: Extension of existing search acceptance fixture, not a new issue or verified fix.

Publication transformation: Only synthetic labels retained; actual source reference and routing/date text omitted.

## TR-L0531 Catalog introductions define count and link grain

Source lines 531–541; requirement. SFB mapping: SFB-005. Earlier digest topics: 03.

A catalog introduction may define counts as folder totals and links as the first document, although a row alone appears to describe a multi-page download. Carry the parent count/link definitions into selection, preserve the original row-only expectation and its correction, and distinguish complete-file from complete-folder coverage. An expected first-document length is not a failed download or missing evidence.

Acceptance checks

- Selection inherits introduction-level count/link definitions.
- Original mistaken expectation and correction both remain recorded.
- A complete first document is not called a failed folder download.
- Complete-file and complete-folder coverage remain distinct.

Qualification: Source reports a local workflow error corrected by the introduction, not an inspected Sherlock defect or fixed product behavior.

Publication transformation: Actual catalog values, identities and redundant date/routing statements omitted.

## TR-L0542 Acquisition-time joins versus current-state enrichment

Source lines 542–553; requirement. SFB mapping: SFB-005. Earlier digest topics: 02, 03.

Saved metadata may remain identical while a live local-filename join changes following a new acquisition. Preserve the acquisition-time inventory or label the join as current-state enrichment; its change is neither source mutation nor failed historical reproduction. Preserve capped queries, previous-page availability, missing termination evidence, absent empty-result keys and inconsistent reported counts. Correcting a local parser must not change frozen extraction. Split-cover handling belongs to the existing document-role fixture rather than a duplicate issue.

Acceptance checks

- Acquisition-time and current-state joins are distinguishable.
- New local files do not create a false source-mutation or reproduction-failure claim.
- Caps, prior pages, uncertain termination, absent keys and inconsistent counts remain explicit.
- Frozen extraction bytes remain unchanged after parser correction.

Qualification: Source reports corrected local parser defects, not inspected Sherlock bugs.

Publication transformation: Actual filenames, source identity and redundant routing/date statements omitted.

## TR-L0554 Missing descriptive fields and strict-versus-diagnostic success

Source lines 554–563; requirement. SFB mapping: SFB-005. Earlier digest topics: 02, 03, 05.

When a descriptive field is omitted, retain strict-contract failure, supplied fields and quarantined occurrences. Do not fill the omission with a literal sentinel or discard its identifier. Reconcile total, strict-valid and quarantined counts at occurrence and unique-ID grain. A separate diagnostic success is not a full-contract pass. Include a known-positive content item missed by one terminated keyword query but retrieved by another; locator success does not certify OCR/index coverage.

Acceptance checks

- Omitted descriptive field stays missing with its identifier and quarantined occurrence retained.
- Total equals the properly reconciled strict-valid and quarantined populations at both required grains.
- Diagnostic success cannot clear strict failure.
- Known-positive missed-query control prevents OCR/index-recall claims from a locator control.

Qualification: Generic workflow extension, not an inspected product defect.

Publication transformation: Real catalog/source identifiers and redundant routing/date text omitted.

## TR-L0564 Keyword matches need source-context roles and pending enclosures stay pending

Source lines 564–571; requirement. SFB mapping: SFB-005. Earlier digest topics: 02, 03, 22.

A keyword-positive catalog precaution and an actual measurement report missed by the query require source-context role review before a match becomes a measured event or a nonmatch becomes absence. A cover saying an enclosure will follow upon receipt preserves a pending-delivery state. A separate review request is not completed review. Neither pending enclosure nor requested review may be promoted to later completion without evidence.

Acceptance checks

- Precautionary keyword match is not labeled an actual measurement/event.
- Missed measurement report defeats absence inference from that query.
- Future enclosure and review request remain pending/requested until separately supported.

Qualification: Extension of search/source-role fixture, not a new product-defect claim.

Publication transformation: Actual source content and routing/date text omitted.

## TR-L0572 Actual attachment identity and typed dimensions outrank label expectations

Source lines 572–581; requirement. SFB mapping: SFB-005. Earlier digest topics: 03, 19, 22.

Synthetic case: a cover promises drawings A/D while supplied title blocks identify C/F for another subsystem of the same project. Preserve both descriptions and classify actual attachments; do not rewrite them to match the catalog or infer intent from mismatch. Reject joining equal numerical dimensions if one is platform height and the other conduit diameter.

Acceptance checks

- Cover claims and actual title-block identities remain separately recorded.
- Attachments are classified from actual content without catalog-driven rewriting.
- Mismatch alone does not establish intent.
- Equal numbers with different quantity roles cannot be joined.

Qualification: Generic attachment/quantity-role extension, not a new defect or product fix.

Publication transformation: Only synthetic labels and dimensions' roles retained; redundant routing/date text omitted.

## TR-L0582 Annotated copies preserve unknown authorship and shared family

Source lines 582–589; requirement. SFB mapping: SFB-005. Earlier digest topics: 03, 22.

One unmarked copy may say included while related copies have a handwritten consult separate file note. Preserve the annotation, unknown author/date and common source family. Do not silently overwrite the printed text or count versions as independent events. Reject treating every copy as promising an enclosure and reject treating the annotation alone as suppression.

Acceptance checks

- Printed text and handwritten modification remain separately preserved.
- Unknown annotation author/date remain unknown.
- Related versions remain one source family rather than independent events.
- Neither universal enclosure promise nor suppression is inferred from the annotation alone.

Qualification: Generic workflow extension, not an inspected product bug.

Publication transformation: Source identities and redundant routing/date text omitted.

## TR-L0590 Experimental endpoints, interventions and separate load cases

Source lines 590–604; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 20, 22.

Synthetic case: an assembly earns a temperature-limited rating; a later loaded run stops for safety before support failure; an instrument’s recording stops before heating stops; an abstract misassigns the longest run to another boundary condition. Retain rating, damage, observed support, observation stop, heating stop and unknown later behavior as separate events. Record interventions and valid sensor intervals. Never sum separately analyzed load cases into an invented performed load. Correct current summaries from detailed records while preserving conflicting source statements and favorable design rationale.

Acceptance checks

- Rating, damage, support, observation/heating stops and unknown later response are separate records.
- Interventions and valid sensor intervals remain explicit.
- Separate analyzed loads cannot be reported as one executed combined experiment.
- Corrected summary retains conflicting abstract/source statements and favorable rationale.

Qualification: Observed investigation-workflow need, not an inspected Sherlock bug or verified fix.

Publication transformation: Actual experiments, values, sources and redundant routing/date text omitted; the original explicitly synthetic reproduction is retained.

## TR-L0605 Validation reference, metric, calibration and model-version roles

Source lines 605–618; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 19, 24.

Synthetic case: a report calls a code-translation check validation, separately uses physical connector tests to select capacity/interface, and compares reduced and detailed models before changing a downstream material law. Preserve reference type, response metric, experimental denominator, calibration role and model version at each step. Close displacement agreement must not erase divergent forces or become heated-system validation. Physical component support must not disappear merely because system-level comparison is unlocated. Keep reported, executed, reproduced and independently validated states distinct. A wrong page-offset probe leaves existing derivatives excluded until correctly scoped; it must not silently count them reviewed.

Acceptance checks

- Each validation/calibration step retains reference, response metric, denominator and model version.
- Displacement agreement coexists with force divergence and does not establish heated-system validity.
- Narrow physical component evidence remains available despite missing system validation.
- Reported/executed/reproduced/independently validated states are separate.
- Wrong-offset derivatives remain excluded pending proper scope review.

Qualification: Existing provenance/metric/scope extension, not a new defect claim or roadmap.

Publication transformation: Actual report, page, model and source identities and redundant routing/date text omitted.

## TR-L0619 Thermal boundary inputs and fitted histories are not held-out outputs

Source lines 619–627; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 20.

A measured boundary input remains distinct from an evaluated interior output. A fitted event history is not a held-out forecast. Synthetic checks must flag a statistic exceeding one of two claimed thresholds, retain null table cells, and attach units/denominators plus run/channel identity to every comparison. Agreement at selected sensors must coexist with retained failures.

Acceptance checks

- Boundary-input and interior-output roles are distinct.
- Fitted history is not classified as holdout forecast.
- Exceeding either claimed threshold is flagged.
- Null cells, units, denominators and run/channel identity are retained.
- Successful sensors do not erase failed comparisons.

Qualification: Deduplicated workflow requirement, not a newly verified product bug.

Publication transformation: Actual thermal data and source identifiers plus redundant routing/date text omitted.

## TR-L0628 Shared reporting and rounded displays do not establish native runs

Source lines 628–636; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 22.

An earlier fuller source may contain two explicitly labeled test tables while a later paper cross-references only one. Identical printed values establish shared reporting, not identical native runs. A graph can show a positive property where a coarse table rounds to zero. Preserve source/version/channel joins, distinguish rounded display from executable input, and allow clarifying counterevidence to narrow critique without erasing earlier uncertainty.

Acceptance checks

- Shared printed values do not imply identical executed native runs.
- Source/version/channel joins remain explicit across editions.
- Positive graph versus rounded-zero table is not automatically an executed zero property.
- Counterevidence narrows current critique while historical uncertainty remains preserved.

Qualification: Lineage/precision extension, not a new product-defect or verified delivery claim.

Publication transformation: Actual paper/source identities, values and redundant routing/date statements omitted.

## TR-L0637 Property-specific validity domains survive similar tabulations

Source lines 637–646; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 20.

A source may print a property table beyond the range it explicitly calls valid while a downstream table repeats its shape at another precision. Preserve property-specific validity domains, measurement-versus-calculation roles, formulation identity and native-input status. A resolved rounding question is distinct from unresolved domain or assignment questions. Similar values neither erase qualifications nor automatically establish an executed model defect.

Acceptance checks

- Validity domain, derivation role, formulation identity and native-input status are explicit per property.
- Resolved rounding does not close unresolved domain/assignment concerns.
- Similar values cannot remove qualifications or establish an executed defect without an execution link.

Qualification: Generic SFB-004/SFB-005 extension; no inspected software defect or verified fix is claimed.

Publication transformation: Actual materials, values, sources and redundant routing/date text omitted.

## TR-L0647 Material identity, shared validity limits and older validation datasets

Source lines 647–659; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 20, 22.

Synthetic case: a method cites a source with a validity limit covering several materials, publishes differing material curves and an alternative heat-storage representation, but states earlier validation runs used an older dataset. Do not import one material's values into another, drop a shared qualification merely because the label differs, or infer the active solver property from a plotted curve. Preserve validation-run/property versions and explicit older-data chronology. Require an execution link before transferring validation or assigning a downstream error.

Acceptance checks

- Material identities prevent cross-material numeric substitution.
- Shared validity qualifications remain attached despite differing labels.
- Plots alone do not identify active solver property settings.
- Validation-run and property-data versions preserve older-data chronology.
- Validation transfer or downstream-error assignment requires execution linkage.

Qualification: Reproducible evidence-modeling requirement, not a source-inspected Sherlock defect.

Publication transformation: Actual material values, sources, attachments and redundant routing/date text omitted.

## TR-L0660 Replacement material role differs from intact-material law

Source lines 660–668; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 06, 19.

A deliberately low-capacity replacement can represent selected damaged regions, while an inventory records material-command names without their arguments. Preserve intended region/role, actual assignment, active formulation and execution as distinct joins. Neither extreme replacement property nor command count establishes an erroneous intact-material law.

Acceptance checks

- Replacement role, assigned region, active formulation and execution are independently represented.
- Command names/counts without arguments do not establish actual property assignment.
- Weak replacement material does not by itself show a wrong intact-material law.

Qualification: Extension of existing material/version fixture, not a new product-defect claim.

Publication transformation: Actual material-command and source identities and redundant routing/date text omitted.

## TR-L0669 Quoted-field parsing and private-sentinel error-path tests

Source lines 669–679; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 04, 05.

A synthetic quoted field containing a comma must not shift subsequent numeric roles even if the whole row is unresolved. Preserve quoted and doubled-quote boundaries, blank-versus-zero distinctions and unresolved status. Invalid CLI arguments must not echo a private sentinel through default error handling. Exercise both successful and failing output paths for sentinel leakage before source execution.

Acceptance checks

- Quoted commas and doubled quotes preserve field boundaries and subsequent numeric roles.
- Blank, zero and unresolved values remain distinct.
- Success and invalid-argument error output never disclose the dummy private sentinel.
- Leakage fixtures run before native source reading.

Qualification: Source reports both local research-parser defects caught before native reading, not demonstrated Sherlock defects or fixes.

Publication transformation: Actual sentinels and source values are not included; redundant routing/date text omitted.

## TR-L0680 Metadata-specific allowances must not relax native-source caps

Source lines 680–686; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 05, 07, 09.

A legitimate inventory may exceed the intentionally smaller per-source byte limit. Retain failed receipts, provide pinned metadata its own exact-size/hash allowance, and prove the native-source cap unchanged. Do not classify the local guard mistake as a bad source or weaken all limits to make verification pass.

Acceptance checks

- Oversized metadata retains the failed receipt and receives only an exact pinned allowance.
- Native-source cap is unchanged and still rejects over-limit source input.
- Local guard configuration failure is not reported as source corruption.

Qualification: Local workflow requirement, not an inspected Sherlock defect or delivery claim.

Publication transformation: Actual inventory sizes and identities plus redundant routing/date text omitted.

## TR-L0687 Whole-file integrity scope differs from selected-field interpretation

Source lines 687–696; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 02, 05.

A reader can correctly restrict decoded fields but accidentally restrict a promised whole-file guard to selected lines. Synthetic overlong unselected-line fixtures must catch this mismatch before native reading. Distinguish integrity coverage from interpretation coverage, enforce every declared cap at its declared scope, and preserve the failed check plus adjacent-boundary repair tests.

Acceptance checks

- An overlong unselected line fails a declared whole-file guard.
- Selected interpretation does not shrink whole-input integrity coverage.
- Each cap has explicit scope and adjacent-boundary tests.
- Failed check remains preserved after repair.

Qualification: Deduplicated local workflow lesson, not a demonstrated Sherlock defect.

Publication transformation: Actual source contents, identifiers, results and paths are not included; redundant routing/date text omitted.

## TR-L0697 Requested object, durable reviewer decisions and provider-context disclosure

Source lines 697–713; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 04, 10, 21, 24, 26.

Synthetic case: a user asks to organize existing work, an assistant substitutes future feature stages, a disposable index contains unique reviewer decisions, and a handoff forbids uploads but requires private source context. Preserve the requested object and report undelivered work separately from valid transmission gates. Reconstruct decisions from a durable versioned source, not new inference. Distinguish application network behavior from agent-provider context disclosure and require an approved context packet. Record per-turn authorship/effort and inspected coverage rather than attributing an entire project from one model label.

Acceptance checks

- Future roadmap is not accepted as delivery of requested organization of existing work.
- Transmission gates do not conceal undelivered local work.
- Unique reviewer decisions have a durable versioned source independent of disposable indexes.
- Provider-context disclosure is separately reviewed and approved.
- Authorship/effort and inspected coverage are recorded per turn rather than inferred for a whole project.

Qualification: Source describes observed workflow needs/design gaps, not demonstrated Sherlock defects, data loss or disclosure.

Publication transformation: Private source context, actual messages, paths and identities plus redundant routing/date text omitted.

## TR-L0714 Documentation, installed version and scientific-readiness states

Source lines 714–724; requirement. SFB mapping: SFB-005. Earlier digest topics: 07, 24, 26.

Synthetic case: a README names an older release than the lock and installed byte inventory, while an investigation contains setup questions but no admitted evidence. Report these states separately, date old security receipts, and distinguish fresh raw-file counts from engine replay and scientific acceptance. Stale documentation alone establishes neither engine defect nor adapter failure.

Acceptance checks

- README version, lock version and installed-byte version remain separately reported.
- Setup-only state is not admitted evidence or completed replay.
- Old security receipts retain their dates.
- Raw-file counts do not establish engine replay or scientific acceptance.
- Documentation mismatch alone cannot classify an engine/adapter defect.

Qualification: Motivated by an observed documentation/runtime mismatch; generic fixture, not an established engine defect.

Publication transformation: Actual release numbers, case identifiers, paths and redundant routing/date text omitted.

## TR-L0725 Read-only scientific projections coexist with export writes

Source lines 725–734; requirement. SFB mapping: SFB-005. Earlier digest topics: 04, 25.

Distinguish an export's read-only scientific projection from newly created output files and expected audit-log append. Test these categories separately with synthetic records: a false authority-merger flag does not prove no state changed. Destination IDs and well-formed hashes require actual endpoint/byte verification before being called resolved. Test whole-object metadata minimization before selecting any real payload.

Acceptance checks

- Scientific nonmutation, output creation and expected audit append are checked separately.
- No authority merge is not reported as no mutation.
- Destination resolution includes endpoint and byte-digest verification rather than syntax alone.
- Whole-object metadata minimization is tested before real-data selection.

Qualification: This source entry was source-inspected but not run-verified at its historical point; later executed follow-up appears in distinct records. No scientific validation or product defect is established here.

Publication transformation: Actual engine/repository identifiers, paths and redundant routing/date text omitted.

## TR-L0735 Export harness failure is not target execution or a zero-test pass

Source lines 735–750; requirement. SFB mapping: SFB-005. Earlier digest topics: 08, 23, 25, 26.

A bounded pilot can fail before export because its harness lacks a test-runner stream interface and supplies an unsupported evidence-direction literal. Distinguish launch/configuration failure, fixture-setup refusal, executed target case and verified result. Zero collected tests with zero reported failures is not a pass; missing post-run inventory is not an empty successful inventory. Before target execution, verify the actual CLI enum and stream contract; preserve every attempt and explicit synthetic/pending/non-scientific fields. Do not relabel an unexecuted export as product failure or passing capability. Exhaustion of a single repair allowance ends automatic correction; new attempts require separate authorization.

Acceptance checks

- Actual CLI enum and stream contract are checked before export cases run.
- Zero collected tests cannot yield a passing result.
- Absent inventory remains absent, not empty-success.
- All attempts retain launch/setup/execution/verification stage and synthetic/pending/non-scientific flags.
- Unexecuted target cases remain unexecuted.
- After the declared one-repair budget is exhausted, no automatic corrective loop starts.

Qualification: Source describes harness defects and review misses, not Sherlock defects or bridge-result findings. At this point export requirements remained source-inspected, not runtime-verified; later separately authorized execution is retained separately.

Publication transformation: Actual harness paths, source material and redundant routing/date text omitted.

## TR-L0751 Attributed synthetic execution findings and enforcement limits

Source lines 751–760; context. SFB mapping: SFB-005. Earlier digest topics: 25, 26.

The source reports two separately authorized synthetic retries reaching export, retaining synthetic/pending/non-scientific flags and matching declared semantic results. They accepted a nonexistent destination with a syntactically valid digest, allowed exploratory evidence export after its raw file changed or disappeared, and retained local artifact locators in output metadata. These are observed enforcement-scope limits, not proof that a declared exporter contract was violated, a destination admission succeeded, or scientific evidence became valid. Earlier unexecuted states remain preserved as history.

Qualification: Historical local synthetic results attributed to this source, not rerun or independently authenticated by this transcription. Product contract compliance, destination admission and scientific validity are not established.

Publication transformation: Exact dates, local engine identifiers, artifact paths and run receipts omitted; synthetic observed behaviors and result scope retained.

## TR-L0761 Export reliance requires resolution, current-byte checks and exact metadata review

Source lines 761–773; requirement. SFB mapping: SFB-005. Earlier digest topics: 04, 07, 25.

Explicitly distinguish serialized, destination-resolved, current-source-verified, admitted and human-accepted states. Before relying on a real export, independently resolve destination and digest, recheck selected source bytes, review exact metadata payload for disclosure, and retain unresolved states rather than silently upgrading them. Synthetic tests must cover valid/missing destinations, matching/mismatched digests, changed/missing source bytes and locator disclosure. Test the declared enforcement layer without retroactively changing exporter requirements. Neither automatic product patch nor real-case transfer follows from these requirements.

Acceptance checks

- Serialization does not imply resolution, source verification, admission or human acceptance.
- Real export reliance requires independent endpoint/digest resolution, current selected-byte checks and exact metadata review.
- Synthetic matrix includes valid/missing destination, digest match/mismatch, changed/missing source and locator disclosure.
- Unresolved states remain unresolved.
- Evaluation honors the previously declared enforcement layer rather than inventing retroactive requirements.

Qualification: Desired integration behavior accompanying locally observed synthetic exporter limits; not a product fix, admission or real-data authorization.

Publication transformation: Local control-result locator and redundant dated routing statements omitted.

## TR-L0774 Quantifiers, review roles and force-bound meanings

Source lines 774–792; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 10, 18, 20, 21, 24.

Synthetic case: a question asks whether motion was mostly vertical; a subtest finds one fragment outside an outline; self-review is followed by a separately authored later review. Preserve the question-to-tested-proposition mapping. Failure of universal containment is not a mass-fraction, motion-phase or mechanism finding. Store reviewer identity/role, source coverage, prior exposure and actual freeze/receipt times; a later summary cannot become an original-time freeze. Test logical compatibility before calling differently qualified assertions contradictory, such as upper/lower bounds sharing an endpoint. For derived force bounds retain weighted versus instantaneous force, point versus center of mass, assigned versus calibrated units and lower-bound versus equality meanings. Exact independent arithmetic is not historical validation.

Acceptance checks

- One outside fragment does not answer a mostly-vertical or mass-fraction proposition.
- Review identity, role, coverage, exposure and actual times remain attributable.
- Late summary cannot backdate an original freeze.
- Qualified bounds are checked for logical compatibility before contradiction labels.
- Weighted/instantaneous, point/COM, assigned/calibrated and bound/equality distinctions survive calculation and reporting.
- Independent exact arithmetic does not imply historical validity.

Qualification: Observed local reasoning/workflow failures or needs, not inspected Sherlock defects or verified fixes.

Publication transformation: Actual case observations, values, reviewer identities and paths plus redundant routing/date text omitted; explicitly synthetic case retained.

## TR-L0793 Physical constraints differ from optional measurement routes

Source lines 793–804; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 20, 24.

Distinguish a required physical constraint from an optional route to establish it. A normalized force ratio need not require absolute mass if pose/center-of-mass geometry is independently bounded. An attached material subset is not an invalid body merely because it remains attached. Preserve body membership and external-force boundary; compare a necessary lower threshold with an independently justified upper bound; reject cross-camera transfer without material/time/geometry joins. Point-only observation-equivalent examples are not full-image or structurally feasible reconstructions.

Acceptance checks

- An independently justified alternative measurement route is not rejected for lacking one optional method.
- Normalized force-ratio inference distinguishes needed geometry from unnecessary absolute-mass gating.
- Attached body subset retains fixed membership and explicit external-force boundary.
- Lower threshold is compared only with independently justified upper bound.
- Cross-camera transfer requires material, time and geometry joins.
- Point-only equivalence is not labeled full-image or structural feasibility.

Qualification: Additional observed local reasoning-workflow needs, not demonstrated Sherlock defects.

Publication transformation: Actual case geometry, source identities and redundant date/routing text omitted.

## TR-L0805 Catalog scope, effective archive format and safe header previews

Source lines 805–821; requirement. SFB mapping: SFB-005. Earlier digest topics: 02, 04, 05, 07.

A generic catalog may advertise a large collection while a tool returns only a partial item list; source identifiers may contain none of the initial semantic filename terms. Preserve catalog assertion versus inspected coverage, permit an explicitly versioned identifier query, and never turn a name nonmatch into content absence. An archive guard must follow the effective format header interpreted by its actual library, not a different header it trusted independently. Preserve failed-version source/results, replay boundary controls and distinguish finite-input verification from general hostile-input certification. Byte hashing, payload decoding and interpretation are different operations. Header-only previews must not print a first data row; test allowlisted output with a deliberately sensitive dummy field.

Acceptance checks

- Catalog asserted scope and actual partial inspected list remain distinct.
- Versioned identifier search does not rewrite original semantic-query coverage.
- Filename nonmatch is not content absence.
- Archive guard evaluates the format effective for the actual parser.
- Failed version/results and boundary controls remain preserved.
- Finite-input success cannot be claimed as general hostile-input certification.
- Hashing, decoding and interpretation have distinct operation status.
- A dummy sensitive first data row never leaks through header-only output.

Qualification: Source reports local workflow/tool defects and needs, not inspected Sherlock defects, fixes or scientific findings.

Publication transformation: Actual catalog, archive, source identities, counts, paths and redundant routing/date text omitted.

## TR-L0822 Literal search restrictions and malformed-attempt accounting

Source lines 822–834; requirement. SFB mapping: SFB-005. Earlier digest topics: 02, 08.

A locator using site.example.org instead of the intended site:example.org must not later be described as a domain-restricted search. Preserve the literal query and explicit domain fields; validate recognized operator syntax; distinguish requested restrictions from observed result coverage; retain truncated displays and count malformed or failed attempts against declared search limits. Existing failure-capture fixtures also cover setup failure before receipt initialization and logger-versus-direct-stderr gaps. These extend existing fixtures rather than opening duplicate issues.

Acceptance checks

- Use generic domains and dummy identifiers to exercise malformed and valid operators, preserving both literal requests and result coverage.
- Count malformed attempts against the declared search budget and retain setup/logger failure evidence.

Qualification: The source reports an analyst-workflow error and improvement request, not a source-inspected Sherlock defect or verified product fix. Tests described here remain proposed unless explicitly reported otherwise.

Publication transformation: Historical local-queue and destination-routing status is omitted; no technical condition is omitted. Generic operator examples are retained.

## TR-L0835 Batched search attribution without invented query-result joins

Source lines 835–846; requirement. SFB mapping: SFB-005. Earlier digest topics: 02.

When a two-query request returns a single combined result list without per-result query membership, preserve both queries and their combined returned set. Do not invent per-query hit counts, rankings or zero-hit claims. Explicit query-result joins must be retained or marked unknown; both queries consume the declared budget. Separate calls can preserve attribution prospectively, but a missing join does not authorize an additional historical search after the budget has been used.

Acceptance checks

- A mock two-query union containing one shared result retains explicit membership or records it as unknown.
- Verify that both queries count toward budget and that missing joins do not trigger unauthorized extra searches.

Qualification: The source describes an observed tool/workflow limitation, not an inspected Sherlock defect or verified fix.

Publication transformation: Historical routing, delivery status and recurrence date are omitted. No real queries, identifiers or returned personal information are included.

## TR-L0847 Delayed search population and explicit zero states

Source lines 847–859; requirement. SFB mapping: SFB-005. Earlier digest topics: 02.

A submitted search can expose a heading without entries or an explicit zero-result state, then populate on a later same-page observation. Distinguish typed, submitted, pending/unknown, populated and explicit-zero states. Record the selected category as well as the query. Permit a declared bounded readiness observation without a second submission. An empty temporary container is not a negative source finding. Preserve both observed states and label delay as inferred when no loading marker was observed.

Acceptance checks

- A generic delayed-result UI transitions from a heading-only state to populated results without being labeled zero-result or resubmitted.
- Retain query category, observation sequence and whether a loading marker actually appeared.

Qualification: An extension of existing search-coverage/loading-state fixtures; no Sherlock defect or verified fix is demonstrated.

Publication transformation: Historical routing and local-queue status are omitted; generic UI states preserve the technical substance.

## TR-L0860 Scope enforcement before OCR extraction

Source lines 860–872; requirement. SFB mapping: SFB-005. Earlier digest topics: 02.

A coordinate-filtered header/footer locator may admit an entire scanned-page OCR object, exposing content outside the declared reading scope. Restrict pages before parsing content; fail closed when the intended region cannot be reliably isolated. A page's first or last text line is not necessarily its header or footer. Preserve the failed attempt and actual exposed scope instead of calling the attempt compliant. The source reports that the over-scope attempt was stopped and a known-page allowlist used for subsequent decisive review; this does not establish a generally fixed extractor.

Acceptance checks

- Test giant single text objects, transformed or misleading coordinates, and image-only pages.
- Check that unisolatable regions fail closed and that exposed scope remains recorded even after a later compliant review.

Qualification: Reported analyst-tool boundary failure, not an inspected Sherlock defect; the subsequent local mitigation is not a product fix.

Publication transformation: Exposed text, case identity, private locations and historical delivery/routing state are not included.

## TR-L0873 HTML heading-boundary extraction

Source lines 873–878; requirement. SFB mapping: SFB-005. Earlier digest topics: 02.

A line-oriented search can return an entire single-line HTML body, while a fixed-character preview can spill into the next section. Require checked heading boundaries and bounded visible-text output. Preserve truncation and spill as incomplete or over-scope reading, not successful isolation.

Acceptance checks

- Use a single-line HTML body and neighboring sections to ensure line and character caps cannot substitute for checked section boundaries.

Qualification: Recurrence extending an analyst-tool fixture; not a new Sherlock defect claim.

Publication transformation: No substantive technical content omitted.

## TR-L0879 Extraction purpose boundaries across split volumes

Source lines 879–890; requirement. SFB mapping: SFB-005. Earlier digest topics: 02.

A declared initial-page range intended for front matter may encounter substantive chapters immediately after a cover in a second volume. A numeric page allowlist alone does not satisfy a purpose restriction. Identify volume/edition and section boundaries before batch text extraction; use a paired volume's contents and page labels when appropriate. Record unexpectedly exposed pages without silently widening the review or using those pages as evidence.

Acceptance checks

- Test a generic split report whose second volume begins with body text after its cover.
- Verify that purpose boundaries are checked in addition to numeric page limits and that accidental exposure is retained.

Qualification: Reported analyst-workflow failure, not an inspected Sherlock defect or verified fix.

Publication transformation: Actual source names, text, values, private paths and historical routing state are omitted.

## TR-L0891 Layer thickness is not spatial nonuniformity

Source lines 891–898; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19.

Distinguish thickness, covered area, spatial pattern and complete absence. A thinner continuous-layer comparison must not become a spatial-nonuniformity claim, and a sweep over one property must not be described as a tested sweep over the others.

Acceptance checks

- A synthetic continuous-layer thickness sweep remains explicitly a thickness sweep, without claims about spatial pattern, covered area or absence.

Qualification: The source reports an analyst-inference error caught in independent review and locally corrected wording; this is not a demonstrated engine defect or a historical result.

Publication transformation: Historical date and queue/routing metadata are omitted.

## TR-L0899 Response-metric transfer and source-family counting

Source lines 899–912; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 20, 21.

A summary may cite a numerical study for system insensitivity while the detailed study reports local hotspots and a separate integrated-deformation equivalence. Bind any equivalence to its actual geometry, loading, metric and profile set. Do not promote a local or integrated metric to connection or system failure without justified transfer. Two reports summarizing one calculation remain one evidence family. Preserve conflicting distribution labels as source assertions pending input verification, not automatic execution-error or intent findings.

Acceptance checks

- Include a harmless summary typo and metric-dependent equivalence as required countercases.
- Check that local hotspots, integrated equivalence, applicable profiles and evidence-family identity all survive summarization.

Qualification: Reported analyst-workflow need, not an inspected Sherlock defect or verified product fix.

Publication transformation: Source material, identities, actual values, private paths and historical routing are omitted.

## TR-L0913 Intended stochastic distribution versus realized finite profile

Source lines 913–923; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 20.

For a stochastic model that declares a mean/distribution and maps draws onto a finite discretized layer using surrogate material cells, retain the intended law, tail handling, seed, spatial profile, realized moments, mesh and cell-property mapping as distinct fields. Do not infer a truncation rule, deleted element, calibrated ensemble or executed run from prose. Preserve a harmless label typo as a countercase to automatic attribution of model error.

Acceptance checks

- Use a synthetic stochastic finite-layer fixture to check every distinct field and retain unknown execution/truncation/deletion states.

Qualification: Reported research-workflow need, not an inspected Sherlock defect or verified fix.

Publication transformation: Actual case values, source text, private paths and historical queue/routing details are omitted.

## TR-L0924 Increment reference and sufficiency antecedents

Source lines 924–936; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 20.

An increment may subtract a probe's own baseline or a common preloaded baseline. Store initial state, controlled load/displacement, sign, normalization and increment reference separately; reject comparisons across them when unlabeled. Retain every antecedent of a sufficiency statement: equal compliance alone does not imply equal thermal response, and an accompanying one-load match must not disappear from a compressed table. Preserve pre-execution clarification and distinguish program self-consistency, independent arithmetic and physical validation.

Acceptance checks

- Synthetic baselines make own-probe and common-preload increments differ and require an explicit comparison reference.
- Compression retains the one-load match alongside equal compliance and does not promote arithmetic agreement to physical validation.

Qualification: Reported analyst-workflow need discovered in independent review, not an inspected Sherlock defect or verified fix.

Publication transformation: Actual values, source text, case data, private locations and historical routing are omitted.

## TR-L0937 Follow-through reconciliation without erasing history

Source lines 937–954; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 24.

Completed subtests can leave old next-action paragraphs looking actionable, while source/version checks accumulate without changing the central inference. Preserve the original summary and show the current claim disposition and actual verification ceiling. Suppress completed next actions without erasing history. Each remaining action must identify prerequisites and its expected discriminating result. Neither report count, a later publication date nor paired readers of one source establishes scientific completion or independent evidence. Distinguish completed access checking from an unmet content comparison; retain uninspected alternatives.

Acceptance checks

- Use one original summary, three completed follow-ups, one unresolved calibration gate and one catalog-only version lead.
- Verify current dispositions, completed-action suppression, retained history, remaining prerequisites and expected discriminators.

Qualification: Reported workflow need extending provenance/state fixtures, not an inspected product defect or verified fix.

Publication transformation: Investigation identity, actual findings/paths and historical delivery/routing metadata are omitted. Synthetic fixture counts are retained.

## TR-L0955 Quantity definitions, depth comparisons and computed controls

Source lines 955–972; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 20, 18.

For a synthetic report plotting penetration depth and comparing mesh spacing with a differently normalized depth without a stated threshold or boundary condition, bind each number to its quantity definition, equation or missing-equation status, units, geometry and time origin. Preserve a monotonic-ordering conflict without silently choosing a correction. Post-hoc algebraic reconciliations are hypotheses, not recovered author methods. Approximate wording is not an error bar. A single depth/spacing crossing is neither convergence evidence nor a universal temperature-error sign. Independent readers must freeze definitions before comparison; rounded versus unrounded input choices remain explicit. Test controls must actually compute expected conclusions with positive and negative cases, not merely check stored constants.

Acceptance checks

- A synthetic differently normalized depth comparison preserves missing definitions and an ordering conflict.
- Positive and negative controls compute their conclusions rather than assert a pre-stored answer.

Qualification: The source reports the stored-constant test weakness was caught and corrected in local investigation code; no Sherlock defect or product fix was inspected or demonstrated.

Publication transformation: Actual source/result/identity/private metadata and historical routing are omitted.

## TR-L0973 Validation must precede equality-colliding cache lookup

Source lines 973–984; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 18.

Numeric type validation inside a memoized function can be bypassed after valid integer tuples populate the cache: numerically equal boolean or floating-point tuples may hit the cached result without validation. Validate the contract outside the cache or otherwise ensure cached and uncached paths enforce the same contract. Warm the cache with valid data before testing invalid but equality-colliding inputs.

Acceptance checks

- Populate the cache with valid integer inputs, then require rejection of equal-valued boolean and floating-point tuples.
- Compare cached and uncached validation behavior.

Qualification: The source reports both invalid acceptances were reproduced locally, then rejection was rechecked after moving validation outside the cache. This is a local checker correction before fixture outcomes, not an inspected Sherlock defect, historical-data error or product-wide fix.

Publication transformation: Private paths, case payload and historical routing metadata are omitted.

## TR-L0985 Parent/exhibit dates and grouped documentary notation

Source lines 985–994; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 22, 21.

A synthetic adjudication describes an undated equipment invoice and a separately dated service invoice. Keep parent-page and exhibit-page namespaces, document versus transaction dates, adjudicated descriptions versus inspected originals, and group-level payment notation versus individual-check observations separate. Do not transfer a neighboring date or general notation onto an uninspected record. Preserve qualifiers on the source's explanatory inference. Multiple readers of one decision are not additional historical source paths.

Acceptance checks

- A synthetic neighboring-invoice fixture preserves unknown dates and uninspected-original status while retaining the adjudication's attributed statements.
- Group notation remains distinct from an observed individual payment and repeated readers do not increase source-family counts.

Qualification: Extension to existing source-chain fixtures; an analyst-workflow requirement, not proof of an engine defect.

Publication transformation: Date heading and local routing context are omitted; no actual records or names are included.

## TR-L0995 Allowlisted transfer diagnostics and warning origin

Source lines 995–1005; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 04, 08.

A transfer command's comprehensive JSON summary can emit network/certificate metadata despite a successful file transfer. Before displaying results, allowlist status, declared source, type, size and integrity fields. Preserve detailed local records without copying them into reports or feedback. Record warning origin separately by operation: reproducible pixels and clean extraction must not erase a render-stage warning.

Acceptance checks

- Synthetic transfer summaries contain protected diagnostic fields that remain excluded from displayed output.
- A render warning remains recorded even when subsequent extraction is clean and pixels reproduce.

Qualification: Reported investigation-workflow needs, not demonstrated Sherlock defects or fixes.

Publication transformation: Actual names, case facts, paths, headers, network metadata and historical routing are omitted.

## TR-L1006 Bound diagnostic display before emission

Source lines 1006–1014; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 08.

Retain complete local render logs, but display only bounded warning classes, counts, byte size and an integrity pointer. Cap output before emitting it. A console view truncated by a tool's display limit must not be described as complete log review or a clean run.

Acceptance checks

- An oversized synthetic render log remains intact locally while its emitted summary stays within an explicit cap and reports review incompleteness accurately.

Qualification: The source reports an intact log was printed wholesale and exceeded the display limit. This is a local workflow recurrence, not an inspected Sherlock defect or verified fix.

Publication transformation: Source/case payload and historical routing/status details are omitted.

## TR-L1015 Scenario labels do not establish model configuration

Source lines 1015–1030; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 22.

A synthetic report may describe a general nonlinear capability, exclude an effect in a named result family and later show a scenario with the same label in a different file. Preserve the exclusion's stated scope. Do not infer identical configurations from shared scenario names, software capability or nearby prose. Distinguish prescribed initial failures, computed responses, inferred subsequent failures and observed historical events. A result-view screenshot is not a settings dialog. Different hidden configurations can produce the same chosen observable without uniquely identifying history. A prior reviewer's verification question must not be rewritten as that reviewer's factual claim.

Acceptance checks

- Use identical scenario labels with different hidden configurations and a capability description that does not establish actual settings.
- Retain the distinction between a review question and an affirmative factual assertion.

Qualification: Reported local review attribution/configuration traps; no Sherlock defect or fix was tested.

Publication transformation: Actual titles, facts, people, private paths, raw metadata and historical routing state are omitted.

## TR-L1031 Project announcements do not complete each component activity

Source lines 1031–1043; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 22.

A synthetic announcement can describe a completed sale, ongoing general work and a future structural alteration affecting different objects. A later project-completion notice must not automatically complete each earlier activity; a sale must not become measured mass removal; general structural wording must retain unknown member/object assignment. Preserve assertion date, described phase, object, evidence type and unresolved joins, including both material and harmless alternatives.

Acceptance checks

- A synthetic multi-phase announcement and later completion notice retain per-object status and unresolved joins rather than globally completing every activity.

Qualification: The source reports this need was exposed by two readers of one source. It is not a tested Sherlock defect or fix, nor additional historical source independence.

Publication transformation: Actual source/person/location/case information, response metadata and historical routing are omitted.

## TR-L1044 Model-grid ambiguity and coordinate-covariant certificates

Source lines 1044–1061; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 18, 20.

An off-grid generated step can fit a sampled ramp family better than the grid's step family. Lowest residual must not become a physical mechanism or duration label. Preserve grid definitions, all candidates, ground truth and model-discrepancy versus measurement-error status. In constrained optimization, a change of time units requires consistent scaling of primal parameters and active-bound dual multipliers, not only rescaling plotted time. Include interior and active-bound optima. Exact primal feasibility and a matching dual lower bound must survive the coordinate change.

Acceptance checks

- An off-grid synthetic step exposes model-family misclassification by lowest residual while preserving ground truth and all candidates.
- Interior and active-bound optimization controls retain primal feasibility and a matching dual lower bound after time-unit conversion.

Qualification: The source reports an initial local implementation failed the boundary control and passed after a preserved correction. This is an investigation-tool finding and proposed generic fixture, not an inspected Sherlock defect or verified product fix.

Publication transformation: Case coordinates, identities, sources, private paths and historical delivery/routing state are omitted.

## TR-L1062 Shared calibration, local errors and full-support bounds

Source lines 1062–1075; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 13, 20.

A truly shared ordinate offset cancels from paired-curve differences, while separate local errors do not; common horizontal error need not cancel when slopes differ. Preserve named shared calibration, local-error sets, exact versus uncertain knot status and the full demanded support. Retain an interior extremum missed by endpoint-only evaluation. Return unresolved if any admitted location reaches a gap. Distinguish a conservative marginal enclosure from an exact shared-parameter bound, and a uniform-query hull from a joint distribution or integral-error result.

Acceptance checks

- Synthetic paired curves exercise shared vertical offset cancellation, uncancelled local errors and horizontal effects with different slopes.
- Tests include an interior extremum and a support gap, and label the resulting enclosure type correctly.

Qualification: Extension to measurement/covariance requirements, not a newly inspected Sherlock defect, product fix or accepted-engine update.

Publication transformation: Actual sources, case payload and historical queue/routing status are omitted.

## TR-L1076 Preservation acquisition defaults and actual runtime identity

Source lines 1076–1095; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 07, 08.

A launcher hash alone omits the interpreter/package actually used. Default container fixups can change downloaded bytes, and unavailable fragments can be skipped. Pin launcher plus actual runtime/package while distinguishing this from full dependency attestation. Disable automatic repair; refuse missing fragments while retaining partials and diagnostics; exclude inherited proxy/import configuration. Inspect environment key names without disclosing values, separating runtime-added platform keys from inherited user overrides. A stale-client retrieval error remains a failed attempt, not source absence or authentication denial. Preserve it before any separately scoped maintenance test; do not silently broaden a historical-source search. Independent code and receipt checks do not mean child-process/filter controls were independently rerun.

Acceptance checks

- Synthetic defaults tests check repair-disabled behavior, missing-fragment refusal with retained partials and actual runtime/package binding.
- Environment controls omit values, distinguish inherited overrides from runtime-added keys and retain stale-client failure history.

Qualification: The source reports local downloader source inspection and locally exercised child-process/filter controls. These are inspected local defaults and workflow requirements, not demonstrated Sherlock defects or verified fixes.

Publication transformation: Actual identifiers, URLs, case material, environment values, private paths and historical routing are omitted.

## TR-L1096 Decoded equality does not restore repaired container originality

Source lines 1096–1107; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 07, 27.

Raw-preservation acquisition must fail closed unless automatic repair is explicitly disabled in preflight before execution. A prose-only no-remux plan is insufficient. Preserve any changed copy separately from a repair-disabled acquisition. Even if native decoded audio compares equal under the tested decoder, matching decoded streams must not retroactively relabel changed container bytes as raw originals.

Acceptance checks

- A raw-preservation job with repair still enabled is rejected before acquisition.
- Separate repaired and repair-disabled synthetic containers may decode equally but retain distinct byte-layer identity and originality status.

Qualification: The source reports a local execution lapse against a known default, retention of the changed copy, a separate repair-disabled acquisition and equal decoded audio under the tested decoder. This is not a new historical-evidence claim or proven Sherlock defect.

Publication transformation: Actual media payloads, locations, source identifiers, recurrence date and historical routing are omitted.

## TR-L1108 Failure-path capture and render admission are separate checks

Source lines 1108–1125; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 08, 07, 27.

A subprocess timeout can raise before its wrapper preserves captured output; a warning-severity diagnostic need not contain the literal word warning. Preserve command, status and separate stdout/stderr on timeout and nonzero-exit paths. Classify every diagnostic category or reject unknowns. Compare code, dependency and runtime pins before and after execution. Exit success and complete decodable images can coexist with configuration/cache errors. Preserve diagnostics and distinguish byte integrity, visual usability, clean font configuration and numerical-figure fidelity; none automatically proves the others. Missing glyphs must fail visual admission even if PNG decoding succeeds. A warned but apparently complete page needs a documented bounded admission decision, not automatic promotion to a clean render.

Acceptance checks

- Short-timeout and nonzero-exit synthetic children emit known separate stdout/stderr that survive failure capture.
- Unknown warning categories are rejected, and missing-glyph images fail visual admission despite decodable PNG output.
- Warned-but-apparently-complete pages retain a bounded admission decision and diagnostic origin.

Qualification: The source reports failure-path controls exercised in a local research driver, not Sherlock, and says its then-current completed runs did not time out. A separate local document follow-up returned exit success with configuration/cache errors; no engine defect or fix is established.

Publication transformation: Private build paths, raw diagnostic payloads and source identity are omitted; historical claims remain explicitly attributed.

## TR-L1126 Actual visual coverage and saved quantitative baselines

Source lines 1126–1137; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 10, 14, 24.

Distinguish attempted, reliably returned, actually reviewed, repeated and recovered images. A truncated batch is not complete review; permit only logged recovery within frozen coverage. Save quantitative baseline/reference envelopes before long sequential review or context changes. Approximate feature locators cannot later substitute for measurements. A reader lacking those records must report an annotation shortfall rather than invent an onset or blame absent source evidence.

Acceptance checks

- A truncated synthetic review batch retains separate attempted/returned/reviewed/repeated/recovered sets and allows recovery only inside the frozen scope.
- A missing saved baseline produces an annotation-shortfall state, not a fabricated measurement or missing-source claim.

Qualification: Reported local workflow needs, not inspected Sherlock defects or verified engine fixes.

Publication transformation: Case values, source names, images, private paths, diagnostic metadata and historical queue/routing status are omitted.

## TR-L1138 Denied prerequisites must launch zero dependent children

Source lines 1138–1151; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 08, 09.

An explicitly denied output-directory setup must launch zero dependent render jobs, and its failure result must be preserved. Recovery must first confirm earlier children are terminal, create only an authorized scoped destination and pass one bounded preflight before fan-out. Preserve original failure receipts separately from successful recovery. Distinguish truncated projections from complete stdout/stderr. The priority is avoiding repeated preventable failures and false processing claims.

Acceptance checks

- A denied output-directory prerequisite starts zero dependent children.
- A recovery test verifies terminal prior children, authorized scoped destination and one passing bounded preflight before fan-out.

Qualification: The source reports a local orchestration defect where jobs ran after failed setup. The acceptance test is proposed, not implemented or engine-verified, and no Sherlock defect was inspected.

Publication transformation: Case source, private destination path, raw diagnostics and historical routing are omitted.

## TR-L1152 Image loader and forwarding requests require separate provenance

Source lines 1152–1168; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 27, 10.

An original-detail request to an image loader can be lost when a caller forwards the image through a helper without preserving that argument. Retain loader request, forwarding request, saved geometry and actual returned geometry separately. Equal source hashes do not make two reviews matched-resolution. Preserve frozen readings and disagreements; do not assume effects are confined to known disputed glyphs or silently rerun a failed representation contract. A difference in invocation does not by itself prove the sole cause of resizing or a product defect.

Acceptance checks

- A synthetic fine-text page follows both detail-preserving and detail-omitting forwarding paths.
- Include a larger saved raster that may still be displayed smaller and retain requested versus actual geometry at both stages.

Qualification: The source reports different recorded displays and differing forwarding invocations in local review. This is an evidence-integrity workflow note, not an established causal A/B test or verified Sherlock fix.

Publication transformation: Actual images, measurements, names, identifiers, private paths and historical routing/status details are omitted.

## TR-L1169 No resize notice verifies only the recorded invocation change

Source lines 1169–1174; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 27.

Carrying an original-detail request through both loader and forwarding helper, with no explicit resize notice returned, verifies the recorded invocation change only. It does not prove matched displayed geometry, an A/B causal result, calibrated fine-text accuracy or a product fix.

Acceptance checks

- A review receipt with preserved detail flags and no resize notice keeps actual geometry and fine-text accuracy unverified unless separately measured.

Qualification: The source reports both readers used the preserved flags on the next fixed page set. This local follow-through is not independently rerun by this transcription and does not establish a Sherlock fix.

Publication transformation: Actual page-set identity and chronology details are omitted.

## TR-L1175 Preserved detail flags can coexist with display resizing

Source lines 1175–1183; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 27.

If a larger representation reports resizing despite detail flags preserved at both stages, record a display limitation. Do not label this a failed source hash or proof that the invocation repair had no effect. A larger delivered image that still fails to resolve selected fine detail must retain the unresolved relationship.

Acceptance checks

- A synthetic larger representation with explicit resizing preserves source-byte integrity and unresolved fine detail without a causal overclaim.

Qualification: The source reports this local follow-through for both readers; it updates a workflow observation, not a new product issue or verified Sherlock fix.

Publication transformation: Actual images, dimensions, identifiers, case findings, date and routing metadata are omitted.

## TR-L1184 Pin source-specific stored geometry before protocol freeze

Source lines 1184–1197; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 27, 23.

Copying a neighboring raster's width into a new protocol may pass synthetic display checks while actual-source preflight correctly rejects it. Obtain geometry from each pinned source before freezing its protocol. Test wrong-width rejection, preserve failed configurations and record a prospective amendment rather than quietly revising source metadata. Keep orientation-display size separate from stored-pixel size.

Acceptance checks

- Two synthetic image families share height and color mode but have different stored widths.
- A protocol using the neighboring family's width fails before output or annotation, and its failed configuration is preserved.

Qualification: The source reports a local setup error correctly stopped by a guard before output/annotation, not an inspected Sherlock defect or verified engine change.

Publication transformation: Actual images/dimensions/source identifiers/paths/results and historical routing are omitted.

## TR-L1198 Observation chronology, note order and delayed saving

Source lines 1198–1216; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 10.

An ambiguous repeated patch anchor may put a final observation section ahead of intermediate sections even when view/save operations followed the declared sequence. Preserve the frozen artifact and disclose its layout error; heading order is not independent evidence of acquisition or observation chronology. Reject ambiguous insertion anchors and verify section membership/order before freezing. Keep an append-only operation sequence separate from editable presentation. If a source view is followed by an unrelated request and context handoff, retain view/save sequence and delayed-note attribution; prevent an automatic immediate-recording compliance claim and require preservation before the next source view. Independent agreement can support content but cannot retroactively cure the timing deviation.

Acceptance checks

- A repeated-anchor fixture rejects ambiguous insertion and independently records actual operations.
- An interrupted observer saves a delayed note with correct attribution before any further source view, without claiming immediate-recording compliance.

Qualification: Reported local authoring and workflow errors, not inspected Sherlock defects or verified fixes.

Publication transformation: Real source identities, case values, personal fields, private locations, images and historical routing are omitted.

## TR-L1217 Version-bound transcription and post-exchange correction

Source lines 1217–1230; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 10, 22.

A later schedule can contain a value where an earlier schedule is blank, and a reader can accidentally carry the value backward; a miscopied numeral can create an apparent subtotal discrepancy. Bind each transcription to exact source version, page, row and field. Preserve blank, zero and unknown separately. Require a source check before calling an arithmetic mismatch a source anomaly. Keep frozen readings, initial failed arithmetic and a prospectively declared post-exchange correction distinct. Arithmetic agreement alone must neither select the preferred numeral nor retroactively manufacture independent agreement.

Acceptance checks

- Synthetic schedules with later-only values and a miscopied numeral preserve exact source-version binding and blank/zero/unknown states.
- Corrections retain frozen readings, initial arithmetic failure and post-exchange status.

Qualification: Reported evidence-integrity workflow failure, not a demonstrated Sherlock defect or verified fix.

Publication transformation: Actual sources, values, identities, private paths and historical routing are omitted.

## TR-L1231 Capture status and partial-output integrity before content rejection

Source lines 1231–1243; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 08, 07.

Capture basic subprocess status and partial-output diagnostics, including byte count/hash, before shape/content validation rejects short output; include timeout paths. Test the full publication/failure path rather than only helpers. Interpreter selection belongs to the existing runtime-identity requirement, not a duplicate issue.

Acceptance checks

- Run synthetic success, short/nonzero, timeout, changed-input and anchor-mismatch controls through the complete publication/failure path.
- Every content rejection retains available return status and partial-output count/hash first.

Qualification: The source reports separate method/source reviews found the ordering error and a repaired local adapter passed the listed synthetic controls. This is not a Sherlock defect or verified engine fix.

Publication transformation: Case data, source names, private paths, raw diagnostics and historical routing/delivery details are omitted.

## TR-L1244 Warning category counts are not aggregate counts

Source lines 1244–1251; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 08.

One warning category's count must not be reported as the count of all warnings. Retain each category and severity and report the aggregate separately. Preserve a checker's failed assertion when an overlooked category is discovered. Qualify an ambiguous frozen producer label rather than rewriting the result to hide it.

Acceptance checks

- A synthetic mixed diagnostic log retains per-category and per-severity counts plus a separate total, exposing an omitted category without erasing the failed assertion.

Qualification: The source reports a local frozen result was qualified rather than rewritten; no new Sherlock test or fix was claimed.

Publication transformation: Source identifiers, raw diagnostic payloads and historical queue metadata are omitted.

## TR-L1252 Deterministic visual corruption is separate from decode repeatability

Source lines 1252–1264; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 27, 08.

A received video frame can contain severe banding despite no decoder warnings and identical repeated extraction. Byte/decoder repeatability must coexist with a separate visual-quality flag and unobservable-region mask. A passing technical receipt must not clear historical-authenticity or physical-measurement gates.

Acceptance checks

- A synthetic clip intentionally containing stripes and an opaque banner passes byte/decoder repeatability but retains visual-quality defects and a masked unobservable region.

Qualification: Research-workflow lesson extending integrity-versus-usability fixtures, not an inspected Sherlock defect or claimed fix.

Publication transformation: Actual image, source identifier, private path, case details and historical routing are omitted.

## TR-L1265 Native-coordinate human review and local-only review surfaces

Source lines 1265–1282; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 11.

A required human spot-check cannot be fulfilled by a viewer lacking reliable native-pixel coordinates. A reported limitation is neither reviewer approval nor a negative scientific finding. A review surface must remain separate from immutable annotations and actual human acceptance. Report native rather than CSS coordinates; preserve pixel-center/boundary convention; clear stale selections on image/load failure; distinguish hover and locked points. Never turn an automated UI test or generic permission into human acceptance. Serve only allowlisted local assets, with no writes, uploads, analytics or automatic disclosure. Actual application tests and human observations remain separate.

Acceptance checks

- Display a known-size synthetic image at Fit, native and doubled scale with scrolling; select a known pixel and move it using arrow keys.
- Test native-coordinate reporting, selection clearing, hover/lock state and local allowlisting without upload/write/analytics behavior.

Qualification: The source reports a user-observed viewer limitation and a separately implemented/tested bounded local review surface; human review was still pending in that historical note. This is not a demonstrated Sherlock implementation defect or a current human-review status determination.

Publication transformation: Actual case assets, annotations, user data, private paths, date and routing metadata are omitted.

## TR-L1283 Reduced-scale selection limits and failed action preservation

Source lines 1283–1289; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 11.

Reduced-scale mouse pointing can skip native pixels. Disclose that limitation and provide native/doubled scale or single-pixel keyboard adjustment. Preserve loading states and stale-geometry/tool-action failures rather than labeling them successful selections.

Acceptance checks

- Synthetic browser zoom/scroll/keyboard tests distinguish successful native selection from loading or stale-geometry action failures.
- Provide a fine-view or keyboard route for native cells skipped at reduced scale.

Qualification: The source reports local coordinate unit tests, allowlist-server tests and synthetic browser checks passed. These are not Sherlock implementation or verified Sherlock-fix claims, and are not independently rerun by this transcription.

Publication transformation: No substantive requirement omitted; local test assertions remain attributed.

## TR-L1290 Intended versus delivered pointer coordinates

Source lines 1290–1303; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 11.

An automated synthetic center click in a reduced view can reach an adjacent native row. Without delivered event coordinates, neither diagnose input quantization nor exonerate mapping from marker alignment alone. Retain intended and reported cells separately. Require fine-view/keyboard checking and explicit abstention if precise selection remains unreliable; do not infer a universal one-pixel bound. Preserve source size, displayed rectangle, device-pixel ratio, intended input, delivered event coordinates, reported cell and marker location through zoom, scroll and resize. Automated practice remains separate from actual human review.

Acceptance checks

- A diagnostic fixture logs intended and delivered coordinates, event-time geometry, reported cell and marker through zoom/scroll/resize.
- Unreliable precise selection triggers fine-view/keyboard verification or explicit abstention, not a universal one-pixel claim.

Qualification: The source reports an unlogged local synthetic miss; the added diagnostic fixture is a proposed extension, not a demonstrated engine defect.

Publication transformation: Case examples, private paths, date and historical routing are omitted.

## TR-L1304 Bounded pointer diagnostic results do not establish universal accuracy

Source lines 1304–1321; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 11, 09, 10.

A synthetic-only logger preserved requested versus delivered pointer coordinates and event-time geometry across twelve fixed Fit/native/doubled targets. One reduced-view intended miss recurred when adjacent intended rows received the same delivered position. An independently authored cell-boundary oracle agreed with all twelve selected cells and recorded geometry was stable. This supports delivery change as the explanation for that new miss, not the earlier unlogged event, any particular stack layer or a universal rounding rule. No production mapping repair is indicated by this sample. Six fine-view hits do not establish general accuracy; retain fine-view/keyboard checking and abstention. Preserve preparation failures, a source-pin race and replacement packets rather than silently replacing failed cases.

Acceptance checks

- Compare logged delivered positions against an independent cell-boundary oracle, separately from intended targets.
- Retain bounded sample size, unlogged earlier-event uncertainty, preparation failures and replacement-packet history.
- Do not generate historical annotations or human acceptance from diagnostic results.

Qualification: This is the source's attributed synthetic diagnostic/computational-review result, not an independently rerun result here or a verified Sherlock implementation/fix. All retained numeric counts concern synthetic targets.

Publication transformation: Case examples, private paths, recurrence dates and historical delivery/routing state are omitted.

## TR-L1322 Render-affecting metadata and preserved input contracts

Source lines 1322–1343; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 27, 14.

Identical first-frame luminance bytes can coexist with animation or rendering metadata that changes the displayed image. Validate frame count and render-affecting metadata as well as pixels; hash and parse/decode the same captured byte buffer. Independently check each crop/enlargement pixel without calling the producer transform and freeze the display transform before viewing. Distinguish producer-owned normalized-output contracts from preserved input metadata: unchanged older RGB inputs may carry different aspect, gamma or chromaticity properties. Record actual properties and restrict unsupported photometric/metric comparisons; do not silently strip source metadata or claim display equivalence. Keep larger-display visibility separate from physical-component identity, local crossing separate from final disappearance, and an endpoint unresolved after a declared hard stop.

Acceptance checks

- Synthetic animated/transparency and altered-pixel controls check metadata-sensitive display behavior and independent transformed-pixel verification.
- A preserved-input fixture has source-specific aspect/gamma/chromaticity properties different from normalized output and is not silently rewritten.

Qualification: The source reports an observed local-check scope error and locally exercised animation/transparency/altered-pixel controls. No Sherlock engine fix was inspected or verified.

Publication transformation: Actual case media, identities, measurements, private paths and historical routing are omitted.

## TR-L1344 Document-render omissions and transfer-before-admission gating

Source lines 1344–1358; requirement. SFB mapping: SFB-002, SFB-004, SFB-005. Earlier digest topics: 27, 07, 08.

A completed document renderer may omit a language's text because a CMap/font dependency is missing while another installed renderer displays it with original bytes unchanged. Preserve diagnostics and both derivatives. Reject the incomplete render as full-page inspection, and record renderer/runtime plus actual page review rather than only exit status or legible text extraction. Require terminal successful transfer and complete size/hash/type checks before parsing or admission. An in-flight parse failure must not be classified as source corruption.

Acceptance checks

- A generic document with a missing CMap/font dependency preserves incomplete and complete derivatives and denies full-page-inspection status to the incomplete render.
- A generic live transfer cannot reach parser/admission work until terminal success and complete integrity/type checks.

Qualification: The source reports separate local render-dependency and premature-download-read errors. These are local workflow needs, not inspected Sherlock defects or verified engine fixes.

Publication transformation: Actual documents, source identities, personal paths, transport headers and historical routing state are omitted.

## TR-L1359 Live-transfer parse recurrence remains an acquisition-state failure

Source lines 1359–1364; requirement. SFB mapping: SFB-002, SFB-004, SFB-005. Earlier digest topics: 07, 08.

A caller must not parse a document while its transfer handle is still live. Wait for that same handle to complete and verify complete bytes before admission. A later successful parse does not erase the premature parse failure or make it source corruption. Deduplicate this recurrence under the existing terminal-transfer-before-admission requirement.

Acceptance checks

- A live-transfer fixture blocks parsing until the same handle completes and bytes pass checks, preserving the initial premature attempt.

Qualification: The source reports that waiting on the existing local transfer handle and checking complete bytes resolved a parse failure. No new product-defect or verified-fix claim is made.

Publication transformation: Recurrence date and administrative destination/delivery details are omitted.

## TR-L1365 Expected-hash transcription errors are distinct from source changes

Source lines 1365–1373; requirement. SFB mapping: SFB-002, SFB-004, SFB-005. Earlier digest topics: 05, 18.

Distinguish a changed source from an incorrectly transcribed expected hash. Preserve the first failed check. Before correcting a handwritten checker, verify a separate earlier frozen receipt; never silently rebaseline the source. Where possible, consume pinned manifest values instead of manually transcribing them.

Acceptance checks

- Separate fixtures alter source bytes versus mistype the expected hash and require different diagnoses.
- Checker correction requires an independent receipt and retains the initial failure.

Qualification: The source reports a mistyped checker expectation while captured bytes still matched an earlier receipt. This is a local workflow error, not a newly inspected engine defect or fix.

Publication transformation: Actual hash values, source identity and administrative delivery metadata are omitted.

## TR-L1374 Independent freeze, actual view sets and censored event bounds

Source lines 1374–1390; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 10, 14, 21.

Require both annotation records and their hashes before exchanging candidate findings; procedural status may be exchanged without observations. Preserve actual viewed-index sets separately from extracted sets, with overlap/union counts and repeat displays. For two observers sharing a last-visible object but reporting different nested onset brackets and unable to trace the final crossing through an occluder, report separate one-sided bounds and a conservative envelope. Persistent nondetection is not a positive post-event state; shared annotations are not independent sources; an extraction-window endpoint is not an upper bound. Agreement does not authenticate component identity. A later lossless enlargement is a disclosed sensitivity pass, not new resolution or a blind replication.

Acceptance checks

- A synthetic paired-observer censored-event fixture requires both frozen records before findings exchange and retains distinct one-sided bounds.
- The report separates extracted/viewed/repeated sets and excludes unsupported upper bounds, component identity and independence claims.

Qualification: Reported workflow requirements, not inspected Sherlock defects or verified fixes.

Publication transformation: Actual event values, source identities, media, private paths and historical routing are omitted.

## TR-L1391 Moving occlusion thresholds and deferred access states

Source lines 1391–1404; requirement. SFB mapping: SFB-002, SFB-004, SFB-005. Earlier digest topics: 14, 01, 02.

Two cameras' different occlusion edges can make the same object disappear at different times while the reference edge itself moves. Retain viewpoint, threshold and moving-reference identity. Distinguish last visible, bracketed disappearance and physical failure; keep opaque intervening frames censored. A nearby figure's timestamp or uncertainty must not silently become the prose claim's timestamp or uncertainty. Separately, a rate-limited availability query remains a deferred access attempt, not an empty catalog or missing source. Stop that route without blocking unrelated local evidence work.

Acceptance checks

- Synthetic camera geometry includes different moving occlusion edges and preserves event censoring and distinct timestamp attribution.
- A rate-limited query records deferral, respects a route stop and permits unrelated authorized local work.

Qualification: Reported workflow needs, not verified Sherlock defects or fixes.

Publication transformation: Actual values, media, source identifiers, private paths and historical routing state are omitted.

## TR-L1405 Composite-image admissibility and recursive dependency closure

Source lines 1405–1429; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 27, 06.

For a synthetic document figure split across image strips whose page-space joins align but whose final strip has a different pixel scale, distinguish one figure from component objects. Freeze allowed transform/tolerance before observation. Reject proposed lossless common-grid assembly when the criterion fails; retain the unscored figure in coverage rather than dropping it or calling it nondetection. Page-layout context rendering must not silently replace a native-image contract. Pin imported dependencies as well as the producer. A later independent calculation may corroborate a result without repairing its original missing dependency closure. Traverse declared dependency maps with explicit relative-path bases: A pins B and B pins C. Reject conflicting pins and missing descendants. Separate required execution inputs from separately pinned narrative/navigation context. Preserve the incomplete first run. A versioned before/after repair must retain identical substantive output or explicitly explain differences. Keep ciphertext, decrypted encoded-image bytes and rendered pixels distinct.

Acceptance checks

- An incompatible-scale strip figure is retained as unscored rather than assembled contrary to its frozen contract.
- A-to-B-to-C dependency fixtures exercise recursive traversal, relative bases, conflicting pins and missing descendants.
- A repaired version is compared with the preserved incomplete first run, with substantive output equality or explained differences.

Qualification: The source reports local recurrence and local repair/testing, not verified Sherlock behavior or an engine fix.

Publication transformation: Actual image, measurement, source identity, private paths, case material and historical routing/delivery state are omitted.

## TR-L1430 Process success, HTTP denial and cross-client retry history

Source lines 1430–1441; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 01, 07, 04.

Process exit success with HTTP403 and HTML must never admit the response as a PDF; DNS failure is a distinct transport state. Preserve exact-target attempt history across clients instead of treating each client as a first attempt. A stop rule must explicitly say whether cross-client retries are permitted. Raw response headers may contain server cookies and must not be copied into feedback payloads.

Acceptance checks

- Synthetic exit-success/HTTP403/HTML and DNS-failure controls produce distinct states and neither admits a PDF.
- Cross-client attempts share exact-target history and obey an explicit retry rule; cookie-bearing headers remain outside feedback.

Qualification: The source reports these states exercised in a local source check, not a Sherlock engine test; no verified product defect or fix is claimed.

Publication transformation: Actual URLs, headers, identities, case contents and historical routing are omitted. HTTP status and generic media types are retained.

## TR-L1442 Raw response headers require a staging boundary

Source lines 1442–1448; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 04.

Use allowlisted header/transport fields for diagnostics. Preserve raw response headers only as local preservation material behind an explicit staging guard. Logs and proposed feedback must omit cookie values. Successful byte preservation is not disclosure clearance.

Acceptance checks

- A synthetic raw-header fixture contains dummy cookies that remain preserved locally but never enter displayed logs or proposed feedback.

Qualification: The source reports a local checker unnecessarily printed complete raw headers; this is a workflow error and mitigation, not a demonstrated Sherlock implementation bug.

Publication transformation: Actual headers and recurrence date are omitted.

## TR-L1449 Artifact references do not establish transferred bytes

Source lines 1449–1463; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 01, 03, 04.

A provider may successfully return remote artifact references while local byte transfers receive HTTP403 and produce no file. Preserve listed, referenced, transferred and media-verified states separately. Requested fields omitted by normalized metadata must not be attributed to provider absence. Redact signed transport links before diagnostic display: later saved-response redaction does not erase earlier output. Preserve stable safe IDs, stop on denial and avoid treating a benign public query parameter as a secret.

Acceptance checks

- Dummy temporary URLs and synthetic responses test reference-only success, denied byte transfer and omitted normalized fields.
- Redaction happens before output, stable IDs survive, denied routes stop and a public-query-parameter control is not misclassified.

Qualification: Reported local workflow failures/needs, not inspected Sherlock defects or verified product fixes.

Publication transformation: Actual URLs, identifiers, metadata, case contents, private paths and historical routing are omitted.

## TR-L1464 Archived-link target identity and composite names

Source lines 1464–1475; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 06, 01.

An anchor's displayed URL may differ from its actual archived href, parent links can change capture context, and partial identifiers may repeat across distinct full folder labels. Retain exact observed links and composite names. A restored index is not independent corroboration; an archived filename is not acquired bytes; a declared processed upload is not a continuous source. A failed metadata route does not establish absent media.

Acceptance checks

- Generic archived anchors test displayed-target mismatch, changing parent capture context and repeated partial identifiers in different full names.
- Index restoration, filename discovery, processed upload and actual byte acquisition retain distinct evidentiary status.

Qualification: Reported workflow requirements, not inspected Sherlock defects or verified fixes.

Publication transformation: Actual links, source identifiers, case payload and historical routing are omitted.

## TR-L1476 Narrow warning exceptions and explicit prerequisites

Source lines 1476–1491; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 08, 04, 06.

A known software color-conversion fallback may warn while native-format decoding is clean; an unrelated corrupt-frame message must still reject. Retain warned originals and pin the narrow version/source assessment. Distinguish conversion uncertainty from corrupt input. Link prior controls, native checks and reference-inventory identity as explicit prerequisites: a derivative-only receipt does not establish all prerequisites or human review. Redact signed retrieval references before display; subsequent saved-file redaction cannot erase prior tool output.

Acceptance checks

- A synthetic mixed known-plus-unknown log admits only the specifically reviewed exception and rejects the unrelated corrupt-frame message.
- Derivative-only receipts retain unmet prerequisite/human-review status, and dummy expiring references are redacted before output.

Qualification: Reported local workflow needs, not inspected Sherlock defects or verified engine fixes.

Publication transformation: Actual sources, credentials, measurements, private paths, case payload and historical routing are omitted.

## TR-L1492 Catalog field meaning, populated rows and exhaustiveness

Source lines 1492–1506; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 02, 01.

A dated schema may define an everyday-sounding tag narrowly while later public folder listings return filenames without those historical attributes. Retain field meaning, edition and actual populated-row status. A schema or screenshot is not an inventory export, and a no-hit tag/name search is not a negative source-content search. A normalized listing below its cap but lacking pagination metadata is not proven exhaustive. Keep partial-word OCR, missing image-table text and full-page visual reading distinct. Successful bounded raw retrieval after a browser size failure closes only that access gap, not historical authenticity.

Acceptance checks

- Synthetic catalogs distinguish schema definitions from populated rows and retain unknown pagination/exhaustiveness.
- Search and reading receipts distinguish tag/name, partial OCR, missing image-table text and full-page visual scope.

Qualification: Workflow requirements extending source/representation fixtures, not inspected Sherlock defects or verified engine fixes.

Publication transformation: Actual sources, values, identifiers, names, paths and historical routing are omitted.

## TR-L1507 Actual response collections and retrospective coverage claims

Source lines 1507–1518; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 02, 10.

A folder-search response may place entries under results while a child listing uses files. A failed selector is a parser/schema error, not zero results. Preserve a populated example of each response shape and reject an unknown or missing collection field. Keep an earlier explicit parent link, a later null parent field and the exact scoped listing request separate. A newly enumerated candidate set does not retroactively turn a prior unrelated scene-screen into review of those candidates' content.

Acceptance checks

- Synthetic populated results and files shapes parse correctly; unknown/missing collection fields reject without claiming source absence.
- New enumeration retains actual historical review coverage instead of retroactively relabeling an unrelated screen.

Qualification: Reported workflow recurrence, not an inspected Sherlock defect or implemented fix.

Publication transformation: Actual source names, identifiers, payloads, private paths and historical routing state are omitted.

## TR-L1519 Separate catalog snapshots, hashes and counts

Source lines 1519–1530; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 02.

A folder index and adjacent summary can point to different dated snapshots with different upstream hashes and totals. Pin each retrieved artifact and declared upstream version separately. Do not pool counts, silently repair disagreements or infer removals from a mismatch. Keep a zero-hit folder-label search separate from an unperformed document-body search.

Acceptance checks

- A synthetic two-snapshot catalog preserves distinct upstream versions, hashes and totals without automatic removal inference or count pooling.
- Metadata-label zero hits do not claim document-body coverage.

Qualification: Reported workflow need, not a source-inspected Sherlock defect or implemented fix.

Publication transformation: Actual case names, counts, URLs, locations, payloads and historical routing status are omitted. The number of synthetic snapshots is retained.

## TR-L1531 Transfer-decoded text search and explicit excluded content

Source lines 1531–1543; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 02, 04.

Searching stored email bytes before MIME transfer decoding leaves a blind spot requiring a separately scoped decoded-inline-text pass. Preserve raw versus decoded scope, encoding/error counts and attachment exclusions. Find permitted inline markers without printing private bodies or claiming attachment coverage. Archive-name search and document text-layer search similarly require explicit unsearched-content and sparse-page limits.

Acceptance checks

- Synthetic plain, base64 and quoted-printable inline parts contain the same marker; a deliberately excluded attachment contains a different marker.
- Find all permitted inline markers while retaining decoding/error counts, attachment exclusions and non-disclosure of bodies.

Qualification: The source reports a local-method gap and correction, not an inspected Sherlock defect or verified engine fix.

Publication transformation: Actual messages, names, dates, identifiers, paths, source text and historical routing are omitted.

## TR-L1544 Excerpt boundaries and asynchronous observation exchange

Source lines 1544–1559; requirement. SFB mapping: SFB-002, SFB-004, SFB-005. Earlier digest topics: 14, 15, 10, 08.

Adjacent-numbered excerpts can have different endpoint scenes, with the second excerpt beginning with the phenomenon already visible. Reject a seamless join without inventing elapsed time, onset, extinction or editing intent. Source naming and shared landmarks are not positive continuity. Preserve positive appearances separately from obscured samples. If an asynchronous observer summary arrives before a lead reviewer freezes, retain the observer's pre-exchange status but mark the lead's completed record post-exchange. A private earlier impression is not a saved independent record. Keep stage diagnostics/status separate from descriptive admission.

Acceptance checks

- Synthetic adjacent-numbered excerpts with differing endpoint scenes cannot acquire invented continuous timing or event boundaries.
- An observer's early message changes the lead record's independence status without retroactively changing the frozen observer record.

Qualification: The source reports a tested local helper revision separating stage diagnostics/status and descriptive admission; this does not establish a Sherlock engine fix.

Publication transformation: Actual source media, identifiers, results, private paths, case details and historical routing are omitted.

## TR-L1560 Connector omissions, retrospective receipts and stage-specific admission

Source lines 1560–1579; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 03, 08, 04, 01.

A source wrapper can link a catalog while a normalized response omits requested checksums or parents and request scope is reconstructed separately. Distinguish provider absence from connector omission; preserve request/response/version identity and retrospective-receipt status. Separate repository-original from camera-original. A text extractor's missing link or failed access route is not source absence. Matching pixels and correct timestamps can coexist with reproducible concealment errors: probe and decode diagnostics need independent status, not an automatic-pass label or decode-only warning list. An input option resolving an audio-metadata inference must not admit unrelated video errors. Retain complete logs and partial/refused outputs with independent stage-level admission. Redact transient retrieval credentials by construction instead of dumping raw connector responses.

Acceptance checks

- Synthetic normalization drops requested fields and the report attributes the omission correctly while retaining retrospective scope reconstruction.
- Media fixtures separate probe/decode warnings, preserve unrelated video errors after an audio-metadata adjustment and redact dummy transient credentials before logging.

Qualification: Reported workflow/local-helper needs, not newly source-inspected Sherlock defects or verified fixes.

Publication transformation: Actual case files, names, source identifiers, measurements, URLs, local paths, raw diagnostics and historical routing are omitted.

## TR-L1580 Narrow partial admission, inventory grain and candidate freezes

Source lines 1580–1597; requirement. SFB mapping: SFB-002, SFB-004, SFB-005. Earlier digest topics: 08, 10, 14, 21.

Diagnose a recognized terminal serialization token, audio-layout inference during video-only processing and unsupported coded-stream feature separately. Preserve failed attempts and partial output; require narrow revision controls before new admission. A harmless syntax repair must not whitelist unrelated warnings. Refusal does not prove corrupt pixels, while successful exit and generated files do not validate fidelity. Count complete decoded inventories, selected samples, overview derivatives and duplicated receipt references separately. Sparse sampling of an event shorter than the gaps is not an absence test. Freeze paired reviewers' candidate choices before exchange, retain different maybe thresholds even if final outcomes agree and mark later shared follow-ups post-exchange rather than independent first passes.

Acceptance checks

- Three synthetic diagnostic categories exercise independent admission decisions with retained failure/partial-output history.
- A short synthetic event between sparse samples prevents an absence claim.
- Paired candidate reviews preserve distinct maybe thresholds, pre-exchange freezes and post-exchange follow-up status.

Qualification: Reported workflow needs, not inspected Sherlock defects or verified fixes.

Publication transformation: Actual case names, images, source identifiers, private paths, diagnostics and historical routing state are omitted.

## TR-L1598 Annotation-coordinate namespaces and finite inventory conclusions

Source lines 1598–1613; requirement. SFB mapping: SFB-002, SFB-004, SFB-005. Earlier digest topics: 14, 21, 03, 24.

For an annotated application screenshot copied into two example folders, keep author labels, screenshot pixels, source graph coordinates and native-video queries distinct. Folder placement and duplicate bytes establish neither geometric mapping nor independent corroboration. Save descriptive observations before revealing newly acquired labels, while disclosing prior familiarity. Count typed motion histories separately from axes/tape utility objects. Differing counts exclude only complete saved-state substitution, not subset use or proof of deleted data. Retain unresolved transformations and dimensional source, report exactly what each independent review checked and close finite inventories without inventing a universal gate on fresh measurements.

Acceptance checks

- A synthetic duplicated annotated screenshot preserves coordinate namespaces and prior-label exposure without invented mapping or corroboration.
- Differing typed-object counts support only the bounded inventory conclusion and do not block otherwise authorized new measurements.

Qualification: Reported workflow needs, not inspected Sherlock defects or verified fixes.

Publication transformation: Actual case data, identities, files/images, private paths and historical routing are omitted.

## TR-L1614 Sampled-branch dependence and baseline-normalized saved rows

Source lines 1614–1634; requirement. SFB mapping: SFB-002, SFB-004, SFB-005. Earlier digest topics: 16, 15, 18, 06.

Two resize filters may differ on full images yet become identical on a fixed sampling grid, while another filter changes which neighboring frame wins. Retain full-versus-sampled identities, dependence and neighboring alternatives. Nominally separate branches are not independent checks, and score gaps are not exposure confidence. A saved position series may agree after first-shared-row subtraction while absolute positions and fine printed times disagree. Keep all pairings, original offsets, coarse-join and strict-time decisions, rounding bounds and missing states; a baseline zero is automatic. Preserve sparse numeric rows before the first surviving key without calling them independent manual marks or confirmed between-key interpolation. Positive membership outside a publication's time domain does not reverse a negative result restricted to actually joined rows. Use explicit zero-/one-based archive and XML namespaces and retain guard failures before corrected parsing.

Acceptance checks

- Synthetic resize branches exercise identical sampled outputs despite different full images and a changed adjacent-frame winner.
- Synthetic saved rows retain normalized agreement alongside absolute/time disagreement, sparse pre-key rows and domain-restricted membership conclusions.
- Namespace/index guards preserve initial failures and explicit corrected parsing.

Qualification: Reported local workflow requirements, not source-inspected Sherlock defects or verified product fixes.

Publication transformation: Actual values, sources, identities, images, private paths, research reports and historical routing/bridge status are omitted.

## TR-L1635 Prospective target exclusion through actual resampling kernels

Source lines 1635–1648; requirement. SFB mapping: SFB-002, SFB-004, SFB-005. Earlier digest topics: 16.

A similarity search must not use the transient it will later claim to corroborate as its matching target. Freeze a broad exclusion before scoring, check both target locations and test native-source perturbations through the actual resize kernel. Retain all cutoff ties and neighboring alternatives. Top-k is a review budget, not a calibrated confidence set. Static and changing regions can select different or repeated frames; neither result may be silently discarded.

Acceptance checks

- Synthetic controls include blended/duplicate frames and a tie spanning the rank cutoff.
- Masked changes leave scores invariant while unmasked changes affect them, tested through the actual resize kernel at both target locations.
- Retain differing/repeated static-versus-changing frame selections and all neighboring/cutoff alternatives.

Qualification: Extension to existing candidate/branch controls, not a new Sherlock bug or tested engine fix.

Publication transformation: Actual media, coordinates, identifiers, private paths, results and historical queue/routing state are omitted.

## TR-L1649 Parsed versus lexical metadata coverage

Source lines 1649–1664; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 05, 27.

A synthetic XML check reproduces a source-coverage trap: an ordinary element parser drops comments/processing instructions, and reading only node.text loses immediate text after child elements. A ten-character mixed description can therefore look five characters long. Acceptance: declare parsed-element versus lexical-token coverage; retain all immediate text segments, unknown attribute/tag identities and structured-string cases; preserve root versus track ownership, duplicates and missing/empty/whitespace/nonempty distinctions. Hash-only metadata inventory is not plaintext content review, and a display-visibility flag is not evidence of concealment. Test with generic dummy strings before real sources and do not emit arbitrary text in errors.

Acceptance checks

- A mixed-content XML fixture retains immediate text segments and ownership distinctions, declares comment/processing-instruction coverage, and emits no arbitrary metadata in errors.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1665 Joint hidden-precision feasibility

Source lines 1665–1678; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 18, 21.

The local workflow now tests one shared hidden-precision variable per sample, not separate values for each overlapping row. Extend the generic fixture with individually feasible differences that conflict when chained. Require a complete input-checked witness or a certificate made from valid inequalities summing to an impossibility; cross-check with a different exact implementation. Keep closed display bounds, strict interior existence and a selected witness touching a bound distinct. A computational witness is not a recovered historical observation.

Acceptance checks

- Overlapping-row constraints share variables and produce either a complete input-checked witness or a valid impossibility certificate verified by a different exact implementation.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. The historical note reports local synthetic controls and historical arithmetic exercising this requirement; it does not claim a product implementation or fix.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1679 Printed-grid clocks and derivative reconstruction

Source lines 1679–1692; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 14, 15, 18, 21.

The subsequent printed-table audit adds an acceptance case to the existing measurement/provenance fixture: a displayed time grid differs slightly from a nearby encoded rate, and derivative residuals exceed printing bounds under one clock assumption. Preserve the original failed test; declare source-motivated alternatives before testing; recompute bounds rather than widening them by hand; and distinguish individual-row compatibility from a jointly reconstructed hidden-precision dataset or identified historical settings. A graph's drawn fit line and an onset label must not become an undocumented fit mask. Two transcriptions and two arithmetic implementations share their source's errors; record the exact independence layer.

Acceptance checks

- Retain the failed clock test and test source-motivated alternatives under recomputed printing bounds without inventing fit masks or independent source evidence.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1693 Summary version, quantity and execution lineage

Source lines 1693–1705; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 21, 24.

A summarizer can accurately copy an obsolete output whose quantity semantics were corrected in another checkout. A report count can also silently exclude that checkout, and a planning note can label reported cases as completed tests. Synthetic acceptance: bind each summary claim to source version, quantity type, execution state and later correction; distinguish row counts from typed objects, attributed outcomes from independently run experiments, and subset inventories from the declared corpus. Preserve the original statement and authorship edit receipts without making model identity a truth criterion. A matching hash must not clear a false interpretation.

Acceptance checks

- Every summary joins the exact source version, quantity and execution state; subset counts and attributed tests cannot be upgraded by hash agreement.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1706 Shared dependencies across synthesis reports

Source lines 1706–1718; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 06, 19, 21, 24.

Several verified audits can depend on the same missing input or experimental family. Preserve a dependency identity across reports so repetition cannot multiply evidentiary weight. Distinguish a changed aggregate confidence statement from a new measurement, a falsified mechanism, a new ranking or equal odds. Synthetic acceptance: three reports share one unresolved source edge; one later report resolves only its byte-search scope. Show the updated edge once, retain positive and contrary evidence and the old dated assessment, and never promote conditional technical plausibility to comparative probability automatically.

Acceptance checks

- A shared unresolved edge counts once across three synthetic reports, and a later byte-search update changes only that edge while preserving contrary evidence.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1719 Typed reference closure and bounded negative coverage

Source lines 1719–1737; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 02, 05, 06.

All selected parent cards can be present while their referenced leaf tables remain absent from the checked files. Acceptance: preserve consumer/type/source/version edges, distinguish supplied fields from dependency closure, and state exact negative-search coverage rather than global absence. Same-number material and curve IDs are not substitutes. Blank/zero defaults belong to specific fields and consumers, not a global normalizer. Producer status labels and count-versus-list schema errors are harness failures, not mathematical disagreements; retain failed attempts and verify fixed replay inputs separately from output destinations. This extends the fixture to overlapping byte patterns: a match in two encoding alignments does not authenticate either encoding, and normalized zero-/one-based ordinals must retain both original aliases and source identity. Negative literal coverage must remain distinct from absent generated or externally supplied definitions.

Acceptance checks

- Parent-card completeness cannot clear missing leaves; namespace, defaults, encoding hypotheses, normalized ordinals, replay errors and generated-definition uncertainty remain explicit.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1738 Numerical value agreement versus decision agreement

Source lines 1738–1753; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 18.

Two independent numeric methods can agree within a value tolerance yet disagree on exact downstream classes or projection flags. An unresolved category may reflect arithmetic inversion rather than empirical uncertainty, and including it in a candidate union can change that union. Synthetic acceptance: preserve numeric values, decision predicates, failed exact comparisons and uncertainty origin separately; do not promote close numbers to reproduced decisions. Test a fixed-input rational/outward-interval reference without tuning physical parameters, preserving the failed floating runs and original boundary buffer. Unknown input stays distinct from an outside result. Completeness of a faster broad phase must be tested independently of agreement among its retained rows.

Acceptance checks

- Retain failed exact comparisons and original buffers; test rational or outward-interval references without physical tuning and independently test broad-phase completeness.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1754 Relation types, card order and bounded-parser failures

Source lines 1754–1773; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 05, 06, 08.

A finite-element-style synthetic graph can connect distinct node IDs through an interface definition. Preserve separate relation types: shared node, selected surface, candidate counterpart, initialized pair and surviving force path. Equal numeric IDs in node/element/part/set namespaces must not join without an explicit type. A zero direct-graph intersection cannot exclude indirect transfer; a positive selection cannot establish stiffness or historical activation. Acceptance fixture: one non-shared interface, one same-number/different-namespace decoy, one excluded candidate and one unresolved initialization state; reject promotions between those relation types and retain all explicit zeros. Keyword-option order and numeric-card order are separate contracts; reordered options must not discard a heading or shift blank cards. For large scans, preserve the original error's source/line and a partial receipt if a later memory-limit check also fails; do not mask the first failure or invent its missing measurements. Compare compact representations with synthetic ordered/repeated/null fixtures before using them after a resource failure.

Acceptance checks

- A typed-interface fixture rejects promotions between selection, initialization and surviving force paths; preserves explicit zeros, original parse failures and compact-representation controls.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1774 Paired events and measurement definitions

Source lines 1774–1792; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 19, 20, 22, 23.

A source reports initial failure, later failure, and a maximum-moment averaging window. A later comparison reports ultimate load and rotation at that load. Preserve the event/observable pair: selecting the larger load must carry its associated rotation, not an independently maximized value. An omitted plot is not automatic exclusion from a summary table; a defective channel is not automatically a defective whole specimen. Distinguish an explicit sensor sum/mean recipe from a numerical factor that happens to make results agree, and a printed-equation defect from proven execution of that defect. Publication date is not experiment date. Synthetic acceptance: retain null secondary stages, test membership and channel lineage; reject unsupported normalization, paired-event substitutions and date promotion; preserve exact definitions alongside any declared exploratory diagnostic. Also verify that a named control actually exercises the claimed production branch, rather than only a separate helper.

Acceptance checks

- Chosen load and rotation remain paired; stage/channel membership, sensor recipes, dates and actual production-branch coverage must survive the fixture.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1793 Quantity states and separate disclosure permissions

Source lines 1793–1794; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 04, 19, 22.

Deduplicate under SFB-004/SFB-005. Synthetic example: a source lists installed capacity, assumes initial contents, reports later recovery, and a downstream model treats an available quantity as an input; another edition retains removed equipment and changes a unit pair. Acceptance: preserve equipment/date/quantity-state/unit/source-family joins and flag unresolved differences, without converting availability into consumption or model input into independent validation. Separately, a publicly downloadable document can carry confidentiality markings: acquisition, inspection, summary, transfer and publication must have distinct permission states. Public HTTP success, a catalog access label or a hash must not clear sensitive contents or transport metadata automatically.

Acceptance checks

- Preserve equipment/date/state/unit/source joins; public availability, access labels and hashes cannot authorize later disclosure or convert availability into consumption.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1795 Revision roles, totals and unit conventions

Source lines 1795–1796; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 19, 22.

A PDF text extractor can flatten deleted and replacement values into the same sequence, losing which value supersedes which. A matching aggregate can also result from different component sets, and the same unit label can conceal different conversion conventions. Synthetic acceptance: retain source-rendered deletion/insertion roles and revision dates; require verified component membership before reconciling totals; preserve the original unit label and declare conversion basis without claiming which value a downstream model used. A source author's statement that a correction never affected calculations must remain an attributed claim until inputs/outputs are checked. Log rejected reviewer misreadings separately from source discrepancies.

Acceptance checks

- Retain deletion/insertion roles and dates, verify component membership and conversion basis, and keep an author's correction claim attributed until run inputs/outputs are checked.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1797 Wrapper assertions and embedded-source qualifiers

Source lines 1797–1798; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 21, 22.

Extend the existing source-scope acceptance fixture with a public wrapper whose prose generalizes beyond an attached source's sampling limit, and a footnote naming an interview without its date or transcript. Preserve wrapper and embedded-source page namespaces, the narrower underlying observation, and unresolved interview-identity joins. A shared wrapper or matching person's name must not become independent corroboration.

Acceptance checks

- Preserve the embedded sampling limit and unresolved interview identity; a shared wrapper or name cannot supply independent corroboration.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1799 Directed dataflow and lexical parser disagreement

Source lines 1799–1800; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 05, 06, 19.

A synthetic upstream field generator supplies two downstream solvers, while one solver separately supplies damage state to the other. Preserve quantity and direction for each edge; temporal interpolation is not spatial interpolation, and a matching destination input is not proof of its generating program. Add two parsers that hash the same argument with and without a delimiter, classify spaced assignments differently, and leave a shared first-line syntax unresolved. Acceptance: source-locator reconstruction may reconcile hash/count recipes without declaring complete semantic equivalence; retain a tested negative encoding hypothesis and candidate-name ambiguity. Literal-marker absence must not become absence of a generator or historical execution.

Acceptance checks

- Preserve quantity/direction and temporal/spatial interpolation distinctions; reconciled hash/count recipes cannot clear unresolved semantic or generator-execution questions.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1801 Matched quantities, holdout support and printed precision

Source lines 1801–1802; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 18, 19.

A synthetic model is fit to another model's accumulated work while their force histories differ; a later experimental comparison tunes an unloading choice, and the available experimental curve ends before the simulated failure tail. Acceptance: track the particular matched observable, fit/selection versus untouched evaluation, study date and measured support interval; do not turn one matched quantity or later evidence into general historical validation. A separate printed table has apparent division discrepancies that fit display-rounding intervals, while one formula retains a small precision mismatch. Preserve every row, actual displayed precision, the explicit rounding hypothesis and unresolved inputs; interval compatibility is neither authenticated hidden data nor evidence of fabrication.

Acceptance checks

- A fitted work quantity cannot validate a differing force history or unmeasured failure tail; retain all rounding intervals and unresolved formula inputs.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1803 Graph overlays and human mapping gate

Source lines 1803–1814; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 11, 19, 27.

Extend the existing calibration fixture with raster graph strips whose model labels are separate PDF text overlays. Bare image extraction must not become complete figure evidence; retain clipping versus unclipped placement and native-resolution uncertainty. Two same-unit outputs need verified quantity definitions before imposing a work/dissipation identity. Actual human mapping checks must precede consequential automated graph findings, not only later application to a real system. Synthetic arithmetic passes and AI agreement cannot satisfy that gate.

Acceptance checks

- Composite graph evidence retains text overlays, clipping and native uncertainty, and actual human mapping checks precede consequential automated graph findings.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1815 Partial object state and versioned context keys

Source lines 1815–1828; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 02, 10, 12, 22.

A generic source can call an aperture open while retaining some barrier material; a binary intact/removed schema would silently alter that observation. Preserve state definition, partial extent and unresolved classification separately from object identity. A locally held naming key discovered after annotation must be a versioned context extension, not an unavailable-record claim or a retroactive blind-reading assertion. Source-inferred order from a state change must not become independent clock corroboration of that change. For provenance checks, test filename-exclusion rules from both the target root and another working directory, asserting excluded path components rather than assuming a successful search applied them.

Acceptance checks

- Partial barrier state stays distinct from object identity; newly found naming context is versioned; exclusions are tested from multiple working directories by actual path components.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1829 Appearance agreement without material-state promotion

Source lines 1829–1842; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 11, 12.

Two readers can agree on visible irregular edges and unresolved material while using different descriptors such as opening-like versus dark framed pattern. Preserve the raw descriptors, mapping uncertainty, material uncertainty and display/occlusion limits separately; do not summarize agreement on unresolved state as agreement on absence. Human review should name the exact target, record what was actually checked, and leave unchecked targets unaccepted. Acceptance fixture: one locally surface-like patch in an otherwise obscured band cannot assign the whole band, and a clearer neighboring object's image cannot silently replace the declared target.

Acceptance checks

- Preserve raw descriptors, mapping/material uncertainty and occlusion; accept only checked targets and never substitute a clearer neighbor or a local patch for the full band.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1843 Panel codebooks, display priority and uncertain locators

Source lines 1843–1851; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 14, 27.

Same-day source-display extension: a combined map can prioritize one field over another, and the same color can encode different classes in adjacent representations. Synthetic acceptance: retain each panel's codebook and display-priority rule; do not reconstruct a masked field from the composite or count a smaller repeated exposure as a second observation. Record a partly legible embedded workbook title as a locator with explicit glyph uncertainty, not an acquired native file.

Acceptance checks

- A composite cannot reconstruct its masked layer or provide another observation; an uncertain embedded title remains a locator rather than an acquired workbook.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1852 Cumulative unions versus time-specific evidence

Source lines 1852–1860; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 12, 14.

A cumulative label meaning "A or B observed at any sampled time" cannot become "B observed at this time," and its complement cannot become a resolved negative of B. Synthetic acceptance: two different event histories yielding the same union display must retain their different time/phenomenon evidence; an unknown input must not turn into an intact or absent state. Preserve the separate underlying layers when available.

Acceptance checks

- Two histories with the same cumulative union preserve distinct time/phenomenon support; its complement cannot establish absence of one component.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1861 SFB-001 section heading

Source lines 1861–1862; context. SFB mapping: SFB-001. Earlier digest topics: 26.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: Section heading only; its substantive requirements and superseding adoption record are separately transcribed.

## TR-L1863 Historical charter issue priority and state

Source lines 1863–1864; context. SFB mapping: SFB-001. Earlier digest topics: 26.

Historical SFB-001 setup limitation was assigned priority P1 and acknowledged with no fix then reported. That historical state is superseded for local full-charter creation by the later adoption record; do not reopen it as a current defect.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: Date/routing metadata retained only as historical status; no requirement is omitted.

## TR-L1865 Original full-charter creation-path limitation

Source lines 1865–1866; requirement. SFB mapping: SFB-001. Earlier digest topics: 26.

The historical source inspection reported that the case-creation path accepted question, decision, owner, standard and change criterion but stored a generic scope, empty exclusions and empty legal/ethical/privacy/source-safety/retention constraints. The CLI did not expose a full-charter input although its schema already defined those fields. This was source inspection, not a runtime exploit or finding about evidence. The later local adoption record supersedes this no-fix state for full-charter creation.

Acceptance checks

- Retain the originally supplied scope, exclusions and all legal, ethical, privacy, source-safety and retention constraints through the supported creation path.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: Private implementation file paths and symbol locations replaced by component roles; all field requirements retained.

## TR-L1867 Preserve a governing charter without frozen-state edits

Source lines 1867–1868; requirement. SFB mapping: SFB-001. Earlier digest topics: 26.

Impact: A detailed investigation cannot enter the supported creation path with its actual scope and constraints intact. A separate governing charter must remain visible; do not hand-edit frozen case state to bypass the limitation.

Acceptance checks

- A governing charter remains visible and no unsupported frozen-state edit is used to bypass a creation limitation.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L1869 Full-charter input and append-only amendments

Source lines 1869–1870; requirement. SFB mapping: SFB-001. Earlier digest topics: 26.

Requested improvement: Schema-validated full-charter creation plus append-only charter amendments with visible version/reference history. Preserve backward compatibility without silently dropping explicitly supplied fields.

Acceptance checks

- Schema-valid full input and append-only amendments preserve earlier bytes, history and explicitly supplied fields without breaking backward compatibility.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L1871 Charter synthetic reproduction

Source lines 1871–1872; requirement. SFB mapping: SFB-001. Earlier digest topics: 26.

Synthetic reproduction: Create a generic document-comparison case whose intended scope excludes outreach and whose retention/privacy fields contain non-sensitive placeholders. Verify whether the supported creation path can preserve those fields. No real case examples required.

Acceptance checks

- A generic document-comparison charter preserves outreach exclusions and non-sensitive retention/privacy placeholders.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L1873 Charter round-trip and amendment acceptance

Source lines 1873–1874; requirement. SFB mapping: SFB-001. Earlier digest topics: 26.

Acceptance: Exact field round-trip; malformed/omitted required fields rejected; scope/constraints visible in auditable case state and relevant report views; amendments preserve earlier bytes and ledger history; tests show no silent defaults replacing supplied restrictions.

Acceptance checks

- Reject malformed or missing required fields; round-trip exact supplied fields into auditable state and relevant reports without silent restriction-replacing defaults.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L1875 SFB-002 section heading

Source lines 1875–1876; context. SFB mapping: SFB-002. Earlier digest topics: 26.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Section heading only; following units preserve requirements.

## TR-L1877 Punctuation-only ASR and runtime-capability checks

Source lines 1877–1888; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 07, 17, 23.

Preserve ellipsis-only segments and untranscribed intervals separately from silence or no-event findings, even when repeated machine outputs match exactly. Keep nearby self-corrections and alternative explanations with event-related speech. Synthetic acceptance: punctuation-only output cannot become a sound absence claim, and quotation extraction must not discard a following qualifying clause. Also name the verified interpreter: an ambient older Python passed validator-only tests but failed the shared hashing helper before inference. Preflight must exercise required runtime capabilities, not just imports or unrelated unit tests.

Acceptance checks

- Do not convert ellipsis-only or untranscribed intervals to silence; retain following qualifiers and preflight the exact runtime capabilities used by inference.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1889 Authorized local speech routes and neutral adapters

Source lines 1889–1904; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 01, 07, 17.

A conversational audio-input failure does not establish that an already cached local speech-recognition model is unavailable. Inventory authorized local routes separately from perceptual access. Existing project wrappers may add domain vocabulary prompts, read unrelated manifests/credentials, or rewrite transcripts; inspect those side effects before reuse. A neutral investigation adapter should expose model/source/runtime identities, exact preprocessing, prompt use, raw text/timing outputs and repeat disagreement, while preserving human observations as a separate layer. Synthetic acceptance: an adapter invocation omits an unrelated wrapper lexicon, leaves its project unchanged, records downmix/resampling, and never converts a spoken report about an event into detection of that event.

Acceptance checks

- Inspect wrapper side effects; a neutral adapter omits unrelated lexicons and records runtime, preprocessing, prompts, raw outputs and disagreement without treating ASR as human listening.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. ASR output does not supply human listening.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1905 Native metadata versus probe projection

Source lines 1905–1920; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 02, 03, 08, 15.

A generic probe/normalized catalogue can omit native source-name/timecode tags that a bounded container-header check recovers. Synthetic acceptance: preserve the returned projection separately from field absence; retain raw offsets, payloads, NUL-terminated text prefixes and uninterpreted binary tails; never promote editable metadata to an authenticated event clock. Repeated alternate fields in one file are not independent corroboration. A metadata-output command may internally decode while discovering stream information, so verify that behavior before promising zero decoding. Separate output type from execution scope. Preserve oversized/truncated captures and index-skip defects; cap displays without converting missing capture into a complete receipt.

Acceptance checks

- Preserve omitted native fields, raw offsets, NUL prefixes and binary tails; verify hidden decoding behavior and retain incomplete captures without false complete receipts.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1921 Alternate metadata lanes and conditional chronology

Source lines 1921–1932; requirement. SFB mapping: SFB-002. Earlier digest topics: 15, 19.

Original and alternate metadata lanes must remain independently comparable; disagreement should not suppress both usable values. Prefix equality must not be reported as complete-payload equality when binary tails differ. A source-order conflict can survive every within-clip frame choice while still depending on unverified camera-versus-edited-master semantics. Synthetic acceptance must preserve that conditional conflict, test both interpretations, retain mixed lossless byte encodings, and neither authenticate chronology nor erase the conflict merely because an edit is possible.

Acceptance checks

- Compare both metadata lanes, full binary payloads and both camera/edited-master interpretations without authenticating or erasing a conditional conflict.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1933 Invalid counters cannot become valid zero clocks

Source lines 1933–1944; requirement. SFB mapping: SFB-002. Earlier digest topics: 15.

A primary library's display helper maps invalid counter digits to zero. An investigation adapter must preserve invalid/unknown components and raw bytes instead of inheriting that convenient display fallback. Synthetic acceptance: malformed digits, omitted counter labels, changing counting modes, repeated/skipped values and day-wrap candidates stay explicit; an accidental one-step difference across a mode change is not continuous timing in one convention. Matching a stream counter to an editable file label supplies internal consistency, not two independent clocks.

Acceptance checks

- Malformed digits, omitted labels, mode changes, repeated/skipped values and wrap candidates remain explicit; matching editable labels are not independent clocks.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1945 Image-state-derived clocks and joint reconstruction

Source lines 1945–1958; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 14, 15, 21.

A source image can be dated using an observed object's state; an enlargement or derived map may inherit that time. Neither the extra representation nor its new label creates an independent clock or validation observation. Synthetic acceptance: retain the image-to-state-to-inferred-time dependency graph, shared offsets and unexplained travel/dwell assumptions; do not convert overlapping marginal ranges into an independent relative-time confidence interval. Permit explicit joint reconstruction but reject an independent-validation label when it reuses the state that supplied its clock. A primary workflow description is not proof of its application to a particular file.

Acceptance checks

- Retain image-to-state-to-time dependency, shared offsets and travel/dwell assumptions; reused state cannot be independent validation or create relative-time confidence from marginal overlap.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1959 Executable search patterns versus display syntax

Source lines 1959–1966; requirement. SFB mapping: SFB-002. Earlier digest topics: 02, 23.

A saved pattern map can contain extra escaping even when the recorded search results are correct. Preserve that original, publish the exact executable pattern/flag map separately, and reproduce every declared source/page count before calling the search reproducible. A display representation is not automatically executable syntax.

Acceptance checks

- Preserve the original pattern representation, supply an executable pattern/flag map and reproduce every declared source/page count.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. The historical note reports the investigation corrected and checked its own search artifact, not Sherlock product code.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1967 Versioned lossless metadata storage

Source lines 1967–1978; requirement. SFB mapping: SFB-002. Earlier digest topics: 05, 09.

A whole-item compressed-output allowance rejected completed raw-metadata inventories. Synthetic uniform data had not predicted the historical bytes' storage size. Do not discard unexplained padding or selected metadata fields to force a pass. A versioned correction may partition lossless metadata at fixed frame boundaries, with explicit per-artifact and total bounds, exact gap-free coverage, strict decompression and byte equality, exclusive output creation and final source checks. Preserve the original refusals and distinguish a newly enlarged total storage contract from meeting the old limit.

Acceptance checks

- Fixed-boundary lossless partitions must meet explicit artifact/total budgets, strict decompression, byte equality, exclusive creation, gap-free coverage and final source checks while retaining old refusals.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L1979 Narrow local storage-retest scope

Source lines 1979–1986; requirement. SFB mapping: SFB-002. Earlier digest topics: 09, 19.

Local retest: the revised storage implementation passed boundary, corruption, collision and incomplete-output controls, including a high-entropy synthetic fixture and a real synthetic container-to-artifact round trip. The new bounded historical collection also completed; the old cap failures remain recorded. This verifies the investigation's local correction only, not a Sherlock product change. Byte-consistent metadata still requires a separate provenance/clock interpretation; storage success must not auto-promote it to historical truth.

Acceptance checks

- Keep original cap failures and distinguish locally verified storage correction from product change or authenticated clock/provenance interpretation.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L1987 Producer-specific diagnostic grammar

Source lines 1987–1999; requirement. SFB mapping: SFB-002. Earlier digest topics: 08, 23.

A strict producer-specific parser accepted a zero-valued runtime throughput field but refused a space-padded integer form during a larger run. Synthetic acceptance should cover supported producer formatting independently from encoded media timing, while still rejecting unknown lines, warnings and changed frame joins. Preserve the original failed log and admission; a diagnostic-only in-memory normalization is not permission to relabel it clean. Any grammar correction requires a new pinned version, negative controls and a declared execution schedule.

Acceptance checks

- Test supported zero and space-padded runtime formats separately from media timing; unknown warnings and changed joins still fail, and corrections require new pins, negatives and schedule.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2000 Narrow wrapper correction and cumulative accounting

Source lines 2000–2010; requirement. SFB mapping: SFB-002. Earlier digest topics: 07, 09, 23.

Checked the producer's tagged primary source before permitting exactly its single-ASCII-space padding at one named field. A separately identified wrapper preserves the original module and refused output, records both parent and wrapper hashes, and keeps cumulative resource accounting across versions. Author and independent fresh controls passed; new paired extractions also passed while earlier products remained excluded. Tests distinguish inherited child-process coverage from actual configured-wrapper coverage.

Acceptance checks

- Preserve parent/refused output and wrapper hashes, cumulative accounting and configured-wrapper controls; a permitted producer-specific single-space field is not a general normalizer.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. The reported verification is limited to that local correction; it does not authenticate historical sources or establish a general diagnostic normalizer.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2011 Exclusion validity through actual resampling kernels

Source lines 2011–2023; requirement. SFB mapping: SFB-002. Earlier digest topics: 16.

During method preparation, both reviewers identified that a nearest-resized validity mask can admit values contaminated by bilinear mixing from excluded pixels. Mask disjointness alone does not test this. Add a synthetic pair with identical permitted content and contrasting excluded content; require identical values at every declared-valid output location through every allowed resize and field-selection branch. A conservative buffer is acceptable only in its tested domain, with lost coverage explicit. Priority: before relying on scored measurements.

Acceptance checks

- Contrasting excluded pixels cannot change any declared-valid output across allowed resize and field-selection branches; tested buffers report their lost coverage.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2024 Photometric fit/evaluation masks and extrapolation

Source lines 2024–2035; requirement. SFB mapping: SFB-002. Earlier digest topics: 16, 19, 21.

A rectangle labeled "background evaluation" can overlap a separately named training rectangle. Require an actual mask-intersection assertion after resampling/exclusions, not independence inferred from role names. Preserve the original geometry fit and version any new photometric mask. Synthetic acceptance should include global tone changes and local/displaced bright patches, empty threshold unions, clipping ties, and bright values outside the training intensity range. Report that extrapolation and distinguish encoded-bright-pixel support from physical fire area.

Acceptance checks

- Assert training/evaluation mask intersections after processing; test tone/patch/extrapolation/empty-union/clipping cases and keep bright-pixel support separate from fire area.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2036 Prior exposure and partial review independence

Source lines 2036–2041; requirement. SFB mapping: SFB-002. Earlier digest topics: 10, 21.

Record which parent observations, candidate labels and scores were available before each qualitative checkpoint. A hint arriving mid-review changes the remaining interpretation's independence; a later note must not relabel the whole pass blind.

Acceptance checks

- Record hints, labels, scores and parent observations available at each checkpoint; mid-review exposure changes only defensible independence claims.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2042 Saved-review freeze receipts and endpoint joins

Source lines 2042–2054; requirement. SFB mapping: SFB-002. Earlier digest topics: 02, 10, 14, 21.

A reviewer can save an independent annotation and immediately send its coordinates while the other reviewer's estimates still exist only in reasoning. Synthetic acceptance: release comparison payloads only after both saved-artifact hashes/receipts exist; otherwise retain the exact exposure order and downgrade only the affected independence claim. Numerical agreement cannot retroactively satisfy the gate. Also preserve upper-versus-lower endpoint definitions when similarly named features from separate studies are joined, and distinguish an archive-name search from semantic inspection of differently named members.

Acceptance checks

- Do not exchange comparisons before both saved hash receipts exist; preserve exposure order, upper/lower endpoint definitions and archive-name versus semantic inspection limits.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2055 Host visibility, landmark localization and correspondence

Source lines 2055–2067; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 10, 12.

Two readers can both reject a distinctive landmark while one calls its visible host edge ambiguous and the other calls the landmark unavailable. Preserve host-region visibility, landmark localization and correspondence/change as separate fields; do not turn overlapping label semantics into apparent physical disagreement or retroactively recode to manufacture consensus. Synthetic acceptance must also distinguish a visible candidate from a measurement-suitable point. An explicitly source-guided saved-point overlay must not be advertised as independent point selection.

Acceptance checks

- Keep overlapping label meanings separate; do not recode for consensus or treat a source-guided overlay as independent point selection.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2068 Exact rounding, continuous membership and crop records

Source lines 2068–2081; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 11, 18, 27.

A synthetic value immediately below a half-cell boundary can cross that boundary when floating addition rounds before `floor` is applied. The local reproduction returned different cells for float-add-then-floor and exact half-up arithmetic on the same binary input. Declare the rounding convention, test adjacent-to-tie values, and distinguish original continuous-domain membership from rounded-cell membership and crop padding. Preserve a plain crop, a separately marked copy, validity masks and exact saved coordinates; a display convention is not a physical localization error bound.

Acceptance checks

- Test adjacent half-cell ties under declared rounding; preserve continuous-domain membership, rounded cells, padding, plain/marked crops, masks and exact saved coordinates.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. This reproduced numerical/display pitfall is not itself a demonstrated historical measurement error.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2082 Scene planes, seek tails and exact prior-recipe replay

Source lines 2082–2101; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 09, 15, 16, 23.

A synthetic scene can retain highly correlated foreground buildings while its background and dynamic regions differ. Keep registration regions, background checks and post-fit dynamic diagnostics separate; retain repeated-grid aliases, full candidate coverage and prior-viewed versus unused evidence. A score band is not a confidence interval or unique exposure. In a second fixture, seeking preserves an earlier keyframe lead-in and a short input-duration allowance omits a selected interval's final frames despite successful decoding. Require exact per-frame PTS-list coverage and known-anchor pixel agreement, not merely exit status or one sample per second. Preserve the failed partial output and version the read-window correction without changing the selected interval. Reproduction must verify the completed prior recipe, actual arrays and saved native pixels, including recomputed shortlist membership; sharded limits need aggregate accounting that includes failed runs. Nonfinite timestamp strings must fail explicitly.

Acceptance checks

- Require exact selected PTS coverage and anchor pixels, preserve failed partials and prior arrays, recompute shortlist membership, account failed runs and reject nonfinite timestamps.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2102 Changing-image order versus row-list reversal

Source lines 2102–2116; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 16, 21.

Reversing a list of scored rows is not a test of changing-image sequence order. Use invented image sequences with identical stationary scenery and distinct changing regions, then reorder the reference images. Acceptance preserves ambiguous stationary assignments while recovering the reordered changing-detail candidates; it must not issue an original-clock or soundtrack certificate. Keep candidate-set alternatives, coarse-sampling endpoints, mask-dependent detail and aspect normalization explicit. A good candidate can justify a dense test without authorizing post-result threshold/region tuning.

Acceptance checks

- A synthetic reordered-reference sequence with unchanged scenery preserves ambiguous stationary assignments but recovers changing-detail alternatives without clock/soundtrack certification.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. The historical note reports the local synthetic control was added and passed before historical execution; it is a local workflow correction only.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2117 Duplicate indices, repeated pictures and unseen clusters

Source lines 2117–2125; requirement. SFB mapping: SFB-002. Earlier digest topics: 16, 21.

Dense-refinement clarification for that same fixture: reject duplicate index entries, not distinct presented indices carrying identical pictures. A new synthetic control retains all such entries. A top-two visual shortlist can sample only one near-identical cluster while other near-best bands remain unviewed; retain those alternatives and forbid a uniqueness certificate. Refining a previously selected time window is not independent corroboration.

Acceptance checks

- Reject duplicate index records while retaining distinct indices with equal pictures; keep near-best unviewed bands and deny uniqueness or independence from temporal refinement.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2126 Identical-support transform comparison

Source lines 2126–2140; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 16.

Two fitted transforms can admit equally many pixels at different positions. Comparing scores on those different sets can misattribute a support change to geometry. A synthetic fixture now explicitly gives equal-cardinality but unequal-position valid sets. Acceptance records both sets and their intersection, evaluates the already selected transforms on that common set without refitting, and applies coverage against the original full-mask denominator. Preserve missing-transform and coverage/variance failures rather than replacing them with zero.

Acceptance checks

- Record both positional supports and their intersection; score already chosen transforms on that intersection without refitting and use the original full-mask denominator while preserving failures.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. The historical note reports independent local controls passed for the differing-position fixture and common-support gates; this is not product-fix verification.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2141 Historical media-method issue priority and state

Source lines 2141–2142; context. SFB mapping: SFB-002. Earlier digest topics: 26.

The historical source assigned SFB-002 priority P2, required before quantitative media work, and recorded acknowledgment with no fix then reported.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Historical status metadata only; no technical requirement omitted.

## TR-L2143 Media workbench versus validated measurement bridge

Source lines 2143–2144; requirement. SFB mapping: SFB-002. Earlier digest topics: 24, 26.

The README documents specialist processing only for deterministic text comparison. A separate media workbench currently preserves bytes and derivatives; a validated motion/audio-measurement bridge is not established here. This is a capability request, not a claim that every underlying schema field is missing.

Acceptance checks

- Readiness distinguishes bytes/derivatives preservation from a validated motion/audio-method bridge without asserting every underlying schema field is missing.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2145 Time-based measurement add-on contract

Source lines 2145–2146; requirement. SFB mapping: SFB-002. Earlier digest topics: 14, 15, 17, 24.

Requested improvement: A documented add-on contract for time-based measurements: original presentation timestamps and edit/duplicate/drop maps, source/derivative IDs and hashes, units and coordinate transforms, calibration, uncertainty, procedure/environment hashes, diagnostic failures, and a limited claim ceiling. Keep measured motion separate from inferred event cause.

Acceptance checks

- Retain PTS, edit/duplicate/drop maps, lineage/hashes, units, transforms, calibration, uncertainty, procedure/environment pins and diagnostic failures under a causal claim ceiling.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2147 Synthetic trajectory and synchronized-tone fixture

Source lines 2147–2148; requirement. SFB mapping: SFB-002. Earlier digest topics: 14, 15, 17.

Synthetic reproduction: Import a known-trajectory video and synchronized test tone with deliberate edits, variable frame timing, and duplicate frames. No real footage or case records required.

Acceptance checks

- A known-trajectory test video and synchronized tone exercise deliberate edits, variable timing and duplicate frames without historical evidence.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2149 Measurement reproducibility and uncertainty acceptance

Source lines 2149–2150; requirement. SFB mapping: SFB-002. Earlier digest topics: 14, 15, 17, 24.

Acceptance: Timestamp/lineage preservation; error within declared calibration/tracking tolerances; unsupported/unaligned input fails visibly; equivalent reruns reproduce results or meet declared numeric tolerances; reports retain uncertainty and do not promote a measurement into a causal finding automatically.

Acceptance checks

- Unsupported/unaligned input fails visibly; reruns reproduce or meet declared tolerances; reports retain uncertainty without automatic causal promotion.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2151 Implicit transforms and rational timing alignment

Source lines 2151–2152; requirement. SFB mapping: SFB-002. Earlier digest topics: 08, 15, 27.

The historical technical supplement reports that synthetic local timing review exposed default autorotation/autoscaling and output-clock normalization. The local correction disables implicit transforms, validates per-frame geometry/format, checks exact rational source/output PTS alignment, rejects malformed hashes, and preserves initial/sanitized failure provenance. These are generic acceptance requirements, not evidence that Sherlock implemented or validated the method.

Acceptance checks

- Disable implicit autorotation/autoscaling, verify per-frame geometry/format and exact rational PTS alignment, reject malformed hashes and preserve original/sanitized failure provenance.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Delivery routing, receiving-log locator and case-payload exclusion boilerplate removed; technical conditions retained.

## TR-L2153 Measured mixing, seek differences and distinct event clocks

Source lines 2153–2154; requirement. SFB mapping: SFB-002. Earlier digest topics: 15, 17, 27.

A measured default downmix can differ from an arithmetic mean; independent-channel content can cancel; direct seeking can return different decoded samples than full-file decoding at the same requested interval. Plot limits can hide retained numeric peaks, and machine transcript segment offsets can be mistaken for sound or visual event times. Synthetic acceptance: left-only/right-only/in-phase/antiphase fixtures; measured mixing coefficients; full-decode versus seek comparisons with retained residuals; explicit plotted-versus-numeric range checks; separate audio sample clock, video PTS, transcript navigation and independently reviewed event annotations. A successful rerun must not imply source authenticity or detection calibration.

Acceptance checks

- Test left/right/in-phase/antiphase inputs, mixing coefficients, full-decode/seek residuals and plot-versus-numeric ranges; distinguish audio, video, transcript and reviewed event clocks.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2155 Waveform specificity and execution gates

Source lines 2155–2167; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 17, 23.

A synthetic repeated tone produces multiple perfect waveform matches, whereas a shifted nonperiodic passage has a recoverable offset. Acceptance: retain full signed search profiles, competing peaks, undefined low-energy scores, channel pairs and explicit candidate selection; separate sample-grid resolution from timing accuracy. A scale-one failed screen must not exclude shared material after speed or other processing changes, and reversal is not a calibrated independent null. Historical execution should require a successful controls receipt tied to the actual code, protocol, runtime and decoder pins.

Acceptance checks

- Retain signed full profiles, competitors, low-energy undefined scores, channel pairs and selection; require controls tied to actual code/protocol/runtime/decoder before historical use.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2168 Negative visual claims and extraction coverage

Source lines 2168–2169; requirement. SFB mapping: SFB-002. Earlier digest topics: 14, 15, 27.

Extend the existing media fixture with endpoint samples separated by an uninspected interval, later refinement that starts after a visible change, and two synthetic containers with identical decoded pixels/timestamps but unequal container bytes. Acceptance: a negative claim requires explicit temporal and resolution coverage; refinement keeps its original declared selection and cannot become earliest-onset coverage retrospectively; distinguish byte identity from decoded-product identity and record runtime pins for each execution. Separate shot changes, foreground actions, camera movement, transcript pointers and structural features instead of assigning a generic event-onset field.

Acceptance checks

- Retain uninspected temporal intervals, original refinement scope, byte/decoded identity, execution pins and distinct shot/foreground/camera/transcript/structural event fields.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2170 Visibility versus transient-detection opportunity

Source lines 2170–2183; requirement. SFB mapping: SFB-002. Earlier digest topics: 12, 14.

A spatially visible region is not a calibrated transient-detection opportunity; a hidden source may illuminate another exposed region. Synthetic acceptance: retain separate source-region visibility, observable outward effects, exposure/ sampling coverage and detector sensitivity. Distinguish an unseen boundary behind foreground from an unlocated boundary possibly outside the frame. Preserve categorical reviewer disagreements without translating them into area fractions. In a later sequential fixture, retain an isolated one-frame bright change as a descriptive candidate rather than requiring persistence that deletes it automatically; neither that candidate nor its absence identifies a mechanism.

Acceptance checks

- Separate source visibility, outward effects, sampling and sensitivity; preserve categorical disagreements and isolated one-frame candidates without automatic mechanism inference.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2184 Joint spatial-temporal support for persistent states

Source lines 2184–2193; requirement. SFB mapping: SFB-002. Earlier digest topics: 12, 14.

Observing a lower region earlier and an upper region later must not create unobserved lower-region/later coverage. Conversely, a resolved post-event image may test a persistent effect without continuous footage; a transient or newly occurring transition has a different temporal contract. Acceptance: preserve joint place/time/quantity support, distinguish absent index tags from absent pixels, and never relabel a negative observation of one phenomenon as a negative observation of another.

Acceptance checks

- Do not combine different region/time samples into unobserved coverage; persistent effects and new/transient changes use different temporal contracts and phenomenon-specific negatives.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2194 Sequential-review context and row-scoped coverage

Source lines 2194–2205; requirement. SFB mapping: SFB-002. Earlier digest topics: 10, 12, 21.

Sequential-page follow-through, same note: synthetic overlapping batches should distinguish a reader's first-frame missing incoming context from a poor-quality-image uncertainty. Preserve both readers' shared boundary rows; repeated context is not another vote. When several images are displayed together, record saving before the next page, not before the next already-seen frame. Acceptance also requires row-scoped coverage parsing: an index repeated in explanatory prose must not become an extra observation. Fixed-sample reannotation and result-selected follow-up remain separate states.

Acceptance checks

- Separate missing incoming context from image uncertainty, retain shared boundary rows without extra votes and count row observations rather than indices repeated in prose.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. The historical note reports a local bookkeeping error was corrected without changing the observations.

Publication transformation: Historical routing and generic no-payload boilerplate omitted; fixed-sample versus result-selected states and the local bookkeeping-correction scope retained.

## TR-L2206 Candidate initiation, continuation and nested events

Source lines 2206–2216; requirement. SFB mapping: SFB-002. Earlier digest topics: 10, 12.

The same fixture should distinguish a newly selected candidate, continuation of an existing candidate, and no additional candidate. Otherwise equal scene descriptions can receive different codes without being contradictory physical observations. Include a brief separate point inside a longer changing-edge interval: grouping consecutive positive rows must not erase that nested candidate or turn every retained row into a separate event. Acceptance preserves original descriptions, candidate identity/location and initiation/continuation uncertainty without post-result relabeling or vote-derived confidence.

Acceptance checks

- Preserve nested short candidates inside longer positive intervals, original descriptions/identity/location and onset uncertainty without post-result recoding or vote-derived confidence.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2217 Byte-distinct pixel-identical sources and image coverage

Source lines 2217–2226; requirement. SFB mapping: SFB-002. Earlier digest topics: 03, 27.

Source-copy follow-through, same SFB-002 contract: a PNG fixture should encode the same pixels through two byte-distinct valid streams. Verify each against its own receipt before comparing complete decoded arrays; unequal file hashes are a check trigger, not by themselves corruption or a new historical source. Stored pixel-hash agreement alone is not a fresh decode check. Include a full-frame metadata list with only a sparse set of actual image products; report metadata rows, existing images and reviewed images separately.

Acceptance checks

- Verify each stream's own receipt and freshly decode full arrays; count metadata rows, actual images and reviewed images separately.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2227 Concurrent diagnostic context and source-text roles

Source lines 2227–2228; requirement. SFB mapping: SFB-002. Earlier digest topics: 08, 15, 27.

A diagnostic warning without a timestamp cannot be attached to the nearest message from a concurrent pipeline. Synthetic acceptance: nested context prefixes, interleaved unrelated stages, repeated/suppressed messages, terminal warnings and unrelated fatal errors; require complete same-context association and source/output clock/count checks. Preserve a marked preamble separately from later measurement selections: disjoint indices neither prove those selections damaged nor certify them clean. Keep exact source-copy bytes distinct from executable-equivalent text and separately label analyst annotations in machine-result summaries.

Acceptance checks

- Timestamp-free warnings require complete same-context association; retain preamble/selections, source/output clocks/counts, source-copy versus executable text and separate analyst annotations.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2229 Intensity and acquisition-time non-identifiability

Source lines 2229–2230; requirement. SFB mapping: SFB-002. Earlier digest topics: 14, 15, 19.

Add a synthetic acceptance witness where distinct acquisition and postprocessing histories have identical sampled arrays and presentation times. Preserve both histories rather than treating a classifier tie as an implementation defect. An image-space interpolation coefficient is not an exposure fraction; retain unclipped coefficients, native-clock versus fitted residuals, zero-span undefined values, and ordinary motion/noise counterexamples. A fixed screen region may become foreground or occlusion and must not silently remain a material track.

Acceptance checks

- Retain distinct histories with identical sampled arrays/PTS, unclipped interpolation coefficients, clock/fitted residuals and undefined cases; fixed screen regions cannot silently stay material tracks.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2231 Clean clocks and decode do not prove pixel continuity

Source lines 2231–2232; requirement. SFB mapping: SFB-002. Earlier digest topics: 08, 15, 21.

Further observed acceptance cases for the existing visual-coverage and diagnostic notes: a video with orderly PTS and clean video decoding can already contain mixed/banded image interruptions; an unmapped audio-layout diagnostic should remain a separately classified, preserved warning rather than silently invalidate or certify video pixels. Synthetic acceptance: insert degraded mixed frames into a regular-clock fixture, verify that byte identity does not become continuity, retain unsampled gaps and nonblind reviewer hints, and reject all diagnostics outside a prospectively declared narrow grammar. Separate raw address-bearing logs from deterministic image/selection outputs.

Acceptance checks

- Test degraded mixed frames in a regular-clock fixture, preserve audio-warning classification, sampling gaps and hints, and reject diagnostics outside a declared narrow grammar.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2233 Reference identity and common coordinate errors

Source lines 2233–2234; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 11, 14, 16, 21.

A textual landmark description can be paired with the wrong pixel coordinate; repeated nominal manual coordinates and self-correlation do not verify the intended feature. Synthetic acceptance: place a bright corner beside a low-texture region, supply a misplaced annotation, and require a baseline marker/patch overlay with separately recorded identity and texture checks before freezing a reference set. Preserve the original annotation and post-output correction as distinct records; do not silently replace evaluation points or confuse coarse envelope agreement with verified material identity. Also retain nearby tied peaks even when a distant-competitor margin is large; image-clipped search support; all-reference admission failures; and a flexible fit whose omitted-reference prediction worsens despite smaller training error. A common coordinate error can pass both training and leave-one-out checks, so those are not independent validation sources.

Acceptance checks

- Require marked baseline identity/texture checks; retain corrections, tied peaks, clipped support, failed references and worsened holdout predictions despite improved fit.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2235 Rehashed preflights and exact execution identity

Source lines 2235–2236; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 18, 23.

A copied preflight can be internally rehashed yet disagree with the approved candidate object or first-qualified choice. Bind the consumer to the exact declaration, visual review, parameters, procedure and source identities; test an actual altered/rehashed file through the entry point, not only a pure validation function. Preserve the finite rejected calculations before failing. A result at a numerical cutoff can change its binary flag between correct floating implementations: retain the declared flag, report arithmetic tolerance/conditioning and use exact reasoning where available, rather than calling solver roundoff a physical discrepancy. Initial procedure pins and final dependency unions have different roles; reviewers must verify their declared relationship, not assume identical inventories. Distinct repeated-run directories are also necessary to claim two executions.

Acceptance checks

- Exercise altered/rehashed files through actual entry points; retain rejected calculations, cutoff conditioning, pin/union relationships and distinct repeated-run directories.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2237 Location versus correspondence and differential inference

Source lines 2237–2238; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 12, 14, 18, 27.

Extend the existing annotation contract with a generic fixture where two analysts place the same visible corner at the same coordinates but disagree about whether it continues the original feature. Preserve location and correspondence as separate fields; rectangle overlap cannot repair identity. Include a second fixture where one displacement interval excludes zero and another includes it, but their difference still includes zero: separate threshold outcomes do not establish a difference or event order. A third fixture removes one reference map at an earlier selected sample; the first available positive mapped interval moves later without changing the underlying observations. Report that as an availability effect, not delayed motion. A marked derivative must not inherit an unmarked-image caption, and display-cell origins versus centers must be explicit.

Acceptance checks

- Equal coordinates do not establish feature continuity; differing zero tests do not establish a nonzero difference; missing maps cause availability effects, not delayed motion.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2239 Calibration identities and clock-rate sensitivity

Source lines 2239–2240; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 14, 15, 18.

Preserve assigned units separately from independently verified physical calibration. A tape can reproduce a stored transform exactly while several different landmark pairs share its length. Synthetic acceptance: retain candidate endpoint identities and distinguish floor level, window top and parapet; do not manufacture a discrepancy from unlike quantities or validate endpoints with scalar agreement. Distinguish pixels-per-length from length-per-pixel, playback rate from analysis and exposure clocks, constant origin shifts from window/initial-condition changes, and horizontal-marker amplification from vertical physical descent. Require clock-rate sensitivity with its squared effect and correct direction; do not treat arbitrary synthetic parameters as historical error bounds. Reject calibrating a measurement by assuming the very quantity it is meant to test, while permitting a separate authenticated calibration experiment. Missing provenance must not automatically become a measured distortion or a veto on explicit conditional reasoning.

Acceptance checks

- Verify endpoint/quantity identity and scale direction; test squared clock-rate sensitivity without circular calibration or turning synthetic perturbations into historical error bars.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2241 Direct endpoints, periodicity and declared displays

Source lines 2241–2242; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 11, 14, 21, 27.

Extend the calibration fixture with a query at a foreground boundary and visible repetition nearby. Preserve direct endpoint identity separately from an extrapolated row and indirect approximate-scale support; neither occlusion alone nor a strong periodicity score resolves the calibration. Nested windows and repeated transforms reuse evidence and must not become independent confirmations. Exact saved coordinates and display-centre/corner conventions are not physical localization precision. Check declared versus actually generated display labels and exact-point exclusion versus patch overlap; retain a scoped discrepancy instead of silently rewriting a frozen declaration.

Acceptance checks

- Keep direct endpoint identity separate from extrapolation/periodicity; verify labels and point/patch exclusion while preserving frozen declarations and dependent repeated transforms.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2243 Annotation history and all-window fit semantics

Source lines 2243–2244; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 14, 15, 18.

A saved “keyframe” may represent manual or automatic marking, or a loader fallback; membership is not a historical provenance trail or independent measurement. Extend the generic fixture with preserved positions, optional key metadata and distinct original/derived states, including a strictly validated alternative numeric-array serialization. Retain the initial format rejection and recoverable code rather than calling it scientific missingness. For trajectory tools, preserve every declared overlapping window and model, the polynomial normalization and derivative response weights; do not promote a window-centered coefficient to an instantaneous event or turn coincident nominal/encoded clocks into independent corroboration. Unit perturbation response is not a measured uncertainty distribution, and a plotted near-reference segment must not replace all-window results.

Acceptance checks

- Preserve marking/fallback provenance, optional metadata, validated alternative serialization and recoverable rejection; retain every fit window/model, normalization and derivative weights.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2245 Contour observables, joint fits and negative controls

Source lines 2245–2246; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 12, 14, 18.

A fixed-image-column silhouette sample and a material landmark require different observable types; common vertical translation can cancel while horizontal motion changes the sampled contour. Preserve a known sampling coordinate when the other coordinate becomes unlocalizable. For subjective interval propagation, distinguish each window's feasible coefficient from one jointly feasible sequence across overlapping windows; retain any constructed feasibility witness as a calculation, never an observation or probability. Numerical texture-screen success must not overwrite a separate visual rejection. Negative-control records should preserve attempted inputs (nonfinite values symbolically), not just rejection names; derivative failure receipts should cover exception paths as well as explicit mismatches.

Acceptance checks

- Distinguish fixed-column silhouette from material landmarks, retain a known coordinate, joint-feasibility scope, visual rejections and attempted symbolic nonfinite inputs/exception receipts.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2247 Architectural regions and simultaneous two-axis feasibility

Source lines 2247–2248; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 12, 14, 18.

Preserve a source-supported architectural region separately from an exact physical material point, attachment, depth and metric calibration. A generic facade graphic can identify a component family without supplying an engineering node or distance. Extend the joint-box fixture to x/y simultaneously, retaining original observer-box intersections, empty local intersections, global separation conflicts and constructed witness membership. Uniform box widening is mathematical sensitivity, never an estimated actual error. Test labels must name operations actually performed: a constant difference array is not evidence that two source arrays underwent a shared transformation; retain the transformation inputs to test that claim.

Acceptance checks

- Keep region identity separate from material point/attachment/depth/calibration; joint x/y tests retain intersections, conflicts, witnesses and actual transformation inputs.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2249 SFB-003 section heading

Source lines 2249–2250; context. SFB mapping: SFB-003. Earlier digest topics: 26.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Section heading only; requirements follow.

## TR-L2251 Historical feedback-readiness issue state

Source lines 2251–2252; context. SFB mapping: SFB-003. Earlier digest topics: 26.

The historical source assigns priority P2 to investigation/development coordination; it records acknowledgment and a verified minimal project log while broader acceptance criteria remained unmet.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Historical date/status metadata only; requirements are preserved separately.

## TR-L2253 Stable feedback intake and capability-specific readiness

Source lines 2253–2254; requirement. SFB mapping: SFB-003. Earlier digest topics: 26.

Requested improvement: A lightweight project-owned intake for investigation feedback with stable IDs, duplicate linkage, impact, safe reproduction, acceptance tests, acknowledgment, and fix-verification status. Readiness should distinguish schema availability, implemented command, tested synthetic behavior, validated domain method, and human/expert review prerequisite.

Acceptance checks

- Keep stable IDs, duplicate links, impact, safe reproduction, tests, acknowledgment and fix verification; distinguish schema, command, synthetic, domain-method and human/expert readiness.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2255 Duplicate feedback and reported-fix fixture

Source lines 2255–2256; requirement. SFB mapping: SFB-003. Earlier digest topics: 26.

Synthetic reproduction: Submit the same capability request twice, acknowledge one canonical item, and mark an implementation reported but not independently retested.

Acceptance checks

- Two identical requests resolve to one canonical acknowledgment and a reported implementation stays not independently retested.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2257 Versioned status and unverified fixes

Source lines 2257–2258; requirement. SFB mapping: SFB-003. Earlier digest topics: 26.

Acceptance: No duplicate active work item; versioned status history; a reported fix remains unverified until its acceptance test is recorded; a generic stage label cannot imply that a specialist measurement or inverse-analysis capability exists.

Acceptance checks

- No duplicate active item; version status history and require recorded acceptance tests before verifying a fix or claiming specialist capability.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2259 Delivery-ledger heading

Source lines 2259–2260; context. SFB mapping: none. Earlier digest topics: 26.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Ledger heading only; substantive acceptance lessons in following entries retained.

## TR-L2261 Tracking search surfaces and claim ceilings

Source lines 2261–2262; requirement. SFB mapping: SFB-002. Earlier digest topics: 14, 16, 23.

Synthetic template tracking motivates these requirements: high correlation is not physical-point identity; retain full search surfaces and competing coordinates; record boundary/occlusion stopping rather than silent interpolation; distinguish deterministic scientific products from variable runtime logs. Acceptance reconstructs every selected/competing result and includes known-translation and identity/occlusion limitation tests. The historical entry records acknowledgment, not implementation or verified fix.

Acceptance checks

- Reconstruct selected and competing results; test known translation and identity/occlusion limits while separating deterministic products and runtime logs.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Delivery destination/file and payload-history details replaced by generic acknowledgment scope; no requirement omitted.

## TR-L2263 Deterministic scientific products versus variable logs

Source lines 2263–2264; requirement. SFB mapping: SFB-002. Earlier digest topics: 08, 23.

Two extraction runs can have identical sampled pixels and encoded timestamps while their final processing-throughput fields differ. This is already covered by the acknowledged deterministic-products versus runtime-logs requirement, not a new issue. Retain complete logs and explicit differing fields; keep material equality separate from whole-log inequality. A synthetic fixture should preserve that distinction while refusing changed frame timestamps, unexpected diagnostic lines or unexplained differences. Do not expand a generic warning allowlist to obtain a pass.

Acceptance checks

- Preserve full logs and explicit runtime-only differences while refusing changed timestamps, unknown diagnostics and unexplained differences; do not widen warning allowlists to pass.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. The historical audit retained the distinction; it did not establish a product implementation or fix.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2265 SFB-004 section heading

Source lines 2265–2266; context. SFB mapping: SFB-004. Earlier digest topics: 26.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Section heading only; requirements follow.

## TR-L2267 Distinct search and acquisition dispositions

Source lines 2267–2268; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 01, 02, 03.

Extend the existing acquisition-state fixture with four distinct outcomes: a located packet not fetched pending approval; a standalone route rejected by the tool; an attachment name without a usable link in the inspected representation; and a paper located only through a bibliography. Acceptance: do not collapse these into unavailable, reviewed, withheld or historically absent; preserve exact search coverage, independent source-family limits and unused search allowance. A guessed sheet name used as a query must never become a verified member locator.

Acceptance checks

- Located-not-fetched, tool-rejected, unusable attachment name and bibliography-only states remain distinct with exact coverage, remaining search allowance and unresolved guessed locators.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2269 Errata and scope-specific applicability

Source lines 2269–2270; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 19, 22.

Extend the existing version/dependence fixture with an erratum that swaps directional values and changes a plan attribution. Acceptance: preserve the original reading, update current attribution, and keep the author's assertion about historical inputs separate from actual input/run verification. A floor-specific modification must not propagate as either universal presence or universal absence. Distinguish source-label associations from a second export that verifies only property references; a nearby caption cannot replace the direct named-endpoint locator.

Acceptance checks

- Keep originals/current attribution and author assertions/run verification separate; floor-specific changes cannot become universal and nearby captions cannot replace named endpoint locators.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2271 Missing references and formulation-dependent fields

Source lines 2271–2272; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 05, 06, 19.

Extend the existing typed-namespace fixture with a missing reference in region A and a same-original-ID definition in region B whose include transform changes the effective namespace. Add same-number component pairs that differ in their material reference. Acceptance: report both the unresolved reference and the supplied counterpart without silently substituting it or claiming blanket absence. Keep raw numeric cards and versioned field interpretations separate: an explicit point table can supersede a zero scalar field, and a dimension field's meaning can depend on a formulation flag. Model-specific mass allocation must not become measured physical density. Preserve the source mapping, manual-version/run gap and independently tested scope, including known parser omissions.

Acceptance checks

- Preserve unresolved and supplied counterparts under include transforms; raw cards, explicit-table overrides, formulation meanings, modeled mass and manual/run/parser gaps remain explicit.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2273 Repeated-field trace and source-defined order

Source lines 2273–2274; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 05, 06, 19.

Extend the existing typed-model fixture with repeated coefficients at identifiers that belong to only one structural part, alongside shared-part identifiers with no repeats. Acceptance: do not infer a load/export-region identity from part membership; preserve row order without treating it as chronology or precedence; label analyst-defined sorting runs separately from source-defined blocks. Keep reported software version, acquired executable identity and authenticated run/input linkage as distinct states. A periodic coordinate pattern should remain descriptive until its generating rule is located.

Acceptance checks

- Typed part membership, row order and periodic patterns cannot establish export region, chronology or generator identity; distinguish reported software, acquired executable and authenticated run.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2275 Runnable failed revisions versus failure-class demonstrations

Source lines 2275–2276; requirement. SFB mapping: SFB-004. Earlier digest topics: 07, 23.

A failed run receipt can pin a code hash while the corresponding source revision is no longer saved. Acceptance: retain the runnable revision or explicitly report replay unavailable; current synthetic reproduction of a failure class is not an exact rerun of that earlier revision.

Acceptance checks

- Retain failed runnable source revisions or label exact replay unavailable; current synthetic failure-class reproduction is not a rerun of an absent revision.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2277 Typed records, duplicate semantics and safe diagnostics

Source lines 2277–2278; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 04, 05, 06.

A numeric input can use two rows for one element and repeat an identical assignment to a shared node. Synthetic acceptance: distinguish physical lines, typed records, unique identifiers and part-incidence counts; keep contradictory duplicates separate from exact repetitions; preserve required blank cards and type-specific identifier offsets. A named diagnostic must resolve through its referenced set and member graph, not through a coincidentally matching ID. Validate the active include/deletion state before labeling a supplied companion as applied, and do not turn input coefficients or model-authored labels into historical physical observations. Numeric-only inspection must allowlist keyword text as well as values; unknown text and failed-parser diagnostics must not leak source metadata.

Acceptance checks

- Separate physical lines/records/IDs/incidences, exact and contradictory duplicates, blanks/offsets, graph-resolved diagnostics and applied state; allowlist keyword text and numeric output.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2279 Historical operation-scope issue state

Source lines 2279–2280; context. SFB mapping: SFB-004. Earlier digest topics: 26.

The historical source assigns SFB-004 priority P2 for comparison/validation integrity and records acknowledgment with no fix then reported. It is a workflow-contract request, not source-inspected evidence that a particular field is absent.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Historical status/date metadata only; requirements retained elsewhere.

## TR-L2281 Operation scope and dependent validation labels

Source lines 2281–2282; requirement. SFB mapping: SFB-004. Earlier digest topics: 19, 21.

A project can use several methods while a clip shows only one unidentified operation. Project-level documentation must not silently label that clip's mechanism. Likewise, an image time inferred with a model assumption cannot serve as independent validation of that same assumption. Derivative copies must not inflate independent sample counts.

Acceptance checks

- Project-wide methods do not label an unresolved clip; assumption-derived clocks and derivative copies cannot independently validate that assumption or increase source count.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2283 Synthetic operation and clock-dependence fixture

Source lines 2283–2284; requirement. SFB mapping: SFB-004. Earlier digest topics: 19, 21.

Synthetic reproduction: One project has operations A/B using different methods, three clips including one unresolved operation, and two timestamps: an independent clock and an interval inferred from model assumption X.

Acceptance checks

- Exercise operations A/B with different methods, three clips including one unresolved operation, and independent versus assumption-X-derived timing.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2285 Late corrections without rewriting classifier inputs

Source lines 2285–2286; requirement. SFB mapping: SFB-004. Earlier digest topics: 10, 19, 21.

Acceptance: Clip/operation/project scopes remain explicit; unresolved method stays unknown; attribution and dependence links are retained; common-origin derivatives count once; assumption-X-derived labels cannot qualify as independent validation of X. Record a late correction without silently rewriting historical classifier inputs.

Acceptance checks

- Retain operation/project/clip scopes, unknown methods, attribution/dependence links and original classifier inputs; count common-origin derivatives once.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2287 Historical SFB-004 delivery scope

Source lines 2287–2288; context. SFB mapping: SFB-004. Earlier digest topics: 26.

The historical ledger reports SFB-004 delivered for logging and triage only, followed by acknowledgment under its existing ID. This did not authorize broad implementation or real-investigation access and did not verify a software fix.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Exact routing, dates and receiving-log details removed; authorization and acknowledgment limits retained.

## TR-L2289 Caution, opportunity and decisive exclusion calibration

Source lines 2289–2304; requirement. SFB mapping: SFB-004. Earlier digest topics: 12, 21.

Extend the already acknowledged caution/exclusion fixture, not a new duplicate issue. A synthetic region has minor frame overlap, unknown glazing and adequate displayed-appearance opportunity; another has dominant obstruction. Require separate candidate identity, opportunity, incidental caution and reasoned decisive exclusion. Switching among ordinary appearance classes must not change membership with identical opportunity inputs. A passing opportunity paired with `non_evaluable` must retain both inputs and an explicit consistency-review state, not silently become a negative observation. Test threshold-touching intervals, zero in-frame extent, and exclusion precedence while preserving unresolved reasons. Text-scenario agreement is rule comprehension, not visual calibration or accuracy.

Acceptance checks

- Appearance-class changes cannot alter membership with unchanged opportunity; inconsistent passing-opportunity/non-evaluable pairs require explicit review; test boundary, zero-extent and precedence cases.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2305 Nonexclusive observations and source-family normalization

Source lines 2305–2321; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 12, 21, 22.

Extend the existing annotation/dependence fixture rather than opening a duplicate issue. Synthetic smoke presence, local flame nondetection and ambiguous brightness may coexist. Preserve separate axes, every locator and the original reason: agreement on a coarse presence field must not erase disagreement on location, target identity or shape. An uncertain smooth bright edge must not silently become positive fire evidence. Separately, a raw credit string, normalized source-family key and verified common-origin relationship are different fields; mixed raw/normalized keys cannot be counted as distinct independent sources. Test an explicitly linked video pair with inconsistent credits and an approximate time inherited from a precisely timed neighbor: keep the contradiction and original precision, not a fabricated combined answer.

Acceptance checks

- Retain coexisting observation axes, locators, shape/identity disagreements, raw versus normalized credits and verified common origin; inherited precision and contradictions remain unmerged.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2322 Earlier delivery-history heading

Source lines 2322–2323; context. SFB mapping: none. Earlier digest topics: 26.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Heading only; following units preserve technical content.

## TR-L2324 Feedback deduplication and safe-payload review boundary

Source lines 2324–2325; requirement. SFB mapping: SFB-002, SFB-004, SFB-005. Earlier digest topics: 04, 26.

Deduplicate workflow lessons under existing IDs. Reproducible local method/source-reading lessons are not automatically source-inspected Sherlock defects or verified fixes. Before any later send, review the minimized exact payload and chosen destination; exclude case names, actual footage, personal metadata, local paths, headers and linked investigation reports.

Acceptance checks

- Before transfer, review the minimized exact payload and chosen destination; extend stable issues without treating separate workflow findings as inspected product defects.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Historical delivery/date labels removed; complete substantive deduplication and publication controls retained.

## TR-L2326 Nonzero-start seek coverage and display geometry

Source lines 2326–2326; requirement. SFB mapping: SFB-002. Earlier digest topics: 15, 27.

Synthetic reproduction: a tiny nonzero-start video has valid frames in requested absolute-second bins, but an exit-0 seeking command yields no images; an exact-duration boundary also wrongly rejects complete coverage. Test a full unseeked reference decode against the bounded selector and retain both failed candidates and corrected outcomes. Acceptance: every requested bin maps to an actual exact-rational PTS; empty-successful output fails; nonsquare sample aspect is separate from stored raster; RGB conversion never implies calibrated radiometry.

Acceptance checks

- Every requested bin maps to actual rational PTS; empty exit-success output fails, exact-duration complete coverage passes, and aspect/RGB semantics remain explicit.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2327 Compilation clocks and inherited exposure times

Source lines 2327–2327; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 14, 15, 21.

Synthetic reproduction: a joined video lists rounded chapter offsets and historical start times, while a report's cited close-up appears at a different relative position; a film photo is timed using a separate digital exposure. Acceptance: retain shot coverage, source-declared clocks, actual decoder PTS, exact-versus-similar frame correspondence and missing edit/clock records separately. Do not invent a constant offset, continuous burn history or independent corroboration from a reused source family. Truncated displays count as unreviewed, not successful visual inspections.

Acceptance checks

- Keep chapter/source clocks, decoder PTS, shot coverage and exact/similar correspondence distinct; do not invent offsets, continuous history or independence from reused families.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2328 Preserved partials and independently admitted retries

Source lines 2328–2328; requirement. SFB mapping: SFB-005. Earlier digest topics: 01, 07.

Synthetic reproduction: HTTP 200 terminates with a timeout and partial bytes; a fresh no-clobber copy resumes with HTTP 206. Acceptance: preserve the failed original, verify numeric range, final size/hash and prefix identity before admitting the new file. Keep transport metadata local pending exact-payload review. A successful HTTP or process exit alone is not source acquisition, and an access denial is not historical absence.

Acceptance checks

- Retain failed original; verify range/size/hash/prefix identity of a separate no-clobber retry; transport metadata needs review and access denial is not historical absence.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: A case-linked shorthand naming the original transport lesson is omitted; the full synthetic HTTP 200/206 fixture and requirements remain.

## TR-L2329 Reference-object materialization and secret-free receipts

Source lines 2329–2329; requirement. SFB mapping: SFB-005. Earlier digest topics: 01, 04, 07.

September28 recurrence, local only: A declared timeout again left an HTTP200 partial; a separately preserved full retry met the expected byte count and passed later checks. Retain both attempt states and never treat the partial as an extra source. Extend the generic adapter fixture to accept a documented top-level authenticated file-reference object as well as any supported string form; do not misclassify an object as a missing download or print/store its temporary bearer URL. Test shape validation, empty inline bytes, exact source/size joins and secret-free receipts.

Acceptance checks

- Separate partial and full attempts; support documented authenticated-reference object and string shapes without emitting bearer URLs; test empty bytes and source/size joins.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2330 Requested limits versus measured timeout compliance

Source lines 2330–2330; requirement. SFB mapping: SFB-005. Earlier digest topics: 07, 08, 09.

A terminal timeout receipt reported elapsed time beyond the explicitly requested cap. Desired behavior: retain configured limit, reported elapsed time, terminal status and admitted/excluded state separately; a requested setting is not proof the cap was met. Synthetic extension: a mock HTTP200 partial ends with a timeout after its configured limit, followed by one permitted, separately preserved complete retry. Acceptance: flag the overrun without silently relaxing the rule, retain and exclude the partial, distinguish integrity checks from protocol compliance, and never restart a live process merely because an observation wait ended. Priority: evidence-integrity reporting.

Acceptance checks

- Flag overrun without relaxing the cap; preserve/exclude partials, separate integrity from compliance and do not restart live processes at observation-wait timeout.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. The cause of the observed cap overrun remains unknown.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2331 Received candidates and unresolved origins

Source lines 2331–2332; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 22.

Synthetic reproduction: a field inventory attributes items A/B to a facility; a receiving agency preserves those exact compound codes but leaves origin blank and lists them as unidentified. Acceptance: advance receipt without claiming accepted origin; distinguish report acknowledgement from a signed transfer and a physical-photo join, Trip Date from intake date, repeated tables from independent custody evidence, and a request-log locator from a response/outcome. Preserve the earlier unknown-receipt state as dated history and require attribution worksheets for the remaining question.

Acceptance checks

- Advance receipt without origin authentication; distinguish report/signed-transfer/photo joins, trip/intake dates, repeated tables and request/response states while retaining dated unknown history.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2333 Failed feedback delivery and routing authorization

Source lines 2333–2334; requirement. SFB mapping: SFB-003, SFB-005. Earlier digest topics: 26.

The historical ledger describes a minimized feedback send refused because the designated task was archived. No receipt or acknowledgment was claimed. Routing required user selection of reopening or another destination; an agent must not silently unarchive or create a replacement. Feedback-routing failure is distinct from a blocker on otherwise authorized independent scientific work.

Acceptance checks

- A failed archived-destination send is neither receipt nor acknowledgment; do not unarchive or create a replacement without authorization, and do not halt unrelated scientific work.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Historical dates and destination context generalized; lifecycle and authorization requirements retained.

## TR-L2335 Model domains and negative-outcome types

Source lines 2335–2336; requirement. SFB mapping: SFB-004. Earlier digest topics: 19, 20.

Pending SFB-004 supplement: preserve model domain, imposed versus predicted events, calibration dependencies and negative-outcome type. Synthetic reproduction is a failure-titled paper that computes heat transfer, prescribes an opening time from an image and has a non-spread alternative run. Acceptance: no inference of global mechanical collapse, independently predicted opening failure or a whole-system no-collapse control. Unknown actual loading, prior damage/preparation and recording provenance must stay explicit, not default to absent or matched.

Acceptance checks

- A heat-transfer paper with prescribed opening time and non-spread alternative cannot establish global collapse, predicted failure or a whole-system no-collapse control; unknown initial conditions stay unknown.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2337 Conflicting version labels and edition verification

Source lines 2337–2338; requirement. SFB mapping: SFB-005. Earlier digest topics: 03, 19.

Pending SFB-005 supplement: preserve conflicting version labels when one acquired PDF identifies itself as an author original and another repository labels an unacquired, same-named but different-sized file accepted. Acceptance: keep source-attached assertions, acquisition status and hashes; no assumed byte identity, final-edition peer-review status or extra independent corroboration.

Acceptance checks

- Preserve source-attached edition assertions, acquired state and hashes; same names cannot establish byte identity, final peer-review status or independent evidence.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2339 Supplement deduplication and defect-claim limits

Source lines 2339–2340; requirement. SFB mapping: SFB-003, SFB-005. Earlier digest topics: 26.

These generic workflow supplements extend existing issues instead of opening duplicate feature requests. They are not demonstrated defects in Sherlock's current implementation.

Acceptance checks

- Add workflow refinements under existing issues without automatically classifying them as current product defects.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Historical date/routing labels removed; deduplication and claim limits retained.

## TR-L2341 Download initiated versus acquired bytes

Source lines 2341–2341; requirement. SFB mapping: SFB-005. Earlier digest topics: 01.

A public download action returned without a file path; the page subsequently displayed a download-in-progress heading, and the available content-export command was unsupported. Impact: mistaking UI progress for acquisition would allow unread evidence into a report. Synthetic reproduction: a generic repository page advertises a PDF and displays a download message, but the tool returns no usable bytes. Acceptance: retain separate located, initiated, acquired, parsed and reviewed states; require an actual artifact and integrity/format checks for acquired status; preserve the failure without claiming the source is absent, unsafe or deliberately withheld.

Acceptance checks

- Require an actual artifact and integrity/format checks for acquisition; UI progress or unsupported export does not establish reviewed bytes, absence, danger or withholding.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2342 Item provenance versus collection or sorting labels

Source lines 2342–2342; requirement. SFB mapping: SFB-004. Earlier digest topics: 03, 21, 22.

A report describes sorting material in a named area while expressly retaining mixed origins; a separate specimen report gives tentative origin and unresolved event timing. Impact: joining these by their location label could invent custody or historical causation. Synthetic reproduction: mixed items from facilities A/B enter sorting zone A, while an unrelated specimen X is tentatively attributed to A and laboratory testing identifies damage without dating it. Acceptance: storage/sorting location, asserted origin, exact member location, custody transfers, laboratory observation and historical timing remain distinct; an explicit source-backed link is required before joining the specimen to that sorting operation. Compatible laboratory chemistry must not become a demonstrated historical cause.

Acceptance checks

- Keep sorting location, asserted origin, member location, transfers, laboratory observation and historical timing separate; source-backed links are required before joining provenance.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2343 Representation coverage and document locators

Source lines 2343–2344; requirement. SFB mapping: SFB-005. Earlier digest topics: 03, 22, 27.

An HTML transcription omits a chart that is present in the source scan and differs in two date fields; another acquired PDF ends at an advertised spreadsheet's cover, without its item rows. Impact: an agent could call accessible material missing, merge distinct claims or mark an inventory complete merely because the container parses. Synthetic reproduction: a scanned report with a table and a replacement redaction sheet, an incomplete text mirror, and a companion attachment cover without the attachment. Acceptance: store source-specific physical-page, printed-page and section locators; record reviewed coverage and absent components; preserve conflicting transcriptions and explicit corrections; do not count alternate representations as independent corroboration or infer a missing attachment's contents from its title.

Acceptance checks

- Preserve page namespaces, missing components, conflicting text and explicit corrections; parsed containers, alternate mirrors and cover titles cannot supply missing evidence.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2345 Exact outbound scope and delivery recording

Source lines 2345–2346; requirement. SFB mapping: SFB-003, SFB-005. Earlier digest topics: 04, 26.

Proposed outbound supplements exclude source documents, case examples, names, actual measurements, confidential metadata and case-specific paths. Before sending, review the exact combined payload and user-selected destination under the privacy rule; request logging/triage only and record the actual delivery outcome.

Acceptance checks

- Review exact combined payload and user-selected destination, minimize protected content, request the intended scope and record actual delivery outcome.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No technical content omitted; this is the source's disclosure-control requirement, not approval for a future send.

## TR-L2347 Generic examples distinct from report attachments

Source lines 2347–2348; requirement. SFB mapping: SFB-003, SFB-004, SFB-005. Earlier digest topics: 04, 26.

Deduplicate model, inventory and bridge follow-up under existing IDs. Proposed software examples remain generic; linked local investigation reports are not outbound attachments.

Acceptance checks

- Deduplicate existing IDs and keep linked local investigation reports outside an outbound generic-software payload.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Date and historical unsent state omitted; substantive payload boundary retained.

## TR-L2349 Model transitions and illustrative annotations

Source lines 2349–2349; requirement. SFB mapping: SFB-004. Earlier digest topics: 19.

Synthetic reproduction: a static model retains load successfully, a revised model changes both geometry and thermal loading, and a proposed seconds-scale cascade is illustrated with annotated video stills. A construction photograph also carries a drawn rotation tangent. Acceptance: preserve the stable response; distinguish prescribed damage from calculated failure, static instability from dynamic contact/impact, and an illustrative annotation from an observed measurement. Do not label the changed cases a one-variable ablation or count the same interpretation as independent validation. Retain conflicting source labels pending native outputs.

Acceptance checks

- Preserve stable response and simultaneous changed factors; distinguish prescribed/calculated, static/dynamic, illustration/measurement and dependent interpretation.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2350 Closed acquisition gaps and item-component joins

Source lines 2350–2350; requirement. SFB mapping: SFB-005. Earlier digest topics: 03, 22.

Synthetic reproduction: an early mirror ends at an inventory cover, while a later official copy includes all advertised rows; one numbered item contains two attached components, and the cover lists only an aggregate shipment total. Acceptance: close the specific acquisition gap without erasing its history; preserve component/item namespaces and row boundaries; do not assign aggregate totals to rows or infer an item-to-specimen/receipt join. Alternate representations remain one source family. OCR and locator titles are not substitutes for row inspection or acquisition.

Acceptance checks

- Close only the specific edition gap while preserving history and row namespaces; aggregate totals and OCR/title locators cannot supply component, specimen or receipt joins.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2351 Schema availability versus authenticated translation

Source lines 2351–2352; requirement. SFB mapping: SFB-003, SFB-005. Earlier digest topics: 06, 23, 25, 26.

Historical isolated bridge-schema checks reported acceptance of unverified locators, hashes and endpoint IDs, default date-format non-enforcement, and rejection of a question reference kind. Synthetic acceptance tests must distinguish schema availability, expected schema behavior, a verified translation adapter, a two-engine workflow and a validated scientific method. An adapter needs byte/hash and exact endpoint/version verification plus explicit direction/role and reference-kind policy. An offline runner must declare dependencies and report unavailable validators, schema rejections and harness failures separately, without engine imports or workspace/provider access. Those schema limits did not establish a defect in an adapter not then located; a generic operating-system-read restriction was a local harness issue, not a Faraday defect.

Acceptance checks

- Separate expected schema behavior from verified adapter/workflow/method; verify bytes/endpoints/versions and policy, and distinguish unavailable validators, rejection and harness failure.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Historical bridge-capability statements must not override the later controlled synthetic export pilot; export does not establish two-way admission or scientific validation. Publication-time supersession context about the later export pilot is drawn from supplemental source SUP-01, not the feedback lines assigned to this unit.

Publication transformation: Private local report links removed. Historical schema-only scope preserved; later controlled synthetic export testing is a distinct development, not two-way admission or scientific validation.

## TR-L2353 Expected schema acceptance is not authentication

Source lines 2353–2354; requirement. SFB mapping: SFB-003, SFB-005. Earlier digest topics: 25, 26.

The historical schema-only note reports 13 expected outcomes, including acceptance of deliberately unverified inputs; this is not 13 successful authentication checks or scientific tests. It claims no new implementation fix. Before any new send, minimize the exact payload and omit local report links, source bytes, case details and environment metadata. Publication-time update from SUP-01: later controlled synthetic export testing supersedes schema-only capability descriptions but does not establish two-way admission or scientific validation.

Acceptance checks

- Label all 13 synthetic schema outcomes as expected-behavior checks, not authentication or scientific tests; exact outgoing payload remains minimized.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Historical bridge-capability statements must not override the later controlled synthetic export pilot; export does not establish two-way admission or scientific validation. Publication-time supersession context about the later export pilot is drawn from supplemental source SUP-01, not the feedback lines assigned to this unit.

Publication transformation: Historical archived-routing and delivery labels removed; synthetic test count and scope limits retained.

## TR-L2355 Byte layers, placement and annotation denominators

Source lines 2355–2356; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 12, 13, 21, 27.

Generic byte-layer requirements distinguish container bytes, stored ciphertext, decrypted encoded images and decoded pixels. Figure association uses page placement and actual reviewed content, not object enumeration order. Annotation requirements preserve localized positives outside incomplete-opening denominators, undefined empty denominators, caution versus decisive exclusion and the fact that shared geometry is not independent geometry validation. The original reviewer field-usage difference must remain recorded rather than be relabeled into consensus. These were acknowledged integration requirements from a separate prototype, not source-inspected Sherlock defects or verified fixes.

Acceptance checks

- Keep container/ciphertext/decrypted-encoded/decoded layers and placement-based figure association; preserve localized positives, undefined denominators, caution/exclusion and shared-geometry dependence.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Exact receiving turn ID, dates, file locator and case-payload boilerplate removed; all technical requirements and status limitations retained.

## TR-L2357 Timing APIs, decoder warnings and many-to-one matching

Source lines 2357–2358; requirement. SFB mapping: SFB-002. Earlier digest topics: 08, 15, 16, 27.

Synthetic examples distinguish stretched engine-time and uniform mean-duration APIs with identical endpoints, serializer units versus runtime API units, corrupt-frame warnings despite exit 0, per-source acceptance, diagnostic byte integrity versus semantic repeatability, and false/many-to-one nearest matches in countdown, static and repeated imagery. Historical acknowledgment was logging/triage only; it did not verify implementation or authorize new real-case access.

Acceptance checks

- Identical endpoints cannot equate timing APIs or units; exit-success warnings and per-source admission remain explicit, and repeated/static imagery retains false/many-to-one candidates.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Exact delivery turn/date and receiving-log location omitted; complete generic acceptance distinctions retained.

## TR-L2359 Historical package/timing feedback delivery

Source lines 2359–2360; context. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 26.

The historical ledger records delivery and acknowledgment of SFB-005 plus an SFB-002 project-timing supplement using synthetic examples. This verifies receipt/triage, not a software fix or demonstrated product defect.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Private routing identifiers, excluded-payload inventory and destination-log locator removed. Substantive requirements are preserved in their own source units.

## TR-L2361 Image identity, cadence and conflicting event times

Source lines 2361–2362; requirement. SFB mapping: SFB-002, SFB-004. Earlier digest topics: 15, 21, 22.

Generic cadence requirements distinguish pixel identity, approximate image similarity, original exposure identity and acquisition cadence; no automatic retiming or deletion follows. Event-time requirements retain conflicting source assertions, their time bases and alignment/calibration dependencies. Synthetic examples use generic noisy/static images and unrelated placeholder times. The historical acknowledgment is receipt of a contract request, not a verified product defect/fix or implementation authorization.

Acceptance checks

- Distinguish exact/approximate pixels, original exposure and cadence; forbid automatic retiming/deletion and retain conflicting time assertions with bases/alignment dependencies.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Exact delivery turn/date and destination-log locator removed; technical distinctions and synthetic scope retained.

## TR-L2363 Historical initial feedback batch delivery

Source lines 2363–2364; context. SFB mapping: SFB-001, SFB-002, SFB-003. Earlier digest topics: 26.

The historical ledger records SFB-001 through SFB-003 delivered together as minimized technical observations and synthetic tests for documentation/triage, not implementation. It excluded the investigation charter, case documents, private correspondence and broader task history.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: Delivery date/routing details omitted; authorization and payload boundaries retained.

## TR-L2365 Acknowledgment versus unresolved broader readiness

Source lines 2365–2366; requirement. SFB mapping: SFB-001, SFB-002, SFB-003. Earlier digest topics: 26.

The historical recipient log acknowledged SFB-001 through SFB-003. It then confirmed an unsupported full-charter path and a missing validated media-method contract. The full-charter limitation was later superseded by local adoption verification. A minimal feedback log did not establish command-managed lifecycle, duplicate handling, readiness distinctions or fix-verification gates. Delivery/triage did not establish a software fix, causal finding or case finding.

Acceptance checks

- Do not infer command lifecycle, duplicate handling, readiness or fix verification from a minimal log; retain later SFB-001 resolution instead of reopening its old state.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: Absolute private receiving-log path omitted. The early SFB-001 no-fix state is explicitly historical and superseded.

## TR-L2367 SFB-005 section heading

Source lines 2367–2368; context. SFB mapping: SFB-005. Earlier digest topics: 26.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Section heading only; requirements follow.

## TR-L2369 Per-chunk dependency maps and shared resource lanes

Source lines 2369–2382; requirement. SFB mapping: SFB-005. Earlier digest topics: 06, 09.

A passing synthetic suite did not test omission of a required source entry from one chunk's input map. Acceptance must check every chunk against a fresh mandatory source/reference map; checking only a conflict-free union is insufficient. Separate negative controls now exercise missing source/reference, cross-pass conflicts and changed bytes at final recheck. A second local failure arose when parallel synthetic suites shared a byte-counted directory and one removed its temporary fixture during the other's filesystem walk. Preserve the incomplete run, serialize runs sharing that accounting boundary, and rerun unchanged checks; do not convert missing files into zero-byte successes.

Acceptance checks

- Each chunk must contain a fresh mandatory dependency map; preserve failed shared-directory races, serialize shared accounting, rerun unchanged controls and never count missing files as zero-byte success.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2383 Owned descendants and bounded process cleanup

Source lines 2383–2394; requirement. SFB mapping: SFB-005. Earlier digest topics: 08, 09.

Test a successful parent with a still-running child, a termination-ignoring descendant, an immediate stop, interruption and a failed final filesystem inspection. Acceptance requires bounded cleanup of the owned process group, the original failure reason, honest unknown measurements, persistent failure receipts and actual child-termination checks. A successful leader exit alone is insufficient; requested limits, observed duration and possible polling overshoot stay separate.

Acceptance checks

- Test successful leader/live child, ignored termination, immediate stop, interruption and failed final inspection; retain failures/unknowns and verify descendants terminate under bounded cleanup.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. The historical source retains local preflight failures and subsequent passing checks; their operating-system cause is unproven.

Publication transformation: Historical delivery/routing and payload-exclusion boilerplate removed; the retained-failure and unproven-cause qualification is preserved.

## TR-L2395 Historical package-completeness issue state

Source lines 2395–2396; context. SFB mapping: SFB-005. Earlier digest topics: 26.

The historical source assigns SFB-005 priority P2 and records acknowledgment with no fix then reported. It is an investigation-workflow requirement, not a source-inspected Sherlock defect.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Historical date metadata removed; status limitations retained.

## TR-L2397 Wrappers, engines and stale outputs do not prove complete cases

Source lines 2397–2398; requirement. SFB mapping: SFB-005. Earlier digest topics: 01, 06, 19.

A successful HTTP response and valid ZIP may deliver only a README pointing elsewhere. Different landing pages may converge on the same package. A repaired earlier-version archive, a final report and a public solver engine do not establish a complete final-version executable case. A published postprocessor warning about previous-run outputs also motivates an explicit input/run/output identity contract; no contaminated scientific run was demonstrated here.

Acceptance checks

- A valid response/archive/engine/report cannot establish a complete final-version executable case or valid current-run outputs.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2399 Synthetic redirected package and stale-run fixture

Source lines 2399–2400; requirement. SFB mapping: SFB-005. Earlier digest topics: 01, 06, 19.

Synthetic reproduction: A final-version landing page yields a small valid ZIP with only a README; the README redirects to an earlier-version package also linked by another site. Supply a generic engine repository without the case input manifest, and a results directory from a prior synthetic run.

Acceptance checks

- Exercise a README-only final wrapper redirecting to an earlier package, convergent landing pages, a generic engine missing case inputs and prior-run results.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2401 Acquisition ladder and bound input/run/output identity

Source lines 2401–2402; requirement. SFB mapping: SFB-005. Earlier digest topics: 01, 06, 19, 23.

Acceptance: Distinguish link located, response obtained, wrapper acquired, target package acquired, version crosswalk verified, dependencies complete, execution reproduced and physical validation. Deduplicate convergent origins; retain exact artifact hashes and unresolved version relationships. Engine availability must not imply case completeness. Postprocessing must bind outputs to a specific input/run manifest, flag stale or unmatched outputs without deleting preserved records, and retain failures as separate results.

Acceptance checks

- Keep located/wrapper/target/version/dependency/execution/physical-validation states distinct, deduplicate convergent origins and flag stale outputs without deleting them.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2403 Project settings, media lineage and archive path safety

Source lines 2403–2404; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 04, 05, 15.

Related SFB-002 supplement: Saved project frame duration/step settings are distinct from encoded presentation timestamps and original acquisition timing. Retain nested archive/project/media lineage, literal settings and verified software semantics separately. Use a synthetic archive with safe relative media and a duplicate Windows-absolute entry; never use the latter as an extraction destination or repeat personal path components in diagnostics. This adds scope to the existing measurement contract, not a request to launch untrusted projects.

Acceptance checks

- Preserve nested project/media lineage and literal settings versus verified timing semantics; never extract to a Windows-absolute alias or echo its personal components.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2405 Nullable clocks and ordinal-only screens

Source lines 2405–2421; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 08, 15.

A local native-media parser accepted absent stored PTS and relabeled decoder best-effort timestamps as PTS; it also failed on a final record without either field. Preserve nullable stored and decoder-estimated clocks separately, including genuine zero values. An ordinal-only source screen may continue under its own declared method, but must not clear a failed timing test or fill absent values from nominal frame rate. A nine-frame synthetic fixture with missing first/final fields now passes the local separation controls; present disagreement, nonmonotonic known values and fewer-than-eight inputs are rejected for the fixed eight-frame screen. Failure-output preservation remains a separate requirement. The historical local adapter still had limitations around partial stdout on timeout and oversized-output receipt handling; a narrow nullable-clock repair did not clear those limitations.

Acceptance checks

- Keep null and genuine zero clocks separate; ordinal-only methods cannot clear failed timing gates or fill nominal clocks; fixed eight-frame screens reject disagreement, bad monotonicity and insufficient inputs.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Historical routing and payload-exclusion boilerplate removed; the separate partial-stdout and oversized-receipt limitations are retained explicitly.

## TR-L2422 Decoder timestamps versus stored/exposure timing

Source lines 2422–2436; requirement. SFB mapping: SFB-002, SFB-005. Earlier digest topics: 15.

The earlier shorthand “stored PTS” must not imply literal container or camera storage merely because a decoder reports a value. A normal processing path may derive a present timestamp; an explicit generation path can fill absent values without authenticating exposure timing. Extend the synthetic fixture with distinct packet DTS, frame PTS, best-effort and generated-output fields, picture reordering and ordinal gaps. Acceptance: preserve raw nulls and field provenance; generated regularity cannot clear an original-clock gate; compare timestamp differences against ordinal gaps, not just successive known values. Source-slice hash equality and unique positional joins must not become proof of one packet per exposure.

Acceptance checks

- Keep packet DTS, frame PTS, best-effort and generated output provenance, reordering and ordinal gaps; neither generated regularity nor slice hashes establish original exposure timing.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2437 Checker-owned fields and safe intermediate arithmetic

Source lines 2437–2447; requirement. SFB mapping: SFB-002, SFB-004, SFB-005. Earlier digest topics: 18.

Related checker controls, under the existing completeness/exact-arithmetic fixture: a producer-selected empty comparison-field list must not make a changed baseline pass; independently enforce the full declared field set. Two individually safe integers can yield an unsafe subtraction or product; reject unsafe intermediates or use exact integer arithmetic. Both failures were reproduced synthetically and repaired in the local checker before its historical use. A passing check must list unchecked summary flags/status labels rather than silently certify the whole report. No product-wide fix or delivery is claimed.

Acceptance checks

- Reject producer-empty comparison sets and unsafe intermediate arithmetic; explicitly list unchecked flags/statuses rather than certify a whole report.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2448 SFB-001 adoption-verification heading

Source lines 2448–2449; context. SFB mapping: SFB-001. Earlier digest topics: 26.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: Historical section heading; substantive adoption state follows.

## TR-L2450 Superseding local full-charter adoption

Source lines 2450–2451; requirement. SFB mapping: SFB-001. Earlier digest topics: 26.

The source preserves the original SFB-001 inspection and early no-fix entries as history of the prior CLI. Its later project-owned local integration pins Sherlock 0.1.2 and uses the supported full-charter path. It reports exact preservation of the original charter text in structured scope, explicit constraint/review fields, and open questions retaining material-change conditions. This clears the local full-charter creation blocker; it does not amend the scientific charter or imply an accepted case finding.

Acceptance checks

- Keep the original charter text exact in structured scope, retain explicit review/constraints and open questions with material-change criteria; do not upgrade initialization to accepted findings.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: Private integration link, charter filename and real investigation question IDs/count replaced by generic roles. Software version and exact-preservation requirement retained.

## TR-L2452 Initialization authority and disabled downstream actions

Source lines 2452–2453; requirement. SFB mapping: SFB-001, SFB-003. Earlier digest topics: 24, 26.

Only charter and question state was initialized. Evidence files and research reports were not imported; no accepted findings, publication or canonical promotion was created. The local workbench acts as an agent and disables review acceptance, report generation and automatic report downloads. Its integration guide identifies the pinned runtime and verification commands; original charter bytes, prior work-package results and existing scientific outputs remain preserved.

Acceptance checks

- Charter/question initialization imports no evidence/reports and creates no accepted findings/publication/promotion; preserve pinned runtime checks and original scientific artifacts.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Original SFB-001 no-fix statements are historical; later supported local full-charter adoption clears that setup blocker without resolving other method contracts.

Publication transformation: Private work-package identifier generalized; technical authority and preservation boundaries unchanged.

## TR-L2454 SFB-001 adoption does not resolve specialist contracts

Source lines 2454–2455; requirement. SFB mapping: SFB-002, SFB-003, SFB-004, SFB-005. Earlier digest topics: 24, 26.

SFB-002 through SFB-005 and their domain-method requirements are not resolved by this adoption. Validated media measurement, calibration and uncertain event-time treatment, comparison/annotation contracts, resolved-package completeness and run identity still require their specific acceptance evidence. The command-based feedback lifecycle requested under SFB-003 is also not established by a local runtime launcher. Software initialization is distinct from method validation, human/expert review and scientific completion. No new feedback transmission or external disclosure accompanies this local entry.

Acceptance checks

- Require separate evidence for media/calibration/uncertain timing/comparison/annotation/package/run contracts and feedback lifecycle; distinguish initialization from method/human/scientific completion.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2456 Historical bridge-capability heading

Source lines 2456–2457; context. SFB mapping: SFB-003, SFB-005. Earlier digest topics: 26.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Historical bridge-capability statements must not override the later controlled synthetic export pilot; export does not establish two-way admission or scientific validation.

Publication transformation: Heading only; specific capabilities, tests and limits follow.

## TR-L2458 Assertion time, utterance position and enclosure namespace

Source lines 2458–2459; requirement. SFB mapping: SFB-004, SFB-005. Earlier digest topics: 03, 22.

A document dated after an event attributes a counterfactual opinion to an interviewee; a transcript has a segment-start clock but no per-utterance timestamps; a response encloses an index containing other request identifiers. Preserve assertion time, described event time, utterance position, document role and parent/enclosure identifiers separately. Synthetic acceptance: reject automatic conversion of later opinion into prior forecast, header time into every utterance's time, or an index-production response into disposition of a listed request. Keep challenged joins and reviewer narrowing auditable.

Acceptance checks

- Reject later-opinion-to-prior-warning, segment-header-to-every-utterance and index-response-to-listed-request-disposition promotions; retain challenged joins and review narrowing.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Historical bridge-capability statements must not override the later controlled synthetic export pilot; export does not establish two-way admission or scientific validation.

Publication transformation: Non-substantive historical routing and payload-exclusion boilerplate following the technical note is omitted; source claim-status limits remain in qualification.

## TR-L2460 Capability lead is not verified runtime support

Source lines 2460–2461; requirement. SFB mapping: SFB-003, SFB-005. Earlier digest topics: 25, 26.

The historical source records reported bridge availability as a capability lead pending verification, not a finding that the pinned runtime supports it or that scientific review occurred. No callable bridge tool was present in the tool inventory at that historical check. This inventory observation is not a current claim of absence: later interface/schema review is a subsequent source-log stage, and controlled synthetic export testing is publication-time context from SUP-01, neither of which alone establishes two-way admission or scientific validation.

Acceptance checks

- Record claimed bridge availability as a lead until the pinned runtime and callable interface are inspected; no scientific review follows merely from a capability report.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Historical bridge-capability statements must not override the later controlled synthetic export pilot; export does not establish two-way admission or scientific validation. Publication-time supersession context about the later export pilot is drawn from supplemental source SUP-01, not the feedback lines assigned to this unit.

Publication transformation: User/investigation routing context generalized. The historical inventory limit is not presented as current capability status.

## TR-L2462 Documented interoperability versus implemented workflow

Source lines 2462–2463; requirement. SFB mapping: SFB-003, SFB-005. Earlier digest topics: 25, 26.

The historical local review verified a documented external-engine/Faraday interoperability contract, defined a first synthetic acceptance test and preserved pinned-runtime/data-flow boundaries. At that stage the operational bridge and its tests remained unverified and no bridge was invoked. Publication-time update from SUP-01: subsequent controlled synthetic export testing is recorded separately; it does not establish two-way Sherlock admission or scientific validation.

Acceptance checks

- A documented external-engine contract and planned synthetic test cannot establish an invoked, tested operational bridge or validated scientific method.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Historical bridge-capability statements must not override the later controlled synthetic export pilot; export does not establish two-way admission or scientific validation. Publication-time supersession context about the later export pilot is drawn from supplemental source SUP-01, not the feedback lines assigned to this unit.

Publication transformation: Private capability-review link omitted. Historical schema-only/contract-stage limitation explicitly separated from later export tests.

## TR-L2464 Schema-only outcomes and preserved failed attempts

Source lines 2464–2465; requirement. SFB mapping: SFB-003, SFB-005. Earlier digest topics: 25, 26.

The historical interface audit found a format-1 receipt schema, example/test source and launcher skeleton. An isolated schema-only continuation reported 13 expected outcomes, zero failed/skipped and exit 0, with source pins unchanged and no engine or case transfer. Earlier dependency and harness failures were retained. The proposed two-engine scientific fixture was not run; operational translation and domain-review capability remained unverified then. These checks superseded the earlier lack of interface/schema-test inspection, not operational/scientific limits. Publication-time update from SUP-01: later controlled synthetic export testing is a further distinct stage, not evidence of two-way admission or scientific validation.

Acceptance checks

- Retain earlier dependency/harness failures; 13 expected outcomes with zero failures/skips and exit 0 establish only declared schema behavior, not authentication, translation or scientific review.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Historical bridge-capability statements must not override the later controlled synthetic export pilot; export does not establish two-way admission or scientific validation. Publication-time supersession context about the later export pilot is drawn from supplemental source SUP-01, not the feedback lines assigned to this unit.

Publication transformation: Private interface/schema verification links removed; synthetic outcome count and historical claim scope retained.

## TR-L2466 Bridge reliance preflight and audit-use contracts

Source lines 2466–2467; requirement. SFB mapping: SFB-003, SFB-005. Earlier digest topics: 23, 25, 26.

Before relying on the bridge, inspect its supported interface, version, actual implementation/tests, destination and data flow; compare the development checkout with the separately pinned local runtime. Do not silently upgrade the runtime, invoke a bridge, import/export case data or supply human-review attestations. Potential uses include auditing claim-to-source links, assumptions, disconfirming tests, uncertainty, calibration versus validation, and reproducibility. Each use needs a declared input, audit question, procedure/version and acceptance criteria.

Acceptance checks

- Inspect interface/version/implementation/tests/destination/dataflow and compare development with pinned runtime; no silent upgrade, invocation, data transfer or human attestation.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Historical bridge-capability statements must not override the later controlled synthetic export pilot; export does not establish two-way admission or scientific validation.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.

## TR-L2468 Minimal synthetic bridge use and review-output limits

Source lines 2468–2468; requirement. SFB mapping: SFB-003, SFB-005. Earlier digest topics: 04, 25, 26.

First validate an appropriate minimal synthetic workflow only after its execution and disclosure boundaries are understood. Any real material transfer must satisfy the repository's exact-payload/destination privacy rule. Preserve Faraday's suggestions as review outputs with provenance and unresolved objections; they are not new historical evidence, independent experiments, professional certification, accepted findings or authority to promote records. Any demonstrated integration friction should extend the existing SFB issues where applicable. This note itself initiates no bridge call or transmission.

Acceptance checks

- Understand execution/disclosure boundaries before a minimal synthetic workflow; real transfer requires exact-payload/destination approval and review suggestions remain non-authoritative outputs.

Qualification: Historical source requirement and reported local experience, not independently rerun by this transcription. A local workflow repair or acceptance proposal is not a demonstrated Sherlock defect, implementation, verified product fix or scientific finding; the listed checks are not claimed executed by this publication. Historical bridge-capability statements must not override the later controlled synthetic export pilot; export does not establish two-way admission or scientific validation.

Publication transformation: No substantive technical content omitted; purely typographic paragraph wrapping and heading formatting may be normalized.
