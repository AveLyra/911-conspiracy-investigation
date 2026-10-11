"""E4 primary literal manual annotations. No pixel classifier or RGB reader.

The literal rows below were authored after the thirteen recorded context reads.
Expansion is syntactic only. Empty columns were inspected, not interpolated.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = [195, 0, 440, 92]
CONTEXT = [193, 0, 442, 92]

# x, confident rows, tentative rows; '-' denotes an empty set.
# S01 is a visually continuous gold solid local piece; conflicts break its
# attributable support without inventing invisible connecting cells.
SOLID = """
227 80-81 79,82
228 80 79,81
229 79 80
230 79 80
231 78-79 80
232 78 79
233 77 78
234 76-77 78
235 76 77
236 75 74,76
237 74-75 73,76
238 74 73,75
239 73-74 75
240 73 72,74
241 72 73
242 72 71,73
243 71 70,72
244 70-71 69,72
245 70 69,71
246 69-70 68,71
247 68-69 67,70
248 68 67,69
249 67-68 66,69
250 66-67 65,68
251 66 65,67
252 65-66 64,67
253 65 64,66
254 64-65 63,66
255 64 63,65
256 63 62,64
257 62-63 61
258 62 61,63
259 61 60,62
260 60-61 59
261 60 59,61
262 59-60 58,61
263 58-59 57,60
264 58 57,59
265 57-58 56,59
282 46-47 45,48
283 46-47 45,48
284 46 45,47
285 45-46 44,47
286 45 44,46
287 44 43,45
288 44 43,45
289 43 42,44
290 42-43 41,44
291 41-42 40,43
292 41 40,42
293 40 39,41
294 39-40 38,41
295 39 38,40
296 38-39 37,40
297 38 37,39
298 37-38 36,39
299 37 36,38
300 36-37 35,38
301 35-36 34,37
302 35 34,36
303 34-35 33,36
304 34 33,35
305 33-34 32,35
306 32-33 31,34
307 32 31,33
308 31-32 30,33
309 31 30,32
310 30-31 29,32
311 29-30 28,31
312 29 28,30
313 29 27-28,30
314 28 27,29
315 27-28 26,29
316 27 26,28
317 26-27 25,28
318 26 25,27
319 25-26 24,27
320 25 24,26
321 24 23,25
322 24 23
323 23 22
324 23 22
328 20-21 19,22
329 20-21 19,22
338 16 15,17
339 16 15,17
340 15-16 14,17
341 15 14,16
342 14-15 13,16
343 14 13,15
344 13-14 12,15
345 13 12,14
346 12-13 11,14
347 12-13 11,14
348 12 11,13
349 11-12 10,13
350 11 10,12
351 11 10,12
352 10-11 9,12
353 10 9,11
354 10 9,11
355 9-10 8,11
356 9 8,10
357 8-9 7,10
358 8-9 7,10
359 8 7,9
360 7-8 6,9
361 7-8 6,9
362 7 6,8
363 6-7 5,8
364 6-7 5,8
365 6 5,7
366 6 5,7
367 6 5,7
368 5 4,6
369 5 4,6
370 4-5 3,6
371 4 3,5
372 4 3,5
373 3-4 2,5
374 3 2,4
375 3 2,4
376 3 2,4
377 3 2,4
378 2-3 1
379 2 1
380 2 1
381 2 1
382 1-2 0
383 1 0,2
384 1 0,2
385 0-1 2
386 0 1
387 0 -
388 0 -
389 0 -
390 0 -
391 0 -
392 - 0
"""

# Separate distinguishable lower gold broken-line bodies. Literal provenance
# of uncertain early material is in CONFLICT, not an assumed dash continuation.
DASH = {
    'D01': """
284 - 56-57
285 56 57
286 56 55,57
287 55 54,56
288 55 54,56
289 54 55
290 54 53,55
291 - 53
""",
    'D02': """
293 - 50
294 50 49,51
295 50 49,51
296 49 48,50
297 48-49 50
298 48 47,49
299 47-48 49
300 - 47-48
""",
    'D03': """
302 - 45
303 45 44,46
304 44-45 43,46
305 44 43,45
306 43 42,44
307 42-43 41,44
308 42 41,43
309 - 41-43
""",
    'D04': """
312 - 39
313 39 38,40
314 38 37,39
315 38 37,39
316 37 36,38
317 36-37 35,38
318 36 35,37
319 - 35-36
""",
    'D05': """
321 - 33
322 33-34 32,35
323 33 32,34
324 32-33 31,34
325 31-32 30,33
326 31 30,32
327 30-31 29,32
328 - 30-31
329 - 30
""",
    'D06': """
331 28 27,29
332 27-28 26,29
333 27-28 26,29
334 26 25,27
335 26 25,27
336 26 25,27
337 - 25-26
""",
    'D07': """
340 23 22,24
341 22-23 21,24
342 22-23 21,24
343 21-22 20,23
344 21 20,22
345 20-21 19,22
346 20-21 19,22
347 - 20-21
""",
    'D08': """
349 - 17-18
350 17-18 16,19
351 17-18 16,19
352 16-17 15,18
353 16 15,17
354 16 15,17
355 15-16 14,17
356 - 15-16
""",
    'D09': """
