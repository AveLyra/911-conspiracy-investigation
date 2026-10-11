"""Root replay and preservation checks; never changes evidence or prior outputs."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def pin(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'sha256': digest, 'bytes': path.stat().st_size}


def read(path):
    return json.loads(path.read_text())


def main():
    destination = HERE / 'final-verification.json'
    if destination.exists():
        raise FileExistsError('Existing final verification preserved')
    start = time.monotonic()
    records = [HERE / name for name in ['PROTOCOL.md', 'config.json', 'preparation-review.json',
        'extract_dense.py', 'dense_screen.py', 'test_dense_screen.py', 'independent_check.py',
        'extraction-check.json', 'independent-check.json', 'root-observations.json',
        'independent-visual-review.json', 'report.md', 'final_verify.py']]
    before = {p.name: pin(p) for p in records}
    result = {'status': 'started', 'before': before, 'python': sys.executable}
    try:
        checker_path = HERE / 'independent_check.py'
        assert pin(checker_path)['sha256'] == '9866921fa63dd4384a9e1a029d2805982893a35629eeff6429ea58ff0b949453'
        spec = importlib.util.spec_from_file_location('root_replay_checker', checker_path)
        check = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(check)
        arithmetic = check.load_arithmetic()
        result['synthetic_replay'] = arithmetic.synthetic()
        score = check.scores(HERE / 'screen01', HERE / 'screen02', arithmetic)
        previous = read(HERE / 'independent-check.json')['verification']
        assert score == previous, 'Root replay differs from separate reviewer'
        result['score_replay'] = {k: v for k, v in score.items() if k != 'comparisons'}
        extraction = check.extraction(HERE / 'extract01', HERE / 'extract02', result)
        assert extraction == read(HERE / 'extraction-check.json')['verification']
        result['extraction_replay'] = extraction
        parent = HERE.parent / 'picture01'
        check.checked_receipt(parent)
        old = {(r['reference_index'], r['source_index']): r for r in read(parent / 'results.json')}
        common = [r for r in read(HERE / 'screen01/results.json') if r['source_index'] in range(300, 511, 30)]
        assert len(common) == 24
        for row in common:
            assert row == old[(row['reference_index'], row['source_index'])]
            assert (parent / row['surface_file']).read_bytes() == (HERE / 'screen01' / row['surface_file']).read_bytes()
        result['coarse_overlap'] = {'rows_transforms': 24, 'identical_npz_files': 24}
        frozen = {str(p.relative_to(HERE / 'screen01')): pin(p) for p in (HERE / 'screen01').rglob('*') if p.is_file()}
        command = [sys.executable, '-B', str(HERE / 'dense_screen.py'), 'screen', '--run', 'screen01', '--controls', 'controls01']
        refusal = subprocess.run(command, capture_output=True, timeout=60)
        assert refusal.returncode != 0 and b'FileExistsError' in refusal.stderr
        assert frozen == {str(p.relative_to(HERE / 'screen01')): pin(p) for p in (HERE / 'screen01').rglob('*') if p.is_file()}
        result['existing_output_refusal'] = {'argv': command, 'exit': refusal.returncode,
            'expected_exception': 'FileExistsError', 'preserved_files': len(frozen)}
        parsed = list(HERE.rglob('*.json'))
        for path in parsed:
            read(path)
        links = re.findall(r'\]\(([^)]+)\)', (HERE / 'report.md').read_text())
        for link in links:
            if link != 'final-verification.json':
                assert (HERE / link).exists(), link
        result['json_files_parsed_before_receipt'] = len(parsed)
        result['report_local_links'] = len(links)
        result['after'] = {p.name: pin(p) for p in records}
        assert result['after'] == before
        result['status'] = 'complete'
    except Exception as exc:
        result.update(status='failed', error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        result['elapsed_s'] = time.monotonic() - start
        with destination.open('x') as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
            stream.write('\n')
    print(json.dumps({'status': result['status'], 'score_pairs': score['pairs'], 'native_pixel_checks': extraction['selected_png_pixel_comparisons']}))


if __name__ == '__main__':
    main()
