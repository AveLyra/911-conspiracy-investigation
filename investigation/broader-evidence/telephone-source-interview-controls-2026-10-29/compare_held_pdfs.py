"""Compare byte identity and decoded page images without changing source PDFs.

Usage: bundled-python compare_held_pdfs.py SOURCES_DIRECTORY
This compares image samples, not histories, intent, native interview recordings,
or the completeness of the original paper file. Text equality is reported only
as exact extracted-string equality; no normalization selects a preferred value.
"""
import hashlib, json, pathlib, sys
from pypdf import PdfReader

def digest(data): return hashlib.sha256(data).hexdigest()

def describe(path):
    body=path.read_bytes()
    reader=PdfReader(path)
    pages=[]
    for number,page in enumerate(reader.pages,1):
        images=[]
        for item in page.images:
            im=item.image
            images.append({'mode':im.mode,'size':list(im.size),'decoded_samples_sha256':digest(im.tobytes())})
        text=page.extract_text() or ''
        pages.append({'page':number,'media_box':[str(x) for x in page.mediabox],'extracted_characters':len(text),'extracted_utf8_sha256':digest(text.encode()),'images':images})
    return {'filename':path.name,'bytes':len(body),'sha256':digest(body),'page_count':len(pages),'embedded_attachment_count':len(reader.attachments),'pages':pages}

def compare(root):
    a=describe(root/'Marquis-2609600.pdf')
    b=describe(root/'SOC-2609603.pdf')
    arpey=describe(root/'Arpey-2609591.pdf')
    pairs=[]
    for x,y in zip(a['pages'],b['pages']):
        pairs.append({'page':x['page'],'exact_extracted_text_equal':x['extracted_utf8_sha256']==y['extracted_utf8_sha256'],'decoded_image_sample_sets_equal':x['images']==y['images'],'media_boxes_equal':x['media_box']==y['media_box']})
    return {'method':'pypdf page image decoded samples and exact extracted UTF-8; no OCR or source alteration','source_descriptions':[arpey,a,b],'pair_comparison':{'pdf_bytes_identical':a['sha256']==b['sha256'],'page_counts_equal':a['page_count']==b['page_count'],'page_pairs':pairs},'not_tested':['PDF production history','provenance before current official downloads','verbatim interview audio','native carrier/operator or FAA clocks','full page rendering equivalence by pixel subtraction','completeness of November 19 paper interview']}

if __name__=='__main__': print(json.dumps(compare(pathlib.Path(sys.argv[1])),indent=2))
