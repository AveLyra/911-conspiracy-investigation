"""Read-only portable document checks. These do not test historical truth."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    checks = []

    def check(name, passed, scope):
        checks.append({'name': name, 'passed': bool(passed), 'scope': scope})

    provenance = read('PROVENANCE.json')
    review = read('frozen/REVIEW.json')
    frozen = read('frozen/CLAIMS-FROZEN.json')
    findings = read('FINDINGS.json')['findings']
    support = read('CLAIM-SUPPORT.json')
    dependence = read('SOURCE-DEPENDENCE.json')
    compare = read('COMPARISONS.json')
    check('six_target_snapshots', len(provenance['frozen_files']) == 6 and all(sha((ROOT / r['file']).read_bytes()) == r['sha256'] and (ROOT / r['file']).stat().st_size == r['bytes'] and r['source_commit'] == provenance['frozen_target_commit'] for r in provenance['frozen_files']), 'Exact exported prior research bytes, not source or historical authenticity')
    check('ten_originals_preserved', len(frozen['claims']) == len(review['claims']) == 10 and all(all(review['claims'][i].get(k) == v for k, v in c.items()) for i, c in enumerate(frozen['claims'])), 'Every frozen claim field retained; exact assessment-line check was separately local')
    check('freeze_reference', review['freeze_sha256'] == sha((ROOT / 'frozen/CLAIMS-FROZEN.json').read_bytes()), 'Review points to the captured freeze')
    check('all_claims_covered_once', len(support['claims']) == 10 and {x['claim_id'] for x in support['claims']} == {x['claim_id'] for x in review['claims']} and len({x['claim_id'] for x in support['claims']}) == 10 and all(len(x['assertions']) == 2 for x in support['claims']), 'Twenty compact assertion groups; no experiment count or complete atomization claimed')
    check('eight_typed_findings', {x['id'] for x in findings} == {'EM%02d' % n for n in range(1, 9)} and all(x.get('kind') and x.get('confidence') and x.get('strongest_objection') and x.get('repair') and x.get('state') for x in findings), 'Issue, objection, repair and adoption state represented; not automatic endorsement')
    valid_locs = True
    for finding in findings:
        for locator in finding['locations']:
            if locator['file'].startswith('frozen/'):
                lines = (ROOT / locator['file']).read_text().splitlines()
                valid_locs = valid_locs and 1 <= locator['line_start'] <= locator['line_end'] <= len(lines)
    check('frozen_line_references_in_range', valid_locs, 'Bounds only; semantic citation coverage is a separate reading judgment')
    expected_usage = {}
    for claim in review['claims']:
        for locator in claim['inspected_source_locators']:
            expected_usage.setdefault(locator.split(':', 1)[0], []).append(claim['claim_id'])
    check('document_reuse_map', dependence['document_reuse'] == expected_usage and dependence['repeated_independence_warning_distinct_values'] == len({x['independence'] for x in review['claims']}), 'Reported document overlap, not instrument-channel dependence authentication')
    values = compare['inputs']

    def seconds(value):
        h, m, s = map(int, value.split(':'))
        return h * 3600 + m * 60 + s

    check('labeled_arithmetic', seconds(values['NTSB_reported_impact_EDT']) - seconds(values['transcript_last_listed_time_EDT']) == compare['performed_comparisons']['nominal_label_difference_seconds'] == 2 and values['NPS_FBI_attributed_total_calls'] - values['NPS_FBI_attributed_Airfone_calls'] == compare['performed_comparisons']['NPS_summary_non_Airfone_count_by_subtraction'] == 2, 'Arithmetic on labeled source statements, not measured clock offset or authenticated call count')
    a = provenance['arithmetic_copy']
    check('arithmetic_copy_unchanged', sha((ROOT / a['file']).read_bytes()) == a['sha256'] and (ROOT / a['file']).stat().st_size == a['bytes'], 'Unchanged held native arithmetic copy; original target-tree absence separately observed')
    nps_hash = next(x['sha256'] for x in provenance['source_versions'] if x['id'] == 'calls.html')
    anchors = [x for x in read('LOCATOR-MAP.json')['anchors'] if x['source_id'] == 'calls.html']
    check('six_versioned_nps_anchors', len(anchors) == 6 and len({x['original_derived_line'] for x in anchors}) == 6 and all(x['source_sha256'] == nps_hash and x['held_raw_html_line'] > 0 for x in anchors), 'Anchor/hash consistency; exact source text containment separately checked in local build')
    broken = []
    for target in re.findall(r'\]\(([^)]+)\)', (ROOT / 'README.md').read_text()):
        if not target.startswith(('https://', 'http://', '#')) and not (ROOT / target.split('#', 1)[0]).is_file():
            broken.append(target)
    check('new_report_relative_links_resolve', not broken, 'This supplement report only; frozen predecessor defects intentionally preserved')
    check('completion_and_replication_limits', review['complete'] is False and read('frozen/BACKLOG.json')['complete'] is False and all(x['independent_historical_replication'] is False for x in review['claims']) and support['historical_verdict_changes_by_this_audit'] == 0 and dependence['independent_historical_replications_performed'] == 0, 'No historical replication, adjudication or audit-wide completion claim')
    # Match actual path/key/token shapes, not those patterns' source-code spelling.
    marker_patterns = [re.compile(r'/Users/[A-Za-z0-9._-]+/'), re.compile(r'-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----'), re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}')]

    def has_marker(value):
        return any(pattern.search(value) for pattern in marker_patterns)

    synthetic_markers = ['/' + 'Users' + '/example/unapproved.txt', '-' * 5 + 'BEGIN OPENSSH PRIVATE KEY' + '-' * 5, 'ghp_' + 'a' * 36]
    check('marker_screen_controls', all(has_marker(value) for value in synthetic_markers) and not has_marker("'/Users/' in text or 'PRIVATE KEY-----' in text"), 'Synthetic positive path/key/token shapes and negative source-pattern literal; no actual credentials used')
    local_markers = []
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix in ['.md', '.json', '.diff']:
            text = path.read_text()
            if has_marker(text):
                local_markers.append(str(path.relative_to(ROOT)))
    check('local_path_and_secret_pattern_screen', not local_markers, 'Narrow pattern screen only; manual payload disclosure review remains separate')
    print(json.dumps({'result': 'PASS' if all(x['passed'] for x in checks) else 'FAIL', 'checks': checks, 'broken_report_links': broken, 'local_marker_files': local_markers, 'historical_tests_performed': 0, 'scope': 'Portable document preservation, consistency and arithmetic checks only. Does not repeat private-baseline checks or authenticate historical evidence.'}, indent=2))
    return 0 if all(x['passed'] for x in checks) else 1


if __name__ == '__main__':
    raise SystemExit(main())
