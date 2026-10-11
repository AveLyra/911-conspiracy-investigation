# Released-model locators for the municipal structural question

October 5, 2026. Independent, prior-informed derivative review under [SCOPE.md](SCOPE.md). Research only; no new source decompression, primary-page view, mesh extraction, solver run, physical measurement, or cause ranking. This initial note was completed before reading the root's new synthesis or the third checker's receipt. Coordination supplied the municipal column labels and known parser provenance; the checker subsequently sent freeze/digest metadata, not its substantive table, before this note froze. This is separately implemented checking, not blinded discovery or expert acceptance.

## Answer

There is a **positive model-side anchor**: each of municipal labels **70, 71, 73 and 74** has an explicit, unique diagnostic-label → part-set → part → section/material association in accepted `run06`. The association is not inferred from `PID = 100 + column number`, even though those numbers happen to coincide here. Together with existing controls 44, 76 and 79, these are useful starting points for a drawing/model coordinate crosswalk.

There is **not yet an exact municipal altered-member or physical-floor join**. The accepted derivative fields do not establish which modeled beams, slab elements, connections or elevations correspond to S-S-1, SKS-S-2, either S-TS-7 revision, or the distinct seventh-floor CO23 work. This is a missing registration/member-identification step, not evidence that all model geometry is unavailable or that the alterations were omitted. It does not require installation to be proved before a conditional design/model comparison.

## Exact successful joins

Inputs: [member-map.json](../model-member-map/run06/member-map.json) (`M`), its [receipt](../model-member-map/run06/receipt.json) (`MR`), and [material crosswalk run01.json](../material-run-crosswalk/run01.json) (`V`). No producer helper was imported.

Selection was exactly `M.column_diagnostics[].column_number in {44,70,71,73,74,76,79}`. The source label is parsed in [map_members.py](../model-member-map/map_members.py), `metadata()` at lines 354–410: a full match of `Col(?:umn)?\s*0*(\d+)\s+X-Sect` in a `DATABASE_CROSS_SECTION_PLANE_ID` heading. That diagnostic's **actual** `psid` joins `SET_PART_LIST`; its actual `part_ids` then join the typed tables. Nonmatching headings remain unnumbered. The result writer at lines 501–516 aggregates the referenced parts, explicitly not the cutting-plane intersection.

All seven selected labels occur once; each set here contains one part and has `missing_part_ids=[]`. All selected part, section and material joins are present. Source for every row below is **SRC-121, `wtc7_global_8a_no-conn-matl.k.gz`**, effective ID offset zero. Source line numbers are preserved derivative locators, not source lines newly reread in this task.

| Column label | Diagnostic keyword line | Part-set keyword line | PSID / explicit PID / SID | PART keyword / card lines | MID | Shell records |
|---|---:|---:|---:|---:|---:|---:|
| 44 | 369 | 366 | 144 / 144 / 144 | 3070 / 3072 | 100 | 624 |
| 70 | 551 | 548 | 170 / 170 / 170 | 3408 / 3410 | 99 | 800 |
| 71 | 558 | 555 | 171 / 171 / 171 | 3421 / 3423 | 99 | 584 |
| 73 | 572 | 569 | 173 / 173 / 173 | 3447 / 3449 | 99 | 952 |
| 74 | 579 | 576 | 174 / 174 / 174 | 3460 / 3462 | 99 | 592 |
| 76 | 593 | 590 | 176 / 176 / 176 | 3486 / 3488 | 99 | 944 |
| 79 | 614 | 611 | 179 / 179 / 179 | 3525 / 3527 | 99 | 952 |

These source-authored column labels associate **parts**, not every element of a full-height physical column or the altered adjacent beams. MID 99 and MID 100 resolve in `V.material_id_index` to `MAT_ELASTIC_VISCOPLASTIC_THERMAL`, SRC-121 keyword lines 2486 and 2496 respectively. They are **not missing definitions**. Their complete numerical card bodies are not among this crosswalk's 20 `selected_materials`; this note makes no material-capacity finding. The master row numeric values are `[pid,pid,mid,0,pid,0,0,0]` for these parts.

### Available numeric geometry, with its coordinate ceiling

