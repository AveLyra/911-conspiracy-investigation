"""Read-only saved-artifact checks; not a solver or fresh raw-source scan."""
import argparse
import ast
import hashlib
import json
import re
from pathlib import Path

UNIT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    checks = []

    def require(label, condition):
        if condition is not True:
            raise ValueError(label)
        checks.append(label)

    def read(name):
        return json.loads((UNIT / name).read_text())

    pin_rows = re.findall(r"^\| ([\w.-]+) \| ([a-f0-9]{64}) \|$",
                          (UNIT / 'validation.md').read_text(), re.M)
    require('nonempty_unique_documented_pins', bool(pin_rows)
            and len(pin_rows) == len(dict(pin_rows)))
    for name, expected in pin_rows:
        require('pin:' + name, sha(UNIT / name) == expected)

    root = read('casea-root01.json')
    repeat = read('casea-root02.json')
    require('root_repeat_status', root['status'] == repeat['status'] == 'PASS')
    require('all_root_result_fields_repeat', root['result'] == repeat['result'])
    r = root['result']
    require('casea_coverage', len(r['casea']['members']) == 45152
            and r['casea']['unique_ids'] == 45152
            and len(r['shells']) == 45152 and r['unmatched_shell_ids'] == []
            and r['casea']['duplicate_ids'] == {}
            and r['casea']['blank_slots'] == 316064
            and r['casea']['zero_slots'] == 0)
    require('all_18_zero_groups', len(r['groups']) == 18 and r['relations'] == []
            and all(g['relation_count'] == 0 and g['matching_eids'] == []
                    and g['matching_nodes'] == [] for g in r['groups']))
    require('coordinate_and_alias_coverage', len(r['selected_coordinates']) == 1189
            and len(r['master_alias_membership']) == 742
            and all(x['listed'] is False for x in r['master_alias_membership']))
    require('source_eof_receipts', len(r['sources']) == 4
            and all(x['eof'] is True and x['pin_after'] is True
                    for x in r['sources'].values())
            and sum(x['lines'] for x in r['sources'].values()) == 11337995
            and sum(x['uncompressed_bytes'] for x in r['sources'].values()) == 567741319)
    cc = read('casea-comparison-root01.json')
    require('independent_casea_comparison', cc['status'] == 'PASS'
            and cc['comparison']['passed'] is True)
    master = read('independent-master-aliases-root01.json')
    rows = master['result']['comparison']['alias_comparisons']
    require('fresh_master_comparison', master['status'] == 'PASS'
            and master['result']['comparison']['passed'] is True
            and len(rows) == 742
            and sum(len(x['field_equal']) for x in rows) == 7420
            and all(x['passed'] is True and x['listed_in_frozen_casea'] is False
                    and all(v is True for v in x['field_equal'].values()) for x in rows))
    inv = r['springs_numeric_inventory']
    sc = read('spring-comparison-root01.json')
    require('independent_spring_comparison', sc['status'] == 'passed'
            and sc['result']['all_common_fields_equal'] is True
            and sc['result']['scope_counts'] == {
                'all_curve_header_fields': 472, 'all_curve_points': 968,
                'all_inventory_curves': 59, 'element_numeric_fields': 136,
                'selected_blocks': 9, 'selected_card_fields': 96,
                'selected_cards': 12, 'selected_elements': 17, 'selected_part_counts': 3})
    dp = read('definition-presence01.json')
    di = read('independent-definition-presence01.json')
    require('definition_family_coverage', dp['status'] == 'PASS'
            and dp['result']['family_counts'] == {
                'DEFINE_CURVE': 59, 'DEFINE_FUNCTION': 0, 'DEFINE_TABLE': 0}
            and dp['result']['variant_count'] == 0 and di['status'] == 'passed'
            and di['result']['family_counts'] == {'CURVE': 59, 'FUNCTION': 0, 'TABLE': 0})
    ar = read('spring-arithmetic01.json')
    ar2 = read('spring-arithmetic02.json')
    ai = read('independent-spring-arithmetic01.json')
    require('arithmetic_repeat', ar['status'] == ar2['status'] == 'UNRESOLVED_DEPENDENCY'
            and ar['result'] == ar2['result'])
    require('no_historical_curve_evaluation', ar['result']['historical_curve_evaluations'] == 0
            and ar['result']['missing_from_supplied_DEFINE_CURVE_registry'] == [602, 803]
            and ai['status'] == 'SOURCE_DEPENDENCY_UNRESOLVED'
            and ai['result']['curves'] == [])
    ir = ai['result']
    require('arithmetic_all_cards_counts', ir['selected_source_cards'] == inv['selected_cards']
            and ir['selected_part_counts'] == inv['selected_part_counts']
            and ir['selected_element_count'] == 17 and len(ir['chains']) == 17
            and len(ir['unresolved_dependencies']) == 17)
    elements = {int(e['values'][0]): e for e in inv['target_elements']}
    require('arithmetic_exact_element_selection', set(elements) == {c['eid'] for c in ir['chains']})
    for c in ir['chains']:
        pid = c['effective_pid']
        lcd = 602 if pid in (820, 821) else 803
        require('chain:' + str(c['eid']), c['source_element'] == elements[c['eid']]
                and c['part'] == inv['selected_cards'][f'*PART:{pid}']
                and c['section'] == inv['selected_cards'][f'*SECTION_DISCRETE:{pid}']
                and c['material'] == inv['selected_cards'][f'*MAT_SPRING_NONLINEAR_ELASTIC:{pid}']
                and c['LCD'] == lcd
                and c['missing_curve_dependencies'] == [{'curve_id': lcd, 'role': 'LCD'}])
    require('missing_typed_curves', not {602, 803}.intersection(
            c['curve_id'] for c in inv['curve_inventory']))
    for name in ('independent-master-aliases01.json', 'independent-master-aliases02.json'):
        failed = read(name)
        require('preserved_pre_source_failure:' + name,
                failed['status'] == 'FAIL' and failed['sources'] == {})
    failed = read('spring-comparison01.json')
    require('preserved_adapter_failure', failed['status'] == 'failed'
            and failed['failure_code'] == 'INPUT_NOT_PASSED')
    pyfiles = sorted(UNIT.glob('*.py'))
    jsonfiles = sorted(UNIT.glob('*.json'))
    for path in pyfiles:
        ast.parse(path.read_text(), filename=path.name)
    for path in jsonfiles:
        json.loads(path.read_text())
    links = 0
    for name in ('report.md', 'validation.md'):
        content = (UNIT / name).read_text()
        require('no_trailing_whitespace:' + name,
                all(line == line.rstrip() for line in content.splitlines()))
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if '://' in target or target.startswith('#'):
                continue
            require('local_link:' + name + ':' + target,
                    (UNIT / target.split('#', 1)[0]).exists())
            links += 1
    return {'checks': checks, 'counts': {'predicates': len(checks),
            'documented_pins': len(pin_rows), 'python_asts': len(pyfiles),
            'json_files': len(jsonfiles), 'report_validation_local_links': links},
            'reviewed_document_sha256': {n: sha(UNIT / n) for n in ('report.md', 'validation.md')},
            'limits': ['Saved-artifact verification, not another raw-source scan.',
                       'No solver execution, physical validation or historical-cause inference.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = Path(args.output)
    if out.parent.resolve() != UNIT or out.exists():
        raise SystemExit('Output must be a new file in this unit.')
    result = verify()
    receipt = {'status': 'PASS', 'code_sha256': sha(Path(__file__)), 'result': result}
    with out.open('x') as handle:
        json.dump(receipt, handle, indent=2, sort_keys=True)
        handle.write('\n')
    print(json.dumps({'status': 'PASS', 'counts': result['counts']}))
