"""Compare minimized frozen derivatives only; never open native sources."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROLES = {
    'MP': [('label','Lab'),('material','MAT')]+[(f'c{i}',f'C{i}') for i in range(5)],
    'MPDATA': [('label','Lab'),('material','MAT'),('start','SLOC')]+[(f'c{i}',f'C{i}') for i in range(1,7)],
    'MPTEMP': [('start','SLOC')]+[(f't{i}',f'T{i}') for i in range(1,7)],
    'TB': list(zip(('label','material','ntemp','npts','option','unused','function'),('Lab','MATID','NTEMP','NPTS','TBOPT','reserved','FuncName'))),
    'TBTEMP': [('temperature','TEMP'),('kmod','KMOD')],
    'TBDATA': [('start','STLOC')]+[(f'c{i}',f'C{i}') for i in range(1,7)],
    'ET': [('local_type','ITYPE'),('library_code','ENAME')]+[(f'kop{i}',f'KOP{i}') for i in range(1,7)]+[('inopr','INOPR')],
}


def compare(a,b):
    # No silent fallback for whole-row malformed forms: a future occurrence
    # needs an explicit comparison rule, not conversion to a passing row.
    assert len(a)==len(b)
    assert len({(r['line'],r['segment']) for r in a})==len(a)
    assert len({(r['line'],r['segment']) for r in b})==len(b)
    fields=0
    for x,y in zip(a,b):
        for key in ('line','segment','command','segment_sha256','argument_count'):
            assert x[key]==y[key]
        assert x['status'] in ('literal_fields','unresolved_fields')
        assert y['status']==('decoded' if x['status']=='literal_fields' else 'unresolved')
        assert y['reasons']==([] if x['status']=='literal_fields' else ['unresolved_field'])
        assert not y['extra_nonblank']
        roles=ROLES[x['command']]
        assert len(x['fields'])==len(y['fields'])==len(roles)
        for xf,yf,(xr,yr) in zip(x['fields'],y['fields'],roles):
            assert xf['role']==xr and yf['field']==yr
            assert xf['kind']==('integer' if yf['kind']=='id' else yf['kind'])
            kind=xf['kind']
            assert kind in ('blank','label','integer','number','unresolved')
            if kind=='unresolved':
                assert xf['sha256']==yf['sha256']
            elif kind!='blank':
                assert xf['lexeme' if kind in ('integer','number') else 'value']==yf['value']
            fields+=1
        extras=max(x['argument_count']-len(roles),0)
        assert x['trailing_extra_blanks']==extras
        tail=extras
        for f in reversed(x['fields'][:min(x['argument_count'],len(roles))]):
            if f['kind']!='blank':
                break
            tail+=1
        assert y['trailing_blank_count']==tail
    return fields


def perturbation_checks(a,b):
    """Deliberately corrupt cloned derivative rows; never change saved inputs."""
    mutations = [
        lambda x,y: y[0].update(line=y[0]['line']+1),
        lambda x,y: y[0].update(segment_sha256='0'*64),
        lambda x,y: y[0].update(argument_count=99),
        lambda x,y: y[0].update(status='decoded'),
        lambda x,y: y[0]['fields'][0].update(value='999'),
        lambda x,y: y[0]['fields'][0].update(field='wrong_role'),
        lambda x,y: y[0]['fields'][1].update(sha256='0'*64),
        lambda x,y: y[0].update(trailing_blank_count=99),
        lambda x,y: y.pop(),
        lambda x,y: (x.append(deepcopy(x[0])),y.append(deepcopy(y[0]))),
    ]
    for mutate in mutations:
        x,y=deepcopy(a[:1]),deepcopy(b[:1])
        mutate(x,y)
        try:
            compare(x,y)
        except AssertionError:
            continue
        raise AssertionError('perturbation_not_detected')
    return len(mutations)


def main():
    payloads=[(HERE/n).read_bytes() for n in ('producer-run01.json','producer-run02.json','independent-run03.json','independent-run04.json')]
    assert payloads[0]==payloads[1] and payloads[2]==payloads[3]
    p,o=json.loads(payloads[0]),json.loads(payloads[2])
    assert p['status']=='PASS' and o['status']=='ok'
    assert p['protocol_sha256']==o['protocol_sha256']
    assert p['manifest_sha256']==o['manifest_sha256']
    a,b=p['result'],o['result']
    assert a['source_sha256']==b['source_sha256']
    assert a['bytes']==b['byte_count']==212384
    assert a['lines']==b['physical_lines']==5474
    fields=compare(a['rows'],b['selected_rows'])
    controls=perturbation_checks(a['rows'],b['selected_rows'])
    counts=Counter(r['command'] for r in a['rows'])
    assert all(a['commands'][c]==b['counts'][c]==n for c,n in counts.items())
    assert len(a['rows'])==233 and fields==1578
    print(json.dumps({'status':'PASS','selected_rows':len(a['rows']),'fields':fields,'perturbation_checks':controls,
                      'selected_counts':dict(sorted(counts.items())),
                      'statuses':dict(Counter(r['status'] for r in a['rows'])),
                      'producer_sha256':hashlib.sha256(payloads[0]).hexdigest(),
                      'independent_sha256':hashlib.sha256(payloads[2]).hexdigest()},sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except Exception:
        print('{"status":"FAIL","code":"comparison"}')
        raise SystemExit(1)
