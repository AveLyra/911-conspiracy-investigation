# Sherlock feedback preservation audit — October 9, 2026

**Outcome:** the received 27-item batch does not itself establish complete preservation of the original requirements. Concrete qualifications and tests are absent or only broadly represented. A local technical-detail supplement is prepared; **at initial preparation, nothing from this audit had been sent, committed or pushed**.

## Subsequent repository publication

The user subsequently authorized documentation, commit and push to the private and public repositories. [PUBLICATION.md](PUBLICATION.md) controls that later publication status; the original preparation statements above and frozen receipts below remain historical. Repository publication is not a new message or acknowledgment by the Sherlock task. The selected public addendum does not include private source paths or receipt records.

## Scope and acceptance

Compare the pinned original feedback, exact transmitted batch and saved acknowledgment; preserve technical detail; keep source-to-message-to-acknowledgment links locally. No investigation source acquisition, new scientific analysis, legal drafting, product implementation or source-record rewriting is authorized here.

Acceptance for preservation is complete accounting of the source blocks and exact retention of selected technical bundles, with every locator/receipt-identifier substitution logged. This is **not** a claim that topic matching proves clause-by-clause semantic equivalence to the older digest. Acceptance for delivery requires separate authorization of the exact new payload, an actual send receipt and verification of a detail-level recipient acknowledgment; those steps remain pending.

## Results

- The current feedback source has 2,468 lines and reconstructs the exact 2,455-line pre-delivery source whose hash appears in the prior receipt.
- All 272 nonblank source blocks are accounted for: 225 technical bundles retained; 47 administrative/heading/status/resolved-item blocks explicitly listed for non-retransmission.
- All 27 sent item IDs and all 27 corresponding recipient-log item IDs are present exactly once. This verifies item-level receipt, not preservation of every source clause.
- [Detailed comparison](requirement-gap-review.md) records 24 selected comparisons, including counterexamples to overclaiming a gap: actual resampling-kernel exclusion is already explicit in sent item 16, and common-support/no-refitting is already explicit there too.
- The [technical annex](technical-annex.txt) retains complete technical bundles with stable FBR identifiers. It is approximately 217 kB because tests and qualifications have not been condensed again. It is not the whole investigation record; nevertheless, size and safe content require exact-payload review before sending.

The strongest limitation on these results is that **225 is a bundle count, not a count of distinct atomic requirements**, and the 24 detailed comparisons are not an exhaustive clause-level omission census. The complete selected source text is retained precisely so this limitation does not silently delete remaining requirements. The annex is a preservation solution, not certification of a finished deduplicated implementation specification.

## Review and delivery boundary

Proposed recipient: **Define Phase 0 invariants**, the existing Sherlock task. Proposed payload is exactly [supplement-cover.txt](supplement-cover.txt) plus [technical-annex.txt](technical-annex.txt). The cover binds the annex hash and requests intake/triage only. Review excludes investigation documents, case links, source identifiers, private paths, personal contact data and original receipt IDs from the proposed payload; a textual screen supplements but does not substitute for human content review.

Local-only: source crosswalks, detailed comparison, source hashes/locators, prior delivery records and acknowledgment links. Do not transmit the whole directory. Do not append these drafts to the parent feedback log as though delivered. After authorized delivery, save exact payload/receipt, check the recipient's preserved detailed text, and append the new receipt and detail acknowledgment to the local traceability record. Reopening a chat is not delivery; a receipt is not a fix.

## Files and authority

- [source-crosswalk.csv](source-crosswalk.csv) / [JSON](source-crosswalk.json): every source block, inclusion/exclusion reason, original and pre-delivery locators, source/annex hashes and topic links. JSON contains local paths and is not an outbound attachment.
- [sent-item-crosswalk.json](sent-item-crosswalk.json): exact sent item text, hash and recipient-log disposition/pointer. Scope remains item-level.
- [traceability.json](traceability.json): original bundle → older sent items → older acknowledgment → draft supplement, with new delivery/acknowledgment fields explicitly null.
- [manifest.json](manifest.json): pinned inputs, source reconstruction and preservation scope.
- [verification.json](verification.json): actually executed preservation checks and negative controls. These are audit checks, not Sherlock feature tests.
- [findings.json](findings.json): structured form of the 24 detailed comparisons.

The original source and destination log remain authoritative for what was written and acknowledged. This audit does not change their history or any case pleading. Resolved SFB-001 material remains in the original source and destination's existing SFB-001 section; it is not reopened or certified anew.

## Method and limitations

The source and sent batch were read; the pre-delivery version was reconstructed from the documented routing/delivery additions and verified against its earlier receipt hash. Source paragraphs were explicitly classified rather than deleted by keyword. Technical text was retained verbatim except five logged changes: one case-source label generalized, one link destination removed while retaining its label, and three historical receipt UUIDs replaced. Those redactions are not implementation requirements. Historical routing boilerplate remains clearly marked as historical within retained bundles.

The builder uses standard Ruby libraries only and does not execute source notes, import Sherlock or contact a provider. A separate verifier compares generated artifacts back to pinned inputs and exercises in-memory missing-row, altered-text, duplicate-ID and annex-tampering controls. Deterministic rerun equality is checked for generated preservation files. Exact commands and observed results are in verification.json.

The evidence-falsification-auditor and source-of-truth-guardian skills shaped the distinction between receipt, content retention, semantic equivalence and verified implementation. repo-orchestrator kept this bounded work separate from the active investigation. The write-page guidance was used for readable local documentation in the established repository, with no cloud Page or disclosure.
