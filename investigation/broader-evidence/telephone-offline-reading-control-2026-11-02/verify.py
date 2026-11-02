"""Payload preservation and synthetic-input checks; control outcome stays FAILED."""
import ast
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import wave


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'BUNDLE-HASHES.json').read_text())
    for item in manifest['files']:
        data = (root / item['name']).read_bytes()
        assert len(data) == item['bytes']
        assert hashlib.sha256(data).hexdigest() == item['sha256']
    control = json.loads((root / 'CONTROL-RESULT.json').read_text())
    assert control['control_result'] == 'FAILED'
    assert control['court_speech_inputs_processed'] == 0 and control['court_speech_readings'] is None
    assert control['inference']['exit_code'] == 0
    assert control['observed_selected_machine_output'] == 'You'
    assert control['machine_text_sha256'] == hashlib.sha256(b'You\n').hexdigest()
    for name in ('reproduce_control.py', 'verify.py'):
        ast.parse((root / name).read_text())
    spec = importlib.util.spec_from_file_location('control_reproducer', root / 'reproduce_control.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    wav = module.make_wav_bytes()
    assert hashlib.sha256(wav).hexdigest() == control['synthetic_input']['wav_sha256']
    with wave.open(io.BytesIO(wav), 'rb') as f:
        assert (f.getnchannels(), f.getsampwidth(), f.getframerate(), f.getnframes()) == (1, 2, 16000, 160000)
        pcm = f.readframes(f.getnframes())
    assert len(pcm) == 320000 and not any(pcm)
    assert hashlib.sha256(pcm).hexdigest() == control['synthetic_input']['pcm_sha256']
    command = module.engine_arguments('ENGINE', 'MODEL', 'ZERO_WAV', 'OUTPUT_PREFIX')
    assert command == control['executed_argument_template']
    print(json.dumps({'preservation_and_reproducer_structure_checks': 'passed',
                      'body_files_checked': len(manifest['files']), 'synthetic_generator_matches_actual_input': True,
                      'original_speech_control_result': 'FAILED', 'actual_court_speech_runs': 0,
                      'standalone_reproducer_inference_rerun': False,
                      'scope': 'File hashes, syntax, exact command options and synthetic WAV generation only. Does not change the failed control or establish historical speech accuracy.'}, indent=2))


if __name__ == '__main__':
    main()
