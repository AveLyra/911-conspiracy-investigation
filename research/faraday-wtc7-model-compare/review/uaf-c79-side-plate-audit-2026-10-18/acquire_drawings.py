"""One bounded public GET per technical sheet; no source overwrite or repair."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
import urllib.request

SOURCES = {
    "frankel-9114-public-copy": "https://www.metabunk.org/attachments/9114-pdf.28807/",
    "frankel-1091-public-copy": "https://www.metabunk.org/attachments/1091-pdf.28913/",
}
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path, value):
    with path.open("x") as f:
        json.dump(value, f, indent=2)
        f.write("\n")
class HttpsOnly(urllib.request.HTTPRedirectHandler):
    max_redirections = 5
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not newurl.startswith("https://"):
            raise ValueError("Non-HTTPS redirect rejected")
        return super().redirect_request(req, fp, code, msg, headers, newurl)
def acquire(item):
    label, url = item
    target = output/(label+".pdf")
    receipt = {"label":label,"url":url,"started_utc":datetime.now(timezone.utc).isoformat(),"custody":"Public technical drawing copy on a discussion-site attachment host, not authenticated agency original"}
    start = time.monotonic()
    try:
        request = urllib.request.Request(url, headers={"User-Agent":"Public-source-technical-audit/1.0","Accept-Encoding":"identity"})
        with urllib.request.build_opener(HttpsOnly()).open(request,timeout=20) as response, target.open("xb") as f:
            receipt.update(status=response.status, final_url=response.url, headers={k:v for k,v in response.headers.items() if k.lower() in {"content-type","content-length","last-modified","etag"}})
            count=0
            while True:
                if time.monotonic()-start>60:
                    raise TimeoutError("60-second total limit")
                chunk=response.read(65536)
                if not chunk: break
                count+=len(chunk)
                if count>16*1024*1024: raise ValueError("16MiB limit")
                f.write(chunk)
        receipt["complete"]=True
    except Exception as e:
        receipt.update(complete=False,error=f"{type(e).__name__}: {e}")
    if target.exists():receipt.update(bytes=target.stat().st_size,sha256=sha(target))
    receipt["ended_utc"]=datetime.now(timezone.utc).isoformat()
    save(output/(label+"-receipt.json"),receipt)
    return receipt
if __name__=="__main__":
    output=Path(sys.argv[1]);output.mkdir(parents=True,exist_ok=False)
    with ThreadPoolExecutor(max_workers=2) as pool: receipts=list(pool.map(acquire,SOURCES.items()))
    print(json.dumps(receipts,indent=2))
