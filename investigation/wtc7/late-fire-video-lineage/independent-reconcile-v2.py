#!/usr/bin/env python3
"""Kit-only, byte-pinned adapter of our verifier, never the screening helper."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE/'independent-reconcile.py'
BASE_SHA = '547cc1c701ac01cf08c466b6bcb3e2b6534176f0025298ada96a71dfdc658f90'
NEW_PINS = {'screen_local_v2.py':'890963c2104f53813593b4e09da9b3c5892d2461a2a6a415f06f84842b31d8f9',
            'test_screen_local_v2.py':'61fee5f4bd23a6ce3b6abd372c3f40d6d9e0d3ea9ab3d71ebe745c239c731c83',
            'GRAMMAR-FOLLOWUP.md':'8c1f26316c6ace3f68fb06881b9eed465827672bb7d7168aa250275ae8efa723'}


def require(condition, code):
    if not condition:
        raise ValueError(code)


def load_core():
    data = BASE.read_bytes()
    require(hashlib.sha256(data).hexdigest() == BASE_SHA, 'base_verifier_pin')
    # Three explicit, count-guarded identifier adaptations to our own verified
    # checker. No source-media text, document code or screening helper executes.
    source = data.decode()
    changes = [("r'run0[12]-(?:", "r'v2-run0[12]-(?:"),
               ("name.split('-',1)[1]", "name.removeprefix('v2-').split('-',1)[1]"),
               ("('script_identity','screen_local.py','screen_local.snapshot.py')",
                "('script_identity','screen_local_v2.py','screen_local.snapshot.py')")]
    for old,new in changes:
        require(source.count(old) == 1, 'adapter_exact_replacement_count')
        source = source.replace(old,new)
    namespace = {'__name__':'independent_v2_core', '__file__':str(BASE)}
    exec(compile(source,str(BASE)+'[v2-identifiers]','exec'),namespace)
    return namespace, changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True, choices=['v2-run01-CAMERA3-KIT-MP4','v2-run02-CAMERA3-KIT-MP4'])
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    require(bool(re.fullmatch(r'independent-v2-reconciliation-0[12]\.json',args.out)), 'output_name')
    require(not (HERE/args.out).exists() and not (HERE/args.out).is_symlink(), 'output_exists')
    core, replacements = load_core()
    old_controls = core['controls']()
    original_bins = core['bins']

    def bins_v2(text,tick,seconds):
        normalized, terminal_count = [], 0
        for raw in text.splitlines():
            if raw.endswith('|'):
                tokens = raw.split('|')
                require(len(tokens) == 4 and tokens[-1] == '' and all(tokens[:-1]), 'terminal_delimiter_shape')
                raw = raw[:-1]
                terminal_count += 1
            normalized.append(raw)
        plan,coverage,geometry = original_bins('\n'.join(normalized),tick,seconds)
        coverage['recognized_terminal_delimiter_records'] = terminal_count
        return plan,coverage,geometry

    plain = 'pts=-1|width=4|height=3\npts=0|width=4|height=3\npts=3|width=4|height=3'
    reference = original_bins(plain,Fraction(1),2)
    for value,count in [(plain,0),('\n'.join(x+'|' for x in plain.splitlines()),3),
                        (plain.replace('height=3\n','height=3|\n',1),1)]:
        plan,coverage,geometry = bins_v2(value,Fraction(1),2)
        require(plan == reference[0] and geometry == reference[2], 'grammar_positive_plan')
        require(coverage.pop('recognized_terminal_delimiter_records') == count and coverage == reference[1], 'grammar_positive_coverage')
    good='pts=0|width=4|height=3|'
    bad=['|'+good,good.replace('|width','||width'),good+'|',good+'||',good+'extra=7',
         'pts=0|width=4|extra=3|','pts=0|width=4|width=3|','pts=0|width=4|',
         'pts=N/A|width=4|height=3|','pts=0.5|width=4|height=3|',
         good+'\n'+good,good+'\npts=-1|width=4|height=3|',good+'\npts=1|width=5|height=3|']
    for text in bad:
        try:
            bins_v2(text,Fraction(1),2)
        except ValueError:
            continue
        raise ValueError('grammar_expected_refusal')
    core['bins'] = bins_v2
    pin,read = core['pin'],core['read']
    pins={name:pin(HERE/name) for name in {**core['PINS'],**NEW_PINS}}
    require(all(pins[name]['sha256'] == h for name,h in {**core['PINS'],**NEW_PINS}.items()), 'control_pin')
    sources={s['id']:s for s in read(HERE/'selection.json')['sources']}
    outer=read(HERE/args.run/'receipt.json')
    require(outer['revision'] == 'v2-single-terminal-empty-token', 'revision_name')
    require(outer['grammar_declaration_identity'] == pins['GRAMMAR-FOLLOWUP.md'] == pin(HERE/args.run/'grammar-followup.snapshot.md'), 'declaration_snapshot')
    result=core['check_run'](args.run,sources)
    result['recognized_terminal_delimiter_records']=read(HERE/args.run/'CAMERA3-KIT-MP4/receipt.json')['coverage']['recognized_terminal_delimiter_records']
    require(all(pin(HERE/name) == p for name,p in pins.items()) and pin(BASE)['sha256'] == BASE_SHA, 'control_changed')
    payload={'status':'passed','scope':'Kit-only v2; other failed sources not admitted','producer':pin(__file__),
             'base_verifier':pin(BASE),'identifier_replacements':replacements,'control_pins':pins,
             'original_synthetic_controls':old_controls,'additional_grammar_controls':{'positive_variants':3,'negative_fixtures':len(bad),'status':'passed_before_historical_inventory'},
             'runs':[result],'images_displayed':0,'screening_helper_imported':False}
    with (HERE/args.out).open('x') as output:
        json.dump(payload,output,indent=2,sort_keys=True)
        output.write('\n')
    print(json.dumps({'output':args.out,'identity':pin(HERE/args.out),'result':{k:result[k] for k in ['run','decoded_frames','samples','sheets','product_hash_references','recognized_terminal_delimiter_records','fallback_notices']}}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        code=str(error) if isinstance(error,ValueError) and re.fullmatch('[a-z_]+',str(error)) else 'verification_operation_failed'
        print(json.dumps({'status':'failed','code':code}),file=sys.stderr)
        sys.exit(1)
