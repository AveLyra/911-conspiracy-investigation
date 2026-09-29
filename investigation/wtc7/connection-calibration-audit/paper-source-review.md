# Exact-paper source review — bounded access result

Research only; 2026-09-12 local / 2026-09-13 UTC. Owned source-method subtask under `PROTOCOL.md`. No legal conclusion, model execution, property substitution, or historical-run authentication.

## Result

The exact cited paper is bibliographically identified, but its full text was **not acquired in this bounded pass**:

Sadek, F., El-Tawil, S., and Lew, H. S. (2008), “Robustness of Composite Floor Systems with Shear Connections: Modeling, Simulation, and Evaluation,” *Journal of Structural Engineering*, **134(11), 1717–1725**, DOI **10.1061/(ASCE)0733-9445(2008)134:11(1717)**.

The [publisher article record](https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9445%282008%29134%3A11%281717%29), as returned by the search index, and the [November 2008 issue contents](https://ascelibrary.org/toc/jsendh/134/11) identify this paper and its 2008 publication. The author's [publications list, Archival Journal Publications, item 50](https://public.websites.umich.edu/~eltawil/publications.html) identifies the same authors, title, volume, issue and pages. That item supplies no paper-download link.

The [NIST exact-title entry](https://www.nist.gov/publications/robustness-composite-floor-systems-shear-connections-modeling-simulation-and-evaluation) displays February 19, **2017**, both as its published/created date and in its generated citation. This is conflicting portal metadata, not a reason to change the publisher's 2008 article date or infer a second experiment. The [NIST structural-robustness bibliography, Journal Papers](https://www.nist.gov/el/mssd/structural-robustness-publications) separately gives 2008, the exact DOI and pages, although it shortens the title. Its paper link returns to the same NIST entry, not a PDF. These are identifiers/descriptions of one publication, not independent validation studies.

## What is supplied, and what remains unavailable

| Question | Evidence supplied in this pass | Limit |
| --- | --- | --- |
| Study identity and broad purpose | Official bibliographic records identify the paper; NIST's abstract describes analytical column-removal assessment of a concrete-deck/steel-beam floor system and shear connections. | An abstract is not the complete method, result tables or reference list. |
| Physical specimens, test count and conditions | No original-paper full-text evidence acquired. | Specimen count, geometry, restraints, loading history/direction, temperature and measured failure modes are **unresolved**, not zero or absent. |
| Calibration inputs and underlying experiments | No paper methods, tables or references acquired. | Cannot identify from this pass which measurements, analytical relations or prior studies supplied the spring law, or which observations were used to fit it. |
| Independent verification | No original measured-versus-predicted comparison acquired. | Cannot separate fitting data from held-out testing, quantify agreement/disagreement, or claim physical validation. |
| Transfer to the WTC 7 implementation | The prior NIST report audit remains available separately; see below. | Publication attribution alone does not identify calibrated cards, location-specific scaling, spreadsheet mappings, or the executable historical input. |

The NIST abstract's analytical findings must not be relabeled as measured physical performance. Conversely, failure to retrieve the paper is not evidence that the paper contains no experimental basis or that its model is invalid. No numerical comparison, graph digitization, or replacement property law was attempted.

## Existing NIST evidence retained, not replaced

The previous [material/run source review](../material-run-crosswalk/method-source-review.md) already read and visually inspected NCSTAR 1-9A PDF pages **73–77 / printed 22–26** and the reference at **PDF 117 / printed 66**. Those report pages are the existing source for the described fin-spring → calibrated shell/discrete connection-model chain and comparisons, not evidence newly extracted from the inaccessible paper. The previous review pins §3.3.1, Figures 3-2/3-3 and the location/geometry/capacity spreadsheet. It also explicitly separates that LS-DYNA construction from NCSTAR 1-9's ANSYS break-element implementation.

Source PDF: `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf`; previously recorded SHA-256 `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`. Prior full-page renders are `/private/tmp/material-method-source.rQlqbx/ncstar1-9a-p73.png` through `ncstar1-9a-p77.png`, and `ncstar1-9a-p117.png`. This subtask did not re-render or independently re-check those bytes/pages. Root separately owns the current NIST-page analysis and release-inventory crosswalk.

The other Sadek 2008 moment-connection paper (NIST publication 861512), later theses and NIST TN 1749 are not substitutes for the exact paper. No claims from them are imported here. A later retrospective study could supply separate validation context but cannot silently become evidence available in the 2008 paper.

## Access record and finite stopping point

Four distinct focused search queries were used; the fourth was retried once solely because output capture was truncated. Selected primary routes were the publisher's article/issue/PDF/EPDF/full-text endpoints, the author bibliography and NIST's exact-title/bibliography pages. The publisher's PDF route returned **HTTP 403** in a direct request; no PDF bytes were downloaded. Other web routes returned cache/internal or URL-safety errors as recorded. These observed access failures do **not** establish a paywall or that no public copy exists. No login, payment, author contact, private source or access-control bypass was attempted.

The author's bibliography and NIST entry supplied no direct paper PDF link. Search results also included later works and third-party request/abstract pages; none was treated as the exact primary full text. The bounded pass therefore stops at a positive bibliographic finding and a precisely located unresolved dependency: **the original paper's full methods/results/reference list and the primary experimental sources actually used for the fin/shear-tab spring law**. Without those pages, this subtask cannot supply physical sample counts or complete the fit-versus-independent-test provenance chain.

See [retrieval-log.json](sources/retrieval-log.json) for exact queries/routes and [manifest.json](sources/manifest.json) for the empty acquired-PDF inventory. Zero acquired PDFs means no original-paper page/marking inspection occurred; it is not a sensitivity-clearance finding or a zero-test finding. Metadata above was obtained from public engineering publication pages. No raw production, held packet, correspondence, or arbitrary personal/contact data was inspected or stored.
