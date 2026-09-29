# Spring-curve search across released model inputs

The additional released numeric inputs contain no literal markers for the
LS-DYNA curve, table or function-definition families searched. This extends
the earlier file-coverage finding: the selected spring references LCD602 and
LCD803 remain unresolved in the inspected released numeric packages. It does
not establish that the definitions never existed or identify why applicable
definitions have not been located.[1][2]

This is working scientific research, not a solver reproduction, expert opinion,
procedural fact promotion or determination about intentional withholding.
Two independently implemented source readers agree across all 25,645 common
body/exclusion records; a fresh replay reproduces the complete comparison.
The two root passes and prior coverage reconciliation also pass.[1][4][6]

## Coverage and result

| Selected material | Bodies fully read | Read bytes | Result |
|---|---:|---:|---|
| Three June APDL inputs | 3 | 706,329 | Zero searched literal family markers |
| June thermal ZIP, non-PNG members | 25,362 | 477,264,192 | Zero searched literal family markers; one 328-byte all-NUL body |
| Remaining September inputs, SRC116–118 | 3 | 35,151,379 | Zero searched literal family markers |
| Total new scan | 25,368 | 513,121,900 | All selected bodies reached EOF |

The ZIP has 25,639 entries: 25,634 regular files and five directories.
Its 272 PNG bodies were excluded; their inventory records were retained.
The new scan covers 8,648,698 physical LF-delimited lines. All read bytes
are within the ASCII byte range, including the separately counted NUL bytes;
there is no basis for treating the all-NUL body as a usable text program.[1]

The search detects `*DEFINE_CURVE`, `*DEFINE_TABLE` and `*DEFINE_FUNCTION`
stems anywhere in the body, not just expected keyword positions. Comments,
quoted strings and suffix variants could therefore produce retained hits.
ASCII/UTF-8 and UTF-16LE/BE literal patterns were tested; line-leading flags
and encoding-pattern matches are kept distinct from valid source syntax.
No candidate explicit definition was identified by this literal search, so
this pass supplied no new selected curve/table for extraction or evaluation.[1][3]

All three APDL files and every non-PNG archive body match the preserved
June manifest hashes. The 25,365 June body identities, byte/hash/line/NUL
coverage and the three September uncompressed byte/hash/line totals also
reconcile with the earlier preserved source audits. The two new root result
objects agree completely. These checks authenticate the inspected local
bytes relative to the saved records, not their historical execution.[1][4]

The independent comparison covers 407,801 record fields with zero mismatches,
including identities, byte/hash/line coverage, declared exclusion metadata
and every common marker field. All 17 cross-reader synthetic fixtures and
29 comparison-mutation controls pass. These test implementation and comparison
behavior; they are not additional historical evidence or unperformed scans
of excluded image bodies.[6]

## What the expanded search resolves

The preceding selected-spring audit traced all 17 discrete candidates through
their supplied part, section and material cards. Parts820/821 reference
LCD602 and part859 references LCD803. Neither reference occurs in the 59
curves supplied in SRC119–121; independent full-stream checks there also
found no table/function-family definitions.[2]

The new pass closes the previously untested explicit-definition search in
the remaining September inputs and the already inventoried June numeric
package. A similarly numbered ANSYS node, material or parameter is not the
missing LS-DYNA curve. The thermal ZIP and its extracted copies are aliases,
not separate corroborating releases. No replacement curve was constructed
from another input or from a presumed force law.

The result is consequential for reproducibility: no applicable explicit table
was identified under this declared search, so the selected force-response
calculation remains unresolved.
It remains inappropriate to infer a spring's stiffness, capacity or historical
resistance merely from the presence of its material card. Conversely, this
local input limitation does not prove that the historical simulation lacked
those definitions or used an invalid law.

## Limits and next discriminating evidence

This is a byte-pattern search, not an interpreter for APDL or LS-DYNA. It
does not evaluate generated strings, external calls, runtime export, binary
restart state or other encodings. The earlier thermal-transfer audit did
not authenticate a complete generating program or historical run. Its lexical
findings cannot be upgraded into proof that no such program existed.[5]

PNG pixels, PDF/presentation bodies and possible embedded attachments were
not searched for runnable definitions. Nor does the preserved manifest
establish every byte delivered historically, every agency-held input, or the
contents of unavailable files. These are explicit coverage limits, not
positive evidence for either an innocent or deliberate explanation.

The highest-value next evidence is the complete applicable input/include/
restart package with a typed crosswalk for LCD602/803, linked to the actual
executable build and run. Its D3HSP/input diagnostics and discrete-force/
displacement histories would help determine how the references were resolved
and used. A newly located candidate still needs source/version authentication,
full definition extraction and the previously declared independent arithmetic
checks before it can support a physical inference.[2][3]

No collapse-cause ranking changes through this search. It does not identify
an initiating failure, time-dependent support loss, deliberate intervention
or intent. The next investigation step should use this now-specific missing
dependency rather than repeating the same finite literal search.

## Claim ledger

| Claim | Type and support | Strongest alternative / falsifier | Permitted strength |
|---|---|---|---|
| The selected new bodies contain no searched literal definition stems. | Derived complete-byte scan, independently reproduced; source hashes and full common-field coverage checked.[1][4][6] | A reproducible missed marker or coverage/hash mismatch would defeat the claim. | Strong within the declared literal/byte scope, not general-language absence. |
| LCD602/803 remain unresolved in the inspected released numeric packages. | Typed prior consumer audit plus the expanded search.[1][2] | An applicable, authenticated explicit or generated definition and its package linkage would resolve the dependency. | Supported as a scoped reproducibility limitation, not universal absence. |
| These missing tables demonstrate historical model invalidity or concealment. | Not established by this search. | Other run files, generation or restart state could supply the definitions; intent requires separate affirmative evidence. | Unsupported from these results alone. |

## Sources

1. [Root scan](root-01.json), [complete repeat](root-02.json),
   [prospective protocol](PROTOCOL.md), and [byte conventions](SCAN-CONVENTIONS.md).
   Sources: preserved June production, linked through SRC084, manifest SHA256
   `30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf`;
   SRC085 thermal ZIP and supplementary SRC116–118. Per-body hashes and locators
   are retained without exporting original comments, metadata or embedded paths.
2. [Completed selected-spring audit](../c79-casea-spring-audit/report.md)
   and its [independent definition inventory](../c79-casea-spring-audit/independent-definition-presence01.json).
3. [Primary-manual field review](../c79-casea-spring-audit/spring-manual-review.md)
   and [declared arithmetic protocol](../c79-casea-spring-audit/ARITHMETIC-PROTOCOL.md).
   These distinguish curve/table identity, supplied points and runtime behavior.
4. [Complete saved-coverage reconciliation](coverage-check01.json), using
   the [earlier June full-body result](../thermal-transfer-crosswalk/run01.json).
5. [Thermal-source transfer crosswalk](../thermal-transfer-crosswalk/report.md)
   and [verification limits](../thermal-transfer-crosswalk/validation.md).
6. [Independent source scan](independent-scan01.json),
   [complete comparison](independent-comparison01.json),
   [fresh root replay](independent-comparison-root01.json), and
   [independent review](independent-review.md). Alias padding and zero-/one-based
   archive ordinals are explicitly reconciled; independent-only fields retain
   their separate verification status.
