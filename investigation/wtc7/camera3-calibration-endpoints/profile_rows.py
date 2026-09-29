#!/usr/bin/env python3
"""Declared image-repetition diagnostic, not floor/acceleration estimation."""
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
LAGS = list(range(8,19))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def correlations(values, detrend):
    values = np.asarray(values,dtype=np.float64)
    if detrend:
        x = np.arange(len(values),dtype=np.float64)
        design = np.column_stack((np.ones(len(values)),x))
        values = values-design@np.linalg.lstsq(design,values,rcond=None)[0]
    rows=[]
    for lag in LAGS:
        first,last=values[:-lag],values[lag:]
        first,last=first-first.mean(),last-last.mean()
        n1,n2=np.linalg.norm(first),np.linalg.norm(last)
        value=None if min(n1,n2)<=1e-10 else float(np.dot(first,last)/(n1*n2))
        rows.append(dict(lag_pixels=lag,pairs=len(first),correlation=value))
    valid=[r for r in rows if r['correlation'] is not None]
    best=max((r['correlation'] for r in valid),default=None)
    maxima=[] if best is None else [r['lag_pixels'] for r in valid if best-r['correlation']<=1e-12]
    return dict(linear_detrend=detrend,correlations=rows,maximizing_lags=maxima)


def main():
    if len(sys.argv)!=2:
        raise ValueError('Supply one new receipt filename')
    output=HERE/sys.argv[1]
    if output.parent!=HERE or output.exists():
        raise ValueError('Only a new immediate receipt is permitted')
    controls=[]
    x=np.arange(183,dtype=np.float64)
    for period in (12,13,14):
        values=np.cos(2*np.pi*x/period)
        for detrend in (False,True):
            result=correlations(values,detrend)
            assert result['maximizing_lags']==[period]
            controls.append(dict(kind='cosine',period=period,result=result))
    for kind,values,detrend in [('constant_raw',np.ones(183),False),
                                ('constant_detrended',np.ones(183),True),
                                ('affine_ramp_detrended',2*x+10,True)]:
        result=correlations(values,detrend)
        assert result['maximizing_lags']==[]
        controls.append(dict(kind=kind,result=result))
    old=json.loads((HERE/'run01/receipt.json').read_text())
    results=[]
    for row in old['selected']:
        path=Path(row['native']['path'])
        assert sha(path)==row['native']['sha256']
        image=Image.open(path)
        assert image.mode=='L' and image.size==(720,480)
        pixels=np.asarray(image)
        sums=pixels[202:385,402:412].sum(axis=1,dtype=np.uint64)
        profile=sums.astype(np.float64)/10
        windows=[]
        for name,lo,hi in [('full',0,183),('upper',0,91),('lower',91,183)]:
            for detrend in (False,True):
                windows.append(dict(name=name,y_start=202+lo,y_stop=202+hi,
                                    result=correlations(profile[lo:hi],detrend)))
        results.append(dict(index=row['index'],native_sha256=sha(path),
                            row_integer_sums=[int(v) for v in sums],
                            row_means=[float(v) for v in profile],windows=windows))
    pins={name:sha(HERE/name) for name in ['PROTOCOL.md','PROFILE-DECLARATION.md',
          'prepare.py','run01/receipt.json','root-observations.md','independent-observations.md']}
    result=dict(status='pass_image_repetition_diagnostic',python=platform.python_version(),
                numpy=np.__version__,pillow=pillow_version,script_sha256=sha(Path(__file__)),
                pins=pins,box=[402,202,412,385],lags=LAGS,controls=controls,results=results,
                limit='Pixel repetition is not architectural identification, verified metric scale or a historic error bound')
    with output.open('x') as stream:
        json.dump(result,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')
    print(json.dumps(dict(status=result['status'],controls=len(controls),
          summaries=[dict(index=r['index'],peaks=[dict(window=w['name'],
          detrended=w['result']['linear_detrend'],lags=w['result']['maximizing_lags'])
          for w in r['windows']]) for r in results])))


if __name__=='__main__':
    main()
