# Full Clip 7 source/product check

2026-10-04 UTC. Root's read-only computational check, performed after both
extractions and before scoring. **Passed within the scope below.** No image
was displayed, no score loaded and no physical or historical-cause finding made.

Both complete extractions contain exactly indices 0–1127, with identical frame
records. Separate pixel loops verified **2256 new PNG/RGB pairs** plus **nine
pilot PNG/RGB pairs**. All nine earlier selections match by source index,
metadata and hashes, despite their different output-file ordinals. Every one
of the **2357 captured dependencies** retained its hash at the end of the check.

## Method and actual execution

Root ran a stdout-only script with the bundled Python 3.12.14, `-B -`, from this
directory (terminal 98018, initial tool chunk `be53d8`, final `0e3df0`, exit 0).
Assertions were enabled. The script imported the pinned supplementary artifact
checker and used its `extraction` function for saved receipt/command, inventory,
PTS, geometry and diagnostic joins. That function reuses the unchanged configured
sampler only for inventory/diagnostic/showinfo parsing; this is not an entirely
independent decoder implementation. Root separately decoded every admitted PNG
with Pillow, required PNG/RGB/720×480 and computed SHA-256 of `image.tobytes()`.
The byte hash had to match each frame record, and both whole frame lists had to
be equal. No FFmpeg/FFprobe process was launched by the checker.

The direct checks also verified the complete source manifest, held source size
and SHA, plan/manifest copies, fresh controls, supervisor start/end identities,
exact runner argument vectors, predecessor pins, parent supervisor identity,
create-only job outputs, and requested/observed resource limits. Saved source
identity matched before/after both extractions. All received probe/decoder
commands returned zero; diagnostics were clean with exactly 1128 show-frame
and 1128 show-color records per extraction. Probe diagnostic streams were empty.

Every native frame retains 720×480, SAR 8:9, yuv411p probe format, interlaced
bottom-field-first metadata, integer PTS equal to source index and exact time
base 333673/10000000. Encoded PTS is not an authenticated event clock. Pilot
indices are 0,141,282,423,564,705,846,987,1127. Pixel/byte reproduction establishes
consistency with the held source, not original-camera authenticity, exact
exposure, independently calibrated measurement or human/scientific acceptance.

## Saved identities and limits

| Artifact | SHA-256 |
| --- | --- |
| Held Clip 7, 140334936 bytes | `a2aefd37d58a7f2e7cea73c8d06114ec941e2178d1a4ddc9419649dd9936487b` |
| Both new frames.json | `a7793e5d1f4a7faafe102029ebf99aede540021c83f292e5c9232de13622c13c` |
| Earlier pilot frames.json | `15a0d0ae2b7d0f650688abf90bd474f7f1dafdb8f6a595a3ad9e046b980d9e0f` |
| Supplementary checker used | `c7342eb153dcdfed1762d9d312b46a26b1e4d84f7a3eac6849a38eab0b99cfe8` |
| Implementation review | `17b338a58697d0b2249056341cb5b2adaf7e192884df3f02b69adb8dfdbd0f9a` |
| Fresh root controls | `3c656d64ba2d435c86e8db240a2e52b899d94f653d6d75416e6eb9988ce10641` |

| Job | Supervisor seconds | Extraction-directory bytes | Free bytes afterward |
| --- | ---: | ---: | ---: |
| extract01 | 25.260862249997444 | 883725454 | 8175042560 |
| extract02 | 25.099711541901343 | 883725454 | 7285846016 |

Both completed with exit 0 and passed wrapper end checks. Their 240-second,
1280-MiB/64-MiB-reserve limits, inclusive lane limit and free-space floor were
satisfied in the saved records. Sampled monitoring is not a hard quota or an
independent continuous resource trace. All original and earlier failed outputs
remain preserved. No historical retry, deletion, scoring or visual judgment
formed part of this check.
