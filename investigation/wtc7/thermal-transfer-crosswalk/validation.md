# Thermal-transfer crosswalk validation

2026-09-12. Research-only numerical/source verification, not historical solver
execution, physical validation or a completed investigation. The final
[report](report.md) incorporates the independent comparison, selected-source
supplement and inference review. All source/canonical/legal files remain
unchanged. No source instruction, solver, Faraday bridge or external transfer
was executed.

## Executed checks

| Check | Actual outcome and scope |
|---|---|
| Root full source scans, run01/run02 | Eight synthetic groups passed before each scan. Both terminal PASS; all result objects exactly equal. Elapsed54.817492/53.127918s; peak RSS88,260,608/93,323,264bytes. Only command/time/memory receipt fields differ. |
| Original independent scan and comparison |21 controls;25,365 full-body receipts agree, including all read-byte hashes and25,137 operation locators. Recognized counts agree. Independence and explicit schema differences are recorded in[verification-review.md](verification-review.md). |
| Root repeat of comparison |`independent-comparison02.json` terminal PASS,21 controls,0.635992s. It reuses frozen results, not a third source scan. |
| Targeted producer details02 |Six controls;1,864 bodies/469,040,000bytes checked against root source hashes, all selected locators joined. Terminal PASS,40.530193s,161,447,936-byte peak RSS. |
| Producer details03, additive BOM test |Seven controls; same selected bodies; terminal PASS,41.105629s,175,751,168-byte peak RSS. Zero exact initial UTF-8 BOMs. Removing the added BOM fields leaves details02's records exactly unchanged. |
| Independent post-schema supplement02 |18 controls; all1,864 selected-body hashes/EOF/CRC receipts and36,923 target segments;318,922 comparison operations with no failures. All25,137 argument recipes/candidate fields and1,549 differing token buckets reconstructed.2.788010s,398,409,728-byte peak RSS. |
| Root source rerun of supplement |`independent-supplement03.json` terminal PASS with18 controls;2.805673s,397,492,224-byte peak RSS. Its complete result object exactly equals supplement02. This is confirmatory reproduction using the independent implementation, not another blinded implementation. |
| Independent inference/code review |Eight pure synthetic cases reproduced assignment/format/numeric-prefix limitations. Final report/detail review found no material causal or source-role overstatement; requested final supplement qualification was incorporated. No raw source rescan by this reviewer. |

The independent supplement verifies **details02**, and separately checks BOM
absence. It does not certify every field or every code path of details03.
Root's exact preserved-field comparison joins those producer versions; the
entire later producer is not relabeled independently verified.

The source-reconciled difference inventory covers five assignment-prefix
segments, nine MV-prefix segments and1,536 first-line ASCII segments. These
account for1,549 differing per-file hash buckets; buckets are not rows.
371 remaining identifier occurrences across14 token hashes and1,536 first
lines across24 segment hashes remain semantically unresolved. Thirty syntactic
assignments are not evaluated. The three original comment-counter differences
have distinct declared definitions; individual empty-tail comments were not
newly localized by the supplement. No full lexer equivalence is claimed.

## Retained failures and limitations

- The initial targeted scanner used a costly repeated inventory traversal.
  It was deliberately interrupted via its live handle; session87729 returned
  terminal exit130. It did not create details01.json. Its code is preserved
  as`crosswalk_details-slow01.py`, SHA-256
  `8031a6eef243037c4955ee5b8b8ac1779c0a2df3d16a7c3c25dfdb5bd5712f4e`.
  No completed source result or durable automatic failure receipt is claimed
  for that interrupted attempt. An indexed lookup plus an equivalence control
  produced details02; interrupt handling was added for later receipts.
- The independent supplement first refused a changed protocol pin before
  source-body reads. Its failure receipt is preserved as
  `independent-supplement01.json`, SHA-256
  `03160116199bf047fae695a1169a08ff22aff2fb22c130f900529b512caaec34`.
  After the amended protocol was fully read and repinned, supplement02 passed.
- The pre-BOM protocol was reconstructed from the unchanged prefix and its
  SHA matched the hash saved by details02 exactly. It is now retained as
  `DETAIL-PROTOCOL-before-bom.md`; this recovery is not represented as a
  separately saved preregistration made before the original scan.
