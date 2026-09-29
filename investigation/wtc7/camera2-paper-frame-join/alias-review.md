# Public-kit WTC7 alias metadata review

2026-09-19. Separate follow-up to [settings-review.md](settings-review.md), under [ADDENDUM-01.md](ADDENDUM-01.md). The original settings review remains unchanged at SHA-256 `ec4956a7b0f3c41f36da691cd626bd95a7f546caa93fc29694682576a52d111d`. This reviewer has viewed no new image or video, executed no saved project, inferred no historical time origin and calculated no trajectory. The metadata findings below were obtained before the subsequently declared thumbnail extraction; root's visual review is separate.

## Result and evidence boundary

Both named public-kit aliases contain real saved Tracker projects and embedded video copies. Their literal media references are `DistantViewWTC7.avi` and `TiltedCameraWTC7Clip.mp4`. Neither embedded video's SHA-256 equals the held Camera2 converted MOV. That excludes identical file bytes; it does **not** exclude the same camera view, an excerpt, alternate encode or shared recorded-content lineage.

No inspected field affirmatively identifies either project as the 2023 paper's Camera2 analysis. The Dan Rather directory label is suggestive in light of the paper's p. 10 distinction between earlier Dan Rather footage and Camera2, but the label is not independent video identification. The Tilted Camera label remains unresolved from metadata. Both projects' six-frame steps are affirmative settings for those projects; they cannot silently supply the unrecovered Camera2 six-frame setting. A shared 58.293 m assigned tape in the Tilted and Camera3 examples is likewise no cross-view calibration.

## Exact coverage and record pins

The only parent read was `/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip`, 172,774,879 bytes, freshly verified SHA-256 `c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189`. Only the two named TRZ bodies were opened. Each nested archive has five entries. All ten entry bodies were read in memory for CRC/size/hash checking; only each `.trk` was parsed for the allowlisted metadata. HTML was not interpreted and thumbnails/video were not viewed or decoded. The [sanitized receipt](alias-receipt.json) contains every nested entry's ordinal, basename, size and hash, while omitting original paths and unrelated descriptive metadata.

| Parent member | Verified bytes | Verified SHA-256 |
|---|---:|---|
| `The Kit/WTC7-Dan Rather/DistantViewWTC7.trz` | 9,477,547 | `8afe02fa78440768ff01bf4cd7cdcd27cbe872466f46be80d79115708c381c0e` |
| `The Kit/WTC7-Tilted Camera/WTC7TiltedCamera.trz` | 15,608,229 | `7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552` |

Each nested archive has a thumbnail at entry 0, an info HTML at entry 1, equal-hash video copies at entries 2 and 3, and its TRK at entry 4. The repeated video is package duplication, not a second independent recording.

| Nested source, identified by alias and entry ordinal | Bytes | SHA-256 |
|---|---:|---|
| Dan Rather, 2 and 3: `DistantViewWTC7.avi` | 4,749,520 each | `a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e` |
| Dan Rather, 4: `DistantViewWTC7_DistantViewWTC7.trk` | 68,489 | `5aa2bea2b6532713bc9abae647e0486c937892a96d33a3892fc0f6109a11a693` |
| Tilted, 2 and 3: `TiltedCameraWTC7Clip.mp4` | 7,768,869 each | `393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f` |
| Tilted, 4: `WTC7TiltedCamera_TiltedCameraWTC7.trk` | 161,200 | `babf332bd340c1e902870f14d4370eab4f3a54de388ce06c1ca85ae222b1b5da` |

## Literal saved settings

Class names below are the XML classes; exact qualified classes/property/value triples are retained in the receipt. Both `TrackerPanel.semantic_version` fields are `6.1.2`, and both saved `length_unit` fields are `m`. Values are configuration data, not independently measured frames, exposure times or physical dimensions.

