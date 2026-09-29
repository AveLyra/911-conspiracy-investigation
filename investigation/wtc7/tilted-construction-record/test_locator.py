#!/usr/bin/env python3
"""Synthetic privacy/coverage tests; no historical source loading or raw logs."""
import argparse
import contextlib
import copy
import io
import json
from pathlib import Path
import platform
import sys
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
import locator as subject


def sentinel():
    return ''.join(chr(x) for x in [81,90,88,95,80,82,73,86,65,84,69,95,57,55,49])


def prop(parent,name,kind,text=None,**extra):
    node=ET.SubElement(parent,'property',{'name':name,'type':kind,**extra})
    node.text=text
    return node


def fixture():
    root=ET.Element('object',{'class':subject.held.TRACKER+'TrackerPanel'})
    prop(root,'description','string','')
    prop(root,'method','string',sentinel())
    outside=ET.SubElement(prop(root,'other','object'),'object',{'class':subject.held.MASS})
    prop(outside,'description','string',sentinel())
    tracks=prop(root,'tracks','collection')
    owners=[]
    for i in range(10):
        cls=subject.held.TRACKER+'CoordAxes' if i in (0,4) else subject.held.MASS
        obj=ET.SubElement(prop(tracks,'item','object'),'object',{'class':cls})
        if cls!=subject.held.MASS: continue
        owners.append(obj)
        prop(obj,'name','string',sentinel()+str(i))
        prop(obj,'dependent','boolean','false')
        prop(obj,'mass','double','123.456789')
    return root,owners,tracks


def export(root):
    return subject.locate(ET.tostring(root,encoding='utf-8'))


def canonical(data):
    return json.dumps(data,sort_keys=True,ensure_ascii=True,allow_nan=False)


