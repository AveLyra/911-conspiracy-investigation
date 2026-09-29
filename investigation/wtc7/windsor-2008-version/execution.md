# Execution and access record

2026-09-20 UTC. This is a retrospective record of the tool observations listed below, not raw HTTP logs or preserved article bytes. Research only; [prospective protocol](PROTOCOL.md) SHA-256 `7e9bd0c52a9e378c8a3833c8592d8f81fb7117607e7890fcfd26981d0f420251`.

## Actual source operations

1. Opened the [Edinburgh catalogue](https://www.research.ed.ac.uk/en/publications/effects-of-fire-on-a-concrete-structure-modelling-the-windsor-tow/). Returned HTML with article metadata, abstract and the exact external file link. The metadata's country label was not adopted as verified geography. Repeated citation formats are one source.
2. Clicked that exact [external file link](https://bibliotecadigital.ipb.pt/bitstream/10198/1719/4/2008_ref_76.PDF). Returned HTML headed `Repositório :: Entrar`, with sign-in options, rather than a PDF. The clock checked immediately afterward was 2026-09-20 09:13:58 UTC. No numeric HTTP status or file bytes were available. No login, submission, preservation GET, alternate client or bitstream retry followed.
3. Ran the two queries below together, then the third separately. All three narrow official-domain queries were used.
4. Opened the separately identified [2009 thesis landing page](https://era.ed.ac.uk/items/2ca19958-abdd-42f6-8c03-6775017f9690). The web tool returned an internal `(400) Timeout fetching` error. This is a tool fetch error, not an authenticated origin-server HTTP status, access denial, or sign-in result. Clock afterward: 2026-09-20 09:15:26 UTC. No live transfer handle was returned; no retry was performed.

| Query | Domain restriction | Relevant outcome |
|---|---|---|
| `"Effects of fire on a concrete structure" Windsor` | ed.ac.uk, uc.pt, ipb.pt | Repeated catalogue, proceedings locators, and a separate thesis lead. |
| `"Fire Design of Concrete Structures" "978-972-96524-2-4"` | uc.pt, ipb.pt | Indexed proceedings/front-matter and programme locators, not admitted pages. |
| `"Fire Design of Concrete Structures" "2008" publisher` | uc.pt | Unrelated course/regulation/brochure results; no verified publisher full-text route adopted. |

Spelling note: the query text above is exact; the outcome column is our summary. Query results are not a complete catalogue or absence test.

## Indexed but uninspected locators

These links were returned in searches. They are leads only, not admitted sources. Do not use the alternate IPB routes to retry the observed sign-in route through another spelling/client.

- Proceedings [repository download locator](https://bibliotecadigital.ipb.pt/bitstreams/14120ca5-d952-48cf-bf2a-a92412cd2552/download) and [API-content locator](https://bibliotecadigital.ipb.pt/server/api/core/bitstreams/14120ca5-d952-48cf-bf2a-a92412cd2552/content): snippets include book identity and contents/pagination; neither was opened.
- Proceedings [institutional personal-page locator](https://pages.ipb.pt/~ppiloto/pdf/p77.pdf): indexed front matter; not opened or acquired. Its existence as a search result prevents describing the selected route's failure as worldwide nonavailability.
- [Programme locator](https://bibliotecadigital.ipb.pt/bitstreams/5e862af2-1eb5-4879-ba6a-fcfc4de88885/download): indexed Fletcher presentation, not opened.
- [Thesis full-metadata locator](https://era.ed.ac.uk/items/2ca19958-abdd-42f6-8c03-6775017f9690/full): search attributes *Tall concrete buildings subject to vertically moving fires: A case study approach* to Ian A. Fletcher, 2009. The full-metadata URL itself was not opened; the ordinary landing page timed out as recorded above.
- [Thesis indexed PDF locator](https://era.ed.ac.uk/bitstream/handle/1842/3199/IAF%20Thesis.pdf?isAllowed=y&sequence=1) and [API-content locator](https://era.ed.ac.uk/server/api/core/bitstreams/4f9ade1c-384a-42d6-b863-e1de2cd5657c/content): not opened or acquired. One snippet suggests similarly titled Coimbra and Singapore conference entries; this is a version-ambiguity lead, not a visually verified bibliography. No thesis method, quantity or conclusion is promoted from these snippets.

## Budget and acceptance

- Three of three allowed queries used.
- Two of four metadata/locator opens used (catalogue, thesis landing page).
- One of one selected full-text web opens used; result was HTML, not PDF.
- Zero preservation GETs; zero admitted PDFs/pages; zero new calculations, renderings or model runs.
- No live acquisition, rendering or locator process remains.
- The pre-source reviewer inspected the local protocol and prior records; this was not a second network observation or article reading.

The unused metadata allowance does not require more searches. This unit closes without version equivalence. No inferred global absence, concealment, or causal-ranking change. Full investigation remains active.

## Local verification

The [bounded text review](review.md) found no material correction. Its optional wording change was adopted: search returned additional proceedings locators, not a verified additional copy. A typo in the query-outcome summary was corrected. The review's snapshot hashes remain historical; those small edits and this verification entry intentionally change the final report/execution hashes. The reviewer made no independent remote observation, PDF reading or calculation replay.

Root's read-only `python3 -B` preservation check confirmed the protocol pin above and all eleven standalone Luna originals against the earlier attribution ledger. Combined final navigation checks covered these four Windsor-version Markdown files and four new synthesis/review files: 8 files, 59 local targets, no missing target, trailing whitespace, conflict marker or missing final newline. Twelve external links were not reopened. Both new research-navigation entries were present in each of the two indexes; argument-review pins matched. The scoped `git diff --check` for research/README.md, STATUS.md and SHERLOCK-FEEDBACK.md passed. These are document-integrity checks, not source acquisition or version-equivalence verification. No source, frozen reading, accepted engine record, legal record, commit or push is changed by this unit.
