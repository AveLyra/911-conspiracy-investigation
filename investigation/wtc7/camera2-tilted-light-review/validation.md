# Native appearance review: execution and verification

2026-09-26. Research-only closure of the fixed 32-image unit. No causal
inference, human acceptance or whole-investigation completion.

## Execution boundary

The September24 preparation stopped after the protocol/root header and initial
metadata-check attempts because of a reported usage interruption. The tasks
were resumed September26 after their terminal errors were confirmed. No image
block was counted as completed during the interruption. The protocol was
unchanged, hash `489c08bf5217b08850b23ffd63a1457b3643742bc02bf18b83cfe1f67717ecc7`.

Root and Reader A each viewed exactly the 32 prescribed complete native PNGs
once at original detail in nine blocks. Each saved a block before opening the
next; both full records froze before substantive exchange. No retries, extra
views, crop/resize/enhancement, new video decode or measurements occurred.
The views are qualitative, prior-informed and share sources/tools/model
dependencies. Whole-image readability does not establish fine-feature
resolution or calibrated detection sensitivity.

Root's early comparisons to already-viewed blocks were not exclusively
within-block notes; [critical comparison](comparison-review.md) preserves
this minor process qualification. No unseen future images or pre-freeze peer
descriptions were used. Frozen descriptions were not rewritten to harmonize
the readers. Reader A's uncertainty distinguishing 313/358 from faint
neighbors remains explicit; retention does not prove event continuation.

## Frozen identities

| Record | SHA-256 |
|---|---|
| Root observations | `2a2151dbedb8edb6bb765ad365c8254a886be8a5c502e8b338fcfb836902a301` |
| Reader A observations | `d13ca4ebc155373cd95a016f07b0edf2c5ec23e893a201d97d9c6944d76adbff` |
| Source check | `c70eb26547c1adf9688bb1e17d595263251e59ce876548c74f69384d2ccda921` |
| Admission JSON | `a5707111d1aa5d4d62394d6bc44ae909e502536d19226c1a14548300254b6be7` |
| All-row comparison | `7daf0ef2ee4fcb099e894c8ad1179aca6532a3b48e22542a86c5f919eba88ae2` |

The independently checked [source admission](source-check.md) contains its
full executable stdout-only command and all per-frame/pixel/clock identities.
It passed 32 native PNG contracts, six shortlist associations and 61 unchanged
checked input files, Python3.12.14/Pillow12.3.0, no warnings. It did not rerun
the earlier 17,136 comparisons or validate every one of the 476 native files.
Two failed schema assertions (SHA strings mistaken for identity dictionaries)
are retained there; neither was a source mismatch or counted as a pass.

Root separately checked the 32 native byte/pixel/geometry contracts and six
shortlists before views; the fresh check covered 37 pins including protocol.
The final read-only metadata check below ran after both freezes and before
navigation changes. It checked five record pins, all 61 admission input
identities, both ordered 32-row records/nine blocks and six exact shortlists.
Actual output: `PASS: 5 frozen documents, 61 unchanged admitted inputs, both
ordered 32-row records / 9 blocks, 6 exact shortlist maps; no new viewing or
pixel measurement`. Exit0. It used the bundled Python3.12.14 runtime.

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B - <<'PY'
import hashlib,json,re
from pathlib import Path
b=Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation')
u=b/'camera2-tilted-light-review'
pins={'PROTOCOL.md':'489c08bf5217b08850b23ffd63a1457b3643742bc02bf18b83cfe1f67717ecc7','root-observations.md':'2a2151dbedb8edb6bb765ad365c8254a886be8a5c502e8b338fcfb836902a301','reader-a-observations.md':'d13ca4ebc155373cd95a016f07b0edf2c5ec23e893a201d97d9c6944d76adbff','source-check.md':'c70eb26547c1adf9688bb1e17d595263251e59ce876548c74f69384d2ccda921','admission.json':'a5707111d1aa5d4d62394d6bc44ae909e502536d19226c1a14548300254b6be7'}
for p,h in pins.items(): assert hashlib.sha256((u/p).read_bytes()).hexdigest()==h,p
ad=json.loads((u/'admission.json').read_text())
for p,i in ad['inputs'].items():
 data=Path(p).read_bytes(); assert len(data)==i['bytes'] and hashlib.sha256(data).hexdigest()==i['sha256'],p
expected=[('Camera2',i) for i in [6924,6925,6926]]+[('Tilted',i) for i in range(306,322)]+[('Camera2',i) for i in [6969,6970,6971]]+[('Tilted',i) for i in range(352,362)]
a=(u/'reader-a-observations.md').read_text(); r=(u/'root-observations.md').read_text()
keys=[(f,int(i)) for f,i in re.findall(r'^### (Camera2|Tilted) (\d+)\s*$',a,re.M)]
assert keys==expected and len(set(keys))==32
assert [int(x) for x in re.findall(r'^\| (\d+) \|',r,re.M)]==[i for f,i in expected]
assert len(re.findall(r'^## Block \d+',r,re.M))==len(re.findall(r'^## Block \d+',a,re.M))==9
expected_sets={'6924':list(range(306,315)),'6925':list(range(306,319)),'6926':list(range(308,317))+list(range(318,322)),'6969':list(range(352,359)),'6970':list(range(352,361)),'6971':list(range(355,362))}
assert ad['per_query_shortlists']==expected_sets
assert len(ad['frames'])==32
print('PASS: 5 frozen documents, 61 unchanged admitted inputs, both ordered 32-row records / 9 blocks, 6 exact shortlist maps; no new viewing or pixel measurement')
print('admitted inputs',len(ad['inputs']))
PY
```

The admission includes then-current navigation/control files. Later intentional
STATUS navigation edits will change that historical snapshot's identity;
do not silently repin it or call a resulting navigation-only mismatch a source
corruption. Frozen input/image/observation pins remain the current source checks.

The independent text reviewer checked all32 row identities/path associations
and all six exact query memberships. It did not independently replay view/save
chronology or inspect pixels. The complete report preserves the key limit:
every local query also admits the conspicuous/patterned alternative, so a
unique exposure is not established by favorable appearance pairs.

The reviewer subsequently read the complete report at SHA-256
`53f8c8955c493ef503ff4bae0cfe36eab4d1da27931917aa9858fbd500d7f672`
and found no material synthesis correction needed, while preserving its
text-only/reader-reported-process limit. Root's final metadata/Markdown check
passed nine frozen pins across this unit and the comparison design, all60
unchanged non-STATUS admission inputs, eight Markdown files and25 local links.
The one changed snapshot member was the deliberately updated STATUS, not a
source. Scoped `git diff --check` also exited0. These remain integrity and
reporting checks, not an empirical validation of physical-light origin.

## Preservation and actual status

Only this unit's working notes and research navigation changed. The numeric
target-join outputs and all sources remain unchanged. No source authentication,
actual-human review, physical source identification, accepted engine state,
external transfer, legal promotion, staging, commit or push occurred for this
unit. Worktree HEAD was freshly observed at
`2fab1389ba8529494dd206a948014cd41cbf97d2`, not the older summary's commit.
Main's unrelated changes and new correspondence were not investigated or edited.

The fixed source/appearance task is complete within its limits; the full goal,
human R1/curve gates and broader Luna reevaluation remain incomplete. Existing
generic feedback already covers source-copy dependence, ambiguity and typed
claims; no duplicate issue or archived-task transmission was added. The next
active independent work is the user's reviewed NIST/UAF comparison design,
not more fixed-window pixel inspection.