358 - 12-13
359 13 12,14
360 12-13 11,14
361 12-13 11,14
362 12 11,13
363 11-12 10,13
364 11 10,12
365 - 10-11
366 - 10-11
""",
    'D10': """
368 9 8,10
369 9 8,10
370 8-9 7,10
371 8 7,9
372 8 7,9
373 7-8 6,9
374 - 7-8
""",
    'D11': """
377 - 6
378 6 7
379 5-6 7
380 5 6
381 4-5 6
382 4 5
383 4 5
384 - 4
""",
    'D12': """
386 - 3
387 3 4
388 3 4
389 2-3 4
390 2 3
391 2 3
392 2 3
393 - 2
""",
    'D13': """
395 - 1
396 1 0,2
397 0-1 2
398 0-1 2
399 0 1
400 0 1
401 - 0-1
402 - 0-1
""",
}

# name, candidate routes, literal rows, reason. Core here means confident
# visible ink, not confidence in model identity. These cells occur only here.
CONFLICT = [
('early-red-contact', ['solid'], """
208 90-91 -
209 90 89,91
210 89-90 88,91
211 89 88,90
212 89 88,90
213 88 87,89
214 88 87,89
215 87 86,88
216 86 87-88
217 85-86 84,87
218 85 84,86
219 84-85 83,86
220 84 85
221 84 85
222 83-84 85
223 83 82,84
224 82 83
225 82 81,83
226 81 80,82
""", 'Visible gold/orange contact with red ink; the local solid gold candidate is not uniquely separable. This does not implicate the gold dash route.'),
('green-contact', ['solid'], """
266 57-58 56,59
267 56-57 55,58
268 55-57 54,58
269 55-56 54,57
270 54-55 53,56
271 53-54 52,55
272 53-54 52,55
273 52-53 51,54
274 52 51,53
275 50-51 49,52
276 50-51 49,52
277 49-50 48,51
278 48-49 47,50
279 48-49 47,50
280 47-48 46,49
281 46-47 45,48
""", 'Gold approach overlaps green ink/compression. Visible mixed ink retained without transferring green cells to a confident gold route.'),
('lower-style-uncertain', ['dash'], """
275 - 62
276 - 62
277 - 62
278 - 61
279 - 60
""", 'Pale lower tan/gray material near other strokes may be a gold dash edge, but local style/ownership cannot be established. One isolated uncertainty piece per column; no assumed connected dash body.'),
('blue-contact', ['solid'], """
322 - 25
323 - 24
324 - 24
325 22-23 24
326 22-23 21,24
327 21-22 20,23
330 20 19,21
331 19-20 18
332 18-19 20
333 17-18 19
334 17-18 19
335 16-17 18
336 15-16 17
337 16-17 15
""", 'Gold solid candidate meets blue/purple stroke and cannot be separated uniquely in these cells. Dash candidate is not implicated.'),
('near-top-between-routes', ['solid', 'dash'], """
378 - 4-5
379 - 3-4
380 - 3-4
381 - 3
382 - 3
383 - 3
386 - 2
387 - 1-2
388 - 1-2
389 - 1
390 - 1
391 - 1
392 - 1
393 - 0-1
394 - 0-2
395 - 0
""", 'Gold edge/compression between approaching same-color routes cannot be assigned uniquely. Stored once; candidate routes reference these exact cells.'),
('top-trailing-pale', ['dash'], """
403 - 0-3
404 - 0-2
405 - 0-2
""", 'Very pale yellow-tinted top-edge residual after the lower dash body; visible values retained but body membership and attribution are unresolved.'),
]

RECEIPTS = [
    [193,202,'64969a'], [203,222,'c4bf50'], [223,242,'46c75f'],
    [243,262,'4e6db1'], [263,282,'d9c260'], [283,302,'9bf03a'],
    [303,322,'0caf72'], [323,342,'663b49'], [343,362,'a53b34'],
    [363,382,'89f220'], [383,402,'dccaed'], [403,422,'d184b4'],
    [423,441,'d37194'],
]


def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def rows(literal):
    out = []
    if literal != '-':
        for part in literal.split(','):
            ends = list(map(int, part.split('-')))
            out.extend(range(ends[0], ends[-1] + 1))
    assert out == sorted(set(out))
    assert all(0 <= y < 92 for y in out)
    return out


def literals(text):
    for line in text.splitlines():
        if line.strip():
            x, c, f = line.split()
            core, fringe = rows(c), rows(f)
            assert not set(core) & set(fringe)
            yield int(x), core, fringe


def flags(x, core, fringe):
    selected = set(core + fringe)
    return ([name for name, yes in [
        ('target_left', x == 195), ('target_right', x == 439),
        ('target_top', 0 in selected), ('target_bottom', 91 in selected)] if yes]
        if selected else [])


def record(x, core, fringe, fragment, reason, refs=None):
    refs = refs or []
    membership = ([{'fragment_id':fragment,'core':core,'fringe':fringe}]
                  if core or fringe else [])
    boundary = flags(x, core, fringe)
    status = ('boundary_truncated' if boundary else
              'identified_local_fragment' if core else 'fringe_only' if fringe else
              'identity_conflict' if refs else 'no_attributable_cells')
    return dict(x=x, core=core, fringe=fringe,
                fragment_id=fragment if membership else None,
                fragment_membership=membership, status=status, reason=reason,
                boundary_flags=boundary, unassigned_band_refs=refs)


def build():
    readcols = [x for a,b,_ in RECEIPTS for x in range(a,b+1)]
    assert readcols == list(range(193,442))
    routes = {r:{x:record(x,[],[],None,
        'All context rows inspected; no cells confidently or tentatively attributed to this local gold route. This is not absence, zero, an endpoint, or an inferred bridge.')
        for x in range(195,440)} for r in ('solid','dash')}
    for x,c,f in literals(SOLID):
        assert not routes['solid'][x]['core'] and not routes['solid'][x]['fringe']
        routes['solid'][x] = record(x,c,f,'E4P-S01',
            'Manually read local gold solid stroke; core is confident visible attribution and fringe is tentative edge/compression. Local identity is not transferred across strip seams or hidden cells.')
    for fragment, literal in DASH.items():
        for x,c,f in literals(literal):
            assert not routes['dash'][x]['core'] and not routes['dash'][x]['fringe']
            routes['dash'][x] = record(x,c,f,'E4P-'+fragment,
                'Manually read one distinguishable lower gold dash body. Fringe is tentative local edge/compression, not interpolation between bodies.')
    bands=[]
    for name,candidates,literal,reason in CONFLICT:
        for x,c,f in literals(literal):
            band_id=f'E4P-U-{name}-{x}'
            b=record(x,c,f,band_id,reason)
            b.update(band_id=band_id, candidate_routes=candidates, status='identity_conflict')
            bands.append(b)
            for r in candidates:
                e=routes[r][x]
                e['unassigned_band_refs'].append(band_id)
                if not e['core'] and not e['fringe']:
                    e['status']='identity_conflict'
                e['reason'] += ' Additional visible unresolved ink is retained once in the referenced same-column band.'
    for x in range(195,440):
        allsets=[set(routes[r][x]['core']+routes[r][x]['fringe']) for r in routes]
        allsets += [set(b['core']+b['fringe']) for b in bands if b['x']==x]
        for i,a in enumerate(allsets):
            for b in allsets[i+1:]:
                assert not a&b, (x,a&b)
    expected = {
        'PROTOCOL.md':'cc94c588f9b132318c7ca55fcffe1ed7eafbb92fd131583ffcbc74a13e5e54b7',
        'READERS.md':'6a019e587d1cdb47303047c5c03dbae4d9c347941a8227f27a7a8e0b8dfd0b5b',
        'read_context.py':'384d0bef93d4bc05ed8cb10f5a6d27426ab983ffcb4a3e31d5ca84b116961ac3',
        'context01.json':'783cd6f756918cef8a70ea79d925d7b010554b535f8d8f654970605d1c8b9095',
        'context02.json':'783cd6f756918cef8a70ea79d925d7b010554b535f8d8f654970605d1c8b9095',
        '../../native-strips01/Im10.jpg':'fe8c069f4bb7a19f6eb996b42b266c55552a110f8e9cbc6e9cc0d7269547cdd3',
        '../../render01/page-076.png':'0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
        '../PROTOCOL.md':'2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
        '../read_context.py':'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    }
    inputs={k:pin(HERE/k) for k in expected}
    assert all(inputs[k]['sha256']==v for k,v in expected.items())
    return dict(region_id='E4-Im10',pair='E4',source='Im10.jpg',reader='primary',
        target_box=TARGET,context_box=CONTEXT,inputs=inputs,
        script_pin=pin(Path(__file__)),coverage=dict(
            actual_complete_context_columns=[193,441],actual_rows=[0,91],
            context_cells=22908,route_column_records=490,
            read_receipts=[dict(first=a,last=b,exec_chunk_id=c,truncated=False)
                           for a,b,c in RECEIPTS],
            display='Only exact white omitted; inclusive equal-RGB row runs and gN=N,N,N; all other cells printed.',
            complete_source_orientation=True,other_new_annotations_seen=False,
            prior_knowledge='Instructions and full source orientation; no historical column-level E4 annotation read before assignment.',
            uncompleted_context_columns=[]),
        routes={r:list(entries.values()) for r,entries in routes.items()},
        unassigned_bands=bands,human_accepted=False,physical_support=None)


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--verify-only',action='store_true')
    args=parser.parse_args()
    output=build()
    content=json.dumps(output,sort_keys=True,indent=2)+'\n'
    target=HERE/'reader-E4-primary.json'
    if args.verify_only:
        assert target.read_text()==content, 'Expansion changed'
    else:
        with target.open('x') as file:
            file.write(content)
    print(json.dumps(dict(output=pin(target),script_pin=output['script_pin'],
        route_records=sum(map(len,output['routes'].values())),
        unassigned_records=len(output['unassigned_bands']),
        mode='verified_exact_reexpansion' if args.verify_only else 'exclusive_created')))
