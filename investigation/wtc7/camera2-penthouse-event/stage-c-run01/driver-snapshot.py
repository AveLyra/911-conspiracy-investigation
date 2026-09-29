"""Fixed Stage C displays from preserved PNGs; no decoding or feature inference."""
import argparse
from fractions import Fraction
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import re
import sys
import types
import warnings

import PIL
from PIL import Image, PngImagePlugin, _imaging

UNIT = Path(__file__).resolve().parent
SOURCE = UNIT / 'run01/camera2'
CROP_MODULE = UNIT.parent / 'camera2-calibration-source/prepare_context.py'
CROP_SHA = '31c7ca05494fa3abb8ea4300077691c8aa79abd2e0238fad6b8c0317ba33be91'
DECLARATION_SHA = '7a1bf712a8d1b5dc629395e2c704afda1cce93068db386f0125e460663b2554d'
INDICES = (6593, 6689, 6701, 6707, 6714, 6717, 6724, 6736, 6784, 6881, 6904,
           *range(6920, 6979), 7013)
RECTANGLE = (300, 125, 465, 245)
SCALE = 4
EXECUTION_KIND = 'stage-c-historical-display'
PINS = {
    UNIT / 'STAGE-C.md': DECLARATION_SHA,
    UNIT.parent / 'CHARTER.md': '54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
    CROP_MODULE: CROP_SHA,
    SOURCE / 'selection.json': 'e297292a04a093d757b7693b9914abe4b88db4e6b836461f49c8dee411e78b2d',
    UNIT / 'root-stage-b.md': 'c01c9fe3628fae76417d11c166f5981706162c93362984c6114157a6a70e2bbf',
    UNIT / 'root-stage-b-scope.md': '3135cf7600ab4b9cef7a60adef238cf653ce38a71fe7af64f54b98b3254124c3',
    UNIT / 'observer-stage-b.md': 'cea1a9c0db50d0ece47ceb19a877f97977d8348e47c61a84fc630ce5c54a6da5',
    UNIT / 'observer-stage-b-scope.md': '9794d0e106f87bdb0a8783c559992ec62757c9088ba993dd8d5a6da48e13809d',
}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def fingerprint(path):
    with Path(path).open('rb') as stream:
        before = os.fstat(stream.fileno())
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        after = os.fstat(stream.fileno())
    require((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns), 'changed-during-hash')
    return {'bytes': after.st_size, 'sha256': digest}


