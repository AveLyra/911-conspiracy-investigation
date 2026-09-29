# Batch 2 source and coverage audit

Research derivative under the unchanged investigation charter and main repository `AGENTS.md`, `WORKFLOW.md`, and `START-HERE.md`. Source reviewer: separate Codex AI agent `/root/fire_coverage_sources`; not a human forensic specialist. This audit records document attribution and extraction integrity. It creates no appearance labels and authenticates no historic camera capture, clock, facade identity, floor location, physical mechanism, or intent.

The evidence-falsification, source-of-truth, and PDF skills informed the separation of report assertions from image observations, full-page caption review, same-origin grouping, and preservation of source uncertainty. No authority boundary was crossed and no legal spine, original source, sent/filed artifact, or old review record was changed.

## Coverage and integrity

The frozen key contains 28 distinct JPEG objects on 23 full pages. Twenty-five are photographic report images and three are geometry graphics. The prior main and reviewer records contain the same 12 unique photographic asset IDs. Subtraction leaves exactly the 13 declared batch-2 photographs, on 10 pages. All extracted JPEG filenames agree with the key; no extra or missing JPEG was found.

`inventory.py` enforces the protocol hash, the exact declared 13-ID set, the key and both prior-review hashes, the report hash, exact counts, uniqueness, and complete photographic/geometry partition before output. It rehashes all 28 JPEGs, all 28 decrypted encoded streams, all 28 encrypted on-disk streams, and all 23 full-page PNGs and both corresponding context files. JPEG dimensions agree with the key. Every JPEG hash also equals its preserved decrypted encoded JPEG stream hash. It checks the source report before and after. These are fresh file-integrity/coverage checks; the earlier independent-parser extraction checks are cited through pinned receipts and were not rerun here.

| Artifact | SHA-256 |
|---|---|
| Preserved NCSTAR 1-9 report | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` |
| Protocol | `8ea3df6a4550e55de334ac20ce45a8fb05aa00f47800a6ca7b874f74803d94ff` |
| Reviewed extraction key | `c0361c5a3ae52c2663a6772db6078824b4b123e59d8e50d2e24b26d85855afa3` |
| Prior main review | `d7673cc50ebca454ea30a0d2c45e44041e9d06de9f586e32dd27a65818f535ce` |
| Prior separate review | `03c671cfb383e939509e0008101a81e4954141c8c8f680596bbecde573f128f0` |
| This `inventory.py` | `6b952d2dad01e66e58f18652e943cb1e93c82d07ab60c5dd4a309c8262245dd1` |
| `source-attributions.json` | `d86eeaabcc5e6628004ca78b819576ede846665dba82a16e50b099828481bce0` |
| `inventory01.json` | `8d16768c37ccf00a81c9fb1441427360d00d2cc679b8c9e38fefc1e7caacbda9` |

The first inventory execution reached exclusive output creation after successful checks but received `PermissionError: [Errno 1] Operation not permitted` for `inventory01.json`, because the investigation worktree is outside the initial writable roots. No output was created by that attempt. The same command then succeeded with narrowly scoped escalation; no automatic-review rejection occurred. A separate read-only `--check` run reproduced the complete in-memory inventory and passed. There were no failed data assertions and no source edits, new extraction, render, crop, enhancement, download, network call, or transmission.

Commands used the installed runtime:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/fire-coverage-batch2/inventory.py
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/fire-coverage-batch2/inventory.py --check
```

This closes the inventory gap for the declared 28-object extraction only. It does not establish coverage of every NCSTAR photograph, public recording, facade, floor, time interval, interior space, or WP1 question.

## Source-page inspection and namespace

Every figure in this audit belongs to **NIST NCSTAR 1-9, Chapter 5**. Physical PDF page numbers are one-based. For these pages, the printed number is physical minus 44; printed and physical numbers must not be interchanged. Figure associations follow visual page placement, not PDF object invocation order. Page 255 invokes the lower Figure 5-126 first and upper Figure 5-125 second; page 285 similarly invokes lower 5-158 before upper 5-157.

All 23 existing complete 935 x 1210 page PNGs were inspected for figure placement, caption text, source credits and printed page numbers: physical 149, 154, 157, 198, 199, 214, 235, 239, 240, 242, 243, 244, 245, 246, 247, 248, 255, 265, 267, 278, 279, 280, 285. The 13 new photographs occur on physical **198, 199, 235, 239, 243, 244, 246, 255, 265 and 285**. Per-page IDs, absolute PNG/text paths and SHA-256 values are in `inventory01.json`.

