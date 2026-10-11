# Independent first-floor metadata lookup review

## Initial independent freeze

Research-only companion check under PROTOCOL.md SHA256 `d11b4009d5d88549cb48339cda373b156f50f97e64da5728c839084bc65c104f`.
This portion was prepared without reading the root lookup implementation, result,
report or candidate disposition. The protocol and earlier municipal work are known;
this is an independently implemented check, not a historically blinded study.

Only the 24 held JSON inputs enumerated below were opened for metadata analysis.
No PDF parsing, image views, OCR, rendering, source download, network, headers,
transport logs, model payload, legal-file edit or corpus recensus was performed.
This note is the only repository write. Main controls and charter remain controlling.
The source-of-truth and evidence-audit skills kept supplied metadata, derived matches,
interpretation and unverified historical applicability separate. The data-quality
skill was used as a scoped companion check, without a new notebook or publication.

### Result and limits

- All 4,205 catalog rows and 302 response occurrences were searched in the prescribed
  fields. Responses contain 208 unique result IDs, 46 repeated-ID groups and 94 extra
  appearances. No within-response duplicate result IDs occurred.
- Catalog: 38 matches, comprising 36 WTC 7 and two off-source rows. Predicate counts:
  structural_context 33; first_floor 5. All are
  lower-specificity context leads. There are no sheet-token or combined
  first-floor/structural subject leads.
- Responses: 11 matched occurrences, eight distinct document IDs, all WTC 7 and all
  lower-specificity structural-context leads. Their matches occur in supplied
  folder_name fields, not document titles.
- The missing folder_name property occurs in eight response occurrences/eight IDs.
  Literal string `None` occurs in 22 occurrences/18 IDs; it is not converted to a
  missing value. The other 182 unique IDs have another supplied folder label.
- All supplied property envelopes and locations agree across repeated result IDs;
  zero conflicts. Query-dependent scores/order vary in 43 repeated-ID groups and
  are not confidence, historical dates or supplied-description disagreement.
- Exact source/box/folder context keys join 200 unique response IDs to one catalog
  row each; eight cannot be joined because the folder field is absent. This is
  context alignment, not proof of catalog document membership or independent evidence.
- Three saved responses reach COUNT_LIMIT and expose next_avail=true. The other
  20 report NO_MORE_RESULTS for their saved query/service result, not complete archive
  recall. Missing descriptions, unreturned pages and unsearched fields remain unknown.
- These metadata results do not identify an applicable S-1/S-S-1 drawing, revision,
  grid/member key, installation, physical mapping or model correspondence. A finite
  separately declared public title/content test would be needed for any chosen lead.
  Nothing here reopens an exhausted image allowance or authorizes acquisition.

## Actual execution and preserved failure

