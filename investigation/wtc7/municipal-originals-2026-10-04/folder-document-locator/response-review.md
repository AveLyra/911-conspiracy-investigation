# Independent saved-response review

October 4, 2026. Additive follow-up after initial `metadata-review.md` froze at SHA256 `9eab085e9209707ee16b1640ee9ff2ad3d29ee50f0f284fad3a44ab9ba176f14`. No root interpretation/report was read before this response-review freeze. No network, downloaded-code execution, PDF/image content reading, or source edits.

**Result: the two saved responses support a complete returned-ID list for these exact queries, with matching target tuples and 3-document/6-page and 2-document/2-page totals. Three additional IDs are now located.** Completeness remains scoped to the responding index/query, not every historical record, all possible labels, document-content distinctness, or completed engineering work.

## Pinned inputs

Files are in this unit directory. The preserved `folders.json` supplies the exact target keys already reviewed in the initial note.

| File | SHA256 |
|---|---|
| structural-request.json | b2f568e98237707d63661874262b68ec650d8ee26c32da9085198469af1af7bb |
| structural-response.json | 470c1b10d25218dcf05319199591bea8f906b178e05d92f78711622e70fe247a |
| sprinkler-request.json | d60767327692fc11c2329f95508c5354431c7ea102cd750c9f5f7bc039ee92f6 |
| sprinkler-response.json | 05d526268ba8ae78cb90c6a507d5076b29980ef920a7954c01e080e5470a470f |

Root identifies these as acquired City metadata responses. This local review checks their saved contents, identities and consistency; it does not independently recreate network provenance or certify the server's historical inventory.

## Returned records, not inferred neighbors

All five records have source **WTC 7**, box **7DCAS**, agency **Citywide Administrative Services, Dept. of**, and production volume **NYC-WTC0007**. These latter two fields are now directly returned per record rather than inferred from aggregate catalog totals.

| Folder | Returned ID | Reported pages | Reported PDF bytes | Reported production end | Content-read status in this investigation unit |
|---|---|---:|---:|---|---|
| Structural services | NYC-WTC_000167235 | 2 | 79607 | NYC-WTC_000167236 | Earlier design-sprinkler unit read first PDF; no re-view here |
| Structural services | NYC-WTC_000167240 | 2 | 79462 | NYC-WTC_000167241 | Newly located ID; contents unread here |
| Structural services | NYC-WTC_000167759 | 2 | 79419 | NYC-WTC_000167760 | Newly located ID; contents unread here |
| Fuel tank room sprinkler | NYC-WTC_000171300 | 1 | 84808 | NYC-WTC_000171300 | Earlier design-sprinkler unit read first PDF; no re-view here |
| Fuel tank room sprinkler | NYC-WTC_000171557 | 1 | 85393 | NYC-WTC_000171557 | Newly located ID; contents unread here |

Exact folder strings are `Mayor's Office of Emergency Management 7 World Trade Center, 23rd Floor Structural Engineering Services` and `Fire Sprinkler Quotation®Fuel Tank Room`. Every returned record matches its complete source/box/folder tuple literally. The first identifiers are present. All five IDs are globally distinct; this does **not** mean five substantively independent documents. Differences in byte counts/Bates IDs can coexist with duplicate or revised content.

## Query and coverage checks

Both saved requests use `ALL extension:pdf source:"WTC 7" box_name:"7DCAS" folder_name:"<exact folder string>"`, with count 25, `content_sample_length: 0`, and 11 metadata properties requested as `VALUE`, excluding content. Each response's `search_request` equals its saved request after removing the response-added empty `user_context` object. No unsolicited broadened query or different folder key appears.

This supplies observed evidence that those two fielded queries returned the intended literal tuples in these responses. It does not retroactively make exact-field syntax documented in the initially reviewed adapter, establish universal escaping/equality semantics, or independently test the index's recall.

- Structural response: 3 returned records; `estimated_count: 3`; page sum 6. Sprinkler response: 2 records; `estimated_count: 2`; page sum 2. These agree with the September 11 folder snapshot expectations, without relying on the older September 9 summary.
- Both explicitly have `prev_avail: false` and `next_avail: false`. Each has exactly one `per_service_dataset`, ID `https://nyc.mindbreeze.com/search/september-11/`, with **`termination_cause: "NO_MORE_RESULTS"`**. A retained paging-state object does not override these terminal fields or itself imply another page is required.
- Returned counts are below the requested limit of 25; neither response looks truncated merely by reaching that count. `estimated_count` remains an estimate by name; scoped completion is supported by its agreement with actual results, explicit terminal fields, and the matching catalog counts together—not by treating the estimate alone as an exact census.
- Each result has exactly the 11 requested property IDs, without duplicates, and one data value per property. Its result ID, `mes:key`, and `.pdf` title agree. Page counts are canonical positive-integer strings; PDF sizes are positive integer-valued numbers. The independent check did not use the downloaded adapter's lossy `int(float(...))` conversion or normalizer.
- `related_document` was neither requested nor returned in the result properties; its name in `available_properties` is not an actual attachment/relationship value. It cannot establish document relationships here. `mes:date`/relevance/rank/order values likewise do not establish creation chronology, revision order, or confidence in content.

No incorrect target join, duplicate ID, count disagreement, or reported unfinished service was found. Missing/relabeled/unindexed records could still escape these queries; matching metadata is not proof that no other historical records exist.

## Reproducible local checks and limits

- Full two request files read with `cat`: `279990`, exit 0.
- Full structural and sprinkler responses read with `jq '.'`: `f8da99` and `573f74`, exit 0, untruncated. This included result properties and terminal service fields, not only summary totals.
- Four input hashes: `6dd38d`, exit 0. Response sizes: 11,186 and 9,587 bytes (`7e0d3a`, exit 0).
- Independent standard-library `python3` stdin check: `c926e8`, exit 0. It imported only `json`, `re`, and `pathlib`, read only preserved JSON, and rejected duplicate JSON object keys. It required exact request echo; one unique target catalog row; literal tuple agreement; canonical key/title/result-ID agreement; unique single-valued requested properties; valid page/byte types; five unique IDs including both first IDs; returned/estimated/catalog document-count agreement; page-count sums; explicit false next/previous flags; and the one expected service with `NO_MORE_RESULTS`. Output listed all five IDs/pages/bytes/end IDs above and a final PASS. Nothing from downloaded Python was imported or executed.
- Destination absence check `81cac2`, exit 0; only this additive note created with `apply_patch`. Initial metadata review, responses, protocol, and all prior readings remain unchanged.

The next content discriminator is the newly located **167240, 167759, and 171557**, currently reported as five pages combined. Each requires a separately declared acquisition/complete-reading step; labels/counts alone cannot establish an accepted agreement, revised scope, actual drawing, completed inspection, or even substantively new material. Repeated proposal/quote copies would be a meaningful negative result, not new independent corroboration. No such retrieval or source-content conclusion occurred in this review.
