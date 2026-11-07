"""Screen the published historical CSV derivative against the W14A field tuple."""
import csv
import hashlib
import json
import re
import sys
from decimal import Decimal
from pathlib import Path

FIELD = tuple(map(Decimal, ('16', '15.5', '1.1875')))
FIELDS = ('d', 'bf', 'tf')
LIMITS = tuple(map(Decimal, ('0', '0.25', '0.5', '1')))
EDITIONS = ('ASD7', 'ASD8', 'LRFD1', 'ASD9')
DESIGNATION = re.compile(r'W\s*(13|14)\s*[xX]\s*([0-9]+)[A-Za-z]?')
SOURCES = {
    'aisc_shapes_historic_clean.csv': (
        '58c915d41833295a66baee2705f299b774ca044c45a718c5ccbd84cc16ccc654',
        '9acb9ac44b8ff57745970cffea1c4c41bf7238c2',
    ),
    'aisc_historic_shape_defs.csv': (
        'b73b416120865f030e47e15885ef8cbc657dde9057806d55574b36c15e01f9b3',
        'd289ad995296a6b80035cfd67d453a385cfce896',
    ),
}


def verify_file(path, hashes):
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == hashes[0], path.name
    header = f'blob {len(data)}\0'.encode()
    assert hashlib.sha1(header + data).hexdigest() == hashes[1], path.name


def describe(candidate):
    line, record, dimensions, distance = candidate
    return {
        'csv_line': line,
        'designation': record['Designation'],
        'table_inches': dict(zip(FIELDS, map(str, dimensions))),
        'max_absolute_difference_inches': str(distance),
    }


def screen(candidates):
    return {
        'rows': len(candidates),
        'within_each_dimension_inches': {
            str(limit): [describe(c) for c in candidates if c[-1] <= limit]
            for limit in LIMITS
        },
        'closest': [describe(c) for c in candidates
                    if c[-1] == min(x[-1] for x in candidates)],
    }


def run(sources):
    for name, hashes in SOURCES.items():
        verify_file(sources / name, hashes)
    by_edition = {edition: {13: [], 14: []} for edition in EDITIONS}
    with (sources / 'aisc_shapes_historic_clean.csv').open(newline='') as source:
        reader = csv.DictReader(source)
        assert reader.fieldnames[5:10] == ['d', 'tw', 'tw/2', 'bf', 'tf']
        for ordinal, row in enumerate(reader, start=2):
            assert reader.line_num == ordinal
            match = DESIGNATION.fullmatch(row['Designation'])
            if row['Edition'] not in by_edition or row['Type'] != 'W' or not match:
                continue
            nominal = int(match.group(1))
            dimensions = tuple(Decimal(row[name]) for name in FIELDS)
            assert all(x > 0 for x in dimensions)
            assert all(row[k] == '0' for k in ('ddet', 'bfdet', 'tfdet'))
            distance = max(abs(value - field) for value, field in zip(dimensions, FIELD))
            by_edition[row['Edition']][nominal].append((ordinal, row, dimensions, distance))

    alias_8 = next(c for c in by_edition['ASD8'][14] if c[0] == 8990)
    alias_lrfd = next(c for c in by_edition['LRFD1'][13] if c[0] == 7972)
    assert alias_8[2] == alias_lrfd[2] and alias_8[1]['W'] == alias_lrfd[1]['W'] == '211'
    return {
        'field_inches': dict(zip(FIELDS, map(str, FIELD))),
        'method': 'Tabulated dimensions only. Inclusive per-dimension bands, illustrative only.',
        'w14_rows_by_edition': {ed: screen(families[14]) for ed, families in by_edition.items()},
        'lrfd1_w13_control': screen(by_edition['LRFD1'][13]),
        'shared_tuple_control': {'ASD8': describe(alias_8), 'LRFD1': describe(alias_lrfd)},
    }


if __name__ == '__main__':
    print(json.dumps(run(Path(sys.argv[1])), indent=2))
