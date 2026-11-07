"""Approaches and mandatory turns come from actual SUMO connections, not invented OD."""
import xml.etree.ElementTree as E,math
from functools import lru_cache
from .m15_common import *
from .m14_vehicles import registry
from .recovery_routing import graph,context
from . import m045_access as access
DIRS={'s':'straight','l':'left','L':'left','r':'right','R':'right','t':'uturn','T':'uturn'}
def vector(e):
 pts=[[float(v)for v in p.split(',')[:2]]for p in e.find('lane').get('shape').split()];return pts[-1][0]-pts[0][0],pts[-1][1]-pts[0][1]

@lru_cache(maxsize=1)
def catalog():
 import copy
 c=copy.deepcopy(anchor_catalog());_,es,meta,cs,out,_=model()
 for a in c['approaches']:
  a['m14_movements']=copy.deepcopy(a['movements']);a['boundary_status']='MODEL ROUTE COHORT BOUNDARY, not a measured external traffic cordon'
  if a['id']in ['frontage','rail_crossing']:continue
  anchor=a['anchor_edge'];prefix=chain(anchor,True);queue=[([anchor],0)];paths=[]
  while queue:
   path,dist=queue.pop(0);eid=path[-1]
   if len(path)>1 and(float(es[eid].find('lane').get('length'))>70 or dist>200):
    if meta.get(eid,{}).get('road_function')in['main_arterial_road','feeder_road','frontage_road']:paths.append(path)
    continue
   if len(path)>=16:continue
   for to in sorted({q['to']for q in out.get(eid,[])if q.get('dir')not in ['t','T']}):
    if to not in path:queue.append((path+[to],dist+float(es[to].find('lane').get('length'))))
  moves={t:{'available':False,'candidates':[],'basis':'Existing explicit connection chain across split signal/priority junctions. Macro direction inferred from entrance/exit heading; no topology edit.'}for t in ['straight','left','right','uturn']}
  u=vector(es[anchor])
  for path in paths:
   v=vector(es[path[-1]]);angle=math.degrees(math.atan2(u[0]*v[1]-u[1]*v[0],u[0]*v[0]+u[1]*v[1]));turn='straight'if abs(angle)<=45 else'left'if 45<angle<135 else'right'if -135<angle<-45 else'uturn'
   if turn=='uturn':continue # no invented macro U-turn; direct source turn can be audited separately
   suffix=chain(path[-1],False);ids=prefix+path[1:-1]+suffix
   candidate={'connection_from':anchor,'connection_to':path[1],'prefix':prefix+path[1:-1],'suffix':suffix,'destination_edge':suffix[-1],'macro_connection_chain':path,'macro_heading_angle_deg':round(angle,2),'destination_name':meta.get(path[-1],{}).get('name'),'destination_role':meta.get(path[-1],{}).get('road_function')}
   moves[turn]['available']=True;moves[turn]['candidates'].append(candidate)
  a['movements']=moves;a['catalog_correction']='M14 stopped at signal stop-line split. M15 follows existing connections through next distributed junction nodes.'
 c['turn_limit']='Macro heading labels are INFERRED over existing SUMO connections, not field legal certification. All candidate edges/connections screened by vehicle. U-turn not inferred.';c['version']='m15-catalog-1';c['geospatial_acceptance']='PARTIAL — retained OSM aligned, no independent surveyed geometry';c['missing_coverage']=['Sedati and Jenggolo/Jenggala naming not verified in retained named roads; no fabricated approach','Six anchors are selected cohorts; western rail-crossing direction exists but is not a seventh approach in this catalog','Frontage anchor remains northern corridor, not invented central interchange']
 return c
@lru_cache(maxsize=1)
def model():
 root=E.parse(NETWORK).getroot();edges={e.get('id'):e for e in root.findall('edge')if e.get('function')!='internal'};meta={e['id']:e for e in load(ROOT/'simulation/network/m045/provisional/inspection.json')['edges']};cs=[dict(c.attrib)for c in root.findall('connection')if not c.get('from','').startswith(':')];out={};incoming={}
 for c in cs:out.setdefault(c['from'],[]).append(c);incoming.setdefault(c['to'],[]).append(c)
 return root,edges,meta,cs,out,incoming
def compatible(a,b,meta):
 x,y=meta.get(a,{}),meta.get(b,{})
 return x.get('road_function')==y.get('road_function')and(x.get('name')==y.get('name')or x.get('road_function')=='main_arterial_road')
def chain(anchor,backward=False,target_m=420):
 _,edges,meta,cs,out,inc=model();ids=[anchor];length=float(edges[anchor].find('lane').get('length'))
 for _ in range(60):
  edge=ids[0]if backward else ids[-1];choices=inc.get(edge,[])if backward else out.get(edge,[]);choices=[c for c in choices if c.get('dir')=='s'];candidates=sorted({c['from']if backward else c['to']for c in choices if compatible(anchor,c['from']if backward else c['to'],meta)})
  if not candidates or length>=target_m:break
  nxt=max(candidates,key=lambda e:float(edges[e].find('lane').get('length')))
  if nxt in ids:break
  if backward:ids.insert(0,nxt)
  else:ids.append(nxt)
  length+=float(edges[nxt].find('lane').get('length'))
 return ids
