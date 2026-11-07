"""Operational restrictions and executable, explicitly unverified flyover concepts."""
import copy,xml.etree.ElementTree as E,math
from .recovery_common import *
from .m04_demand import activate,xml,execute
from .m08_network import allowed
CONCEPT_ALLOW='motorcycle passenger delivery bus truck'
SCENARIOS={'S00':'Existing inherited model','S01':'Road signal timing adjustment','S02':'Existing turn restriction','S03':'Existing frontage exit restriction','S04':'Heavy vehicle departure scheduling','S05':'Corridor coordination - blocked without second verified controller','S06A':'UNVERIFIED ENGINEERING CONCEPT - one lane per direction','S06B':'UNVERIFIED ENGINEERING CONCEPT - two lanes per direction','S07':'Construction-phase lane closure/diversion'}
def validate(spec):
 sid=spec.get('id','S00')
 if sid not in SCENARIOS:raise ValueError('Unknown scenario')
 if sid=='S05':raise ValueError('BLOCKED: parent contains one modeled road controller only. No second physical signal controller invented for corridor coordination.')
 if sid.startswith('S06')and spec.get('acknowledge_concept')is not True:raise ValueError('Acknowledge UNVERIFIED ENGINEERING CONCEPT: DED alignment, clearance, structure, land and swept path unverified')
 if sid=='S01':
  if not 5<=float(spec.get('green_s',20))<=60 or not 3<=float(spec.get('yellow_s',3))<=6 or not 2<=float(spec.get('all_red_s',2))<=10:raise ValueError('Controller safety bounds violated')
 if sid=='S04'and not 0<=float(spec.get('deferral_s',600))<=3600:raise ValueError('Heavy deferral outside bounded range')
 if sid=='S07'and spec.get('stage','one_lane')not in ['one_lane','full_closure']:raise ValueError('Unknown construction stage')
 return sid
def restrict_internal(root):
 incoming={}
 for c in root.findall('connection'):
  if not c.get('from').startswith(':')and c.get('via'):incoming.setdefault(c.get('via'),set()).update(allowed(c))
 for edge in root.findall('edge'):
  if edge.get('function')!='internal':continue
  for lane in edge.findall('lane'):
   if lane.get('id')in incoming:
    admit=allowed(lane)&incoming[lane.get('id')];lane.attrib.pop('allow',None);lane.attrib.pop('disallow',None);lane.set('allow',' '.join(sorted(admit)))if admit else lane.set('disallow','all')
