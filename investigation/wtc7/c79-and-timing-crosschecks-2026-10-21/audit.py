"""Read-only PDF-layer, source-pin and arithmetic checks, not a solver test."""
import argparse
import datetime
from decimal import Decimal
import hashlib
import json
from pathlib import Path

import fitz
from pypdf import PdfReader


PINS = {
    'nist': '30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f',
    'ara': 'cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4',
    'uaf': 'f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa',
    'uaf_other': '41dd3390627fac24c2bd696160c48f15e05d3213cc05325c4e4e89608df96d27',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    for key in PINS:
        parser.add_argument('--' + key.replace('_', '-'), type=Path, required=True)
    args = vars(parser.parse_args())
    checks = []

    def check(name, value):
        if not value:
            raise AssertionError(name)
        checks.append(name)

    before = {k: sha(p.read_bytes()) for k, p in args.items()}
    for k in PINS:
        check(k + ' source hash matches pin', before[k] == PINS[k])
    docs = {k: fitz.open(p) for k, p in args.items()}
    layers = {}
    for key in ('uaf', 'uaf_other'):
        p = docs[key][98]
        images = [i for i in p.get_images(full=True) if (i[2], i[3]) == (749, 582)]
        check(key + ' one Figure 3.14 embedded image', len(images) == 1)
        im = images[0]
        overlay = [s for b in p.get_text('dict')['blocks'] if 'lines' in b
                   for line in b['lines'] for s in line['spans']
                   if s['text'] == 'W21x44;  G3005 w/o bracing']
        check(key + ' exact vector overlay text', len(overlay) == 1)
        span = overlay[0]
        fills = [d for d in p.get_drawings() if d['fill'] is not None
                 and d['rect'].contains(fitz.Rect(span['bbox']))]
        check(key + ' vector label has covering filled path', len(fills) >= 1)
        text = ' '.join(p.get_text().split())
        check(key + ' caption names W21x44 G3005', 'Figure 3.14 UAF analysis of the W21x44 G3005' in text)
        layers[key] = {
            'physical_page': 99, 'printed_page': 86, 'figure': '3.14',
            'caption_member_label': 'W21x44 G3005',
            'rendered_vector_label': span['text'],
            'vector_label_bbox_pdf_points': list(span['bbox']),
            'covering_fills': [{'bbox_pdf_points': list(d['rect']), 'rgb': d['fill']} for d in fills],
            'image_xref': im[0], 'image_size_pixels': [im[2], im[3]],
            'image_rect_pdf_points': [list(r) for r in p.get_image_rects(im[0])],
            'decoded_stream_sha256': sha(docs[key].xref_stream(im[0])),
            'decoded_pixels_sha256': sha(fitz.Pixmap(docs[key], im[0]).samples),
            'alpha_mask_sha256': sha(docs[key].xref_stream(im[1])) if im[1] else None,
            'underlying_raster_label_manual_transcription': 'W24x55; G3005 w/o bracing',
            'native_member_section': None,
        }
    for prop in ('decoded_stream_sha256', 'decoded_pixels_sha256', 'alpha_mask_sha256'):
        check('Figure 3.14 ' + prop + ' matches both UAF copies', layers['uaf'][prop] == layers['uaf_other'][prop])
    ara = docs['ara']
    a_text = ' '.join(ara[159].get_text().split())
    caption = 'Figure 4-60. Core collapse sequence at 6.2 to 8.5 s (14.5 to 21.8 s).'
    check('ARA Figure 4-60 caption exactly located', caption in a_text)
    other_extractor = ' '.join(PdfReader(args['ara']).pages[159].extract_text().split())
    check('ARA caption independently extracted', caption in other_extractor)
    check('ARA list of figures repeats 14.5', '6.2 to 8.5 s (14.5 to 21.8 s)' in ' '.join(ara[16].get_text().split()))
    check('original NIST Figure 12-68 conflict retained', 'Time: 5.5 to 7.8 s (21.5 to 23.8 s)' in ' '.join(docs['nist'][658].get_text().split()))
    check('UAF general CTE text located', '14 microstrain/°C (7.78 microstrain/°F)' in docs['uaf'][44].get_text())
    check('UAF modified coefficient located', '11.5' in docs['uaf'][92].get_text() and '40%' in docs['uaf'][92].get_text())
    control = ' '.join(ara[155].get_text().split())
    check('control termination and stability reason retained', 'terminated 4.26 s after ANSYS damage application' in control and 'since the structure was stable' in control)
    check('4-hour C79 event timestamp located', '-1.3 (14.7) s' in ara[126].get_text())
    check('control uses 4-hour temperatures and 3.5-hour damage', 'Case B, 4.0 h temperatures' in docs['nist'][633].get_text() and 'Case B, 3.5 h damage' in docs['nist'][633].get_text())
    D = Decimal
    calculations = {
        'ARA_caption_offsets_s': [str(D('14.5')-D('6.2')), str(D('21.8')-D('8.5'))],
        'panel_offsets_s': [str(D(b)-D(a)) for a,b in [('6.2','19.5'),('7.4','20.7'),('8.5','21.8')]],
        'general_UAF_CTE_per_F_from_per_C_microstrain': str(D('14') / D('1.8')),
        'conditional_increase_percent_using_rounded_general_CTE': str((D('11.5') / D('7.78')-1)*100),
        'conditional_increase_percent_using_general_CTE_per_C': str((D('11.5')*D('1.8') / D('14')-1)*100),
        'control_elapsed_after_damage_s': str(D('12.76')-D('8.5')),
        '4hour_C79_elapsed_after_damage_s': str(D('14.7')-D('8.5')),
        'difference_in_followup_before_C79_event_s': str(D('14.7')-D('12.76')),
    }
    check('caption first offset is 8.3 not 13.3', calculations['ARA_caption_offsets_s'] == ['8.3','13.3'])
    check('common solver-clock difference is 1.94 s', calculations['difference_in_followup_before_C79_event_s'] == '1.94')
    after = {k: sha(p.read_bytes()) for k,p in args.items()}
    check('all source hashes unchanged', before == after)
    print(json.dumps({
        'generated_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_hashes_before': before, 'source_hashes_after': after,
        'UAF_figure_3_14_layers': layers,
        'calculations': calculations,
        'ARA_caption_verbatim': caption,
        'source_pin_and_extraction_checks_passed': len(checks), 'checks': checks,
        'actual_native_CTE_baseline': None,
        'control_delayed_collapse_result': None,
        'scientific_scope': 'Source/PDF-layer identity and exact arithmetic only. No solver run, new historical timing or cause/intent finding.',
    }, indent=2))


if __name__ == '__main__':
    main()