| Property | Dan Rather example | Tilted Camera example |
|---|---:|---:|
| `XuggleVideo.path`, basename only | `DistantViewWTC7.avi` | `TiltedCameraWTC7Clip.mp4` |
| `VideoClip.video_framecount` | 962 | 476 |
| `VideoClip.startframe` | 0 | 0 |
| `VideoClip.stepsize` | 6 | 6 |
| `VideoClip.stepcount` | 161 | 80 |
| `VideoClip.starttime` | 0.0 | -2020.0 |
| `StepperClipControl.delta_t` | 33.3667000333667 | 33.36666666666667 |
| `StepperClipControl.rate` | 1.0 | 1.0 |
| `StepperClipControl.frame` | 0 | 258 |
| `ImageCoordSystem$FrameData.xorigin` | 479.7266754270696 | 470.25 |
| `ImageCoordSystem$FrameData.yorigin` | 399.2641261498029 | 349.0 |
| `ImageCoordSystem$FrameData.angle` | -0.7742201649280619 | -2.5913472025433153 |
| `ImageCoordSystem$FrameData.xscale` and `yscale` | 1.9452779103716007 | 1.4841091539439202 |
| `TapeMeasure.worldlengths[0]` | 66.0654 | 58.293 |
| `TapeMeasure$FrameData.(x1,y1)` | (425.0,319.0) | (444.9122807017544,185.82456140350877) |
| `TapeMeasure$FrameData.(x2,y2)` | (427.0,190.49999999999966) | (441.3701657458563,272.2651933701657) |

`ImageCoordSystem.fixedorigin`, `fixedangle` and `fixedscale`, plus `TapeMeasure.fixedtape`, `fixedlength` and `stickmode`, are all `true` in both examples. The negative `starttime` is preserved literally; this unit does not map it to a visible event or the paper's clock. No track-point coordinates, fitting masks or unrelated project descriptions were exported.

## Verification and repeatability

The first metadata run passed exact parent/two-member hashes and all nested declared/actual size checks, using Python 3.12.14. A later read-only rerun produced byte-identical JSON stdout to the saved earlier read-only output and parsed identically to `alias-receipt.json` (the stored receipt is compact JSON, so its presentation whitespace differs from stdout). A distinct direct-class XPath selector then re-read the two original in-memory TRKs and checked **50 scalar fields, two worldlengths and two video basenames** against the recursive-allowlist receipt. It also rechecked the parent hash, both outer-member hashes and all ten nested hashes/sizes. Result: pass. This is a separate code route by the same reviewer using the same XML library, not an independent human, expert or parser implementation.

XML DTD/entity declarations were rejected; numeric/boolean/unit output was allowlisted. Archive data were bounded, read as bytes and never used as filesystem paths. Errors were summarized without emitting raw XML/author paths. The reader does not execute kit code. The exact scripts below make the checks reproducible without storing original XML or project data.

Execution issues were operational, not source failures: the first receipt save timed out during automatic permission review; a check confirmed no receipt existed, and one retry succeeded. The first thumbnail write failed `PermissionError`; the unchanged script then succeeded with scoped worktree permission. The source checks did not fail. No main file was used as a workaround.

## Separately declared thumbnail handoff

After the metadata result, the second-stage addendum was read before extraction at hash `5cb6e8c9dd32f244a0f98ea35dcefdc226976cf22b76d84d20bb34da1c1dec79` (the earlier metadata-stage addendum was `f4ead1ff06ddb1ae789da1a5c3a8ebecea774a17f4fee25ba7360836e063fda4`). Exactly the two existing entry-0 PNGs were copied unchanged to fixed sanitized destinations, with exclusive creation and a post-write hash check:

| Output | Bytes | SHA-256 |
|---|---:|---|
| `alias-dan-rather-thumbnail.png` | 50,862 | `a589732d45c779571b618086c92edb23fbbb37e9393bc19f021dc785fb3cbe57` |
| `alias-tilted-camera-thumbnail.png` | 60,119 | `fff0d244ee5019886e722a68a64b9489967bef5d6ee9fb8a9d2eee856e9c054d` |

[thumbnail-receipt.json](thumbnail-receipt.json) retains parent/member/entry lineage. This reviewer did not inspect either image. Root's whole-thumbnail comparison to previously reviewed Camera2 images is the next separately authorized visual test. Even a convincing view match would not identify an exact native frame, demonstrate the project generated the paper's 2023 table, recover its fitting mask, authenticate its metric scale or establish its assigned zero's event meaning. A poor thumbnail may leave the view unresolved and must not be forced into an identification.

The next decision is therefore view correspondence, followed only where useful by a separately scoped project-to-paper/frame join. No source absence, invalid-measurement, gravity or causal finding follows from this metadata check.

## Reproducible scripts

Save each code block under its named script in a scratch directory and use the bundled Python path shown in the commands. These are the exact executed script contents; paths intentionally target the pinned parent and current unit. The thumbnail script refuses existing output files; a repeat extraction requires a separately chosen fresh destination, not overwriting the handoff images.

