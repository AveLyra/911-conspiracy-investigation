"""Literal independent E5 annotation; mechanical expansion never selects RGB cells."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = {
    'PROTOCOL.md': 'be57860a830ab716498ba5d25733021c1c975da1b0427f50f64071af4eaf5f16',
    'IDENTITY-CLARIFICATION.md': 'c9d79b6d92a5cbc2f4747e027bce81ee5b1cbec0528b018b368f22fd2b01098b',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    'context01.json': '59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
    'context02.json': '59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
    'read_context.py': '67e6788059653ba5d1e3eb18302e46bbc4299149646a8fed1516416dd7d1fe22',
    '../../native-strips01/Im9.jpg': '3154e28ea82ca2f39c465a7bdfe367677216543df296cf918cbbd259248f8129',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'context-independent-check.json': 'd06d8bce8e58c0016582cd5e0dd52b13ad9daadd86ca21f71f26484305e9373b',
}
# Inclusive x ranges, explicit rows. Authored from every declared raw column.
# No threshold, RGB predicate, fitted trajectory, added margin, or gap bridge.
SOLID_RUNS = [[400,404,[],[46]],[405,407,[46],[45]],[408,408,[45,46],[44]],[409,410,[45],[44,46]],[411,412,[44,45],[43,46]],[413,415,[44],[43,45]],[416,416,[43,44],[42,45]],[417,417,[43],[42,44]],[418,420,[42,43],[41,44]],[421,422,[42],[41,43]],[423,424,[41,42],[40,43]],[425,426,[41],[40,42]],[427,428,[40,41],[39,42]],[429,431,[40],[39,41]],[432,433,[39,40],[38,41]],[434,436,[39],[38,40]],[437,439,[38,39],[37,40]],[440,442,[38],[37,39]],[443,445,[37,38],[36,39]],[446,450,[37],[36,38]],[451,453,[36,37],[35,38]],[454,460,[36],[35,37]],[461,462,[35,36],[34]],[463,467,[35],[34]],[468,469,[35],[34,36]]]
DASH_RUNS = [[428,430,[],[46],"d01"],[433,434,[46],[45],"d02"],[435,435,[45,46],[44],"d02"],[436,437,[45],[44,46],"d02"],[438,438,[44,45],[43,46],"d02"],[439,439,[44],[45],"d02"],[441,441,[],[43],"d03"],[442,443,[43],[42,44],"d03"],[444,444,[42,43],[41,44],"d03"],[445,446,[42],[41,43],"d03"],[447,448,[41,42],[40,43],"d03"],[451,451,[],[40,41],"d04"],[452,452,[40],[39,41],"d04"],[453,453,[40],[39,41],"d04"],[454,455,[39],[38,40],"d04"],[456,457,[39],[38,40],"d04"],[458,458,[],[39],"d04"],[460,460,[],[38],"d05"],[461,462,[38],[39],"d05"],[463,463,[37,38],[39],"d05"],[464,467,[37],[38],"d05"],[468,468,[],[37],"d05"]]
UNASSIGNED_RUNS = [[432,432,[],[46],"u-pale01"],[440,440,[],[44],"u-pale02"],[449,449,[],[41,42],"u-pale03"],[461,462,[],[37],"u-between01"],[463,467,[36],[],"u-between01"],[470,476,[35,36],[34,37],"u-merged01"],[477,485,[34,35],[33,36],"u-merged01"],[486,512,[34],[33,35],"u-merged01"],[513,572,[34],[33,35],"u-merged01"],[573,632,[34],[33,35],"u-merged01"],[633,660,[34],[33,35],"u-merged01"],[661,689,[33,34],[32,35],"u-merged01"]]
RAW_BLOCKS = [{"first":393,"last":422,"tool_chunk_id":"99e446","exit_code":0,"original_token_count":3327},{"first":423,"last":462,"tool_chunk_id":"bf7d1f","exit_code":0,"original_token_count":2621},{"first":463,"last":512,"tool_chunk_id":"e49995","exit_code":0,"original_token_count":3152},{"first":513,"last":572,"tool_chunk_id":"de2c4e","exit_code":0,"original_token_count":3695},{"first":573,"last":632,"tool_chunk_id":"91519b","exit_code":0,"original_token_count":3438},{"first":633,"last":691,"tool_chunk_id":"d2cd28","exit_code":0,"original_token_count":3485}]
READING_COMPLETED_UTC = '2026-10-08T01:40:47+00:00'
TARGET = [395, 18, 690, 47]
CONTEXT = [393, 16, 692, 49]

def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def boundary_flags(x, rows):
    result = []
    if rows:
        if x == 395:
            result.append('target_left')
        if x == 689:
            result.append('target_right')
        if 18 in rows:
            result.append('target_top')
        if 46 in rows:
            result.append('target_bottom')
    return result

def expand_runs(runs, default_id=None):
    expanded = {}
    for run in runs:
        first, last, core, fringe = run[:4]
        local = run[4] if len(run) == 5 else default_id
        require(type(first) is int and type(last) is int and 395 <= first <= last <= 689, 'literal column bounds')
        for x in range(first, last + 1):
            require(x not in expanded, 'overlapping literal runs')
            expanded[x] = (list(core), list(fringe), local)
    return expanded

def validate_rows(x, core, fringe):
    for rows in (core, fringe):
        require(type(rows) is list and all(type(y) is int and 18 <= y <= 46 for y in rows), 'integer target rows')
        require(rows == sorted(set(rows)), 'ordered unique rows')
    require(not set(core) & set(fringe), 'core/fringe disjoint')
    require(type(x) is int and 395 <= x <= 689, 'target x')

def build():
    before = {name: pin(HERE / name) for name in PINS}
    require(all(before[name]['sha256'] == expected for name, expected in PINS.items()), 'frozen input pin')
    require((HERE / 'context01.json').read_bytes() == (HERE / 'context02.json').read_bytes(), 'same frozen contexts')
    solid = expand_runs(SOLID_RUNS, 'E5i-solid-approach01')
    dash = expand_runs(DASH_RUNS)
    unknown = expand_runs(UNASSIGNED_RUNS)
    routes = {'solid': [], 'dash': []}
    bands = []
    for x in range(395, 690):
        uc, uf, local = unknown.get(x, ([], [], None))
        bid = 'E5i-' + local if local else None
        validate_rows(x, uc, uf)
        bands.append({
            'x': x, 'core': uc, 'fringe': uf, 'status': 'identity_conflict' if uc or uf else 'no_attributable_cells',
            'fragment_id': bid, 'model': None, 'boundary_flags': boundary_flags(x, uc + uf),
            'note': (
                'Single visible blue band; confidently selected ink is not confidently assigned model identity. '
                'Two locally coincident contributions, one continuing contribution, hidden overprinting, or an ended solid trace '
                'remain alternatives. The boundary of confident attribution is not a physical endpoint.'
                if local == 'u-merged01' else
                'Blue material between or adjacent to local pieces cannot be assigned uniquely to a model/body. '
                'Fringe may include compression/background material; do not duplicate into either attributed route.'
                if local else
                'No separate unassigned cells selected in this inspected column; this is not absence of hidden curve ink.'
            ),
            'competing_identities': (
                ['spring-associated ink', 'shell-associated ink', 'overprinted contributions']
                if uc or uf else []
            ),
            'fringe_alternative': 'Compression/background material remains possible for tentative cells.',
        })
        refs = [{'band_id': bid, 'x': x}] if bid else []
        for route, mapping in (('solid', solid), ('dash', dash)):
            core, fringe, fragment = mapping.get(x, ([], [], None))
            if route == 'dash' and fragment:
                fragment = 'E5i-' + fragment
            validate_rows(x, core, fringe)
            selected = core + fringe
            flags = boundary_flags(x, selected)
            if selected:
                status = 'boundary_truncated' if flags else 'identified_local_fragment' if core else 'fringe_only'
                text = (
                    'Local blue continuous approach is distinguishable in the full strip from separated lower dash bodies; '
                    'solid assignment uses observed style and the confirmed legend, not height alone. '
                    'Only these selected cells are attributed; referenced shared material stays separate.'
                    if route == 'solid' else
                    'Local blue broken-body/endpoint material is distinguished from the continuous approach using the full strip and confirmed legend. '
                    'This local fragment ID does not bridge a gap or recover a hidden solid contribution. '
                    'Only these cells are attributed; referenced shared material stays separate.'
                )
                if flags:
                    text += ' Selected cells touch the target boundary; core may lie outside the crop when only fringe is selected.'
            else:
                status = 'identity_conflict' if refs else 'no_attributable_cells'
                text = (
                    'No model-specific cells assigned from the referenced visible band. Empty attribution is not absence, '
                    'zero support, a solid endpoint, or a claim that both models occupy the band.'
                    if refs else
                    'No cells attributed to this route in this inspected target column. '
                    'Crop exclusion, pale material and hidden contributions remain possible; this does not establish a true gap or endpoint.'
                )
            routes[route].append({
                'x': x, 'core': core, 'fringe': fringe, 'status': status, 'fragment_id': fragment,
                'boundary_flags': flags, 'note': text, 'unassigned_band_refs': refs,
            })
            require(not any(y in uc + uf for y in selected), 'no band/route duplicate')
        a, b = routes['solid'][-1], routes['dash'][-1]
        require(not any(y in b['core'] + b['fringe'] for y in a['core'] + a['fringe']), 'no duplicate model ink')
    for route in routes.values():
        require([r['x'] for r in route] == list(range(395, 690)), 'all route columns')
    require([r['x'] for r in bands] == list(range(395, 690)), 'all unassigned columns')
    require([x for block in RAW_BLOCKS for x in range(block['first'], block['last'] + 1)] == list(range(393, 692)), 'full raw context reading')
    # Diagnostic only: flag literal transcription mistakes, never redraw/reselect.
    context = json.loads((HERE / 'context01.json').read_text())
    require(context['target_boxes']['E5'] == TARGET and context['context_boxes']['E5'] == CONTEXT, 'context identity')
    pixels = {(row['x'], row['y']): row['rgb'] for row in context['cells']['E5']}
    require(len(pixels) == len(context['cells']['E5']) == 9867, 'context count')
    exact_white = []
    selected_count = 0
    for scope, records in list(routes.items()) + [('unassigned', bands)]:
        for row in records:
            for label in ('core', 'fringe'):
                for y in row[label]:
                    selected_count += 1
                    if pixels[row['x'], y] == [255, 255, 255]:
                        exact_white.append({'scope': scope, 'class': label, 'x': row['x'], 'y': y})
    after = {name: pin(HERE / name) for name in PINS}
    require(before == after, 'unchanged dependencies')
    return {
        'pair': 'E5', 'reader': 'quiet_mechanism_inference_review; independent prior-informed AI source reader',
        'status': 'frozen_manual_native_annotation_not_accepted_measurement',
        'reading_completed_utc': READING_COMPLETED_UTC,
        'freeze_time_note': 'Fixed reading-completion anchor, not a runtime timestamp or independent witness. Later file pins identify the freeze; mechanical repeats retain this same anchor.',
        'target_box': TARGET, 'context_box': CONTEXT,
        'inputs': before, 'inputs_after': after, 'script_pin': pin(Path(__file__)),
        'literal_manual_transcription': {'solid_runs_inclusive': SOLID_RUNS,
                                        'dash_runs_inclusive': DASH_RUNS,
                                        'unassigned_runs_inclusive': UNASSIGNED_RUNS,
                                        'unspecified_route_column': 'Explicit inspected no_attributable_cells unless a referenced unassigned band requires identity_conflict.',
                                        'unspecified_unassigned_column': 'Explicit inspected empty unassigned record, not a missing or uninspected column.'},
        'coverage': {
            'full_native_Im9_viewed': True, 'full_composed_page_viewed': True,
            'native_view_detail': 'original, 745x92 unchanged',
            'page_view_detail': 'original requested; tool resized 1700x2200 to1376x1780. Native coordinates came from exact raw context.',
            'view_receipt': 'functions image call immediately following source reads 0f85a6/ca6e6b',
            'raw_blocks': RAW_BLOCKS, 'raw_rows_inclusive': [16, 48],
            'raw_context_columns': 299, 'raw_context_cells': 9867, 'all_blocks_untruncated': True,
            'exact_white_omission_rule': 'Only RGB255,255,255 omitted by frozen show; omitted positions read as exact white. Every other RGB value displayed/read.',
            'target_columns': 295, 'model_route_records': 590, 'unassigned_band_records': 295,
            'uncompleted': 'E4 has not been independently annotated by this reader; E5 outside this fixed target, full supported domains, physical ordinates and human selected-curve review remain uncompleted.',
        },
        'identity_basis': (
            'Complete native strip and composed-page legend identify blue five-bolt solid Spring and dashed Shell styles. '
            'The separated approach permits local assignments only. Where the approaching pieces become a single narrow band, '
            'the selected ink is recorded once without model identity; the particular solid endpoint and hidden overprint are unresolved. '
            'Red/green traces elsewhere in the raw context are not E5 selections.'
        ),
        'independence': 'Same-source nonblind AI. Prior energy inventory, E5 one-band correction and method knowledge known. No current root E5 or other new peer annotation read before this freeze. No human/expert participation claimed.',
        'limits': [
            'Core means confidently attributed visible ink; fringe is tentative edge/compression attribution. These are not calibrated pre-raster containment bounds.',
            'In an unassigned band, core confidence concerns visible ink only, not model identity or two hidden curves.',
            'Unselected pale cells are not certified outside the mathematical curve; raw context remains preserved.',
            'Local dash IDs do not join gaps. A loss of confident model attribution is not a demonstrated curve endpoint.',
            'Exact-white checking is a transcription diagnostic, not a pixel classifier or license for algorithmic redrawing.',
            'No source editing, fitted curve, threshold, interpolation, physical ordinate, admitted support, metric, cause, human acceptance or legal promotion.',
        ],
        'pre_freeze_transcription_checks': {
            'all_target_records_expanded': True, 'bounds_order_disjointness_and_flags': 'passed',
            'selected_cells_checked_for_exact_white': selected_count,
            'selected_exact_white_cells': exact_white,
            'pre_freeze_corrections': [],
            'context_previously_independently_verified': 'context-independent-check.json; all 26641 saved batch cells. Contexts not regenerated for this reading.',
        },
        'human_accepted': False, 'physical_support': None, 'routes': routes, 'unassigned_bands': bands,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', choices=['reader-E5-independent.json', 'reader-E5-independent-repeat.json'])
    args = parser.parse_args()
    result = build()
    checks = result['pre_freeze_transcription_checks']
    summary = {'route_records': 590, 'unassigned_records': 295,
               'selected_cells': checks['selected_cells_checked_for_exact_white'],
               'selected_exact_white_cells': checks['selected_exact_white_cells'],
               'route_status_counts': {k: dict(Counter(r['status'] for r in v)) for k, v in result['routes'].items()},
               'script_pin': result['script_pin']}
    if args.check:
        print(json.dumps(summary, sort_keys=True))
        if checks['selected_exact_white_cells']:
            raise SystemExit(1)
        return
    require(args.output is not None, 'output required')
    require(not checks['selected_exact_white_cells'], 'Preserve and manually review exact-white transcription failures before freeze; never auto-remove.')
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
    with (HERE / args.output).open('xb') as stream:
        stream.write(payload)
    summary['output'] = args.output
    summary['output_pin'] = pin(HERE / args.output)
    print(json.dumps(summary, sort_keys=True))

if __name__ == '__main__':
    main()

