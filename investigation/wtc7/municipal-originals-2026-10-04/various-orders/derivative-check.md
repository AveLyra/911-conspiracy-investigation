# Independent various-orders derivative check

October 4, 2026. Complete: four page rasters reproduce exactly, and all nine
preserved files match the completed root scratch copies. Two independent
renderer processes exited 0; neither was restarted. No larger repeat was used.
This is local same-renderer derivation verification, not source authentication,
historical corroboration, visual readability or engineering validity.

## Scope and inputs

Read this unit's complete protocol, its incorporated change-order protocol,
the acquisition source log and the PDF skill before rendering. Main
AGENTS/WORKFLOW/CHARTER hashes match the previously read controls. Applied
evidence/source-preservation boundaries: no source/image content views,
root/peer interpretation reads, OCR, crops, rotation, network, source/frozen
file edits, Git or engine actions. Only this new note and private scratch
outputs were written.

Protocol SHA-256:
`516e9f3ba2e060434a48cd2ea0375791e5d701dcc56aade4faf70d79bbf49c76`.

Command path abbreviations:

```sh
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/various-orders
T=/private/tmp/various-orders-derivative.iEERTE
R=/private/tmp/wtc7-various-orders.SPzf16
P=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm
I=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo
```

`shasum -a 256` and `wc -c` verified both declared unit sources before
rendering (`f39f38`, exit 0); both hashes were unchanged afterward (`a9922f`,
exit 0). Total source bytes: 217425. Each `$I <source>` call exited 0 with
empty stderr and reported two pages, no encryption and PDF 1.5 (`0ad95a`).
Only these metadata fields and file size were printed, not page content.

| Source filename | Pages | Bytes | SHA-256, before/after |
|---|---:|---:|---|
| NYC-WTC_000167170.pdf | 2 | 104270 | `3a2fce21c438e04d976eae93b8e1225d388c008aa28d72aad58af3e433b4033c` |
| NYC-WTC_000171802.pdf | 2 | 113155 | `7ab6722000bac41812f2fc796846d04212f6cbabad5c96d1d3109c85d5ffeee2` |

## Renderer and independent executions

`mktemp -d /private/tmp/various-orders-derivative.XXXXXX` created `T`
(`6227d5`, exit 0). Created its own `fonts.conf` with `apply_patch` and
explicitly created `T/font-cache` with `mkdir` (`296bff`, exit 0).
Config uses `/System/Library/Fonts`, `/Library/Fonts`, `fonts.dtd` and only
that private cache. Checker config SHA-256:
`ef577a356d63ebb89ae3ed7cf36c9adbc833e58bfd885b1a35a91c5b042d1141`.
Root config SHA-256:
`428d6782ccf4944b2004e4fc124faa6e62875b8197d81a61fc3fb14277ab2ce9`.
`diff -u "$R/fonts.conf" "$T/fonts.conf"` returned expected exit 1
(`00614e`): only cache path differs. `$P -v` reported Poppler 26.05.0.

