"""Preserve the preceding public master and its exact qualified supplement."""
import hashlib
import json
import re

REL = 'revisions/2026-11-04-assistance-and-search-recheck'
PRECEDING_SHA256 = '94b97b034745240c84f36c17790e47ad8f3400752c344a913e0d7a3954d9d9bb'
ADDITION_SHA256 = '2c299177b94153ccaf3eaae94cbfb5edc704ebe0d0c0de7f3c3e4e6bc2911fbc'
sha = lambda raw: hashlib.sha256(raw).hexdigest()

def preceding_master(root):
    update = json.loads((root / REL / 'UPDATE.json').read_text())
    addition = (root / REL / 'ADDITION.md').read_bytes()
    current = (root / 'MASTER-LEADS.md').read_bytes()
    assert update['reader'] == 'MASTER-LEADS.md'
    assert update['before_sha256'] == PRECEDING_SHA256
    assert update['addition_sha256'] == ADDITION_SHA256 == sha(addition)
    assert len(addition) and current.endswith(addition), 'Exact supplement missing or changed'
    before = current[:-len(addition)]
    assert len(before) == update['before_bytes'] and sha(before) == PRECEDING_SHA256, 'Preceding public master changed'
    assert sha(current) == update['current_sha256']
    return before

def verify_supplement(root):
    checks = []
    def check(name, ok):
        checks.append({'name': 'Assistance/search supplement ' + name, 'passed': bool(ok)})
    try:
        before = preceding_master(root)
        check('exact preceding master and canonical addition preserved', True)
    except (AssertionError, OSError, ValueError, KeyError):
        check('exact preceding master and canonical addition preserved', False)
        return checks
    text = (root / REL / 'ADDITION.md').read_text()
    expected = {'assistance-and-search-recheck-2026-11-04'} | {f'recheck-2026-11-04-{i:02}' for i in range(1, 5)}
    actual = re.findall(r'<a id="([^"]+)"', text)
    check('five distinct new anchors without older ID changes', len(actual) == len(expected) and set(actual) == expected and not set(actual).intersection(re.findall(r'<a id="([^"]+)"', before.decode())))
    for i in range(1, 5):
        anchor = f'<a id="recheck-2026-11-04-{i:02}"></a>'
        block = text.split(anchor, 1)[1].split('<a id=', 1)[0]
        check(f'all evidence contrary findings TODOs and citations in recheck {i}', all(label in block for label in ['**Observed record:**', '**Contrary findings and limits:**', '**Open TODO / discriminating test:**', '**Primary citation:**']))
    check('court preliminary scope and rejected video interpretations', all(v in text for v in ['for jurisdictional purposes', 'Physical page 42 rejects', 'reserves disputed motive', 'not a final merits judgment']))
    check('FBI affirmative contrary finding and scoped count correction', all(v in text for v in ['did not knowingly conspire', 'insufficient for prosecution', 'September 8, 2021', '60 interviews during 2007–2016', 'not a count of every PENTTBOM interview']))
    check('access restriction rationale alternatives and missing originals', all(v in text for v in ['future informant recruitment', 'separate refusal and immunity condition', 'original requests, refusal letters', 'competing explanation']))
    check('search copy-deletion scope legal distinction and negative foreknowledge finding', all(v in text for v in ["deletion concerned Scott's copy", 'no legal barrier', 'routine precedence', 'no evidence of specific intelligence about the September 11 plot']))
    check('no new owning IDs empirical result or request adopted', all(v in text for v in ['175 M IDs and 481 owning source-finding objects remain unchanged', 'not four additional independent anomalies', 'No numerical conspiracy probability', 'completed records request']))
    check('four original primary-source routes retained', all(v in text for v in ['https://www.nysd.uscourts.gov/sites/default/files/2025-08/03-md-01570%2011182.pdf#page=40', 'https://vault.fbi.gov/9-11-attacks-investigation-and-related-materials/', 'https://www.govinfo.gov/content/pkg/GPO-CRPT-107srpt351/pdf/GPO-CRPT-107srpt351.pdf#page=837', 'https://oig.justice.gov/sites/default/files/archive/special/0506/chapter5.htm']))
    check('public revision checklist available', (root / REL / 'REVIEW.md').is_file())
    return checks
