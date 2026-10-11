# Independent test/acceptance metadata review

October5,2026 UTC. Bounded research-only metadata review, separately completed before reading any root-derived candidate list or report. No network, source PDF/image content, OCR, acquisition, main/legal/status/README edits or source alteration. This frozen note preserves the completed dispatched review as WIP while the user returns to the coordinate request; it does not start the next content task.

## Scope, controls and actual checks

Read evidence/source-of-truth/data-quality/repo-orchestrator skills completely (`69b2ff`,exit0), required shared instructions/references (`0d1b33`,exit0); the optional inline-receipt reference's initially truncated middle was completed at `d92c2a`. The scoped companion uses this assigned repository note, not a separate notebook/dashboard or publication. Read full new protocol (`9bccc3`,exit0), prior drawing-locator protocol and all five saved request bodies (`199f8b`,exit0), prior `check_metadata.py` as the local schema contract only (`e50e3c`,exit0; not imported/executed). Current main AGENTS/WORKFLOW/START-HERE/charter hashes matched previously fully read versions; protocol hash verified `3938808129a75bf279e8ca8edb885282a7eb96bd4a58514556091e4254d09163` (`a810f6`,exit0). Repo intake polled original session51958 to terminal `4fd311`,exit0, branch research/sherlock-wtc7-investigation, HEAD ca1c2233; existing WIP untouched.

Schema inspection `5651ee` and independent full catalog parsing `dcacbf` exited0. Only the specified main lead memo was searched, `rg -n -i 'generator|sign[ -]*off|punch'` (`abebfc`,exit0): one match at line67 discussing already known NIST generator-room sprinkler coverage, not a test/result/signoff locator. No broad local content search.

Response inspection `03e1ee` established current nested result/property schema. Initial independent parser `abb642` **failed exit1** because it assumed every resultset contained `results`; the empty date response omits that key. Diagnostic `532900` exited0 but overbroad output truncated; it is not claimed as a full visual read of signoff metadata. Its complete displayed date result and the subsequent full machine parse established the missing-key empty shape. The revised parser accepted missing `results` **only** for date with estimated0, next/previousfalse and sole NO_MORE_RESULTS; it did not silently coerce arbitrary missing data into empty results. No source/request changed.

Final independent stdout-only parse `cebb94`,exit0, read every byte of ten saved request/response JSONs with duplicate-key rejection. It checked exact request echo after removing only empty user_context; count50/content_sample_length0; exact eleven VALUE property requests; unique property IDs and exactly one scalar value each; string/numeric type validity; exact title/key and connector-ID joins; WTC7 source; positive whole-integral page and finite byte counts; production IDs; mes:date numeric unit ms_since_1970; within-query ID uniqueness; all properties and raw property data equality across repeated IDs; known167873control. All reported production-end minus start plus1 also equal page counts, a metadata consistency check not historical authentication. All result objects share id/location/order/properties/rank_score/relevance_score fields; no sampled content field was supplied. No semantic historical date was inferred from mes:date.

Second exact source/box/folder join check `3c2642`,exit0: every unique response record joins a held catalog folder; none of the returned folder groups exceeds the catalog document count. No new search or source reading was performed. Existing-PDF joins below use filenames and filesystem byte sizes **only**, scoped to this municipal unit tree; PDF contents and hashes were not newly read.

## Held catalog grain and matched folders

`../folder-document-locator/folders.json`:421135bytes,SHA256 `cf3afa33cc58a0f2a9d48e6fbac57cdd8bb060b046cf5373d261d37bb976b704`; captured_at2026-09-11T12:57:00+00:00, not a guarantee of current archive completeness. All4205rows passed six-field schema/type checks, positive document/page counts, firstBates format and unique(source_index,box,folder)grain. Case-insensitive `generator|sign[ -]*off|punch` applied to **folder labels**, not all metadata or source content.29matchingWTC7folders;0off-source matches. Their catalog totals37documents/163pages are **folder totals**, not the page counts of29firstBates PDFs. No matching sign-off label; that is not proof no sign-off document exists.

All rows below have sourceWTC7,box7DCAS. Exact spelling/symbols preserved; IDs omit the common NYC-WTC_000 prefix only for compact display.