Supplementary PDF text was read directly, without output files or rendering, on physical 161-165, 233-234, 238, 241, 253-254, 264 and 284. This supplies section and neighboring-figure caveats. These supplementary pages were text-reviewed, not newly visually verified. Page 233 provided preceding section context and no new image attribution. Existing page PNGs were usable, so no new rendering was necessary.

| New asset | Figure | Physical / printed | Report-attributed view and timing |
|---|---|---|---|
| A-873f87e7149b | 5-60 | 198 / 154 | South face, helicopter photograph; around 12:35 p.m. |
| A-f1e2fa01e344 | 5-61 | 199 / 155 | Enlarged, intensity-adjusted portion of 5-60; no new timestamp |
| A-e1b0c06ad11d | 5-104 | 235 / 191 | North face looking down Greenwich; 11:28:15 a.m., no individual uncertainty printed |
| A-9e7b4935c8aa | 5-109 | 239 / 195 | Southwest corner around 22nd floor; caption 12:10-12:25 p.m.; preceding prose conflicts on a.m. |
| A-0b722775db93 | 5-110 | 239 / 195 | West face near south edge; 12:27:30 p.m. +/- 1 s |
| A-fa6f410444bb | 5-113 | 243 / 199 | Northwest corner lower floors; enlargement of 5-64, estimated 2:15-2:45 p.m. |
| A-ffe3726a0312 | 5-114 | 244 / 200 | Oblique east face; 2:08:28 p.m. +/- 1 s |
| A-0e60b82a1a4c | 5-116 | 246 / 202 | East-face video frame; estimated interval 2:15-2:27 p.m. |
| A-671f312eade8 | 5-125 | 255 / 211 | North face, caption assigns 7th and 12th floors; within a few minutes of 5-124 |
| A-6902e91e39ee | 5-126 | 255 / 211 | North face, caption assigns 12th floor; 3:11:15-3:16:51 p.m. |
| A-69d899e75343 | 5-135 | 265 / 221 | East edge of north face and oblique east face; likely 3:20-3:40 p.m. |
| A-7b61385d1373 | 5-157 | 285 / 241 | North face from northeast; within a few minutes of report's 5:20:52 p.m. collapse reference |
| A-8bc36f05fe38 | 5-158 | 285 / 241 | Western edge of north face; same approximate collapse-relative wording, exact event time unknown |

These are report claims, not reconstructed time measurements. In particular, 5:20:52 p.m. is not the exact capture time of either 5-157 or 5-158. The approximate timing of 5-125 must not inherit Figure 5-124's 3:10:46 p.m. +/- 3 s precision. Full-page credit text and all per-image processing/local caveats are retained in `source-attributions.json`.

## Origin dependencies and credit limits

1. **5-60 and 5-61:** same NYPD photograph, with 5-61 an enlargement/intensity-adjusted derivative. They are two extracted samples, not two independent captures. The report's east-edge overlay uses an assumed parallelism because smoke obstructs the edge.
2. **5-113:** explicitly enlarged from 5-64, which is outside this 28-object extraction. Same NYPD institutional credit as 5-60/5-61 does not establish the same camera or exposure. This audit verifies the derivative statement, not the absent original's capture chain.
3. **5-157 and 5-158:** physical 284 says the camera zoomed during the clip used for 5-157 and that 5-158 shows a pulse within that sequence. Treat them as a report-linked sequence with unresolved credit: 5-157 displays Fox News, while 5-158 is explicitly `Source: Unknown`. Neither overwrite Unknown with Fox nor count two independent videos merely because the asset/credit fields differ. The report itself says exact event time is unknown and cannot be associated with a known WTC 7 event; the isolated JPEGs cannot establish the stated pulse duration or mechanism.
4. **Repeated credits:** group the Spak material conservatively as one credit family; the page for 5-59 prints Steven Spak while other entries print Steve Spak. Frank Didik appears in 5-125, 5-126 and prior 5-150; Richard Peskin appears in prior 5-148, 5-149 and 5-151. A repeated photographer/organization is a dependence warning, not proof of the same exposure, and different names alone do not prove independent custody or clocks.

Inventory implementation caveat: `source_credit_family` preserves full visible credit strings for some prior entries and shortened family names for new entries. Consequently it is **not a globally normalized categorical code** and its unique-string count must not be reported as an independent-source count. For grouping, use `source_credit_as_displayed` with the equivalences just stated; the explicit `origin_group` links for 5-60/5-61 and 5-157/5-158 already agree. This mixed-key limitation is recorded rather than overwriting the completed inventory. Geometry graphics share the report source and are reference-only; they supply neither historic fire captures nor independent measurements.

