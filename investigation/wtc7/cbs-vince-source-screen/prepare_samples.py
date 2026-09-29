"""Probe a declared two-clip stage and freeze nine rational PTS targets; no PNG decode."""
import argparse
from bisect import bisect_left
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
HELPER = HERE.parent / 'late-fire-sequence/sample_sequence.py'
HELPER_SHA256 = 'c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d'
INPUT_SCHEMA = 'cbs-vince-input-v1'
OUTPUT_SCHEMA = 'cbs-vince-nine-target-v1'


def file_sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


if file_sha(HELPER) != HELPER_SHA256:
    raise RuntimeError('Unreviewed sampling helper; import refused')
SPEC = importlib.util.spec_from_file_location('cbs_reviewed_sampler', HELPER)
sampler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sampler)
require = sampler.require


def read_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(sampler.Refusal('nonfinite JSON')))


def validate_input(doc):
    require(isinstance(doc, dict) and set(doc) == {'schema', 'stage', 'sources'} and
            doc['schema'] == INPUT_SCHEMA, 'input manifest schema mismatch')
    require(type(doc['stage']) is int and 1 <= doc['stage'] <= 4, 'invalid stage')
    sources = doc['sources']
    require(isinstance(sources, list) and len(sources) == 2, 'complete two-clip stage required')
    for item in sources:
        require(isinstance(item, dict) and set(item) ==
                {'id', 'clip_number', 'path', 'sha256', 'bytes'}, 'source declaration schema mismatch')
        require(type(item['clip_number']) is int, 'integer clip number required')
        sampler.validate_source({key: item[key] for key in ('id', 'path', 'sha256', 'bytes')} |
                                {'count': 1, 'indices': [0]})
    first = 2 * doc['stage'] - 1
    require([item['clip_number'] for item in sources] == [first, first + 1],
            'declared ascending stage pair required')
    require(len({item['id'] for item in sources}) == 2, 'duplicate source id')
    require(len({item['path'] for item in sources}) == 2, 'duplicate source path')


def positive_ratio(value, separator, label):
    require(isinstance(value, str) and
            re.fullmatch(r'[0-9]+' + re.escape(separator) + r'[0-9]+', value) is not None,
            'invalid ' + label)
    parts = [int(x) for x in value.split(separator)]
    require(all(x > 0 for x in parts), 'nonpositive ' + label)
    return Fraction(*parts)


def declared_video(container):
    require(isinstance(container, dict) and isinstance(container.get('format'), dict) and
            container['format'].get('format_name') == 'avi', 'unreviewed container format')
    require(isinstance(container.get('streams'), list) and
            all(isinstance(s, dict) for s in container['streams']), 'container streams required')
    videos = [s for s in container['streams'] if s.get('codec_type') == 'video']
    require(videos, 'container has no selected video stream')
    first = videos[0]
    require((first.get('codec_name'), first.get('pix_fmt')) in
            (('dvvideo', 'yuv411p'), ('ffv1', 'bgr0')), 'unreviewed selected codec/pixel format')
    return first


def checked_inventory(doc, container):
    require(isinstance(doc, dict) and isinstance(doc.get('frames'), list) and doc['frames'],
            'nonempty decoded frame inventory required')
    require(isinstance(doc.get('streams'), list) and len(doc['streams']) == 1,
            'one selected video stream required')
    stream = doc['streams'][0]
    require(isinstance(stream, dict), 'stream object required')
    tb = positive_ratio(stream.get('time_base'), '/', 'time base')
    require(type(stream.get('index')) is int and stream['index'] >= 0, 'invalid stream index')
    require(isinstance(stream.get('pix_fmt'), str) and
            re.fullmatch(r'[a-zA-Z0-9_]{1,32}', stream['pix_fmt']) is not None, 'invalid pixel format')
    sar = positive_ratio(stream.get('sample_aspect_ratio'), ':', 'stream SAR')
    count = len(doc['frames'])
    frames, stream, helper_tb = sampler.inventory(doc, count)
    require(helper_tb == tb, 'time-base disagreement')
    for frame in frames:
        require(isinstance(frame, dict) and frame.get('media_type') == 'video', 'invalid video frame')
        require(type(frame.get('stream_index')) is int and frame['stream_index'] == stream['index'],
                'frame stream-index mismatch')
        require(all(type(frame.get(key)) is int and frame[key] > 0 for key in ('width', 'height')),
                'invalid frame geometry')
        require(frame.get('pix_fmt') == stream['pix_fmt'], 'frame pixel-format mismatch')
        require(positive_ratio(frame.get('sample_aspect_ratio'), ':', 'frame SAR') == sar,
                'frame SAR mismatch')
        for key in ('interlaced_frame', 'top_field_first'):
            require(type(frame.get(key)) is int and frame[key] in (0, 1), 'invalid ' + key)
    first = declared_video(container)
    require(first.get('index') == stream['index'], 'selected v:0 identity mismatch')
    for key in ('width', 'height', 'pix_fmt', 'codec_name'):
        require(first.get(key) == stream.get(key), 'container/frame stream metadata mismatch: ' + key)
    require(positive_ratio(first.get('time_base'), '/', 'container time base') == tb,
            'container/frame time-base mismatch')
    require(positive_ratio(first.get('sample_aspect_ratio'), ':', 'container SAR') == sar,
            'container/frame SAR mismatch')
    reported_counts = []
    for origin, metadata in [('container', first), ('frames', stream)]:
        for key in ('nb_frames', 'nb_read_frames'):
            value = metadata.get(key)
            if value is None or value == 'N/A':
                continue  # Unknown header count is not zero; count comes from the complete inventory.
            require((type(value) is int and value > 0) or
                    (isinstance(value, str) and re.fullmatch(r'[0-9]+', value) is not None),
                    'invalid reported frame count')
            require(int(value) == count, 'reported/decoded frame count mismatch')
            reported_counts.append({'origin': origin, 'field': key, 'count': int(value)})
    return frames, stream, tb, reported_counts


