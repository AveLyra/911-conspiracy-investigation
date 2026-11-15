#!/usr/bin/env python3
"""Compare page-position image patterns; output metrics only, not source images."""
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
P=argparse.ArgumentParser();P.add_argument('--pdf',required=True);P.add_argument('--images',required=True);P.add_argument('--manifest',required=True);P.add_argument('--render-dir',required=True);a=P.parse_args()
pdf=Path(a.pdf);assert hashlib.sha256(pdf.read_bytes()).hexdigest()=='957eecd527e1f1ee56867704b630c81edb766e76b8519b95abb5e660ac335f20'
root=Path(a.images);items=json.loads(Path(a.manifest).read_text());items=items.get('images',items) if isinstance(items,dict) else items; by={x['reader_page']:x for x in items};assert len(by)==28
out=Path(a.render_dir);out.mkdir(exist_ok=False);subprocess.run(['pdftoppm','-r','100','-png',str(pdf),str(out/'page')],check=True)
def v(path):
 x=np.asarray(Image.open(path).convert('L').resize((192,192)),dtype=float).reshape(-1);return (x-x.mean())/(x.std()+1e-8)
reader=[];render=[]
for i in range(1,29):
 f=root/('reader-page-%02d.jpg'%i);assert hashlib.sha256(f.read_bytes()).hexdigest()==by[i]['sha256'];reader.append(v(f));render.append(v(out/('page-%02d.png'%i)))
c=np.array(reader)@np.array(render).T/len(reader[0]);rows=[]
for i in range(28):
 off=np.delete(c[i],i); rows.append({'reader_page':i+1,'pdf_same_position':i+1,'same_position_correlation':round(float(c[i,i]),6),'best_other_correlation':round(float(off.max()),6),'best_pdf_page':int(np.argmax(c[i]))+1})
print(json.dumps({'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'dimensions':[192,192],'render_dpi':100,'rows':rows,'same_position_best':sum(x['best_pdf_page']==x['reader_page'] for x in rows),'min_margin':min(x['same_position_correlation']-x['best_other_correlation'] for x in rows)},indent=2))
