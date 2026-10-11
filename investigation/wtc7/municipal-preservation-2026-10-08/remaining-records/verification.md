# Technical integrity verification only

October 8, 2026 local time. Separate check by `energy_admission_review`.
**PASS within the technical scope below. Content review remains stopped/pending
authorization.** No document text, OCR, other readers' interpretations or new
image display was used in this verification task. This is not the intended
two-reading content review, a legal conclusion or human/expert acceptance.

The checker earlier viewed some group-B pages in its source-reading assignment
before the sensitivity stop. This technical check does not erase that history,
extend that reading or report marked content. It verifies file identity,
population, page/image structure and three fixed rendering repeats only.

## Inputs and current-file reconciliation

Root directory R:

```text
/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-preservation-2026-10-08/remaining-records
```

The frozen controls matched:

| Input | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL.md` | 4810 | `935f642f7473efad228e625fc641248ebc2e750592bf08669cfb10679e9eec73` |
| `roster.json` | 1486 | `8d2f17061c013e9cb4980b14fa95cb63d7d96524424ab19aa24d3b72d02094f2` |
| `../response.json` | 26269 | `328a3a58d22d98c4cbc56ff8683ce618bfd76cbeebb33be8fccbfc3e23432542` |

The parent response contains 16 unique returned IDs. Exactly the roster's 14
remain after excluding 153903 and 153904; no new content-dependent exclusion
was made. Each selected ID's numeric `pdf_size`, `page_count` and
`production_end` matched the roster. No response title, correspondence text or
private contact field was used. This tests the returned population, not the
completeness of City holdings.

All 14 expected source paths exist, with no extra `sources/*.pdf` path.
They total 2,998,001 bytes and 70 pages. Every source has a PDF signature;
`pdfinfo` exited 0 with zero stderr bytes, and its page count matched the
roster. A separate pypdf page-tree count also matched. The current source
hashes below additionally match all 14 acquisition-time hashes in the technical
table of [execution.md](execution.md#actual-acquisition), derived there from
root's acquisition/admission receipts. This checker did not repeat HTTP
requests or independently witness those original transactions.

The execution record compared at this check was 6,354 bytes, SHA-256
`8b31ed628315e837c367ef65b4b7aec6f5a2f618803155fa89667169c489209d`.
Its technical acquisition table was parsed by exact row structure, with
14 required entries; that file was unchanged during the comparison.

| Source under `sources/<ID>.pdf` | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| NYC-WTC_000153905 | 4 | 227819 | `d93bd5c644fe715f3e00403e79fec629670f8d3d4b9032d8c181b80eb75666b9` |
| NYC-WTC_000153909 | 6 | 285122 | `d0e36a2544636d9f1f44c661187bf647da704b9cf80864daf5f6ef8a64816ce1` |
| NYC-WTC_000153915 | 7 | 332019 | `abd658876aea96345a4375f40144669f19d7760b4388ba98f33eec0b21fa22da` |
| NYC-WTC_000153922 | 4 | 196812 | `3d0c5bf1a8dac8c6c615bea183a34f7b261065cda00818576eb472cd1af47cc6` |
| NYC-WTC_000153926 | 2 | 94452 | `2fda66c2f96b041e259138220ec40b16c987f64ec0cd3d659bca9501ad16e527` |
| NYC-WTC_000153928 | 5 | 192371 | `b210cb96d374e77a3e81990554716626fa81afa584c72889def4165e40186192` |
| NYC-WTC_000153933 | 4 | 146159 | `1ad8b407a793986037f4f8fabde11deb45090715a239d8e276f1b411d574dce2` |
| NYC-WTC_000153937 | 13 | 460319 | `d7090b78cad6f469a0a555bcd939d84c3d7d286039967548956b772b543ec3f2` |
| NYC-WTC_000153950 | 4 | 127310 | `8de4e227d8df8872092bca9085b0893a2970c1ec5fb385f8c4f81f8179acde89` |
| NYC-WTC_000153954 | 5 | 170214 | `434f7bccd3140f9933ccc95843aa7c551b35c8c9c20ac4c4d41f8bfd592ff897` |
| NYC-WTC_000153959 | 5 | 341431 | `caaa89c30b16fafd6d08fcb1bdef2906f725e9ba3bd3eeb0365b8146cfa74323` |
| NYC-WTC_000153964 | 7 | 271806 | `7b0e40f47f823c46450993cf6dc40f0f961e6447397115e87df2648d579da5ba` |
| NYC-WTC_000153971 | 3 | 95953 | `067fe09e2d26274c75f699b94a2a3cd36ba33b6daeee76a12d77ceb58a007d4f` |
| NYC-WTC_000153974 | 1 | 56214 | `cb56ae9d529750542675e76e9e928ef3274faca4705828923f0b6e183eaab3e7` |

## Commands, environment and actual receipts

All shell commands used `login:false` and absolute paths. Initial metadata
inspection used jq only to establish response structure and select the
permitted numeric/ID fields. Tool versions were read with:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo -v
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -v
```

Both reported **Poppler 26.05.0**, receipt `1922f0`, exit 0.
Python was 3.12.14, Pillow 12.3.0, pypdf 6.10.0. These are
environment identities, not a complete dynamically linked dependency closure.

An initial metadata-only command checked five page sizes/rotations and created
the new temporary directory, receipt `56e88f`, exit 0:

```text
mktemp -d /private/tmp/wtc7-remaining-records-verify.XXXXXX
```

It returned `/private/tmp/wtc7-remaining-records-verify.qP3E63`.
Only the three requested first-page rerenders were created there; existing
sources and renders were never overwritten.

The main verification was a stdout-only inline Python check:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -
```

Initial receipt `9f0927`, session 13993; completion `2e8ef0`, exit 0,
elapsed 2.573 seconds. It used hashlib/JSON for IDs, exact byte counts and
pins; subprocess for each exact-source `pdfinfo`; Pillow `verify()` followed
by reopening and `load()` for every PNG; and pypdf media-box/rotation metadata
for expected dimensions. It required equality of the exact expected and
actual PDF/PNG path sets, not merely equal counts. Assertions would stop on a
mismatch. No OCR or page-text extraction was called.

For each of the 14 sources it ran:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdfinfo R/sources/<ID>.pdf
```

Here R and ID are notation for the absolute root above and the exact fixed
source-table IDs, not unspecified command inputs. Captured output was parsed
for page count; other PDF metadata was not printed or interpreted. All
subprocesses had a 45-second timeout; no timeout or nonzero exit occurred.

The three exact repeat commands used the same native Poppler wrapper, 150 dpi,
PNG output, and only PDF page 1:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm -f 1 -l 1 -r 150 -png -singlefile /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-preservation-2026-10-08/remaining-records/sources/NYC-WTC_000153905.pdf /private/tmp/wtc7-remaining-records-verify.qP3E63/NYC-WTC_000153905
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm -f 1 -l 1 -r 150 -png -singlefile /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-preservation-2026-10-08/remaining-records/sources/NYC-WTC_000153937.pdf /private/tmp/wtc7-remaining-records-verify.qP3E63/NYC-WTC_000153937
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm -f 1 -l 1 -r 150 -png -singlefile /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-preservation-2026-10-08/remaining-records/sources/NYC-WTC_000153974.pdf /private/tmp/wtc7-remaining-records-verify.qP3E63/NYC-WTC_000153974
```

All three exited 0 with zero stdout and stderr bytes. Before writing a repeat,
the checker required that its output path did not already exist.

A second stdout-only Python check, receipt `3e5d2b`, exit 0, matched the
acquisition table and recomputed the identical 70-PNG registry digest. It also
resolved and pinned the wrapper chain shown below. The first main check
bracketed 89 protected files (three controls, 14 PDFs, 70 PNGs and two native
wrapper scripts) before/after; all matched. The underlying executable pins
were taken afterward in this second check, not falsely described as part of
that initial before/after set. Shared libraries were not separately pinned.

Tool paths below are relative to
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/`:

| Tool or wrapper | Bytes | SHA-256 |
|---|---:|---|
| `bin/override/pdfinfo` | 156 | `fee70ade670fb025343aca2b5c3a2aacacb8ed9edce1b716b233b5de924b6bf5` |
| `bin/override/pdftoppm` | 157 | `de772e88ab9977ccde25def9b403bf42675d75f5dd82b19fbd7d8123ad183159` |
| `native/poppler/bin/pdfinfo` | 309 | `45fa717fb4aaec4bfbefc3a07612ff2539dbfcce30fb30e976aa5d4a35bef802` |
| `native/poppler/bin/pdftoppm` | 310 | `d9d81b176e8fd38d07f2fbf4f84c17dc991c6bac3730ff3cad3239c4fcbed892` |
| `native/poppler/poppler/bin/pdfinfo` | 120608 | `28cf84323fa69e7331fc3af1263d4a03e1f34618b2c5902e7bbbb2534c9ec9a4` |
| `native/poppler/poppler/bin/pdftoppm` | 89840 | `604a1ec277109188347ede09a714c334d3f801b91324f05f1c568f53ad8d8271` |

## Exact page paths, decoding and dimensions

Exactly 70 expected PNG paths were present, without missing/extra PNGs.
For each N-page source the expected basename was
`page-{ordinal zero-padded to len(str(N))}.png`; only the 13-page source
therefore uses two digits. All images decoded as RGB PNGs and all dimensions
matched `ceil(media_box_points * 150 / 72)` per axis, swapping dimensions
when the page rotation required it. This was a page-structure/metadata check,
not confirmation of a Bates stamp's visible text or document completeness.

Current PNGs total **6,902,494 bytes**. The deterministic registry digest is
`649b9c95b86248b4610440beb2fba482f31d5c25e43898ae40c85bfd6921be5a`.
Definition: SHA-256 of UTF-8 JSON with sorted keys and compact separators,
mapping each exact R-relative PNG path to
`{bytes,sha256,mode,size}`, where mode is `RGB` and size is
`[width,height]`. These are current verification-time pins. No original
render-time PNG manifest was available; temporal continuity back to original
rendering is not established for all 70 images by this later hash table.

| Exact R-relative page path | Dimensions | Bytes | Current SHA-256 |
|---|---|---:|---|
| `renders/NYC-WTC_000153905/page-1.png` | 1277 x 1687 | 127914 | `4f3b44250acb960d0395494ccbf47e3ab17406bd030876c1311fea66f3b96711` |
| `renders/NYC-WTC_000153905/page-2.png` | 1275 x 1686 | 163475 | `bb1880fc591ffc8ad3cae8d5702fc04b85b0e200534adafbae0907497aa6f443` |
| `renders/NYC-WTC_000153905/page-3.png` | 1277 x 1688 | 165872 | `8499f7d01c835143c2a6cfcf1fb555704823fc549675c76c04200bc19110a8ed` |
| `renders/NYC-WTC_000153905/page-4.png` | 1279 x 1690 | 125134 | `d36222bcabe8be80e7720454ccd9b207a91790483f8b61a1be22368213358a9b` |
| `renders/NYC-WTC_000153909/page-1.png` | 1277 x 1686 | 103806 | `980821c71a9aeb7536eb45505d325e03d5e3b4306ce7d1da56446815987e2bce` |
| `renders/NYC-WTC_000153909/page-2.png` | 1279 x 1687 | 175683 | `bc79174be6ca8c2312bf76be11dfb8d1431732dc75a88b6012f2560ed631ab83` |
| `renders/NYC-WTC_000153909/page-3.png` | 1276 x 1685 | 189392 | `9599848c3bc2c3e5ec81419fcf3957a0ffe9fa2024801736f8464e580ffae6ae` |
| `renders/NYC-WTC_000153909/page-4.png` | 1276 x 1686 | 157595 | `313b4fdf090049f8e721dc83c60f9963e9d13fcdbce9cead89f2c88301856e3d` |
| `renders/NYC-WTC_000153909/page-5.png` | 1282 x 1689 | 19123 | `b4d564ab88084e607d842e5b2b73d32439e210233356243d94512baacf0717b1` |
| `renders/NYC-WTC_000153909/page-6.png` | 1275 x 1684 | 80382 | `91334aad0a079a7703ee6a33bc583c856b9bf265cdaed94983f70a7d01bdbd2a` |
| `renders/NYC-WTC_000153915/page-1.png` | 1283 x 1689 | 90002 | `2995d76a9f3c2dfdde2a4616c85df5ed652b930357fa86c1f80131987fffa1e1` |
| `renders/NYC-WTC_000153915/page-2.png` | 1686 x 1279 | 80693 | `7e39a8e143b1fe674c572783d2654ea900feed76606b860623b1bd918ca13b40` |
| `renders/NYC-WTC_000153915/page-3.png` | 1281 x 1686 | 114297 | `664428a962c1b9b1dc4e806b32e0c9d9c2015f6529defd4a5d425a8f4692c5a2` |
| `renders/NYC-WTC_000153915/page-4.png` | 1690 x 1284 | 79086 | `cee7346ac66f032b41fe5826dc3b7439200c9d6abc65e4d20a1a2ae1992bdd87` |
| `renders/NYC-WTC_000153915/page-5.png` | 1312 x 1711 | 119786 | `3e3e7720b358589bbc65d3fd89e2913fcb0e9d2172014db09a610b9ee6e31d1b` |
| `renders/NYC-WTC_000153915/page-6.png` | 1688 x 1279 | 101783 | `4fd9e7dde03b506a25502bee21894235f87edf9200f9051e2f108987528106b7` |
| `renders/NYC-WTC_000153915/page-7.png` | 1281 x 1687 | 74790 | `9ac293f9881f71df79fecf13e1591e7bfc3991fc5970f5dc3a2480dfcdd175fd` |
| `renders/NYC-WTC_000153922/page-1.png` | 1284 x 1687 | 119312 | `aee5479acd5872849d345c4d6b3167d7eeb970901a30b0e109b1b6d3695b9c26` |
| `renders/NYC-WTC_000153922/page-2.png` | 1284 x 1689 | 108744 | `0aa9b42882b99f0619383062ccc39654bed7bd91bbd193381905043635c4b162` |
| `renders/NYC-WTC_000153922/page-3.png` | 1278 x 1682 | 117891 | `b0763384cbae79292d2bbb838cac3ebb2a1637f2eb1f7f2273d14001d6fb0b64` |
| `renders/NYC-WTC_000153922/page-4.png` | 1277 x 1681 | 124716 | `6833f05271e0aaaefb5d9dbdd3730b8451a563aa165799eef60b5defda652ba5` |
| `renders/NYC-WTC_000153926/page-1.png` | 1287 x 1686 | 111752 | `9cc6c28e65f3a59c3fc23084a5edcffce9e1bae383fa64c73f7dc45a1ae83dd3` |
| `renders/NYC-WTC_000153926/page-2.png` | 1279 x 1682 | 102463 | `9cb9076e716c7dd3f01d8d28e7778823723c385a247fe82da549ebffe718550a` |
| `renders/NYC-WTC_000153928/page-1.png` | 1277 x 1683 | 107244 | `9180d86c466366def3ad66dccf549810e3301379f760113a3c3646eabea310f6` |
| `renders/NYC-WTC_000153928/page-2.png` | 1279 x 1686 | 108841 | `6281a7344fbdac72f66ea9221f76a96cb5fbcfd24d3a9c8f1671e55eeb28807f` |
| `renders/NYC-WTC_000153928/page-3.png` | 1281 x 1684 | 50767 | `f2547cbaa3c68984122227fd122711fc9221bb24454cf6a8f93c287a5fec03eb` |
| `renders/NYC-WTC_000153928/page-4.png` | 1281 x 1686 | 100084 | `74dc723394958b3d28aa1660754d8d05e6f586ebd12eaf75c2417f9f7095a619` |
| `renders/NYC-WTC_000153928/page-5.png` | 1279 x 1687 | 93448 | `4323820e4bc82093a0b7f1bbfd86723d4da70095bf86824a9465de193e1a8250` |
| `renders/NYC-WTC_000153933/page-1.png` | 1279 x 1687 | 79344 | `6781740fe7b7e0ca5cdbf7158d9d411ed19ff9db5513c501b0ee24e72c46450d` |
| `renders/NYC-WTC_000153933/page-2.png` | 1279 x 1684 | 71073 | `65f58b04b382ed2108471c48a3c6725084e85e499b4e915ec316df4eaeae25be` |
| `renders/NYC-WTC_000153933/page-3.png` | 1279 x 1684 | 98449 | `7ec841bb1da9b48c7a5bab5c21385ba76664fbcb13b28690dd6af3e0c64ab3cb` |
| `renders/NYC-WTC_000153933/page-4.png` | 1279 x 1687 | 92298 | `2efa768803bdc69580af0eacac211f9894698a896e549cd4e6fca8a04e7753a3` |
| `renders/NYC-WTC_000153937/page-01.png` | 1279 x 1684 | 98944 | `ca1d767fe4b4d1fa24f64f186d6a51778f77398d73b33d334af2d0132ebc76eb` |
| `renders/NYC-WTC_000153937/page-02.png` | 1279 x 1684 | 92957 | `b9194808a2a1611be7b796d862fd764c62ad54de923d74887aa80de3df808c29` |
| `renders/NYC-WTC_000153937/page-03.png` | 1279 x 1682 | 121445 | `7b15ec7aeb5821a9f7d44a218e6ece868e60fecf7a6c851e3484a32ca36b6a9e` |
| `renders/NYC-WTC_000153937/page-04.png` | 1287 x 1691 | 22991 | `666d4663aa646c60b2df7c64c7e75540d43169955cc669c2397f4124e11058db` |
| `renders/NYC-WTC_000153937/page-05.png` | 1279 x 1682 | 90195 | `5e1cbb3833f4b1ec849ac7897bdbf8ab776649261aea4cd814505dae64427ad7` |
| `renders/NYC-WTC_000153937/page-06.png` | 1279 x 1682 | 80551 | `a16e3946e41b3fbc159171b8f54ed8c43211872c21ba53f0d4fc4973aa2e0444` |
| `renders/NYC-WTC_000153937/page-07.png` | 1279 x 1682 | 89759 | `e3b8461daa9fb6c35a4819553504a31794ea24cf7d31ea73dcf8534c8ecbb161` |
| `renders/NYC-WTC_000153937/page-08.png` | 1279 x 1682 | 29459 | `35aef85739186219be4f7c03f1f34f147f81b46863debe964063c752da42cb1b` |
| `renders/NYC-WTC_000153937/page-09.png` | 1279 x 1682 | 98757 | `e6446225bb9a2cec17d7aa2167df61074fde11fe940fd3152c0dc34fcc273642` |
| `renders/NYC-WTC_000153937/page-10.png` | 1278 x 1681 | 111816 | `8985feca4330f18e36529b73633eb08a1e656ab754daa5b45d31b10f7656bb5f` |
| `renders/NYC-WTC_000153937/page-11.png` | 1279 x 1684 | 97310 | `3468b5d8a7e2df00a7cb8d7371a076eda20748102e0c0f026f4f6d074b279257` |
| `renders/NYC-WTC_000153937/page-12.png` | 1279 x 1684 | 107081 | `37d39f9365323bda747bda4ed602cba12752ce33c8feaf1558c065ba7bb7c426` |
| `renders/NYC-WTC_000153937/page-13.png` | 1279 x 1684 | 32874 | `1b4832c929240233fe70d915a3849c3deb20eaf0264b2e06e380fd7c1ab5811b` |
| `renders/NYC-WTC_000153950/page-1.png` | 1282 x 1689 | 80209 | `f5a7d9f6ae15c685dc2fd243fe8cc50e3498935fa61034e1e6a95a2fea99b621` |
| `renders/NYC-WTC_000153950/page-2.png` | 1279 x 1684 | 80446 | `203934319addf6a2943b3ac7a89dffb504125e6d48f03923e33ddeb0a99f3b89` |
| `renders/NYC-WTC_000153950/page-3.png` | 1279 x 1687 | 79899 | `72a366f0d8e346f3f57830f167ce08a24c9b93fd9859bd01285fb6cbdc8487ef` |
| `renders/NYC-WTC_000153950/page-4.png` | 1280 x 1687 | 66577 | `e4620296830b5c2aa2844e549e17daf94cd5f1f94d29cad76d0cc7831acbe3da` |
| `renders/NYC-WTC_000153954/page-1.png` | 837 x 1322 | 60393 | `4041e365923094034df9fafa068666435a690689ff6f7a735849970c253fe709` |
| `renders/NYC-WTC_000153954/page-2.png` | 1279 x 1686 | 141456 | `a29626a83a7208f99c8ce42d357f285e0c1b2058f88a47d7083f72cafce6581b` |
| `renders/NYC-WTC_000153954/page-3.png` | 1282 x 1689 | 63005 | `80c0edddb9bb027641e83de909c2dc996c8ffc51e4606611732ddd9cc3e90971` |
| `renders/NYC-WTC_000153954/page-4.png` | 1657 x 1321 | 48671 | `24f89d8f2b24b71e207bacbaa1c37333f1a4a331d18066fa722c3e2f34570c52` |
| `renders/NYC-WTC_000153954/page-5.png` | 1661 x 1327 | 44428 | `fceceb80e1b6ad53fe76facc1a21531b2b127075319d829dcb9391bb9d454f46` |
| `renders/NYC-WTC_000153959/page-1.png` | 1280 x 1686 | 143190 | `732619fccd925623428c8177bb581c5dcfdbbee579491d536bf62e8377545469` |
| `renders/NYC-WTC_000153959/page-2.png` | 1279 x 1686 | 146581 | `4584caef414bc78027ab3d1e93428000102329fb382685088e12d911c809b656` |
| `renders/NYC-WTC_000153959/page-3.png` | 1284 x 1691 | 144152 | `2e0fe34078945d13978b47d17408c8d610649a1e67fd8f6a182d0a5825d850b0` |
| `renders/NYC-WTC_000153959/page-4.png` | 1283 x 1689 | 152695 | `8e6bc7c5358a58ec46af3e7597d6f8aa42af0d7bb89e149acb4c51a6ef1c254f` |
| `renders/NYC-WTC_000153959/page-5.png` | 1282 x 1689 | 155143 | `ff2c2f2d0b97b3c613d71c8634c8f17f176aa93e1eca4435a55e94cc92fd594b` |
| `renders/NYC-WTC_000153964/page-1.png` | 1660 x 1321 | 30931 | `d2142404fdf4703ad78048c95b99b81e5a9dfd7ceeea82b8230afa0fc65c8c1f` |
| `renders/NYC-WTC_000153964/page-2.png` | 1668 x 1332 | 39807 | `c2012681729093f3630fb932761ff36ad412b5e537bd5a56fab90650c1b0ad5e` |
| `renders/NYC-WTC_000153964/page-3.png` | 1272 x 1659 | 118645 | `1e29b86d2b1683a076590e44854fc6d97f66e3fc1c113b2b8103db6381744047` |
| `renders/NYC-WTC_000153964/page-4.png` | 1272 x 1660 | 116475 | `f5e3abdd2cf9acd7c0111d3fecbe59d8def7729c8123669315cd63312e4a8eed` |
| `renders/NYC-WTC_000153964/page-5.png` | 1267 x 1650 | 93623 | `e7c8bbd9e895469e87f20b38c4fb4781b271e4eed597f4400574771f646b4cc1` |
| `renders/NYC-WTC_000153964/page-6.png` | 1272 x 1654 | 104786 | `b1cfb3bcca5e6fba43c50f336112afeb650a9e8513b7415dff0fa7ad333a5952` |
| `renders/NYC-WTC_000153964/page-7.png` | 1269 x 1655 | 103753 | `50dc1e049f05fff0867e8f431ee5186d6c1c7d58921e5d4ab92119738c9e4fad` |
| `renders/NYC-WTC_000153971/page-1.png` | 1281 x 1683 | 129063 | `cc336abaa44925d9cba9980b4cc7db789129e4635351fe431ef5f26d41473a5b` |
| `renders/NYC-WTC_000153971/page-2.png` | 1279 x 1686 | 29337 | `3a56f24ee718c4e616f7756cb4627a9834ee119e4f710628765936e08387cfef` |
| `renders/NYC-WTC_000153971/page-3.png` | 1279 x 1686 | 77126 | `46280648f81d9c6dc2adfcfdb9a5671a7cc9408775cead1e1d22322dbd8c8178` |
| `renders/NYC-WTC_000153974/page-1.png` | 1279 x 1686 | 122725 | `1ca1294b29a17cdc644099406f14209bba8a53217aaefaeb23ec97b914d2b912` |

## Three fixed rerender comparisons

For each row below, the fresh PNG's bytes, mode, dimensions and full decoded
RGB pixel array equaled the existing original page PNG exactly. The pixel
hash is SHA-256 of Pillow's complete `tobytes()` RGB buffer; no threshold,
resizing or favorable-region selection was applied.

| Document, PDF page 1 | PNG bytes | Matching PNG SHA-256 | Matching RGB-pixel SHA-256 |
|---|---:|---|---|
| 153905 | 127914 | `4f3b44250acb960d0395494ccbf47e3ab17406bd030876c1311fea66f3b96711` | `b7e6e9d8597d1fdce7ed339d48fb365f8d39aefedfcbc239c3da216d71d22d38` |
| 153937 | 98944 | `ca1d767fe4b4d1fa24f64f186d6a51778f77398d73b33d334af2d0132ebc76eb` | `f445c33d5de2de55790ccc93f852eabab6c5b7f159ec7bdfdefaf57c407836d7` |
| 153974 | 122725 | `1ca1294b29a17cdc644099406f14209bba8a53217aaefaeb23ec97b914d2b912` | `a9a1c164d299621884216dae05917405d255bb921bc012bab93bc985e72f1aef` |

The independent step is the separately written reconciliation/check and fresh
render invocation. **The renderer is shared Poppler, and pixel decoding uses
the same Pillow implementation for both copies.** Exact agreement establishes
repeatability for these three selected pages, not independent renderer fidelity
for all pages, historical authenticity, preservation compliance or substantive
correctness. The other 67 pages received format/load/dimension/hash checks,
not a fresh-render comparison or new visual reading.

## Stop and preserved boundary

Technical acceptance is complete for the checks listed above: 14 acquisition
hash/roster matches, 70 exact paths and valid dimension-matched PNGs, three
exact byte/pixel repeats, and unchanged protected inputs. No technical failure
or mismatch occurred in this bounded check.

Marked-content analysis remains stopped pending the specified authorization.
No primary-B interpretation note, peer rotation, substantive reconciliation,
human acceptance, cause ranking, legal promotion, network request, engine
change, commit or push was performed by this technical task. Root owns current
status/navigation; this record does not silently complete the content unit.

