# Independent technical review of NBC dense sampling

October 9, 2026. Research-only technical review by the delegated
`/root/current_structural_opportunity` agent. The reviewer previously inspected
WP3/WP4 records but did not author this unit's producer or visual annotations.
This is separate implementation checking on shared inputs, not an independent
historical source, actual-human acceptance or expert assessment.

**Result: pass within the declared selection and derivative-identity scope.**
No material producer defect was found. Both saved runs were complete when
compared. The saved independent checker was rerun successfully with exit 0.
No protocol, producer, source, run, visual finding or accepted state was changed
by this review. The only reviewer-created files are this record and
[independent_check.py](independent_check.py).

## Checks actually performed

The reviewer read the complete protocol and producer. The independent checker
does not import the producer or its `select` function. It reconstructs the
small selection as the full index range and the large selection by mapping
each rational absolute timestamp's floor to its first inventory index, then
appending the last frame when needed. It compares the complete ordered index
lists, not just their lengths, against the selected records and actual
extraction-filter expressions.

For every selected frame in both runs, it verifies the saved SHA-256 and byte
size; 320×240 RGB raster; original-PTS preservation; exact rational
best-effort-PTS/timebase/time joins; showinfo output ordinal, PTS, raster and
format; and showinfo RGB Adler32 checksum against the PNG's decompressed pixel
bytes. Each image's pixels also match its unaltered row-major sheet placement.
Labels are outside those checked raster regions.

The checker verifies all recorded product pins and that no unlisted product
file exists in either run directory, excluding the deliberately unlisted
start/receipt records. It freshly verifies protocol, producer, acquisition
manifest, FFmpeg/FFprobe binary and source-file identities against the receipt
pins, as well as all recorded command exit codes. An additional inline check
joins the receipt's source paths and expected hashes/sizes to the acquisition
manifest itself.

| Result, identical for run01 and run02 | Small candidate | Large candidate |
| --- | ---: | ---: |
| Decoded inventory frames | 295 | 10,648 |
| Selected frames | 295 | 357 |
| Selection | Every index 0–294 | First frame in each of 356 occupied one-second bins, plus final index 10,647 |
| First exact encoded time, seconds | 7919/45000 | 7919/45000 |
| Last exact encoded time, seconds | 448919/45000 | 15978419/45000 |
| Largest selected-time gap | 1/30 second | 1 second |
| PNG/hash/raster/showinfo/PTS/sheet comparisons | 295 | 357 |
| Inventory diagnostic lines | 0 | 2 |
| Selected extraction diagnostic lines | 0 | 4 |

Each run's 695 recorded product pins and three controlled-input pins passed.
Across runs, the complete parsed inventories and selected-row objects are
identical; all 652 PNG pairs and all 33 sheet pairs (15 small, 18 large) are
byte-identical. Across both runs, the checker performed 1,304 selected-frame
identity checks.

The producer's seven selection checks also passed. Their fixtures cover
variable cadence, exact bin boundaries, an empty bin, appended final frame,
all-frame selection, a singleton, empty input, duplicate/decreasing timestamps,
and a missing timestamp. Several properties share one fixture; this is seven
checks, not one separately counted test per property.

## Actual commands and execution

Working directory for the commands below:

`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`

The first independent audit was an inline Python heredoc. Its successful body
is preserved in `independent_check.py`, with only a shebang and explanatory
docstring added. The saved-file replay used exactly:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/nbc-dense-screen-2026-10-09/independent_check.py
```

It exited 0 and printed the per-run and cross-run result objects summarized
above. The command was invoked once from the saved file; polling the running
process did not rerun it. The checker writes no files and does not decode
source media anew.

The producer fixture command was:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/nbc-dense-screen-2026-10-09/screen.py --test
```

Exit 0, stdout `7 selection checks passed`.

The runtime readback command was:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -c 'import platform, PIL; print("Python", platform.python_version()); print("Pillow", PIL.__version__)'
```

Exit 0: Python 3.12.14; Pillow 12.3.0.

The separate source-manifest and original-PTS audit executed:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B - <<'PY'
import json
from pathlib import Path
base = Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/nbc-dense-screen-2026-10-09')
rec = json.loads((base/'run01/receipt.json').read_text())
manifest_path = next(Path(p) for p in rec['inputs_before'] if p.endswith('/manifest.json'))
manifest = json.loads(manifest_path.read_text())
assert len(manifest['sources']) == 2
for label, expected_name, source in zip(('small','large'),('sources/collapse wtc.mpg','sources/wtc5.mpeg.mpg'),manifest['sources'],strict=True):
    assert source['path'] == expected_name
    assert rec['sources'][label]['path'] == str(manifest_path.parent/source['path'])
    assert rec['sources'][label]['before'] == {'bytes':source['acquired_size_bytes'],'sha256':source['sha256']}
    frames=json.loads((base/'run01'/(label+'-inventory.stdout')).read_text())['frames']
    print(json.dumps({'candidate':label,'source_manifest_join':'pass','inventory_frames_missing_original_pts':sum('pts' not in f for f in frames),'present_pts_differ_from_best_effort':sum(f['pts'] != f['best_effort_timestamp'] for f in frames if 'pts' in f)}))
PY
```

