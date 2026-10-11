"""Extract all twelve pinned JPEG codestreams unchanged for native inspection.

No assembly, scaling, tracing, hidden-pixel recovery or graph metric.
"""
import hashlib
import io
import json
import platform
from pathlib import Path

import pypdf
from PIL import Image

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    out = HERE/'native-strips01'
    if out.exists() or out.is_symlink():
        raise FileExistsError(out)
    data = SOURCE.read_bytes()
    if sha(data) != 'cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4':
        raise ValueError('source hash mismatch')
    inventory = HERE/'pypdf-representation01.json'
    invbytes = inventory.read_bytes()
    rows = json.loads(invbytes)['image_invocations']
    if len(rows) != 12 or {r['name'] for r in rows} != {f'Im{i}' for i in range(12)}:
        raise ValueError('wrong strip membership')
    reader = pypdf.PdfReader(io.BytesIO(data))
    if reader.is_encrypted:
        reader.decrypt('')
    resources = reader.pages[75]['/Resources']['/XObject']
    prepared = []
    for row in rows:
        blob = resources['/'+row['name']].get_data()
        if sha(blob) != row['encoded_jpeg_sha256']:
            raise ValueError('strip hash mismatch')
        image = Image.open(io.BytesIO(blob)); image.load()
        if image.format != 'JPEG' or list(image.size) != row['native_dimensions']:
            raise ValueError('unexpected image')
        prepared.append((row,blob))
    if SOURCE.read_bytes() != data or inventory.read_bytes() != invbytes:
        raise ValueError('input changed')
    out.mkdir()
    for row,blob in prepared:
        with (out/(row['name']+'.jpg')).open('xb') as stream:
            stream.write(blob)
    result = {'status':'unmodified_native_strips_not_curve_support',
        'source_sha256':sha(data),'inventory_sha256':sha(invbytes),
        'script_sha256':sha(Path(__file__).read_bytes()),
        'python':platform.python_version(),'pypdf':pypdf.__version__,
        'strips':rows,
        'limits':['Preserve actual CTMs; do not assume uniform pitch across all strips.',
                  'PDF overlays can hide native JPEG pixels; embedded bytes alone do not establish published visibility.',
                  'No curve identity, ordinate, uncertainty bound or human acceptance.']}
    with (out/'receipt.json').open('x') as stream:
        json.dump(result,stream,indent=2,sort_keys=True); stream.write('\n')
    print(json.dumps({'directory':str(out),'strips':len(rows),'source_unchanged':SOURCE.read_bytes()==data}))

if __name__ == '__main__':
    main()
