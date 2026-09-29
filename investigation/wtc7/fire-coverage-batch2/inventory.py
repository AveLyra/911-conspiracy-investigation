#!/usr/bin/env python3
"""Read-only audit of frozen run-01 assets; exclusive-create inventory01.json.

No extraction, image alteration, page rendering, label reading, or overwrites.
Use --check to compare a fresh in-memory inventory with the existing output.
"""
import argparse
import hashlib
import json
import platform
from collections import Counter
from pathlib import Path

import PIL
from PIL import Image

MAIN = Path('/Users/admin/docs/911')
BASE = MAIN / 'research/sherlock-wtc7-investigation/fire-annotation'
HERE = Path(__file__).resolve().parent
SOURCE_SHA = '30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f'
PROTOCOL_SHA = '8ea3df6a4550e55de334ac20ce45a8fb05aa00f47800a6ca7b874f74803d94ff'
KEY_SHA = 'c0361c5a3ae52c2663a6772db6078824b4b123e59d8e50d2e24b26d85855afa3'
PRIOR_MAIN_SHA = 'd7673cc50ebca454ea30a0d2c45e44041e9d06de9f586e32dd27a65818f535ce'
PRIOR_REVIEWER_SHA = '03c671cfb383e939509e0008101a81e4954141c8c8f680596bbecde573f128f0'
DECLARED_NEW_IDS = {
    'A-873f87e7149b', 'A-e1b0c06ad11d', 'A-9e7b4935c8aa',
    'A-0b722775db93', 'A-fa6f410444bb', 'A-ffe3726a0312',
    'A-0e60b82a1a4c', 'A-6902e91e39ee', 'A-671f312eade8',
    'A-69d899e75343', 'A-8bc36f05fe38', 'A-7b61385d1373',
    'A-f1e2fa01e344',
}


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load(path):
    return json.loads(path.read_text())


def pin(path):
    return {'path': str(path), 'sha256': sha(path), 'bytes': path.stat().st_size}


def check_artifact(record):
    path = BASE / record['path']
    actual = pin(path)
    assert actual['sha256'] == record['sha256'], (path, 'hash mismatch')
    assert actual['bytes'] == record['bytes'], (path, 'byte-count mismatch')
    if 'dimensions' in record:
        with Image.open(path) as image:
            dimensions = list(image.size)
        assert dimensions == record['dimensions'], (path, 'dimension mismatch')
        actual['dimensions'] = dimensions
    return actual


