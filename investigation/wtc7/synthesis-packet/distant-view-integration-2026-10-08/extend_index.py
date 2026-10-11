#!/usr/bin/env python3
"""Exact additive v2-preservation wrapper around the unchanged v1 validator.

No source interpretation or new scientific test is performed. Production is
disabled until the reviewed extension's literal hash replaces the placeholder.
Pure functions taking a validator/context are exposed for synthetic tests only;
the CLI has no control-path, hash, baseline or acceptance overrides.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import types

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
OLD = HERE.parent / 'integration-2026-10-08'
EXTENSION_SHA = '41046974bccc6694b8fe9114a738511a7b8858f784892b8705d7a34f7651cc61'
VALIDATOR_SHA = '97c4cba63dd29ddc0667262a9038bfb86670ee1ddee8e27175e53626c9aaee96'
FIXED = {
    'baseline': (OLD / 'candidate-index.json', '6ad3012fd455dafe4face2cf031a3624135f83c99b24dfe641e6a35e0084f7e1'),
    'protocol': (HERE / 'PROTOCOL.md', 'ea61050d5d95fa2978bb33a093331a9e1e44ad11fe3af7241c4366f5685f58aa'),
    'old_validator': (OLD / 'validate_index.py', VALIDATOR_SHA),
    'original_baseline': (OLD / 'baseline-index.json', 'fcc7eef21ad67f61bfe46c8cd9a326974c19979ac0a838cc386680c144ed9d61'),
    'original_inputs': (OLD / 'inputs.json', 'f2458dd600accc1234c58738de11525b433cd55017e56f55295a2fee01b17fe8'),
    'original_protocol': (OLD / 'PROTOCOL.md', 'fbfc63b9c4559d2b7e99cf0daeb67db4f078322a74f2080da5cad2b2af78b888'),
}
CLAIMS = (
    'Q03-DistantView-selected-corner-coverage',
    'Q03-DistantView-contour-correspondence',
    'Q10-DistantView-localization-pilot-pending',
    'Q03-DistantView-PTS-type-association',
    'Q10-DistantView-generated-clock-limit',
)
UNITS = {
    'source-screen': (CLAIMS[:1], 'T-DistantView-source-screen'),
    'contour-correspondence': (CLAIMS[1:2], 'T-DistantView-contour-correspondence'),
    'localization-packet': (CLAIMS[2:3], 'T-DistantView-localization-packet'),
    'encoded-timing': (CLAIMS[3:], 'T-DistantView-encoded-timing'),
}
FAMILIES = {'F-DistantView-access-copy', 'F-FFmpeg-tagged-source'}
PARENTS = {'Q03': 'Q03-observed-sequence', 'Q10': 'Q10-tool-and-record-limits'}
LIMIT_FLAGS = {'human_acceptance_supplied', 'expert_acceptance_supplied',
               'cause_ranking_changed', 'canonical_promotion', 'new_measurement'}
REGISTRIES = ('artifacts', 'families', 'transforms', 'claim_links')
ARTIFACT_FIELDS = ('input_artifacts', 'code_artifacts', 'output_artifacts', 'verification_artifacts')
LIMIT = ('Exact declared additions, prior-data preservation, reference reachability and selected pins only; '
         'not semantic support, inherited-test reruns, independent origins, source authenticity, '
         'human/expert acceptance, historical timing or cause ranking.')


def bootstrap_bytes(path, expected_sha=None):
    """Minimal pre-import guard; subsequent checks reuse the pinned old helpers."""
    path = Path(path)
    if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
        raise ValueError(f'missing/non-file/symlink control: {path}')
    before = path.stat()
    data = path.read_bytes()
    after = path.stat()
    fields = ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    if any(getattr(before, k) != getattr(after, k) for k in fields):
        raise ValueError(f'control changed while reading: {path}')
    digest = hashlib.sha256(data).hexdigest()
    if expected_sha is not None and digest != expected_sha:
        raise ValueError(f'hard-pinned control changed: {path}')
    return data, {'bytes': len(data), 'sha256': digest}


def load_validator():
    """Import only exact pinned code; no pycache or old CLI execution."""
    path = FIXED['old_validator'][0]
    data, _ = bootstrap_bytes(path, VALIDATOR_SHA)
    module = types.ModuleType('pinned_v1_index_validator')
    module.__file__ = str(path)
    exec(compile(data, str(path), 'exec'), module.__dict__)
    return module


def keys(v, value, required, where, optional=()):
    v.obj(value, where)
    v.require(set(required) <= set(value) <= set(required) | set(optional),
              f'{where}: missing or undeclared keys')


def pin_shape(v, row, where):
    keys(v, row, {'path', 'bytes', 'sha256'}, where)
    v.string(row['path'], where + '.path')
    v.require(type(row['bytes']) is int and row['bytes'] >= 0, where + ': invalid bytes')
    v.require(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}', row['sha256']),
              where + ': invalid sha256')


def shape_additions(v, additions):
    keys(v, additions, {*REGISTRIES, 'additional_claims'}, 'additions')
    for field in REGISTRIES:
        v.obj(additions[field], field)
    for row in additions['artifacts'].values():
        keys(v, row, {'path', 'bytes', 'sha256', 'role'}, 'artifact')
        pin_shape(v, {k: row[k] for k in ('path', 'bytes', 'sha256')}, 'artifact pin')
        v.string(row['role'], 'artifact role')
    for row in additions['families'].values():
        keys(v, row, {'description', 'basis', 'independence_limit', 'origin_status'}, 'family')
        for basis in v.seq(row['basis'], 'family basis'):
            keys(v, basis, {'artifact_id', 'locator'}, 'family basis row')
    for row in additions['transforms'].values():
        keys(v, row, {*ARTIFACT_FIELDS, 'status', 'missing', 'limit'}, 'transform')
    for row in v.seq(additions['additional_claims'], 'additional_claims'):
        keys(v, row, {'id', 'parent_claim', 'claim', 'layer', 'grade', 'ceiling',
                      'alternative', 'would_change_with'}, 'additional claim')
    for row in additions['claim_links'].values():
        keys(v, row, {'question', *v.EDGE_FIELDS, 'verification_status', 'remaining_gap', 'absences'}, 'claim link')
        for item in v.seq(row['work_packages'], 'work_packages'):
            keys(v, item, {'id', 'role'}, 'WP edge')
        for field in ('dependencies', 'causal_links'):
            for item in v.seq(row[field], field):
                keys(v, item, {'id', 'relation', 'scope', 'basis'}, field + ' edge')
        v.require(row['causal_links'] == [], 'new units establish no mechanical transition')
        absence = v.obj(row['absences'], 'absences')
        for item in absence.values():
            keys(v, item, {'kind', 'reason', 'consequence'}, 'absence')
        v.require(absence.get('causal_links', {}).get('kind') == 'not_applicable',
                  'causal links require explicit nonapplicability')
        for item in v.seq(row['evidence'], 'evidence'):
            keys(v, item, {'artifact_id', 'locator', 'role', 'family_id'}, 'evidence', {'basis'})
        keys(v, row['verification_status'], {'source_inspection', 'calculation_reproduction',
                                             'human_acceptance', 'expert_review'}, 'verification_status')


def apply_extension(v, baseline, manifest, extension_pin):
    """Pure structure/preservation operation; filesystem authority is checked outside."""
    keys(v, manifest, {'version', 'controls', 'root_updates', 'additions', 'revision'}, 'manifest')
    v.require(type(manifest['version']) is int and manifest['version'] == 1, 'manifest version must be integer 1')
    keys(v, manifest['controls'], {'baseline', 'protocol', 'old_validator'}, 'controls')
    for name, row in manifest['controls'].items():
        pin_shape(v, row, 'controls.' + name)
    pin_shape(v, extension_pin, 'extension pin')
    updates = manifest['root_updates']
    keys(v, updates, v.MUTABLE, 'root_updates')
    v.require(type(updates['version']) is int and updates['version'] == 3, 'root version must be integer 3')
    for field in v.MUTABLE - {'version'}:
        v.string(updates[field], 'root_updates.' + field)
    prior = v.obj(baseline.get('integration'), 'baseline integration')
    v.require(type(baseline.get('version')) is int and baseline['version'] == 2, 'expected v2 baseline')
    for field, count in (('artifacts', 207), ('families', 19), ('transforms', 23), ('claim_links', 58),
                         ('additional_claims', 18)):
        v.require(len(prior[field]) == count, 'wrong baseline ' + field + ' count')
    v.require('distant_view_revision' not in prior, 'revision already exists')
    additions = manifest['additions']
    shape_additions(v, additions)
    claim_ids = [v.string(r['id'], 'new claim ID') for r in additions['additional_claims']]
    v.require(len(claim_ids) == 5 and set(claim_ids) == set(CLAIMS), 'exact five new claims required')
    v.require(set(additions['claim_links']) == set(CLAIMS), 'exact five new claim links required')
    v.require(set(additions['families']) == FAMILIES, 'exact two new families required')
    v.require(set(additions['transforms']) == {t for _, t in UNITS.values()}, 'exact four new transforms required')
    for field in REGISTRIES:
        v.require(not (set(prior[field]) & set(additions[field])), field + ': ID collision')
    for row in additions['additional_claims']:
        parent = PARENTS[row['id'][:3]]
        v.require(row['id'] not in prior['claim_links'] and row['parent_claim'] == parent, 'claim collision/wrong parent')
        v.require(additions['claim_links'][row['id']]['question'] == row['id'][:3], 'wrong question')
    revision = manifest['revision']
    keys(v, revision, {'date', 'units', 'status_supplements', 'limits', 'scope'}, 'revision')
    v.require(revision['date'] == updates['date'], 'revision/root dates differ')
    v.string(revision['scope'], 'revision.scope')
    keys(v, revision['limits'], LIMIT_FLAGS, 'revision.limits')
    v.require(all(value is False for value in revision['limits'].values()), 'acceptance/ranking/measurement flags must remain false')
    units = v.seq(revision['units'], 'units')
    v.require(len(units) == 4, 'exact four units required')
    seen = set()
    for row in units:
        keys(v, row, {'id', 'claim_ids', 'transform_ids'}, 'unit')
        uid = v.string(row['id'], 'unit ID')
        v.require(uid in UNITS and uid not in seen, 'unknown or duplicate unit')
        seen.add(uid)
        cids, tid = UNITS[uid]
        v.require(set(v.strings(row['claim_ids'], 'unit claims', True)) == set(cids), 'wrong unit claim coverage')
        v.require(v.strings(row['transform_ids'], 'unit transforms', True) == [tid], 'wrong unit transform coverage')
        for cid in cids:
            v.require(tid in additions['claim_links'][cid]['transforms'], 'unit transform not reachable from claim')
    statuses = revision['status_supplements']
    keys(v, statuses, set(PARENTS.values()), 'status_supplements')
    for parent, row in statuses.items():
        keys(v, row, {'disposition', 'supporting_claim_ids', 'limit'}, 'status supplement')
        for field in ('disposition', 'limit'):
            v.string(row[field], 'status supplement.' + field)
        ids = v.strings(row['supporting_claim_ids'], 'supporting_claim_ids', True)
        v.require(bool(ids) and all(cid in CLAIMS and PARENTS[cid[:3]] == parent for cid in ids),
                  'wrong status supplement support')
    result = copy.deepcopy(baseline)
    result.update(copy.deepcopy(updates))
    integration = result['integration']
    for field in REGISTRIES:
        integration[field].update(copy.deepcopy(additions[field]))
    integration['additional_claims'].extend(copy.deepcopy(additions['additional_claims']))
    integration['distant_view_revision'] = {**copy.deepcopy(revision),
                                           'extension': copy.deepcopy(extension_pin),
                                           'protocol': copy.deepcopy(manifest['controls']['protocol']),
                                           'baseline': copy.deepcopy(manifest['controls']['baseline'])}
    reachable = {e['artifact_id'] for row in additions['claim_links'].values() for e in row['evidence']}
    used_transforms = {t for row in additions['claim_links'].values() for t in row['transforms']}
    for tid in used_transforms:
        v.require(tid in integration['transforms'], 'unknown transform')
        for field in ARTIFACT_FIELDS:
            reachable.update(integration['transforms'][tid][field])
    v.require(set(additions['artifacts']) <= reachable, 'new artifact unreachable from new claims/transforms')
    return result


def assert_candidate(v, candidate, expected):
    v.require(v.encoded(candidate) == v.encoded(expected), 'candidate differs from exact frozen extension of v2')


def unique_artifact_paths(v, candidate, base, roots):
    seen = {}
    for aid, row in candidate['integration']['artifacts'].items():
        path = v.resolve_file(row['path'], base, roots)
        v.require(path not in seen, f'duplicate resolved artifact path: {aid} and {seen.get(path)}')
        seen[path] = aid


def prepare():
    if not re.fullmatch('[0-9a-f]{64}', EXTENSION_SHA):
        raise ValueError('extension hash is PENDING_ROOT_FROZEN_REVIEW; no candidate build/check authorized')
    controls = {**FIXED, 'extension': (HERE / 'extension.json', EXTENSION_SHA)}
    before = {str(p): bootstrap_bytes(p, digest)[1] for p, digest in controls.values()}
    for path in (HERE / 'extend_index.py', HERE / 'test_extend_index.py'):
        before[str(path)] = bootstrap_bytes(path)[1]
    # All hard controls were checked before either importing code or loading JSON.
    v = load_validator()
    manifest = v.load_json(HERE / 'extension.json')
    keys(v, manifest.get('controls'), {'baseline', 'protocol', 'old_validator'}, 'controls')
    for name, row in manifest['controls'].items():
        pin_shape(v, row, 'controls.' + name)
        v.require(v.check_pin(row, BASE, v.APPROVED_ROOTS) == FIXED[name][0], 'wrong control path: ' + name)
    baseline = v.load_json(FIXED['baseline'][0])
    extension_pin = {'path': str((HERE / 'extension.json').relative_to(BASE)),
                     **before[str(HERE / 'extension.json')]}
    expected = apply_extension(v, baseline, manifest, extension_pin)
    return v, expected, before


def unchanged(v, before):
    for path, state in before.items():
        current = v.resolve_file(path, BASE, v.APPROVED_ROOTS)
        v.require(v.encoded(v.file_state(current)) == v.encoded(state), 'control/candidate changed: ' + path)


def check_prepared(v, candidate_path, expected, before):
    """Bracket exact comparison AND the old validator with unchanged control checks."""
    path = v.resolve_file(str(candidate_path), BASE, v.APPROVED_ROOTS)
    tracked = {**before, str(path): v.file_state(path)}
    try:
        unchanged(v, before)
        candidate = v.load_json(path)
        assert_candidate(v, candidate, expected)
        unique_artifact_paths(v, candidate, BASE, v.APPROVED_ROOTS)
        # Original v1 controls and no hash/root overrides: old checker is unchanged.
        result = v.validate(path, FIXED['original_baseline'][0], FIXED['original_inputs'][0])
        v.require((result['claim_links'], result['additional_claims'], result['families'], result['transforms'])
                  == (63, 23, 21, 27), 'final roster counts differ')
    finally:
        unchanged(v, tracked)
    return {'status': 'pass', 'candidate_sha256': tracked[str(path)]['sha256'],
            'v2_preservation': 'exact_plus_frozen_extension', 'legacy_validation': result, 'limit': LIMIT}


def write_exclusive(v, expected, name, directory=HERE):
    v.require(name in ('candidate01.json', 'candidate02.json'), 'only literal candidate01.json/candidate02.json')
    directory = Path(directory)
    v.require(directory.is_dir() and not any(p.is_symlink() for p in (directory, *directory.parents)),
              'invalid/symlink output directory')
    path = directory / name
    payload = (json.dumps(expected, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
    with path.open('xb') as handle:
        handle.write(payload)
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('check').add_argument('--index', type=Path, required=True)
    commands.add_parser('build').add_argument('--out', choices=('candidate01.json', 'candidate02.json'), required=True)
    args = parser.parse_args(argv)
    try:
        v, expected, before = prepare()
        path = write_exclusive(v, expected, args.out) if args.command == 'build' else args.index.absolute()
        result = check_prepared(v, path, expected, before)
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({'status': 'fail', 'error': str(exc), 'limit': LIMIT}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
