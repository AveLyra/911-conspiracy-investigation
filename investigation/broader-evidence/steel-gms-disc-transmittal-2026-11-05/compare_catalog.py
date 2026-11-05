"""Compare public catalog paths and declared sizes without opening media."""
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json
import re
import sys

from inspect_release32 import read_bencode


manifest = Path(sys.argv[1]).read_bytes()
digest = hashlib.sha256(manifest).hexdigest()
if digest != "f5b35756ef065710c2b602fac70e42044e04a50df48c7420a8f7627cdf9d7163":
    raise ValueError("Manifest bytes differ from the source pin")

entries = read_bencode(manifest)[b"info"][b"files"]
paths = [
    (tuple(part.decode("utf-8") for part in row[b"path"]), row[b"length"])
    for row in entries
]
groups = defaultdict(Counter)
for parts, _ in paths:
    for i, part in enumerate(parts):
        if re.search(r"(?i)WTCI[- ]0*(93|102|134|143)[- ]I\b", part):
            groups["/".join(parts[i - 1:i + 1])][Path(parts[-1]).suffix.lower()] += 1


def by_basename(disc):
    result = defaultdict(list)
    for parts, size in paths:
        if disc in parts:
            result[parts[-1].casefold()].append(size)
    return result


gms8 = by_basename("42A0375 - G33D9")
multiple = by_basename("42A0377 - G33D11")
shared = gms8.keys() & multiple.keys()
pairs = [(a, b) for name in shared for a in gms8[name] for b in multiple[name]]
prior = json.loads(Path(sys.argv[2]).read_text())
anchors = {
    Path(entry["catalog_path"]).name.casefold()
    for series in prior["candidate_series"].values()
    for entry in series.values()
}
print(json.dumps({
    "file_paths": len(paths),
    "groups_by_extension": groups,
    "shared_casefolded_basenames": len(shared),
    "candidate_pairs": len(pairs),
    "pairs_with_equal_declared_length": sum(a == b for a, b in pairs),
    "previous_anchor_basenames": len(anchors),
    "previous_anchors_in_42A0375": len(anchors & gms8.keys()),
    "previous_anchors_in_42A0377": len(anchors & multiple.keys()),
}, indent=2, sort_keys=True))
