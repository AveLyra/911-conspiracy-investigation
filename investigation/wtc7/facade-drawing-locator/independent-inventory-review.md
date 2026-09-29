# Independent inventory and archive-name locator review

2026-09-24. Separately authored computational-agent review. Research-only;
no structural-expert certification, original-source authentication or causal
finding. The main repository controls and charter govern. The evidence /
falsification and source-of-truth skills were read and applied to separate
inventory pointers from supplied drawings and bounded negatives from absence.

## Canonical and public inventory pass

Before this file was written, the reviewer independently read the complete
existing `camera3-facade-feature/source-geometry-review.md` and searched the
current main inventories. No original dimensioned north elevation or upper
louver attachment drawing was identified in this bounded inventory layer.
This is not evidence that the drawings are absent from held productions,
unreleased, or nonexistent.

Case-insensitive regular expression:

```text
\b(drawings?|elevations?|Roth|louvers?|louvres?|curtain|architectural)\b
```

| Main-repository source | Scope | Result |
|---|---|---|
| `intake/source-inventory.csv` | 133 records; title, document type, original filename, current path, status and notes | No target-term match; no SRC drawing candidate |
| `exhibits/index/exhibit-map.csv` | 25 records; title, relevance, file path and notes | No target-term match; no EXH drawing candidate |
| `research/wtc7-video-comparison/source-manifest.csv` | 27 records, all fields | No target-term match |
| `research/wtc7-video-comparison/media/video-acquisition-manifest.csv` | 9 records, all fields | No target-term match |
| `research/wtc7-video-comparison/` | All 15 files returned by `rg --files` with `.md`, `.csv`, `.json` suffixes | Only generic structural-drawing references in the comparison memo at lines 132, 178 and 221 |
| `authority/source-index.md`, `authority/authority-index.md`, `authority/README.md` | Complete target-term search | No target-term match |

The comparison memo's three matches are general methodological/argumentative
references, not an attached sheet, a sheet identifier, a technical page locator
or a request identifying this specific drawing. No exact supplied-drawing
classification or SRC/EXH join follows from them. The previous source review's
Emery Roth & Sons 1985 family remains a lead, not a newly reviewed original.

CSV parsing used `csv.DictReader`; canonical sender, recipient and origin
columns were excluded. No whole inventory rows, contact fields, correspondence,
private identifiers or raw notes were displayed. The public-reference snippets
were confined to the three generic drawing mentions above. No PDF pages,
archives, web results or source payloads were opened during this first pass.

| File, relative to main unless specified | SHA-256 |
|---|---|
| `intake/source-inventory.csv` | `9b1a2d364314ce1a8aec8ff3ea4775d3ed24d3707cf19f18cb70bd11395d1352` |
| `exhibits/index/exhibit-map.csv` | `2d1e61b551d5adf83ff07be57703fa9db3e316248305b5ca1b7838580b3176a9` |
| `research/wtc7-video-comparison/source-manifest.csv` | `6d3fe8322ee8c914500086d7add9f5886eb291e22ebf8456d17a0cb5b7fb5521` |
| `research/wtc7-video-comparison/media/video-acquisition-manifest.csv` | `5f39f34f6ba978ff8e030c632ab49c54950faaaf2fb3654ccd5cdc14bdfee6dc` |
| `research/wtc7-video-comparison/wtc7-video-demolition-comparison.md` | `b0236c2e63a0602bec3fd6bd846d243220418bf06234dfa8f7db622c42a3464e` |
| `authority/source-index.md` | `c8f942aeda021e7390a3609fff7eab554b32e58041243ae59595f4ebffddde3a` |
| `authority/authority-index.md` | `5709964b62811892519d7a752ab49971b2fb385cbc61904168d418bf1a9a6ae6` |
| `authority/README.md` | `917e13598440b645ba25a4fc9b23b8ef48ca6ab8876db7c56f3a7ac0696e5453` |
| Worktree `camera3-facade-feature/source-geometry-review.md` | `e2af9e7d546e2f35b122bded6f69b467c810c79894b37b970bb0f06f02aa86d9` |

