"""File-level source-to-recording integrity and distribution evidence."""
from pathlib import Path
import json,gzip,zipfile,os,importlib.metadata as metadata,shutil
from .m12_release import ROOT,REL,APP,DOC,digest,copy
def main():
 rows=[];catalog=json.loads((ROOT/'presentation_demo/m09/cache/catalog.json').read_text());cache=ROOT/'presentation_demo/m09/cache'
 for r in catalog['runs']:
  ip=cache/r['index'];assert digest(ip)==r['index_sha256'];i=json.loads(gzip.decompress(ip.read_bytes()));m=i['metrics'];assert m['requested']==m['routable']+m['failed_routes'];assert m['routable']==m['departed']+m['not_departed'];assert m['departed']==m['arrived']+m['running_at_end'];assert m['unserved_total_at_horizon']==m['requested']-m['arrived']
  sources=[]
  folder=ROOT/i['source_run_folder']
  for name,h in i['source_files_sha256'].items():
   p=folder/name
   if not p.is_file():p=ROOT/name
   assert p.is_file(),str(p)
   assert digest(p)==h,(r['id'],name);sources.append({'file':str(p.relative_to(ROOT)),'sha256':h,'bytes':p.stat().st_size})
  for c in i['chunks']:assert digest(cache/c['path'])==c['sha256']
  assert digest(cache/i['scene'])==i['scene_sha256']
  rows.append({'id':r['id'],'source_folder':i['source_run_folder'],'source_files':sources,'signal_events':len(i['events']),'vehicles':len(i['vehicles']),'sumo_version':i['sumo_version'],'metrics':m,'index_sha256':digest(ip),'teleports':i['teleports'],'collisions':i['collisions'],'illegal_permissions':i['illegal_permissions']})
 old={}
 for folder in ['backend','frontend/dist-m10','frontend/dist-m085']:
  for p in (ROOT/folder).rglob('*'):
   if p.is_file() and p.suffix!='.pyc' and not p.name.startswith('m12_'):
    if folder!='backend':assert digest(p)==digest(APP/p.relative_to(ROOT))
 deck=ROOT/'presentation_demo/m11/M11_PRESENTASI_TEKNIS_GEDANGAN.pptx'
 with zipfile.ZipFile(deck) as z:
  assert z.testzip() is None
  notes=[n for n in z.namelist() if n.startswith('ppt/notesSlides/notesSlide') and n.endswith('.xml')];slides=[n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')];assert len(slides)==15 and len(notes)==15
 value={'status':'PASS','runs':rows,'frontend_m10_byte_identical':True,'frontend_m085_byte_identical':True,'pptx_slides':len(slides),'pptx_notes':len(notes),'immutable_presentation_files':[{'name':p.name,'sha256':digest(p),'package_equal':digest(p)==digest(APP/'presentation_demo/m11'/p.name)} for p in (ROOT/'presentation_demo/m11').iterdir() if p.is_file() and p.suffix in ['.pptx','.pdf','.mp4']],'baseline_empirical':'BLOCKED','M085_original_status':'PARTIAL_BROWSER_ACCEPTANCE_PENDING; release adapter tested separately'}
 DOC.joinpath('SOURCE_INTEGRITY_AUDIT.json').write_text(json.dumps(value,indent=2),encoding='utf-8');print(json.dumps({'status':'PASS','run_sources_verified':len(rows),'notes':len(notes)}))
 licenses=REL/'DOCUMENTATION/LICENSES';licenses.mkdir(exist_ok=True)
 copy(Path('C:/Users/ROG ALLY/AppData/Local/Programs/Python/Python312/LICENSE.txt'),licenses/'Python-LICENSE.txt')
 versions={}
 for name in ['reportlab','pillow','jsonschema','jsonschema-specifications','referencing','rpds-py','attrs','typing-extensions','charset-normalizer','pyinstaller']:
  dist=metadata.distribution(name);versions[name]=dist.version
  for f in dist.files or []:
   if any(s in str(f).lower() for s in ['license','copying','notice']) and dist.locate_file(f).is_file():copy(dist.locate_file(f),licenses/name/str(f).replace('..','_'))
 for name in ['react','react-dom','scheduler','three']:
  p=ROOT/'frontend/node_modules'/name;versions[name]=json.loads((p/'package.json').read_text())['version']
  for f in p.glob('*'):
   if f.is_file() and any(s in f.name.lower() for s in ['license','copying','notice']):copy(f,licenses/name/f.name)
 (licenses/'THIRD_PARTY_NOTICES.md').write_text('''# Notis pihak ketiga
Python runtime dan SQLite disertakan sesuai lisensi distribusi Python. Lisensi dependency Python/frontend tersedia di subfolder. SUMO executable tidak dibundel.

Geometri diturunkan dari OpenStreetMap contributors, ODbL 1.0; attribution tetap di view 3D dan provenance network. https://www.openstreetmap.org/copyright | https://opendatacommons.org/licenses/odbl/1-0/

PyInstaller bootloader distribution exception mengizinkan distribusi aplikasi non-GPL. https://www.pyinstaller.org/en/stable/license.html
Python binary redistribution: https://www.python.org/doc/copyright/

Tidak ada font Microsoft yang disalin dari Windows. Font lokal dalam build M10 dipertahankan bersama notis asal. PPTX meminta Arial, yang perlu tersedia pada aplikasi pembaca; PDF/HTML memakai render M11 lokal.
''',encoding='utf-8');(REL/'MANIFESTS/DEPENDENCY_VERSIONS.json').write_text(json.dumps(versions,indent=2))
if __name__=='__main__':main()