def build():
    key_path = BASE / 'assets/run-01/reviewed-provenance-key.json'
    main_path = BASE / 'main-image-level.json'
    reviewer_path = BASE / 'reviewer-image-level.json'
    attrib_path = HERE / 'source-attributions.json'
    extraction_path = BASE / 'assets/run-01/extraction-receipt.json'
    verification_path = BASE / 'assets/run-01/verification-receipt.json'
    protocol_path = HERE / 'PROTOCOL.md'
    for path, expected in [(protocol_path, PROTOCOL_SHA), (key_path, KEY_SHA),
                           (main_path, PRIOR_MAIN_SHA), (reviewer_path, PRIOR_REVIEWER_SHA)]:
        assert sha(path) == expected, (path, 'protocol input pin mismatch')
    key = load(key_path)
    attributions = load(attrib_path)
    source = MAIN / key['source']['path']
    source_before = pin(source)
    assert source_before['sha256'] == SOURCE_SHA == key['source']['sha256']
    prior_main = [x['asset_id'] for x in load(main_path)['images']]
    prior_reviewer = [x['asset_id'] for x in load(reviewer_path)['assets']]
    assert len(prior_main) == len(set(prior_main))
    assert len(prior_reviewer) == len(set(prior_reviewer))
    assert set(prior_main) == set(prior_reviewer), 'prior review sets differ'
    prior = set(prior_main)
    photo_ids = {x['asset_id'] for x in key['assets'] if x['role'] == 'report_photographic_image'}
    geometry_ids = {x['asset_id'] for x in key['assets'] if x['role'] == 'report_geometry_graphic'}
    all_ids = {x['asset_id'] for x in key['assets']}
    assert len(all_ids) == len(key['assets'])
    assert prior <= photo_ids
    assert photo_ids.isdisjoint(geometry_ids)
    assert photo_ids | geometry_ids == all_ids
    new_ids = photo_ids - prior
    assert len(all_ids) == 28 and len(photo_ids) == 25 and len(geometry_ids) == 3
    assert len(prior) == 12 and len(new_ids) == 13
    assert new_ids == DECLARED_NEW_IDS, 'new sample differs from declared protocol set'
    source_rows = {x['asset_id']: x for x in attributions['new_photographic_attributions']}
    assert set(source_rows) == new_ids
    on_disk_ids = {x.stem for x in (BASE / 'assets/run-01/images').glob('*.jpg')}
    assert on_disk_ids == all_ids, 'disk/key image coverage differs'
    pages = {}
    for page in key['pages']:
        pages[page['physical_page']] = {
            'page_id': page['page_id'],
            'physical_page': page['physical_page'],
            'printed_page': page['printed_page'],
            'render': check_artifact(page['render']),
            'context_text': check_artifact(page['text']),
            'context_text_fragments': check_artifact(page['text_fragments']),
            'full_page_visually_reviewed_by_source_agent': page['physical_page'] in attributions['method']['full_page_pngs_visually_reviewed'],
        }
    records = []
    for asset in key['assets']:
        asset_id = asset['asset_id']
        assert len(asset['figure_associations']) == 1
        association = asset['figure_associations'][0]
        figure = association['figure']
        for item in asset['invocations']:
            assert item['physical_page'] == association['physical_page']
        view = check_artifact(asset['extracted_view'])
        assert view['dimensions'] == asset['native_pdf_dimensions']
        decrypted = check_artifact(asset['raw_encoded_stream'])
        ciphertext = check_artifact(asset['on_disk_ciphertext_stream'])
        assert view['sha256'] == decrypted['sha256']
        assert asset['extracted_view']['pixel_resize'] is False
        assert asset['extracted_view']['additional_image_recompression'] is False
        if asset_id in prior:
            status = 'prior_paired_photographic'
        elif asset_id in new_ids:
            status = 'new_batch2_photographic'
        else:
            status = 'reference_only_geometry'
        attribution = source_rows.get(asset_id)
        if attribution:
            assert attribution['figure'] == figure
            assert attribution['physical_page'] == association['physical_page']
            assert attribution['page_id'] == pages[association['physical_page']]['page_id']
        credit = attributions['source_credit_by_figure'][figure]
        if 'Spak' in credit:
            credit_family = 'Spak'
        elif 'New York City Police' in credit:
            credit_family = 'NYPD'
        else:
            credit_family = attribution['source_credit_family'] if attribution else credit
        records.append({
            'asset_id': asset_id,
            'role': asset['role'],
            'review_status': status,
            'prior_main': asset_id in prior_main,
            'prior_reviewer': asset_id in prior_reviewer,
            'object_key': asset['object_key'],
            'native_dimensions': asset['native_pdf_dimensions'],
            'image': view,
            'decrypted_encoded_stream': decrypted,
            'on_disk_ciphertext_stream': ciphertext,
            'figure_association': association,
            'page': pages[association['physical_page']],
            'document_source_family': 'NIST-NCSTAR-1-9-preserved-report',
            'source_credit_as_displayed': credit,
            'source_credit_family': credit_family,
            'origin_group': attribution['origin_group'] if attribution else 'prior-figure-' + figure if asset_id in prior else 'report-geometry-reference',
            'origin_group_limit': 'Grouping is a report-attributed lineage/credit key, not independent camera custody or proof that different group IDs are independent captures.',
            'new_attribution_record': 'source-attributions.json#' + asset_id if attribution else None,
        })
    counts = dict(Counter(x['review_status'] for x in records))
    source_after = pin(source)
    assert source_before == source_after
    extraction = load(extraction_path)
    verification = load(verification_path)
    assert extraction['source_sha256_before'] == extraction['source_sha256_after'] == SOURCE_SHA
    assert extraction['source_mutated'] is False
    assert verification['source_sha256'] == SOURCE_SHA
    return {
        'schema_version': 1,
        'status': 'exploratory checked derivative; no canonical promotion, appearance adjudication or source authentication',
        'method': 'Set subtraction from both prior review ID lists; independently rehash source/all28 images/all28 decrypted and ciphertext streams/all23 full-page renders and context files; read native dimensions; preserve complete figure associations.',
        'runtime': {'python': platform.python_version(), 'Pillow': PIL.__version__},
        'script': pin(Path(__file__).resolve()),
        'source_before': source_before,
        'source_after': source_after,
        'source_unchanged': source_before == source_after,
        'input_pins': [pin(p) for p in [protocol_path, key_path, main_path, reviewer_path, attrib_path, extraction_path, verification_path]],
        'protocol_input_pins_verified': True,
        'declared_sample_membership_verified': True,
        'counts': {'all_extracted_assets': len(records), 'photographic_assets': len(photo_ids), 'geometry_graphics': len(geometry_ids), 'full_pages': len(pages), **counts, 'new_photo_full_pages': len({r['page']['physical_page'] for r in records if r['review_status'] == 'new_batch2_photographic'})},
        'prior_id_sets_equal': True,
        'all_disk_jpeg_ids_match_key': True,
        'prior_paired_ids': sorted(prior),
        'new_photographic_ids': sorted(new_ids),
        'reference_only_ids': sorted(geometry_ids),
        'source_attribution_namespace': attributions['source']['figure_namespace'],
        'existing_extraction_receipt_scope': extraction['verification_limit'],
        'existing_independent_parser_receipt_status': verification['status'],
        'existing_independent_parser_receipt_scope': verification['limitation'],
        'fresh_check_scope': 'Rehash/dimensions and set coverage only; independent parser extraction was not rerun in batch2. Existing receipts are pinned and attributed, not reported as fresh extraction.',
        'assets': records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    inventory = build()
    destination = HERE / 'inventory01.json'
    if args.check:
        assert load(destination) == inventory, 'inventory changed'
        print(json.dumps({'status': 'pass', 'counts': inventory['counts'], 'inventory_sha256': sha(destination)}))
    else:
        with destination.open('x') as stream:
            json.dump(inventory, stream, indent=2)
            stream.write('\n')
        print(json.dumps({'status': 'created', 'counts': inventory['counts'], 'inventory_sha256': sha(destination)}))


if __name__ == '__main__':
    main()