def build(spec):
 sid=validate(spec);key=identity({'spec':spec,'parent':sha(PARENT),'builder':sha(__file__)})[:20];folder=NETS/key;folder.mkdir(parents=True,exist_ok=True);dest=folder/'network.net.xml'
 if(folder/'manifest.json').exists():
  m=load(folder/'manifest.json');assert sha(dest)==m['network_sha256'];return folder,m
 parent=E.parse(PARENT).getroot();root=copy.deepcopy(parent);changes=[];newedges=[];scope='OPERATIONAL_DERIVATIVE'
 if sid=='S01':
  tl=next(t for t in root.findall('tlLogic')if t.get('id')=='m05_gedangan');tl.set('offset',str(float(spec.get('offset_s',0))))
  for phase in tl.findall('phase'):
   state=phase.get('state');kind='green_s'if any(s in'gG'for s in state)else'yellow_s'if'y'in state else'all_red_s';phase.set('duration',str(float(spec.get(kind,{'green_s':20,'yellow_s':3,'all_red_s':2}[kind]))))
  changes.append({'controller':'m05_gedangan','program':E.tostring(tl,encoding='unicode'),'basis':'Existing protected-link allocation retained; user-input timing is a synthetic operation assumption'})
 elif sid in ['S02','S03']:
  if sid=='S02':a,b=spec.get('from_edge','w512351908_s4_p0_0_f'),spec.get('to_edge','w320353609_s0_p0_0_f')
  else:
   from .recovery_routing import find_path
   p,_=find_path(PARENT,'w1181141358_s0_p0_0_f','w266287937_s54_p0_0_f','car')
   if not p:raise ValueError('Existing frontage exit route missing')
   meta={e['id']:e for e in load(ROOT/'simulation/network/m045/provisional/inspection.json')['edges']};pair=next(((a,b)for a,b in zip(p,p[1:])if meta[a]['road_function']=='frontage_road'and meta[b]['road_function']!='frontage_road'),None)
   if not pair:raise ValueError('No existing frontage exit transition identified; cannot invent one')
   a,b=pair
  for c in root.findall('connection'):
   if(c.get('from'),c.get('to'))==(a,b):changes.append({'from':a,'to':b,'fromLane':c.get('fromLane'),'toLane':c.get('toLane')});c.attrib.pop('allow',None);c.set('disallow','all')
  if not changes:raise ValueError('Requested restriction is not an existing source movement')
  restrict_internal(root)
 elif sid=='S07':
  eid=spec.get('closed_edge','w512351908_s3_p0_0_f');edge=next((e for e in root.findall('edge')if e.get('id')==eid),None)
  if edge is None or edge.get('function')=='internal'or eid.startswith('m05_rail_'):raise ValueError('Construction edge must be existing ordinary road')
  lanes=edge.findall('lane');indices=list(range(len(lanes)))if spec.get('stage','one_lane')=='full_closure'else[int(spec.get('lane_index',0))]
  if any(i<0 or i>=len(lanes)for i in indices):raise ValueError('Closed lane index not present')
  for i in indices:lanes[i].attrib.pop('allow',None);lanes[i].set('disallow','all');changes.append({'edge':eid,'closed_lane':lanes[i].get('id'),'stage':spec.get('stage','one_lane'),'status':'SYNTHETIC_CONSTRUCTION_STAGE_NOT_ACTUAL_WORK_NOTICE'})
  for c in root.findall('connection'):
   if c.get('from')==eid and int(c.get('fromLane'))in indices or c.get('to')==eid and int(c.get('toLane'))in indices:c.attrib.pop('allow',None);c.set('disallow','all')
  restrict_internal(root)
 elif sid.startswith('S06'):
  scope='UNVERIFIED ENGINEERING CONCEPT';newedges,changes=flyover(folder,sid,parent,spec);root=E.parse(folder/'network.net.xml').getroot()
 if not sid.startswith('S06'):xml(dest,root)
 oldids={e.get('id')for e in parent.findall('edge')if e.get('function')!='internal'};ids={e.get('id')for e in root.findall('edge')if e.get('function')!='internal'};oldcon={(c.get('from'),c.get('to'),c.get('fromLane'),c.get('toLane'))for c in parent.findall('connection')if not c.get('from').startswith(':')};newcon={(c.get('from'),c.get('to'),c.get('fromLane'),c.get('toLane'))for c in root.findall('connection')if not c.get('from').startswith(':')}
 if not sid.startswith('S06'):
  assert oldids==ids and oldcon==newcon
  for a,b in zip(parent.findall('edge'),root.findall('edge')):
   assert a.attrib==b.attrib
   for l,k in zip(a.findall('lane'),b.findall('lane')):assert {x:v for x,v in l.attrib.items()if x not in ['allow','disallow']}=={x:v for x,v in k.attrib.items()if x not in ['allow','disallow']}
 else:
  assert ids-oldids==set(newedges);assert not(oldids-ids)
  if any(a not in newedges and b not in newedges for a,b,_,_ in newcon-oldcon):raise ValueError('Unexpected new existing-to-existing movement from NETCONVERT')
  if oldcon-newcon:raise ValueError('NETCONVERT removed inherited ground movements')
 # Rail paths/controllers remain byte-identical for all concepts/operations.
 before=[E.tostring(e)for e in parent.findall('edge')if e.get('id').startswith('m05_rail_')];after=[E.tostring(e)for e in root.findall('edge')if e.get('id').startswith('m05_rail_')]
 rail_geometry_equal=[{k:v for k,v in E.fromstring(e).attrib.items()}for e in before]==[{k:v for k,v in E.fromstring(e).attrib.items()}for e in after]
 manifest={'id':sid,'name':SCENARIOS[sid],'spec':spec,'network_path':str(dest.relative_to(ROOT)),'network_sha256':sha(dest),'parent_network':str(PARENT.relative_to(ROOT)),'parent_sha256':sha(PARENT),'classification':scope,'changes':changes,'new_edges':newedges,'existing_movements_added':[list(k)for k in sorted(newcon-oldcon)if k[0]not in newedges and k[1]not in newedges],'old_movements_removed':[list(k)for k in sorted(oldcon-newcon)],'rail_edge_attributes_preserved':rail_geometry_equal,'below_structure_lane_count':'Inherited existing two per main direction, not assumed equal to deck; official six-lane below ROW proposal not a supplied final DED','legal_clearance_swept_path':'MISSING - no oversize, trailer or heavy_truck allowed on concept structure','field_legal_approved':False,'builder_sha256':sha(__file__)};save(folder/'manifest.json',manifest);return folder,manifest
