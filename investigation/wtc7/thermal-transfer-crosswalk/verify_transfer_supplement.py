#!/usr/bin/env python3
"""Post-schema, bounded source check. No interpreter, raw-text export or solver."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import resource
import sys
import time
import zipfile

HERE = Path(__file__).resolve().parent
PINS = {
    'verify_transfer.py': '218490aa1cf64b7cc791a27275aba5c11f11e8213f6d20a8e24f419d7cddac2d',
    'independent01.json': '20b397590bc7d2831fdc0230f045c1d42fe4a68b1f35ff1345cfea9c1eb3eab9',
    'independent-comparison01.json': '29113ef800f4f5bba9f2c5cf0bcf586420f2a6507eff2649bbe68810a52af64e',
    'run01.json': '4754a59f0628a3ed91e913ce9aa5215254a4e476dcd17d9ee32e964eda2f8117',
    'details02.json': '4072b415f7197a7c1bf9b4da8bc820d6dd5ae9e6f08422d823ffd0b4bb815f64',
    'DETAIL-PROTOCOL.md': '1ff4718d1b5dfb1eee7e3a313dfc49a4ec3ffb5ce5a2cb3666fdebb8d7fa2f11',
}
import hashlib
def sha(b): return hashlib.sha256(b).hexdigest()
def file_sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024**2), b''): h.update(b)
    return h.hexdigest()

assert file_sha(HERE/'verify_transfer.py') == PINS['verify_transfer.py']
spec = importlib.util.spec_from_file_location('frozen_independent_transfer', HERE/'verify_transfer.py')
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
# Only the previously frozen independent scanner supplies source caps, source
# selection, byte/CRC receipts and its own declared lexical conventions.
# No producer module is imported. Its post-schema hash/field recipes are tested.
CONTEXT = {'source': '', 'line': 0, 'completed': 0}
ASSIGNMENT = re.compile(r'[A-Za-z_][A-Za-z0-9_]*(?:\([^=]*\))?\s*=')
BOM = b'\xef\xbb\xbf'
EXTENSIONS = {'', 'int', 'apdl', 'txt', 'out', 'log', 'k'}

def need(ok, code): core.need(ok, code, CONTEXT['source'], CONTEXT['line'])

def fields(s):
    """Retain quote bytes; only unquoted commas split a field."""
    cuts = [0]; quoted = None; pos = 0
    while pos < len(s):
        c = s[pos]
        if quoted is not None:
            if c == quoted:
                if pos+1 < len(s) and s[pos+1] == quoted:
                    pos += 2
                    continue
                quoted = None
        elif c in ('\"', "'"):
            quoted = c
        elif c == ',':
            cuts.append(pos+1)
        pos += 1
    need(quoted is None, 'unclosed_field_quote')
    return [s[a:b-1].strip() for a,b in zip(cuts,cuts[1:])] + [s[cuts[-1]:].strip()]

def literal(v):
    if len(v) >= 2 and v[0] in ('\"', "'") and v[-1] == v[0]:
        q = v[0]
        return v[1:-1].replace(q+q, q)
    return v

def prefix_token(s):
    """Reconstruct the producer's declared ASCII prefix-token hash recipe.

    This adapter is deliberately not the frozen independent full-field rule.
    """
    n = len(s); j = 1 if n and s[0] in '/*' else 0
    if j == n or not (s[j].isascii() and s[j].isalpha()): return None
    j += 1
    while j < n and (s[j].isascii() and (s[j].isalnum() or s[j] == '_')): j += 1
    if j != n and s[j] != ',' and not s[j].isspace(): return None
    return s[:j].upper()

def own_bucket(s):
    t, _ = core.first_field(s)
    t = t.upper()
    if not t or core.NUM.fullmatch(t) or all(core.NUM.fullmatch(x) for x in t.split()): return None
    if '=' in t or s.startswith('('): return None
    return sha(t.encode('latin-1'))

def syntax(s):
    if ASSIGNMENT.match(s): return {'class': 'parameter_assignment'}
    if s in ('*','/',',',';',':','(',')'): return {'class': 'standalone_punctuation'}
    if s and all(c.isascii() and not c.isalnum() and not c.isspace() for c in s):
        return {'class': 'ascii_punctuation_sequence', 'length':len(s), 'distinct_punctuation_count':len(set(s))}
    if len(s) >= 2 and s[0] in ('\"', "'") and s[-1] == s[0]:
        return {'class':'quoted_text_syntax', 'length':len(s)}
    t, _ = core.first_field(s)
    p = prefix_token(s)
    if p == 'MV':
        return {'class': 'allowlisted_mv_syntax', 'command': 'MV', 'whitespace_token_count': len(s.split())}
    if core.TOKEN.fullmatch(t.upper()):
        r = {'class': 'full_identifier_token', 'prefixed': t.startswith(('/', '*'))}
        if t.upper() in core.VOCAB: r['command'] = t.upper()
        return r
    if p is not None: return {'class': 'identifier_prefix_with_noncomma_suffix'}
    if s and all(ord(c) < 128 for c in s):
        return {'class': 'unresolved_ascii_syntax', 'length':len(s),
                'ascii_letter_count':sum(c.isalpha() for c in s),
                'ascii_digit_count':sum(c.isdigit() for c in s)}
    return {'class': 'unresolved_nonascii_syntax'}

def candidate_maps(inventory):
    index = defaultdict(list); parents = {}
    for alias, name in inventory.items():
        p = PurePosixPath(name)
        index[p.name].append(alias); parents[alias] = str(p.parent)
    return index, parents

def operation(s, alias, inventory_maps):
    fs = fields(s); name = fs[0].upper()
    need(name in ('/INPUT','/OUTPUT'), 'operation_full_token')
    raw = fs[1:]; decoded = [literal(v) for v in raw]
    filepart = decoded[0] if decoded else ''
    ext = decoded[1] if len(decoded) > 1 else ''
    directory = decoded[2] if len(decoded) > 2 else ''
    dynamic = any('%' in v for v in decoded)
    pathlike = '/' in filepart or '\\' in filepart or bool(directory)
    literal_search = bool(filepart) and not dynamic and not pathlike
    # Colon/path punctuation is also retained as a caution rather than used
    # to resolve a working directory. The compared root recipe is above.
    caution = any(c in filepart+ext for c in ':\\/')
    index, parents = inventory_maps
    candidates = list(index.get(filepart+('.'+ext if ext else ''), ())) if literal_search else []
    same = [a for a in candidates if alias.startswith('ZIP') and a.startswith('ZIP') and parents[a] == parents[alias]]
    token = prefix_token(s)
    need(token == name, 'operation_prefix_vs_full')
    _, tail = core.first_field(s)
    return {
        'command': name,
        'root_arguments_sha256': sha(s[len(token):].encode('latin-1')),
        'independent_arguments_sha256': sha(tail.encode('latin-1')),
        'field_count': len(raw), 'field_hashes': [sha(x.encode('latin-1')) for x in raw],
        'extension_class': ext.lower() if ext.lower() in EXTENSIONS else 'other',
        'dynamic_percent_syntax': dynamic, 'path_or_directory_present': pathlike,
        'additional_path_punctuation_caution': caution,
        'literal_basename_candidate_search': literal_search,
        'exact_basename_candidates': candidates, 'same_archive_parent_candidates': same,
    }

def bom_observation(data):
    r = {'leading_utf8_bom': data.startswith(BOM)}
    if not r['leading_utf8_bom']: return r
    tail = data[3:].split(b'\n', 1)[0].rstrip(b'\r')
    pieces, comment, unclosed = core.split_syntax(tail.decode('latin-1'))
    r.update(first_line_after_prefix_bytes=len(tail), first_line_after_prefix_sha256=sha(tail),
             only_prefix_on_first_line=not tail.strip(), unclosed_quote=unclosed,
             after_prefix_nonempty_code_segments=sum(bool(x.strip()) for x in pieces),
             after_prefix_comment_present=comment is not None)
    # No Unicode reinterpretation of any other source byte is performed.
    return r

def controls():
    passed = []
    def ok(label, condition): need(condition, 'control_'+label); passed.append(label)
    ok('quoted_comma', fields("/INPUT,'a,b',int") == ['/INPUT', "'a,b'", 'int'])
    ok('doubled_quote', literal("'a''b'") == "a'b")
    try: fields("/INPUT,'unfinished")
    except core.AuditError as e: ok('unclosed_quote', e.code == 'unclosed_field_quote')
    else: need(False, 'control_unclosed_quote_accepted')
    inv = {'ZIP00001':'A/x.int','ZIP00002':'B/x.int','ZIP00003':'A/driver.int'}
    maps = candidate_maps(inv)
    r = operation('/INPUT,x,int','ZIP00003',maps)
    ok('candidate_ambiguity', r['exact_basename_candidates'] == ['ZIP00001','ZIP00002'] and r['same_archive_parent_candidates'] == ['ZIP00001'])
    ok('hash_recipes', r['root_arguments_sha256'] == sha(b',x,int') and r['independent_arguments_sha256'] == sha(b'x,int'))
    ok('directory_rejection', not operation('/INPUT,x,int,folder','ZIP00003',maps)['literal_basename_candidate_search'])
    ok('dynamic_rejection', not operation('/INPUT,%x%,int','ZIP00003',maps)['literal_basename_candidate_search'])
    ok('quote_protection', len(core.split_syntax("/INPUT,'a!b$c,d',int $ /OUTPUT,z,out")[0]) == 2)
    ok('bom_only', bom_observation(BOM+b'\nBF,1,TEMP,2\n')['only_prefix_on_first_line'])
    ok('bom_with_command', bom_observation(BOM+b'BF,1,TEMP,2\n')['after_prefix_nonempty_code_segments'] == 1)
    ok('not_bom', not bom_observation(b'\xef\xbb\xbe\n')['leading_utf8_bom'])
    ok('assignment', all(syntax(x)['class'] == 'parameter_assignment' for x in ('x = 1','x(2)=1','x=1')))
    ok('punctuation', syntax('*')['class'] == 'standalone_punctuation')
    ok('repeated_punctuation', syntax('********')['class'] == 'ascii_punctuation_sequence')
    ok('quoted_text_syntax', syntax("'arbitrary text'")['class'] == 'quoted_text_syntax')
    ok('prefix_vs_full', prefix_token('MV a b') == 'MV' and own_bucket('MV a b') == sha(b'MV A B'))
    ok('unknown_suppression', 'SECRET' not in json.dumps(syntax('SECRET,private')))
    ok('nul_exclusion', core.lexical(b'/INPUT,x\n\0','SYNTHETIC')['commands'] is None)
    return {'passed':len(passed), 'groups':passed}

def run():
    for name, wanted in PINS.items(): need(file_sha(HERE/name) == wanted, 'frozen_dependency_pin')
    details = json.loads((HERE/'details02.json').read_text())['result']
    own = json.loads((HERE/'independent01.json').read_text())['result']
    comp = json.loads((HERE/'independent-comparison01.json').read_text())['result']
    root = json.loads((HERE/'run01.json').read_text())['result']
    ownfiles = {f['source']: f for f in own['files']}
    rootfiles = {f['alias']: f for f in root['records']}
    diff = {f['source']:f['differences'] for f in comp['vocabulary_token_differences']}
    selected = {r['alias']:r for r in details['records']}
    selection_expected = {a for a,r in rootfiles.items() if r['scan'].get('operations') or r['scan'].get('unknown_tokens') or r['scan'].get('line_kinds',{}).get('noncommand_unresolved_segments')}
    need(set(selected) == selection_expected and set(diff) <= set(selected), 'selection_coverage')
    paths = core.approved_apdl(); before = core.source_pins(paths)
    inventory = {'APDL%02d'%i:r['relative_path'] for i,(_,r) in enumerate(paths,1)}
    files = []; total = 0; coverage = Counter(); syntax_counts = Counter(); unresolved_original = Counter(); fail = []
    def check(ok, code, loc=None):
        coverage['comparisons'] += 1
        if not ok: fail.append({'source': CONTEXT['source'], 'line': CONTEXT['line'], 'code': code, **(loc or {})})
    with zipfile.ZipFile(core.ZIP) as z:
        entries = z.infolist(); need(len(entries) <= core.ENTRY_CAP, 'entry_cap')
        inventory.update({'ZIP%05d'%i:x.filename for i,x in enumerate(entries,1) if not x.is_dir()})
        index = candidate_maps(inventory)
        # All candidate identities are pinned against the frozen metadata.
        for alias, name in inventory.items(): check(sha(name.encode('utf-8')) == rootfiles[alias]['name_sha256'], 'inventory_name_hash')
        for alias, prior in selected.items():
            CONTEXT.update(source=alias, line=0)
            wanted = ownfiles[alias]['receipt']
            if alias.startswith('APDL'):
                p = paths[int(alias[4:])-1][0]
                with p.open('rb') as f: data, receipt = core.read_body(f,alias,wanted['bytes_read'])
            else:
                entry = entries[int(alias[3:])-1]
                need(not entry.is_dir() and not entry.filename.lower().endswith('.png'), 'selected_body_kind')
                with z.open(entry) as f: data, receipt = core.read_body(f,alias,entry.file_size,entry.CRC)
            total += len(data); need(total <= core.TOTAL_CAP, 'aggregate_cap')
            need(receipt['sha256'] == wanted['sha256'] == prior['sha256'], 'selected_body_hash')
            need(b'\0' not in data, 'nul_semantics_excluded')
            physical = data.split(b'\n')
            if data.endswith(b'\n'): physical.pop()
            need(all(len(line)+1 <= core.LINE_CAP for line in physical), 'line_cap')
            target = defaultdict(list)
            for group in ('unknown','unresolved_segments','operations'):
                for r in prior[group]: target[(r['line'],r['segment'])].append((group,r))
            wanted_lines = {line for line,_ in target}
            segments = {}
            for line in wanted_lines:
                need(1 <= line <= len(physical), 'target_line_bounds')
                pieces, _, unclosed = core.split_syntax(physical[line-1].rstrip(b'\r').decode('latin-1'))
                need(not unclosed, 'target_unclosed_quote')
                for num,piece in enumerate(pieces,1):
                    if (line,num) in target: segments[(line,num)] = piece.strip()
            need(set(segments) == set(target), 'target_segment_coverage')
            independent_ops = {(x['line'],x['segment']):x for x in ownfiles[alias]['lexical']['operations']}
            rederived_own = Counter(); rederived_root = Counter(); rows = []; ops = []
            b = bom_observation(data)
            if b['leading_utf8_bom']: coverage['leading_utf8_bom_files'] += 1
            if b.get('only_prefix_on_first_line'): coverage['bom_only_first_lines'] += 1
            for (line,num), references in sorted(target.items()):
                CONTEXT['line'] = line; s = segments[(line,num)]; coverage['target_segments'] += 1
                # Target unknown/residual locations are complete for every
                # differing hash bucket, checked against each frozen count.
                if any(g != 'operations' for g,_ in references):
                    h = own_bucket(s)
                    if h: rederived_own[h] += 1
                for group, ref in references:
                    loc = {'line':line,'segment':num}
                    if group == 'operations':
                        r = operation(s,alias,index); original = independent_ops.get((line,num),{})
                        check(r['independent_arguments_sha256'] == original.get('arguments_sha256'), 'independent_argument_hash',loc)
                        check(r['root_arguments_sha256'] == ref['arguments_sha256'], 'root_argument_hash',loc)
                        check(r['command'] == original.get('command') == ref['command'], 'operation_command',loc)
                        for k in ('field_count','field_hashes','extension_class','dynamic_percent_syntax','path_or_directory_present','literal_basename_candidate_search','exact_basename_candidates','same_archive_parent_candidates'):
                            check(r[k] == ref[k], 'operation_'+k,loc)
                        ops.append({**loc,**r}); coverage['operations'] += 1
                        continue
                    c = syntax(s)
                    if group == 'unknown':
                        p = prefix_token(s)
                        check(p is not None and sha(p.encode('ascii')) == ref['token_sha256'], 'unknown_prefix_hash',loc)
                        rederived_root[ref['token_sha256']] += 1
                    else: check(sha(s.encode('latin-1')) == ref['segment_sha256'], 'unresolved_segment_hash',loc)
                    if line == 1 and num == 1 and b['leading_utf8_bom']:
                        c = {'class':'utf8_bom_only' if b['only_prefix_on_first_line'] else 'utf8_bom_prefixed'}
                    if ref['class'] == 'parameter_assignment': check(c['class'] == 'parameter_assignment', 'assignment_class',loc)
                    syntax_counts[c['class']] += 1
                    if group == 'unknown' and ref['class'] == 'unresolved': unresolved_original[c['class']] += 1
                    rows.append({**loc,'original_group':group,'original_class':ref['class'],
                                 'segment_sha256':sha(s.encode('latin-1')), 'independent_bucket_sha256':own_bucket(s),
                                 'root_token_sha256':ref.get('token_sha256'), **c})
            check(len(ops) == len(independent_ops), 'operation_coverage')
            verified_diffs = []
            for r in diff.get(alias,[]):
                h = r['token_sha256']
                check(rederived_own[h] == r['independent'], 'differing_independent_bucket')
                check(rederived_root[h] == r['root'], 'differing_root_bucket')
                verified_diffs.append({'token_sha256':h,'independent':rederived_own[h],'root':rederived_root[h]})
                coverage['differing_hash_buckets'] += 1
            files.append({'source':alias,'name_sha256':sha(inventory[alias].encode('utf-8')),
                          'receipt':receipt,'bom':b,'classifications':rows,'operations':ops,'differing_hash_buckets':verified_diffs})
            CONTEXT['completed'] += 1
            if CONTEXT['completed'] % 500 == 0: print(json.dumps({'progress_files':CONTEXT['completed'],'read_bytes':total}),flush=True)
    after = core.source_pins(paths); need(after == before,'source_pins_changed')
    for name,wanted in PINS.items(): need(file_sha(HERE/name) == wanted,'frozen_dependency_pin_after')
    return {'status':'PASS' if not fail else 'FAIL_COMPARISON','failures':fail,
            'source_pins_before':before,'source_pins_after':after,'selected_files':len(files),'read_bytes':total,
            'coverage':dict(coverage),'syntax_classes':dict(syntax_counts),
            'original_371_unresolved_syntax_classes':dict(unresolved_original),'records':files,
            'limits':['Post-schema source checking, not blind discovery.','Imports only the frozen independent scanner, not producer modules.',
                      'Candidate aliases mean exact inventory name matches, not historical execution or working-directory resolution.',
                      'Syntax classification and BOM removal on a diagnostic first line do not authenticate language semantics.',
                      'Unknown identifiers remain hashed; no solver, macro expansion, exporter-absence or causal finding.']}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--controls',action='store_true'); p.add_argument('--output',required=True); args=p.parse_args()
    need(re.fullmatch(r'independent-supplement(?:-controls)?[0-9]{2}\.json',args.output) is not None,'output_name')
    dest=HERE/args.output; need(not dest.exists(),'create_only_output')
    start=time.monotonic(); receipt={'code_sha256':file_sha(Path(__file__)),'dependency_pins':PINS,'command':sys.argv,'python':sys.version.split()[0]}
    result=None
    try:
        receipt['controls']=controls()
        if not args.controls: result=run()
        peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss; need(peak<=core.MEM_CAP,'memory_cap')
        receipt.update(status='PASS' if result is None or result['status']=='PASS' else 'FAIL',peak_rss_bytes=peak)
    except (Exception,KeyboardInterrupt) as e:
        receipt.update(status='FAIL',error={'code':e.code if isinstance(e,core.AuditError) else type(e).__name__,**CONTEXT},completed_body_receipts=core.PROGRESS)
    receipt['seconds']=time.monotonic()-start
    with dest.open('x') as f: json.dump({'receipt':receipt,'result':result},f,indent=2,sort_keys=True); f.write('\n')
    print(json.dumps({'status':receipt['status'],'output':args.output,'sha256':file_sha(dest),'seconds':receipt['seconds'],'error':receipt.get('error')}))
    return 0 if receipt['status']=='PASS' else 1

if __name__=='__main__': sys.exit(main())
