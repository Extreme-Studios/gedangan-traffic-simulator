"""Focused meeting distribution, not a 17 GB research workspace backup."""
from pathlib import Path
import json,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'presentation_demo/m11'
def main():
 files=set()
 for folder in ['frontend/dist-m10','presentation_demo/m09/cache','presentation_demo/m11/assets','presentation_demo/m11/slides','presentation_demo/m11/qa']:
  for p in (ROOT/folder).rglob('*'):
   if p.is_file()and p.suffix not in ['.webm']and not p.name.endswith('.progress.json')and p.name!='browser-performance.jsonl':files.add(p)
 for p in OUT.glob('*'):
  if p.is_file()and p.suffix in ['.md','.json','.html','.pdf','.pptx','.mp4','.png','.bat','.js']and p.name!='package-manifest.json':files.add(p)
 for name in ['START_PRESENTASI_TEKNIS_GEDANGAN.bat','backend/__init__.py','backend/gedangan/__init__.py','backend/gedangan/m10_server.py','backend/gedangan/m11_launch.py','presentation_demo/m09/M09_DEMO_MANIFEST.json','presentation_demo/m10/acceptance.json']:
  files.add(ROOT/name)
 target=OUT/'GEDANGAN_M11_PAKET_PRESENTASI.zip'
 with zipfile.ZipFile(target,'w')as z:
  for p in sorted(files):z.write(p,p.relative_to(ROOT).as_posix(),compress_type=zipfile.ZIP_STORED if p.suffix in ['.png','.gz','.pptx','.pdf','.mp4']else zipfile.ZIP_DEFLATED)
  z.writestr('MULAI_DI_SINI.txt','Ekstrak seluruh paket. Jalankan START_PRESENTASI_TEKNIS_GEDANGAN.bat pada folder utama. Memerlukan Python 3.12+ yang sudah terpasang, atau venv proyek. Tanpa Python/server, buka presentation_demo/m11/MULAI_PRESENTASI.html untuk deck, PDF dan video offline. Semua rekaman dan assets yang diperlukan tersedia lokal. Paket ini bukan backup seluruh workspace penelitian. Laporan regresi/hash berlaku pada workspace asli. M12 tidak dimulai.\n')
 with zipfile.ZipFile(target)as z:assert z.testzip()is None
 h=hashlib.sha256()
 with target.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 result={'file':target.name,'files':len(files)+1,'bytes':target.stat().st_size,'sha256':h.hexdigest(),'archive_crc':'PASS','scope':'Focused offline meeting package; unchanged M10 build and cache; no research venv, authoring dependencies, raw capture tools, or 17 GB full workspace copy'}
 (OUT/'package-manifest.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
