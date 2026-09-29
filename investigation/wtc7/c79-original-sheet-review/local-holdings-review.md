# Local original-sheet holdings and navigation review

2026-09-13. Retrospective handoff of two completed, bounded read-only searches;
not a new holdings scan, PDF review or source acquisition. The parent requested
this durable record after the findings were returned. Research only, under
[PROTOCOL](PROTOCOL.md) and the investigation charter.

## State and authority

The dedicated worktree is `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`,
branch `research/sherlock-wtc7-investigation`, HEAD
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`. At handoff preparation the unit is
untracked intentional WIP; its scoped Git history has no earlier commit.
The current protocol hash is
`804acf3e9075100e631abe962daa5cad957e6a3ac1479fb591251d081f61d84a`.
This note is the only authorized write by this arm. No commit or push.

Main AGENTS.md, WORKFLOW.md and START-HERE.md, the worktree CHARTER, current
member/detail report and latest STATUS handoff were read for the original local
search. Main authority/research files are read-only dependencies. The sparse
worktree is not a complete mirror; a missing worktree file is not repository
or source absence. Source-of-truth and evidence-audit controls keep navigation
claims separate from inspected originals; the context-distiller skill governs
this handoff, not new scientific findings.

## Completed search and finite coverage

Permitted holdings roots were exactly:

1. `/Users/admin/docs/911/authority/`
2. `/Users/admin/docs/911/research/`
3. `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/`

The earlier ordinary `rg --files` listing across those roots returned **7,169
paths**. A later `rg --files -uu` listing returned **11,080 paths**, including
ignored/hidden paths. These are earlier observed path counts, not fresh counts
at this note's save time, unique-document counts, or inspected-content counts.
Copies and derivatives were not treated as independent witnesses. No complete
inventory snapshot was saved by this arm; the counts and commands were returned
in the tool record. This handoff did not rerun the holdings scan.

| Pass | Filename/navigation terms | Coverage and result |
|---|---|---|
| Original-sheet names | Frankel; Cantor; 1091, 9114, 9102; A2001/A1370 with separator variants; S-8/S-8-10; E12/13; 11-209/12-009 | Both ordinary and ignored/hidden filename passes found no matching requested sheet or FOIA-archive filename. No archive members were searched. |
| Alternate naming/navigation | drawing; erection; shop detail/plan; structural plan/drawing; public FOIA; UAF/Hulsey; structural reevaluation; technical README/source-index/catalog/review names | Located existing report/review references and a preserved UAF presentation; no complete original-sheet copy was identified. Selected existing public navigation records were read, not a broad content search. |
| Salvarinas paper | Salvarinas; fabrication; construction aspects; CISC/CSCC1986; structural engineering conference; broader 1986/CISC/CSCC/proceedings/Seven World Trade Center filename forms | No matching standalone publication filename. Targeted checks of the 13 existing navigation/review files below did not identify an acquired full-paper copy/version. |

The precise Salvarinas target was John J. Salvarinas, *Seven World Trade Center,
New York, Fabrication and Construction Aspects*, Canadian Structural Engineering
Conference Proceedings (1986), pp. 11-1–11-44. That bibliographic target came from
the task; this local pass did not authenticate a title page or edition.

The **13-file targeted scope** applies specifically to the Salvarinas navigation
follow-up, not every file read in the earlier original-sheet task. It comprised:

- Main `authority/source-index.md` and `authority/independent/uaf-wtc7-notes.md`.
- Main `research/nist-claim-strain-audit.md` and `research/wtc7-collapse-evaluation-synthesis.md`.
- Main `research/sherlock-wtc7-investigation/structural-chain-source-audit.md`
  and `structural-chain-source-audit/visual-review-v1.md`.
- Main `research/sherlock-wtc7-investigation/wp0/inventory.json` and
  `wp0/provenance-map.json`.
- Main `research/sherlock-wtc7-investigation/model-access-audit/source-catalog.json`.
- Worktree `research/sherlock-wtc7-investigation/c79-member-detail-crosswalk/drawing-source-review.md`
  and `c79-member-detail-crosswalk/report.md`.
- Worktree `research/sherlock-wtc7-investigation/c79-contact-geometry/source-crosswalk-review.md`
  and `c79-restraint-audit/source-review.md`.

An additional attempted `c79-member-detail-crosswalk/source-review.md` path did
not exist; it is excluded from the 13 and supplied no evidence. Targeted term
checks were not full rereads of all 13 files.

**Scope deviation:** The initial setup control/report-name filename listing
traversed the main repository root as well as named investigation paths, beyond
the intended holdings-listing roots. It returned an archive control-file path;
no archive content was opened. This was reported to the parent. Subsequent
holdings inventories were confined to the three roots above. No raw details
from that incidental filename listing are reproduced here, and it is not
counted as an expanded source-content review or privacy clearance.

## Results: originals versus references

| Located item | What this arm established | What it does not establish |
|---|---|---|
| [Drawing-source review](../c79-member-detail-crosswalk/drawing-source-review.md), lines 94–99 and 113–124 at the earlier read | Navigation identifies S-8/S-8-10/E12/13; public FOIA archive names `NIST_WTC7_FOIA_11-209.zip` and `NIST_WTC7_FOIA_12-009.zip`; Frankel 1091/9114/9102 and A2001/A1370 leads | No bulk archive or complete original sheet was inspected by this arm. Publisher-attributed identifiers are not authenticated installed-floor details. |
| [Preserved UAF presentation](../c79-member-detail-crosswalk/drawing-public-sources/uaf-progress-2017.pdf) and its [source README](../c79-member-detail-crosswalk/drawing-public-sources/README.md) | Existing metadata identifies the 2017 progress presentation. The review describes page 39's Frankel 9114/A2001 detail depiction and page 16's Salvarinas/Bailey-attributed plan excerpt | This arm did not open or visually inspect the PDF. Neither the cited depiction nor excerpt is a complete original drawing sheet or the full 1986 Salvarinas paper. |
| [Older public model-access catalog](/Users/admin/docs/911/research/sherlock-wtc7-investigation/model-access-audit/source-catalog.json), entry for `sources/uaf-direct-download.zip`, and [saved inspection](/Users/admin/docs/911/research/sherlock-wtc7-investigation/model-access-audit/run-v1/inspection.json), `uaf_wrapper` | The earlier search log reports an 834-byte README wrapper; the saved inspection records one `readme.txt` member, not the advertised full dataset | The ZIP was not opened or relisted here. Its filename is not evidence that the full model/drawing collection is locally preserved. Saved earlier member metadata is not a fresh archive check. |
| Main NIST report filenames and existing technical reviews | Public report holdings and derivative references are available as read-only dependencies | Their availability does not establish possession of separately named original sheets. No NIST PDF contents were newly read in these searches. |
| Salvarinas full paper | No acquired complete copy/version was located within this filename/navigation scope; the sole relevant selected-note hit was the UAF page-16 attribution above | Not proof of nonexistence, lack of public availability, or absence inside uninspected collections or differently named files. |

The previously recorded publication/sheet search is finished as a **bounded local
nonfinding with positive citation/depiction leads**, not an exhaustive absence
finding. It does not resolve Floor14 west-attachment identity, floor/revision
applicability, installed condition, released model coordinates or restraint
capacity. No geometric transform, floor-to-Z assignment or physical calculation
was performed.

## Verification and retained pins

The following are hashes actually read during the earlier local holdings pass,
not fresh payload hashes obtained for this handoff:

| Existing navigation/review artifact | Earlier observed SHA-256 |
|---|---|
| `c79-member-detail-crosswalk/report.md` | `54326664ec394421ae7894c3a634c417a03bddbd8facdde15a07800a6d0d000a` |
| `c79-member-detail-crosswalk/drawing-source-review.md` | `fac85c5d3de5c5e074ce3d77e09ec1d4fbaaa3df357c55617a425a37f681bbaf` |
| `c79-member-detail-crosswalk/drawing-public-sources/README.md` | `48c60eada86115a6a85cac58b91707bb3c0524f3bed2fbad2e2536cd5cfc84e7` |
| Main `model-access-audit/source-catalog.json` | `801471430488f1dc03726a55458dcfa1c0a018dcc90690d5191faeb7a231d54f` |
| Main `model-access-audit/run-v1/inspection.json` | `f3ec6b25464adf6ca3f9b972a9d4826c02e0729b711a1ee11a33a7a29750848b` |

These pins identify the records supporting the navigation result; they do not
authenticate original engineering sheets or historical execution. No web query,
archive inspection, held-packet access, raw model scan, unknown correspondence
read, source execution, solver, upload or other transmission occurred in this
arm. During the searches the two public bulk-drawing archives remained pending
the parent's exact approval request; this note neither grants nor infers that
approval. Main and prior-unit files were not edited.

## Smallest next independent task

The parent owns public publication retrieval and any approval-dependent archive
decision. Review an actually acquired, admitted complete technical sheet/paper,
including title/revision and member/floor applicability, against the published
depiction. Preserve a specific access/coverage limit if unavailable. Full-reasoning
source review is appropriate; a fresh broad local inventory is not needed
without a new file/version or a concrete alternate-name lead. A successful
source comparison still requires independent model-coordinate and physical-state
checks before it can establish the selected connection's behavior.
