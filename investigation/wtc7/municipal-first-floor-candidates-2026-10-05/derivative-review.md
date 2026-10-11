# Drawing-candidate derivative verification

October 5, 2026. Independent mechanical reproduction, not a source-content reading. **All 29 initial rasters pass full-byte and dimension comparison, from two completed independent rendering processes.** Both readers subsequently closed their new-page sets at those 29 initial rasters, with zero larger repeats; this closes the declared new-raster reproduction coverage. No complete-content-review or historical-authenticity acceptance is claimed by this derivative result.

## Scope and preflight

Read the complete frozen [protocol](PROTOCOL.md), SHA-256 `60a2b129cf6d67b5b8204a6756ff7919c86a63fd4e06d3761c8215404aaf23f2`, and applicable PDF/evidence/source skills and required references. Main AGENTS, WORKFLOW, START-HERE and charter pins match the previously read controlling versions. Receipts `372984` and `56d776`, exit 0. No blocking method issue; the parent accepted the clarification that no interpolation means no **additional post-render alteration**, not a claim that the renderer/viewer performs no scaling or resampling.

This reviewer did not open source images, extract PDF text, inspect root/peer observation files, interpret drawing fields, download sources, or execute a structural model. The source-log read (`ea62ab`, exit 0) concerned process/representation only. The two admitted PDFs and named root rasters were used only for hashing and rendering/byte/header comparison. Source admission and historical/public provenance remain separately attributed to the acquisition record; this is not another network witness.

## Inputs and separate rendering environment

| Source | Bytes | Admitted page population | SHA-256 |
|---|---:|---:|---|
| NYC-WTC_000173192.pdf | 253273 | 4 | `6e3433d6addbb43c79625ae6b7564fd8d353dbde1d55ff45997323167e598ad1` |
| NYC-WTC_000169180.pdf | 4451736 | 25 | `e7c938b689f9e4d0c2a1146349a637dde7edccdd384d7bfc8dc5ccd0d473c513` |

Source/config checking and creation of the separate scratch directory completed `f7829f`, exit 0. New directory: `/private/tmp/wtc7-plan-candidate-repro.9KnhR8`. Its `fonts.conf` was created with apply_patch and names `/System/Library/Fonts`, `/Library/Fonts` and its own `font-cache` directory. The cache directory was separately created; configuration specifies it but directory existence alone does not prove fontconfig used it.

Bundled runtime paths were obtained through the workspace dependency tool. `pdftoppm -v` independently returned **26.05.0**. Pre-render source pins, identical font-directory lists/different cache directories, and presence/valid PNG headers of all 29 root initial rasters passed `e88870`, exit 0. All initial root rasters have maximum dimension 2400; orientation is preserved, not inferred as documentary geometry.

| Environment item | SHA-256 |
|---|---|
| Bundled `dependencies/bin/override/pdftoppm` launcher | `de772e88ab9977ccde25def9b403bf42675d75f5dd82b19fbd7d8123ad183159` |
| Bundled `dependencies/native/poppler/poppler/bin/pdftoppm` binary | `98ac4fedc4258b7125ad1048034c1448dccc58503614eb105f19d12cdb3a2d0d` |
| Preserved root fonts.conf | `ea6ddd53f5c13830c73ac159bf59fc1ee0f1a0c30faf3226a501cac89a489272` |
| Separate reproduction fonts.conf | `755546e5588b59c56d78b9f10cbfad1a3328d29f3eb1e5952d31ae47688b037c` |

The launcher and binary paths are under `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/`. Root uses a different private cache `/private/tmp/wtc7-plan-candidates.nzCgwO/font-cache`. No source or root derivative was edited; reproduction outputs and their diagnostics are in the new scratch directory.

## Actual commands and terminal states

Both calls used the absolute admitted PDF path under this unit, absolute output prefix in the new scratch directory, and the explicit font configuration. The exact command pattern was:

```sh
FONTCONFIG_FILE=/private/tmp/wtc7-plan-candidate-repro.9KnhR8/fonts.conf \
  /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm \
  -f 1 -l PAGE_COUNT -png -scale-to 2400 ABSOLUTE_UNIT_PDF \
  /private/tmp/wtc7-plan-candidate-repro.9KnhR8/ID \
  > /private/tmp/wtc7-plan-candidate-repro.9KnhR8/render-ID.stdout \
  2> /private/tmp/wtc7-plan-candidate-repro.9KnhR8/render-ID.stderr
```

