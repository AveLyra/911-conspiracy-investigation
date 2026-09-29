# Six-frame source and representation receipt

2026-09-24. Research preparation only. Separate checker: `/root/curve_source`.
This check found **no mismatch** in the six declared source-index joins,
existing PNG bytes/header dimensions, selected maps, whole-source PTS
inventories, or the receipt product entries checked. It did not display or
decode an image, assign a feature coordinate, read old numerical observations,
or test the earlier R1 detection.

## Scope and controlling material

The main AGENTS.md, WORKFLOW.md, START-HERE.md and investigation CHARTER were
read in this ongoing session and their unchanged hashes rechecked. The older
`comparator-roof-onset/FEATURES.md`, `PROTOCOL.md` and
`independent-verification.md` were read completely for method and provenance
context. The last file was read in complete sequential ranges after an initial
combined output was truncated. This unit's newly saved PROTOCOL.md, including
its before-view correction and actual-human mapping gate, was also read.

This is a prospective metadata prerequisite, not clearance of that human gate
or of a numerical comparison. The checker knows the old feature definitions
and source selection; this is not historical-source independence or a blinded
replication. The old numerical observation tables were not opened for this
task.

All relative paths below are under
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/comparator-roof-onset/`
unless explicitly stated otherwise. All input files remained read-only. This
note is the only file created by the checker for this task.

## Actual check

Executed a read-only `python3 -B - <<'PY'` command from the investigation
worktree, using Python **3.14.0** and only `pathlib`, `hashlib`, `json`,
`fractions`, `struct` and `platform`. The inline program asserted exact pins,
indexed parsed metadata, read PNG headers, and reread all checked inputs. It
did not invoke Pillow, FFmpeg, a media decoder, subprocess, or a network tool.
No new script or derivative was generated.

The command returned
`PASS_metadata_bytes_headers_and_exact_clock_joins_only`, exit 0. Specifically:

- Rehashed the actual original access-copy video bytes and reconciled both
  receipts' source path, `source_before`, and `source_after` identities.
- Rehashed both selected maps; verified byte equality, 242 rows, and the exact
  source-index sequence 239 through 480 inclusive. Each of the six selected
  indices occurred exactly once; the corresponding row dictionaries matched.
- Rehashed both whole-source inventories and the held upstream inventory;
  all three were byte-identical, with 1,350 rows. Every `pts` was an integer,
  equaled `best_effort_timestamp`, and the sequence was strictly increasing.
- For each selected row, joined `source_index` to the zero-based whole-source
  inventory row, checked its PTS and time base, and used `fractions.Fraction`
  to check `source_seconds_exact == source_pts * source_time_base`.
- Read all twelve selected PNG files; checked actual byte size and SHA-256
  against their own map and receipt product entries and checked corresponding
  run02/run03 PNG bytes for equality.
- Checked each PNG signature, IHDR length/type and the complete IHDR tuple.
  Every tuple was `(1280, 720, 8, 2, 0, 0, 0)`: header-declared 1280×720,
  8-bit truecolor RGB, standard PNG compression/filter method, noninterlaced.
  This was a header check, not decompression or a fresh source-to-pixel check.
- Rehashed each selected-map and whole-PTS-inventory product against its own
  receipt. Each receipt reported `complete` and 242 historical frames. The
  present product-membership check covered **six PNGs plus two metadata
  products per run**, not every receipt product or every selected PNG.
- Reread all **20** checked video, map, receipt, inventory and PNG files at the
  end; their bytes were unchanged during the check.

## Video and metadata pins

Actual video:
`/Users/admin/docs/911/research/wtc7-video-comparison/media/comparators/explosive/Capital One Tower Implosion [rW_xXcS4y3A].f136.mp4`

- Bytes: **4,901,052**.
- SHA-256: `8560cd686a18c8fcc16fe802691e0f17f117c713b4cd1862017af24d391ce5a2`.

| File | Bytes | SHA-256 |
|---|---:|---|
| run02/comparator-selected.json | 98,723 | `14c72246559d79812c1eef4b42d977c64d1f28bc97d0f034a945cddb8db5561a` |
| run03/comparator-selected.json | 98,723 | `14c72246559d79812c1eef4b42d977c64d1f28bc97d0f034a945cddb8db5561a` |
| run02/comparator-all-frame-pts.json | 193,227 | `d8496f26d271eda8955e0fc46b3ff98754c2b5bc06793e8729adf0840a387c3b` |
| run03/comparator-all-frame-pts.json | 193,227 | `d8496f26d271eda8955e0fc46b3ff98754c2b5bc06793e8729adf0840a387c3b` |
| run02/receipt.json | 70,641 | `e17b37b98c136ba81c79c70ccd03f4b709b127507fd5c6111c5b217b2a14856c` |
| run03/receipt.json | 70,641 | `e7f2303079ad3810ccab88d403eb548a71b05db9bdb5f4e595e043bfdfcd4f28` |

The third, held upstream PTS inventory is
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/av-correspondence/run01/comparator-all-frame-pts.json`.
It has the same 193,227-byte size and `d8496f26…a387c3b` full hash shown above.