Executed exactly once per PDF, concurrently in separate subprocesses:

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 2 -png -scale-to 2400 "$U/NYC-WTC_000167170.pdf" "$T/167170" >"$T/167170.stdout" 2>"$T/167170.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 2 -png -scale-to 2400 "$U/NYC-WTC_000171802.pdf" "$T/171802" >"$T/171802.stdout" 2>"$T/171802.stderr"
```

Each Python subprocess wrapper saved the expanded command, UTC start/end,
monotonic elapsed time, actual renderer return code and wrapper streams in
`T/<ID>-receipt.json`, then propagated that return code. The original live
handles were polled to terminal; neither command was restarted.

| ID | Start UTC | End UTC | Seconds | Handle / terminal receipt | Renderer exit |
|---|---|---|---:|---|---:|
| 167170 | 23:06:18.164208 | 23:06:28.312241 | 10.145416 | 4755 / a75e8a | 0 |
| 171802 | 23:06:18.164160 | 23:06:29.946592 | 11.782130 | 42049 / 90fbd6 | 0 |

Both wrapper streams were empty. All four saved renderer stdout/stderr files
are zero bytes with SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
No warning was emitted. Saved receipt SHA-256 values:

- `167170-receipt.json`: `f1ca6975731f7600058b93a366ed6e3196f97bb055806cf5a267d82022abfbec`.
- `171802-receipt.json`: `70d60e6d65f67d476edaa06d4f63674eeae8171a5e36e0f6434ecfd3d46b3e0a`.

## Four initial comparisons

Root reported two completed PDF render processes (`d81def`, `e6f87a`, exit 0)
and four ready page rasters before comparison. Those root process statuses
are attributed, distinct from the independent executions above. Both checker
processes were terminal before comparison.

Actual commands (`a9922f`, exit 0): explicit `cmp -s "$T/$name" "$R/$name"`
for each basename below; `shasum -a 256` and `file` on both copies; `wc -c`
on fresh images and diagnostics. `find "$T" -maxdepth 1 -type f -name
'*.png' | wc -l` counted exactly four. Each comparison returned 0; both
headers match, and exact bytes also establish equal size. All are 8-bit RGB,
non-interlaced.

| PNG basename | Dimensions, both copies | Bytes per copy | SHA-256, fresh and root |
|---|---:|---:|---|
| 167170-1.png | 1794 x 2400 | 157291 | `c4b014f88383852135a4623538a5a521c921e6353dfc265ca82a2a56ebf2a47b` |
| 167170-2.png | 1794 x 2400 | 166313 | `4b03099d470fe7d5abdc30fb0cdc6ca06974e07a8ebb8910e84dec6e5eda3818` |
| 171802-1.png | 1780 x 2400 | 160518 | `d3d4edaecb03c2a04cecad136fda0bea46cb818120bb29748be0dea1c91dfce5` |
| 171802-2.png | 1785 x 2400 | 167680 | `072acbf88c30cecaf3d2cfa5b845604aaebd7cf73d70cbaa839e837fcafff6a4` |

Total fresh PNG bytes: 651802. No missing initial page, source-pin change,
renderer failure or byte/dimension mismatch occurred. Scratch images,
diagnostics and individual receipts remain retained; temporary storage is
not a durability guarantee.

## Preserved copies and final coverage

After the temporary pause, complete note readback (`60e6f5`, exit 0) and
bounded scratch inventory (`347165`, exit 0) confirmed the existing checkpoint.
No renderer was restarted. Subsequent receipt/config hashes and empty-stream
checks (`82e376`, exit 0) match the pins above; both saved process receipts
were read back (`82e376`, `3bba35`) and retain actual renderer exit 0.

Root then confirmed both readers finished: four initial views each, zero
larger repeats. This closure is attributed to root's message, not an
independent content review. Root supplied frozen observation pins
`ff086381acabc8273d599389abe35d49646dd3e2a60e0a594b13d87a158d1184`
and `92146980463019ac4b507ebb36a219215b7906f5e6d381f544c5f827170f81c6`;
those notes were not opened or independently hashed by this checker.

At `2026-10-04T23:18:59Z`, independent preservation check `3bba35` exited 0.
For the exact nine basenames below, ran `cmp -s "$U/$artifact"
"$R/$artifact"`, recorded each return code and ran `shasum -a 256` on both
copies:

```text
NYC-WTC_000167170.pdf
NYC-WTC_000171802.pdf
fonts.conf
167170-1.png
167170-2.png
171802-1.png
171802-2.png
167170.stderr
171802.stderr
```

Result: nine pairs, all comparison exits 0, zero failures. Source, root
font-config and PNG pins match those above. `wc -c` confirmed both preserved
stderr files remain empty; their SHA-256 is the empty-file pin above.
`file` confirmed all four preserved PNG dimensions/headers match the table.
The unit protocol hash also remained unchanged. This verifies post-copy
equality, not the historical copying method or absence of any earlier
overwrite. Root's separate equality receipt was not substituted for this check.

Final coverage is four whole-page rasters from two PDFs and two successful
independent renderer executions, with no omitted requested repeat. No render,
source-pin, byte, header-dimension or preservation failure occurred. The
expected font-cache-path `diff` exit 1 is disclosed above, not a failed render.

## Limits

Shared Poppler and fonts can reproduce the same defect. No visual correctness,
legibility, display geometry, source authenticity, historical completeness,
engineering adequacy, construction, inspection or human acceptance was tested.
The checked hashes do not convert this derivation test into historical evidence.
