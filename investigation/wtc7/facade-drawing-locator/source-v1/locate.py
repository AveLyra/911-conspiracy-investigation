"""Bounded local path/member locator; no content extraction or raw names exported."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
MAIN = Path('/Users/admin/docs/911')
WORK = HERE.parents[2]
ROOTS = {**{'main_'+name.replace('/', '_'): MAIN/name for name in
           ('authority', 'research', 'exhibits/raw', 'exhibits/processed', 'filings/exhibits')},
         'worktree_research': WORK/'research'}
TERMS = {key: re.compile(pattern, re.I) for key, pattern in
         {'drawing': r'drawing', 'elevation': r'elevation', 'roth': r'roth',
          'louver': r'louver', 'louvre': r'louvre', 'curtain': r'curtain',
          'architect': r'architect'}.items()}
INVENTORY_TERM = re.compile(r'\b(drawings?|elevations?|Roth|louvers?|louvres?|curtain|architectural)\b', re.I)
BLOCKED_NAME = re.compile(r'(?:NIST.*FOIA.*(?:11[-_]209|12[-_]009)|(?:11[-_]209|12[-_]009).*\.zip)', re.I)
OTHER_CONTAINERS = {'.7z', '.rar', '.tar', '.tgz', '.gz', '.bz2', '.xz'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        while chunk := stream.read(1024*1024):
            h.update(chunk)
            size += len(chunk)
    return {'sha256': h.hexdigest(), 'bytes': size}


def term_hits(name):
    return [key for key, rx in TERMS.items() if rx.search(name)]


def listed(root):
    if not root.exists():
        return [], 'absent'
    result = subprocess.run(['rg', '--files', '--hidden', '--no-ignore', '-0', str(root)],
                            capture_output=True, check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError('Declared path listing failed; stderr not exported')
    paths = [Path(p.decode()) for p in result.stdout.split(b'\0') if p]
    paths = [p for p in paths if not p.is_relative_to(HERE)]
    return sorted(paths), 'listed'


def archive_metadata(path):
    size = path.stat().st_size
    if size > 1024**3:
        return {'status': 'over_byte_cap', 'bytes': size}
    if path.is_symlink():
        return {'status': 'symlink_not_opened', 'bytes': size}
    if BLOCKED_NAME.search(str(path)):
        return {'status': 'prior_approval_boundary_not_opened', 'bytes': size}
    try:
        with path.open('rb') as stream:
            stream.seek(max(0, size-65557))
            tail = stream.read(65557)
        index = tail.rfind(b'PK\x05\x06')
        if index < 0 or index+22 > len(tail):
            return {'status': 'no_bounded_eocd', 'bytes': size}
        fields = struct.unpack('<4s4H2LH', tail[index:index+22])
        _, disk, directory_disk, disk_entries, total_entries, directory_size, offset, comment = fields
        if index+22+comment != len(tail):
            return {'status': 'ambiguous_or_trailing_eocd', 'bytes': size}
        if disk or directory_disk or disk_entries != total_entries:
            return {'status': 'multidisk_not_listed', 'bytes': size}
        if total_entries == 65535 or directory_size == 0xffffffff or offset == 0xffffffff:
            return {'status': 'zip64_not_listed', 'bytes': size}
        if total_entries > 100000 or directory_size > 32*1024**2:
            return {'status': 'directory_cap', 'bytes': size}
        before = pin(path)
        with zipfile.ZipFile(path) as archive:
            entries = archive.infolist()
            if len(entries) != total_entries:
                raise ValueError('Central directory count mismatch')
            names = [i.filename for i in entries]
            hits = [{'member_name_sha256': sha(i.filename.encode()),
                     'suffix': Path(i.filename).suffix.lower(),
                     'terms': term_hits(i.filename), 'uncompressed_bytes': i.file_size,
                     'encrypted': bool(i.flag_bits & 1), 'directory': i.is_dir()}
                    for i in entries if term_hits(i.filename)]
        after = pin(path)
        if before != after:
            raise RuntimeError('Archive changed during metadata read')
        return {'status': 'members_listed_no_payload_read', **before,
                'member_count': len(entries),
                'member_name_catalog_sha256': sha(b''.join(n.encode()+b'\0' for n in names)),
                'matches': hits,
                'nested_container_count': sum(Path(n).suffix.lower() in {'.zip','.trz',*OTHER_CONTAINERS} for n in names)}
    except (OSError, zipfile.BadZipFile, ValueError, struct.error) as error:
        return {'status': 'metadata_read_failed', 'exception_class': type(error).__name__, 'bytes': size}


def inventory_check():
    specs = [('intake/source-inventory.csv', 'source_id',
              ('title','document_type','original_filename','current_path','status','notes')),
             ('exhibits/index/exhibit-map.csv', 'exhibit_number',
              ('title','relevance','file_path','notes'))]
    output = []
    for name, identity, fields in specs:
        path = MAIN/name
        before = pin(path)
        with path.open(newline='') as stream:
            reader = csv.DictReader(stream)
            if any(f not in reader.fieldnames for f in (identity,*fields)):
                raise ValueError('Required inventory field missing')
            rows = list(reader)
        matches = [{'record_id': row[identity], 'matched_fields':
                    [field for field in fields if INVENTORY_TERM.search(row.get(field) or '')]}
                   for row in rows if any(INVENTORY_TERM.search(row.get(field) or '') for field in fields)]
        assert before == pin(path)
        output.append({'source': name, 'pin': before, 'searched_fields': fields,
                       'rows': len(rows), 'matches': matches})
    return output


def run():
    roots = []
    for label, root in ROOTS.items():
        paths, status = listed(root)
        rel = [p.relative_to(root).as_posix() for p in paths]
        output = {'root': label, 'status': status, 'path_count': len(paths),
                  'relative_path_catalog_sha256': sha(b''.join(s.encode()+b'\0' for s in rel)),
                  'matches': [], 'zip_metadata': [], 'other_containers': []}
        for path, name in zip(paths, rel):
            identifier = sha(name.encode())
            suffix = path.suffix.lower()
            hit = term_hits(name)
            if hit:
                output['matches'].append({'relative_path_sha256': identifier, 'suffix': suffix, 'terms': hit})
            if suffix in ('.zip', '.trz'):
                output['zip_metadata'].append({'relative_path_sha256': identifier,
                                               'suffix': suffix, **archive_metadata(path)})
            elif suffix in OTHER_CONTAINERS:
                output['other_containers'].append({'relative_path_sha256': identifier, 'suffix': suffix,
                                                  'status': 'not_member_listed'})
        paths_after, status_after = listed(root)
        assert paths == paths_after and status == status_after, 'Path set changed during read'
        roots.append(output)
    return {'path_term_patterns': {k:v.pattern for k,v in TERMS.items()},
            'inventory_pattern': INVENTORY_TERM.pattern, 'roots': roots,
            'canonical_inventories': inventory_check(),
            'scope': 'path/member-name locator only; no archive extraction, PDF reading or drawing absence claim'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, choices=('run01','run02'))
    args = parser.parse_args()
    out = HERE/args.out
    if out.exists():
        raise FileExistsError('Refusing existing output')
    dependencies = [HERE/'PROTOCOL.md',Path(__file__),Path(sys.executable)]
    before = {str(p): pin(p) for p in dependencies}
    result = run()
    after = {str(p): pin(p) for p in dependencies}
    assert before == after
    out.mkdir()
    with (out/'results.json').open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    with (out/'receipt.json').open('x') as stream:
        json.dump({'before':before,'after':after,'python':sys.version,'results':pin(out/'results.json')},stream,indent=2)
        stream.write('\n')
    print(json.dumps({'roots':len(result['roots']),
                      'paths':sum(r['path_count'] for r in result['roots']),
                      'path_matches':sum(len(r['matches']) for r in result['roots']),
                      'archives':sum(len(r['zip_metadata']) for r in result['roots']),
                      'results':pin(out/'results.json')}))


if __name__ == '__main__':
    main()
