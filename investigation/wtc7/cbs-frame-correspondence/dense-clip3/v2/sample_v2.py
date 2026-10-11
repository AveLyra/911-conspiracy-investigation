"""Versioned sampler configuration: exactly one optional ASCII fps-padding space.

The separate imported module keeps every function body unchanged. Its __file__
and PARENT_SHA256 are explicitly configured for truthful existing receipts:
code_sha256 is THIS adapter, parent_code_sha256 is the original sampler.
No original disk file or saved diagnostic stream is rewritten.
"""
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parents[2]/'late-fire-sequence/sample_sequence.py'
PARENT_SHA = 'c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d'
if hashlib.sha256(PARENT.read_bytes()).hexdigest() != PARENT_SHA:
    raise ValueError('sampler parent pin mismatch')
spec = importlib.util.spec_from_file_location('configured_sampler_v2', PARENT)
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)
original_pattern = (rf'frame=\s*\d+ fps={api.NUMBER} q={api.NUMBER} Lsize=N/A time=\d+:\d+:\d+\.\d+ '
                    rf'bitrate=N/A speed=\s*{api.NUMBER}x\s*')
api.require(api.BARE_INFO[-1] == original_pattern, 'unexpected parent final-summary pattern')
api.require(original_pattern.count('fps='+api.NUMBER) == 1, 'fps fragment cardinality')
api.BARE_INFO[-1] = original_pattern.replace('fps='+api.NUMBER, 'fps= ?'+api.NUMBER)
api.__file__ = str(Path(__file__).resolve())
api.PARENT_SHA256 = PARENT_SHA


if __name__ == '__main__':
    raise SystemExit(api.main())