Exit 0: both manifest joins pass; zero missing original PTS in small and three
in large; every present original PTS equals its best-effort timestamp.
The follow-up locator command was:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B - <<'PY'
import json
from pathlib import Path
base=Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/nbc-dense-screen-2026-10-09/run01')
frames=json.loads((base/'large-inventory.stdout').read_text())['frames']
rows=json.loads((base/'large-selected.json').read_text())
missing=[i for i,f in enumerate(frames) if 'pts' not in f]
print(json.dumps({'large_indices_missing_original_pts':missing,'selected_missing_original_pts':[r['source_index'] for r in rows if r['pts'] is None],'best_effort_fields_present_for_all':all('best_effort_timestamp' in f for f in frames)}))
PY
```

Exit 0: missing original PTS at large indices 1014, 4014, 10014; none selected;
best-effort timestamps exist throughout.

Fresh hash readback used:

```sh
shasum -a 256 research/sherlock-wtc7-investigation/nbc-dense-screen-2026-10-09/independent_check.py research/sherlock-wtc7-investigation/nbc-dense-screen-2026-10-09/PROTOCOL.md research/sherlock-wtc7-investigation/nbc-dense-screen-2026-10-09/screen.py research/sherlock-wtc7-investigation/nbc-dense-screen-2026-10-09/run01/receipt.json research/sherlock-wtc7-investigation/nbc-dense-screen-2026-10-09/run02/receipt.json
```

Exit 0. Pins, including freshly checked source identities:

| Artifact | SHA-256 |
| --- | --- |
| independent_check.py | `03f00ab1b730d2a6c8446fd385dc843d493ef21d9b8799f17e6f61c02210fcfa` |
| PROTOCOL.md | `18c6bd7b8cd0795000a342ae669036235678ea9946d974807fba26ea8834ab77` |
| screen.py | `cd127069cf76b484bc14f2d8f053c28eecac629a2f8c3ff1a95fc2446d010035` |
| Acquisition manifest | `ed1d8a7a1f1d89d6bed9c42325cb70bf194a6bfee8f655cc650709e83ace474a` |
| Small source, 2,703,430 bytes | `9ebd451c32f2a2bfd031cefae87aba5f74e238e31abd2b66f5cf39c5dc62ff54` |
| Large source, 99,297,340 bytes | `1bc402b59122eb8ecd1cdd7b473c4fa6b492e98c85cf42afa26f71134ed4d4de` |
| run01/receipt.json | `192bcf06269476189ee69181b53c0cf26522b45c3a7d1d669036826a9e7fa9c1` |
| run02/receipt.json | `6ef872802fffef7bb63f32993008a387a60bd3fdda0a794fb21f1e508680cf98` |
| FFmpeg executable | `7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569` |
| FFprobe executable | `fd670257233c93c88608a62ed8b5ddeeb812bd341dfb39bbe0e1c654b91672ad` |

## Retained auditor failures

The initial `python3 -B -c 'import PIL; print(PIL.__version__)'` command exited 1
with `ModuleNotFoundError: No module named 'PIL'`. The bundled runtime was then
located and used; no dependency was installed and no producer file changed.

The first inline independent checker exited 1 because its own timebase regex
captured the trailing comma in `1/90000,`, which `Fraction` rejected. The
auditor narrowed that capture to the integer/rational field and replayed the
complete audit successfully. This was an auditor parser defect, not a producer
or media finding. The saved checker preserves the successful corrected body.
The tool transcript retains the failed inline invocation; no failure receipt
was written into the producer's run directories.

The preliminary listing of the two proposed review-file paths exited 1 because
they did not yet exist. This confirmed creation targets, not an analysis failure.

## Diagnostic and inference limits

Large-file inventory stderr reports damaged texture and unavailable motion
vectors. Extraction retains those plus concealed-error and corrupt-decoded-frame
warnings near the tail. The receipt's diagnostic list is a filtered summary;
the complete saved stderr remains controlling. Exit zero and repeatable decoded
pixels do not certify clean media or restore missing source information. Log
proximity alone does not conclusively assign corruption to a selected frame.

A successful comparison checks saved decoder output and raster consistency,
not independent decoding by a different implementation or historical fidelity.
Both runs use the same producer and decoder stack. Encoded best-effort times
are not authenticated event clocks. Square-pixel contact sheets preserve the
selected raster bytes but do not establish scene geometry.

Small-file coverage is all successfully inventoried decoded frames, not an
unavailable original. Large-file coverage is the fixed selected sample, with a
one-second maximum gap; a brief intervening shot, alternate framing, corruption
or unrecognizable view could escape it. This review supplies no new visual
match/nonmatch, audio listening, soundtrack authentication, collapse measurement,
cause ranking, expert conclusion or actual-human acceptance.
