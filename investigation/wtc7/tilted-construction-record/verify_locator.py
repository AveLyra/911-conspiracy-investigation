#!/usr/bin/env python3
"""Independent DOM oracle for the declared hash-only metadata locator.

No producer/helper import. No source reads on import. Historical CLI remains
subject to the external code/synthetic/source-admission gate.
"""
from collections import Counter
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import platform
import re
import stat
import sys
from xml.dom import Node, minidom
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip')
PARENT_SHA = 'c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189'
NESTED_SHA = '7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552'
PROJECT_SHA = 'babf332bd340c1e902870f14d4370eab4f3a54de388ce06c1ca85ae222b1b5da'
NAME_SHA = '40d861420e948192e232ab4bd5c6ae347211e14bd8cfc2a0d0a388f04aa08bf0'
PROTOCOL_SHA = '47d55648820416cb92d35d562335a6332a8eff490c9a3e861ecda3a54cd6e030'
HELPER_SHA = '872d37a02cbbad8c8e80e2f40068e0f8e0606411c4494173bf7f3c9f24b36181'
OUTER_NAME = 'The Kit/WTC7-Tilted Camera/WTC7TiltedCamera.trz'
PREFIX = 'org.opensourcephysics.cabrillo.tracker.'
MEDIA = 'org.opensourcephysics.media.core.'
PANEL = PREFIX+'TrackerPanel'
MASS = PREFIX+'PointMass'
CLASSES = frozenset({PANEL, PREFIX+'CoordAxes', MASS, MASS+'$FrameData',
    MEDIA+'ImageCoordSystem', MEDIA+'ImageCoordSystem$FrameData',
    PREFIX+'TapeMeasure', PREFIX+'TapeMeasure$FrameData', MEDIA+'VideoClip',
    MEDIA+'StepperClipControl', 'org.opensourcephysics.media.xuggle.XuggleVideo',
    MEDIA+'VideoClipControl', MEDIA+'ReferenceFrame', PREFIX+'ParticleDataTrack',
    PREFIX+'DataTrack', 'java.awt.Color', 'java.util.ArrayList', '[I', '[D'})
FIELDS = frozenset('name description notes note comment comments method algorithm construction '
    'history provenance source expression function model dependent autofill autotracker autoTracker '
    'autotrack keyFrames framedata mass visible locked footprint color trail font format '
    'description_visible data_functions tracks semantic_version width height magnification '
    'center_x center_y length_unit mass_unit units_visible'.split())
TYPES = frozenset('string int double boolean object array collection'.split())
TARGETS = ('name','description','note','comment','method','construction','history')
STEMS = ('descript','comment','note','method','algorithm','construct','history','provenance',
         'dependent','autofill','autotrack','expression','function','model')


def require(condition, code):
    if not condition:
        raise ValueError(code)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(data):
    return {'bytes': len(data), 'sha256': digest(data)}


def ident(value, allowed=()):
    encoded = b'' if value is None else value.encode('utf-8')
    out = {'present': value is not None, 'characters': 0 if value is None else len(value), **pin(encoded)}
    if value is not None and value in allowed:
        out['label'] = value
    return out


def textual(value):
    state = 'absent' if value is None else 'empty' if value == '' else 'whitespace_only' if value.isspace() else 'nonempty'
    return {**ident(value), 'state': state}


def expanded(node):
    # ElementTree expands namespace names and omits xmlns declarations.
    return '{'+node.namespaceURI+'}'+node.localName if node.namespaceURI else node.nodeName


def element_children(node):
    return [child for child in node.childNodes if child.nodeType == Node.ELEMENT_NODE]


def attributes(node):
    result = {}
    for i in range(node.attributes.length):
        item = node.attributes.item(i)
        if item.namespaceURI == 'http://www.w3.org/2000/xmlns/':
            continue
        result[expanded(item)] = item.value
    return result


def text_segments(node):
    """Project DOM Text/CDATA onto ET leading text and element-child tails.

    Comments/PIs are deliberately ignored, not interpreted or inventoried.
    Text separated only by those omitted nodes coalesces as in the declared
    default ElementTree representation.
    """
    groups = [[]]
    for child in node.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            groups.append([])
        elif child.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
            if child.data:
                groups[-1].append(child.data)
    return [''.join(group) if group else None for group in groups]


