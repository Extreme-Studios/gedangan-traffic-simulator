"""Unique pending-ID evidence percentages, not fabricated causal percentages."""
import xml.etree.ElementTree as E
from collections import Counter,defaultdict
from .m155_common import *
from .m14_vehicles import registry
from .recovery_routing import context
def pending_at_horizon(result):
 folder=RUNS/result['run_id'];ledger=load(folder/'vehicle-results.json');rows={q['id']:q for q in ledger};types={v['id']:v for v in registry()};last=[]
 for _,n in E.iterparse(folder/'fcd.xml',events=('end',)):
  if n.tag=='timestep':last=[dict(v.attrib)for v in n.findall('vehicle')];n.clear()
 by=defaultdict(list)
 for v in last:
  if v['id']in rows:by[v['lane']].append(v)
 net,*_=context(str(NETWORK.resolve()),sha(NETWORK));pending=[q for q in ledger if q['edges']and not q['departed']];out=[]
 for q in pending:
  v=types[q['vehicle_type_id']];p=v['parameters'];lanes=[]
  for l in net.getEdge(q['origin_edge']).getLanes():
   gaps=[float(x['pos'])-types[rows[x['id']]['vehicle_type_id']]['parameters']['length']for x in by[l.getID()]];free=min(gaps,default=l.getLength());lanes.append({'lane':l.getID(),'length_m':l.getLength(),'class_allowed':l.allows(v['sumo_vclass']),'observed_entry_free_m':max(0,free),'nominal_required_m':p['length']+p['minGap'],'proxy_body_gap_fits':l.allows(v['sumo_vclass'])and free>=p['length']+p['minGap'],'occupancy':len(by[l.getID()])})
  code='OBSERVED_GEOMETRIC_ENTRY_SPACE_SHORTAGE'if not any(x['proxy_body_gap_fits']for x in lanes)else'UNRESOLVED_OTHER_INSERTION_CHECK';out.append({'id':q['id'],'class':q['vehicle_type_id'],'origin_edge':q['origin_edge'],'approach':q['approach'],'scheduled_s':q['depart_seconds'],'not_entered_by_s':result.get('execution_horizon_s',result['request']['duration_s']),'evidence_class':code,'lane_evidence':lanes,'causal_status':'UNRESOLVED_FULL_CAUSAL_ATTRIBUTION; geometric obstruction observed, not an isolated cause estimate'})
 count=Counter(q['evidence_class']for q in out);total=len(out);value={'run_id':result['run_id'],'denominator_unique_pending_ids':total,'evidence_coverage':[{'category':k,'vehicles':v,'percent_of_unique_pending':100*v/total if total else 0}for k,v in count.items()],'pending_by_approach':dict(Counter(q['approach']for q in out)),'pending_on_origin_edges_under5m':sum(all(l['length_m']<5 for l in q['lane_evidence'])for q in out),'full_causal_assignment':'UNRESOLVED: percentages describe observed conditions at horizon, not proportions caused by signals/rail/geometry. Counterfactual runs supply separate effects.','ids':out};save(DOC/'rootcause'/(result['run_id']+'.json'),value);return value
def compare():
 cases={p.stem:load(p)for p in (DOC/'cases').glob('*.json')};baseline=cases['baseline-3000'];rows=[]
 for name in ['baseline-3000','discharge-3000','green30-3000','no-trains-3000']:
  r=cases[name];same=load(RUNS/r['run_id']/'demand.json')['requests']==load(RUNS/baseline['run_id']/'demand.json')['requests'];assert same
  cp=r['hour_checkpoint'];rows.append({'case':name,'run_id':r['run_id'],'same_full_request_class_route_departure_cohort':same,'cohort_sha256':r['cohort_sha256'],'network_sha256':r['network_sha256'],'demand_horizon_s':r['demand_duration_s'],'execution_horizon_s':r['execution_horizon_s'],'first_hour':cp,'end':{k:r[k]for k in ['requested','routed','departed','arrived','active','not_departed','failed_routes']},'mean_waiting_s_departed_censored':r['departed_mean_waiting_s'],'actual_clearance_time_s':r['clearance_time_s'],'clearance_time_additional_s':r['additional_discharge_s'],'discharge_time_censored':r['clearance_time_s']is None,'extra_time_tested_s':r['execution_horizon_s']-r['demand_duration_s'],'corrected_demand_window_arrivals_per_hour':cp['arrived']*3600/r['demand_duration_s'],'execution_window_arrivals_per_hour':r['arrived']*3600/r['execution_horizon_s'],'raw_legacy_throughput_key_note':'Raw inherited throughput_arrivals_per_hour divides execution-end arrivals by demand duration. For extended horizon, use explicit checkpoint and execution rate here; UI shows checkpoint rate.'});pending_at_horizon(r)
 assert rows[0]['first_hour']==rows[1]['first_hour'];value={'comparisons':rows,'paired_factors':{'discharge-3000':'Execution horizon only3600→7200; same demand/route/seed/control/event list, no new vehicles after3600','green30-3000':'Assumed green duration12→30 only; unchanged phase sequence/yellow/all-red, resulting cycle changes documented','no-trains-3000':'Train event list removed only, road cohort unchanged'},'geometry_before_after':'No proven geometry change; not fabricated as an improvement comparison','field_inference':'NONE; throughput differences are effects in the uncalibrated model only'};save(DOC/'controlled-comparisons.json',value);return value
if __name__=='__main__':print(json.dumps(compare()['paired_factors'],ensure_ascii=True),flush=True)
