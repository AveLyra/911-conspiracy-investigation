import urllib.request,datetime,json,hashlib,pathlib
out=pathlib.Path('/workspace/scratch/235f530e8960/r08_work/alternate_routes')
urls=[('record_nerdm','https://data.nist.gov/od/id/mds2-2181?format=nerdm'),('record_rmm','https://data.nist.gov/rmm/records/mds2-2181'),('search_choe','https://data.nist.gov/rmm/records?searchphrase=Choe'),('rmm_openapi','https://data.nist.gov/rmm/openapi.json'),('doi','https://doi.org/10.18434/M32181')]
records=[]
for name,u in urls:
 r={'name':name,'requested_url':u,'method':'GET','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'}),timeout=25) as f:
   b=f.read();p=out/(name+'.response');p.write_bytes(b);r.update(http_status=f.status,final_url=f.url,content_type=f.headers.get('Content-Type'),byte_size=len(b),sha256=hashlib.sha256(b).hexdigest(),saved_path=str(p),response_headers=dict(f.headers))
   try:
    j=json.loads(b)
    if name=='search_choe': print(json.dumps([{'id':v.get('@id'),'title':v.get('title'),'landingPage':v.get('landingPage')} for v in j['ResultData']]))
    else: print(json.dumps(j)[:18000] if name!='rmm_openapi' else 'openapi saved')
   except Exception: pass
 except Exception as e:r['error']=repr(e)
 r['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();records.append(r);print(json.dumps({k:v for k,v in r.items() if k!='response_headers'}))
 (out/'retrieval_manifest.json').write_text(json.dumps(records,indent=2))
