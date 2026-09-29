#!/usr/bin/env python3
"""Independent pdfminer parser checks; never invokes the producer verify mode."""
import hashlib
import io
import json
from pathlib import Path
import platform
import sys

import pdfminer
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTImage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from PIL import Image

import compare

HERE=Path(__file__).absolute().parent
SOURCE=Path("/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf")
SOURCE_SHA="30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f"
KEY_SHA="ac3fd35f7dbc0bee7d970c677e0609520455b789d0a77ffc3d3fb2840ecd86da"


def require(value, why):
    if not value: raise ValueError(why)


def walk(obj):
    if isinstance(obj,LTImage): yield obj
    for child in getattr(obj,"_objs",[]): yield from walk(child)


def main():
    before={}
    def capture(path,sha=None,size=None):
        allowed=SOURCE.parent if Path(path)==SOURCE else (HERE.parent if Path(path)==compare.BASE else HERE)
        path=compare.safe_path(allowed,path)
        raw=path.read_bytes(); actual=compare.digest(raw)
        require(sha is None or actual==sha,"input SHA mismatch")
        require(size is None or len(raw)==size,"input size mismatch")
        before[str(path)]=actual
        return raw
    capture(SOURCE,SOURCE_SHA,52766002)
    key=compare.legacy(()).decode_json(capture(HERE/"assets/run01/provenance-key.json",KEY_SHA))
    receipt=compare.legacy(()).decode_json(capture(HERE/"assets/run01/extraction-receipt.json"))
    capture(HERE/"assets/run01/wrapper-receipt.json")
    capture(Path(__file__).absolute())
    capture(HERE/"compare.py")
    capture(compare.BASE,compare.BASE_SHA256)
    capture(HERE/"PROTOCOL.md",compare.PROTOCOL_SHA256)
    for note,sha in compare.NOTE_PINS.items(): capture(HERE/note,sha)
    require(key["selected_physical_pages"]==list(range(251,287)),"page membership mismatch")
    by_obj={a["object_reference"]["object_id"]:a for a in key["assets"]}
    require(len(by_obj)==56==len(key["assets"]),"object membership mismatch")
    for pin in receipt["files_verified"]:
        capture(HERE/pin["path"],pin["sha256"],pin["bytes"])
    selected_path=HERE/"anonymous-key.json"
    if selected_path.exists():
        selected=compare.legacy(()).decode_json(capture(selected_path))
        selected_ids=[a["asset_id"] for a in selected["assets"]]
    else:
        selected_ids=None
    checks=[]; inspected=[]
    with SOURCE.open("rb") as stream:
        document=PDFDocument(PDFParser(stream),password="")
        encrypted=bool(document.encryption)
        manager=PDFResourceManager(caching=True)
        device=PDFPageAggregator(manager)
        interpreter=PDFPageInterpreter(manager,device)
        for number,page in enumerate(PDFPage.create_pages(document),1):
            if number<251: continue
            if number>286: break
            interpreter.process_page(page)
            layout=device.get_result()
            inspected.append(number)
            for image in walk(layout):
                obj=image.stream.objid
                require(obj in by_obj,"unknown parsed image object")
                entry=by_obj[obj]
                matches=[i for i in entry["invocations"] if i["physical_page"]==number]
                require(len(matches)==1,"page invocation match not unique")
                invocation=matches[0]
                dims=[image.stream.attrs["Width"],image.stream.attrs["Height"]]
                require(dims==entry["native_pdf_dimensions"],"independent dimensions mismatch")
                residual=max(abs(x-y) for x,y in zip(image.bbox,invocation["page_bbox_unclipped_points"]))
                require(residual<=1e-4,"independent placement mismatch")
                ciphertext=image.stream.get_rawdata()
                encoded=image.stream.get_data()
                pin=entry["extracted_view"]
                require(compare.digest(encoded)==pin["sha256"] and len(encoded)==pin["bytes"],"independent encoded JPEG mismatch")
                require(encoded==capture(HERE/pin["path"],pin["sha256"],pin["bytes"]),"encoded parent bytes differ")
                with Image.open(io.BytesIO(encoded)) as header:
                    require(header.format=="JPEG" and list(header.size)==dims,"encoded JPEG header mismatch")
                checks.append({"asset_id":entry["asset_id"],"object_id":obj,"physical_page":number,
                               "dimensions":dims,"placement_bbox_points":list(image.bbox),
                               "placement_max_absolute_residual_points":residual,
                               "decrypted_terminal_encoded_jpeg_sha256":compare.digest(encoded),
                               "predecipher_raw_stream_sha256":compare.digest(ciphertext),
                               "predecipher_raw_differs_from_encoded_jpeg":ciphertext!=encoded})
    require(inspected==list(range(251,287)),"not all 36 pages parsed")
    require(len(checks)==56 and {x["asset_id"] for x in checks}=={x["asset_id"] for x in key["assets"]},"parsed invocation membership mismatch")
    if selected_ids is not None:
        require(set(selected_ids)<={x["asset_id"] for x in checks},"selected image not independently checked")
    for path,sha in before.items():
        require(compare.digest(Path(path).read_bytes())==sha,"input changed during independent verification")
    result={"accepted":True,"parser":"pdfminer.six","parser_version":pdfminer.__version__,
            "python":platform.python_version(),"physical_pages":inspected,"source_encrypted":encrypted,
            "source_sha256":SOURCE_SHA,"key_sha256":KEY_SHA,"input_snapshot":before,
            "recorded_product_count":len(receipt["files_verified"]),"image_invocation_count":len(checks),
            "selected_image_count":None if selected_ids is None else len(selected_ids),
            "selected_asset_ids":selected_ids,"image_checks":checks,
            "distinction":"Raw PDF stream bytes before pdfminer decipher are ciphertext in this encrypted report; JPEG comparison uses decrypted terminal DCT codestream bytes. Neither are camera originals.",
            "limitations":["No pixels/captions/observer labels viewed.","Byte, dimension and placement checks do not establish figure association, historical authenticity, fire severity or causal inference.","All recorded product hashes verified; hashes do not independently verify rendered visual appearance or extracted text."]}
    out=compare.safe_path(HERE,"independent-extraction-verification.json",existing=False)
    with out.open("x") as f: json.dump(result,f,indent=2,sort_keys=True); f.write("\n")
    print(json.dumps({"accepted":True,"pages":len(inspected),"objects":len(checks),"products":len(receipt["files_verified"]),"selected":result["selected_image_count"],"max_placement_residual":max(x["placement_max_absolute_residual_points"] for x in checks)}))


if __name__=="__main__": main()
