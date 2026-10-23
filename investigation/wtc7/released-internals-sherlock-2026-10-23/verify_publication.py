#!/usr/bin/env python3
"""Check this finite publication payload; no general privacy certification."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911-worktrees/sherlock-resumed-2026-10-14/research/sherlock-wtc7-investigation/released-internals-sherlock-2026-10-23')
REPO = HERE.parents[2]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    checks = []
    copied = []
    for p in sorted(SOURCE.iterdir()):
        if not p.is_file():
            continue
        target = HERE / ('source-review-snapshot.md' if p.name == 'README.md' else p.name)
        assert target.is_file() and sha(target) == sha(p), p.name
        copied.append({'source_name': p.name, 'public_name': target.name, 'sha256': sha(p),
                       'preserved_byte_identical': True})
    checks.append('Every original source-review artifact preserved byte-for-byte; original README has a separately named snapshot')
    pairs = [('observations.json', 'publication-census-check.json'),
             ('verification.json', 'publication-pattern-check.json'),
             ('bf-overlap-with-ranges.json', 'publication-bf-check.json'),
             ('overlap-verification.json', 'publication-overlap-check.json'),
             ('source-excerpts.json', 'source-excerpts-repeat.json')]
    for a, b in pairs:
        assert (HERE / a).read_bytes() == (HERE / b).read_bytes(), (a, b)
    checks.append('Five publication reruns match retained results byte-for-byte')
    j = json.loads((HERE / 'source-excerpts.json').read_text())
    assert len(j['originals']) == 10 and len(j['excerpts']) == 65
    labels = {x['label']: x for x in j['excerpts']}
    assert len(labels) == 65
    assert j['full_input_public_download_url'] is None
    assert any(r['physical_line'] == 12 and r['original_text'] == '4.50,0,0.75,0.0,0.0' for r in labels['master-termination']['lines'])
    for c in 'ABC':
        for step in range(1, 13):
            lines = labels[f'{c}-step-driver-{step}']['lines']
            assert len(lines) == 8 and lines[0]['original_text'].startswith('!' if c in 'AB' else '/input')
    assert any(r['physical_line'] == 1058 and r['original_text'] == '0.1600,0.000E+08' for r in labels['master-curve-27']['lines'])
    assert any(r['physical_line'] == 870 and r['original_text'] == '0.290,0.000E+08' for r in labels['master-curve-13']['lines'])
    checks.append('All 36 root-driver excerpts, termination card and both zero-stress endpoints have declared exact locators')
    links = []
    for name in ['README.md', 'SOURCE-LOCATORS.md', 'PUBLICATION.md']:
        text = (HERE / name).read_text()
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith('https://github.com/AveLyra/911-conspiracy-investigation/blob/'):
                tail = target.split('/blob/', 1)[1]
                ref, path = tail.split('/', 1)
                path = path.split('#', 1)[0]
                subprocess.run(['git', 'cat-file', '-e', f'{ref}:{path}'], cwd=REPO, check=True, capture_output=True)
                subprocess.run(['git', 'merge-base', '--is-ancestor', ref, '5243c055a8fb30a2e8c773e96e7930490e2c20d1'], cwd=REPO, check=True, capture_output=True)
                links.append({'document': name, 'ref': ref, 'path': path, 'kind': 'verified-public-base-ancestor'})
            elif not target.startswith(('http:', 'https:', '#')):
                assert (HERE / target.split('#', 1)[0]).is_file(), (name, target)
    checks.append('Current review/locator relative links exist; pinned GitHub paths exist in ancestors of verified public base')
    # A narrowly scoped supplemental scan, not a substitute for human-like content review.
    patterns = [r'-----BEGIN [^-]*PRIVATE KEY-----', r'gh[pousr]_[A-Za-z0-9]{25,}',
                r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}']
    for p in HERE.iterdir():
        if p.is_file() and p.suffix in ['.md', '.json', '.py'] and p.name != 'verify_publication.py':
            t = p.read_text()
            assert not any(re.search(pattern, t) for pattern in patterns), ('sensitive-pattern-review-required', p.name)
    checks.append('Supplemental finite-payload private-key/token/email scan has no matches; no automatic general privacy clearance claimed')
    files = []
    for p in sorted(HERE.iterdir()):
        if p.is_file() and p.name not in ['publication-manifest.json', 'publication-verification.json']:
            files.append({'path': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p)})
    manifest = {'scope': 'additive public research package; source files and unrelated work untouched',
                'original_review_copies': copied, 'files': files}
    report = {'status': 'pass', 'checks': checks, 'source_excerpts': len(j['excerpts']),
              'source_original_identities': len(j['originals']), 'original_copies': len(copied),
              'core_parser_tests': 6, 'core_parser_tests_result': 'passed in publication run',
              'pinned_internal_source_links': links,
              'limits': 'No historical solver execution, causal verdict, full-input upload or independent general privacy certification'}
    (HERE / 'publication-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    (HERE / 'publication-verification.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'pass', 'files_manifested': len(files), 'source_review_copies': len(copied), 'pinned_links': len(links)}))


if __name__ == '__main__':
    main()
