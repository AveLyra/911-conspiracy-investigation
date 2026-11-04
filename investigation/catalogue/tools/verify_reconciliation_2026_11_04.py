"""Verify the current research projection without requiring private input files."""
import hashlib
import json
from verify_assistance_search_2026_11_04 import preceding_master

sha = lambda raw: hashlib.sha256(raw).hexdigest()

def verify_current(root):
    checks = []
    def check(name, value):
        checks.append({'name': 'November4 ' + name, 'passed': bool(value)})
    revision = json.loads((root / 'data/reconciliation-2026-11-04.json').read_text())
    findings = json.loads((root / 'data/source-findings.json').read_text())['findings']
    ids = {row['id'] for row in findings}
    added = findings[370:]
    canonical = lambda obj: json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()
    check('481 unique findings and exact111 additions', len(findings) == len(ids) == 481 and len(added) == 111 and {r['id'] for r in added} == set(revision['added_ids']))
    check('all370 preceding normalized finding objects unchanged', sha(canonical(findings[:370])) == revision['old370_normalized_sha256'])
    check('all111 complete normalized finding objects pinned', all(sha(canonical(r)) == revision['new_normalized_object_sha256'][r['id']] for r in added))
    for name, transform in revision['transforms'].items():
        raw = preceding_master(root) if name == 'MASTER-LEADS.md' else (root / name).read_bytes()
        prefix, suffix = transform['prefix'].encode(), transform['suffix'].encode()
        matches = raw.startswith(prefix) and (not suffix or raw.endswith(suffix))
        old = raw[len(prefix):len(raw) - len(suffix) if suffix else None]
        check('unchanged preceding reader bytes ' + name, matches and sha(old) == transform['preceding_sha256'])
    for name, expected in revision['protected_preceding_hashes'].items():
        check('unchanged protected earlier payload ' + name, sha((root / name).read_bytes()) == expected)
    master = (root / 'MASTER-LEADS.md').read_text()
    text = (root / 'SOURCE-FINDINGS.md').read_text()
    for row in added:
        ident = row['id']; anchor = '<a id="' + ident.lower() + '"></a>'
        block = text.split(anchor, 1)[1].split('<a id="', 1)[0] if anchor in text else ''
        check('master and annotated finding ' + ident, bool(block) and 'SOURCE-FINDINGS.md#' + ident.lower() in master)
        for key, value in row.items():
            if key == 'id': continue
            exact = value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False)
            check('complete exported field ' + ident + '/' + key, exact in block)
    body = (root / 'LATEST-SOURCE-UNITS.md').read_text()
    reports = json.loads((root / 'data/report-supplements-2026-11-04.json').read_text())['reports']
    check('65 distinct complete report supplements', len(reports) == len({r['source_body_sha256'] for r in reports}) == 65)
    for row in reports:
        h = row['source_body_sha256']
        start, end = '<!-- BEGIN REPORT BODY ' + h + ' -->\n', '\n<!-- END REPORT BODY ' + h + ' -->'
        extracted = body.split(start, 1)[1].split(end, 1)[0] if start in body else ''
        check('complete qualified report prose ' + row['unit'], bool(extracted) and sha(extracted.encode()) == row['rendered_body_sha256'] and row['destination'] in master)
    inventory = json.loads((root / 'data/report-inventory-2026-11-04.json').read_text())['reports']
    check('full report-version index677 bodies1085 representations', len(inventory) == len({r['source_body_sha256'] for r in inventory}) == 677 and sum(r['representations'] for r in inventory) == 1085)
    check('newest archival and workplan findings retained', {'NR156', 'NR157', 'NR150', 'NR148'}.issubset(ids))
    guide = (root / 'CURRENT-RECONCILIATION-2026-11-04.md').read_text()
    check('contrary findings failed checks and open tests explicit', all(v in guide for v in ['May-family response', 'signed Beverly Hills approval', 'original substantive criteria remain open or partial', 'not independent evidence or probabilities', 'private correspondence']))
    check('private inventory and causal validation not promoted', not revision['private_source_inventory_exported'] and not revision['source_or_causal_validation'] and revision['no_deletion'])
    check('omission negative control', ids - {'NR157'} != ids and len(ids - {'NR157'}) != 481)
    return checks
