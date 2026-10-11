"""Literal manual F5 peer selection; expansion never examines source RGB."""
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTEXT_SHA = '6289f98ee3ae3c89e894b10b8c5dd512e1b9d4716075ff6fe8a62900028b6ab5'


def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def dependencies(extra=()):
    paths = ['PROTOCOL.md', 'PROTOCOL-V2.md', 'READERS.md', '../PROTOCOL.md',
             'read_context.py', 'read_context_v2.py', '../read_context.py',
             '../approach34/read_context.py', 'context01.json', 'context02.json',
             '../../native-strips01/Im1.jpg', '../../native-strips01/Im3.jpg',
             '../../render01/page-076.png', '../../NUMERICAL-PROTOCOL.md',
             '../../HUMAN-REVIEW-GATE.md',
             '../../remaining-route-inventory/reader-root.json',
             '../../remaining-route-inventory/reader-force.json',
             '../../remaining-route-inventory/force-reconciliation.json',
             '../../remaining-route-inventory/report.md',
             '/Users/admin/docs/911/AGENTS.md', '/Users/admin/docs/911/WORKFLOW.md',
             '/Users/admin/docs/911/START-HERE.md',
             '/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md',
             '/Users/admin/.codex/skills/evidence-falsification-auditor/SKILL.md',
             '/Users/admin/.codex/skills/source-of-truth-guardian/SKILL.md', *extra]
    result = {os.path.relpath((HERE / p).resolve(), HERE): pin((HERE / p).resolve()) for p in paths}
    for name in ('context01.json', 'context02.json'):
        if result[name]['sha256'] != CONTEXT_SHA:
            raise ValueError('Frozen context changed: ' + name)
        # Only the input metadata is used; cells are never examined or selected.
        upstream = json.loads((HERE / name).read_text())['inputs']
        for relative, expected in upstream.items():
            key = os.path.relpath((HERE / relative).resolve(), HERE)
            current = pin(HERE / key)
            if current != expected:
                raise ValueError('Transitive context dependency changed: ' + key)
            result[key] = current
    return result


def rows(text):
    if text == '-':
        return []
    result = []
    for piece in text.split(','):
        ends = [int(v) for v in piece.split('-')]
        result.extend(range(ends[0], ends[-1] + 1))
    if result != sorted(set(result)):
        raise ValueError('Literal rows not sorted and unique')
    return result


def flags(x, selected, box):
    return [name for name, yes in (
        ('target_left', bool(selected) and x == box[0]),
        ('target_right', bool(selected) and x == box[2] - 1),
        ('target_top', box[1] in selected),
        ('target_bottom', box[3] - 1 in selected)) if yes]


def literals(text):
    # Each line is manually selected: x, inclusive core rows, inclusive fringe rows.
    for line in text.strip().splitlines():
        if line.strip():
            x, core, fringe = line.split()
            yield int(x), rows(core), rows(fringe)


def assemble(pair, source, box, context, routes_literal, bands_literal, coverage, script):
    inputs = dependencies([script.name])
    result = {'region_id': pair + '-' + source[:-4], 'pair': pair, 'source': source,
              'reader': 'force56_peer', 'target_box': box, 'context_box': context,
              'inputs': inputs, 'script_pin': pin(script), 'coverage': coverage,
              'routes': {}, 'unassigned_bands': [], 'human_accepted': False,
              'physical_support': None}
    for route in ('solid', 'dash'):
        reason = ('Inspected whole target column: no confidently attributable local '
                  + ('solid' if route == 'solid' else 'broken')
                  + ' cells; other-color ink and nonspecific pale JPEG background are excluded. '
                  'This is not physical absence or zero force.')
        table = {x: {'x': x, 'core': [], 'fringe': [], 'fragment_id': None,
                     'fragment_membership': [], 'status': 'no_attributable_cells',
                     'reason': reason, 'boundary_flags': [], 'unassigned_band_refs': []}
                 for x in range(box[0], box[2])}
        for fragment_id, text in routes_literal.get(route, []):
            for x, core, fringe in literals(text):
                row = table[x]
                if set(core + fringe) & set(row['core'] + row['fringe']):
                    raise ValueError('Overlapping literal pieces')
                row['core'] = sorted(row['core'] + core)
                row['fringe'] = sorted(row['fringe'] + fringe)
                row['fragment_membership'].append({'fragment_id': fragment_id,
                                                   'core': core, 'fringe': fringe})
        for row in table.values():
            selected = row['core'] + row['fringe']
            if selected:
                row['fragment_id'] = (row['fragment_membership'][0]['fragment_id']
                                      if len(row['fragment_membership']) == 1 else None)
                row['boundary_flags'] = flags(row['x'], selected, box)
                row['status'] = ('boundary_truncated' if row['boundary_flags'] else
                                 'identified_local_fragment' if row['core'] else 'fringe_only')
                row['reason'] = ('Manual attribution of visible ' + pair + ' ' + route +
                    ' stroke using native RGB and whole-strip style. Core is direct local ink; '
                    'fringe is tentative edge/compression attribution. No gap or seam is bridged.')
                if row['boundary_flags']:
                    row['reason'] += ' Selected cells touch the crop boundary, not a demonstrated physical endpoint.'
        result['routes'][route] = list(table.values())
    for fragment_id, candidate_routes, reason, text in bands_literal:
        for x, core, fringe in literals(text):
            band_id = fragment_id + '-x' + str(x)
            band = {'x': x, 'core': core, 'fringe': fringe, 'fragment_id': fragment_id,
                    'fragment_membership': [{'fragment_id': fragment_id, 'core': core, 'fringe': fringe}],
                    'status': 'identity_conflict', 'reason': reason,
                    'boundary_flags': flags(x, core + fringe, box),
                    'unassigned_band_refs': [], 'band_id': band_id,
                    'candidate_routes': candidate_routes}
            result['unassigned_bands'].append(band)
            for route in candidate_routes:
                row = result['routes'][route][x - box[0]]
                row['unassigned_band_refs'].append(band_id)
                row['status'] = 'identity_conflict'
                row['reason'] += ' Same-column candidate ink is retained once in an unassigned band; its identity is unresolved.'
    validate(result)
    if inputs != dependencies([script.name]):
        raise ValueError('Dependency changed during expansion')
    return result


