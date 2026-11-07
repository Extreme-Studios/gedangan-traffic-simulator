"""Additive migration; never changes an earlier milestone's source/build."""
from .m155_common import *
def main():
 freeze()
 for name in ['engine','diagnostics','server','evidence','failures']:
  src=ROOT/f'backend/gedangan/m15_{name}.py';dst=ROOT/f'backend/gedangan/m155_{name}.py'
  if dst.exists():continue
  s=src.read_text(encoding='utf-8')
  for a,b in [('m15_common','m155_common'),('m15_demand','m155_demand'),('m15_network','m155_network'),('m15_engine','m155_engine'),('m15_diagnostics','m155_diagnostics'),('m15_failures','m155_failures'),('dist-m15','dist-m155'),("'m15.html'","'m155.html'"),('5200','5201'),("version':'m15-1'","version':'m155-1'"),('M15 ','M15.5 ')]:s=s.replace(a,b)
  dst.write_text(s,encoding='utf-8')
 dst=ROOT/'frontend/src/m155';dst.mkdir(parents=True,exist_ok=True)
 for name in ['main.tsx','Inspection.tsx','style.css','core.ts','world.tsx']:
  p=dst/name
  if not p.exists():p.write_text((ROOT/'frontend/src/m15'/name).read_text(encoding='utf-8').replace('M15 ·','M15.5 ·').replace('documentation/m15/','documentation/m155/'),encoding='utf-8')
