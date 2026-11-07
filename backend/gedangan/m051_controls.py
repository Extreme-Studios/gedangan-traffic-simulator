"""Actual SUMO positive and negative controls, immutable original fixture."""
import importlib.util,xml.etree.ElementTree as E
from .m04_demand import ROOT,activate,save
from .m051_causality import Trace,analyze_trace

def main():
 activate();import traci
 for name in ['positive_storage','negative_free','negative_signal']:
  folder=ROOT/'simulation/runs/m051'/name
  spec=importlib.util.spec_from_file_location('backend.gedangan.m051_private_fixture',ROOT/'backend/gedangan/m05_spillback_fixture.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.DIR=folder
  original_get=traci.getConnection;original_start=traci.start;proxies={}
  def start(args,*a,**kw):
   if name!='positive_storage':
    path=folder/'network.net.xml';root=E.parse(path).getroot()
    for tl in root.findall('tlLogic'):
     for child in list(tl):tl.remove(child)
     phases=[(90,'r'),(300,'G'),(3,'y'),(2,'r')] if name=='negative_signal' and tl.get('id')=='b' else [(1000,'G')]
     for dur,state in phases:E.SubElement(tl,'phase',duration=str(dur),state=state)
    E.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
   return original_start(args+['--seed','42'],*a,**kw)
  def get(label=None):
   c=original_get(label) if label is not None else original_get()
   if c not in proxies:proxies[c]=Trace(c,folder/'network.net.xml')
   return proxies[c]
  traci.getConnection=get;traci.start=start
  try:
   # Original fixture asserts positive detection; negative controls intentionally reject it.
   try:m.main()
   except AssertionError:
    if name=='positive_storage':raise
  finally:traci.getConnection=original_get;traci.start=original_start
  save(folder/'priority-trace.json',next(iter(proxies.values())).frames);events=analyze_trace(folder);print(name,len(events),sum(e['cause']=='VERIFIED_SPILLBACK' for e in events),flush=True)
if __name__=='__main__':main()
