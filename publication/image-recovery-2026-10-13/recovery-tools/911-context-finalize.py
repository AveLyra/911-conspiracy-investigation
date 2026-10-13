"""Finalize a read-only review; write proposals and recovery records only.

This program contains no deletion, unlink, overwrite, linking or restoration
operation. Every new report is created exclusively. Investigation files are
opened for reads only.
"""
import collections
import csv
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

BASE = Path('${SOURCE_WORKSPACE}')
OUT = BASE/'outputs/911-context-review-2026-10-12'
PRIOR = BASE/'outputs/911-image-relevance-2026-10-12'
VAULT = BASE/'outputs/911-image-recovery'
LFS = [Path('${SOURCE_CASE_REPOSITORY}/.git/lfs/objects'),
       Path('${SOURCE_CASE_REPOSITORY}/.git/modules/911-conspiracy-investigation-public/lfs/objects')]

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def load(p):
    with open(p) as f:
        return json.load(f)

def readcsv(p):
    with open(p, newline='') as f:
        return list(csv.DictReader(f))

def save(p, data):
    with open(p, 'x') as f:
        json.dump(data, f, indent=2)

def csvsave(p, rows):
    assert rows
    with open(p, 'x', newline='') as f:
        w = csv.DictWriter(f, list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def textsave(p, value):
    with open(p, 'x') as f:
        f.write(value)

def regular(p, inside=None):
    p = Path(p)
    assert p.is_absolute() and p.resolve() == p, ('noncanonical or symlink path', str(p))
    if inside:
        assert p.is_relative_to(inside), ('outside recovery vault', str(p))
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode), ('not a regular file', str(p))
    return s

def snapshot(s):
    return {'dev': s.st_dev, 'ino': s.st_ino, 'nlink': s.st_nlink,
            'size': s.st_size, 'mtime_ns': s.st_mtime_ns, 'blocks': s.st_blocks}

