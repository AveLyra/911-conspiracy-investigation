"""Verify two public content packages, preserving their scope and dependencies."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
OTHER=HERE.parent/'operational-record-followup-2026-10-26'


def pin(path):
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


def verify():
    checks=[]
    total=0
    for root in [HERE,OTHER]:
        manifest=json.loads((root/'MANIFEST.json').read_text())
        actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
                and str(p.relative_to(root)) not in {'MANIFEST.json','VERIFICATION.json'}}
        assert actual==set(manifest),(root.name,actual-set(manifest),set(manifest)-actual)
        for name,expected in manifest.items():
            path=root/name
            assert pin(path)==expected,(root.name,name)
            assert path.suffix in {'.md','.json','.py','.diff','.txt'},path
        total+=len(manifest)
    checks.append('both public file sets and all manifest SHA-256/length pins match; raw PDFs/media excluded')

    scope=json.loads((HERE/'PUBLICATION-SCOPE.json').read_text())
    for row in scope['exact_native_copies']:
        root=HERE if row['package']==HERE.name else OTHER
        assert pin(root/row['public_path'])==row['pin'],row['public_path']
    checks.append('selected native reports, protocols, ledgers, diffs and published snapshots match preservation pins')

    rf=json.loads((OTHER/'findings.json').read_text())['findings']
    assert [r['id'] for r in rf]==[f'RF{i:03}' for i in range(1,9)]
    bp=json.loads((HERE/'integrated-findings.json').read_text())['findings']
    assert [r['id'] for r in bp]==[f'BP{i:02}' for i in range(1,11)]
    original=json.loads((OTHER/'targets.json').read_text())
    updated=json.loads((HERE/'targets-v2.json').read_text())
    assert updated['targets'][1:]==original['targets'][1:]
    assert len(updated['bank_phone_original_targets'])==10
    assert 'BR04 remains unchanged and open' in updated['cross_track_safeguards']['BR04']
    checks.append('eight RF findings, ten BP findings and ten BPR targets retained; other four bundles unchanged')

    r=subprocess.run([sys.executable,'-B',str(HERE/'sources/published/verify_public.py')],check=True,capture_output=True,text=True)
    prior=json.loads(r.stdout)
    assert prior['public_files']==15 and prior['selected_window_rows']==27
    assert prior['carrier_rows']==8 and prior['carrier_billed_minutes']==42
    recount=json.loads((HERE/'recount-verification.json').read_text())
    assert [recount[k] for k in ['all_labelled_table_rows','date_window_rows',
           'window_rows_involving_BAYOUMI_2','window_rows_involving_BAYOUMI_4']]==[67,27,21,6]
    checks.append('fifteen-file prior publication validates; confirming carrier sample and unresolved count comparison retained')

    links=0
    for root in [HERE,OTHER]:
        for path in root.glob('*.md'):
            for link in re.findall(r'\]\(([^\s]+)\)',path.read_text()):
                if link.startswith(('https://','http://','#')):
                    continue
                assert (path.parent/link.split('#')[0]).is_file(),(path.name,link)
                links+=1
    report=(HERE/'REPORT.md').read_text()
    for token in ['April19','April20','22 calls','27 rows','$1,558','1A','June23','$100,000']:
        assert token in report,token
    checks.append('public document links resolve and material conflicting values/open-question distinctions remain')
    return {'date':'2026-10-26','status':'passed','checks':checks,
            'content_files_checked':total,'relative_links_checked':links,
            'RF_findings':8,'BP_findings':10,'BPR_targets':10,
            'limits':'Publication integrity/coverage checks only, not historical, legal or scientific validation; remote publication checked separately.'}


if __name__=='__main__':
    print(json.dumps(verify()))
