# Observer Stage C scope and display ledger

September 20, 2026 UTC. This new sensitivity pass follows the completely read
`STAGE-C.md`, main repository controls, full research charter, and evidence/
source-preservation skills. It does not replace any Stage A/B freeze. The
observer knows both Stage B records and the exchange review, including the
published-context exposure already disclosed there. No root Stage C record or
new root observation will be read before both Stage C freezes are confirmed.

Before any Stage C image display, declare viewing only these existing complete
`stage-c-run01/fNNNNNN-4x.png` files, in ascending source-index order:

```text
6593, 6689, 6701, 6707, 6714, 6717, 6724, 6736, 6784, 6881, 6904,
6920–6978 inclusive, 7013
```

This is exactly 71 distinct images. Each is the fixed source rectangle
[300,465) × [125,245), enlarged 4× by integer nearest-neighbor replication.
Only these verified, already existing 660×480 displays may be opened. No
native-crop display, alternate crop, contrast alteration, overlay, interpolation,
source acquisition, fresh extraction or scope expansion is authorized. Repeats
of this same fixed set are permitted and will be counted separately.

The parent reported admission after producer/pixel controls and independent
product/source/snapshot checks. This observer did not execute those Stage C
checks and will not describe them as personal verification. Viewing admission
does not establish feature identity or the specified crossing.

## Actual display log

At creation no Stage C image had been displayed. The completed first pass,
in actual successful-display order, was:

```text
6593, 6689, 6701, 6707, 6714, 6717,
6724, 6736, 6784, 6881, 6904,
6920, 6921, 6922, 6923, 6924, 6925, 6926, 6927, 6928, 6929,
6930, 6931, 6932, 6933, 6934, 6935, 6936, 6937, 6938, 6939,
6940, 6941, 6942, 6943, 6944, 6945, 6946, 6947, 6948, 6949,
6950, 6951, 6952, 6953, 6954, 6955, 6956, 6957, 6958, 6959,
6960, 6961, 6962, 6963, 6964, 6965, 6966, 6967, 6968, 6969,
6970, 6971, 6972, 6973, 6974, 6975, 6976, 6977, 6978,
7013
```

After completing that first pass, four permitted repeats were displayed in
this order: **6958, 6964, 6970, 6978**. Thus actual successful coverage is
71 distinct complete enlarged images, 75 display instances. No other image
was opened in this pass.

One earlier request for ten images (6724, 6736, 6784, 6881, 6904, 6920,
6921, 6922, 6923, 6924) returned a wholly truncated tool output stating
that it exceeded available model context. No images from that response were
available to the observer. Those ten were not counted as viewed and were
subsequently successfully displayed in smaller ascending batches, as recorded
above. This is one failed/truncated batch, ten unsuccessful image-display
requests, not ten additional successful observations. There were 85 image-path
requests in all, including those ten and the four actual repeats.

The observer re-read the complete protocol after conversation compaction and
continued the recorded pass; the first six successful displays were retained
in the explicit handoff, not silently claimed as a second viewing. Root sent
only its procedural freeze notice during the pass. Neither root Stage C file
nor new root findings were read before this observer's freeze.

Only this scope note and `observer-stage-c.md` were written. No source,
earlier freeze, code, transform, product, legal or engine file was changed.

## Nonvisual arithmetic checks

A read-only Python3.13.7/Fraction calculation against the existing
`run01/camera2/selection.json` checked indices 6714, 6717, 6958, 6978 and
7013. The first attempt used the nonexistent `stage-b-run01` directory and
failed with FileNotFoundError (exit1). The second used the correct path but
compared integer indices with stored strings, returned no selected rows and
therefore provided no verification despite exit0. The corrected third attempt
converted the stored index strings to integers, asserted exactly the five
requested indices, printed their PTS/exact times and computed the two rational
differences; it passed, exit0. These mistakes did not modify any file or image.
The intermediate `rg --files` path locator returned truncated filenames;
only the explicit existing `run01/camera2/selection.json` was then read.

Stage C production, pixel-oracle, pairwise and freeze checks remain attributed
to the parent; this observer did not independently rerun them.
