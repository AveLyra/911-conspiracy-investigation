import hashlib,json,sys
from pathlib import Path
from io import BytesIO
import fitz,numpy as np
from PIL import Image
pdf=Path(sys.argv[1]);root=Path(sys.argv[2]);manifest=json.loads(Path(sys.argv[3]).read_text())
assert hashlib.sha256(pdf.read_bytes()).hexdigest()=="957eecd527e1f1ee56867704b630c81edb766e76b8519b95abb5e660ac335f20"
expected={x["reader_page"]:x["sha256"] for x in manifest["images"]}
assert set(range(1,29)).issubset(expected)
doc=fitz.open(pdf);assert doc.page_count==28
refs={}
for n in range(1,29):
 p=root/f"reader-page-{n:02}.jpg"; data=p.read_bytes();assert hashlib.sha256(data).hexdigest()==expected[n];refs[n]=Image.open(BytesIO(data)).convert("L")
out=[]
for n in range(1,29):
 raw=doc[n-1].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).tobytes("png");a=Image.open(BytesIO(raw)).convert("L")
 for kind,other in (("same",n),("adjacent",n%28+1)):
  b=refs[other];z=a.resize(b.size,Image.Resampling.LANCZOS); x=np.asarray(z,dtype=float).ravel();y=np.asarray(b,dtype=float).ravel()
  corr=float(np.corrcoef(x,y)[0,1]);mae=float(np.mean(np.abs(x-y)));out.append({"pdf_page":n,"reader_page":other,"comparison":kind,"correlation":round(corr,4),"mae":round(mae,3)})
print(json.dumps({"pdf_hash_verified":True,"reader_hashes_verified":28,"versions":{"pymupdf":fitz.VersionBind,"numpy":np.__version__,"pillow":__import__("PIL").__version__},"comparisons":out},indent=2))
