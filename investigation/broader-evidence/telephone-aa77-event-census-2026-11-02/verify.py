"""Reproduce supplied readings and optional original-image/native-input checks."""
import argparse
import hashlib
import json
from pathlib import Path
from compare_events import analyze

HERE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--capture-dir',type=Path)
    p.add_argument('--transcriptions',type=Path)
    args=p.parse_args()
    for x in json.loads((HERE/'BUNDLE-HASHES.json').read_text())['files']:
        data=(HERE/x['name']).read_bytes()
        assert len(data)==x['bytes'] and hashlib.sha256(data).hexdigest()==x['sha256'],x['name']
    rows=json.loads((HERE/'OBSERVATIONS.json').read_text())['records']
    expected=json.loads((HERE/'RESULT.json').read_text())
    # Normalize numeric JSON dictionary keys before comparing saved outputs.
    assert json.loads(json.dumps(analyze(rows)))==expected
    original_hashes=0
    if args.capture_dir:
        for x in json.loads((HERE/'SOURCES.json').read_text())['images']:
            raw=(args.capture_dir/x['filename']).read_bytes()
            assert len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['sha256']
            original_hashes+=1
    native=False
    input_sha=None
    if args.transcriptions:
        raw=args.transcriptions.read_bytes();d=json.loads(raw)
        assert json.loads(json.dumps(analyze(d['records'])))==expected
        input_sha=hashlib.sha256(raw).hexdigest()
        native=True
    print(json.dumps(dict(bundle_hashes_match=True,derived_public_readings_reproduce=True,
          original_image_hashes_checked=original_hashes,
          raw_CSC_transcription_comparison=native,
          supplied_transcription_sha256=input_sha,
          record_count=expected['record_count'],accepted_CSC_groups=expected['accepted_csc_groups'],
          unaccepted_CSC_records=expected['unaccepted_csc_records'],
          equality_negative_controls=expected['controls'],
          scope='Arithmetic/equality on supplied manual readings and optional source-byte integrity; no independent image transcription, native carrier release, clock calibration, schema authority, caller/recipient/voice/conversation or historical causal authentication.'),indent=2))

if __name__=='__main__':main()
