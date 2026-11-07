"""Baseline, actual trajectory access/control safety and output repeat verification."""
import xml.etree.ElementTree as E,hashlib,json
from .m04_demand import ROOT,load,save,sha
from .m051_causality import analyze_trace
DOC=ROOT/'documentation/m051';RUNS=ROOT/'simulation/runs/m051'
def digest(path):
 h=hashlib.sha256()
 for _,e in E.iterparse(path,events=['end']):
  if e.tag=='timestep':h.update(json.dumps({'step':dict(e.attrib),'vehicles':sorted([dict(v.attrib) for v in e],key=lambda v:v['id'])},sort_keys=True,separators=(',',':')).encode());e.clear()
 return h.hexdigest()
def assert_baseline():
 baseline=load(DOC/'baseline-sha256.json');drift=[p for p,h in baseline.items() if sha(ROOT/p)!=h];assert not drift,drift
 return baseline,drift
def main():
 baseline,drift=assert_baseline()
 types={v['id']:v['sumo_vclass'] for v in load(ROOT/'configuration/demand-m04/vehicle-registry.json')['vehicles']};types['m05_train']='rail';audits=[];repro=[]
 for p in sorted(RUNS.glob('*/run-manifest.json')):
  folder=p.parent;r=load(folder/'result.json');net=E.parse(ROOT/r['network_path']).getroot();lanes={l.get('id'):l for e in net.findall('edge') for l in e.findall('lane')};events=[e for e in load(folder/'events.json') if e['controller']=='osm_859708050'];ei=0;state='';illegal=[];red=[];samples=0
  for _,step in E.iterparse(folder/'fcd.xml',events=['end']):
   if step.tag!='timestep':continue
   t=float(step.get('time'))+.5
   while ei<len(events) and events[ei]['time']<=t:state=events[ei]['state'];ei+=1
   for v in step.findall('vehicle'):
    samples+=1;lane=v.get('lane');l=lanes[lane];cls=types[v.get('type')]
    if (l.get('allow') is not None and cls not in l.get('allow').split()) or cls in l.get('disallow','').split():illegal.append([t,v.get('id'),lane])
    if cls!='rail' and lane.startswith(':osm_859708050_') and state and set(state)<=set('rR'):red.append([t,v.get('id'),lane])
   step.clear()
  audit={'run':folder.name,'samples':samples,'illegal_lane_samples':illegal,'road_crossing_closed_samples':red,'collisions':r['collisions'],'teleports':r['teleports']};audits.append(audit);assert not illegal and not red and not r['collisions'] and not r['teleports']
  original=ROOT/'simulation/runs/m05'/folder.name;repro.append({'run':folder.name,'demand_equal_to_m05':sha(folder/'demand.json')==sha(original/'demand.json'),'tripinfo_elements_equal_to_m05':E.tostring(E.parse(folder/'tripinfo.xml').getroot())==E.tostring(E.parse(original/'tripinfo.xml').getroot()),'fcd_elements_digest_equal_to_m05':digest(folder/'fcd.xml')==digest(original/'fcd.xml')})
  analyze_trace(folder);before=sha(folder/'causal-events.json');analyze_trace(folder);assert sha(folder/'causal-events.json')==before
 save(DOC/'safety.json',audits);save(DOC/'reproducibility.json',{'baseline_files_checked':len(baseline),'baseline_drift':drift,'network_copy_identical':sha(ROOT/'simulation/network/m051/provisional/network.net.xml')==sha(ROOT/'simulation/network/m05/provisional/network.net.xml'),'runs':repro,'causal_classification_repeated_identically':True,'FCD_digest_method':'SHA256 of canonical step attributes and all vehicle attributes sorted by ID. XML whitespace, execution headers and comments excluded; no numeric/state attributes omitted.'})
 finalize_accounting()
 print('safe samples',sum(a['samples'] for a in audits),'runs',len(audits))
def finalize_accounting():
 for p in RUNS.glob('*/run-manifest.json'):
  folder=p.parent;r=load(folder/'result.json');steps=E.parse(folder/'summary.xml').getroot().findall('step');r['loaded']=int(steps[-1].get('loaded'));r['not_departed']=r['requested_road']+r['requested_train']-r['departed'];r['loaded_source']='SUMO final summary loaded counter, not an event-set missing initial preloaded vehicles';assert r['loaded']==r['requested_road']+r['requested_train'];assert r['requested_road']+r['requested_train']==r['arrived']+len(r['running'])+r['not_departed'];save(folder/'result.json',r)
  if (folder/'playback.json').exists():
   playback=load(folder/'playback.json');playback['result']=r;save(folder/'playback.json',playback)
if __name__=='__main__':main()
