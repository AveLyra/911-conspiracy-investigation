"""Additional name-only predicates using the previously bounded locator."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
PATTERNS = {
    'wtci_120_i': r'WTCI[-_ ]*0*120[-_ ]*I(?:[^A-Za-z0-9]|$)',
    'foia_12_178': r'FOIA[-_ ]*12[-_ ]*178(?:[^0-9]|$)',
    'export_folder': r'120806[_-]1247(?:[^0-9]|$)',
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, choices=('identifiers01', 'identifiers02'))
    args = parser.parse_args()
    out = HERE / args.out
    if out.exists():
        raise FileExistsError('Refusing existing identifier output')
    spec = importlib.util.spec_from_file_location('name_locator', HERE / 'locate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    deps = [HERE/'PROTOCOL.md', HERE/'IDENTIFIER-ADDENDUM.md', HERE/'locate.py',
            Path(__file__), Path(sys.executable)]
    before = {str(p): module.pin(p) for p in deps}
    module.TERMS = {k: re.compile(v, re.I) for k, v in PATTERNS.items()}
    module.INVENTORY_TERM = re.compile('|'.join('(?:'+v+')' for v in PATTERNS.values()), re.I)
    result = module.run()
    after = {str(p): module.pin(p) for p in deps}
    assert before == after
    out.mkdir()
    with (out/'results.json').open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    with (out/'receipt.json').open('x') as stream:
        json.dump({'before': before, 'after': after, 'python': sys.version,
                   'results': module.pin(out/'results.json')}, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'roots': len(result['roots']),
                      'path_matches': sum(len(r['matches']) for r in result['roots']),
                      'member_matches': sum(len(a.get('matches', [])) for r in result['roots'] for a in r['zip_metadata']),
                      'inventory_matches': sum(len(i['matches']) for i in result['canonical_inventories']),
                      'results': module.pin(out/'results.json')}))


if __name__ == '__main__':
    main()
