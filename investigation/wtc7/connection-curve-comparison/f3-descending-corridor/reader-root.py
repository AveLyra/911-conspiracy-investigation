"""Expand literal manual row runs; no image classification or measurement fit."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Each line is a manual native-column reading: x, core rows, fringe rows.
# Inclusive runs and commas preserve exact membership. A dash means empty.
SOLID = '''
272 0 1
273 0-2 -
274 1-3 -
275 2-4 5
276 3-5 6
277 5-6 4,7
278 6-7 5,8-9
279 7-9 6,10
280 8-10 11
281 10-11 9,12
282 11-12 10,13-14
283 12-14 11,15
284 13-15 12,16
285 15-16 14,17
286 16-17 15,18-19
287 17-19 16,20
288 18-20 21
289 20-21 19,22
290 21-23 20
291 22-24 21,25
292 24-25 23,26
293 25-26 24,27-28
294 26-28 25,29
295 27-29 30
296 29-30 28,31
297 30-32 29
298 31-33 30,34
299 33-34 32,35
300 34-35 33,36
301 35-37 34,38
302 37-38 35-36,39-40
303 38-40 37,41
304 39-41 38,42
305 41-42 39-40,43
306 42-44 41,45
307 44-45 43,46
308 45-47 44,48
309 46-48 45,49-50
310 48-50 47,51
311 49-51 52
312 51-52 50,53
313 52-54 51,55
314 53-55 52,56
315 55-56 54,57-58
316 56-58 55,59-60
317 58-59 57,60-61
318 59-61 58,63
319 60-62 63
320 62-64 61,65
321 64-65 62-63,66
322 65-67 64
323 66-68 65,69
324 68-70 67,71
325 69-71 72
326 71-73 70,74
327 72-74 75
328 74-76 73,77
329 75-77 78
330 77-78 76,79
331 78-79 77,80
332 79-80 78,81
333 80-81 82
334 81-82 80,83
335 82-83 81,84-85
336 83-84 82,85
337 84-85 83,86
338 85-86 84,87
339 86-87 85
340 87 86
341 - 87
'''
# x, reader-local fragment, core rows, fringe rows. Multiple lines at one x
# retain distinct fragments and do not fill intervening rows.
DASH = '''
294 d01 - 0
295 d01 - 0-1
296 d01 0 1
297 d01 0 1
298 d01 0-1 2
299 d01 1-2 0,3
300 d01 2-3 1
301 d02 7 6,8
302 d02 7-8 6,9
303 d02 8-9 7,10
304 d02 9-11 8
305 d02 11-12 9-10
306 d02 - 11-12
307 d02 - 12
307 d03 - 15-17
308 d03 15-17 18
309 d03 17-18 15-16,19-20
310 d03 18-20 17
311 d03 19-20 21
312 d03 20-21 19,22
313 d03 - 20-21
314 d04 24 23,25-26
315 d04 24-27 23,28
316 d04 26-29 25,30
317 d04 28-29 27,30
318 d05 33 32,34
319 d05 33-34 32,35
320 d05 34-35 33,36
321 d05 35-37 34,38
322 d05 36-38 35,39-40
323 d05 38 37,39
323 d06 - 41-42
324 d06 42-43 41,44
325 d06 43-45 41-42,46
326 d06 45-47 44,48
327 d06 46-47 45,48-49
328 d06 - 46-49
329 d07 - 51-52
330 d07 51-53 50,54-56
331 d07 53-56 52,57
332 d07 55-57 54,58
333 d07 - 57
333 d08 61 60,62
334 d08 61-63 60,64
335 d08 62-64 61,65
336 d08 64-65 63,66
337 d08 65-66 64,67
338 d08 - 66-67
338 d09 - 69-70
339 d09 70-71 69,72
340 d09 70-72 73
341 d09 72-73 71,74
342 d09 73-74 72
343 d09 73-74 75
344 d09 - 73-74
346 d10 77 76,78
347 d10 77-78 76,79-80
348 d10 78-80 77,81
349 d10 79-80 78,81
350 d10 80-81 79
351 d10 80-81 82
352 d10 - 81-82
353 d11 - 84
354 d11 84-85 83,86
355 d11 84-86 87
356 d11 86-87 85
357 d11 87 86
358 d11 - 87
'''


def rows(text):
    if text == '-':
        return []
    out = []
    for part in text.split(','):
        limits = list(map(int, part.split('-')))
        assert len(limits) in (1, 2)
        out.extend(range(limits[0], limits[-1] + 1))
    assert out == sorted(set(out)) and all(0 <= y <= 87 for y in out)
    return out


def main():
    source = HERE.parent / 'native-strips01/Im4.jpg'
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    assert sha(source) == '53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd'
    assert sha(HERE/'PROTOCOL.md') == '12525bcb149368f18d85e3611f32137ccdeef723cc95df93cf2b5d9b13f2aa27'
    assert sha(HERE/'raw-context.json') == 'd8836b922545220c5e0ac83e33e3bea81bb3f0ce8726fd73899f291cdb0d6f2f'
    selected = {}
    for line in SOLID.splitlines():
        if line.strip():
            x, core, fringe = line.split()
            selected[('solid', int(x))] = [('s01', rows(core), rows(fringe))]
    for line in DASH.splitlines():
        if line.strip():
            x, fragment, core, fringe = line.split()
            selected.setdefault(('dash', int(x)), []).append((fragment, rows(core), rows(fringe)))
    result = []
    for route in ['solid', 'dash']:
        for x in range(270,360):
            pieces = selected.get((route,x), [])
            core = sorted({y for _, c, _ in pieces for y in c})
            fringe = sorted({y for _, _, f in pieces for y in f})
            assert not set(core) & set(fringe)
            outside = []
            if 0 in core + fringe:
                outside.append('strip_top')
            if 87 in core + fringe:
                outside.append('strip_bottom')
            if core or fringe:
                if x == 270: outside.append('target_left')
                if x == 359: outside.append('target_right')
            status = ('boundary_truncated' if outside else 'identified_local_fragment' if core else
                      'fringe_only' if fringe else 'no_attributable_cells')
            note = ('Local continuous neutral descending stroke; pale edge attribution remains subjective.' if route=='solid' else
                    'Local broken neutral descending pattern; fragment IDs do not connect across gaps.')
            if not pieces:
                note = 'No cells attributed to this route in inspected native column; not a verified gap or physical zero. Other color/compression marks remain unassigned.'
            if outside:
                note += ' Selected cells touch a strip edge; no endpoint or inter-strip continuity inferred.'
            if len(pieces)>1:
                note += ' Two separate tentative or visible dash pieces share this column; keep row sets separate.'
            result.append({'route':route,'column':x,'core_rows':core,'fringe_rows':fringe,
                           'status':status,'note':note,'boundary_flags':outside,
                           'fragment_id':pieces[0][0] if len(pieces)==1 else None,
                           'fragment_membership':{f:{'core_rows':c,'fringe_rows':r} for f,c,r in pieces}})
    assert len(result)==180
    record={'reader':'Root AI, prior-informed; separately frozen before reading corridor peer annotation',
            'source_sha256':sha(source),'protocol_sha256':sha(HERE/'PROTOCOL.md'),
            'raw_context_sha256':sha(HERE/'raw-context.json'),'transcription_sha256':sha(Path(__file__)),
            'coverage':{'native_strip':'Full unchanged Im4 viewed at original detail.',
                        'composed_page':'Complete page076 viewed; tool resized1700x2200 to1376x1780, not used for native coordinates.',
                        'raw_blocks_inclusive':[[270,284],[285,314],[315,344],[345,361],[268,269]],
                        'tool_receipts':['0ba3ea','f14307','9ca38c','921bbc'],
                        'rows_each_block':[0,87],'display':'All nonwhite triples shown, omitted cells exactly255 eachchannel; no output truncation observed.'},
            'method':'Manual row membership from full native stroke shapes, neighboring columns and exact RGB. Literal runs expand mechanically without any pixel selection algorithm. Local neutral black patterns are separated from the colored route at later columns; color/position alone do not establish model identity. Earlier14root/peer annotations known from completed stage; their narrowboxes are not copied as independent evidence.',
            'limits':['Core/fringe is subjective raster attribution, not calibrated centerline uncertainty.',
                      'Unassigned pale cells can contain true edges; omission is not proven background.',
                      'Local solid/dash identity remains provisional; no crossings or seams joined.',
                      'No physical ordinates, support domain, confidence interval or causal comparison.'],
            'observations':result,'human_accepted':False}
    with (HERE/'reader-root.json').open('x') as stream:
        json.dump(record,stream,indent=2,allow_nan=False); stream.write('\n')
    print(json.dumps({'entries':len(result),'sha256':sha(HERE/'reader-root.json')}))


if __name__=='__main__':
    main()
