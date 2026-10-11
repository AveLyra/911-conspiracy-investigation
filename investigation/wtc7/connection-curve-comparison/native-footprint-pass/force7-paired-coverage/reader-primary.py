"""Primary AI reading: literal cell expansion only, no RGB-based selection.

The literals below were authored after actual complete source/context reading.
The context RGB is used only for an exact-white diagnostic AFTER selection;
it never selects, filters, expands, removes or reassigns a cell.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED = {
    'PROTOCOL.md': 'aae8d37e8f0cda59f4c226e05c386f0dd73ace7b6954c7cd7ea81142f252ab19',
    'READERS.md': 'd62c0390fbb19bc507cb49a8da3d04802f1ad39e39784eb88ae27cc909424417',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../force56-remainder/READERS.md': 'e2508d4ca55ea9e6f06fef260a7ab17613ecbe533be47376c5c63264c436da2f',
    '../force56-remainder/independent_check.py': '326cd663a0e5bf8f9eefafb45d1421fa5f81056891a26228ad49168fc28665b0',
    '../read_context.py': 'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    '../approach34/read_context.py': '384d0bef93d4bc05ed8cb10f5a6d27426ab983ffcb4a3e31d5ca84b116961ac3',
    'read_context.py': '826e1bc24904d631b0b613ceea73b6ddc14b228438e77db751f291a60c717599',
    'context01.json': 'ff9f1f0e47b443994c6ba5325a1f2347c2522f48f2a79012b3c6d285bcb6874f',
    'context02.json': 'ff9f1f0e47b443994c6ba5325a1f2347c2522f48f2a79012b3c6d285bcb6874f',
    'context-check.json': '85445cc886a9e4e1bf9d6019d454a5b7c8450d56b182b84124fa16af411d70ad',
    'context_check.py': '41fc7d84f84372ee9f89f880c8a6e05f8ea0fdda53a67d34672a7a2f70a9fc8a',
    '../../native-strips01/Im2.jpg': '9f527c50ac92ef12454c550c66699773465cdc9aecfea55ca4130403166ae8e9',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
    '../../NUMERICAL-PROTOCOL.md': 'e03c47c1945b9eb9fd0a040d757d5f5f66bf76791ced8944323d3c92d1120df3',
    '../../HUMAN-REVIEW-GATE.md': '5c739ea10b6fe51b719a10205cef52737ff74cc29d1431272dd5dfea90d92c71',
    '../../native-strips01/receipt.json': '2cb27c3aeb27a9ef898d7d387984c030587a656273591a8d34ff4f8052514add',
    '../../extract_native_strips.py': '3836d008cf3ad4b0bc7c6216b12e4b1b39ce4a4cc0bef70491660d56a888d566',
    '../../pypdf-representation01.json': '1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5',
    '../../../../../../../911/authority/nist/wtc7/ncstar-1-9a.pdf': 'cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4',
    '../../../../../../../911/research/sherlock-wtc7-investigation/CHARTER.md': '54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
}

# Each line is x | manually selected core rows | manually selected fringe rows.
# Distinct bodies retain distinct IDs; missing columns are never interpolated.
BODIES = {
    'primary-dash-01': '''
232|83-84|81-82,85
233|81-83|79-80,84-85
234|79-81|77-78,82-84
235|78-79|77,80
''',
    'primary-dash-02': '''
236|73-75|72,76
237|72-74|71,75-76
238|71-73|70,74-75
239|71-72|70,73-75
240|70-71|69,72-73
241|70|69,71-73
''',
    'primary-dash-03': '''
250|61-62|59-60
251|59-62|57-58
252|58-60|57,61-62
253|58-59|57,60-61
''',
    'primary-dash-04': '''
256|60|57-59
257|58-60|57,61
258|55-59|54,60
259|54-57|53,58-59
260|55|54,56-57
''',
    'primary-dash-05': '''
262||56-57
263|56-57|55,58
264|56-57|54-55,58-59
265|55-57|54,58-59
266|53-56|52,57-58
267|53-54|52,55-56
''',
    'primary-dash-06': '''
269|49-50|48,51
270|49-50|48,51-52
271|50-51|49,52
272|51|49-50,52-53
273|50-51|49,52
274|50-51|48-49,52
275|50|49,51
''',
    'primary-dash-07': '''
276||46-47
277|46-47|45,48
278|46-47|45,48
279|46-47|45,48
280|46-47|44-45,48
281|44-46|43,47
282|44-46|43,47
''',
    'primary-dash-08': '''
284|40-41|39,42-43
285|40-41|39,42-43
286|40-42|39,43
287|41-42|40,43-44
288|42-43|40-41,44
289|41-43|40,44-45
290|41-42|40,43-44
''',
    'primary-dash-09': '''
292|36-38|35,39
293|35-37|34,38-39
294|34-36|33,37-38
295|34-35|33,36-38
296|34-35|33,36-37
297||34-36
''',
    'primary-dash-10': '''
299||31-33
300|31-32|30,33-34
301|30-32|29,33-34
302|30-31|29,32-33
303|30-31|29,32-33
304|30-31|32
305|30-31|32
''',
    'primary-dash-11': '''
309|25-27|24
310|24-26|23,27
311|23-24|22,25-26
312|23-24|22,25
313||23-24
''',
    'primary-dash-12': '''
315||22-23
316|21-23|20,24
317|21-22|20,23
318|20-22|19,23
319|20-21|19,22-23
320|20-21|19,22
321|20-21|19,22
322||20-21
''',
    'primary-dash-13': '''
323||16-17
324|14-17|13,18
325|13-15|12,16-17
326|12-14|11,15
327|12-13|11,14
328|12-13|14
''',
}

# x, local unresolved piece, candidate routes, core, fringe, actual reason.
# Band cells occur only here; they are NOT duplicated into either model.
BANDS = (
    (231, 'lead-01', ('dash',), '', '81-85', 'Pale green material before the first distinct broken body; body ownership remains tentative.'),
    (235, 'lead-02', ('dash',), '', '74-75', 'Separate pale upper piece near the next broken body; not pooled with the lower body in this column.'),
    (242, 'cap-02', ('dash',), '', '69-72', 'Pale lower cap distinct from the blue-contact band above; assignment to the preceding body unresolved.'),
    (242, 'blue-contact', ('dash',), '', '64-67', 'Mixed green/cyan/blue contact; no uniquely separable green footprint assigned.'),
    (243, 'blue-contact', ('dash',), '', '63-66', 'Mixed green/cyan/blue contact; no uniquely separable green footprint assigned.'),
    (244, 'blue-contact', ('dash',), '', '63-66', 'Mixed green/cyan/blue contact; no uniquely separable green footprint assigned.'),
    (245, 'blue-contact', ('dash',), '', '63-66', 'Mixed green/cyan/blue contact; no uniquely separable green footprint assigned.'),
    (246, 'blue-contact', ('dash',), '', '63-66', 'Mixed green/cyan/blue contact; no uniquely separable green footprint assigned.'),
    (247, 'blue-contact', ('dash',), '', '64-66', 'Mixed green/cyan/blue contact; no uniquely separable green footprint assigned.'),
    (248, 'blue-contact', ('dash',), '', '63-66', 'Mixed green/cyan/blue contact; no uniquely separable green footprint assigned.'),
    (249, 'lead-03', ('dash',), '', '58-62', 'Pale upper green piece near separation from blue; not used to connect through the contact.'),
    (250, 'blue-contact-tail', ('dash',), '', '63', 'Single mixed-colored cell between assigned green and the blue stroke; retained once as unresolved.'),
    (254, 'cap-03', ('dash',), '', '58-59', 'Gray-green terminal material is too weak for unique body attribution.'),
    (261, 'between-04-05', ('dash',), '', '55-58', 'Pale material between distinguishable broken bodies; no assumed connection.'),
    (268, 'lead-06', ('dash',), '', '49-50', 'Upper pale piece may lead the next body; kept separate from the lower cap candidate.'),
    (268, 'cap-05', ('dash',), '', '52-53', 'Lower pale cap may belong to the preceding body; not pooled with the upper piece.'),
    (283, 'lead-08', ('dash',), '', '40-42', 'Upper pale piece has unresolved ownership at the next body approach.'),
    (283, 'cap-07', ('dash',), '', '43-46', 'Lower pale piece has unresolved ownership near the preceding cap.'),
    (291, 'lead-09', ('dash',), '', '36-38', 'Upper pale piece may lead the next body; kept separate from the lower cap.'),
    (291, 'cap-08', ('dash',), '', '41-43', 'Lower pale piece may trail the previous body; no gap is filled.'),
    (298, 'cap-09', ('dash',), '', '34-35', 'Pale terminal material does not uniquely identify a broken-body continuation.'),
    (304, 'red-contact-upper-edge', ('dash',), '', '29', 'Yellow mixed edge between red and assigned green; no exclusive green ownership claimed.'),
    (305, 'red-contact-upper-edge', ('dash',), '', '29', 'Yellow mixed edge between red and assigned green; no exclusive green ownership claimed.'),
    (306, 'red-contact', ('dash',), '', '30-32', 'Green/red contact approach and pale cap remain unassigned; no hidden green stroke inferred.'),
    (307, 'red-contact', ('dash',), '', '26-30', 'Brown/red mixed crossing material; possible green participation does not establish separate ink.'),
    (308, 'red-contact', ('dash',), '', '24-29', 'Green flank meets red mixed pixels; attribution remains unresolved until the separated body.'),
    (314, 'between-11-12', ('dash',), '', '22-24', 'Pale material between two distinguishable broken bodies; not assigned a continuous trajectory.'),
    (328, 'solid-top-contact', ('solid',), '', '0-1', 'Brown/olive top-edge material near the entering green solid route; red overlap prevents unique attribution.'),
    (329, 'solid-top-contact', ('solid',), '', '0-2', 'Olive/brown mixed material at top and right crop edges; the clear green outside the target is context only.'),
    (329, 'dash-right-cap', ('dash',), '', '12-15', 'Pale broken-route cap at the right crop edge; neighboring red ink and clipping keep ownership unresolved.'),
)

BLOCKS = (
    (218, 225, '98cf50'), (226, 233, 'aef451'), (234, 241, '458262'),
    (242, 249, 'a98ad6'), (250, 257, '79f4a3'), (258, 265, '7eb01b'),
    (266, 273, '7b683a'), (274, 281, 'e73360'), (282, 289, '783327'),
    (290, 297, '8cb700'), (298, 305, '198623'), (306, 313, '8aa6fd'),
    (314, 321, '15c1cc'), (322, 329, '8f5a64'), (330, 331, 'a64e93'),
)


def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def inputs():
    result = {name: pin(HERE / name) for name in EXPECTED}
    for name, expected in EXPECTED.items():
        if result[name]['sha256'] != expected:
            raise ValueError('Frozen input changed: ' + name)
    for name in ('context01.json', 'context02.json'):
        context = json.loads((HERE / name).read_text())
        for dependency, expected in context['inputs'].items():
            if dependency not in result or result[dependency] != expected:
                raise ValueError('Context transitive input missing/changed: ' + dependency)
    return result


def rows(text):
    result = []
    for token in text.split(',') if text else []:
        bounds = list(map(int, token.split('-')))
        lo, hi = bounds if len(bounds) == 2 else (bounds[0], bounds[0])
        if not 0 <= lo <= hi <= 87:
            raise ValueError('Malformed literal rows')
        result.extend(range(lo, hi + 1))
    if len(result) != len(set(result)):
        raise ValueError('Repeated literal cell')
    return sorted(result)


def flags(x, selected):
    return [name for condition, name in (
        (x == 220, 'target_left'), (x == 329, 'target_right'),
        (0 in selected, 'target_top'), (87 in selected, 'target_bottom'))
        if selected and condition]


def row(x, core=(), fringe=(), fragment=None, reason='', refs=(), unresolved=False):
    core, fringe, refs = list(core), list(fringe), list(refs)
    selected = set(core) | set(fringe)
    boundary = flags(x, selected)
    status = ('identity_conflict' if refs or unresolved else
              'boundary_truncated' if boundary else
              'identified_local_fragment' if core else
              'fringe_only' if fringe else 'no_attributable_cells')
    membership = [{'fragment_id': fragment, 'core': core, 'fringe': fringe}] if selected else []
    return {'x': x, 'core': core, 'fringe': fringe, 'fragment_id': fragment if selected else None,
            'fragment_membership': membership, 'status': status, 'reason': reason,
            'boundary_flags': boundary, 'unassigned_band_refs': refs}


def validate(data):
    if (data['human_accepted'] is not False or data['physical_support'] is not None
            or data['reader'] != 'primary' or data['source'] != 'Im2.jpg'
            or data['region_id'] != 'F7-Im2-early' or data['target_box'] != [220, 0, 330, 88]):
        raise ValueError('Invalid provenance/acceptance')
    bands, occupied = {}, {}
    all_rows = list(data['unassigned_bands'])
    for route in ('solid', 'dash'):
        records = data['routes'][route]
        if [r['x'] for r in records] != list(range(220, 330)):
            raise ValueError('Incomplete route coverage')
        all_rows.extend(records)
    for entry in all_rows:
        x, c, f = entry['x'], entry['core'], entry['fringe']
        if not 220 <= x <= 329 or any(type(v) is not int or not 0 <= v <= 87 for v in c + f):
            raise ValueError('Cell outside target')
        if c != sorted(set(c)) or f != sorted(set(f)) or set(c) & set(f):
            raise ValueError('Invalid cell class sets')
        selected = set(c) | set(f)
        if occupied.setdefault(x, set()) & selected:
            raise ValueError('Duplicate route/band ink')
        occupied[x].update(selected)
        expected_members = ([{'fragment_id': entry['fragment_id'], 'core': c, 'fringe': f}]
                            if selected else [])
        if entry['fragment_membership'] != expected_members:
            raise ValueError('Membership mismatch')
        if selected and not entry['fragment_id']:
            raise ValueError('Missing fragment identity')
        if entry['boundary_flags'] != flags(x, selected) or not entry['reason'].strip():
            raise ValueError('Missing reason or wrong boundary flags')
        refs, status = entry['unassigned_band_refs'], entry['status']
        if refs != sorted(set(refs)):
            raise ValueError('Repeated/unsorted band references')
        if 'band_id' in entry:
            key = x, entry['band_id']
            if key in bands or not selected or refs or entry['candidate_routes'] not in (['solid'], ['dash'], ['solid', 'dash']):
                raise ValueError('Invalid unresolved band')
            if status != 'identity_conflict':
                raise ValueError('Unassigned band must retain conflict')
            bands[key] = entry
        else:
            expected = ('identity_conflict' if refs else 'boundary_truncated' if flags(x, selected)
                        else 'identified_local_fragment' if c else 'fringe_only' if f else 'no_attributable_cells')
            if status != expected:
                raise ValueError('Route status mismatch')
    for route in ('solid', 'dash'):
        for entry in data['routes'][route]:
            expected = sorted(bid for (x, bid), band in bands.items()
                              if x == entry['x'] and route in band['candidate_routes'])
            if entry['unassigned_band_refs'] != expected:
                raise ValueError('Nonreciprocal candidate-route reference')
    coverage = data['coverage']
    if ([x for a, b, _ in BLOCKS for x in range(a, b + 1)] != list(range(218, 332))
            or coverage['full_context_inspected'] is not True
            or coverage['raw_context_cells'] != 10032 or coverage['uncompleted_context'] != []):
        raise ValueError('Invalid coverage attestation')


def build():
    before = inputs()
    script_before = pin(Path(__file__))
    routes = {route: {} for route in ('solid', 'dash')}
    for route in routes:
        for x in range(220, 330):
            reason = ('Inspected the entire column; no locally separable F7 solid stroke attributed. '
                      'Other colors and compression are not assigned; this is not physical absence.' if route == 'solid' else
                      'Inspected the entire column; no local F7 broken-body cells attributed. '
                      'This does not fill a gap or assert absence of the generating curve.')
            routes[route][x] = row(x, reason=reason)
    for fragment, text in BODIES.items():
        for literal in text.strip().splitlines():
            x, core, fringe = literal.split('|')
            x, core, fringe = int(x), rows(core), rows(fringe)
            if routes['dash'][x]['fragment_membership']:
                raise ValueError('Repeated manual body column')
            routes['dash'][x] = row(x, core, fringe, fragment,
                'Manually attributed local green broken body using source style and neighboring inspected cells; '
                'core/fringe are subjective rendered-ink classes, not generating-curve bounds.')
    bands = []
    for x, local_id, candidates, core, fringe, reason in BANDS:
        band_id = 'primary-U-' + local_id
        band = row(x, rows(core), rows(fringe), band_id, reason, unresolved=True)
        band.update(band_id=band_id, candidate_routes=list(candidates))
        bands.append(band)
        for candidate in candidates:
            routes[candidate][x]['unassigned_band_refs'].append(band_id)
    for route in routes.values():
        for entry in route.values():
            if entry['unassigned_band_refs']:
                entry['unassigned_band_refs'].sort()
                entry['status'] = 'identity_conflict'
                entry['reason'] += ' Same-column unresolved band(s) retain candidate-specific reciprocal references.'
    data = {
        'region_id': 'F7-Im2-early', 'pair': 'F7', 'source': 'Im2.jpg', 'reader': 'primary',
        'target_box': [220, 0, 330, 88], 'context_box': [218, 0, 332, 88],
        'inputs': before, 'script_pin': script_before,
        'coverage': {
            'full_context_inspected': True, 'raw_context_cells': 10032,
            'raw_blocks': [{'columns': [a, b], 'receipt': 'exec_command chunk ' + receipt,
                            'truncated': False} for a, b, receipt in BLOCKS],
            'rows': [0, 87], 'uncompleted_context': [],
            'display_convention': 'read_context.py show; only exactly (255,255,255) omitted; gN=N,N,N; equal-RGB row runs inclusive.',
            'actual_views': [
                {'path': '../../native-strips01/Im2.jpg',
                 'receipt': 'functions.exec tools.view_image detail=original: first of two image outputs immediately after chunks d08fcd and 99d6e2; complete native 741x88 strip displayed.'},
                {'path': '../../render01/page-076.png',
                 'receipt': 'Same functions.exec tools.view_image call sequence: second of two outputs; complete page displayed; system resize notice 1700x2200 to1376x1780. No native coordinates read from resized page.'}],
            'prior_knowledge': 'AI reader envelope_arithmetic, primary. Prior knowledge of legend, numerical protocol, conditional-envelope packet and parent report of zero prior primary-shell F7 paired coverage; previously authored synthetic arithmetic and server tests. This is prior-informed target selection, not blind reading or an independent historical source. No counterpart new annotation, literals, notes or choices inspected.',
        },
        'routes': {key: list(value.values()) for key, value in routes.items()},
        'unassigned_bands': bands, 'human_accepted': False, 'physical_support': None,
    }
    validate(data)
    if before != inputs() or script_before != pin(Path(__file__)):
        raise ValueError('Inputs/script changed during literal expansion')
    return data


def diagnostics(data):
    # Diagnostic only, after manual selection: never modify selected cells.
    context = json.loads((HERE / 'context01.json').read_text())
    rgb = {(c['x'], c['y']): c['rgb'] for c in context['cells']['F7']}
    all_rows = data['routes']['solid'] + data['routes']['dash'] + data['unassigned_bands']
    white = [(r['x'], y) for r in all_rows for y in r['core'] + r['fringe']
             if rgb[r['x'], y] == [255, 255, 255]]
    return {'route_records': {k: len(v) for k, v in data['routes'].items()},
            'route_status_counts': {k: dict(Counter(r['status'] for r in v)) for k, v in data['routes'].items()},
            'route_cell_counts': {k: {cls: sum(len(r[cls]) for r in v) for cls in ('core', 'fringe')}
                                  for k, v in data['routes'].items()},
            'unassigned_band_records': len(data['unassigned_bands']),
            'unassigned_cells': sum(len(r['core']) + len(r['fringe']) for r in data['unassigned_bands']),
            'selected_exact_white_diagnostics': white, 'human_accepted': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--save', action='store_true')
    args = parser.parse_args()
    data = build()
    report = diagnostics(data)
    if args.save:
        target = HERE / 'reader-primary.json'
        with target.open('x') as stream:
            json.dump(data, stream, sort_keys=True, indent=2, allow_nan=False)
            stream.write('\n')
        if data['inputs'] != inputs() or data['script_pin'] != pin(Path(__file__)):
            raise ValueError('Changed inputs after save; preserve failed output')
        report['saved_output'] = pin(target)
    print(json.dumps(report, sort_keys=True))