def quantile_targets(frames, tb):
    pts = [frame['pts'] for frame in frames]
    require(pts and all(type(p) is int for p in pts) and
            all(a < b for a, b in zip(pts, pts[1:])), 'strict integer PTS required')
    require(isinstance(tb, Fraction) and tb > 0, 'positive rational time base required')
    rows = []
    for j in range(9):
        target = Fraction(pts[0]) + Fraction(j, 8) * (pts[-1] - pts[0])
        index = bisect_left(pts, target)
        require(index < len(pts), 'quantile target outside inventory')
        rows.append({'j': j, 'fraction': str(Fraction(j, 8)),
                     'target_pts_exact': str(target), 'target_seconds_exact': str(target * tb),
                     'selected_index': index, 'selected_pts': pts[index],
                     'selected_seconds_exact': str(pts[index] * tb)})
    return rows, sorted({row['selected_index'] for row in rows})


def probe_source(item, dest, pins):
    dest.mkdir()  # Existing output is a refusal, not a retry or overwrite.
    receipt = {'schema': OUTPUT_SCHEMA, 'source': item, 'pins': pins,
               'status': 'refused', 'scientific_or_human_acceptance': False,
               'source_identity': {}, 'probe_diagnostics': {}, 'reasons': []}
    source = None
    selection = None
    try:
        source = sampler.absolute(item['path'])
        before = sampler.observed_identity(source)
        receipt['source_identity']['before'] = before
        require(sampler.identity_matches(before, item), 'source identity mismatch before')
        docs = {}
        commands = {
            'container': [sampler.FFPROBE, '-v', 'warning', '-show_streams', '-show_format', '-of', 'json', str(source)],
            'frames': [sampler.FFPROBE, '-v', 'warning', '-select_streams', 'v:0', '-show_frames',
                       '-show_streams', '-show_format', '-of', 'json', str(source)],
        }
        for name, command in commands.items():
            stdout, stderr, status = sampler.run_command(command, dest, name)
            receipt['probe_diagnostics'][name] = {'status': 'parse_failed'}
            receipt['probe_diagnostics'][name] = sampler.probe_diagnostics(stderr)
            require(status['returncode'] == 0, name + ' process nonzero or launch failure')
            require(receipt['probe_diagnostics'][name]['status'] == 'clean', name + ' diagnostics refused')
            docs[name] = read_json(stdout)
            if name == 'container':
                declared_video(docs[name])  # Stop unknown lanes before even the frame-inventory probe.
        frames, stream, tb, counts = checked_inventory(docs['frames'], docs['container'])
        targets, indices = quantile_targets(frames, tb)
        selection = {'id': item['id'], 'clip_number': item['clip_number'],
                     'count': len(frames), 'time_base': str(tb), 'first_pts': frames[0]['pts'],
                     'last_pts': frames[-1]['pts'], 'width': stream['width'], 'height': stream['height'],
                     'sample_aspect_ratio': stream['sample_aspect_ratio'], 'pix_fmt': stream['pix_fmt'],
                     'codec_name': stream['codec_name'],
                     'reported_frame_counts': counts, 'targets': targets, 'indices': indices}
    except Exception as exc:
        receipt['reasons'].append(type(exc).__name__ + ': ' + str(exc))
    finally:
        if source is not None:
            try:
                after = sampler.observed_identity(source)
                receipt['source_identity']['after'] = after
                require(sampler.identity_matches(after, item), 'source identity mismatch after')
                require(receipt['source_identity'].get('before') == after, 'source changed during probe')
            except Exception as exc:
                receipt['reasons'].append(type(exc).__name__ + ': ' + str(exc))
        if not receipt['reasons'] and selection is not None:
            sampler.save(dest / 'targets.json', selection)
            receipt['status'] = 'metadata_selection_only_not_extracted'
        sampler.save(dest / 'receipt.json', receipt)
    return receipt, selection if not receipt['reasons'] else None


