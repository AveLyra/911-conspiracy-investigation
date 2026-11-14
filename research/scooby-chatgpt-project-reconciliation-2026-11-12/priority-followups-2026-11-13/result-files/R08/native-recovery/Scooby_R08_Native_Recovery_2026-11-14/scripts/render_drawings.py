#!/usr/bin/env python3
"""Extract original drawings; create explicitly derived PNG previews with Inkscape."""
import concurrent.futures, hashlib, json, pathlib, subprocess, zipfile
ROOT=pathlib.Path(__file__).resolve().parent
src=ROOT/'direct_get/native/drawings.xlsx'
dest=ROOT/'drawings_inspection'
dest.mkdir(exist_ok=True)
with zipfile.ZipFile(src) as z:
    for n in z.namelist():
        if n.startswith('xl/media/'):
            (dest/pathlib.Path(n).name).write_bytes(z.read(n))
def render(p):
    out=p.with_suffix('.png')
    args=['inkscape',str(p),'--export-type=png','--export-width=2400',f'--export-filename={out}']
    r=subprocess.run(args,capture_output=True,text=True,timeout=50)
    result={'source_member':'xl/media/'+p.name,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
      'derived_preview':out.name,'command':args,'exit_code':r.returncode,'stderr':r.stderr,
      'preview_sha256':hashlib.sha256(out.read_bytes()).hexdigest() if out.exists() else None,
      'note':'Rasterized preview, not a measurement or native cell. Original EMF retained in source workbook.'}
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records=list(pool.map(render,sorted(dest.glob('*.emf'))))
(dest/'render_manifest.json').write_text(json.dumps(records,indent=2)+'\n')
for r in records:print(r['source_member'],r['exit_code'],r['derived_preview'])
