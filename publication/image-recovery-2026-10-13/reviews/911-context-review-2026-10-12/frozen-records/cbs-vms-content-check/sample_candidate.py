"""Bounded scene-screen derivatives; never an event-clock or cause measurement."""
from pathlib import Path
import bisect
import hashlib
import json
import re
import sys
from PIL import Image
import inspect_candidate as m

SOURCE_SHA = 'bae07b52bc85c735c72b227b55a327da3a49c6bf6a0798ccc9d85602dae185ad'
CONTROL_SHA = '03faf8b842dbec9ea7358b91f3cb0097a40a1b0719696b698025a4b79599b8c6'
WARNING = re.compile(rb'\[swscaler @ 0x[0-9a-f]+\] \[swscaler @ 0x[0-9a-f]+\] No accelerated colorspace conversion found from yuv420p to rgb24\.')


def check_diagnostics(stderr, status, allow_fallback):
    m.prior.require(status['returncode'] == 0, 'nonzero/launch failure')
    lines = stderr.splitlines()
    m.prior.require(not stderr or (allow_fallback and lines and
                    all(WARNING.fullmatch(line) for line in lines)), 'unreviewed diagnostic')


def extract(source, digest, indices, size, out, allow_fallback, expected_md5=None, colors=None):
    m.prior.require(indices and all(type(i) is int and i >= 0 for i in indices)
                    and all(a < b for a, b in zip(indices, indices[1:])), 'invalid indices')
    m.prior.require(m.prior.sha(source) == digest, 'wrong source bytes')
    out.mkdir()
    native = out / 'native'; native.mkdir()
    command = [m.prior.FFMPEG, '-nostdin', '-hide_banner', '-nostats', '-v', 'warning',
               '-n', '-copyts', '-noautorotate', '-guess_layout_max', '0', '-i', str(source),
               '-map', '0:v:0', '-an', '-sn', '-dn', '-map_metadata', '-1', '-map_chapters', '-1',
               '-vf', "select='" + '+'.join(f'eq(n,{i})' for i in indices) + "'",
               '-noautoscale', '-pix_fmt', 'rgb24', '-fps_mode', 'passthrough',
               '-enc_time_base:v', 'demux', str(native/'frame-%06d.png')]
    stdout, stderr, status = m.prior.run_command(command, out, 'decode')
    check_diagnostics(stderr, status, allow_fallback)
    m.prior.require(not stdout, 'unexpected stdout')
    files = sorted(native.glob('*.png'))
    m.prior.require(len(files) == len(indices), 'image count mismatch')
    rows = []
    for order, (i, file) in enumerate(zip(indices, files), 1):
        m.prior.require(file.name == f'frame-{order:06d}.png', 'wrong output order')
        with Image.open(file) as im:
            im.load()
            m.prior.require(im.size == size and im.mode == 'RGB', 'geometry/mode mismatch')
            pixels = im.tobytes()
        md5 = hashlib.md5(pixels).hexdigest()
        if expected_md5 is not None:
            m.prior.require(md5 == expected_md5[i], 'full-stream pixel mismatch')
        if colors is not None:
            m.prior.require(pixels == bytes(colors[order-1]) * (size[0]*size[1]), 'synthetic pixel mismatch')
        rows.append({'order': order, 'source_index': i, 'path': str(file.relative_to(out)),
                     'rgb_md5': md5, 'rgb_sha256': hashlib.sha256(pixels).hexdigest(),
                     'png_sha256': m.prior.sha(file)})
    m.prior.require(m.prior.sha(source) == digest, 'source changed')
    m.prior.save(out/'frames.json', rows)
    m.prior.save(out/'receipt.json', {'script_sha256': m.prior.sha(Path(__file__)),
        'source_sha256': digest, 'diagnostic_lines': len(stderr.splitlines()),
        'status': 'descriptive_derivatives_only', 'scientific_or_human_acceptance': False})
    return rows


def controls():
    for stderr, status, allow in [(b'unknown\n', {'returncode': 0}, True),
                                  (b'', {'returncode': 7}, True),
                                  (b'[swscaler @ 0x1] [swscaler @ 0x2] No accelerated colorspace conversion found from yuv420p to rgb24.\n', {'returncode': 0}, False)]:
        try: check_diagnostics(stderr, status, allow)
        except m.prior.Refusal: pass
        else: raise RuntimeError('diagnostic negative control failed')
    control = m.BASE.parent/'late-fire-catalog-join/control01/synthetic.avi'
    rows = extract(control, CONTROL_SHA, [0,60,120,124], (96,64), m.BASE/'control01', False,
                   colors=[(255,0,0),(0,255,0),(0,0,255),(0,0,255)])
    print('PASS: three diagnostic negatives and four known-color synthetic images')


def sample(name, plan_sha):
    m.prior.require(name in ['run01','run02'], 'bounded destination required')
    m.prior.require(m.prior.sha(m.BASE/'FRAME-PLAN.md') == plan_sha, 'plan changed')
    f = json.loads((m.BASE/'diagnostics/probe.stdout').read_bytes())['frames']
    pts = [x['pts'] for x in f]
    m.prior.require(len(f) == 4531 and all(type(x) is int for x in pts)
                    and all(a < b for a,b in zip(pts,pts[1:])), 'inventory mismatch')
    indices = sorted(set([0,len(f)-1] + [bisect.bisect_left(pts,t) for t in range(pts[0],pts[-1]+1,4000)]))
    m.prior.require(len(indices) == 77, 'selection count mismatch')
    checks = [x.split(',') for x in (m.BASE/'diagnostics/decode01.stdout').read_text().splitlines()
              if x and not x.startswith('#')]
    m.prior.require(len(checks) == len(f) and [int(x[2]) for x in checks] == pts, 'checksum timeline mismatch')
    md5 = [x[5].strip() for x in checks]
    rows = extract(m.BASE/'sources/CBS-VMS-Wtc7.wmv', SOURCE_SHA, indices, (320,240),
                   m.BASE/name, True, expected_md5=md5)
    locators = [{'order': r['order'], 'source_index': r['source_index'],
                 'pts': pts[r['source_index']], 'time_base': '1/1000'} for r in rows]
    m.prior.save(m.BASE/name/'locators.json', locators)
    m.prior.save(m.BASE/name/'plan-pin.json', {'sha256': plan_sha})
    print('PASS:',name,len(rows),'native-size images match full RGB stream pixels')


if __name__ == '__main__':
    if sys.argv[1:] == ['controls']: controls()
    else: sample(sys.argv[1],sys.argv[2])
