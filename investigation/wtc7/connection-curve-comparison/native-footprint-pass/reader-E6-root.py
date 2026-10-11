"""Literal root E6 reading expanded without pixel classification or interpolation."""
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
# Inclusive manual column runs, not a measured brightness rule or fitted path.
DASH_CORES = [
    ('d01',515,518), ('d02',523,527), ('d03',532,537),
    ('d04',541,546), ('d05',551,555), ('d06',560,565),
    ('d07',569,574), ('d08',579,583), ('d09',588,592),
    ('d10',597,602), ('d11',606,611), ('d12',616,620),
    ('d13',625,629), ('d14',634,639), ('d15',644,648),
    ('d16',653,657), ('d17',662,667), ('d18',671,676),
    ('d19',680,685),
]
WEAK_LOWER_BODY_ROWS = [602,620,639,662,671,680,681]


def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def build():
    inputs = {name: pin(HERE/name) for name in EXPECTED}
    if any(inputs[name]['sha256'] != value for name,value in EXPECTED.items()):
        raise ValueError('Frozen input changed')
    routes = {'solid': [], 'dash': []}
    for x in range(515,690):
        flags = (['target_left'] if x == 515 else []) + (['target_right'] if x == 689 else [])
        routes['solid'].append({
            'x':x, 'core':[70] if x <= 540 else [69,70],
            'fringe':[69,71] if x <= 540 else [68,71],
            'status':'boundary_truncated' if flags else 'identified_local_fragment',
            'fragment_id':'s01', 'boundary_flags':flags,
            'note':'Locally continuous upper red stroke; changing occupancy toward rows69/70. Adjacent selected rows tentative; more distant pale tails remain unassigned. No original pre-raster containment or identity across the earlier contact is asserted.',
        })
        body = [name for name,first,last in DASH_CORES if first <= x <= last]
        if len(body) > 1:
            raise ValueError('Overlapping literal runs')
        if body:
            core = [73] if x in WEAK_LOWER_BODY_ROWS else [73,74]
            fringe = [72,74,75] if x in WEAK_LOWER_BODY_ROWS else [72,75]
            fragment = body[0]
            status = 'boundary_truncated' if flags else 'identified_local_fragment'
            note = 'Distinguishable local lower broken red body; adjacent rows72/75 tentative. The explicitly listed weak lower-row body edges retain row74 only as fringe. Body identity is local, not through the earlier contact.'
        elif x == 689:
            core, fringe, fragment, status = [], [72,73,74,75], 'd20', 'boundary_truncated'
            note = 'Weak leading edge at target right; darker corresponding lower red body visible in context columns690/691. All selected target cells tentative. Context does not expand the annotation or establish a physical endpoint.'
        else:
            core, fringe, fragment, status = [], [72,73,74,75], None, 'identity_conflict'
            note = 'Pale lower-band material and/or weak dash-body edge retained as candidate fringe, but not uniquely assigned to a body. No true gap, continuous path, zero physical support, or original-curve containment is asserted.'
        routes['dash'].append({'x':x,'core':core,'fringe':fringe,'status':status,
                               'fragment_id':fragment,'boundary_flags':flags,'note':note})
    if inputs != {name:pin(HERE/name) for name in EXPECTED}:
        raise ValueError('Input changed during expansion')
    return {
        'pair':'E6', 'reader':'root', 'status':'frozen_manual_native_annotation_not_accepted_measurement',
        'target_box':[515,57,690,85], 'context_box':[513,55,692,87],
        'coordinate_convention':'Zero-based native pixel cells; boxes half-open; manual column runs inclusive.',
        'inputs':inputs, 'script_pin':pin(Path(__file__)),
        'coverage':{
            'complete_native_strip_viewed':True,'complete_composed_page_viewed':True,
            'image_view':'Same unchanged complete Im8/page view as root E7 in this continuation; page display1700x2200 resized1376x1780. Native coordinates read from raw RGB.',
            'raw_context_blocks':[[513,557],[558,602],[603,647],[648,691]],
            'raw_context_receipts':['d5724d','f54905','0599c9','dd43f5'],
            'raw_context_rows':[55,86], 'context_cells':5728,
            'all_target_columns_read':True,'records':350,
            'uncompleted':'Other new regions and previously inventoried approach/contact regions remain outside this artifact.',
        },
        'literal_runs':{
            'solid':[{'columns':[515,540],'core':[70],'fringe':[69,71],'fragment_id':'s01'},
                     {'columns':[541,689],'core':[69,70],'fringe':[68,71],'fragment_id':'s01'}],
            'dash_core_runs':DASH_CORES,'dash_body_core':[73,74],'dash_body_fringe':[72,75],
            'weak_lower_body_rows':WEAK_LOWER_BODY_ROWS,'weak_core':[73],'weak_fringe':[72,74,75],
            'dash_last_column':{'x':689,'core':[],'fringe':[72,73,74,75],'fragment_id':'d20'},
            'dash_other_columns':{'core':[],'fringe':[72,73,74,75],'status':'identity_conflict','fragment_id':None},
        },
        'identity_basis':'Locally continuous upper red trace and distinguishable lower dash bodies, with the confirmed composed-page solid Spring/dashed Shell and six-bolt red legend. Not a height-only identification; earlier same-color contact remains unresolved.',
        'independence':'Prior-informed AI designated primary reader. Independent E6 annotation and literal transcription not inspected before this freeze. Shared-source annotation, not blind or human/professional verification.',
        'limits':'Native candidate footprints only, not calibrated pre-raster bounds. Unassigned interbody material is retained and not joined. No physical ordinates, support intervals, whole-curve discrepancies or causal result.',
        'human_accepted':False,'routes':routes,
    }


if __name__ == '__main__':
    result = build()
    output = HERE/'reader-E6-root.json'
    with output.open('x') as handle:
        json.dump(result,handle,indent=2,sort_keys=True,allow_nan=False)
        handle.write('\n')
    print(json.dumps({'output':str(output),'pin':pin(output),'records':sum(map(len,result['routes'].values()))}))
