# Municipal integration inventory

## Scope and result

Mechanical local inventory for the fixed integration scope, not a new source-content review. Snapshot: 2026-10-05T03:37:34.221917+00:00 through 2026-10-05T03:44:19.942213+00:00 (UTC; local research date October 4, 2026). The scope pin is `cbdab06e50e20d863d08bd7a3d47bd0da0c980663db99108645ce554e47733c1`.

Base directory `M` is:

`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04`

Every non-absolute path below is the exact path relative to this base; absolute paths are explicitly shown for the three outside context inputs. All other files remained read-only. Only this inventory note was written.

Observed **49 local PDF files, 123 physical pages, 7,859,629 bytes**: the declared 49/123 target matches. All 49 have PDF magic, are unencrypted, and parsed for page count without warnings or failures. All 49 current source hashes match exact pins in both their unit's existing source log and derivative receipt; none lack a local pin. One further verification receipt also matched the fsk56 source pin. These are current integrity comparisons against existing receipts, not new authentication or repetition of the receipts' historical renderer runs.

The 49 files form **49 distinct SHA-256 byte groups; no byte-identical duplicate groups** were found inside this directory tree. This does not imply 49 semantic document families, independent witnesses, independent evidentiary chains, or independent installation/acceptance events. Similar packets can have different bytes; semantic-family classification belongs to the separate synthesis. The page total is a count of locally held physical PDF pages, not new page readings. References to already-held pages do not add a file or page here.

All fixed **20 content reports, five locator reports, and three outside context reports/plans** exist and are pinned below. The OEM comparison unit has a content report but no PDF physically under its own directory; outside referenced source PDFs were not added to this bounded inventory or re-inspected. Reports, locators, context reviews, and source receipts are derivative research inputs, not additional independent primary evidence.

## Commands, receipts, and retained failure

The applicable PDF, repository-orchestration, source-of-truth, and evidence-falsification skills were used to keep this check structural and provenance-focused. They did not authorize source-content interpretation or new acquisition. The complete integration scope and skills were read; unchanged current main-control pins were rechecked. Control read/hash receipt `7e42bf` and skill read receipt `5df437` ended 0. Main controls: AGENTS `934437bfc0ddbe522cc73461819593706d12c0644cb306d263d9f1fe3914a857`; WORKFLOW `17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a`; START-HERE `b291da2b9ab3f1a8e9e69ff5a5d930c689ff2d45a6b2ce06a521e76295fbd560`; investigation CHARTER `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.

Discovery used `rg --files --hidden --no-ignore` with bounded file-name filters (receipt `bc4fac`, exit 0); the exact three outside context paths were then supplied by the coordinator. No outside source content was searched. Inventory ran stdout-only Python with the bundled interpreter:

`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`

Python 3.12.14, pypdf 6.10.0. The actual inventory enumerator was:

```python
subprocess.run(["rg", "--files", "--hidden", "--no-ignore", "-g", "*.pdf", str(M)],
               capture_output=True, text=True, check=True)
