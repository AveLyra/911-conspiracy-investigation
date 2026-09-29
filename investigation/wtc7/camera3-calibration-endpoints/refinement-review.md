# Independent endpoint-refinement review and first-pass comparison

September 12, 2026. Separate computational AI review under the existing protocol/charter, not a clean holdout, human review, new historical measurement or acceleration fit. Only this new review is authored. The initial [independent observations](independent-observations.md) remain unchanged.

## Result

All twelve enlarged endpoint images were inspected before reading [root-observations.md](root-observations.md). The enlargement supports a more specific **image-phase** description of the upper query: it lies near the transition from a pale stripe into the darker stripe below, visually near the darker stripe's upper edge. It does not establish that this transition is a window top, floor slab or any numbered architectural level.

At the lower query, all three marked enlargements place the saved-coordinate query at the narrow transition between the gray banded facade to the left and the bright foreground structure to the right. That is an **occlusion-boundary association**, not a clean, independently identified background-building window/floor mark. The precise subpixel side should not be overclaimed. The evidence still does not identify two corresponding material endpoints or validate the assigned metric scale.

Approximately fifteen visible stripe cycles remains a useful **conditional dimensional lead**, not an established count between two identified endpoints. The new crops are too short vertically to recount the full span. My earlier rough 14-16 interval envelope remains separately attributed; root's first-pass note explicitly withheld a reliable corresponding-window count. This is not a two-reviewer confirmation of fifteen intervals.

## Display contract and interpretation

Read `refine.py` in full as data; did not execute it. Its two half-open source rectangles are upper `[398,184,432,210)` and lower `[400,377,434,405)`, enlarged 12x nearest-neighbor. The unmarked products are 408 x 312 and 408 x 336 respectively. Enlargement repeats source pixels and supplies no new optical resolution. The marked RGB products are separate analytical displays; the red cross represents the **saved-coordinate query**, not a manually localized historical feature or evidence of a mark actually present in the video.

The recipe's integer-source-index-as-pixel-centre convention maps a source coordinate to `u=12(x-x0+0.5)-0.5`, likewise for y. The recorded upper query is displayed at approximately `(202.0248,152.3842)` and the lower at `(208.9840,170.2321)`. A pixel-corner convention would shift the displayed cross by less than one native pixel. Blur, coarse native samples and mixed foreground/background boundary pixels also limit side/phase classification. Neither the cross placement nor its many displayed decimal digits resolve that uncertainty.

## Complete twelve-image observations

For each row below, viewed the complete unmarked patch and then its corresponding complete query-overlay patch. No other new image was viewed in this pass.

| Index / region | Unmarked and overlaid appearance | Permissible refinement |
|---|---|---|
| 138 / upper | Alternating gray horizontal/slanted bands. The cross centre is near the pale-to-darker transition, rather than a discrete corner. | A darker stripe's upper-edge neighborhood is a better image description than an unspecified band interior. The exact architectural phase remains ambiguous. |
| 138 / lower | Target banding at left, bright near-vertical foreground edge at right. The cross is on the narrow transition neighborhood. | Supports the original foreground-overlap concern; does not reveal a clean background window marker at the query. |
| 141 / upper | Similar stripe transition at the query, with local intensity/blur differences. | Same qualified image-phase association; no independent floor label or subpixel landmark emerges. |
| 141 / lower | Cross remains at the facade/bright-foreground transition; source blocks straddle a blurred boundary. | No defensible exact-side assignment or corresponding-material endpoint. |
| 168 / upper | The query remains near the upper boundary of a darker band beneath a pale stripe. | Architectural top/bottom/slab meaning remains unresolved despite the clearer display location. |
| 168 / lower | Bright foreground overlap and gray banding to the left remain visible at the query neighborhood. | Same occlusion limit, not proof that a particular hidden row continues to the saved coordinate. |

The original subjective native-coordinate envelopes are not narrowed or rewritten. The refinement adds a query-relative visual interpretation, not new measured feature centres, tracked motion or a numerical stationarity test.

## Comparison after independent refinement viewing

The frozen root note was read in full only after all twelve images. It describes the upper query as an unresolved repeated-window/band location below the dark upper rectangle, not a parapet, and the lower as at/near the bright foreground structure's left edge, with the background facade visible immediately to the left. These agree with the material scope of my frozen first pass and the refinement. Root's context envelopes are broader: upper `x=410..420,y=191..202` and lower `x=412..422,y=384..398`; my initial `x=410..420,y=193..201` and `x=414..420,y=387..396` are contained within them. These are subjective context envelopes, not independent statistical error distributions, and containment does not authenticate a material point.