|Catalog ordinal|First ID|Folder documents/pages|Exact folder label|
|---:|---:|---:|---|
|2574|173500|1/28|23 Floor Punch List|
|2576|174100|1/27|23rd Floor Punch List|
|2604|167301|1/1|7 WTC OEM Emergency Generator - Fee Proposal|
|2605|173014|3/13|7 WTC Punch List|
|2833|172395|1/2|7 World Trade Center ®Mayor's Office of ®Emergency Management®Emergency Generator Full Load Test|
|2846|171511|1/1|7 World Trade Center®7th Floor®Generator Room|
|2866|171513|2/2|7th Fl. Generator room insulation recommendations|
|2892|171241|1/1|ATTACHED PLEASE FIND 2ND. ARCHITECTURAL PUNCH LIST FOR AST. 7TH. AND 23RD. FLOORS FOR OEM|
|3153|166871|1/1|Emerg. Generators|
|3154|172397|1/1|Emergency Generator Full Load Test|
|3155|174136|1/1|Emergency Generator Operation®Press Room®Audio Visual Work®Leak Detection System|
|3209|166874|1/52|GENERATOR PREPURCHASE SPECIFICATION|
|3210|173715|1/1|GENERATOR TEST RESULTS.|
|3400|172389|4/12|Mayor's Office of Emergency Management (Generator Test) Our Job No. 1854|
|3666|167731|1/1|Mayor's Office of Emergency Management ®Emergency Generator Noise|
|3673|171252|1/3|Mayor's Office of Emergency Management®(Generator Test)®Our Job No. 1854|
|3721|167727|2/3|Mayor's Office of Emergency Management®Emergency Generator Noise|
|3735|167730|1/1|Mayor's Office of Emergeney Management Emergency Generator Noise 7 World Trade Center|
|3828|172972|1/1|OEM - Swanke Punch List|
|3835|166872|1/1|OEM 7 WTC Emergency Generator Specifications|
|3857|171510|1/1|OEM Generator Room®7 World Trade Center®7th Floor|
|3881|171514|1/1|OEM, 7 WTC, 7th FL.®Generator Room|
|3882|171561|1/1|OEM, 7 WTC, 7th Fl.®Generator Room|
|3885|172973|1/1|OEM-Swanke Punch List|
|3948|168654|1/1|Peoria emergency generator test|
|3957|172134|2/2|Prepurchase of Generators Mayor's Office of Emergency Management 7 World Trade Center|
|3958|167821|1/1|Prepurchase of Generators ®Mayor's Office of Emergency Management ®7 World Trade Center|
|4094|172975|1/1|Shen Milson & Wilkie punchlist for MOEM Audio-Visual systems dated 7/20/99|
|4138|173494|1/1|UPDATE OF PUNCH LIST|

Main lead memo pin: `01f7419ec36c6686ac154c6f6e05e3309d90704069957119cfc9efb8160bc3ea`. Memo context is derivative lead history, not independently inspected source facts in this unit.

## Response coverage and its limits

All five saved queries echo exactly; control only is the known-folder query. Query labels below refer to the saved exact request bodies, not interpreted search-engine semantics.

|Query|Returned|Estimated|Returned page sum|next/previous|Service termination|Coverage|
|---|---:|---:|---:|---|---|---|
|generator test|50|144|1198|true/false|COUNT_LIMIT|Partial first result batch|
|quoted sign off|20|20|152|false/false|NO_MORE_RESULTS|Ended for this exact query, not all sign-off records|
|punch|50|91|1562|true/false|COUNT_LIMIT|Partial first result batch|
|quoted7/17/99|0|0|0|false/false|NO_MORE_RESULTS|No returns for this string; resultskeyabsent|
|known-folder control|1|1|1|false/false|NO_MORE_RESULTS|Returned167873exactly|

121query occurrences collapse to111unique documentIDs and1772reported physical pages (including the one-pagecontrol). No duplicate IDs within a query, no cross-query property disagreement. Generator and punch results are **explicitly incomplete**; the fixed cap was not expanded. Estimated counts are server estimates, not independently measured archive populations. Exact-query NO_MORE_RESULTS does not calibrate OCR/tokenization recall. Datezero does not refute the known July17text or establish absent tests. The control proves only this route/known-record retrieval. SourceWTC7 includes varied agency/box contexts and is not proof every result concerns the same OEM test.