## Material source limitations and claim strength

The following are the strongest directly supported audit claims (grade A **as statements about the preserved source or checked bytes**, not grade A historical/physical claims): exact extraction-set membership, checked hashes/dimensions, visible figure placement/credits, report-stated transformations, and explicit same-origin relationships. A changed hash, differing prior set, or mismatch between caption placement and object association would falsify those claims; none was observed in this run.

Historical timing, scene geometry and fire/window assignments remain report-attributed. No original camera file, clock-calibration worksheet, complete adjacent sequence, or independent survey was authenticated here. The strongest disconfirming material against overconfident fire-timeline use is the report's own qualified language:

- Physical 161-164 / printed 117-120 describes sporadic imagery, building obstruction, smoke/dust and access limitations. Some camera clocks were tied to known events; many other times were estimated from shadows or fire-window positions. Appearance-derived timing cannot become independent support for the same appearance-based spread claim without an additional check.
- Physical 164-165 / printed 120-121 explicitly distinguishes no visible flame in an observable window from code 9 for smoke, inadequate resolution or no suitable image. This prevents source-image nondetection from being translated into absence of fire in unseen spaces.
- Figure 5-104 is embedded in early smoke/dust context. Physical 234 limits its negative wording to the visible north-face portion. It is not a building-wide no-fire control. Figures 5-60/5-61 occur in structural-damage discussion and do not receive an independent new fire timestamp merely by entering this annotation batch.
- Physical 240 says wind could bank smoke against the south face and prevent source identification. Physical 244 says Figure 5-114's steep angle prevents precise fire-window identification. Physical 254 says 5-126 does not extend low enough to show floor 7. A lower floor missing from the frame is unobserved, not negative.
- Figure 5-135's caption identifies background WTC 5 and WTC 6 and the U.S. Post Office foreground. Its entire visible bright region cannot be assigned to WTC 7 by proximity. Physical 264 says some lower east-face smoke cannot be sourced and brackets the image's unknown time from comparative appearance.
- Figure 5-109's caption says 12:10-12:25 p.m. but physical 238 prints 12:10 a.m. at the lower bound. Prior Figure 5-111 prints 12:28 a.m. +/- 3 min while adjacent sequence is p.m. Physical 235's unrelated Figure 5-105 discussion prints 12:10 a.m., and physical 241 prints 12:45 a.m. in a daytime sequence. These are source text inconsistencies, not grounds to invent a verified corrected clock. The caption-specific claims and conflicts remain separately attributed.
- Crops, enlargements, intensity adjustments, labels and arrows predate this audit and are often explicitly disclosed. Preserving native **PDF** JPEG bytes does not recover native **camera** pixels, original dynamic range, lost surroundings or full processing history. These limitations are not evidence of manipulation or wrongdoing.

The highest-value next checks are the original photographs/full video sequences and their clock-calibration/derivation records, especially the 5-60/5-61 original, the 5-64 parent of 5-113, the approximate 5-116/5-125/5-135 times, and the conflicting credit/exact timing of 5-157/5-158. Those inputs could strengthen, change or falsify precise facade/time interpretations. This bounded audit neither retrieves them nor supplies their missing information. It provides no interior temperature, burning duration, fuel/ventilation history, fire extent, structural consequence, collapse-cause ranking or intent finding.

No root or fresh-reviewer image labels were opened. The root later reported both observation records frozen before source findings were released; the image-record files themselves were outside this agent's read/write task. All edits were confined to `inventory.py`, `inventory01.json`, `source-attributions.json`, and this review in the assigned investigation worktree directory.

## Source-review correction disposition - 2026-09-16

The source reviewer checked only the three requested corrections in `report.md` (checked SHA-256 `737245b4e522ddd9dae0fd39c64e451184ac1070773819bcbf1aa112830b49bc`). All three are resolved: the Figure 5-116 row now states that its interval was estimated and its exact time remains unknown; the Figure 5-126 row calls the source a photograph; and the first claim-ledger row distinguishes the prior pair's 12 images from the current pair's 13 new images. No new source work or appearance review was performed for this disposition, and no report, raw label, attribution JSON, or generated inventory was edited. The original review text and all preceding pins are preserved; the pre-append review SHA-256 was `0bad5f39047f99a2252f232eeb12e8f680407282469926037b2713ce77d1bdd1`.