### inspect_aliases.py

```python
import hashlib, io, json, math, ntpath, platform, re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

PARENT = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip')
PARENT_SHA = 'c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189'
CAMERA2_SHA = '84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730'
SELECT = {
    'The Kit/WTC7-Dan Rather/DistantViewWTC7.trz': '8afe02fa78440768ff01bf4cd7cdcd27cbe872466f46be80d79115708c381c0e',
    'The Kit/WTC7-Tilted Camera/WTC7TiltedCamera.trz': '7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552',
}
MAX_BYTES = 128 * 1024 * 1024
NUMERIC = {'video_framecount', 'startframe', 'stepsize', 'stepcount', 'starttime', 'delta_t', 'frame', 'rate', 'xorigin', 'yorigin', 'angle', 'xscale', 'yscale', 'x1', 'y1', 'x2', 'y2'}
BOOL = {'fixedorigin', 'fixedangle', 'fixedscale', 'fixedtape', 'fixedlength', 'stickmode'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def basename(name):
    base = ntpath.basename(name.rstrip('/\\'))
    return base if re.fullmatch(r'[A-Za-z0-9 ._()\[\]-]{1,160}', base) else '[redacted nonconforming basename]'

def settings(data):
    if len(data) > 10 * 1024 * 1024 or b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise ValueError('XML outside bounded contract')
    root = ET.fromstring(data)
    scalars, videos, lengths = [], [], []
    def visit(element, objects, properties):
        objects = objects + ([element.get('class', '')] if element.tag == 'object' else [])
        if element.tag == 'property':
            name, value = element.get('name', ''), (element.text or '').strip()
            if name == 'path' and any(c.endswith('Video') for c in objects):
                videos.append({'video_class': objects[-1], 'basename': basename(value), 'original_path_omitted': True})
            if len(element) == 0:
                selected = name in NUMERIC | BOOL | {'semantic_version', 'length_unit'}
                if name in NUMERIC and (not re.fullmatch(r'[-+0-9.eE]+', value) or not math.isfinite(float(value))):
                    raise ValueError('Non-numeric selected scalar')
                if name in BOOL and value not in {'true', 'false'}:
                    raise ValueError('Invalid boolean scalar')
                if name == 'semantic_version' and not re.fullmatch(r'[0-9.]+', value):
                    raise ValueError('Non-numeric semantic version')
                if name == 'length_unit' and value not in {'m', 'cm', 'mm', 'ft', 'in', ''}:
                    raise ValueError('Unexpected unit')
                if selected:
                    scalars.append({'object_class': objects[-1] if objects else '', 'property': name, 'saved_text': value})
                if name.startswith('[') and properties and properties[-1] == 'worldlengths':
                    if not re.fullmatch(r'[-+0-9.eE]+', value) or not math.isfinite(float(value)):
                        raise ValueError('Invalid world length')
                    lengths.append({'object_class': objects[-1], 'property': 'worldlengths', 'index': name, 'saved_text': value})
            properties = properties + [name]
        for child in element:
            visit(child, objects, properties)
    visit(root, [], [])
    return {'video_references': videos, 'selected_scalars': scalars, 'worldlengths': lengths}

def bounded_read(archive, info):
    if info.flag_bits & 1 or info.file_size > MAX_BYTES or info.file_size / max(1, info.compress_size) > 500:
        raise ValueError('Bounded archive contract failed')
    with archive.open(info) as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) != info.file_size:
        raise ValueError('Declared and actual size mismatch')
    return data

def run():
    with PARENT.open('rb') as handle:
        parent_sha = hashlib.file_digest(handle, 'sha256').hexdigest()
    if parent_sha != PARENT_SHA:
        raise ValueError('Parent hash mismatch')
    receipt = {'parent_sha256': parent_sha, 'parent_bytes': PARENT.stat().st_size, 'camera2_comparison_sha256': CAMERA2_SHA, 'python': platform.python_version(), 'scope': 'Two named nested archives only; memory reads and XML metadata; no extraction, decode, preview, project execution or raw author-path output.', 'aliases': []}
    with zipfile.ZipFile(PARENT) as outer:
        for selected, expected in SELECT.items():
            matches = [i for i in outer.infolist() if i.filename == selected]
            if len(matches) != 1:
                raise ValueError('Missing or duplicate selected member')
            data = bounded_read(outer, matches[0])
            if sha(data) != expected:
                raise ValueError('Selected member hash mismatch')
            result = {'outer_member': selected, 'bytes': len(data), 'sha256': sha(data), 'entries': []}
            with zipfile.ZipFile(io.BytesIO(data)) as inner:
                infos = inner.infolist()
                if len(infos) > 1000 or sum(i.file_size for i in infos) > MAX_BYTES:
                    raise ValueError('Nested inventory exceeds bound')
                for index, info in enumerate(infos):
                    content = bounded_read(inner, info)
                    entry = {'entry_index': index, 'basename': basename(info.filename), 'original_path_omitted': True, 'declared_bytes': info.file_size, 'actual_bytes': len(content), 'sha256': sha(content), 'directory': info.is_dir()}
                    suffix = ntpath.splitext(info.filename)[1].lower()
                    if suffix in {'.mp4', '.wmv', '.avi', '.mov'}:
                        entry['same_bytes_as_held_camera2_mov'] = sha(content) == CAMERA2_SHA
                    if suffix == '.trk':
                        entry['settings'] = settings(content)
                    result['entries'].append(entry)
            receipt['aliases'].append(result)
    print(json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False))

if __name__ == '__main__':
    try:
        run()
    except Exception as error:
        print('Bounded alias inspection failed: ' + type(error).__name__, file=sys.stderr)
        sys.exit(1)
```

