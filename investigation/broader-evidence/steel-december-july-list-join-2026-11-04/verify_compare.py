"""Reproduce literal row/string accounting from preserved ledgers; no object-identity or loss inference."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
from pypdf import PdfReader
DEC_LEDGER_SHA='662deb4043786fe6def1eb4d34e5bf390b903b599d6f7d4e5dff6c807af8a95d'
JUL_LEDGER_SHA='6d60fd5e30f77662d4fb77a47bdc5c48e49b27b7818ba317e1a64b0580067475'
SOURCES={
 'december_source':('fd1eeb230cdba27ffc4bde627b208fcce24fc6dc7c4d7f27eca5e34f9de1119d',224690,9),
 'july_ledger_source':('f2696cfeab6ca20d807923afbe9c0c8ad86e13612b56aa2bc2a64311f8dd1a75',61333079,533),
 'july_paired_counterpart':('d28acba7420a8273e5d797e36f2a60f65bfa1b219505c4f641f04b674883dbdf',148109,11)
}
def checked_ledger(path,sha):
 raw=Path(path).read_bytes();assert hashlib.sha256(raw).hexdigest()==sha
 return json.loads(raw)
def summarize(rows):
 c=Counter(x['identifier_verbatim'] for x in rows)
 return {'rows':len(rows),'distinct_exact_cells':len(c),'per_source_page':dict(sorted(Counter(x['physical_pdf_page'] for x in rows).items())),
         'repeated_exact_cells':{k:v for k,v in sorted(c.items()) if v>1},
         'literal_first_hyphen_prefix_counts':dict(sorted(Counter(x['identifier_verbatim'].split('-',1)[0] for x in rows).items()))}
def compare(december_ledger,july_ledger,**source_paths):
 d=checked_ledger(december_ledger,DEC_LEDGER_SHA);j=checked_ledger(july_ledger,JUL_LEDGER_SHA)
 verified=[]
 for name,spec in SOURCES.items():
  path=source_paths[name];raw=Path(path).read_bytes();sha,size,pages=spec
  assert len(raw)==size and hashlib.sha256(raw).hexdigest()==sha
  assert len(PdfReader(path).pages)==pages
  verified.append({'source_role':name,'sha256':sha,'bytes':size,'PDF_pages':pages})
 for rows,expected_pages in [(d,set(range(3,10))),(j,set(range(69,78)))]:
  assert set(x['physical_pdf_page'] for x in rows)==expected_pages
  assert [x['ledger_row'] for x in rows]==list(range(1,len(rows)+1))
  for p in expected_pages:
   page=[x for x in rows if x['physical_pdf_page']==p]
   assert [x['identifier_row_on_page'] for x in page]==list(range(1,len(page)+1))
  assert all(x['identifier_verbatim'] and x['identifier_verbatim']==x['identifier_verbatim'].strip() for x in rows)
 assert all(x['source_field'] in ['Inventory Archive Item Number','NIST Number'] for x in d)
 assert all(x['source_field']=='NIST Number' for x in d if x['physical_pdf_page']==9)
 assert all(x['source_field']=='Inventory Archive Item Number' for x in d if x['physical_pdf_page']<8)
 D=Counter(x['identifier_verbatim'] for x in d);J=Counter(x['identifier_verbatim'] for x in j)
 common=sorted(D.keys()&J.keys());d_only=sorted(D.keys()-J.keys());j_only=sorted(J.keys()-D.keys())
 assert len(D)==len(common)+len(d_only) and len(J)==len(common)+len(j_only)
 exact_groups={'exact_common_cells':common,'December_only_exact_cells':d_only,'July_only_exact_cells':j_only,
               'comparison_rule':'Case-sensitive complete identifier-cell strings only; no padding, alias resolution, annotation removal, lowercasing or object equivalence.'}
 matches=[]
 for label in common:
  matches.append({'identifier_verbatim':label,'December_positions':[x for x in d if x['identifier_verbatim']==label],
                 'July_prior_ledger_positions':[x for x in j if x['identifier_verbatim']==label]})
 targets={label:{'December_positions':[x for x in d if x['identifier_verbatim']==label],
                 'July_prior_ledger_positions':[x for x in j if x['identifier_verbatim']==label]}
          for label in ['H-0012','G-0006','I-0137']}
 summary={'December':summarize(d),'July_prior_ledger':summarize(j),
          'December_source_field_counts':dict(sorted(Counter(x['source_field'] for x in d).items())),
          'July_NIST_prefixed_rows':sum(x['identifier_verbatim'].startswith('NIST-') for x in j),
          'exact_common_cell_count':len(common),'December_only_exact_cell_count':len(d_only),'July_only_exact_cell_count':len(j_only),
          'exact_common_cells':common,'paired_positions':matches,'target_literal_lookups':targets,
          'source_entity_checks':verified,'ledger_SHA256s':{'December':DEC_LEDGER_SHA,'July_prior':JUL_LEDGER_SHA},
          'manual_reading_is_not_proven_by_code':True,
          'not_measured':['physical objects','lost or destroyed specimens','native inventory aliases','building origin','same specimen between dates','laboratory outcome','current legal rights'],
          'July_counterpart_scope':'Only selected counterpart rows read; complete July ledger comes from the separately pinned Clearwater packet, not assumed whole-copy equivalence.'}
 return summary,exact_groups
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ['december-ledger','july-ledger','december-source','july-ledger-source','july-paired-counterpart']:p.add_argument('--'+name,required=True)
 a=p.parse_args();summary,groups=compare(a.december_ledger,a.july_ledger,december_source=a.december_source,july_ledger_source=a.july_ledger_source,july_paired_counterpart=a.july_paired_counterpart)
 print(json.dumps({'summary':summary,'exact_groups':groups},indent=2))
