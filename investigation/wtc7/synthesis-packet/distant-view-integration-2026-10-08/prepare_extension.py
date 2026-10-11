"""Prepare only the prospective DistantView extension; never mutate an index.

Selected entry-point hashing is not a rerun of inherited checks or source review.
The explicit --write operation creates extension.json exclusively. --check-only
performs the same preparation without writing. --check-saved compares saved bytes.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
MAIN = Path('/Users/admin/docs/911')
OLD = BASE / 'synthesis-packet/integration-2026-10-08'
BASELINE = OLD / 'candidate-index.json'
CURRENT = BASE / 'synthesis-packet/material-claim-index.json'
BASELINE_SHA = '6ad3012fd455dafe4face2cf031a3624135f83c99b24dfe641e6a35e0084f7e1'
PROTOCOL_SHA = 'ea61050d5d95fa2978bb33a093331a9e1e44ad11fe3af7241c4366f5685f58aa'
VALIDATOR_SHA = '97c4cba63dd29ddc0667262a9038bfb86670ee1ddee8e27175e53626c9aaee96'
D = 'distant-view-source-screen/'
C = D + 'continuity-274-411/'
L = D + 'localization-review/'
E = D + 'encoded-timing/'
FD = 'F-DistantView-access-copy'
FF = 'F-FFmpeg-tagged-source'
T = ['T-DistantView-source-screen', 'T-DistantView-contour-correspondence',
     'T-DistantView-localization-packet', 'T-DistantView-encoded-timing']
IDS = ['Q03-DistantView-selected-corner-coverage',
       'Q03-DistantView-contour-correspondence',
       'Q10-DistantView-localization-pilot-pending',
       'Q03-DistantView-PTS-type-association',
       'Q10-DistantView-generated-clock-limit']


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def load_validator():
    path = OLD / 'validate_index.py'
    require(digest(path) == VALIDATOR_SHA, 'old validator changed')
    spec = importlib.util.spec_from_file_location('pinned_old_index_validator', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare():
    v = load_validator()
    roots = (MAIN, BASE.parents[1])
    controls = {}
    for name, path, expected in [('baseline', BASELINE, BASELINE_SHA),
                                 ('protocol', HERE / 'PROTOCOL.md', PROTOCOL_SHA),
                                 ('old_validator', OLD / 'validate_index.py', VALIDATOR_SHA)]:
        actual = v.file_state(path)
        require(actual['sha256'] == expected, name + ' frozen hash changed')
        controls[name] = {'path': str(path.relative_to(BASE)), **actual}
    current_before = v.file_state(CURRENT)
    require(current_before == v.file_state(BASELINE), 'active index is not frozen version2')
    baseline = v.load_json(BASELINE)
    old_artifacts = baseline['integration']['artifacts']
    old_paths = {}
    for aid, row in old_artifacts.items():
        path = v.resolve_file(row['path'], BASE, roots)
        old_paths.setdefault(path, []).append((aid, row))
    artifacts, ids, watched = {}, {}, {}

    def add(label, path_text, role):
        path = v.resolve_file(path_text, BASE, roots)
        state = v.file_state(path)
        watched[path] = state
        if path in old_paths:
            aid, row = old_paths[path][0]
            require(all(row2['bytes'] == state['bytes'] and row2['sha256'] == state['sha256']
                        for _, row2 in old_paths[path]), 'old artifact pin changed: ' + label)
        else:
            aid = f'DVA{len(artifacts) + 1:03d}'
            require(aid not in old_artifacts, 'artifact ID collision')
            artifacts[aid] = {'path': path_text, 'role': role, **state}
            old_paths[path] = [(aid, artifacts[aid])]
        require(label not in ids, 'duplicate preparation label')
        ids[label] = aid
        return aid

    add('charter', str(MAIN / 'research/sherlock-wtc7-investigation/CHARTER.md'),
        'Controlling research charter; reused authority, not new evidence')
    add('archive', str(MAIN / 'research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip'),
        'Held public archive container; nested copies do not establish independent cameras')
    add('avi', D + 'source/DistantViewWTC7.avi', 'Unchanged held access-copy AVI, not authenticated camera original')
    add('preservation', D + 'source/receipt.json', 'Archive/member/copy-preservation receipt, not historical authenticity')
    add('screen_protocol', D + 'PROTOCOL.md', 'Frozen original source-screen method, including failed matching-timestamp requirement')
    add('ordinal_protocol', D + 'ORDINAL-ADDENDUM.md', 'Prospective ordinal-only alternative preserving the original timing failure')
    add('screen_report', D + 'report.md', 'Bounded source-screen interpretation and actual failure/verification account')
    add('screen_root', D + 'root-observations.md', 'Frozen root AI reading of eight selected scenes; shared-source observation')
    add('screen_peer', D + 'peer-observations.md', 'Separately frozen peer AI reading of the same eight scenes, not a new camera')
    add('first_adapter', D + 'prepare.py', 'Preserved initial adapter and embedded controls; original parser contract failed')
    add('ordinal_adapter', D + 'ordinal_screen.py', 'Executed nullable-clock/ordinal adapter with embedded synthetic controls')
    add('decode_base', 'tilted-camera-source-join/prepare_media.py', 'Hash-pinned reused preservation/probe/decode implementation and embedded controls')
    add('first_probe_execution', D + 'probe01/execution.json', 'FFprobe returned-zero execution record; subsequent wrapper KeyError and absent stdout documented in report/addendum')
    for n in ('02', '03'):
        add('old_raw_' + n, D + f'probe{n}-diagnostics/probe-stdout.json', 'Preserved complete old raw FFprobe output with nullable frame fields')
        add('selection_' + n, D + f'probe{n}/selection.json', 'All old nullable timing rows and fixed eight-ordinal selection')
    for n in ('01', '02'):
        add('screen_frames_' + n, D + f'views{n}/frames.json', 'Saved all-frame hash records and selected-image lineage; manifest, not independent video decoding')
    add('screen_checker', D + 'verify_independent.py', 'Separate source/nullable-row/PNG arithmetic checker and embedded synthetic controls')
    add('screen_receipt', D + 'independent-verification.json', 'Prior actual checker result and 59-pin closure entry point; scope excludes independent video decode')

    for label, name, role in [
        ('contour_protocol', 'PROTOCOL.md', 'Frozen all138-frame/all137-link categorical screen contract'),
        ('contour_report', 'report.md', 'Correspondence-feasibility result, changing-silhouette alternative and clock limits'),
        ('contour_root', 'root-observations.json', 'Frozen root AI frame/link judgments and actual-view record'),
        ('contour_peer', 'peer-observations.json', 'Frozen peer AI frame/link judgments, including299–300 softening'),
        ('contour_compare', 'comparison.json', 'Derived roster counts, runs and categorical comparison, not accuracy estimate'),
        ('contour_code', 'derive.py', 'Executed native/crop/contact-page construction and roster controls'),
        ('contour_checker', 'verify_independent.py', 'Separate pixel/mapping/roster checker; shares label renderer and does not redecode AVI'),
        ('contour_execution', 'execution.md', 'Actual commands, review stages and preservation limits'),
        ('contour_precheck', 'pre-view-verification.json', 'Pre-reading derivative verification without source classifications'),
        ('contour_finalcheck', 'final-verification.json', 'Post-freeze derivative/roster check and 660-pin entry point; not human acceptance'),
    ]:
        add(label, C + name, role)
    for n in ('01', '02'):
        add('contour_frames_' + n, C + f'run{n}/frames.json', 'Native/crop identities, nullable timing copies and exact source rectangles')
        add('contour_pages_' + n, C + f'run{n}/pages.json', 'Complete contact-page cell mappings; selected pixels remain in inherited verification closure')

    for label, name, role in [
        ('pilot_protocol', 'PROTOCOL.md', 'Frozen six-frame human localization preparation contract'),
        ('pilot_report', 'report.md', 'Reported software/browser verification and unresolved Fit-targeting miss; not human observations'),
        ('pilot_instructions', 'HUMAN-REVIEW.md', 'Pending user-only response instructions; no acceptance supplied'),
        ('pilot_builder', 'build_packet.py', 'Packet construction and embedded controls, including narrow nonserved FFmpeg-alias exception'),
        ('pilot_server', 'serve_review.py', 'Local read-only server adapter, not a currently witnessed running service'),
        ('pilot_verifier', 'verify_packet.mjs', 'Separate byte/metadata/route checker; not image decoder or localization-accuracy test'),
        ('pilot_html', 'review.html', 'Read-only viewer source with uninspected/null historical defaults'),
        ('pilot_ui', 'review.mjs', 'Viewer interaction implementation, not historical coordinates'),
        ('pilot_response', 'response.mjs', 'Session-draft response validator, not human authentication'),
        ('pilot_mapping_tests', 'test_mapping.mjs', 'Synthetic mapping controls, not feature-localization accuracy'),
        ('pilot_response_tests', 'test_response.mjs', 'Synthetic response/lifecycle controls, not historical observations'),
    ]:
        add(label, L + name, role)
    for n in ('01', '02'):
        add('pilot_manifest_' + n, L + f'packet{n}/manifest.json', 'Prepared packet manifest with six ordinals, false acceptance/coordinate flags, 660 inherited plus17 packet-input pins')

    for label, name, role in [
        ('timing_protocol', 'PROTOCOL.md', 'Prospective default/genpts metadata-only comparison and explicit interpretation ceilings'),
        ('timing_report', 'report.md', 'Metadata findings, retained failures and source-code interpretation; no recovered capture clock'),
        ('timing_code', 'audit.py', 'Executed finite metadata/payload accounting implementation'),
        ('timing_tests', 'test_audit.py', 'Synthetic metadata, null, mapping and failure-retention controls'),
        ('timing_checker', 'verify.mjs', 'Separate raw-JSON arithmetic/source-slice checker; no independent decoder'),
        ('ff_avi', 'avidec.c', 'Official n7.1.1 AVI demuxer source for semantics; not proved identical compiled execution'),
        ('ff_demux', 'demux.c', 'Official n7.1.1 packet/timestamp handling source for semantics'),
        ('ff_decode', 'decode.c', 'Official n7.1.1 best-effort timestamp selection source for semantics'),
    ]:
        add(label, E + name, role)
    for n in ('01', '02'):
        for label, tail, role in [
            ('timing_default_', 'default/stdout.json', 'Complete raw default FFprobe packet/frame records; frame PTS are processed metadata'),
            ('timing_generated_', 'genpts/stdout.json', 'Complete explicit genpts diagnostic output, never substituted into old records'),
            ('timing_analysis_', 'analysis.json', 'Derived counts, exact ordinal-gap arithmetic, joins and arm differences'),
            ('timing_receipt_', 'receipt.json', 'Actual process/diagnostic record, before/after pins and11 output-pin entry point'),
        ]:
            add(label + n, E + f'run{n}/' + tail, role)
        add('timing_independent_' + n, E + f'run{n}-independent.json', 'Executed independent arithmetic check receipt with explicit limits')

    # Fixed identity controls used in these completed units, not new source choices.
    expected = {
        'avi': 'a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e',
        'screen_report': '5807c05db2e79139ea4da5c0e7ffed7a48ee8b04f4a00f698afa717f6fca5799',
        'contour_report': '02923415257177de1511947fd889bb854694429e8073748dc32947661cc4f029',
        'pilot_report': '277e1c03f13e18491d41fba367d32784750eb2fa35203851a177ed50d679c311',
        'timing_report': 'c90b1a9ecc6bbf585304082b576feff555fc31f01f1cdcffb535b24744139c70',
    }
    merged_artifacts = {**old_artifacts, **artifacts}
    for label, sha in expected.items():
        require(merged_artifacts[ids[label]]['sha256'] == sha, 'reviewed source changed: ' + label)

    def a(*labels):
        values = [ids[label] for label in labels]
        require(len(values) == len(set(values)), 'duplicate transform artifact')
        return values

    transforms = {
        T[0]: {
            'input_artifacts': a('charter', 'archive', 'avi', 'screen_protocol', 'ordinal_protocol'),
            'code_artifacts': a('first_adapter', 'ordinal_adapter', 'decode_base', 'screen_checker'),
            'output_artifacts': a('preservation', 'first_probe_execution', 'old_raw_02', 'old_raw_03',
                                  'selection_02', 'selection_03', 'screen_frames_01', 'screen_frames_02',
                                  'screen_root', 'screen_peer', 'screen_report'),
            'verification_artifacts': a('screen_receipt'),
            'status': 'existing_executed_ordinal_screen_not_rerun_in_integration',
            'missing': ['Original complete matching-timestamp contract failed; probe01 raw stdout was not retained.',
                        'Authenticated capture/master chronology, independent-camera relation and lower-step descending coverage remain unestablished.'],
            'limit': 'Eight selected native Y images, two AI readings on one access copy. Old source/frame/PNG checks are linked, not rerun. The checker compared all saved frame hashes but did not independently decode unselected video pixels. Initial12 passing controls did not cover the failed parser contract; ordinal adapter timeout partial-stdout and oversized-response receipt limits remain. Later units extend only their separately declared scopes.'
        },
        T[1]: {
            'input_artifacts': a('avi', 'contour_protocol', 'screen_frames_01', 'selection_02'),
            'code_artifacts': a('contour_code', 'contour_checker'),
            'output_artifacts': a('contour_frames_01', 'contour_frames_02', 'contour_pages_01', 'contour_pages_02',
                                  'contour_root', 'contour_peer', 'contour_compare', 'contour_report'),
            'verification_artifacts': a('contour_execution', 'contour_precheck', 'contour_finalcheck'),
            'status': 'existing_executed_categorical_correspondence_screen_not_rerun_in_integration',
            'missing': ['Fixed material-point identity, original exposure cadence, coordinates, scale and feature-to-body relation remain unestablished.'],
            'limit': 'All138 frames and137 links were judged under the fixed crop/page/three-context contract. Both passes are AI observations, not human/expert acceptance; zero categorical disagreement is not zero localization error. Peer299–300 tonal softening and changing-projected-silhouette alternative remain. The final660-pin receipt is an entry point: this integration does not rehash its entire closure or view images. Separate pixel checker shares the label renderer and does not itself redecode AVI.'
        },
        T[2]: {
            'input_artifacts': a('pilot_protocol', 'contour_frames_01', 'contour_finalcheck'),
            'code_artifacts': a('pilot_builder', 'pilot_server', 'pilot_verifier', 'pilot_html', 'pilot_ui',
                                'pilot_response', 'pilot_mapping_tests', 'pilot_response_tests'),
            'output_artifacts': a('pilot_manifest_01', 'pilot_manifest_02', 'pilot_instructions', 'pilot_report'),
            'verification_artifacts': a('pilot_report', 'pilot_manifest_01', 'pilot_manifest_02'),
            'status': 'packet_prepared_and_scoped_software_checks_recorded_actual_human_responses_pending',
            'missing': ['Actual attributable six-frame user observations or explicit unavailability are pending.',
                        'Automated feature-localization accuracy/abstention challenge has not been executed; Fit targeting cause remains unresolved.'],
            'limit': 'Two byte-identical packets and recorded96 software tests concern UI/bookkeeping, not feature accuracy or96 scientific observations. Manifests retain660+17 dependency pins and generated-prefix/copied-product identities; inherited files are not flattened or rerun here. Browser QA was root-reported and synthetic-only; historical image loads received DOM/metadata checks without coordinates. Fit intended500,180 produced500,179 with no delivered-event log;100/200 percent and keyboard guidance is not a precision guarantee. Initial alias/test/HTTP failures remain in report; no actual human, expert, current-live-server or forensic-security acceptance is supplied.'
        },
        T[3]: {
            'input_artifacts': a('avi', 'old_raw_02', 'old_raw_03', 'timing_protocol', 'ff_avi', 'ff_demux', 'ff_decode'),
            'code_artifacts': a('timing_code', 'timing_tests', 'timing_checker'),
            'output_artifacts': a('timing_default_01', 'timing_generated_01', 'timing_analysis_01',
                                  'timing_default_02', 'timing_generated_02', 'timing_analysis_02', 'timing_report'),
            'verification_artifacts': a('timing_receipt_01', 'timing_receipt_02', 'timing_independent_01', 'timing_independent_02'),
            'status': 'existing_executed_metadata_comparison_not_rerun_in_integration',
            'missing': ['Untraced compiled execution branches, independent MPEG4 picture/bitstream correspondence and historical capture chronology remain unknown.'],
            'limit': 'Default and explicit genpts arms internally decode for FFprobe metadata; no image/audio output or pixel comparison in this unit. Source-slice hashing and unique positions establish reported payload accounting, not one packet per exposure. Nulls/old strict-PTS failure remain untouched. Official code supports possible semantics, not every executed branch or an exact dynamic-library build lock. Independent checks use the same raw FFprobe outputs and leave ancillary producer flags/status-label wording unchecked as recorded. Initial syntax/source-download/checker issues are retained in the report; source/diagnostic/output pins are reached through the two run receipts.'
        },
    }

    families = {
        FD: {
            'description': 'One held DistantView access-copy lineage, from duplicate embedded AVI bytes in a single public archive, through decoded derivatives, observations, packet preparation and metadata diagnostics.',
            'basis': [
                {'artifact_id': ids['preservation'], 'locator': 'parent, outer_member, outer_sha256, ordinals and media'},
                {'artifact_id': ids['screen_report'], 'locator': 'Source and fixed coverage; Why no publication table comparison was run'},
            ],
            'independence_limit': 'The two embedded copies, repeated decodes/probes, crops, two AI readers and genpts arm are not independent historical origins. Relation to F-Camera2 remains unresolved: this grouping neither declares another independent camera nor proves the same camera. Different graphics, framing or filenames are insufficient. R1 human judgments and other source families are not transferred into DistantView acceptance.',
            'origin_status': 'identified_at_declared_layer',
        },
        FF: {
            'description': 'Three official FFmpeg n7.1.1 source files documenting software timestamp paths, not observations of the WTC7 event.',
            'basis': [
                {'artifact_id': ids['ff_avi'], 'locator': 'get_duration lines139–146; stream timing675–714; packet DTS1540–1576'},
                {'artifact_id': ids['ff_demux'], 'locator': 'compute_pkt_fields1002–1121; parser1232–1249; genpts1541–1587'},
                {'artifact_id': ids['ff_decode'], 'locator': 'guess_correct_pts289–312; application699–701'},
            ],
            'independence_limit': 'One software-project/tag family. Three files and two code readers are not three event witnesses or proof of the installed binary’s complete executed branches. Source-code interpretation and historical media evidence have different roles; source-download failures and compiled/runtime limitations are retained in the timing report.',
            'origin_status': 'identified_at_declared_layer',
        },
    }

    claims = [
        {'id': IDS[0], 'parent_claim': 'Q03-observed-sequence',
         'claim': 'Both frozen eight-scene AI readings identify the outer image-right corner in standing scenes and at a lower position in ordinal411; neither recovers the lower roof-step junction separately in that descending sample.',
         'layer': 'qualified_AI_observation_of_access_copy_derivatives',
         'grade': 'A for the recorded readings; B for bounded visual coverage under the declared screen',
         'ceiling': 'Eight selected scenes, not onset, continuous material identity, coordinates, physical calibration or an independent-camera finding.',
         'alternative': 'A changing projected silhouette, obscuration or a related processed copy can supply the recognizable corner without a fixed physical point or new independent view.',
         'would_change_with': 'A source-specific contrary feature identification or authenticated view/exposure relation; later continuity evidence extends only its own fixed interval.'},
        {'id': IDS[1], 'parent_claim': 'Q03-observed-sequence',
         'claim': 'Two separately frozen AI readings record V for all138 frames274–411 and supported for all137 adjacent contour links, with no categorical disagreement.',
         'layer': 'qualified_visual_correspondence_observation_and_roster_arithmetic',
         'grade': 'A for preserved roster counts; B for the declared visual-correspondence-feasibility judgment',
         'ceiling': 'Not a fixed material point, equally spaced original exposures, human/expert acceptance, localization-error estimate, measured trajectory or causal transition.',
         'alternative': 'A changing projected silhouette can preserve a recognizable junction. Peer-noted299–300 tonal softening remains despite the supported link.',
         'would_change_with': 'A qualified contrary identification or unsupported adjacent pair would defeat the uninterrupted combined criterion unless resolved through prospectively declared evidence; do not discard it because the two AI readers agreed.'},
        {'id': IDS[2], 'parent_claim': 'Q10-tool-and-record-limits',
         'claim': 'The six-frame DistantView localization packet is prepared with no proposed historical coordinates; actual attributable human responses remain pending.',
         'layer': 'research_preparation_and_pending_user_observation_state',
         'grade': 'A for saved packet flags and documented preparation; no human localization result',
         'ceiling': 'Synthetic software/browser checks do not establish feature-localization accuracy. The unresolved Fit intended500,180 to reported500,179 miss is not a general one-pixel bound or diagnosed quantization.',
         'alternative': 'The apparent Fit targeting miss could reflect input delivery, geometry changes or a mapping issue; a prepared viewer can still be inadequate for a particular user or feature.',
         'would_change_with': 'Preserved actual six-frame user judgments or explicit unavailability; recurring fine-view mismatch blocks coordinate use. A later automated locator separately requires a frozen synthetic accuracy/abstention challenge.'},
        {'id': IDS[3], 'parent_claim': 'Q03-observed-sequence',
         'claim': 'Default FFprobe output lacks frame PTS on all4 I and325 P pictures and none of633 B pictures; final ordinal961 alone lacks best-effort, in both repeated metadata runs.',
         'layer': 'derived_file_tool_metadata_observation',
         'grade': 'A for raw-output counts and exact field comparisons in this file/tool configuration',
         'ceiling': 'This systematic missingness is not affirmative evidence of missing historical exposures. Old stored_pts is decoded-frame output, not necessarily a literal AVI or camera timestamp; the original strict gate remains failed.',
         'alternative': 'Documented codec/demux processing can produce the pattern, while prior editing, dropped/duplicated exposures or cadence conversion can coexist with orderly metadata.',
         'would_change_with': 'A contradictory raw-output/field mapping or independently established picture/bitstream relation could change the processing account; authenticated camera/master chronology is needed for capture timing.'},
        {'id': IDS[4], 'parent_claim': 'Q10-tool-and-record-limits',
         'claim': 'Explicit genpts output adds329 frame PTS,329 packet PTS and one best-effort field, producing frame labels1–962 without changes to the checked payloads or other requested identity fields.',
         'layer': 'derived_generated_metadata_result_with_conditional_source_code_interpretation',
         'grade': 'A for output arithmetic and payload accounting; C for an untraced internal processing explanation; D for authentic capture timing',
         'ceiling': 'Generated regularity does not recover the camera clock, certify pixel identity, prove one packet per exposure, clear the failed original contract or admit labels into a physical measurement.',
         'alternative': 'A processed or cadence-converted recording can receive the same orderly labels; untested packed/multiple/uncoded-picture semantics and build/runtime differences remain.',
         'would_change_with': 'A contradictory source/bitstream mapping or executed-branch evidence could revise the explanation; a traceable camera/master chronology could address historical cadence. Any later measurement using generated labels requires its own explicit conditional protocol.'},
    ]

    def evidence(label, locator, role, family=FD):
        return {'artifact_id': ids[label], 'locator': locator, 'role': role, 'family_id': family}

    def link(n, evidence_rows, gap, d8_scope=None):
        deps = [] if d8_scope is None else [{
            'id': 'D8', 'relation': 'limits', 'scope': d8_scope,
            'basis': 'Physical feature/projection/capture-clock joins are additional inference requirements, not prerequisites to recording these contours or file metadata.'}]
        absent = {'causal_links': {
            'kind': 'not_applicable',
            'reason': 'This source/contour/metadata/preparation result establishes none of the eight mechanical transitions.',
            'consequence': 'No causal-support edge, initiation mechanism, force result or ranking change is supplied.'}}
        if not deps:
            absent['dependencies'] = {
                'kind': 'not_applicable',
                'reason': 'This exact pending-human/preparation state is not a D1–D9 physical test; its human and future method gates are explicit in remaining_gap.',
                'consequence': 'Do not require native solver files to inspect the packet, or treat software checks as satisfaction of the human/physical gates.'}
        return {
            'question': 'Q03' if n in (0, 1, 3) else 'Q10',
            'work_packages': [
                {'id': 'WP01', 'role': 'Selected-input lineage only'},
                {'id': 'WP02', 'role': 'Auditable route and review boundaries'},
                {'id': 'WP12', 'role': 'Scoped reproduction and contrary limits'},
                {'id': 'WP05', 'role': (
                    'Source-visibility precursor, not a motion measurement',
                    'Ordinal-contour correspondence, not fixed material identity',
                    'Localization preparation only; actual human responses pending',
                    'Encoded timing metadata, not the capture clock',
                    'Generated-label conditionality, not recovered historical timing',
                )[n]}],
            'dependencies': deps, 'causal_links': [], 'evidence': evidence_rows,
            'transforms': [T[(0, 1, 2, 3, 3)[n]]],
            'verification_status': {
                'source_inspection': 'Prior source-unit observations/metadata and relevant code readings are linked; this integration adds no media viewing, listening or source acquisition.',
                'calculation_reproduction': 'Prior scoped verification is recorded in the linked transform; only selected entry-point hashes and references are checked in this integration, not its entire inherited closure or historical calculations.',
                'human_acceptance': 'No DistantView human responses or acceptance supplied; R1 and other existing actual human records remain unchanged and are not transferred.',
                'expert_review': 'No independent qualified forensic/engineering acceptance supplied. Prior AI method/checker contributions are not expert or author-independent validation.'},
            'remaining_gap': gap, 'absences': absent,
        }

    links = {
        IDS[0]: link(0, [
            evidence('avi', 'Complete held AVI bytes; selected decoded ordinals0,137,274,411,549,686,823,961 identified by selection manifests', 'Underlying access-copy input only; no new image reading or authentication in this integration'),
            evidence('preservation', 'parent, outer_member, outer_sha256, ordinals and media', 'Preserved nested-archive identity and duplicate-copy relation, not independent historical source evidence'),
            evidence('screen_root', 'Descriptions by frame ordinal:0,137,274,411; Fixed Camera2 contextual comparison; Result and next test', 'Frozen prior-informed AI visual observations, not primary camera metadata or calibrated motion'),
            evidence('screen_peer', 'Descriptive readings:0000,0137,0274,0411; Coverage disposition and possible next test', 'Second frozen reading of the same source derivatives, not independent filming'),
            evidence('screen_report', 'Why no publication table comparison was run; Executed checks and retained failures', 'Interpretive limit: different time-zero definitions and absent exposure join; records wrapper failure despite FFprobe return0'),
        ], 'Selected lower-step descending coverage, material identity and independent view/source chronology remain unestablished. The later correspondence screen advances the outer corner only; no lag-fitted publication-table join is authorized.',
           'Only converting the selected apparent corner coverage into physical feature identity, cross-camera timing or geometry; not the eight-scene observation itself'),
        IDS[1]: link(1, [
            evidence('contour_root', 'frames[ordinal274..411], links[from274..410], actual_views and first_pass_frozen_before_peer_exchange', 'Frozen categorical frame/link AI judgments and inspection attestation; no human or coordinate data'),
            evidence('contour_peer', 'frames[ordinal274..411], links[from274..410], including link299→300 reason; actual_views and prior_knowledge', 'Separate same-source AI judgments retaining tonal/texture softening despite supported correspondence'),
            evidence('contour_compare', 'readers, frame_status_disagreements, link_status_disagreements, combined_uninterrupted_observational_candidate and limits', 'Derived roster arithmetic and comparison, not observer-accuracy calibration'),
            evidence('contour_report', 'What was seen, and what could make the interpretation wrong; Next prerequisite and stop', 'Changing-silhouette alternative and explicit limits on material identity, clocks, geometry and automatic measurement'),
            evidence('contour_finalcheck', 'counts, rosters, runs, input_pins_unchanged and limits', 'Existing structural/pixel/mapping check and dependency-closure entry point, not certification of visual truth'),
        ], 'Actual six-frame human localization observations and a separately frozen automatic accuracy/abstention challenge remain pending; fixed material identity, original timing, scale/projection, deformation and feature-to-body mapping remain distinct physical requirements.',
           'Only physical interpretation of the recognized contour as a fixed body/feature with calibrated time and projection; not recording ordinal categorical correspondence'),
        IDS[2]: link(2, [
            evidence('pilot_manifest_01', 'frame_order, historical_coordinates_generated, human_observations_or_acceptance, source_images_copied_or_converted and routes', 'Prepared six-frame packet and false acceptance/coordinate flags; not authentication of a future user'),
            evidence('pilot_manifest_02', 'Same frame_order and product pins as packet01', 'Repeated preparation copy, not another observation'),
            evidence('pilot_instructions', 'What to inspect; Returning your observations', 'User-only pending observation contract; subjective inclusive boxes, null statuses and no default statistical confidence interval'),
            evidence('pilot_report', 'Actual browser checks and unresolved display limit; Failures and review disposition; Local operation and next gate', 'Root-reported synthetic browser QA and retained Fit miss; no independent browser witness or historical localization accuracy'),
        ], 'Six attributable actual human responses or explicit unavailability remain needed for this pilot; generated flags/session drafts do not supply them. Fine-view mismatch would block coordinate use. Future automation needs separate synthetic accuracy/abstention validation; physical clock/geometry/body joins remain separate, and six favorable responses would not certify all138 frames.'),
        IDS[3]: link(3, [
            evidence('timing_default_01', 'packets_and_frames entries with type=frame: pict_type, pts, best_effort_timestamp, pkt_dts and pkt_pos; streams[0].time_base', 'Raw reported default FFprobe metadata, not authenticated original exposure timestamps'),
            evidence('timing_default_02', 'Same raw frame/packet/stream records as run01', 'Same-tool repeatability, not a second capture source'),
            evidence('timing_analysis_01', 'arms.default.frame_summaries.all and selected_274_411; arms.default.packet_summary; baseline_comparisons', 'Derived missingness/type tables and null-aware ordinal-gap arithmetic'),
            evidence('timing_independent_01', 'independent.default.tabs, selected_tabs, frame_pts_offsets, frame_best_effort_offsets and limitations', 'Independent arithmetic on shared raw metadata, not independent decoding'),
            evidence('ordinal_protocol', 'Revised output contract', 'Preserved original strict-timing failure and separate nullable fields; never replaced by later generated values'),
            evidence('timing_report', 'Why the distinction matters; Effect on the investigation and next boundary', 'Interpretation narrows the old stored_pts shorthand without rewriting old fields or authenticating historical cadence'),
        ], 'Capture/master chronology and independent picture/bitstream mapping remain unresolved. Known metadata regularity and picture-type association do not establish absence of edits, dropped/duplicated exposures or cadence conversion; the original complete matching-PTS test remains failed.',
           'Only historical exposure timing or calibrated/cross-camera use of these metadata labels; not the null/type tabulation'),
        IDS[4]: link(4, [
            evidence('timing_generated_01', 'packets_and_frames: generated packet/frame pts and best_effort_timestamp; streams', 'Explicitly generated diagnostic arm, distinct from default metadata and from historical camera time'),
            evidence('timing_generated_02', 'Same genpts output records as run01', 'Repeated same-configuration output, not independent clock evidence'),
            evidence('timing_analysis_01', 'arm_differences.all and identity; arms.genpts.frame_summaries; arms.default/arms.genpts.payload_checks and joins', 'Derived329/329/1 absent-to-present changes and packet-source accounting; not pixel or exposure identity'),
            evidence('timing_independent_01', 'changes_by_field, independent.genpts, raw_hashes and limitations', 'Executed separate arithmetic/source-slice check with stated coverage limits'),
            evidence('timing_independent_02', 'changes_by_field, independent.genpts, raw_hashes and limitations', 'Second-run independent-check receipt on repeated inputs, not another historical origin'),
            evidence('ff_avi', 'get_duration139–146; stream time base675–714; packet DTS1540–1576', 'Primary code for possible counter-derived AVI timing; no executed-branch proof', FF),
            evidence('ff_demux', 'compute_pkt_fields1002–1121; parser1232–1249; genpts1541–1587', 'Primary code for possible default filling/look-ahead/EOF fallback, not recovered original timestamps', FF),
            evidence('ff_decode', 'guess_correct_pts289–312; application699–701', 'Primary code selecting supplied PTS/DTS using fault counts, not interpolation of missing exposures', FF),
            evidence('timing_report', 'Verification and preserved failures; Effect on the investigation and next boundary', 'Scoped checks, untraced explanation, retained failures and prohibition on automatic measurement adoption'),
        ], 'Actual internal branch attribution, independent picture/bitstream correspondence and original capture clock remain unestablished. Any later use of generated labels requires an explicit conditional measurement protocol, not a silent repair of old nulls; no new probe or bitstream expansion is authorized by this integration.',
           'Only a future physical-time/cross-camera inference using generated labels; not this bounded software-output comparison'),
    }

    scope = ('Research-only additive integration of four completed DistantView units. '
             'All version2 records, claims, links, statuses, failures and review history remain unchanged; '
             'the dated supplement adds source-qualified observations, pending-human preparation and metadata limits. '
             'Selected entry points are pinned, not every inherited dependency reverified. No new measurement, '
             'camera independence, human/expert acceptance, cause ranking or canonical promotion follows.')
    result = {
        'version': 1,
        'controls': controls,
        'root_updates': {
            'version': 3, 'date': '2026-10-08', 'scope': scope,
            'remaining_index_work': ('The baseline40 claims, prior18 additions and five DistantView additions are traversable at their stated ceilings. '
                                     'This is not full scientific acceptance, corpus exhaustion, engine import or a cause assessment. '
                                     'Actual DistantView localization responses, graph review, uncompleted F7 provenance, '
                                     'physical clock/geometry/body joins, native structural inputs and other preserved charter gaps remain separate.')},
        'additions': {'artifacts': artifacts, 'families': families, 'transforms': transforms,
                      'additional_claims': claims, 'claim_links': links},
        'revision': {
            'date': '2026-10-08',
            'units': [{'id': 'source-screen', 'claim_ids': [IDS[0]], 'transform_ids': [T[0]]},
                      {'id': 'contour-correspondence', 'claim_ids': [IDS[1]], 'transform_ids': [T[1]]},
                      {'id': 'localization-packet', 'claim_ids': [IDS[2]], 'transform_ids': [T[2]]},
                      {'id': 'encoded-timing', 'claim_ids': IDS[3:], 'transform_ids': [T[3]]}],
            'status_supplements': {
                'Q03-observed-sequence': {
                    'disposition': 'DistantView now supplies an eight-scene outer-corner coverage lead and two frozen complete274–411 contour readings. Encoded nulls align with picture type, not affirmative evidence of missing exposures. These additions do not replace the earlier StageC correction: frame6959 is not established as the first frame without any visible bump, and component passage remains unresolved.',
                    'supporting_claim_ids': [IDS[0], IDS[1], IDS[3]],
                    'limit': 'No fixed material point, independently authenticated camera, source-clock recovery, physical trajectory, cross-camera lag or native-model join. The lower west-center junction is not substituted by the clearer outer corner; all old Q03 statuses remain exactly preserved.'},
                'Q10-tool-and-record-limits': {
                    'disposition': 'A six-frame localization packet is prepared but actual human responses remain pending. The completed default/genpts test distinguishes raw nulls, generated metadata and possible software paths without repairing the earlier strict timing gate. Prior Faraday, source-access and other tool dispositions remain unchanged.',
                    'supporting_claim_ids': [IDS[2], IDS[4]],
                    'limit': 'Unresolved Fit targeting remains; software tests do not establish feature accuracy. No actual human/expert acceptance, decoded-picture/bitstream authentication, generated-clock measurement admission, solver/bridge activation or automatic continuation of stopped routes.'}},
            'limits': {'human_acceptance_supplied': False, 'expert_acceptance_supplied': False,
                       'cause_ranking_changed': False, 'canonical_promotion': False, 'new_measurement': False},
            'scope': scope,
        },
    }
    require(len(claims) == len(links) == 5 and len(transforms) == 4 and len(families) == 2, 'finite extension counts')
    require(set(links) == set(IDS), 'claim IDs differ')
    require(not set(links) & set(baseline['integration']['claim_links']), 'claim collision')
    require(not set(transforms) & set(baseline['integration']['transforms']), 'transform collision')
    require(not set(families) & set(baseline['integration']['families']), 'family collision')
    reached = {row['artifact_id'] for link_row in links.values() for row in link_row['evidence']}
    for transform in transforms.values():
        for field in ('input_artifacts', 'code_artifacts', 'output_artifacts', 'verification_artifacts'):
            reached.update(transform[field])
    require(set(artifacts) <= reached, 'unreachable selected artifact')
    require(all(aid in merged_artifacts for aid in reached), 'unknown artifact reference')
    for name, row in controls.items():
        require(v.file_state(BASE / row['path']) == {k: row[k] for k in ('bytes', 'sha256')}, 'control changed: ' + name)
    require(v.file_state(CURRENT) == current_before, 'active index changed during preparation')
    require(all(v.file_state(path) == state for path, state in watched.items()), 'selected artifact changed during preparation')
    return result, ids


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check-only', action='store_true')
    mode.add_argument('--check-saved', action='store_true')
    mode.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result, ids = prepare()
    raw = (json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
    output = HERE / 'extension.json'
    if args.write:
        with output.open('xb') as f:
            f.write(raw)
    elif args.check_saved:
        require(output.read_bytes() == raw, 'saved extension differs from exact preparation')
    print(json.dumps({'status': 'prepared_not_frozen_or_adopted', 'mode': 'write' if args.write else 'check-saved' if args.check_saved else 'check-only',
                      'path': str(output), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                      'new_artifacts': len(result['additions']['artifacts']), 'new_claims': 5, 'new_transforms': 4,
                      'new_families': 2, 'reused_artifact_ids': sorted(set(ids.values()) - set(result['additions']['artifacts'])),
                      'limit': 'No candidate/current-index generation, no historical rerun, no full inherited closure recheck or scientific acceptance.'}, indent=2))


if __name__ == '__main__':
    main()
