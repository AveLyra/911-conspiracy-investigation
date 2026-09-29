"""Extract three fixed report representations; no historical measurements."""
import hashlib
import io
import json
from pathlib import Path
import platform

import pypdf
from PIL import Image

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf')
SOURCE_SHA = '30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    before = digest(SOURCE.read_bytes())
    if before != SOURCE_SHA:
        raise ValueError('Source PDF differs')
    reader = pypdf.PdfReader(SOURCE)
    outputs = []
    for page, name, obj_id, size, filename in (
        (167, '/Im0', 711, (378, 504), 'figure530.jpg'),
        (168, '/Im0', 714, (1024, 768), 'figure531-decoded.png'),
        (168, '/Im1', 715, (540, 301), 'figure532.jpg'),
    ):
        ref = reader.pages[page - 1]['/Resources']['/XObject'].raw_get(name)
        obj = ref.get_object()
        if ref.idnum != obj_id or (obj['/Width'], obj['/Height']) != size:
            raise ValueError('Fixed object identity/dimensions differ')
        if obj['/Filter'] == '/DCTDecode':
            raw = obj.get_data()
            kind = 'decrypted terminal JPEG codestream; no re-encoding'
        elif obj['/Filter'] == '/FlateDecode' and obj_id == 714:
            raw = reader.pages[page - 1].images[name].data
            kind = 'decoded report raster exported losslessly as PNG by pypdf'
        else:
            raise ValueError('Unexpected representation')
        with Image.open(io.BytesIO(raw)) as im:
            if im.size != size or im.format != ('PNG' if obj_id == 714 else 'JPEG'):
                raise ValueError('Export dimensions/format differ')
        outputs.append((filename, raw, {
            'page': page, 'resource': name, 'object_id': obj_id,
            'dimensions': size, 'kind': kind, 'bytes': len(raw),
            'sha256': digest(raw), 'file': filename,
        }))
    if digest(SOURCE.read_bytes()) != before:
        raise ValueError('Source changed during extraction')
    out = HERE / 'representations'
    out.mkdir(exist_ok=False)
    for filename, raw, _ in outputs:
        with (out / filename).open('xb') as f:
            f.write(raw)
    receipt = {'source_sha256': before, 'source_unchanged': True,
               'script_sha256': digest(Path(__file__).read_bytes()),
               'python': platform.python_version(), 'pypdf': pypdf.__version__,
               'outputs': [row for _, _, row in outputs],
               'ceiling': 'Report representation identity only; no camera authenticity, clocks or glass findings.'}
    with (out / 'receipt.json').open('x') as f:
        json.dump(receipt, f, indent=2)
        f.write('\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
