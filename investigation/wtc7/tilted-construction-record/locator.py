#!/usr/bin/env python3
"""Inert, hash-only saved-construction locator. No saved value disclosure."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import re
import sys
import types

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
HELPER = HERE.parent/'tilted-camera-source-join'/'project-export.py'
HELPER_SHA = '872d37a02cbbad8c8e80e2f40068e0f8e0606411c4494173bf7f3c9f24b36181'
PROTOCOL_SHA = '47d55648820416cb92d35d562335a6332a8eff490c9a3e861ecda3a54cd6e030'
FIELDS = frozenset('name description notes note comment comments method algorithm construction '
    'history provenance source expression function model dependent autofill autotracker autoTracker '
    'autotrack keyFrames framedata mass visible locked footprint color trail font format '
    'description_visible data_functions tracks semantic_version width height magnification '
    'center_x center_y length_unit mass_unit units_visible'.split())
TYPES = frozenset('string int double boolean object array collection'.split())
TARGETS = ('name','description','note','comment','method','construction','history')
STEMS = ('descript','comment','note','method','algorithm','construct','history','provenance',
         'dependent','autofill','autotrack','expression','function','model')


def sha(data): return hashlib.sha256(data).hexdigest()


def byte_pin(data): return {'bytes':len(data), 'sha256':sha(data)}


def file_pin(path):
    with Path(path).open('rb') as stream:
        digest = hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':Path(path).stat().st_size, 'sha256':digest}


def require(ok, code):
    if not ok: raise ValueError(code)


def load_helper(path=HELPER, expected=HELPER_SHA):
    data = Path(path).read_bytes()
    require(sha(data)==expected, 'helper_pin_before_execution')
    module = types.ModuleType('pinned_project_loader')
    module.__file__ = str(path)
    # Exactly the verified bytes; its __main__ branch is not invoked.
    exec(compile(data,str(path),'exec'),module.__dict__)
    return module


held = load_helper()
CLASSES = frozenset(held.KNOWN_CLASSES)


def identity(value, allowed=()):
    if value is None:
        return {'present':False, 'characters':0, **byte_pin(b'')}
    require(type(value) is str, 'identity_type')
    result = {'present':True, 'characters':len(value), **byte_pin(value.encode('utf-8'))}
    if value in allowed: result['label'] = value
    return result


def text_info(value):
    state = ('absent' if value is None else 'empty' if value=='' else
             'whitespace_only' if value.isspace() else 'nonempty')
    return {**identity(value), 'state':state}


def node_info(node, paths):
    attributes = []
    for key,value in sorted(node.attrib.items()):
        allowed = FIELDS if key=='name' else CLASSES|TYPES if key in ('class','type') else ()
        attributes.append({'key':identity(key,('name','class','type')),
                           'value':identity(value,allowed)})
    segments = [{'kind':'leading_text','xml_path':paths[node],'text':text_info(node.text)}]
    for child in node:
        segments.append({'kind':'child_tail','xml_path':paths[child],'text':text_info(child.tail)})
    immediate = (node.text or '') + ''.join(child.tail or '' for child in node)
    return {'xml_path':paths[node], 'tag':identity(node.tag,('object','property')),
            'attributes':attributes, 'child_count':len(node),
            'name':identity(node.get('name'),FIELDS),
            'class':identity(node.get('class'),CLASSES|TYPES),
            'type':identity(node.get('type'),CLASSES|TYPES),
            'text':text_info(node.text), 'tail':text_info(node.tail),
            'immediate_text':text_info(immediate), 'immediate_segments':segments,
            'content_state':'structured' if len(node) else text_info(node.text)['state']}


def selected_owner(obj, owner_id, paths, ordinal=None, object_ordinal=None, shape_issues=()):
    properties = [child for child in obj if child.tag=='property']
    counts = Counter((n.get('name') is not None,n.get('name','')) for n in properties)
    direct = []
    for child in properties:
        record = node_info(child,paths)
        duplicate = counts[(child.get('name') is not None,child.get('name',''))] > 1
        kind = child.get('type')
        unexpected = (kind not in TYPES or child.get('name') is None or
                      (kind in {'string','int','double','boolean'} and len(child)>0) or
                      (kind=='object' and (len(child)!=1 or child[0].tag!='object')))
        record.update(duplicate_name=duplicate, unexpected_shape=unexpected,
                      review_required=duplicate or unexpected)
        direct.append(record)
    fields = {}
    for name in TARGETS:
        matches = [n for n in direct if n['name'].get('label')==name]
        fields[name] = {'status':'missing' if not matches else 'single' if len(matches)==1 else 'duplicate',
                        'count':len(matches), 'occurrences':[
                            {'xml_path':n['xml_path'],'content_state':n['content_state'],
                             'immediate_text':n['immediate_text'],
                             'child_count':n['child_count'],'review_required':n['review_required']}
                            for n in matches]}
    unexpected_children = [paths[n] for n in obj if n.tag!='property']
    return {'owner_id':owner_id, 'xml_path':paths[obj], 'class':identity(obj.get('class'),CLASSES),
            'track_item_ordinal_one_based':ordinal, 'track_object_ordinal_one_based':object_ordinal,
            'direct_property_count':len(direct), 'direct_properties':direct,
            'target_fields':fields, 'unexpected_direct_children':unexpected_children,
            'owner_shape_issues':list(shape_issues), 'review_required':bool(shape_issues) or
                bool(unexpected_children) or any(n['review_required'] for n in direct)}


def locate(data):
    root, paths = held.parse_xml(data)
    nodes = list(root.iter())
    ledger = [node_info(node,paths) for node in nodes]
    containers = [n for n in root if n.get('name')=='tracks']
    require(len(containers)==1, 'tracks_container_count_not_one')
    container = containers[0]
    container_issues = []
    if container.tag!='property' or container.get('type')!='collection':
        container_issues.append('unexpected_tracks_container_shape')
    owners = [selected_owner(root,'root',paths)]
    objects, items = [], []
    mass_ordinal = 0
    for item_ordinal,item in enumerate(container,1):
        candidates = [n for n in item if n.tag=='object']
        issues = []
        if item.tag=='object':
            candidates = [item]
            issues.append('direct_object_without_item_wrapper')
        if (item.tag!='property' or item.get('name')!='item' or item.get('type')!='object'
                or len(candidates)!=1 or len(item)!=1):
            issues.append('unexpected_track_item_shape')
        items.append({'xml_path':paths[item], 'item_ordinal_one_based':item_ordinal,
                      'object_count':len(candidates),'shape_issues':issues,
                      'review_required':bool(issues)})
        for child_ordinal,obj in enumerate(candidates,1):
            object_ordinal = len(objects)+1
            objects.append({'xml_path':paths[obj], 'item_ordinal_one_based':item_ordinal,
                            'object_ordinal_one_based':object_ordinal,
                            'object_within_item_ordinal_one_based':child_ordinal,
                            'class':identity(obj.get('class'),CLASSES),
                            'review_required':bool(issues)})
            if obj.get('class')==held.MASS:
                mass_ordinal += 1
                owner = selected_owner(obj,f'pointmass{mass_ordinal:02d}',paths,
                                       item_ordinal,object_ordinal,issues)
                owner['pointmass_ordinal_one_based'] = mass_ordinal
                owners.append(owner)
    hits, leaves, structured = [], [], []
    for node in nodes:
        for attribute in ('name','class'):
            value = node.get(attribute)
            if value is None: continue
            for stem in STEMS:
                if stem in value.lower():
                    hits.append({'xml_path':paths[node], 'attribute':attribute,'stem':stem,
                                 'identity':identity(value), 'child_count':len(node),
                                 'content_state':'structured' if len(node) else text_info(node.text)['state']})
        if node.get('type')=='string':
            item = {'xml_path':paths[node], 'name':identity(node.get('name'),FIELDS),
                    'child_count':len(node), 'text':text_info(node.text),
                    'content_state':'structured' if len(node) else text_info(node.text)['state']}
            (structured if len(node) else leaves).append(item)
    return {'schema_version':1, 'status':'hash_only_locator_not_content_interpretation',
            'source_project':byte_pin(data),
            'path_convention':'one-based element-child XPath; root /*[1]',
            'text_semantics':'parsed UTF8 character data, no lexical XML spelling; text/tail separate; immediate text excludes descendant text',
            'excluded':'XML comments and processing instructions omitted by pinned ElementTree parser; no absence conclusion about them',
            'name_allowlist':sorted(FIELDS),'class_allowlist':sorted(CLASSES),'type_allowlist':sorted(TYPES),
            'target_field_names':list(TARGETS),'keyword_stems':list(STEMS),
            'element_count':len(ledger),'attribute_count':sum(len(n.attrib) for n in nodes),
            'elements':ledger,'tracks_container_path':paths[container],
            'tracks_container_shape_issues':container_issues,'track_items':items,'track_objects':objects,
            'pointmass_owner_count':mass_ordinal,'owners':owners,
            'stem_hit_count':len(hits),'stem_hits':hits,
            'leaf_string_count':len(leaves),'leaf_strings':leaves,
            'structured_string_count':len(structured),'structured_strings':structured,
            'review_required':bool(container_issues) or any(i['review_required'] for i in items) or
                              any(o['review_required'] for o in owners)}


def output_path(name):
    require(type(name) is str and re.fullmatch('[a-z][a-z0-9_-]{0,63}',name), 'invalid_output_name')
    path = HERE/name
    require(not path.exists() and not path.is_symlink(), 'output_already_exists')
    return path


def write_json(path, data):
    payload = (json.dumps(data,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode()
    with path.open('xb') as stream: stream.write(payload)
    return byte_pin(payload)


def safe_error(error):
    # Never echo exception text, traceback locals, source snippets or paths.
    return {'status':'failed_not_admitted','code':'locator_operation_failed',
            'exception_text':identity(str(error))}


def historical(name, reviewed_sha):
    out = output_path(name)  # Existing output refusal precedes source loader.
    before = {'producer':file_pin(__file__), 'tests':file_pin(HERE/'test_locator.py'),
              'helper':file_pin(HELPER), 'protocol':file_pin(HERE/'PROTOCOL.md')}
    require(before['producer']['sha256']==reviewed_sha,'producer_review_pin')
    require(before['helper']['sha256']==HELPER_SHA and before['protocol']['sha256']==PROTOCOL_SHA,
            'helper_or_protocol_pin')
    out.mkdir()
    write_json(out/'input-receipt.json',{'inputs_before':before,'python':platform.python_version(),
               'stage':'source_metadata_only','status':'started_not_admitted'})
    try:
        data, source = held.load_source()
        require(sha(data)==held.TRK_HASH,'source_project_pin')
        result = locate(data)
        require(result['pointmass_owner_count']==8,'historical_pointmass_count')
        result['source_lineage'] = {k:source[k] for k in ('parent','nested_archive','project',
            'outer_entry_index_zero_based','nested_project_entry_index_zero_based',
            'nested_project_name_sha256','raw_project_or_media_written','source_unchanged_after_read')}
        after = {'producer':file_pin(__file__), 'tests':file_pin(HERE/'test_locator.py'),
                 'helper':file_pin(HELPER), 'protocol':file_pin(HERE/'PROTOCOL.md')}
        require(before==after,'procedure_changed')
        require(file_pin(held.SOURCE)==source['parent'],'source_changed_after_parse')
        product = write_json(out/'locator.json',result)
        write_json(out/'receipt.json',{'status':'metadata_exported_pending_independent_verification',
                   'inputs_before':before,'inputs_after':after,'source_lineage':result['source_lineage'],
                   'product':product,'python':platform.python_version(),
                   'raw_source_written':False,'plaintext_saved_values_written':False})
        return {'status':'metadata_exported_pending_independent_verification','product':product,
                'owners':len(result['owners']),'elements':result['element_count']}
    except Exception as error:
        write_json(out/'failure.json',safe_error(error))
        raise


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    parser.add_argument('--reviewed-producer-sha256',required=True)
    args=parser.parse_args()
    try:
        print(json.dumps(historical(args.out,args.reviewed_producer_sha256),sort_keys=True))
    except Exception as error:
        print(json.dumps(safe_error(error),sort_keys=True),file=sys.stderr)
        return 1
    return 0


if __name__=='__main__':
    sys.exit(main())
