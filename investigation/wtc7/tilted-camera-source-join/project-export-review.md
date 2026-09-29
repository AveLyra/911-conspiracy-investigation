# Complete Tilted Camera saved-project export

2026-09-19. Research derivative under `PROTOCOL.md` and the investigation
`CHARTER.md`; no source promotion, historical-input finding, physical calibration,
new annotation, table comparison, acceleration calculation or causal inference.
Prepared by a separate computational source-export agent, not an outside expert.

## Result and scope

The byte-pinned TRK contains eight PointMass objects and **334 saved coordinate
rows**. All 334 exported rows contain finite x/y doubles. Each object's rows form
a contiguous six-index sequence within its own reported endpoints. No duplicate
frame indices, duplicated x/y properties, missing coordinates, rows outside the
saved video domain, or rows outside the literal saved clip-step domain were
found. The two freshly produced exports are byte-identical.

The selected project contains 10 track collection items: CoordAxes, TapeMeasure,
then eight PointMass objects. Each PointMass has exactly two direct arrays,
`framedata` and `keyFrames`; both were completely exported. Array selection did
not use the paper's values, observed motion or a fitted time range.

| Stable ID | Safe source label, if exported | Saved rows | Saved index range, increment 6 | Key-frame entries | Missing positions among 80 literal clip steps |
|---|---|---:|---|---:|---:|
| pointmass01 | NW Corner | 75 | 0–444 | 75 | 5 |
| pointmass02 | Withheld; name hash retained | 80 | 0–474 | 80 | 0 |
| pointmass03 | Mid E Penthouse | 16 | 18–108 | 16 | 64 |
| pointmass04 | Withheld; name hash retained | 30 | 144–318 | 30 | 50 |
| pointmass05 | Withheld; name hash retained | 43 | 150–402 | 8 | 37 |
| pointmass06 | NE Corner | 16 | 252–342 | 16 | 64 |
| pointmass07 | W Penthouse | 34 | 150–348 | 34 | 46 |
| pointmass08 | Withheld; name hash retained | 40 | 210–444 | 40 | 40 |

`pointmass05` has key-frame entries at 360, 366, 372, 378, 384, 390, 396 and 402.
Its 35 saved rows at 150–354 lack key-frame membership. The seven other objects'
key-frame lists equal their saved-row lists. No duplicate keys or keys lacking a
saved row were found. **Stored numeric presence is not a finding that every row
is an independent human measurement.** Key-frame membership likewise does not
identify a human rather than automated marker. The software-semantics review is
the separate authority for interpreting the loader and interpolation behavior.

Only four plainly structural labels were added to an exact allowlist after an
in-memory classification. The remaining labels stay anonymous with hashes;
they are not classified as private, wrong or irrelevant. The ordinal IDs are
the stable join keys. No label has been equated to a paper point or independently
verified building feature by this export.

## Saved settings and missing states

The numeric export records the owning object class, property name, literal text,
numeric value, occurrence count/status and an unambiguous positional XML path.
Coordinates retain each row's original index, ordinal, x/y field occurrences,
finite-state result and saved key-frame membership. It retains missing video
frame indices, missing clip-step indices, duplicate indices, out-of-domain
indices, unknown/missing arrays and scalar occurrence states explicitly.

The literal settings include:

- `VideoClip`: `video_framecount=476`, `startframe=0`, `stepsize=6`,
  `stepcount=80`, `starttime=-2020.0`, `playallsteps=true`.
- `StepperClipControl`: `rate=1.0`, `delta_t=33.36666666666667`, `frame=258`.
- `ImageCoordSystem`: fixed origin, angle and scale are all `true`; locked is
  `false`. Its one frame-data object is at index 0, with `xorigin=470.25`,
  `yorigin=349.0`, `angle=-2.5913472025433153`, and both scales
  `1.4841091539439202`.
- The TapeMeasure's one saved endpoint row has `x1=444.9122807017544`,
  `y1=185.82456140350877`, `x2=441.3701657458563`, `y2=272.2651933701657`;
  its indexed world-length value is `58.293`. The saved panel length-unit string
  is `m`. An assigned length is not an independently validated dimension.
- The saved semantic-version string is `6.1.2`; it is not an execution record.

Full XML name/class searches found **zero candidates** for filters,
referenceframes, time-source/DataTrack nodes, or autofill/dependent property
names. The XuggleVideo object contains only its path field, which was not
exported. These are statements about literal saved presence. They do not clear
software defaults, encoded/baked transformations, omitted state, prior editing,
historical camera calibration, or the actual clip's timestamp interpretation.
No angle, clock or scale conversion was performed here.