def dom_inventory(data):
    require(type(data) is bytes and len(data) <= 2_000_000, 'xml_envelope')
    require(b'\x00' not in data and b'<!DOCTYPE' not in data.upper() and b'<!ENTITY' not in data.upper(), 'xml_envelope')
    try:
        data.decode('utf-8-sig')
        document = minidom.parseString(data)
    except Exception:
        raise ValueError('invalid_utf8_xml') from None
    root = document.documentElement
    require(expanded(root) == 'object' and attributes(root).get('class') == PANEL, 'root_schema')
    nodes, paths, attrs, kids, leading, tails = [], {}, {}, {}, {}, {}

    def visit(node, path, depth):
        require(depth <= 40, 'xml_depth_limit')
        require(len(nodes) < 20000, 'xml_node_limit')
        nodes.append(node)
        paths[node] = path
        attrs[node] = attributes(node)
        kids[node] = element_children(node)
        segments = text_segments(node)
        leading[node] = segments[0]
        for index, child in enumerate(kids[node], 1):
            tails[child] = segments[index]
            visit(child, path+f'/*[{index}]', depth+1)
    tails[root] = None
    visit(root, '/*[1]', 0)

    def record(node):
        a = attrs[node]
        segments = [{'kind':'leading_text', 'xml_path':paths[node], 'text':textual(leading[node])}]
        segments.extend({'kind':'child_tail','xml_path':paths[ch],'text':textual(tails[ch])} for ch in kids[node])
        all_immediate = (leading[node] or '') + ''.join(tails[ch] or '' for ch in kids[node])
        metadata = []
        for key in sorted(a):
            allowed = FIELDS if key == 'name' else CLASSES | TYPES if key in ('type','class') else ()
            metadata.append({'key':ident(key, ('name','class','type')), 'value':ident(a[key], allowed)})
        return {'xml_path':paths[node], 'tag':ident(expanded(node), ('object','property')),
                'attributes':metadata, 'child_count':len(kids[node]),
                'name':ident(a.get('name'), FIELDS), 'class':ident(a.get('class'), CLASSES | TYPES),
                'type':ident(a.get('type'), CLASSES | TYPES), 'text':textual(leading[node]),
                'tail':textual(tails[node]), 'immediate_text':textual(all_immediate),
                'immediate_segments':segments,
                'content_state':'structured' if kids[node] else textual(leading[node])['state']}

    records = {node: record(node) for node in nodes}

    def owner(node, owner_id, item_number=None, object_number=None, issues=()):
        properties = [ch for ch in kids[node] if expanded(ch) == 'property']
        names = [(attrs[ch].get('name') is not None, attrs[ch].get('name', '')) for ch in properties]
        direct = []
        for ch, name_key in zip(properties, names):
            duplicate = names.count(name_key) > 1
            kind = attrs[ch].get('type')
            unexpected = kind not in TYPES or 'name' not in attrs[ch]
            if kind in ('string','int','double','boolean') and kids[ch]:
                unexpected = True
            if kind == 'object' and (len(kids[ch]) != 1 or expanded(kids[ch][0]) != 'object'):
                unexpected = True
            direct.append({**records[ch], 'duplicate_name':duplicate,
                           'unexpected_shape':unexpected, 'review_required':duplicate or unexpected})
        target_fields = {}
        for name in TARGETS:
            selected = [r for r in direct if r['name'].get('label') == name]
            target_fields[name] = {
                'status': 'missing' if not selected else 'single' if len(selected) == 1 else 'duplicate',
                'count':len(selected), 'occurrences':[
                    {key:r[key] for key in ('xml_path','content_state','immediate_text','child_count','review_required')}
                    for r in selected]}
        unexpected_children = [paths[ch] for ch in kids[node] if expanded(ch) != 'property']
        return {'owner_id':owner_id, 'xml_path':paths[node], 'class':ident(attrs[node].get('class'), CLASSES),
                'track_item_ordinal_one_based':item_number, 'track_object_ordinal_one_based':object_number,
                'direct_property_count':len(direct), 'direct_properties':direct, 'target_fields':target_fields,
                'unexpected_direct_children':unexpected_children, 'owner_shape_issues':list(issues),
                'review_required':bool(issues or unexpected_children) or any(r['review_required'] for r in direct)}

    containers = [ch for ch in kids[root] if attrs[ch].get('name') == 'tracks']
    require(len(containers) == 1, 'tracks_container_count_not_one')
    container = containers[0]
    container_issues = []
    if expanded(container) != 'property' or attrs[container].get('type') != 'collection':
        container_issues.append('unexpected_tracks_container_shape')
    owners = [owner(root, 'root')]
    items, objects = [], []
    mass_count = 0
    for index, item in enumerate(kids[container], 1):
        candidates = [ch for ch in kids[item] if expanded(ch) == 'object']
        issues = []
        if expanded(item) == 'object':
            candidates = [item]
            issues.append('direct_object_without_item_wrapper')
        if (expanded(item) != 'property' or attrs[item].get('name') != 'item' or
                attrs[item].get('type') != 'object' or len(candidates) != 1 or len(kids[item]) != 1):
            issues.append('unexpected_track_item_shape')
        items.append({'xml_path':paths[item], 'item_ordinal_one_based':index,
                      'object_count':len(candidates), 'shape_issues':issues, 'review_required':bool(issues)})
        for within, obj in enumerate(candidates, 1):
            ordinal = len(objects)+1
            objects.append({'xml_path':paths[obj], 'item_ordinal_one_based':index,
                            'object_ordinal_one_based':ordinal, 'object_within_item_ordinal_one_based':within,
                            'class':ident(attrs[obj].get('class'), CLASSES), 'review_required':bool(issues)})
            if attrs[obj].get('class') == MASS:
                mass_count += 1
                current = owner(obj, f'pointmass{mass_count:02d}', index, ordinal, issues)
                current['pointmass_ordinal_one_based'] = mass_count
                owners.append(current)
    hits, leaves, structured = [], [], []
    for node in nodes:
        for attribute in ('name','class'):
            value = attrs[node].get(attribute)
            if value is not None:
                for stem in STEMS:
                    if stem in value.lower():
                        hits.append({'xml_path':paths[node], 'attribute':attribute, 'stem':stem,
                                     'identity':ident(value), 'child_count':len(kids[node]),
                                     'content_state':records[node]['content_state']})
        if attrs[node].get('type') == 'string':
            subset = {key:records[node][key] for key in ('xml_path','name','child_count','text','content_state')}
            (structured if kids[node] else leaves).append(subset)
    result = {
        'schema_version':1, 'status':'hash_only_locator_not_content_interpretation', 'source_project':pin(data),
        'path_convention':'one-based element-child XPath; root /*[1]',
        'text_semantics':'parsed UTF8 character data, no lexical XML spelling; text/tail separate; immediate text excludes descendant text',
        'excluded':'XML comments and processing instructions omitted by pinned ElementTree parser; no absence conclusion about them',
        'name_allowlist':sorted(FIELDS), 'class_allowlist':sorted(CLASSES), 'type_allowlist':sorted(TYPES),
        'target_field_names':list(TARGETS), 'keyword_stems':list(STEMS),
        'element_count':len(nodes), 'attribute_count':sum(len(attrs[n]) for n in nodes),
        'elements':[records[n] for n in nodes], 'tracks_container_path':paths[container],
        'tracks_container_shape_issues':container_issues, 'track_items':items, 'track_objects':objects,
        'pointmass_owner_count':mass_count, 'owners':owners, 'stem_hit_count':len(hits), 'stem_hits':hits,
        'leaf_string_count':len(leaves), 'leaf_strings':leaves,
        'structured_string_count':len(structured), 'structured_strings':structured,
        'review_required':bool(container_issues) or any(i['review_required'] for i in items) or any(o['review_required'] for o in owners)}
    document.unlink()
    return result


