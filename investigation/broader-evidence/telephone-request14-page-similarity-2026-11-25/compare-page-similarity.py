import sys
from pathlib import Path
from io import BytesIO
import fitz
import numpy as np
from PIL import Image

doc = fitz.open(sys.argv[1])
root = Path(sys.argv[2])
for pdf_page, reader_page in [(1,1),(25,25),(27,27),(28,28),(25,28)]:
    ref = Image.open(root / f"reader-page-{reader_page:02}.jpg").convert("L")
    png = doc[pdf_page-1].get_pixmap(matrix=fitz.Matrix(2,2), alpha=False).tobytes("png")
    rendered = Image.open(BytesIO(png)).convert("L").resize(ref.size, Image.Resampling.LANCZOS)
    x = np.asarray(rendered, dtype=float).ravel()
    y = np.asarray(ref, dtype=float).ravel()
    print(pdf_page, reader_page, round(float(np.corrcoef(x,y)[0,1]),4), round(float(np.mean(abs(x-y))),3))
