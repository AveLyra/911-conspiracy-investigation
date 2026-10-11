# OEM comparison execution and provenance

October 4, 2026. Investigation worktree, branch
research/sherlock-wtc7-investigation, HEAD ca1c2233. Intake completed with
exit0 (`58b397`, original handle89916); existing WIP preserved. Main AGENTS,
WORKFLOW, START-HERE and full-charter hashes remain unchanged (`44f8bd`).
Applicable instructions were read; preceding goal turn was progress. No
network retrieval or main-source modification occurred in this comparison.

## Initial fixed pages and current identity

[PROTOCOL.md](PROTOCOL.md) was saved and hashed before new source viewing:
`d90c185f2d39ef527677e2302cf586d57de76b276540dafa37226c177fb9e905`
(`4e59cc`, exit0). It fixes physical59-61 / printed25-27 and treats existing
municipal results as known rather than blinded evidence.

The source is the held main
[NCSTAR1-1J PDF](/Users/admin/docs/911/research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/sources/ncstar-1-1j-attempt02.pdf),
578804 bytes, SHA-256
`7b1fe2a7a94a67c54fdaabe27e3309b439551512cff97e5026e0b62bb51bf623`.
Root ran shasum and pdfinfo (`04e8a3`, exit0), confirming84pages and print
permission. The PDF's template title/2008 metadata is not substituted for
its report identity or treated as fraud evidence. No permission bypass or
content extraction occurred.

Root's read-only Python check (`4e59cc`) compared the three held original and
reproduction PNGs against their exact prior receipt entries, including the
matching source pin, dimensions and recorded zero stderr. All three byte
comparisons and hashes matched. Root read the entire separate
[provenance check](provenance-check.md) (`17a618`, exit0), which independently
verified source size/pin, all image pairs/header dimensions and exact receipt
fields. This is fresh integrity checking of earlier reproduced derivatives,
not a new renderer run or verification of a historical exit code absent from
the old receipt.

| Held physical-page image | SHA-256 of each original and reproduction |
| --- | --- |
| p59.png | 880960ccfc33489160eeeda73d9900d77977b3ff58c459042826c1db13b25250 |
| p60.png | 8abc1a82fa2ecf87b58bfa34ff531fb8fd19af1fedfe72e5b78492cf6641c798 |
| p61.png | c0577e09891e1cc0b6607dbc35093f34142c3208f045f6fdacc09f405892594f |

Old reproduction receipt SHA-256:
`8dad5cf679a7ab1e2b476bf7a9ca6fa51a3ed4db99465365996c21c064802147`.
Current provenance-note SHA-256:
`8d980244f46dff4901c436cc7223aa205593de6dfaadde8fa832e0b9895ae7ef`.

## Initial independent readings

Root viewed all three complete pages once at original detail; no repeat,
crop, OCR, measurement or other primary page. Frozen [root notes](root-observations.md),
SHA-256 `b07785bd6ce44518915a15c632782f7495786eb55906a3c93d4c90189ae8eebd`
(`8f334e`, exit0), preceded substantive exchange. The separate reader likewise
read exactly three complete pages once and froze [review.md](review.md),
SHA-256 `f0dd1489b216b7fc57db66969f7a96d5bab344836b4c4d5d625ae6f6fa9974c6`
(`8b62f5`, exit0). Root read the complete review (`17a618`). No material source
disagreement was found. These are shared-source prior-informed AI readings,
not independent historical witnesses or engineering/human acceptance.

After both freezes the reviewer fully read the root notes and draft synthesis
(`84c83b`, exit0), hash check `75e5ae` confirming frozen notes unchanged.
Reviewed draft SHA-256:
`198b1cf116ea71b0a93d920e3f40cbeebc5b4622d4a532d91cd18639ade5c6e0`.
No material correction was found; derivative checking was outside that text
review. A draft punctuation artifact was corrected before this critique;
it was not a frozen source or note change.

## Declared figure addition and new rendering

The initial text directly references Figures6-1/6-2/6-3. Only after the first
readings froze and their comparison completed did root save the prospective
[figure supplement](FIGURE-SUPPLEMENT.md), SHA-256
`674e9bf12918b1d64e48630802804d8362951acffe1875cf4f26679c7f8cdc8d`
(`c76919`, exit0,14:53:16 UTC). It adds exactly physical62-64, preserving the
initial three-page scope rather than claiming the figures were already read.

Root inspected the prior rendering implementation/configuration (`90bfa3`)
but did not rerun its historical writing script. A fresh temporary fontconfig
uses the same system font directories and a temporary cache, avoiding writes
to the main repository. Saved [configuration](figure-render/fonts.conf) SHA-256:
`71464029ed6cc6dcca2c8daf2dc6e5f60516ea3645d71a4e4f9b08b32dc4b61f`.
Its cache path is temporary, not an artifact destination or evidence source.

