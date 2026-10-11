#!/usr/bin/env python3
"""Preserve two authorized raw-file responses; ephemeral locators only on stdin."""
import hashlib
import json
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = Path(__file__).resolve().parent
CANDIDATES = [
    ('wtc-7-b1.mpg', '1cRKKHryagLgSSuRwLoL-Qwq93fI-Mv_o', 86021896),
    ('wtc-7-b.mpg', '1LDl5mlwBxSKnL1C7VpfbDNK0ztvjvFrw', 30330880),
]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validate_url(url):
    p = urllib.parse.urlsplit(url)
    if p.scheme != 'https' or not p.hostname or not p.hostname.endswith('.oaiusercontent.com') or p.username or p.password or p.port not in (None, 443):
        raise ValueError('Unapproved artifact transport host')


def main():
    rows = json.loads(sys.stdin.readline())
    if not isinstance(rows, list) or len(rows) != 2:
        raise ValueError('Exactly two transport locators required')
    for row, (_, file_id, size) in zip(rows, CANDIDATES):
        if row['id'] != file_id or row['bytes'] != size:
            raise ValueError('Transport/candidate metadata mismatch')
        validate_url(row['url'])
    out = HERE / 'media'
    out.mkdir(exist_ok=False)
    opener = urllib.request.build_opener(NoRedirect)
    results = []
    for row, (name, file_id, expected) in zip(rows, CANDIDATES):
        result = {'name': name, 'drive_id': file_id, 'expected_bytes': expected,
                  'transport': 'Tool-returned authenticated raw-file reference; ephemeral URL deliberately not retained',
                  'status': 'started'}
        results.append(result)
        started = time.monotonic()
        try:
            with opener.open(row['url'], timeout=30) as response:
                result['http_status'] = response.status
                result['content_type'] = response.headers.get('Content-Type')
                length = response.headers.get('Content-Length')
                result['content_length'] = int(length) if length is not None else None
                if response.status != 200 or (length is not None and int(length) != expected):
                    raise ValueError('Unexpected HTTP status or content length')
                digest, count = hashlib.sha256(), 0
                with (out / name).open('xb') as target:
                    while True:
                        if time.monotonic() - started > 180:
                            raise TimeoutError('Bounded acquisition elapsed limit')
                        block = response.read(min(1024 * 1024, expected - count + 1))
                        if not block:
                            break
                        count += len(block)
                        if count > expected or count > 300000000:
                            raise ValueError('Download byte cap exceeded')
                        target.write(block)
                        digest.update(block)
                result.update(bytes=count, sha256=digest.hexdigest())
                if count != expected:
                    raise ValueError('Incomplete acquired file')
                result['status'] = 'acquired_unmodified_bytes_not_yet_media_verified'
        except Exception as error:
            result['status'] = 'failed_preserve_partial_if_present'
            result['exception_type'] = type(error).__name__
            if isinstance(error, urllib.error.HTTPError):
                result['http_status'] = error.code
            # Exception text and raw HTTP headers may contain ephemeral credentials.
        finally:
            result['elapsed_s'] = time.monotonic() - started
            print(json.dumps({k: result[k] for k in ['name','status','exception_type'] if k in result}), flush=True)
    with (HERE / 'acquisition-receipt.json').open('x') as target:
        json.dump({'procedure_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   'results': results, 'scope': 'No repair, remux, playback or source authenticity finding'}, target, indent=2)
        target.write('\n')
    if any(r['status'].startswith('failed') for r in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