def strict_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate_json_key')
            result[key] = value
        return result
    def nonfinite(_):
        raise ValueError('nonfinite_json')
    return json.loads(data, object_pairs_hook=pairs, parse_constant=nonfinite)


def compare_products(xml, one, two, lineage=None):
    require(one == two, 'producer_repeat_not_identical')
    left = strict_json(one)
    expected = dom_inventory(xml)
    if lineage is not None:
        expected['source_lineage'] = lineage
    # Exact type-sensitive canonical encoding catches int/bool equivalence.
    require(json.dumps(left, sort_keys=True, separators=(',',':'), allow_nan=False) ==
            json.dumps(expected, sort_keys=True, separators=(',',':'), allow_nan=False), 'metadata_oracle_mismatch')
    return {key:expected[key] for key in ('element_count','attribute_count','pointmass_owner_count',
                                         'stem_hit_count','leaf_string_count','structured_string_count')}


def guarded_member(info, limit):
    name = info.filename
    require(bool(name) and '\\' not in name and '\x00' not in name and ':' not in name and
            not name.startswith('/') and '..' not in PurePosixPath(name).parts and not info.is_dir() and
            0 < info.file_size <= limit and not (info.flag_bits & 1) and
            not stat.S_ISLNK(info.external_attr >> 16), 'archive_member_refused')


