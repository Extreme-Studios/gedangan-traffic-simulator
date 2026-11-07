"""Type/access/connection screened shortest paths; no synthetic diversion links."""
import heapq,xml.etree.ElementTree as E
from functools import lru_cache
from .recovery_common import *
from .m04_demand import activate,registry
from . import m045_access as access
@lru_cache(maxsize=12)
def context(path,signature):
 activate();import sumolib
 net=sumolib.net.readNet(str(path),withInternal=True);root=E.parse(path).getroot();meta={e['id']:e for e in load(ROOT/'simulation/network/m045/provisional/inspection.json')['edges']};cs={}
 for c in root.findall('connection'):
  if not c.get('from').startswith(':'):cs.setdefault(c.get('from'),[]).append(c)
 access.install_screens();return net,root,meta,cs
@lru_cache(maxsize=128)
def graph(path,signature,vehicle):
 net,root,meta,cs=context(path,signature);v=next(v for v in registry()if v['id']==vehicle);legal={};reasons={}
 for edge in net.getEdges():
  eid=edge.getID()
  if eid.startswith('recovery_fo_'):
   reason='CONCEPT_SPECIAL_VEHICLE_CLEARANCE_MISSING'if vehicle in ['heavy_truck','trailer','oversize']else None
   if reason is None and not any(l.allows(v['sumo_vclass'])and l.getWidth()>=v['parameters']['width']for l in edge.getLanes()):reason='CONCEPT_LANE_PERMISSION_DENIED'
  else:
   if eid not in meta:continue
   reason=access.type_screen_impl({'origin_edge':eid,'destination_edge':eid,'network_variant':'provisional'},v,meta,net)
   if reason is None and not meta[eid]['access_policy'][v['sumo_vclass']]['allowed']:reason='SOURCE_ACCESS_POLICY_DENIED'
   if reason is None:
    tags=meta[eid]['tags'];chain=['access','vehicle','motor_vehicle',{'motorcycle':'motorcycle','bus':'bus','truck':'hgv','trailer':'hgv'}.get(v['sumo_vclass'],'motorcar')]
    if any(tags.get(k)in ['no','private','destination','customers','delivery','permit']or k+':conditional'in tags for k in chain):reason='SOURCE_ACCESS_OR_CONDITIONAL_UNRESOLVED'
  if reason:reasons[eid]=reason
  else:legal[eid]=edge
 adjacency={}
 for a,cons in cs.items():
  if a not in legal:continue
  for c in cons:
   b=c.get('to');cls=v['sumo_vclass']
   if b not in legal or c.get('disallow')=='all'or cls in c.get('disallow','').split()or(c.get('allow')is not None and cls not in c.get('allow').split()):continue
   if not net.getEdge(a).getLane(int(c.get('fromLane'))).allows(cls)or not net.getEdge(b).getLane(int(c.get('toLane'))).allows(cls):continue
   via=c.get('via')
   if via and not net.getLane(via).allows(cls):continue
   adjacency.setdefault(a,{})[b]=max(legal[b].getLength(),.1)/max(legal[b].getSpeed(),.1)
 return adjacency,legal,reasons
def find_path(network,origin,destination,vehicle):
 path=str(Path(network).resolve());signature=sha(network);adj,legal,reasons=graph(path,signature,vehicle)
 if origin not in legal or destination not in legal:return None,{'status':'UNROUTABLE','reason':reasons.get(origin)or reasons.get(destination)or'MISSING_ENDPOINT'}
 cost={origin:legal[origin].getLength()/max(legal[origin].getSpeed(),.1)};previous={};queue=[(cost[origin],origin)]
 while queue:
  d,e=heapq.heappop(queue)
  if d!=cost[e]:continue
  if e==destination:
   route=[e]
   while e in previous:e=previous[e];route.append(e)
   route.reverse()
   # Trailer curve/conditional/source-shape screens from M04.5 remain mandatory.
   if vehicle=='trailer':
    net,root,meta,cs=context(path,signature);v=next(v for v in registry()if v['id']==vehicle);connections=[{'from':c.get('from'),'to':c.get('to'),'fromLane':int(c.get('fromLane')),'toLane':int(c.get('toLane')),'allowed_vclasses':[v['sumo_vclass']]if c.get('to')in adj.get(c.get('from'),{})else[]}for group in cs.values()for c in group];reason=access.route_screen_impl(route,{'origin_edge':origin,'destination_edge':destination,'network_variant':'provisional'},v,meta,net,connections)
    if reason:return None,{'status':'UNROUTABLE','reason':reason}
   return route,{'status':'ROUTABLE','method':'Dijkstra over explicit per-type source/access/dimension and lane-to-lane permitted graph, validated by real SUMO loading/movement','freeflow_s':d,'length_m':sum(legal[e].getLength()for e in route),'uses_flyover':any(e.startswith('recovery_fo_')for e in route)}
  for b,t in adj.get(e,{}).items():
   nd=d+t
   if nd<cost.get(b,float('inf')):cost[b]=nd;previous[b]=e;heapq.heappush(queue,(nd,b))
 return None,{'status':'UNROUTABLE','reason':'NO_CONNECTED_PERMITTED_EXISTING_OR_DECLARED_CONCEPT_PATH','not_magic_diverted':True}
def movements():
 result={m['id']:m['endpoints']['provisional']for m in load(ROOT/'simulation/demand/m04/od-matrix.fixture.json')['movements']};result['ketajen_crossing']={'origin_edge':'w1240685448_s1_p0_0_f','destination_edge':'w1240685448_s1_p2_0_f'};result['north_to_ketajen']={'origin_edge':result['northbound']['origin_edge'],'destination_edge':result['station_junction']['destination_edge']};return result
def route_all(network,qs):
 od=movements();cache={};rows=[]
 for q in qs:
  if q['od_id']not in od:raise ValueError('Unknown OD; no endpoint invented: '+q['od_id'])
  ends=od[q['od_id']];key=(q['od_id'],q['vehicle_type_id'])
  if key not in cache:cache[key]=find_path(network,ends['origin_edge'],ends['destination_edge'],q['vehicle_type_id'])
  p,info=cache[key];rows.append({**q,**ends,**info,'edges':p or[]})
 return rows
