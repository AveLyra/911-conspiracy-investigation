"""Read QuickTime atom bounds and stsz/stts tables; never decode media.

Offsets are zero-based file bytes; sample positions are zero-based table indexes.
Only known structural containers are traversed. Other payloads are not interpreted.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, io, json, platform, struct, sys

CONTAINERS = {b'moov', b'trak', b'mdia', b'minf', b'stbl', b'edts', b'dinf'}
MAX_ATOMS = 10000
MAX_TABLE_BYTES = 8 * 1024 * 1024

class InvalidTable(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise InvalidTable(message)

def u32(data, offset):
    require(offset >= 0 and offset + 4 <= len(data), 'truncated uint32')
    return struct.unpack_from('>I', data, offset)[0]

def table_stsz(data, offset=0):
    require(len(data) >= 12, 'truncated stsz fixed fields')
    version, flags = data[0], int.from_bytes(data[1:4], 'big')
    require(version == 0, 'unsupported stsz version')
    fixed, count = u32(data, 4), u32(data, 8)
    expected = 12 if fixed else 12 + count * 4
    require(expected == len(data), 'stsz declared entries do not match payload length')
    sizes = list(struct.unpack_from('>'+str(count)+'I', data, 12)) if not fixed and count else []
    zeroes = [i for i, size in enumerate(sizes) if size == 0]
    r = dict(version=version, flags=flags, default_sample_size=fixed,
             sample_count=count, sample_count_byte_offset=offset+8,
             table_start_byte_offset=offset+12, stored_entry_count=len(sizes),
             positive_size_count=count if fixed else sum(size > 0 for size in sizes),
             zero_size_count=0 if fixed else len(zeroes), zero_size_indexes=zeroes,
             zero_size_entry_byte_offsets=[offset+12+4*i for i in zeroes],
             total_declared_sample_bytes=fixed*count if fixed else sum(sizes),
             minimum_size=fixed if fixed and count else min(sizes, default=None),
             maximum_size=fixed if fixed and count else max(sizes, default=None))
    r['first_entries']=[dict(index=i,size=size,byte_offset=offset+12+4*i) for i,size in enumerate(sizes[:10])]
    r['last_entries']=[dict(index=i,size=sizes[i],byte_offset=offset+12+4*i) for i in range(max(0,len(sizes)-10),len(sizes))]
    return r

def table_stts(data, offset=0):
    require(len(data) >= 8, 'truncated stts fixed fields')
    version, flags = data[0], int.from_bytes(data[1:4], 'big')
    require(version == 0, 'unsupported stts version')
    count = u32(data,4)
    require(8 + count*8 == len(data), 'stts declared entries do not match payload length')
    entries=[]
    first_sample=0
    first_time=0
    for i in range(count):
        samples,delta=struct.unpack_from('>II',data,8+i*8)
        entries.append(dict(index=i,byte_offset=offset+8+i*8,sample_count=samples,
                            sample_delta=delta,first_sample_index=first_sample,
                            first_sample_media_time_units=first_time))
        first_sample += samples
        first_time += samples*delta
    return dict(version=version, flags=flags, entry_count=count,
                entry_count_byte_offset=offset+4, total_samples=first_sample,
                sum_sample_deltas_media_units=first_time, entries=entries)

def inspect(source, size):
    atoms=[]
    tables=[]
    hints=[]
    def read_at(position, length):
        require(0 <= position <= size and 0 <= length <= MAX_TABLE_BYTES, 'read outside allowed size')
        require(position+length <= size, 'read beyond file')
        source.seek(position)
        data=source.read(length)
        require(len(data)==length, 'short read')
        return data
    def walk(start, end, path, depth=0):
        require(depth < 16, 'too many atom levels')
        position=start
        type_counts={}
        while position < end:
            require(len(atoms) < MAX_ATOMS, 'too many atoms')
            require(end-position>=8, 'truncated atom header')
            header=read_at(position,8)
            declared,kind=struct.unpack('>I4s',header)
            header_size=8
            if declared==1:
                require(end-position>=16, 'truncated extended atom header')
                length=struct.unpack('>Q',read_at(position+8,8))[0]
                header_size=16
            elif declared==0:
                length=end-position
            else:
                length=declared
            require(length>=header_size and position+length<=end, 'invalid atom bounds')
            type_counts[kind]=type_counts.get(kind,0)+1
            label=kind.decode('latin1')+'['+str(type_counts[kind])+']'
            here=path+'/'+label
            payload=position+header_size
            row=dict(path=here,type_hex=kind.hex(),type=kind.decode('latin1'),
                     offset=position,size=length,header_bytes=header_size,
                     payload_offset=payload,end_exclusive=position+length)
            atoms.append(row)
            if kind in CONTAINERS:
                walk(payload,position+length,here,depth+1)
            elif kind in (b'stsz',b'stts'):
                data=read_at(payload,length-header_size)
                result=(table_stsz if kind==b'stsz' else table_stts)(data,payload)
                tables.append(dict(atom=row,fields=result))
            elif kind==b'hdlr' and length-header_size>=12:
                # Raw four-byte locator only; no additional handler fields interpreted.
                hints.append(dict(path=here,kind='raw four bytes at handler payload+8',
                                  byte_offset=payload+8,ascii=read_at(payload+8,4).decode('latin1')))
            elif kind==b'stsd' and length-header_size>=16:
                hints.append(dict(path=here,kind='raw four bytes at description payload+12',
                                  byte_offset=payload+12,ascii=read_at(payload+12,4).decode('latin1')))
            position+=length
        require(position==end, 'container end mismatch')
    walk(0,size,'')
    return dict(atoms=atoms, tables=tables, raw_track_hints=hints,
                source_size=size, atom_count=len(atoms), source_decoded=False,
                edit_chunk_duration_header_semantics='not interpreted in this pass')

def controls():
    def atom(kind,body):return struct.pack('>I4s',8+len(body),kind)+body
    tests=[]
    def good(name,fn,check):
        result=fn();require(check(result),name+' produced wrong result')
        tests.append(dict(name=name,expected='accept with specified values',passed=True))
    def bad(name,fn):
        try:fn()
        except InvalidTable as e:
            tests.append(dict(name=name,expected='reject malformed/unsupported input',passed=True,error=str(e)))
        else:raise AssertionError(name+' was not rejected')
    good('variable sizes retain zero entry',lambda:table_stsz(b'\0'*4+struct.pack('>IIIII',0,3,10,0,12),100),lambda r:r['sample_count']==3 and r['positive_size_count']==2 and r['zero_size_entry_byte_offsets']==[116])
    good('constant sizes have no stored entries',lambda:table_stsz(b'\0'*4+struct.pack('>II',4,9)),lambda r:r['sample_count']==9 and r['stored_entry_count']==0 and r['total_declared_sample_bytes']==36)
    good('stts keeps zero delta and run counts',lambda:table_stts(b'\0'*4+struct.pack('>IIIII',2,2,3,1,0)),lambda r:r['total_samples']==3 and r['sum_sample_deltas_media_units']==6 and r['entries'][1]['sample_delta']==0)
    bad('truncated stsz header',lambda:table_stsz(b'\0'*11))
    bad('stsz overclaimed entries',lambda:table_stsz(b'\0'*4+struct.pack('>III',0,2,10)))
    bad('stsz surplus bytes',lambda:table_stsz(b'\0'*4+struct.pack('>III',4,2,10)))
    bad('unsupported stsz version',lambda:table_stsz(b'\1\0\0\0'+struct.pack('>II',4,2)))
    bad('stts overclaimed entries',lambda:table_stts(b'\0'*4+struct.pack('>III',2,3,4)))
    bad('truncated atom header',lambda:inspect(io.BytesIO(b'1234567'),7))
    bad('atom exceeds parent bounds',lambda:inspect(io.BytesIO(struct.pack('>I4s',100,b'mdat')),8))
    bad('truncated extended atom header',lambda:inspect(io.BytesIO(struct.pack('>I4s',1,b'mdat')),8))
    body=atom(b'moov',atom(b'trak',atom(b'stsz',b'\0'*4+struct.pack('>II',4,2))))
    good('nested tables preserve absolute offsets',lambda:inspect(io.BytesIO(body),len(body)),lambda r:r['tables'][0]['fields']['sample_count_byte_offset']==32)
    body=struct.pack('>I4sQ',1,b'mdat',16)
    good('valid extended atom',lambda:inspect(io.BytesIO(body),len(body)),lambda r:r['atoms'][0]['header_bytes']==16)
    body=struct.pack('>I4s',0,b'mdat')+b'abc'
    good('size-zero atom reaches parent end',lambda:inspect(io.BytesIO(body),len(body)),lambda r:r['atoms'][0]['end_exclusive']==11)
    return tests

def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    args=p.parse_args();test_results=controls()
    before=args.source.stat()
    started=datetime.now(timezone.utc).isoformat()
    sha=hashlib.sha256()
    with args.source.open('rb') as f:
        while block:=f.read(8*1024*1024):sha.update(block)
        result=inspect(f,before.st_size)
    after=args.source.stat()
    require((before.st_size,before.st_mtime_ns,before.st_ino)==(after.st_size,after.st_mtime_ns,after.st_ino),'source stat changed during read')
    result.update(started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),
                  sha256=sha.hexdigest(),source_bytes=before.st_size,
                  source_stat_unchanged=True,source_open_mode='rb',
                  parser_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  python_version=sys.version,platform=platform.platform(),controls=test_results)
    with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(sha256=result['sha256'],atom_count=result['atom_count'],
                         tables=[dict(path=t['atom']['path'],fields=t['fields']) for t in result['tables']],
                         controls_passed=len(test_results),source_stat_unchanged=True),indent=2))

if __name__=='__main__':main()
