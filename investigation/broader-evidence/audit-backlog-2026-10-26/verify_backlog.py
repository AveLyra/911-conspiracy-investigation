"""Offline preservation and coverage checks for this public planning snapshot.

Does not retrieve/authenticate source URLs or complete any historical audit.
Git objects may supply existing reference targets omitted by sparse checkout.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote, urlparse

unit = Path(__file__).resolve().parent
git_root = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=unit, text=True).strip())


def load(name):
    return json.loads((unit / name).read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_reference(name):
    candidate = (unit / name).resolve()
    relative = candidate.relative_to(git_root).as_posix()
    if candidate.is_file():
        return candidate.read_bytes()
    return subprocess.check_output(['git', 'show', 'HEAD:' + relative], cwd=git_root)


backlog = load('audit-todos-v1.json')
tasks = backlog['tasks']
expected_ids = {f'AUD{i:03}' for i in range(1, 17)}
assert len(tasks) == 16 and {t['id'] for t in tasks} == expected_ids
assert {t['group'] for t in tasks} == set(range(1, 9))
assert backlog['next_substantive_audit'] == ['AUD001', 'AUD002', 'AUD003']
request = (unit / 'REQUEST.md').read_text()
coverage = {r['id']: r for r in load('COVERAGE.json')['tasks']}
source_urls = set()
for task in tasks:
    group = task['group']
    assert task['priority'].startswith(f'P{group}') if group < 8 else task['priority'] == 'Cross-cutting requirement for every track'
    assert coverage[task['id']]['priority'] == task['priority']
    assert task['exact_original_request_wording'] in request
    assert sha(read_reference(task['request_source']['file'])) == task['request_source']['sha256']
    assert all(task.get(k) for k in ['next_original_record', 'discriminating_test', 'observable_completion_criteria', 'unresolved_conflicting_values_or_interpretations'])
    assert all(dep in expected_ids for dep in task['dependencies'])
    assert task['progress']['planned'] is True
    assert all(task['progress'][k] is False for k in ['target_originals_acquired', 'target_originals_inspected', 'target_audit_verified', 'this_new_todo_published'])
    assert task['source_references']
    for source in task['source_references']:
        assert source.get('url') or source.get('file')
        if source.get('url'):
            assert urlparse(source['url']).scheme == 'https'
            source_urls.add(source['url'])
        if source.get('file'):
            assert sha(read_reference(source['file'])) == source['sha256']
    for row in task['original_assessment_wording']:
        source = read_reference(row['source_file'])
        assert sha(source) == row['source_sha256']
        assert row['exact_original_wording'] in source.decode()

assert set(load('COVERAGE.json')['native_primary_source_urls']) <= source_urls
assert load('COVERAGE.json')['native_primary_source_url_count'] == 9
for name in ['README.md', 'REQUEST.md']:
    text = (unit / name).read_text()
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if not urlparse(link).scheme:
            read_reference(unquote(link.split('#', 1)[0]))
        elif link.startswith('https://github.com/AveLyra/911-conspiracy-investigation/blob/'):
            suffix = link.split('/blob/', 1)[1]
            commit, path = suffix.split('/', 1)
            subprocess.check_call(['git', 'cat-file', '-e', commit + ':' + path], cwd=git_root)

for row in load('MANIFEST.json')['files']:
    data = (unit / row['path']).read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256']

print(json.dumps({'result': 'PASS', 'tasks': 16, 'tracks': 8, 'native_primary_starting_URLs_retained': 9, 'AUD016_existing_crosswalk_reference': 'resolved', 'priorities_targets_tests_completion_criteria': 'present', 'packaged_hashes_and_internal_references': 'checked', 'live_source_retrieval_or_authentication': False, 'historical_audits_completed_by_this_check': False}, indent=2))
