#!/usr/bin/env python3
"""Synthetic-only independent oracle controls; no historical loader call."""
import base64
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import platform
import re
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('independent_locator_checker', Path(__file__).with_name('verify_locator.py'))
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)
SENTINEL = base64.b64decode('TkVWRVJfUFJJTlRfUFJJVkFURV9TRU5USU5FTA==').decode()


def document(root_body='', items=None):
    if items is None:
        items = '<property name="item" type="object"><object class="'+subject.MASS+'"><property name="name" type="string">'+SENTINEL+'</property></object></property>'
    return ('<object class="'+subject.PANEL+'">'+root_body+'<property name="tracks" type="collection">'+items+'</property></object>').encode()


def encoded(result):
    return json.dumps(result, sort_keys=True).encode()


def shared_synthetic_fixture():
    # Reconstruct the producer's documented synthetic fixture independently.
    # ET is used only as a fixture serializer; the oracle parses with minidom.
    def prop(parent, name, kind, value=None):
        node=ET.SubElement(parent,'property',{'name':name,'type':kind})
        node.text=value
        return node
    secret=''.join(chr(x) for x in [81,90,88,95,80,82,73,86,65,84,69,95,57,55,49])
    root=ET.Element('object',{'class':subject.PANEL})
    prop(root,'description','string','')
    prop(root,'method','string',secret)
    outside=ET.SubElement(prop(root,'other','object'),'object',{'class':subject.MASS})
    prop(outside,'description','string',secret)
    tracks=prop(root,'tracks','collection')
    for i in range(10):
        cls=subject.PREFIX+'CoordAxes' if i in (0,4) else subject.MASS
        obj=ET.SubElement(prop(tracks,'item','object'),'object',{'class':cls})
        if cls==subject.MASS:
            prop(obj,'name','string',secret+str(i))
            prop(obj,'dependent','boolean','false')
            prop(obj,'mass','double','123.456789')
    return ET.tostring(root,encoding='utf-8')