def prepare(manifest_path, manifest_digest, protocol_path, protocol_digest, out):
    for path in (manifest_path, protocol_path, out):
        sampler.absolute(str(path))
    out.mkdir()
    result = {'schema': OUTPUT_SCHEMA, 'status': 'refused', 'sources': [], 'reasons': [],
              'scientific_or_human_acceptance': False}
    inputs = {}
    selections = []
    manifest = None
    try:
        for path, pin, name in [(manifest_path, manifest_digest, 'manifest.input.json'),
                                (protocol_path, protocol_digest, 'protocol.input.md')]:
            sampler.digest_string(pin)
            require(sampler.observed_identity(path)['sha256'] == pin, 'declaration hash mismatch')
            with (out / name).open('xb') as handle:
                handle.write(path.read_bytes())
            require(file_sha(out / name) == pin, 'declaration snapshot mismatch')
        require(file_sha(HELPER) == HELPER_SHA256, 'unreviewed sampling helper')
        manifest = read_json((out / 'manifest.input.json').read_bytes())
        validate_input(manifest)
        inputs = {str(path): file_sha(path) for path in
                  (manifest_path, protocol_path, Path(__file__), HELPER, Path(sys.executable), Path(sampler.FFPROBE))}
        result['pins_before'] = inputs
        result['environment'] = {'python': sys.version, 'pillow': sampler.pillow_version,
                                 'probe_version_required': '7.1.1', 'selected_video_stream': 'v:0'}
        stdout, stderr, status = sampler.run_command([sampler.FFPROBE, '-version'], out, 'ffprobe-version')
        require(status['returncode'] == 0 and not stderr and
                stdout.startswith(b'ffprobe version 7.1.1 '), 'ffprobe version refused')
        for item in manifest['sources']:
            receipt, selection = probe_source(item, out / item['id'], inputs)
            result['sources'].append({'id': item['id'], 'status': receipt['status']})
            if selection is not None:
                selections.append(selection)
    except Exception as exc:
        result['reasons'].append(type(exc).__name__ + ': ' + str(exc))
    finally:
        try:
            after = {path: file_sha(path) for path in inputs}
            result['pins_after'] = after
            result['pins_unchanged'] = bool(inputs) and inputs == after
            require(result['pins_unchanged'], 'inputs changed or preparation not reached')
            if not result['reasons'] and len(selections) == 2:
                for item in manifest['sources']:
                    require(sampler.identity_matches(sampler.observed_identity(Path(item['path'])), item),
                            'source identity changed before stage manifest')
                sources = [{key: item[key] for key in ('id', 'path', 'sha256', 'bytes')} |
                           {'count': selection['count'], 'indices': selection['indices']}
                           for item, selection in zip(manifest['sources'], selections)]
                selection_manifest = {'schema': sampler.SCHEMA, 'sources': sources}
                sampler.validate_manifest(selection_manifest)
                sampler.save(out / 'sampling-manifest.json', selection_manifest)
                sampler.save(out / 'selection-targets.json',
                             {'schema': OUTPUT_SCHEMA, 'stage': manifest['stage'], 'sources': selections})
                result['status'] = 'prepared_not_executed'
            elif not result['reasons']:
                result['reasons'].append('One or more clip inventories refused; no stage sampling manifest')
        except Exception as exc:
            result['reasons'].append(type(exc).__name__ + ': ' + str(exc))
        result['products'] = {str(p.relative_to(out)): {'bytes': p.stat().st_size, 'sha256': file_sha(p)}
                              for p in sorted(out.rglob('*')) if p.is_file()}
        sampler.save(out / 'preparation-receipt.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('manifest', 'protocol', 'out'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--protocol-sha256', required=True)
    args = parser.parse_args()
    result = prepare(args.manifest, args.manifest_sha256, args.protocol, args.protocol_sha256, args.out)
    print(json.dumps({'status': result['status'], 'source_count': len(result['sources']),
                      'scientific_or_human_acceptance': False}))
    return 0 if result['status'] == 'prepared_not_executed' else 1


if __name__ == '__main__':
    sys.exit(main())
