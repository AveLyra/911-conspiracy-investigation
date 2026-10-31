#!/usr/bin/env python3
"""Read-only public catalogue verification; no private sources or network required."""
from pathlib import Path
import hashlib,json,re,sys

P=Path(__file__).resolve().parents[1]
meta=json.loads((P/'PUBLICATION.json').read_text())
checks=[]
def check(name,value):checks.append({'name':name,'passed':bool(value)})
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
master=json.loads((P/'data/master-leads.json').read_text())['entries']
findings=json.loads((P/'data/source-findings.json').read_text())['findings']
documentary=json.loads((P/'data/documentary-units.json').read_text())['records']
sets={'MASTER-LEADS.md':{f'm{x:03}' for x in range(1,176)},'SOURCE-FINDINGS.md':{x['id'].lower() for x in findings},'EARLIER-CHAT-AUDIT.md':{f'early-{x:02}' for x in range(1,12)},'DOCUMENTARY-CLAIMS.md':{f'documentary-b{x:03}' for x in range(1,234)}|{f'documentary-h{x:03}' for x in range(1,15)},'CONSOLIDATED-AND-RECENT.md':{f'consolidated-{x:02}' for x in range(1,50)}|{f'recent-{x:02}' for x in range(1,14)},'HISTORICAL-CONTEXT.md':{f'historical-{x:02}' for x in range(15,66) if x not in [16,25]}}
sets['MASTER-LEADS.md']|={f'master-family-{x}' for x in range(1,15)}
sets['SOURCE-FINDINGS.md']|={'family-'+re.sub(r'\d','',x['id']).lower() for x in findings}
check('exact175 master research IDs',len(master)==175 and {x['id'] for x in master}=={f'M{x:03}' for x in range(1,176)})
check('370 unique source IDs',len(findings)==370 and len({x['id'] for x in findings})==370)
check('247 original documentary IDs',len(documentary)==247 and {x['id'] for x in documentary}=={f'B{x:03}' for x in range(1,234)}|{f'H{x:03}' for x in range(1,15)})
for name,ids in sets.items():
    actual=set(re.findall(r'<a id="([^"]+)"', (P/name).read_text()))
    check('exact annotation IDs '+name,actual==ids)
check('56 source report bodies',len(set(re.findall(r'<a id="unit-[^"]+"',(P/'LATEST-SOURCE-UNITS.md').read_text())))==56)
for ident in ['fa044','pl022','pl023','pl024','pl025','nr068','nr069','nr070','nr071','nr072','pl026','pl027','nr073','pl028','pl029']:
    text=(P/'SOURCE-FINDINGS.md').read_text().split(f'<a id="{ident}"></a>',1)[1].split('<a id=',1)[0]
    check('addition observation contrary and TODO '+ident,all(word in text for word in ['**Context / contrary evidence:**','**Open TODO:**','**Citations:**']))
for i in range(1,12):
    block=(P/'EARLIER-CHAT-AUDIT.md').read_text().split(f'<a id="early-{i:02}"></a>',1)[1].split('<a id=',1)[0]
    check('recovered context contrary and TODO '+str(i),'**Context / contrary evidence:**' in block and '**Open TODO:**' in block)
