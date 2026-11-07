"""Reproducible selective payload assembly. Never modifies a previous milestone."""
import json,shutil,hashlib,zipfile,os,sys,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REL=ROOT/'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR';APP=REL/'APPLICATION';DOC=ROOT/'documentation/m12'
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def copy(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True)
 if src.is_dir():shutil.copytree(src,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 else:shutil.copy2(src,dst)
def manifest():
 files={p.relative_to(APP).as_posix():digest(p) for p in APP.rglob('*') if p.is_file() and p.name!='runtime-manifest.json'}
 (APP/'release/runtime-manifest.json').write_text(json.dumps(files,indent=2),encoding='utf-8');return files
def main():
 for d in ['APPLICATION','DEMO_DATA','PRESENTATION','REPORTS','DOCUMENTATION','SCREENSHOTS','VIDEO','QA_EVIDENCE','MANIFESTS']:(REL/d).mkdir(parents=True,exist_ok=True)
 for r in ['frontend/dist-m10','frontend/dist-m085','presentation_demo/m09/cache','presentation_demo/m09/M09_DEMO_MANIFEST.json','presentation_demo/m10/acceptance.json','configuration/calibration-m06','configuration/demand-m04/vehicle-registry.json','documentation/m06/survey-plan.json','data/templates/m06','simulation/network/m051/provisional/network.net.xml','backend/gedangan/m06_observations.py']:
  copy(ROOT/r,APP/r)
 for p in (ROOT/'presentation_demo/m11').iterdir():
  if p.is_dir() and p.name in ['slides','assets']:copy(p,APP/'presentation_demo/m11'/p.name)
  elif p.is_file() and p.suffix in ['.html','.pdf','.pptx','.md','.mp4','.js'] and p.name!='readiness.js':copy(p,APP/'presentation_demo/m11'/p.name)
 copy(ROOT/'presentation_demo/m11/M11_NUMERIC_DATA_AUDIT.json',APP/'release/audit.json')
 # Only distribution HTML is adapted: external scripts satisfy the local host CSP.
 # PPTX, PDF, video and slide images retain their original bytes.
 for name in ['M11_PRESENTASI_OFFLINE.html','MULAI_PRESENTASI.html']:
  p=APP/'presentation_demo/m11'/name;s=p.read_text(encoding='utf-8').replace('http://127.0.0.1:5186/visual.html','http://127.0.0.1:5192/visual.html')
  scripts=[]
  def external(m):
   scripts.append(m.group(1));return '<script src="'+p.stem+'.m12.js"></script>'
  s=re.sub(r'<script>(.*?)</script>',external,s,flags=re.S)
  p.write_text(s,encoding='utf-8')
  if scripts:p.with_suffix('.m12.js').write_text('\n'.join(scripts),encoding='utf-8')
 (APP/'presentation_demo/m11/readiness.js').write_text("window.M11_READINESS={status:'M12_OFFLINE_PACKAGE',message:'Paket M12. Jalankan GEDANGAN_TRAFFIC_SIMULATOR.exe untuk membuka layanan 3D. PDF, slide dan video tersedia lokal.',app_url:(location.protocol==='http:'?location.origin:'http://127.0.0.1:5192')+'/visual.html'};document.addEventListener('DOMContentLoaded',()=>{const a=document.querySelector('#open3d');if(a)a.href=window.M11_READINESS.app_url});",encoding='utf-8')
 for p in (ROOT/'frontend/m12').iterdir():copy(p,APP/'release'/p.name)
 for p in (ROOT/'presentation_demo/m11').iterdir():
  if p.is_file() and p.suffix in ['.pptx','.pdf','.md']:copy(p,REL/'PRESENTATION'/p.name)
 copy(ROOT/'presentation_demo/m11/GEDANGAN_3D_DEMO.mp4',REL/'VIDEO/GEDANGAN_3D_DEMO.mp4')
 copy(ROOT/'presentation_demo/m11/M11_SLIDE_CONTACT_SHEET.png',REL/'SCREENSHOTS/M11_SLIDE_CONTACT_SHEET.png')
 for name,args in [('START_GEDANGAN_TRAFFIC_SIMULATOR',''),('STOP_GEDANGAN_TRAFFIC_SIMULATOR','--stop'),('START_PRESENTATION','--page presentation'),('OPEN_FIELD_SURVEY','--page survey')]:
  (REL/(name+'.bat')).write_text('@echo off\r\nstart "" "%~dp0APPLICATION\\GEDANGAN_TRAFFIC_SIMULATOR.exe" '+args+'\r\n',encoding='ascii')
 files=manifest();(REL/'DEMO_DATA/README.md').write_text('23 indeks, chunks dan scene actual SUMO berada di APPLICATION/presentation_demo/m09/cache. Tidak digandakan. Catalog dan setiap indeks memiliki SHA-256.\n',encoding='utf-8')
 (REL/'MANIFESTS/RELEASE_METADATA.json').write_text(json.dumps({'product':'Gedangan Traffic Simulator','version':'1.0.0','status':'PRESENTATION-READY ILLUSTRATIVE RELEASE','release_date':None,'release_date_status':'Assigned only after final QA completion','developer':'EXTREME STUDIOS','runtime':'Frozen Windows x64 Python host; external Python/Node/SUMO not required','browser_prerequisite':'Installed current Microsoft Edge or Chrome with WebGL2; no browser engine bundled','empirical_baseline':'BLOCKED - DATA REQUIRED','infrastructure':'CONCEPT ONLY','human_acceptance':'PENDING','m01_m11_immutable':True},indent=2),encoding='utf-8')
 print(json.dumps({'payload_files':len(files),'root':str(REL)}))
if __name__=='__main__':main()
