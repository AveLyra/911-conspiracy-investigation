"""Reproduce entity/text checks and narrow printed-record comparisons, not historical adjudication."""
import argparse,json,hashlib,subprocess
from pathlib import Path
from datetime import datetime,timezone
import fitz
p=argparse.ArgumentParser()
p.add_argument('pdf_directory',type=Path)
p.add_argument('audio_directory',type=Path)
p.add_argument('release',type=Path)
p.add_argument('output',type=Path)
a=p.parse_args();assert not a.output.exists(),'Preserve earlier receipts; choose a new output'
pins=json.loads((a.release/'SOURCES.json').read_text());comps=json.loads((a.release/'COMPARISONS.json').read_text())
checks=[];pages={};rendered={}
for pin in pins['PDFs']:
 path=a.pdf_directory/pin['filename'];body=path.read_bytes()
 with fitz.open(path) as d:
  texts=[x.get_text() for x in d]
  actual={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'pdf_pages':len(d),'page_text_sha256':[hashlib.sha256(x.encode()).hexdigest() for x in texts]}
  expected={k:pin[k] for k in actual};checks.append({'id':pin['id'],'kind':'PDF entity/text integrity','passed':actual==expected,'actual':actual})
  pages[pin['id']]=texts
  if pin['id']=='F04':
   for n in [63,64]:
    pix=d[n-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
    rendered[n]={'dimensions':[pix.width,pix.height],'pixel_sha256':hashlib.sha256(pix.samples).hexdigest(),'text_layer_bytes':len(texts[n-1].encode()),'text_sha256':hashlib.sha256(texts[n-1].encode()).hexdigest()}
  checks.append({'id':pin['id'],'kind':'Embedded-file API inventory','embedded_file_names':d.embfile_names(),'scope':'No assertion about every possible PDF object or original external payload.'})
ex=[]
for e in json.loads((a.release/'SOURCE-EXCERPTS.json').read_text())['groups']:
 lines=pages[e['source']][e['pdf_page']-1].splitlines()
 ok=all(lines[row['line']-1]==row['text'] for row in e['lines'])
 ex.append({'source':e['source'],'page':e['pdf_page'],'selected_lines':len(e['lines']),'passed':ok})
def sec(s):
 hours=int(s[:2]);mins=int(s[2:4]);seconds=int(s.split(':')[1])
 assert 0<=hours<24 and 0<=mins<60 and 0<=seconds<60
 return hours*3600+mins*60+seconds
anchor_results=[]
for row in next(c for c in comps if c['id']=='D02')['anchors']:
 assert row['associate'] in pages['F04'][row['associate_page']-1]
 assert row['other'] in pages['F04'][row['other_page']-1]
 anchor_results.append({'event':row['event'],'associate_page':row['associate_page'],'other_page':row['other_page'],'associate_time':row['associate'],'other_time':row['other'],'associate_minus_other_seconds':sec(row['associate'])-sec(row['other'])})
diffs=[x['associate_minus_other_seconds'] for x in anchor_results]
clock={'scope':'Printed times under manually proposed event association; no native clock/utterance identity established','rows':anchor_results,'differences_seconds':diffs,'single_constant_offset_fits_all_rows':len(set(diffs))==1}
annotation=[]
for row in next(c for c in comps if c['id']=='D03')['candidate_pairs']:
 annotation.append({'event':row['event'],'graphic':row['graphic'],'comparison':row['comparison'],'graphic_minus_comparison_seconds':sec(row['graphic'])-sec(row['comparison'])})
x,y=next(c for c in comps if c['id']=='D05')['elapsed_inputs']
assert x in pages['F04'][44] and y in pages['F04'][44]
relay={'first_printed_time':x,'relay_printed_time':y,'difference_seconds':sec(y)-sec(x),'scope':'Difference in printed labels only; source audio, elapsed historical time, intervening information and intent are not verified.'}
au=pins['audio'];ap=a.audio_directory/au['filename'];b=ap.read_bytes();actual_audio={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert actual_audio=={k:au[k] for k in actual_audio}
pr=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(ap)],capture_output=True,text=True,check=True)
meta=json.loads(pr.stdout);duration=float(meta['format']['duration'])
audio={'id':'A01',**actual_audio,'format_name':meta['format']['format_name'],'duration_seconds':duration,'streams':[{'codec_name':s.get('codec_name'),'sample_rate':s.get('sample_rate'),'channels':s.get('channels')} for s in meta['streams']],
 'nominal_labeled_interval_seconds':(26+10)*60,'duration_minus_nominal_seconds':duration-(26+10)*60,'scope':'Byte identity/format only. No listening/transcription, native cassette/WAV provenance, utterance/clock/segment/completeness authentication; nominal endpoints are not exact historical boundary observations.'}
result={'verified_utc':datetime.now(timezone.utc).isoformat(),'fitz_version':fitz.VersionBind,'PDF_entity_checks':[x for x in checks if x['kind']=='PDF entity/text integrity'],'PDF_attachment_API_inventory':[x for x in checks if x['kind']=='Embedded-file API inventory'],'exact_excerpt_groups':ex,'printed_anchor_comparison':clock,'annotation_comparison':{'inputs':'Manually transcribed from source images; not automatically extracted or independently calibrated','rows':annotation},'printed_relay_difference':relay,'p63_p64_representation':{'pages':rendered,'same_pixels':rendered[63]['pixel_sha256']==rendered[64]['pixel_sha256'],'same_text':rendered[63]['text_sha256']==rendered[64]['text_sha256'],'scope':'Same account/Bates association is manual. Render/text difference does not establish different substantive accounts or independent corroboration.'},'audio':audio,
 'all_entity_and_exact_excerpt_checks_passed':all(x['passed'] for x in checks if 'passed' in x) and all(x['passed'] for x in ex),
 'substantive_goal_complete':False,'limits':'Manual reading/transcription and candidate event associations are not proven by this software. No source value/cause selected; no historical cause/intent adjudication.'}
with a.output.open('x') as h:h.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({'PDF_entities_checked':len(result['PDF_entity_checks']),'PDF_pages_checked':sum(x['actual']['pdf_pages'] for x in result['PDF_entity_checks']),'exact_excerpt_groups':len(ex),'all_entity_and_exact_excerpt_checks_passed':result['all_entity_and_exact_excerpt_checks_passed'],'printed_anchor_differences':diffs,'single_constant_offset_fits':clock['single_constant_offset_fits_all_rows'],'annotation_candidate_differences':[x['graphic_minus_comparison_seconds'] for x in annotation],'printed_relay_seconds':relay['difference_seconds'],'audio_duration_seconds':duration},indent=2))
assert result['all_entity_and_exact_excerpt_checks_passed']
