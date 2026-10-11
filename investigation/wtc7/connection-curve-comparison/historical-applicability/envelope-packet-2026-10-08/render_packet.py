"""Deterministic JS presentation wrapper; no edits to the frozen packet."""
import argparse
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PACKET_SHA='cb0f9da2f36e384eeeb046528696bba4f379fc8419f393a18ae2f809b05829cc'


def build():
    raw=(HERE/'packet01.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PACKET_SHA or raw!=(HERE/'packet02.json').read_bytes():
        raise ValueError('frozen packet mismatch')
    packet=json.loads(raw)
    # No dependency paths or historical measurements beyond proposed mappings.
    data={key:packet[key] for key in ('status','slots','summary','assets','assumptions','domain_kind')}
    for asset in data['assets'].values():asset.pop('path')
    data['packet_sha256']=PACKET_SHA
    return ('export const PACKET = '+json.dumps(data,sort_keys=True,separators=(',',':'),allow_nan=False)+';\n').encode()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('run',choices=('01','02'))
    args=parser.parse_args();raw=build();path=HERE/('viewer-data'+args.run+'.mjs')
    with path.open('xb') as output:output.write(raw)
    print(json.dumps({'file':path.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}))