Each bound below is the stored `member_geometry_bounds`, verified equal to that part's `geometry_bounds`. It covers the **entire referenced part set**, not only its diagnostic plane, not a selected physical floor, and not a demonstrated full-height column. These are model-number coordinates; no length unit, compass orientation or physical-floor conversion is assigned here.

| Label | Model X min…max | Model Y min…max | Model Z min…max |
|---|---|---|---|
| 44 | 17.13738…17.68602 | 15.85341…16.30299 | −70.50379…−43.6118 |
| 70 | −17.55013…−17.09547 | −0.28448…0.28448 | −71.1708…−43.6118 |
| 71 | −17.54759…−17.09801 | −9.659619…−9.11098 | −71.1708…−43.6118 |
| 73 | −8.76173…−8.30707 | −0.28448…0.28448 | −71.1708…−43.6118 |
| 74 | −8.76173…−8.30707 | −9.66978…−9.10082 | −71.1708…−43.6118 |
| 76 | −0.22733…0.22733 | −0.28448…0.28448 | −71.1708…−43.6118 |
| 79 | 13.13262…13.77258 | 2.408667…3.077733 | −71.1708…−43.6118 |

All seven diagnostic first cards are `[psid,0,0,-64.9,0,0,90.4748]`; the recorded second cards are null-valued. **−64.9 is not hereby the first or seventh floor.** The included outside geometry has a checked identity coordinate transform and +1000 PID/MID/SID namespace offsets; identity here means include-to-master, not model-to-building registration. It does not authenticate a physical coordinate convention.

## Fixed municipal target dispositions

| Target | Available association | Missing or unresolved link / contrary interpretation |
|---|---|---|
| First-floor S-S-1 and SKS-S-2 notched-beam/restoration work | Held municipal design evidence as scoped; four named column labels now have the explicit model anchors above | No accepted target-beam identifiers, elevation-to-Z rule or exact connection/element correspondence established. The tank/slab-opening columns may locate a related region without identifying these altered beams; do not silently equate the two operations. |
| October and December S-TS-7 slab/opening revisions | Revision-specific municipal drawing leads remain distinct | No exact slab-element region, reinforcement representation or revision-specific model implementation established. A column part's bounds are not the floor slab mesh. Drawing differences alone do not establish model omission. |
| CO23 seventh-floor work | A separate municipal scope, not the first-floor alteration | The main inventory contains literal `7th floor mass1` and `7th floor mass2` part titles in `discrete_mass.k.gz`. These are mass-component leads, **not a demonstrated CO23 structural-member join**; no title-order→PID or CO23→mass inference was made. |
| CO40 | Preserved as an unjoined separate record in the fixed scope | No substitution of CO40 for S-TS-7 or CO23, and no model-implementation finding. |

The failure here is to establish the target correspondence with the inspected accepted fields, not an exhaustive no-match claim about every raw model title, drawing package or later production. Pending original structural packages are a separate access/reading boundary, not failed downloads or proof that the source does not exist.

## What the current model records do and do not supply

- The exact query population contains **83 diagnostics** (labels 1–81 and two unnumbered entries), **392 used-part rows**, **459 part references/definitions**, and **379 effective material IDs**. Keys were unique at their actual grains. All seven requested labels were present; section/material IDs and element-family counts agreed across `M` and `V`.
- `M.parts[].elements` supplies per-family counts, not an all-element-ID/connectivity table for each of these new target regions. Full geometry is not absent merely because this accepted output is aggregated. Existing selected-element exports and the C79 restraint/contact work are narrower populations.
- The [C79 released mapping review](../c79-member-detail-crosswalk/released-mapping-review.md) already documents actual C79 shell/node locators, the explicit 44/76/79 controls and separate connection/contact studies. Those cannot be reassigned to first-floor alterations or CO23. In particular, **beam PIDs 73/74 are not Column labels 73/74**. Existing local connection axes and global-model coordinates are distinct frames.
- The [original-sheet review](../c79-original-sheet-review/report.md), [local holdings review](../c79-original-sheet-review/local-holdings-review.md) and [facade locator](../facade-drawing-locator/report.md) preserve specific original-design/package leads and their limited inventory coverage. They do not presently provide the municipal beam/floor mapping. No pending PDF/TIFF/package was opened here; no new archive-completeness claim is made.
- The [main released-input audit](/Users/admin/docs/911/research/sherlock-wtc7-investigation/lsdyna-supplement-content-audit/report.md) describes a global LS-DYNA input assembly, separate from the reported 16-story ANSYS work. Its earlier “SI-like” units inference is not a verified physical registration. The [structural-chain source audit](/Users/admin/docs/911/research/sherlock-wtc7-investigation/structural-chain-source-audit.md), SC06, attributes fixed column ends below second-floor framing and nondeformable substation treatment to NIST. That creates a specific lower-region idealization question, not an automatic conclusion that every first-floor alteration is outside the global model.
- Existing parser/independent-validation histories remain in [member-map validation](../model-member-map/validation.md) and [material validation](../material-run-crosswalk/validation.md). This task used corrected **run06**, not its failed predecessors; it did not rerun those large source-level validations. Run lineage/restarts and historical installation remain distinct from present static input correspondence.

