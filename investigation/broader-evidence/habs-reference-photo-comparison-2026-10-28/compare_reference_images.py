from pathlib import Path
import argparse,hashlib,json
import numpy as np
import PIL
from PIL import Image
from numpy.lib.stride_tricks import sliding_window_view

def prepare(path,margin):
    with Image.open(path) as im:
        im=im.convert('L')
        w,h=im.size
        box=(round(w*margin),round(h*margin),round(w*(1-margin)),round(h*(1-margin)))
        cropped=im.crop(box)
        return np.asarray(cropped.resize((256,256),resample=Image.Resampling.BICUBIC),dtype=np.float64)

def compare(a,b):
    patch=a[16:240,16:240]
    centered=patch-patch.mean()
    denominator_a=np.sqrt(np.sum(centered**2))
    windows=sliding_window_view(b,(224,224))
    sums=windows.sum(axis=(-2,-1))
    sums_sq=np.einsum('ijkl,ijkl->ij',windows,windows,optimize=False)
    numerator=np.einsum('ijkl,kl->ij',windows,centered,optimize=False)
    denominator=denominator_a*np.sqrt(np.maximum(0,sums_sq-sums**2/patch.size))
    scores=np.divide(numerator,denominator,out=np.full_like(numerator,np.nan),where=denominator>0)
    y,x=np.unravel_index(np.nanargmax(scores),scores.shape)
    return {'centered_pearson_r':float(scores[16,16]),'best_translated_pearson_r':float(scores[y,x]),
            'best_window_offset_from_center':[int(x)-16,int(y)-16],
            'translation_space':'256x256 normalized thumbnail; not historical native-image displacement'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',action='append',required=True,help='P31=path, P29=path, A26=path, A21=path')
    args=parser.parse_args()
    supplied=dict(item.split('=',1) for item in args.input)
    assert set(supplied)=={'P31','P29','A26','A21'}
    rows=json.loads((Path(__file__).parent/'SOURCES.json').read_text())
    for row in rows:
        row['path']=supplied[row['id']]
    paths={}
    entity_checks=[]
    for row in rows:
        p=Path(row['path']);data=p.read_bytes()
        with Image.open(p) as im:
            shape=list(im.size);pixel_hash=hashlib.sha256(im.convert('RGB').tobytes()).hexdigest()
        passed=(hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes']
                and shape==row['pixels'] and pixel_hash==row['decoded_RGB_sha256'])
        entity_checks.append({'id':row['id'],'passed':passed,'sha256':row['sha256'],'decoded_RGB_sha256':pixel_hash,'pixels':shape})
        paths[row['id']]=p
    assert all(r['passed'] for r in entity_checks)
    pairs=[('P31','A26','intended'),('P29','A21','intended'),('P31','A21','cross_column_control'),('P29','A26','cross_column_control'),('P31','P31','identical_source_control'),('P29','P29','identical_source_control')]
    results=[]
    for margin in [0.05,0.10,0.15]:
        images={key:prepare(path,margin) for key,path in paths.items()}
        for first,second,kind in pairs:
            values=compare(images[first],images[second])
            results.append({'parent':first,'other':second,'kind':kind,'fractional_margin':margin,
                            'original_files_equal':paths[first].read_bytes()==paths[second].read_bytes(),
                            **values})
    print(json.dumps({'entity_checks':entity_checks,'comparisons':results,
                      'versions':{'numpy':np.__version__,'Pillow':PIL.__version__},
                      'method':'Predeclared grayscale/crop/resize/translation Pearson correlation; same pixels fitted and evaluated; no statistical identification threshold.',
                      'physical_or_exposure_identity_test':False,
                      'custody_or_calibrated_thermal_test':False},indent=2))
if __name__=='__main__':
    main()
