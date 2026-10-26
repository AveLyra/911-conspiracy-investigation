"""Compare preserved public PDF representations without rewriting either."""
from pathlib import Path
import hashlib, json
from pypdf import PdfReader

R=Path(__file__).resolve().parent
def digest(b):return hashlib.sha256(b).hexdigest()
def page_state(p):
    images=[]
    for key,obj in (p.get('/Resources',{}).get('/XObject',{}) or {}).items():
        obj=obj.get_object()
        if obj.get('/Subtype')=='/Image':
            color=obj.get('/ColorSpace'); color=color.get_object() if hasattr(color,'get_object') else color
            color_kind=str(color[0]) if isinstance(color,(list,tuple)) else str(color)
            assert 'IndirectObject' not in color_kind, 'Unresolved transient color representation'
            images.append(dict(name=str(key),width=obj.get('/Width'),height=obj.get('/Height'),bits=obj.get('/BitsPerComponent'),colorspace_kind=color_kind,decoded_bytes=len(obj.get_data()),decoded_sha256=digest(obj.get_data())))
    pixels=[dict(name=str(im.name), size=list(im.image.size), mode='RGB', pixel_sha256=digest(im.image.convert('RGB').tobytes())) for im in p.images]
    content=p.get_contents()
    return dict(media_box=list(map(float,p.mediabox)),crop_box=list(map(float,p.cropbox)),content_sha256=digest(content.get_data() if content is not None else b''),images=images, pixel_images=pixels)

def main():
    files=['sources/fbi-ec-2016-04-04.pdf','sources/fbi-vault-ec-2016-04-04.pdf']
    states=[]
    for f in files:
        b=(R/f).read_bytes();reader=PdfReader(R/f)
        states.append(dict(file=f,bytes=len(b),sha256=digest(b),pages=[page_state(p) for p in reader.pages]))
    assert len(states[0]['pages'])==len(states[1]['pages'])==17
    rows=[]
    for i,(a,b) in enumerate(zip(states[0]['pages'],states[1]['pages']),1):
        rows.append(dict(physical_page=i,content_equal=a['content_sha256']==b['content_sha256'],images_equal=a['images']==b['images'],pixels_equal=a['pixel_images']==b['pixel_images'],boxes_equal=a['media_box']==b['media_box'] and a['crop_box']==b['crop_box']))
    catalog=(R/'sources/govinfo-ec-catalog.html').read_text()
    pos=catalog.find('November 2013')
    record=dict(scope='17 PDF page content streams, direct image payloads, independently decoded RGB pixels and page boxes; not full PDF object graph, fonts, annotations or edit history',representations=states,comparison=rows,
                every_tested_page_component_equal=all(all(row[k] for k in ['content_equal','images_equal','pixels_equal','boxes_equal']) for row in rows),
                catalog_November2013_present=pos>=0,catalog_excerpt=catalog[max(0,pos-100):pos+280] if pos>=0 else None,
                historical_authentication_or_independent_corroboration=False,
                interpretation='Preserve different whole-file bytes. Matching tested page components would limit the difference in this specific comparison; it would not determine how/why files differ or authenticate every assertion.')
    with (R/'source-version-comparison-v3.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
    print(json.dumps({k:record[k] for k in ['every_tested_page_component_equal','catalog_November2013_present','historical_authentication_or_independent_corroboration']}))

if __name__=='__main__':main()
