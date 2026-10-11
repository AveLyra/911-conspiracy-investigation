"""Literal manual F6 peer selection; no RGB-dependent selection or gap bridge."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
HELPER_SHA = '7e5bf88b89275aab01f6c38e779b63f34ca4022b27af47660a8dab6198285565'


def helper():
    path = HERE / 'reader-F5-peer.py'
    if hashlib.sha256(path.read_bytes()).hexdigest() != HELPER_SHA:
        raise ValueError('Frozen peer helper changed')
    spec = importlib.util.spec_from_file_location('force56_peer_literal_helper', path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


DASH = [
('F6-P-D01', '''
282 - 86-87
283 87 86
284 86-87 85
285 85-86 84,87
286 84-85 83,86
287 83-84 82,85
288 - 82-84
'''),
('F6-P-D02', '''
290 - 80-81
291 81 80,82-83
292 81 80,82
293 80-81 79,82
294 79-80 78,81
295 78 77,79
296 77 76,78
297 - 76-77
'''),
('F6-P-D03', '''
298 73-74 72,75
299 73-74 72,75
300 73-74 72,75
301 73-74 72,75
302 73-74 72,75
303 - 74
'''),
('F6-P-D04', '''
305 - 68
306 68 67,69
307 67-68 66,69
308 66-67 65,68
309 65-66 64,67
310 65-66 64,67
311 66 65,67
312 - 66-67
'''),
('F6-P-D05', '''
313 - 69-70
314 70-71 69,72
315 70-72 69,73
316 71-73 70
317 72-74 71,75
318 73-75 72,76
319 74-75 73,76
320 - 74-76
'''),
('F6-P-D06', '''
322 - 77-78
323 77-78 76,79
324 78-79 77,80-81
325 79-81 78,82
326 81-82 80,83
327 - 81-83
''')]

BANDS = [
('F6-P-U03', ['dash'], 'Red broken crest approach contacts the green solid trace. Brown/olive ink cannot uniquely assign red membership; retain once and only the dash route is a candidate for F6.', '''
303 72-73 -
304 72 73
'''),
('F6-P-U07', ['dash'], 'A later red-dash candidate overlaps green ink at the native bottom edge. Preserve mixed cells as unresolved; no seam join or physical endpoint follows.', '''
326 86 87
327 86-87 -
328 - 87
''')]


def build():
    h = helper()
    before = h.dependencies(['reader-F5-peer.py', Path(__file__).name])
    coverage = {
        'full_context_inspected': True, 'raw_context_cells': 2590,
        'raw_blocks': [
            {'columns': [268,283], 'receipt': '03c618'},
            {'columns': [284,299], 'receipt': '6d8faf'},
            {'columns': [300,315], 'receipt': 'b28c5c'},
            {'columns': [316,331], 'receipt': '089e72'},
            {'columns': [332,341], 'receipt': '942719'}],
        'actual_views': h.COVERAGE['actual_views'],
        'prior_knowledge': h.COVERAGE['prior_knowledge'],
        'uncompleted_context': [], 'rows_inspected': [53,87],
        'target_route_rows': 140,
        'display_convention': h.COVERAGE['display_convention'],
        'control_receipt': h.COVERAGE['control_receipt']}
    result = h.assemble('F6', 'Im1.jpg', [270,55,340,88], [268,53,342,88],
                        {'solid': [], 'dash': DASH}, BANDS, coverage,
                        Path(__file__).resolve())
    # Include the complete helper dependency map, not merely its source pin.
    result['inputs'].update(before)
    if before != h.dependencies(['reader-F5-peer.py', Path(__file__).name]):
        raise ValueError('Dependencies changed during literal expansion')
    return result


if __name__ == '__main__':
    h = helper()
    before = h.dependencies(['reader-F5-peer.py', Path(__file__).name])
    value = build()
    target = Path(__file__).with_suffix('.json')
    with target.open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')
    if before != h.dependencies(['reader-F5-peer.py', Path(__file__).name]):
        raise ValueError('Input changed after save; preserve output as failed')
    print(json.dumps({'output': str(target), 'pin': h.pin(target),
                      'script_pin': h.pin(Path(__file__))}))
