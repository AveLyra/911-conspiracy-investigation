"""Read-only scoped holdings and PDF checks; no native UAF solver verification."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

import fitz


NATIVE = {'.inp', '.cae', '.odb', '.s2k', '.sdb', '.sdbk', '.s$k', '.cdb'}
ARCHIVES = {'.zip', '.7z', '.rar', '.tar', '.gz', '.bz2', '.xz'}
PINS = {
    'uaf': 'f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa',
    'uaf_other': '41dd3390627fac24c2bd696160c48f15e05d3213cc05325c4e4e89608df96d27',
    'nist': '30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f',
    'wrapper': '9f5ed822b4f5b28efef1051d731eb64d27547ef44903c897fe946c806267f25d',
}
README_PIN = '96a368fccb099aee2ee95a1a0c6fb83cdf02560077a6b9eebc864041293c0e4f'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def classify(names):
    return {
        'native_suffix_candidates': sorted(n for n in names if Path(n).suffix.lower() in NATIVE),
        'archive_candidates': sorted(n for n in names if Path(n).suffix.lower() in ARCHIVES),
    }


def inventory(root):
    if not root.is_dir():
        return {'available': False, 'path_count': None, 'errors': ['Declared directory is unavailable.']}
    command = ['rg', '--files', '-uuu', '--no-follow', '-0', '-g', '!**/.git/**', '-g', '!.git', str(root)]
    try:
        completed = subprocess.run(command, capture_output=True, timeout=45)
    except subprocess.TimeoutExpired:
        return {'available': True, 'path_count': None, 'errors': ['45-second enumeration bound exceeded; no absence inference.']}
    errors = [completed.stderr.decode(errors='replace')] if completed.stderr else []
    if completed.returncode not in (0, 1):
        errors.append('Enumeration exited ' + str(completed.returncode))
    names = [Path(os_name.decode()).relative_to(root).as_posix() for os_name in completed.stdout.split(b'\0') if os_name]
    names.sort()
    return {
        'available': True, 'path_count': len(names),
        'sorted_relative_paths_sha256': digest(('\n'.join(names) + '\n').encode()),
        'symlink_policy': 'rg --no-follow; symlink destinations not inventoried', 'errors': errors, **classify(names),
    }


def zip_manifest(path):
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        if len(infos) > 10000:
            raise ValueError('Archive member-count bound exceeded; do not extract.')
        records = []
        for info in infos:
            row = {'name': info.filename, 'bytes': info.file_size,
                   'compressed_bytes': info.compress_size, 'crc32': f'{info.CRC:08x}'}
            if info.filename == 'readme.txt' and info.file_size <= 65536:
                row['sha256'] = digest(archive.read(info))
            records.append(row)
        return {'members': records, **classify([i.filename for i in infos])}


def archive_directory_summary(path):
    manifest = zip_manifest(path)
    size = path.stat().st_size
    return {
        'archive_bytes': size,
        'archive_sha256': file_hash(path) if size <= 64 * 1024 * 1024 else None,
        'member_count': len(manifest['members']),
        'directory_records_sha256': digest(json.dumps(manifest['members'], sort_keys=True).encode()),
        'native_suffix_candidates': manifest['native_suffix_candidates'],
        'nested_archive_candidates': manifest['archive_candidates'],
        'scope': 'ZIP central directory only; native payloads not decompressed. Whole-file SHA omitted above 64 MiB.',
    }


def main():
    parser = argparse.ArgumentParser()
    for key in PINS:
        parser.add_argument('--' + key.replace('_', '-'), type=Path, required=True)
    parser.add_argument('--public-repo', type=Path, required=True)
    parser.add_argument('--physical-root', action='append', default=[], help='LABEL=PATH')
    parser.add_argument('--review-dir', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    paths = {key: getattr(args, key) for key in PINS}
    before = {key: file_hash(p) for key, p in paths.items()}
    checks = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    for key, pin in PINS.items():
        check(key + ' source hash matches', before[key] == pin)
    roots = {}
    for item in args.physical_root:
        label, value = item.split('=', 1)
        roots[label] = inventory(Path(value))
    tree = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', 'HEAD'], cwd=args.public_repo, text=True).splitlines()
    tracked = {'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.public_repo, text=True).strip(),
               'path_count': len(tree), 'sorted_relative_paths_sha256': digest(('\n'.join(sorted(tree)) + '\n').encode()), **classify(tree)}
    wrapper = zip_manifest(paths['wrapper'])
    check('wrapper has only the known README', len(wrapper['members']) == 1 and wrapper['members'][0]['name'] == 'readme.txt')
    check('wrapper README hash matches', wrapper['members'][0]['sha256'] == README_PIN)
    docs = {key: fitz.open(paths[key]) for key in ('uaf', 'uaf_other', 'nist')}
    attachments = {key: docs[key].embfile_count() for key in ('uaf', 'uaf_other')}
    layers = {}
    for key in ('uaf', 'uaf_other'):
        page = docs[key][98]
        images = [i for i in page.get_images(full=True) if (i[2], i[3]) == (749, 582)]
        check(key + ' Figure 3.14 raster located', len(images) == 1)
        check(key + ' vector W21 label retained', 'W21x44;  G3005 w/o bracing' in page.get_text())
        check(key + ' W21 caption retained', 'Figure 3.14 UAF analysis of the W21x44 G3005' in page.get_text())
        layers[key] = {'figure': '3.14', 'physical_page': 99, 'printed_page': 86,
                       'embedded_raster_sha256': digest(docs[key].xref_stream(images[0][0])),
                       'underlying_label_manual_transcription': 'W24x55; G3005 w/o bracing',
                       'rendered_label': 'W21x44;  G3005 w/o bracing',
                       'actual_native_section': None}
    check('Figure 3.14 raster matches across final PDFs', layers['uaf']['embedded_raster_sha256'] == layers['uaf_other']['embedded_raster_sha256'])
    uaf_claim = ' '.join(docs['uaf'][96].get_text().split())
    check('UAF section criticism source-pinned', 'results for G3005 based on a W24x55, not a W21x44' in uaf_claim)
    check('UAF separates four adjacent W24 beams', 'W24x55 for the four adjacent beams' in uaf_claim)
    nist_figure = docs['nist'][393].get_text()
    check('NIST Figure 8-22 labels its floor beams W24x55', 'W24x55 Floor Beams' in nist_figure)
    check('NIST Figure 8-22 labels separate girder W33x130', 'W33x130 Girder' in nist_figure)
    syntax_command = ['rg', '-l', '-i', '-uuu', '--max-filesize', '4M', '-g', '*.inp', '-g', '*.txt', '-g', '*.dat', '-g', '*.py', '-g', '*.s2k',
                      '-e', r'^\*(?:NODE|ELEMENT|BEAM SECTION|SHELL SECTION|SOLID SECTION)(?:\s*,|\s*$)', 'research', 'investigation']
    syntax = subprocess.run(syntax_command, cwd=args.public_repo, capture_output=True, text=True)
    if syntax.returncode not in (0, 1):
        raise RuntimeError('Syntax scan failed: ' + syntax.stderr)
    renders = []
    if args.review_dir:
        args.review_dir.mkdir(parents=True, exist_ok=False)
        for key, number in [('uaf', 97), ('uaf', 99), ('nist', 394), ('nist', 398)]:
            pix = docs[key][number - 1].get_pixmap(dpi=130, colorspace=fitz.csRGB, alpha=False)
            target = args.review_dir / f'{key}-physical-{number}.png'
            with target.open('xb') as stream:
                stream.write(pix.tobytes('png'))
            renders.append({'source': key, 'physical_page': number, 'file': target.name, 'sha256': file_hash(target), 'dpi': 130})
    after = {key: file_hash(p) for key, p in paths.items()}
    check('all preserved inputs unchanged', before == after)
    result = {
        'generated_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_hashes_before': before, 'source_hashes_after': after,
        'public_tracked_tree': tracked, 'physical_inventories': roots,
        'wrapper': wrapper, 'UAF_PDF_embedded_file_counts': attachments,
        'UAF_Figure_3_14': layers,
        'native_syntax_scan': {'command': syntax_command, 'exit_code': syntax.returncode,
                               'stderr': syntax.stderr, 'candidate_files': syntax.stdout.splitlines()},
        'review_renders': renders, 'checks_passed': len(checks), 'checks': checks,
        'actual_UAF_G3005_section': None, 'actual_NIST_G3005_section': None,
        'native_model_executed': False,
        'limits': ['Scoped paths, ZIP directory and small plaintext syntax only; no whole-disk or historical archive absence claim.',
                   'Raster text and output-database filenames are manually inspected figure locators, not native assignments.',
                   'No aggregate download, native ODB read, solver run or cause/intent finding.'],
    }
    with args.out.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'checks_passed': len(checks), 'root_summaries': {k: {'available': v['available'], 'path_count': v['path_count'], 'native': v.get('native_suffix_candidates'), 'archives': v.get('archive_candidates'), 'errors': v['errors']} for k, v in roots.items()}, 'syntax_hits': result['native_syntax_scan']['candidate_files'], 'attachments': attachments}, indent=2))


if __name__ == '__main__':
    main()