The 15-file public research catalog digest is
`82392e14c22e7b892bc2993e93065d28b295d5409518360a45bf071700562ae9`,
computed from sorted `relative_path + NUL + file_sha256 + newline` entries.
The four CSV hashes were also rechecked unchanged at the end of the pass.

## Independent metadata reproduction: declaration before results

The parent requested an independent reproduction of the locator protocol's
six-root file/member-name coverage. This reviewer has not read root's
`run01/results.json`, locator implementation, counts or archive results at
this declaration. Read-only inline code will be written independently.

Use `rg --files --hidden --no-ignore` separately in each declared existing
root, without `--follow`; record absence/error separately. Exclude this
locator unit and its descendants from both research trees. Sort relative
POSIX names, match the protocol's stems without a word-boundary requirement,
and output only root labels, name hashes, suffixes, term labels and counts.
For the independent pre-comparison catalog, hash newline-joined relative
names with a final newline for each nonempty root. Retain no new plaintext
name lists. Known pending-packet path families 11-209 and 12-009 are excluded
before archive opening; any additional known aliases supplied by root will
also be excluded. Unknown aliases cannot be recognized by a naming-only scan.

ZIP/TRZ metadata inspection will read only file metadata, the bounded end
record/central directory and `ZipInfo` fields; no extraction, payload opening,
nested recursion or execution. Before `ZipFile.infolist`, reject symlinks,
files larger than 1 GiB, invalid/ambiguous EOCD, multi-disk or ZIP64 records,
more than 100,000 entries, or central directories larger than 32 MiB. Record
other-format containers separately. Plain model GZIPs are not treated as
drawing indexes. Each archive's matching name catalog will use hashes only.
Freeze independent counts and catalog hashes here before reading root's
results, then append a comparison and explicit limitations.

No authority boundary changes, main/source edits, external transfer or case
promotion are authorized by this locator.

## Frozen independent metadata results, before root comparison

The independently written inline Python command exited 0. At this point the
reviewer has not read root's locator code or `run01/results.json`. Root supplied
no additional known pending-packet aliases or hashes; that is not an assurance
that no unknown alias exists. Names were never printed. Source-byte hashing
read archive bytes for integrity only; no member payload was decompressed or
interpreted. EOCD/central-directory metadata supplied the names/counts.

All six exact roots were checked; five existed. The independent implementation
used `rg --files --hidden --no-ignore` with each root as `cwd`, then sorted its
relative names. The exclusion prefix was
`sherlock-wtc7-investigation/facade-drawing-locator/` (including the unit name
itself). Match stems were `drawing`, `elevation`, `roth`, `louver`, `louvre`,
`curtain`, `architect`, each case-insensitive. The earlier canonical CSV pass
used whole words, deliberately distinct from this protocol's path stems.

| Root label | Files | Matching paths | Independent relative-name catalog SHA-256 |
|---|---:|---:|---|
| main-authority | 47 | 0 | `6021584016997d8dc692e075377a1b8116f5796af73d33a0d900c2bf9f083746` |
| main-research | 10,117 | 0 | `eb2d391100af93429e2a595680f941e562cb026fb10c47545359569a8788778c` |
| main-raw | 151 | 0 | `062e8e8fef1b03f7b159bc7da53f1ae06eb71e2a9c3041227575efe3198423aa` |
| main-processed | 56 | 0 | `32f9ff7a215b17e3b088786dbca21ae38efc0585cf87f00603d269ba4619b306` |
| main-filed-exhibits | absent | — | Not created |
| worktree-research | 22,529 | 3 | `bc28d8fcf9c51cbea87b3e766a541cede6ecc1fff5e1d19c7ad92ad864fca88d` |

Total **32,900 file paths**. The three positive names all matched `drawing`:
two `.md` paths and one `.pdf` path, all in worktree research. A matching path
does not establish an original drawing. No returned file path was a symlink;
this is not a separate inventory of symlinks that `rg` omits, and directory
symlinks were not followed.

The combined independent catalog hash is
`08644d06f7177ae33de973ff802c069636e11d5e20c7fb87628dd2e8e4c48e28`.
Its recipe is sorted `root_label + NUL + relative_path`, newline-joined with
a final newline. This intentionally distinct recipe must not be compared
as if it were root's serialization. The three-match JSON catalog hash is
`43f445e3aa7aafc5291a262e29bbb5925fa5e6ee823e00d11afcd46d56cdfa66`;
entries contain only root, relative-path hash, suffix and matched stems, in
enumeration order, JSON with sorted keys and separators `(',', ':')`.

