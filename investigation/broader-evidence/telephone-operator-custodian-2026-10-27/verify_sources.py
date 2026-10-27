"""Check seven held image entities; this does not authenticate any telephone call."""
import argparse, hashlib, json
from pathlib import Path
from PIL import Image

parser=argparse.ArgumentParser()
parser.add_argument('source_directory',type=Path)
parser.add_argument('pins',type=Path)
parser.add_argument('output',type=Path)
args=parser.parse_args()
assert not args.output.exists(), 'Preserve the earlier run; choose a new output'
checks=[]
for row in json.loads(args.pins.read_text()):
    path=args.source_directory/row['filename']
    body=path.read_bytes()
    with Image.open(path) as image:
        actual={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),
                'width':image.width,'height':image.height,'image_format':image.format}
        image.verify()
    expected={key:row[key] for key in actual}
    checks.append(dict(id=row['id'],filename=row['filename'],actual=actual,
                       expected=expected,passed=actual==expected))
result=dict(scope='Entity integrity and decoding only; manual transcriptions, historical provenance and call joins are not software-verified',
            source_checks=len(checks),passed=sum(x['passed'] for x in checks),
            all_passed=all(x['passed'] for x in checks),checks=checks)
with args.output.open('x') as handle:json.dump(result,handle,indent=2)
print(json.dumps({key:value for key,value in result.items() if key!='checks'},indent=2))
assert result['all_passed']
