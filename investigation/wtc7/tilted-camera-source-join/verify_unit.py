#!/usr/bin/env python3
"""Read-only integrated preservation/repeat checks, not physical validation."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load(relative):
    return json.loads((HERE / relative).read_text())


def main():
    pins = {}
    comparisons = []
    def same(left, right):
        first, second = sha(HERE / left), sha(HERE / right)
        assert first == second, (left, right)
        pins[left], pins[right] = first, second
        comparisons.append([left, right])

    for filename in ['frames.json', 'receipt.json'] + [f'frame-{n:04d}.png' for n in [0,67,135,203,271,339,407,475]]:
        same('views01/' + filename, 'views02/' + filename)
    same('project01.json', 'project02.json')
    for filename in ['scores.json', 'summary.json', 'receipt.json']:
        same('scene01/' + filename, 'scene02/' + filename)
    for filename in ['comparison.json', 'summary.json', 'controls.json', 'receipt.json']:
        same('table01/' + filename, 'table02/' + filename)
    same('scene-independent01.json', 'scene-independent02.json')
    same('table-independent01.json', 'table-independent02.json')

    scene = load('scene01/receipt.json')
    for relative, expected in scene['inputs'].items():
        actual = sha(HERE / relative)
        assert actual == expected, relative
        pins[relative] = actual
    table = load('table01/receipt.json')
    for relative, expected in table['inputs'].items():
        actual = sha(HERE / relative)
        assert actual == expected['sha256'], relative
        assert (HERE / relative).stat().st_size == expected['bytes'], relative
        pins[relative] = actual
    for relative, expected in table['outputs'].items():
        path = HERE / 'table01' / relative
        assert sha(path) == expected['sha256'] and path.stat().st_size == expected['bytes']
    for relative, key in [('compare_project_table.py','producer'), ('project-table-controls.py','tests')]:
        assert sha(HERE / relative) == table[key]['sha256']

    data = load('table01/comparison.json')
    assert len(data['tracks']) == 8 and len(data['pairs']) == 48
    saved = [r for t in data['tracks'] for r in t['rows']]
    assert len(saved) == 334
    assert sum(not r['saved_keyFrame_member'] for r in saved) == 35
    assert sum(r['printed_time_rounding_0_01s_compatible'] for r in saved) == 5
    passing = [p['pair_id'] for p in data['pairs'] if p['displacement_summary']['all_available_compatible']]
    assert passing == ['pointmass01_Y_nw_y', 'pointmass02_X_ref_x', 'pointmass02_Y_ref_y', 'pointmass06_Y_ne_y', 'pointmass08_Y_wc_y']
    assert not any(p['absolute_summary']['all_available_compatible'] for p in data['pairs'])
    assert sum(p['counts']['shared_finite_nominal_time'] for p in data['pairs']) == 1512
    assert sum(p['counts']['shared_finite_printed_time_0_01s_compatible'] for p in data['pairs']) == 0
    pm05 = next(p for p in data['pairs'] if p['pair_id'] == 'pointmass05_Y_ec_y')
    assert pm05['displacement_summary']['available_count'] == 43
    assert pm05['displacement_summary']['print_enclosure_pass_count'] == 32
    failures = [r['saved']['frame'] for r in pm05['rows'] if r['displacement'] is not None and not r['displacement']['print_enclosure_compatible']]
    assert failures == [252,258,270,276,282,288,294,300,306,312,318]
    assert all(not r['saved']['saved_keyFrame_member'] for r in pm05['rows'] if r['saved'] and r['saved']['frame'] in failures)
    assert load('scene01/summary.json')['visual_candidate_union'] == [6613,6681,6748,6749,6817,6884,6952,7020,7088]
    assert all(sha(HERE / relative) == expected for relative, expected in pins.items())
    print(json.dumps({'status':'pass', 'scope':'preserved output equality, input pins and reported discrete counts; not independent scientific reproduction',
                      'repeat_file_pairs':comparisons, 'verified_pin_count':len(pins),
                      'verified_pin_map_sha256':hashlib.sha256(json.dumps(pins,sort_keys=True).encode()).hexdigest(), 'saved_rows':334,
                      'pairs':48, 'shared_finite_rows':1512, 'strict_time_passes_shared_rows':0,
                      'strict_nominal_grid_passes_all_saved_rows':5, 'pm05_failing_frames':failures}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
