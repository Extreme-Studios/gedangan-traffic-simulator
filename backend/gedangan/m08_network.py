"""NETCONVERT derivatives with exact geometry/topology and narrowing-only access audits."""
import shutil,copy,xml.etree.ElementTree as E
from collections import Counter
from .m04_demand import ROOT,load,save,sha,xml,execute,activate
from .m07_growth import fingerprint
from .m07_runner import NETWORKS
from .m08_scenarios import validate
OUT=ROOT/'simulation/network/m08'
CLASSES=['motorcycle','passenger','delivery','bus','truck','trailer','rail']
def allowed(element):
 return {c for c in CLASSES if (element.get('allow') is None or c in element.get('allow').split()) and element.get('disallow')!='all' and c not in element.get('disallow','').split()}
def geometry(root):
 return {'location':dict(root.find('location').attrib),'lanes':{l.get('id'):{k:v for k,v in l.attrib.items() if k not in ['allow','disallow']} for e in root.findall('edge') for l in e.findall('lane')},'junctions':{j.get('id'):dict(j.attrib) for j in root.findall('junction')},'edges':{e.get('id'):{k:v for k,v in e.attrib.items()} for e in root.findall('edge')}}
def links(root):return {(c.get('from'),c.get('to'),c.get('fromLane'),c.get('toLane')):c for c in root.findall('connection')}
def signal_safe(root):
 audits=[]
 for tl in root.findall('tlLogic'):
  if tl.get('id')!='m05_gedangan':continue
  phases=tl.findall('phase')
  if any(sum(c in 'gG' for c in p.get('state'))>1 for p in phases):raise ValueError('Conflicting/multiple protected links not admitted')
  if len(phases)%3:raise ValueError('Signal clearance sequence missing')
  for i in range(0,len(phases),3):
   green,yellow,red=phases[i:i+3]
   if float(yellow.get('duration'))<3 or float(red.get('duration'))<2 or set(red.get('state'))!={'r'} or sum(c=='y' for c in yellow.get('state'))!=1:raise ValueError('Signal yellow/all-red clearance violated')
  audits.append({'controller':tl.get('id'),'phase_count':len(phases),'cycle_s':sum(float(p.get('duration')) for p in phases),'one_protected_link':True,'synthetic_not_field_timing':True})
 return audits
