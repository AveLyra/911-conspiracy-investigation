"""Check supplied locator accounting and optional original source bytes.

No independent OCR, interview/custody/voice authentication or claim that
missing source records never existed.
"""
import argparse,hashlib,json
from pathlib import Path

HERE=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--mirror',type=Path);p.add_argument('--official',type=Path);a=p.parse_args()
    manifest=json.loads((HERE/'BUNDLE-HASHES.json').read_text())
    for item in manifest['files']:
        b=(HERE/item['name']).read_bytes()
        assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],item['name']
    sources=json.loads((HERE/'SOURCES.json').read_text());checked=[]
    for key,path in [('mirror',a.mirror),('official',a.official)]:
        if path:
            b=path.read_bytes();pin=sources[key]
            assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256']
            checked.append(key)
    d=json.loads((HERE/'FOOTER-MAP.json').read_text());rows=d['rows']
    assert [r['physical_page']for r in rows]==list(range(1,74))
    accepted=[r['printed_footer']for r in rows if r['printed_footer'] is not None]
    assert len(accepted)==70 and len(set(accepted))==70
    assert all(r['printed_footer']is None for r in rows[:3])
    assert rows[69]['printed_footer']=='000000768' and rows[70]['printed_footer']=='000000770'
    assert rows[71]['printed_footer']=='000000771' and rows[72]['printed_footer']=='000000772'
    assert '000000769'not in accepted
    assert rows[51]['printed_footer']=='000000740'
    assert rows[56]['printed_footer']=='000000753'
    assert rows[67]['printed_footer']=='000000766' and rows[69]['printed_footer']=='000000768'
    observations=json.loads((HERE/'OBSERVATIONS.json').read_text())
    dates=next(x for x in observations if x['id']=='PD05')
    assert dates['investigation_raw']=='06/10/2001' and dates['transcription_raw']=='06/28/2002'
    assert dates['preferred_year_selected']is False
    print(json.dumps(dict(bundle_hashes_match=True,source_entities_checked=checked,
          supplied_footer_positions_accounted=73,accepted_footer_readings=70,
          handwritten_unbates_faces=[1,2,3],supplied769notlocated=True,
          critical_prior_locators_preserved=True,conflicting_date_strings_preserved=True,
          scope='Integrity and internal accounting of supplied visual readings; does not independently read images, authenticate historical interviews/calls/collector/custody, prove a cause for gaps/date fields or recover a disposition.'),indent=2))

if __name__=='__main__':main()