All computation below ran stdout-only with
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 - <<'PY'`
and the indicated Python body, ending at `PY`. No producer parser was imported.

- Exact `rg --files --hidden --no-ignore -g '*-response.json'` over the four
  authorized directories: receipt d198da, exit 0, found 23 response files.
  The catalog makes 24. No transports or headers entered the input set.
- Initial shape/hash probe: 477c85, exit 0. A long displayed shape output was
  truncated by presentation; the captured full JSON-lines result was successfully
  parsed for all 24 inventory entries. No missing parse was treated as a pass.
  Property/empty-result schema probe b1f264, exit 0.
- Schema-only profile: 16c683, exit 0, started
  `2026-10-05T04:59:15.755260+00:00`, analysis 0.209861 s, tool wall 1.394556917 s.
  This preceded the semantic protocol receipt and is retained below.
- Protocol complete read 8e83c8, exit 0; hash check 8c28f6, exit 0, exact frozen hash
  above. Identifier/source schema clarification ebfe20, exit 0, before extraction.
- Failed synthetic test 2ff0bc, exit 1 (0.199120916 s tool wall):
  `AssertionError: sheet negative XS-S-1`. This assertion was before protocol/source
  opens in the script. The declared expression matches the trailing `S-1` inside
  that compound. Only this synthetic expectation was moved from negative to
  positive; the frozen expressions, inputs and match selection were unchanged.
- Corrected extraction efe666, exit 0, 43 tests, analysis 0.480094 s,
  tool wall 0.732822334 s. It found the same 38 catalog and 11 response matches.
- Final independent extraction 983dee, exit 0, started `2026-10-05T05:03:17.215362+00:00`,
  analysis 0.253417 s, tool wall 1.456843708 s. This strengthened the
  synthetic field-isolation test to include unsearched echo/facet/paging tokens,
  added explicit source/box/folder joins and actual occurrence/ID accounting.
  All 44 tests passed. All 24 input pins and the protocol were unchanged
  before/after execution. No duplicate JSON key, duplicate property ID,
  malformed catalog row width, selected multivalue/non-string field or supplied
  repeated-property conflict was found.

These are actual current metadata checks. They are not new transport, renderer,
historical authenticity, engineering or human acceptance checks. Prior renderer
receipts are not replayed or adopted as new observations here.

## Exact finite input inventory

All relative paths are under
`../municipal-originals-2026-10-04/`. Total: 24 files, 933,955 bytes.

| Exact relative input | Bytes | SHA256 |
| --- | ---: | --- |
| folder-document-locator/folders.json | 421135 | cf3afa33cc58a0f2a9d48e6fbac57cdd8bb060b046cf5373d261d37bb976b704 |
| drawing-locator/control-response.json | 8451 | fdf92a229791be47e9ca997939bc9df8f9543fa4eb7764c3bb3c1770a52ae57b |
| drawing-locator/skp3-response.json | 22502 | a13e7e290cd0e625db4502ec4197389c1c549b138b48502c2daebc00c62a3a26 |
| drawing-locator/skp4-response.json | 21189 | e4848f93061aaf339bdfb006fce212f95805298ba24fe60e8e1d2fbcb6be9a0b |
| drawing-locator/sts7-response.json | 10553 | 639d3c9f00b00acbdf613525c3ffa27b6f2e3190a1b566269a003d59424b41c7 |
| folder-document-locator/sprinkler-front-response.json | 9587 | 61f3eb3219955a11c9648fb50b8603e98e7de0ca99d15f230cc1eb4ad2beec13 |
| folder-document-locator/sprinkler-response.json | 9587 | 05d526268ba8ae78cb90c6a507d5076b29980ef920a7954c01e080e5470a470f |
| folder-document-locator/structural-front-response.json | 11120 | 858004f96f45f33ac637a6ae7d84cf7b6e4c8c6750df285b316b37eef77c913a |
| folder-document-locator/structural-response.json | 11186 | 470c1b10d25218dcf05319199591bea8f906b178e05d92f78711622e70fe247a |
| test-acceptance-locator/control-response.json | 8451 | 7386207c519d9144fc0a2b9e6092351a41ba38059f2008e8156d4ed0686f6a29 |
| test-acceptance-locator/date-response.json | 1760 | ea21d260015169581e7b80212786e6be4aeb7abd6ea8c821a555998ba89a2e4f |
| test-acceptance-locator/generator-response.json | 66134 | bf13d5608fc49e3da64b3291b2779ddfd64692e05ae7c7fa063a9d7e2afd3186 |
| test-acceptance-locator/punch-response.json | 65056 | cd6bfc2d72090d0dcd33cf8b014d4be63ae4b05d71ace3de66700cfa45f6b73d |
| test-acceptance-locator/signoff-response.json | 30480 | 42c16897153f26bb0a0844f6693cd5cac3818a9dbd6e8acb85563a2616a5e6eb |
| job1854-followup-locator/apt-response.json | 28606 | edca6e7e2e4ce1fe9597e02ad43d73638e8c9143e2add8e2c6460f8fccefd7cc |
| job1854-followup-locator/break_glass-response.json | 16556 | 440be5766c79591ae7dae03a1f3778e8330c75350f6cc611ebf70266dd0e7ae4 |
| job1854-followup-locator/control-response.json | 8451 | bbdeb6f33a4e8d937d9b13e666f226b6fee5bfbdbf436763bfce250f864ca80a |
| job1854-followup-locator/date_slash-response.json | 17739 | 4bc4695cb8e94616475a92f75b1cd748c4bfd25e0947696db73e04bb517f51de |
| job1854-followup-locator/date_words-response.json | 29768 | c062562ca7eb8931edd58ebefb9a29c5ef369ec75ffae98e98130860fc3dd2db |
| job1854-followup-locator/fuel_pump-response.json | 17729 | 75efcf4871d44c4e20b85fa3f1dd812b092c20b8257a36d43e986fe0f909ee72 |
| job1854-followup-locator/load_shedding-response.json | 15507 | 921d6ab1d95e67be18399c36e4931c98a6af842f5195266fb18a5b9a71f390bf |
| job1854-followup-locator/penn-response.json | 64684 | 1202cd667c7ce002ff231ef4b2e9460f01795b9b054a3dd935b2f131fac8efce |
| job1854-followup-locator/penn_phrase-response.json | 26105 | 54457b9032d4d1783ee38c5a9a2bd6b043ccc0334035af855928ef0c6acf3283 |
| job1854-followup-locator/transient-response.json | 11619 | 37b9ecb12c0a722caf551f42398af6d80d336ea1bf92ad9100e981d4a0289ae3 |

## Grain, schema and missingness

Catalog `rows[]` are positional folder/group rows with ordered `columns`:
`source_index, box, folder, documents, pages, first_bates`.
All 4,205 rows have width six and types int/string/string/int/int/string.
Source index resolves through the catalog's `sources[]`; counts are
0:2,546; 1:20; 2:1,639. The catalog declares 4,205 rows/24,437 documents and
the row sums equal 24,437 documents/172,544 pages. These are catalog aggregate
counts, not counts of admitted PDFs. Exact complete rows, source/box/folder keys,
and first_bates values are each unique in this file. There are 20 empty box labels,
22 empty folder labels and one literal `None` folder label, with no nulls or
missing positions. `labels_withheld` is supplied as zero.

Responses use `resultset.results[]` at search-hit/document-record grain:
`id, location, order, properties, rank_score, relevance_score`.
Properties are identified by `properties[].id`, with display `name` and
one `data[].value` item. Requested IDs, in order, are
`mes:key, title, source, agency, box_name, folder_name, page_count, pdf_size,
production_volume, production_end, mes:date`; all 23 echoes have these exact
VALUE requests and content_sample_length=0. Folder responses request 25;
the other responses request 50. No query text is searched by this check.

Supplied strings use `data[0].value.str`; page_count is a digit string in all
302 occurrences. pdf_size is a positive finite integral-valued JSON float at
`data[0].value.num` in all 302. mes:date is a float with a unit string; neither
service clocks nor ranking numbers establish a historical date or confidence.
All eleven fields are supplied except the eight omitted folder_name properties.
Every supplied property has exactly one data item; no null/empty selected data or
empty response string occurs. Absent folder counts by file: apt four, penn three,
transient one. Missing folders remain unknown, not predicate nonmatches on an
observed value.

All resultsets have prev_avail=false and one per_service_dataset. Paging-state
key names are `digest, id, state_base64`; opaque token values were neither
decoded nor searched. date-response has estimated_count=0, no results member,
NO_MORE_RESULTS and one status-message member. Its reported zero occurrence
count preserves that missing-member structure rather than inventing an empty list.

| Saved response | Returned occurrences | Requested count | Estimated count | next_avail | Service termination |
| --- | ---: | ---: | ---: | --- | --- |
| drawing-locator/control-response.json | 1 | 50 | 1 | false | NO_MORE_RESULTS |
| drawing-locator/skp3-response.json | 13 | 50 | 13 | false | NO_MORE_RESULTS |
| drawing-locator/skp4-response.json | 12 | 50 | 12 | false | NO_MORE_RESULTS |
| drawing-locator/sts7-response.json | 3 | 50 | 3 | false | NO_MORE_RESULTS |
| folder-document-locator/sprinkler-front-response.json | 2 | 25 | 2 | false | NO_MORE_RESULTS |
| folder-document-locator/sprinkler-response.json | 2 | 25 | 2 | false | NO_MORE_RESULTS |
| folder-document-locator/structural-front-response.json | 3 | 25 | 3 | false | NO_MORE_RESULTS |
| folder-document-locator/structural-response.json | 3 | 25 | 3 | false | NO_MORE_RESULTS |
| test-acceptance-locator/control-response.json | 1 | 50 | 1 | false | NO_MORE_RESULTS |
| test-acceptance-locator/date-response.json | 0 (member absent) | 50 | 0 | false | NO_MORE_RESULTS |
| test-acceptance-locator/generator-response.json | 50 | 50 | 144 | true | COUNT_LIMIT |
| test-acceptance-locator/punch-response.json | 50 | 50 | 91 | true | COUNT_LIMIT |
| test-acceptance-locator/signoff-response.json | 20 | 50 | 20 | false | NO_MORE_RESULTS |
| job1854-followup-locator/apt-response.json | 19 | 50 | 19 | false | NO_MORE_RESULTS |
| job1854-followup-locator/break_glass-response.json | 8 | 50 | 8 | false | NO_MORE_RESULTS |
| job1854-followup-locator/control-response.json | 1 | 50 | 1 | false | NO_MORE_RESULTS |
| job1854-followup-locator/date_slash-response.json | 9 | 50 | 9 | false | NO_MORE_RESULTS |
| job1854-followup-locator/date_words-response.json | 19 | 50 | 19 | false | NO_MORE_RESULTS |
| job1854-followup-locator/fuel_pump-response.json | 9 | 50 | 9 | false | NO_MORE_RESULTS |
| job1854-followup-locator/load_shedding-response.json | 7 | 50 | 7 | false | NO_MORE_RESULTS |
| job1854-followup-locator/penn-response.json | 50 | 50 | 157 | true | COUNT_LIMIT |
| job1854-followup-locator/penn_phrase-response.json | 16 | 50 | 16 | false | NO_MORE_RESULTS |
| job1854-followup-locator/transient-response.json | 4 | 50 | 4 | false | NO_MORE_RESULTS |

### Preserved schema-only profile

```json
{"catalog":{"column_missingness":{"box":{"absent":0,"empty_string":20,"literal_None":0,"null":0,"types":{"str":4205}},"documents":{"absent":0,"empty_string":0,"literal_None":0,"null":0,"types":{"int":4205}},"first_bates":{"absent":0,"empty_string":0,"literal_None":0,"null":0,"types":{"str":4205}},"folder":{"absent":0,"empty_string":22,"literal_None":1,"null":0,"types":{"str":4205}},"pages":{"absent":0,"empty_string":0,"literal_None":0,"null":0,"types":{"int":4205}},"source_index":{"absent":0,"empty_string":0,"literal_None":0,"null":0,"types":{"int":4205}}},"columns":["source_index","box","folder","documents","pages","first_bates"],"declared_documents":24437,"declared_rows":4205,"first_bates_keys":{"duplicate_groups":0,"extra_occurrences":0,"unique":4205},"full_row_duplicates":{"duplicate_groups":0,"extra_occurrences":0,"unique":4205},"labels_withheld":0,"row_lengths":{"6":4205},"rows":4205,"source_box_folder_keys":{"duplicate_groups":0,"extra_occurrences":0,"unique":4205},"source_index_counts":{"0":2546,"1":20,"2":1639},"sum_documents":24437,"sum_pages":172544},"elapsed_seconds":0.209861,"extra_result_occurrences":94,"failures":[],"field_missingness":{"agency":{"data_length_1":302,"present":302,"value_str":302},"box_name":{"data_length_1":302,"present":302,"value_str":302},"folder_name":{"absent":8,"data_length_1":294,"literal_None":22,"present":294,"value_str":294},"mes:date":{"data_length_1":302,"present":302,"value_num":302},"mes:key":{"data_length_1":302,"present":302,"value_str":302},"page_count":{"data_length_1":302,"digit_string":302,"present":302,"value_str":302},"pdf_size":{"data_length_1":302,"positive_finite_integral_numeric":302,"present":302,"value_num":302},"production_end":{"data_length_1":302,"present":302,"value_str":302},"production_volume":{"data_length_1":302,"present":302,"value_str":302},"source":{"data_length_1":302,"present":302,"value_str":302},"title":{"data_length_1":302,"present":302,"value_str":302}},"input_bytes":933955,"input_count":24,"pagination":[{"estimated_count":1,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"drawing-locator/control-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":1,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":13,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"drawing-locator/skp3-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":13,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":12,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"drawing-locator/skp4-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":12,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":3,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"drawing-locator/sts7-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":3,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":2,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"folder-document-locator/sprinkler-front-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":25,"results_member_present":true,"returned":2,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":2,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"folder-document-locator/sprinkler-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":25,"results_member_present":true,"returned":2,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":3,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"folder-document-locator/structural-front-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":25,"results_member_present":true,"returned":3,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":3,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"folder-document-locator/structural-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":25,"results_member_present":true,"returned":3,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":1,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"test-acceptance-locator/control-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":1,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":0,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"test-acceptance-locator/date-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":false,"returned":0,"sample_length":0,"service_count":1,"status_messages_count":1,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":144,"folder_absent":0,"next_avail":true,"order_next_result_present":true,"paging_state_keys":[["digest","id","state_base64"]],"path":"test-acceptance-locator/generator-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":50,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["COUNT_LIMIT"]},{"estimated_count":91,"folder_absent":0,"next_avail":true,"order_next_result_present":true,"paging_state_keys":[["digest","id","state_base64"]],"path":"test-acceptance-locator/punch-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":50,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["COUNT_LIMIT"]},{"estimated_count":20,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"test-acceptance-locator/signoff-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":20,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":19,"folder_absent":4,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"job1854-followup-locator/apt-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":19,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":8,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"job1854-followup-locator/break_glass-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":8,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":1,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"job1854-followup-locator/control-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":1,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":9,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"job1854-followup-locator/date_slash-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":9,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":19,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"job1854-followup-locator/date_words-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":19,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":9,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"job1854-followup-locator/fuel_pump-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":9,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":7,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"job1854-followup-locator/load_shedding-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":7,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":157,"folder_absent":3,"next_avail":true,"order_next_result_present":true,"paging_state_keys":[["digest","id","state_base64"]],"path":"job1854-followup-locator/penn-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":50,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["COUNT_LIMIT"]},{"estimated_count":16,"folder_absent":0,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"job1854-followup-locator/penn_phrase-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":16,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]},{"estimated_count":4,"folder_absent":1,"next_avail":false,"order_next_result_present":false,"paging_state_keys":[["digest","id","state_base64"]],"path":"job1854-followup-locator/transient-response.json","prev_avail":false,"request_eleven_fields_exact":true,"requested_count":50,"results_member_present":true,"returned":4,"sample_length":0,"service_count":1,"status_messages_count":0,"termination_causes":["NO_MORE_RESULTS"]}],"pins_unchanged":true,"repeated_id_location_conflict_groups":0,"repeated_id_order_variation_groups":43,"repeated_id_property_conflict_fields":{},"repeated_id_property_conflict_groups":0,"repeated_id_score_variation_groups":43,"repeated_result_id_groups":46,"response_result_occurrences":302,"schema_types":{"agency.data[].value.str":{"str":302},"box_name.data[].value.str":{"str":302},"folder_name.data[].value.str":{"str":294},"mes:date.data[].value.num":{"float":302},"mes:date.data[].value.unit":{"str":302},"mes:key.data[].value.str":{"str":302},"page_count.data[].value.str":{"str":302},"pdf_size.data[].value.num":{"float":302},"production_end.data[].value.str":{"str":302},"production_volume.data[].value.str":{"str":302},"property.data":{"list":3314},"property.data[].value":{"dict":3314},"property.id":{"str":3314},"property.name":{"str":3314},"result.id":{"str":302},"result.location":{"str":302},"result.order":{"dict":302},"result.properties":{"list":302},"result.rank_score":{"float":302},"result.relevance_score":{"float":302},"source.data[].value.str":{"str":302},"title.data[].value.str":{"str":302}},"started_utc":"2026-10-05T04:59:15.755260+00:00","unique_id_folder_states":{"absent":8,"literal_None":18,"other_present":182},"unique_result_ids":208,"within_file_duplicates":{}}
```

## Complete catalog matches

One JSON object per original matched row. Ordinals are one-based; spans are
zero-based half-open character offsets in the original field. All source text
and count values below are metadata, not conclusions about drawing content.

```json
{"box":"DEP Box 44","category":"lower-specificity context lead","documents":5,"first_bates":"NYC-WTC_000165453","folder":"Proposed Sewer Relocation in Conjunction with new Subway Interconnection 3RD AVE AT 60TH STREET DRAWINGS 9/29/81-138/3","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[96,104],"text":"DRAWINGS"}]}},"ordinal":1298,"pages":8,"predicates":["structural_context"],"source":"DEP Hard Copies (68 Boxes)","source_index":0,"source_scope":"off-source"}
{"box":"DEP Box 44","category":"lower-specificity context lead","documents":11,"first_bates":"NYC-WTC_000165461","folder":"U.S.S. Intrepid Museum - Pier 86 W. 46 St. DRAWINGS","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[43,51],"text":"DRAWINGS"}]}},"ordinal":1301,"pages":35,"predicates":["structural_context"],"source":"DEP Hard Copies (68 Boxes)","source_index":0,"source_scope":"off-source"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":2,"first_bates":"NYC-WTC_000166793","folder":"AISI Beam Column Design with Lateral Torsional Buckling","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[5,9],"text":"Beam"}]}},"ordinal":2882,"pages":8,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000173191","folder":"Addendum modifying Specifications and Drawings date 5/04/98","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[38,46],"text":"Drawings"}]}},"ordinal":2903,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000173199","folder":"Addendum to Specifications and Drawings dated 5/4/1998","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[31,39],"text":"Drawings"}]}},"ordinal":2904,"pages":6,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000173363","folder":"Addendum to Specifications and Drawings dated 5/4/98","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[31,39],"text":"Drawings"}]}},"ordinal":2905,"pages":6,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000172329","folder":"Architect or Engineers Drawing No. M1.01, M1.07, M14.01, M123","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[23,30],"text":"Drawing"}]}},"ordinal":2940,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":10,"first_bates":"NYC-WTC_000166752","folder":"Architectural Sketch Log","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[14,20],"text":"Sketch"}]}},"ordinal":2941,"pages":18,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000173739","folder":"Architecturl Sketch Log","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[13,19],"text":"Sketch"}]}},"ordinal":2942,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000167926","folder":"Bullet Resisting Door Systems®Bullet Resisting Fixed Windows and Framing Systems","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[65,72],"text":"Framing"}]}},"ordinal":2967,"pages":2,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000168094","folder":"Drawing Plan Section","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[0,7],"text":"Drawing"}]}},"ordinal":3135,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000167874","folder":"Drawings","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[0,8],"text":"Drawings"}]}},"ordinal":3136,"pages":3,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000168096","folder":"Drawings for your P.O.#2219","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[0,8],"text":"Drawings"}]}},"ordinal":3137,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000166827","folder":"Eng. Sketches","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[5,13],"text":"Sketches"}]}},"ordinal":3159,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000166842","folder":"Example of beam mounted antenna monopole for multiple antennae","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[11,15],"text":"beam"}]}},"ordinal":3164,"pages":4,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000167801","folder":"FINAL DRAWINGS","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[6,14],"text":"DRAWINGS"}]}},"ordinal":3171,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000167881","folder":"FSK-43 & FSK-45AND LOUVER SHOP DRAWINGS.","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[31,39],"text":"DRAWINGS"}]}},"ordinal":3177,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000172233","folder":"Fuel Line Enclosure Framing Plan","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[20,27],"text":"Framing"}]}},"ordinal":3195,"pages":2,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000172319","folder":"List of Drawings","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[8,16],"text":"Drawings"}]}},"ordinal":3272,"pages":4,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000173192","folder":"List of Drawings Addendum #1","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[8,16],"text":"Drawings"}]}},"ordinal":3273,"pages":4,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000167669","folder":"List of Drawings Issued for Bulletin # 1","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[8,16],"text":"Drawings"}]}},"ordinal":3274,"pages":4,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000173834","folder":"Mayor's O.E.M.®7 World Trade Center Shop Drawings Job # 1854","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[41,49],"text":"Drawings"}]}},"ordinal":3354,"pages":2,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":3,"first_bates":"NYC-WTC_000167235","folder":"Mayor's Office of Emergency Management 7 World Trade Center, 23rd Floor Structural Engineering Services","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[72,82],"text":"Structural"}]}},"ordinal":3646,"pages":6,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000167655","folder":"Mayor's Office of Emergency Management Drawings","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[39,47],"text":"Drawings"}]}},"ordinal":3654,"pages":4,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000172204","folder":"New Closet as per Sketch FSK-44","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[18,24],"text":"Sketch"}]}},"ordinal":3804,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000172268","folder":"Novalink shop drawings","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[14,22],"text":"drawings"}]}},"ordinal":3816,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000171312","folder":"Project OEM®Location 7 WTC®Fuel Oil Piping on 1st floor","input":"folder-document-locator/folders.json","matches":{"folder":{"first_floor":[{"span":[46,55],"text":"1st floor"}]}},"ordinal":3975,"pages":1,"predicates":["first_floor"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000167918","folder":"REQUESTED DRAWING","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[10,17],"text":"DRAWING"}]}},"ordinal":4024,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":4,"first_bates":"NYC-WTC_000166710","folder":"RFI Log®Architectural Sketch Log","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[22,28],"text":"Sketch"}]}},"ordinal":4029,"pages":26,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000174143","folder":"Requested Drawing®As Per Your Request","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[10,17],"text":"Drawing"}]}},"ordinal":4051,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000171459","folder":"Revised Per Sketch Dated 1/21/99®Change Order #1®Mayor's Office of Emergency Management®7 World Trade Center - 23rd Floor","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[12,18],"text":"Sketch"}]}},"ordinal":4057,"pages":4,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000171807","folder":"SK'S FOR PENETRATION AT BEAMS ON 7TH. FLOOR AS PER YOUR REQUEST.","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[9,20],"text":"PENETRATION"},{"span":[24,29],"text":"BEAMS"}]}},"ordinal":4073,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000168697","folder":"Shop Drawings Job # 1854","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[5,13],"text":"Drawings"}]}},"ordinal":4095,"pages":1,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000171851","folder":"The Cantor Seinuk Group P.C. First Floor - rebars","input":"folder-document-locator/folders.json","matches":{"folder":{"first_floor":[{"span":[29,40],"text":"First Floor"}]}},"ordinal":4126,"pages":1,"predicates":["first_floor"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000171853","folder":"The Cantor Seinuk Group P.C. First floor - rebars","input":"folder-document-locator/folders.json","matches":{"folder":{"first_floor":[{"span":[29,40],"text":"First floor"}]}},"ordinal":4127,"pages":1,"predicates":["first_floor"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000171390","folder":"Work Order®7 W. T. C.®1st Floor","input":"folder-document-locator/folders.json","matches":{"folder":{"first_floor":[{"span":[22,31],"text":"1st Floor"}]}},"ordinal":4163,"pages":1,"predicates":["first_floor"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000173900","folder":"fsk-58 revised as per structural engineer comments for your use.","input":"folder-document-locator/folders.json","matches":{"folder":{"structural_context":[{"span":[22,32],"text":"structural"}]}},"ordinal":4191,"pages":2,"predicates":["structural_context"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
{"box":"7DCAS","category":"lower-specificity context lead","documents":1,"first_bates":"NYC-WTC_000171752","folder":"provide demo & temp lt & power for fuel oil piping on 1st floor","input":"folder-document-locator/folders.json","matches":{"folder":{"first_floor":[{"span":[54,63],"text":"1st floor"}]}},"ordinal":4195,"pages":1,"predicates":["first_floor"],"source":"WTC 7","source_index":2,"source_scope":"WTC 7"}
```

## Complete response match occurrences

Repeated query appearances remain explicit. The supplied result ID and selected
property strings are preserved without normalizing labels or substituting None.
The extra agency/production identifiers are locator metadata, not independent sources.

```json
{"category":"lower-specificity context lead","id":"september11 Connector:September11_MD:NYC-WTC_000167874:","input":"drawing-locator/skp4-response.json","matches":{"folder_name":{"structural_context":[{"span":[0,8],"text":"Drawings"}]}},"ordinal":7,"predicates":["structural_context"],"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Drawings"},"mes:key":{"present":true,"value":"NYC-WTC_000167874"},"page_count":{"present":true,"value":"3"},"production_end":{"present":true,"value":"NYC-WTC_000167876"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000167874.pdf"}},"source_scope":"WTC 7"}
{"category":"lower-specificity context lead","id":"september11 Connector:September11_MD:NYC-WTC_000173670:","input":"drawing-locator/sts7-response.json","matches":{"folder_name":{"structural_context":[{"span":[14,20],"text":"Sketch"}]}},"ordinal":3,"predicates":["structural_context"],"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Architectural Sketch Log"},"mes:key":{"present":true,"value":"NYC-WTC_000173670"},"page_count":{"present":true,"value":"1"},"production_end":{"present":true,"value":"NYC-WTC_000173670"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000173670.pdf"}},"source_scope":"WTC 7"}
{"category":"lower-specificity context lead","id":"september11 Connector:September11_MD:NYC-WTC_000167235:","input":"folder-document-locator/structural-front-response.json","matches":{"folder_name":{"structural_context":[{"span":[72,82],"text":"Structural"}]}},"ordinal":1,"predicates":["structural_context"],"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Mayor's Office of Emergency Management 7 World Trade Center, 23rd Floor Structural Engineering Services"},"mes:key":{"present":true,"value":"NYC-WTC_000167235"},"page_count":{"present":true,"value":"2"},"production_end":{"present":true,"value":"NYC-WTC_000167236"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000167235.pdf"}},"source_scope":"WTC 7"}
{"category":"lower-specificity context lead","id":"september11 Connector:September11_MD:NYC-WTC_000167240:","input":"folder-document-locator/structural-front-response.json","matches":{"folder_name":{"structural_context":[{"span":[72,82],"text":"Structural"}]}},"ordinal":2,"predicates":["structural_context"],"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Mayor's Office of Emergency Management 7 World Trade Center, 23rd Floor Structural Engineering Services"},"mes:key":{"present":true,"value":"NYC-WTC_000167240"},"page_count":{"present":true,"value":"2"},"production_end":{"present":true,"value":"NYC-WTC_000167241"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000167240.pdf"}},"source_scope":"WTC 7"}
{"category":"lower-specificity context lead","id":"september11 Connector:September11_MD:NYC-WTC_000167759:","input":"folder-document-locator/structural-front-response.json","matches":{"folder_name":{"structural_context":[{"span":[72,82],"text":"Structural"}]}},"ordinal":3,"predicates":["structural_context"],"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Mayor's Office of Emergency Management 7 World Trade Center, 23rd Floor Structural Engineering Services"},"mes:key":{"present":true,"value":"NYC-WTC_000167759"},"page_count":{"present":true,"value":"2"},"production_end":{"present":true,"value":"NYC-WTC_000167760"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000167759.pdf"}},"source_scope":"WTC 7"}
{"category":"lower-specificity context lead","id":"september11 Connector:September11_MD:NYC-WTC_000167235:","input":"folder-document-locator/structural-response.json","matches":{"folder_name":{"structural_context":[{"span":[72,82],"text":"Structural"}]}},"ordinal":1,"predicates":["structural_context"],"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Mayor's Office of Emergency Management 7 World Trade Center, 23rd Floor Structural Engineering Services"},"mes:key":{"present":true,"value":"NYC-WTC_000167235"},"page_count":{"present":true,"value":"2"},"production_end":{"present":true,"value":"NYC-WTC_000167236"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000167235.pdf"}},"source_scope":"WTC 7"}
{"category":"lower-specificity context lead","id":"september11 Connector:September11_MD:NYC-WTC_000167240:","input":"folder-document-locator/structural-response.json","matches":{"folder_name":{"structural_context":[{"span":[72,82],"text":"Structural"}]}},"ordinal":2,"predicates":["structural_context"],"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Mayor's Office of Emergency Management 7 World Trade Center, 23rd Floor Structural Engineering Services"},"mes:key":{"present":true,"value":"NYC-WTC_000167240"},"page_count":{"present":true,"value":"2"},"production_end":{"present":true,"value":"NYC-WTC_000167241"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000167240.pdf"}},"source_scope":"WTC 7"}
{"category":"lower-specificity context lead","id":"september11 Connector:September11_MD:NYC-WTC_000167759:","input":"folder-document-locator/structural-response.json","matches":{"folder_name":{"structural_context":[{"span":[72,82],"text":"Structural"}]}},"ordinal":3,"predicates":["structural_context"],"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Mayor's Office of Emergency Management 7 World Trade Center, 23rd Floor Structural Engineering Services"},"mes:key":{"present":true,"value":"NYC-WTC_000167759"},"page_count":{"present":true,"value":"2"},"production_end":{"present":true,"value":"NYC-WTC_000167760"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000167759.pdf"}},"source_scope":"WTC 7"}
{"category":"lower-specificity context lead","id":"september11 Connector:September11_MD:NYC-WTC_000166842:","input":"job1854-followup-locator/penn-response.json","matches":{"folder_name":{"structural_context":[{"span":[11,15],"text":"beam"}]}},"ordinal":14,"predicates":["structural_context"],"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Example of beam mounted antenna monopole for multiple antennae"},"mes:key":{"present":true,"value":"NYC-WTC_000166842"},"page_count":{"present":true,"value":"4"},"production_end":{"present":true,"value":"NYC-WTC_000166845"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000166842.pdf"}},"source_scope":"WTC 7"}
{"category":"lower-specificity context lead","id":"september11 Connector:September11_MD:NYC-WTC_000168697:","input":"job1854-followup-locator/penn-response.json","matches":{"folder_name":{"structural_context":[{"span":[5,13],"text":"Drawings"}]}},"ordinal":27,"predicates":["structural_context"],"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Shop Drawings Job # 1854"},"mes:key":{"present":true,"value":"NYC-WTC_000168697"},"page_count":{"present":true,"value":"1"},"production_end":{"present":true,"value":"NYC-WTC_000168697"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000168697.pdf"}},"source_scope":"WTC 7"}
{"category":"lower-specificity context lead","id":"september11 Connector:September11_MD:NYC-WTC_000173834:","input":"job1854-followup-locator/penn-response.json","matches":{"folder_name":{"structural_context":[{"span":[41,49],"text":"Drawings"}]}},"ordinal":45,"predicates":["structural_context"],"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Mayor's O.E.M.®7 World Trade Center Shop Drawings Job # 1854"},"mes:key":{"present":true,"value":"NYC-WTC_000173834"},"page_count":{"present":true,"value":"2"},"production_end":{"present":true,"value":"NYC-WTC_000173835"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000173834.pdf"}},"source_scope":"WTC 7"}
```

## Exact coverage controls

Controls compare exact `NYC-WTC_000<ID>` first_bates/mes:key values, independently
of the text predicates. 166828 appears at catalog row 3653 and drawing/sts7 result 1;
173199 at catalog row 2904 but no response occurrence; 173529 at catalog row 2836
but no response occurrence; 173670 has no catalog first_bates row and occurs at
drawing/sts7 result 3. The latter's exact context joins catalog row 2941 whose first
Bates is 166752; that does not establish full group membership from an aggregate row.
Control absence is a bounded metadata-coverage limit, not evidence the historical
record did not exist. Earlier content roles were supplied by the protocol and
were not re-read or independently established here.

```json
{"166828":{"catalog":[{"box":"7DCAS","documents":1,"first_bates":"NYC-WTC_000166828","folder":"Mayor's Office of Emergency Management Alt. Route for Oil Pipes","input":"folder-document-locator/folders.json","ordinal":3653,"pages":8,"source":"WTC 7","source_index":2}],"responses":[{"id":"september11 Connector:September11_MD:NYC-WTC_000166828:","input":"drawing-locator/sts7-response.json","ordinal":1,"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Mayor's Office of Emergency Management Alt. Route for Oil Pipes"},"mes:key":{"present":true,"value":"NYC-WTC_000166828"},"page_count":{"present":true,"value":"8"},"production_end":{"present":true,"value":"NYC-WTC_000166835"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000166828.pdf"}}}]},"173199":{"catalog":[{"box":"7DCAS","documents":1,"first_bates":"NYC-WTC_000173199","folder":"Addendum to Specifications and Drawings dated 5/4/1998","input":"folder-document-locator/folders.json","ordinal":2904,"pages":6,"source":"WTC 7","source_index":2}],"responses":[]},"173529":{"catalog":[{"box":"7DCAS","documents":1,"first_bates":"NYC-WTC_000173529","folder":"7 World Trade Center, Manhattan Freedom of Information Request","input":"folder-document-locator/folders.json","ordinal":2836,"pages":10,"source":"WTC 7","source_index":2}],"responses":[]},"173670":{"catalog":[],"responses":[{"id":"september11 Connector:September11_MD:NYC-WTC_000173670:","input":"drawing-locator/sts7-response.json","ordinal":3,"properties":{"agency":{"present":true,"value":"Citywide Administrative Services, Dept. of"},"box_name":{"present":true,"value":"7DCAS"},"folder_name":{"present":true,"value":"Architectural Sketch Log"},"mes:key":{"present":true,"value":"NYC-WTC_000173670"},"page_count":{"present":true,"value":"1"},"production_end":{"present":true,"value":"NYC-WTC_000173670"},"production_volume":{"present":true,"value":"NYC-WTC0007"},"source":{"present":true,"value":"WTC 7"},"title":{"present":true,"value":"NYC-WTC_000173670.pdf"}}}]}}
```

## Exact context joins and conflicts

Each entry is a unique supplied response ID. A null row-ordinal field means the
source/box/folder context is incomplete; it is not a fabricated label.

```json
{"catalog_row_ordinals":[4075],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167873:"}
{"catalog_row_ordinals":[2964],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171286:"}
{"catalog_row_ordinals":[3694],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171620:"}
{"catalog_row_ordinals":[3329],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172947:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172953:"}
{"catalog_row_ordinals":[2759],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171840:"}
{"catalog_row_ordinals":[3053],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173920:"}
{"catalog_row_ordinals":[2963],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173949:"}
{"catalog_row_ordinals":[2963],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000174004:"}
{"catalog_row_ordinals":[4142],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167170:"}
{"catalog_row_ordinals":[4142],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171802:"}
{"catalog_row_ordinals":[2870],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168581:"}
{"catalog_row_ordinals":[2649],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168580:"}
{"catalog_row_ordinals":[3136],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167874:"}
{"catalog_row_ordinals":[3653],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000166828:"}
{"catalog_row_ordinals":[2941],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173670:"}
{"catalog_row_ordinals":[3190],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171300:"}
{"catalog_row_ordinals":[3190],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171557:"}
{"catalog_row_ordinals":[3646],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167235:"}
{"catalog_row_ordinals":[3646],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167240:"}
{"catalog_row_ordinals":[3646],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167759:"}
{"catalog_row_ordinals":[3673],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171252:"}
{"catalog_row_ordinals":[3400],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172539:"}
{"catalog_row_ordinals":[3400],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172543:"}
{"catalog_row_ordinals":[3400],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000174096:"}
{"catalog_row_ordinals":[3400],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172389:"}
{"catalog_row_ordinals":[3948],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168654:"}
{"catalog_row_ordinals":[2833],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172395:"}
{"catalog_row_ordinals":[3154],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172397:"}
{"catalog_row_ordinals":[3210],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173715:"}
{"catalog_row_ordinals":[3572],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173121:"}
{"catalog_row_ordinals":[3572],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173319:"}
{"catalog_row_ordinals":[3303],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000166707:"}
{"catalog_row_ordinals":[3303],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173688:"}
{"catalog_row_ordinals":[2925],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173115:"}
{"catalog_row_ordinals":[3098],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171251:"}
{"catalog_row_ordinals":[3097],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172977:"}
{"catalog_row_ordinals":[3432],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168653:"}
{"catalog_row_ordinals":[2794],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168652:"}
{"catalog_row_ordinals":[3432],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171981:"}
{"catalog_row_ordinals":[3572],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172123:"}
{"catalog_row_ordinals":[3687],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172316:"}
{"catalog_row_ordinals":[3097],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172976:"}
{"catalog_row_ordinals":[3572],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173073:"}
{"catalog_row_ordinals":[2593],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173103:"}
{"catalog_row_ordinals":[4091],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173226:"}
{"catalog_row_ordinals":[3650],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173352:"}
{"catalog_row_ordinals":[3650],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173355:"}
{"catalog_row_ordinals":[3534],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173709:"}
{"catalog_row_ordinals":[2666],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173708:"}
{"catalog_row_ordinals":[3101],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172523:"}
{"catalog_row_ordinals":[3687],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172627:"}
{"catalog_row_ordinals":[3577],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173147:"}
{"catalog_row_ordinals":[3087],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173162:"}
{"catalog_row_ordinals":[2953],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172283:"}
{"catalog_row_ordinals":[4091],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173231:"}
{"catalog_row_ordinals":[4091],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173236:"}
{"catalog_row_ordinals":[3594],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172388:"}
{"catalog_row_ordinals":[3594],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172538:"}
{"catalog_row_ordinals":[3594],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172542:"}
{"catalog_row_ordinals":[3594],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000174095:"}
{"catalog_row_ordinals":[3209],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000166874:"}
{"catalog_row_ordinals":[4205],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168718:"}
{"catalog_row_ordinals":[3989],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000166571:"}
{"catalog_row_ordinals":[4203],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000166488:"}
{"catalog_row_ordinals":[2880],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169609:"}
{"catalog_row_ordinals":[2880],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169723:"}
{"catalog_row_ordinals":[2880],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169837:"}
{"catalog_row_ordinals":[2880],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169936:"}
{"catalog_row_ordinals":[2880],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000170060:"}
{"catalog_row_ordinals":[2880],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000170296:"}
{"catalog_row_ordinals":[3241],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173734:"}
{"catalog_row_ordinals":[3241],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171358:"}
{"catalog_row_ordinals":[4094],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172975:"}
{"catalog_row_ordinals":[2574],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173500:"}
{"catalog_row_ordinals":[2576],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000174100:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171237:"}
{"catalog_row_ordinals":[2892],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171241:"}
{"catalog_row_ordinals":[2605],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173014:"}
{"catalog_row_ordinals":[4138],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173494:"}
{"catalog_row_ordinals":[2605],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173495:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171707:"}
{"catalog_row_ordinals":[3828],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172972:"}
{"catalog_row_ordinals":[3885],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172973:"}
{"catalog_row_ordinals":[2605],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173489:"}
{"catalog_row_ordinals":[2880],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167029:"}
{"catalog_row_ordinals":[2947],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167056:"}
{"catalog_row_ordinals":[2840],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169815:"}
{"catalog_row_ordinals":[3251],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169821:"}
{"catalog_row_ordinals":[2946],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000170182:"}
{"catalog_row_ordinals":[2880],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000170238:"}
{"catalog_row_ordinals":[2880],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000170192:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000170436:"}
{"catalog_row_ordinals":[2840],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171263:"}
{"catalog_row_ordinals":[2838],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171788:"}
{"catalog_row_ordinals":[2838],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171793:"}
{"catalog_row_ordinals":[2614],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172527:"}
{"catalog_row_ordinals":[2839],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172561:"}
{"catalog_row_ordinals":[2839],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172566:"}
{"catalog_row_ordinals":[2840],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173911:"}
{"catalog_row_ordinals":[2838],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000174040:"}
{"catalog_row_ordinals":[2838],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000174043:"}
{"catalog_row_ordinals":[2838],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000174046:"}
{"catalog_row_ordinals":[4093],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167259:"}
{"catalog_row_ordinals":[2880],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000170577:"}
{"catalog_row_ordinals":[3252],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000170445:"}
{"catalog_row_ordinals":[3736],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167191:"}
{"catalog_row_ordinals":[3921],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167253:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167537:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167556:"}
{"catalog_row_ordinals":[3349],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167648:"}
{"catalog_row_ordinals":[3710],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168334:"}
{"catalog_row_ordinals":[3723],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167719:"}
{"catalog_row_ordinals":[3982],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167934:"}
{"catalog_row_ordinals":[4184],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167845:"}
{"catalog_row_ordinals":[3657],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167941:"}
{"catalog_row_ordinals":[3999],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000170888:"}
{"catalog_row_ordinals":[3189],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171284:"}
{"catalog_row_ordinals":[3946],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171432:"}
{"catalog_row_ordinals":[3189],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171491:"}
{"catalog_row_ordinals":[3946],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171535:"}
{"catalog_row_ordinals":[3128],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171597:"}
{"catalog_row_ordinals":[2588],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171698:"}
{"catalog_row_ordinals":[3191],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172489:"}
{"catalog_row_ordinals":[3188],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172616:"}
{"catalog_row_ordinals":[2893],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172760:"}
{"catalog_row_ordinals":[2893],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172758:"}
{"catalog_row_ordinals":[3657],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173794:"}
{"catalog_row_ordinals":null,"context_complete":false,"id":"september11 Connector:September11_MD:NYC-WTC_000165940:"}
{"catalog_row_ordinals":null,"context_complete":false,"id":"september11 Connector:September11_MD:NYC-WTC_000165962:"}
{"catalog_row_ordinals":null,"context_complete":false,"id":"september11 Connector:September11_MD:NYC-WTC_000166093:"}
{"catalog_row_ordinals":null,"context_complete":false,"id":"september11 Connector:September11_MD:NYC-WTC_000166099:"}
{"catalog_row_ordinals":[4071],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172166:"}
{"catalog_row_ordinals":[3007],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173547:"}
{"catalog_row_ordinals":[4028],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173607:"}
{"catalog_row_ordinals":[4028],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173761:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167584:"}
{"catalog_row_ordinals":[4153],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168166:"}
{"catalog_row_ordinals":[4204],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169180:"}
{"catalog_row_ordinals":[3827],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171520:"}
{"catalog_row_ordinals":[4156],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172449:"}
{"catalog_row_ordinals":[4009],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172450:"}
{"catalog_row_ordinals":[3604],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171905:"}
{"catalog_row_ordinals":[3848],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171909:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167344:"}
{"catalog_row_ordinals":[2957],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171020:"}
{"catalog_row_ordinals":[3638],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173358:"}
{"catalog_row_ordinals":[2958],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000170925:"}
{"catalog_row_ordinals":[3516],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168696:"}
{"catalog_row_ordinals":[3517],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173833:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167385:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167590:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168065:"}
{"catalog_row_ordinals":[2796],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168701:"}
{"catalog_row_ordinals":[2787],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172110:"}
{"catalog_row_ordinals":[2614],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172381:"}
{"catalog_row_ordinals":[2614],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172594:"}
{"catalog_row_ordinals":[2692],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173184:"}
{"catalog_row_ordinals":[2614],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000174093:"}
{"catalog_row_ordinals":[3082],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171242:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000170817:"}
{"catalog_row_ordinals":[3144],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167735:"}
{"catalog_row_ordinals":[3877],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167322:"}
{"catalog_row_ordinals":[3877],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167732:"}
{"catalog_row_ordinals":[3399],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172731:"}
{"catalog_row_ordinals":null,"context_complete":false,"id":"september11 Connector:September11_MD:NYC-WTC_000166345:"}
{"catalog_row_ordinals":[4090],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172958:"}
{"catalog_row_ordinals":[2881],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173952:"}
{"catalog_row_ordinals":null,"context_complete":false,"id":"september11 Connector:September11_MD:NYC-WTC_000166386:"}
{"catalog_row_ordinals":[3824],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172103:"}
{"catalog_row_ordinals":[3308],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000166769:"}
{"catalog_row_ordinals":[3164],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000166842:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167339:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167380:"}
{"catalog_row_ordinals":[2890],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167482:"}
{"catalog_row_ordinals":[2890],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167499:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167517:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167570:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167554:"}
{"catalog_row_ordinals":[3412],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167698:"}
{"catalog_row_ordinals":[2596],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167896:"}
{"catalog_row_ordinals":[3131],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168221:"}
{"catalog_row_ordinals":[4095],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000168697:"}
{"catalog_row_ordinals":[4204],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169034:"}
{"catalog_row_ordinals":[4204],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169030:"}
{"catalog_row_ordinals":[4204],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169096:"}
{"catalog_row_ordinals":[4204],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169051:"}
{"catalog_row_ordinals":[4204],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169072:"}
{"catalog_row_ordinals":[3347],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171485:"}
{"catalog_row_ordinals":[3912],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000171884:"}
{"catalog_row_ordinals":[3412],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172135:"}
{"catalog_row_ordinals":[3824],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172275:"}
{"catalog_row_ordinals":[3169],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172347:"}
{"catalog_row_ordinals":[2953],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172440:"}
{"catalog_row_ordinals":[3758],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173248:"}
{"catalog_row_ordinals":[3926],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173710:"}
{"catalog_row_ordinals":[3308],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173798:"}
{"catalog_row_ordinals":[3354],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173834:"}
{"catalog_row_ordinals":[3915],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000173926:"}
{"catalog_row_ordinals":[3824],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000174139:"}
{"catalog_row_ordinals":null,"context_complete":false,"id":"september11 Connector:September11_MD:NYC-WTC_000166435:"}
{"catalog_row_ordinals":[3959],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000166535:"}
{"catalog_row_ordinals":[3807],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167359:"}
{"catalog_row_ordinals":[3412],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167822:"}
{"catalog_row_ordinals":[3348],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000172371:"}
{"catalog_row_ordinals":[3648],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000167866:"}
{"catalog_row_ordinals":null,"context_complete":false,"id":"september11 Connector:September11_MD:NYC-WTC_000166426:"}
{"catalog_row_ordinals":[4204],"context_complete":true,"id":"september11 Connector:September11_MD:NYC-WTC_000169094:"}
```

Supplied-property/location conflict list: `[]`.

## Reproducible final independent command body

The final stdout-only body below includes the exact pins, expressions, rejection
checks, controls, complete-hit collection and before/after pin checks. No root
query/result is read. To replay, use the Python invocation given above; it writes
only to stdout. Source data remain authoritative over this derived receipt.

```python
from pathlib import Path
from collections import Counter, defaultdict
import json, re, hashlib, time, datetime
BASE=Path("/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation")
M=BASE/"municipal-originals-2026-10-04"
PROTOCOL=BASE/"municipal-first-floor-locator-2026-10-05/PROTOCOL.md"
EXPECTED=json.loads("[{\"path\":\"folder-document-locator/folders.json\",\"bytes\":421135,\"sha256\":\"cf3afa33cc58a0f2a9d48e6fbac57cdd8bb060b046cf5373d261d37bb976b704\"},{\"path\":\"drawing-locator/control-response.json\",\"bytes\":8451,\"sha256\":\"fdf92a229791be47e9ca997939bc9df8f9543fa4eb7764c3bb3c1770a52ae57b\"},{\"path\":\"drawing-locator/skp3-response.json\",\"bytes\":22502,\"sha256\":\"a13e7e290cd0e625db4502ec4197389c1c549b138b48502c2daebc00c62a3a26\"},{\"path\":\"drawing-locator/skp4-response.json\",\"bytes\":21189,\"sha256\":\"e4848f93061aaf339bdfb006fce212f95805298ba24fe60e8e1d2fbcb6be9a0b\"},{\"path\":\"drawing-locator/sts7-response.json\",\"bytes\":10553,\"sha256\":\"639d3c9f00b00acbdf613525c3ffa27b6f2e3190a1b566269a003d59424b41c7\"},{\"path\":\"folder-document-locator/sprinkler-front-response.json\",\"bytes\":9587,\"sha256\":\"61f3eb3219955a11c9648fb50b8603e98e7de0ca99d15f230cc1eb4ad2beec13\"},{\"path\":\"folder-document-locator/sprinkler-response.json\",\"bytes\":9587,\"sha256\":\"05d526268ba8ae78cb90c6a507d5076b29980ef920a7954c01e080e5470a470f\"},{\"path\":\"folder-document-locator/structural-front-response.json\",\"bytes\":11120,\"sha256\":\"858004f96f45f33ac637a6ae7d84cf7b6e4c8c6750df285b316b37eef77c913a\"},{\"path\":\"folder-document-locator/structural-response.json\",\"bytes\":11186,\"sha256\":\"470c1b10d25218dcf05319199591bea8f906b178e05d92f78711622e70fe247a\"},{\"path\":\"test-acceptance-locator/control-response.json\",\"bytes\":8451,\"sha256\":\"7386207c519d9144fc0a2b9e6092351a41ba38059f2008e8156d4ed0686f6a29\"},{\"path\":\"test-acceptance-locator/date-response.json\",\"bytes\":1760,\"sha256\":\"ea21d260015169581e7b80212786e6be4aeb7abd6ea8c821a555998ba89a2e4f\"},{\"path\":\"test-acceptance-locator/generator-response.json\",\"bytes\":66134,\"sha256\":\"bf13d5608fc49e3da64b3291b2779ddfd64692e05ae7c7fa063a9d7e2afd3186\"},{\"path\":\"test-acceptance-locator/punch-response.json\",\"bytes\":65056,\"sha256\":\"cd6bfc2d72090d0dcd33cf8b014d4be63ae4b05d71ace3de66700cfa45f6b73d\"},{\"path\":\"test-acceptance-locator/signoff-response.json\",\"bytes\":30480,\"sha256\":\"42c16897153f26bb0a0844f6693cd5cac3818a9dbd6e8acb85563a2616a5e6eb\"},{\"path\":\"job1854-followup-locator/apt-response.json\",\"bytes\":28606,\"sha256\":\"edca6e7e2e4ce1fe9597e02ad43d73638e8c9143e2add8e2c6460f8fccefd7cc\"},{\"path\":\"job1854-followup-locator/break_glass-response.json\",\"bytes\":16556,\"sha256\":\"440be5766c79591ae7dae03a1f3778e8330c75350f6cc611ebf70266dd0e7ae4\"},{\"path\":\"job1854-followup-locator/control-response.json\",\"bytes\":8451,\"sha256\":\"bbdeb6f33a4e8d937d9b13e666f226b6fee5bfbdbf436763bfce250f864ca80a\"},{\"path\":\"job1854-followup-locator/date_slash-response.json\",\"bytes\":17739,\"sha256\":\"4bc4695cb8e94616475a92f75b1cd748c4bfd25e0947696db73e04bb517f51de\"},{\"path\":\"job1854-followup-locator/date_words-response.json\",\"bytes\":29768,\"sha256\":\"c062562ca7eb8931edd58ebefb9a29c5ef369ec75ffae98e98130860fc3dd2db\"},{\"path\":\"job1854-followup-locator/fuel_pump-response.json\",\"bytes\":17729,\"sha256\":\"75efcf4871d44c4e20b85fa3f1dd812b092c20b8257a36d43e986fe0f909ee72\"},{\"path\":\"job1854-followup-locator/load_shedding-response.json\",\"bytes\":15507,\"sha256\":\"921d6ab1d95e67be18399c36e4931c98a6af842f5195266fb18a5b9a71f390bf\"},{\"path\":\"job1854-followup-locator/penn-response.json\",\"bytes\":64684,\"sha256\":\"1202cd667c7ce002ff231ef4b2e9460f01795b9b054a3dd935b2f131fac8efce\"},{\"path\":\"job1854-followup-locator/penn_phrase-response.json\",\"bytes\":26105,\"sha256\":\"54457b9032d4d1783ee38c5a9a2bd6b043ccc0334035af855928ef0c6acf3283\"},{\"path\":\"job1854-followup-locator/transient-response.json\",\"bytes\":11619,\"sha256\":\"37b9ecb12c0a722caf551f42398af6d80d336ea1bf92ad9100e981d4a0289ae3\"}]")
PROTOCOL_SHA="d11b4009d5d88549cb48339cda373b156f50f97e64da5728c839084bc65c104f"
PATTERNS={
"sheet":r"(?<![A-Za-z0-9])(?:SKS[\s._–-]*S[\s._–-]*[12]|S[\s._–-]*S[\s._–-]*1|S[\s._–-]*1)(?![A-Za-z0-9])",
"first_floor":r"(?<![A-Za-z0-9])(?:first|1st)[\s._–-]*(?:floor|fl)(?![A-Za-z0-9])",
"structural_context":r"(?<![A-Za-z0-9])(?:structural|framing|beams?|notch(?:es|ed|ing)?|penetrations?|drawings?|sketch(?:es)?)(?![A-Za-z0-9])"}
RX={k:re.compile(v,re.I) for k,v in PATTERNS.items()}
def unique_pairs(pairs):
 d={}
 for k,v in pairs:
  if k in d: raise ValueError("duplicate JSON key")
  d[k]=v
 return d
def strict_load(b):
 return json.loads(b,object_pairs_hook=unique_pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError("nonfinite constant")))
def propmap(row):
 d={}
 for p in row["properties"]:
  if p["id"] in d: raise ValueError("duplicate property id")
  d[p["id"]]=p
 return d
def scalar(pm,key,required=False):
 if key not in pm:
  if required: raise ValueError("required property absent")
  return {"present":False}
 data=pm[key].get("data")
 if not isinstance(data,list) or len(data)!=1: raise ValueError("not exactly one data item")
 item=data[0]
 if not isinstance(item,dict) or set(item)!={"value"}: raise ValueError("malformed property data item")
 value=item["value"]
 if not isinstance(value,dict) or set(value)!={"str"} or not isinstance(value["str"],str): raise ValueError("not scalar string")
 return {"present":True,"value":value["str"]}
def scan(fields):
 return {field:{k:[{"text":m.group(),"span":list(m.span())} for m in rx.finditer(v)] for k,rx in RX.items() if rx.search(v)} for field,v in fields.items() if any(rx.search(v) for rx in RX.values())}
def classify(matches,source):
 kinds={k for val in matches.values() for k in val}
 category="sheet-token lead" if "sheet" in kinds else "subject lead" if {"first_floor","structural_context"}<=kinds else "lower-specificity context lead"
 return {"source_scope":"WTC 7" if source=="WTC 7" else "off-source","category":category,"predicates":sorted(kinds)}
def validate_row(row):
 if not isinstance(row,list) or len(row)!=6: raise ValueError("malformed catalog row width")
def expect_reject(fn):
 try: fn()
 except (ValueError,TypeError,KeyError): return True
 return False
tests=[]
def test(name,condition):
 tests.append({"test":name,"pass":bool(condition)})
 if not condition: raise AssertionError(name)
positive=["S-1","s_1","S.S.1","SKS-S-1","SKS S 2","S–S–1","A-S-1","S-1.1","S-1-1","XS-S-1"]
negative=["AS-1","S-10","S-1A","S-2","S/S/1"]
for value in positive: test("sheet positive "+value,bool(RX["sheet"].search(value)))
for value in negative: test("sheet negative "+value,not RX["sheet"].search(value))
for value in ["First Floor","1st-fl","first_floor"]: test("floor positive "+value,bool(RX["first_floor"].search(value)))
for value in ["first floorboard","21st floor","first floors"]: test("floor negative "+value,not RX["first_floor"].search(value))
for value in ["beam","beams","notch","notches","notched","notching","drawings","sketches","penetrations"]: test("structural positive "+value,bool(RX["structural_context"].search(value)))
for value in ["notchingX","beamline","redrawing"]: test("structural negative "+value,not RX["structural_context"].search(value))
synthetic={"title":"Routine","folder_name":"Routine","search_request":{"query":"S-1 first floor beam"},"facet":"S-1","paging_state":"S-1"}
test("field isolation: unselected echo/facet/paging ignored",scan({k:synthetic[k] for k in ["title","folder_name"]})=={})
test("duplicate JSON keys rejected",expect_reject(lambda:strict_load('{"x":1,"x":2}')))
test("duplicate property ids rejected",expect_reject(lambda:propmap({"properties":[{"id":"title"},{"id":"title"}]})))
for data in [[],[{"value":{"str":"S-1"}},{"value":{"str":"S-1"}}],[{"value":{"num":1}}],[{"value":{"str":["S-1"]}}]]:
 test("invalid selected property rejected "+str(len(data)),expect_reject(lambda data=data:scalar({"title":{"data":data}},"title")))
test("malformed row width rejected",expect_reject(lambda:validate_row([0,"box"])))
test("missing distinct from literal None",scalar({},"folder_name")=={"present":False} and scalar({"folder_name":{"data":[{"value":{"str":"None"}}]}},"folder_name")=={"present":True,"value":"None"})
test("occurrence versus ID accounting",len(["a","a","b"])==3 and len(set(["a","a","b"]))==2)
t0=time.monotonic(); start=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()==PROTOCOL_SHA,"protocol changed"
data={x["path"]:(M/x["path"]).read_bytes() for x in EXPECTED}
for x in EXPECTED:
 assert len(data[x["path"]])==x["bytes"] and hashlib.sha256(data[x["path"]]).hexdigest()==x["sha256"],"input pin changed"
docs={k:strict_load(v) for k,v in data.items()}
cat=docs["folder-document-locator/folders.json"]
assert cat["columns"]==["source_index","box","folder","documents","pages","first_bates"]
catalog_hits=[]; response_hits=[]; controls={n:{"catalog":[],"responses":[]} for n in ["166828","173199","173529","173670"]}
all_by_id=defaultdict(list); occurrences=0; properties_missing=Counter(); literal_none=Counter(); pagination=[]
def catrecord(n,row):
 return {"input":"folder-document-locator/folders.json","ordinal":n,"source_index":row[0],"source":cat["sources"][row[0]],"box":row[1],"folder":row[2],"documents":row[3],"pages":row[4],"first_bates":row[5]}
for n,row in enumerate(cat["rows"],1):
 validate_row(row)
 if not isinstance(row[2],str): raise ValueError("catalog folder nonstring")
 rec=catrecord(n,row); matches=scan({"folder":row[2]})
 if matches: catalog_hits.append({**rec,"matches":matches,**classify(matches,rec["source"])})
 for key in controls:
  if row[5]=="NYC-WTC_000"+key: controls[key]["catalog"].append(rec)
for rel,obj in docs.items():
 if rel.endswith("folders.json"): continue
 rs=obj["resultset"]; rows=rs.get("results",[])
 if not isinstance(rows,list): raise ValueError("results not list")
 req=obj["search_request"]
 pagination.append({"input":rel,"returned":len(rows),"results_member_present":"results" in rs,"estimated_count":obj["estimated_count"],"requested_count":req["count"],"sample_length":req["content_sample_length"],"prev_avail":rs["prev_avail"],"next_avail":rs["next_avail"],"termination_causes":[v["termination_cause"] for v in rs["per_service_dataset"]]})
 for ordinal,row in enumerate(rows,1):
  pm=propmap(row); occurrences+=1
  vals={f:scalar(pm,f,required=f in ["title","source","mes:key"]) for f in ["title","folder_name","source","mes:key","box_name","page_count","agency","production_volume","production_end"]}
  for k,v in vals.items():
   if not v["present"]: properties_missing[k]+=1
   elif v["value"]=="None": literal_none[k]+=1
  core={"input":rel,"ordinal":ordinal,"id":row["id"],"properties":vals}
  all_by_id[row["id"]].append({"record":core,"all_properties":pm,"location":row["location"]})
  fields={k:vals[k]["value"] for k in ["title","folder_name"] if vals[k]["present"]}
  matches=scan(fields)
  if matches: response_hits.append({**core,"matches":matches,**classify(matches,vals["source"]["value"])})
  for key in controls:
   if vals["mes:key"]["value"]=="NYC-WTC_000"+key: controls[key]["responses"].append(core)
conflicts=[]
for identifier,group in all_by_id.items():
 fields=set().union(*(set(x["all_properties"]) for x in group))
 different=[f for f in sorted(fields) if len({json.dumps(x["all_properties"].get(f,{"ABSENT":True}),sort_keys=True) for x in group})>1]
 if different or len({x["location"] for x in group})>1:
  conflicts.append({"id":identifier,"fields":different,"location_disagreement":len({x["location"] for x in group})>1,"occurrences":[{"input":x["record"]["input"],"ordinal":x["record"]["ordinal"]} for x in group]})
assert all(hashlib.sha256((M/k).read_bytes()).hexdigest()==hashlib.sha256(v).hexdigest() for k,v in data.items()),"input changed during run"
assert hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()==PROTOCOL_SHA,"protocol changed during run"
def counts(hits):
 return dict(Counter(h["source_scope"]+" | "+h["category"] for h in hits))
response_unique={}
for h in response_hits:
 response_unique.setdefault(h["id"],h)
context_index=defaultdict(list)
for n,row in enumerate(cat["rows"],1): context_index[(cat["sources"][row[0]],row[1],row[2])].append(n)
context_joins=[]
for identifier,items in all_by_id.items():
 r=items[0]["record"]; v=r["properties"]
 present=all(v[k]["present"] for k in ["source","box_name","folder_name"])
 key=tuple(v[k]["value"] for k in ["source","box_name","folder_name"]) if present else None
 context_joins.append({"id":identifier,"context_complete":present,"catalog_row_ordinals":context_index.get(key,[]) if present else None})
test("actual occurrence/ID accounting",sum(len(v) for v in all_by_id.values())==occurrences and len(response_unique)==len({h["id"] for h in response_hits}))
summary={"catalog_rows":len(cat["rows"]),"response_occurrences":occurrences,"response_unique_ids":len(all_by_id),"catalog_hits":len(catalog_hits),"catalog_hit_categories":counts(catalog_hits),"response_hit_occurrences":len(response_hits),"response_hit_unique_ids":len(response_unique),"response_occurrence_categories":counts(response_hits),"response_unique_categories":counts(list(response_unique.values())),"selected_field_missing":dict(properties_missing),"literal_None":dict(literal_none),"cross_query_conflicts":len(conflicts),"exact_context_join_counts":dict(Counter("missing selected context" if not j["context_complete"] else "one catalog row" if len(j["catalog_row_ordinals"])==1 else "no catalog row" if not j["catalog_row_ordinals"] else "multiple catalog rows" for j in context_joins)),"tests_passed":len(tests),"pins_unchanged":True}
print(json.dumps({"started_utc":start,"elapsed_seconds":round(time.monotonic()-t0,6),"protocol_sha256":PROTOCOL_SHA,"inputs":EXPECTED,"patterns":PATTERNS,"tests":tests,"summary":summary,"pagination":pagination,"catalog_hits":catalog_hits,"response_hits":response_hits,"controls":controls,"conflicts":conflicts,"exact_context_joins":context_joins},ensure_ascii=False,sort_keys=True))

```

## Frozen test outcomes

```json
{"pass":true,"test":"sheet positive S-1"}
{"pass":true,"test":"sheet positive s_1"}
{"pass":true,"test":"sheet positive S.S.1"}
{"pass":true,"test":"sheet positive SKS-S-1"}
{"pass":true,"test":"sheet positive SKS S 2"}
{"pass":true,"test":"sheet positive S–S–1"}
{"pass":true,"test":"sheet positive A-S-1"}
{"pass":true,"test":"sheet positive S-1.1"}
{"pass":true,"test":"sheet positive S-1-1"}
{"pass":true,"test":"sheet positive XS-S-1"}
{"pass":true,"test":"sheet negative AS-1"}
{"pass":true,"test":"sheet negative S-10"}
{"pass":true,"test":"sheet negative S-1A"}
{"pass":true,"test":"sheet negative S-2"}
{"pass":true,"test":"sheet negative S/S/1"}
{"pass":true,"test":"floor positive First Floor"}
{"pass":true,"test":"floor positive 1st-fl"}
{"pass":true,"test":"floor positive first_floor"}
{"pass":true,"test":"floor negative first floorboard"}
{"pass":true,"test":"floor negative 21st floor"}
{"pass":true,"test":"floor negative first floors"}
{"pass":true,"test":"structural positive beam"}
{"pass":true,"test":"structural positive beams"}
{"pass":true,"test":"structural positive notch"}
{"pass":true,"test":"structural positive notches"}
{"pass":true,"test":"structural positive notched"}
{"pass":true,"test":"structural positive notching"}
{"pass":true,"test":"structural positive drawings"}
{"pass":true,"test":"structural positive sketches"}
{"pass":true,"test":"structural positive penetrations"}
{"pass":true,"test":"structural negative notchingX"}
{"pass":true,"test":"structural negative beamline"}
{"pass":true,"test":"structural negative redrawing"}
{"pass":true,"test":"field isolation: unselected echo/facet/paging ignored"}
{"pass":true,"test":"duplicate JSON keys rejected"}
{"pass":true,"test":"duplicate property ids rejected"}
{"pass":true,"test":"invalid selected property rejected 0"}
{"pass":true,"test":"invalid selected property rejected 2"}
{"pass":true,"test":"invalid selected property rejected 1"}
{"pass":true,"test":"invalid selected property rejected 1"}
{"pass":true,"test":"malformed row width rejected"}
{"pass":true,"test":"missing distinct from literal None"}
{"pass":true,"test":"occurrence versus ID accounting"}
{"pass":true,"test":"actual occurrence/ID accounting"}
```

Root-result reconciliation is not included in this initial freeze. Any later
comparison must be an attributed, appended section retaining this initial portion.

## Post-freeze reconciliation and draft critique

The initial 97,457-byte portion was frozen at SHA256
`b34fab4ce62ba1c8efc5321f4bbb98622904d59820dabf61f2181da89aedf1b8`
before any root result or report access. It is retained byte-for-byte.
The root result reviewed is `result.json`, 229,797 bytes, SHA256
`317f60e10c8987acffc5b6f0baed9a521deac9a2953dd6b9f9af930ff8a55219`.
No root implementation was imported or used to construct the independent result.

- Root-result schema inspection 417fee exited 0, but its displayed output was
  truncated. The compact inspection 408382 exited 0. Neither displayed excerpt
  was substituted for the complete comparison.
- Complete comparison 2be125 exited 0: 529/529 explicit checks passed, zero failures;
  elapsed comparison 1.005908 s, tool wall 2.454663084 s. It replayed the code
  embedded in this already-frozen note against the fixed inputs, captured its
  stdout in memory and compared the complete root JSON. This is an attributed
  post-freeze reconciliation, not a second blinded experiment.
- Exact agreement covers all 24 input pins; protocol and pattern strings; six
  summary counts; all 38 catalog row identities, original fields, matched text
  and spans; all 11 matched response appearances/eight IDs; all supplied scalar
  properties for all 208 IDs and all 302 file/ordinal appearances; all 23 coverage
  records and their ordered returned IDs; eight exact missing-property locations;
  all four controls; and zero supplied-property/location conflicts.
- Root `context lead` is the same lower-specificity category described in this
  independent receipt. Root's `off-source` label retains the two non-WTC-7
  catalog hits; this note additionally names their lower-specificity predicate
  category. No substantive disagreement or omitted match was found.
- Test accounting is explicit: 43 passed in efe666; 44 in the final 983dee run
  and its post-freeze replay. The extra test is actual occurrence/ID accounting;
  field isolation was also strengthened without changing the test count.
  The earlier 2ff0bc compound-token expectation failure remains in the initial
  portion and was not erased or relabeled as a source/predicate failure.

### Bounded draft review

The complete draft read at 1b0da9 (exit 0) was `report.md`, 8,412 bytes,
SHA256 `2ab79449480f329ef1b02508dec0172b90d8495e038a689749eda4eafbb6b97d`.
The factual-disposition review found no numeric or metadata-applicability
overclaim requiring correction. The draft correctly treats the negative result
as scoped, retains the known-packet nonmatch, separates exact controls from text
matches, notes caps/missing folders, and leaves source applicability unresolved.
Its eight-row navigation table is explicitly a subset of the retained 38-row
result rather than an exhaustive or mandatory acquisition list.

b391cf exited 0 (0.4963115 s tool wall): all eight navigation-table rows exactly
match their catalog row/first-Bates/counts/original label, all five local links
exist, and the catalog capture timestamp is
`2026-09-11T12:57:00+00:00`, supporting its September 11 capture statement.
The draft's pending-independent-review language must be updated by the root
after receipt reconciliation; this is status text, not a failed result check.
I did not independently re-audit the root's sixteen-test chronology, prior
PDF content roles, or the SFB-005 feedback fixture. Those attributed/history
claims are not part of the fixed metadata reproduction or new acceptance here.

No source or frozen initial finding was changed for agreement. No new acquisition,
primary-content view, network request, model join or archive-wide absence claim
was introduced. The root owns report/status updates and any separately declared
next retrieval.

### Exact reconciliation command

```bash
'/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3' - <<'PY'
from pathlib import Path
import re,json,hashlib,io,contextlib,time
U=Path("/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-first-floor-locator-2026-10-05")
nb=(U/"independent-review.md").read_bytes()
assert hashlib.sha256(nb).hexdigest()=="b34fab4ce62ba1c8efc5321f4bbb98622904d59820dabf61f2181da89aedf1b8"
rb=(U/"result.json").read_bytes()
assert hashlib.sha256(rb).hexdigest()=="317f60e10c8987acffc5b6f0baed9a521deac9a2953dd6b9f9af930ff8a55219"
root=json.loads(rb); env={}; out=io.StringIO(); started=time.monotonic()
code=re.findall(r"\x60\x60\x60python\n(.*?)\n\x60\x60\x60",nb.decode(),re.S)[0]
with contextlib.redirect_stdout(out): exec(compile(code,"frozen-independent-replay","exec"),env)
own=json.loads(out.getvalue()); checks={}
def ck(k,v):
 checks[k]=bool(v)
 if not v: raise AssertionError(k)
ck("protocol_and_patterns",root["protocol_sha256"]==own["protocol_sha256"] and root["patterns"]==own["patterns"])
ck("all_24_pins",sorted((p["file"],p["bytes"],p["sha256"]) for p in root["pins"])==sorted((p["path"],p["bytes"],p["sha256"]) for p in own["inputs"]))
ck("six_summary_counts",root["counts"]=={"matching_appearances":11,"matching_document_ids":8,"matching_folder_rows":38,"missing_folder_appearances":8,"query_occurrences":302,"unique_document_ids":208})
def matches(v):
 return sorted((field,category,m["text"],tuple(m["span"])) for field,cats in v.items() for category,ms in cats.items() for m in ms)
def rootmatches(v):
 return sorted((m["field"],m["category"],m["text"],tuple(m["span"])) for m in v)
cats={r["ordinal"]:r for r in own["catalog_hits"]}
ck("38_catalog_ordinals",set(cats)=={r["row_ordinal_one_based"] for r in root["catalog"]["matching_rows"]})
for r in root["catalog"]["matching_rows"]:
 a=cats[r["row_ordinal_one_based"]]
 ck("catalog_row_"+str(a["ordinal"]),all(r[k]==a[k] for k in ["box","documents","first_bates","folder","pages","source"]) and rootmatches(r["matches"])==matches(a["matches"]) and r["disposition"]==("off-source" if a["source_scope"]=="off-source" else "context lead"))
hits={(h["input"],h["ordinal"]):h for h in own["response_hits"]}
ck("11_response_occurrence_keys",set(hits)=={(r["file"],r["result_ordinal_one_based"]) for r in root["matching_appearances"]})
for r in root["matching_appearances"]:
 a=hits[(r["file"],r["result_ordinal_one_based"])]
 ck("response_hit_"+r["file"]+":"+str(r["result_ordinal_one_based"]),r["result_id"]==a["id"] and rootmatches(r["matches"])==matches(a["matches"]) and all((k in r["properties"])==v["present"] and (not v["present"] or r["properties"][k]==v["value"]) for k,v in a["properties"].items()) and r["disposition"]=="context lead")
own_documents={}
own_missing=[]
for identifier,group in env["all_by_id"].items():
 first=group[0]; pm=first["all_properties"]
 properties={k:next(v for typ,v in p["data"][0]["value"].items() if typ!="unit") for k,p in pm.items()}
 key=properties["mes:key"]
 own_documents[key]={"properties":properties,"appearances":sorted((x["record"]["input"],x["record"]["ordinal"]) for x in group)}
 for x in group:
  for f in ["title","folder_name"]:
   if f not in x["all_properties"]: own_missing.append((x["record"]["input"],x["record"]["ordinal"],key,f))
ck("208_document_keys",set(root["documents"])==set(own_documents))
for k,v in root["documents"].items():
 a=own_documents[k]
 ck("all_properties_"+k,v["properties"]==a["properties"])
 ck("all_appearances_"+k,sorted((x["file"],x["result_ordinal_one_based"]) for x in v["appearances"])==a["appearances"])
ck("eight_missing_properties_exact",sorted(own_missing)==sorted((r["file"],r["result_ordinal_one_based"],r["key"],r["field"]) for r in root["missing_fields"]))
coverage={r["input"]:r for r in own["pagination"]}
for r in root["coverage"]:
 a=coverage[r["file"]]
 ck("coverage_"+r["file"],all(r[k]==a[k] for k in ["estimated_count","next_avail","prev_avail","requested_count","returned","termination_causes"]) and r["results_key_present"]==a["results_member_present"])
 ck("coverage_ids_"+r["file"],r["ids"]==[env["scalar"](env["propmap"](v),"mes:key",True)["value"] for v in env["docs"][r["file"]]["resultset"].get("results",[])])
ck("zero_conflicts",root["disagreements"]==own["conflicts"]==[])
for key,group in own["controls"].items():
 rr=root["known_controls"]["NYC-WTC_000"+key]
 ck("control_catalog_"+key,sorted(r["row_ordinal_one_based"] for r in rr if "row_ordinal_one_based" in r)==sorted(r["ordinal"] for r in group["catalog"]))
 ck("control_response_"+key,sorted((r["file"],r["result_ordinal_one_based"],r["result_id"]) for r in rr if "result_ordinal_one_based" in r)==sorted((r["input"],r["ordinal"],r["id"]) for r in group["responses"]))
ck("root_result_pin_unchanged",hashlib.sha256((U/"result.json").read_bytes()).hexdigest()==hashlib.sha256(rb).hexdigest())
ck("initial_note_unchanged",hashlib.sha256((U/"independent-review.md").read_bytes()).hexdigest()==hashlib.sha256(nb).hexdigest())
print(json.dumps({"elapsed_seconds":round(time.monotonic()-started,6),"checks":len(checks),"passed":sum(checks.values()),"failed":[k for k,v in checks.items() if not v],"replay_tests":own["summary"]["tests_passed"],"exact_scope":{"pins":24,"catalog_hits":38,"matched_occurrences":11,"matched_unique_ids":8,"all_documents":208,"all_appearances":302,"coverage_records":23,"controls":4,"missing_folder_occurrences":8},"root_result_sha256":hashlib.sha256(rb).hexdigest(),"independent_initial_sha256":hashlib.sha256(nb).hexdigest()}))
PY
```

### Concurrent report revision and replay clarification

Final guard b11597 exited 1 at the report.md pin assertion. The initial-prefix,
protocol and result pin checks preceding it passed. This was a detected concurrent
report revision, not a mismatch in the 24 metadata inputs or lookup output.
The root explicitly identified the intended report revision as SHA256
`051666bc0d1451a74420c261185edecdeba4392968687710f3722b3a23785df4`.
I deliberately re-read that complete revision in 30208a (exit 0,
0.175592459 s tool wall). It replaces pending-review status with attributed
independent-replay/method results. The numerical findings, bounded disposition
and stated limitations remain consistent; no factual correction is requested.
The root/method review's own command histories are attributed, not independently
observed here. The earlier draft pin and failed guard remain above.

The exact reconciliation command above is the **historical pre-append invocation**,
not a command expected to pass unchanged against this expanded note. Its full-file
initial-hash guard intentionally rejects a later appended file. For a current replay,
first verify `sha256(note_bytes[:97457])` equals
`b34fab4ce62ba1c8efc5321f4bbb98622904d59820dabf61f2181da89aedf1b8`,
then use precisely those initial 97,457 bytes when extracting the independent
Python body and when applying the historical initial-artifact check. Do not
silently replace that frozen hash with the expanded note's hash. The independent
extraction body itself remains executable as printed and never reads this
reconciliation section. Later source/report versions require their own explicit
pin review rather than removal of a failed guard.
