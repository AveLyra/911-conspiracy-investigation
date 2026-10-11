"""Read-only independent raw-response diagnostic; writes JSON only to stdout.

No imports of root/previous extractors. Missing folder_name is quarantined,
never synthesized; any other unknown schema exception raises an error.
"""
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import sys

FIELDS = ('mes:key', 'title', 'source', 'agency', 'box_name', 'folder_name',
          'page_count', 'pdf_size', 'production_volume', 'production_end', 'mes:date')
LABELS = ('penn', 'penn_phrase', 'apt', 'transient', 'date_slash', 'date_words',
          'load_shedding', 'fuel_pump', 'break_glass', 'control')

def require(ok, why):
    if not ok:
        raise ValueError(why)

def pairs_unique(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, f'duplicate JSON key {key}')
        out[key] = value
    return out

def load(path):
    raw = path.read_bytes()
    value = json.loads(raw, object_pairs_hook=pairs_unique,
                       parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    return value, {'file': path.name, 'bytes': len(raw),
                   'sha256': hashlib.sha256(raw).hexdigest()}

def positive_integral(value):
    return (type(value) in (int, float) and math.isfinite(value)
            and value > 0 and value == int(value))

def parse_record(row):
    require(isinstance(row, dict), 'row not object')
    props = row['properties']
    require(isinstance(props, list), 'properties not list')
    raw, values = {}, {}
    for p in props:
        require(isinstance(p, dict) and set(p) == {'id', 'name', 'data'}, 'property shape')
        key = p['id']
        require(key in FIELDS and key not in raw, 'unknown/duplicate property')
        require(type(p['name']) is str and p['name'], 'property display name')
        require(isinstance(p['data'], list) and len(p['data']) == 1, 'non-scalar data')
        entry = p['data'][0]
        require(isinstance(entry, dict) and set(entry) == {'value'}, 'data entry shape')
        v = entry['value']
        if key in ('pdf_size', 'mes:date'):
            expected = {'num', 'unit'} if key == 'mes:date' else {'num'}
            require(isinstance(v, dict) and set(v) == expected, 'numeric scalar shape')
            require(positive_integral(v['num']), 'invalid numeric scalar')
            if key == 'mes:date':
                require(v['unit'] == 'ms_since_1970', 'date unit')
            values[key] = v['num']
        else:
            require(isinstance(v, dict) and set(v) == {'str'}, 'string scalar shape')
            require(type(v['str']) is str and len(v['str']) > 0, 'invalid string scalar')
            values[key] = v['str']
        raw[key] = p
    missing = sorted(set(FIELDS) - set(raw))
    require(missing in ([], ['folder_name']), f'unknown missingness {missing}')
    key = values['mes:key']
    require(re.fullmatch(r'NYC-WTC_[0-9]{9}', key) is not None, 'malformed key')
    require(values['title'] == key + '.pdf', 'title/key mismatch')
    require(row['id'] == 'september11 Connector:September11_MD:' + key + ':', 'connector ID mismatch')
    require(values['source'] == 'WTC 7', 'source mismatch')
    require(re.fullmatch(r'[1-9][0-9]*', values['page_count']) is not None, 'page count')
    require(re.fullmatch(r'NYC-WTC_[0-9]{9}', values['production_end']) is not None, 'end ID')
    pages = int(values['page_count'])
    require(int(values['production_end'][-9:]) - int(key[-9:]) + 1 == pages, 'Bates extent/page mismatch')
    return {'id': key, 'source_result_id': row['id'], 'fields': values,
            'raw_properties': raw, 'missing_properties': missing,
            'strict_valid': not missing, 'page_count_derived': pages,
            'pdf_size_derived': int(values['pdf_size'])}

def parse_response(label, query, request, response):
    require(request == {'user': {'query': {'unparsed': query}}, 'count': 50,
                       'content_sample_length': 0,
                       'properties': [{'name': f, 'formats': ['VALUE']} for f in FIELDS]}, 'request mismatch')
    echo = copy.deepcopy(response['search_request'])
    extra = {}
    if 'user_context' in echo and 'user_context' not in request:
        require(echo['user_context'] == {}, 'nonempty echo context')
        extra['user_context'] = echo.pop('user_context')
    require(echo == request, 'echo mismatch')
    estimate = response['estimated_count']
    require(type(estimate) is int and estimate >= 0, 'estimate type/range')
    rs = response['resultset']
    require(type(rs['next_avail']) is bool and type(rs['prev_avail']) is bool, 'paging booleans')
    present = 'results' in rs
    if not present:
        require(estimate == 0 and rs['next_avail'] is False, 'unsafe missing results')
    rows = rs.get('results', [])
    require(isinstance(rows, list) and len(rows) <= 50, 'results type/cap')
    require(estimate >= len(rows), 'estimate smaller than returned')
    records, seen = [], set()
    for ordinal, row in enumerate(rows, 1):
        record = parse_record(row)
        require(record['id'] not in seen, 'duplicate result ID')
        seen.add(record['id'])
        record['ordinal'] = ordinal
        records.append(record)
    services = rs.get('per_service_dataset', [])
    require(isinstance(services, list), 'service dataset type')
    causes = [s.get('termination_cause') for s in services]
    complete = (not rs['next_avail'] and not rs['prev_avail'] and estimate == len(rows)
                and bool(causes) and all(c == 'NO_MORE_RESULTS' for c in causes))
    return {'label': label, 'query': query, 'request_echo_matches_supplied_fields': True,
            'server_added_echo_fields': extra, 'estimated_count': estimate,
            'returned_count': len(rows), 'page_sum': sum(x['page_count_derived'] for x in records),
            'strict_valid_count': sum(x['strict_valid'] for x in records),
            'quarantined_count': sum(not x['strict_valid'] for x in records),
            'next_avail': rs['next_avail'], 'prev_avail': rs['prev_avail'],
            'termination_causes': causes, 'results_key_present': present,
            'complete_query_response': complete, 'ids_in_returned_order': [x['id'] for x in records]}, records

def merge(unique, record, label):
    key = record['id']
    member = {'query': label, 'ordinal': record['ordinal']}
    stored = {k: v for k, v in record.items() if k != 'ordinal'}
    if key in unique:
        require({k: v for k, v in unique[key].items() if k != 'memberships'} == stored,
                f'cross-query conflict {key}')
        unique[key]['memberships'].append(member)
    else:
        unique[key] = dict(stored, memberships=[member])

def extract(base):
    queries, qpin = load(base / 'queries.json')
    require(tuple(queries) == LABELS, 'query population/order')
    pins, covers, unique, exceptions = [qpin], [], {}, []
    for label in LABELS:
        request, rpin = load(base / (label + '-request.json'))
        response, spin = load(base / (label + '-response.json'))
        pins.extend((rpin, spin))
        cover, records = parse_response(label, queries[label], request, response)
        covers.append(cover)
        for record in records:
            merge(unique, record, label)
            if not record['strict_valid']:
                exceptions.append({'query': label, 'ordinal': record['ordinal'],
                                   'id': record['id'], 'missing_properties': record['missing_properties']})
    require(covers[-1]['ids_in_returned_order'] == ['NYC-WTC_000167873'], 'control failed')
    records = [unique[k] for k in sorted(unique)]
    # Recheck exactly the same input bytes after extraction, no source edits.
    for pin in pins:
        _, current = load(base / pin['file'])
        require(current == pin, 'input changed during extraction')
    return {'kind': 'independent_diagnostic_not_full_contract_pass',
            'strict_contract_passed': not exceptions, 'input_pins': pins,
            'queries': covers, 'exceptions': exceptions, 'records': records,
            'totals': {'queries': len(covers), 'occurrences': sum(c['returned_count'] for c in covers),
                       'occurrence_pages': sum(c['page_sum'] for c in covers),
                       'strict_valid_occurrences': sum(c['strict_valid_count'] for c in covers),
                       'quarantined_occurrences': len(exceptions), 'unique_ids': len(records),
                       'unique_pages': sum(r['page_count_derived'] for r in records),
                       'strict_valid_unique': sum(r['strict_valid'] for r in records),
                       'quarantined_unique': sum(not r['strict_valid'] for r in records)}}

def selftest():
    q = 'synthetic'
    req = {'user': {'query': {'unparsed': q}}, 'count': 50, 'content_sample_length': 0,
           'properties': [{'name': f, 'formats': ['VALUE']} for f in FIELDS]}
    vals = {'mes:key':'NYC-WTC_000000001','title':'NYC-WTC_000000001.pdf','source':'WTC 7',
            'agency':'test','box_name':'test','folder_name':'None','page_count':'1',
            'pdf_size':1,'production_volume':'test','production_end':'NYC-WTC_000000001','mes:date':1}
    props = []
    for f, v in vals.items():
        value = {'num':v} if type(v) is int else {'str':v}
        if f == 'mes:date': value['unit'] = 'ms_since_1970'
        props.append({'id':f,'name':f,'data':[{'value':value}]})
    row = {'id':'september11 Connector:September11_MD:NYC-WTC_000000001:', 'properties':props}
    rsp = {'estimated_count':1,'search_request':dict(req,user_context={}),
           'resultset':{'results':[row],'next_avail':False,'prev_avail':False,
                        'per_service_dataset':[{'termination_cause':'NO_MORE_RESULTS'}]}}
    checks = []
    c, rr = parse_response('s',q,req,rsp); require(c['complete_query_response'], 'positive'); checks.append('valid')
    absent = copy.deepcopy(rsp); absent['resultset']['results'][0]['properties'] = [p for p in props if p['id'] != 'folder_name']
    c, rr = parse_response('s',q,req,absent); require(c['quarantined_count']==1 and 'folder_name' not in rr[0]['fields'], 'quarantine'); checks.append('missing folder quarantined')
    empty = copy.deepcopy(rsp); empty['estimated_count']=0; del empty['resultset']['results']
    require(parse_response('s',q,req,empty)[0]['complete_query_response'], 'empty'); checks.append('absent zero results')
    for change in ('next','prev','count','cause','missing_cause'):
        r=copy.deepcopy(rsp)
        if change=='next': r['resultset']['next_avail']=True
        if change=='prev': r['resultset']['prev_avail']=True
        if change=='count': r['estimated_count']=2
        if change=='cause': r['resultset']['per_service_dataset'][0]['termination_cause']='COUNT_LIMIT'
        if change=='missing_cause': del r['resultset']['per_service_dataset']
        require(not parse_response('s',q,req,r)[0]['complete_query_response'], change); checks.append('incomplete '+change)
    bad = []
    r=copy.deepcopy(rsp); r['resultset']['results'].append(copy.deepcopy(row)); r['estimated_count']=2; bad.append(('duplicate ID',r))
    r=copy.deepcopy(rsp); r['search_request']['count']=49; bad.append(('echo mismatch',r))
    r=copy.deepcopy(rsp); r['estimated_count']=0; bad.append(('estimate below rows',r))
    r=copy.deepcopy(rsp); r['resultset']['results'][0]['properties'].append(copy.deepcopy(props[0])); bad.append(('duplicate property',r))
    r=copy.deepcopy(rsp); r['resultset']['results'][0]['properties'][0]['data'].append({'value':{'str':'x'}}); bad.append(('nonscalar',r))
    r=copy.deepcopy(empty); r['estimated_count']=1; bad.append(('unsafe absent results',r))
    for name,r in bad:
        try: parse_response('s',q,req,r)
        except ValueError: checks.append('refused '+name)
        else: raise ValueError('not refused '+name)
    unique={}; rec=parse_record(row); rec['ordinal']=1; merge(unique,rec,'s')
    changed=copy.deepcopy(rec); changed['fields']['agency']='different'
    try: merge(unique,changed,'s2')
    except ValueError: checks.append('refused cross-query conflict')
    else: raise ValueError('conflict accepted')
    print(json.dumps({'synthetic_checks':len(checks),'results':checks}))

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--selftest': selftest()
    else: print(json.dumps(extract(Path(__file__).resolve().parent),ensure_ascii=False,separators=(',',':')))
