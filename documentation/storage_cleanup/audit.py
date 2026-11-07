"""Read-only inventory with hashes; does not follow reparse directories."""
import os,json,hashlib,time
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'documentation/storage_cleanup'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 files=[];links=[];errors=[];start=time.time()
 for parent,dirs,names in os.walk(ROOT,followlinks=False):
  keep=[]
  for d in dirs:
   p=Path(parent)/d
   if p.is_symlink()or p.is_junction():links.append({'path':p.relative_to(ROOT).as_posix(),'target':str(p.resolve()),'traversed':False})
   else:keep.append(d)
  dirs[:]=keep
  for n in names:
   p=Path(parent)/n;r=p.relative_to(ROOT).as_posix()
   if r.startswith('documentation/storage_cleanup/'):continue
   try:s=p.stat();files.append({'path':r,'bytes':s.st_size,'sha256':sha(p),'mtime_ns':s.st_mtime_ns})
   except Exception as e:errors.append({'path':r,'error':str(e)})
 folder=defaultdict(lambda:[0,0]);groups=defaultdict(list)
 for f in files:
  groups[(f['sha256'],f['bytes'])].append(f['path'])
  for p in Path(f['path']).parents:
   if str(p)!='.':folder[p.as_posix()][0]+=f['bytes'];folder[p.as_posix()][1]+=1
 duplicates=[{'sha256':h,'bytes_each':s,'copies':len(ps),'redundant_bytes_upper_bound':s*(len(ps)-1),'paths':ps}for(h,s),ps in groups.items()if len(ps)>1 and s>0];duplicates.sort(key=lambda x:x['redundant_bytes_upper_bound'],reverse=True)
 data={'scope':'Logical file sizes, no junction traversal; audit-generated files excluded; not allocated disk clusters','files':files,'bytes':sum(f['bytes']for f in files),'file_count':len(files),'folders':[{'path':p,'bytes':v[0],'files':v[1]}for p,v in sorted(folder.items(),key=lambda x:x[1][0],reverse=True)],'duplicate_groups':duplicates,'duplicate_redundant_upper_bound_bytes':sum(g['redundant_bytes_upper_bound']for g in duplicates),'junctions':links,'errors':errors,'elapsed_s':round(time.time()-start,2)}
 (ROOT/'STORAGE_INVENTORY_BEFORE.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
 lines=['# STORAGE AUDIT BEFORE','',f"Logical bytes: {data['bytes']:,} | GiB: {data['bytes']/2**30:.3f} | Files: {len(files):,}",'','Ukuran logis filesystem; junction tidak ditelusuri. Folder bertingkat saling mencakup; persentase tidak boleh dijumlahkan. Duplikat hash bukan otomatis aman dihapus.','', '| Folder terbesar | Bytes | GiB | % proyek |','|---|---:|---:|---:|']
 lines += [f"| {f['path']} | {f['bytes']:,} | {f['bytes']/2**30:.3f} | {100*f['bytes']/data['bytes']:.2f}% |"for f in data['folders'][:20]]
 lines+=['','## 100 berkas terbesar','| Path | Bytes |','|---|---:|']+[f"| {f['path']} | {f['bytes']:,} |"for f in sorted(files,key=lambda f:f['bytes'],reverse=True)[:100]]
 lines+=['',f"Duplikasi SHA256 (batas atas redundansi, termasuk salinan runtime wajib): {data['duplicate_redundant_upper_bound_bytes']:,} bytes.",f"Junction dilewati: {len(links)}; error: {len(errors)}."]
 (ROOT/'STORAGE_AUDIT_BEFORE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print(json.dumps({k:data[k]for k in ['bytes','file_count','elapsed_s','errors']}),flush=True)
 for f in data['folders'][:30]:print(json.dumps(f),flush=True)
if __name__=='__main__':main()
