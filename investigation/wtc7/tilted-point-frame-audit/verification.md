# Independent representation verification

Status: `pass_representation_only` for the two prepared runs. This is a source-guided presentation audit under the protocol's conditional H0, not validation of the original tracking, material-point identity, calibration, or collapse mechanism. No historical images were displayed by this verifier. Physical and actual-human acceptance are not established by these checks.

## Scope and independence

The verifier independently reconstructed the saved PM05/PM08 row selection, exact binary-float rounding, crop support, padding, masks, marker geometry, clock joins, and complete panel pixels. It read the producer as a schema reference but never imported or called it to obtain expected values. NumPy integer-coordinate gathering supplies the expected crop pixels; an independent Boolean-coordinate predicate supplies the 40 marker pixels. Controls use a separate slow crop loop and analytically specified coordinates.

The frozen source contract and method review remain unchanged. The complete canonical selection is PM05 frames 150–402 by six (43 rows: 8 keys, 35 nonkeys), PM08 frames 210–444 by six (40 keys), and their 50-frame union. These are saved membership flags, not proof of human marking or interpolation. PM05/PM08 are source track identifiers, not independently confirmed physical-feature identities.

Pillow image decoding and font rendering are shared dependencies. The verifier did not run a third independent full-video decode: it compared all 476 new frame/PTS/hash records to pinned held records, checked the full raw-stream digest **receipt** against the held digest and command, and independently hashed the actual 50 selected native PNG luma arrays. Root's two producer decode runs and this independent array/presentation check are different kinds of evidence; neither validates historical engine behavior.

## Commands and environment

All commands below used working directory `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`. Runtime: bundled Python 3.12.14, Pillow 12.3.0, NumPy 2.3.5. Runtime and source identities are retained in the receipts. This is an intentionally dirty research worktree; no general cleanliness claim is made.

The verifier controls were actually run with each output suffix `01`, `02`, and `03`:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/tilted-point-frame-audit/test_verify.py --out research/sherlock-wtc7-investigation/tilted-point-frame-audit/verify-controls03
```

An initial sandbox attempt for `verify-controls01` failed at directory creation before running tests. The same narrowly scoped command then ran with approved worktree write access. Later generated receipts also used narrowly approved access; the source and test edits used `apply_patch`.

The historical verification command actually run, after root's explicit authorization, was:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/tilted-point-frame-audit/verify.py --runs research/sherlock-wtc7-investigation/tilted-point-frame-audit/run01 research/sherlock-wtc7-investigation/tilted-point-frame-audit/run02 --reviewed-producer-sha256 94eae0ca4eccb80eef453e76e3597f64955039f1ad9a15337de345ed1e1181a5 --out research/sherlock-wtc7-investigation/tilted-point-frame-audit/verification01.json
```

It exited 0. Replays must use a fresh `verification*.json` output name: existing receipts are not overwritten.

## Controls, retained failure, and correction

- `verify-controls01`: 12 tests passed, exit 0; foundational arithmetic, complete source selection/clock joins, pin errors, and pixel-corruption controls.
- `verify-controls02`: 15 tests ran, **one error**, zero assertion failures, exit 1. Its failed receipt and test transcript remain intact.
- `verify-controls03`: 15 tests passed, exit 0, after the narrow checker correction described below. This is the final checker version.

The failed control exposed an overly strict checker assumption about font bearings, not a crop/source geometry error. With the declared Pillow default font at size 12, a label anchored at `(744,72)` beginning with `x` had glyph bounds `(743,75,788,84)` and advance length 44. The protocol requires labels outside protected image regions; it does not require nonnegative left glyph bearings relative to a text anchor. Root reviewed and authorized a checker-only correction before historical verification.

The final checker requires the declared text advance to fit its width and allows at most one pixel of exterior horizontal font bearing. The 16-pixel vertical label band, absolute non-overlap with every native/crop rectangle, and exact full-canvas rendered-pixel comparison remain enforced. No one-pixel allowance was granted to source pixels, crop geometry, padding, masks, or markers. The failed run is not reclassified as passed.

