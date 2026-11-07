"""Lossless renderer transport derived from immutable SUMO playback JSON."""
from .simple_common import *
import gzip,struct,array,sys

def build(run_id):
 assert len(run_id)==24 and all(c in '0123456789abcdef'for c in run_id)
 source=RUNS/run_id
 if not source.is_dir():source=PARENT_RUNS/run_id
 index=load(source/'playback-index.json');out=DATA/'recordings'/run_id;out.mkdir(parents=True,exist_ok=True)
 frames=[];total=0;chunks=[];inputs={};peaks={};types=[v['type']for v in index['vehicles']]
 for name in index['chunks']:
  p=source/name;inputs[name]=sha(p);target=out/(name+'.f64.gz')
  with gzip.open(p,'rt',encoding='utf-8')as handle:rows=json.load(handle)
  packed=array.array('d');local=[];offset=0
  for frame in rows:
   local.append([frame['t'],offset,len(frame['p'])]);counts={}
   for pose in frame['p']:
    assert len(pose)==6;packed.extend(pose);counts[types[pose[0]]]=counts.get(types[pose[0]],0)+1
   for kind,count in counts.items():peaks[kind]=max(peaks.get(kind,0),count)
   offset+=len(frame['p'])*6;total+=len(frame['p'])
  if sys.byteorder!='little':packed.byteswap()
  if not target.exists():
   with gzip.open(target,'wb',compresslevel=4)as handle:handle.write(packed.tobytes())
  chunks.append({'file':target.name,'frames':local,'positions':offset//6,'byte_length':len(packed)*8,'sha256':sha(target)})
  frames.extend(f['t']for f in rows)
 save(out/'index.json',{**index,'chunks':chunks,'transport':'Float64 little-endian, all six original fields; no quantization, sample reduction or vehicle removal','positions':total,'frame_count':len(frames),'max_active_by_type':peaks,'source_index_sha256':sha(source/'playback-index.json'),'source_chunk_sha256':inputs,'typed_bytes':total*48})
 return out

def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('run_id',nargs='*',default=['cc419452a995456df324fd05','569df9741bf6f16d1cffa31e']);args=p.parse_args()
 for key in args.run_id:
  out=build(key);i=load(out/'index.json');print({'id':key,'frames':i['frame_count'],'positions':i['positions'],'typed_bytes':i['typed_bytes']},flush=True)
if __name__=='__main__':main()