### check_alias_fields.py

```python
import collections, hashlib, io, json, ntpath, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

UNIT = Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera2-paper-frame-join')
PARENT = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip')
GROUPS = {
    'org.opensourcephysics.cabrillo.tracker.TrackerPanel': ['semantic_version', 'length_unit'],
    'org.opensourcephysics.media.core.VideoClip': ['video_framecount', 'startframe', 'stepsize', 'stepcount', 'starttime'],
    'org.opensourcephysics.media.core.StepperClipControl': ['rate', 'delta_t', 'frame'],
    'org.opensourcephysics.media.core.ImageCoordSystem': ['fixedorigin', 'fixedangle', 'fixedscale'],
    'org.opensourcephysics.media.core.ImageCoordSystem$FrameData': ['xorigin', 'yorigin', 'angle', 'xscale', 'yscale'],
    'org.opensourcephysics.cabrillo.tracker.TapeMeasure': ['fixedtape', 'fixedlength', 'stickmode'],
    'org.opensourcephysics.cabrillo.tracker.TapeMeasure$FrameData': ['x1', 'y1', 'x2', 'y2'],
}

def run():
    expected = json.loads((UNIT / 'alias-receipt.json').read_text())
    with PARENT.open('rb') as source:
        assert hashlib.file_digest(source, 'sha256').hexdigest() == expected['parent_sha256']
    counts = {'parent_hashes': 1, 'outer_hashes': 0, 'nested_hashes_and_sizes': 0, 'selected_scalar_fields': 0, 'worldlength_fields': 0, 'video_basename_fields': 0}
    with zipfile.ZipFile(PARENT) as outer:
        for alias in expected['aliases']:
            outer_bytes = outer.read(alias['outer_member'])
            assert hashlib.sha256(outer_bytes).hexdigest() == alias['sha256']
            counts['outer_hashes'] += 1
            with zipfile.ZipFile(io.BytesIO(outer_bytes)) as inner:
                infos = inner.infolist()
                assert len(infos) == len(alias['entries'])
                for row, info in zip(alias['entries'], infos):
                    content = inner.read(info)
                    assert hashlib.sha256(content).hexdigest() == row['sha256']
                    assert len(content) == row['actual_bytes'] == row['declared_bytes'] == info.file_size
                    counts['nested_hashes_and_sizes'] += 1
                    if 'settings' not in row:
                        continue
                    assert b'<!DOCTYPE' not in content.upper() and b'<!ENTITY' not in content.upper()
                    root = ET.fromstring(content)
                    actual = []
                    for cls, properties in GROUPS.items():
                        for obj in root.findall(".//object[@class='" + cls + "']") + ([root] if root.get('class') == cls else []):
                            for name in properties:
                                for prop in obj.findall("./property[@name='" + name + "']"):
                                    actual.append((cls, name, prop.text.strip()))
                    wanted = [(r['object_class'], r['property'], r['saved_text']) for r in row['settings']['selected_scalars']]
                    assert collections.Counter(actual) == collections.Counter(wanted)
                    counts['selected_scalar_fields'] += len(wanted)
                    tapes = root.findall(".//object[@class='org.opensourcephysics.cabrillo.tracker.TapeMeasure']")
                    values = [(p.get('name'), p.text.strip()) for obj in tapes for p in obj.findall("./property[@name='worldlengths']/property")]
                    assert values == [(r['index'], r['saved_text']) for r in row['settings']['worldlengths']]
                    counts['worldlength_fields'] += len(values)
                    refs = root.findall(".//object[@class='org.opensourcephysics.media.xuggle.XuggleVideo']/property[@name='path']")
                    names = [ntpath.basename(p.text.strip()) for p in refs]
                    assert names == [r['basename'] for r in row['settings']['video_references']]
                    counts['video_basename_fields'] += len(names)
    print(json.dumps({'result': 'pass', 'method': 'Direct class-specific XPath selection and multiset comparison; distinct from recursive scalar allowlist; same reviewer and XML parser.', 'checks': counts}, sort_keys=True))

if __name__ == '__main__':
    try:
        run()
    except Exception as error:
        print('Alias field comparison failed: ' + type(error).__name__, file=sys.stderr)
        sys.exit(1)
```