### Archive/member metadata

**14 ZIP/TRZ paths**, **25,755 member-name entries**, **zero matching member
names**. All 14 passed this run's EOCD and size gates. None of the returned
archive paths matched the excluded pending-packet naming families. This does
not prove those packets nonexistent or establish an unknown alias's identity.
There were no rejected/unreadable ZIP/TRZ paths in this finite enumeration.
Eight other-format paths were `.gz` (two main-research and six main-raw),
counted but not opened as drawing indexes. No other configured container
suffixes (`.tgz`, `.rar`, `.7z`, `.tar`, `.bz2`, `.xz`) were found. This suffix
check cannot identify an archive hidden behind an arbitrary extension.

The following frozen archive-byte pins and member counts retain duplicate
paths. Two main-research TRZs share the same bytes/member names; copies are
not independent sources. Member catalog recipe: sorted exact names,
newline-joined, final newline. ZIP directory entries count as entries.

| Root | Relative-path SHA-256 | Archive-byte SHA-256 | Members | Member-name catalog SHA-256 |
|---|---|---|---:|---|
| main-research | `7cf7c0f9134bbdf8b0510c38135fdae0cac7d116f201e2fae129f82104b37ec1` | `20687c183a965610c58899ee419137d9417638f521af865a84d8610a28d7d5fd` | 7 | `509fd896f2a82b9a7100edb0fd60c7ec18bb94398bd0a7c49dbc5dfb737970ce` |
| main-research | `d2e01069e2865422d26696b9e68272d3d9e83f86df60c8c5cb208c3e0b9e7227` | `c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189` | 55 | `1c732630fafc65e44709e630e9336d6a7134a5185142f11e6ee868497b8386d8` |
| main-research | `812a698f9a9aed7781c6b52015352aed9b890c0fd8159e4037169f8109622d0f` | `aceb800c8baa6b39ceba698fcf16198fe9f0480c66673065d31e0203c09306a8` | 5 | `a6b099f4fd596e47d8e576bf6f4594fe6fad7ddf13204a175e3e4b225893951e` |
| main-research | `d19504d15e1069f787ef92e4ceaf801abd2ef2dbfa7b903a974da1e288ac119f` | `aceb800c8baa6b39ceba698fcf16198fe9f0480c66673065d31e0203c09306a8` | 5 | `a6b099f4fd596e47d8e576bf6f4594fe6fad7ddf13204a175e3e4b225893951e` |
| main-research | `6f7232c038b0197a5e0ac9788b034096b52ecbf5bbc29743a8bb3f9ca99b3265` | `9f5ed822b4f5b28efef1051d731eb64d27547ef44903c897fe946c806267f25d` | 1 | `4d74a7032a81569a2cffb772ef82a728771041efa82c159777d3be07ab09a1eb` |
| main-raw | `60ff420539fc3a2c36e63928fc2298dc1ac5e221fc5f42cbcac019ed5b2592c7` | `f92c33db94425d564549140458c3d1a11e3f04f9642b238e2248db277781a1fa` | 4 | `d737fe3719e0a3f4b18a9d2d93670f65b2c2d020f7f7f8e31e50f325b11eaf72` |
| main-raw | `c25252c3e251223d416c67031ee7ab524aafea4d794f07f4ee91bb152b07c80e` | `fafdf59060838d1f462bde6f3502728591645a37ed373bdfd81a90c22f6a23dd` | 6 | `3ede593bc31b9a42461858a9a2cc4aab6c93bc6ef1aab263cb1d09f0ce81e4ca` |
| main-raw | `973ab5b58a085c6a5304b8f9a9a8b9453c0f3db8593eec95d45e09526680c130` | `024484d96a67f31c0490abbe176c488569b3cffe76da1005cee49ccc9478fa91` | 6 | `3ede593bc31b9a42461858a9a2cc4aab6c93bc6ef1aab263cb1d09f0ce81e4ca` |
| main-raw | `c3d560cc6e2cab22ec0d389f3037fb2428a1ad6a98c86f6ef6520a4fb55343ba` | `1f4a4ada81381e03b24fa41913fafd5f44911a812ce554b8d2af49206bdabde5` | 2 | `f762ad6f8fdea3c583656655c062955ce0a67d7da13cdd4e6cb33b6cca063e0f` |
| main-raw | `60fd4bc694acbda725fa880f856be684204a1f597826eb3121672c1f65cce48a` | `717d3519a001d046296ffc93aa36f60e1fe2d1f6acc269e95a0346581d8f331f` | 3 | `5d18a66a5fe4da69ed1ccf2a3cbdd81e195c4b2e95d646f0b45aa03b519c2355` |
| main-raw | `ebb87b48b39086c08590bb8af8def01f3b0133ec5d3d80bc127c093d05bd858a` | `2e61dbe6262f4ee79fd8349beaf423869bf2d99b16e6be5b32529f1e15e2c897` | 8 | `bff44b0f12732488aee9700c760abb9748590f0001cfe0783c1aa7ae1b96094a` |
| main-raw | `c45f80703e185d1b74105f00bd0af1786ea3fa1cbf782da53d2f2edffc610cf5` | `2a2ec74d4806df1c03fb7054aeb7bdec8be476fa1b51f0f526496d5fa770de36` | 7 | `b41bb53ca50a5a5be66147841b12dd29769af45be333902e9f1a7a1db3cfd530` |
| main-raw | `1614e0973e45ab462c156f3af04b2b34db550fa1df41f7cd717baff00cad0b94` | `2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181` | 25,639 | `c4074dbcd0747bb98df1e0b97d3447a24df7c18de009dea53a4bfed7f25f7284` |
| main-raw | `07daaed89e0768fa9447d1a44ccfacadb3ed052e36a3c109e2575d20dcd852e1` | `0f5c9c4a781073ada5967a49f5336e4a9194af3a5263914039e287e8e808795d` | 7 | `87b182f0581d0428fe4fa117cb72fea74abc426b0efbf9024b10e110b5761bc9` |