@lru_cache(maxsize=1)
def anchor_catalog():
 root,edges,meta,cs,out,_=model();anchors=sorted({c['from']for c in cs if c.get('tl')=='m05_gedangan'});front='w1181141358_s0_p0_0_f';anchors.extend([front,'w1240685448_s1_p1_0_f']);approaches=[]
 for anchor in anchors:
  points=[[float(v)for v in p.split(',')[:2]]for p in edges[anchor].find('lane').get('shape').split()];dx,dy=points[-1][0]-points[0][0],points[-1][1]-points[0][1];direction=('NB'if dy>0 else'SB')if abs(dy)>abs(dx)else('EB'if dx>0 else'WB');name=meta.get(anchor,{}).get('name')or'Koridor utama';role=meta.get(anchor,{}).get('road_function');aid='frontage'if anchor==front else'northbound'if role=='main_arterial_road'and direction=='NB'else'southbound'if role=='main_arterial_road'else'sukodono'if'Sukodono'in name else'ketajen'
  if anchor=='w1240685448_s1_p1_0_f':aid='rail_crossing'
  prefix=chain(anchor,True);turns={}
  for turn in ['straight','left','right','uturn']:
   choices=sorted({c['to']for c in out.get(anchor,[])if DIRS.get(c.get('dir'))==turn})
   turns[turn]={'available':bool(choices),'candidates':[{'connection_from':anchor,'connection_to':to,'prefix':prefix,'suffix':chain(to,False),'destination_edge':chain(to,False)[-1]}for to in choices],'basis':'Actual explicit SUMO connection dir at this anchor; no route/destination substitution'}
  approaches.append({'id':aid,'label':('Frontage'if aid=='frontage'else name)+' · '+direction,'direction':direction,'anchor_edge':anchor,'origin_edge':prefix[0],'upstream_length_m':round(sum(float(edges[e].find('lane').get('length'))for e in prefix),2),'road_function':role,'movements':turns})
 if len({a['id']for a in approaches})!=len(approaches):raise ValueError('Approach label ambiguity; audit before use')
 tl=next(t for t in root.findall('tlLogic')if t.get('id')=='m05_gedangan');phases=[{'index':i,'duration':float(p.get('duration')),'state':p.get('state')}for i,p in enumerate(tl.findall('phase'))]
 return {'network_path':str(NETWORK.relative_to(ROOT)),'network_sha256':sha(NETWORK),'existing_only':True,'flyover_edges':[],'approaches':approaches,'signal':{'controller':'m05_gedangan','classification':'ASSUMED SIGNAL PROFILE — inherited actual network program, not official field timing','phases':phases,'cycle_s':sum(p['duration']for p in phases)},'rail':{'direction_options':[{'id':'N_TO_S','label':'Utara → selatan, mapped rail route'}],'reverse_direction_status':'UNAVAILABLE: existing baseline contains one directed rail route; no reverse edge invented','classification':'EDITABLE ASSUMED SCHEDULE — NOT OFFICIAL TIMETABLE'},'slow_vehicle_status':'No baseline lane explicitly admits bicycle; becak_nonmotor/bicycle requests remain UNROUTABLE','turn_limit':'Only anchor-level movements proven in source graph are offered. Missing left/right/U-turn never manufactured; this is not a complete field turning survey.'}
@lru_cache(maxsize=128)
def route(vehicle,approach,turn):
 v=next(v for v in registry()if v['id']==vehicle);a=next((a for a in catalog()['approaches']if a['id']==approach),None)
 if not a:return {'route_status':'UNROUTABLE','reason':'UNKNOWN_APPROACH','edges':[]}
 m=a['movements'].get(turn)
 if not m or not m['available']:return {'route_status':'UNROUTABLE','reason':'MOVEMENT_NOT_IN_EXISTING_CONNECTIONS','edges':[]}
 if v['sumo_vclass']=='bicycle':return {'route_status':'UNROUTABLE','reason':'EXISTING_NETWORK_HAS_NO_BICYCLE_PERMISSION; NO_PERMISSION_BYPASS','edges':[]}
 ref=v['source_type_id'];adj,legal,reasons=graph(str(NETWORK.resolve()),sha(NETWORK),ref);net,_,meta,connections=context(str(NETWORK.resolve()),sha(NETWORK))
 for candidate in m['candidates']:
  ids=candidate['prefix']+candidate['suffix']
  if any(e not in legal for e in ids):continue
  if any(b not in adj.get(x,{})for x,b in zip(ids,ids[1:])):continue
  if vehicle=='becak_motor':
   if any(access.type_screen_impl({'origin_edge':e,'destination_edge':e,'network_variant':'provisional'},v,meta,net)for e in ids):continue
   if any(not any(l.allows(v['sumo_vclass'])and l.getWidth()>=v['parameters']['width']for l in net.getEdge(e).getLanes())for e in ids):continue
  if vehicle=='trailer':
   cs=[{'from':c.get('from'),'to':c.get('to'),'fromLane':int(c.get('fromLane')),'toLane':int(c.get('toLane')),'allowed_vclasses':['trailer']if c.get('to')in adj.get(c.get('from'),{})else[]}for values in connections.values()for c in values];reason=access.route_screen_impl(ids,{'origin_edge':ids[0],'destination_edge':ids[-1],'network_variant':'provisional'},v,meta,net,cs)
   if reason:continue
  return {'route_status':'ROUTABLE','reason':None,'origin_edge':ids[0],'destination_edge':ids[-1],'edges':ids,'mandatory_turn_from':candidate['connection_from'],'mandatory_turn_to':candidate['connection_to'],'route_length_m':sum(net.getEdge(e).getLength()for e in ids),'permission_status':'In-model class/access/dimension/conditional screens, not a field legal clearance certificate'}
 return {'route_status':'UNROUTABLE','reason':'TYPE_ACCESS_DIMENSION_CURVE_OR_CONNECTION_RESTRICTION','edges':[],'origin_edge':a['origin_edge']}
