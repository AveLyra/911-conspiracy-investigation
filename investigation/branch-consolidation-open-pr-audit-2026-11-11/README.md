# Open pull requests and public main: bounded audit

November 11, 2026. GitHub listed 11 open PRs: #1–6 and #8–12. This is a file-identity and ancestry screen, not a full scientific or sensitive-data review. No PR or branch was closed, merged, deleted or modified.

The previous public consolidation [explicitly copied selected source files without merging source branches](../branch-consolidation-public-refs-2026-11-10/README.md). Therefore copied research can exist on main while its original PR remains open and Git reports the head as unmerged. Some PRs target another research branch rather than main; merge status against those bases differs from inclusion in main.

| PR | File comparison to main | Ancestry of head in main | Caveat |
| --- | --- | --- | --- |
| [#12](https://github.com/AveLyra/911-conspiracy-investigation/pull/12) | 13 of 13 changed head files byte-identical | No | Compared with its declared research-branch base. |
| [#11](https://github.com/AveLyra/911-conspiracy-investigation/pull/11) | 19 of 19 identical | No | Compared with its declared research-branch base. |
| [#10](https://github.com/AveLyra/911-conspiracy-investigation/pull/10) | 9 of 9 identical | Yes | Draft targets another branch. |
| [#9](https://github.com/AveLyra/911-conspiracy-investigation/pull/9) | 10 of 10 identical | Yes | Targets another branch. |
| [#8](https://github.com/AveLyra/911-conspiracy-investigation/pull/8) | 34 of 34 identical | No | Compared from merge-base with main. |
| [#6](https://github.com/AveLyra/911-conspiracy-investigation/pull/6) | 7 of 7 identical | No | Compared from merge-base with main. |
| [#5](https://github.com/AveLyra/911-conspiracy-investigation/pull/5) | 57 of 57 identical | No | Compared with its declared research-branch base. |
| [#4](https://github.com/AveLyra/911-conspiracy-investigation/pull/4) | 84 identical, 1 different, 15 absent | No | Compared from merge-base with main; includes inherited changes, not necessarily unique to this PR. |
| [#3](https://github.com/AveLyra/911-conspiracy-investigation/pull/3) | 25 identical, 1 different, 15 absent | No | Compared from merge-base with main; overlaps #4's inherited files. |
| [#2](https://github.com/AveLyra/911-conspiracy-investigation/pull/2) | 14 identical, 1 different, 1 absent | No | Compared from merge-base with main. |
| [#1](https://github.com/AveLyra/911-conspiracy-investigation/pull/1) | 1 different | No | The current master list has evolved; difference alone does not establish missing content. |

Counts compare extant paths in each head, so they do not audit deletions, rename semantics, contents copied elsewhere under a different path, or later corrections. Main was `c55bb83c29b75ad72360d5d2bfbe87bd9d70ea1b` for this screen. The 15 missing paths in #3 and #4 overlap: 14 files under `telephone-ua175-summary-review-2026-10-28` and one archived FAA PDF path. Their absence from main at those paths does not establish that they were not preserved on a public branch, in another form, or locally. Their provenance, sensitivity, LFS handling and replacement by later research must be reviewed before any integration or closure. The different FAA README and master list likewise require semantic comparison rather than overwriting the newer files.

For follow-up, inspect the per-PR patch and preservation manifests, verify any proposed material's disclosure eligibility, then record whether each change is incorporated, superseded or still needs integration. Open PRs can be closed without deleting source branches, but no closure should represent them as merged unless that is true.

## Reconciliation after the screen

The fourteen-file [Flight 175 summary review](../broader-evidence/telephone-ua175-summary-review-2026-10-28/README.md) is now copied byte-for-byte from public PR #3 head `9ea289e6e2d7ec284eff654ed96f52364b91edb6`; it was inherited by #4. The package contains dated analyses, source pins and scripts, not the underlying hosted images; it is retained as historical research and its factual claims were not newly verified during this file reconciliation. Source-sensitive identifiers and raw images are described as excluded in the source review; an automated scan for email addresses, private-key language and local user paths was also run on the copied text, without matches. This limited screen is not an exhaustive privacy or copyright audit.

For #2, the missing FAA PDF was a 132-byte Git LFS pointer in the public source history. The current main [FAA review](../broader-evidence/faa-investigation-followup-order-2026-10-28/README.md) expressly states its payload is not included; that qualification is retained rather than presenting a pointer as an accessible document. The review's newer wording and LFS exclusion explain its differences from the old PR head. Original public branch history remains preserved; payload availability was not verified and no LFS data was uploaded.

For #1, the historical [175-entry register](../wtc7/master-lead-register-2026-10-26-outstanding/MASTER-LIST.md), structured register and [source review](../broader-evidence/outstanding-records-verification-2026-10-26/REPORT.md) already exist on main. Their direct link is restored in the current master list; the older root navigation is not substituted for the updated list.

The other seven PRs' compared head files already match main. After publication of this reconciliation, the 11 PRs are candidates for closure as accounted-for work, not as merged commits. Closure does not delete their branches or establish that omitted LFS content is publicly accessible. PR status on GitHub, rather than this dated audit, is authoritative.