## Exact six-frame crosswalk

Each basename below exists under **both** `run02/comparator/` and
`run03/comparator/`. Every paired file has the size/hash shown. The source
index is a **zero-based whole-video inventory row**; the PNG number is a
separate **one-based output ordinal**, not the source index. The time base is
exactly **1/30000**. Decimal seconds are rounded displays of the exact rational
encoded PTS coordinate, not a verified camera exposure clock.

| Source index | PNG basename | Source PTS | Exact seconds | Display seconds | Bytes | SHA-256 |
|---|---|---:|---|---:|---:|---|
| 239 | frame-0001.png | 239239 | 239239/30000 | 7.974633333333 | 881140 | `9f8d2878a69952da6d4a1e31f3a58415c9271c19e95160b28674692f5fb0439f` |
| 434 | frame-0196.png | 434434 | 217217/15000 | 14.481133333333 | 922606 | `cbd2078df347521154157ae7c3b637585d3196cd3b1d1398ccc19be00cacacc5` |
| 441 | frame-0203.png | 441441 | 147147/10000 | 14.714700000000 | 927384 | `13c3d28ee22e129de4de3030cb2d9543079518b766f01487bf43694cdbf0f95f` |
| 442 | frame-0204.png | 442442 | 221221/15000 | 14.748066666667 | 928276 | `62f63c6b6f912cc4d5f859175dbd7b8da987dc6a440bd0f17366b803c02bea68` |
| 443 | frame-0205.png | 443443 | 443443/30000 | 14.781433333333 | 927885 | `d64ec51cf17c6df8254446b642cef0542612e509245539b010c1bc8d473f80b3` |
| 444 | frame-0206.png | 444444 | 37037/2500 | 14.814800000000 | 927123 | `4679ce4d4e6634ac5721e36abc328ff11e75fa8eb57e468f6d390cf8c2200491` |

Each PNG had a matching product entry in **each respective run's receipt**;
none of the six was inferred from a directory listing alone. Frames 441–444
are consecutive source indices; 239 and 434 do not make the full selected
list consecutive. Map `interval` fields are extraction sentinels, not physical
event times, onset brackets, or timing uncertainty.

## Interpretation ceiling and exclusions

This establishes scoped **integrity and metadata correspondence**, not
authenticity. The video is a preserved, project-attributed platform video-only
access copy, not an authenticated native camera original. Byte equality can
preserve a shared extraction error or upstream alteration. Receipt agreement
is not independent evidence of the filmed event or the intended feature.

The existing independent-verification record reports broader decoder/RGB
reproduction work, using the same FFmpeg family; that historical work was
read, **not rerun here**. Its prior colorspace notices and declared network
deviation are not erased by this narrow pass. This check did not revalidate
the decoder, all extraction diagnostics, every receipt product, all 242 PNGs,
the visual contents, display geometry, or the source-to-pixel correspondence.
The PNG header check alone also does not establish a single-frame/no-APNG
contract: ancillary chunks were not separately inventoried.

No old or new position envelopes, numerical detections, event ordering,
physical first motion, reference stationarity, demolition mechanics, WTC7
cause, or causal ranking was assessed. No human mapping check occurred. The
actual-human prerequisite and the protocol's other gates remain outstanding;
this receipt cannot substitute for them or retroactively complete the older
study.