for row in documentary:check('documentary prior verdict not adopted '+row['id'],'prior verdict not accepted' in row['assessment_status'])
text=(P/'LATEST-SOURCE-UNITS.md').read_text()
check('current method publication distinguished from dated local-only state','## Publication status reconciliation' in text and 'b30daf0f664b8688b18dea4fa08587a12dbefa97' in text and 'independent decoder validation' in text)
check('unperformed same-content tests remain open','Re-encoding can change bytes' in text and 'waveform alignment' in text and 'Open TODO' in text)
check('FAA preservation source clocks and qualifications retained',all(v in text for v in ['110000 UTC to 120400 UTC','2000 - 2400 local','0000 - 2400 local','09/14/2001 01:00 PM','header zone unverified','not independent witnesses','documented deviation','withdrawal/amendment']))
check('FAA handoff and verified publication states distinguished','## Update 051 publication verified after handoff' in text and 'handoff-time status' in text and '45ee3925dc1edd3137cf85182570bfc8440afcac' in text)
check('FAA052 conditional labels matching control and no sum',all(v in text for v in ['1230–1331 and 1331–1340','1230–1344','1245–1314','1245–1316','1255–1315','1255–1316','1232–1259','4, 2, 1 and 0 minutes','matching Boston pair','Do not sum','Unique tape/channel IDs']))
check('FAA052 actual reading routing and instruments remain qualified',all(v in text for v in ['1,2,3,4,8,15,16,26','eighteen pages remain unread','AAT-20','AAT-200','partly occluded footer','underlying instruments','corrected May2003','62a102da31cc82a7216dc41e60bed185a11c8d45']))
check('FAA053 candidate and all distinct fields preserved',all(v in text for v in ['TMU commercial line1078','1255–1316 UTC','not the initially sought Operations Manager1230–1344','Fill Transcript','Full Transcript','AAL11','ZBW-ARTCC-148','UAL175_R42_memo.doc','1300:41','09/27/2001','D:20051222232254','D:20131106161605']))
check('FAA053 sparse dialogue and search limits remain open',all(v in text for v in ['does not prove missing speech','pertaining to the subject accident','no correct flight label is selected','title-only/unopened','NOM audio remains metadata-only/unmapped','0584407dac2190a9f9514ee157124446e60672d5']))
check('FAA054 memo acquired dialogue and media remain open',all(v in text for v in ['Previously title-only AWA940','31,742 bytes','OMIC1230–1344','UAL175_MEMO.doc','ZNY-ARTCC-148','February 4, 2002','09/25/2001','need not contain the transcript body','No missing speech, trimming or measured gap']))
check('FAA054 roles matching control and unopened corrections preserved',all(v in text for v in ['ZNY OMIC and CC-NOM separately','not timestamped communications','subject and work-file aircraft labels both say UAL175','neither corrects AWA937','Title-only/unopened NARA7598362','companion7598360','not a proven replacement relationship or the May2003 QFR correction','191c27f34284bdbbf006db5bb2b41071125f19d7']))
check('FAA055 all33 rows acquisition and different correction stages retained',all(v in text for v in ['Previously title-only AEA1124','AEA1122/NARA7598360 are now acquired','All33 visible requests/queries','F01–F29','M01–M04','separate evidentiary stages','conditional release are distinct','608171664400ed8d1e95f70277ea994702a3cbd7']))
check('FAA055 disputed values contrary evidence and native tests stay open',all(v in text for v in ['1301:06/1301:05','1305:34/1305:33','ZBW IGN at1306:17','contrary original/remaining-copy response','contrary evidence to assuming every change was concealed','UAL175 9-11-01.doc','UAL175 Change 2.doc','do not infer twenty deleted pages','AEA1121/NARA7598359','AEA1123/NARA7598361','Actual May2003 draft/corrected QFR/receipt']))
check('FAA056 acquired entities and exact publication',all(v in text for v in ['AEA1121/NARA7598359 and AEA1123/NARA7598361 are now acquired','464,135 bytes','190,274 bytes','a42d0956202dacc3b971d21f479966d56fefcd60']))
check('FAA056 missing page dispatch and receipt distinct',all(v in text for v in ['page 2 of the 23-page','two copies enclosed','not in the acquired three-page scan','Friday as certified','5/14/02','actual receipt and approval','Native filenames']))
check('FAA056 timestamp pairs not measured clocks',all(v in text for v in ['1245:58/1245:59','1244:58/1244:59','1302:00/1302:02','1302:04/1302:06','−60, −60, +4, +4 seconds','not measured hardware-clock offsets','1301:37/1301:35','1311:06 following 1311:09']))
check('FAA056 contrary source explanations attributed',all(v in text for v in ['both correct or no change','not independently verified equipment behavior','radio/landline coordination','channel-specific reception','1258:18','1305:22/1310:46']))
check('FAA056 version and line1078 distinctions preserved',all(v in text for v in ['28 pages for the fourth/associate55','page 19 placed after page 9','four Correction made annotations','five-page Ninth','Eighth nine-page','does not authenticate the two-page AWA937','not independent corroboration']))
check('FAA056 selected ledger and count limits preserved',all(v in text for v in ['30 selected FIELD-LEDGER observations V01–V30','135 numbered transcript-review items','19+26+24+41+6+7+7+5','not 135 independent errors or events','Prior update055’s 33 rows']))
check('FAA056 policy originals copies and acceptance gaps preserved',all(v in text for v in ['from copies of Form8020-3','not destruction of the original','2000 FAA Order8020.11B','2003 Change 1','not newly read here','72c(11)/77d(4)','May 2003 QFR drafting/correction/delivery','five tracks/eighteen substantive criteria remain incomplete/partial','not a new independent twelve-page image review']))
check('057policy edition applicability and incomplete original tests',all(v in text for v in ['77d(3)(a)','72c(11)','four or more quiet minutes','Do not backdate that rule','76a NOTE','Two delimiter failures']))
check('058actual package counterpart and conflicts retained',all(v in text for v in ['15,505,493 bytes /237 pages','Physical49/printed2of23','1244:58/ZBW IGN','1244:59/R42','AAL11/ZBW-ARTCC-148/AAL11','DESTROY:March11,2004','32 passed /4 failed literal OCR anchors']))
check('059marked body uncertainty and duplicate rows not erased',all(v in text for v in ['1301:43/Unknown','1301:28/N90','1301:46/Unknown','All48 timed rows,45 distinct second labels','1301:07,1303:39 and1303:40','341+573+346=1,260seconds','unchanged and unrepaired']))
check('060general acknowledgment not precise final delivery',all(v in text for v in ['11/15/2001 7:46AM','2/1/2002 8:39AM','January4,2002','2/12/02','not a second independent delivery','35','different positions, not automatically a page-count discrepancy','final acceptance']))
check('061form ranges conditional time pairs and pagination limits',all(v in text for v in ['0632–1432','0632–0810','0810/0930/1315','1210/1330/1715','240minutes conditional','neither range controls','Page8of8 not located','physical34 remained unread','34/237 images leaves203']))
check('062November body versus April association and event attributions',all(v in text for v in ['e45e7435e80b81df3f0c0376fb7be049595c1653dc6a00f1b6718c1b7dd411b3','c19d9e7ae4176fb411def7259f7657d2c80bf1bdf1a803c8f4fb1b7af83bab5f','7:38 is manifest lockout','7:44 concerns declaration','29 checks passed/1 exact OCR anchor failed','nor were they','TI-TODO01']))
source_results=meta['source_check_results'];expected_results={'057':(20,0),'058':(32,4),'059':(24,0),'060':(29,0),'061':(33,0),'062':(29,1)}
check('all six original source-check totals and exact failure counts retained',set(source_results)==set(expected_results) and all((source_results[n]['passed'],source_results[n]['failed'])==counts and len(source_results[n]['failed_checks'])==counts[1] for n,counts in expected_results.items()))
check('058four original failed predicates retained',[z['check'] for z in source_results['058']['failed_checks']]==['Physical49 safe field anchors at4-16','Physical186 safe field anchors at54-54','Physical187 safe field anchors at5-5','Physical190 safe field anchors at3-37'])
check('062original failed predicate retained',source_results['062']['failed_checks']==[{'label':'selected visible OCR anchor p8: not in continuous contact','actual':False,'expected':True,'passed':False}])
check('source-check results linked with immutable result hashes',all(z['verification_url'].startswith('https://github.com/AveLyra/911-conspiracy-investigation/blob/'+z['commit']+'/') and len(z['verification_sha256'])==64 for z in source_results.values()))
check('allfive tracks eighteen criteria stay unfinished','All five tracks and eighteen substantive criteria remain open/partial' in text and 'not a fresh independent primary-image' in text)
methods=meta['source_method_records']
check('five new research reports distinct from one execution note',set(methods)-{'336-337'}=={'063','064','065','066','326-639-939'} and len(meta['execution_status_notes'])==1 and meta['counts']['source_units']==56)
check('063partial mirror raw order blanks and source-role limits',all(v in text for v in ['No source PDF was downloaded','0740,0738','own time cell blank','12rows,10time cells and2blanks','No unique event/call/version join or actual 13-minute delay','not receipt/execution/display state']))
r63=methods['063']['record'];check('063original screenshot ledger result retained',r63['all_capture_bytes_and_hashes_match'] and r63['manual_rows']==12 and r63['printed_time_cells']==10 and r63['blank_time_cells_preserved']==2 and len(r63['decreasing_adjacent_labels'])==1 and r63['decreasing_adjacent_labels'][0]['nominal_label_seconds_difference']==-120)
check('064plans and distinct document schedule objects retained',all(v in text for v in ['row1343','Row1739','Accident_1738/11sep.doc','not proof audio was saved','row1743 continues at p7top with schedule','row0015/12Sep','independent reader']))
r64=methods['064']['record'];check('064two screenshot checks not native or successful retrieval',len(r64['actual_checks'])==2 and all(z['bytes_match'] and z['sha256_match'] for z in r64['actual_checks']) and not r64['source_PDF_or_DOC_authenticated'] and not r64['recording_retrieval_success_or_delivery_proved'])
check('065official locator and metadata-level limits retained',all(v in text for v in ['NARA2608461','series2555805','Container20','510,869bytes','Not Yet Available Online','Possibly Restricted','Partially Restricted','T1:','T2:','T3:']))
r65=methods['065']['record'];check('065exact FAILED prospective cap preserved',r65['prospective_navigation_cap']==8 and r65['actual_navigation_requests']==10 and r65['navigation_cap_result'].startswith('FAIL: two requests over') and r65['pdf_page_images_read']==2 and 'not retrospectively called passing' in text)
r66=methods['066']['record'];check('066date unknown partial views and raw identifiers retained',r66['within_caps'] and r66['actual']['new_viewer_pages']==4 and r66['actual']['viewport_images']==7 and not r66['actual_full_pages_read'] and all(v in text for v in ['Page9 date header was not inspected','0834/1133 cannot be assigned to the attack morning','raw advisory ID01 025','not a validated count of25','not current','fax/retraction','not a whole-log absence finding']))
s67=meta['execution_status_notes'][0];ids67={f'{p}{i:02}' for p,count in [('FAA',4),('TEL',4),('REC',3),('MAT',3),('STL',4)] for i in range(1,count+1)}
check('067dated blocked state all18 IDs without private goal payload',s67['id']=='067' and s67['original_record_goal_status']=='blocked' and set(s67['criteria_ids'])==ids67 and len(s67['criteria_ids'])==18 and s67['full_scope_preserved'] and not s67['global_archive_exhaustion_claimed'] and not s67['private_source_records_exported'] and not s67['later_collateral_step_completes_original_goal'])
check('067bounded searches and dated owner limits not absence proof',all(v in text for v in ['three consecutive goal turns','notLoaded/interrupted','2187/2234/2236/2241','not in RECAP','Four approximate SOCC native searches','Three PASSUR queries','The audit did not establish every external archive exhausted','dated owner states']))
reply=methods['326-639-939']['record'];check('replysix reference checks not independent manual truth',len(reply['checks'])==6 and all(z['matches'] for z in reply['checks']) and not reply['manual_reading_independently_verified_by_this_code'] and not reply['historical_or_native_authentication_performed'])
check('replydates nonautomatic thread and unidentified referent retained',all(v in text for v in ['August16,2001','August15 inquiry','not automatically a reply','August24,5:29PM','unidentified earlier communication','London/Paris','Frahm']))
check('replyvisible equality source dependence and contrary explanation retained',all(v in text for v in ['March11,2006','physicalp5 repeats','detected no substantive visible wording difference','no pixel/native identity','not independent corroboration','Different information, questions, thresholds','blanket stopped-investigation','DRAFT-T01–T06','336/337 are untried']))
check('new method records have immutable source-result links',all(z['result_url'].startswith('https://github.com/AveLyra/911-conspiracy-investigation/blob/'+z['commit']+'/') and len(z['result_sha256'])==64 for z in methods.values()))
check('336337source copy roles and missing report boundary retained',all(v in text for v in ['301,981bytes/six pages','359,793bytes/five pages','August21,2001 request/cover','No readable counterpart of the referenced report/page7','not visibly a French intelligence agency assessment','Masood Al-Benin','dark image that remained uninterpretable']))
check('336337index labels do not authenticate attachment or motive',all(v in text for v in ['Broad index labels are retained beside actual contents','exact missing-attachment join','not independent evidence','no controlling account','blanket stopped-investigation']))
check('336337editorial held-versus-new corrections preserved',all(v in text for v in ['M-MP1-88000363–88000368','M-MP1-88000370–88000374','Report-line pins locate derivative prose only','326/639are previously acquired/read','939was previously acquired/read but not newly acquired or read','previous_now_held/searches_completed','strict whitespace gate remained enabled']))
r336=methods['336-337']['record'];p336={z['exhibit']:z for z in r336['checks'] if 'exhibit' in z}
check('336337six PDF plus index reference integrity within limits',len(r336['checks'])==7 and all(z['matches'] for z in r336['checks']) and p336['336']['sha256']=='fd8137a4554318a5a6b1b71ebfe032da8fb996d7cd69c863edd4cbd407fa5f37' and p336['336']['pages']==6 and p336['337']['sha256']=='fc4f9d1ac19ce4c638d5dd4989f53dec4d55ea5a6f2626daae199b5a0942af68' and p336['337']['pages']==5 and not r336['manual_reading_independently_verified_by_this_code'] and not r336['historical_or_native_authentication_performed'])
f336=meta['source_workflow_failures']['336-337'];e336=meta['editorial_history']['336-337']
check('336337failed precommit and pinned editorial history preserved',f336['failed_operation']=='gitave diff --cached --check before commit' and f336['result'].startswith('exit2;') and f336['no_commit_or_push_created_by_failed_script'] and 'strict whitespace gate unchanged' in f336['repair'] and e336['diff_url'].endswith('/EDITORIAL-REVISION.diff') and len(e336['sha256'])==64)
check('336337open TODOs and next candidates remain unaccepted',all(v in text for v in ['DRAFT-T01–T06 remain','complete referenced report/page7','59B/346/642 are indexed candidate','All five tracks and eighteen original substantive criteria remain open/partial']))
pattern=re.compile(r'\]\((?:<([^>]+)>|([^\)\n]+))\)');broken=[];links=0
for f in P.glob('*.md'):
    for angled,plain in pattern.findall(f.read_text()):
        value=angled or plain
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',value):continue
        links+=1;name,_,anchor=value.partition('#');target=f.parent/name if name else f
        if value.startswith('/') or not target.is_file():broken.append([f.name,value,'missing or absolute target']);continue
        if anchor and f'id="{anchor}"' not in target.read_text():broken.append([f.name,value,'missing stable anchor'])