- Root's frozen lexer has synthetic format/comment and unknown-token limits.
  No format records occurred in its historical result, but that does not make
  it a general APDL parser. Numeric-prefix classification is not full numeric
  validation. Quoted/dynamic construction and runtime execution remain outside
  this audit. The original programs/results were not silently patched.
- One328-byte all-NUL member remains excluded from semantic interpretation;
  all272 PNG bodies remain excluded. A zero literal-marker count does not
  prove exporter absence. Memory gates measure peak RSS after processing,
  rather than enforce per-allocation limits at the operating-system level.
- Publicly reachable modern command documentation exposed confidentiality/
  proprietary markings. Further use/export remains held. The final argument
  relies on unmarked NIST primary reports and minimized lexical observations,
  not those pages as approved historical semantic authority.

## Source-page checks

Root inspected complete NCSTAR1-9 PDF pages455/457 and523/524, including headings
and the footnote on524; and NCSTAR1-5G pages120/121/168. This confirms the
two-thermal-data-set statement, temporal-interpolation context, distinct
damage handoff and scope of the tower predecessor. It does not prove a
historical software implementation. The separate[method-source review](method-source-review.md)
records additional text/search coverage and source pins. The supporting
Prasad/Baum paper is background in that note, not newly claimed fully read by root.

The last two NCSTAR1-9 pages were rendered with bundled Poppler using
`-f 523 -l 524 -r 105 -png` and the existing project Fontconfig file; exit0,
no stderr. Their temporary filenames are`ncstar1-9-cross-523.png` and
`ncstar1-9-cross-524.png` under`/private/tmp/thermal-transfer-method.abc7tO/`.
Sources were not edited or re-exported.

## Core integrity pins

| Artifact | SHA-256 |
|---|---|
| Root protocol |`f79b1e78d01f7d4de1e994ed83d4f93b4a3a307714cdb53823be1e430ac0b34e`|
| Root scanner |`c6e69416a50a20a26ac15da70fdd3cc6fb56178c07b50a35c06b4b3fb6c3cd53`|
| run01 / run02 |`4754a59f0628a3ed91e913ce9aa5215254a4e476dcd17d9ee32e964eda2f8117` / `9ed79a923d0d15717fd687bd698ecd8d9b6f3a0b00b36b17834b9515c1995310`|
| Original / amended detail protocol |`1886f5a4ab9cd93c11d95696d863498dfc39cf9760f78801ee17e22efb082387` / `1ff4718d1b5dfb1eee7e3a313dfc49a4ec3ffb5ce5a2cb3666fdebb8d7fa2f11`|
| details02 / details03 |`4072b415f7197a7c1bf9b4da8bc820d6dd5ae9e6f08422d823ffd0b4bb815f64` / `a9d15ec021e306c2f9b9ee89422c459ad0b14439d35c8d4f207481ed094b7fdf`|
| Final detail scanner |`a097aa7eb31fcab07ed57ec0dda123bcaae473e35698eca1804f74dd2d8b99e6`|
| Root comparison repeat |`c622aabec66a54b0805e7e7c9382927f524fd21b00f27a1b2e4c6794844d3719`|
| Independent supplement code |`70a67f093a7168ea8c11beb950233ea868ccbd622addf1f7b041d1a7be918df4`|
| supplement02 / root repeat03 |`6ba520481f1f52e70124d451baa637dab3c7b1f2f2ba8f0f19b786f7e6b6693c` / `d3d99312174d764daf59f2fbb6696d559c08068ccd79453af2b3e480aabbad65`|

Receipts pin runtime/commands and dependency versions. Bundled Python3.12.14
was used; no new package or solver was installed. Repeat commands with unused
output names are documented in both independent reviews. Existing-output
refusal and protocol/source pins must not be bypassed to obtain a new pass.

The repository's read-only strict record validator passed for headers,
issue/fact links and citation tags. It does not validate engineering results.
Final local syntax, JSON, links, whitespace and artifact-pin checks are recorded
in the current investigation handoff after final report/navigation edits.
