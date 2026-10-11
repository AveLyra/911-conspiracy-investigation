"""Literal E5 primary reading; expansion transcribes manual sets, not RGB rules."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = {
    'PROTOCOL.md':'be57860a830ab716498ba5d25733021c1c975da1b0427f50f64071af4eaf5f16',
    'IDENTITY-CLARIFICATION.md':'c9d79b6d92a5cbc2f4747e027bce81ee5b1cbec0528b018b368f22fd2b01098b',
    '../PROTOCOL.md':'2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json':'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    '../../native-strips01/Im9.jpg':'3154e28ea82ca2f39c465a7bdfe367677216543df296cf918cbbd259248f8129',
    '../../render01/page-076.png':'0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'context01.json':'59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
    'context02.json':'59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48',
}
# Each tuple is [first,last,core,fringe,local ID], inclusive x bounds.
# Runs merely abbreviate manually read identical choices; no interpolation.
SOLID_RUNS = [
    [403,403,[],[46],'s01'], [404,404,[46],[],'s01'],
    [405,407,[46],[45],'s01'], [408,408,[45,46],[44],'s01'],
    [409,410,[45],[44,46],'s01'], [411,412,[44,45],[],'s01'],
    [413,415,[44],[43,45],'s01'], [416,416,[43,44],[42,45],'s01'],
    [417,418,[43],[42,44],'s01'], [419,420,[42,43],[41,44],'s01'],
    [421,422,[42],[41,43],'s01'], [423,424,[41,42],[40,43],'s01'],
    [425,426,[41],[40,42],'s01'], [427,428,[40,41],[39,42],'s01'],
    [429,431,[40],[39,41],'s01'], [432,433,[39,40],[38,41],'s01'],
    [434,436,[39],[38,40],'s01'], [437,439,[38,39],[37,40],'s01'],
    [440,442,[38],[37,39],'s01'], [443,445,[37,38],[36,39],'s01'],
    [446,450,[37],[36,38],'s01'], [451,453,[36,37],[35,38],'s01'],
    [454,459,[36],[35,37],'s01'], [460,460,[35,36],[34,37],'s01'],
    [461,462,[35,36],[34],'s01'], [463,466,[35],[34],'s01'],
]
DASH_RUNS = [
    [432,432,[],[46],'d01'], [433,433,[46],[45],'d01'],
    [434,434,[46],[45],'d01'], [435,435,[45,46],[44],'d01'],
    [436,437,[45],[44,46],'d01'], [438,438,[44,45],[43,46],'d01'],
    [439,439,[44],[45],'d01'],
    [442,442,[43],[42,44],'d02'], [443,443,[43],[42,44],'d02'],
    [444,444,[42,43],[44],'d02'], [445,446,[42],[41,43],'d02'],
    [447,448,[41,42],[40,43],'d02'], [449,449,[],[41,42],'d02'],
    [451,451,[],[40,41],'d03'], [452,452,[40],[39,41],'d03'],
    [453,453,[39,40],[41],'d03'], [454,454,[39,40],[],'d03'],
    [455,457,[39],[38,40],'d03'], [458,458,[],[39],'d03'],
    [460,460,[],[38],'d04'], [461,462,[38],[37,39],'d04'],
    [463,466,[37],[38],'d04'],
]
BAND_RUNS = [
    [463,466,[36],[],'u-contact'],
    [467,467,[35],[34,36,37],'u-merged'],
    [468,469,[35],[34,36],'u-merged'],
    [470,474,[35,36],[34,37],'u-merged'],
    [475,483,[34,35],[33,36],'u-merged'],
    [484,649,[34],[33,35],'u-merged'],
    [650,689,[33,34],[32,35],'u-merged'],
]


def pin(path):
    b = path.read_bytes()
    return {'sha256':hashlib.sha256(b).hexdigest(), 'bytes':len(b)}


def flags(x, rows):
    if not rows:
        return []
    return (['target_left'] if x==395 else []) + (['target_right'] if x==689 else []) + (['target_top'] if 18 in rows else []) + (['target_bottom'] if 46 in rows else [])


def literal(runs, x):
    matches = [r for r in runs if r[0] <= x <= r[1]]
    if len(matches) > 1:
        raise ValueError('Overlapping literal runs')
    return (matches[0][2], matches[0][3], matches[0][4]) if matches else ([],[],None)


def entry(x, core, fringe, status, fragment, note, refs=None):
    return {'x':x, 'core':core, 'fringe':fringe, 'status':status,
            'fragment_id':fragment, 'boundary_flags':flags(x, core+fringe),
            'note':note, 'band_refs':refs or []}


def build():
    before = {k:pin(HERE/k) for k in EXPECTED}
    if any(before[k]['sha256'] != v for k,v in EXPECTED.items()):
        raise ValueError('Changed input')
    routes = {'solid':[], 'dash':[]}
    bands = []
    for x in range(395,690):
        c,f,bid = literal(BAND_RUNS,x)
        bands.append(entry(x,c,f,'identity_conflict' if bid else 'no_attributable_cells',bid,
            'Visible contact/merged ink assigned once. A band core certifies the reader attribution of ink, not model identity. An empty record does not establish a physical gap.'))
        for route,runs in [('solid',SOLID_RUNS), ('dash',DASH_RUNS)]:
            c,f,local = literal(runs,x)
            status = ('boundary_truncated' if flags(x,c+f) else 'identified_local_fragment' if c else 'fringe_only') if local else 'identity_conflict' if bid else 'no_attributable_cells'
            routes[route].append(entry(x,c,f,status,local,
                'Approach identity uses connected solid versus discrete dashed style in unchanged context, not height alone. Tentative edge cells stay fringe; core may coexist with separately unassigned contact ink. Empty cells are unknown attribution, not zero support. Later shared ink does not prove two coincident traces.',
                [bid] if bid else []))
    # Reject bad transcription; never choose/replace cells from their colors.
    pixels = {(r['x'],r['y']):r['rgb'] for r in json.loads((HERE/'context01.json').read_text())['cells']['E5']}
    for records in [*routes.values(),bands]:
        if [r['x'] for r in records] != list(range(395,690)):
            raise ValueError('Coverage')
        for r in records:
            if set(r['core']) & set(r['fringe']):
                raise ValueError('Class overlap')
            for y in r['core']+r['fringe']:
                if not 18 <= y < 47 or pixels[r['x'],y] == [255,255,255]:
                    raise ValueError(('Invalid selected cell',r['x'],y))
    for s,d,u in zip(routes['solid'],routes['dash'],bands):
        sets = [set(r['core']+r['fringe']) for r in (s,d,u)]
        if any(sets[i]&sets[j] for i,j in [(0,1),(0,2),(1,2)]):
            raise ValueError('Duplicate attribution')
    if before != {k:pin(HERE/k) for k in EXPECTED}:
        raise ValueError('Input changed')
    return {
        'pair':'E5', 'reader':'root', 'status':'frozen_manual_native_annotation_not_accepted_measurement',
        'target_box':[395,18,690,47], 'context_box':[393,16,692,49],
        'inputs':before, 'script_pin':pin(Path(__file__)),
        'literal_instructions':{'solid_runs_inclusive':SOLID_RUNS, 'dash_runs_inclusive':DASH_RUNS, 'band_runs_inclusive':BAND_RUNS},
        'coverage':{'native_strip_viewed':True, 'complete_composed_page_viewed':True,
            'view_receipt':'unchanged Im9 before29bc64; full composed page repeated immediately before this script creation',
            'page_display_limit':'Coordinates from raw native RGB, not resized1700x2200 page preview.',
            'context_blocks_inclusive':[[393,441],[442,491],[492,541],[542,591],[592,641],[642,691]],
            'raw_read_receipts':['872e68','d3d6d1','5ad756','60ae2b','49b927','8e7c86'],
            'context_rows_inclusive':[16,48], 'context_cells':9867,
            'all_target_columns_read':True, 'model_route_records':590, 'unassigned_band_records':295},
        'identity_basis':'Confirmed legend blue/five bolts, solid Spring/dashed Shell. Separable approach pieces precede local contact. Row36 at463..466 remains unassigned beside separately assigned cores; from467 the selected shared band cannot be uniquely partitioned. These reader limits do not locate a mathematical merge or endpoint.',
        'independence':'Prior-informed primary AI; no current peer E5 annotation inspected before freeze. Same source, not blinded or independent human acceptance.',
        'limits':'Manual native ink attribution only; no threshold, interpolation, seam join, calibrated pre-raster bound, admitted support, model discrepancy or cause inference. Unselected pale cells are not certified outside the original curve.',
        'human_accepted':False, 'physical_support':None, 'routes':routes, 'unassigned_bands':bands,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    args = parser.parse_args()
    result = build()
    target = HERE/args.output
    with target.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False)
        f.write('\n')
    print(json.dumps({'output':str(target), 'pin':pin(target), 'route_records':590, 'band_records':295}))