The refinement slightly sharpens my upper image-phase description from a pale stripe/adjoining darker boundary to the upper-edge neighborhood of the darker stripe. This is an additive interpretation from the explicitly post-first-view display, not a correction silently inserted into the initial record. Root's initial phase uncertainty is not a contradictory refined finding; that note preceded these displays.

The meaningful non-consensus concerns counting. I retained a tentative 14-16-cycle span with approximately 15 plausible in the prior wider views. Root stated that it had not made a reliable corresponding-window interval count between the exact endpoints. Neither description establishes an exact endpoint-to-endpoint count, and the present small patches do not supply one. Root's withholding should not be converted into agreement with my numerical envelope; conversely, it does not refute the existence of visible facade repetition.

## Conditional value and remaining discriminator

A roughly fifteen-cycle facade span is compatible with the independently checked assigned length of fifteen regular 12.75-ft floor intervals. That makes row correspondence worth testing. It does not prove one cycle equals one story, pick one of the seven matching numbered floor pairs, settle stripe phase, or identify the hidden lower endpoint. Corresponding window offsets could cancel, but unlike phases, partial occlusion and an off-by-one interpretation remain alternatives.

A fixed-strip periodicity diagnostic, if separately declared, could test local image repetition. It would not by itself identify floor numbers, material window/slab phase, the lower query's occluded feature, a historical metre, or gravity. I have not read, tuned, waited for or used any such output in this review. A useful direct discriminator remains a clearer source-linked calibration image/architectural annotation that names both feature phases and handles the foreground overlap; no gravity-based choice of endpoints is justified.

## Pins, viewing identity and limits

All paths below are relative to `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-calibration-endpoints/`.

| Input | SHA-256 |
|---|---|
| Frozen `independent-observations.md` | `f27e4352733c61ce838f836cdc05cbdd6e3a6b7b1dff806ac0a3e2ff3268c6a3` |
| Root first-pass `root-observations.md`, read after twelve-image inspection | `4a87459c047d179854fae44e52d125056422f0058c50384fb309b24678a1835f` |
| `refine.py`, read as data only | `8bf67d74d89dc3ef89f3a23f622a1aba2104e9d1f7883a0d49cb6b7079734cd8` |
| `refinement01/receipt.json` | `104c342609d05b3067c65463841429f368771ce416950ef0c0bac58c760d037d` |
| `run01/receipt.json` | `8ae034a788f93a8c8c80704c4fe4b675105065be2a28567e9c4c21cf47a83219` |

Every row below denotes two actually viewed products under `refinement01/`: `<region>-<index>-unmarked.png` and `<region>-<index>-query-overlay.png`.

| Region-index | Unmarked SHA-256 | Query-overlay SHA-256 |
|---|---|---|
| upper-0138 | `4abd68ccb10fe02f7da9a76f5c76529314bfd1d89be0d51a7e2ce9fadfe30a91` | `65960915cc7437e1cc95f865053bfb091ec2af758a5ec08e498d2bd8889e4160` |
| lower-0138 | `552a65c8988c815048d9e5fdaee28ab78aae997b8b347d90097c8e836e31e79b` | `e99362681b298690a08cf7551779c7596360a90c00096e111feb5f5d47bc4beb` |
| upper-0141 | `f84dc00bbb971b9803aebd4c3cb682bca9dd99ea4098184a10d83093eaef2680` | `a40d05a6d88cb88b1a14b8bf4c9f9b26e38a970ac2bef87f669578b032fba48a` |
| lower-0141 | `fed2db71b3154db498e572a3a10718a4e2e9655f1bdbfd23093161da05a59535` | `12b5b0f8d2f79269ac3c99ca4e360cb1455698cf175514e69a14a641a81e16ff` |
| upper-0168 | `e4bec8c9bb780e0fc89335c26011e5a7015ccef06762e107a2e1098a9cad6099` | `33b9a82d4e3e253e0051ebd64692872f4bb264f2ecd4a0c16835c294b40cee10` |
| lower-0168 | `7f701c02b7667b8d01ceccb8c8330d770f3826bb4daff9d0c93af7351bc50618` | `ab36e1842f208f5fb42507283d4afd2388ef1f9354a8f7f74bc8ecb44a4e5a20` |

Using bundled Python 3.12.14, I independently checked all twelve product hashes, dimensions and L/RGB modes against the receipt/recipe, and checked the three pinned dependencies (`refine.py`, root declaration, prior receipt). All passed. The receipt reports Pillow 12.0.0 for generation but no Python version; this review does not invent one. The initial note already preserves source, native pixel, encoded PTS and first-crop identities. No media was decoded or rehashed, raw private fields accessed, diagnostic/physical fit rerun, source retrieved, or original annotation changed here.

The evidence/source rules keep displayed query placement, visually inferred phase, physical endpoint identity and metric validation separate. This finite post-output visual/comparison review is complete and does not change a causal ranking.
