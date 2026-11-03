"""Compare supplied carrier-printout readings, never identify a historical call.

Native mode reads csc_accepted strings; public mode reads only derived group
aliases. Neither mode independently reads images or authenticates schema/clocks.
"""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

def key(row):
    return row.get('csc_accepted', row.get('accepted_csc_group'))

def same_key(a, b):
    return key(a) is not None and key(b) is not None and key(a) == key(b)

def members(rows):
    groups = {}
    for row in rows:
        if key(row) is not None:
            groups.setdefault(key(row), []).append(row['record_number'])
    return sorted(sorted(v) for v in groups.values())

def clock_seconds(value):
    hh, mm, ss = map(int, value.split(':'))
    assert 0 <= hh < 24 and 0 <= mm < 60 and 0 <= ss < 60
    return hh*3600+mm*60+ss

def analyze(rows):
    assert [r['record_number'] for r in rows] == list(range(1, 24))
    assert all(isinstance(r['duration_field'], int) and r['duration_field'] >= 0 for r in rows)
    groups, labels = {}, {}
    for r in rows:
        k = key(r)
        if k is not None:
            labels.setdefault(k, f'K{len(labels)+1:02d}')
            groups.setdefault(labels[k], []).append(r)
    details = []
    for label, selected in groups.items():
        details.append(dict(alias=label,records=[r['record_number'] for r in selected],
                            printed_starts=list(dict.fromkeys(r['printed_start'] for r in selected)),
                            duration_fields=[r['duration_field'] for r in selected],
                            event_codes=[r['event_code'] for r in selected],
                            both_zero_and_positive=any(r['duration_field']==0 for r in selected) and
                                                   any(r['duration_field']>0 for r in selected)))
    routed_pairs = []
    for r in rows:
        if r['event_code'] == 29:
            positive = [x['record_number'] for x in rows if same_key(r, x) and x['duration_field']>0]
            routed_pairs.append(dict(routed_record=r['record_number'],routed_duration=r['duration_field'],
                                     positive_same_accepted_csc=positive))
    anchors = []
    for r in rows:
        if r['duration_field'] > 0:
            bill = clock_seconds(r['event_time'])-clock_seconds(r['billing_start'])
            answer = clock_seconds(r['event_time'])-clock_seconds(r['answer_supervision'])
            anchors.append(dict(record=r['record_number'],duration_field=r['duration_field'],
                                printed_event_minus_billing_seconds=bill,
                                printed_event_minus_answer_seconds=answer,
                                numeric_duration_matches_billing_span=r['duration_field']==bill,
                                numeric_duration_matches_answer_span=r['duration_field']==answer))
    # Actual source/equality controls and counterfactuals; not historical tests.
    assert same_key(rows[3], rows[6])
    assert not same_key(rows[3], rows[7])
    altered = deepcopy(rows[6])
    if 'csc_accepted' in altered:
        altered['csc_accepted'] = str(key(altered))+'-SYNTHETIC-ALTERATION'
    else:
        altered['accepted_csc_group'] = str(key(altered))+'-SYNTHETIC-ALTERATION'
    assert altered['printed_start']==rows[3]['printed_start'] and not same_key(rows[3], altered)
    assert members(rows)==members(list(reversed(rows)))
    missing = deepcopy(rows[0]);other = deepcopy(rows[0])
    missing['csc_accepted']=None;other['csc_accepted']=None
    assert not same_key(missing,other)
    return dict(record_count=len(rows),reader_pages=sorted({p for r in rows for p in r['reader_pages']}),
                printed_start_labels_in_source_order=list(dict.fromkeys(r['printed_start'] for r in rows)),
                accepted_csc_record_count=sum(key(r) is not None for r in rows),
                accepted_csc_groups=len(groups),
                unaccepted_csc_records=[r['record_number'] for r in rows if key(r) is None],
                full_gs_exact_equalities_tested=False,
                event_code_counts=dict(sorted(Counter(r['event_code'] for r in rows).items())),
                zero_duration_records=[r['record_number'] for r in rows if r['duration_field']==0],
                positive_duration_records=[r['record_number'] for r in rows if r['duration_field']>0],
                groups=details, routed_records_and_positive_same_csc=routed_pairs,
                positive_anchor_comparisons=anchors,
                unresolved_event_time_records=[r['record_number'] for r in rows if r['event_time'] is None],
                all_zero_rows_have_printed_1969_billing_and_answer=all(
                    r['billing_start']=='Wed Dec 31 18:00:00 1969' and r['answer_supervision']=='Wed Dec 31 18:00:00 1969'
                    for r in rows if r['duration_field']==0),
                controls=dict(accepted_equal_pair=True,unequal_pair=True,
                              changed_key_same_time_not_joined=True,
                              reversed_input_same_memberships=True,
                              two_missing_keys_not_joined=True),
                scope='Calculations on manually supplied fields. CSC-only accepted comparisons; no full GS, raw/native release, system allocation rule, calibrated elapsed time, carrier-leg/caller/conversation or independent source-image authentication.')

def safe_rows(rows):
    groups = {}
    safe = []
    for row in rows:
        r = deepcopy(row)
        k = r.pop('csc_accepted')
        if k is not None:
            groups.setdefault(k, f'K{len(groups)+1:02d}')
        r['accepted_csc_group'] = groups.get(k) if k is not None else None
        safe.append(r)
    return safe

if __name__ == '__main__':
    source = Path(sys.argv[1]);data=json.loads(source.read_text())
    rows=data['records']
    result=analyze(rows)
    with Path(sys.argv[2]).open('x') as out:
        json.dump(result,out,indent=2);out.write('\n')
    if len(sys.argv)>3:
        with Path(sys.argv[3]).open('x') as out:
            json.dump(dict(records=safe_rows(rows),source_reading_status='Manual readings, derived aliases; raw CSC/GS/contact/card identifiers excluded.',private_input_sha256=hashlib.sha256(source.read_bytes()).hexdigest()),out,indent=2);out.write('\n')
    print(json.dumps({k:result[k] for k in ['record_count','accepted_csc_record_count',
                     'accepted_csc_groups','unaccepted_csc_records','positive_duration_records']},indent=2))