All 14 archive sizes and mtimes remained unchanged during their individual
checks. This is an integrity check, not proof of original authenticity or a
check of all changes before/after the entire investigation. Central-directory
sizes were 56–2,204,824 bytes. The largest inspected compressed archive was
172,774,879 bytes. Zero member matches produce JSON `[]` hash
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

The independently observed metadata supports only this finite-name-search
result. Generic filenames, nested archives, arbitrary suffixes, unnamed sheets,
scanned PDF contents and unknown aliases remain outside identification. This
scan does not show whether any payload contains the requested architecture.

## Post-freeze root comparison

The pre-comparison version of this note was SHA-256
`9fb6b199775227831b2a0528e266a938091be8e5cdd66c67dea424d05868eb4a`.
Only after that pin was displayed did the reviewer open root's
`run01/results.json`, SHA-256
`d7a9c499fe5fda082d905dc3ad4cc4b068a2b4714b722c667b787db25bb10821`.
Its protocol pin at that point was
`4f5720bd45da86ddbb83abbae38f8a7982cdf7abd38e83168a3669bd64612f4d`.

The counts, all three matched relative-path identities/stems/suffixes, all
14 archive-byte hashes and member counts, zero member matches, both canonical
CSV pins/counts/negative results, and all eight other-container identities
agree. A second independently implemented command verified this with explicit
assertions and exited 0.

Catalog hashes initially differ because the independent recipe sorts relative
strings and uses LF delimiters, while root sorts `Path` objects and uses NUL
terminators. Root preserves central-directory order for the member catalog;
the independent initial recipe sorts member names. These are serialization
differences, not discrepant name sets. The comparison command re-enumerated
using NUL-delimited `rg` output, verified there were **zero newline-containing
paths**, retained the original independent sorted/LF hashes unchanged, then
recomputed root's stated serialization. All five present-root catalogs and
all 14 member-name catalogs matched exactly. The absent sixth root agreed.
This normalization was done only after the independent findings were frozen.

