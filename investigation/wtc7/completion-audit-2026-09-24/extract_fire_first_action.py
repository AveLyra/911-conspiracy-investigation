#!/usr/bin/env python3
"""Reuse the preserved report extractor without editing it or the source."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SCRIPT = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-annotation/prepare_assets.py')
PIN = 'd9dbd73bc7483e5e1d136085c257bc5db3c808db53e4d95b40feade9c71e5af1'
if hashlib.sha256(SCRIPT.read_bytes()).hexdigest() != PIN:
    raise ValueError('Historical extractor changed; review before execution')
spec = importlib.util.spec_from_file_location('held_fire_extractor', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.HERE = HERE / 'fire-first-action'
module.SELECTED = [274, 275, 276, 277]
module.PAGE_ORDER = [274, 275, 276, 277]
# Historical main reads this protocol; copy exactly, not a substitute summary.
protocol = (HERE / 'FIRE-FIRST-ACTION.md').read_bytes()
protocol_path = module.HERE / 'assets' / 'PROTOCOL.md'
protocol_path.parent.mkdir(parents=True, exist_ok=True)
if protocol_path.exists():
    if protocol_path.read_bytes() != protocol:
        raise ValueError('Protocol copy differs')
else:
    with protocol_path.open('xb') as handle:
        handle.write(protocol)
run = sys.argv[1] if len(sys.argv) == 2 else 'run01'
sys.argv = [str(SCRIPT), '--run', run]
module.main()
receipt = {'wrapper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'extractor_path': str(SCRIPT), 'extractor_sha256': PIN,
           'protocol_sha256': hashlib.sha256(protocol).hexdigest(),
           'overrides': {'HERE': str(module.HERE), 'SELECTED': module.SELECTED, 'PAGE_ORDER': module.PAGE_ORDER},
           'note': 'Historical receipt command names reused extractor; this receipt supplies actual wrapper/overrides. No verify mode invoked.'}
with (module.HERE / 'assets' / run / 'wrapper-receipt.json').open('x') as handle:
    json.dump(receipt, handle, indent=2)
    handle.write('\n')
