"""Expand the root reader's literal E7 annotation; never select pixels from RGB."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = {
    '../native-strips01/Im8.jpg': '0c49df5f6117d3f0e9b206d7c3352edf57849e4ac00ef9764b857b1445947d83',
    '../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    'REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    'context01.json': 'b611904d9f065dcd23860e7bca998b26a07b6c0196b20dd5af9d3b1e854cadfb',
    'context02.json': 'b611904d9f065dcd23860e7bca998b26a07b6c0196b20dd5af9d3b1e854cadfb',
}

# Inclusive manually read column runs. These do not come from a color cutoff.
# The near-end body edges are less certain than the contrasting interior row.
DASH_CORES = [
    ('d01',580,582), ('d02',586,591), ('d03',595,600),
    ('d04',605,610), ('d05',614,619), ('d06',623,628),
    ('d07',633,638), ('d08',642,647), ('d09',651,656),
    ('d10',660,666), ('d11',670,675), ('d12',679,684),
    ('d13',688,689),
]


def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def build():
    inputs = {name: pin(HERE/name) for name in EXPECTED}
    if any(inputs[name]['sha256'] != expected for name, expected in EXPECTED.items()):
        raise ValueError('Frozen input changed')
    routes = {'solid': [], 'dash': []}
    for x in range(580,690):
        flags = (['target_left'] if x == 580 else []) + (['target_right'] if x == 689 else [])
        routes['solid'].append({
            'x': x, 'core': [24], 'fringe': [23,25,26],
            'status': 'boundary_truncated' if flags else 'identified_local_fragment',
            'fragment_id': 's01', 'boundary_flags': flags,
            'note': 'Continuous local green stroke; row24 confidently attributed, adjacent rows23/25 and paler row26 tentative. Row22 and farther pale material left unassigned, not certified outside the original stroke. No earlier-crossing identity or physical endpoint claim.',
        })
        body = [name for name, first, last in DASH_CORES if first <= x <= last]
        if len(body) > 1:
            raise ValueError('Overlapping literal dash runs')
        routes['dash'].append({
            'x': x, 'core': [19] if body else [],
            'fringe': [18,20] if body else [18,19,20],
            'status': ('boundary_truncated' if flags else 'identified_local_fragment') if body else 'identity_conflict',
            'fragment_id': body[0] if body else None,
            'boundary_flags': flags,
            'note': ('Contrasting local dash-body row19; rows18/20 tentative stroke edge. Farther pale tails remain unassigned; no calibrated original-curve containment.' if body else
                     'Pale upper-band material and/or weak body edge; these candidate fringe cells cannot be assigned uniquely to a local dash body. No true gap, continuous path, or zero-support assertion.'),
        })
    if inputs != {name: pin(HERE/name) for name in EXPECTED}:
        raise ValueError('Input changed during expansion')
    return {
        'pair': 'E7', 'reader': 'root', 'status': 'frozen_manual_native_annotation_not_accepted_measurement',
        'target_box': [580,14,690,30], 'context_box': [578,12,692,32],
        'coordinate_convention': 'Zero-based native pixel cells; boxes half-open; literal dash runs inclusive.',
        'inputs': inputs, 'script_pin': pin(Path(__file__)),
        'coverage': {
            'complete_native_strip_viewed': True,
            'complete_composed_page_viewed': True,
            'page_display_limit': '1700x2200 source was displayed at 1376x1780; native coordinates use unchanged RGB data, not that resized page.',
            'current_view_receipt': '48bd7c/8cb80e/43b901 image call; images followed those command receipts',
            'raw_context_blocks': [[578,615],[616,653],[654,691]],
            'raw_context_receipts': ['fd24d1','22baa5','d8d6e0'],
            'raw_context_rows': [12,31], 'context_cells': 2280,
            'all_target_columns_read': True, 'records': 220,
            'prior_reading': 'Same complete E7 context read in the preceding goal continuation; current blocks were reread after context recovery before freezing.',
            'uncompleted': 'Root E6 and other new regions are not annotated in this artifact.',
        },
        'literal_runs': {'solid': {'columns': [580,689], 'core': [24], 'fringe': [23,25,26], 'fragment_id':'s01'},
                         'dash_core_runs': DASH_CORES,
                         'dash_body_core': [19], 'dash_body_fringe': [18,20],
                         'dash_other_columns': {'core': [], 'fringe': [18,19,20], 'status':'identity_conflict','fragment_id':None}},
        'identity_basis': 'Full strip shows a locally continuous lower green stroke and repeated upper green dash bodies. Confirmed composed-page legend identifies solid Spring and dashed Shell, green seven bolts. Local style, not height alone; identity through earlier crossing is unresolved.',
        'independence': 'Prior-informed AI primary reader. No current independent E7 annotation inspected before this freeze. Shared source and earlier qualitative knowledge; not blind, a second historical source, human review, or expert certification.',
        'limits': 'Manual attribution is not a calibrated pre-raster bound. Candidate interbody fringe remains identity-conflicted, never bridged. Local IDs are reader-specific. No physical ordinate, support interval, discrepancy, uncertainty coverage probability or cause inference.',
        'human_accepted': False, 'routes': routes,
    }


if __name__ == '__main__':
    result = build()
    output = HERE/'reader-E7-root.json'
    with output.open('x') as handle:
        json.dump(result, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write('\n')
    print(json.dumps({'output': str(output), 'pin': pin(output), 'records': sum(map(len,result['routes'].values()))}))