The two processes were launched once in parallel, with pairs `(PAGE_COUNT, ID) = (4, 173192)` and `(25, 169180)`. No input was recomputed or operation restarted merely because a tool yielded.

| Reproduction | Initial receipt / handle | Terminal receipt / exit |
|---|---|---|
| 173192, pages 1–4 | `f65262` / 1192 | `f0820f` / 0 |
| 169180, pages 1–25 | `4d9102` / 56633 | `495e30` / 0 |

## Completed initial four-page check

Direct complete-byte comparison, PNG signature/dimension checks and unchanged 173192 source pin passed `781d0d`, exit 0. Exactly four reproduction PNGs exist for that initial prefix. Each matches its same-name preserved root image, not merely its dimensions or a perceptual similarity score.

| Raster | Bytes | Width × height | SHA-256 |
|---|---:|---|---|
| 173192-1.png | 150933 | 1784 × 2400 | `75b6167e3e20135fc4e780285b0e5eac8e33635d9844ef7c4336f01839f4c7d9` |
| 173192-2.png | 163254 | 1791 × 2400 | `58c6ac42ee352eb3e3c40a77ee9af74b083934ec375385482f4f6e47b7508cda` |
| 173192-3.png | 179010 | 1786 × 2400 | `9baf1a5422291e959253e5c63690a4128cf5127ff37092bf376d2252c0c086e0` |
| 173192-4.png | 74885 | 1786 × 2400 | `160e2f7b2d2f70433f05c87ed2a718f2e160658e50bb284268f8c6b44e74e4e2` |

The reproduction's stdout/stderr and preserved root `render-173192.stderr` are all zero bytes. Empty-byte SHA-256 is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. This is an actual diagnostic observation for those completed files, not a general warning-free/source-quality certification.

## Completed second-packet check

After handle 56633 actually returned terminal exit 0, the complete-byte/header comparison passed `6873e3`, exit 0, for exactly all 25 second-packet PNGs. Both admitted PDF byte counts and SHA-256 values were unchanged after reproduction. No substitute rendering or repeated attempt was necessary.