def main():
    assert os.statvfs(BASE).f_bavail*os.statvfs(BASE).f_frsize >= 10_000_000_000
    audit = load(OUT/'audit-scope.json')
    scope = load(OUT/'scope.json')
    groups = load(OUT/'groups.json')
    results = load(OUT/'recovery-results.json')
    summary = load(OUT/'recovery-summary.json')
    pages = load(OUT/'pages.json')
    individual = load(OUT/'individual-native-review.json')
    notes = [json.loads(line) for line in (OUT/'visual-review-notes.jsonl').read_text().splitlines()]
    manifest = load(VAULT/'recovery-manifest.json')
    inventory = readcsv(PRIOR/'distinct-image-content.csv')
    core = readcsv(PRIOR/'priority-core-keep.csv')
    controls = readcsv(PRIOR/'method-controls-keep.csv')
    navigation = readcsv(PRIOR/'lower-priority-navigation.csv')
    scopebyhash = {r['sha256']: r for r in scope}
    resultbyid = {r['review_id']: r for r in results}
    assert len(scope) == len(scopebyhash) == len(resultbyid) == 913
    assert len(core) == 1566 and len(controls) == 6 and len(navigation) == 50
    assert len(inventory) == 2535 and len(groups) == 16
    assert summary['byte_recovery_verified'] == 913 and summary['missing'] == []
    assert summary['no_image_writes'] and summary['no_deletions']
    assert sha(VAULT/'recovery-manifest.json') == audit['recovery_manifest_sha256']
    assert sha(PRIOR/'priority-context-keep.csv') == audit['scope_csv_sha256']
    assert sha(PRIOR/'priority-core-keep.csv') == audit['core_csv_sha256']
    scopeids = {r['review_id'] for r in scope}
    pagemap = {p['page_id']: p for p in pages}
    pagedids = [v for p in pages for v in p['review_ids']]
    assert len(pages) == len(notes) == 64
    assert len(pagedids) == 913 and set(pagedids) == scopeids
    categories = {}
    for n in notes:
        notedids = []
        for start, end, category in n['ranges']:
            for number in range(start, end+1):
                rid = f'I{number:04d}'
                assert rid not in categories
                categories[rid] = {'category': category, 'note': n['note']}
                notedids.append(rid)
        assert set(notedids) == {v for p in n['pages'] for v in pagemap[p]['review_ids']}
    assert set(categories) == scopeids
    for p in pages:
        assert sha(p['path']) == p['sha256']
    for r in individual:
        assert r['review_id'] in scopeids and r['sha256'] == next(s['sha256'] for s in scope if s['review_id'] == r['review_id'])
    assert len(individual) == 8
    for r in scope:
        got = resultbyid[r['review_id']]
        for flag in ['byte_recovery_verified', 'group_execution_passed', 'current_png_match',
                     'current_rgb_match', 'current_size_match', 'current_dimensions_match']:
            assert got[flag] is True, (r['review_id'], flag)
        assert got['generated_png_sha256'] == got['current_png_sha256'] == r['sha256']
        assert got['generated_rgb_sha256'] == r['rgb_sha256_current']
        assert got['generated_bytes'] == int(r['bytes'])
        assert got['frozen_png_match'] is not False and got['frozen_rgb_match'] is not False

    # Freeze source recovery locations, exact decoder argv and all frozen source
    # frame rows. Historical failure statuses are deliberately unchanged.
    videos = []
    recipes = []
    for g in groups:
        receiptpath = OUT/'receipts'/(g['group_id']+'.json')
        receipt = load(receiptpath)
        pin = g['source_pin']
        assert receipt['group_execution_passed'] and receipt['returncode'] == 0
        assert receipt['source_sha256_before'] == receipt['source_sha256_after'] == pin['sha256']
        assert sha(receipt['stderr_path']) == receipt['stderr_sha256']
        assert receipt['historical_status_unchanged'] == g['historical_status']
        for p in g['existing_video_paths']:
            s = regular(p)
            before = snapshot(s)
            assert s.st_size == pin['bytes'] and sha(p) == pin['sha256']
            assert before == snapshot(regular(p))
            videos.append({'group_id': g['group_id'], 'source_id': pin['id'],
                           'preserved_path': p, 'sha256': pin['sha256'], 'bytes': pin['bytes'],
                           'used_for_verified_regeneration': p == g['preserved_video_path'],
                           'source_original_path': pin['path'], 'inode': s.st_ino, 'mtime_ns': s.st_mtime_ns,
                           'current_sha256_verified': True, 'preservation': 'KEEP; excluded from deletion list',
                           'historical_status': g['historical_status']})
        recipes.append({'group_id': g['group_id'], 'run': g['run'], 'preserved_video_path': g['preserved_video_path'],
                        'source_pin': pin, 'verification_argv': receipt['verification_argv'],
                        'original_argv': g['original_argv'], 'original_frozen_frames': g['frames'],
                        'receipt_path': str(receiptpath), 'receipt_sha256': sha(receiptpath),
                        'scope_review_ids': [r['review_id'] for r in g['scope']],
                        'historical_status': g['historical_status']})
    csvsave(OUT/'preserved-videos.csv', videos)
    save(OUT/'recovery-recipes.json', {
        'status': 'tested_in_memory_only; no on-disk restoration or deletion performed',
        'decoder_record': str(OUT/'decoder.json'), 'dependencies_record': str(OUT/'decoder-dependencies.json'),
        'instructions': [
            'Retain videos, provenance and failure records. Verify video SHA-256 before restoring.',
            'Use the recorded FFmpeg binary, options and source frame selection. The current verification argv outputs an image2pipe PNG stream.',
            'A future restorer must parse PNG chunks through IEND in stream order as 911-context-review.py did, compare each frozen/current object hash, and only then write to a new staging directory.',
            'Restore only scope objects matching SHA-256 and dimensions; map filenames to the full original source paths in proposed-deletions.csv and recovery-manifest.json.',
            'Recreate the object-store path and hardlinked aliases only when expressly requested; do not restore obsolete project trees automatically.',
            'Alternatively use a currently hash-verified retained PNG in retained-png-copies.csv. These independent inode copies remain excluded from this deletion proposal.',
            'Any mismatch must stop restoration and retain the original failed-run labels. Reproducibility does not supply missing independent original PNG hashes or authenticate historical claims.'
        ], 'groups': recipes})

    # Verify retained independent native PNGs as a second recovery route. LFS
    # names alone do not establish integrity, so read and hash the contents.
    pngcopies = []
    copyhashes = set()
    for r in scope:
        h = r['sha256']
        for root in LFS:
            p = root/h[:2]/h[2:4]/h
            if not p.exists():
                continue
            s = regular(p)
            before = snapshot(s)
            assert s.st_size == int(r['bytes']) and sha(p) == h
            assert before == snapshot(regular(p))
            assert (s.st_dev, s.st_ino) != (r['initial_stat']['dev'], r['initial_stat']['ino'])
            pngcopies.append({'review_id': r['review_id'], 'sha256': h, 'preserved_path': str(p),
                              'bytes': s.st_size, 'inode': s.st_ino, 'mtime_ns': s.st_mtime_ns,
                              'exact_byte_recovery': 'read contents; SHA-256 and length matched current native PNG',
                              'preservation': 'KEEP; excluded from deletion list; local Git LFS object',
                              'remote_LFS_download_tested': False})
            copyhashes.add(h)
    csvsave(OUT/'retained-png-copies.csv', pngcopies)

    # Recheck the entire previously recovered vault and account for every
    # hardlink. This prevents either omission of hidden links or mistaken
    # counting of aliases as independent storage/evidence.
    aliases = collections.defaultdict(list)
    for a in manifest['restored']:
        aliases[a['sha256']].append(a)
    inventorybyhash = {r['sha256']: r for r in inventory}
    assert set(inventorybyhash) == set(aliases)
    assert set(scopebyhash).isdisjoint({r['sha256'] for r in core+controls+navigation})
    proposed = []
    protected = []
    objectreviews = []
    checked_aliases = 0
    distinct_inode_set = set()
    for n, h in enumerate(sorted(aliases), 1):
        row = inventorybyhash[h]
        objectpath = VAULT/'.objects'/h[:2]/h
        s = regular(objectpath, VAULT)
        before = snapshot(s)
        assert s.st_size == int(row['bytes']) and sha(objectpath) == h
        assert before == snapshot(regular(objectpath, VAULT))
        inodekey = (s.st_dev, s.st_ino)
        assert inodekey not in distinct_inode_set
        distinct_inode_set.add(inodekey)
        members = aliases[h]
        allpaths = [objectpath]+[Path(a['restored_path']) for a in members]
        assert len(set(allpaths)) == len(allpaths) == s.st_nlink, (h, 'hardlink count disagreement')
        for p in allpaths:
            ps = regular(p, VAULT)
            assert snapshot(ps) == before, ('alias metadata differs', str(p))
        checked_aliases += len(members)
        if h not in scopebyhash:
            protected.append({'sha256': h, 'representative_path': row['representative_path'],
                              'object_store_path': str(objectpath), 'bytes': s.st_size,
                              'verified_sha256': h, 'all_aliases_metadata_verified': len(members),
                              'retention_status': row['retention_status'],
                              'scope': 'KEEP; excluded from deletion list'})
            continue
        r = scopebyhash[h]
        assert before == r['initial_stat'], (r['review_id'], 'candidate changed since preparation')
        assert len(members) == int(r['recovery_path_count'])
        q = categories[r['review_id']]
        receiptpath = OUT/'receipts'/(r['group_id']+'.json')
        independent_hash = any(a['original_hash_verified'] for a in members)
        assert independent_hash == (r['has_original_hash_verified_path'] == 'True')
        qualifier = ('Independent saved original PNG hash matched.' if independent_hash else
                     '188-object refused-run group: archive-copy bytes matched current video regeneration; no independent original PNG hash located; historical refusal unchanged.')
        objectreviews.append({'review_id': r['review_id'], 'sha256': h, 'representative_path': r['representative_path'],
                              'bytes': s.st_size, 'allocated_bytes_counted_once': s.st_blocks*512,
                              'all_local_vault_links': len(allpaths), 'group_id': r['group_id'], 'run': r['run'],
                              'source_index': r['source_index'], 'source_pts': r['source_pts'], 'time_base': r['time_base'],
                              'encoded_seconds': r['encoded_seconds'], 'preserved_video_path': r['preserved_video_path'],
                              'video_sha256': r['video_sha256'], 'exact_png_and_rgb_regeneration_passed': True,
                              'independent_original_png_hash_verified': independent_hash,
                              'additional_retained_png_copy_verified': h in copyhashes,
                              'original_hash_qualification': qualifier, 'historical_status_unchanged': r['historical_status'],
                              'visual_page': r['preview_page'], 'visual_cell': r['preview_cell'],
                              'observed_scene_category': q['category'], 'visual_observation_and_limits': q['note'],
                              'relevance_decision': 'Preserve full source video, locators, failure records and retained LFS PNGs; do not discard as irrelevant.',
                              'local_png_recommendation': 'Eligible for removal ONLY after explicit approval of proposed-deletions.csv',
                              'recovery_receipt': str(receiptpath), 'receipt_sha256': sha(receiptpath)})
        for p in allpaths:
            is_object = p == objectpath
            alias = next((a for a in members if a['restored_path'] == str(p)), None)
            proposed.append({'path': str(p), 'path_role': 'object_store_root' if is_object else 'hardlinked_source_alias',
                             'review_id': r['review_id'], 'sha256': h, 'bytes': s.st_size,
                             'allocated_bytes_counted_once': s.st_blocks*512 if is_object else 0,
                             'device': s.st_dev, 'inode': s.st_ino, 'hardlink_count': s.st_nlink,
                             'mtime_ns': s.st_mtime_ns, 'mode_octal': oct(stat.S_IMODE(s.st_mode)),
                             'source_path': alias['source_path'] if alias else '',
                             'group_id': r['group_id'], 'source_index': r['source_index'], 'source_pts': r['source_pts'],
                             'time_base': r['time_base'], 'preserved_video_path': r['preserved_video_path'],
                             'video_sha256': r['video_sha256'], 'recovery_receipt': str(receiptpath),
                             'byte_recovery_verified': True, 'independent_original_png_hash_verified': independent_hash,
                             'retained_png_copy_verified': h in copyhashes, 'historical_status': r['historical_status'],
                             'approval_status': 'PROPOSAL ONLY; NOT APPROVED; DO NOT DELETE'})
        if n % 400 == 0:
            print('Rechecked recovered vault objects', n, '/', len(aliases), flush=True)
    assert checked_aliases == len(manifest['restored']) == 5344
    assert len(protected) == 1622 and len(objectreviews) == 913 and len(proposed) == 2551
    assert len({r['path'] for r in proposed}) == 2551
    objectreviews.sort(key=lambda r: r['review_id'])
    proposed.sort(key=lambda r: (r['review_id'], r['path_role'], r['path']))
    csvsave(OUT/'object-review.csv', objectreviews)
    csvsave(OUT/'proposed-deletions.csv', proposed)
    textsave(OUT/'proposed-deletions.txt', '\n'.join(r['path'] for r in proposed)+'\n')
    csvsave(OUT/'protected-image-objects.csv', protected)
    csvsave(OUT/'visual-category-counts.csv', [{'category': k, 'objects': v} for k,v in sorted(collections.Counter(q['category'] for q in categories.values()).items())])
    assert sha(VAULT/'recovery-manifest.json') == audit['recovery_manifest_sha256']
    frozenrecords = readcsv(OUT/'frozen-records.csv')
    for f in frozenrecords:
        assert sha(f['path']) == f['sha256'] and Path(f['path']).stat().st_size == int(f['bytes'])
    decoder = load(OUT/'decoder.json')
    assert sha(decoder['path']) == decoder['sha256']
    dependencies = load(OUT/'decoder-dependencies.json')
    for d in dependencies['files']:
        assert sha(d['path']) == d['sha256'] and Path(d['path']).stat().st_size == d['bytes']

    logical = sum(r['bytes'] for r in objectreviews)
    allocated = sum(r['allocated_bytes_counted_once'] for r in objectreviews)
    originalcount = sum(r['independent_original_png_hash_verified'] for r in objectreviews)
    assert logical == 523435438 and allocated == 525246464 and originalcount == 725
    videogroups = {g['source_pin']['sha256']: g['source_pin']['bytes'] for g in groups}
    grouptext = '\n'.join(f"  {g['group_id']}: {len(g['scope']):3d} images | {sum(int(r['bytes']) for r in g['scope'])/1e6:8.2f} MB | {g['source_pin']['id']} | {g['historical_status']}" for g in groups)
    directcopytext = f'{len(copyhashes)} of the 913 objects also have {len(pngcopies)} separately stored local Git LFS PNG copies, all freshly SHA-256 and length verified. Those copies are KEEP entries, never in the proposal.'
    review = f'''All 913 context/diagnostic images reviewed; nothing deleted.
Status: exact deletion proposal ready for the user's explicit approval.

The 913 PNGs contain potentially useful fire/facade details, collapse and cloud sequences, emergency-response context, broadcast statements/captions, source edits, and decoding failures. They should not be discarded on an assumption that they are irrelevant. All of that image content remains recoverable from the preserved videos; the proposal concerns expendable local derivatives after tested recovery, not rejection of the investigation content.

EXACT PROPOSAL
  List: {OUT/'proposed-deletions.csv'}
  Plain paths: {OUT/'proposed-deletions.txt'}
  2,551 regular-file entries: 1,638 hardlinked source aliases plus 913 object-store roots.
  These entries represent 913 distinct images, not 2,551 independent observations.
  523,435,438 image bytes (523.44 MB decimal / 499.19 MiB).
  525,246,464 allocated bytes counted once per inode (525.25 MB / 500.91 MiB) is an upper estimate; actual freed space may be smaller because of retained copies, APFS sharing or snapshots. Do not add alias byte counts to estimate savings.
  No directories, source videos, Git/LFS histories, native PNGs outside this exact vault list, chats, caches, dependencies or other investigation files are proposed for deletion.
  Every proposed path was freshly checked as a regular non-symlink file within the recovery vault. All links to each candidate inode are explicitly listed, with the SHA-256, inode, link count, size and mtime snapshot. Approval cannot apply to a modified list.

ACTUAL RECOVERY VERIFICATION
  16 serial FFmpeg runs recreated all 913 scoped PNGs through RAM. All 913 matched the current PNG SHA-256, decoded RGB SHA-256, dimensions and length. All source-video hashes matched their preserved pins before and after decoding; all runs exited 0 with no missing or extra output frames. Decoder warnings/errors are saved verbatim; exit 0 does not imply clean or scientifically accepted footage.
  Current decoder: {decoder['resolved_path']} (FFmpeg 7.1.1).
  The frozen original source-frame selections, PTS/time-base records and decoder argv are retained in scope.json, groups.json, frozen-records/, recovery-recipes.json and receipts/. The original investigation Git commit is {audit['source_commit']}.
  {directcopytext}
  No full-resolution output images were written by the test, and no on-disk/app restoration or remote GitHub/Drive/LFS download was tested. Exact encoded bytes were SHA-256 compared in RAM; this is materially stronger than guessing that extraction is repeatable.

PROVENANCE LIMITS
  725 images have matched independent saved original PNG hashes. 188 are recovered archive-copy PNGs from the historically refused Camera2 and 27-Angles runs: their current recovered bytes now match video regeneration, but no independent original PNG hashes were located. This test does not retroactively create those missing hashes or clear the original processing refusals. The Dub6-44 manual-review/error state also remains unchanged.
  Byte recovery does not authenticate a building identity, event clock, edited overlay, broadcast assertion or physical cause. Replays and edited angles are not independent observations.

VISUAL REVIEW AND RELEVANCE
  Every scoped image was viewed once in one of 64 full-uncropped labeled contact pages, at up to 384x288 preview size. Eight selected native-resolution PNGs were also inspected (individual-native-review.json). This was a complete scene-level review of all 913, not a forensic review of every pixel of all native-resolution images.
  object-review.csv provides a row for every image, its observation/limitations, page/cell, source locator, exact recovery checks and recommendation. visual-review-notes.jsonl accounts for every review ID exactly once.
  Fire-like regions, poor visibility and corrupted frames are preserved alike. CNN warning captions and the BBC correspondent/collapse captions are potentially useful reporting/chronology leads; source video/audio/timing must be checked before drawing conclusions. Countdown leaders and the Stand By card retain file/edit alignment context. No unique evidence or contrary result was designated irrelevant.

PRESERVED MATERIAL AND WHERE TO RECOVER IT
  preserved-videos.csv lists every currently verified local source-video path and pin: 16 distinct videos, {sum(videogroups.values()):,} bytes total, all excluded from deletion. Some are content-addressed files without extensions in the main 911 or public submodule's .git/lfs/objects tree; preserve those Git LFS stores. Original worktree source paths in frozen receipts can be obsolete; use the verified preserved paths in the new records.
  retained-png-copies.csv lists the independent current native PNG backups. Their presence and current contents were tested, but remote recovery was not. Git LFS garbage collection/pruning must not remove these source/backup pins without a separate verified preservation plan and exact approval.
  All 1,622 other recovered image objects (1,566 core study images, six method-control objects and 50 navigation sheets) were freshly hash-checked along with every vault alias; all are excluded. Their locations and retention labels are in protected-image-objects.csv. The original recovery-manifest.json, recovery reports, prior relevance review, source/case records and all original failure labels remain unchanged. No source repository or project tree was modified by this review.
  The audit records and bounded review previews are retained in {OUT}.

WHAT REMOVAL WOULD COST AND WHAT RECOVERY STILL DEPENDS ON
  Removing this list would remove ready-to-open native PNGs and their restored original relative paths within the vault. Rebuilding those paths requires an explicit restore using the preserved maps; reduced JPEG review pages are not substitutes for exact native pixels. Historical processing failures remain failures even after restoration.
  Current recovery is verified. Future byte-identical regeneration for objects without a retained exact PNG additionally depends on the videos, frame/decoder recipes and a compatible toolchain. The decoder binary and 90 resolved Homebrew files were hashed, not packaged as a portable runtime; three @rpath dependencies and system/OS dependencies were not independently resolved/copied. Current successful decoding establishes today's recovery; a future FFmpeg/macOS upgrade may change pixels or PNG encoding. Retain the installed decoder and recovery records, and re-run hashes immediately before any approved unlink. Do not claim a future recovery test passed from this current result.
  The strongest reason to keep these local PNGs is immediate access and independence from future decoder availability. The proposed storage gain is only about half a GB at most; if that convenience is more valuable, retaining them is reasonable.

PER-GROUP VERIFIED SCOPE
{grouptext}

COMMANDS ACTUALLY RUN
  {BASE/'work/911-context-review.py'} prepare (bundled Python, -B)
  {BASE/'work/911-context-review.py'} verify (bundled Python, -B)
  {BASE/'work/911-context-finalize.py'} (bundled Python, -B)
  Plus native/preview viewing, git show of frozen records, ffmpeg -version, otool -L and dependency/content hashing.
  Full command arguments and outputs are in the saved receipts; recovery-results.csv has every actual scoped comparison. The verification process has no deletion mode. No scientific admission, publication or restoration activation was performed.

APPROVAL BOUNDARY
  The user's AGENTS.md instruction says: 'Never delete ... without first presenting the specific deletion list and obtaining the user's explicit approval for that list.' This proposal has not been approved and no files were deleted. A later approved execution must revalidate the exact CSV checksum, every current candidate inode/hash/link count and all preserved recovery sources before unlinking only these named paths; changes or failed checks require a revised review/approval.
  Deletion-list SHA-256: {sha(OUT/'proposed-deletions.csv')}
'''
    textsave(OUT/'deletion-review.txt', review)
    files = sorted(p for p in OUT.rglob('*') if p.is_file())
    save(OUT/'final-verification.json', {
        'status': 'review_complete_proposal_only_no_deletion',
        'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'visual_pages': 64, 'visual_objects_exactly_once': 913, 'additional_native_inspections': 8,
        'png_byte_and_pixel_regeneration_passed': 913, 'regeneration_failed_or_missing': 0,
        'independent_original_png_hash_objects': originalcount, 'archive_copy_no_independent_original_png_hash_objects': 913-originalcount,
        'preserved_videos': len(videogroups), 'preserved_video_routes_hashed': len(videos),
        'retained_exact_png_objects': len(copyhashes), 'retained_exact_png_routes_hashed': len(pngcopies),
        'entire_vault_objects_current_sha256_verified': len(inventory), 'entire_vault_aliases_metadata_verified': checked_aliases,
        'protected_image_objects_verified': len(protected), 'candidate_inode_count': 913,
        'exact_deletion_file_entries': len(proposed), 'unique_candidate_bytes': logical,
        'allocated_bytes_counted_once_upper_estimate': allocated, 'directories_in_deletion_list': 0,
        'all_candidate_hardlinks_accounted_for': True, 'candidate_metadata_unchanged_since_preparation': True,
        'recovery_manifest_sha256_unchanged': audit['recovery_manifest_sha256'],
        'frozen_record_files_sha256_verified': len(frozenrecords),
        'decoder_and_resolved_dependency_hashes_current': True, 'portable_runtime_backup_tested': False,
        'on_disk_restoration_tested': False, 'remote_recovery_tested': False,
        'deletions_performed': 0, 'investigation_source_files_modified': 0,
        'full_resolution_images_written_by_audit': 0, 'free_bytes_at_finalization': os.statvfs(BASE).f_bavail*os.statvfs(BASE).f_frsize,
        'review_output_logical_bytes_before_final_record': sum(p.stat().st_size for p in files),
        'deletion_list_sha256': sha(OUT/'proposed-deletions.csv'),
        'artifact_hashes': [{'path': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size} for p in files]
    })
    print(json.dumps({'complete': True, 'scope': 913, 'proposed_file_entries': len(proposed),
                      'allocated_upper_bytes': allocated, 'retained_native_png_objects': len(copyhashes),
                      'protected_objects': len(protected), 'deleted': 0,
                      'report': str(OUT/'deletion-review.txt'), 'list': str(OUT/'proposed-deletions.csv')}), flush=True)

if __name__ == '__main__':
    main()
