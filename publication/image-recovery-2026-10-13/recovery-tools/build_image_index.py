"""Expand the pre-deletion hash index without modifying archived records."""
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess

TASK = Path(__file__).resolve().parent
PRIOR = TASK.parent / '911-preservation'
REPO = '${SOURCE_CASE_REPOSITORY}'
COMMIT = '354af3e8b34e9ff3ffbb5f29e643538e090e63d1'
PREFIX = 'research/sherlock-wtc7-investigation/'
OLD_ROOT = '${SOURCE_SHERLOCK_WORKTREE}/'
records = json.loads((PRIOR / 'deletion-image-recovery-verification.json').read_text())['image_records']
index = {r['source_path']: {**r, 'expected_hashes': set(), 'hash_sources': []} for r in records}
for r in records:
    for h in r['recorded_image_hashes']:
        if isinstance(h, str):
            index[r['source_path']]['expected_hashes'].add(h)
        elif isinstance(h, dict):
            for k in ['sha256', 'png_sha256', 'hash']:
                if k in h:
                    index[r['source_path']]['expected_hashes'].add(h[k])

def add(path, digest, source, parent=None):
    if not isinstance(path, str) or not isinstance(digest, str) or not re.fullmatch('[a-f0-9]{64}', digest):
        return
    if path.startswith(OLD_ROOT):
        path = path[len(OLD_ROOT):]
    elif not path.startswith(PREFIX) and parent is not None and not path.startswith('/'):
        path = str(Path(parent) / path)
    if path in index:
        index[path]['expected_hashes'].add(digest)
        if source not in index[path]['hash_sources']:
            index[path]['hash_sources'].append(source)

def walk(node, source, parent):
    if isinstance(node, list):
        for x in node:
            walk(x, source, parent)
    elif isinstance(node, dict):
        for pathkey in ['file', 'path']:
            if pathkey in node:
                for hashkey in ['png_sha256', 'sha256']:
                    if hashkey in node:
                        add(node[pathkey], node[hashkey], source, parent)
        for k, v in node.items():
            if k.endswith(('.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff')):
                if isinstance(v, str):
                    add(k, v, source, parent)
                elif isinstance(v, dict):
                    add(k, v.get('sha256') or v.get('png_sha256'), source, parent)
            if isinstance(v, (dict, list)):
                walk(v, source, parent)

tree = subprocess.check_output(['git', '-C', REPO, 'ls-tree', '-rlz', COMMIT])
metadata = []
for entry in tree.split(b'\0'):
    if not entry:
        continue
    left, path = entry.split(b'\t', 1)
    mode, kind, oid, size = left.split()
    path = path.decode()
    if path.startswith(PREFIX) and path.endswith('.json') and int(size) < 32_000_000:
        metadata.append((path, oid.decode(), int(size)))
batch = subprocess.Popen(['git', '-C', REPO, 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
for path, oid, size in metadata:
    batch.stdin.write((oid+'\n').encode()); batch.stdin.flush()
    header = batch.stdout.readline().split()
    actual_size = int(header[-1])
    data = batch.stdout.read(actual_size)
    if batch.stdout.read(1) != b'\n':
        raise RuntimeError('batch framing')
    try:
        doc = json.loads(data)
    except (ValueError, UnicodeDecodeError):
        continue
    walk(doc, path, str(Path(path).parent))
batch.stdin.close(); batch.wait()
for r in index.values():
    r['expected_hashes'] = sorted(r['expected_hashes'])
summary = {'images': len(index), 'with_saved_hash': sum(bool(r['expected_hashes']) for r in index.values()),
           'multiple_saved_hashes': sum(len(r['expected_hashes']) > 1 for r in index.values()),
           'metadata_files_checked': len(metadata),
           'by_study': {study: {'images': len(rs), 'with_saved_hash': sum(bool(r['expected_hashes']) for r in rs)}
                        for study, rs in __import__('itertools').groupby(sorted(index.values(), key=lambda r: r['source_path'].split('/')[2]), key=lambda r: r['source_path'].split('/')[2])
                        for rs in [list(rs)]}}
result = {'source_repository': REPO, 'source_commit': COMMIT, 'summary': summary, 'images': list(index.values())}
with (TASK / 'expanded-image-index.json').open('x') as f:
    json.dump(result, f, indent=2)
print(json.dumps(summary, indent=2))
