"""E4 peer's manual native-cell reading; mechanical literal expansion only.

No RGB access, threshold, detector, interpolation or counterpart import occurs.
Every row token is a manually chosen inclusive native row run. Read coverage
and interpretive limits are in the companion notes, frozen before exchange.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = [195, 0, 440, 92]
CONTEXT = [193, 0, 442, 92]
EXPECTED = {
    'PROTOCOL.md': 'cc94c588f9b132318c7ca55fcffe1ed7eafbb92fd131583ffcbc74a13e5e54b7',
    'READERS.md': '6a019e587d1cdb47303047c5c03dbae4d9c347941a8227f27a7a8e0b8dfd0b5b',
    'read_context.py': '384d0bef93d4bc05ed8cb10f5a6d27426ab983ffcb4a3e31d5ca84b116961ac3',
    'context01.json': '783cd6f756918cef8a70ea79d925d7b010554b535f8d8f654970605d1c8b9095',
    'context02.json': '783cd6f756918cef8a70ea79d925d7b010554b535f8d8f654970605d1c8b9095',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../read_context.py': 'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    '../../native-strips01/Im10.jpg': 'fe8c069f4bb7a19f6eb996b42b266c55552a110f8e9cbc6e9cc0d7269547cdd3',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}

# x core fringe. '-' means none. Each table was authored after raw reading.
# Fragment boundaries preserve visibility interruptions; they do not assert
# that a hidden historical stroke begins or ends at the boundary.
SOLID = {
'peer-E4-solid-01': '''
226 80:81 82
227 80:81 79,82
228 80 79,81
229 79 78,80:81
230 78:79 80
231 78:79 80
232 77:78 79
233 77 76,78:79
234 76 75,77:78
235 75:76 74,77
236 75 74,76
237 74:75 73,76
238 74 73,75
239 73 72,74:75
240 73 72,74
241 72 71,73
242 - 70:73
243 71 70,72
244 70:71 69,72
245 70 69,71:72
246 69 68,70:71
247 68:69 67,70
248 68 67,69
249 67:68 66,69
250 66:67 65,68
251 66 65,67
252 65:66 64,67
253 65 64,66
254 64:65 63,66
255 64 63,65
256 63 62,64
257 62:63 61
258 61:62 60,63
259 61 60,62
260 60:61 59
261 60 59,61
262 59:60 58
263 58:59 57,60
264 58 57,59:60
265 57:58 56,59
''',
'peer-E4-solid-02': '''
272 53 52,54
273 52:53 51,54
274 52:53 51,54
''',
'peer-E4-solid-03': '''
282 46:47 45,48
283 46:47 45,48
284 46 45,47:48
285 45:46 44,47
286 44:45 46
287 44:45 43,46
288 43:44 42,45
289 43 42,44:45
290 42:43 41,44
291 41:42 40,43
292 41 40,42:43
293 40 39,41:42
294 39:40 38,41
295 39 38,40:41
296 38:39 37,40
297 37:38 36,39
298 37:38 36,39
299 36:37 35,38
300 36:37 35,38
301 35:36 34,37
302 35 34,36
303 34:35 33,36
304 34 33,35:36
305 33:34 32,35
306 32:33 31,34
307 32 31,33:34
308 31:32 30,33
309 31 30,32
310 30:31 29,32
311 29:30 28,31
312 29 28,30:31
313 28:29 27,30
314 28 27,29
315 27:28 26,29
316 27 26,28
317 26:27 25,28
318 26 25,27
319 25:26 24,27
320 25 24,26
321 24 23,25
322 23:24 22,25
323 23 22,24
324 23 22
''',
'peer-E4-solid-04': '''
328 20:21 19,22
329 20:21 19,22
''',
'peer-E4-solid-05': '''
336 17 16,18
337 16:17 18
338 16:17 15,18
339 16 15,17:18
340 15:16 14,17
341 15 14,16
342 14:15 13,16
343 14 13,15
344 13:14 12,15
345 13 12,14:15
346 12:13 11,14
347 12:13 11,14
348 12 11,13
349 11:12 10,13
350 11 10,12
351 11 10,12
352 10:11 9,12
353 10 9,11
354 10 9,11
355 9:10 8,11
356 9 8,10
357 8:9 7,10
358 8:9 7,10
359 8 7,9
360 7:8 6,9
361 7:8 6,9
362 7 6,8
363 6:7 5,8
364 6:7 5,8
365 6 5,7
366 6 5,7
367 5:6 4,7
368 5 4,6
369 4:5 3,6
370 4:5 3,6
371 4 3,5
372 4 3,5
373 3:4 2,5
374 3 2,4
375 3 2,4
376 3 2,4
377 3 2,4
378 2:3 1
379 2 1,3
380 2 1,3
381 2 1,3
382 1 0,2
383 1 0,2
384 1 0,2
385 0:1 2
386 0:1 2
387 0 -
388 0 -
389 0 -
390 0 -
391 0 -
392 0 -
''',
}

DASH = {
'peer-E4-dash-01': '''
284 - 56:57
285 56 57
286 56 55,57
287 55 54,56:57
288 54:55 56
289 54 55:56
290 - 54:55
''',
'peer-E4-dash-02': '''
293 - 50:51
294 50:51 49,52
295 50:51 49,52
296 49 48,50:51
297 48:49 50
298 48 49:50
299 48 47,49
300 - 47:48
''',
'peer-E4-dash-03': '''
302 - 44:45
303 45 44,46
304 44:45 43,46
305 44 43,45:46
306 43:44 42,45
307 43 42,44:45
308 42:43 41,44
309 - 41:43
''',
'peer-E4-dash-04': '''
312 - 39
313 38:39 37,40
314 38:39 37,40
315 38 37,39
316 37 36,38
317 36:37 35,38
318 36 35,37
319 - 36
''',
'peer-E4-dash-05': '''
321 - 33:34
322 33:34 32,35
323 32:34 31,35
324 32:33 31,34
325 31:32 30,33
326 31 30,32:33
327 30:31 29,32
328 - 30:31
''',
'peer-E4-dash-06': '''
330 - 29
331 28 27,29
332 28 27,29
333 27:28 26,29
334 26:27 25,28
335 26 25,27
336 26 25,27
337 - 25:27
''',
'peer-E4-dash-07': '''
340 - 22:23
341 22:23 21,24
342 22:23 21,24
343 21:22 20,23
344 21 20,22
345 20:21 19,22
346 - 20:21
''',
'peer-E4-dash-08': '''
349 - 18:19
350 17:18 16,19
351 17:18 16,19
352 16:17 15,18
353 16:17 15,18
354 16 15,17
355 16 15,17
356 - 15:16
''',
'peer-E4-dash-09': '''
358 - 12:14
359 13:14 12,15
360 12:13 11,14
361 12:13 11,14
362 12 11,13
363 11:12 10,13
364 11:12 10,13
365 - 11
''',
'peer-E4-dash-10': '''
368 9 8,10
369 9 8,10
370 8:9 7,10
371 8:9 7,10
372 8 7,9
373 7:8 6,9
374 - 7:8
''',
'peer-E4-dash-11': '''
377 - 6
378 6 5,7
379 5:6 4,7
380 5 4,6
381 4:5 6
382 4:5 3,6
383 4 3,5
''',
'peer-E4-dash-12': '''
386 - 3
387 3 4
388 3 4
389 2:3 4
390 2 3:4
391 2 3:4
392 2 3
''',
'peer-E4-dash-13': '''
396 1 2
397 0:1 2
398 0:1 2
399 0 1:2
400 0 1
401 0 1
402 - 0:1
''',
}

# Unassigned ink is stored once. Candidate lists are route-specific and no
# attribution entry duplicates these cells. Candidate solid alone can mean
# unresolved overlap with a non-E4 color; this schema does not encode those
# other-color owners. Core below means visible ink, not a resolved route.
UNASSIGNED = [
('early-red-gold', ['solid'], '''
208 - 90:91
209 - 89:91
210 - 89:91
211 - 88:90
212 - 88:90
213 - 88:89
214 - 87:89
215 - 86:88
216 - 86:88
217 - 85:87
218 - 84:87
219 - 84:86
220 - 84:85
221 - 83:85
222 - 83:85
223 - 82:84
224 - 82:84
225 - 81:83
''', 'Gold-compatible edge material adjoins red ink at the bottom approach; unique E4 cell attribution is unresolved. Only the locally continuous solid approach is a candidate here; no dashed-route inference.'),
('green-contact-a', ['solid'], '''
266 56 55,57:58
267 56 55,57:58
268 - 54:57
269 - 54:56
270 - 53:55
271 - 52:54
''', 'Gold/green contact prevents unique cell ownership for the solid approach. Green-colored ink is not assigned as a gold core.'),
('green-contact-b', ['solid'], '''
275 - 50:52
276 - 49:52
277 - 49:51
278 - 48:50
279 - 48:50
280 - 47:49
281 - 46:48
''', 'Solid-gold approach contacts green ink; olive and mixed fringes do not uniquely identify E4 cells.'),
('blue-contact-a', ['solid'], '''
325 - 21:23
326 - 20:23
327 - 20:22
''', 'The gold approach meets a blue body; mixed or overprinted cells remain unresolved for solid gold.'),
('blue-contact-b', ['solid'], '''
330 - 19:21
331 - 18:20
332 - 18:20
333 - 17:20
334 - 17:19
335 - 17:19
''', 'Blue overprint and gold-compatible fringe cannot be partitioned uniquely; candidate solid refers only to the possible E4 contribution, not ownership of the other color.'),
('upper-edge-shared', ['solid','dash'], '''
387 - 1:2
388 - 1:2
389 - 1
390 - 1
391 - 1
392 - 1
393 - 0:3
394 - 0:2
395 - 0:2
396 - 0
''', 'Same-color fringes approach the Im10 top edge and cannot be uniquely assigned between visible solid and dashed pieces; no seam continuation or endpoint is inferred.'),
]

RECEIPTS = [
    [193,207,'e0842d'], [208,227,'758c6a'], [228,247,'7d199e'],
    [248,267,'18e7b9'], [268,287,'20a9c0'], [288,307,'7c2427'],
    [308,332,'9c650e'], [333,357,'b5d29d'], [358,387,'4eb36a'],
    [388,414,'5881fd'], [415,441,'14151a'],
]


def pin(path):
    b = path.read_bytes()
    return {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}


def inputs():
    out = {p: pin(HERE/p) for p in EXPECTED}
    if any(out[p]['sha256'] != h for p,h in EXPECTED.items()):
        raise ValueError('A pinned dependency changed')
    return out


def rows(token):
    if token == '-':
        return []
    out = []
    for run in token.split(','):
        bounds = [int(v) for v in run.split(':')]
        a,b = bounds if len(bounds) == 2 else (bounds[0],bounds[0])
        if b < a:
            raise ValueError('Reversed manual row run')
        out.extend(range(a,b+1))
    if out != sorted(set(out)):
        raise ValueError('Unsorted/duplicate literal rows')
    return out


def lines(table):
    for line in table.strip().splitlines():
        x,core,fringe = line.split()
        yield int(x), rows(core), rows(fringe)


def flags(x,selected):
    return [name for name,yes in [
        ('target_left',x==195 and bool(selected)),
        ('target_right',x==439 and bool(selected)),
        ('target_top',0 in selected), ('target_bottom',91 in selected)] if yes]


def entry(x,core,fringe,fragment,reason,refs=None):
    selected = core+fringe
    boundary = flags(x,selected)
    status = ('boundary_truncated' if boundary else 'identified_local_fragment'
              if core else 'fringe_only' if fringe else 'identity_conflict'
              if refs else 'no_attributable_cells')
    return dict(x=x,core=core,fringe=fringe,
                fragment_id=fragment if selected else None,
                fragment_membership=[dict(fragment_id=fragment,core=core,fringe=fringe)] if selected else [],
                status=status,reason=reason,boundary_flags=boundary,
                unassigned_band_refs=refs or [])


def expand():
    routes = {}
    for route, tablemap in [('solid',SOLID),('dash',DASH)]:
        records = {}
        for fragment,table in tablemap.items():
            for x,core,fringe in lines(table):
                if x in records:
                    raise ValueError('Repeated attributed column')
                records[x] = entry(x,core,fringe,fragment,
                    'Manually read gold stroke' + (' with locally continuous solid style; no connection across an unresolved interval is asserted.' if route=='solid' else ' in a separately distinguishable dashed body; fringe is tentative edge/compression attribution and no dash gap is bridged.'))
        routes[route] = records
    bands = []
    for group,candidates,table,reason in UNASSIGNED:
        for x,core,fringe in lines(table):
            band_id = f'peer-E4-{group}-x{x}'
            b = entry(x,core,fringe,f'peer-E4-unassigned-{group}',reason)
            b.update(band_id=band_id,candidate_routes=candidates)
            if not b['boundary_flags']:
                b['status']='identity_conflict'
            bands.append(b)
            for route in candidates:
                r=routes[route].setdefault(x,entry(x,[],[],None,
                    'No uniquely attributable cells; see route-specific unresolved ink.',[band_id]))
                if band_id not in r['unassigned_band_refs']:
                    r['unassigned_band_refs'].append(band_id)
                    r['reason'] += ' Additional nearby ink remains unresolved in the referenced band.'
                if not r['core'] and not r['fringe']:
                    r['status']='identity_conflict'
    for route in routes:
        for x in range(195,440):
            if x not in routes[route]:
                reason = ('Inspected all context rows; no uniquely attributable gold '+route+' cells selected in this target column. Empty is not a zero curve, absence finding, or physical endpoint.')
                routes[route][x]=entry(x,[],[],None,reason)
        routes[route]=[routes[route][x] for x in range(195,440)]
    return routes,bands


def validate(routes,bands):
    for route,records in routes.items():
        assert [r['x'] for r in records] == list(range(195,440))
    for r in [r for records in routes.values() for r in records]+bands:
        assert 195 <= r['x'] < 440
        assert r['reason']
        for kind in ['core','fringe']:
            assert r[kind] == sorted(set(r[kind]))
            assert all(type(y) is int and 0 <= y < 92 for y in r[kind])
            assert sorted(y for m in r['fragment_membership'] for y in m[kind]) == r[kind]
        assert not set(r['core']) & set(r['fringe'])
        assert r['boundary_flags'] == flags(r['x'],r['core']+r['fringe'])
        assert bool(r['fragment_membership']) == bool(r['core']+r['fringe'])
    bandmap={b['band_id']:b for b in bands}
    for b in bands:
        assert b['core'] or b['fringe']
        for route in b['candidate_routes']:
            assert b['band_id'] in routes[route][b['x']-195]['unassigned_band_refs']
        for route in routes:
            r=routes[route][b['x']-195]
            assert not set(b['core']+b['fringe']) & set(r['core']+r['fringe'])
    for route,records in routes.items():
        for r in records:
            for ref in r['unassigned_band_refs']:
                assert bandmap[ref]['x']==r['x'] and route in bandmap[ref]['candidate_routes']
            if not r['core'] and not r['fringe'] and r['unassigned_band_refs']:
                assert r['status']=='identity_conflict'
    for x in range(195,440):
        a,b=routes['solid'][x-195],routes['dash'][x-195]
        assert not set(a['core']+a['fringe']) & set(b['core']+b['fringe'])


def build():
    before=inputs()
    routes,bands=expand()
    validate(routes,bands)
    assert (routes,bands)==expand()
    output=dict(region_id='E4-Im10',pair='E4',source='Im10.jpg',reader='peer',
                target_box=TARGET,context_box=CONTEXT,inputs=before,
                script_pin=pin(Path(__file__)),
                coverage=dict(context_columns_inclusive=[193,441],context_rows_inclusive=[0,91],
                              raw_context_cells=22908,route_records=490,
                              actual_read=True,uncompleted_context_columns=[],
                              exact_white_omission=True,finite_untruncated_receipts=RECEIPTS,
                              prior_knowledge='Prior-informed AI; own full Im10 and page76 orientation before raw blocks; no counterpart annotation read.',
                              aggregate_ownership_limitation='Route candidates concern E4 only. Other-color candidate owners are described in reasons, not represented as routes. Same-color shared fringe has aggregate route refs, not a member-specific ownership solver.'),
                routes=routes,unassigned_bands=bands,human_accepted=False,physical_support=None)
    assert before==inputs()
    return output


def main():
    output=build()
    assert output==build()
    payload=json.dumps(output,indent=2,sort_keys=True)+'\n'
    assert payload==json.dumps(output,indent=2,sort_keys=True)+'\n'
    with (HERE/'reader-E4-peer.json').open('x') as f:
        f.write(payload)
    print(json.dumps({'output':pin(HERE/'reader-E4-peer.json'),'route_records':sum(map(len,output['routes'].values())),
                      'unassigned_bands':len(output['unassigned_bands']),'manual_expansion_repeated_equal':True}))


if __name__=='__main__':
    main()
