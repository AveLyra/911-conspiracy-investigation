#!/usr/bin/env python3
"""Generate one local synthetic speech fixture; never print the ground truth."""
from __future__ import annotations

import array
import hashlib
import json
import os
from pathlib import Path
import platform
import secrets
import shutil
import subprocess
import sys
from datetime import datetime, timezone
import wave

UNIT = Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/audio-listening-2026-10-05')
EXPECTED_PROTOCOL = 'c0d6f9aafd8295cfef9e2f865a174c2afbd1335e398fca333a638d7c7782b4af'
FIXTURE = UNIT / 'fixture'
SEALED = FIXTURE / 'sealed'
SAY = '/usr/bin/say'
FFMPEG = '/opt/homebrew/bin/ffmpeg'
FFPROBE = '/opt/homebrew/bin/ffprobe'
WORD_BANK = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def new_json(path: Path, obj: object) -> None:
    with path.open('x', encoding='utf-8') as handle:
        json.dump(obj, handle, indent=2)
        handle.write('\n')


def main() -> int:
    if digest(UNIT / 'PROTOCOL.md') != EXPECTED_PROTOCOL:
        raise RuntimeError('Protocol hash mismatch; fixture not generated.')
    if FIXTURE.exists():
        raise RuntimeError('Fixture destination already exists; refuse overwrite.')
    FIXTURE.mkdir(mode=0o700)
    SEALED.mkdir(mode=0o700)
    shutil.copyfile(Path(__file__), SEALED / 'generate_fixture.py')
    receipt = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'classification': 'SYNTHETIC capability fixture; not historical or case evidence',
        'seal': 'Procedural withholding from root until frozen response; not encryption.',
        'protocol_sha256': EXPECTED_PROTOCOL,
        'generator_sha256': digest(SEALED / 'generate_fixture.py'),
        'python': sys.version,
        'platform': platform.platform(),
        'randomization': 'six independent secrets.choice selections with replacement; OS entropy; no resampling',
        'voice': 'Samantha',
        'speech_rate_words_per_minute': 125,
        'commands': [],
        'attempt': 1,
        'heard_by_generator': False,
        'historical_inputs': [],
        'loudspeaker_playback': False,
    }

    def run(arguments: list[str], name: str, *, required: bool = True) -> subprocess.CompletedProcess:
        result = subprocess.run(arguments, capture_output=True, timeout=60, check=False)
        (SEALED / (name + '.stdout')).write_bytes(result.stdout)
        (SEALED / (name + '.stderr')).write_bytes(result.stderr)
        receipt['commands'].append({'argv': arguments, 'returncode': result.returncode,
                                    'stdout': name + '.stdout', 'stderr': name + '.stderr'})
        if required and result.returncode != 0:
            raise RuntimeError(name + ' failed; see preserved sealed log.')
        return result

    status = 1
    try:
        words = [secrets.choice(WORD_BANK) for _ in range(6)]
        transcript = SEALED / 'transcript.txt'
        with transcript.open('x', encoding='utf-8') as handle:
            handle.write(', '.join(words) + '.\n')
        new_json(SEALED / 'ground-truth.json', {'words': words, 'word_count': 6,
                                             'transcript_sha256': digest(transcript)})
        run(['/usr/bin/sw_vers'], 'macos-version')
        run([FFMPEG, '-version'], 'ffmpeg-version')
        run([FFPROBE, '-version'], 'ffprobe-version')
        run(['/usr/bin/codesign', '-dvv', SAY], 'say-signature')
        receipt['say_binary_sha256'] = digest(Path(SAY))
        source = SEALED / 'synthesis.aiff'
        wav = FIXTURE / 'synthetic-capability.wav'
        run([SAY, '-v', 'Samantha', '-r', '125', '-f', str(transcript), '-o', str(source)], 'synthesis')
        receipt['synthesis_success'] = True
        receipt['synthesis_aiff_sha256'] = digest(source)
        run([FFMPEG, '-nostdin', '-hide_banner', '-loglevel', 'error', '-n', '-i', str(source),
             '-map_metadata', '-1', '-ac', '1', '-ar', '8000', '-c:a', 'pcm_s16le', str(wav)], 'convert')
        probe_result = run([FFPROBE, '-v', 'error', '-show_entries',
                            'format=format_name,duration,size:stream=codec_name,sample_rate,channels,bits_per_sample',
                            '-of', 'json', str(wav)], 'probe')
        receipt['probe'] = json.loads(probe_result.stdout)
        run([FFMPEG, '-nostdin', '-hide_banner', '-loglevel', 'error', '-i', str(wav),
             '-f', 'null', '-'], 'full-decode')
        with wave.open(str(wav), 'rb') as stream:
            frames = stream.getnframes()
            rate = stream.getframerate()
            channels = stream.getnchannels()
            width = stream.getsampwidth()
            compression = stream.getcomptype()
            pcm = stream.readframes(frames)
        assert (rate, channels, width, compression) == (8000, 1, 2, 'NONE')
        assert frames > 0 and len(pcm) == frames * 2
        samples = array.array('h', pcm)
        assert any(samples), 'All-zero PCM does not satisfy nonempty synthetic speech fixture.'
        receipt['format_check'] = {'frames': frames, 'rate': rate, 'channels': channels,
                                   'sample_width_bytes': width, 'compression': compression,
                                   'full_pcm_byte_length': len(pcm), 'nonzero_pcm': True}
        receipt['decode_success'] = True
        receipt['verification_limit'] = 'Format/decode/nonempty verification only; no intelligibility or listening claim.'
        public = {'path': str(wav), 'sha256': digest(wav), 'bytes': wav.stat().st_size,
                  'format': 'WAV pcm_s16le', 'sample_rate_hz': rate, 'channels': channels,
                  'duration_seconds': frames / rate, 'synthesis_success': True, 'decode_success': True}
        new_json(FIXTURE / 'public-receipt.json', public)
        receipt['output'] = public
        receipt['status'] = 'format-valid synthetic fixture generated'
        print(json.dumps(public, sort_keys=True))
        status = 0
    except BaseException as exc:
        receipt['status'] = 'failed; no success claim'
        receipt['error'] = type(exc).__name__ + ': ' + str(exc)
        print('Fixture attempt failed; sealed receipt preserves the failure. Ground truth remains withheld.')
    finally:
        new_json(SEALED / 'generation-receipt.json', receipt)
        hashes = {str(path.relative_to(FIXTURE)): digest(path)
                  for path in sorted(FIXTURE.rglob('*')) if path.is_file()}
        new_json(SEALED / 'file-hashes.json', hashes)
    return status


if __name__ == '__main__':
    raise SystemExit(main())