## Highest-value next discriminator

Prospectively bound **drawing-to-model registration and target-member identification** around the four named anchors, retaining controls 44/76/79. First determine which held original/detail drawing explicitly identifies the first-floor target beams, floor/elevation convention and the relevant column/grid reference; keep CO23's seventh-floor members in a separate lane. Require a sourced scale/origin/axis/floor relation and a second independent geometric/elevation check before selecting a target element region. A bounding-box centre is not automatically a column centreline, and a repeated grid spacing is not enough to settle orientation or floor. Do not choose a Z band because it yields the expected result.

If the held details supply that registration, a separately declared **local** member/element inventory can test model representation of the notch/restoration, slab opening and relevant connection/section assumptions. If they do not, return the exact missing dimension/elevation/member sheet or registration record; do not launch an undirected archive queue. Both outcomes matter: a positive representation weakens a specific omission claim; an authenticated mismatch supports a bounded model-fidelity question but not its dynamic importance, installed state or historical cause. Conditional design/model comparison is useful before installation is proved; sensitivity/capacity calculation requires its own later scope.

## Reproducible derivative checks and actual coverage

Ran read-only `python3` JSON queries; no imports of the producer, native keyword reads or output files. The substantive query completed as **`b03613`, exit 0** after session 69025. A second bounds-equality and pin query completed **`ca7622`, exit 0** after session 72694. `MR.status` was `complete`, scope `local_input_joins_no_solver_or_causal_finding`; `sha256(M)==MR.result_sha256` passed. The following is a compact replay of the checked selection/join contract, run from the research base; it deliberately does not convert physical coordinates:

```python
from pathlib import Path
import hashlib, json
paths = [Path('model-member-map/run06/member-map.json'),
         Path('model-member-map/run06/receipt.json'),
         Path('material-run-crosswalk/run01.json')]
m, r, v = [json.loads(p.read_text()) for p in paths]
assert hashlib.sha256(paths[0].read_bytes()).hexdigest() == r['result_sha256']
for rows, key in [(m['column_diagnostics'], lambda x:(x['source'],x['plane_id'])),
                  (m['parts'], lambda x:x['pid']),
                  (v['all_part_references'], lambda x:x['pid']),
                  (v['used_parts'], lambda x:x['pid']),
                  (v['material_id_index'], lambda x:x['effective_id'])]:
    keys = [key(x) for x in rows]
    assert len(keys) == len(set(keys))
for n in [44,70,71,73,74,76,79]:
    ds = [d for d in m['column_diagnostics'] if d['column_number'] == n]
    assert len(ds) == 1
    d = ds[0]
    assert not d['missing_part_ids'] and len(d['partset']['part_ids']) == 1
    for pid in d['partset']['part_ids']:
        ps = [p for p in m['parts'] if p['pid'] == pid]
        refs = [p for p in v['all_part_references'] if p['pid'] == pid]
        used = [p for p in v['used_parts'] if p['pid'] == pid]
        assert len(ps) == len(refs) == len(used) == 1
        p, a, u = ps[0], refs[0], used[0]
        assert p['definition']['material_id'] == a['mid'] == u['mid']
        assert p['definition']['section_id'] == a['sid'] == u['sid']
        assert p['elements'] == u['elements']
        assert p['geometry_bounds'] == d['member_geometry_bounds']
        mats = [t for t in v['material_id_index'] if t['effective_id'] == a['mid']]
        assert len(mats) == 1
        print(n, d, p, a, u, mats)
for p in paths:
    print(p, hashlib.sha256(p.read_bytes()).hexdigest())
```

