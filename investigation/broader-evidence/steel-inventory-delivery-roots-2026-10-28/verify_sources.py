"""Verify preserved entities and limited source-text locations, not historical acts."""
from pathlib import Path
import argparse
import hashlib
import json
import re
from pypdf import PdfReader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--input', action='append', required=True, help='ID=actual preserved PDF path')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    inputs = {}
    for entry in args.input:
        key, name = entry.split('=', 1)
        if key in inputs:
            raise ValueError('Duplicate source ID')
        inputs[key] = Path(name)
    pins = json.loads((args.directory / 'SOURCE-PINS.json').read_text())
    required = {x['id'] for x in pins}
    assert set(inputs) == required
    expected_pages = {'J05':4, 'J06':5, 'PA2005':63, 'LMDC2011':14, 'LMDC2012':14}
    readers = {}
    entities = []
    for pin in pins:
        key = pin['id']; path = inputs[key]; data = path.read_bytes()
        ok = data.startswith(b'%PDF-') and len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256']
        assert ok, key
        readers[key] = PdfReader(path)
        assert len(readers[key].pages) == expected_pages[key], key
        entities.append({'id':key, 'sha256':pin['sha256'], 'bytes':len(data), 'pages':len(readers[key].pages), 'passed':True})

    def normalized(key, n):
        return re.sub(r'\s+', '', readers[key].pages[n-1].extract_text() or '').lower()

    j05 = normalized('J05',3)
    pa05 = normalized('PA2005',6)
    later11 = normalized('LMDC2011',5)
    later12 = normalized('LMDC2012',5)
    j06 = normalized('J06',4)
    lookups = [
        {'id':'J05-delivery','passed':all(x in j05 for x in ['october2004','furnishedtolmdc','submittedtoshpo','writtenrequests'])},
        {'id':'PA2005-reported-year','passed':'completedinoctober2004' in pa05},
        {'id':'LMDC2011-reported-year','passed':'preparedandcompletedin2006' in later11},
        {'id':'LMDC2012-reported-year','passed':'preparedandcompletedin2006' in later12},
        {'id':'J06-later-plan','passed':all(x in j06 for x in ['onjune8','protectionprocedure','keyplan','june12']) and 'july2006' in normalized('J06',1)}]
    result = {'entity_checks':entities, 'source_locator_checks':lookups,
              'all_passed':all(x['passed'] for x in entities+lookups),
              'reported_completion_years':{'PA2005':2004,'J05':2004,'LMDC2011':2006,'LMDC2012':2006},
              'distinct_reported_years':sorted({2004,2006}),
              'new_full_page_images_read':9,
              'checks_scope':'Byte/page identity and limited source-text anchors with whitespace removed for navigation only. Original text is preserved. No inventory identity, delivery receipt, disposition, specimen origin, execution or historical cause is authenticated.',
              'actual_inventory_acquired':False, 'historical_test_completed':False}
    if args.output:
        with args.output.open('x') as f:
            json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'entity_checks':len(entities),'source_locator_checks':len(lookups),'all_passed':result['all_passed'],'reported_completion_years':result['reported_completion_years']},indent=2))
    if not result['all_passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
