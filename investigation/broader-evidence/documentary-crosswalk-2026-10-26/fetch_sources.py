"""Bounded public-document acquisition, exclusive writes, no raw header dumps."""
from pathlib import Path
import datetime, hashlib, json, urllib.request

R = Path(__file__).resolve().parent
SOURCES = {
    'doj-oig-chapter5.html': 'https://oig.justice.gov/sites/default/files/archive/special/0506/chapter5.htm',
    'fbi-ec-2016-04-04.pdf': 'https://www.govinfo.gov/content/pkg/GOVPUB-J1_14-PURL-gpo159739/pdf/GOVPUB-J1_14-PURL-gpo159739.pdf',
    'sdny-11182-2025-08-28.pdf': 'https://www.nysd.uscourts.gov/sites/default/files/2025-08/03-md-01570%2011182.pdf',
}

def fetch(name, url):
    receipt = dict(url=url, accessed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), file='sources/' + name)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Public-source historical research'})
        with urllib.request.urlopen(req, timeout=25) as response:
            b = response.read(16 * 1024 * 1024 + 1)
            assert len(b) <= 16 * 1024 * 1024, 'Document exceeds bounded acquisition; no write'
            receipt.update(http_status=response.status, final_url=response.url,
                           content_type=response.headers.get('Content-Type'),
                           content_encoding=response.headers.get('Content-Encoding'))
        assert b.startswith(b'%PDF-') if name.endswith('.pdf') else b'html' in b[:500].lower()
        with (R / 'sources' / name).open('xb') as f:
            f.write(b)
        receipt.update(bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), status='acquired; not yet substantively verified')
    except Exception as e:
        receipt.update(status='acquisition failed', error=type(e).__name__ + ': ' + str(e))
    return receipt

if __name__ == '__main__':
    (R / 'sources').mkdir(exist_ok=True)
    rows = [fetch(name, url) for name, url in SOURCES.items()]
    with (R / 'acquisition-v1.json').open('x') as f:
        json.dump(rows, f, indent=2)
        f.write('\n')
    print(json.dumps(rows, indent=2))
