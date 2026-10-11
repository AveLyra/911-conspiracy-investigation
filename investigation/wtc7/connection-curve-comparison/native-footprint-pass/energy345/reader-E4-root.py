"""Literal primary E4 reading; RGB is used only to check transcription."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = {
    'PROTOCOL.md': 'be57860a830ab716498ba5d25733021c1c975da1b0427f50f64071af4eaf5f16',
    'IDENTITY-CLARIFICATION.md': 'c9d79b6d92a5cbc2f4747e027bce81ee5b1cbec0528b018b368f22fd2b01098b',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    '../../native-strips01/Im9.jpg': '3154e28ea82ca2f39c465a7bdfe367677216543df296cf918cbbd259248f8129',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'context01.json': '59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
    'context02.json': '59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
}
# Inclusive manual local bodies, not a color predicate or fitted period.
DASH_RUNS = [
    [489,494],[499,503],[508,513],[517,522],[526,531],[536,540],
    [545,550],[554,559],[564,568],[573,577],[582,587],[591,596],
    [600,605],[610,615],[619,624],[628,633],[638,643],[647,652],
    [656,661],[665,671],[675,680],[684,689],
]


def pin(path):
    b = path.read_bytes()
    return {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}


def flags(x, rows):
    if not rows:
        return []
    return (['target_left'] if x == 440 else []) + (['target_right'] if x == 689 else []) + (['target_top'] if 72 in rows else []) + (['target_bottom'] if 91 in rows else [])


def entry(x, core, fringe, status, fragment, note, refs=None):
    return {'x': x, 'core': core, 'fringe': fringe, 'status': status,
            'fragment_id': fragment, 'boundary_flags': flags(x, core + fringe),
            'note': note, 'band_refs': refs or []}


def build():
    before = {k: pin(HERE / k) for k in EXPECTED}
    if any(before[k]['sha256'] != v for k, v in EXPECTED.items()):
        raise ValueError('Changed input')
    routes = {'solid': [], 'dash': []}
    bands = []
    for x in range(440, 690):
        matches = [i for i, (a, b) in enumerate(DASH_RUNS, 1) if a <= x <= b]
        if len(matches) > 1:
            raise ValueError('Overlapping literal runs')
        if x <= 479:
            core, fringe, local = [86,87], [85,88], 'u-merged01'
        elif x <= 485:
            core, fringe, local = [86], [85,87,88], 'u-merged01'
        elif matches:
            core, fringe, local = [], [], None
        else:
            core, fringe, local = [], [86,87], f'u-pale-{x}'
        bands.append(entry(x, core, fringe,
            'identity_conflict' if core or fringe else 'no_attributable_cells', local,
            'Merged ink or tentative interbody material recorded once; model contribution unresolved. Unselected pale cells are not certified outside the original curve. Empty attribution is not absent historical ink.'))
        refs = [local] if local else []
        routes['solid'].append(entry(x, [], [], 'identity_conflict', None,
            'No independently separable solid trace assigned. Hidden overlap, local mixture and ended solid trace remain alternatives; no endpoint or zero-support finding.', refs))
        if matches:
            routes['dash'].append(entry(x, [86], [85,87,88],
                'boundary_truncated' if x == 689 else 'identified_local_fragment', f'd{matches[0]:02d}',
                'Locally repeated body supported by full-strip dashed style. Manual edge judgment, not a calibrated containment bound; no bridge to another body. Hidden solid contribution is not excluded.'))
        else:
            routes['dash'].append(entry(x, [], [], 'identity_conflict', None,
                'No uniquely identified dashed cells; merged band or uncertain edge stays unassigned, not a verified gap.', refs))
    # These checks reject a transcription error; they never add/remove a cell.
    pixels = {(r['x'], r['y']): r['rgb'] for r in json.loads((HERE/'context01.json').read_text())['cells']['E4']}
    for group in [*routes.values(), bands]:
        if [r['x'] for r in group] != list(range(440,690)):
            raise ValueError('Coverage')
        for r in group:
            if set(r['core']) & set(r['fringe']):
                raise ValueError('Class overlap')
            for y in r['core'] + r['fringe']:
                if not 72 <= y < 92 or pixels[r['x'], y] == [255,255,255]:
                    raise ValueError(('Invalid selected cell', r['x'], y))
    for s, d, u in zip(routes['solid'], routes['dash'], bands):
        sets = [set(r['core'] + r['fringe']) for r in (s,d,u)]
        if any(sets[i] & sets[j] for i,j in [(0,1),(0,2),(1,2)]):
            raise ValueError('Duplicate attribution')
    if before != {k: pin(HERE/k) for k in EXPECTED}:
        raise ValueError('Input changed')
    return {
        'pair': 'E4', 'reader': 'root',
        'status': 'frozen_manual_native_annotation_not_accepted_measurement',
        'target_box': [440,72,690,92], 'context_box': [438,70,692,92],
        'inputs': before, 'script_pin': pin(Path(__file__)),
        'literal_instructions': {'dash_runs_inclusive': DASH_RUNS,
            'merged_early': {'columns_inclusive':[440,479], 'core':[86,87], 'fringe':[85,88]},
            'merged_later': {'columns_inclusive':[480,485], 'core':[86], 'fringe':[85,87,88]},
            'other_interbody': {'core':[], 'fringe':[86,87]},
            'dash_core':[86], 'dash_fringe':[85,87,88]},
        'coverage': {'native_strip_viewed': True, 'complete_composed_page_viewed': True,
            'page_display_limit':'1700x2200 displayed at1376x1780; coordinates from raw RGB, not resized page.',
            'view_receipt':'image call after 656666; unchanged Im9 viewed again before 29bc64',
            'context_blocks_inclusive':[[438,499],[500,563],[564,627],[628,691]],
            'raw_read_receipts':['78a4a3','7c85fb','5d7a70','6af9de'],
            'context_rows_inclusive':[70,91], 'context_cells':5588,
            'all_target_columns_read':True, 'model_route_records':500, 'unassigned_band_records':250},
        'identity_basis':'Source legend gold/four bolts, solid Spring/dashed Shell. Early merged band is not separable; later repeated bodies support local dash assignment only. The image does not establish a solid endpoint or two coincident ordinates.',
        'independence':'Prior-informed primary AI reading. No current peer E4 content inspected before freeze; same source, not blinded or human acceptance.',
        'limits':'Native visible-ink assignment only; no threshold, interpolation, seam join, pre-raster containment, physical ordinate, admitted support, model discrepancy or cause inference.',
        'human_accepted':False, 'physical_support':None, 'routes':routes, 'unassigned_bands':bands,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = build()
    target = HERE / args.output
    with target.open('x') as f:
        json.dump(result, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')
    print(json.dumps({'output':str(target), 'pin':pin(target), 'route_records':500, 'band_records':250}))