| Raster | Bytes | Width × height | SHA-256 |
|---|---:|---|---|
| 169180-01.png | 168557 | 1803 × 2400 | `3b9706d0487f3a6e4d13b4e76f5560489d1e4806f039150fd47b262581c4fc9d` |
| 169180-02.png | 120486 | 1803 × 2400 | `885d2ce4f933a17fcc54b4dd435351a8fa039aa094cab79c446fa1dfc04bfbc5` |
| 169180-03.png | 142535 | 1819 × 2400 | `df921209c8b19a1b1fe83393c512f8c56f2303e7a4ee1188753fe23ca11a3c32` |
| 169180-04.png | 26442 | 1794 × 2400 | `b32540f5c75ed744232048ac47f341468f267318771c63ece60cd91a8d46ba02` |
| 169180-05.png | 360421 | 1428 × 2400 | `48d16e2be9f39f5227f442a210f6960c982f0d52375f445db48df34d9a84a314` |
| 169180-06.png | 413876 | 1434 × 2400 | `6a3b67f21bd5baf0801901dfe73d6f31e47e760abf7ad8b4b65c7b0056439d73` |
| 169180-07.png | 379908 | 1440 × 2400 | `fcfde37ae153c72e30431e53a71b7eb2aa0d0c72d6d8bf7da45257025be0ec42` |
| 169180-08.png | 273038 | 1440 × 2400 | `77bd7cdf3e37323893278150ade18466ff5e0e0ebcce6631addbc99c96d89edd` |
| 169180-09.png | 441387 | 1435 × 2400 | `c26e4bab27e39ecd30e5a72eabf9d1a5b6bc8b8e6ab425c5f55a25837b503b36` |
| 169180-10.png | 322735 | 1456 × 2400 | `cb17f505e0260e046b2d2fed5071c0d0289c1dd51bea86bf7528c7e604b71505` |
| 169180-11.png | 187883 | 1803 × 2400 | `e98e5620215b5c9f7bf93f0b8a07ea0d5ee14c7338416e793c6ca86ddd06c228` |
| 169180-12.png | 119524 | 1803 × 2400 | `5068942ba83e7a296dd3ae449b156c896448e91d9b5a60c1b9291b73aacd5850` |
| 169180-13.png | 98952 | 1803 × 2400 | `b5fc8b4c933bebce833236262efc3a78a9e2ece4882df912935cab0f8a06147f` |
| 169180-14.png | 87133 | 1808 × 2400 | `3cbeacec76f475371949bd1a2a085ad04cebdd34b5fa4a9bd6cdd5f852c4213d` |
| 169180-15.png | 197210 | 1803 × 2400 | `5958d5277adba46f4cc984173928b96472e6cd7ce8eebb960d32dffb25d4771e` |
| 169180-16.png | 245097 | 1807 × 2400 | `6fd126293c468c39901247fff7f7f639a352b443b6e912891bec97fd083ffbd2` |
| 169180-17.png | 159173 | 1805 × 2400 | `3391866feed217ecc65ed921dcf7904a0560908c731ea3ae04e0a8abc174d62f` |
| 169180-18.png | 462620 | 1437 × 2400 | `8aec8ad8aa2034a7ef45ce39499f5f76c8130522645c456fe054610cb9951da7` |
| 169180-19.png | 335274 | 1461 × 2400 | `2948a2fafff3f8ecfb71aa41473dd99fabf0529ceff0552b52a1d8eee061bb1b` |
| 169180-20.png | 471079 | 1464 × 2400 | `951a2a0f319f449b4c12fcdf8948d843c9578963a094819481f631b488d1303e` |
| 169180-21.png | 341259 | 1471 × 2400 | `a7d52896a917c9451ec92a81b209d81243afb13e0d75711f56df3a36ed33d15c` |
| 169180-22.png | 485541 | 1474 × 2400 | `59a70883a36af772ecad32075bdf9ba86636852494980ca47b1d770795fb4ec5` |
| 169180-23.png | 348744 | 1459 × 2400 | `65c67031584bc45bd5f7f0a5c4d8b37e87d15fd7450bce4ad35cad2f0289877a` |
| 169180-24.png | 63105 | 1596 × 2400 | `2c60a1a89f15994cf388d19e76eae9cd134dfaec7b31c943228b17d375bb03c0` |
| 169180-25.png | 42897 | 1584 × 2400 | `e54d0264a524473f40a1c2788c0fd8135646e78efd4a14e0053905b8b20b5138` |

The second reproduction's stdout and stderr, and preserved root `render-169180.stderr`, are also zero bytes with the empty-byte hash above. Thus both independently executed render processes reached exit 0 with empty captured diagnostics; no source PDF changed. The check used direct equality of each complete PNG byte string plus PNG-header dimensions, not only a filename or size match. No reader interpretation was inspected to obtain this result.

## Closed new-raster coverage

Root subsequently reported its new-source reading closed at all 29 initial rasters, zero larger repeats (process receipt `c35533`, exit 0). The independent reader subsequently reported the same closed set, zero larger repeats (process receipt `06ae68`, exit 0). These are process-only reader reports, not findings exchanged with this checker. Neither observation record was opened. There is no unverified larger raster in the declared used new-page population.

The saved 29-row table was separately checked against both complete byte sets, including every byte count, dimension and hash; both font configurations and the protocol pin also matched (`b493c3`, exit 0). Both root and independent initial PDF-to-PNG transformations therefore have matching outputs for this fixed new-page population. No additional view/render was performed after receiving the readers' closure reports.

Matching renders establish same-input derivative reproducibility only; they cannot establish source authenticity, historical accuracy, human-readable fine detail, display fidelity, installed conditions or the correctness of either reader's interpretation. Source hashes identify admitted bytes, not proof of the underlying municipal events. The earlier comparison pages 173199 p1/p5 are not newly rerendered by this unit's new-page reproduction check; their separate authorized views do not add new derived pages to this reproduction population. Complete reading, comparison, interpretation and synthesis acceptance remain separate.
