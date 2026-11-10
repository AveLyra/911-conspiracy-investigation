"""Read-only reproducibility checks; prints observations, never edits a source PDF."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re

import fitz
from pypdf import PdfReader


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    for key in ('nist', 'uaf', 'uaf_other', 'cole', 'cole_prior'):
        parser.add_argument('--' + key.replace('_', '-'), type=Path, required=True)
    args = parser.parse_args()
    paths = vars(args)
    before = {key: digest(path.read_bytes()) for key, path in paths.items()}
    docs = {key: fitz.open(path) for key, path in paths.items()}
    nist_pages = {i: docs['nist'][i - 1].get_text() for i in (396, 397, 659)}
    nist_text = ' '.join((nist_pages[396] + nist_pages[397]).split())
    assert 'girder temperature had reached 398' in nist_text
    # A page footer interrupts this sentence in extracted text. Check both
    # source-page fragments explicitly rather than discarding the footer silently.
    assert 'all four erection bolts at Column 44 had' in ' '.join(nist_pages[396].split())
    assert 'failed, leaving the girder essentially unrestrained against rotation at both ends.' in ' '.join(nist_pages[397].split())
    assert 'beam temperature of 436' in nist_text
    # An independently implemented extractor must also recover the numeric rows.
    second = PdfReader(args.nist)
    secondary = ' '.join(second.pages[396].extract_text().split())
    assert '2.10 436 364 Northmost floor beam began to buckle laterally' in secondary
    assert '2.18 476 398 Both top plate bolts of girder to Column 44 had failed' in secondary
    events = [
        {'time_s': 2.04, 'beam_C': 406, 'girder_C': 339, 'event': 'both C44 seat bolts failed'},
        {'time_s': 2.10, 'beam_C': 436, 'girder_C': 364, 'event': 'northmost beam began lateral buckling'},
        {'time_s': 2.18, 'beam_C': 476, 'girder_C': 398, 'event': 'both C44 top plate bolts failed'},
    ]
    # The report displays distinct solver-step states. Filenames do not establish settings.
    images = {}
    for key in ('uaf', 'uaf_other'):
        images[key] = {}
        for physical, figure in ((91, '3.4'), (94, '3.7')):
            page = docs[key][physical - 1]
            matches = [im for im in page.get_images(full=True)
                       if (im[2], im[3]) == ((681, 513) if figure == '3.4' else (1092, 845))]
            assert len(matches) == 1, (key, physical, matches)
            item = matches[0]
            images[key][figure] = {
                'physical_page': physical, 'printed_page': physical - 13,
                'xref': item[0], 'width': item[2], 'height': item[3],
                'decoded_stream_sha256': digest(docs[key].xref_stream(item[0])),
                'decoded_pixels_sha256': digest(fitz.Pixmap(docs[key], item[0]).samples),
            }
    for figure in ('3.4', '3.7'):
        for field in ('decoded_stream_sha256', 'decoded_pixels_sha256'):
            assert images['uaf'][figure][field] == images['uaf_other'][figure][field]
    cole = docs['cole']
    prior = docs['cole_prior']
    assert len(cole) == len(prior) == 18
    differences = [i + 1 for i in range(18) if cole[i].get_text() != prior[i].get_text()]
    assert not differences
    terms = ['Hulsey', 'Alaska', 'Fairbanks', 'UAF']
    hits = {term: [i + 1 for i, p in enumerate(cole)
                   if re.search(r'\b' + re.escape(term) + r'\b', p.get_text(), re.I)]
            for term in terms}
    after = {key: digest(path.read_bytes()) for key, path in paths.items()}
    assert before == after
    result = {
        'generated_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_hashes_before': before, 'source_hashes_after': after,
        'nist_table_8_2_selected_rows': events,
        'C44_top_bolts_minus_first_buckling_s': round(2.18 - 2.10, 2),
        'figure_12_68_panel_offsets_s': [round(a-b, 1) for a,b in [(19.5,6.2),(20.7,7.4),(21.8,8.5)]],
        'figure_12_68_caption_offsets_s': [round(a-b, 1) for a,b in [(21.5,5.5),(23.8,7.8)]],
        'uaf_embedded_images': images,
        'cole_page_text_differences': differences,
        'cole_opinion_whole_word_hits': hits,
        'muPDF_version': fitz.VersionBind,
        'scope': 'Source integrity, text extraction and arithmetic only; no FE execution, historical timing measurement or causal finding.',
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
