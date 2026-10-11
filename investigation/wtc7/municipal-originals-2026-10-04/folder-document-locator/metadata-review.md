# Independent local metadata review

October 4, 2026. First findings frozen before receiving root's interpretation or City-query results. **The two exact captured folder matches are established; remaining document IDs and current City completeness are not established by these three files.** Research-only, separately reasoned AI review, not historical-source independence or a content/engineering finding.

## Scope, sources, and pins

Read the complete unit protocol, main charter, applicable worktree AGENTS and main WORKFLOW/START-HERE; main AGENTS controls also supplied in the conversation remain controlling over older worktree wording. Evidence/source skills and their audit references were read; the data-quality skill was used only for a scoped grain, key, and completeness check within this existing investigation. No dashboard, notebook, automation, or publication workflow was initiated.

Only new output: this working note. Three supplied files under `/private/tmp/wtc7-folder-locator.RayuZv/` were read without importing or executing `portal.py`. The complete 472-line adapter and 35-line summary were read; the folder schema, metadata, and two selected rows were read closely, while all 4,205 rows were parsed for narrow structural/count/key checks—not reviewed for unrelated contents. No network, source PDF, image, new source acquisition, or root findings were used.

| Held file | Bytes | SHA256 |
|---|---:|---|
| folders.json | 421135 | cf3afa33cc58a0f2a9d48e6fbac57cdd8bb060b046cf5373d261d37bb976b704 |
| catalog-summary.json | 1160 | e30fd353a280639bc560b2ffcb404e2bac36d475a5660e69e4bdf1099d9cb9cc |
| portal.py | 20905 | 79dffa99e9c3a74b5fcaecb60e7335b0ff1ac6b7f3fcdca12525cb1d0790c4dc |

Protocol SHA256: `e4ec67f60955ee307fb0dc21cc43592f00e2ee16585de4a48469254f3f36d9fe`.

The main locator's lines 128–130 identify these exact upstream resources:

- https://github.com/pranava0x0/sept11documents-mcp/blob/main/docs/data/folders.json
- https://github.com/pranava0x0/sept11documents-mcp/blob/main/docs/data/catalog-summary.json
- https://github.com/pranava0x0/sept11documents-mcp/blob/main/sept11/adapters/portal.py

These are third-party, mutable-branch source locators. The local hashes pin acquired bytes; I did not independently verify their remote commit or retrieval timestamps. Embedded capture dates describe the publisher's snapshots, not my retrieval time or the underlying documents' dates.

## Exact two-folder joins

`folders.json` declares columns `[source_index, box, folder, documents, pages, first_bates]`; `sources[2]` is **WTC 7**. Both target rows use source index 2 and box **7DCAS**.

| First document | Exact folder label | Documents / pages | Location |
|---|---|---|---|
| NYC-WTC_000167235 | Mayor's Office of Emergency Management 7 World Trade Center, 23rd Floor Structural Engineering Services | 3 / 6 | zero-based row 3645; file line 3668 |
| NYC-WTC_000171300 | Fire Sprinkler Quotation®Fuel Tank Room | 2 / 2 | zero-based row 3189; file line 3212 |

Each first ID, exact `(source_index, box, folder)` tuple, and selected folder-name string matches exactly **one** row in this snapshot. Preserve the literal `®` in the sprinkler label; silently replacing it with a space/newline would create a different string, even if a search engine later normalizes it.

The grain is **folder within source and box**, not one document or one PDF page. Counts are aggregated over the group. `first_bates` is one selected first ID, not a list, last ID, range, attachment count, or demonstrated arithmetic sequence. Do not infer 167237/167239 or 171301 from the counts. These rows contain neither the other document IDs nor per-document page counts/bytes, agency, or production-volume fields. Aggregate agency/production counts in the separate summary cannot populate those missing joins.

## Snapshot and count checks

- Folder snapshot claims capture **2026-09-11T12:57:00+00:00**, underlying CSV hash `26f24148f19971988a3fa033b0f82cc68b8801db6d8b40bbced2ff2528e1173e`, 24,437 documents, 4,205 rows, and zero withheld labels. The CSV itself was not inspected; the last field is the publisher's screen result, not a comprehensive privacy/completeness certificate.
- Parsed rows = **4,205**, matching `rows_total`; summed row document counts = **24,437**, matching `documents`; summed pages = **172,544**. Unique composite keys and first IDs both = **4,205**; distinct folder-name strings = **4,172**. Composite groups must not be confused with global distinct folder labels.
- Separate `catalog-summary.json` claims **2026-09-09T15:30:00Z**, CSV hash `687a0c6688dabd6c6f75f47c40ce089bd0929122f6ffaa33d3fc7fa86a7bbc91`, 24,441 documents, 173,299 pages, and 4,173 folders. This is **not the same capture or CSV**. The adapter's `summarize_catalog` computes folders as distinct folder-name strings, not source/box/folder groups.
- Thus the 4,205-versus-4,173 comparison is not a like-for-like missing-folder count. Even the distinct-name comparison (4,172 versus 4,173), document difference (four), and page difference (755) span different snapshots. They identify a freshness/comparability boundary, not proof of deletion, withholding, or a change in either target folder.

**High-confidence local conclusion:** the captured two-folder joins are usable locator evidence. **Material limit:** they do not themselves enumerate the remaining documents or establish current portal coverage. The smallest discriminator is a bounded current response with exact source/box/folder properties and all returned IDs, retaining any mismatch rather than forcing agreement.

## Public-search contract actually documented in the held adapter

The adapter is third-party implementation evidence, not independently verified City API documentation. Its opening docstring says the anonymous JSON route was verified on September 9, 2026; this review did not test that claim.

