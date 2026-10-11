"""Literal manual E3 peer annotation. No RGB reading or cell selection code."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = [195, 35, 365, 92]
CONTEXT = [193, 33, 367, 92]
EXPECTED = {
    'PROTOCOL.md': 'cc94c588f9b132318c7ca55fcffe1ed7eafbb92fd131583ffcbc74a13e5e54b7',
    'READERS.md': '6a019e587d1cdb47303047c5c03dbae4d9c347941a8227f27a7a8e0b8dfd0b5b',
    'read_context.py': '384d0bef93d4bc05ed8cb10f5a6d27426ab983ffcb4a3e31d5ca84b116961ac3',
    '../read_context.py': 'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../../native-strips01/Im10.jpg': 'fe8c069f4bb7a19f6eb996b42b266c55552a110f8e9cbc6e9cc0d7269547cdd3',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    'context01.json': '783cd6f756918cef8a70ea79d925d7b010554b535f8d8f654970605d1c8b9095',
    'context02.json': '783cd6f756918cef8a70ea79d925d7b010554b535f8d8f654970605d1c8b9095',
}

# Format: x core-rows fringe-rows. A hyphen alone is an empty set.
# Row ranges are inclusive literal instructions, not interpolation.
SOLID = '''
222 91 90
223 90 91
224 90 89
225 89 -
226 89 88
227 88-89 -
228 88 87,89
229 87 -
230 87 86
231 86 -
232 86 85
234 85 -
235 84-85 -
236 84 83,85
237 84 83,85
263 72 73
264 72 71
265 71 70,72
266 71 70
267 70 71
268 70 69,71
269 69 68,70
270 69 68,70
271 68-69 -
272 68 67,69
273 67 68
274 67 66,68
275 66-67 -
276 66 65,67
277 65-66 -
278 65 64,66
279 65 64,66
280 64 65
281 64 63,65
282 63-64 -
283 63 62,64
284 63 62,64
285 62 63
286 62 61,63
287 61-62 -
288 61 60,62
289 61 60,62
290 60 59,61
291 60 59,61
292 59-60 -
293 59 58,60
294 59 58,60
295 58 59
296 58 57,59
297 57-58 -
298 57 58
299 57 56,58
300 56-57 -
301 56 57
302 56 55,57
303 56 55
304 55 56
305 55 54,56
306 55 54
307 54 55
308 54 53,55
309 54 53,55
310 53 54
311 53 52,54
312 53 52,54
313 53 52
314 52 53
315 52 51,53
316 52 51,53
317 51-52 53
318 51 50,52
319 51 50,52
320 51 50
321 50 49,51
322 50 49,51
323 50 49,51
324 49-50 -
325 49 50
326 49 48,50
327 49 48,50
328 48-49 -
329 48 49
330 48 47,49
331 48 47,49
332 48 47,49
333 47-48 -
334 47 46,48
335 47 46,48
336 47 46,48
337 47 46,48
338 47 46
339 46-47 -
340 46 47
341 46 45,47
342 46 45,47
343 46 45,47
344 46 45
345 46 45
346 46 45
347 45-46 -
348 45 44,46
349 45 44,46
350 45 44
351 45 44
352 45 44
353 45 44
354 45 44
355 44-45 -
356 44 45
357 44 45
358 44 43,45
359 44 43
360 44 43
361 44 43
362 44 43
363 44 43
364 44 43
'''

DASH = {
    'peer-dash-01': '''
233 - 91
234 91 -
235 - 91
''',
    'peer-dash-02': '''
238 90 91
239 90 89,91
240 89-90 -
241 89 88,90
242 89 88
243 88 87,89
244 88 87,89
''',
    'peer-dash-03': '''
247 - 86-87
248 86 85,87
249 85-86 -
250 85 84,86
251 85 84,86
252 84 85
253 84 83,85
254 - 84
''',
    'peer-dash-04': '''
256 - 82-83
257 82 81,83
258 82 81,83
259 81 82
260 81 80,82
261 80-81 -
262 80 79,81
263 - 80
''',
    'peer-dash-05': '''
265 - 78
266 78 77,79
267 78 77,79
268 77 78
269 77 76,78
270 76-77 -
271 76 75,77
272 - 75-77
273 - 76
''',
    'peer-dash-06': '''
275 - 74-75
276 74 73,75
277 73-74 -
278 73 72,74
279 73 72,74
280 72 73
281 72 73
282 - 72-73
''',
    'peer-dash-07': '''
284 - 70-71
285 70 69,71
286 70 69,71
287 69-70 68
288 69 68,70
289 68-69 -
290 68 67,69
291 - 67-68
''',
    'peer-dash-08': '''
293 - 66-67
294 66 65,67
295 66 65,67
296 65 66
297 65 64,66
298 65 64
299 64 63,65
300 - 63-65
''',
    'peer-dash-09': '''
303 - 62-63
304 62 61,63
305 62 61
306 61 62
307 61 60,62
308 60-61 59
309 60 59,61
310 - 60
''',
    'peer-dash-10': '''
312 - 58-59
313 58 57,59
314 58 57,59
315 58 57
316 57 56,58
317 57 56,58
318 57 56
319 - 56-57
''',
    'peer-dash-11': '''
321 - 55-56
322 55 54,56
323 55 54,56
324 54-55 -
325 54 53,55
326 54 53
327 53-54 -
328 - 53-54
''',
    'peer-dash-12': '''
330 - 52-53
331 52 53
332 52 51,53
333 52 51
334 51 52
335 51 50,52
336 51 50,52
337 - 50-51
''',
    'peer-dash-13': '''
340 - 49-50
341 49-50 -
342 49 48,50
343 49 48,50
344 49 48
345 48 49
346 48 49
347 - 48
''',
    'peer-dash-14': '''
349 - 47-48
350 48 47
351 47-48 -
352 47 48
353 47 48
354 47 48
355 47 -
356 - 47
''',
    'peer-dash-15': '''
358 - 46
359 46 47
360 46 47
361 46 47
362 46 -
363 46 -
364 46 -
''',
}

# Each selected cell appears once. These records retain visible candidates;
# they do not establish that all ink belongs to E3 or to one hidden curve.
UNASSIGNED = [
    ('peer-entry-candidate', ['solid'],
     'Dark cropped entry candidate; source-edge clipping and colored compression prevent a unique E3 solid attribution.', '''
219 - 91
220 91 -
221 91 -
'''),
    ('peer-early-color-contact', ['solid'],
     'Possible E3 solid edge/body mixed with nearby blue broken ink; no E3 dash candidate is implicated. Fragment membership is uncertain, not absent.', '''
224 - 91
225 - 90-91
226 - 90
229 - 88
230 - 88
231 - 87
232 - 87
233 86-87 85
234 - 86
235 - 86
'''),
    ('peer-blue-black-contact', ['solid'],
     'Locally visible dark approach ink cannot be cleanly allocated between the E3 continuous candidate and nearby blue broken stroke/compression. Candidate route solid does not exclude a non-E3 ink owner; no E3 dash identity is inferred.', '''
238 83-84 82,85
239 83-84 85
240 83 82,84
241 83 82,84
242 82-83 81
243 82 81,83
244 81 80,82
245 80-81 -
246 80 79,81
247 80 79
248 79 78,80
249 78-79 77
250 78 77,79
251 77 76,78
252 77 76,78
253 76-77 75
254 76 75,77
255 76 75
256 75 74,76
257 74-75 73
258 73-74 72,75
259 73-74 72
260 73 72,74
261 73 72,74
262 72-73 71
263 - 71
'''),
    ('peer-between-black-bodies', ['solid', 'dash'],
     'A pale row lies between separately visible black body candidates. Its allocation to the two stroke margins or compression cannot be resolved; it is recorded once.', '''
350 - 46
351 - 46
352 - 46
353 - 46
354 - 46
355 - 46
'''),
    ('peer-late-black-contact', ['solid', 'dash'],
     'The row between the approaching black cores is not uniquely assignable to either local style. Separate visible cores do not establish hidden continuation beyond this target.', '''
359 - 45
360 - 45
361 - 45
362 - 45
363 - 45
364 - 45
'''),
]

READ_BLOCKS = [
    [193,202,'3229fe'], [203,212,'43b34d'],
    [213,222,'06a54f'], [223,232,'9c2e96'],
    [233,242,'f515c5'], [243,252,'328fad'],
    [253,262,'c54483'], [263,272,'4bf66c'],
    [273,282,'63ea86'], [283,292,'91ca20'],
    [293,307,'9c573b'], [308,322,'380f9a'],
    [323,337,'2d6eb7'], [338,352,'f98114'], [353,366,'c6650d'],
]


def rows(literal):
    if literal == '-':
        return []
    out = []
    for token in literal.split(','):
        ends = [int(n) for n in token.split('-')]
        if len(ends) == 1:
            out.append(ends[0])
        elif len(ends) == 2 and ends[0] <= ends[1]:
            out.extend(range(ends[0], ends[1] + 1))
        else:
            raise ValueError('Invalid literal row instruction')
    assert out == sorted(set(out))
    return out


def table(literal):
    result = {}
    for line in literal.strip().splitlines():
        x, core, fringe = line.split()
        x = int(x)
        assert x not in result
        result[x] = (rows(core), rows(fringe))
    return result


def pin(path):
    data = path.read_bytes()
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def inputs():
    answer = {name: pin(HERE/name) for name in EXPECTED}
    assert all(answer[name]['sha256'] == expected for name, expected in EXPECTED.items())
    return answer


def flags(x, selected):
    if not selected:
        return []
    return [name for yes, name in [
        (x == TARGET[0], 'target_left'),
        (x == TARGET[2]-1, 'target_right'),
        (TARGET[1] in selected, 'target_top'),
        (TARGET[3]-1 in selected, 'target_bottom'),
    ] if yes]


def record(x, core, fringe, piece, reason, refs=None):
    refs = [] if refs is None else refs
    selected = sorted(core + fringe)
    boundary = flags(x, selected)
    if selected and boundary:
        status = 'boundary_truncated'
    elif core:
        status = 'identified_local_fragment'
    elif fringe:
        status = 'fringe_only'
    elif refs:
        status = 'identity_conflict'
    else:
        status = 'no_attributable_cells'
    return {'x': x, 'core': core, 'fringe': fringe,
            'fragment_id': piece if selected else None,
            'fragment_membership': ([{'fragment_id':piece,'core':core,'fringe':fringe}] if selected else []),
            'status': status, 'reason': reason, 'boundary_flags': boundary,
            'unassigned_band_refs': refs}


def build():
    before = inputs()
    script_pin = pin(Path(__file__))
    literal_solid = table(SOLID)
    literal_dash = {}
    for piece, literal in DASH.items():
        for x, sets in table(literal).items():
            assert x not in literal_dash
            literal_dash[x] = (*sets, piece)
    bands = []
    references = {route: {x: [] for x in range(195,365)} for route in ['solid','dash']}
    for band_id, candidates, reason, literal in UNASSIGNED:
        for x, (core, fringe) in table(literal).items():
            band = record(x, core, fringe, band_id + '-visible-piece', reason)
            band.update({'band_id':band_id, 'candidate_routes':candidates})
            bands.append(band)
            for route in candidates:
                references[route][x].append(band_id)
    routes = {'solid':[], 'dash':[]}
    for route in routes:
        for x in range(195,365):
            refs = references[route][x]
            if route == 'solid' and x in literal_solid:
                core, fringe = literal_solid[x]
                piece = 'peer-solid-entry-local' if x < 238 else 'peer-solid-post-contact-local'
                reason = 'Manually read local continuous-style black candidate; pale margins are tentative and no continuity through color-contact uncertainty is asserted.'
            elif route == 'dash' and x in literal_dash:
                core, fringe, piece = literal_dash[x]
                reason = 'Manually read this distinct black dash-body candidate and tentative edge cells; adjacent empty columns are not bridged.'
            else:
                core, fringe, piece = [], [], None
                reason = ('Visible candidate ink remains in the referenced unassigned band; empty model-attributed sets do not mean absence.' if refs else
                          'All context rows in this column were inspected; no cells are attributed to this E3 route inside the target. This does not assert true absence, zero, or a physical endpoint.')
            if refs and (core or fringe):
                reason += ' Additional same-column candidate cells remain unresolved in the referenced band.'
            routes[route].append(record(x, core, fringe, piece, reason, refs))
    result = {
        'region_id':'E3-Im10', 'pair':'E3', 'source':'Im10.jpg', 'reader':'peer',
        'reader_identity':'/root/approach_source_peer', 'target_box':TARGET, 'context_box':CONTEXT,
        'inputs':before, 'script_pin':script_pin,
        'coverage': {
            'all_context_cells_actually_read':True, 'context_cell_count':10266,
            'row_range_inclusive':[33,91], 'blocks_inclusive_and_receipt':READ_BLOCKS,
            'display':'Exact RGB row runs; gN means (N,N,N); only exact white omitted. All outputs untruncated, exit 0.',
            'synthetic_control_receipt':'67ebc7: all 11 controls true; context01/context02 hashes matched.',
            'source_orientation':'Both unchanged complete images viewed once before this batch protocol; reuse is prior-informed and hashes were rechecked. No coordinates inferred from page display.',
            'annotation_scope':'Every x195..364 for each route; target cells only. No counterpart new annotation read before freeze.',
            'limitations':'AI self-attested source inspection, not independently witnessed perception, a blind study, a human spot-check, or expert validation.',
            'uncompleted_context':[],
        },
        'routes':routes, 'unassigned_bands':bands,
        'unassigned_ownership_limitation':'The solid-only bands retain possible E3 solid membership against non-target blue/color-compression alternatives. Candidate routes refer only to this E3 export and do not certify exclusive E3 ownership; the schema does not enforce per-member non-E3 candidates.',
        'human_accepted':False, 'physical_support':None,
        'frozen_before_exchange':True,
    }
    validate(result)
    assert before == inputs() and script_pin == pin(Path(__file__))
    return result


def validate(result):
    occupied = set()
    by_band = {(b['band_id'], b['x']): b for b in result['unassigned_bands']}
    assert len(by_band) == len(result['unassigned_bands'])
    for route, records in result['routes'].items():
        assert [r['x'] for r in records] == list(range(195,365))
        for r in records:
            for ref in r['unassigned_band_refs']:
                assert route in by_band[ref,r['x']]['candidate_routes']
    for b in result['unassigned_bands']:
        assert b['core'] or b['fringe']
        for route in b['candidate_routes']:
            assert b['band_id'] in result['routes'][route][b['x']-195]['unassigned_band_refs']
    for r in result['routes']['solid'] + result['routes']['dash'] + result['unassigned_bands']:
        assert 195 <= r['x'] < 365
        assert r['reason']
        assert not set(r['core']) & set(r['fringe'])
        for kind in ['core','fringe']:
            assert r[kind] == sorted(set(r[kind]))
            assert all(type(y) is int and 35 <= y < 92 for y in r[kind])
            assert sorted(y for m in r['fragment_membership'] for y in m[kind]) == r[kind]
        selected = r['core'] + r['fringe']
        assert r['boundary_flags'] == flags(r['x'], selected)
        for y in selected:
            point = (r['x'],y)
            assert point not in occupied, ('duplicated selected source cell', point)
            occupied.add(point)
        assert bool(r['fragment_membership']) == bool(selected)
        if r['status'] == 'no_attributable_cells':
            assert not selected and not r['unassigned_band_refs']
        if not selected and r['unassigned_band_refs']:
            assert r['status'] == 'identity_conflict'
    covered = [x for first,last,_ in READ_BLOCKS for x in range(first,last+1)]
    assert covered == list(range(193,367))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--save', action='store_true', help='Exclusive-create assigned JSON; otherwise print bytes.')
    args = parser.parse_args()
    first = json.dumps(build(), indent=2, sort_keys=True) + '\n'
    second = json.dumps(build(), indent=2, sort_keys=True) + '\n'
    assert first == second
    if args.save:
        destination = HERE/'reader-E3-peer.json'
        with destination.open('x') as f:
            f.write(first)
        print(json.dumps({'path':destination.name, **pin(destination), 'records':340,
                          'two_in_memory_expansions_identical':True, 'validation':'passed'}))
    else:
        print(first, end='')


if __name__ == '__main__':
    main()
