> **Historical research:** This document reports a prior source review, not a current instruction or new model run. Missing sources and run artifacts are identified; see the [publication note](../README.md).

# Grade-label correction receipt

2026-09-10. Focused pre-integration correction requested by parent review. No new source work, network, findings, source pins or empirical judgment added. The active [claim ledger](claim-ledger.md) now uses the evidence-falsification skill's A–E meanings instead of its earlier nonstandard B/U legend.

A labels only verified publication content here; C labels materially assumption-dependent inference; D preserves unresolved historical/empirical propositions; E labels unsupported or contradicted overclaims. In particular, lack of an underlying equipment record is not treated as evidence that the equipment did not exist. Mixed propositions now distinguish a conditional inference, unresolved event fact, and an overstatement that the fact was measured or proven. B retains its standard strongly-supported meaning but is not assigned in this bounded review.

The prior ledger and receipts were copied byte-for-byte before editing:

| Preserved file | SHA-256 |
| --- | --- |
| [claim-ledger.pre-grade-revision.md](claim-ledger.pre-grade-revision.md) | `aa9485cb759b750077042fe605d8963c4fc595c5f72d4a7a8d435fef7911436c` |
| source-manifest.pre-grade-revision.json (historical local reference `source-manifest.pre-grade-revision.json`; not included here) | `47f09c54c8b56e33196744a3ea53ba5630e4f330bfa93b1b85d122781cec3fe2` |
| verification.pre-grade-revision.json (historical local reference `verification.pre-grade-revision.json`; not included here) | `f4825c97fa2d97783bddf9c2599512ee20f1e75bc7a087dbc0bf78e20efedd3f` |

The pre-revision manifest's `claim-ledger.md` hash refers to the preserved pre-revision ledger, not the new active ledger. Its other original entries remain unchanged. The current `source-manifest.json` and `verification.json` are regenerated final receipts and include the preserved attestation files plus this explanation. Source PDFs, rendered pages, page selections, render receipts, report, source log and verification script are unchanged. No completed extraction or render was rerun.

## Intermediate receipt coverage race

The first grade-correction regeneration returned passing selected-page/link/source checks and a 98-entry manifest. Six parent-owned independent-reproduction PNGs had temporarily appeared in `derivatives-root-check/` while the manifest scanned this directory. The immediate independent rehash then failed with `FileNotFoundError` for its physical-105 entry after the parent moved those outputs intact to the separate parent-owned `nist-root-reproduction/` directory. Thus the intermediate manifest must not be represented as a verified current 98-file snapshot. No child source or reviewed image failed a content check.

Preserved intermediate outputs: source-manifest.transient-root-check.json (historical local reference `source-manifest.transient-root-check.json`; not included here) and verification.transient-root-check.json (historical local reference `verification.transient-root-check.json`; not included here). They retain the original generated result and now-stale paths. The parent confirmed no further writes to this child directory before final regeneration. The final receipt uses the stable child scope, while preserving this failed rehash and both earlier attestations as history. No new source reading or independent visual-coverage claim arises from the parent's six temporary files.
