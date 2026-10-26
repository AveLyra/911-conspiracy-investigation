#!/usr/bin/env python3
"""Check this public documentation package, not the underlying engineering."""
import argparse
import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
EXPECTED={'README.md','MASTER-LIST.md','AS-COMPILED.md','SOURCE-EXCERPTS.md',
 'SOURCE-LINKS.md','CORRECTIONS.md','PUBLICATION.md','register.json',
 'verify_public.py','VERIFICATION.json','TEXT-CHANGES.diff','MANIFEST.json',
 'INHERITED-BIBLIOGRAPHY.md','2012-REQUEST-ADDENDUM.md'}

def sha(b):return hashlib.sha256(b).hexdigest()
def load():return json.loads((HERE/'register.json').read_text())

class PublicRegisterTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.p=load()

 def test_01_complete_id_coverage(self):
  self.assertEqual([e['id'] for e in self.p['entries']],[f'M{i:03}' for i in range(1,135)])
  self.assertEqual((self.p['inherited_count'],self.p['addition_count']),(88,43))

 def test_02_source_pins(self):
  self.assertEqual(len(self.p['source_manifest']),29)
  for e in self.p['entries']:
   for loc in e['locators']:
    self.assertEqual(loc['source_sha256'],self.p['source_manifest'][loc['source_id']]['sha256'])
    self.assertRegex(loc['source_sha256'],r'^[0-9a-f]{64}$')

 def test_03_published_excerpts(self):
  text=(HERE/'SOURCE-EXCERPTS.md').read_text()
  for e in self.p['entries']:
   loc=e['locators'][0]
   self.assertEqual(sha(loc['excerpt'].encode()),loc['published_excerpt_sha256'])
   self.assertIn(loc['excerpt'],text)

 def test_04_relationship_targets(self):
  ids={e['id'] for e in self.p['entries']}
  for e in self.p['entries']:self.assertTrue(set(e['related'])<=ids)

 def test_05_readable_master_coverage(self):
  text=(HERE/'MASTER-LIST.md').read_text()
  self.assertEqual(re.findall(r'^### (M\d{3}) —',text,re.M),[e['id'] for e in self.p['entries']])

 def test_06_prior_edition_kept(self):
  text=(HERE/'AS-COMPILED.md').read_text()
  self.assertIn('historical status',text)
  self.assertEqual(len(re.findall(r'^### M\d{3} —',text,re.M)),131)
  self.assertRegex(self.p['source_master_sha256'],r'^[0-9a-f]{64}$')

 def test_07_corrections_are_additive(self):
  for eid in ('M096','M098','M107','M124'):
   e=next(x for x in self.p['entries'] if x['id']==eid)
   self.assertIn('publication_addendum',e)
  self.assertIn('WARC',next(x for x in self.p['entries'] if x['id']=='M098')['next_test'])
  self.assertIn('ARC',self.p['corrections']['M098'])

 def test_08_no_absolute_host_paths(self):
  pattern=re.compile(r'(?<![A-Za-z0-9])/(?:Users|Volumes|private)/|C:\\Users\\')
  self.assertIsNotNone(pattern.search('`/Users/example/file`'))
  self.assertIsNone(pattern.search('assets/users/contents'))
  for path in HERE.iterdir():
   if path.is_file() and path.suffix in ('.md','.json','.diff'):
    self.assertIsNone(pattern.search(path.read_text()),path.name)

 def test_09_case_material_excluded(self):
  pattern=re.compile(r'BEGIN [A-Z ]*PRIVATE KEY|\bR22\b|\bFD2[12]\b|\bFletcher\b|\bVaughn\b|\bECF\b|Exemption\s*3|Rule\s*26',re.I)
  for path in HERE.iterdir():
   if path.is_file() and path.suffix in ('.md','.json','.diff'):
    self.assertIsNone(pattern.search(path.read_text()),path.name)

 def test_10_public_citations_and_local_anchors(self):
  for path in HERE.glob('*.md'):
   text=path.read_text()
   for target in re.findall(r'\]\(([^)]+)\)',text):
    if target.startswith(('http:','https:')):continue
    filename,_,anchor=target.partition('#')
    if not filename:destination=path
    else:destination=HERE/filename
    if destination.name in ('VERIFICATION.json',) and not destination.exists():continue
    self.assertTrue(destination.is_file(),(path.name,target))
    if anchor:
     dest=destination.read_text()
     self.assertIn(f'id="{anchor}"',dest,(path.name,target))

 def test_11_small_additive_text_payload(self):
  for path in HERE.iterdir():
   self.assertFalse(path.is_symlink())
   self.assertIn(path.name,EXPECTED)
   if path.is_file():self.assertLess(path.stat().st_size,16*1024*1024)

 def test_12_nonreplication_limits_retained(self):
  text=(HERE/'MASTER-LIST.md').read_text()
  self.assertIn('not 134 independent errors',text)
  self.assertIn('not establish acquisition of Column 79 Model-9/Model-10',text)
  self.assertIn('not a physical collapse',text)

 def test_13_recovered_record_addendum(self):
  self.assertEqual([e['id'] for e in self.p['entries'][-3:]],['M132','M133','M134'])
  self.assertEqual(self.p['source_manifest']['request-2012-scan']['physical_pages'],4)
  self.assertEqual(self.p['source_manifest']['appeal-2014-scan']['physical_pages'],29)
  self.assertIn('native authentication',self.p['entries'][-2]['limit'])

def write_once(path,data):
 if path.exists():
  if path.read_bytes()==data:return
  raise FileExistsError(path.name)
 with path.open('xb') as f:f.write(data)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--record',action='store_true')
 args=parser.parse_args()
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PublicRegisterTests))
 if not result.wasSuccessful():raise SystemExit(1)
 if args.record:
  diffs=[]
  for path in sorted(HERE.glob('*.md')):
   p=subprocess.run(['git','diff','--no-index','--text','--','/dev/null',path.name],cwd=HERE,text=True,capture_output=True)
   assert p.returncode==1,path.name
   diffs.append(p.stdout)
  write_once(HERE/'TEXT-CHANGES.diff',''.join(diffs).encode())
  receipt={'date':'2026-10-25','command':'python3 -B verify_public.py --record',
   'tests_run':result.testsRun,'failures':0,'errors':0,'entries':load()['entry_count'],
   'scope':'Coverage, source pins, published excerpts, citation relocation, additive corrections and disclosure guards; not engineering validation.',
   'original_source_package':'Preserved locally; byte/word/URL comparison is a separate preparation check.',
   'pdf_layout':'Not applicable; no PDF created.',
   'remote_publication':'Not asserted by this precommit receipt; verify the actual resulting Git commit and remote files separately.'}
  write_once(HERE/'VERIFICATION.json',(json.dumps(receipt,indent=2)+'\n').encode())
  manifest={path.name:{'bytes':path.stat().st_size,'sha256':sha(path.read_bytes())}
    for path in sorted(HERE.iterdir()) if path.is_file() and path.name!='MANIFEST.json'}
  write_once(HERE/'MANIFEST.json',(json.dumps(manifest,indent=2)+'\n').encode())
 print(json.dumps({'tests':result.testsRun,'status':'passed','engineering_replication':False}))

if __name__=='__main__':main()
