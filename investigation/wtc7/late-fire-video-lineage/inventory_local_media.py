#!/usr/bin/env python3
"""Bounded metadata/hash inventory; does not decode media or fetch network data.

Run with Python and --main-root /Users/admin/docs/911. JSON goes to stdout.
Only explicitly declared public media/manifests are read. Existing fixture paths
are enumerated, not opened. No raw headers, process logs, or platform JSON read.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess

MEDIA = Path('research/wtc7-video-comparison/media')
FIRE = Path('research/sherlock-wtc7-investigation/fire-originals')
KIT = Path('research/sherlock-wtc7-investigation/camera3-provenance')
CMP = Path('research/sherlock-wtc7-investigation/camera3-recording-comparison')
EXTS = {'.mp4', '.wmv', '.mov', '.webm', '.m4a', '.mkv', '.avi', '.mpg', '.mpeg'}


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def listed(root, rel):
    command = ['rg', '--files', '--hidden', '--no-ignore', '-0',
               '-g', '!**/held-uninspected/**', '-g', '!**/confidential/**']
    for ext in sorted(EXTS):
        command += ['-g', '*' + ext]
    command += [str(rel)]
    result = subprocess.run(command, cwd=root, check=True, capture_output=True)
    return sorted(Path(p.decode()) for p in result.stdout.split(b'\0') if p)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--main-root', type=Path, default=Path('/Users/admin/docs/911'))
    args = parser.parse_args()
    root = args.main_root.resolve(strict=True)
    manifest_rel = MEDIA / 'video-acquisition-manifest.csv'
    with (root / manifest_rel).open(newline='') as stream:
        acquisition = list(csv.DictReader(stream))
    paths_by_scope = {str(p): listed(root, p) for p in [MEDIA, FIRE, KIT, CMP]}
    all_paths = sorted(set(p for paths in paths_by_scope.values() for p in paths))
    selected = [p for p in all_paths if '/fixtures/' not in str(p) and p.name != 'synthetic.mkv']
    excluded_fixtures = [str(p) for p in all_paths if p not in selected]
    meta = {}
    for row in acquisition:
        rel = MEDIA / row['local_path']
        is_comparator = row['record_id'].startswith('VID-DEM')
        is_audio = row['video_codec'] == 'none'
        if 'analysis-source' in rel.parts:
            family = 'camera_' + row['display_name'].split('Camera ')[1].split('.')[0].split('_')[0]
        elif 'compilations' in rel.parts:
            family = '27_angles_montage'
        elif is_comparator:
            family = 'capital_one_comparator'
        else:
            family = 'cnn_archive' if 'CNN' in row['display_name'] else 'bbc_archive'
        meta[str(rel)] = {
            'record_id': row['record_id'], 'role': 'comparator' if is_comparator else ('audio_only' if is_audio else 'wtc7_video_access_copy'),
            'lineage_group': family, 'expected_bytes': int(row['bytes']),
            'expected_sha256': row['sha256'], 'manifest': str(manifest_rel),
            'source_page': row['source_page'], 'source_id': row['remote_file_id'],
            'description': row['display_name'], 'limitations': row['limitations'],
            'reported_duration_seconds': float(row['duration_seconds']),
            'reported_video_codec': row['video_codec'],
            'reported_width': int(row['width']) if row['width'] else None,
            'reported_height': int(row['height']) if row['height'] else None,
            'reported_frame_rate': row['nominal_frame_rate'] or None,
            'reported_audio_codec': row['audio_codec'],
            'metadata_measurement': 'inherited acquisition-manifest fields; no fresh probe',
        }
    peskin = FIRE / 'peskin/sources'
    for name, size, sha, role in [
        ('peskin-commons-resumed.webm', 696711067, '0f438006c27e3059e7a5a480d4a7ee5382c5a136945c2a0120e583e3456f324d', 'wtc7_video_access_copy'),
        ('peskin-commons-access.webm', 432152249, '65af2e29c4fa42e6fe77df2cbe99b7028a35ddcf82acbb7aab309e39b3ae5509', 'incomplete_transfer_excluded'),
    ]:
        meta[str(peskin / name)] = {
            'record_id': 'PESKIN_COMPLETE' if role == 'wtc7_video_access_copy' else 'PESKIN_PARTIAL',
            'role': role, 'lineage_group': 'peskin_joined_access_copy',
            'expected_bytes': size, 'expected_sha256': sha,
            'manifest': str(FIRE / 'peskin/report.md') + ':18-19',
            'source_id': 'NIST FOIA 09-42 R14 / Cumulus Peskin 01-44 asserted by Commons description; YouTube eEwSHkQvTI8',
            'limitations': 'Joined Commons/YouTube-derived copy; original AVI lineage and historical clocks unverified. Incomplete transfer is not a second source.',
            'reported_duration_seconds': 2967.201 if role == 'wtc7_video_access_copy' else None,
            'reported_video_codec': 'vp9' if role == 'wtc7_video_access_copy' else None,
            'reported_width': 1620 if role == 'wtc7_video_access_copy' else None,
            'reported_height': 1080 if role == 'wtc7_video_access_copy' else None,
            'reported_sample_aspect_ratio': '8:9' if role == 'wtc7_video_access_copy' else None,
            'reported_frame_rate': '30000/1001' if role == 'wtc7_video_access_copy' else None,
            'metadata_measurement': 'inherited sanitized report/validation fields; no fresh probe',
        }
    receipts = []
    for run in ['run-v1', 'run-v1-repeat']:
        base = KIT / 'kit-inventory' / run
        receipt_path = base / 'receipt.json'
        receipt = json.loads((root / receipt_path).read_text())
        receipts.append(receipt_path)
        for name, sha in receipt['products'].items():
            if Path(name).suffix.lower() not in EXTS:
                continue
            is_mp4 = name.endswith('.mp4')
            meta[str(base / name)] = {
                'record_id': 'KIT_MP4' if is_mp4 else 'KIT_WMV',
                'role': 'wtc7_video_access_copy' if is_mp4 else 'wtc7_video_access_copy_with_prior_decode_exclusion',
                'lineage_group': 'camera_3', 'expected_sha256': sha,
                'expected_bytes': 3996436 if is_mp4 else 1350045,
                'manifest': str(receipt_path),
                'source_id': 'WTC-911-Motion-Lab.zip / ' + name,
                'reported_duration_seconds': 29.533268 if is_mp4 else 29.501,
                'reported_video_codec': 'h264' if is_mp4 else 'wmv3',
                'reported_width': 720, 'reported_height': 480, 'reported_frame_rate': '15/1',
                'metadata_measurement': 'inherited kit-inspection metadata; no fresh probe',
                'limitations': 'Same Camera 3 recording family; duplicate archive entries/reproduction copies are not independent witnesses. WMV retained as source bytes but previous matching decode was excluded.',
            }
    files = []
    for rel in selected:
        full = root / rel
        full.resolve(strict=True).relative_to(root)
        before = full.stat()
        sha = digest(full)
        after = full.stat()
        record = {'path': str(rel), **meta.get(str(rel), {'role': 'unmatched_metadata'})}
        record.update(actual_bytes=after.st_size, actual_sha256=sha,
                      unchanged_during_hash=(before.st_size, before.st_mtime_ns, before.st_ino) == (after.st_size, after.st_mtime_ns, after.st_ino),
                      matches_expected_bytes=after.st_size == record.get('expected_bytes'),
                      matches_expected_sha256=sha == record.get('expected_sha256'))
        files.append(record)
    prefix = root / peskin / 'peskin-commons-access.webm'
    resumed = root / peskin / 'peskin-commons-resumed.webm'
    remaining = prefix.stat().st_size
    prefix_hash = hashlib.sha256()
    with resumed.open('rb') as stream:
        while remaining:
            block = stream.read(min(1024 * 1024, remaining))
            if not block:
                raise RuntimeError('Complete copy unexpectedly short during prefix check')
            prefix_hash.update(block)
            remaining -= len(block)
    kit_receipt = json.loads((root / receipts[0]).read_text())
    archive_rel = KIT / kit_receipt['source']['name']
    archive = {'path': str(archive_rel), 'role': 'preserved_packaging_container',
               'manifest': str(receipts[0]), 'actual_bytes': (root / archive_rel).stat().st_size,
               'actual_sha256': digest(root / archive_rel),
               'expected_bytes': kit_receipt['source']['bytes'], 'expected_sha256': kit_receipt['source']['sha256']}
    archive['matches_expected_bytes'] = archive['actual_bytes'] == archive['expected_bytes']
    archive['matches_expected_sha256'] = archive['actual_sha256'] == archive['expected_sha256']
    outer_path = KIT / 'kit-inventory/run-v1/outer-entries.json'
    outer = json.loads((root / outer_path).read_text())
    inventory_only = []
    excluded_archive_members = []
    for row in outer:
        if Path(row.get('entry_name', '')).suffix.lower() not in EXTS or row['disposition'] != 'inventory_only':
            continue
        item = {k: row[k] for k in ['entry_index', 'entry_name', 'actual_bytes', 'sha256', 'disposition']}
        item.update(manifest=str(outer_path), hash_status='inherited prior member hash; no new extraction or member rehash')
        if '/WTC7-' in row['entry_name']:
            inventory_only.append(item)
        else:
            excluded_archive_members.append(item)
    groups = {}
    for row in files:
        groups.setdefault(row['actual_sha256'], []).append(row['path'])
    duplicates = [{'sha256': sha, 'paths': paths, 'independent_sources_added_by_copies': 0}
                  for sha, paths in groups.items() if len(paths) > 1]
    checksums = {}
    for line in (root / MEDIA / 'SHA256SUMS').read_text().splitlines():
        sha, path = line.split('  ', 1)
        checksums[str(MEDIA / path)] = sha
    checksum_consistency = all(checksums.get(str(MEDIA / row['local_path'])) == row['sha256'] for row in acquisition)
    payload = {
        'schema': 'late-fire-local-media-inventory-v1', 'inventory_date': '2026-09-16',
        'authority': 'Research inventory only; no legal-record promotion or authentication.',
        'source_root': str(root), 'method': 'rg filename enumeration with ignored files included; exact CSV/JSON/sanitized-note metadata; streaming SHA-256 over selected files; no decode/probe, network, archive extraction, audio listening, or appearance interpretation.',
        'searched_roots': list(paths_by_scope),
        'scope_reason': 'Original task media/fire roots plus known Camera3 kit and comparison paths referenced by preserved public-media provenance notes.',
        'excluded_areas': ['personal/litigation/confidential packets', 'held-uninspected areas', 'raw HTTP headers and process logs', 'platform .info.json bodies/ephemeral media URLs', 'arbitrary repository media search', 'archive member content outside already-extracted Camera3 files'],
        'enumerated_media_path_counts': {key: len(value) for key, value in paths_by_scope.items()},
        'selected_file_count': len(files), 'unique_selected_byte_sequences': len(groups),
        'wtc7_selected_file_paths_excluding_incomplete_and_comparators': sum(row['role'].startswith('wtc7') or row['role'] == 'audio_only' for row in files),
        'all_selected_file_hashes_match': all(row['matches_expected_sha256'] for row in files),
        'all_selected_file_sizes_match': all(row['matches_expected_bytes'] for row in files),
        'all_selected_files_unchanged_during_hash': all(row['unchanged_during_hash'] for row in files),
        'unmatched_selected_paths': [row['path'] for row in files if row['role'] == 'unmatched_metadata'],
        'metadata_paths_without_selected_file': sorted(set(meta) - set(str(p) for p in selected)),
        'acquisition_manifest_and_sha256sums_consistent': checksum_consistency,
        'files': files, 'exact_duplicate_groups': duplicates,
        'peskin_partial_prefix_check': {'prefix_bytes': prefix.stat().st_size, 'resumed_prefix_sha256': prefix_hash.hexdigest(), 'matches_partial': prefix_hash.hexdigest() == meta[str(peskin / 'peskin-commons-access.webm')]['expected_sha256'], 'conclusion': 'Incomplete transfer is an exact prefix of complete access copy, not an independent source.'},
        'packaging_archive': archive,
        'inventory_only_wtc7_archive_members': inventory_only,
        'excluded_non_wtc7_or_comparator_archive_members': excluded_archive_members,
        'excluded_synthetic_media_paths': excluded_fixtures,
        'target_candidate_note': 'No selected file or inventory-only WTC7 member is named Fox or identifies Figures 5-157/5-158. Camera2 CBS converted clip, BBC/CNN broadcast segments, 27-angle montage, and Peskin joined copy are metadata-defined candidate access families only. Archive DistantViewWTC7/TiltedCameraWTC7 filenames are unresolved leads. No target-shot match is established.',
        'claim_ceiling': 'Hash equality supports current byte identity to the declared pins only. File count, unique hashes, common-family labels, and inherited durations do not authenticate camera originals, independent viewpoints, historical clocks, continuity, or target-figure correspondence.',
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
