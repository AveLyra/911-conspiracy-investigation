"""Fixed-roster derivative integrity only; no PDF text/figure interpretation."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader
import pypdf

OUT = Path('/private/tmp/windsor-integrity.QxjmlU')
SOURCE = Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/windsor-thesis-2026-10-08')
PDF = SOURCE/'fletcher-2009-thesis.pdf'
RENDER = Path('/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm')
RANGES = [(1,1),(11,15),(33,34),(81,94),(114,138),(139,152),(153,154),(161,162),(166,171),(197,202)]
PAGES = [n for a,b in RANGES for n in range(a,b+1)]
EXPECTED = {'bytes':4425293,'sha256':'4066628f6c6a8b13f7fef63e1602a1b3eae807acbac7f032b67e68c1718a1543'}

def pin(p):
    with p.open('rb') as stream:
        digest = hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':p.stat().st_size,'sha256':digest}

def save(p,j):
    with p.open('x') as stream:
        json.dump(j,stream,indent=2,sort_keys=True);stream.write('\n')

assert len(PAGES)==len(set(PAGES))==77
assert pin(PDF)==EXPECTED
assert PDF.open('rb').read(5)==b'%PDF-'
assert len(PdfReader(PDF).pages)==207
assert not list(OUT.glob('page-*.png'))
config = ET.parse(OUT/'fonts.conf').getroot()
root_config = ET.parse(SOURCE/'render/fonts.conf').getroot()
assert [n.text for n in config.findall('dir')]==[n.text for n in root_config.findall('dir')]
assert [n.text for n in config.findall('cachedir')]==[str(OUT/'font-cache')]
(OUT/'font-cache').mkdir(exist_ok=False)
env = dict(os.environ,FONTCONFIG_FILE=str(OUT/'fonts.conf'),FONTCONFIG_PATH=str(OUT))
names=[f'page-{n:03}.png' for n in PAGES]
assert sorted(p.name for p in (SOURCE/'render').glob('page-*.png'))==sorted(names)
held={name:pin(SOURCE/'render'/name) for name in names}
methods={str(p):pin(p) for p in [PDF, RENDER, Path(sys.executable), Path(pypdf.__file__),
    Path(Image.__file__),OUT/'fonts.conf',OUT/'verify_render.py',SOURCE/'PROTOCOL.md',SOURCE/'PAGE-SELECTION.md',
    SOURCE/'SCOPE-EXPANSION.md',SOURCE/'failed-render-receipts.json',SOURCE/'render/fonts.conf',
    SOURCE/'render/render-receipts.json',SOURCE/'render/expansion-render-receipts.json']}
version=subprocess.run([str(RENDER),'-v'],capture_output=True,env=env,timeout=10)
assert version.returncode==0
receipt={'scope':'same-renderer independent execution; not independent rendering algorithm, source accuracy or historical authentication',
    'status':'started','source_before':pin(PDF),'pdf_pages':207,'ranges':RANGES,'roster':PAGES,
    'method_before':methods,'held_before':held,'font_directories':[n.text for n in config.findall('dir')],
    'fontconfig_file':str(OUT/'fonts.conf'),'fontconfig_path':str(OUT),
    'runtime':{'python':platform.python_version(),'pypdf':pypdf.__version__,'pillow':Image.__version__},
    'renderer_version':{'stdout':version.stdout.decode(),'stderr':version.stderr.decode()},
    'commands':[],'comparisons':[]}
save(OUT/'start.json',receipt)
started=time.monotonic()
try:
    for first,last in RANGES:
        assert time.monotonic()-started<600
        cmd=[str(RENDER),'-f',str(first),'-l',str(last),'-r','110','-png',str(PDF),str(OUT/'page')]
        with (OUT/f'render-{first}-{last}.stdout').open('xb') as stdout, (OUT/f'render-{first}-{last}.stderr').open('xb') as stderr:
            run=subprocess.run(cmd,stdout=stdout,stderr=stderr,env=env,timeout=60)
        stdout_pin=pin(OUT/f'render-{first}-{last}.stdout');stderr_pin=pin(OUT/f'render-{first}-{last}.stderr')
        receipt['commands'].append({'command':cmd,'returncode':run.returncode,'stdout':stdout_pin,'stderr':stderr_pin})
        print(json.dumps({'range':[first,last],'exit_code':run.returncode,'stderr_bytes':stderr_pin['bytes']}),flush=True)
        assert run.returncode==0 and stdout_pin['bytes']==stderr_pin['bytes']==0, 'render failure or diagnostic: stop; no further ranges'
        assert all((OUT/f'page-{n:03}.png').is_file() for n in range(first,last+1))
    assert sorted(p.name for p in OUT.glob('page-*.png'))==sorted(names)
    for name in names:
        original=SOURCE/'render'/name; reproduced=OUT/name
        byte_equal=original.read_bytes()==reproduced.read_bytes()
        with Image.open(original) as a, Image.open(reproduced) as b:
            a.load();b.load()
            pixel_equal=a.mode==b.mode and a.size==b.size and a.tobytes()==b.tobytes()
            record={'name':name,'png':pin(reproduced),'byte_identical':byte_equal,'pixel_identical':pixel_equal,
                    'mode':a.mode,'dimensions':list(a.size),'decoded_pixel_sha256':hashlib.sha256(a.tobytes()).hexdigest()}
        receipt['comparisons'].append(record)
        assert byte_equal and pixel_equal, name
    receipt['source_after']=pin(PDF)
    receipt['method_after']={p:pin(Path(p)) for p in methods}
    receipt['held_after']={name:pin(SOURCE/'render'/name) for name in names}
    assert receipt['source_after']==EXPECTED and receipt['method_after']==methods and receipt['held_after']==held
    receipt['status']='passed'
except BaseException as exc:
    receipt.update(status='failed',error_type=type(exc).__name__,error=str(exc))
    raise
finally:
    receipt['elapsed_s']=time.monotonic()-started
    receipt['source_final']=pin(PDF)
    save(OUT/'receipt.json',receipt)
print(json.dumps({'status':receipt['status'],'pages':len(receipt['comparisons']),
    'png_bytes':sum(r['png']['bytes'] for r in receipt['comparisons']),
    'all_byte_identical':all(r['byte_identical'] for r in receipt['comparisons']),
    'all_pixel_identical':all(r['pixel_identical'] for r in receipt['comparisons']),
    'elapsed_s':receipt['elapsed_s'],'receipt':pin(OUT/'receipt.json')}),flush=True)
