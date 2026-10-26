"""Recount labelled FBI table rows. Requires pypdf; does not authenticate calls."""
from pathlib import Path
import argparse, datetime, hashlib, json, re

SOURCE_SHA256 = '9b5403658314bc650d98eca56f4680613a57c6953a31386b434184f0b234a1ba'

def recount(pdf):
    from pypdf import PdfReader
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == SOURCE_SHA256, 'Different source bytes; preserve as a separate version'
    pages = PdfReader(pdf).pages
    rows = []
    for index in range(34, 37):
        for line_number, line in enumerate(pages[index].extract_text().splitlines(), 1):
            if re.match(r'^\s*\d{1,2}/\d{1,2}/\d\d\s', line):
                date = datetime.datetime.strptime(line.split()[0], '%m/%d/%y').date()
                rows.append(dict(physical_page=index+1, extracted_text_line=line_number,
                    verbatim=line.rstrip(), iso_date=str(date)))
    window = [r for r in rows if '1999-12-06' <= r['iso_date'] <= '2000-02-04']
    return dict(source_file='fbi-eo14040-2c-part5.pdf', physical_pages=[35,36,37],
        bates='EO14040-002757–002759', all_labelled_table_rows=len(rows),
        date_window_inclusive=['1999-12-06','2000-02-04'], date_window_rows=len(window),
        window_rows_involving_BAYOUMI_2=sum('BAYOUMI#2' in r['verbatim'] for r in window),
        window_rows_involving_BAYOUMI_4=sum('BAYOUMI#4' in r['verbatim'] for r in window),
        unit='printed table row; not authenticated unique call or identified speaker', rows=rows)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    args = parser.parse_args()
    print(json.dumps(recount(args.pdf), indent=2))
