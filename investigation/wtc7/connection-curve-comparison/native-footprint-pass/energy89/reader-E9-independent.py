"""Literal independent E9 reading; expansion never chooses RGB cells."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = {
    'PROTOCOL.md': '98edc562841efdbc3ffb7f25c813b507cf553142a972f5558680e7218f7e6e25',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    '../read_context.py': 'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    '../../NUMERICAL-PROTOCOL.md': 'e03c47c1945b9eb9fd0a040d757d5f5f66bf76791ced8944323d3c92d1120df3',
    '../../HUMAN-REVIEW-GATE.md': '5c739ea10b6fe51b719a10205cef52737ff74cc29d1431272dd5dfea90d92c71',
    'read_context.py': '377d4f41b990502ca87fc7d1b4b9b069eede0aa71f281c68cb5ae879d7196a2c',
    'context01.json': '0f7528e58a57f7244673a79d4fbfd77bdb9c8c6f277cb57b3686cb8bcff818c7',
    'context02.json': '0f7528e58a57f7244673a79d4fbfd77bdb9c8c6f277cb57b3686cb8bcff818c7',
    '../../native-strips01/Im7.jpg': '3509c0fb002d47d1cc9d1ae624377534c8b31bd9fea7fdadd380a7b5f4d4a09d',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    '/Users/admin/docs/911/AGENTS.md': '934437bfc0ddbe522cc73461819593706d12c0644cb306d263d9f1fe3914a857',
    '/Users/admin/docs/911/WORKFLOW.md': '17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a',
    '/Users/admin/docs/911/START-HERE.md': 'b291da2b9ab3f1a8e9e69ff5a5d930c689ff2d45a6b2ce06a521e76295fbd560',
    '/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md': '54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
}
# Inclusive x ranges and explicit manually selected row lists. These literal
# choices were made after viewing the full images and reading each raw column.
SOLID_RUNS = [[530,530,[49],[48,50]],[531,533,[48,49],[47,50]],[534,535,[48],[47,49]],[536,537,[47,48],[46]],[538,541,[47],[46,48]],[542,543,[46,47],[45,48]],[544,546,[46],[45,47]],[547,548,[46],[45]],[549,549,[45,46],[44]],[550,553,[45],[44,46]],[554,557,[44,45],[43]],[558,559,[44],[43,45]],[560,562,[44],[43,45]],[563,567,[43,44],[42,45]],[568,575,[43],[42,44]],[576,579,[42,43],[41,44]],[580,589,[42],[41,43]],[590,591,[41,42],[40,43]],[592,607,[41,42],[40,43]],[608,623,[41],[40,42]],[624,655,[41],[40,42]],[656,689,[41],[40,42]]]
DASH_RUNS = [[530,530,[52,53],[51,54],"d01"],[531,532,[52],[51,53],"d01"],[533,533,[],[52],"d01"],[535,535,[51],[50,52],"d02"],[536,537,[50,51],[52],"d02"],[538,538,[50,51],[49,52],"d02"],[539,541,[50],[49,51],"d02"],[542,542,[],[50],"d02"],[544,544,[],[49],"d03"],[545,546,[49],[48,50],"d03"],[547,549,[48,49],[50],"d03"],[550,550,[48],[47,49],"d03"],[551,551,[],[48,49],"d03"],[554,554,[48],[47,49],"d04"],[555,557,[47,48],[49],"d04"],[558,559,[47],[46,48],"d04"],[560,560,[],[47,48],"d04"],[563,569,[47],[46,48],"d05"],[570,570,[],[47],"d05"],[572,572,[],[47],"d06"],[573,578,[47],[46,48],"d06"],[579,579,[],[47],"d06"],[581,581,[],[47],"d07"],[582,587,[47],[46,48],"d07"],[588,588,[],[47,48],"d07"],[591,591,[47],[46,48],"d08"],[592,597,[47],[46,48],"d08"],[600,600,[],[47,48],"d09"],[601,606,[47],[46,48],"d09"],[607,607,[],[47,48],"d09"],[609,609,[],[47],"d10"],[610,615,[47],[46,48],"d10"],[616,616,[],[47],"d10"],[618,618,[],[47],"d11"],[619,623,[47],[46,48],"d11"],[624,625,[47],[46,48],"d11"],[628,634,[47],[46,48],"d12"],[637,637,[],[47,48],"d13"],[638,643,[47],[46,48],"d13"],[644,644,[],[47],"d13"],[646,646,[],[47],"d14"],[647,652,[47],[46,48],"d14"],[653,653,[],[47,48],"d14"],[656,662,[47],[46,48],"d15"],[665,665,[],[47,48],"d16"],[666,671,[47],[46,48],"d16"],[674,674,[],[47,48],"d17"],[675,680,[47],[46,48],"d17"],[681,681,[],[47],"d17"],[683,683,[],[47],"d18"],[684,689,[47],[46,48],"d18"]]
UNASSIGNED_RUNS = [[536,537,[],[49],"u-halo01"],[547,549,[],[47],"u-halo02"],[554,557,[],[46],"u-halo03"]]
RAW_BLOCKS = [{"first":528,"last":559,"tool_chunk_id":"890da8","exit_code":0,"original_token_count":3161},{"first":560,"last":591,"tool_chunk_id":"7fc94c","exit_code":0,"original_token_count":3055},{"first":592,"last":623,"tool_chunk_id":"ebb0b8","exit_code":0,"original_token_count":3141},{"first":624,"last":655,"tool_chunk_id":"03c35b","exit_code":0,"original_token_count":3142},{"first":656,"last":691,"tool_chunk_id":"f87161","exit_code":0,"original_token_count":3559}]
READING_COMPLETED_UTC = '2026-10-08T02:54:21+00:00'
TARGET = [530, 30, 690, 56]
CONTEXT = [528, 28, 692, 58]


def pin(path):
    value = path.read_bytes()
    return {'sha256': hashlib.sha256(value).hexdigest(), 'bytes': len(value)}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def boundary_flags(x, rows):
    result = []
    if rows:
        if x == 530:
            result.append('target_left')
        if x == 689:
            result.append('target_right')
        if 30 in rows:
            result.append('target_top')
        if 55 in rows:
            result.append('target_bottom')
    return result


def expand_runs(runs, default_id=None):
    expanded = {}
    for run in runs:
        first, last, core, fringe = run[:4]
        local = run[4] if len(run) == 5 else default_id
        require(type(first) is int and type(last) is int and 530 <= first <= last <= 689, 'literal x bounds')
        for x in range(first, last + 1):
            require(x not in expanded, 'overlapping literal runs')
            expanded[x] = (list(core), list(fringe), local)
    return expanded


def validate_rows(x, core, fringe):
    require(type(x) is int and 530 <= x <= 689, 'target column')
    for rows in (core, fringe):
        require(type(rows) is list and all(type(y) is int and 30 <= y <= 55 for y in rows), 'target row')
        require(rows == sorted(set(rows)), 'ordered unique rows')
    require(not set(core) & set(fringe), 'core/fringe disjoint')


def build():
    before = {name: pin(HERE / name) for name in PINS}
    require(all(before[name]['sha256'] == expected for name, expected in PINS.items()), 'frozen input pin')
    require((HERE / 'context01.json').read_bytes() == (HERE / 'context02.json').read_bytes(), 'context repeat bytes')
    solid = expand_runs(SOLID_RUNS, 'E9i-solid01')
    dash = expand_runs(DASH_RUNS)
    unknown = expand_runs(UNASSIGNED_RUNS)
    routes = {'solid': [], 'dash': []}
    bands = []
    for x in range(530, 690):
        uc, uf, local = unknown.get(x, ([], [], None))
        bid = 'E9i-' + local if local else None
        validate_rows(x, uc, uf)
        bands.append({
            'x': x, 'core': uc, 'fringe': uf,
            'status': 'identity_conflict' if uc or uf else 'no_attributable_cells',
            'fragment_id': bid, 'model': None,
            'boundary_flags': boundary_flags(x, uc + uf),
            'note': (
                'Pale interstitial purple material cannot be assigned uniquely to the nearby solid or dash edge. '
                'It is retained once without model identity; compression/background material is an alternative. '
                'The separately attributed bodies remain locally distinguishable.'
                if bid else
                'No separate unassigned cells selected in this inspected column. This is not proof of no hidden contribution.'
            ),
            'competing_identities': ['solid-edge material', 'dash-edge material', 'mixed or compression/background material'] if bid else [],
        })
        refs = [{'band_id': bid, 'x': x}] if bid else []
        for route, mapping in (('solid', solid), ('dash', dash)):
            core, fringe, fragment = mapping.get(x, ([], [], None))
            if route == 'dash' and fragment:
                fragment = 'E9i-' + fragment
            validate_rows(x, core, fringe)
            selected = core + fringe
            flags = boundary_flags(x, selected)
            if selected:
                status = 'boundary_truncated' if flags else 'identified_local_fragment' if core else 'fringe_only'
                note = (
                    'Purple local continuous stroke identified from complete-strip style and the confirmed composed-page legend, not height alone. '
                    'Only the explicit rows are attributed; any referenced interstitial material stays separate.'
                    if route == 'solid' else
                    'Purple local broken-body or tentative endpoint identified from observed dash structure and the confirmed legend. '
                    'This reader-local body ID does not join gaps. Fringe-only endpoint attribution is tentative and may include compression material.'
                )
                if flags:
                    note += ' Selected cells touch the target boundary; the crop edge is not a physical endpoint.'
            else:
                status = 'identity_conflict' if refs else 'no_attributable_cells'
                note = (
                    'No model-specific cells selected from the referenced unassigned material; empty attribution is not absence or zero support.'
                    if refs else
                    'No cells attributed to this route in this inspected target column. Very pale or hidden material remains possible; no gap is interpolated.'
                )
            routes[route].append({
                'x': x, 'core': core, 'fringe': fringe, 'status': status,
                'fragment_id': fragment, 'boundary_flags': flags, 'note': note,
                'unassigned_band_refs': refs,
            })
            require(not any(y in uc + uf for y in selected), 'no unassigned/model duplicate')
        a, b = routes['solid'][-1], routes['dash'][-1]
        require(not any(y in b['core'] + b['fringe'] for y in a['core'] + a['fringe']), 'no duplicated model attribution')
    for records in routes.values():
        require([row['x'] for row in records] == list(range(530, 690)), 'complete route order')
    require([row['x'] for row in bands] == list(range(530, 690)), 'complete band order')
    require([x for block in RAW_BLOCKS for x in range(block['first'], block['last'] + 1)] == list(range(528, 692)), 'complete raw read ranges')
    context = json.loads((HERE / 'context01.json').read_text())
    require(context['target_boxes']['E9'] == TARGET and context['context_boxes']['E9'] == CONTEXT, 'context identity')
    pixels = {(row['x'], row['y']): row['rgb'] for row in context['cells']['E9']}
    require(len(pixels) == len(context['cells']['E9']) == 4920, 'complete context count')
    require(set(pixels) == {(x, y) for x in range(528, 692) for y in range(28, 58)}, 'complete context coordinates')
    exact_white = []
    selected_count = 0
    # Diagnostic only: never changes the literal selections.
    for scope, records in list(routes.items()) + [('unassigned', bands)]:
        for row in records:
            for label in ('core', 'fringe'):
                for y in row[label]:
                    selected_count += 1
                    if pixels[row['x'], y] == [255, 255, 255]:
                        exact_white.append({'scope': scope, 'class': label, 'x': row['x'], 'y': y})
    after = {name: pin(HERE / name) for name in PINS}
    require(before == after, 'unchanged inputs')
    return {
        'pair': 'E9',
        'reader': 'quiet_mechanism_inference_review; separate prior-informed AI source reader',
        'status': 'frozen_manual_native_annotation_not_accepted_measurement',
        'reading_completed_utc': READING_COMPLETED_UTC,
        'freeze_time_note': 'Fixed reading-completion anchor, not a runtime timestamp or independent witness. File pins identify the freeze; repeats retain this anchor.',
        'target_box': TARGET, 'context_box': CONTEXT,
        'inputs': before, 'inputs_after': after, 'script_pin': pin(Path(__file__)),
        'literal_manual_transcription': {
            'solid_runs_inclusive': SOLID_RUNS, 'dash_runs_inclusive': DASH_RUNS,
            'unassigned_runs_inclusive': UNASSIGNED_RUNS,
            'unspecified_route_column': 'Explicit inspected no_attributable_cells unless a real referenced band requires identity_conflict.',
            'unspecified_unassigned_column': 'Explicit inspected empty band record, not a missing or uninspected column.',
        },
        'coverage': {
            'full_native_Im7_viewed': True, 'full_composed_page_viewed': True,
            'native_view_detail': 'Complete unchanged 745x92 Im7; original detail requested and returned.',
            'page_view_detail': 'Complete unchanged page-076.png; original detail requested and returned. Raw native context supplies the coordinate readings.',
            'view_receipt': 'functions image call with source-pin receipt e1c752; full Im7 and page displayed before raw-column reading.',
            'raw_blocks': RAW_BLOCKS, 'raw_rows_inclusive': [28, 57],
            'raw_context_columns': 164, 'raw_context_cells': 4920, 'all_blocks_untruncated': True,
            'exact_white_omission_rule': 'Only RGB255,255,255 omitted by frozen show. Omitted positions are exact white; every other context RGB value was displayed and read.',
            'target_columns': 160, 'model_route_records': 320, 'unassigned_band_records': 160,
            'uncompleted': 'E8 is assigned separately. E9 outside this target, earlier crossings, supported domains, physical ordinates, calibrated curve bounds and selected-curve human acceptance remain uncompleted.',
        },
        'identity_basis': (
            'Complete native strip shows a continuous purple trace and separated purple dash bodies. '
            'The composed-page legend names solid Spring and dashed Shell and purple nine bolts. '
            'Assignments are local style attributions, not inherited from height or an earlier crossing. '
            'Only pale interstitial material is unassigned in this reading; no whole-band double attribution is imposed.'
        ),
        'independence': (
            'Same-source, nonblind, prior-informed AI. Earlier inventory, one-band and finite-recovery method context are known. '
            'No current root E9 or other current E9 reading/score was opened before this freeze. '
            'Own earlier E5 expansion was inspected only as a schema/mechanical implementation reference. No human/expert participation claimed.'
        ),
        'limits': [
            'Core and fringe are subjective visible-ink attributions, not calibrated pre-raster containment bounds or a confidence interval.',
            'Tentative pale dash endpoints and halos can be compression/background material. Unselected pale material is not certified outside the mathematical curve.',
            'Unassigned cells are recorded once without model identity; neither one nor two hidden original contributions is established.',
            'A local fragment ID does not bridge a dash gap or identify a physical endpoint; earlier crossings and hidden overprint remain untested outside this local reading.',
            'Pin equality and exact-white diagnostics verify transcription constraints, not perceptual truth or model identity.',
            'No thresholds, detector, added algorithmic margin, interpolation, fitted trajectory, physical ordinate, support admission, curve metric, causal inference, human acceptance, legal promotion or source editing.',
        ],
        'pre_freeze_transcription_checks': {
            'all_target_records_expanded': True,
            'bounds_order_disjointness_and_flags': 'passed',
            'selected_cells_checked_for_exact_white': selected_count,
            'selected_exact_white_cells': exact_white,
            'manual_pre_export_resolution': 'Before any annotation export, nine pale interstitial cells at x536-537 y49, x547-549 y47 and x554-557 y46 were retained once as unassigned fringe. No RGB rule selected or redrew cells.',
            'post_export_corrections': [],
            'context_check_limit': 'Saved context coordinates, pins and repeat bytes checked here; fresh all-source-cell verification is a separate checker assignment, not claimed performed by this reader.',
        },
        'human_accepted': False, 'physical_support': None,
        'routes': routes, 'unassigned_bands': bands,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', choices=['reader-E9-independent.json', 'reader-E9-independent-repeat.json'])
    args = parser.parse_args()
    require(boundary_flags(530, []) == [], 'empty edge control')
    require(boundary_flags(530, [30, 55]) == ['target_left', 'target_top', 'target_bottom'], 'left/corner control')
    require(boundary_flags(689, [47]) == ['target_right'], 'right fringe control')
    require(boundary_flags(600, [47]) == [], 'interior control')
    result = build()
    checks = result['pre_freeze_transcription_checks']
    summary = {
        'route_records': 320, 'unassigned_records': 160,
        'selected_cells': checks['selected_cells_checked_for_exact_white'],
        'selected_exact_white_cells': checks['selected_exact_white_cells'],
        'route_status_counts': {k: dict(Counter(r['status'] for r in rows)) for k, rows in result['routes'].items()},
        'script_pin': result['script_pin'],
    }
    if args.check:
        print(json.dumps(summary, sort_keys=True))
        if checks['selected_exact_white_cells']:
            raise SystemExit(1)
        return
    require(args.output is not None, 'output required')
    require(not checks['selected_exact_white_cells'], 'Preserve and review transcription failures; never auto-remove.')
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
    with (HERE / args.output).open('xb') as stream:
        stream.write(payload)
    summary['output'] = args.output
    summary['output_pin'] = pin(HERE / args.output)
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()

