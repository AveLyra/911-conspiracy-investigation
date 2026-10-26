"""Lossless assessment cross-reference inventory, not a verdict generator."""
from pathlib import Path
from collections import Counter
import hashlib, json, re

R = Path(__file__).resolve().parent
BASE = 'ddd475b4e3c43a92a713426b6dc4c9f350930abd'
BASEURL = 'https://github.com/AveLyra/911-conspiracy-investigation/blob/' + BASE + '/investigation/wtc7/master-lead-register-2026-10-25/MASTER-LIST.md'

# Explicit reviewed cross-references. These refer to focal topics; the original
# verdict and all subsidiary factual claims remain unverified by the mapping.
MAP = {
    6: ('partly covered', [55,57,59,60,86,109], 'The register addresses selected collapse/material observations, not the series-wide aircraft/calls verdict.'),
    237: ('partly covered', [61,62,64], 'Related thermal/mechanical principles; the focal paragraph is about the Twin Towers, not a reproduced WTC 7 result.'),
    239: ('partly covered', [13,69], 'Related limits on exterior-fire inference; no independent Twin Towers temperature reconstruction here.'),
    241: ('partly covered', [87], 'The comparator-method question overlaps; the individual historical building comparisons remain outside this register.'),
    248: ('partly covered', [55,56,57,86,117], 'WTC 7 sound/witness questions overlap; every Twin Towers witness is not covered.'),
    249: ('partly covered', [86], 'Seismic timing/attribution overlaps; exact film formulation and every station record remain to test.'),
    250: ('partly covered', [59,60,109,110], 'Steel attribution and sample selection overlap, with building-specific limits.'),
    251: ('partly covered', [64], 'Furnace/assembly comparison overlaps; every UL representation and employment claim does not.'),
    260: ('partly covered', [60,109], 'Material-identity and chronology questions overlap; this is no fresh composition determination.'),
    262: ('partly covered', [59,60,109,110], 'Same FEMA Sample 1 chain is covered; both samples and each historical interpretation need separate treatment.'),
    263: ('partly covered', [60], 'Material-to-mechanism bridge overlaps; this does not authenticate every dust specimen.'),
    264: ('partly covered', [60], 'Dust/material claims occur in prior forensic context; this inventory does not replicate Harrit.'),
    265: ('partly covered', [60], 'Competing chip interpretations share an issue, not an automatically identical sample.'),
    285: ('partly covered', [67,69], 'WTC 7 damage/fire context overlaps; assess each subsidiary factual assertion separately.'),
    286: ('partly covered', [11,12,13,67,69], 'Fire observation/model-input distinction is covered; film views and rhetorical size judgment are not certified.'),
    287: ('already covered', [9,67], 'Focal WTC 7 free-fall observation and its inferential limits are explicit in the register/audit; edition/timestamp remains unverified.'),
    288: ('partly covered', [1,4,5,68,83], 'Exterior/interior ordering and motion overlap; Fiterman damage and exact footprint wording require their own records.'),
    289: ('already covered', [7], 'Directly observed exterior events versus inferred interior failure is the focal proposition; no new endorsement of the whole narrative.'),
    290: ('partly covered', [7,87,124], 'Mechanism versus model-output limits and generator lead overlap; every diesel-history account is not covered.'),
    292: ('partly covered', [72,73,74,101,102,103,104,105,106,107,108,127,130,131], 'UAF geometry/state and prescribed-result limits overlap; report review history and every support-loss case are separate assertions.'),
    295: ('partly covered', [57,86], 'Source-specific destructive-event timing overlaps; exact Jennings/Hess recording chains remain to test.'),
    311: ('partly covered', [115,116], 'Contractor scope/time is covered; director biography and day-of-attack control must be separately verified.'),
    312: ('partly covered', [42,115,116], 'Installed conditions/access evidence overlaps; specific elevator/powerdown allegations are additional leads.'),
    313: ('partly covered', [59,60,65,66,109,110,111,112,123], 'Actual steel records and preservation vulnerabilities are covered; every disposal decision is not.'),
    314: ('partly covered', [55,58,60], 'Residue-testing limitation is related; a WTC 7 acoustic exclusion cannot stand in for tower-steel chemistry.'),
    315: ('partly covered', [3,7,54,87], 'Modeling scope distinctions overlap; tower propagation is a different analysis.'),
    316: ('partly covered', [46,48,49,50,51,52,54,132,133,134], 'Release/reproduction/notice questions overlap; withholding, legal merits and fraud are separate propositions.'),
}
HMAP = {
    10: ('partly covered', [59,65,66,109,110,111,112,123], 'Related steel/preservation chain; specific NSF request and recycling decision require original hearing/decision records.'),
    12: ('partly covered', [113,114], 'UMS samples and VHS examination are covered; the October 17 Exxon possible-match/clock lead is a distinct unresolved chain.'),
    16: ('partly covered', [113,114], 'Related UMS file family; the exact June 2002 deletion sheet is an additional disclosure-scope claim.'),
}