## Complete returned ID list

G=generator,S=signoff,P=punch,C=control. IDs are exact numeric suffixes of NYC-WTC_000; page/byte values are **individual-document metadata**, not read PDFs. All111unique IDs from the admitted capped responses are retained. Raw linked responses preserve full exact labels/properties.

|ID|Queries|Pages|Bytes|
|---:|---|---:|---:|
|166488|G|46|2798051|
|166571|G,S,P|127|5943038|
|166707|G|3|148252|
|166874|G|52|2600724|
|167029|P|25|1039279|
|167056|P|12|692501|
|167191|P|3|198555|
|167253|P|6|293113|
|167259|P|23|1222261|
|167537|P|1|51078|
|167556|P|1|54099|
|167648|P|1|146332|
|167719|S|1|73316|
|167845|S|1|44179|
|167873|C|1|40327|
|167934|S|2|189822|
|167941|S|1|77703|
|168334|P|1|49334|
|168652|G|1|41972|
|168653|G|1|52501|
|168654|G|1|73353|
|168718|G,P|256|25100075|
|169609|G,P|98|5069983|
|169723|G,P|91|4685110|
|169815|P|4|140394|
|169821|P|15|1266850|
|169837|G,P|90|4708124|
|169936|G,P|120|4599183|
|170060|G,P|113|4131979|
|170182|P|10|626457|
|170192|P|33|1169840|
|170238|P|57|2411497|
|170296|G,P|114|4923280|
|170436|P|8|417505|
|170445|P|106|4426506|
|170577|P|116|5728366|
|170888|S|1|88247|
|171237|P|4|353595|
|171241|P|1|41784|
|171251|G|1|64028|
|171252|G|3|172757|
|171263|P|2|94165|
|171284|S|1|91814|
|171300|S|1|84808|
|171358|P|1|59134|
|171432|S|1|56557|
|171491|S|1|85858|
|171535|S|1|57168|
|171557|S|1|85393|
|171597|S|1|60692|
|171698|S|2|84932|
|171707|P|27|822905|
|171788|P|2|88208|
|171793|P|2|92627|
|171981|G|1|50937|
|172123|G|3|137893|
|172283|G|1|84159|
|172316|G|3|121241|
|172388|G|1|54846|
|172389|G|3|172163|
|172395|G|2|103619|
|172397|G|1|35481|
|172489|S|1|95065|
|172523|G|4|182316|
|172527|P|2|137560|
|172538|G|1|53785|
|172539|G|3|171315|
|172542|G|1|53725|
|172543|G|3|169718|
|172561|P|2|95615|
|172566|P|2|109831|
|172616|S|1|95793|
|172627|G|2|112294|
|172758|S|1|92691|
|172760|S|1|87181|
|172953|S,P|5|345271|
|172972|P|1|54254|
|172973|P|1|38529|
|172975|P|1|61119|
|172976|G|1|67745|
|172977|G|1|60316|
|173014|P|3|168724|
|173073|G|3|137264|
|173103|G|5|350288|
|173115|G|5|233908|
|173121|G|2|93450|
|173147|G|2|116229|
|173162|G|1|58192|
|173226|G|5|285085|
|173231|G|5|265327|
|173236|G|5|299954|
|173319|G|2|132202|
|173352|G|3|137939|
|173355|G|3|128668|
|173489|P|5|290845|
|173494|P|1|40929|
|173495|P|5|288292|
|173500|P|28|786885|
|173688|G|2|88496|
|173708|G|1|38969|
|173709|G|1|52524|
|173715|G|1|36410|
|173734|P|1|37430|
|173794|S|1|83199|
|173911|P|2|95432|
|174040|P|2|85981|
|174043|P|2|86249|
|174046|P|2|88799|
|174095|G|1|55156|
|174096|G|3|169639|
|174100|P|27|824189|

## Exact joins and candidate priority, not content findings