def validate(data):
    box = data['target_box']
    used = set()
    for route in ('solid', 'dash'):
        assert [r['x'] for r in data['routes'][route]] == list(range(box[0], box[2]))
    for row in [r for rr in data['routes'].values() for r in rr] + data['unassigned_bands']:
        selected = row['core'] + row['fringe']
        for cls in ('core', 'fringe'):
            assert row[cls] == sorted(set(row[cls]))
            assert all(type(y) is int and box[1] <= y < box[3] for y in row[cls])
            assert sorted(y for p in row['fragment_membership'] for y in p[cls]) == row[cls]
        assert not set(row['core']) & set(row['fringe'])
        assert row['boundary_flags'] == flags(row['x'], selected, box)
        for y in selected:
            assert (row['x'], y) not in used
            used.add((row['x'], y))
    actual = [x for b in data['coverage']['raw_blocks'] for x in range(b['columns'][0], b['columns'][1]+1)]
    assert actual == list(range(data['context_box'][0], data['context_box'][2]))


SOLID = '''
315 - 0-1
316 - 2-3
317 0 1-3
318 0-1 2-3
319 0-2 3
320 2-3 1,4
321 2-3 4
322 3-4 2,5
323 4-6 3,7
324 5-6 4,7
325 6-7 5,8
326 7-9 6,10
327 8-10 7,11
328 10-11 9,12
329 11-13 10,14
330 12-15 11,16
331 14-16 13,17
332 15-17 14,18
333 17-19 16,20-21
334 18-20 17,21
335 20-21 19,22
336 21-23 20,24
337 22-25 21,26
338 24-26 23,27
339 25-27 28
340 27-29 26,30
341 28-31 27,32
342 30-32 29,33
343 31-33 30,34
344 33-35 32,36
345 34-36 33,37
346 36-38 35,39
347 37-39 40
348 39-41 38,42
349 40-42 39,43
350 42-44 41
351 43-45 42,46
352 44-47 43,48
353 46-48 45,49
354 48-50 47,51
355 49-52 48,53
356 51-53 50,54
357 53-55 52,56
358 54-56 53,57
359 55-58 54,59
360 57-60 56,61
361 59-61 58,62
362 60-62 63
363 62-64 61,65
364 63-66 62,67
365 65-67 64,68
366 66-69 65,70
367 68-70 67,71
368 70-72 69,73
369 71-74 70,75
370 73-76 72,77
371 74-78 73,79
372 76-79 75,80
373 78-80 77,81
374 79-82 78,83
375 81-84 80,85
376 83-85 82,86-87
377 84-87 83
378 86-87 85
379 - 87
'''

