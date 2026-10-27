"""Verify publication bytes, reported-value arithmetic and optional source pins.

No network, uploads, source edits or historical-authentication claim.
"""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--zip', type=Path)
    ap.add_argument('--notes', type=Path)
    ap.add_argument('--interviews', type=Path)
    args = ap.parse_args()
    base = Path(__file__).resolve().parent
    checks = []
    def check(label, condition):
        if not condition:
            raise AssertionError(label)
        checks.append(label)
    manifest = json.loads((base/'MANIFEST.json').read_text())
    for row in manifest['files']:
        data = (base/row['file']).read_bytes()
        check('sha256:'+row['file'], sha(data) == row['sha256'])
        check('bytes:'+row['file'], len(data) == row['bytes'])
    comp = json.loads((base/'CALL-COMPARISON.json').read_text())
    for row in comp['rows']:
        label = row['start_ed_t']
        check('minutes-to-seconds:'+label,
              60*row['commission_minutes']+row['commission_seconds_component'] == row['commission_seconds'])
        check('retained-difference:'+label,
              row['court_text_seconds']-row['commission_seconds'] == row['difference_seconds'])
    check('retained-159-versus-154', comp['rows'][2]['court_text_seconds'] == 159 and comp['rows'][2]['commission_seconds'] == 154)
    check('totals', sum(r['court_text_seconds'] for r in comp['rows']) == 795 and sum(r['commission_seconds'] for r in comp['rows']) == 790)
    if args.zip:
        from extract_swf_text import extract
        data = args.zip.read_bytes()
        check('official-distribution-acquired-version', sha(data) == '3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801')
        with zipfile.ZipFile(args.zip) as z:
            check('ZIP-CRC-all-members', z.testzip() is None)
            raw = z.read('AA77.swf')
        result = extract(raw)
        check('AA77-acquired-version', result['input_sha256'] == '844dfb545c8414f9e7da1edc89ffe090a09d00d721a2c65c820e15f5fe201a06')
        check('text-and-font-coverage', len(result['text_definitions']) == 548 and len(result['fonts']) == 14)
        by_id = {r['id']:r for r in result['text_definitions']}
        for pin in json.loads((base/'SWF-SOURCE-PINS.json').read_text())['pins']:
            check('source-text-definition:'+str(pin['id']), by_id[pin['id']] == pin)
    if args.notes or args.interviews:
        from pypdf import PdfReader
        if args.notes:
            check('notes-acquired-version', sha(args.notes.read_bytes()) == 'd59f7501da1899836bbe553e3e35fd056152046f2eae8050670f6424919869ad')
            text = ' '.join(PdfReader(args.notes).pages[6].extract_text().split())
            check('note57-154-source', '9:25:48 for 2 minutes, 34 seconds' in text)
            check('note57-matching-limit', 'do not allow for a determination' in text)
        if args.interviews:
            check('interviews-acquired-version', sha(args.interviews.read_bytes()) == 'e3cf374351cb753d1297433f86bb5807c56cb42a6dc69837a9df02dd0d54f4aa')
            reader = PdfReader(args.interviews)
            check('interview-scan-page-count', len(reader.pages) == 73)
            for n, snippets in {48:['Keyton','It was not a collect call','caller identification'],51:['Voss believes that both calls','collect calls'],49:['he did not look at his','watch']}.items():
                text = ' '.join(reader.pages[n-1].extract_text().split())
                for snippet in snippets:
                    check('interview-source:'+str(n)+':'+snippet, snippet in text)
    print(json.dumps({'status':'passed','checks':checks,'count':len(checks),
                      'source_mode':bool(args.zip or args.notes or args.interviews),
                      'limit':'Byte/source-pin/arithmetic verification only; visual review separately documented. No caller, duration, completeness or intent validation.'},indent=2))


if __name__ == '__main__':
    main()
