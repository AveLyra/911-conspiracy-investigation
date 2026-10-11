"""Dependency-only completion; preserve candidate producer, bytes and all samples."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRAFT_SHA = '48015d31f451d838ec4b3438e329edd3938a81507c25d537d9c877a88b3f23fe'
CANDIDATE_SHA = 'ceadeebf040913d5654c20bce5d55dca5ae2b7e4d6612821818f67af6024fb1c'


def import_candidate():
    path = HERE / 'packet.py'
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != DRAFT_SHA:
        raise ValueError('candidate producer changed')
    spec = importlib.util.spec_from_file_location('preserved_candidate_producer', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


draft = import_candidate()


def extend_closure(candidate, receipt, owner, method_files):
    result = copy.deepcopy(candidate)
    pins = dict(candidate['inputs'])
    draft.require(pins == candidate['inputs_after'], 'candidate pin drift')
    draft.include_declared(pins, receipt, owner)
    for path in method_files:
        draft.include(pins, path)
    after = {name: draft.pin(draft.BASE / name) for name in pins}
    draft.require(pins == after, 'repair input drift')
    result['inputs'], result['inputs_after'] = pins, after
    for key in candidate:
        if key not in ('inputs', 'inputs_after'):
            draft.require(result[key] == candidate[key], 'repair changed scientific payload')
    return result


def build():
    method_files = [HERE / name for name in
                    ('DEPENDENCY-REPAIR.md', 'packet_v2.py', 'test_packet_v2.py',
                     'packet01.json', 'packet02.json')]
    method_before = {}
    for path in method_files:
        draft.include(method_before, path,
                      CANDIDATE_SHA if path.suffix == '.json' else None)
    candidate = draft.build()
    raw = draft.encode(candidate)
    draft.require(hashlib.sha256(raw).hexdigest() == CANDIDATE_SHA, 'candidate replay differs')
    for name in ('packet01.json', 'packet02.json'):
        draft.require((HERE / name).read_bytes() == raw, 'preserved candidate differs')
    receipt = draft.load(draft.OLD / 'independent-check.json')
    result = extend_closure(candidate, receipt, draft.BASE, method_files)
    draft.require(all(result['inputs'][name] == expected for name, expected in method_before.items()),
                  'repair controls changed during candidate replay')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', choices=('01', '02'))
    args = parser.parse_args()
    result = build()
    path = HERE / ('packet-v2-' + args.run + '.json')
    draft.old.save(path, draft.encode(result))
    print(json.dumps({'file': path.name, 'pin': draft.pin(path),
                      'input_pins': len(result['inputs']), 'summary': result['summary']}, sort_keys=True))
