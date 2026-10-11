#!/usr/bin/env python3
"""Deterministic synthetic-only packet derivative. No media decoding or serving."""
import argparse
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
LOCAL = HERE.parent
R1 = LOCAL.parent.parent / 'comparator-r1-replication'
PROTOCOL_SHA = 'c1b27cc20a7ed57498f9398743cd9bf46491030071b9ad4bbb9c58d9b5b39e9c'
ORIGINAL_SHA = '1c6b76f665ae63f43a722139317ba5890a9f1c7e25511f094a6f6fa4184e4bb6'
HANDLER_SHA = '1ea233c4fa8074298f9791a305fa46f0b1ac3151ce00ce48c8edd7e99de48142'
CONTROL_SHA = 'f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48'
ORIGINALS = {
    'review.html': 'f32657ca617bb3c4b815aada46b26a9d1b33c1223644d59fdf9139e24afabe74',
    'review.mjs': '318904031cde1047be376679e4ed6649836c8ab3caad6f773c4ae763e91cdca6',
    'response.mjs': '2e9f0c1acf98d2b63b9db6d20824b3e152cc55fedab84dabe789477bc53499d8',
    'coordinate-core.mjs': '9cff4290fc41e27126b36402818b1ecb55057e003f819ecbe8cef53281d2e2c4',
    'assets.mjs': '0b26c9e5c169c4910b2259de3eda38b6106dc0abb745aa73ff1cad44821e2915'}
CODE = {'/': 'review.html', '/review.mjs': 'review.mjs', '/response.mjs': 'response.mjs',
        '/coordinate-core.mjs': 'coordinate-core.mjs', '/assets.mjs': 'assets.mjs',
        '/diagnostics.mjs': 'diagnostics.mjs'}
ROUTES = set(CODE) | {'/control.png'}
TAG = b'  <script type="module" src="./diagnostics.mjs"></script>\n'


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path, expected=None):
    path = Path(path)
    require(not any(p.is_symlink() for p in [path, *path.parents]), 'symlink refused')
    require(path.is_file(), 'regular file required: ' + str(path))
    data = path.read_bytes()
    if expected is not None:
        require(identity(data) == expected if isinstance(expected, dict) else
                identity(data)['sha256'] == expected, 'input pin mismatch: ' + str(path))
    return data


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def inject(html):
    require(html.count(b'</body>') == 1 and b'diagnostics.mjs' not in html,
            'unexpected original HTML')
    return html.replace(b'</body>', TAG + b'</body>')


def expected_packet(local=LOCAL, here=HERE, r1=R1, originals=ORIGINALS,
                    original_sha=ORIGINAL_SHA, protocol_sha=PROTOCOL_SHA,
                    handler_sha=HANDLER_SHA, control_sha=CONTROL_SHA):
    """Overrides are for synthetic fixtures only; CLI provides none."""
    pins = {}
    def take(path, expected=None):
        data = read(path, expected); pins[str(path)] = identity(data); return data
    take(here / 'PROTOCOL.md', protocol_sha)
    manifest = json.loads(take(local / 'packet02/manifest.json', original_sha))
    products = {}
    for name, digest in originals.items():
        data = take(local / 'packet02' / name, digest)
        require(manifest['products'][name] == identity(data), 'original product/manifest mismatch')
        products[name] = inject(data) if name == 'review.html' else data
    take(r1 / 'serve_review.py', handler_sha)
    control = r1 / 'localization-control/fixture.png'
    control_bytes = take(control, control_sha)
    asset = manifest['assets']['control']
    require(asset['synthetic'] is True and asset['width'] == 1280 and asset['height'] == 720
            and asset['url'] == '/control.png' and asset['mode'] == 'RGB'
            and asset['bytes'] == len(control_bytes) and asset['sha256'] == control_sha,
            'synthetic control metadata mismatch')
    products['diagnostics.mjs'] = take(here / 'diagnostics.mjs')
    for name in ('build_diagnostic.py', 'serve_diagnostic.py',
                 'test_diagnostic.py', 'test_diagnostics.mjs'):
        take(here / name)
    routes = {url: {'kind': 'packet', 'path': name, **identity(products[name]),
                   'mime': 'text/html; charset=utf-8' if name.endswith('.html')
                           else 'text/javascript; charset=utf-8'} for url, name in CODE.items()}
    routes['/control.png'] = {'kind': 'source', 'path': str(control),
                            **identity(control_bytes), 'mime': 'image/png'}
    for path, pin in pins.items(): read(path, pin)
    return products, {
        'schema': 'synthetic-pointer-diagnostic-packet-v1', 'synthetic_only': True,
        'historical_measurement': False, 'human_acceptance': False,
        'protocol_sha256': protocol_sha, 'original_packet_sha256': original_sha,
        'inputs': pins, 'products': {k: identity(v) for k, v in products.items()},
        'routes': routes, 'limit_events': 100,
        'derivation': 'Original HTML plus one module tag; four other UI modules unchanged.',
        'closure_limit': 'Selected code/control inputs only; no historical media closure replay.'}


def output_path(name, root=HERE):
    require(isinstance(name, str) and re.fullmatch(r'packet[0-9]{2,}', name),
            'explicit packetNN output required')
    path = root / name
    require(not path.exists() and not path.is_symlink(), 'output already exists')
    require(not any(p.is_symlink() for p in [root, *root.parents]), 'symlink output ancestor')
    return path


def build(name, root=HERE, prepare=expected_packet):
    out = output_path(name, root)
    products, manifest = prepare()
    out.mkdir()
    for filename, data in {**products, 'manifest.json': json_bytes(manifest)}.items():
        with (out / filename).open('xb') as target: target.write(data)
    # A failed post-check preserves the directory and every written product.
    again, check = prepare()
    require(products == again and manifest == check, 'inputs changed during build')
    for name, data in {**again, 'manifest.json': json_bytes(check)}.items():
        require(read(out / name) == data, 'product changed during build')
    return manifest


def check_packet(path, prepare=expected_packet):
    require(path.is_dir() and not path.is_symlink(), 'packet directory required')
    products, manifest = prepare()
    require({p.name for p in path.iterdir()} == set(products) | {'manifest.json'},
            'unexpected/missing packet files')
    for name, data in {**products, 'manifest.json': json_bytes(manifest)}.items():
        require(read(path / name) == data, 'packet differs from exact derivation')
    again, after = prepare()
    require(products == again and manifest == after, 'input pins changed during check')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for action in ('build', 'check'):
        part = sub.add_parser(action); part.add_argument('--out', required=True)
    args = parser.parse_args()
    if args.command == 'build': manifest = build(args.out)
    else:
        require(re.fullmatch(r'packet[0-9]{2,}', args.out), 'unsafe packet name')
        manifest = check_packet(HERE / args.out)
    print(json.dumps({'status': 'passed', 'command': args.command, 'out': args.out,
                      'routes': len(manifest['routes']), 'historical_measurement': False}))


if __name__ == '__main__':
    main()
