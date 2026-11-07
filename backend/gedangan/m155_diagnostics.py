"""Measured model states; insertion evidence is distinguished from inferred causes."""
from collections import defaultdict,Counter
import statistics,xml.etree.ElementTree as E
from .m155_common import *
from .m14_vehicles import registry
class Diagnostics:
 def __init__(self,rows,net,warmup=0):
  self.rows=rows;self.byid={q['id']:q for q in rows};self.net=net;self.lanes={l.getID():l for e in net.getEdges(withInternal=True)for l in e.getLanes()};self.types={v['id']:v for v in registry()};self.warmup=warmup;self.edges=defaultdict(lambda:{'vehicle_seconds':0,'speed_seconds':0,'stopped_vehicle_seconds':0,'max_count':0,'max_stopped':0,'max_queue_extent_m':0,'boundary_samples':0});self.approaches=defaultdict(lambda:{'speed_seconds':0,'vehicle_seconds':0,'stopped_vehicle_seconds':0});self.timeline=[];self.pending_samples=[];self.last_pending=[];self.latest=[]
 def sample(self,t,states,departed,arrived,pending_actual=None):
  road=[v for v in states if v['id']in self.byid];bylane=defaultdict(list);byedge=defaultdict(list);self.latest=road
  for v in road:
   bylane[v['lane']].append(v);byedge[self.lanes[v['lane']].getEdge().getID()].append(v)
   if t>self.warmup:
    a=self.approaches[self.byid[v['id']]['approach']];a['vehicle_seconds']+=.5;a['speed_seconds']+=v['speed']*.5;a['stopped_vehicle_seconds']+=.5*(v['speed']<.3)
  for eid,vs in byedge.items():
   if t<=self.warmup:continue
   e=self.edges[eid];e['vehicle_seconds']+=len(vs)*.5;e['speed_seconds']+=sum(v['speed']for v in vs)*.5;e['max_count']=max(e['max_count'],len(vs));e['stopped_vehicle_seconds']+=sum(v['speed']<.3 for v in vs)*.5
  for lane,vs in bylane.items():
   stopped=[v for v in vs if v['speed']<.3]
   if not stopped or t<=self.warmup:continue
   st=self.edges[self.lanes[lane].getEdge().getID()];tail=min(v['pos']-self.types[self.byid[v['id']]['vehicle_type_id']]['parameters']['length']for v in stopped);span=max(v['pos']for v in stopped)-tail;st['max_stopped']=max(st['max_stopped'],len(stopped));st['max_queue_extent_m']=max(st['max_queue_extent_m'],span);st['boundary_samples']+=int(tail<=2)
  if t%10!=0:return
  pending=[q for q in self.rows if q['edges']and q['depart_seconds']<t and q['id']not in departed];self.last_pending=[q['id']for q in pending]
  grouped=defaultdict(list)
  for q in pending:grouped[(q['origin_edge'],q['vehicle_type_id'],q['approach'])].append(q)
  sample=[]
  for (origin,typ,approach),qs in grouped.items():
   p=self.types[typ]['parameters'];need=p['length']+p['minGap'];cls=self.types[typ]['sumo_vclass'];gaps=[]
   for lane in self.net.getEdge(origin).getLanes():
    tail=min((v['pos']-self.types[self.byid[v['id']]['vehicle_type_id']]['parameters']['length']for v in bylane.get(lane.getID(),[])),default=lane.getLength());allowed=lane.allows(cls);gaps.append({'lane':lane.getID(),'length_m':lane.getLength(),'class_allowed':allowed,'observed_entry_free_m':round(max(0,tail),3),'nominal_required_m':need,'space_proxy_fits':allowed and tail>=need,'active_count':len(bylane.get(lane.getID(),[]))})
   reason='OBSERVED_ENTRY_SPACE_SHORTAGE'if not any(g['space_proxy_fits']for g in gaps)else'GAP_PROXY_SUFFICIENT_BUT_PENDING: downstream/route-choice/insertion safety checks unresolved'
   sample.append({'time_s':t,'origin_edge':origin,'class':typ,'approach':approach,'direction':approach,'pending':len(qs),'oldest_scheduled_s':min(q['depart_seconds']for q in qs),'oldest_delay_s':round(t-min(q['depart_seconds']for q in qs),3),'lane_evidence':gaps,'cause_classification':'INFERRED_FROM_MEASURED_MODEL_STATE','reason':reason,'id_examples':[q['id']for q in qs[:5]]})
  self.pending_samples.extend(sample);self.timeline.append({'time_s':t,'departed':len(departed),'arrived':len(arrived),'active':len(road),'stopped':sum(v['speed']<.3 for v in road),'pending_scheduled_not_departed':len(pending),'traci_pending':len(pending_actual)if pending_actual is not None else None})
 def finish(self,ledger,result,folder):
  means=lambda xs:statistics.mean(xs)if xs else None;summary=[]
  for a in sorted({q['approach']for q in ledger}):
   qs=[q for q in ledger if q['approach']==a];ds=[q for q in qs if q['departed']];arr=[q for q in qs if q['arrived']];st=self.approaches[a];delayed=[q for q in ds if float(q['tripinfo']['departDelay'])>.500001];origins=Counter(q.get('origin_edge')for q in qs if q['edges']and not q['departed']);summary.append({'approach':a,'input':len(qs),'routed':sum(bool(q['edges'])for q in qs),'scheduled_departure':sum(bool(q['edges'])and q['depart_seconds']<result.get('execution_horizon_s',result['request']['duration_s'])for q in qs),'loaded':sum(q['loaded']for q in qs),'entering':len(ds),'exiting':len(arr),'active_at_horizon':sum(q['active']for q in qs),'pending':sum(bool(q['edges'])and not q['departed']for q in qs),'failed':sum(not q['edges']for q in qs),'delayed_insertion_departed':len(delayed),'mean_insertion_delay_s_departed':means([float(q['tripinfo']['departDelay'])for q in ds]),'max_insertion_delay_s_departed':max((float(q['tripinfo']['departDelay'])for q in ds),default=0),'mean_speed_m_s_analysis':st['speed_seconds']/st['vehicle_seconds']if st['vehicle_seconds']else None,'mean_waiting_s_departed_censored':means([float(q['tripinfo']['waitingTime'])for q in ds]),'arrived_only_mean_travel_s':means([float(q['tripinfo']['duration'])for q in arr]),'analysis_vehicle_seconds':st['vehicle_seconds'],'analysis_stopped_vehicle_seconds':st['stopped_vehicle_seconds'],'pending_origins':dict(origins),'analysis_window_entering':sum(float(q['tripinfo']['depart'])>=self.warmup for q in ds),'analysis_window_exiting':sum(float(q['tripinfo']['arrival'])>=self.warmup for q in arr),'route_examples':[{'id':q['id'],'class':q['vehicle_type_id'],'turn':q['turn'],'edges':q['edges'],'origin':q.get('origin_edge'),'destination':q.get('destination_edge')}for q in qs[:1]]})
  edges=[];duration=result.get('execution_horizon_s',result['request']['duration_s'])-self.warmup
  for eid,st in self.edges.items():
   edge=self.net.getEdge(eid);storage=sum(l.getLength()for l in edge.getLanes());edges.append({'edge':eid,**st,'mean_speed_m_s':st['speed_seconds']/st['vehicle_seconds']if st['vehicle_seconds']else None,'mean_density_veh_per_lane_km':st['vehicle_seconds']/duration/storage*1000 if storage else None,'storage_lane_m':storage,'from_node':edge.getFromNode().getID(),'to_node':edge.getToNode().getID(),'definition':'Sampled in-model stopped extent/density; not calibrated capacity or field spillback'})
  edges.sort(key=lambda s:s['stopped_vehicle_seconds'],reverse=True)
  analysis={'window_start_s':self.warmup,'window_end_s':result.get('execution_horizon_s',result['request']['duration_s']),'warmup_excludes_initial_interval_only':True,'approaches':summary,'bottleneck_candidates':edges[:30],'pending_cause_counts':dict(Counter(s['reason']for s in self.pending_samples)),'insertion_cause_limit':'SUMO does not expose a complete per-vehicle insertion-rejection reason. Lane entry gap is observed; nominal length+minGap is only a proxy. Future priority/TLS, safe braking, route lane, junction occupancy may also prevent insertion. No definitive attribution without evidence.','classification':'ACTUAL_SUMO_DIAGNOSTICS / HYPOTHETICAL_INPUT'}
  save(folder/'approach-analysis.json',analysis);save(folder/'edge-diagnostics.json',edges);save(folder/'insertion-samples.json',self.pending_samples);save(folder/'demand-timeline.json',self.timeline)
  result.update(volume=load(folder/'demand.json').get('volume'),warmup_s=self.warmup,analysis=analysis,delayed_insertion_departed=sum(q['delayed_insertion_departed']for q in summary),scheduled_departure=sum(bool(q['edges'])for q in ledger),pending_traci_at_end=len(self.last_pending),insertion_diagnostic_note=analysis['insertion_cause_limit'])
  for q in ledger:
   q['scheduled_departure_s']=q['depart_seconds'];q['actual_departure_s']=float(q['tripinfo']['depart'])if q['departed']else None;q['insertion_delay_s']=float(q['tripinfo']['departDelay'])if q['departed']else result.get('execution_horizon_s',result['request']['duration_s'])-q['depart_seconds']if q['edges']else None;q['insertion_delay_censored']=bool(q['edges'])and not q['departed'];q['not_departed_at_horizon']=bool(q['edges'])and not q['departed']
