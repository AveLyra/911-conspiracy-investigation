"""Validate completed retention review, without mutating source images."""
import collections
import csv
import datetime
import hashlib
import json
from pathlib import Path
import shutil

WS = Path('${SOURCE_WORKSPACE}')
OUT = WS / 'outputs/911-image-relevance-2026-10-12'
MANIFEST = WS / 'outputs/911-image-recovery/recovery-manifest.json'


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def table(name):
    return list(csv.DictReader(open(OUT / name)))


def write(name, rows):
    with open(OUT / name, 'x', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


objects = table('distinct-image-content.csv')
paths = table('all-image-paths.csv')
aliases = table('duplicate-paths.csv')
visual = table('visual-review-selections.csv')
inventory = json.loads((OUT / 'inventory-verification.json').read_text())
assert sha(MANIFEST) == '77c4eed1d6c29a561a4974bee4d5358a444217a0995e3b4ece9683a38fc2913e'
assert len(objects) == 2535 and len(paths) == 5344 and len(aliases) == 2809
assert len({r['sha256'] for r in objects}) == 2535
assert {r['sha256'] for r in objects} == {r['sha256'] for r in paths}
assert sum(int(r['bytes']) for r in objects) == 1633150952
assert sum(r['original_hash_verified'] == 'True' for r in paths) == 4967
assert sum(r['has_original_hash_verified_path'] != 'True' for r in objects) == 188
assert len(visual) == 260 and len({r['sheet'] for r in visual}) == 16
assert len({r['sha256'] for r in visual}) == 245
assert len(table('historical-native-keep.csv')) == 2479
assert len(table('method-controls-keep.csv')) == 6
assert len(table('lower-priority-navigation.csv')) == 50
core = [r for r in objects if r['recommendation'] in ['keep_core_sequence', 'keep_fire_source_and_continuity']]
context = [r for r in objects if r['role'] == 'historical-native' and r not in core]
assert len(core) == 1566 and len(context) == 913
write('priority-core-keep.csv', core)
write('priority-context-keep.csv', context)
original = json.loads(MANIFEST.read_text())['restored']
original_by_path = {r['restored_path']: r for r in original}
for r in paths:
    source = original_by_path[r['restored_path']]
    assert source['sha256'] == r['sha256']
    assert str(source['original_hash_verified']) == r['original_hash_verified']
    assert Path(r['restored_path']).stat().st_size == int(r['bytes'])
    assert Path(r['representative_path']).is_file()
assert inventory['source_files_unchanged'] and inventory['manifest_unchanged']
for record in json.loads((OUT / 'source-records.json').read_text()):
    assert sha(record['local_read_copy']) == record['sha256']
    source = record['source']
    if '@' not in source:
        assert sha(source) == record['sha256'], 'Current research status changed during review'
assert (OUT / 'visual-observations.md').exists() and (OUT / 'retention-review.md').exists()
artifacts = []
for f in sorted(OUT.rglob('*')):
    if f.is_file():
        artifacts.append({'path': str(f), 'bytes': f.stat().st_size, 'sha256': sha(f)})
finished = {
    'status': 'PASS_RETENTION_REVIEW_COMPLETE_NO_DELETION',
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'paths_accounted': 5344, 'distinct_content_objects_accounted': 2535,
    'core_native_objects_recommend_keep': 1566,
    'context_and_diagnostic_native_objects_recommend_keep': 913,
    'synthetic_control_objects_recommend_keep_once': 6,
    'lower_priority_navigation_objects_retained_pending_any_future_proposal': 50,
    'fresh_hash_verification': 'All 2,535 distinct image objects passed in the initial inventory command; finalizer validates mappings and continued availability, without repeating the historical calculations.',
    'original_hash_verified_paths': 4967,
    'paths_archive_only': 188, 'paths_equivalent_refused_run_reconstruction': 189,
    'distinct_objects_without_original_hash_verified_reference': 188,
    'frame_record_join_counts': inventory['frame_metadata_join_kinds'],
    'visual_preview_sheets_displayed': 16, 'preview_cells_considered': 260,
    'distinct_previewed_recovered_objects': 245,
    'synthetic_control_objects_displayed_separately': 6,
    'full_native_frame_visual_certification': False,
    'pending_user_DistantView_response_satisfied_by_this_review': False,
    'source_files_and_manifest_preserved': True,
    'deletions': 0, 'uploads': 0, 'scientific_findings_accepted': 0,
    'review_artifact_bytes_before_final_record': sum(a['bytes'] for a in artifacts),
    'free_bytes_at_final_check': shutil.disk_usage(WS).free,
    'artifacts': artifacts,
}
(OUT / 'final-verification.json').write_text(json.dumps(finished, indent=2) + '\n')
print(json.dumps({k: v for k, v in finished.items() if k != 'artifacts'}, indent=2))
