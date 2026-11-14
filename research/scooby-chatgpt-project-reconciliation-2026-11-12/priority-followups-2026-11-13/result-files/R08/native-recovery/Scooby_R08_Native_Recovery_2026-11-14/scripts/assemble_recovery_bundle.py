#!/usr/bin/env python3
"""Assemble verified native sources and explicitly derived audit products."""
import csv,datetime,hashlib,html,json,pathlib,shutil,subprocess,zipfile
from urllib.parse import urlparse
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT.parent/'outputs'
BUNDLE=OUT/'Scooby_R08_Native_Recovery_2026-11-14'
NAMES=['drawings.xlsx','CB-DA-AMB.xlsx','CB-DA.xlsx','CB-DA-SC.xlsx','CB-SP.xlsx','CB-SP-SC.xlsx']
def h(x):return html.escape(str(x if x is not None else ''))
def sha(p):
 d=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):d.update(b)
 return d.hexdigest()
def read(p):return json.loads(p.read_text())
def copy(src,dest):
 dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
def table(headers,rows):
 return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+h(v)+'</th>' for v in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def code(x):return '<code>'+h(x)+'</code>'
def link(url,label):return '<a href="'+h(url)+'">'+h(label)+'</a>'
def main():
 OUT.mkdir(exist_ok=True);BUNDLE.mkdir(exist_ok=True)
 invs={name:read(ROOT/'native_inventory'/pathlib.Path(name).stem/'inventory.json') for name in NAMES}
 sps=next(s for s in invs['CB-SP-SC.xlsx']['sheets'] if 'FireLoading' in s['sheet'])
 assert sps['data_row_count']==16949, 'Wait for final timed-row refinement'
 assert sum(len(v['sheets']) for v in invs.values())==30
 attempts=read(ROOT/'direct_get/attempts.json')
 manifests=[]
 for n in NAMES:
  src=ROOT/'direct_get/native'/n
  a=next(x for x in attempts if x.get('saved_relative_path')=='native/'+n)
  assert a['http_status']==200 and a['valid_xlsx'] and sha(src)==a['native_file_sha256']==invs[n]['sha256']
  copy(src,BUNDLE/'native'/n)
  manifests.append({'bundle_path':'native/'+n,'acquisition_alias':n,'official_filename':pathlib.Path(urlparse(a['final_url']).path).name,
    'requested_url':a['requested_url'],'final_url':a['final_url'],'retrieval_started_utc':a['started_utc'],'retrieval_finished_utc':a['finished_utc'],
    'route_http_status':a['redirects'][0]['http_status'] if a['redirects'] else a['http_status'],'final_http_status':a['http_status'],
    'bytes':src.stat().st_size,'sha256':a['native_file_sha256'],'http_mime_type':a['content_type'],
    'detected_mime_type':subprocess.check_output(['file','--brief','--mime-type',str(src)],text=True).strip(),
    'zip_crc_verified':invs[n]['zip_crc_error_member'] is None,'xlsx_xml_parsed':True,'sheet_count':len(invs[n]['sheets'])})
 for f in ROOT.joinpath('native_inventory').rglob('*'):
  if f.is_file() and 'drawings_media' not in f.parts:
   copy(f,BUNDLE/'audit/native_inventory'/f.relative_to(ROOT/'native_inventory'))
 for f in ROOT.joinpath('alternate_routes').rglob('*'):
  if f.is_file():copy(f,BUNDLE/'provenance/alternate_routes'/f.relative_to(ROOT/'alternate_routes'))
 copy(ROOT/'direct_get/attempts.json',BUNDLE/'provenance/direct_get_attempts.json')
 copy(ROOT/'direct_get/responses/project.body',BUNDLE/'provenance/nist_project_page.html')
 copy(ROOT/'web_reader_attempts.json',BUNDLE/'provenance/web_reader_attempts.json')
 for f in ['agent_official_routes.json','gate_event_clock_checks.json','gate_small_sheet_cells.json','gate_evidence_notes.json','gate_evidence_notes.md',
           'corrected_instrument_map.csv','channel_crosswalk_sources.json','instrument_map_summary.json','instrument_map_discrepancies.md',
           'instrument_map_definition_discrepancies.json','instrument_map_unjoined_channels.json','instrument_map_dictionary_channels_without_headers.json',
           'drawing_media_inventory.csv','drawing_VD_positions_observed_and_derived.json','published_uncertainty_map.csv']:
  p=ROOT/f
  assert p.exists(), f'Missing expected audit output: {f}'
  copy(p,BUNDLE/'audit'/f)
 for f in ROOT.joinpath('gate_reports').iterdir():
  if f.is_file():copy(f,BUNDLE/'sources/reports'/f.name)
 for f in ROOT.joinpath('prior/Scooby').iterdir():
  if f.is_file():copy(f,BUNDLE/'sources/prior_audit'/f.name)
 for f in ROOT.joinpath('drawings_inspection').glob('*.png'):copy(f,BUNDLE/'previews'/f.name)
 copy(ROOT/'drawings_inspection/render_manifest.json',BUNDLE/'provenance/drawing_render_manifest.json')
 scripts=['recover_nist.py','inventory_native.py','build_channel_crosswalk.py','audit_primary_time_and_export.py','finish_inventory.py','write_published_uncertainty_map.py','drawing_visual_review.py','render_drawings.py','assemble_recovery_bundle.py']
 for f in scripts:
  if (ROOT/f).exists():copy(ROOT/f,BUNDLE/'scripts'/f)
 (BUNDLE/'provenance/native_file_manifest.json').write_text(json.dumps(manifests,indent=2)+'\n')
 with (BUNDLE/'provenance/native_file_manifest.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(manifests[0]));w.writeheader();w.writerows(manifests)
 # Compact tables are calculated from the preserved XML inventory; source data are not edited.
 sheetrows=[];datarows=[];timeinfo=[];quality=[]
 for n,inv in invs.items():
  for s in inv['sheets']:
   sheetrows.append([h(n),h(s['sheet']),code(s['declared_dimension']),code(s['nonempty_extent']),h(s['nonempty_cell_count']),h(s['formula_count'])])
   if s.get('data_sheet_by_observed_time_headers'):
    nc=s['data_column_count'];nr=s['data_row_count']
    cols=s['columns'];missing=sum(c.get('blank_or_absent_count',0) for c in cols)
    affected=sum(bool(c.get('blank_or_absent_count',0)) for c in cols)
    errors=sum(c.get('error_count',0) for c in cols)
    nonnumeric=sum(c.get('non_numeric_count',0)+c.get('nonfinite_count',0) for c in cols)
    datarows.append([h(n),h(s['sheet']),h(f'{nr:,}'),h(nc),code(f'A2:{cols[-1]["column"]}{s["data_rows_end"]}'),h(f'{missing:,}'),h(affected)])
    quality.append({'workbook':n,'sheet':s['sheet'],'timed_records':nr,'columns_including_time_and_derived':nc,'missing_cells_within_timed_records':missing,'columns_with_missing_cells':affected,'excel_error_cells':errors,'nonnumeric_or_nonfinite_cells':nonnumeric})
    a=s['time_columns_derived']['A'];b=s['time_columns_derived']['B']
    first=a.get('derived_first_datetime_unspecified_timezone',a.get('derived_first_time_of_day',''))
    last=a.get('derived_last_datetime_unspecified_timezone',a.get('derived_last_time_of_day',''))
    timeinfo.append([h(n),h(s['sheet']),code(s['header_cells'][0]['resolved']),h(first)+' → '+h(last),h(b['first'][2])+' → '+h(b['last'][2]),h(b['minimum_delta'])+' / '+h(b['median_delta'])+' / '+h(b['maximum_delta'])])
 (BUNDLE/'audit/measurement_sheet_summary.json').write_text(json.dumps(quality,indent=2)+'\n')
 with (BUNDLE/'audit/sheet_inventory.csv').open('w',newline='') as f:
  fields=['workbook','sheet','declared_dimension','nonempty_extent','nonempty_cells','formulas','timed_records','data_columns']
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for n,inv in invs.items():
   for s in inv['sheets']:w.writerow(dict(zip(fields,[n,s['sheet'],s['declared_dimension'],s['nonempty_extent'],s['nonempty_cell_count'],s['formula_count'],s.get('data_row_count',''),s.get('data_column_count','')])))
 total=sum(x['bytes'] for x in manifests);records=sum(x['timed_records'] for x in quality)
 assert records==90340
 formula_total=sum(s['formula_count'] for inv in invs.values() for s in inv['sheets'])
 style='''body{font:16px/1.55 system-ui,-apple-system,Segoe UI,sans-serif;color:#202a32;background:#f7f8fa;margin:0}main{max-width:1320px;margin:0 auto;padding:48px 30px 80px}h1{font-size:34px;line-height:1.15}h2{font-size:24px;margin-top:42px;border-top:1px solid #ccd5de;padding-top:24px}h3{font-size:19px}p{max-width:1050px}a{color:#154e80}code{font:13px/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;overflow-wrap:anywhere}pre{white-space:pre-wrap;background:#edf1f5;padding:16px;border-radius:6px}.status{background:#e7f1ed;border-left:5px solid #31805d;padding:18px 22px}.pending{background:#fff5df;border-left:5px solid #b87b13;padding:16px 22px}.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13px;margin:16px 0 24px;background:white}th,td{padding:9px 10px;border:1px solid #d4dce3;text-align:left;vertical-align:top}th{background:#e9eef4}td code{font-size:12px}details{background:white;padding:12px 16px;border:1px solid #d4dce3;margin:12px 0}summary{font-weight:650;cursor:pointer}.muted{color:#566572;font-size:14px}.tags{font-size:14px;color:#566572}.figure{max-width:100%;height:auto}li{margin:7px 0}@media print{body{background:white}main{padding:10px}h2{break-after:avoid}.scroll{overflow:visible}table{font-size:10px}details{display:block}}'''
 parts=['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>R08 — NIST native workbook recovery</title><style>'+style+'</style></head><body><main>',
  '<p class="tags">Scooby · 14 November 2026 · Native-source recovery and inventory</p><h1>R08 — NIST workbooks recovered and audited</h1>',
  f'<div class="status"><strong>Recovery complete: 6 of 6 original NIST XLSX files.</strong> All returned final HTTP 200 after official 302 redirects, passed ZIP CRC verification and parsed as XLSX. The six files total {total:,} bytes. The audit covers 30 sheets, nine measurement sheets, {records:,} timed records, and 1,398 header occurrences. Originals were not opened and resaved.</div>',
  '<p>This supersedes the 13 November source-access failure. The separate ambient specimen CB-DA-AMB, CB-DA’s own ambient preload, and CB-DA’s fire phase remain distinct. The official spreadsheets contain published engineering measurements, author-deleted intervals and calculated summary columns; “native” here identifies the distributed NIST files, not untouched continuous DAQ output.</p>',
  '<div class="pending"><strong>Benchmark decision:</strong> the native-file and source-identification gate passes. A fully specified quantitative thermal-and-damage benchmark is not yet ready to run: clocks, physical sensor-validity windows, thermal-input choices and constitutive assumptions must first be fixed in a bounded input specification. Intact ambient and suitable structural-response segments are now available. No structural model, calibration or holdout test ran.</div>',
  '<h2>1. Source identity and retrieval</h2>',
  '<p>The project page is '+link('https://www.nist.gov/programs-projects/measurement-structural-performance-fire/steel-concrete-composite-floors','NIST Steel–Concrete Composite Floors')+'. The six official document routes resolved to files under '+code('https://www.nist.gov/system/files/documents/2020/02/14/')+'. Acquisition aliases in this bundle deliberately remain stable for the cell-level audit; the manifest also records the official filename.</p>']
 rows=[]
 for m in manifests:
  rows.append([code(m['acquisition_alias'])+'<br><span class="muted">'+h(m['official_filename'])+'</span>',link(m['requested_url'],'document route')+'<br>'+link(m['final_url'],'exact final file URL'),h(f'{m["bytes"]:,}'),code(m['sha256']),h(m['retrieval_finished_utc'])])
 parts.append(table(['Bundle native filename / official filename','Source URLs','Bytes','SHA-256','Retrieval completed UTC'],rows))
 parts += ['<p>Every native response and detected file type is '+code('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')+'. Exact start/end times, redirects, HTTP headers, MIME, byte counts, hashes and validity results are in '+code('provenance/direct_get_attempts.json')+' and '+code('provenance/native_file_manifest.json')+'. An independent direct-URL ambient GET produced the same SHA-256; its duplicate bytes are omitted from the bundle.</p>',
 '<p>The official persistent identity is '+link('https://doi.org/10.18434/M32181','DOI 10.18434/M32181')+', '+code('ark:/88434/mds2-2181')+'. '+link('https://data.nist.gov/od/id/mds2-2181?format=nerdm','NERDm metadata')+' version 1.0.1 was retrieved (4,821 bytes; SHA-256 '+code('5817a0e536eff9b5c34b3c166a17f0f4d2c95517370d41eaa4b480ce30130f5a')+'). It identifies this experiment but contains no DataFile download URLs or workbook hashes. Version 1.0.0 likewise contains no file distribution. The documented dataset-directory response lists zero files; the ARK-form directory gives HTTP 404. These are metadata-delivery limitations, not absence of the successfully recovered www.nist.gov files.</p>',
 '<p>The web text reader rejected the drawings and ambient downloads with its own unsupported-XLSX content-type error; that is not an origin HTTP 400. Direct binary GET succeeded. The official PDFs '+link('https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2054.pdf','TN 2054')+' and '+link('https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2055.pdf','TN 2055')+' were also recovered and included with separate retrieval metadata. Earlier PDF 403 responses were superseded by successful direct requests. No non-NIST workbook copy was used.</p>',
 '<h2>2. Every sheet and used range</h2><p>“Declared” is the OOXML worksheet dimension. “Nonempty extent” is the bounding rectangle of stored values or formulas; it can contain empty internal cells. Formatting-only cells can extend a declared range. Graphics may extend well beyond populated cell columns, so drawing anchors and all 19 embedded images are inventoried separately. All workbook sheet identities, properties, metadata, styles, comments and relationships are retained in the per-workbook inventories.</p>',
 table(['Workbook','Sheet','Declared range','Nonempty extent','Nonempty cells','Formula cells'],sheetrows),
 '<h2>3. Native measurement ranges and missingness</h2><p>Counts below are timed row records, not unique sensors or independent experimental replicates. Header row 1 is excluded. Missingness means an absent/blank cell inside the declared timed data rectangle; it does not count deleted time intervals as fabricated rows. Per-column first/last nonempty cells, gaps, explicit versus absent blanks, error/marker scans and values are in '+code('audit/native_inventory/*/channel_headers_and_quality.csv')+' and '+code('inventory.json')+'.</p>',
 table(['Workbook','Measurement sheet','Timed records','Columns including time/summary','Timed data range','Blank/absent cells','Affected columns'],datarows),
 '<p>CB-SP-SC’s fire sheet has a larger used range than its time series. Row 16951 contains only '+code('DK16951=MAX(DK2:DK16950)')+' and '+code('HR16951=MAX(HR2:HR16950)')+', with source caches 716.1276 and 736.4374. Its last timed row is 16950. The two summary cells are preserved and excluded from time-series missingness and record counts.</p>',
 '<p>Source error, nonnumeric and nonfinite-cell scans are reported separately from physical validity. A numerical value is not proof that a sensor still measured its intended quantity. Specimen X indicators in the generic channel list are not per-row quality flags. The recovered records include comments and events but do not supply a complete machine-readable physical-validity mask or calibration-certificate set. Published uncertainty is carried separately in '+code('audit/published_uncertainty_map.csv')+'.</p>',
 '<h2>4. Clocks, sampling and events</h2><p>All nine measurement sheets put the time coordinate in column A and elapsed seconds in column B, with exact labels in row 1. Excel serials are preserved. CB-DA-SC and CB-SP-SC use time-of-day fractions with a date written in A1; their numerical clock cells alone do not encode a calendar date. No timezone is supplied in the reviewed cells.</p>',
 table(['Workbook','Sheet','A1 text','Derived A-clock first → last (timezone unspecified)','Stored B first → last, seconds','Derived B delta min / median / max, seconds'],timeinfo),
 '<p>TN 2054 §4.3 (printed p.64; PDF p.82) reports nominal 1 Hz acquisition and an averaging process. The distributed tables must be assessed from their actual intervals. CB-DA’s elapsed steps alternate around 1.0000/1.0001 s; its wall-clock two-second step at '+code('A10437:A10438')+' has no corresponding elapsed-clock gap. CB-SP preload has a 720 s wall-clock jump at '+code('A6724:A6725')+' while B advances 12 s. CB-SP-SC preload and fire have 109 s and 107 s wall-clock steps while their B columns remain at one-second steps. These clock disagreements are preserved rather than repaired.</p>',
 table(['Specimen','Fire elapsed zero','Recorded ignition offset, seconds','Source event cells'],[
  ['CB-DA','Natural-gas flow','23.001399999999194',code('User Events!B3:D4')],['CB-DA-SC','Natural-gas flow','12',code('User Events!B4:D5')],['CB-SP','Natural-gas flow','53.003200000000106',code('User Events!B3:D4')],['CB-SP-SC','Natural-gas flow','21',code('User Events!B4:D5')]]),
 '<p>For a later ignition-relative comparison, subtract the specimen’s recorded ignition offset into a separately named derived field. Do not overwrite native elapsed seconds. A preload sheet starts its own clock; equal-looking elapsed values do not join preload to fire.</p>',
 '<h3>Ambient deletions and one event correction</h3><p>The ambient table contains six jumps after source rows 609, 1209, 2435, 3466, 4703 and 5303: 814, 872, 783, 224, 2439 and 480 seconds. Native comments at those rows describe deleted data during fiber-optic pauses, between cycles, or without a more specific reason. The intervals remain missing; no interpolation or invented row was inserted.</p>',
 '<p>'+code('CB-DA-AMB / User Events!B6')+' stores 4344 s for the first-cycle endpoint, while C6’s timestamp matches '+code('CB-DA-AMB Data!A3466')+' exactly; '+code('B3466')+' is 5930 s and its comment identifies the first-cycle end. A reconciled event time of <strong>5930 s</strong> is therefore supported by native cross-evidence. It remains a derived correction beside the unmodified 4344 s source value, with a 1586 s discrepancy flag.</p>',
 '<h2>5. Corrected instrument map and unresolved conflicts</h2><p>'+code('audit/corrected_instrument_map.csv')+' contains 1,398 header occurrences across nine sheets: 1,365 sensor-named columns, 18 time fields and 15 native summary columns. Each row retains exact header cells, units, local channel-list cells, drawings-list cells, source URLs/hashes, and original descriptions. Joins trim surrounding legend whitespace and separate trailing units; they do not silently remove hyphens or merge specimens. Eight auxiliary-temperature headers lack a local/drawings definition. Twenty-eight observed headers have blank specimen X flags; four X-marked dictionary channels have no corresponding header.</p>',
 table(['Issue','Observed source evidence','Treatment in corrected map'],[
  ['Fire vertical labels',code('CB-DA-FireLoadingData!IK1:IN1')+' = VD2–VD5; drawing C1 caption '+code('InstrumentationLayout-FireTests!B32')+' agrees. TN 2055 §2.4 p.23 instead says VD1–VD4.','Use the observed header identities; retain the published discrepancy.'],
  ['Fire vertical locations','Both local and general dictionaries shift the prose locations (Mid Span/West/Mid West/Mid East); original drawing C1 orders VD2/3/4/5 west-to-east outer/inner/inner/outer.','Retain original descriptions and expose a separate diagram-supported provisional spatial map.'],
  ['Ambient vertical channels',code('CB-DA-AMB Data!BE1:BJ1')+' = VD1–VD6; VD1 is beam-midspan and VD2 slab-midspan in the ambient dictionary.','Keep its sensor dictionary separate from the fire tests.'],
  ['Loading-truss rotations','Both original drawings place RotLT1 west, RotLT2 middle, RotLT3 east; fire dictionaries reverse the outer descriptions.','Preserve source text and add a diagram-supported provisional correction.'],
  ['Actuator and angle units','Ambient baseline uses in/kip; fire specimens, including their preloads, use mm/kN. All 75 rotation header occurrences state rad.','No measurement conversion performed; source units retained.'],
  ['Connection thermocouples','Generic list uses shear-tab descriptions for some TCW/TCE sensors where CB-DA’s local list specifies angle legs.','Keep specimen connection geometry explicit; use local definitions with figure cross-checks.'],
  ['Precise thermal location conflicts','Examples: CB-DA TC6_26 north/south deck descriptions; TC4_13 mid/top web; SC STC1 offsets differ between lists.','Flag unresolved precise location; do not silently choose coordinates.'],
  ['Gas drawing label','C4(a) duplicates TCC1 at a southeast point, while C4(b) identifies the corresponding point as TCC13 south.','Keep diagram discrepancy; no native measurement header renamed.']]),
 '<p>Drawing C1’s written dimensions yield 335.28, 548.64, 731.52 and 944.88 cm for VD2–VD5 by explicit arithmetic. TN 2055 Table 13 lists 336, 548, 732 and 944 cm from the west-column centerline. The diagram datum and table datum are kept separate, and those numbers are not silently equated or rounded into one another. These are geometry annotations, not measured time-series values or pixel-derived positions.</p>',
 '<p>The drawings workbook has six sheets and 19 native embedded graphics. Their source-member hashes, sheet/caption cells, anchors and preview status are recorded. The optional PNGs are derived rasterizations of native EMF graphics, not regenerated diagrams. Ambient Figure B1(d) renders incompletely in Inkscape; the original EMF remains intact in the workbook and that panel was not used to infer missing details.</p>',
 '<h2>6. Formulas, caches and calibration distinctions</h2>',
 f'<p>The full inventory preserves all {formula_total:,} source formula cells and cached values, including the two untimed MAX cells. Shared-formula followers can have an empty formula-text node while referring to a stored shared master; that is not a missing formula. Shared masters, group IDs/ranges and follower records are retained separately. Nothing was recalculated or resaved.</p>',
 '<p>For example, CB-DA fire '+code('JN2')+' contains '+code('AVERAGE(F2,G2,H2,I2,J2,K2,L2,P2,Q2,R2,S2,T2,U2,V2)*3.9')+' with stored cache 27.739223571428571. It selects fourteen brace-strain channels and excludes ColW1 and ColE1. Native comments at the force header/list state that negative means compression. This is an author-calculated force estimate, not an independent load-cell measurement. '+code('JM2=AVERAGE(IL2,IM2)')+' separately averages VD3 and VD4.</p>',
 '<p>Published expanded uncertainties (k=2), standard uncertainties, sample standard deviations and nominal sensor ranges remain different quantities. The detailed uncertainty sidecar cites the relevant report and operating conditions; a dictionary’s Range Low/High field is not a calibration certificate. The report’s 3.90 kN/µε relation and the workbook’s ×3.9 formula do not themselves establish the adequacy of an independent fixture calibration.</p>',
 '<h2>7. Benchmark gate after inspecting the originals</h2>',
 '<p><strong>Pass: native evidence intake.</strong> The prior missing-byte blocker is resolved, and the complete sheet/header/time/formula evidence is now inspectable. A bounded ambient or structural-response study can use intact segments with explicit exclusions.</p>',
 '<p><strong>Not yet passed: a fully specified quantitative thermal-and-damage run.</strong> The central remaining limitation is physical validity, not file access. TN 2055 §3.3.3 (printed p.56; PDF p.59) documents CB-DA beam-thermocouple lead insulation failure around ten minutes after ignition and secondary junctions. Stored numeric values can then represent a different physical temperature. CB-DA-SC and CB-SP have different failure histories; CB-SP-SC has improved routing. A blank-cell mask cannot resolve this. Approximate report times also cannot identify an exact first invalid worksheet cell without an explicit derived rule.</p>',
 '<p>TN 2054 §4.5 and TN 2055 §3.4.3 additionally limit rotation measurements by temperature and cable survival. Load removal is part of the actual experiment: CB-DA’s native event log records unloading at 1802.1081 s from gas flow, before its later cooling and fire-out events. A survival target cannot assume full sustained actuator loading after that event. CB-SP-SC has separate bolt-fracture, unloading, fire-out and late-collapse events, which must remain distinct damage/outcome targets.</p>',
 '<p><strong>Smallest next action:</strong> assemble one fixed model-input specification from these recovered files and reports: reconcile event clocks; choose reliable channels and time windows; list reported geometry, load/control and restraint/material inputs; mark selected heat-transfer and high-temperature constitutive laws as assumptions; then freeze target quantities, acceptance tolerances and a whole-specimen holdout. Keep thermal inputs separate from channels used for thermal validation. Do not require deleted pause records before using intact ambient loading segments. No further download, external contact or fee is needed to begin that preparation.</p>',
 '<h2>8. Reproducibility and delivery contents</h2><p>The ZIP retains the six unchanged XLSX files, both official Technical Notes, the prior gate report/map, exact retrieval records, persistent-data metadata, full OOXML inventories, corrected channel crosswalk, uncertainty/quality notes, formulas and caches, drawing previews, and executable audit scripts. Matched-pair CSV.gz files expose the original lexical stored values with a source row number; formula-cell exports use their cached values and remain accompanied by the formula ledger. No data cleaning, interpolation or unit conversion is presented as observation.</p>',
 '<pre>native/                         Six byte-identical NIST workbooks\nprovenance/                     HTTP records, original URLs, hashes, PDR records\naudit/native_inventory/         Every sheet; headers, missingness, formulas, comments\naudit/corrected_instrument_map.csv\naudit/published_uncertainty_map.csv\naudit/gate_evidence_notes.md     Exact cells and report-page limits\npreviews/                       Native-PNG copies and derived EMF previews\nsources/reports/                Official TN 2054 and TN 2055 plus retrieval metadata\nsources/prior_audit/            Original 13 November gate report and map\nscripts/                        Read-only download and audit code\nSHA256SUMS.txt                   Checksums of every bundle member except itself</pre>',
 '<p class="muted">Evidence labels: original bytes/cells/formula text/comments are observed. Hashes, ranges, joins, counts, clock differences, date interpretations, diagram-dimension arithmetic and event reconciliation are derived. No native workbook was modified. No model, calibration, holdout, contact, records request, payment or Deep Research was performed.</p></main></body></html>']
 report=''.join(parts)
 (BUNDLE/'Scooby_R08_Native_Recovery_Audit_2026-11-14.html').write_text(report)
 copy(BUNDLE/'Scooby_R08_Native_Recovery_Audit_2026-11-14.html',OUT/'Scooby_R08_Native_Recovery_Audit_2026-11-14.html')
 copy(ROOT/'corrected_instrument_map.csv',OUT/'Scooby_R08_Corrected_Instrument_Map_2026-11-14.csv')
 readme='''# R08 NIST native workbook recovery — 14 November 2026

Start with Scooby_R08_Native_Recovery_Audit_2026-11-14.html. All six original NIST XLSX files are in native/. They total 170,176,394 bytes. Stable acquisition aliases are mapped to exact official filenames and URLs in provenance/native_file_manifest.json. No native workbook was changed.

The source-access gate passes. No structural model ran. A full quantitative thermal/damage benchmark still requires explicit physical channel-validity windows, clock alignment and thermal/material assumptions; see audit/gate_evidence_notes.md.

## Verify without a network

From this extracted directory:

    python3 scripts/verify_bundle.py

SHA256SUMS.txt hashes every delivered member except itself. The independent direct ambient URL retrieval matched the canonical route hash; its duplicate bytes are omitted.

## Repeat the audit without modifying sources

    python3 scripts/inventory_native.py --input native --out rebuilt_inventory
    python3 scripts/audit_primary_time_and_export.py --input native --out rebuilt_inventory
    python3 scripts/finish_inventory.py --input native --out rebuilt_inventory
    python3 scripts/build_channel_crosswalk.py --native-dir native --retrieval-manifest provenance/direct_get_attempts.json --output-dir rebuilt_map

The inventory uses Python standard-library ZIP/XML parsing. Source values, formulas, caches and comments remain separate. A formula follower with empty f text may refer to a shared-formula master; inspect the shared masters ledger. Derived statistics and range/clock/alias interpretations are not native cells.

## Re-fetch original official routes into a NEW directory

    python3 scripts/recover_nist.py --out fresh_http

Compare downloaded bytes with the manifest before treating them as this archived version. This script uses only ordinary official NIST routes and records redirects and HTTP outcomes. It does not use third-party mirrors or bypass access controls.

The matched-pair CSV.gz exports retain source Excel row numbers and original lexical values; cached values in formula cells are accompanied by the source formula ledger. Other three fire workbooks are fully inventoried and included unchanged; no duplicate whole-data CSV is required to recover their values.

The illustration PNGs are optional derived previews of original EMF members (or unchanged embedded PNGs), not digitized measurement plots. Ambient figure B1(d) renders incompletely in Inkscape; consult the untouched embedded original. Rendering, visual-review annotations and assembly scripts preserve the original r08_work staging-path convention and can be adapted without changing sources. The documented CLI commands above are directly portable.

The 13 November prior artifacts are retained for history and are superseded as to file access. The full source/reference/HTTP manifests distinguish successful bytes from tool parser errors and earlier failed routes. No external contact, request, payment, Deep Research, structural model, calibration or holdout run occurred.
'''
 (BUNDLE/'README.md').write_text(readme)
 verifier='''#!/usr/bin/env python3
import hashlib,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1]
bad=[];count=0
for line in (root/'SHA256SUMS.txt').read_text().splitlines():
 expected,name=line.split('  ',1);p=root/name;h=hashlib.sha256()
 if not p.is_file():bad.append((name,'MISSING'));continue
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 if h.hexdigest()!=expected:bad.append((name,'HASH MISMATCH'))
 count+=1
print(f'Verified {count} files; failures: {len(bad)}')
for x in bad:print(*x)
sys.exit(bool(bad))
'''
 (BUNDLE/'scripts/verify_bundle.py').write_text(verifier)
 files=sorted(p for p in BUNDLE.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
 (BUNDLE/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+p.relative_to(BUNDLE).as_posix()+'\n' for p in files))
 # Only inputs already validated are packaged; store XLSX/PDF/GZ members without needless recompression.
 zpath=OUT/'Scooby_R08_Native_Recovery_2026-11-14.zip'
 with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(BUNDLE.rglob('*')):
   if p.is_file():z.write(p,BUNDLE.name+'/'+p.relative_to(BUNDLE).as_posix(),compress_type=zipfile.ZIP_STORED if p.suffix.lower() in ['.xlsx','.pdf','.gz','.png'] else zipfile.ZIP_DEFLATED)
 result={'bundle':str(zpath),'bytes':zpath.stat().st_size,'sha256':sha(zpath),'members':len(files)+1,'native_files':6,'sheets':30,'timed_records':records,'formula_cells':formula_total,'report':str(OUT/'Scooby_R08_Native_Recovery_Audit_2026-11-14.html'),'map':str(OUT/'Scooby_R08_Corrected_Instrument_Map_2026-11-14.csv')}
 (OUT/'Scooby_R08_Delivery_Manifest_2026-11-14.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
