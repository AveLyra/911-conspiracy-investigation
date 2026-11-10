"""Source/bundle integrity and declared locator reproduction; not historical validation."""
from pathlib import Path
from html.parser import HTMLParser
import argparse
import hashlib
import json
import re


class Rows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.parts = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.active, self.parts = True, []
        if self.active and tag in ('td', 'th', 'br', 'p'):
            self.parts.append(' ')

    def handle_data(self, data):
        if self.active:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'tr' and self.active:
            self.rows.append(' '.join(''.join(self.parts).split()))
            self.active = False


def check(path, expected):
    data = Path(path).read_bytes()
    assert len(data) == expected['bytes'], str(path) + ' bytes differ'
    assert hashlib.sha256(data).hexdigest() == expected['sha256'], str(path) + ' SHA-256 differs'
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--source-pdf', type=Path)
    ap.add_argument('--locator-index', type=Path)
    ap.add_argument('--court-index', type=Path)
    args = ap.parse_args()
    manifest = json.loads((args.bundle / 'BUNDLE-HASHES.json').read_text())
    for item in manifest['files']:
        check(args.bundle / item['name'], item)
    sources = json.loads((args.bundle / 'SOURCES.json').read_text())
    scope = json.loads((args.bundle / 'SEARCH-SCOPE.json').read_text())
    obs = {x['id']: x for x in json.loads((args.bundle / 'OBSERVATIONS.json').read_text())}
    assert len(obs) == 7
    assert obs['RC01']['native_tape_or_receipt_recovered'] is False
    assert obs['RC02']['completed_direct_passenger_FBI_patch_proved'] is False
    assert obs['RC03']['preferred_network_state_or_cause_selected'] is False
    assert obs['RC04']['lost_calls_raw'] == '9:36 AM'
    assert obs['RC05']['end_raw'] == 'approximately 10:45a.m.'
    assert obs['RC05']['same_leg_as_RC04_or_operator_estimates_authenticated'] is False
    result = {'exit_code': 0, 'bundle_files_checked': len(manifest['files']),
              'source_pdf_bytes_verified': False, 'topic_index_reproduced': False,
              'court_index_reproduced': False, 'manual_image_readings_verified_by_code': False,
              'historical_call_tape_custody_clock_or_goal_authenticated': False}
    if args.source_pdf:
        check(args.source_pdf, sources['official_pdf'])
        result['source_pdf_bytes_verified'] = True
    if args.locator_index:
        data = args.locator_index.read_bytes()
        assert hashlib.sha256(data).hexdigest() == scope['ordinary_index_sha256']
        rows = json.loads(data)
        assert len(rows) == scope['index_rows']
        hits = []
        for row in rows:
            tags = [k for k, pattern in scope['patterns'].items() if re.search(pattern, row['ordinary_text'], re.I)]
            if ('recording' in tags or 'carrier' in tags) and any(x in tags for x in ('custody', 'notes', 'followup')):
                hits.append({'physical_page': row['physical_page'], 'tags': tags})
        assert hits == scope['part01_hits']
        result.update(topic_index_reproduced=True, topic_hit_pages=[x['physical_page'] for x in hits])
    if args.court_index:
        data = check(args.court_index, sources['court_index'])
        parser = Rows()
        parser.feed(data.decode('utf-8', 'replace'))
        assert len(parser.rows) == scope['court_parsed_rows']
        selected = [x for x in parser.rows if re.search(r'gronlund|glick|cassette|voicemail', x, re.I)]
        assert not [x for x in selected if re.search(r'gronlund|glick', x, re.I)]
        assert selected == [x['title'] for x in scope['court_generic_matches']]
        result.update(court_index_reproduced=True, parsed_court_rows=len(parser.rows), name_matches=0, generic_cassette_matches=len(selected))
    result['limit'] = 'Integrity and exact declared-index reproduction, not independent image transcription, native recording/custody authentication or calibrated timeline.'
    return result


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
