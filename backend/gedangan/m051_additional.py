"""Complete inherited candidate coverage: train schedules, block control and Strict."""
import importlib.util,shutil
from .m04_demand import ROOT,load,save,sha,activate
from .m051_causality import Trace,analyze_trace,RUNS,NET,DOC

def main():
 home=activate();import traci
 mode=NET/'provisional-block-control';mode.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'simulation/network/m05/provisional-block-control/network.net.xml',mode/'network.net.xml')
 spec=importlib.util.spec_from_file_location('backend.gedangan.m051_private_extra',ROOT/'backend/gedangan/m05_behavior.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.NET=NET;m.RUNS=RUNS;m.DOC=DOC
 jobs=[]
 for seed in [42,43]:
  for name,trains,delay in [('D_two',(70,170),3),('D_consecutive',(70,85),3),('D_long',(70,),20)]:jobs.append((f'{name}_seed{seed}',{'n':90,'seed':seed,'signals':False,'trains':trains,'opening_delay':delay},NET/'provisional/network.net.xml'))
 jobs += [('H_close_block_control',{'n':90,'signals':False,'trains':(70,85),'opening_delay':10,'network_override':mode/'network.net.xml'},mode/'network.net.xml'),('strict_signal_seed42',{'mode':'strict','n':60},NET/'strict/network.net.xml')]
 for label,kwargs,network in jobs:
  original=traci.getConnection;proxy={}
  def get(label=None):
   c=original(label) if label is not None else original()
   if c not in proxy:proxy[c]=Trace(c,network)
   return proxy[c]
  traci.getConnection=get
  try:m.run(home,label,**kwargs)
  finally:traci.getConnection=original
  folder=RUNS/label;save(folder/'priority-trace.json',next(iter(proxy.values())).frames)
  save(folder/'run-manifest.json',{'SUMO':'1.28.0','seed':kwargs.get('seed',42),'network_sha256':sha(network),'demand_sha256':sha(folder/'demand.json'),'matches_m05_demand':sha(folder/'demand.json')==sha(ROOT/'simulation/runs/m05'/label/'demand.json'),'baseline_run':f'simulation/runs/m05/{label}','no_speed_or_position_override':True,'mode':kwargs.get('mode','provisional')})
  analyze_trace(folder)
 # Exact duplicate configurations are linked as aliases only after verifying original M05 physics/demand equality.
 import xml.etree.ElementTree as E
 for alias,source in [('G_e2_instrumented','E_combined_seed42'),('I_repro_single_seed42','C_single_seed42')]:
  a=ROOT/'simulation/runs/m05'/alias;b=ROOT/'simulation/runs/m05'/source
  assert sha(a/'demand.json')==sha(b/'demand.json') and E.tostring(E.parse(a/'tripinfo.xml').getroot())==E.tostring(E.parse(b/'tripinfo.xml').getroot())
  target=RUNS/alias;target.mkdir(exist_ok=True)
  for name in ['priority-trace.json','fcd.xml','tripinfo.xml','summary.xml','demand.json','events.json','result.json'] :shutil.copy2(RUNS/source/name,target/name)
  r=load(target/'result.json');r['name']=alias;save(target/'result.json',r)
  save(target/'run-manifest.json',{'SUMO':'1.28.0','seed':42,'network_sha256':r['network_sha256'],'demand_sha256':sha(target/'demand.json'),'matches_m05_demand':True,'trace_equivalent_to':source,'equivalence_basis':'Byte-identical original demand and exact original tripinfo attributes; complete FCD attribute parity independently verified by m051_verify. This is an evidence alias, not an additional SUMO execution.'})
  analyze_trace(target)
if __name__=='__main__':main()
