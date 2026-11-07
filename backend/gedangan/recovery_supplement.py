"""Small explicit class/connectivity and frontage intervention fixtures."""
from .recovery_common import *
from .recovery_engine import run,compare
from .recovery_routing import movements
from .recovery_data import CLASSES
def main():
 base={'date':'2026-08-04','time':'21:00','demand_mode':'SYNTHETIC_SCENARIO','acknowledge_estimate':True,'horizon_s':900,'warmup_s':300,'seed':121,'train_times_s':[240,480],'scenario':{'id':'S00'},'flows':[{'od_id':od,'vehicle_type_id':cls,'veh_per_hour':5}for od in ['northbound','southbound','feeder_to_main','main_to_feeder','frontage_continuity','frontage_exit','station_junction','ketajen_crossing','local_trip']for cls in CLASSES]};matrix=run(base);save(DOC/'multiclass-actual-run.json',matrix)
 rows=load(RUNS/matrix['run_id']/'vehicle-results.json');compat=[]
 for od in sorted({r['od_id']for r in rows}):
  for cls in CLASSES:
   vs=[r for r in rows if r['od_id']==od and r['vehicle_type_id']==cls];compat.append({'OD':od,'class':cls,'requested':len(vs),'routed':sum(bool(v['edges'])for v in vs),'loaded':sum(v['loaded']for v in vs),'departed':sum(v['departed']for v in vs),'moved':sum(v['moved']for v in vs),'arrived':sum(v['arrived']for v in vs),'running':sum(v['running_at_end']for v in vs),'failed_reasons':sorted({v.get('reason')for v in vs if not v['edges']})})
 save(DOC/'multiclass-compatibility.json',compat)
 front={**base,'horizon_s':600,'warmup_s':120,'seed':122,'flows':[{'od_id':od,'vehicle_type_id':cls,'veh_per_hour':60}for od in ['frontage_continuity','frontage_exit']for cls in ['motorcycle','car','light_truck']]};a=run(front);b=run({**front,'scenario':{'id':'S03'}});delta=compare(a,b);save(DOC/'frontage-targeted-comparison.json',delta)
 # Restrict an actual through movement on purpose as a movement-control counterexample.
 # This is not presented as an approved field turn prohibition.
 turn={**base,'horizon_s':600,'warmup_s':120,'seed':123,'flows':[{'od_id':'southbound','vehicle_type_id':'car','veh_per_hour':120}]};c=run(turn);d=run({**turn,'scenario':{'id':'S02','from':'unused','from_edge':'w512351908_s4_p0_0_f','to_edge':'w512351908_s5_p0_0_f'}});save(DOC/'movement-targeted-comparison.json',compare(c,d))
 value={'status':'PASS'if all(not r['teleports']and not r['illegal_permissions']and not r['collisions']for r in [matrix,a,b,c,d])and(b['rerouted']or b['lost_routes'])and(d['rerouted']or d['lost_routes'])else'PARTIAL_REQUIRES_REVIEW','runs':[r['run_id']for r in [matrix,a,b,c,d]],'frontage_rerouted':b['rerouted'],'frontage_unaccommodated':b['lost_routes'],'movement_rerouted':d['rerouted'],'movement_unaccommodated':d['lost_routes'],'oversize_approved':False,'status_scope':'Synthetic technical class/connectivity fixtures, not actual night volume or field access permits'};save(DOC/'supplemental-acceptance.json',value);print(json.dumps(value),flush=True)
if __name__=='__main__':main()
