"""Create isolated visual staging and a pre-implementation defect register."""
from .m156_common import ROOT,load,save,sha,now
import shutil

def main():
 doc=ROOT/'documentation/m1562';doc.mkdir(parents=True,exist_ok=True)
 snapshot=doc/'preservation-before.json'
 if not snapshot.exists():
  prior=load(ROOT/'documentation/m1561/preservation-before.json')
  files=[ROOT/p for p in prior]
  files+=list((ROOT/'frontend/src/m1561').rglob('*'))+list((ROOT/'frontend/dist-m1561').rglob('*'))+list((ROOT/'documentation/m1561').rglob('*'))+list((ROOT/'staging/m1561').rglob('*'))+list((ROOT/'backend/gedangan').glob('m1561_*.py'))+list(ROOT.glob('M15_6_1*.md'))
  save(snapshot,{p.relative_to(ROOT).as_posix():sha(p)for p in files if p.is_file()and '__pycache__'not in p.parts})
 defects=[('P0','SOURCE','550 invented footprints and repetitive roadside buildings','Replace population with recovered source polygons; no fictional infill'),('P0','MEMORY','3.44M/4.55M nested JS position rows retained at 3000/5000 demand','Lossless Float64 typed-array transfer with bounded chunk conversion; verify exact endpoint samples'),('P1','STATION','Station is a generic house-like mass 24m off source node','Recover actual footprint if possible; photo-reference appearance, disclose unknown heights'),('P1','GROUND','Large uniform beige ground, abrupt asphalt border','Source landuse polygons and subtle local material transitions; avoid invented drainage'),('P1','CAMERA','Frontage relationship too distant for useful vehicle detail','Separate close-up frontage/corridor/station presets; preserve positions'),('P1','ASSET','Repeated gables, floating-looking bushes and thin roof detail','Fewer detailed source-positioned assets; restrained vegetation'),('P1','EVIDENCE','Previous video only canvas, excludes full dashboard','Capture actual full application screen 45-60s with live animation'),('P2','LIFECYCLE','Recording switch can retain overlapping decode work','Abort prior request; worker conversion; disposal; bounded current frame cache')]
 save(doc/'defect-register-before.json',{'created_utc':now(),'status':'PRE_IMPLEMENTATION','evidence':['documentation/m1561/evidence/overview.jpg','documentation/m1561/evidence/railway-crossing.jpg','documentation/m1561/evidence/actual-playback.webm','M15_6_PERFORMANCE_REPORT.md'],'ranked_defects':[dict(priority=p,area=a,defect=d,action=x)for p,a,d,x in defects]})
 (doc/'DEFECT_REGISTER.md').write_text('# M15.6.2 — Ranked defects before implementation\n\n'+ '\n'.join(f'{i+1}. **{p} / {a}** — {d}. Action: {x}.'for i,(p,a,d,x)in enumerate(defects)),encoding='utf-8')
 for name in ['src']:
  target=ROOT/'frontend'/name/'m1562'
  if not target.exists():shutil.copytree(ROOT/'frontend'/name/'m1561',target)
 for suffix in ['common','server','engine','diagnostics','edge_inspection','failures']:
  text=(ROOT/f'backend/gedangan/m1561_{suffix}.py').read_text(encoding='utf-8').replace('m1561','m1562').replace('M15.6.1','M15.6.2').replace('5203','5204')
  (ROOT/f'backend/gedangan/m1562_{suffix}.py').write_text(text,encoding='utf-8')
 for old,new in [('m1561.html','m1562.html'),('vite.m1561.config.ts','vite.m1562.config.ts'),('tsconfig.m1561.json','tsconfig.m1562.json')]:
  (ROOT/'frontend'/new).write_text((ROOT/'frontend'/old).read_text(encoding='utf-8').replace('m1561','m1562').replace('M15.6.1','M15.6.2'))
 for p in (ROOT/'frontend/src/m1562').glob('*'):
  if p.is_file():p.write_text(p.read_text(encoding='utf-8').replace('m1561','m1562').replace('M15.6.1.1','M15.6.2').replace('M15.6.1','M15.6.2'),encoding='utf-8')
 print({'preserved_files':len(load(snapshot)),'defects':len(defects)})
if __name__=='__main__':main()
