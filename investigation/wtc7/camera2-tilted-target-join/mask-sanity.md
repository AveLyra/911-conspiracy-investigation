# Fixed exclusion sanity check

2026-09-24. Root, prior-informed AI; not human annotation acceptance.
Before any new historical score or alternate-frame view, read the frozen
protocol SHA-256
`e9345fd05579cfcc7f45b1fa850271eeea8f3f7abe23a80dfb70bc6063364503`.
The three right-side masks were fixed before these two views.

Checked actual source PNG byte hashes against the exact matching rows of
`../tilted-camera-source-join/candidates01/selection.json`, itself pinned to
`360d4646eb9318da7dd741f3c6be4d57c6c7c6879313514c98826257c7f89552`.
The read-only check required exactly one row for each index and exited0.

Then displayed the complete native640×480 image at original detail, once each,
in this order:

| Source index | PNG SHA-256 | Coarse mask observation |
|---|---|---|
| 6925 | `cdd265e54fceb34833cc73de718780e2b371f34f7a52204a5fa3f3221e4bf9ce` | The described small point at the upright tip above the left foreground roof lies in the far-left part of the image, comfortably left of the fixed midpoint. |
| 6970 | `8ad5db0624224ba32a9508ccc85848ddb3c1e1f9c589284655442f026a08b156` | The supplied point description is again at the far-left upright, comfortably left of the fixed midpoint. |

Both full images displayed successfully; no retry, crop, enhancement, overlay,
new coordinate/intensity measurement or alternative historical image was used.
This supports excluding the described appearances from the declared right-half
sample. It is not identification of an emitter, pixel-precise localization,
proof of physical attachment or independence of all processing effects. The
resampling-footprint perturbation controls remain a separate software check.
No mask was moved after viewing. No Tilted counterpart was viewed or selected.
