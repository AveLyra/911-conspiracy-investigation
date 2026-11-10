import json
from pathlib import Path

def seconds(value):
    h, m, s = value[:2], value[2:4], value[5:]
    return int(h)*3600 + int(m)*60 + int(s)

def run():
    item = next(x for x in json.loads((Path(__file__).parent/'RESULTS.json').read_text())['items'] if x['id']=='FIVE03')
    comparisons = []
    for row in item['preserved_pairs'][:3]:
        end = row['rerecording'][-1].split('–')[-1]
        comparisons.append({'role':row['role'], 'latest_listed_rerecording_end':end, 'last_printed_timed_row':row['last_printed_timed_row'], 'transcript_terminal_label':row['terminal_minute_label'], 'last_timed_row_precedes_latest_listed_end_under_conditional_pairing':seconds(row['last_printed_timed_row']) < seconds(end+':00')})
    return {'comparisons':comparisons,'conditions':'Same source/day/clock/role/copy pairing is assumed only for this comparison, not established. Minute labels are not calibrated media endpoints.','not_tested':'Actual audio/coverage/clock/transcription/native origin or historical truth','Boston':'Matching declared labels reused; no new terminal-page reading'}

if __name__=='__main__':
    print(json.dumps(run(), indent=2))