The export intentionally omits author paths, arbitrary strings, descriptive
metadata, contact data, UI plots, fit descriptions and display-color contents.
Unknown source names/types are hashed rather than echoed. Each numeric field
requested by the allowlist has an explicit missing/present/duplicate state;
missing optional settings have not been replaced with defaults. No raw XML was
printed, saved or executed. The public archive and all prior work remained
unchanged.

## Integrity and reproducibility

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Parent WTC-911-Motion-Lab ZIP | 172774879 | `c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189` |
| Named Tilted Camera TRZ | 15608229 | `7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552` |
| TRK, zero-based nested entry 4 | 161200 | `babf332bd340c1e902870f14d4370eab4f3a54de388ce06c1ca85ae222b1b5da` |
| project-export.py | 20921 | `872d37a02cbbad8c8e80e2f40068e0f8e0606411c4494173bf7f3c9f24b36181` |
| project-export-tests.py | 10343 | `62f72f9566a3b606d22b7e52ef2d44ee9020dcc5058933bd0edcecf9e655c4e1` |
| project01.json | 1078537 | `4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8` |
| project02.json | 1078537 | `4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8` |

The loader pins parent, named TRZ and TRK bytes, checks source stability, reads
only the named nested TRK in memory, and writes to two fixed safe output names
with exclusive creation. Archive paths are never filesystem destinations.
Traversal, absolute/Windows paths, symlinks, encryption flags and size violations
are rejected. UTF-8 and XML envelope/root guards reject DTD/entity declarations,
NUL/UTF-16 payloads, malformed XML and an unexpected root class. Numeric invalid,
nonfinite, duplicate and missing states are retained without a usable value.

Commands actually run from the investigation worktree:

```sh
python3 research/sherlock-wtc7-investigation/tilted-camera-source-join/project-export-tests.py
python3 research/sherlock-wtc7-investigation/tilted-camera-source-join/project-export.py --out project01.json
python3 research/sherlock-wtc7-investigation/tilted-camera-source-join/project-export.py --out project02.json
```

Python 3.12.14. The **17 synthetic tests passed**, initially in 0.011 s and on
the final repeated run in 0.010 s. They cover sparse rows and missing clip steps,
duplicate rows/coordinates/arrays/keys, missing coordinates/arrays/keys,
nonfinite and arbitrary values, unexpected row/root schema, invalid indices,
DTD/entity/UTF-16/malformed XML, ordinal locators, special-state visibility,
label and metadata suppression, unsafe archive/output paths, and determinism.
No browser check applies to this inert non-UI exporter.

Both exports succeeded under worktree-scoped write approval. A fresh read-only
oracle, using direct XML traversal rather than the export parser, then checked
1,469 locators, 742 saved lexical values, all 668 x/y coordinate scalars, all
eight complete arrays and key lists, label hashes, source pins, producer/test
hashes and byte equality. **It passed**. This is a second implementation check
by the same computational agent, not an independent human replication.

Positional XML paths use XPath element-child positions, with `/*[1]` as the
root; all brackets are one-based. A primitive serialized array records both
its container `xml_path` and its lexical child's `serialized_xml_path`. For
example, the tape world-length scalar is
`/*[1]/*[13]/*[2]/*[1]/*[11]/*[1]`. The primitive keyFrames literal must be read
at `serialized_xml_path`, not at the parent array's `xml_path`.

## Preserved failed attempts and corrections

1. The first exploratory command interpreted the protocol's original "ordinal
   4" as a one-based ordinal and accessed zero-based entry 3. It read that
   entry's bytes in memory, then **failed the expected TRK size/hash assertion**.
   That entry was the duplicate MP4. No decode, XML parse, saved media, source
   mutation or output file occurred. The parent clarified the protocol to
   explicit **zero-based** entry indices before the successful exporter ran.
   The exporter now validates size and the exact name hash before reading the
   fifth entry.
2. The first normal-sandbox `project01.json` command returned exit 1 with
   `source_or_output_operation_failed`. No output was created. The same command
   succeeded under narrowly scoped permission to write that named file in the
   dedicated investigation worktree. Main was not used as a workaround.
3. A read-only summary command had an unmatched dictionary brace and failed
   with a `SyntaxError` before execution. Correcting the brace produced the
   coverage summary; neither export changed.
4. The first direct-XML oracle incorrectly used the parent array's `xml_path`
   for a serialized keyFrames literal, and its lexical equality assertion
   failed. The schema already supplied `serialized_xml_path`; the corrected
   oracle used it and passed. No output was regenerated or silently repaired.
5. An intentional third command targeting the existing `project01.json`
   returned exit 1 with `output_already_exists`. Exclusive output preservation
   therefore worked; the existing export's hash remained unchanged.

## Claim ceilings and next discriminator

**A, directly established within inspected bytes:** the selected source's
saved-array counts, numeric presence, index/key-frame differences and literal
settings, supported by source pins and a complete direct-source equality check.
**A, derived within the declared saved domain:** missing index lists and repeat
byte equality. These grades say nothing about measurement accuracy.