DASH = [
('F5-P-D02', '''
368 4-5 3,6
369 4-5 3,6
370 4-6 3,7
371 5-7 4,8
372 - 6-7
'''),
('F5-P-D03', '''
372 - 10-11
373 11-12 10,13-14
374 12-14 11,15
375 14-15 13,16
376 - 14-16
377 - 15-16
'''),
('F5-P-D04', '''
378 - 18-19
379 18-19 20
380 18-20 17,21-22
381 19-21 22
382 20-21 19,22
383 21-22 20,23
384 22-23 21,24
385 - 22-23
'''),
('F5-P-D05', '''
387 - 26-28
388 27-29 26,30
389 28-31 27,32
390 31-32 30,33
'''),
('F5-P-D06', '''
391 36 35,37
'''),
('F5-P-D07', '''
395 45 44,46
396 45-48 44,49-50
397 47-50 46,51
398 - 48-51
'''),
('F5-P-D08', '''
398 - 53-55
399 54-57 53,58-59
400 56-59 55,60
401 - 58-60
'''),
('F5-P-D09', '''
401 - 63-64
402 64-66 63,67
403 66-68 65,69
404 - 68-69
'''),
('F5-P-D12', '''
414 - 86-87
415 87 86
416 - 86-87
''')]

BANDS = [
('F5-P-U01', ['dash'], 'Blue-dash candidate and red stroke share purple/magenta ink at the top edge; local color ownership is unresolved. No solid-route candidate here.', '''
361 0 1
362 0-2 3
363 0-2 3
364 2 1,3
'''),
('F5-P-U02', ['dash'], 'Magenta transition precedes the separately legible blue dash; overlap with red makes exact dash attribution unresolved.', '''
367 4-5 6
'''),
('F5-P-U06', ['dash'], 'Blue broken descent contacts red shoulder ink; retain mixed material once without carrying either route through the crossing.', '''
392 37-38 35-36,39
393 38-41 37,42
394 - 37-41
'''),
('F5-P-U10', ['dash'], 'The candidate broken blue body coincides with red solid ink. Mixed-color cells do not uniquely establish blue dash ownership.', '''
404 - 72-75
405 73-76 72,77
406 75-78 74,79
407 77-79 76,80-81
'''),
('F5-P-U11', ['dash'], 'A later broken blue candidate meets red ink near the bottom boundary; preserve contact and clipping without a seam join or physical endpoint.', '''
408 81-83 80,84
409 82-85 81,86
410 84-86 83,87
411 86 85,87
412 - 86-87
413 - 87
''')]

COVERAGE = {
    'full_context_inspected': True, 'raw_context_cells': 10472,
    'raw_blocks': [
        {'columns': [308,315], 'receipt': '37a3b1'},
        {'columns': [316,331], 'receipt': '914dbc'},
        {'columns': [332,347], 'receipt': 'a85860'},
        {'columns': [348,363], 'receipt': '67abc9'},
        {'columns': [364,379], 'receipt': 'b58250'},
        {'columns': [380,395], 'receipt': 'fc5e1e'},
        {'columns': [396,411], 'receipt': '4edba0'},
        {'columns': [412,426], 'receipt': 'df9574'}],
    'actual_views': [
        {'path': '../../native-strips01/Im3.jpg', 'tool': 'view_image',
         'receipt': None, 'note': 'Whole unchanged 741x88 strip displayed; tool returned no separate receipt ID.'},
        {'path': '../../native-strips01/Im1.jpg', 'tool': 'view_image',
         'receipt': None, 'note': 'Whole unchanged companion strip displayed for F6.'},
        {'path': '../../render01/page-076.png', 'tool': 'view_image', 'receipt': None,
         'note': 'Whole page displayed resized from1700x2200 to1376x1780; orientation only, not native coordinates.'}],
    'prior_knowledge': 'Prospectively designated peer for both regions. Read main controls, skills, finite protocols, context helpers, numerical/human-review contracts and historical F5/F6 inventory/location correction. Prior inventory jq slice accidentally exposed historical F7 text (receipt9e481e); no F7 raw or new counterpart data read. No primary annotations inspected. Same underlying source as primary is not independent historical evidence.',
    'uncompleted_context': [], 'rows_inspected': [0,87],
    'target_route_rows': 230,
    'display_convention': 'Only exact RGB255,255,255 omitted; gN means exact N,N,N; inclusive equal-RGB runs. All displayed columns were untruncated.',
    'control_receipt': '37a3b1: fifteen read_context_v2 controls true before annotation saves'}


def build():
    return assemble('F5', 'Im3.jpg', [310,0,425,88], [308,0,427,88],
                    {'solid': [('F5-P-S01', SOLID)], 'dash': DASH}, BANDS,
                    COVERAGE, Path(__file__).resolve())


if __name__ == '__main__':
    before = dependencies([Path(__file__).name])
    value = build()
    target = Path(__file__).with_suffix('.json')
    with target.open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')
    if before != dependencies([Path(__file__).name]):
        raise ValueError('Input changed after save; preserve output as failed')
    print(json.dumps({'output': str(target), 'pin': pin(target), 'script_pin': pin(Path(__file__))}))