Full narrative reads: member-map/material-crosswalk reports and validation records; C79 member report, released mapping and validation; original-sheet report and local-holdings review; facade locator; main released-input report and structural-chain source audit. Code reading was restricted to relevant metadata/bounds branches, not a fresh full-code audit. Numeric/schema queries covered the three pinned outputs above plus selected technical fields of the main inventory. The two September 27 alteration/structural-condition followups received **targeted text-locator checks only**, not new complete primary reviews; they identified different alteration packages and supplied no new target correspondence. Main controls/charter were verified at unchanged previously read pins; all applicable skills were read. No confidential/contact/raw-header content was output.

Read receipts: `f4219b`, `921992`, `ca1ac0`, `64be45`, `bcf269`, `2c13ff`, `53bd79`, all exit 0. Combined-output truncation in the C79 mapping and structural-chain reads was recovered by narrow rereads (`64be45` and `974b1c`/`ca7622`), not silently treated as full. Scope reread `a6c747`, exit 0. Schema queries `2995f1`, `b4d59c`, `388296`, exit 0. No assertion of new source-level validation or independent historical witness follows from these derivative checks.

### Local input pins (SHA-256)

Paths below are relative to the research base unless prefixed `MAIN/`, which means `/Users/admin/docs/911/research/sherlock-wtc7-investigation/`. Pins establish present byte identity, not authenticity of a historical model run.

| Input | SHA-256 |
|---|---|
| municipal-model-crosswalk-2026-10-05/SCOPE.md | `590e33bb59e197f637561a6140dec1e4434c45d163c918c8e9a2c8a03f375baa` |
| model-member-map/run06/member-map.json | `eae21a0ac384b8b6f23e58eb3f56f439f577a9b954fafb757be189fd7f0a4f8e` |
| model-member-map/run06/receipt.json | `4ed99830a61606e18ac0720102354c3450ecffc61fc7743d35f9b62b9750529d` |
| material-run-crosswalk/run01.json | `b69c12ec0668c9bdf5f5ea59dbf483d2a959de7bd477c172efe69c2f03e33594` |
| model-member-map/map_members.py | `f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b` |
| model-member-map/report.md | `68a1978db06ba10461c39e4c0074480fc4fef440f8bbda9d866113e2d5a8e4e5` |
| model-member-map/validation.md | `390122d5a2205109af3c3961a1ebd92526760bbb866c0972ee79f12f7e52b3c9` |
| material-run-crosswalk/report.md | `a9afca6aa6221db2f96bb0d2720cadb7094532105f5e86661fb591b9315babcf` |
| material-run-crosswalk/validation.md | `c3a27a29ca094319dad2f2ea7520b9f83404528f943d4a0b273a27e0411d5fa9` |
| c79-member-detail-crosswalk/report.md | `54326664ec394421ae7894c3a634c417a03bddbd8facdde15a07800a6d0d000a` |
| c79-member-detail-crosswalk/released-mapping-review.md | `a1034c44f9e411d727a61f7e6e943064c601320b7ac7c7641731c7df27a60630` |
| c79-original-sheet-review/report.md | `1f7805337632f0f3b03b399cb64dd54d27a3d48bce3f5ba69dc2caf876bbb53c` |
| c79-original-sheet-review/local-holdings-review.md | `39f08e5f7157dcbef751b80b5e948735b60f3440dd35d7dddd5362e2d0f28295` |
| facade-drawing-locator/report.md | `fb90cea12178a52a67918c4a6275e44349bd917ae2fd00158922a3c5ba5c24f0` |
| MAIN/lsdyna-supplement-content-audit/report.md | `1d0b1d3031d7ee5b8baa87459c166fb5460954cc96e864a45199a52365483f9e` |
| MAIN/lsdyna-supplement-content-audit/inventory.json | `391b13a37df24c9b2c987d0e1d03bf27513bd718fa3fecd168a95f614104dbf3` |
| MAIN/structural-chain-source-audit.md | `7ae495511780584a9c87d9ed9527ee593fae221e9c3a6b7a9927003007d2c06c` |

The derivative replay establishes only the stated static associations and boundaries. The broader investigation and separate human/expert/observation-matrix decisions remain open.