### extract_alias_thumbnails.py

```python
import hashlib, io, json, ntpath, sys, zipfile
from pathlib import Path

PARENT = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip')
DEST = Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera2-paper-frame-join')
PARENT_SHA = 'c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189'
SELECTION = [
    ('The Kit/WTC7-Dan Rather/DistantViewWTC7.trz', '8afe02fa78440768ff01bf4cd7cdcd27cbe872466f46be80d79115708c381c0e', 'DistantViewWTC7_thumbnail.png', 'a589732d45c779571b618086c92edb23fbbb37e9393bc19f021dc785fb3cbe57', 'alias-dan-rather-thumbnail.png'),
    ('The Kit/WTC7-Tilted Camera/WTC7TiltedCamera.trz', '7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552', 'WTC7TiltedCamera_thumbnail.png', 'fff0d244ee5019886e722a68a64b9489967bef5d6ee9fb8a9d2eee856e9c054d', 'alias-tilted-camera-thumbnail.png'),
]

def run():
    with PARENT.open('rb') as handle:
        assert hashlib.file_digest(handle, 'sha256').hexdigest() == PARENT_SHA
    prepared = []
    with zipfile.ZipFile(PARENT) as outer:
        for member, member_hash, thumb, thumb_hash, output in SELECTION:
            data = outer.read(member)
            assert hashlib.sha256(data).hexdigest() == member_hash
            with zipfile.ZipFile(io.BytesIO(data)) as inner:
                matched = [(i, info) for i, info in enumerate(inner.infolist()) if ntpath.basename(info.filename) == thumb]
                assert len(matched) == 1
                index, info = matched[0]
                assert info.file_size < 1024 * 1024 and not info.flag_bits & 1
                content = inner.read(info)
                assert len(content) == info.file_size
                assert hashlib.sha256(content).hexdigest() == thumb_hash
                assert not (DEST / output).exists()
                prepared.append((output, content, {'outer_member': member, 'outer_member_sha256': member_hash, 'nested_entry_index': index, 'nested_basename': thumb, 'original_path_omitted': True, 'output_basename': output, 'bytes': len(content), 'sha256': thumb_hash}))
    rows = []
    for output, content, row in prepared:
        with (DEST / output).open('xb') as handle:
            handle.write(content)
        with (DEST / output).open('rb') as handle:
            assert hashlib.file_digest(handle, 'sha256').hexdigest() == row['sha256']
        rows.append(row)
    print(json.dumps({'parent_sha256': PARENT_SHA, 'scope': 'Only two existing PNG thumbnails copied to fixed sanitized paths; no image viewing, resizing, enhancement, video decode or project execution.', 'thumbnails': rows}, indent=2, sort_keys=True))

if __name__ == '__main__':
    try:
        run()
    except Exception as error:
        print('Bounded thumbnail extraction failed: ' + type(error).__name__, file=sys.stderr)
        sys.exit(1)
```

Actual run commands (metadata stdout was captured by the orchestration tool and saved through a structured patch):

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /private/tmp/wtc7-camera2-settings-cFee5g/inspect_aliases.py
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /private/tmp/wtc7-camera2-settings-cFee5g/check_alias_fields.py
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /private/tmp/wtc7-camera2-settings-cFee5g/extract_alias_thumbnails.py
```