The independent original archive guard already rejected the ZIP64 locator
signature in the 20 bytes immediately before the EOCD, in addition to sentinel
fields. The parent flagged a possible gap in root's original guard; the second
independent command retained this stricter rejection and also rejected a
minimum-length ZIP64 record signature immediately before EOCD. All 14 actual
inputs still passed; their frozen byte hashes and both catalog forms agreed.
Thus the stated metadata results are independently reproduced on these inputs.
This is not a synthetic adversarial test or a general certification of root's
parser; the separate parser review owns that question.

## Frozen independent identifier-extension results

After reading `IDENTIFIER-ADDENDUM.md`, but **before reading root's identifier
results or wrapper**, the reviewer independently queried its three exact
case-insensitive predicates. Root's parent message had already disclosed the
expected zero-result direction, so this is separate execution, not a blinded
expectation. No root implementation/result values were used to compute it.

```text
WTCI[-_ ]*0*120[-_ ]*I(?:[^A-Za-z0-9]|$)
FOIA[-_ ]*12[-_ ]*178(?:[^0-9]|$)
120806[_-]1247(?:[^0-9]|$)
```

Results: **zero matching paths** among the same 32,900; **zero matching member
names** among the same 25,755; **zero matching rows** among 133 source and 25
exhibit records using the same allowlisted fields. All source/archive pins and
catalogs remained as above. No additional payload or container format was
opened. The filename query includes arbitrary suffixes, but a matching ISO
would only be a path locator, never a mounted/read filesystem.

Twelve declared-string predicate controls passed: positive and negative cases
for each identifier, including rejection of trailing `II`/`IA` for the WTCI
Roman-numeral suffix, rejection of `1789`/`179` for the FOIA number, and rejection
of a longer numeric volume suffix or missing required volume separator.
Positive cases used the addendum's named technical identifiers and their
permitted lower-case/compact variants. These are regex checks, not independent
verification of the uploader's production attribution.

This paragraph freezes the identifier findings before root-identifier result
inspection. The source-locator ceiling is unchanged: generic unnamed/scanned
payloads, nested contents and alternate unknown identifiers are untested.

### Identifier comparison after freeze

Pre-comparison note SHA-256:
`b9d44666ed8d7d3194387285cc242ac0d6a6344de1b778c1755103350c3e05d8`.
The reviewed identifier addendum is
`923c245ad4c92915716cf39b5f091048ee835fb64512aa71b285a252b5e6470c`.
Root's subsequently opened `identifiers01/results.json` is
`1c371828bc33292bd6f824c74fac2299e89556a91bfc9f828d9b508efd4d72d9`.

A further read-only Python assertion command exited 0: all three exact
predicates, six root states/catalogs, 32,900 path count, 14 archive-byte pins
and ordered member catalogs, 25,755 member count, both canonical CSV pins and
record counts agree with the independently frozen result. All three match
categories are zero. The root identifier run reuses the same observed catalog;
that agreement does not convert the new uploader identifiers into verified
agency attribution or make a name search into content inspection.

## Verification scope and final disposition

Actual commands were read-only `python3 -B` inline programs using Python
standard-library `csv`, `hashlib`, `json`, `pathlib`, `re`, `struct`, `subprocess`
and `zipfile`, plus `rg --files --hidden --no-ignore` (the comparison added
`-0`), and named-file SHA-256 checks. The first program independently produced
the frozen counts, archive pins and LF catalogs. The second independently
re-enumerated names, asserted the frozen values, normalized catalogs for root
comparison, and separately computed the identifier results and 12 predicate
controls. The final program asserted the root identifier predicates/results
against the already independently verified catalog. Each computation exited 0.
No root locator function was imported or invoked by the independent programs.

No names, contact fields, raw notes, correspondence or payload text were added
to this note. Only this review file was created/updated by this reviewer; main,
sources and other agents' products were unchanged. The root's new architectural
web lead and any source-image review are outside this review's scope.

**Disposition:** independently reproduced finite locator coverage, with no
identified original north-elevation/louver-detail source in the named inventory
and name-search layers. This satisfies this reproduction task, not original
drawing inspection, a physical body/COM constraint, a ranking change, or goal
completion. The remaining specific dependency is a safely selected actual
dimensioned sheet/detail with revision and feature correspondence, not another
claim of global absence based on these negative names.