def flyover(folder,sid,parent,spec):
 home=activate();prefix=folder/'parent';log=execute([home/'bin/netconvert.exe','-s',PARENT,'--plain-output-prefix',prefix,'--offset.disable-normalization','true'],folder/'plain-export.json')
 if log['returncode']:raise RuntimeError('Plain NETCONVERT export failed')
 edges=E.parse(str(prefix)+'.edg.xml').getroot();nodes=E.parse(str(prefix)+'.nod.xml').getroot();conns=E.parse(str(prefix)+'.con.xml').getroot();ns={n.get('id'):n for n in nodes};es={e.get('id'):e for e in edges};lane_count=1 if sid=='S06A'else 2;height=float(spec.get('concept_height_m',8));shift=20 if sid=='S06A'else 35
 if not 6<=height<=10:raise ValueError('Concept sensitivity height restricted6..10m; not a clearance certificate')
 # Existing same-corridor arterial nodes. No ramp connection to unrelated roads.
 pairs=[('nb','w562358500_s13_p0_0_f','w266287935_s6_p0_0_f'),('sb','w512351908_s1_p0_0_f','w562358499_s1_p0_0_f')];created=[];details=[]
 for direction,approach,exit in pairs:
  start=es[approach].get('to');end=es[exit].get('from');a=ns[start];b=ns[end];x0,y0=float(a.get('x')),float(a.get('y'));x1,y1=float(b.get('x')),float(b.get('y'));distance=math.hypot(x1-x0,y1-y0)
  if distance<height/.06*2:raise ValueError('Concept ramp length insufficient for illustrative6% bound')
  mid=[]
  for j,f in enumerate([.3,.7]):
   name=f'recovery_fo_{direction}_{j}';x=x0+(x1-x0)*f+shift;y=y0+(y1-y0)*f;E.SubElement(nodes,'node',id=name,x=str(x),y=str(y),z=str(height),type='priority');mid.append(name)
  seq=[start,*mid,end];ids=[]
  for j,(u,v)in enumerate(zip(seq,seq[1:])):
   eid=f'recovery_fo_{direction}_{j}';E.SubElement(edges,'edge',id=eid,**{'from':u,'to':v,'numLanes':str(lane_count),'speed':'13.89','priority':'10','width':'3.5','allow':CONCEPT_ALLOW});created.append(eid);ids.append(eid)
  route=[approach,*ids,exit]
  for a,b in zip(route,route[1:]):
   al=int(es[a].get('numLanes','2'))if a in es else lane_count;bl=int(es[b].get('numLanes','2'))if b in es else lane_count
   for i in range(min(al,bl)):E.SubElement(conns,'connection',**{'from':a,'to':b,'fromLane':str(i),'toLane':str(i),'allow':CONCEPT_ALLOW})
  details.append({'direction':direction,'approach':approach,'exit':exit,'entry_node':start,'exit_node':end,'entry_xy':[x0,y0],'exit_xy':[x1,y1],'deck_lanes_per_direction':lane_count,'assumed_height_m':height,'lateral_concept_offset_m':shift,'ground_links_retained':True,'no_middeck_local_access':True,'status':'UNVERIFIED ENGINEERING CONCEPT - not official DED','affected_OD':'Arterial through traffic whose legal route reaches the two interface nodes'})
 xml(folder/'concept.nod.xml',nodes);xml(folder/'concept.edg.xml',edges);xml(folder/'concept.con.xml',conns)
 args=[home/'bin/netconvert.exe','--node-files',folder/'concept.nod.xml','--edge-files',folder/'concept.edg.xml','--connection-files',folder/'concept.con.xml','--tllogic-files',str(prefix)+'.tll.xml','-o',folder/'network.net.xml','--offset.disable-normalization','true','--no-turnarounds','true','--junctions.join','false','--geometry.remove','false']
 result=execute(args,folder/'concept-build.json')
 if result['returncode']:raise RuntimeError('Flyover NETCONVERT failed; inspect retained errors')
 save(folder/'engineering-constraints.json',{'status':'UNVERIFIED ENGINEERING CONCEPT','alternatives':details,'DED':'NOT SUPPLIED','land_approval':'MISSING','height_clearance':'MISSING - selected height is sensitivity parameter only','swept_path':'MISSING','railway_design_approval':'MISSING','concept_scope':'Traffic connectivity/capacity sensitivity only; not structural/geotechnical/physical/legal feasibility'})
 return created,details
if __name__=='__main__':
 for sid in ['S00','S01','S02','S03','S04','S06A','S06B','S07']:
  try:p,m=build({'id':sid,'acknowledge_concept':True});print(sid,p.name,len(m['new_edges']),flush=True)
  except Exception as e:print(sid,'FAILED',str(e),flush=True)
