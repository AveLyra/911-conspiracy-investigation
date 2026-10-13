"""Enrich this task's review tables only; all investigation files stay read-only."""
import csv
import collections
import hashlib
import json
from pathlib import Path
import subprocess

WS = Path('${SOURCE_WORKSPACE}')
OUT = WS / 'outputs/911-image-relevance-2026-10-12'
REPO = '${SOURCE_CASE_REPOSITORY}'
REV = '354af3e8b34e9ff3ffbb5f29e643538e090e63d1'
PREFIX = 'research/sherlock-wtc7-investigation/'


def readjson(rel):
    return json.loads(subprocess.check_output(['git', '-C', REPO, 'show', REV + ':' + PREFIX + rel], text=True))


rows = list(csv.DictReader(open(OUT / 'all-image-paths.csv')))
before = {(r['restored_path'], r['sha256'], r['original_hash_verified']) for r in rows}
distant = {r['index']: r for r in readjson('distant-view-source-screen/continuity-274-411/run01/frames.json')}
tilted = {r['index']: r for r in readjson('tilted-point-frame-audit/run01/manifest.json')['frames']}
planned = {}
for source, rel in [
    ('/v2-run01-VID-WTC7-001/', 'late-fire-video-lineage/v2-run01-VID-WTC7-001/VID-WTC7-001/planned-frames.json'),
    ('/run01-VID-WTC7-006/', 'late-fire-video-lineage/run01-VID-WTC7-006/VID-WTC7-006/planned-frames.json'),
]:
    planned[source] = (rel, {r['sample_index']: r for r in readjson(rel)})

for r in rows:
    source = r['source_path']
    stem_index = int(Path(source).stem.split('-')[-1]) if Path(source).stem.startswith('frame-') else None
    if r['study'] == 'distant-view-source-screen':
        rec = distant[stem_index]
        assert rec['native']['sha256'] == r['sha256']
        rel = 'distant-view-source-screen/continuity-274-411/run01/frames.json'
        r.update(frame_index=stem_index, pts=rec['stored_pts'], encoded_seconds=rec['stored_pts_seconds_exact'],
                 frame_record=REPO + '@' + REV + ':' + PREFIX + rel, frame_record_join='located_hash_matched')
    elif r['study'] == 'tilted-point-frame-audit':
        rec = tilted[stem_index]
        assert rec['native_png'] == 'native/' + Path(source).name
        rel = 'tilted-point-frame-audit/run01/manifest.json'
        r.update(frame_index=stem_index, pts=rec['pts'], encoded_seconds=rec['time_seconds_exact'],
                 frame_record=REPO + '@' + REV + ':' + PREFIX + rel, frame_record_join='located_named_frame_and_recovery_hash_sources')
    else:
        for needle, (rel, mapping) in planned.items():
            if needle in source:
                rec = mapping[stem_index - 1]
                r.update(frame_index=rec['source_frame_index'], pts=rec['source_pts'],
                         encoded_seconds=rec['source_seconds_exact'], frame_record=REPO + '@' + REV + ':' + PREFIX + rel,
                         frame_record_join='planned_locator_inferred_from_filename_order_not_completed_byte_join')


def writecsv(name, data):
    with open(OUT / name, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)


assert before == {(r['restored_path'], r['sha256'], r['original_hash_verified']) for r in rows}
assert len(rows) == 5344 and len({r['sha256'] for r in rows}) == 2535
writecsv('all-image-paths.csv', rows)
aliases = [r for r in rows if r['content_alias'] == 'True']
assert len(aliases) == 2809
writecsv('duplicate-paths.csv', aliases)
selected = list(csv.DictReader(open(OUT / 'visual-review-selections.csv')))
lookup = {r['source_path']: r for r in rows}
for r in selected:
    r['frame_index'] = lookup[r['source_path']]['frame_index']
writecsv('visual-review-selections.csv', selected)
verification = json.loads((OUT / 'inventory-verification.json').read_text())
verification['frame_metadata_join_kinds'] = dict(collections.Counter(r['frame_record_join'] for r in rows))
verification['metadata_joined_paths'] = sum(r['frame_record_join'].startswith('located') for r in rows)
verification['planned_only_locator_paths'] = sum(r['frame_record_join'].startswith('planned_') for r in rows)
verification['metadata_enrichment_changed_image_bytes_or_original_hash_status'] = False
(OUT / 'inventory-verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps({'frame_metadata_joins': verification['frame_metadata_join_kinds'], 'rows': len(rows), 'image_mutations': 0}, indent=2))
