#!/usr/bin/env python3
"""Pinned existing extractor, new fixed pages/output; no source modification."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SCRIPT = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-annotation/prepare_assets.py')
PIN = 'd9dbd73bc7483e5e1d136085c257bc5db3c808db53e4d95b40feade9c71e5af1'
if hashlib.sha256(SCRIPT.read_bytes()).hexdigest() != PIN:
    raise ValueError('Reviewed extractor changed')
spec = importlib.util.spec_from_file_location('held_extractor', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.HERE = HERE
module.SELECTED = list(range(251, 287))
module.PAGE_ORDER = module.SELECTED.copy()
protocol = (HERE / 'PROTOCOL.md').read_bytes()
dest = HERE / 'assets' / 'PROTOCOL.md'
dest.parent.mkdir(exist_ok=True)
if dest.exists():
    if dest.read_bytes() != protocol:
        raise ValueError('Protocol copy differs')
else:
    with dest.open('xb') as handle:
        handle.write(protocol)
run = sys.argv[1] if len(sys.argv) == 2 else 'run01'
sys.argv = [str(SCRIPT), '--run', run]
module.main()
receipt = {'wrapper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'extractor_sha256': PIN, 'extractor_path': str(SCRIPT),
           'protocol_sha256': hashlib.sha256(protocol).hexdigest(),
           'overrides': {'HERE': str(HERE), 'SELECTED': module.SELECTED, 'PAGE_ORDER': module.PAGE_ORDER},
           'note': 'Historical receipt names reused extractor; this wrapper supplies actual invocation overrides. No verify mode called.'}
with (HERE / 'assets' / run / 'wrapper-receipt.json').open('x') as handle:
    json.dump(receipt, handle, indent=2)
    handle.write('\n')