- `FRONT` (line 41) = `https://sept11documents.cityofnewyork.us`; `BACKEND` (line 42) = `https://nyc.mindbreeze.com/search/september-11`. `PortalClient` defaults to FRONT; `_post_json` appends a path to `self.base`. The catalog summary records BACKEND as `api_base`. The mere presence of BACKEND does not mean a default client automatically switches to it.
- `search` (lines 177–194) constructs a POST to `/api/v2/search`, JSON body `user.query.unparsed = query`, `count`, `content_sample_length`, and `properties`. Each property request is `{name: FIELD, formats: ["VALUE"]}`; only `content` uses `HTML`. Optional facets/order-by are added separately. This is documented as retrieval, not a source-data mutation; no downloaded method was run.
- Relevant requested fields: `mes:key`, `title`, `source`, `agency`, `box_name`, `folder_name`, `page_count`, `pdf_size`, `production_volume`, `production_end`, `related_document`, `mes:date`. Avoid requesting `content` for this metadata-only unit.
- **Important syntax ceiling:** the held code's concrete query example/default is `ALL extension:pdf`. It accepts arbitrary unparsed query text but contains no target-folder example, escaping specification, equality operator, or guarantee that quoted `folder_name` search is exact equality. Requesting a property by name is not proof of field-filter syntax. Exact folder-filter semantics must come from the parent's authorized query documentation/response, not be attributed to this file. Regardless of search syntax, post-check the returned raw source/box/folder tuple.
- `iter_results` (lines 196–228) expects `response.resultset.results`; each result has `properties`, each property keyed by `id`. `_value` (lines 301–316) takes only `data[0]`, then `value.str`, `value.num`, or an `html` fallback. `simplify_result` (lines 319–342) uses `mes:key` with `title` fallback and a separately imported `normalize_bates` helper; that helper's implementation was not supplied/read here.
- `page_count` and `pdf_size` are converted with `int(float(value))` in `simplify_result`. Do not inherit this as a validity check: it could silently truncate fractional values. Retain raw values, confirm finite positive integers, and compare counts only at the correct grain.
- The helper requests `related_document` but does **not** retain it in its simplified result. It takes only the first value and collapses repeated property IDs by dictionary construction. For this audit, retain complete raw responses so additional/multivalued data and identity disagreements are not silently lost.
- Continuation: inspect `resultset.next_avail`; next state comes from `resultset.paging_state`, or the list of `per_service_dataset[*].paging_state`. Next request carries `paging_states` (list) and `paging.direction = "NEXT"`. Duplicate Bates IDs and repeated paging states cause the helper to refuse; missing state with more results also refuses.
- Coverage caveat: the helper returns on an empty result list before checking `next_avail`, treats absent/false `next_avail` alike, and stops at an optional `max_results`. It does not demonstrate a total-hit-count extraction contract or reconcile totals. Preserve those distinctions: empty/malformed response, result cap, missing pagination, and true completion are not interchangeable. No returned total/count should be invented when absent.

## Minimal acceptance checks for the parent's separately authorized query

Require exact target tuple per result, canonical unique returned document IDs, unambiguous raw ID/title correspondence, valid per-document page counts, and retained pagination state/status. Check both known first IDs are present. If all pages are demonstrably covered, compare the current response's document/page sums with its own reported totals and then, separately, with the dated folder expectations (3/6 and 2/2). A discrepancy can reflect search semantics, indexing changes, missing metadata, or incomplete pagination; it is not automatically missing historical evidence. Any extra folder hit is rejected from the target join, not silently relabeled. Two-page/100-record/eight-request protocol limits remain binding.

## Actual local verification

- Full skills/protocol read `5498cb`; source-skill references plus controls `86bd3e`/`43eed8`; truncated analytics reads were completed explicitly in `e81ff7`, `0674af`, `524213`, with focused quality `9600be` and shared instructions `a519b1`. Full main charter `e0742c`. All terminal exit 0; no truncated file was treated as fully read.
- `wc -lc` of three inputs: `1d04e1`, exit 0. Full summary `bd380f`; full adapter split 1–240 / 241–500 at `b7eb91` / `40509a`; folder header `4e3399`, exact row search `cb8949`; all exit 0.
- `shasum -a 256` of three inputs and protocol: `2efdcd`, exit 0. Main locator's exact URL lines: `62889c`, exit 0.
- Independent `jq` profile (`165fd9`, exit 0) parsed the whole folder JSON and printed row/document/page sums, distinct folder/composite/first-ID counts, and the two zero-based target positions. Schema/domain checks (`e3ba46`, exit 0, `true`) required the six named columns, row/header and document/header agreement, six-element rows, valid source indexes/string keys/positive numeric counts, canonical first-ID pattern, and exactly one occurrence of each target first ID. This check did not purport to validate all historical metadata or integer-valued counts beyond the tested predicate.
- Target-only decoded-source and uniqueness check (`12121f`, exit 0) used `. as $d | [.rows[] | select(.[5]=="NYC-WTC_000167235" or .[5]=="NYC-WTC_000171300") | . as $r | {source:$d.sources[$r[0]],box:$r[1],folder:$r[2],documents:$r[3],pages:$r[4],first_bates:$r[5],matches_same_composite_key:([$d.rows[]|select(.[0:3]==$r[0:3])]|length),matches_same_folder_name:([$d.rows[]|select(.[2]==$r[2])]|length)}]`.
- Destination absence `6d77d1`, exit 0; only this note created with `apply_patch`. No downloaded Python executed/imported, no network or PDF/image reads, no change to sources, canonical records, engine/bridge, or git state.

No causal ranking, installed-condition conclusion, archive-wide completeness claim, or historical authenticity claim follows from this metadata review.
