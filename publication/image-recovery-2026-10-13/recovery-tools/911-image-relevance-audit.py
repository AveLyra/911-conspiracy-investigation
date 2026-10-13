"""Read-only review of a frozen recovery inventory; creates a new audit folder.

Does not remove, rename, edit, regenerate, publish, or accept investigation data.
"""
from __future__ import annotations

import collections
import csv
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps

WS = Path('${SOURCE_WORKSPACE}')
VAULT = WS / 'outputs/911-image-recovery'
OUT = WS / 'outputs/911-image-relevance-2026-10-12'
REPO = Path('${SOURCE_CASE_REPOSITORY}')
PREFIX = 'research/sherlock-wtc7-investigation/'
MANIFEST = VAULT / 'recovery-manifest.json'
EXPECTED_MANIFEST = '77c4eed1d6c29a561a4974bee4d5358a444217a0995e3b4ece9683a38fc2913e'


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def dump(name, value):
    with open(OUT / name, 'x') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def csvfile(name, rows):
    if not rows:
        raise ValueError('empty table ' + name)
    with open(OUT / name, 'x', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def gittext(path):
    p = subprocess.run(['git', '-C', str(REPO), 'show', REV + ':' + path],
                       capture_output=True, text=True,
                       env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'})
    return p.stdout if p.returncode == 0 else None


assert digest(MANIFEST) == EXPECTED_MANIFEST, 'Recovery inventory changed'
manifest = json.loads(MANIFEST.read_text())
REV = manifest['source_commit']
raw = manifest['restored']
assert len(raw) == 5344 and not manifest['unresolved'] and not manifest['mismatches']
OUT.mkdir(mode=0o700, exist_ok=False)
(OUT / 'source-records').mkdir()
(OUT / 'visual-review').mkdir()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
free_start = shutil.disk_usage(WS).free

scope = {
    'started_utc': started,
    'scope': 'Retention relevance of exactly 5,344 recovered image paths; no deletion.',
    'source_manifest': str(MANIFEST), 'source_manifest_sha256': EXPECTED_MANIFEST,
    'frozen_research_commit': REV,
    'deliverables': ['all-path inventory', 'distinct-content inventory',
                     'study/sequence table', 'exact duplicate-path table',
                     'exact lower-priority derivative table',
                     'visual review selections and evidence-based retention report'],
    'acceptance': ['Every recovery path accounted exactly once',
                   'Every distinct image byte hash checked',
                   'Original-hash qualifications retained',
                   'All relevant and contrary evidence protected',
                   'No mutation of vault or investigation records',
                   'Sampling distinguished from full visual review',
                   'No deletion, publication or scientific acceptance'],
    'free_bytes_start': free_start,
    'classification_boundary': 'This is a local storage review, not an accepted scientific finding or a case-record promotion.',
}
dump('scope.json', scope)

DOCS = [
    'CHARTER.md',
    'cbs-frame-correspondence/report.md',
    'cbs-frame-correspondence/dense-clip3/report.md',
    'cbs-frame-correspondence/dense-clip3/v2/report.md',
    'cbs-frame-correspondence/dense-clip7/report.md',
    'cbs-vince-source-screen/report.md',
    'cbs-vince-source-screen/stage2/report.md',
    'cbs-vince-source-screen/stage3/report.md',
    'cbs-vince-source-screen/stage4/report.md',
    'cbs-vince-source-screen/stage4/root-clip8.md',
    'cbs-vms-content-check/report.md',
    'cbs-vms-content-check/window-report.md',
    'distant-view-source-screen/continuity-274-411/report.md',
    'distant-view-source-screen/localization-review/report.md',
    'late-fire-catalog-join/report.md',
    'late-fire-sequence/report.md',
    'late-fire-video-lineage/report.md',
    'late-fire-video-lineage/root-screening-2026-09-19.md',
    'late-fire-video-lineage/validation.md',
    'tilted-point-frame-audit/report.md',
]
doc_index = []
for rel in DOCS:
    source = PREFIX + rel
    text = gittext(source)
    assert text is not None, 'Missing controlling research record ' + source
    target = OUT / 'source-records' / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    doc_index.append({'source': str(REPO) + '@' + REV + ':' + source,
                      'local_read_copy': str(target), 'sha256': digest(target)})

LIVE = Path('${SOURCE_SHERLOCK_WORKTREE}/research/sherlock-wtc7-investigation')
for rel in ['distant-view-source-screen/localization-recovery-2026-10-11/HUMAN-REVIEW.md',
            'completion-audit-2026-10-12/report.md']:
    source = LIVE / rel
    target = OUT / 'source-records/current' / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    doc_index.append({'source': str(source), 'local_read_copy': str(target),
                      'sha256': digest(target)})
dump('source-records.json', doc_index)

STUDY = {
    'cbs-frame-correspondence': ('Q01,Q02,Q10', 'Keep complete dense comparison populations, including poor candidates and failed-run history; the full search changed the leading candidates.'),
    'cbs-vince-source-screen': ('Q01,Q02,Q10', 'Keep source screen context, partial matches and nonmatches; catalogue labels do not establish subject or source identity.'),
    'cbs-vms-content-check': ('Q01,Q02,Q03,Q10', 'Keep visible-fire, obscuration, montage/chronology and failed-source-match observations; building/floor/source attribution remains unresolved.'),
    'distant-view-source-screen': ('Q03,Q04,Q05,Q10', 'Keep all 138 adjacent frames for continuity, feature identity, localization and pending human review; six samples cannot replace the complete sequence.'),
    'late-fire-catalog-join': ('Q01,Q02,Q10', 'Keep clean-source samples for report-still correspondence and visibility; preserve separately the rejected decoder products and diagnostic history.'),
    'late-fire-sequence': ('Q01,Q02,Q10', 'Keep flame-like appearances and disconfirming endpoint frames; incompatible source boundaries reject a proposed continuity shortcut.'),
    'late-fire-video-lineage': ('Q01,Q03,Q07,Q10', 'Keep source-search coverage, fire/motion/context samples, obscuration, montage and recording-quality limits; repeated packaging is not independent evidence.'),
    'tilted-point-frame-audit': ('Q03,Q04,Q05,Q10', 'Keep all 50 source images corresponding to 83 saved points, including disputed or obscured features; a roofline position is not automatically a persistent material point.'),
}


def classify(source):
    p = source.lower()
    study = source.split('/')[2]
    if any(t in p for t in ['synthetic', 'tiny-fixture', '/control']):
        return ('synthetic-method-control', 'keep_method_control',
                'Q10', 'Software fixture only; no historical 9/11 content. Keep one distinct byte object plus run metadata for method reproducibility.')
    if '/overview/' in p:
        return ('navigation-sheet', 'optional_navigation_derivative',
                STUDY[study][0], 'Resized contact sheet from retained native images; useful navigation/audit aid, not an additional historical observation. Exact-byte recreation was not rerun here.')
    if '/cbs-net-dub6-44/' in p:
        return ('historical-native', 'keep_failed_derivative_separate',
                'Q01,Q10', 'Repeated DV bitstream errors prevented visual admission. Preserve diagnostic history; do not promote these pixels to accepted fire evidence.')
    if '/v2-run01-vid-wtc7-001/' in p or '/run01-vid-wtc7-006/' in p:
        return ('historical-native', 'keep_failed_derivative_separate',
                'Q03,Q07,Q10', 'Camera2 or compilation processing was refused; recovered published archive copy lacks an independent saved original hash. Preserve source/quality history separately from admitted observations.')
    if '/dense-clip3/extract01/' in p:
        return ('historical-native', 'retain_qualified_duplicate_mapping',
                'Q01,Q02,Q10', 'Earlier refused-run reconstruction, not certified original bytes. Identical image content is retained in an original-hash-verified accepted v2 extraction; preserve the refusal and qualification in metadata.')
    if study in ['cbs-frame-correspondence', 'distant-view-source-screen', 'tilted-point-frame-audit']:
        return ('historical-native', 'keep_core_sequence', *STUDY[study])
    if '/vince-clip8/' in p:
        return ('historical-native', 'keep_scope_control_and_broader_911_context',
                'Q01,Q10', 'Nine samples expose a distant twin-tower scene, not the WTC7 report references. Lower direct WTC7 value, but preserve the negative source-screen result and broader 9/11 context.')
    if '/camera3-kit-mp4/native/' in p and int(Path(source).stem.split('-')[-1]) <= 5:
        return ('historical-native', 'keep_source_leader_context',
                'Q03,Q07,Q10', 'Countdown graphic rather than event footage. Retain the source sequence/clock context; it is not a collapse or fire observation.')
    if study in ['late-fire-sequence', 'late-fire-catalog-join']:
        return ('historical-native', 'keep_fire_source_and_continuity', *STUDY[study])
    return ('historical-native', 'keep_source_screen_context', *STUDY[study])


metadata_cache = {}
joins = {}
parents = sorted({x['source_path'].rsplit('/', 1)[0] for x in raw})
for parent in parents:
    base = parent.rsplit('/', 1)[0]
    candidates = [base + '/frames.json']
    if 'tilted-point-frame-audit/' in base:
        candidates.append(base + '/manifest.json')
    if any(t in base for t in ['v2-run01-VID-WTC7-001', 'run01-VID-WTC7-006']):
        candidates.append(base + '/planned-frames.json')
    if 'cbs-frame-correspondence/dense-clip3/extract01/' in base:
        candidates.append(base.replace('/dense-clip3/extract01/', '/dense-clip3/v2/extract01/') + '/frames.json')
    found = None
    for candidate in candidates:
        if candidate not in metadata_cache:
            text = gittext(candidate)
            metadata_cache[candidate] = json.loads(text) if text else None
        data = metadata_cache[candidate]
        if data is not None:
            found = (candidate, data)
            break
    if not found:
        continue
    candidate, data = found
    records = data if isinstance(data, list) else data.get('frames', [])
    for record in records:
        if not isinstance(record, dict):
            continue
        file = record.get('file') or record.get('path') or record.get('png') or record.get('native_png')
        if file:
            joins[base + '/' + file] = (candidate, record)

by_hash = collections.defaultdict(list)
by_parent = collections.defaultdict(list)
records = []
verified = {}
signatures = {}
for ordinal, item in enumerate(raw, 1):
    source = item['source_path']
    path = Path(item['restored_path'])
    st = path.stat()
    assert path.is_file() and st.st_size == item['original_size'], source
    sha = item['sha256']
    if sha not in verified:
        assert digest(path) == sha, source
        with Image.open(path) as im:
            shape = [im.width, im.height, im.mode, im.format]
        verified[sha] = {'size': st.st_size, 'allocated_bytes': st.st_blocks * 512,
                         'inode': [st.st_dev, st.st_ino], 'shape': shape}
    assert verified[sha]['inode'] == [st.st_dev, st.st_ino], 'Equal hashes have separate inodes; storage calculation needs review'
    signatures[str(path)] = [st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns, st.st_mode, st.st_nlink]
    role, recommendation, questions, reason = classify(source)
    meta = joins.get(source)
    if not meta and '/dense-clip3/extract01/' in source:
        meta = joins.get(source.replace('/dense-clip3/extract01/', '/dense-clip3/v2/extract01/'))
    frame = meta[1] if meta else {}
    index = frame.get('source_index', frame.get('source_frame_index', frame.get('index', frame.get('ordinal'))))
    record = {
        'manifest_row': ordinal, 'study': source.split('/')[2],
        'source_path': source, 'restored_path': str(path), 'sha256': sha,
        'bytes': st.st_size, 'width': verified[sha]['shape'][0],
        'height': verified[sha]['shape'][1], 'mode': verified[sha]['shape'][2],
        'role': role, 'recommendation': recommendation, 'questions': questions,
        'reason': reason, 'frame_index': index if index is not None else '',
        'pts': frame.get('pts', frame.get('source_pts', '')),
        'encoded_seconds': frame.get('pts_seconds_exact', frame.get('source_seconds_exact', frame.get('time_seconds_exact', ''))),
        'frame_record': (str(REPO) + '@' + REV + ':' + meta[0]) if meta else '',
        'frame_record_join': 'located' if meta else 'use_preserved_recovery_hash_sources_or_refusal_records',
        'original_hash_verified': bool(item['original_hash_verified']),
        'recovery_method': item['recovery_method'],
        'recovery_qualification': item.get('qualification', ''),
        'saved_hash_sources': json.dumps(item.get('hash_sources', []), separators=(',', ':')),
        'representative_path': '', 'content_alias': '',
    }
    records.append(record)
    by_hash[sha].append(record)
    by_parent[source.rsplit('/', 1)[0]].append(record)

PRIORITY = {
    'keep_core_sequence': 0, 'keep_fire_source_and_continuity': 1,
    'keep_source_screen_context': 2, 'keep_scope_control_and_broader_911_context': 3,
    'keep_source_leader_context': 4, 'keep_failed_derivative_separate': 5,
    'keep_method_control': 6, 'optional_navigation_derivative': 7,
    'retain_qualified_duplicate_mapping': 8,
}
objects = []
aliases = []
for sha, members in sorted(by_hash.items()):
    primary = min(members, key=lambda r: (not r['original_hash_verified'], PRIORITY[r['recommendation']], r['source_path']))
    for r in members:
        r['representative_path'] = primary['restored_path']
        r['content_alias'] = r is not primary
        if r is not primary:
            aliases.append(dict(r))
    objects.append({
        'sha256': sha, 'representative_path': primary['restored_path'],
        'representative_source_path': primary['source_path'],
        'role': primary['role'], 'recommendation': primary['recommendation'],
        'questions': ','.join(sorted({q for r in members for q in r['questions'].split(',')})),
        'reason': primary['reason'], 'bytes': verified[sha]['size'],
        'allocated_bytes_counted_once': verified[sha]['allocated_bytes'],
        'width': primary['width'], 'height': primary['height'],
        'recovery_path_count': len(members),
        'referencing_studies': ','.join(sorted({r['study'] for r in members})),
        'has_original_hash_verified_path': any(r['original_hash_verified'] for r in members),
    })

csvfile('all-image-paths.csv', records)
csvfile('distinct-image-content.csv', objects)
csvfile('duplicate-paths.csv', aliases)
csvfile('historical-native-keep.csv', [r for r in objects if r['role'] == 'historical-native'])
csvfile('method-controls-keep.csv', [r for r in objects if r['role'] == 'synthetic-method-control'])
csvfile('lower-priority-navigation.csv', [r for r in objects if r['role'] == 'navigation-sheet'])

sequences = []
for parent, members in by_parent.items():
    hashes = {r['sha256'] for r in members}
    sequences.append({
        'source_parent': parent, 'paths': len(members), 'distinct_hashes_in_sequence': len(hashes),
        'bytes_not_additive_across_sequences': sum(verified[h]['size'] for h in hashes),
        'role': members[0]['role'], 'recommendation': members[0]['recommendation'],
        'questions': members[0]['questions'], 'reason': members[0]['reason'],
    })
csvfile('all-sequences.csv', sorted(sequences, key=lambda r: r['source_parent']))

# Produce small, explicitly downscaled context aids. They are NOT forensic
# measurement images and are not substituted for the untouched native files.
visual_rows = []


def sheet(name, title, selected):
    width, height, cols = 300, 232, 4
    rows = (len(selected) + cols - 1) // cols
    canvas = Image.new('RGB', (cols * width, 58 + rows * height), '#f4f4f4')
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=14)
    draw.text((10, 8), title, font=font, fill='#111111')
    draw.text((10, 30), 'Downscaled audit aid; source images and aspect/field qualifiers remain unchanged.', font=font, fill='#333333')
    for cell, r in enumerate(selected):
        x, y = (cell % cols) * width, 58 + (cell // cols) * height
        with Image.open(r['restored_path']) as im:
            # Fit stored raster only; do not correct sample aspect or fields.
            tile = ImageOps.contain(im.convert('RGB'), (width - 12, 184))
        canvas.paste(tile, (x + (width - tile.width) // 2, y + 3))
        clip = r['source_path'].split('/')[-3]
        label = clip[:27] + ' | ' + Path(r['source_path']).stem
        draw.text((x + 5, y + 192), label, font=font, fill='#111111')
        draw.text((x + 5, y + 212), 'index ' + str(r['frame_index']), font=font, fill='#333333')
        visual_rows.append({'sheet': name, 'cell_one_based': cell + 1,
                            'source_path': r['source_path'], 'restored_path': r['restored_path'],
                            'sha256': r['sha256'], 'frame_index': r['frame_index']})
    canvas.save(OUT / 'visual-review' / name, quality=87, optimize=True)


def select_parent(needle):
    return sorted([r for r in records if needle in r['source_path']], key=lambda r: r['source_path'])


def evenly(seq, n):
    return [seq[i] for i in sorted({round(k * (len(seq) - 1) / (min(n, len(seq)) - 1)) for k in range(min(n, len(seq)))})] if len(seq) > 1 else seq


for clip, indices in [('clip3', [0, 24, 47, 94, 118, 127, 128, 135, 141, 156, 186, 187]),
                      ('clip7', [0, 141, 282, 423, 536, 537, 538, 539, 540, 541, 543, 544, 564, 705, 846, 987, 1127])]:
    needle = ('/dense-clip3/v2/extract01/' if clip == 'clip3' else '/dense-clip7/extract01/')
    seq = select_parent(needle)
    selected = [r for r in seq if r['frame_index'] in indices]
    assert len(selected) == len(indices), (clip, len(selected))
    sheet('dense-' + clip + '.jpg', 'CBS dense ' + clip + ': candidates AND context/failures', selected)

screen = [r for r in records if r['study'] == 'cbs-vince-source-screen' and '/run01/' in r['source_path'] and r['role'] == 'historical-native']
for stage in range(1, 5):
    selected = [r for r in screen if '/stage' + str(stage) + '/' in r['source_path']]
    assert len(selected) == 18
    sheet('cbs-screen-stage' + str(stage) + '.jpg', 'CBS source screen stage ' + str(stage) + ': all 18 fixed samples', selected)

for name, needle, n in [
    ('cbs-vms', '/cbs-vms-content-check/run01/native/', 24),
    ('dub5-14', '/late-fire-sequence/run01/cbs-net-dub5-14/native/', 12),
    ('dub5-15', '/late-fire-sequence/run01/cbs-net-dub5-15/native/', 18),
    ('dub6-rejected', '/late-fire-catalog-join/run01/cbs-net-dub6-44/native/', 6),
    ('peskin', '/run01-PESKIN-COMPLETE/PESKIN-COMPLETE/native/', 24),
    ('cnn', '/run01-VID-WTC7-004/VID-WTC7-004/native/', 18),
    ('bbc', '/run01-VID-WTC7-005/VID-WTC7-005/native/', 18),
    ('camera3', '/v2-run01-CAMERA3-KIT-MP4/CAMERA3-KIT-MP4/native/', 15),
    ('tilted', '/tilted-point-frame-audit/run01/native/', 12),
    ('distant', '/distant-view-source-screen/continuity-274-411/run01/native/', 12),
]:
    selected = evenly(select_parent(needle), n)
    assert selected, needle
    sheet(name + '.jpg', name + ': fixed context sample, not new measurement', selected)

csvfile('visual-review-selections.csv', visual_rows)
for path, before in signatures.items():
    st = Path(path).stat()
    after = [st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns, st.st_mode, st.st_nlink]
    assert before == after, 'Investigation file changed during audit: ' + path
assert digest(MANIFEST) == EXPECTED_MANIFEST
assert len(records) == 5344 and len(objects) == 2535 and len(aliases) == 2809
assert len({r['restored_path'] for r in records}) == 5344
assert {r['sha256'] for r in records} == {r['sha256'] for r in objects}
assert all(Path(r['representative_path']).exists() for r in records)
counts = {}
for role in sorted({r['role'] for r in records}):
    selected_paths = [r for r in records if r['role'] == role]
    selected_objects = [r for r in objects if r['role'] == role]
    counts[role] = {'paths': len(selected_paths), 'distinct_objects': len(selected_objects),
                    'bytes': sum(r['bytes'] for r in selected_objects),
                    'allocated_bytes': sum(r['allocated_bytes_counted_once'] for r in selected_objects)}
summary = {
    'status': 'INVENTORY_AND_HASH_VERIFICATION_PASS_VISUAL_REVIEW_PENDING',
    'finished_inventory_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'paths': len(records), 'distinct_objects': len(objects), 'duplicate_alias_paths': len(aliases),
    'logical_all_path_bytes': sum(r['bytes'] for r in records),
    'distinct_content_bytes': sum(r['bytes'] for r in objects),
    'distinct_inode_allocated_bytes': sum(r['allocated_bytes_counted_once'] for r in objects),
    'roles': counts,
    'object_recommendations': dict(collections.Counter(r['recommendation'] for r in objects)),
    'source_rows_original_hash_verified': sum(r['original_hash_verified'] for r in records),
    'source_rows_without_original_hash': sum(not r['original_hash_verified'] for r in records),
    'objects_without_any_original_hash_verified_path': sum(not r['has_original_hash_verified_path'] for r in objects),
    'metadata_joined_paths': sum(r['frame_record_join'] == 'located' for r in records),
    'source_files_unchanged': True, 'manifest_unchanged': True,
    'source_records_copied': len(doc_index), 'contact_sheets': len(list((OUT / 'visual-review').glob('*.jpg'))),
    'visual_selection_count': len(visual_rows),
    'free_bytes_end': shutil.disk_usage(WS).free,
    'deletions': 0, 'uploads': 0, 'new_investigation_findings_accepted': 0,
}
dump('inventory-verification.json', summary)
print(json.dumps(summary, indent=2))