```

For each sorted returned path the run used `Path.read_bytes()`, `hashlib.sha256(data).hexdigest()`, and `pypdf.PdfReader(BytesIO(data))`; it recorded `len(reader.pages)`, `is_encrypted`, PDF magic, parser-warning count, and exact SHA-string matches/line numbers in the same-unit allowlisted receipts (`source-log.md`, `derivative-check.md`, `verification.md`, `provenance-check.md` when present). No PDF text, metadata fields, or images were extracted. That run started 2026-10-05T03:37:34.221917+00:00, ended 2026-10-05T03:37:35.164162+00:00, elapsed 0.941636 seconds. Initial handle `38060` (`c34bbb`) was polled to terminal `409371`, exit 0. Its 49/123 assertions passed; parse failures, parser warnings, and missing local pins were all zero.

The fixed report/context inventory and stricter same-line association check ran 2026-10-05T03:38:47.017497+00:00–2026-10-05T03:38:47.153622+00:00, elapsed 0.136137 seconds (`3ed888`, **exit 1 retained**). All 28 specified files existed and were hashed. The extra heuristic incorrectly required a PDF identifier and its exact source hash to occur on one line. It passed for 45 PDFs but flagged four PDFs/six receipt links whose filename and hash were wrapped across lines. This was a formatting-check failure, not a source-hash mismatch. No source, expected hash, or original receipt was changed.

Bounded `sed -n` checks of the six relevant receipt ranges (`d05bab`, exit 0) showed the filename/hash associations. A separate explicit-range Python check (`42b313`, exit 0; 2026-10-05T03:44:19.933220+00:00–2026-10-05T03:44:19.942213+00:00, 0.009007 seconds) then asserted the full PDF filename and exact hash within each of those same selected ranges: **6/6 passed**. The six ranges were:

| PDF | Receipt | Inclusive lines |
| --- | --- | --- |
| `enclosure-framing/NYC-WTC_000172233.pdf` | `enclosure-framing/source-log.md` | 25–42 |
| `enclosure-framing/NYC-WTC_000172233.pdf` | `enclosure-framing/derivative-check.md` | 19–37 |
| `fsk56-followup/NYC-WTC_000174022.pdf` | `fsk56-followup/derivative-check.md` | 12–25 |
| `fuel-route-followup/NYC-WTC_000171753.pdf` | `fuel-route-followup/derivative-check.md` | 1–15 |
| `oil-route-packet/NYC-WTC_000166828.pdf` | `oil-route-packet/source-log.md` | 20–37 |
| `oil-route-packet/NYC-WTC_000166828.pdf` | `oil-route-packet/derivative-check.md` | 22–38 |

No missing pins or unresolved file/receipt discrepancies remained. This correction preserves the original exit-1 result; it does not assert that the same-line heuristic itself passed. Before adding this note, `test ! -e M/integration-inventory.md` ended 0 (`a83d62`).

## Counts by physical holding unit

The following counts include only PDFs physically under each unit; reports are enumerated separately below.

| Unit | PDF files | Physical pages | PDF bytes |
| --- | ---: | ---: | ---: |
| `.` | 2 | 11 | 546180 |
| `followup` | 2 | 8 | 481147 |
| `structural-followup` | 2 | 3 | 143573 |
| `hatch-followup` | 2 | 2 | 119114 |
| `fsk56-followup` | 1 | 3 | 135742 |
| `design-sprinkler-followup` | 3 | 4 | 204742 |
| `enclosure-framing` | 1 | 2 | 145877 |
| `enclosure-framing/oem-comparison` | 0 | 0 | 0 |
| `fuel-route-followup` | 1 | 1 | 62089 |
| `oil-route-packet` | 1 | 8 | 533928 |
| `folder-siblings` | 3 | 5 | 244274 |
| `drawing-review` | 2 | 4 | 325986 |
| `change-order-review` | 4 | 10 | 709482 |
| `various-orders` | 2 | 4 | 217425 |
| `approval-breakdowns-a` | 3 | 11 | 1171404 |
| `approval-breakdowns-b` | 3 | 9 | 809957 |
| `generator-test-results` | 3 | 4 | 175510 |
| `generator-job1854` | 5 | 15 | 855592 |
| `job1854-followup-review` | 6 | 7 | 405916 |
| `generator-service-review` | 3 | 12 | 571691 |
| Total | 49 | 123 | 7859629 |

## Exact PDF inventory and receipt matches

Pin references below are existing receipt paths plus exact-hash line numbers, not fresh render execution receipts. The six wrapped associations above supplement these line references.

| Path | Bytes | SHA-256 | Pages | Existing pin locations |
| --- | ---: | --- | ---: | --- |
| `NYC-WTC_000153903.pdf` | 12357 | `87daf254c97f818598eab7de77481048079c69b300338a5c7734719acb0b985d` | 1 | `source-log.md:45`; `derivative-check.md:42` |
| `NYC-WTC_000173529.pdf` | 533823 | `143af40af3270048ef8b9afc501342f40341c2dc6b9256394396682900e1c2c6` | 10 | `source-log.md:46`; `derivative-check.md:43` |
| `approval-breakdowns-a/NYC-WTC_000171286.pdf` | 489175 | `e0776e7605d5136b5f73863acbf4c8b8654ac7c70cf83d9ef0596053e13d660b` | 5 | `approval-breakdowns-a/source-log.md:24`; `approval-breakdowns-a/derivative-check.md:43` |
| `approval-breakdowns-a/NYC-WTC_000171620.pdf` | 326462 | `3b2d1b201e25385391cc9efb72ce044c80006d6e4cbae8e3fac16f5804eb30e7` | 3 | `approval-breakdowns-a/source-log.md:25`; `approval-breakdowns-a/derivative-check.md:44` |
| `approval-breakdowns-a/NYC-WTC_000172947.pdf` | 355767 | `667a70850ca01b211fa0f21ace5774a06acbd77bf02bbf723ea11eb3b5dc79f6` | 3 | `approval-breakdowns-a/source-log.md:26`; `approval-breakdowns-a/derivative-check.md:45` |
| `approval-breakdowns-b/NYC-WTC_000172953.pdf` | 345271 | `b981e1fde92775b1c59b2d4370488c2d70591efcbb3b98e9a621b2d32e814f00` | 5 | `approval-breakdowns-b/source-log.md:38`; `approval-breakdowns-b/derivative-check.md:43` |
| `approval-breakdowns-b/NYC-WTC_000173949.pdf` | 232649 | `c480f2a9635763caf4cc17be6a3500c1ec2cb42c878165d863192f6e255e3809` | 2 | `approval-breakdowns-b/source-log.md:39`; `approval-breakdowns-b/derivative-check.md:44` |
| `approval-breakdowns-b/NYC-WTC_000174004.pdf` | 232037 | `89de4a3ae1e611c2c27993ced26f4e921650022b7864713c29cce9095f08c93e` | 2 | `approval-breakdowns-b/source-log.md:40`; `approval-breakdowns-b/derivative-check.md:45` |
| `change-order-review/NYC-WTC_000168580.pdf` | 41911 | `d6c8b161f3008b5c667fb7a2aa799d6b887a2ec2da9e9159a58f547d79465727` | 1 | `change-order-review/source-log.md:26`; `change-order-review/derivative-check.md:39` |
| `change-order-review/NYC-WTC_000168581.pdf` | 48367 | `6a5ac540b874575944f6350f808a55ebf70c41e2a9b30f6049e4183298032c71` | 1 | `change-order-review/source-log.md:27`; `change-order-review/derivative-check.md:40` |
| `change-order-review/NYC-WTC_000171840.pdf` | 374954 | `f5da0371e474998eaf37220836e261c8de2c437fcb1dd911533761391ae17a35` | 6 | `change-order-review/source-log.md:28`; `change-order-review/derivative-check.md:41` |
| `change-order-review/NYC-WTC_000173920.pdf` | 244250 | `2d06a8d40c8a8b3433e25509211110165c3ddc7d1e78a383e706803684dc3652` | 2 | `change-order-review/source-log.md:29`; `change-order-review/derivative-check.md:42` |
| `design-sprinkler-followup/NYC-WTC_000167235.pdf` | 79607 | `e05450bbef04fc1df6005a97233ca8c341f900033f425131686592f2feb9dbd7` | 2 | `design-sprinkler-followup/source-log.md:49`; `design-sprinkler-followup/derivative-check.md:24` |
| `design-sprinkler-followup/NYC-WTC_000167873.pdf` | 40327 | `21dfad1a9da62a6e88869612309277f386f6600e54dfa34889ef4da8975e8b3d` | 1 | `design-sprinkler-followup/source-log.md:50`; `design-sprinkler-followup/derivative-check.md:25` |
| `design-sprinkler-followup/NYC-WTC_000171300.pdf` | 84808 | `8643cab6ed8e8c0caff7cd23c73b1841f6bf6f85a90415786cdf92de530db841` | 1 | `design-sprinkler-followup/source-log.md:51`; `design-sprinkler-followup/derivative-check.md:26` |
| `drawing-review/NYC-WTC_000167874.pdf` | 258425 | `18fd09dd9631551ab11f88fc18f56b759338707739463e2a313cc601c2d705af` | 3 | `drawing-review/source-log.md:33`; `drawing-review/derivative-check.md:37` |
| `drawing-review/NYC-WTC_000173670.pdf` | 67561 | `89dfc492e45ca53e8e1247b07d3bd34cd476d80d5a2f13107f7846a162dc0627` | 1 | `drawing-review/source-log.md:34`; `drawing-review/derivative-check.md:38` |
| `enclosure-framing/NYC-WTC_000172233.pdf` | 145877 | `0c1a0d8ea7c269d297e1d5374c4fa2118b848293a8f6cf49c263c82a6830b3f1` | 2 | `enclosure-framing/source-log.md:38`; `enclosure-framing/derivative-check.md:34` |
| `folder-siblings/NYC-WTC_000167240.pdf` | 79462 | `311bd1d07101b27d4055560cfc95b514c1d4a698a6a3c46bf4c367dbf4ca9321` | 2 | `folder-siblings/source-log.md:36`; `folder-siblings/derivative-check.md:37` |
| `folder-siblings/NYC-WTC_000167759.pdf` | 79419 | `88d8cce3415188e9c24c01b43cb64a3ac1219c681626d65b914c127ad4cedf31` | 2 | `folder-siblings/source-log.md:37`; `folder-siblings/derivative-check.md:38` |
| `folder-siblings/NYC-WTC_000171557.pdf` | 85393 | `d1b979b49cb0f13259ec08a514d2e5629265f1d0f08df4fd2cd7c905cacf615a` | 1 | `folder-siblings/source-log.md:38`; `folder-siblings/derivative-check.md:39` |
| `followup/NYC-WTC_000172166.pdf` | 147759 | `362ad11e3e7b5ac89183be9fa0095f2b0803518e3c854a77ae34f8e626012193` | 2 | `followup/source-log.md:31`; `followup/derivative-check.md:49` |
| `followup/NYC-WTC_000173199.pdf` | 333388 | `37b65cb843cd81716df26af8780627e27bed6d0557eb4b3419945ef742495903` | 6 | `followup/source-log.md:30`; `followup/derivative-check.md:48` |
| `fsk56-followup/NYC-WTC_000174022.pdf` | 135742 | `a2d7dc4ce0e26ac431e98691d387161657f989d1d685a300731aec3b8d79735f` | 3 | `fsk56-followup/source-log.md:58`; `fsk56-followup/derivative-check.md:21`; `fsk56-followup/verification.md:18` |
| `fuel-route-followup/NYC-WTC_000171753.pdf` | 62089 | `537331e3169cc995e7729b60c61a806fb65348eae916f93f6f1bbc48bed47310` | 1 | `fuel-route-followup/source-log.md:58`; `fuel-route-followup/derivative-check.md:10` |
| `generator-job1854/NYC-WTC_000171252.pdf` | 172757 | `5185f82a6b8f15b4db8999924abe9897496076bf2936f995fcfa7e83d1ce8473` | 3 | `generator-job1854/source-log.md:58`; `generator-job1854/derivative-check.md:42` |
| `generator-job1854/NYC-WTC_000172389.pdf` | 172163 | `195af40f88f1dd217caee055b379958abc8a4f0dd06d28e00a775dd325a63b29` | 3 | `generator-job1854/source-log.md:59`; `generator-job1854/derivative-check.md:43` |
| `generator-job1854/NYC-WTC_000172539.pdf` | 171315 | `e4d75191b064c94ebe6687077cf3b9c7030e3b43a0c34e161c77abf50deffe0b` | 3 | `generator-job1854/source-log.md:60`; `generator-job1854/derivative-check.md:44` |
| `generator-job1854/NYC-WTC_000172543.pdf` | 169718 | `aa2ec772603711f97829bcbf85e03f1dcf13631ed68e81439d9c79154b6cbde8` | 3 | `generator-job1854/source-log.md:61`; `generator-job1854/derivative-check.md:45` |
| `generator-job1854/NYC-WTC_000174096.pdf` | 169639 | `4a8e51ca1df5d595c982491e012beb3c305017bf865727915f4e9e03bfabae24` | 3 | `generator-job1854/source-log.md:62`; `generator-job1854/derivative-check.md:46` |
| `generator-service-review/NYC-WTC_000168654.pdf` | 73353 | `7b9824f021e7f38cc80465c8fb7b7499dde90b278831c6d16976655eba960e05` | 1 | `generator-service-review/source-log.md:36`; `generator-service-review/derivative-check.md:51` |
| `generator-service-review/NYC-WTC_000172371.pdf` | 101266 | `a86f55c98227e46108d0691b0faff79c1cde6eac5ee4e3ce0abea1c51376532b` | 2 | `generator-service-review/source-log.md:34`; `generator-service-review/derivative-check.md:49` |
| `generator-service-review/NYC-WTC_000172958.pdf` | 397072 | `8b34d8275b5612f758f9ec411124e58295739df17b0b87adbced82b5bb647875` | 9 | `generator-service-review/source-log.md:35`; `generator-service-review/derivative-check.md:50` |
| `generator-test-results/NYC-WTC_000172395.pdf` | 103619 | `f31ce35607d9017d01748dbf4240a4b6a29fa0d2a0f64f83c3b98317861852b1` | 2 | `generator-test-results/source-log.md:34`; `generator-test-results/derivative-check.md:42` |
| `generator-test-results/NYC-WTC_000172397.pdf` | 35481 | `9507ff6e2e6b1171f2ba5024a979c7d4e6538070bcf00917e7b27020f68b55d1` | 1 | `generator-test-results/source-log.md:35`; `generator-test-results/derivative-check.md:43` |
| `generator-test-results/NYC-WTC_000173715.pdf` | 36410 | `6593c96c2511dd7c668af62143d2038145112b81dc78cf87ec0711a573d61e8f` | 1 | `generator-test-results/source-log.md:36`; `generator-test-results/derivative-check.md:44` |
| `hatch-followup/NYC-WTC_000171497.pdf` | 69607 | `62fb129a8860774a6ffd624915ffd0461340e6dfe4113b7d3227993d1d1ba433` | 1 | `hatch-followup/source-log.md:41`; `hatch-followup/derivative-check.md:22` |
| `hatch-followup/NYC-WTC_000172163.pdf` | 49507 | `163f7e8a65d719ec14affd8591faea94b425abe1424941ca57309086d2735ee2` | 1 | `hatch-followup/source-log.md:40`; `hatch-followup/derivative-check.md:21` |
| `job1854-followup-review/NYC-WTC_000167866.pdf` | 114201 | `2558231620941df315322833fb001d78e6b633901e62acf5a3a0bfd5947107f4` | 2 | `job1854-followup-review/source-log.md:39`; `job1854-followup-review/derivative-check.md:54` |
| `job1854-followup-review/NYC-WTC_000171251.pdf` | 64028 | `80680fc00c57f0920f0387ae1f87b71c40c34c254223c8fb44e467dce4818b4d` | 1 | `job1854-followup-review/source-log.md:34`; `job1854-followup-review/derivative-check.md:49` |
| `job1854-followup-review/NYC-WTC_000171520.pdf` | 44470 | `109b1447b5a64ca57f0fd9cacb4d45ec41cc76aa52b71a495e9a39528bcf7d26` | 1 | `job1854-followup-review/source-log.md:37`; `job1854-followup-review/derivative-check.md:52` |
| `job1854-followup-review/NYC-WTC_000172976.pdf` | 67745 | `9528aa1900afa59334f516ff2e3e50a23cba4b92231a62e5cdb7d6df19729618` | 1 | `job1854-followup-review/source-log.md:35`; `job1854-followup-review/derivative-check.md:50` |
| `job1854-followup-review/NYC-WTC_000172977.pdf` | 60316 | `d6de130d5ebd7376bdfb142819458afd211562cfb024456c29be2f6973eda931` | 1 | `job1854-followup-review/source-log.md:36`; `job1854-followup-review/derivative-check.md:51` |
| `job1854-followup-review/NYC-WTC_000174095.pdf` | 55156 | `732e42d9aff12e7536d9dfeda1d81f95ca7edf0f5c58d6b39bce5003ad894288` | 1 | `job1854-followup-review/source-log.md:38`; `job1854-followup-review/derivative-check.md:53` |
| `oil-route-packet/NYC-WTC_000166828.pdf` | 533928 | `3812f9cf9399f044943bf718dcdc5cdad42dd0416a9cea7be10714168edca2e9` | 8 | `oil-route-packet/source-log.md:33`; `oil-route-packet/derivative-check.md:32` |
| `structural-followup/NYC-WTC_000171807.pdf` | 35750 | `1c0753e27edd92e4bc4dde5389f1b1a291bf3ee113a1600b47e73bc373816ab4` | 1 | `structural-followup/source-log.md:36`; `structural-followup/derivative-check.md:46` |
| `structural-followup/NYC-WTC_000173900.pdf` | 107823 | `6dac8359d2f3c9ea98721c1b69f55038838d6755ea806d114cd55ff0b81d86df` | 2 | `structural-followup/source-log.md:37`; `structural-followup/derivative-check.md:47` |
| `various-orders/NYC-WTC_000167170.pdf` | 104270 | `3a2fce21c438e04d976eae93b8e1225d388c008aa28d72aad58af3e433b4033c` | 2 | `various-orders/source-log.md:23`; `various-orders/derivative-check.md:40` |
| `various-orders/NYC-WTC_000171802.pdf` | 113155 | `7ab6722000bac41812f2fc796846d04212f6cbabad5c96d1d3109c85d5ffeee2` | 2 | `various-orders/source-log.md:24`; `various-orders/derivative-check.md:41` |

## Existing pin-receipt snapshots

These 39 existing receipt files were hashed as inputs; their substantive/render assertions were not rerun or promoted by this integration check.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `approval-breakdowns-a/derivative-check.md` | 11363 | `9d18aa9ee2bc64776e23f4378fe6fbc7885b8ea179c4ced07348df5dcab9f2e6` |
| `approval-breakdowns-a/source-log.md` | 12077 | `a3172351708e1fad8d9ae72df40b7baed2d6ee03c30a9298dd99347b84e0e445` |
| `approval-breakdowns-b/derivative-check.md` | 9367 | `db4a7e4d70a6831c993a065198eae7e957ce76126ea65317579377f0b0f6b20f` |
| `approval-breakdowns-b/source-log.md` | 13748 | `3cae4b1849ba997cef94c34a8c91fe20811e6b0635e65066f2e05a8ac8733b21` |
| `change-order-review/derivative-check.md` | 9464 | `7c107c9571a227ebb32fa47ecbc164a2482947789bbb1fa05d475c98b911039a` |
| `change-order-review/source-log.md` | 11147 | `0eb8b8ded26e5c1dfd8d233ed2db7069ff6efad8be3b8ab5cb90d75880eeff42` |
| `derivative-check.md` | 7962 | `d3ed230d1d649ecc8693c0fc69940c3920444acf4eca2960c0f2ca628f15563a` |
| `design-sprinkler-followup/derivative-check.md` | 5524 | `b37b1250c93707324f23a1a506e0fc5964b74dbdffdae42cec78230cce7e6478` |
| `design-sprinkler-followup/source-log.md` | 9509 | `7363cbc6a1f47f4242bb71d320aeae86af7e8c87159085141519a0e022a875d2` |
| `drawing-review/derivative-check.md` | 8129 | `81fa3f3eb3286e1befafdb7308f4c076598fa3c4c4c56b5ed2a3351e35f0f43e` |
| `drawing-review/source-log.md` | 11291 | `6f5a1688216c621b5c16eefd30801df291814a38ac4263ed1c52a441e0314ff3` |
| `enclosure-framing/derivative-check.md` | 3460 | `15b734ab180574ceff3a0e0d4e2a0f1c1f5afbf24680939e056207cb8398278d` |
| `enclosure-framing/source-log.md` | 7751 | `0bd928d535751a4b358789467f0c808d96f89e0d820e798ce6a3b9ecf26780eb` |
| `folder-siblings/derivative-check.md` | 7394 | `cb78af7d54b78a46fc017071c6daa3a20c70a221835eb8c3f505f7f941555d20` |
| `folder-siblings/source-log.md` | 8230 | `fd6af1a5afdfae86390782f42808d3731f6a7529945a1938ac971044345f8f6e` |
| `followup/derivative-check.md` | 5022 | `005f7302f3bf5221afb5ebed476e3a47ff055c0f8a5d5d020ec8d8833b6eea8c` |
| `followup/source-log.md` | 6608 | `9dcfecbce2ca7e941d07b057ca2419215b149395be71f4fc0e667d7f9d2226d8` |
| `fsk56-followup/derivative-check.md` | 7277 | `68d28b63524fc7323d9ec68bb826992e91a5742d4a6e8c956bd1b60d9eb926b4` |
| `fsk56-followup/source-log.md` | 8416 | `903209e16cc84d399c4e47001b0555fadedd8e3af3b8275d05f546579850cc36` |
| `fsk56-followup/verification.md` | 5345 | `3de4f45d1435b16296c79b379ef8b80810308aac920cd64aa4ae507a0cceeb0b` |
| `fuel-route-followup/derivative-check.md` | 5411 | `51ed53aa625cbdfc5b82905e0180abd13dae450413f96ea8930b4c43fe1b8181` |
| `fuel-route-followup/source-log.md` | 7116 | `56fd2a568035da262aa616df014f7cdad70215ff55aaf16849b3e1dadf86b075` |
| `generator-job1854/derivative-check.md` | 12399 | `c3e6271c80e7bd47ec7fb43c08a95d407e3983306807dd51e3a2a7cc555fac18` |
| `generator-job1854/source-log.md` | 10109 | `43f1d9a4a0cd4764c4753f417eb12b3271a09c5a97705dcd52e05fa1ea11623d` |
| `generator-service-review/derivative-check.md` | 12327 | `f794a60ec170fcce72226496111be663bcc04a5ead1d971fa250303c2ece2b16` |
| `generator-service-review/source-log.md` | 10967 | `21852f7d411b59b0c3ea485c141b05a8789f3f83905d375b8da44f18ab2eb6ac` |
| `generator-test-results/derivative-check.md` | 9472 | `2c9d165ed9f1e6c99e06d5b146238f681b33a873afb9590b74babe0bcdc493bf` |
| `generator-test-results/source-log.md` | 7986 | `e1967f66f3e73df1e5d156601eccc05306747cffc8212419f2a93d24f044f743` |
| `hatch-followup/derivative-check.md` | 5042 | `063a2974ded45bfdec057dbce993968becc17081520e8d10eca89c1fa78be0db` |
| `hatch-followup/source-log.md` | 8022 | `32c77493cf71d74e1da983572fe247586ec178fad3fa5fc4dbd31029152c92cd` |
| `job1854-followup-review/derivative-check.md` | 12273 | `dd6d019817b59b7b14dc03b12f440e32be947b969458d28eeec4e81e96220d89` |
| `job1854-followup-review/source-log.md` | 9304 | `176dce01c4218d321bc43d62f2a94510e21d39f5cea8400a81bc2960b41de292` |
| `oil-route-packet/derivative-check.md` | 11085 | `80b47ec12e9144d419c0f73fac3840dd92630014695ee2cd1c8c363274e5b0b1` |
| `oil-route-packet/source-log.md` | 11526 | `c760ef2addddd182294da1e6e2b497d9249e8710d8ec9b24f62c0c67ee35ec2d` |
| `source-log.md` | 10658 | `11d7792df0e4080a14e32e9e65281cb2f009eb160f143f6115ad8da341cb1961` |
| `structural-followup/derivative-check.md` | 4426 | `7182fc77523f7afc11185690e789214fed6275d721518aa14bec51eec7180734` |
| `structural-followup/source-log.md` | 8290 | `22217565f8b248d7dfe12eb5e237e66884befbd318b6e81c534cf96ca88100c7` |
| `various-orders/derivative-check.md` | 7988 | `712acee0a79e5bc405814dc91fb47063dc88bbac9f4c10d9ca4ba0afb1a0610d` |
| `various-orders/source-log.md` | 9226 | `cd328cfed63518cf024c6b823090b808eed041399ef30a652e917ef93841cf94` |

## Fixed report snapshots

The report files were inventoried and hashed, not reread as primary evidence by this checker.

### Twenty content reports

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `report.md` | 8829 | `e5274f088935d459a4ff733b5560517af1feb4544d00413f2173a45c1e2d828a` |
| `followup/report.md` | 6784 | `ae94174aa04498144d439c75e44eb869dbe1284d7ad40104add60a43ef141e54` |
| `structural-followup/report.md` | 6452 | `63f41c26b2b13b6df455825eab3056617d4ec861ebb2185a8fd9951edfafddcf` |
| `hatch-followup/report.md` | 7793 | `ad9e38c525a4988d5aefca5053b5941cf9ed0b4067c4e518bee978a40c6ad34d` |
| `fsk56-followup/report.md` | 5408 | `29d2d9aa26dd7d2dfb03056cbcce97cadb40d2c92e3bb9305d12619b610c2d4e` |
| `design-sprinkler-followup/report.md` | 7564 | `b38eedd5fbfe6f7495dda09a75c353e1f373cc60e88f0e57704cc5e26af2806c` |
| `enclosure-framing/report.md` | 5970 | `60affd797ca2c644c4ea908c77e854eda23b739fd715a9fc90c5a393fd78acba` |
| `enclosure-framing/oem-comparison/report.md` | 9196 | `f7f05726895ed35f087d3604fdeb9797cb6d863ef1661915338b5cf3fdac95ba` |
| `fuel-route-followup/report.md` | 6608 | `9f2146edeab41447edd31f2043a9d1e570828ab25476f05a6f85855965a05df6` |
| `oil-route-packet/report.md` | 13251 | `0aa295e21cd7d7bb2dd9010e13bdd84ca7188e8504754afb0dc3cc5e3846366d` |
| `folder-siblings/report.md` | 5723 | `b46a2a4bf0ced2125dbe50fc29e004f76e25358c42b2b63f28f16e0e04d3e451` |
| `drawing-review/report.md` | 12138 | `0661d0ddaf3398332905565921591a981490eda9b9b212f88f957073b9b9cd7d` |
| `change-order-review/report.md` | 14532 | `bd58b2685b2a421cf8dc4df897a765d885c9bc21fbb92f504fe45342a4a74a76` |
| `various-orders/report.md` | 10345 | `722ef41578c31dbadb97f8df5e629799c304671800e9f8331db521f3afe81c19` |
| `approval-breakdowns-a/report.md` | 13428 | `2500a4d7710068654b287b08fb25a831a8cf4c16296d262ca538f2cf5412613d` |
| `approval-breakdowns-b/report.md` | 13858 | `82c024ff07ed24ab6fc45f52b62de43e038af7c40af5126295de64a9e389e54f` |
| `generator-test-results/report.md` | 5978 | `1836ee92c3db5b185fb4c9094ed9ae90a2d1f8ad26f62660870c14671eebb889` |
| `generator-job1854/report.md` | 9105 | `f9c6e2e42e615a6fd032ccae735dcc3a1d9cc1933f8006e243e311e34bf739d3` |
| `job1854-followup-review/report.md` | 12076 | `b567a540a80867180b08194bf7556a1a8fc3f955bccbeeabb90c019d2bbb19ee` |
| `generator-service-review/report.md` | 12440 | `0b011992cf5d369133b27dad8b8dd5205e03196572d9c6e4ef15bd1e966f74d2` |

### Five locator reports

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `held-record-locator/report.md` | 8087 | `53625d5b825d8ad81d7e4d4cc2f27cb14463bf228b8b9df18ad20008c13b3845` |
| `drawing-locator/report.md` | 6773 | `9f004475e404fe4dcf36fef56d1f0c78f672e45427bd491d72780e48bd1086c5` |
| `folder-document-locator/report.md` | 6659 | `410a4190ec8951a8aa9da78e22bdf1ef5e75155f2d12e7c999b0c57031d7152d` |
| `test-acceptance-locator/report.md` | 5269 | `57feacfb896383fcffedbfc79c9c94a5492dc8a361234b438a773ab9fd3b7eca` |
| `job1854-followup-locator/report.md` | 8245 | `f5b8b4f2fe04e4a9ab0a1f5deacf017278877d1e0301f0d3f62a125dbeb64d28` |

### Three outside context inputs

These plans/reviews are context, not new independent source evidence or new acceptance of their underlying claims.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `/Users/admin/docs/911/research/wtc7-operational-evidence-plan.md` | 20736 | `e6ced568a9a3226af8735f65f7440ee495233d8a3122c395ea82ffe34e147535` |
| `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/completion-audit-2026-10-04/documentary-review.md` | 22205 | `6b8d9584c4ee6527e48b5a477f260344cc2bcfbf1370258eb726f7457e4406b9` |
| `/Users/admin/docs/911/research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/installed-records/relevance-review/report.md` | 13288 | `a73606443e106890875d5fd5a5a3bd7abc72c12b77938f880fae4de21fb00729` |

## Final snapshot validation

Final size/hash validation passed for all **116 listed input files** (49 PDFs, 39 receipt files, and 28 reports/context inputs), with no mismatches; the current PDF path set also exactly matched all 49 listed paths. Receipt `595dfc`, exit 0, ran 2026-10-05T03:47:29.705087+00:00–2026-10-05T03:47:29.862940+00:00, elapsed 0.157870 seconds. It did not reparse pages or repeat source rendering. The exact stdout-only command was the bundled Python interpreter shown above with this here-document body:

```python
from pathlib import Path
import hashlib, re, time, datetime, json
M=Path("/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04")
t=time.perf_counter()
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
note=(M/"integration-inventory.md").read_text()
rows=re.findall(r'^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|',note,re.M)
failures=[]
for name,size,pin in rows:
    path=Path(name) if name.startswith("/") else M/name
    data=path.read_bytes()
    if len(data)!=int(size) or hashlib.sha256(data).hexdigest()!=pin:
        failures.append(name)
actual={str(p.relative_to(M)) for p in M.rglob("*.pdf")}
listed={name for name,_,_ in rows if name.endswith(".pdf")}
if actual!=listed: failures.append("PDF_PATH_SET_MISMATCH")
if len(rows)!=116 or len({name for name,_,_ in rows})!=116: failures.append("INPUT_ROW_COUNT")
print(json.dumps({"start_utc":start,"end_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"elapsed_seconds":time.perf_counter()-t,"checked_files":len(rows),"pdf_paths":len(actual),"failures":failures},indent=2))
raise SystemExit(0 if not failures else 1)
```

## Limits

No network, new acquisition, raw-header/cookie/contact output, PDF text extraction, image view, OCR, crop, rendering, engine operation, Git mutation, or main/legal file edit occurred in this inventory task. Old render receipts remain old receipts; only their present bytes and source-pin associations were checked. No historical authenticity, installed-state, safety, engineering, causal, legal, or human acceptance conclusion follows from this inventory. The fixed 20 reports and five locators are a declared integration population, not a claim that the municipal archive or relevant historical record is complete. The 49/123 totals describe only PDFs currently held within the exact base directory, including any copies that might have existed; no byte-identical copy was actually found there. Outside references and semantic near-duplicates are not counted as independent evidence.