def build(spec,family='pilot-provisional'):
 validate(spec)
 if spec['status'] not in ['SIMULATION_READY_PROVISIONAL','SIMULATED']:raise ValueError('Scenario not executable: '+spec['status'])
 if family not in NETWORKS:raise ValueError('Unknown parent network')
 parent=NETWORKS[family];key=fingerprint({'spec':spec,'parent':sha(parent),'builder':sha(__file__)})[:20];folder=OUT/key;folder.mkdir(parents=True,exist_ok=True);dest=folder/'network.net.xml'
 if (parent.parent/'rail-provenance.json').exists():shutil.copy2(parent.parent/'rail-provenance.json',folder/'rail-provenance.json')
 if (folder/'manifest.json').exists():
  m=load(folder/'manifest.json')
  if sha(dest)!=m['scenario_network_sha256']:raise ValueError('Derivative hash drift')
  return folder,m
 home=activate();before=E.parse(parent).getroot();op=spec['operation'];changed=[]
 if op in ['baseline','heavy_deferral']:shutil.copy2(parent,dest)
 else:
  command=[home/'bin/netconvert.exe','-s',parent,'-o',dest,'--offset.disable-normalization','true','--geometry.remove','false','--junctions.join','false','--no-turnarounds','true']
  if op=='signal':
   tl=next((t for t in before.findall('tlLogic') if t.get('id')=='m05_gedangan'),None)
   if tl is None:raise ValueError('Parent has no valid road controller')
   patch=E.Element('additional');new=E.SubElement(patch,'tlLogic',**tl.attrib);new.set('offset',str(spec['parameters']['offset']))
   for phase in tl.findall('phase'):
    state=phase.get('state');keyname='green' if any(c in 'gG' for c in state) else 'yellow' if 'y' in state else 'all_red';E.SubElement(new,'phase',duration=str(spec['parameters'][keyname]),state=state)
   xml(folder/'signal.add.xml',patch);command+=['--tllogic-files',folder/'signal.add.xml']
  elif op in ['movement_restriction','frontage_restriction']:
   params=spec['parameters'];conns=[c for c in before.findall('connection') if c.get('from')==params['from'] and c.get('to')==params['to']]
   if not conns:raise ValueError('Existing source movement unavailable in selected parent')
   patch=E.Element('connections')
   for c in conns:E.SubElement(patch,'connection',**{k:c.get(k) for k in ['from','to','fromLane','toLane']},disallow='all');changed.append({k:c.get(k) for k in ['from','to','fromLane','toLane']})
   xml(folder/'restrictions.con.xml',patch);command+=['--connection-files',folder/'restrictions.con.xml']
  else:raise ValueError('No executable infrastructure/coordination network')
  log=execute(command,folder/'netconvert-process.json')
  if log['returncode']:raise RuntimeError('NETCONVERT derivative failed; log retained')
 # NETCONVERT may rebuild internal junctions even for operational patches.
 # Retain that intermediate verbatim, then apply only the declared semantic delta
 # to the parent XML. Do not import regenerated geometry or extra movements.
 intermediate=E.parse(dest).getroot()
 if op not in ['baseline','heavy_deferral']:
  shutil.copy2(dest,folder/'netconvert-intermediate.net.xml')
  final=copy.deepcopy(before)
  if op=='signal':
   target=next(t for t in final.findall('tlLogic') if t.get('id')=='m05_gedangan');candidate=next(t for t in intermediate.findall('tlLogic') if t.get('id')=='m05_gedangan')
   if [p.get('state') for p in target.findall('phase')]!=[p.get('state') for p in candidate.findall('phase')]:raise ValueError('NETCONVERT changed phase allocation unexpectedly')
   target.set('offset',candidate.get('offset','0'))
   for a,b in zip(target.findall('phase'),candidate.findall('phase')):a.set('duration',b.get('duration'))
  else:
   for c in final.findall('connection'):
    if c.get('from')==spec['parameters']['from'] and c.get('to')==spec['parameters']['to']:
     c.attrib.pop('allow',None);c.set('disallow','all')
   # Narrow internal lanes to the union of admitted incoming external movements.
   via={}
   for c in final.findall('connection'):
    if not c.get('from').startswith(':') and c.get('via'):via.setdefault(c.get('via'),set()).update(allowed(c))
   for edge in final.findall('edge'):
    if edge.get('function')!='internal':continue
    for lane in edge.findall('lane'):
     if lane.get('id') in via:
      admitted=allowed(lane)&via[lane.get('id')];lane.attrib.pop('allow',None);lane.attrib.pop('disallow',None)
      if admitted:lane.set('allow',' '.join(sorted(admitted)))
      else:lane.set('disallow','all')
  save(folder/'netconvert-intermediate-audit.json',{'geometry_sections_changed':[k for k in geometry(before) if geometry(before)[k]!=geometry(intermediate)[k]],'used_as_final_network':False,'method':'Declared timing/permission semantics applied to original geometry; runtime SUMO parser/routing/safety tests validate final. No generated geometry or new connector imported.'})
  xml(dest,final)
 after=E.parse(dest).getroot();old,new=links(before),links(after);g0,g1=geometry(before),geometry(after)
 if g0!=g1:save(folder/'geometry-drift.json',{'changed_sections':[k for k in g0 if g0[k]!=g1[k]]});raise ValueError('Operational derivative changed geometry/junction/edge identity')
 if set(old)!=set(new):raise ValueError('Operational derivative added/deleted a connection')
 diffs=[]
 for k,c in new.items():
  if allowed(c)-allowed(old[k]):raise ValueError('Expanded movement permission')
  if dict(c.attrib)!=dict(old[k].attrib):diffs.append({'key':list(k),'before':dict(old[k].attrib),'after':dict(c.attrib)})
 rail_before={k:dict(c.attrib) for k,c in old.items() if c.get('tl')=='osm_859708050' or k[0].startswith('m05_rail_') or k[1].startswith('m05_rail_')}
 if any(dict(new[k].attrib)!=v for k,v in rail_before.items()):raise ValueError('Rail/crossing movement changed')
 for e in after.findall('edge'):
  for lane in e.findall('lane'):
   cls=allowed(lane)
   if e.get('id').startswith('m05_rail_') and cls-{'rail'}:raise ValueError('Road access to rail edge')
 signal=signal_safe(after);manifest={'scenario_id':spec['id'],'version':spec['version'],'spec_hash':fingerprint(spec),'specification':spec,'family':family,'parent_network':str(parent.relative_to(ROOT)),'parent_network_sha256':sha(parent),'scenario_network_sha256':sha(dest),'network_path':str(dest.relative_to(ROOT)),'builder_sha256':sha(__file__),'intervention_type':op,'parameters':spec['parameters'],'geometry_unchanged':True,'edge_ids_unchanged':True,'connections_added':[],'connections_removed':[],'connection_changes':diffs,'restricted_movements':changed,'rail_crossing_connections_unchanged':True,'signal_audit':signal,'source_lineage':'Unchanged existing edge/node IDs, M04.5 source inspection and M051 parent. No source OSM mutation.','component_note':'Topology/geometry unchanged; permission-weighted reachability tested by actual DUAROUTER ledger','vehicle_permissions':'No expansion; existing lane access unchanged, connection policy may narrow','validation_status':'SIMULATION_READY_PROVISIONAL — NOT FIELD VERIFIED'}
 save(folder/'manifest.json',manifest);return folder,manifest
if __name__=='__main__':
 from .m08_scenarios import initialize,read
 initialize()
 for sid in ['S00','S01','S02','S03','S04']:
  folder,m=build(read(sid));print(sid,folder.name,'connection changes',len(m['connection_changes']),flush=True)
