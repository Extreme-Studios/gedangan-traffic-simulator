"""Independent full-FCD checks and bounded robustness extensions, all under M08."""
import xml.etree.ElementTree as E
from collections import Counter
from .m04_demand import ROOT,load,save,sha,registry
from .m08_reporting import RUNS,DOC,results
def audit(folder):
 result=load(folder/'m08-result.json');network=ROOT/result['network_path'];inputs={'fcd':sha(folder/'fcd.xml'),'network':sha(network),'result':sha(folder/'m08-result.json'),'registry':sha(ROOT/'configuration/demand-m04/vehicle-registry.json')}
 if (folder/'full-FCD-audit.json').exists():
  old=load(folder/'full-FCD-audit.json')
  if old.get('input_sha256')==inputs:return old
 root=E.parse(network).getroot();lanes={l.get('id'):l for e in root.findall('edge') for l in e.findall('lane')};vclass={v['id']:v['sumo_vclass'] for v in registry()};vclass['m05_train']='rail';illegal=[];samples=0;movements=Counter();prev={};speedmax=0
 for _,step in E.iterparse(folder/'fcd.xml',events=['end']):
  if step.tag!='timestep':continue
  for v in step:
   samples+=1;lane=v.get('lane');cls=vclass[v.get('type')];element=lanes[lane];allow=element.get('allow');deny=element.get('disallow','').split()
   if (allow is not None and cls not in allow.split()) or cls in deny or 'all' in deny:illegal.append({'time':step.get('time'),'id':v.get('id'),'lane':lane,'class':cls})
   if v.get('id') in prev and prev[v.get('id')]!=lane:movements[v.get('type')]+=1
   prev[v.get('id')]=lane;speedmax=max(speedmax,float(v.get('speed')))
  step.clear()
 value={'input_sha256':inputs,'full_FCD_samples_checked':samples,'resolution_s':.5,'illegal_permission_samples':illegal,'actual_lane_transitions_per_type':dict(movements),'max_speed_m_s':speedmax,'physical_legality_or_safety_certified':False,'no_ignoring_class':all(v!='ignoring' for v in vclass.values())};save(folder/'full-FCD-audit.json',value)
 if illegal:raise ValueError('Illegal lane permission in full FCD')
 return value
def all_audits():
 rr=results();values=[audit(RUNS/r['run_id']) for r in rr];save(DOC/'full-FCD-audits.json',values);print('Full-FCD permission audits:',len(values),'runs',sum(v['full_FCD_samples_checked'] for v in values),'samples',flush=True)
 from .m08_topology_audit import main
 main()
def robustness():
 from .m08_toolchain import verify
 verify()
 from .m08_runner import run
 choice=load(DOC/'signal-training.json')['selected'];jobs=[{'solution':s,'year':2040,'growth':g,'seed':42,'family':'pilot-provisional'} for g in ['LOW','HIGH'] for s in ['S00','S01']]+[{'solution':s,'year':2026,'growth':'REFERENCE','seed':42,'family':'pilot-strict'} for s in ['S00','S01']];done=[]
 for j in jobs:
  save(DOC/'robustness-queue.json',{'status':'RUNNING','concurrency':1,'completed':done,'next':j,'total':len(jobs)});r=run(j['solution'],j['year'],j['growth'],j['seed'],j['family'],specification=choice if j['solution']=='S01' else None);done.append({**j,'run_id':r['run_id']})
 save(DOC/'robustness-queue.json',{'status':'COMPLETE','concurrency':1,'completed':done,'total':len(jobs)})
if __name__=='__main__':
 import sys
 robustness() if '--robustness' in sys.argv else all_audits()
