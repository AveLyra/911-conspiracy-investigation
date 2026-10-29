"""Check supplied public PDF entities and selected extraction anchors, not historical truth.

Requires pypdf. Example:
python verify_sources.py --interview DOT-interviews.pdf --interview-text held-pypdf.txt --book AWA-570.pdf
The extraction argument is the complete held page-plus-formfeed derivative identified in SOURCES.json.
"""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import pypdf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interview', type=Path, required=True)
    parser.add_argument('--interview-text', type=Path, required=True)
    parser.add_argument('--book', type=Path, required=True)
    args = parser.parse_args()
    checks = []
    def check(name, condition, detail):
        checks.append({'name': name, 'passed': bool(condition), 'detail': detail})
    expected = [('interview', args.interview, '6c0b0be96d101becd3d1c00fb24e73ab517c2fa2bc475ec16e660eb2afc156a2', 4380), ('book', args.book, '255e4d8c3853ea0363c06808855e151093f97d624eeb53f1beb16ef80b0a330c', 65)]
    readers = {}
    for name, path, digest, count in expected:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        check(name + '_SHA256', actual == digest, actual)
        readers[name] = pypdf.PdfReader(path)
        check(name + '_pages', len(readers[name].pages) == count, len(readers[name].pages))
    derivative = args.interview_text.read_bytes()
    digest = hashlib.sha256(derivative).hexdigest()
    check('held_extraction_SHA256', digest == '5a894644399304097092528f9a2ca61f9532cc5c46f19d45c128095d30d04397', digest)
    pages = derivative.decode().split('\f')
    check('held_extraction_page_entities', len(pages) == 4381, len(pages))
    for number in range(3951, 3965):
        actual = readers['interview'].pages[number - 1].extract_text() or ''
        check('selected_page_extraction_' + str(number), actual.strip() == pages[number - 1].strip(), 'Exact stripped text equality; not image-reading or audio validation.')
    anchors = [(3954, 'technical problems with the tape recording'), (3960, 'which would not necessarily invalidate the previous bulletin'), (3960, 'try to hopefully collect out-dated information and destroy it as we produced the new stuff.'), (3961, 'It was the 12th or the 13th.')]
    for number, anchor in anchors:
        check('interview_anchor_' + str(number) + '_' + str(len(checks)), anchor in ' '.join(pages[number - 1].split()), anchor)
    for number in [7, 33]:
        text = readers['book'].pages[number - 1].extract_text() or ''
        joined = ' '.join(text.split())
        check('book_footer_' + str(number), 'AAT-20' in joined and '6:30AM' in joined, 'Selected extracted footer tokens; spacing follows derivative, image reading separate.')
    text = ' '.join((readers['book'].pages[26].extract_text() or '').split())
    check('book_page27_scoped_labels', 'Prepared by AAT-20 9/17 0900' in text and '10:04am ET' in text, 'Two separately scoped labels retained; no clock or event validation.')
    text = readers['book'].pages[0].extract_text() or ''
    check('book_graphic_cover_extraction_length', len(text) == 2, {'Unicode_characters': len(text), 'limit': 'Image visibly has title/date/source; text-search absence is not image absence.'})
    result = {'runtime': {'python': platform.python_version(), 'pypdf': pypdf.__version__}, 'checks': checks, 'passed': all(row['passed'] for row in checks), 'scope': 'Source-byte/page/extraction/selected-anchor reproducibility only. No native file/version/audio/custody authentication, original correction/action decision, execution/motive/legality or radar/clock/materials validation.'}
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] else 1)

if __name__ == '__main__':
    main()