Filename+byte-size matches within existing municipal packet tree:167873 at `../design-sprinkler-followup/NYC-WTC_000167873.pdf`40327bytes;171300sameunit84808bytes;171557at `../folder-siblings/NYC-WTC_000171557.pdf`85393bytes;172953at `../approval-breakdowns-b/NYC-WTC_000172953.pdf`345271bytes. Those are already held, not four new independent sources. No claim this filename-only scope inventories all holdings elsewhere or verifies file content/authenticity.

Exact source/box/folder aggregation confirms the four Job1854 records172389/172539/172543/174096 are3pages each, jointly4documents/12pages matching their folder row.171252's3pages belong to a separate ®-formatted folder; similar labels do not prove byte identity or four independent tests. Punchfolder173014/173489/173495 has3/5/5pages, together3documents/13pages matching the folder total. FirstBates173014 alone is **3pages**, not13. The remaining named test/punch folder memberships also match their reported folder totals where all listedmembers return; this does not cure overall capped-query incompleteness.

For a later separately authorized finite content batch, the labels **Emergency Generator Full Load Test** at172395(2pages,103619bytes),172397(1page,35481bytes), and **GENERATOR TEST RESULTS.** at173715(1page,36410bytes) are the closest explicit full-load/result leads; within this class their numeric order is172395,172397,173715. This4page selection is a locator judgment, not proof of July17, test success/failure, inspection coverage or content. Job1854 records and the Peoria-labeled168654 remain alternatives; do not assume an off-site labeled test is the relevant installed-system commissioning test. No new content admission or acquisition occurs here.

The20signoff hits have labels including proposals, quotations and payment-routing records rather than an explicit PortAuthoritysignoff label. They cannot be counted as20actualsignoffs. The queried172953 is the already-read conditional accounting packet, illustrating why a returned hit is not independent performance corroboration. Conversely, failure to find a signoff-specific folder label does not exclude a signoff within a generically labeled file. Punch-list labels likewise may be unfinished work lists rather than completion certifications. Primary content and date/system/version joins could confirm or disconfirm each proposed lead; no cause ranking follows from metadata.

## Input pins

|Saved file|Bytes|SHA256|
|---|---:|---|
|generator-request.json|1092|e1544eaee6223d67fae024e8af3b46ecb0f3632ac974f773fe71ca14d7699974|
|generator-response.json|66134|bf13d5608fc49e3da64b3291b2779ddfd64692e05ae7c7fa063a9d7e2afd3186|
|signoff-request.json|1090|49edcbb99fa46b38e296f30604fe9e92712eee08bd1a54aa85144efe4c9fb672|
|signoff-response.json|30480|42c16897153f26bb0a0844f6693cd5cac3818a9dbd6e8acb85563a2616a5e6eb|
|punch-request.json|1083|e89ebba5493130dbd6de0e5907738fb9e20e333521e75be5461605d0f6a8d573|
|punch-response.json|65056|cd6bfc2d72090d0dcd33cf8b014d4be63ae4b05d71ace3de66700cfa45f6b73d|
|date-request.json|1089|96a71e417281f8b1bf7fdbc78d63ab4a9ead179b32885f2f927f3b4540875c94|
|date-response.json|1760|ea21d260015169581e7b80212786e6be4aeb7abd6ea8c821a555998ba89a2e4f|
|control-request.json|1158|05a0df86737b4efeaf9949051c23385e22ed46c16a4ddbca567511e1a45277ef|
|control-response.json|8451|7386207c519d9144fc0a2b9e6092351a41ba38059f2008e8156d4ed0686f6a29|

Transport statuses were supplied by root, not independently reacquired by this reader. This review establishes local schema/identity/arithmetic consistency and specified search coverage only. Raw responses, previous frozen notes and main authority remain unchanged; no root-derived candidate list/report was opened before this independent freeze.

Final own-note transcription check polled original session43004 to terminal `938196`,exit0: all111saved ID/query/page/byte rows and29exact catalog ordinal/label/count rows agreed with the preserved input JSONs. This checks the note against metadata, not against unread source PDFs. No table correction was needed. Freeze hash is returned separately after this receipt append.