class OracleControls(unittest.TestCase):
    def test_exact_owners_ordinals_and_nested_owner_exclusion(self):
        nested = '<property name="nested" type="object"><object class="'+subject.MASS+'"><property name="description" type="string">'+SENTINEL+'</property></object></property>'
        items = '<property name="item" type="object"><object class="'+subject.PREFIX+'CoordAxes"/></property>'
        items += ''.join('<property name="item" type="object"><object class="'+subject.MASS+'"/></property>' for _ in range(8))
        result = subject.dom_inventory(document(nested, items))
        self.assertEqual(result['pointmass_owner_count'], 8)
        self.assertEqual([o['owner_id'] for o in result['owners']], ['root']+[f'pointmass{i:02d}' for i in range(1,9)])
        self.assertEqual(result['owners'][1]['track_item_ordinal_one_based'], 2)
        self.assertEqual(result['owners'][-1]['track_object_ordinal_one_based'], 9)
        self.assertEqual(result['owners'][0]['target_fields']['description']['status'], 'missing')
        self.assertEqual(result['leaf_string_count'], 1)

    def test_direct_duplicate_missing_and_empty_states(self):
        body = '<property name="description" type="string"/><property name="description" type="string">  </property><property name="note" type="string">text</property>'
        result = subject.dom_inventory(document(body))
        root = result['owners'][0]
        self.assertEqual(root['target_fields']['description']['status'], 'duplicate')
        self.assertEqual([r['content_state'] for r in root['target_fields']['description']['occurrences']], ['absent','whitespace_only'])
        self.assertEqual(root['target_fields']['note']['occurrences'][0]['content_state'], 'nonempty')
        self.assertEqual(root['target_fields']['history']['status'], 'missing')
        self.assertTrue(root['review_required'])
        self.assertEqual(subject.textual('')['state'], 'empty')
        self.assertEqual(subject.textual(None)['state'], 'absent')

    def test_mixed_text_cdata_comments_pi_and_tails(self):
        body = '<property name="description" type="string">a<![CDATA[b]]><!--hidden--><?ignored x?><object class="java.awt.Color">child</object>c<![CDATA[d]]><!--hidden2--><property name="note" type="string">z</property>e</property>'
        result = subject.dom_inventory(document(body))
        prop = result['owners'][0]['direct_properties'][0]
        self.assertEqual(prop['text'], subject.textual('ab'))
        self.assertEqual(prop['immediate_text'], subject.textual('abcde'))
        self.assertEqual([r['text'] for r in prop['immediate_segments']], [subject.textual('ab'),subject.textual('cd'),subject.textual('e')])
        self.assertEqual(result['structured_string_count'], 1)
        self.assertTrue(prop['unexpected_shape'])
        self.assertTrue('hidden' not in encoded(result).decode())

    def test_utf8_bytes_and_namespace_clark_names_not_disclosed(self):
        body = '<property name="description" type="string">é🙂</property><q:secret xmlns:q="urn:private" q:secret="'+SENTINEL+'">'+SENTINEL+'</q:secret>'
        result = subject.dom_inventory(document(body))
        prop = result['owners'][0]['direct_properties'][0]
        self.assertEqual(prop['text']['characters'], 2)
        self.assertEqual(prop['text']['bytes'], 6)
        unknown = result['elements'][2]
        self.assertEqual(unknown['tag'], subject.ident('{urn:private}secret'))
        self.assertEqual(len(unknown['attributes']), 1)
        self.assertTrue('urn:private' not in encoded(result).decode())
        self.assertTrue(SENTINEL not in encoded(result).decode())

    def test_arbitrary_attributes_and_literal_allowlist_only(self):
        body = '<property name="description" type="string" privatekey="'+SENTINEL+'">'+SENTINEL+'</property><property name="Description" type="string" class="'+SENTINEL+'"/>'
        result = subject.dom_inventory(document(body))
        raw = encoded(result).decode()
        self.assertTrue(SENTINEL not in raw and 'privatekey' not in raw)
        self.assertEqual(result['owners'][0]['target_fields']['description']['count'], 1)
        self.assertEqual(result['stem_hit_count'], 2)
        self.assertTrue(all('label' not in hit['identity'] for hit in result['stem_hits']))

    def test_stem_substrings_all_name_and_class_hits_without_claim(self):
        body = '<property name="MethodicalNotebookModel" type="object"><object class="local.ExpressionConstruction"/></property>'
        result = subject.dom_inventory(document(body))
        self.assertEqual([(r['attribute'],r['stem']) for r in result['stem_hits']], [('name','note'),('name','method'),('name','model'),('class','construct'),('class','expression')])
        self.assertEqual(result['owners'][0]['target_fields']['method']['status'], 'missing')

    def test_all_leaf_strings_and_structured_strings(self):
        body = '<property name="unknown" type="string"/><property name="description" type="string"><object class="java.awt.Color"><property name="unknown" type="string">x</property></object></property><property name="unknown" type="double">'+SENTINEL+'</property>'
        result = subject.dom_inventory(document(body))
        self.assertEqual(result['leaf_string_count'], 3)
        self.assertEqual(result['structured_string_count'], 1)
        self.assertTrue(SENTINEL not in encoded(result).decode())
        self.assertTrue(any(r['type'].get('label') == 'double' and r['text']['state'] == 'nonempty' for r in result['elements']))

    def test_duplicate_missing_container_and_root_refusal(self):
        for data in [document('<property name="tracks" type="collection"/>'), ('<object class="'+subject.PANEL+'"/>').encode(), b'<object class="wrong"/>']:
            with self.assertRaises(ValueError):
                subject.dom_inventory(data)

    def test_unexpected_shapes_preserved_and_ordinals_retained(self):
        items = '<object class="'+subject.MASS+'"/><property name="item" type="object"><object class="'+subject.MASS+'"/><object class="'+subject.MASS+'"/></property>'
        result = subject.dom_inventory(document('<unknown/>',items))
        self.assertEqual(result['pointmass_owner_count'], 3)
        self.assertEqual([o['track_item_ordinal_one_based'] for o in result['owners'][1:]], [1,2,2])
        self.assertEqual([o['track_object_ordinal_one_based'] for o in result['owners'][1:]], [1,2,3])
        self.assertTrue(result['review_required'])
        self.assertTrue(result['owners'][0]['unexpected_direct_children'])

    def test_envelope_dtd_entities_utf16_and_depth_refused(self):
        good = document()
        bads = [b'<!DOCTYPE object>'+good, b'<!ENTITY x "value">'+good, good.decode().encode('utf-16'), b'<bad>', b'\xff', b'x'*2_000_001]
        bads.append(document('<property>'*42+'</property>'*42))
        for data in bads:
            with self.assertRaises(ValueError):
                subject.dom_inventory(data)

    def test_exact_comparison_and_deliberate_corruptions(self):
        xml = document('<property name="description" type="string">text</property>')
        clean = subject.dom_inventory(xml)
        self.assertEqual(subject.compare_products(xml, encoded(clean), encoded(clean))['pointmass_owner_count'], 1)
        mutations = []
        for key in ('elements','owners','stem_hits','leaf_strings','track_items','track_objects'):
            changed = copy.deepcopy(clean); changed[key].pop(); mutations.append(changed)
        changed = copy.deepcopy(clean); changed['owners'][0]['target_fields']['description']['status']='missing'; mutations.append(changed)
        changed = copy.deepcopy(clean); changed['elements'][1]['text']['sha256']='0'*64; mutations.append(changed)
        changed = copy.deepcopy(clean); changed['pointmass_owner_count']=True; mutations.append(changed)
        changed = copy.deepcopy(clean); changed['elements'][1]['xml_path']='/*[1]/*[99]'; mutations.append(changed)
        for changed in mutations:
            with self.assertRaises(ValueError):
                subject.compare_products(xml,encoded(changed),encoded(changed))
        with self.assertRaises(ValueError):
            subject.compare_products(xml, encoded(clean), encoded(clean)+b' ')

    def test_json_duplicate_and_nonfinite_refused(self):
        for data in [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}']:
            with self.assertRaises(ValueError):
                subject.strict_json(data)

    def test_archive_member_guards(self):
        for name in ('../x','/x','C:/x','a\\x','a/../../x'):
            item=zipfile.ZipInfo(name); item.file_size=10
            with self.assertRaises(ValueError): subject.guarded_member(item,100)
        for mode in ('large','empty','encrypted','symlink'):
            item=zipfile.ZipInfo('safe'); item.file_size=10
            if mode=='large': item.file_size=101
            if mode=='empty': item.file_size=0
            if mode=='encrypted': item.flag_bits=1
            if mode=='symlink': item.external_attr=(stat.S_IFLNK|0o777)<<16
            with self.assertRaises(ValueError): subject.guarded_member(item,100)

    def test_parent_pin_refused_before_archive_parse(self):
        with tempfile.TemporaryDirectory(prefix='synthetic-locator-pin-') as directory:
            source=Path(directory)/'source.bin'; source.write_bytes(b'synthetic-not-an-archive')
            with patch.object(subject,'SOURCE',source), patch.object(subject.zipfile,'ZipFile',side_effect=AssertionError('archive_should_not_open')):
                with self.assertRaisesRegex(ValueError,'parent_pin'): subject.pinned_public_xml()

    def test_producer_synthetic_fixture_exact_full_schema(self):
        path=Path(__file__).parent/'controls02'/'synthetic-locator.json'
        product=path.read_bytes()
        self.assertEqual(subject.digest(product),'efc814ded6b0ec0c3042c3955c6f4874ad5e787f963f93dd0c68b749e2eee694')
        counts=subject.compare_products(shared_synthetic_fixture(),product,product)
        self.assertEqual(counts['pointmass_owner_count'],8)

    def test_verifier_helper_protocol_pins_precede_source(self):
        expected='1'*64
        with tempfile.TemporaryDirectory(prefix='synthetic-verifier-gate-') as directory:
            target=Path(directory)/'verifier01'
            for defect in ('verifier','helper','protocol'):
                def fake_pin(path):
                    name=Path(path).name
                    role='verifier' if name=='verify_locator.py' else 'helper' if name=='project-export.py' else 'protocol' if name=='PROTOCOL.md' else 'other'
                    value={'verifier':expected,'helper':subject.HELPER_SHA,'protocol':subject.PROTOCOL_SHA,'other':'2'*64}[role]
                    return {'bytes':1,'sha256':'0'*64 if role==defect else value}
                with patch.object(subject,'output_directory',return_value=target), patch.object(subject,'file_pin',side_effect=fake_pin), patch.object(subject,'pinned_public_xml') as source:
                    with self.assertRaises(ValueError): subject.historical('verifier01',expected)
                    source.assert_not_called()
                    self.assertFalse(target.exists())

    def test_exclusive_outputs_and_sanitized_cli_errors(self):
        with tempfile.TemporaryDirectory(prefix='synthetic-locator-output-') as directory:
            for name in ('../verifier01','/verifier01','other', 'verifier03'):
                with self.assertRaises(ValueError): subject.output_directory(name,directory)
            target=subject.output_directory('verifier01',directory); target.mkdir()
            with self.assertRaises(ValueError): subject.output_directory('verifier01',directory)
            link=Path(directory)/'verifier02'; link.symlink_to(Path(directory)/'missing')
            with self.assertRaises(ValueError): subject.output_directory('verifier02',directory)
            receipt=target/'receipt.json'; subject.write_exclusive(receipt,{'status':'synthetic'})
            original=receipt.read_bytes()
            with self.assertRaises(FileExistsError): subject.write_exclusive(receipt,{'status':'overwrite'})
            self.assertEqual(receipt.read_bytes(),original)
            err=io.StringIO()
            with contextlib.redirect_stderr(err):
                code=subject.main([SENTINEL])
            self.assertEqual(code,1)
            self.assertTrue(SENTINEL not in err.getvalue())
            with patch.object(subject,'output_directory',side_effect=ValueError('output_exists')), patch.object(subject,'pinned_public_xml',side_effect=AssertionError('no_source_read')):
                with self.assertRaisesRegex(ValueError,'output_exists'): subject.historical('verifier01','0'*64)


