"""Fixed public-report page derivatives; no PDF authoring or measurements."""
import argparse
import hashlib
import importlib.util
import io
import logging
import math
import os
from pathlib import Path
import sys
import warnings
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
HELPER = HERE.parent/'connection-curve-comparison/render.py'
HELPER_SHA = 'a5083f34465587ff8ee877b5bd1d7dd5a7ced28ec491ab3ec9bbc1a5aed011ba'
if hashlib.sha256(HELPER.read_bytes()).hexdigest() != HELPER_SHA:
    raise ValueError('frozen create-only renderer helper mismatch')
spec = importlib.util.spec_from_file_location('frozen_render_helper', HELPER)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

SOURCES = (
    ('1c', 'ncstar-1-1c-source01.pdf', '3ebb14d79b7096a9c3e7769d4af26c43438c9b56d8a17520a1a9ab4def23a054',
     176, (3, 4, 107, 108, 109, 110, 111, 112, 170, 173, 174, 176)),
    ('1i', 'ncstar-1-1i-source01.pdf', '1415e328e076e78c988f6752a8f293273becd46710a4ae6b4f2ea1bc5a42e83d',
     48, (30, 39, 42, 43, 44)),
)


def render(name):
    import PIL
    from PIL import Image
    import pypdf
    from pypdf import PdfReader
    for _, file, digest, _, _ in SOURCES:
        h.check_source(HERE/file, digest)
    inputs = [HERE/file for _, file, _, _, _ in SOURCES] + [Path(__file__), HELPER,
        h.PDFTOPPM, h.FONT_CONFIG, Path(sys.executable), Path(PIL.__file__), Path(pypdf.__file__)]
    before = [h.pin(p) for p in inputs]
    out = h.fresh_output(HERE, name)
    cfg = ET.fromstring(h.FONT_CONFIG.read_bytes())
    caches = cfg.findall('cachedir')
    if len(caches) != 1:
        raise ValueError('unexpected font config')
    caches[0].text = str(out/'font-cache')
    h.write_new(out/'fonts.conf', ET.tostring(cfg, encoding='utf-8', xml_declaration=True))
    env = os.environ.copy()
    env['FONTCONFIG_FILE'] = str(out/'fonts.conf')
    receipt = dict(status='started', dpi=200, complete_pages=True,
        python=sys.version, executable=sys.executable, Pillow=PIL.__version__, pypdf=pypdf.__version__,
        input_pins_before=before, commands=[], pages=[],
        limit='representation integrity, not historical authenticity or a hermetic dependency closure')
    parser_log = io.StringIO()
    handler = logging.StreamHandler(parser_log)
    logger = logging.getLogger('pypdf'); logger.addHandler(handler)
    failure = None
    caught = []
    try:
        receipt['commands'].append(h.command_capture([str(h.PDFTOPPM), '-v'], env, out, 'poppler-version'))
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            for label, file, _, count, pages in SOURCES:
                source = HERE/file
                reader = PdfReader(source)
                if reader.is_encrypted:
                    reader.decrypt('')
                if len(reader.pages) != count:
                    raise ValueError('page count differs from source locator')
                for number in pages:
                    page = reader.pages[number-1]
                    prefix = out/f'{label}-page-{number:03d}'
                    command = h.command_capture([str(h.PDFTOPPM), '-f', str(number), '-l', str(number),
                        '-singlefile', '-r', '200', '-png', str(source), str(prefix)],
                        env, out, f'{label}-page-{number:03d}')
                    receipt['commands'].append(command)
                    if command['exit_code']:
                        raise RuntimeError('page render failed; diagnostics retained')
                    h.write_new(prefix.with_suffix('.txt'), (page.extract_text() or '').encode())
                    with Image.open(prefix.with_suffix('.png')) as image:
                        image.load()
                        width=float(page.mediabox.width); height=float(page.mediabox.height)
                        if int(page.get('/Rotate', 0)) % 180:
                            width,height=height,width
                        if image.mode != 'RGB' or image.size != (math.ceil(width*200/72), math.ceil(height*200/72)):
                            raise ValueError('render dimensions or mode mismatch')
                        receipt['pages'].append(dict(source=label, physical=number,
                            width=image.width, height=image.height, mode=image.mode,
                            image=h.pin(prefix.with_suffix('.png')),
                            pixel_sha256=h.digest(image.tobytes()), text=h.pin(prefix.with_suffix('.txt'))))
        receipt['input_pins_after'] = [h.pin(p) for p in inputs]
        h.same_pins(before, receipt['input_pins_after'])
        if [(x['source'],x['physical']) for x in receipt['pages']] != [
                (label,n) for label,_,_,_,pages in SOURCES for n in pages]:
            raise ValueError('selected page coverage mismatch')
        receipt['status']='complete-derivatives-only'
    except Exception as exc:
        failure=exc; receipt['status']='failed-preserved'; receipt['error_type']=type(exc).__name__
    finally:
        logger.removeHandler(handler)
        h.write_new(out/'parser.stderr',parser_log.getvalue().encode())
        receipt['warnings']=[dict(category=w.category.__name__,message=str(w.message)) for w in caught]
        receipt['products']=[h.pin(p) for p in sorted(out.rglob('*')) if p.is_file()]
        h.json_new(out/'receipt.json',receipt)
    if failure:
        raise failure
    print({'status':receipt['status'],'pages':len(receipt['pages']),
           'nonempty_render_stderr':sum(bool(c['stderr']['bytes']) for c in receipt['commands'] if '-v' not in c['argv']),
           'parser_stderr_bytes':len(parser_log.getvalue()),'warnings':len(receipt['warnings']),
           'receipt_sha256':h.pin(out/'receipt.json')['sha256']})


if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('--out',required=True)
    render(p.parse_args().out)