The final 15 tests cover negative and positive half ties; the value immediately below positive one-half; original-coordinate versus rounded-cell boundaries; missing, duplicated, or altered rows and key membership; all 476 irregular/nonzero-clock joins; bool/nonfinite and duplicate-JSON-key rejection; pin, PTS, hash, size, and index corruption; exact saved text/hex/XML locators and rational residuals; all crop/padding/mask pixels; 3× nearest-neighbor replication; exact marker arms and untouched center; missing-track slots; full-panel native/crop/exterior-label corruption; and exclusive receipt preservation. The one-half-neighbor control is important: ordinary floating addition can round up before `floor`, whereas the defined exact rational half-up rule does not.

## Producer synthetic fixture verification

Before historical verification, an inline Python command imported **only this verifier** and invoked `verify_synthetic_fixture_directory` on both `controls03` and `controls04`, with reviewed producer SHA `94eae0ca4eccb80eef453e76e3597f64955039f1ad9a15337de345ed1e1181a5`. It wrote the exclusive receipt `verification-synthetic01.json`; no historical inputs were read or images displayed.

Both sets passed independent reconstruction of their three complete 1128×648 RGB panels, five point pairs of plain/marked crops, and five masks. Each fixture native image was checked against the specified RGB coordinate pattern, not treated as historical luma. All 19 PNG products and the fixture metadata were byte-identical across the repeat sets. The checks included central fractional points, near-edge points, fully off-image support, and a genuinely missing counterpart. The producer's earlier synthetic caption error and old controls01/02 were preserved by the producer/root; only final corrected controls03/04 were accepted here.

## Historical result

For **each** of run01 and run02, the verifier checked:

- all 476 frame indices, exact PTS/time-base joins, and decoded/luma hash records;
- the exact 83 saved coordinate rows and 50 selected native frames;
- all 349 PNG products and their byte/pixel hashes, modes, and dimensions;
- all native pixels, standalone crops, masks, exact marker changes, protected panel regions, full panel background, and 882 exterior labels;
- the complete manifest, execution/probe records, receipts, and inventory;
- exact byte identity of all **357 substantive files** between the two runs.

Only the two explicitly path-bearing files, `input-receipt.json` and `receipt.json`, are excluded from repeat byte identity. They are still individually checked. Per-run sample counts are 17,280,000 native luma samples; 16,135,200 standalone crop RGB channel samples; 298,800 mask samples; 71,280,000 protected panel RGB channel samples; and 109,641,600 complete-panel RGB channel samples. These are overlapping coverage counts and repeated representations, **not independent scientific observations**.

The result means that the generated views faithfully implement the declared presentation rule for the pinned data. It does not make direct saved-image-coordinate placement historically correct merely because it is implemented correctly. Root's separate qualitative review and any actual-human gate remain separate stages.

## Frozen audit identities

| Artifact | SHA-256 |
| --- | --- |
| `verify.py` | `3b2f45f97a9724a826469e88c5313dba7763d04ae14a1ea575c578827c3acf5e` |
| `test_verify.py` | `c9296ebc297cd71308da575e807b9611e73bd1b7c20a9db25b149c8c86da538f` |
| final producer `prepare.py` | `94eae0ca4eccb80eef453e76e3597f64955039f1ad9a15337de345ed1e1181a5` |
| failed `verify-controls02/receipt.json` | `78ced549f0eafe4ce6ba89d761e58b93ef1245699fc123a360a54a67f8ef98f4` |
| final `verify-controls03/receipt.json` | `cfde67bcc67034c3155a9b27d4f8b138e1d8ad836410e6fb095e739896564aa8` |
| `verification-synthetic01.json` | `07c529581c14f3ff891b6a525d3dfd1d9a3c9131d48c795d40e899c5481df57a` |
| `verification01.json` | `431ea2063f2a101d853bd32b651a11001b6429e46b51fa6bc103fb929fe5f9f2` |

Source and runtime pin details are retained in `verification01.json`, rather than duplicated as a second source ledger. No scientific rank, legal inference, original-track acceptance, or causal conclusion follows from this representation pass.
