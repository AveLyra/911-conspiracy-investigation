"""Fixed Camera 2 extraction only; admission is not event or causal validation."""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

import PIL
from PIL import Image

UNIT = Path(__file__).resolve().parent
OLD = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/multiview-onset-review')
FFMPEG = Path('/opt/homebrew/bin/ffmpeg')
FFPROBE = Path('/opt/homebrew/bin/ffprobe')
DEPENDENCIES = {
    OLD / 'extract.py': 'df245c5fcf2790a45643c1fddf481bd38c63aed3592a4b0c9ad32819c23dc64c',
    OLD / 'PROTOCOL.md': '1dfdabe397ff64fba08b712f2999242380aa1cd5733f74152392064aec8794a5',
    UNIT / 'STAGE-B.md': '24738fd6c695f450972b663cb55836b3d935b8c91487630c1aeca763d21d3da3',
}
SOURCE_ID = 'VID-WTC7-001'
SOURCE_SHA = '84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730'


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def fingerprint(path):
    with Path(path).open('rb') as stream:
        value = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': Path(path).stat().st_size, 'sha256': value}


def write_json(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def fresh_output(path):
    path = Path(path).absolute()
    require(path != UNIT and path.is_relative_to(UNIT), 'output-outside-unit')
    for part in (path, *path.parents):
        if part == UNIT:
            break
        require(not part.is_symlink(), 'output-symlink')
    require(path.resolve().is_relative_to(UNIT), 'output-outside-unit')
    require(not path.exists(), 'output-already-exists')
    return path


def check_dependencies():
    pins = {}
    for path, expected in DEPENDENCIES.items():
        identity = fingerprint(path)
        require(identity['sha256'] == expected, 'dependency-pin: ' + path.name)
        pins[str(path)] = identity
    return pins


def canonical_integer(value):
    require(type(value) is str and re.fullmatch(r'-?(0|[1-9][0-9]*)', value), 'map-integer')
    return int(value)


def select_frames(rows, start=Fraction(220), end=Fraction(234)):
    require(type(start) is Fraction and type(end) is Fraction and start <= end, 'interval')
    require(bool(rows), 'empty-map')
    times = []
    timebase = None
    for index, row in enumerate(rows):
        require(canonical_integer(row['frame_index_zero_based']) == index, 'map-index-order')
        pts = canonical_integer(row['source_pts'])
        require(canonical_integer(row['best_effort_timestamp']) == pts, 'map-best-effort')
        tb = Fraction(row['source_time_base'])
        require(tb > 0 and (timebase is None or tb == timebase), 'map-timebase')
        timebase = tb
        time = Fraction(row['source_time_seconds_exact'])
        require(time == pts * tb, 'map-exact-time')
        require(not times or time > times[-1], 'map-nonmonotone')
        times.append(time)
    inside = [i for i, time in enumerate(times) if start <= time <= end]
    require(bool(inside), 'no-interior-frame')
    require(inside[0] > 0 and inside[-1] < len(rows) - 1, 'missing-adjoining-bound')
    indices = [inside[0] - 1, *inside, inside[-1] + 1]
    require(indices == sorted(set(indices)), 'selection-order-duplicate')
    selected = {i: ['closed-interval-interior'] for i in inside}
    selected[inside[0] - 1] = ['immediately-preceding-bound']
    selected[inside[-1] + 1] = ['immediately-following-bound']
    selected = dict(sorted(selected.items()))
    return selected, {'start_seconds_exact': str(start), 'end_seconds_exact': str(end),
        'closed': True, 'interior_count': len(inside), 'selected_count': len(indices),
        'indices': indices, 'source_time_base': str(timebase)}


class HistoricalAdapter:
    """Unchanged old functions are loaded only after their dependency pin passes."""
    kind = 'historical-extraction'

    def __init__(self):
        specification = importlib.util.spec_from_file_location('camera2_pinned_extractor', OLD / 'extract.py')
        self.module = importlib.util.module_from_spec(specification)
        previous = sys.dont_write_bytecode
        sys.dont_write_bytecode = True
        try:
            specification.loader.exec_module(self.module)
        finally:
            sys.dont_write_bytecode = previous
        self.spec = dict(self.module.SPECS['camera2'])
        require(self.spec['id'] == SOURCE_ID and self.spec['source'] == SOURCE_SHA, 'camera2-spec')
        require(self.module.FFMPEG == FFMPEG, 'decoder-path')

    def inputs(self):
        rows, pins = self.module.inputs(self.spec)
        metadata = json.loads((self.module.TIMING / SOURCE_ID / 'frames.json').read_text())['frames']
        return rows, metadata, pins

    def decode(self, rows, chosen, destination):
        return self.module.decode(self.module.MEDIA / self.spec['name'], rows, 640, 480, chosen, destination)

    def sheets(self, result, destination):
        return self.module.sheets(result, destination)


def validate_metadata(rows, metadata):
    require(len(rows) == len(metadata) == 8042, 'camera2-frame-count')
    for row, frame in zip(rows, metadata):
        require(type(frame['pts']) is int and frame['pts'] == int(row['source_pts']), 'metadata-pts')
        require((frame['width'], frame['height'], frame['pix_fmt']) == (640, 480, 'yuv420p'), 'metadata-geometry')
        require(type(frame['duration']) is int and frame['duration'] > 0, 'metadata-duration')


def admit_result(result, rows, metadata, chosen, destination):
    require(result['checked_frames'] == 8042 and result['geometry'] == [640, 480], 'decoded-count-geometry')
    require(result['exit_code'] == 0, 'decoder-exit')
    expected_diagnostic = {'audio_layout_guess_stereo_lines': 1, 'unclassified_lines': 0,
                           'raw_local_log': 'decoder.local-only.log'}
    require(result['diagnostics'] == expected_diagnostic, 'exactly-one-audio-layout-warning')
    log = (destination / 'decoder.local-only.log').read_bytes().splitlines()
    pattern = rb'\[aist#0:[0-9]+/pcm_s16le @ 0x[0-9a-f]+\] Guessed Channel Layout: stereo'
    require(len(log) == 1 and re.fullmatch(pattern, log[0]), 'raw-diagnostic-contract')
    require(re.fullmatch('[0-9a-f]{64}', result['raw_stream_sha256']), 'raw-stream-hash')
    images = result['images']
    require([canonical_integer(r['frame_index_zero_based']) for r in images] == list(chosen), 'decoded-selection')
    for image, index in zip(images, chosen):
        require({key: image[key] for key in rows[index]} == rows[index], 'selected-map-row')
        require(image['selection_reasons'] == chosen[index], 'selected-reason')
        require(image['png'] == f'f{index:06d}.png', 'selected-filename')
        path = destination / image['png']
        require(fingerprint(path) == image['png_identity'], 'selected-png-pin')
        with Image.open(path) as png:
            require(png.format == 'PNG' and png.mode == 'L' and png.size == (640, 480), 'selected-png-format')
            require(hashlib.sha256(png.tobytes()).hexdigest() == image['luma_sha256'], 'selected-luma-pin')
        duration = metadata[index]['duration']
        image['source_duration_ticks'] = duration
        image['source_duration_seconds_exact'] = str(duration * Fraction(rows[index]['source_time_base']))


def run(out, adapter=None):
    out = fresh_output(out)
    out.mkdir(parents=True, exist_ok=False)
    phase = 'dependency-pins'
    kind = 'historical-extraction' if adapter is None else 'synthetic-adapter-control'
    try:
        dependencies = check_dependencies()
        runtime_paths = [Path(__file__), Path(sys.executable).resolve(), FFMPEG, FFPROBE]
        initial_pins = {**dependencies, **{str(p): fingerprint(p) for p in runtime_paths}}
        snapshots = [(Path(__file__), 'driver-snapshot.py'), (UNIT / 'STAGE-B.md', 'stage-b-snapshot.md'),
            (OLD / 'extract.py', 'inherited-extract-snapshot.py'), (OLD / 'PROTOCOL.md', 'inherited-protocol-snapshot.md')]
        for source, name in snapshots:
            with (out / name).open('xb') as stream:
                stream.write(source.read_bytes())
        write_json(out / 'initial.json', {'kind': kind, 'pins': initial_pins,
            'python': sys.version, 'executable': str(Path(sys.executable).resolve()), 'pillow': PIL.__version__,
            'ffmpeg_version': subprocess.check_output([str(FFMPEG), '-version'], text=True).splitlines()[0],
            'ffprobe_version': subprocess.check_output([str(FFPROBE), '-version'], text=True).splitlines()[0]})
        phase = 'source-inputs'
        implementation = HistoricalAdapter() if adapter is None else adapter
        rows, metadata, before = implementation.inputs()
        chosen, plan = select_frames(rows)
        validate_metadata(rows, metadata)
        require(plan['interior_count'] == 419 and plan['indices'] == list(range(6593, 7014)), 'fixed-camera2-plan')
        write_json(out / 'selection-plan.json', plan)
        write_json(out / 'source-pins-before.json', before)
        destination = out / 'camera2'
        destination.mkdir()
        phase = 'decode'
        result = implementation.decode(rows, chosen, destination)
        phase = 'result-admission'
        admit_result(result, rows, metadata, chosen, destination)
        result['overview_sheets'] = implementation.sheets(result, destination)
        require(result['overview_sheets'] == [f'overview-{n:02d}.png' for n in range(27)], 'overview-count-names')
        require(all((destination / name).is_file() for name in result['overview_sheets']), 'overview-missing')
        phase = 'post-input-pins'
        after_rows, after_metadata, after = implementation.inputs()
        require(after == before and after_rows == rows and after_metadata == metadata, 'post-input-pin')
        write_json(out / 'source-pins-after.json', after)
        require(check_dependencies() == dependencies, 'post-dependency-pin')
        final_pins = {path: fingerprint(Path(path)) for path in initial_pins}
        require(final_pins == initial_pins, 'post-runtime-pin')
        result['input_pins'] = before
        result['input_pins_before'] = before
        result['input_pins_after'] = after
        result['source_id'] = SOURCE_ID
        result['execution_kind'] = kind
        write_json(destination / 'selection.json', result)
        products = {str(p.relative_to(out)): fingerprint(p) for p in sorted(out.rglob('*')) if p.is_file()}
        write_json(out / 'receipt.json', {'status': 'complete', 'execution_kind': kind,
            'cameras': {'camera2': {'checked_frames': 8042, 'selected': len(chosen)}}, 'products': products,
            'runtime_pins_before': initial_pins, 'runtime_pins_after': final_pins})
        return result
    except Exception as error:
        write_json(out / 'failure.json', {'status': 'failed', 'execution_kind': kind,
            'phase': phase, 'error_type': type(error).__name__, 'error': str(error)})
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(argv)
    run(args.out)
    print(json.dumps({'status': 'complete', 'camera': 'camera2', 'selected': 421}))


if __name__ == '__main__':
    main()

# synthetic tamper