The strongest alternative to treating 334 rows as 334 independent observations
is that saved rows contain generated, interpolated, copied, edited or otherwise
dependent positions. The 35-row/key-frame discrepancy is a concrete reason to
preserve that distinction; it does not by itself select one explanation.
The absence of saved filters is compatible with a previously transformed video.

Historical paper correspondence, physical units/calibration, source-media clock
choice, source identity and building-feature identity remain unresolved by this
subtask. The next discriminator is a separately declared, source-semantics-based
row comparison, combined with root's independent media correspondence work.
Matching numbers later would still require a provenance argument to establish
the paper's historical inputs.

## Direct-XML verification command

This is the successful final oracle, retained here so it can be repeated
without adding a second exporter or changing the preserved products:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib,io,json,re,xml.etree.ElementTree as ET,zipfile,collections
base=Path('research/sherlock-wtc7-investigation/tilted-camera-source-join')
one=(base/'project01.json').read_bytes();two=(base/'project02.json').read_bytes();assert one==two
export=json.loads(one)
raw=Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip').read_bytes();assert hashlib.sha256(raw).hexdigest()=='c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189'
with zipfile.ZipFile(io.BytesIO(raw)) as archive:
 member=[q for q in archive.infolist() if q.filename=='The Kit/WTC7-Tilted Camera/WTC7TiltedCamera.trz'];assert len(member)==1;nested=archive.read(member[0])
assert hashlib.sha256(nested).hexdigest()=='7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552'
with zipfile.ZipFile(io.BytesIO(nested)) as archive:
 info=archive.infolist()[4];assert info.file_size==161200;xml=archive.read(info)
assert hashlib.sha256(xml).hexdigest()=='babf332bd340c1e902870f14d4370eab4f3a54de388ce06c1ca85ae222b1b5da'
root=ET.fromstring(xml)
def locate(path):
 indices=[int(i) for i in re.findall(r'\[(\d+)\]',path)];assert indices[0]==1;node=root
 for i in indices[1:]:node=list(node)[i-1]
 return node
counts=collections.Counter()
def check(value):
 if isinstance(value,dict):
  if 'xml_path' in value:
   node=locate(value.get('serialized_xml_path',value['xml_path']));counts['locators']+=1
   if 'saved_text' in value:
    assert node.text.strip()==value['saved_text'];counts['saved_lexical_values']+=1
   if 'text_sha256' in value:
    assert hashlib.sha256((node.text or '').strip().encode()).hexdigest()==value['text_sha256']
  for v in value.values():check(v)
 elif isinstance(value,list):
  for v in value:check(v)
check(export)
mass='org.opensourcephysics.cabrillo.tracker.PointMass'
objects=[o for o in root.findall("./property[@name='tracks']/property/object") if o.get('class')==mass]
assert len(objects)==len(export['pointmass_tracks'])==8
for obj,track in zip(objects,export['pointmass_tracks']):
 arr=obj.findall("./property[@name='framedata']");assert len(arr)==len(track['framedata'])==1
 rawrows=list(arr[0]);rows=track['framedata'][0]['rows'];assert len(rawrows)==len(rows)
 assert [int(q.get('name')[1:-1]) for q in rawrows]==track['saved_indices']
 for rawrow,row in zip(rawrows,rows):
  for axis in ['x','y']:
   original=rawrow.find("./object/property[@name='"+axis+"']");f=row['objects'][0]['coordinates'][axis]
   assert f['status']=='present' and len(f['occurrences'])==1
   assert f['occurrences'][0]['saved_text']==original.text
   assert f['occurrences'][0]['value']==float(original.text);counts['coordinates']+=1
 name=obj.find("./property[@name='name']").text
 assert track['names'][0]['source_name']['sha256']==hashlib.sha256(name.encode()).hexdigest()
 assert len(obj.findall("./property[@type='array']"))==2
 keys=obj.find("./property[@name='keyFrames']/property").text
 assert [int(v) for v in keys[1:-1].split(',')]==track['keyFrames'][0]['values']
for item in export['settings_objects']:
 for f in item['fields'].values():
  for value in f['occurrences']:
   assert value['status'] in ['valid_finite','valid_boolean']
for file,key in [('project-export.py','script'),('project-export-tests.py','tests')]:
 assert export['producer'][key]['sha256']==hashlib.sha256((base/file).read_bytes()).hexdigest()
print(json.dumps({'status':'pass_independent_direct_xml_locator_and_complete_point_array_check','checks':dict(counts),'identical_repeat_bytes':len(one),'sha256':hashlib.sha256(one).hexdigest(),'pointmass_count':len(objects),'point_rows':sum(len(t['saved_indices']) for t in export['pointmass_tracks'])},indent=2))
PY
```
