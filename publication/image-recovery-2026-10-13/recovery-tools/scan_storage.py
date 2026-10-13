"""Read-only allocation scan since the saved cleanup measurement."""
import collections
import datetime
import heapq
import json
import os
from pathlib import Path
import shutil
import stat
import time

TASK = Path(__file__).resolve().parent
BASELINE = TASK.parent / '911-preservation/space-after-cleanup.json'
since = BASELINE.stat().st_mtime
roots = [Path('${SOURCE_USER_HOME}'), Path('/private/tmp'), Path('/private/var/folders')]
groups = collections.defaultdict(lambda: collections.Counter())
largest_new = []
largest_modified = []
errors = collections.Counter()
seen = set()
started = time.time()
before = shutil.disk_usage('/')

def group_for(path):
    s = str(path)
    for prefix, depth in [('${SOURCE_USER_HOME}/Library/', 2), ('${SOURCE_USER_HOME}/dev/', 1),
                          ('${SOURCE_CASE_REPOSITORY}/', 1), ('${SOURCE_USER_HOME}/.codex/', 1),
                          ('${SOURCE_USER_HOME}/Documents/Codex/', 2)]:
        if s.startswith(prefix):
            return prefix + '/'.join(s[len(prefix):].split('/')[:depth])
    return '/'.join(s.split('/')[:5])

def keep(heap, size, path, info):
    heapq.heappush(heap, (size, str(path), info))
    if len(heap) > 45:
        heapq.heappop(heap)

for root in roots:
    stack = [root]
    while stack:
        directory = stack.pop()
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    try:
                        s = entry.stat(follow_symlinks=False)
                        if stat.S_ISDIR(s.st_mode):
                            stack.append(Path(entry.path))
                            continue
                        if not stat.S_ISREG(s.st_mode):
                            continue
                        identity = (s.st_dev, s.st_ino)
                        if s.st_nlink > 1:
                            if identity in seen:
                                continue
                            seen.add(identity)
                        g = groups[group_for(entry.path)]
                        g['files'] += 1
                        g['allocated_bytes'] += s.st_blocks * 512
                        g['logical_bytes'] += s.st_size
                        birth = getattr(s, 'st_birthtime', 0)
                        info = {'bytes': s.st_size, 'allocated_bytes': s.st_blocks * 512,
                                'birth_utc': datetime.datetime.fromtimestamp(birth, datetime.timezone.utc).isoformat(),
                                'modified_utc': datetime.datetime.fromtimestamp(s.st_mtime, datetime.timezone.utc).isoformat()}
                        if birth >= since:
                            g['new_files'] += 1
                            g['new_file_logical_bytes'] += s.st_size
                            g['new_file_allocated_bytes'] += s.st_blocks * 512
                            if s.st_size >= 10_000_000:
                                keep(largest_new, s.st_size, entry.path, info)
                        elif s.st_mtime >= since:
                            g['older_modified_files'] += 1
                            g['older_modified_current_bytes'] += s.st_size
                            if s.st_size >= 10_000_000:
                                keep(largest_modified, s.st_size, entry.path, info)
                    except OSError as e:
                        errors[type(e).__name__] += 1
        except OSError as e:
            errors[type(e).__name__] += 1

after = shutil.disk_usage('/')
result = {'started_utc': datetime.datetime.fromtimestamp(started, datetime.timezone.utc).isoformat(),
          'baseline_timestamp_utc': datetime.datetime.fromtimestamp(since, datetime.timezone.utc).isoformat(),
          'baseline': json.loads(BASELINE.read_text()), 'free_bytes_before_scan': before.free,
          'free_bytes_after_scan': after.free, 'elapsed_seconds': time.time() - started,
          'groups': dict(groups), 'unreadable_counts': dict(errors),
          'largest_new_files': [{'path': p, **i} for _, p, i in sorted(largest_new, reverse=True)],
          'largest_older_modified_files': [{'path': p, **i} for _, p, i in sorted(largest_modified, reverse=True)],
          'limits': ['No earlier per-file baseline exists for most directories; modified old file sizes are not growth measurements.',
                     'New file allocation can overcount APFS shared blocks; creation time can reflect cloning or copying.',
                     'Protected directories are not fully accessible. No files or processes were removed or stopped.']}
with (TASK / 'storage-growth-scan.json').open('x') as f:
    json.dump(result, f, indent=2)
print(json.dumps({'elapsed_seconds': result['elapsed_seconds'], 'free_bytes': after.free,
                  'new_file_groups': sorted([{'group': k, **v} for k, v in groups.items()],
                                            key=lambda x: x.get('new_file_allocated_bytes', 0), reverse=True)[:18],
                  'largest_new_files': result['largest_new_files'][:12],
                  'largest_older_modified_files': result['largest_older_modified_files'][:8],
                  'unreadable_counts': result['unreadable_counts']}, indent=2))
