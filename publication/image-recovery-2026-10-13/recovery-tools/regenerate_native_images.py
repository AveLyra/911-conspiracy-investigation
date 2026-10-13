"""Rebuild only missing native PNGs; verify against preserved pre-deletion hashes."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import threading
from PIL import Image, __version__ as pillow_version
import recover_images as recovery

TASK = Path(__file__).resolve().parent
PREFIX = 'research/sherlock-wtc7-investigation/'
COMMIT = recovery.INDEX['source_commit']
RECEIPTS = recovery.VAULT / 'regeneration-receipts'
RECEIPTS.mkdir(parents=True, exist_ok=True)

def archived(path, parse=True):
    data = subprocess.check_output(['git', '-C', recovery.PRIVATE, 'show', COMMIT+':'+PREFIX+path])
    return json.loads(data) if parse else data

def source_path(source):
    p = recovery.lfs_path(source['sha256'])
    if p is None or p.stat().st_size != source['bytes'] or recovery.digest_file(p) != source['sha256']:
        raise RuntimeError('Preserved source video is missing or fails its saved identity')
    return p

def save_receipt(name, value):
    with (RECEIPTS / (name+'.json')).open('x') as f:
        json.dump(value, f, indent=2)

def create_checked(data, expected, size):
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected or len(data) != size:
        raise RuntimeError('Regenerated PNG differs from saved original hash or size')
    return recovery.store(data=data, expected=expected)

def distant():
    old = archived('distant-view-source-screen/views01/receipt.json')
    rows = archived('distant-view-source-screen/continuity-274-411/run01/frames.json')
    src = source_path(old['media'])
    command = old['execution']['argv'][:]
    command[command.index('-i')+1] = str(src)
    if recovery.digest_file(command[0]) != old['binary']['sha256']:
        raise RuntimeError('DistantView decoder binary differs from saved binary')
    process = subprocess.run(command, capture_output=True, timeout=120)
    raw = process.stdout
    digest = hashlib.sha256(raw).hexdigest()
    if process.returncode or process.stderr or len(raw) != old['execution']['raw_bytes'] or digest != old['execution']['raw_sha256']:
        save_receipt('distant-view-refused', {'argv': command, 'returncode': process.returncode,
                     'stderr': process.stderr.decode(errors='replace'), 'raw_sha256': digest, 'raw_bytes': len(raw)})
        raise RuntimeError('DistantView complete decoded stream differs from saved stream')
    made = []
    for row in rows:
        native = row['native']
        width, height = native['size']
        frame_bytes = width * height * 3 // 2
        offset = row['index'] * frame_bytes
        pixels = raw[offset:offset+width*height]
        if hashlib.sha256(pixels).hexdigest() != native['pixel_sha256']:
            raise RuntimeError('DistantView luminance pixels differ from saved hash')
        output = io.BytesIO()
        Image.frombytes(native['mode'], (width, height), pixels).save(output, format='PNG')
        create_checked(output.getvalue(), native['sha256'], native['bytes'])
        made.append({'index': row['index'], 'png_sha256': native['sha256'], 'original_hash_match': True})
    save_receipt('distant-view', {'source': old['media'], 'argv': command, 'decoder_sha256': old['binary']['sha256'],
                  'pillow': pillow_version, 'raw_bytes': len(raw), 'raw_sha256': digest, 'stderr_bytes': 0,
                  'decoded_stream_matches_saved_original': True, 'frames': made,
                  'scope': 'Restore original native luminance PNGs only; no new annotations, motion fits or physical conclusions.'})
    print('DistantView: all 138 native originals regenerated and hash-verified', flush=True)

def exact_read(stream, n):
    blocks = []
    left = n
    while left:
        block = stream.read(left)
        if not block:
            raise RuntimeError('Truncated PNG stream')
        blocks.append(block); left -= len(block)
    return b''.join(blocks)

def read_png(stream):
    signature = stream.read(8)
    if not signature:
        return None
    if signature != b'\x89PNG\r\n\x1a\n':
        raise RuntimeError('Unexpected image stream signature')
    pieces = [signature]
    while True:
        length = exact_read(stream, 4)
        size = int.from_bytes(length, 'big')
        if size > 8_000_000:
            raise RuntimeError('PNG chunk exceeds bounded native image size')
        kind = exact_read(stream, 4)
        payload = exact_read(stream, size+4)
        pieces.extend([length, kind, payload])
        if kind == b'IEND':
            return b''.join(pieces)

def cbs(clip, manifest_path, run_path):
    manifest = archived(manifest_path)
    source = next(s for s in manifest['sources'] if s['id'] == 'vince-clip'+str(clip))
    src = source_path(source)
    original = archived(run_path+'/decode.command.json')
    rows = archived(run_path+'/frames.json')
    command = original[:-1]
    command[command.index('-i')+1] = str(src)
    # Preserve native decoder/filter/encoder options. Only change the output
    # container to a PNG pipe so no additional staging copy occupies the disk.
    command += ['-c:v', 'png', '-f', 'image2pipe', 'pipe:1']
    made = []
    stderr_path = RECEIPTS / ('cbs-clip'+str(clip)+'.stderr.txt')
    with stderr_path.open('xb') as err:
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=err)
        timer = threading.Timer(180, process.terminate)
        timer.start()
        try:
            for row in rows:
                data = read_png(process.stdout)
                if data is None:
                    raise RuntimeError('Too few source frames emitted')
                expected = row['png_sha256']
                with Image.open(io.BytesIO(data)) as im:
                    im.load()
                    if im.mode != 'RGB' or im.size != (row['width'], row['height']) or hashlib.sha256(im.tobytes()).hexdigest() != row['rgb_sha256']:
                        raise RuntimeError('Regenerated pixels differ from original')
                # A saved PNG hash is stronger than a same-size resemblance.
                if hashlib.sha256(data).hexdigest() != expected:
                    raise RuntimeError('PNG pipe encoding differs from original PNG')
                recovery.store(data=data, expected=expected)
                made.append({'source_index': row['source_index'], 'png_sha256': expected,
                             'rgb_sha256': row['rgb_sha256'], 'original_hash_match': True})
            if read_png(process.stdout) is not None:
                raise RuntimeError('Too many source frames emitted')
            status = process.wait(timeout=30)
            if status:
                raise RuntimeError('CBS decoder returned nonzero')
        finally:
            timer.cancel()
            process.stdout.close()
            if process.poll() is None:
                process.terminate(); process.wait(timeout=30)
    if len(made) != len(source['indices']) or [r['source_index'] for r in rows] != source['indices']:
        raise RuntimeError('Saved frame roster differs from original manifest')
    save_receipt('cbs-clip'+str(clip), {'source': {k:v for k,v in source.items() if k!='indices'},
                  'source_pin_matches': recovery.digest_file(src) == source['sha256'], 'original_argv': original,
                  'recovery_argv': command, 'decoder_sha256': recovery.digest_file(command[0]),
                  'pillow': pillow_version, 'returncode': status, 'stderr_path': str(stderr_path),
                  'stderr_sha256': recovery.digest_file(stderr_path), 'frames': made,
                  'scope': 'Native PNG restoration; original frame selection and PNG/RGB hashes. No scoring or new scientific acceptance.'})
    print('CBS Clip '+str(clip)+': '+str(len(made))+' original frames regenerated and hash-verified', flush=True)

def failed_clip3_equivalents():
    # The earlier refused run retained PNGs but did not write frames.json.
    # Its recorded command is identical apart from input/output locations.
    # Preserve that distinction: equivalence does not supply a missing original hash.
    earlier = archived('cbs-frame-correspondence/dense-clip3/extract01/vince-clip3/decode.command.json')
    later = archived('cbs-frame-correspondence/dense-clip3/v2/extract01/vince-clip3/decode.command.json')
    if earlier[:-1] != later[:-1]:
        raise RuntimeError('Earlier refused extraction has different decoder options')
    rows = archived('cbs-frame-correspondence/dense-clip3/v2/extract01/vince-clip3/frames.json')
    records = {r['source_path']: r for r in recovery.INDEX['images']}
    manifest_path = recovery.VAULT / 'recovery-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    restored = {r['source_path']: r for r in manifest['restored']}
    equivalents = []
    for row in rows:
        path = PREFIX+'cbs-frame-correspondence/dense-clip3/extract01/vince-clip3/'+row['file']
        obj = recovery.OBJECTS / row['png_sha256'][:2] / row['png_sha256']
        if not obj.exists() or recovery.digest_file(obj) != row['png_sha256']:
            raise RuntimeError('Accepted repeat frame is missing')
        restored[path] = recovery.bind(records[path], obj, 'equivalent_extraction_original_hash_unavailable',
                                       COMMIT+':'+PREFIX+'cbs-frame-correspondence/dense-clip3/v2/extract01/vince-clip3/frames.json')
        restored[path]['qualification'] = 'Same saved source/decoder options and pre-deletion size; original refused-run PNG hash unavailable. Original refusal remains unchanged.'
        equivalents.append({'path': path, 'reconstruction_sha256': obj.name, 'original_hash_verified': False})
    manifest['restored'] = list(restored.values())
    manifest['unresolved'] = [r for r in manifest['unresolved'] if r['source_path'] not in restored]
    with manifest_path.open('w') as f:
        json.dump(manifest, f, indent=2)
    save_receipt('earlier-refused-clip3-equivalents', {'original_argv': earlier, 'later_argv': later,
                 'commands_identical_except_destination': True, 'images': equivalents,
                 'qualification': '189 reconstructions are not independently original-hash verified; no change to the refused historical run.'})
    print('Earlier Clip 3 run: 189 equivalent reconstructions, separately labeled without original hashes', flush=True)

def main():
    if not (RECEIPTS / 'distant-view.json').exists():
        distant()
    for clip, mp, rp in [
        (3, 'cbs-frame-correspondence/dense-clip3/v2/manifest.json', 'cbs-frame-correspondence/dense-clip3/v2/extract01/vince-clip3'),
        (7, 'cbs-frame-correspondence/dense-clip7/manifest.json', 'cbs-frame-correspondence/dense-clip7/extract01/vince-clip7')]:
        if not (RECEIPTS / ('cbs-clip'+str(clip)+'.json')).exists():
            cbs(clip, mp, rp)
    for clip in [1, 2, 4, 5, 6, 8]:
        stage = (clip+1)//2
        if not (RECEIPTS / ('cbs-clip'+str(clip)+'.json')).exists():
            cbs(clip, f'cbs-vince-source-screen/stage{stage}/preparation01/sampling-manifest.json',
                f'cbs-vince-source-screen/stage{stage}/run01/vince-clip{clip}')
    recovery.main()
    if not (RECEIPTS / 'earlier-refused-clip3-equivalents.json').exists():
        failed_clip3_equivalents()
    recovery.main()

if __name__ == '__main__':
    main()
