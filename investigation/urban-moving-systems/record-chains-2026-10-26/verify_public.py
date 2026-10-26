"""Verify this publication's bytes/coverage, not historical conclusions."""
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent


def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def verify():
    groups = []
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
              and str(p.relative_to(ROOT)) not in {'MANIFEST.json', 'VERIFICATION.json'}}
    assert actual == set(manifest), (actual - set(manifest), set(manifest) - actual)
    for name, expected in manifest.items():
        assert pin(ROOT / name) == expected, name
    groups.append('publication file set and SHA-256/length pins match')

    provenance = json.loads((ROOT / 'PROVENANCE.json').read_text())
    for item in provenance['preserved_originals']:
        assert pin(ROOT / item['publication_copy']) == item['pin'], item
    groups.append('three preserved report/ledger/manifest copies match native-source pins')

    chains = json.loads((ROOT / 'preserved/chains.json').read_text())['claims']
    assert [c['id'] for c in chains] == [f'UMC{i:02}' for i in range(1, 12)]
    for item in chains:
        assert all(item.get(k) for k in ('source', 'finding', 'status',
                   'contrary_or_limit', 'next_input', 'discriminating_test'))
    groups.append('eleven existing chains retain sources, limits and discriminating inputs')

    text = (ROOT / 'README.md').read_text()
    assert len(re.findall(r'^## [1-6]\. ', text, re.M)) == 6
    for token in ('08:00', '08:58', '09:00-09:10', '08:50-09:00',
                  '08:50-09:03', '09:03-09:07', '09/23/2001', '09/19/2001',
                  '08:46:35am EST', '12:46:35am GMT', '08:29:00', '08:31:00',
                  '011001250 HC JD', '011001250 JD', 'K1966', 'K1967-K1978',
                  '76 black-and-white', '16 references: 15 CPU', 'E01889035',
                  'E01889036', 'E01889037', '13 assets', 'non-scientific'):
        assert token in text, token
    groups.append('all six explanations and specified conflicting values/counts retained')

    sources = json.loads((ROOT / 'SOURCES.json').read_text())['sources']
    assert {r['id'] for r in sources} >= {'P1', 'P3', 'P5', 'P6', 'WH', 'WA', 'S326'}
    for row in sources:
        assert row['url'].startswith('https://')
        assert row['access_date'] == '2026-10-26'
        assert re.fullmatch(r'[a-f0-9]{64}', row['sha256']), row['id']
        assert row['bytes'] > 0
    groups.append('seven source-copy records include URLs, access date and SHA-256')

    for name in ('README.md', 'RECORD.md'):
        body = (ROOT / name).read_text()
        assert not any(t in body for t in ('/Users/', '/Volumes/', 'PRIVATE KEY'))
        for link in re.findall(r'\]\(([^)]+)\)', body):
            if not link.startswith(('https://', '#')):
                if link == 'VERIFICATION.json' and not (ROOT / link).exists():
                    continue  # --record creates this receipt after the checks.
                assert (ROOT / link.split('#')[0]).is_file(), (name, link)
    groups.append('new public document links resolve; local user/store paths absent')

    native = json.loads((ROOT / 'NATIVE-PRESERVATION.json').read_text())
    assert native['verified_package_files'] == 24
    assert native['native_check']['groups'] == 7
    assert native['native_check']['prior_files_unchanged'] == 6
    assert native['native_check']['claims'] == 11
    assert 'new file mode 100644' in (ROOT / 'diffs/publication-additions.diff').read_text()
    groups.append('native check receipt and text-addition diff retained with explicit limits')
    return {'status': 'passed', 'groups': groups, 'files_checked': len(manifest),
            'claims': len(chains), 'explanations': 6,
            'limits': 'Checks bytes, document links and coverage only. Does not authenticate FBI custody, reproduce forensic analysis, or verify remote publication.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', action='store_true')
    args = parser.parse_args()
    result = verify()
    if args.record:
        output = ROOT / 'VERIFICATION.json'
        content = (json.dumps(result, indent=2) + '\n').encode()
        if output.exists():
            assert output.read_bytes() == content
        else:
            with output.open('xb') as stream:
                stream.write(content)
    print(json.dumps(result))
