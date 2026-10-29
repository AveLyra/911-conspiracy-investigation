"""Inspect a preserved public catalog entity; no network or media acquisition."""
import argparse
import collections
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--metadata', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
pins = json.loads((root / 'SOURCES.json').read_text())
raw = args.metadata.read_bytes()
assert len(raw) == pins['archive_metadata']['bytes']
assert hashlib.sha256(raw).hexdigest() == pins['archive_metadata']['sha256']
data = json.loads(raw)
files = data['files']
result = {
    'file_records': len(files),
    'format_counts': dict(collections.Counter(f.get('format', 'unspecified') for f in files)),
    'source_counts': dict(collections.Counter(f.get('source', 'unspecified') for f in files)),
    'original_format_counts': dict(collections.Counter(f.get('format', 'unspecified') for f in files if f.get('source') == 'original')),
    'searched_filename_extensions': ['.wav', '.mdb', '.accdb', '.arc', '.iso', '.zip', '.7z'],
    'matches_for_searched_extensions': [f['name'] for f in files if f.get('name', '').lower().endswith(('.wav', '.mdb', '.accdb', '.arc', '.iso', '.zip', '.7z'))],
    'selected_entry': [{k: f.get(k) for k in ['name', 'format', 'source', 'size', 'sha1', 'md5', 'private']} for f in files if f.get('name') == 'DRM1_DAT2_Channel_2_MCC_Op.mp3'],
}
assert result == json.loads((root / 'CATALOG-RESULTS.json').read_text())
held = pins['held_file_check']
selected = result['selected_entry'][0]
assert held['bytes'] == int(selected['size']) and held['sha1'] == selected['sha1']
assert held['sha256'] == held['preceding_sha256_pin']
print(json.dumps({'catalog_identity_and_accounting': 'passed', 'result': result,
                  'held_check': 'Saved executed fingerprint comparison matches this catalog entry; media is not reread here.',
                  'limits': 'No archive media body, native master, custody, clock, waveform or historical-event authentication.'}, indent=2))
