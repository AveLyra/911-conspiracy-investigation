"""Verify this finite text supplement; no network, source repair or history edits."""
from pathlib import Path
import hashlib, json, re, sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent

def verify():
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    names = {r['file'] for r in manifest['files']}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    assert actual == names | {'MANIFEST.json'}, 'Unexpected or missing public file'
    for row in manifest['files']:
        p = ROOT/row['file']
        assert p.suffix in {'.md','.json','.py','.diff'}
        body = p.read_bytes()
        assert len(body) == row['bytes']
        assert hashlib.sha256(body).hexdigest() == row['sha256'], row['file']
        body.decode('utf-8')
    checked_links = 0
    for p in ROOT.glob('*.md'):
        for target in re.findall(r'\]\(([^\s]+)\)', p.read_text()):
            if urlsplit(target).scheme:
                continue
            assert (p.parent/unquote(target.split('#')[0])).is_file(), (p.name,target)
            checked_links += 1
    report = (ROOT/'RECORD.md').read_text()
    assert [int(x) for x in re.findall(r'^## BP(\d+) ', report, re.M)] == list(range(1,11))
    counts = json.loads((ROOT/'CALL-ROWS.json').read_text())
    rows = counts['rows']
    assert len(rows) == counts['all_labelled_table_rows'] == 67
    window = [r for r in rows if '1999-12-06' <= r['iso_date'] <= '2000-02-04']
    assert len(window) == counts['date_window_rows'] == 27
    assert sum('BAYOUMI#2' in r['verbatim'] for r in window) == 21
    assert sum('BAYOUMI#4' in r['verbatim'] for r in window) == 6
    sample = json.loads((ROOT/'CARRIER-SAMPLE.json').read_text())
    assert len(sample['rows']) == 8
    assert sum(r['billed_minutes'] for r in sample['rows']) == 42
    assert sum(r['destination_label']=='Saudi Arabia' for r in sample['rows']) == 6
    assert sum(r['destination_label']=='UK' for r in sample['rows']) == 2
    sources = json.loads((ROOT/'SOURCES.json').read_text())
    assert sum('sha256' in r for r in sources['new_retrievals']) == 11
    assert sum('sha256' not in r for r in sources['new_retrievals']) == 2
    checks = json.loads((ROOT/'CHECKLIST.json').read_text())
    assert all(r['outcome'] and r['locations'] and r['verification'] for r in checks['items'])
    return dict(status='passed', manifest_files=len(names), public_files=len(actual),
        checked_local_links=checked_links, labelled_finding_sections=10,
        fbi_table_rows=67, selected_window_rows=27, carrier_rows=8,
        carrier_billed_minutes=42, historical_hypotheses_validated=False,
        source_pdf_bytes_in_payload=False, remote_publication_checked_by_this_script=False)

if __name__ == '__main__':
    try:
        print(json.dumps(verify(),indent=2))
    except Exception as exc:
        print(json.dumps({'status':'failed','error':type(exc).__name__+': '+str(exc)}))
        sys.exit(1)