def save(p, value):
    with p.open('x') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')

def urls(text):
    return list(dict.fromkeys(re.findall(r'https?://[^\s)]+', text)))

def edition(file, line, headings):
    if file.startswith('HIGHLIGHT'):
        return dict(film='Later highlighted leads; not attributed to a particular film scene', edition='Not applicable unless a film-occurrence claim is later made', attribution_verified=False)
    if line < 30:
        return dict(film='Cross-film scope/summary', edition='Assessment states Fahrenheit 9/11 (2004), Loose Change Second Edition, Final Cut, and 52-minute 2015 distributor version; not a verified cut concordance', attribution_verified=False)
    if line < 131:
        return dict(film='Fahrenheit 9/11', edition='2004 film as attributed by assessment; exact release/frame/timestamp not independently checked', attribution_verified=False)
    if line < 323:
        return dict(film='Loose Change series', edition='Claim-family attribution only: Second Edition / Final Cut / 52-minute 2015 distributor version; specific cut unresolved; do not substitute full 2009 American Coup', attribution_verified=False)
    return dict(film='Cross-film context and later evidence', edition='No scene-level attribution established; later 2025/2026 evidence is not content of a 2004 film', attribution_verified=False)

def topic_priority(text, line, file):
    if (file.startswith('HIGHLIGHT') and line in [7,8,11]) or (file.startswith('ASSESSMENT') and line in [52,201,335,359,361,363,365,367,398,399]):
        return 'P1 Saudi assistance / FBI-source and intelligence handling', 'Concrete assistance, dated intelligence and source-handling decisions can be tested against original records.'
    if any(x in text.lower() for x in ['interrogat', 'detainees', 'voluntariness', 'planning narrative', 'coercive questioning']):
        return 'P1 interrogation-dependent narrative', 'Trace exact propositions to independent evidence; distinguish date, voluntariness, reliability and corroboration.'
    if (216 <= line <= 221 and file.startswith('ASSESSMENT')) or (file.startswith('ASSESSMENT') and line==400) or any(x in text for x in ['Mineta', 'FAA executives', 'FAA manager']):
        return 'P1 FAA/NORAD/Mineta and preservation', 'Operational recordings and dated responses can discriminate conflicting chronology and subsequent conduct.'
    if any(x in text.lower() for x in ['briefing', 'presidential warnings', 'daily briefing']):
        return 'P1 presidential warnings', 'Test warning content, actual recipients and response rather than general foreseeability alone.'
    if file.startswith('ASSESSMENT') and 343 <= line <= 351:
        return 'P4 historical analogy', 'Retain and verify the precedent; its existence alone supplies no operational link to the 2001 attacks.'
    if (file.startswith('ASSESSMENT') and (63 <= line <= 77 or 328 <= line <= 336)):
        return 'P2 financial/assistance records or P3 context', 'A specified transfer can matter; keep transaction/beneficiary/motive/operational-knowledge propositions separate.'
    if file.startswith('ASSESSMENT') and line < 131:
        return 'P3 political and aftermath context', 'Retained for checking; prioritize an actual attack-related communication, action or transaction over suggestive association.'
    return 'P2 direct attack/evidence claim or methodological check', 'Retain precise evidence and counterevidence; covered WTC 7 topics do not need to be counted again as independent anomalies.'

