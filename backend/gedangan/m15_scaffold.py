"""One-time additive migration. Never rewrites parent files."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 base=ROOT/'backend/gedangan'
 for name in ['network','demand','engine','server']:
  dest=base/f'm15_{name}.py'
  if not dest.exists():
   s=(base/f'm14_{name}.py').read_text(encoding='utf-8').replace('m14_common','m15_common').replace('m14_network','m15_network').replace('m14_demand','m15_demand').replace('m14_engine','m15_engine').replace("'m14_","'m15_").replace('M14','M15').replace('m14-','m15-').replace('dist-m14','dist-m15').replace('5199','5200').replace('manual.html','validation.html')
   if name=='network':s=s.replace('def catalog():','def anchor_catalog():')
   dest.write_text(s,encoding='utf-8')
 dst=ROOT/'frontend/src/m15';dst.mkdir(parents=True,exist_ok=True)
 for name in ['main.tsx','core.ts','world.tsx','style.css']:
  p=dst/name
  if not p.exists():p.write_text((ROOT/'frontend/src/m14'/name).read_text(encoding='utf-8').replace('M14','M15'),encoding='utf-8')
 for a,b in [('manual.html','validation.html'),('vite.manual.config.ts','vite.validation.config.ts'),('tsconfig.m14.json','tsconfig.m15.json')]:
  p=ROOT/'frontend'/b
  if not p.exists():p.write_text((ROOT/'frontend'/a).read_text(encoding='utf-8').replace('src/m14','src/m15').replace('M14','M15').replace('dist-m14','dist-m15').replace('manual.html','validation.html').replace('src/m14','src/m15').replace('vite.manual.config','vite.validation.config'),encoding='utf-8')
if __name__=='__main__':main()
