"""Prospectively corrected 741-column context; failed v1 remains preserved."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
EXPECTED = {'read_context.py':'7eb45a46ea63716e20b9b00dcc7b4757f6a3c021e25cc0c170c97e5cab46951b',
            'PROTOCOL-V2.md':'181a5eda9115ffedd282ae1e83b05c55a07659d6e44b44378b2101388d458b28'}


def pin(path):
    raw = path.read_bytes()
    return {'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}


def setup():
    for name, sha in EXPECTED.items():
        if pin(HERE/name)['sha256'] != sha:
            raise ValueError('Changed v2 dependency '+name)
    spec = importlib.util.spec_from_file_location('force56_failed_v1',HERE/'read_context.py')
    v1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v1)
    before = v1.inputs()
    before.update({name:pin(HERE/name) for name in EXPECTED})
    before['read_context_v2.py'] = pin(Path(__file__))
    return v1, before


def representation(im):
    if im.mode != 'RGB' or im.size != (741,88):
        raise ValueError('Wrong 741 by88 RGB representation')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['controls','save01','save02','show'])
    p.add_argument('--pair',choices=['F5','F6'])
    p.add_argument('--first',type=int);p.add_argument('--last',type=int)
    args = p.parse_args()
    v1,before = setup()
    h = v1.module('base_context_v2','../read_context.py')
    display = v1.module('lossless_display_v2','../approach34/read_context.py')
    if args.mode == 'controls':
        result = display.controls(h)
        result['context_counts'] = [(b[2]-b[0])*(b[3]-b[1]) for b in v1.CONTEXTS.values()] == [10472,2590]
        result['clipped_two_cell_contexts'] = all(v1.CONTEXTS[k] == [max(0,b[0]-2),max(0,b[1]-2),min(741,b[2]+2),min(88,b[3]+2)] for k,b in v1.TARGETS.items())
        representation(Image.new('RGB',(741,88)))
        result['correct_representation'] = True
        try: representation(Image.new('RGB',(745,88)))
        except ValueError: result['wrong_width_rejected'] = True
        else: result['wrong_width_rejected'] = False
        if not all(result.values()) or before != setup()[1]:
            raise AssertionError(result)
        print(json.dumps(result,sort_keys=True));return
    data = {}
    for pair,source in v1.SOURCES.items():
        with Image.open(HERE/'../../native-strips01'/source) as im:
            representation(im)
            data[pair] = h.cells(im,v1.CONTEXTS[pair])
    if before != setup()[1]:raise ValueError('Input changed')
    if args.mode == 'show':
        if args.pair is None or args.first is None or args.last is None:
            raise ValueError('Display bounds required')
        cols = h.sparse(data[args.pair],v1.CONTEXTS[args.pair],args.first,args.last)
        print(f'{args.pair} context {v1.CONTEXTS[args.pair]}; omitted EXACT WHITE only; gN=N,N,N; inclusive equal-RGB runs; no thresholds.')
        for x,col in cols.items():
            rendered = display.encode(col)
            if display.decode(rendered) != col:raise AssertionError('Lossless roundtrip')
            print(f'{x}: {rendered}')
        return
    result = {'inputs':before,'sources':v1.SOURCES,'target_boxes':v1.TARGETS,
              'context_boxes':v1.CONTEXTS,'source_size':[741,88],
              'python':platform.python_version(),'pillow':pillow_version,
              'cells':data,'classification':None,'human_accepted':False}
    target = HERE/('context'+args.mode[-2:]+'.json')
    h.save(target,result)
    if before != setup()[1]:raise ValueError('Input changed after save; preserve as failed')
    print(json.dumps({'output':pin(target),'cells':{k:len(v) for k,v in data.items()}}))


if __name__ == '__main__':main()
