"""Compare safe manual MFR readings with preserved earlier transcriptions.

Usage: python3 compare_briefing_rows.py SAFE-MFR-ROWS.json PRIOR-READINGS.json NEW-RESULT.json
No network, source modification or caller identity inference. A match is a candidate
source association, not authenticated event identity. Test scope is the supplied
readings; glyph accuracy and native switching semantics require other evidence.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import sys

new_path, old_path, output_path = map(Path, sys.argv[1:])
new = json.loads(new_path.read_text())
old = json.loads(old_path.read_text())


def time_key(label):
    """Parse components only for comparison; preserve source strings in output."""
    return tuple(map(int, label.split(':')))


u175 = []
for row in new['UA175']:
    candidates = [p for p in old['UA175']
                  if time_key(row['time_label']) == time_key(p['time_label'])]
    if len(candidates) != 1:
        raise ValueError('UA175 printed time candidate is not unique')
    prior = candidates[0]
    u175.append({'mfr_row': row['row'], 'prior_row': prior['row'],
                 'mfr_time_label': row['time_label'], 'prior_time_label': prior['time_label'],
                 'mfr_length_label': row['length_label'],
                 'mfr_seconds': row['reported_seconds'],
                 'prior_connect': prior['connect'],
                 'prior_connect_reading': prior['connect_reading'],
                 'prior_scp': prior['scp'],
                 'candidate_association_only': True})

# The two No Conn labels are a direct control against substituting positive setup
# readings for successful connection or conversation. No unknown SCP is set to zero.
not_connected = [r for r in u175 if r['mfr_length_label'] == 'No Conn']
selected_scp = [r for r in u175 if r['prior_scp'] is not None]
all_positive_candidates = all(all(v > 0 for v in p['connect_candidates']) for p in old['UA175'])

mfr93_time_counts = Counter(time_key(r['time_label']) for r in new['UA93_airfone'])
old93_time_counts = Counter(time_key(r['time_label']) for r in old['UA93'])
unmatched_new = [r for r in new['UA93_airfone'] if time_key(r['time_label']) not in old93_time_counts]
unmatched_old = [r for r in old['UA93'] if time_key(r['time_label']) not in mfr93_time_counts]
unique_pairs = []
for row in new['UA93_airfone']:
    key = time_key(row['time_label'])
    matches = [p for p in old['UA93'] if time_key(p['time_label']) == key]
    if len(matches) == 1 and mfr93_time_counts[key] == 1:
        prior = matches[0]
        unique_pairs.append({'mfr_block': row['block'], 'mfr_row_in_block': row['row_in_block'],
                             'mfr_time_label': row['time_label'], 'mfr_seconds': row['reported_seconds'],
                             'prior_summary_row': prior['summary_row'], 'prior_scp': prior['scp_summary'],
                             'prior_carrier_scp': prior['scp_carrier'],
                             'prior_connect': prior['connect_summary'], 'candidate_only': True})

result = {
    'input_sha256': {new_path.name: hashlib.sha256(new_path.read_bytes()).hexdigest(),
                     old_path.name: hashlib.sha256(old_path.read_bytes()).hexdigest()},
    'UA175': {'mfr_rows': len(u175), 'numeric_length_rows': sum(r['mfr_seconds'] is not None for r in u175),
              'No_Conn_rows': len(not_connected),
              'earlier_Connect_readings_all_positive_or_positive_candidates': all_positive_candidates,
              'No_Conn_with_positive_or_positive_candidate_Connect': len(not_connected) if all_positive_candidates else None,
              'selected_prior_SCP_comparisons': len(selected_scp),
              'selected_prior_SCP_equal_to_MFR': sum(r['mfr_seconds'] == r['prior_scp'] for r in selected_scp),
              'pairs': u175},
    'UA93': {'mfr_airfone_rows': len(new['UA93_airfone']),
             'mfr_cellular_labels': len(new['UA93_cellular']),
             'mfr_positive_seconds_rows': sum(r['reported_seconds'] > 0 for r in new['UA93_airfone']),
             'mfr_zero_seconds_rows': sum(r['reported_seconds'] == 0 for r in new['UA93_airfone']),
             'printed_time_duplicate_groups': sum(n > 1 for n in mfr93_time_counts.values()),
             'unique_same_printed_time_candidates': len(unique_pairs),
             'unique_candidates_with_accepted_prior_SCP': sum(p['prior_scp'] is not None for p in unique_pairs),
             'unique_candidates_matching_accepted_prior_SCP': sum(p['prior_scp'] == p['mfr_seconds'] for p in unique_pairs if p['prior_scp'] is not None),
             'unique_time_pairs': unique_pairs,
             'unmatched_MFR_time_labels': unmatched_new,
             'unmatched_prior_time_labels': unmatched_old,
             'unmatched_limit': 'Includes possible earlier analyst reading errors; not all are historical discrepancies.'},
    'negative_controls': {
        'positive_Connect_proves_completed_conversation_rejected_by_No_Conn_rows':
            bool(not_connected) and all_positive_candidates,
        'time_only_join_is_unique_rejected': any(n > 1 for n in mfr93_time_counts.values()),
        'unknown_prior_SCP_values_preserved': all(p['scp'] is None for p in old['UA175'] if p['row'] not in [2, 5]),
    },
    'scope': 'Supplied readings and candidate field accounting only; not source independence, native export authentication, clock calibration, exact caller/leg identity or conversation duration.',
    'remaining': 'Preserve all original values and prior versions. MFR definitions are attributed briefing explanations, not vendor definitions or proof of how failed attempts/operator/ground legs were logged.'
}
with output_path.open('x') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps({'UA175': {k: v for k, v in result['UA175'].items() if k != 'pairs'},
                  'UA93': {k: v for k, v in result['UA93'].items() if k not in ['unique_time_pairs', 'unmatched_MFR_time_labels', 'unmatched_prior_time_labels']},
                  'negative_controls': result['negative_controls']}))