def byte_identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def write_json(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def fresh_output(out):
    path = Path(out)
    if not path.is_absolute():
        path = UNIT / path
    require(path.parent == UNIT and path.name in ('stage-c-run01', 'stage-c-run02'), 'output-scope')
    require(not path.is_symlink(), 'output-symlink')
    require(path.resolve().parent == UNIT.resolve(), 'output-confinement')
    require(not path.exists(), 'output-already-exists')
    return path


def load_crop():
    """Import only a byte-pinned module; its historical main is never called."""
    require(not CROP_MODULE.is_symlink(), 'crop-symlink')
    data = CROP_MODULE.read_bytes()
    require(byte_identity(data)['sha256'] == CROP_SHA, 'crop-code-pin')
    module = types.ModuleType('stage_c_pinned_crop')
    module.__file__ = str(CROP_MODULE)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        # Execute the exact hashed source bytes, never an existing .pyc cache.
        exec(compile(data, str(CROP_MODULE), 'exec'), module.__dict__)
    finally:
        sys.dont_write_bytecode = previous
    require(fingerprint(CROP_MODULE)['sha256'] == CROP_SHA, 'crop-code-changed')
    return module


def pinned_inputs():
    identities = {}
    for path, expected in PINS.items():
        require(not path.is_symlink(), 'input-symlink: ' + path.name)
        identity = fingerprint(path)
        require(identity['sha256'] == expected, 'input-pin: ' + path.name)
        identities[str(path)] = identity
    return identities


def runtime_inputs():
    require(platform.python_version() == '3.13.7', 'python-version')
    require(PIL.__version__ == '12.0.0', 'pillow-version')
    paths = [Path(__file__).resolve(), UNIT / 'test_stage_c_display.py',
             Path(sys.executable).resolve(), Path(PIL.__file__), Path(Image.__file__),
             Path(PngImagePlugin.__file__), Path(_imaging.__file__)]
    return {str(path): fingerprint(path) for path in paths}


def canonical_integer(value):
    require(type(value) is str and re.fullmatch(r'0|[1-9][0-9]*', value), 'canonical-integer')
    return int(value)


def canonical_fraction(value):
    require(type(value) is str, 'fraction-type')
    fraction = Fraction(value)
    require(str(fraction) == value, 'canonical-fraction')
    return fraction


def select_rows(document):
    require(document['geometry'] == [640, 480], 'selection-geometry')
    require(document['source_id'] == 'VID-WTC7-001', 'selection-source-id')
    require(document['checked_frames'] == 8042 and document['exit_code'] == 0, 'selection-extraction')
    rows = document['images']
    indices = [canonical_integer(row['frame_index_zero_based']) for row in rows]
    require(indices == list(range(6593, 7014)), 'selection-order-unique-complete')
    require(tuple(sorted(set(INDICES))) == INDICES and len(INDICES) == 71, 'stage-c-indices')
    previous_time = None
    for row, index in zip(rows, indices):
        pts = canonical_integer(row['source_pts'])
        require(canonical_integer(row['best_effort_timestamp']) == pts, 'pts-best-effort')
        tb = canonical_fraction(row['source_time_base'])
        require(tb == Fraction(1, 2997), 'source-timebase')
        time = canonical_fraction(row['source_time_seconds_exact'])
        require(time == pts * tb, 'source-exact-time')
        require(previous_time is None or time > previous_time, 'source-time-order')
        previous_time = time
        ticks = row['source_duration_ticks']
        require(type(ticks) is int and ticks > 0, 'source-duration')
        require(canonical_fraction(row['source_duration_seconds_exact']) == ticks * tb, 'source-duration-time')
        require(row['png'] == f'f{index:06d}.png', 'source-png-name')
        identity = row['png_identity']
        require(type(identity['bytes']) is int and identity['bytes'] > 0, 'source-png-bytes')
        for digest in (identity['sha256'], row['luma_sha256']):
            require(type(digest) is str and re.fullmatch('[0-9a-f]{64}', digest), 'source-hash-format')
    selected = {index: row for index, row in zip(indices, rows)}
    return [selected[index] for index in INDICES]


def read_source(row):
    path = SOURCE / row['png']
    require(not SOURCE.is_symlink() and not path.is_symlink(), 'source-symlink')
    require(path.resolve().parent == SOURCE.resolve(), 'source-confinement')
    data = path.read_bytes()
    require(byte_identity(data) == row['png_identity'], 'source-png-pin')
    with Image.open(io.BytesIO(data)) as image:
        require(image.format == 'PNG' and image.mode == 'L' and image.size == (640, 480), 'source-image-geometry')
        require(getattr(image, 'n_frames', 1) == 1, 'source-image-frames')
        require(not set(image.info) & {'transparency', 'gamma', 'srgb', 'icc_profile'}, 'source-render-metadata')
        plane = image.tobytes()
        require(hashlib.sha256(plane).hexdigest() == row['luma_sha256'], 'source-luma-pin')
        return image.copy()


def products(out):
    return {path.name: fingerprint(path) for path in sorted(out.iterdir()) if path.is_file()}


def warning_records(caught):
    return [{'category': item.category.__name__, 'message': str(item.message)} for item in caught]


def run(out):
    out = fresh_output(out)
    out.mkdir(exist_ok=False)
    phase = 'input-pins'
    caught = []
    before = {}
    after = {}
    runtime_before = {}
    runtime_after = {}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        try:
            before = pinned_inputs()
            runtime_before = runtime_inputs()
            require(RECTANGLE == (300, 125, 465, 245) and SCALE == 4, 'fixed-transform')
            crop_module = load_crop()
            phase = 'selection'
            selection_bytes = (SOURCE / 'selection.json').read_bytes()
            require(byte_identity(selection_bytes) == before[str(SOURCE / 'selection.json')], 'selection-changed')
            rows = select_rows(json.loads(selection_bytes))
            for row in rows:
                path = SOURCE / row['png']
                require(not path.is_symlink(), 'source-symlink')
                identity = fingerprint(path)
                require(identity == row['png_identity'], 'source-png-pin')
                before[str(path)] = identity
            write_json(out / 'input-pins-before.json', before)
            write_json(out / 'runtime-pins-before.json', runtime_before)
            snapshots = [(Path(__file__), 'driver-snapshot.py'),
                         (UNIT / 'test_stage_c_display.py', 'test-snapshot.py'),
                         (CROP_MODULE, 'inherited-crop-snapshot.py'),
                         (UNIT / 'STAGE-C.md', 'stage-c-snapshot.md'),
                         (UNIT.parent / 'CHARTER.md', 'charter-snapshot.md'),
                         (SOURCE / 'selection.json', 'selection-snapshot.json')]
            snapshots += [(UNIT / name, name.replace('.md', '-snapshot.md')) for name in
                          ('root-stage-b.md', 'root-stage-b-scope.md', 'observer-stage-b.md', 'observer-stage-b-scope.md')]
            for source, name in snapshots:
                data = source.read_bytes()
                expected = before.get(str(source), runtime_before.get(str(source)))
                require(byte_identity(data) == expected, 'snapshot-source-changed')
                with (out / name).open('xb') as stream:
                    stream.write(data)
            write_json(out / 'initial.json', {'execution_kind': EXECUTION_KIND,
                'python': sys.version, 'pillow': PIL.__version__, 'command': sys.argv,
                'indices': INDICES, 'rectangle_half_open': RECTANGLE, 'scale': SCALE,
                'limitations': 'display derivative only; no recovered resolution, feature identity or event acceptance'})
            result_rows = []
            phase = 'render'
            for row in rows:
                index = canonical_integer(row['frame_index_zero_based'])
                image = read_source(row)
                native, enlarged = crop_module.crop(image, RECTANGLE, SCALE)
                outputs = {}
                for kind, product, dimensions in [('native', native, (165, 120)), ('4x', enlarged, (660, 480))]:
                    require(product.mode == 'L' and product.size == dimensions, 'product-geometry')
                    product.info.clear()
                    name = f'f{index:06d}-{kind}.png'
                    with (out / name).open('xb') as stream:
                        product.save(stream, format='PNG')
                    with Image.open(out / name) as saved:
                        require(saved.format == 'PNG' and saved.mode == 'L' and saved.size == dimensions,
                                'saved-product-geometry')
                        require(getattr(saved, 'n_frames', 1) == 1 and not saved.info, 'saved-product-metadata')
                        require(saved.tobytes() == product.tobytes(), 'saved-product-pixels')
                    outputs[kind] = {'png': name, 'png_identity': fingerprint(out / name),
                        'luma_sha256': hashlib.sha256(product.tobytes()).hexdigest(),
                        'size': list(dimensions), 'mode': 'L', 'frames': 1, 'png_info_keys': []}
                result_rows.append({'frame_index_zero_based': index, 'source': row, 'outputs': outputs})
            phase = 'post-input-pins'
            after = {path: fingerprint(Path(path)) for path in before}
            write_json(out / 'input-pins-after.json', after)
            require(after == before, 'source-or-dependency-changed')
            require(pinned_inputs() == {path: before[path] for path in map(str, PINS)}, 'post-input-pin')
            phase = 'post-runtime-pins'
            runtime_after = runtime_inputs()
            write_json(out / 'runtime-pins-after.json', runtime_after)
            require(runtime_after == runtime_before, 'runtime-or-code-changed')
            require(not caught, 'unexpected-warning')
            phase = 'product-inventory'
            names = {f'f{index:06d}-{kind}.png' for index in INDICES for kind in ('native', '4x')}
            require({path.name for path in out.glob('*.png')} == names, 'product-count-or-names')
            result = {'status': 'complete', 'execution_kind': EXECUTION_KIND,
                'python': platform.python_version(), 'pillow': PIL.__version__,
                'indices': INDICES, 'rectangle_half_open': RECTANGLE, 'scale': SCALE,
                'resampling': 'NEAREST', 'source_geometry': [640, 480], 'source_mode': 'L',
                'rows': result_rows, 'input_pins_before': before, 'input_pins_after': after,
                'runtime_pins_before': runtime_before, 'runtime_pins_after': runtime_after,
                'warnings': [], 'products': products(out)}
            write_json(out / 'receipt.json', result)
            return result
        except Exception as error:
            write_json(out / 'failure.json', {'status': 'failed', 'execution_kind': EXECUTION_KIND,
                'phase': phase, 'error_type': type(error).__name__, 'error': str(error),
                'warnings': warning_records(caught), 'input_pins_before': before,
                'input_pins_after': after, 'runtime_pins_before': runtime_before,
                'runtime_pins_after': runtime_after, 'partial_products': products(out)})
            raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, choices=('stage-c-run01', 'stage-c-run02'))
    args = parser.parse_args(argv)
    result = run(args.out)
    print(json.dumps({'status': result['status'], 'frames': len(result['rows']), 'images': 142}))


if __name__ == '__main__':
    main()