Actual new rendering command:

```sh
env FONTCONFIG_FILE=/private/tmp/wtc7-oem-figures.aVe622/fonts.conf FONTCONFIG_PATH=/private/tmp/wtc7-oem-figures.aVe622 /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 62 -l 64 -scale-to 2200 -png /Users/admin/docs/911/research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/sources/ncstar-1-1j-attempt02.pdf /private/tmp/wtc7-oem-figures.aVe622/physical
```

Version check reported Poppler26.05.0. Original handle25564 was polled to
terminal exit0 (`aafb52`); no renderer warnings or retries. Hash/header check
`7d1696`, exit0, confirmed all three1700x2200 outputs. Approved no-overwrite
preservation into figure-render completed (`968c4d`, exit0).

| New physical-page render | SHA-256 |
| --- | --- |
| physical-62.png | bd558d4b49cf52bb7b9e41b4384308032136d7a842a446dd5ce38c0ee6d6a9ab |
| physical-63.png | 2f66674ad64d43a9bda0cd2fd85b4c157fba815390a23f50a52d293cb6c1510f |
| physical-64.png | 29c31d34e7e2a6eb98440a4432bf2bc35bff8f2d9dccc9106fe48fd047116f55 |

Root viewed all three complete pages once, no repeats or other transformations,
and froze [supplement notes](root-figure-observations.md) before receiving peer
findings, SHA-256 `cc602d9da3ee0ca80fcc70f81f9c23c7dad4db7036a85cca088d99851809dd4f`
(`eede83`, exit0). All three expected figures occur on pages62-63; page64 is
explicitly intentionally blank and is retained, not replaced by a more useful
unselected page. No dimensions or topology were computed from the schematics.

The separate reader checked all three image pins (`b0418e`, exit0), viewed
all three complete pages once, and froze [figure-review.md](figure-review.md)
before receiving root's supplement (`5e9425`, exit0), SHA-256
`0349d4dbf7609a92defbaad3f0b118093a3c06d361ee34f0047efa464051f669`.
Root read the entire supplement review (`f025fa`, exit0). Subsequent peer
reading of root's supplement (`c29590`) and hash check (`728790`), both exit0,
found no material disagreement and retained both frozen records unchanged.
There were twelve complete first-page displays across both stages/readers,
zero repeats; they remain six shared primary pages, not twelve sources.

The [fresh derivative check](figure-derivative-check.md) ran one independent
three-page render in a separate temporary directory, terminal exit0 and no
warnings. All three outputs match saved bytes/hashes. Its font configuration
differs only in the temporary cache path; that expected diff exit1 is recorded,
not a failure silently converted into a pass. Root read the entire receipt
(`15102d`, exit0), SHA-256
`b142ac0e54129772554f44d8a6002f464b870ab4be2159340660405ae1c35446`.
No old renderer or provenance receipt was overwritten.

No source or legal promotion, engine activation, human acceptance, outside
feedback payload, stage, commit or push. Generic source-role/component/version
issues remain deduplicated under SFB-005; archived feedback routing is unchanged.

## Final combined review

The reviewer read the complete combined six-page synthesis (`15e568`, exit0)
and checked its hash (`45d508`, exit0). No material correction was found;
figure coverage, exact-match limits and the original-record next test were
retained. This was text-only critique with no additional source views or
independent certification of the separate derivative receipt. Root had already
read both verification receipts. Final reviewed report SHA-256:
`f7f05726895ed35f087d3604fdeb9797cb6d863ef1661915338b5cf3fdac95ba`
(also checked by root `530a98`, exit0, after original handle48470 completed).

Current STATUS and research navigation mark both the text comparison and
figure supplement complete without rewriting earlier frozen source findings.
The next action is a bounded inventory check for original OEM drawings and
submittal dispositions, not further inference from the report diagrams.
No overall-goal completion is claimed.

Final stdout-only integrity/navigation check with `python3 -B -` completed
(`5ab9ed`, exit0; original handle7422 polled without restart). It checked13
unit pins (two declarations, four readings, two verification notes, final
report, font configuration and three new images); the main PDF and old receipt
pins; all three old original/reproduction image pairs; the new images' PNG
headers/dimensions and exact output directory membership; ten unit Markdown
files for final newlines/trailing whitespace; and22 local links. No historical
or physical claim is established by those file checks.

`git diff --check -- research/README.md research/sherlock-wtc7-investigation/STATUS.md research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/enclosure-framing/oem-comparison`
and the following worktree status check completed (`51eb6e`, exit0, original
handle56645). The untracked Markdown checks are the separate Python checks,
not implicitly covered by Git diff. Existing unrelated research WIP remains.
No stage, commit, push or main/legal edit occurred. A preliminary diff/path
check also completed (`a729f3`, exit0); it was not the final content check.
