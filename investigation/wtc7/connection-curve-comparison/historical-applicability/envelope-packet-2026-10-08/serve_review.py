"""Fixed-asset loopback viewer using the preserved read-only HTTP handler."""
import argparse
import hashlib
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import types

HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
R1=BASE.parent/'comparator-r1-replication'
HELPER_SHA='1ea233c4fa8074298f9791a305fa46f0b1ac3151ce00ce48c8edd7e99de48142'
PACKET_SHA='cb0f9da2f36e384eeeb046528696bba4f379fc8419f393a18ae2f809b05829cc'
CONTROL_SHA='f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def pinned(path,digest):
    if path.is_symlink():raise ValueError('symlink refused')
    raw=path.read_bytes()
    if sha(raw)!=digest:raise ValueError('asset identity mismatch')
    return raw


def handler():
    path=R1/'serve_review.py';raw=pinned(path,HELPER_SHA)
    module=types.ModuleType('conditional_pinned_readonly_handler');module.__file__=str(path)
    exec(compile(raw,str(path),'exec'),module.__dict__)
    return module.handler_for


def routes():
    raw=pinned(HERE/'packet01.json',PACKET_SHA)
    if raw!=pinned(HERE/'packet02.json',PACKET_SHA):raise ValueError('packet repeat mismatch')
    data=json.loads(raw);assets={}
    for asset in data['assets'].values():
        path=BASE/asset['path'];pinned(path,asset['sha256'])
        mime='image/png' if asset['url']=='/page.png' else 'image/jpeg'
        assets[asset['url']]=(path,asset['sha256'],mime)
    path=R1/'localization-control/fixture.png';pinned(path,CONTROL_SHA)
    assets['/control.png']=(path,CONTROL_SHA,'image/png')
    script=(HERE/'viewer-data01.mjs').read_bytes()
    if script!=(HERE/'viewer-data02.mjs').read_bytes():raise ValueError('presentation repeat mismatch')
    expected={key:data[key] for key in ('status','slots','summary','assets','assumptions','domain_kind')}
    for asset in expected['assets'].values():asset.pop('path')
    expected['packet_sha256']=PACKET_SHA
    if script!=('export const PACKET = '+json.dumps(expected,sort_keys=True,separators=(',',':'),allow_nan=False)+';\n').encode():
        raise ValueError('presentation does not match packet')
    for url,file,mime in (('/', 'review.html','text/html; charset=utf-8'),
                          ('/review.mjs','review.mjs','text/javascript; charset=utf-8'),
                          ('/viewer-data.mjs','viewer-data01.mjs','text/javascript; charset=utf-8')):
        path=HERE/file
        if path.is_symlink():raise ValueError('UI symlink refused')
        assets[url]=(path,sha(path.read_bytes()),mime)
    return assets


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--port',type=int,default=0)
    args=parser.parse_args()
    if not 0<=args.port<=65535:parser.error('invalid port')
    assets=routes();server=ThreadingHTTPServer(('127.0.0.1',args.port),handler()(assets))
    print(json.dumps({'url':f'http://127.0.0.1:{server.server_port}/','assets':len(assets),'writes':False,
                      'pins':{url:digest for url,(_,digest,_) in assets.items()}}),flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