check('all local public reader links',not broken)
private=re.compile(r'(?i:\bRule\s*26\b|\bVaughn\b|\bCORR-\d|\bSRC-\d|@gmail\.com|@proton\.(?:me|mail\.com)|case-management|\.eml\b|drive\.google\.com|docs\.google\.com)|(?<![A-Za-z])/Users/|/Volumes/|/private/var/|/var/folders/|-----BEGIN [A-Z ]*PRIVATE KEY-----')
privacy=[]
for f in list(P.glob('*.md'))+list((P/'data').glob('*.json')):
    if private.search(f.read_text()):privacy.append(str(f.relative_to(P)))
check('private case correspondence credential and locator exclusions',not privacy)
check('no symlinks',not any(f.is_symlink() for f in P.rglob('*')))
listed={r['path'] for r in meta['files']}
actual={str(f.relative_to(P)) for f in P.rglob('*') if f.is_file() and f.name!='PUBLICATION.json' and '__pycache__' not in f.parts}
check('complete unique public payload inventory',listed==actual and len(listed)==len(meta['files']))
for row in meta['files']:
    f=P/row['path'];check('public payload bytes '+row['path'],f.is_file() and f.stat().st_size==row['bytes'] and sha(f)==row['sha256'])
result={'status':'passed' if all(c['passed'] for c in checks) else 'failed','passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'local_reader_links':links,'broken_links':broken,'privacy_matches':privacy,'failures':[c['name'] for c in checks if not c['passed']],'source_or_causal_validation':False}
print(json.dumps(result,indent=2));sys.exit(0 if result['status']=='passed' else 1)
