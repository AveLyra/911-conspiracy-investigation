"""Recover exact image bytes to a separate, internally deduplicated vault."""
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

TASK = Path(__file__).resolve().parent
VAULT = TASK.parents[1] / 'outputs/911-image-recovery'
FILES = VAULT / 'files'
OBJECTS = VAULT / '.objects'
INDEX = json.loads((TASK / 'expanded-image-index.json').read_text())
PRIVATE = '${SOURCE_CASE_REPOSITORY}'
PUBLIC = '${SOURCE_CASE_REPOSITORY}/research/911-conspiracy-investigation-public'
PUBLIC_COMMIT = 'b560f1823b23734f43cc5605a9eaf515a1e0f725'
LFS_ROOTS = [Path('${SOURCE_CASE_REPOSITORY}/.git/lfs/objects'),
             Path('${SOURCE_CASE_REPOSITORY}/.git/modules/911-conspiracy-investigation-public/lfs/objects')]

def digest_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def lfs_path(digest):
    for root in LFS_ROOTS:
        p = root / digest[:2] / digest[2:4] / digest
        if p.is_file():
            return p

def store(path=None, data=None, expected=None):
    if shutil.disk_usage('/').free < 4_000_000_000:
        raise RuntimeError('Recovery stopped before crossing the 4 GB free-space reserve')
    digest = digest_file(path) if path is not None else hashlib.sha256(data).hexdigest()
    if expected and digest != expected:
        raise ValueError('Source content hash mismatch')
    target = OBJECTS / digest[:2] / digest
    if target.exists():
        if digest_file(target) != digest:
            raise ValueError('Existing recovery object mismatch')
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    if path is not None:
        # APFS clone: separate mutable inode, without copying all source blocks.
        result = subprocess.run(['/bin/cp', '-c', '-n', str(path), str(target)], capture_output=True)
        if result.returncode:
            raise RuntimeError('Non-destructive APFS clone failed: ' + result.stderr.decode()[:500])
    else:
        with target.open('xb') as f:
            f.write(data)
    if digest_file(target) != digest:
        raise ValueError('Recovery object verification failed')
    target.chmod(0o444)
    return target

def bind(record, obj, method, source):
    target = FILES / record['source_path']
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if digest_file(target) != obj.name:
            raise ValueError('Refusing to overwrite an existing restored image')
    else:
        os.link(obj, target)
    if target.stat().st_size != record['original_size']:
        raise ValueError('Restored file differs from saved pre-deletion size: '+record['source_path'])
    return {**record, 'restored_path': str(target), 'sha256': obj.name,
            'recovery_method': method, 'recovery_source': str(source),
            'original_hash_verified': obj.name in record['expected_hashes']}

def main():
    public_tree = {}
    for entry in subprocess.check_output(['git', '-C', PUBLIC, 'ls-tree', '-rz', PUBLIC_COMMIT]).split(b'\0'):
        if entry:
            left, path = entry.split(b'\t', 1)
            public_tree[path.decode()] = left.split()[2].decode()
    restored, unresolved, mismatches = [], [], []
    prior = VAULT / 'recovery-manifest.json'
    previous = {r['source_path']: r for r in json.loads(prior.read_text())['restored']} if prior.exists() else {}
    cache = {}
    for record in INDEX['images']:
        p = record['source_path']
        if p in previous:
            r = previous[p]
            if digest_file(r['restored_path']) != r['sha256']:
                raise ValueError('Previously recovered image mismatch')
            restored.append(r)
            continue
        obj = None
        for digest in record['expected_hashes']:
            found = lfs_path(digest)
            own = OBJECTS / digest[:2] / digest
            if own.exists():
                obj = own; method = 'previously_recovered_identical_bytes'; source = own
                break
            if found is not None:
                obj = cache.get(digest)
                if obj is None:
                    obj = store(path=found, expected=digest); cache[digest] = obj
                method = 'retained_lfs_bytes_match_saved_original_hash'; source = found
                break
        if obj is None and record['public_path'] in public_tree:
            oid = public_tree[record['public_path']]
            data = subprocess.check_output(['git', '-C', PUBLIC, 'cat-file', 'blob', oid])
            pointer = re.search(rb'oid sha256:([a-f0-9]{64})\nsize (\d+)', data)
            if pointer:
                digest = pointer[1].decode(); size = int(pointer[2]); found = lfs_path(digest)
                if found is not None:
                    obj = cache.get(digest)
                    if obj is None:
                        obj = store(path=found, expected=digest); cache[digest] = obj
                    method = 'same_path_published_archive_lfs'; source = PUBLIC_COMMIT+':'+record['public_path']
            else:
                obj = store(data=data); method = 'same_path_published_archive_git_blob'; source = PUBLIC_COMMIT+':'+record['public_path']
            if obj is not None and record['expected_hashes'] and obj.name not in record['expected_hashes']:
                mismatches.append({'source_path': p, 'saved_hashes': record['expected_hashes'], 'archive_hash': obj.name})
                obj = None
        if obj is None:
            unresolved.append(record)
        else:
            restored.append(bind(record, obj, method, source))
    summary = {'total_requested_images': len(INDEX['images']), 'restored_images': len(restored),
               'restored_with_saved_original_hash_match': sum(r['original_hash_verified'] for r in restored),
               'unresolved_images': len(unresolved), 'source_mismatches': len(mismatches),
               'unique_recovered_image_objects': len({r['sha256'] for r in restored}),
               'logical_restored_bytes': sum(r['original_size'] for r in restored),
               'free_bytes': shutil.disk_usage('/').free,
               'unresolved_by_study': dict(collections.Counter(r['source_path'].split('/')[2] for r in unresolved))}
    result = {'summary': summary, 'source_commit': INDEX['source_commit'], 'public_copy_commit': PUBLIC_COMMIT,
              'restored': restored, 'unresolved': unresolved, 'mismatches': mismatches,
              'layout': 'Read-only object copies; duplicate paths are hardlinks inside this recovery vault. Source cache inodes are not hardlinked.'}
    VAULT.mkdir(parents=True, exist_ok=True)
    # The manifest describes this task's evolving output, never source evidence.
    with prior.open('w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps(summary, indent=2), flush=True)

if __name__ == '__main__':
    main()
