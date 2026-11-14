#!/usr/bin/env python3
"""Download only official NIST routes and log exact observed HTTP outcomes.

No proxy, alternate DNS, host override, or access-control bypass is used.
XLSX bytes are never opened and resaved. Logs distinguish no HTTP response
from a real HTTP status. Response-body hashes are not workbook hashes unless
valid_xlsx is true.
"""
import argparse, concurrent.futures, datetime, hashlib, io, json, pathlib
import urllib.request, urllib.error, zipfile

ROUTES = [
    ('project', 'https://www.nist.gov/programs-projects/measurement-structural-performance-fire/steel-concrete-composite-floors'),
    ('drawings', 'https://www.nist.gov/document/cbtestsetupinstrumentationdrawings'),
    ('CB-DA-AMB', 'https://www.nist.gov/document/cbdaambientdata'),
    ('CB-DA', 'https://www.nist.gov/document/cbdadata'),
    ('CB-DA-SC', 'https://www.nist.gov/document/cbdascdata'),
    ('CB-SP', 'https://www.nist.gov/document/cbspdata'),
    ('CB-SP-SC', 'https://www.nist.gov/document/cbspscdata'),
    ('CB-DA-AMB-direct', 'https://www.nist.gov/system/files/documents/2020/02/14/CB-DA-AMB.xlsx'),
]

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

class RedirectLog(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain=[]
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append({'url':req.full_url,'http_status':code,'location':headers.get('Location'),'next_url':newurl})
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def retrieve(item, out, method='GET'):
    label,url=item
    rec={'label':label,'method':method,'requested_url':url,'started_utc':now(),
         'final_url':None,'http_status':None,'content_type':None,'response_bytes':None,
         'response_sha256':None,'native_file_bytes':None,'native_file_sha256':None,
         'valid_zip':None,'valid_xlsx':None,'redirects':[],'error':None}
    redirect=RedirectLog()
    opener=urllib.request.build_opener(redirect)
    request=urllib.request.Request(url,method=method,headers={'User-Agent':'Scooby-R08-Source-Recovery/1.0','Accept':'*/*'})
    try:
        try:
            response=opener.open(request,timeout=25)
        except urllib.error.HTTPError as err:
            response=err
        with response:
            body=response.read()
            rec.update(final_url=response.geturl(),http_status=response.status,
                       content_type=response.headers.get('Content-Type'),
                       headers=dict(response.headers.items()),response_bytes=len(body),
                       response_sha256=hashlib.sha256(body).hexdigest())
        if method=='GET':
            rec['valid_zip']=zipfile.is_zipfile(io.BytesIO(body))
            rec['valid_xlsx']=False
            if rec['valid_zip']:
                with zipfile.ZipFile(io.BytesIO(body)) as z:
                    bad=z.testzip()
                    rec['zip_crc_error_member']=bad
                    names=z.namelist()
                    rec['zip_member_count']=len(names)
                    rec['valid_xlsx']=bad is None and '[Content_Types].xml' in names and 'xl/workbook.xml' in names
            if rec['valid_xlsx'] and rec['http_status']==200:
                path=out/'native'/(label+'.xlsx')
                rec.update(native_file_bytes=len(body),native_file_sha256=rec['response_sha256'])
            else:
                path=out/'responses'/(label+'.body')
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(body)
            rec['saved_relative_path']=str(path.relative_to(out))
    except Exception as exc:
        rec['error']=f'{type(exc).__name__}: {exc}'
    rec['redirects']=redirect.chain
    rec['finished_utc']=now()
    return rec

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=pathlib.Path,default=pathlib.Path('http_attempts'))
    p.add_argument('--routes',type=pathlib.Path,help='JSON list of [label,url] pairs; default uses original official routes')
    p.add_argument('--method',choices=['GET','HEAD'],default='GET')
    args=p.parse_args()
    routes=json.loads(args.routes.read_text()) if args.routes else ROUTES
    for _,url in routes:
        host=urllib.parse.urlparse(url).hostname or ''
        if not (host=='nist.gov' or host.endswith('.nist.gov')):
            raise SystemExit(f'Only NIST hosts allowed: {host}')
    args.out.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        records=list(pool.map(lambda x:retrieve(x,args.out,args.method),routes))
    (args.out/'attempts.json').write_text(json.dumps(records,indent=2)+'\n')
    for r in records:
        print(json.dumps({k:r.get(k) for k in ['label','http_status','final_url','response_bytes','content_type','valid_xlsx','error']}))

if __name__=='__main__':
    main()