def run_controls(name):
    if re.fullmatch(r'verifier-controls(?:-root)?\d{2}',name) is None:
        raise ValueError('control_output_name')
    here=Path(__file__).parent
    out=here/name
    if out.exists() or out.is_symlink():
        raise ValueError('control_output_exists')
    paths={'verifier':Path(subject.__file__),'tests':Path(__file__),
           'protocol':here/'PROTOCOL.md','synthetic_reference':here/'controls02'/'synthetic-locator.json'}
    before={key:subject.file_pin(path) for key,path in paths.items()}
    out.mkdir()
    result=unittest.TestResult(); stdout=io.StringIO(); stderr=io.StringIO()
    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
        unittest.defaultTestLoader.loadTestsFromTestCase(OracleControls).run(result)
    after={key:subject.file_pin(path) for key,path in paths.items()}
    failures=[{'test':test.id(),'diagnostic_hash':subject.digest(details.encode()),'diagnostic_bytes':len(details.encode())}
              for test,details in result.failures+result.errors]
    receipt={'tests_run':result.testsRun,'failure_count':len(result.failures),'error_count':len(result.errors),
             'failures':failures,'stdout':subject.textual(stdout.getvalue()),'stderr':subject.textual(stderr.getvalue()),
             'inputs_before':before,'inputs_after':after,'python':platform.python_version(),
             'successful':result.wasSuccessful() and before==after,'synthetic_only':True,
             'historical_source_read':False,'raw_test_diagnostics_saved':False}
    receipt_pin=subject.write_exclusive(out/'receipt.json',receipt)
    print(json.dumps({'successful':receipt['successful'],'tests_run':result.testsRun,
                      'failure_count':len(result.failures),'error_count':len(result.errors),'receipt':receipt_pin},sort_keys=True))
    return 0 if receipt['successful'] else 1


if __name__ == '__main__':
    if len(sys.argv)==1:
        unittest.main(verbosity=2)
    elif len(sys.argv)==3 and sys.argv[1]=='--out':
        try:
            sys.exit(run_controls(sys.argv[2]))
        except Exception:
            print(json.dumps({'status':'failed','code':'synthetic_controls_operation_failed'}),file=sys.stderr)
            sys.exit(1)
    else:
        print(json.dumps({'status':'failed','code':'synthetic_controls_arguments'}),file=sys.stderr)
        sys.exit(1)