class Controls(unittest.TestCase):
    out=None

    def test_eight_direct_owners_ordinals_not_nested(self):
        root,_,_=fixture();data=export(root)
        self.assertEqual(len(data['owners']),9)
        self.assertEqual(data['pointmass_owner_count'],8)
        self.assertEqual([x['owner_id'] for x in data['owners']],['root']+[f'pointmass{i:02d}' for i in range(1,9)])
        self.assertEqual([x['track_item_ordinal_one_based'] for x in data['owners'][1:]],[2,3,4,6,7,8,9,10])
        self.assertEqual(len(data['track_objects']),10)
        # Outside nested mass stays in global ledger, not selected owner scope.
        self.assertEqual(sum(x['class'].get('label')==subject.held.MASS for x in data['elements']),9)

    def test_missing_duplicate_empty_whitespace_nonempty_structured(self):
        root,owners,_=fixture()
        prop(owners[0],'description','string')
        prop(owners[1],'description','string',' \t\n')
        prop(owners[2],'description','string',sentinel())
        child=prop(owners[3],'description','string')
        prop(child,'note','string',sentinel())
        prop(owners[4],'description','string','first')
        prop(owners[4],'description','string','second')
        data=export(root);states=[x['target_fields']['description'] for x in data['owners'][1:]]
        self.assertEqual([x['status'] for x in states],['single']*4+['duplicate']+['missing']*3)
        self.assertEqual([states[i]['occurrences'][0]['content_state'] for i in range(4)],
                         ['absent','whitespace_only','nonempty','structured'])
        self.assertTrue(states[3]['occurrences'][0]['review_required'])
        self.assertTrue(all(x['review_required'] for x in states[4]['occurrences']))
        self.assertEqual(subject.text_info('')['state'],'empty')
        self.assertEqual(subject.text_info(None)['state'],'absent')

    def test_all_unknown_tags_attributes_values_and_namespaces_hashed(self):
        root,owners,_=fixture();secret=sentinel()
        n=ET.SubElement(owners[0],'{urn:'+secret+'}'+secret,{
            '{urn:'+secret+'}'+secret:secret,'name':secret,'type':secret,'class':secret})
        n.text=secret;n.tail=secret
        result=export(root);encoded=canonical(result)
        self.assertTrue(secret not in encoded)
        hashed=subject.sha(n.tag.encode())
        record=next(x for x in result['elements'] if x['tag']['sha256']==hashed)
        self.assertTrue('label' not in record['tag'])
        self.assertEqual(len(record['attributes']),4)
        self.assertTrue(result['owners'][1]['review_required'])
        self.assertTrue(record['xml_path'] in result['owners'][1]['unexpected_direct_children'])

    def test_raw_values_never_emitted_even_if_technical_numeric_boolean(self):
        root,owners,_=fixture();secret=sentinel()
        for name,value in [('description',secret),('name','NW Corner'),('method','construction'),
                           ('width','123.456789'),('visible','false')]:
            prop(owners[0],name,'string',value)
        data=export(root);encoded=canonical(data)
        self.assertTrue(secret not in encoded and 'NW Corner' not in encoded and '123.456789' not in encoded)
        def inspect(obj):
            if isinstance(obj,dict):
                self.assertTrue('saved_text' not in obj and 'value' not in obj or set(obj)=={'key','value'})
                if 'state' in obj and 'sha256' in obj:self.assertTrue('label' not in obj)
                for val in obj.values():inspect(val)
            elif isinstance(obj,list):
                for val in obj:inspect(val)
        inspect(data)

    def test_all_stem_hits_not_literal_field_interpretation(self):
        root,owners,_=fixture()
        prop(owners[0],'unrelated_noteBOOK_methodical','string',sentinel())
        prop(owners[0],'Note','string',sentinel())
        n=prop(root,'opaque','object');ET.SubElement(n,'object',{'class':sentinel()+'HistoryModel'})
        data=export(root)
        hits=[x for x in data['stem_hits'] if x['identity']['sha256']==subject.sha('unrelated_noteBOOK_methodical'.encode())]
        self.assertEqual({x['stem'] for x in hits},{'note','method'})
        self.assertTrue(all('label' not in x['identity'] for x in data['stem_hits']))
        self.assertEqual(data['owners'][1]['target_fields']['note']['status'],'missing')
        self.assertTrue(any(x['attribute']=='class' and x['stem']=='history' for x in data['stem_hits']))

    def test_utf8_counts_and_deterministic_paths(self):
        root,owners,_=fixture();value='é\u2603\U0001f52c'
        prop(owners[0],'note','string',value)
        data=export(root)
        note=data['owners'][1]['target_fields']['note']['occurrences'][0]
        self.assertEqual(note['immediate_text']['characters'],3)
        self.assertEqual(note['immediate_text']['bytes'],9)
        self.assertEqual(note['immediate_text']['sha256'],subject.sha(value.encode()))
        parsed,paths=subject.held.parse_xml(ET.tostring(root,encoding='utf-8'))
        self.assertEqual([x['xml_path'] for x in data['elements']],[paths[n] for n in parsed.iter()])
        self.assertEqual(canonical(data),canonical(export(root)))

    def test_mixed_cdata_comment_pi_element_and_tail_semantics(self):
        header=('<object class="'+subject.held.TRACKER+'TrackerPanel">').encode()
        data=header+b'<property name="description" type="string">a<![CDATA[b]]><!--x-->c<?p x?>d<object class="java.awt.Color">DESCENDANT</object>e<![CDATA[f]]><!--y-->g<?q y?>h</property><property name="tracks" type="collection"/></object>'
        got=subject.locate(data)
        record=got['owners'][0]['direct_properties'][0]
        self.assertEqual(record['text']['sha256'],subject.sha(b'abcd'))
        self.assertEqual(record['immediate_text']['sha256'],subject.sha(b'abcdefgh'))
        self.assertEqual(record['immediate_text']['characters'],8)
        self.assertEqual(record['immediate_segments'][1]['text']['sha256'],subject.sha(b'efgh'))
        self.assertEqual(got['element_count'],4)
        self.assertEqual(got['leaf_string_count'],0)
        self.assertEqual(got['structured_string_count'],1)
        self.assertEqual(record['content_state'],'structured')

    def test_leaf_strings_global_not_only_selected_owner(self):
        root,owners,_=fixture()
        child=prop(owners[0],'description','string')
        prop(child,'note','string',sentinel())
        prop(root,'numeric','double',sentinel())
        got=export(root)
        parsed,paths=subject.held.parse_xml(ET.tostring(root))
        want=[paths[n] for n in parsed.iter() if n.get('type')=='string' and not len(n)]
        self.assertEqual([n['xml_path'] for n in got['leaf_strings']],want)
        self.assertTrue(any(n['name'].get('label')=='description' for n in got['leaf_strings']))
        self.assertEqual(len(got['structured_strings']),1)

    def test_duplicate_or_missing_tracks_refused_unexpected_item_retained(self):
        root,owners,tracks=fixture()
        root.append(copy.deepcopy(tracks))
        with self.assertRaises(ValueError):export(root)
        root.remove(root[-1]);root.remove(tracks)
        with self.assertRaises(ValueError):export(root)
        root.append(tracks)
        extra=ET.SubElement(tracks[1],'object',{'class':subject.held.MASS})
        prop(extra,'method','string',sentinel())
        got=export(root)
        self.assertEqual(got['pointmass_owner_count'],9)
        self.assertTrue(got['track_items'][1]['review_required'])
        self.assertTrue(got['owners'][2]['review_required'])

    def test_bad_xml_envelopes_and_malformed_text_do_not_echo(self):
        root,_,_=fixture();data=ET.tostring(root)
        for bad in [b'<!DOCTYPE object>'+data,b'<!ENTITY x "x">'+data,b'\x00'+data,b'<broken>'+sentinel().encode()]:
            try:subject.locate(bad)
            except Exception as error:
                self.assertTrue(sentinel() not in canonical(subject.safe_error(error)))
            else:self.fail('invalid fixture accepted')

    def test_helper_pin_refuses_before_execution_and_source_pin(self):
        path=self.out/'synthetic-source.bin'
        with path.open('xb') as f:f.write(sentinel().encode())
        with self.assertRaises(ValueError):subject.load_helper(path,'0'*64)
        with patch.object(subject.held,'SOURCE',path):
            with self.assertRaises(ValueError):subject.held.load_source()

    def test_producer_helper_protocol_pins_refuse_before_source_loader(self):
        expected_producer='1'*64
        for defect in ('producer','helper','protocol'):
            def fixed_pin(path):
                path=Path(path)
                role=('protocol' if path.name=='PROTOCOL.md' else
                      'helper' if path==subject.HELPER else
                      'producer' if path==Path(subject.__file__) else 'tests')
                digest={'producer':expected_producer,'helper':subject.HELPER_SHA,
                        'protocol':subject.PROTOCOL_SHA,'tests':'2'*64}[role]
                return {'bytes':1,'sha256':'0'*64 if role==defect else digest}
            with patch.object(subject,'HERE',self.out),patch.object(subject,'file_pin',side_effect=fixed_pin),\
                    patch.object(subject.held,'load_source') as load:
                with self.assertRaises(ValueError):subject.historical('gated-'+defect,expected_producer)
                load.assert_not_called()
                self.assertFalse((self.out/('gated-'+defect)).exists())

    def test_nooverwrite_source_gates_and_failure_diagnostic_privacy(self):
        with patch.object(subject,'HERE',self.out):
            for name in ('../bad','/tmp/bad','nested/bad','',None):
                with self.assertRaises(ValueError):subject.output_path(name)
            (self.out/'existing').mkdir()
            (self.out/'dangling').symlink_to(self.out/'absent')
            for name in ('existing','dangling'):
                with patch.object(subject.held,'load_source') as load:
                    with self.assertRaises(ValueError):subject.historical(name,'0'*64)
                    load.assert_not_called()
        path=self.out/'synthetic-output.json';subject.write_json(path,{'status':'synthetic'})
        before=subject.file_pin(path)
        with self.assertRaises(FileExistsError):subject.write_json(path,{'status':'changed'})
        self.assertEqual(subject.file_pin(path),before)
        self.assertTrue(sentinel() not in canonical(subject.safe_error(ValueError(sentinel()))))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',required=True)
    args=parser.parse_args();out=subject.output_path(args.out)
    before={'producer':subject.file_pin(subject.__file__),'tests':subject.file_pin(__file__),
            'helper':subject.file_pin(subject.HELPER),'protocol':subject.file_pin(subject.HERE/'PROTOCOL.md')}
    out.mkdir();Controls.out=out
    # TestResult stores tracebacks only in memory. Persist hashes, never assertion values.
    result=unittest.TestResult();captured_out=io.StringIO();captured_err=io.StringIO()
    with contextlib.redirect_stdout(captured_out),contextlib.redirect_stderr(captured_err):
        unittest.defaultTestLoader.loadTestsFromTestCase(Controls).run(result)
    failures=[{'test':test.id(),'diagnostic':subject.identity(details)} for test,details in result.failures+result.errors]
    after={'producer':subject.file_pin(subject.__file__),'tests':subject.file_pin(__file__),
           'helper':subject.file_pin(subject.HELPER),'protocol':subject.file_pin(subject.HERE/'PROTOCOL.md')}
    record={'tests_run':result.testsRun,'failure_count':len(result.failures),'error_count':len(result.errors),
            'failures':failures,'captured_stdout':subject.text_info(captured_out.getvalue()),
            'captured_stderr':subject.text_info(captured_err.getvalue()),'inputs_before':before,'inputs_after':after,
            'successful':result.wasSuccessful() and before==after,'python':platform.python_version(),
            'synthetic_only':True,'historical_source_read':False,'raw_test_diagnostics_saved':False}
    if record['successful']:
        root,_,_=fixture()
        record['synthetic_product']=subject.write_json(out/'synthetic-locator.json',export(root))
    receipt=subject.write_json(out/'receipt.json',record)
    print(json.dumps({'successful':record['successful'],'tests_run':result.testsRun,
                      'failure_count':len(result.failures),'error_count':len(result.errors),'receipt':receipt},sort_keys=True))
    sys.exit(0 if record['successful'] else 1)
