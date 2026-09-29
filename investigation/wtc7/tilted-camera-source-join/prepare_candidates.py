#!/usr/bin/env python3
"""Use the existing tested, hash-checked Camera2 decoder for one declared corpus."""
import argparse
import importlib.util
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
HELPER = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/multiview-onset-review/extract.py')
EXPECTED = 'df245c5fcf2790a45643c1fddf481bd38c63aed3592a4b0c9ad32819c23dc64c'


def main():
    p=argparse.ArgumentParser(); p.add_argument('--out', required=True); args=p.parse_args()
    if not re.fullmatch(r'[a-z][a-z0-9_-]*', args.out): raise ValueError('unsafe_output_name')
    output=HERE/args.out
    if output.exists(): raise ValueError('output_exists')
    spec=importlib.util.spec_from_file_location('existing_camera2_extractor', HELPER)
    ex=importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
    ex.require(ex.fingerprint(HELPER)['sha256'] == EXPECTED, 'helper_pin')
    source_spec=ex.SPECS['camera2']; rows, before=ex.inputs(source_spec)
    inputs={str(q):ex.fingerprint(q) for q in [HELPER, Path(__file__), HERE/'PROTOCOL.md',
              HERE/'SCENE-ADDENDUM.md', ex.FFMPEG]}
    selection={i:['scene-addendum-fixed-6500-through-7200'] for i in range(6500,7201)}
    output.mkdir()
    ex.write_json(output/'initial.json', {'inputs':inputs, 'source_inputs':before,
                  'selection_indices':list(selection), 'full_decode_count':len(rows)})
    try:
        report=ex.decode(ex.MEDIA/source_spec['name'], rows, 640,480,selection,output)
        ex.require(ex.inputs(source_spec)[1] == before, 'source_changed')
        ex.require(all(ex.fingerprint(Path(q)) == v for q,v in inputs.items()), 'inputs_changed')
        ex.write_json(output/'selection.json',report)
        ex.write_json(output/'receipt.json', {'status':'decoded_and_hash_verified_not_all_visually_reviewed',
                      'selected':len(report['images']), 'checked_frames':report['checked_frames'],
                      'selection_pin':ex.fingerprint(output/'selection.json'), 'inputs':inputs})
        print(json.dumps({'status':'pass', 'selected':len(report['images']),
                          'all_frame_hashes_checked':report['checked_frames'], 'diagnostics':report['diagnostics']}))
    except Exception as error:
        ex.write_json(output/'failure.json', {'status':'failed','error_type':type(error).__name__})
        raise


if __name__ == '__main__': main()
