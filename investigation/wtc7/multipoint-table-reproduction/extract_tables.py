"""Bounded text-layout transcription; values remain source tokens, not measurements."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from pypdf import PdfReader

SOURCE_SHA = 'cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394'
NUMBER = re.compile(r'-?\d+\.\d+')


def extract(source):
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA
    reader = PdfReader(source)
    result = {}
    for page in (47, 50):
        text = reader.pages[page - 1].extract_text(extraction_mode='layout')
        lines = text.splitlines()
        if page == 47:
            header = next(line for line in lines if re.fullmatch(r'\s*t\s+x\s+y(?:\s+[yv]){14}\s*', line))
            centers = [m.start() for m in re.finditer(r'\S+', header)]
            all_columns = ['time_s', 'ref_x', 'ref_y', 'ep_y', 'ep_v', 'screen_y', 'screen_v', 'wp_y', 'wp_v',
                           'ne_y', 'ne_v', 'ec_y', 'ec_v', 'wc_y', 'wc_v', 'nw_y', 'nw_v']
            selected = [0, 1, 2, 9, 10, 11, 12, 13, 14, 15, 16]
        else:
            all_columns = ['time_s', 'ref_y', 'nw_y', 'nw_relative_y', 'center_y', 'center_relative_y',
                           'center_adjusted_y', 'sw_y', 'sw_relative_y', 'sw_adjusted_y']
            first = next(line for line in lines if re.match(r'\s*8\.00\s', line))
            centers = [(m.start() + m.end() - 1) / 2 for m in NUMBER.finditer(first)]
            selected = list(range(10))
        assert len(centers) == len(all_columns)
        rows = []
        for line in lines:
            if not re.match(r'^\s*-?\d+\.\d+\s', line):
                continue
            cells = [None] * len(centers)
            for m in NUMBER.finditer(line):
                center = (m.start() + m.end() - 1) / 2
                distances = sorted((abs(center - c), j) for j, c in enumerate(centers))
                assert distances[0][0] < 4 and distances[1][0] > 4, (page, line, m.group(), distances)
                j = distances[0][1]
                assert cells[j] is None
                cells[j] = m.group()
            assert cells[0] is not None
            rows.append({'page': page, 'row': len(rows) + 1, **{all_columns[j]: cells[j] for j in selected}})
        assert len(rows) == (70 if page == 47 else 25)
        assert rows[0]['time_s'] == ('-1.0' if page == 47 else '8.00')
        assert rows[-1]['time_s'] == ('12.8' if page == 47 else '8.80')
        result[page] = {'source_sha256': SOURCE_SHA, 'physical_and_printed_page': page,
                        'method': 'pypdf layout tokens assigned to source-header columns; independently visually checked',
                        'columns': [all_columns[j] for j in selected], 'rows': rows}
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    results = extract(args.source)
    args.output.mkdir(exist_ok=False)
    for page, data in results.items():
        with (args.output / f'table{page}.json').open('x') as f:
            json.dump(data, f, indent=2, allow_nan=False)
            f.write('\n')
    print(json.dumps({str(p): len(d['rows']) for p, d in results.items()}))