def pinned_public_xml():
    parent = SOURCE.read_bytes()
    require(len(parent) == 172774879 and digest(parent) == PARENT_SHA, 'parent_pin')
    with zipfile.ZipFile(io.BytesIO(parent)) as outer:
        choices = [(i,q) for i,q in enumerate(outer.infolist()) if q.filename == OUTER_NAME]
        require(len(choices) == 1, 'outer_member_count')
        index, entry = choices[0]
        guarded_member(entry, 20_000_000)
        nested = outer.read(entry)
    require(len(nested) == 15608229 and digest(nested) == NESTED_SHA, 'nested_pin')
    with zipfile.ZipFile(io.BytesIO(nested)) as inner:
        entries = inner.infolist()
        require(len(entries) == 5, 'inner_count')
        entry = entries[4]
        guarded_member(entry, 200_000)
        require(entry.file_size == 161200 and digest(entry.filename.encode()) == NAME_SHA and
                sum(digest(q.filename.encode()) == NAME_SHA for q in entries) == 1, 'project_entry_pin')
        xml = inner.read(entry)
    require(len(xml) == 161200 and digest(xml) == PROJECT_SHA, 'project_pin')
    require(SOURCE.read_bytes() == parent, 'source_changed')
    return xml, {'parent':pin(parent), 'nested_archive':pin(nested), 'project':pin(xml),
                 'outer_entry_index_zero_based':index, 'nested_project_entry_index_zero_based':4,
                 'nested_project_name_sha256':NAME_SHA, 'raw_project_or_media_written':False,
                 'source_unchanged_after_read':True}


def output_directory(name, base=HERE):
    require(name in ('verifier01','verifier02'), 'output_name')
    path = Path(base)/name
    require(not path.exists() and not path.is_symlink(), 'output_exists')
    return path


def write_exclusive(path, payload):
    data = (json.dumps(payload, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
    with Path(path).open('xb') as stream:
        stream.write(data)
    return pin(data)


def file_pin(path):
    return pin(Path(path).read_bytes())


def historical(name, reviewed_sha):
    out = output_directory(name)  # Refusal precedes historical source reads.
    require(re.fullmatch('[0-9a-f]{64}', reviewed_sha) is not None, 'reviewed_verifier_hash')
    paths = {'verifier':Path(__file__), 'verifier_tests':HERE/'test_verify_locator.py',
             'producer':HERE/'locator.py', 'producer_tests':HERE/'test_locator.py',
             'helper':HERE.parent/'tilted-camera-source-join'/'project-export.py',
             'protocol':HERE/'PROTOCOL.md', 'run01':HERE/'run01'/'locator.json',
             'run02':HERE/'run02'/'locator.json', 'receipt01':HERE/'run01'/'receipt.json',
             'receipt02':HERE/'run02'/'receipt.json'}
    before = {key:file_pin(path) for key,path in paths.items()}
    require(before['verifier']['sha256'] == reviewed_sha, 'reviewed_verifier_pin')
    require(before['protocol']['sha256'] == PROTOCOL_SHA and before['helper']['sha256'] == HELPER_SHA, 'procedure_pin')
    receipts = [strict_json(paths[key].read_bytes()) for key in ('receipt01','receipt02')]
    for index, receipt in enumerate(receipts, 1):
        require(receipt.get('status') == 'metadata_exported_pending_independent_verification', 'producer_status')
        require(receipt.get('product') == before[f'run0{index}'], 'producer_product_pin')
        require(receipt['inputs_before'] == receipt['inputs_after'], 'producer_procedure_changed')
        for key in ('producer','tests','helper','protocol'):
            actual = before['producer_tests' if key == 'tests' else key]
            require(receipt['inputs_before'][key] == actual, 'producer_procedure_pin')
    out.mkdir()
    write_exclusive(out/'input-receipt.json', {'status':'started_not_admitted','pins':before,
                    'python':platform.python_version(), 'parser':'stdlib_minidom_no_producer_import'})
    try:
        xml, lineage = pinned_public_xml()
        require(all(r['source_lineage'] == lineage for r in receipts), 'source_lineage_mismatch')
        counts = compare_products(xml, paths['run01'].read_bytes(), paths['run02'].read_bytes(), lineage)
        require(counts['pointmass_owner_count'] == 8, 'historical_owner_count')
        after = {key:file_pin(path) for key,path in paths.items()}
        require(before == after and file_pin(SOURCE) == lineage['parent'], 'inputs_changed')
        result = {'status':'pass_independent_dom_exact_metadata_and_repeat_check', 'counts':counts,
                  'inputs_before':before, 'inputs_after':after, 'source_lineage':lineage,
                  'python':platform.python_version(), 'parser':'stdlib_minidom_no_producer_import',
                  'raw_source_written':False, 'plaintext_saved_values_written':False,
                  'historical_or_physical_validation':False}
        receipt_pin = write_exclusive(out/'verification.json', result)
        return {'status':result['status'], 'verification':receipt_pin, 'counts':counts}
    except Exception:
        write_exclusive(out/'failure.json', {'status':'failed_not_admitted', 'code':'independent_verification_failed'})
        raise


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    try:
        require(len(args) == 4 and args[0] == '--out' and args[2] == '--reviewed-verifier-sha256', 'arguments')
        print(json.dumps(historical(args[1], args[3]), sort_keys=True))
        return 0
    except Exception:
        # No exception text, argument echo, XML snippet or traceback.
        print(json.dumps({'status':'failed_not_admitted','code':'independent_verification_failed'}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