def generate(file, prefix):
    lines = (R / file).read_text().splitlines(keepends=True)
    records, accounted, headers = [], [], []
    n = 0
    while n < len(lines):
        raw = lines[n].rstrip('\r\n')
        number = n + 1
        if not raw.strip():
            accounted.append(dict(line=number, kind='blank')); n += 1; continue
        if raw.startswith('#'):
            headers.append(raw)
            accounted.append(dict(line=number, kind='heading', text=raw)); n += 1; continue
        if raw.strip() == '---' or re.fullmatch(r'\|[- :|]+\|', raw):
            accounted.append(dict(line=number, kind='separator')); n += 1; continue
        if raw.startswith('|') and not raw.startswith('| **'):
            accounted.append(dict(line=number, kind='table-header', text=raw)); n += 1; continue
        if file.startswith('ASSESSMENT') and 17 <= number <= 21:
            accounted.append(dict(line=number, kind='assessment-definition-not-empirical-finding', text=raw)); n += 1; continue
        end = n + 1
        if not raw.startswith('|') and not re.match(r'^(?:- |\d+\. )', raw):
            while end < len(lines) and lines[end].strip() and not re.match(r'^(?:#|\||- |\d+\. )', lines[end]):
                end += 1
        exact = ''.join(lines[n:end]).rstrip('\r\n')
        ident = f'{prefix}{len(records) + 1:03d}'
        label = raw.split('|')[1].strip().replace('**', '') if raw.startswith('|') else raw[:150]
        map_value = (MAP if file.startswith('ASSESSMENT') else HMAP).get(number)
        # Other chemistry prose and UAF prose share only partial issue coverage.
        if map_value is None and file.startswith('ASSESSMENT') and 267 <= number <= 278:
            map_value = ('partly covered', [60,109], 'Material identity/provenance/causation bridge overlaps; this exact chemistry claim is not newly verified.')
        if map_value is None and file.startswith('ASSESSMENT') and 300 <= number <= 304:
            map_value = ('partly covered', [72,73,74,101,102,103,108,127,130,131], 'Selected UAF modeling distinctions overlap; no native assignment/run conclusion follows from this cross-reference.')
        status, mids, reason = map_value or ('outside existing register', [], 'No matching focal claim identified in all 134 baseline entries; related broad context is not claim-level coverage.')
        priority, why = topic_priority(exact, number, file)
        boundaries = [0] + [m.end() for m in re.finditer(r'(?<=[.!?])\s+(?=[A-Z*“])', exact)] + [len(exact)]
        boundaries = sorted(set(boundaries))
        children = [dict(id=ident + f'.s{i+1:02d}', character_span=[a,b], exact_wording=exact[a:b], coverage=status, M_ids=[f'M{x:03d}' for x in mids], source_status='Inventory only; assessment verdict is a proposition to test, not inherited truth') for i,(a,b) in enumerate(zip(boundaries,boundaries[1:]))]
        record = dict(unit_kind='film-or-lead-table-row-with-assessment' if raw.startswith('|') else 'assessment-prose-or-methodological-proposal', id=ident, source_file=file, source_line_start=number, source_line_end=end,
                      exact_original_wording=exact, subject=label, heading_context=list(headers),
                      film_attribution=edition(file,number,headers), coverage=status,
                      matching_M_ids=[f'M{x:03d}' for x in mids], coverage_reason=reason,
                      M_baseline_commit=BASE, M_baseline_url=BASEURL,
                      cited_URLs_as_supplied=urls(exact),
                      assessment_status='CLAIM TO TEST; prior verdict not accepted',
                      priority=priority, priority_reason=why, subclaim_text_spans=children,
                      subclaim_split_limit='Text spans for lossless accountability, not a certification that every sentence is a logically atomic proposition. Source findings split consequential propositions separately.',
                      next_step='Trace the underlying evidence and specific edition; retain contrary evidence and unresolved inputs.')
        records.append(record)
        for k in range(n,end):accounted.append(dict(line=k+1,kind='claim-or-interpretation',record_id=ident))
        n = end
    assert [row['line'] for row in accounted] == list(range(1,len(lines)+1))
    return records,accounted

def main():
    baseline=json.loads((R/'M001-M134-baseline.json').read_text())
    assert len(baseline['entries'])==134
    records=[];line_coverage={}
    for file,prefix in [('ASSESSMENT-ORIGINAL.md','B'),('HIGHLIGHT-ASSESSMENT.md','H')]:
        rows,coverage=generate(file,prefix);records+=rows;line_coverage[file]=coverage
    inventory=dict(status='Complete text-unit cross-reference inventory; substantive source testing separate',
                   baseline_commit=BASE, baseline_entries_unchanged=True,
                   records=records, record_count=len(records),
                   child_text_spans=sum(len(r['subclaim_text_spans']) for r in records),
                   coverage_counts=dict(Counter(r['coverage'] for r in records)),
                   all_original_nonempty_content_accounted=True,
                   source_hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in line_coverage},
                   line_accountability=line_coverage,
                   qualification='This inventory is not verification of film occurrence, primary evidence, earlier verdicts or all compound facts. One chain repeated across rows remains one chain.')
    save(R/'claim-crosswalk-v2.json',inventory)
    text=['# Documentary-claim inventory and M001–M134 cross-reference','',
          'Every assessment verdict below is retained as a claim to test. Coverage is topic/claim overlap, not agreement, authentication or engineering validation. B and H IDs never renumber the frozen M baseline. Exact full text, citations, line accounting and child spans are in `claim-crosswalk-v2.json`.','',
          '| ID | Original source line(s) | Subject | Existing coverage | M IDs |','|---|---|---|---|---|']
    for r in records:
        title=r['subject'].replace('|',' / ').replace('\n',' ')[:170]
        text.append(f"| {r['id']} | {r['source_file']}:{r['source_line_start']}–{r['source_line_end']} | {title} | {r['coverage']} | {', '.join(r['matching_M_ids']) or '—'} |")
    with (R/'CROSSWALK-v2.md').open('x') as f:f.write('\n'.join(text)+'\n')
    print(json.dumps({k:inventory[k] for k in ['record_count','child_text_spans','coverage_counts']},indent=2))

if __name__=='__main__':
    main()
