"""Control-only reproduction. Requires matching existing macOS engine and weights.

python3 reproduce_control.py --engine /path/to/whisper-cli --model /path/to/base.en.bin --out /new/output/directory

No court/source audio, downloads, installations, prompts, tuning or upload.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import wave

ENGINE_SHA = '40bca494d49af736058eb3f33cbcebaa020eacf6d0087b623f334946e1ab2128'
MODEL_SHA = 'a03779c86df3323075f5e796cb2ce5029f00ec8869eee3fdfb897afe36c6d002'
PROFILE = '(version 1)(allow default)(deny network*)'


def make_wav_bytes():
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(16000)
        out.writeframes(b'\0' * 320000)
    return buf.getvalue()


def engine_arguments(engine, model, wav, prefix):
    return [str(engine), '-ng', '-m', str(model), '-f', str(wav), '-l', 'en',
            '-t', '4', '-p', '1', '-tp', '0', '-nf', '-ojf', '-otxt', '-osrt',
            '-of', str(prefix)]


def file_hash(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if sys.platform != 'darwin':
        raise SystemExit('This exact network-denied reproduction requires macOS; no fallback.')
    assert file_hash(args.engine) == ENGINE_SHA, 'Different engine; stop rather than silently change the tested configuration.'
    assert file_hash(args.model) == MODEL_SHA, 'Different model; no download or substitution.'
    assert not args.out.exists(), 'Refusing to replace prior outputs.'
    probe_code = 'import socket,json,errno\ns=socket.socket();s.settimeout(1);n=s.connect_ex(("127.0.0.1",9));print(json.dumps({"errno":n,"denied":n in (errno.EPERM,errno.EACCES)}))'
    probe = subprocess.run(['/usr/bin/sandbox-exec', '-p', PROFILE, sys.executable, '-c', probe_code],
                           capture_output=True, text=True, timeout=15)
    assert probe.returncode == 0 and json.loads(probe.stdout)['denied'], 'Network-denial probe failed; stop.'
    args.out.mkdir(parents=True, exist_ok=False)
    wav = args.out / 'silence-10s.wav'
    data = make_wav_bytes()
    assert hashlib.sha256(data).hexdigest() == 'ee7bea4232762775f8fce9b3e27e4d3948c8ac6a45a87ca769f703d6eed0b448'
    with wav.open('xb') as f:
        f.write(data)
    command = ['/usr/bin/sandbox-exec', '-p', PROFILE, *engine_arguments(args.engine, args.model, wav, args.out / 'reading')]
    with (args.out / 'stdout.log').open('xb') as out, (args.out / 'stderr.log').open('xb') as err:
        result = subprocess.run(command, stdout=out, stderr=err, timeout=300)
    assert result.returncode == 0, 'Inference failed; preserve files and do not retry.'
    text_file = args.out / 'reading.txt'
    text = text_file.read_text()
    record = {'inference_exit_code': result.returncode, 'input_wav_sha256': file_hash(wav),
              'output_text_sha256': file_hash(text_file), 'output_text_stripped_characters': len(text.strip()),
              'control_result': 'PASSED' if not text.strip() else 'FAILED',
              'speech_inputs_processed': 0,
              'limit': 'Synthetic method test only; no source recording, voice, historical clock or speech accuracy established.'}
    with (args.out / 'result.json').open('x') as f:
        json.dump(record, f, indent=2)
        f.write('\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
