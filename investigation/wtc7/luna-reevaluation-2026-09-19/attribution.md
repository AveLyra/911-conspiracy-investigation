# Attribution and preservation ledger

2026-09-19. Local research audit; not a model-quality inference. [Scope](SCOPE.md), [dispositions](report.md), [verification](verification.md).

## Method and limit

An independent attribution reviewer matched local task model metadata to successful edit receipts and replayed those patches in memory. Eleven complete new files match the resulting bytes; one additional artifact is an insertion in an existing status file. A failed validation-file patch was excluded. Root checked the artifact hashes separately. Titles below are the actual task titles, not reconstructed descriptions.

- **Estimate NIST collapse progress**, task `01a0a83b-23a1-7a72-b289-e1f8bb32fe01`: GPT-5.6 Luna, low reasoning; seven synthesis files, September 16, 04:36–04:38 UTC.
- **Investigate 9/11 conspiracy**, task `01a06c9d-b156-7f02-8da7-d7e2b2abc17a`: GPT-5.6 Luna, low reasoning; the two contracting files, closeout, status insertion, and Faraday note, September 16, 06:34–15:21 UTC.
- **Map FOIA case-management needs**, task `01a0b5ff-cdd4-7092-aacb-989d7d271428`: Luna metadata was found, but no file edits were identified in the inspected history. Legal chat text is not audited here.
- **Evaluate NIST collapse explanation**: no Luna-authored file edits identified in the inspected local history. Existing underlying scientific reports are not attributed to Luna merely because Luna summarized them.

Receipt anchors, retained locally rather than copied into the audit: archived rollout `rollout-2026-09-15T23-20-43-01a0a83b-23a1-7a72-b289-e1f8bb32fe01.jsonl`, edit records 184, 224, 245, 272, 279 (259 failed); September 16 rollout `rollout-2026-09-16T02-00-20-01a06c9d-b156-7f02-8da7-d7e2b2abc17a_01a0a8cd-485e-7171-9ca7-1633852e886c.jsonl`, edit records 89, 145, 253, 260, 302. These are provenance checks, not scientific corroboration.

This is the set of twelve traceable investigation artifacts found in the documented search, not proof that every Luna conversation, legal draft or past edit everywhere has been located. Other dirty files remain unattributed and untouched.

## Original hashes

Paths in the first seven rows are relative to `/Users/admin/docs/911/research/sherlock-wtc7-investigation/synthesis-packet/`. Paths in the next four are relative to `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/`.

| Artifact | Original SHA-256 | Attribution scope |
|---|---|---|
| `README.md` | `4a66d971a284cfc4ff0fa000dc07d3a4bfff7335a391ded51726f86777e1798d` | Complete file |
| `inventory.md` | `986b285b838447125cccb815cb4feac83a77aa8c5c444194f69c5f4dfa9fdab0` | Complete file |
| `crosswalk.md` | `048c07165d278fc8ef64ed26e2db4d75878093b85428fea635c6187859d9314f` | Complete file |
| `quantitative-results.md` | `b3e75c8b0c4dbc959a387b54c9dc9fd86a621024c8ee636108807c10e822772b` | Complete file |
| `open-issues.md` | `ba82f8b030cfe10ba466e7521a3d00319a144f50748ccce720afe607c54c22dc` | Complete file |
| `final-outline.md` | `b814a65fad939d71549a4fd276e52ca7cee5f5dd2a4d7003eb5b266d3a83b943` | Complete file |
| `validation.md` | `b0336b08a965b4e15141d2b55844f5615cefba486f2b8541cbc8575735b7c590` | Complete file |
| `contracting-access-custody-audit/README.md` | `037691eef77eb9ce14cf35d5db795695d5baadd55785a1bb6b8b25d1b7c38444` | Complete file |
| `contracting-access-custody-audit/technical-review-update.md` | `70ee769d60bbd70b7f3c73cfc76cd8de71ecdd7c0c7bbfc27784511906c86815` | Complete file |
| `luna-light-provisional-closeout-2026-09-16.md` | `b1219ff52853c1caf7a1e5a83ce038cf8c60f9ca2f90df50aa0ba0bf62e0ba46` | Complete file |
| `STATUS.md` | `8131a5083550eed04aa34f6555639e2adf312c31116f84057fe9a577d16dfe24` | Only the top September 16 provisional-closeout paragraph and adjacent blank line; hash is the entire pre-update file, not sole Luna authorship |

Twelfth artifact: `/Users/admin/docs/911-worktrees/faraday-wtc7-model-compare/review/luna-light-audit-2026-09-16.md`, SHA-256 `46af0f8ff706d7e32e79926c426dfed18b7182dd51c91747dcbb927527e0eec4`; complete file.

All eleven standalone originals are preserved unchanged. The current worktree status paragraph is superseded explicitly, not erased from the historical closeout or this ledger. Main and the Faraday checkout remain read-only in this audit.
