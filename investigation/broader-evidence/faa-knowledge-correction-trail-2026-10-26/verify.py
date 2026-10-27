"""Verify public-package integrity and optionally the identified original source bytes.

Usage: python3 verify.py [--sources-map /path/to/local-map.json]
Source map format: {"DOT-INTERVIEWS":"/local/source.pdf", ...}.
No network access, writes, source modification, redaction reconstruction or authenticity claim.
"""
import argparse, hashlib, json, re
from pathlib import Path

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sources-map',type=Path)
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'MANIFEST.json').read_text())
    for name,row in manifest['files'].items():
        path=root/name
        assert path.is_file(),name
        data=path.read_bytes()
        assert len(data)==row['bytes'] and digest(data)==row['sha256'],name
    sources=json.loads((root/'SOURCES.json').read_text())['sources']
    pins=json.loads((root/'EXCERPTS.json').read_text())['excerpts']
    lookup={p['id']:p for p in pins}
    assert len(lookup)==len(pins)==45
    for pin in pins:
        assert pin['source_id'] in sources
        assert digest(pin['text'].encode())==pin['excerpt_sha256'],pin['id']
        assert 1<=pin['physical_page']<=sources[pin['source_id']]['physical_pages']
        assert pin['text'].rstrip() in (root/'EXCERPTS.md').read_text(),pin['id']
    findings=json.loads((root/'FINDINGS.json').read_text())['entries']
    assert len(findings)==14 and len({f['id'] for f in findings})==14
    for row in findings:
        assert all(x in lookup for x in row['source_pins']),row['id']
        assert row['strongest_alternative_or_objection'] and row['what_would_change_assessment']
    targets=json.loads((root/'OPEN-RECORDS.json').read_text())['targets']
    assert len(targets)==10 and all(t['current_status'] for t in targets)
    # Limited payload screen; requires the separate substantive human/agent review.
    for name in manifest['files']:
        if name==Path(__file__).name:continue
        text=(root/name).read_text()
        assert '/Users/' not in text and '/Volumes/' not in text,name
        assert not re.search(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}',text,re.I),name
        assert 'PRIVATE KEY-----' not in text,name
    result={'manifest_files':len(manifest['files']),'pin_hashes':len(pins),'ledger_entries':len(findings),'open_record_groups':len(targets),'source_byte_hashes':0,'reextracted_substrings':0,'manual_image_fields':sum('image_sha256' in p for p in pins),'limits':'Mechanics only: not source authenticity, historical truth, search completeness or intent.'}
    if args.sources_map:
        from pypdf import PdfReader
        source_map=json.loads(args.sources_map.read_text())
        readers={}
        cache={}
        for ident,path in source_map.items():
            data=Path(path).read_bytes()
            assert digest(data)==sources[ident]['sha256'],ident
            assert len(data)==sources[ident]['bytes'],ident
            result['source_byte_hashes']+=1
        for pin in pins:
            if 'character_start' not in pin:continue
            ident=pin['source_id'];assert ident in source_map,ident
            if ident not in readers:readers[ident]=PdfReader(source_map[ident])
            key=(ident,pin['physical_page'])
            if key not in cache:cache[key]=readers[ident].pages[key[1]-1].extract_text() or ''
            text=cache[key]
            assert digest(text.encode())==pin['page_text_sha256'],pin['id']
            a,b=pin['character_start'],pin['character_end']
            assert text[a:b]==pin['text'],pin['id']
            assert text.count('\n',0,a)+1==pin['source_extraction_line_start'],pin['id']
            assert text.count('\n',0,b)+1==pin['source_extraction_line_end'],pin['id']
            result['reextracted_substrings']+=1
    else:
        result['source_verification']='Not run: provide --sources-map to check original bytes and re-extract pins.'
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
