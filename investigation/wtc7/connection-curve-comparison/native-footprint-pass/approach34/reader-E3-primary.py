"""Root's literal E3 reading; expansion never inspects image or selects RGB."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = {
 'PROTOCOL.md':'cc94c588f9b132318c7ca55fcffe1ed7eafbb92fd131583ffcbc74a13e5e54b7',
 'READERS.md':'6a019e587d1cdb47303047c5c03dbae4d9c347941a8227f27a7a8e0b8dfd0b5b',
 'read_context.py':'384d0bef93d4bc05ed8cb10f5a6d27426ab983ffcb4a3e31d5ca84b116961ac3',
 'context01.json':'783cd6f756918cef8a70ea79d925d7b010554b535f8d8f654970605d1c8b9095',
 'context02.json':'783cd6f756918cef8a70ea79d925d7b010554b535f8d8f654970605d1c8b9095',
 '../../native-strips01/Im10.jpg':'fe8c069f4bb7a19f6eb996b42b266c55552a110f8e9cbc6e9cc0d7269547cdd3',
 '../../render01/page-076.png':'0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}
# Each literal token is column:core/fringe. '-' means empty; commas enumerate
# rows. No RGB lookup, interpolation or threshold fills these instructions.
SOLID = '''
263:72/71,73 264:72/71 265:71/70,72 266:71/70 267:70/69,71
268:70/69,71 269:69/68,70 270:69/68,70 271:68,69/67 272:68/67,69
273:67,68/- 274:67/66,68 275:66,67/- 276:66/65,67 277:65,66/-
278:65/64,66 279:65/64,66 280:64/65 281:64/63,65 282:64/63
283:63/62,64 284:63/62 285:62/63 286:62/61,63 287:61,62/-
288:61/60,62 289:61/60,62 290:60/59,61 291:60/59,61 292:59,60/-
293:59/58,60 294:59/58,60 295:58/59 296:58/57,59 297:57,58/-
298:57/58 299:57/56,58 300:57/56 301:56/55,57 302:56/55,57
303:56/55 304:55/54,56 305:55/54,56 306:55/54 307:54/55
308:54/53,55 309:54/53,55 310:53/54 311:53/52,54 312:53/52
313:53/52 314:52/51,53 315:52/51,53 316:52/51,53 317:51,52/53
318:51/50,52 319:51/50,52 320:50,51/52 321:50/49,51 322:50/49,51
323:50/49,51 324:49,50/51 325:49/50 326:49/48,50 327:49/48,50
328:48,49/- 329:48/49 330:48/47,49 331:48/47,49 332:48/47,49
333:47,48/46 334:47/46,48 335:47/46,48 336:47/46,48 337:47/46,48
338:47/46,48 339:47/46 340:46/47 341:46/45,47 342:46/45,47
343:46/45,47 344:46/45 345:46/45 346:46/45 347:45/46
348:45/44,46 349:45/44,46 350:45/44,46 351:45/44,46
352:45/44 353:45/44 354:45/44 355:44,45/- 356:44/45 357:44/45
358:44/43,45 359:44/43 360:44/43 361:44/43 362:44/43 363:44/43 364:44/43
'''
EARLY_UNASSIGNED = '''
219:-/91 220:-/91 221:91/- 222:91/90 223:90/91 224:90/89,91
225:89/90,91 226:89/88,90 227:88,89/- 228:88/87,89 229:87/86,88
230:87/86,88 231:86/85,87 232:86/85,87 233:85/84,86
234:85/84,86 235:84,85/86 236:84/83,85 237:84/83,85
238:83/82,84 239:83/82,84 240:83/82,84 241:83/82,84
242:82/81,83 243:82/81,83 244:81/80,82 245:80,81/-
246:80/79,81 247:80/79 248:79/78,80 249:78/77,79
250:78/77,79 251:77/76,78 252:77/76,78 253:76/75,77
254:76/75,77 255:76/75 256:75/74,76 257:75/74,76
258:74/73,75 259:74/73,75 260:73/72,74 261:73/72,74 262:73/72
'''
DASH = '''
233:-/91 234:91/- 235:-/91
238:90/91 239:90/89,91 240:89,90/- 241:89/88,90 242:89/88
243:88/87,89 244:88/87,89
247:-/86,87 248:86/85,87 249:85,86/- 250:85/84,86
251:85/84,86 252:84/85 253:84/83,85 254:-/84
256:-/82,83 257:82/81,83 258:82/81,83 259:81/82
260:81/80,82 261:81/80 262:80/79,81 263:-/79,80
265:-/78 266:78/77,79 267:78/77,79 268:77/78
269:77/76 270:76,77/75 271:76/77 272:-/75,76,77 273:-/76
275:-/74,75 276:74/73,75 277:73,74/- 278:73/72,74
279:73/72,74 280:72/73 281:72/73 282:-/72,73
284:-/70,71 285:70/69,71 286:70/69,71 287:69/68,70
288:69/68,70 289:68,69/- 290:68/67,69 291:-/67,68 292:-/68
293:-/66,67 294:66/65,67 295:66/65,67 296:65/66
297:65/64,66 298:65/64,66 299:64/63,65 300:-/63,64,65
303:-/62,63 304:62/61,63 305:62/61,63 306:61/62
307:61/60,62 308:60,61/59 309:60/59,61 310:-/60
312:-/58,59 313:58/57,59 314:58/57,59 315:57,58/-
316:57/56,58 317:57/56,58 318:56,57/- 319:-/56,57
321:-/55,56 322:55/54,56 323:55/54,56 324:54,55/-
325:54/53,55 326:54/53,55 327:53,54/- 328:-/53,54
330:-/52,53 331:52/53 332:52/51,53 333:52/51
334:51/52 335:51/50,52 336:51/50,52 337:-/50,51
340:-/49,50 341:49/50 342:49/48,50 343:49/48,50
344:49/48,50 345:48/49 346:48/49 347:-/48
349:-/47,48 350:48/47,49 351:47/48 352:47/48
353:47/48 354:47/48 355:47/- 356:-/47
358:-/46 359:46/47 360:46/47 361:46/47 362:46/- 363:46/- 364:46/47
'''
DASH_BODIES = [(233,235),(238,244),(247,254),(256,263),(265,273),
 (275,282),(284,292),(293,300),(303,310),(312,319),(321,328),
 (330,337),(340,347),(349,356),(358,364)]
SHARED = '''352:-/46 353:-/46 354:-/46 355:-/46
359:45/- 360:-/45 361:45/- 362:45/- 363:45/- 364:45/-'''
RECEIPTS = [
 {'columns':[193,202],'receipt':'8b1d50'},
 {'columns':[203,222],'receipt':'bf16dc'},
 {'columns':[223,242],'receipt':'f647e5'},
 {'columns':[243,262],'receipt':'83eba9'},
 {'columns':[263,292],'receipt':'951be3'},
 {'columns':[293,326],'receipt':'38fcbd'},
 {'columns':[327,366],'receipt':'ea8868'},
]


def pin(p):
    raw = p.read_bytes()
    return {'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}


def literal(text):
    data = {}
    for token in text.split():
        col,sets = token.split(':'); x = int(col)
        if x in data: raise ValueError('Duplicate literal column')
        c,f = ([int(y) for y in part.split(',')] if part != '-' else []
               for part in sets.split('/'))
        if c != sorted(set(c)) or f != sorted(set(f)) or set(c)&set(f):
            raise ValueError('Literal classes')
        data[x] = (c,f)
    return data


def record(x,c,f,fragment,reason,refs=None,conflict=False):
    selected = set(c)|set(f); flags = []
    if selected:
        if x == 195: flags.append('target_left')
        if x == 364: flags.append('target_right')
        if 35 in selected: flags.append('target_top')
        if 91 in selected: flags.append('target_bottom')
    status = ('identity_conflict' if conflict else
              'boundary_truncated' if selected and flags else
              'identified_local_fragment' if c else 'fringe_only' if f else
              'identity_conflict' if refs else 'no_attributable_cells')
    return {'x':x,'core':c,'fringe':f,'fragment_id':fragment if selected else None,
            'fragment_membership':([{'fragment_id':fragment,'core':c,'fringe':f}]
                                   if selected else []),
            'status':status,'reason':reason,'boundary_flags':flags,
            'unassigned_band_refs':refs or []}


def build():
    before = {name:pin(HERE/name) for name in PINS}
    if any(before[name]['sha256'] != sha for name,sha in PINS.items()):
        raise ValueError('Changed dependency')
    s,d,u,shared = map(literal,(SOLID,DASH,EARLY_UNASSIGNED,SHARED))
    bands = []
    for x in range(195,365):
        for table,bid,routes,reason in [
          (u,'E3-early-contact',['solid'],
           'Early black-approach neighborhood with adjacent colored/broken strokes; this reader conservatively leaves model ownership unresolved, not all ink intrinsically inseparable.'),
          (shared,'E3-near-contact',['solid','dash'],
           'Intervening black ink has unresolved ownership between the two nearby local traces; recorded once.')]:
            if x in table:
                c,f = table[x]
                b = record(x,c,f,bid,reason,conflict=True)
                b.update(band_id=bid,candidate_routes=routes)
                if table is u:
                    b['other_possible_origins'] = ['neighboring colored stroke','compression fringe']
                bands.append(b)
    routes = {'solid':[],'dash':[]}
    for route,table in [('solid',s),('dash',d)]:
        for x in range(195,365):
            c,f = table.get(x,([],[]))
            refs = [b['band_id'] for b in bands if b['x']==x and route in b['candidate_routes']]
            fragment = 'E3-solid-a' if route=='solid' else next(
                (f'E3-dash-{i:02d}' for i,(a,b) in enumerate(DASH_BODIES) if a<=x<=b),None)
            reason = ('Locally identified solid black approach; no seam or hidden continuation inferred.'
                      if route=='solid' else 'Locally distinct lower black dash body; no bridge across gaps.')
            if not(c or f):
                reason = ('Inspecting the complete context did not support a route-specific cell assignment; '
                          'this is not absence or zero physical support.')
            if refs: reason += ' Additional unresolved ink is referenced, not duplicated.'
            routes[route].append(record(x,c,f,fragment,reason,refs))
    if before != {name:pin(HERE/name) for name in PINS}:
        raise ValueError('Input changed during expansion')
    return {'region_id':'E3-Im10','pair':'E3','source':'Im10.jpg','reader':'primary',
       'target_box':[195,35,365,92],'context_box':[193,33,367,92],
       'inputs':before,'script_pin':pin(Path(__file__)),
       'coverage':{'full_context_inspected':True,'raw_context_cells':10266,
          'raw_blocks':RECEIPTS,'whole_strip_and_page_viewed':True,
          'prior_informed_ai':True,'counterpart_new_annotation_read':False,
          'earlier_complete_image_orientation_repeated_this_turn':True},
       'routes':routes,'unassigned_bands':bands,'human_accepted':False,
       'physical_support':None,
       'limits':'Manual native-ink selections, not calibrated pre-raster bounds. Early conservative nonassignment is reader uncertainty, not universal source impossibility. Band IDs group uncertainty and do not assert continuous physical fragments. Dash-body membership including fringe-only tips is tentative; adjacent body07/08 pale tails are not joined.'}


if __name__ == '__main__':
    result = build()
    target = HERE/'reader-E3-primary.json'
    with target.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False); f.write('\n')
    print(json.dumps({'output':pin(target),'route_records':340,'bands':len(result['unassigned_bands'])}))
