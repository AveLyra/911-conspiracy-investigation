# Independent metadata verification

2026-09-24. Separate computational checker; research only. The clarified
[protocol](PROTOCOL.md) controls scope. This is an independently implemented
DOM comparison, not independent historical evidence, human review or physical
validation. No raw project text, saved value, media or new measurement is
included here.

## Result

**Pass:** the independent DOM oracle exactly matches every declared field in
both producer products, and their JSON bytes are identical. Checked coverage:
1,769 parsed elements, 3,220 parsed attributes, eight direct-track PointMass
owners plus the root owner, 138 leaf strings, zero structured strings and zero
hits for the declared stems in name/class attributes. Those zero counts do
not concern searches inside the withheld string values, XML comments/PIs,
other saved versions or outside records.

The comparison covers the complete element/text/attribute ledger, selected
owner/direct-property occurrence records, target-field states, item/object/PM
ordinals, every stem-hit record, both string subsets, counts, allowlists,
source pins and exclusions. Type-sensitive canonical comparison prevents a
boolean from silently equating to an integer. The original producer products
are additionally required to have identical bytes. Current procedure/source
pins and producer receipt claims were checked before and after the run.

## Actual commands and receipts

The following commands were run from
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`:

```sh
python3 -B research/sherlock-wtc7-investigation/tilted-construction-record/test_verify_locator.py --out verifier-controls01
python3 -B research/sherlock-wtc7-investigation/tilted-construction-record/verify_locator.py --out verifier01 --reviewed-verifier-sha256 ca68890d194bde7e3595103bfa411f11b7605109e3737493dc0fd53b75d73299
```

Both completed successfully under narrowly scoped worktree-write approval.
The historical command was executed only after root's complete code review,
passing synthetic replay and express historical-read clearance. It returned
exit 0 and `pass_independent_dom_exact_metadata_and_repeat_check`, with the
counts above. Python for this checker's controls and historical run was
**3.14.0**.

The first synthetic receipt command in the normal sandbox returned the generic
`synthetic_controls_operation_failed` and created no output directory. A
direct synthetic-only run then passed all 17 tests; the same receipt command
under scoped approval passed and saved its receipt. No failed historical
source run occurred. An earlier 15-test development run also passed before
the two final controls were added; it is not substituted for the final gate.

| Artifact | SHA-256 |
|---|---|
| `verify_locator.py` | `ca68890d194bde7e3595103bfa411f11b7605109e3737493dc0fd53b75d73299` |
| `test_verify_locator.py` | `db2447d9b5129de7f6aa88f25eb1585ca2505bc2e67c084531b30a2e997440de` |
| `verifier-controls01/receipt.json` | `cf4770b3bf3594cbbc36d713350f2652c1f14a057e6124d10b3ab6b9f652213d` |
| `verifier01/input-receipt.json` | `fd9ac39adb7d0282f1309f9a38e175cf02cd6ef88e66cfaae74a894dde02bf65` |
| `verifier01/verification.json` | `faef2ce4ea53a8a9e8b170e8621cf9e61f48eeae48c2321fa4346db956e9e0ca` |
| Root `verifier-controls-root01/receipt.json` | `8e2400b6d5865bafd953bd0adc7ebb32f482f71cee9bfb7ea4c224a9cbb19b14` |
| Root `verifier02/verification.json` | `feff5818d860f83adf07e5d1a69b2da83e736b26cf8ad2d7eab9faa466d97e27` |

Root independently executed the 17-control replay and historical `verifier02`
run and reported success. This checker then read/hash-checked their saved
receipts and compared them with its own; it did not execute `verifier02`.
`diff -u` showed that **the only difference in each receipt pair is the Python
version**, 3.14.0 versus root's **3.12.14**. It is not an output-directory
difference. Both control receipts record 17 tests, zero failures/errors and
unchanged inputs. Both historical receipts give the same counts, pins and
pass status. The producer's two runs used Python 3.12.14.

Both producer `locator.json` files are 6,276,196 bytes with SHA-256
`bf47dd03fd41205794d1bce0d6b9893f773d2ff2aed6382d4b91b11d33ce4f6c`.
Both producer final receipts have SHA-256
`586ca63e0b4c737a0b04589979e8b0d459425a2cd00aa37dfac920aef8e35717`.

## Controls, source identity and dependencies

All 17 final synthetic tests passed, including direct/nested ownership and
every PM ordinal, duplicate/missing/whitespace/structured field states,
mixed text/CDATA and child tails, comments/PIs exclusion, namespace Clark-name
normalization, arbitrary identifier/value non-disclosure, global leaf-string
coverage, substring leads versus literal fields, malformed/envelope/depth
guards, duplicate/nonfinite JSON rejection, archive path/symlink/size guards,
wrong source/procedure pins, exclusive output refusal, sanitized CLI errors
and deliberate corruptions of each material comparison family. A separately
reconstructed synthetic fixture exactly matches the producer's pinned
synthetic product without importing its implementation.

The independent loader rechecked the same preserved public archive chain:

- Parent ZIP: `c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189`.
- Named nested TRZ: `7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552`.
- Nested TRK, zero-based entry 4: `babf332bd340c1e902870f14d4370eab4f3a54de388ce06c1ca85ae222b1b5da`.
- Clarified protocol: `47d55648820416cb92d35d562335a6332a8eff490c9a3e861ecda3a54cd6e030`.

The oracle uses stdlib `minidom` and does not import or execute the producer or
its helper. The producer uses ElementTree. Both nevertheless share the same
source bytes, declared schema/text semantics and Python/XML ecosystem;
different frontends are not a wholly independent parser stack. The synthetic
fixture serializer uses ElementTree only to reproduce fixture bytes, not to
parse the historical source. No historical Tracker executable was run.

The DOM projection deliberately follows the declared parsed representation:
element-child paths; coalesced Text/CDATA; separate leading text and child
tails; immediate text excluding descendants; namespace-expanded names;
and no comment/PI inventory. Namespace declarations omitted by ElementTree
are not introduced as additional attributes. This is not a lexical-byte
inventory of every possible documentation channel.

## Claim ceiling

This verifies the locator's bounded metadata accounting and its preservation
of source identity relative to held bytes. It does not read or authenticate
the meaning of the withheld strings, establish the historical marking or
editing method, demonstrate absence of documentation everywhere, or validate
the saved positions, publication version, physical scale or collapse cause.
The strongest competing possibility remains that a method was unsaved,
stored differently or documented elsewhere, or that the analyst selected a
different observable not requiring a persistent step-foot point.

Only the assigned verifier, synthetic controls, receipts and this working
note were created by this lane. Raw/main files, prior freezes, producer
products and accepted engines remain unchanged. No acquisition, plaintext
disclosure, promotion, legal edit, commit or push occurred. The evidence-audit,
source-of-truth and development-verification skills supplied the explicit
provenance, privacy, negative-evidence and reproducibility limits.
