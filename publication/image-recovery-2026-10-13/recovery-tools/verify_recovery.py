"""Read back every recovered path and independently check its saved identity."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
from PIL import Image

TASK = Path(__file__).resolve().parent
VAULT = TASK.parents[1] / 'outputs/911-image-recovery'
manifest = json.loads((VAULT / 'recovery-manifest.json').read_text())
index = json.loads((TASK / 'expanded-image-index.json').read_text())
expected = {r['source_path']: r for r in index['images']}
paths = [r['source_path'] for r in manifest['restored']]
if len(paths) != len(set(paths)) or set(paths) != set(expected) or manifest['unresolved']:
    raise RuntimeError('Restored path population does not equal the original deletion inventory')

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

checked = {}
counts = Counter()
logical = 0
for row in manifest['restored']:
    p = Path(row['restored_path'])
    s = p.stat()
    identity = (s.st_dev, s.st_ino)
    obj = VAULT / '.objects' / row['sha256'][:2] / row['sha256']
    if identity != (obj.stat().st_dev, obj.stat().st_ino):
        raise RuntimeError('Recovered alias is not linked to its recovery object')
    if s.st_size != expected[row['source_path']]['original_size']:
        raise RuntimeError('Pre-deletion file size mismatch')
    if identity not in checked:
        digest = sha(p)
        with Image.open(p) as im:
            im.verify()
        checked[identity] = {'sha256': digest, 'bytes': s.st_size, 'allocated_bytes': s.st_blocks*512}
    digest = checked[identity]['sha256']
    if digest != row['sha256']:
        raise RuntimeError('Recovery manifest hash mismatch')
    original_hashes = expected[row['source_path']]['expected_hashes']
    if original_hashes:
        if digest not in original_hashes:
            raise RuntimeError('Saved original PNG hash mismatch')
        counts['saved_original_hash_match'] += 1
    elif row['recovery_method'] == 'equivalent_extraction_original_hash_unavailable':
        counts['equivalent_reconstruction_original_hash_unavailable'] += 1
    else:
        counts['archived_copy_original_hash_unavailable'] += 1
    if s.st_mode & 0o222:
        raise RuntimeError('Recovery image object unexpectedly writable')
    logical += s.st_size

human = []
for n in [274,300,342,365,388,411]:
    rel = 'research/sherlock-wtc7-investigation/distant-view-source-screen/continuity-274-411/run01/native/frame-'+str(n).zfill(4)+'.png'
    p = VAULT / 'files' / rel
    if sha(p) not in expected[rel]['expected_hashes']:
        raise RuntimeError('Human review frame mismatch')
    human.append({'frame': n, 'path': str(p), 'original_sha256_verified': True})

result = {'verified_at_utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
          'manifest_sha256': sha(VAULT / 'recovery-manifest.json'), 'restored_paths_verified': len(paths),
          'unique_image_objects_read_and_image_format_verified': len(checked), 'counts': dict(counts),
          'logical_image_bytes': logical, 'unique_image_bytes': sum(r['bytes'] for r in checked.values()),
          'unique_image_allocated_bytes_before_APFS_sharing': sum(r['allocated_bytes'] for r in checked.values()),
          'free_bytes_at_verification': shutil.disk_usage('/').free, 'human_review_frames': human,
          'limitations': ['377 images lack a separately saved original-file hash; archived copies and equivalent reconstructions are distinguished.',
                          'Image recovery does not supply human review, original-camera authentication or a new scientific finding.',
                          'APFS clones share source blocks. Filesystem free-space changes also include concurrent background work.'],
          'files_deleted_during_recovery': 0, 'uploads_during_recovery': 0}
with (VAULT / 'verification.json').open('x') as f:
    json.dump(result, f, indent=2)

scan = json.loads((TASK / 'storage-growth-scan.json').read_text())
baseline = scan['baseline']['free']
free = result['free_bytes_at_verification']
g = scan['groups']
backup_dir = TASK.parents[1] / 'outputs/chat-cleanup-2026-10-11'
backups = json.loads((backup_dir / 'deletion-list.json').read_text())
backup_bytes = sum(Path(r['path']).stat().st_size for r in backups['temporary_local_files'])
vm = Path('${SOURCE_USER_HOME}/dev/patamaps/patamaps/.tools/linux-vm/disk.raw').stat()

report = f'''RECOVERY AND STORAGE REPORT
Verified {result['verified_at_utc']}.

Recovery
All 5,344 deleted image paths are populated in the separate recovery vault:
{VAULT / 'files'}
4,967 match preserved original PNG/file hashes. Every recovered path was read
back; all 2,535 distinct image objects passed file hashing and image-format
verification. No mismatches or unresolved image paths remain in the inventory.

The other 377 images have a narrower recovery claim: 188 are same-path published
archive copies with matching pre-deletion sizes but no located separate original
hash; 189 are equivalent reconstructions for an earlier refused Clip 3 extraction.
The latter use the same saved source and decoder options as a verified repeat
and match the pre-deletion sizes. They are explicitly labeled; byte identity to
that original refused run cannot be independently certified. Its original
failure/diagnostic records and refusal remain preserved in Git.

All accepted native frames in the previously missing CBS and DistantView groups
regenerated with their saved PNG/RGB or luminance hashes. DistantView's complete
487,618,560-byte decoded stream also matched the saved original aggregate hash.
All six pending human-review frames (274, 300, 342, 365, 388, 411) are restored
and original-hash verified. Review itself remains pending.

Storage-conscious layout
The 5,344 logical files contain {logical:,} bytes (3.34 GB); duplicates share
2,535 read-only image objects totaling {result['unique_image_bytes']:,} bytes
(1.63 GB). Source-copy objects use separate APFS clone inodes, which further
share blocks with retained cache bytes. Alias paths are hardlinks only inside
the recovery vault. No additional full project checkout was created.
The images may be read normally; copy a file before editing it.

The source snapshot is roryscot/911 commit
354af3e8b34e9ff3ffbb5f29e643538e090e63d1. Published-copy inputs use commit
b560f1823b23734f43cc5605a9eaf515a1e0f725 in the retained public checkout.
The earlier audit's 2,009 located copies and 1,295 original-hash matches are
superseded: expanded metadata parsing found hashes for 4,967 images and 2,141
paths with usable existing bytes; subsequent regeneration completed the set.
The original reports remain historical observations, not permanent-loss findings.
The 102 caches were not rebuilt; they have little substantive investigation
content. Font/Python caches can be regenerated operationally; Finder's previous
folder metadata may not be reproducible. Cache byte recovery was not attempted.
No original-source,
observation-note or numerical-result loss was identified in this image recovery.

Disk growth
The cleanup measurement at {scan['baseline_timestamp_utc']} recorded
{baseline:,} free bytes (44.88 GB), after a gain of 30.71 GB.
At verification, free space is {free:,} bytes ({free/1e9:.2f} GB), approximately
{(baseline-free)/1e9:.2f} GB below that measurement.

Largest newly created file allocations observed since that timestamp:
- ${SOURCE_USER_HOME}/dev/tmp: {g['${SOURCE_USER_HOME}/dev/tmp']['new_file_allocated_bytes']/1e9:.2f} GB,
  predominantly Wargame Workbench build and retained test products.
- ${SOURCE_USER_HOME}/dev/patamaps: {g['${SOURCE_USER_HOME}/dev/patamaps']['new_file_allocated_bytes']/1e9:.2f} GB,
  including a new Linux VM disk using {vm.st_blocks*512/1e9:.2f} GB of allocated
  storage. The VM disk is sparse: its 34.36 GB logical size is not occupied space.
- /private/var/folders/tr: {g['/private/var/folders/tr']['new_file_allocated_bytes']/1e9:.2f} GB,
  including temporary installation/test work. A Wargame clean-install copy alone
  currently accounts for about 6.33 GB of directory allocation.
- Separate chat-backup packaging/readback: {backup_bytes/1e9:.2f} GB in 38 current
  files under {backup_dir}. The prior backup report records full private-Drive
  remote recovery verification; its deletion proposal remains approval-pending.

These are allocation observations, not an exact additive explanation of the
free-space change: APFS clones can share blocks, old files can grow, other work
can remove files, and some protected paths were inaccessible. The scan cannot
measure growth in old files without an earlier per-file baseline. New development
builds, VM storage and temporary copies are the strongest documented explanation
for the renewed pressure; no evidence makes old chats the primary new contributor.
System VM storage is also substantial, but its growth was not established.

Next storage work
Review retained Rust build versions and temporary test copies with their owning
projects. Check recovery for any unique database/VM state or assurance outputs
before considering deletion. The verified chat-backup packaging duplicates are
a separate, already itemized cleanup candidate. No additional deletion was
performed here; exact-list approval remains required under the user's AGENTS.md.
Verified redundant copies are acceptable cleanup targets; preserving valuable
investigation material with a tested recovery route is the user's priority.

Verification commands actually run
- python3 work/911-recovery/build_image_index.py
- python3 work/911-recovery/recover_images.py
- ${SOURCE_USER_HOME}/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B work/911-recovery/regenerate_native_images.py
- ${SOURCE_USER_HOME}/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B work/911-recovery/verify_recovery.py
- python3 work/911-recovery/scan_storage.py
- df, scoped du and read-only Git tree/blob inspection.
The FFmpeg binary hash matched the saved DistantView decoder; Pillow was 12.3.0.
No rescoring, motion fitting, new scientific acceptance, deletion or upload ran.

Recovery records
{VAULT / 'recovery-manifest.json'}
{VAULT / 'verification.json'}
{VAULT / 'regeneration-receipts'}
{TASK / 'expanded-image-index.json'}
{TASK / 'storage-growth-scan.json'}

Resume
Use the manifest's restored_path for each original source_path; protocols,
observations and source declarations remain in the archived Git snapshot.
Keep original-hash verification separate from archive-only and reconstructed
duplicate status. A future active worktree can materialize selected recovered
inputs from this vault without re-decoding or cloning the entire repository.
'''
with (TASK.parents[1] / 'outputs/911-recovery-and-space-report.txt').open('x') as f:
    f.write(report)
with (VAULT / 'RECOVERY.txt').open('x') as f:
    f.write(report)
print(json.dumps({k: result[k] for k in ['status','restored_paths_verified','unique_image_objects_read_and_image_format_verified','counts','unique_image_bytes','free_bytes_at_verification']}, indent=2))
