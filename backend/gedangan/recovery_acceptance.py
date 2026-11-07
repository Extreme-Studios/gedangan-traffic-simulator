"""Sequential actual SUMO acceptance matrix; every failure retained, never mocked."""
import copy,traceback
from .recovery_common import *
from .recovery_engine import run,compare
from .recovery_data import build_demand,initialize,calendar
def main():
 initialize();base={'date':'2026-08-04','time':'07:00','demand_mode':'REFERENCE_ESTIMATE','acknowledge_estimate':True,'horizon_s':900,'warmup_s':300,'seed':42,'northbound_share':.5,'demand_scale':1,'turn_share':.1,'scenario':{'id':'S00'}};jobs=[('morning_base',base),('evening_base',{**base,'time':'17:00'}),('midday_reference',{**base,'time':'12:00'}),('signal_adjustment',{**base,'scenario':{'id':'S01','green_s':25}}),('turn_management',{**base,'scenario':{'id':'S02'}}),('frontage_coordination',{**base,'scenario':{'id':'S03'}}),('heavy_schedule',{**base,'scenario':{'id':'S04','deferral_s':600}}),('flyover_A',{**base,'scenario':{'id':'S06A','acknowledge_concept':True}}),('flyover_B',{**base,'scenario':{'id':'S06B','acknowledge_concept':True}}),('construction_partial',{**base,'scenario':{'id':'S07','stage':'one_lane'}}),('construction_full',{**base,'scenario':{'id':'S07','stage':'full_closure'}}),('morning_without_trains',{**base,'train_times_s':[]}),('morning_signal_off',{**base,'signal_off':True}),('offpeak_explicit_synthetic',{**base,'time':'21:00','demand_mode':'SYNTHETIC_SCENARIO','turn_share':0,'flows':[{'od_id':od,'vehicle_type_id':cls,'veh_per_hour':n}for od in ['northbound','southbound']for cls,n in [('motorcycle',200),('car',150),('bus',5),('light_truck',20)]]}),('direction_split_low',{**base,'northbound_share':.3}),('direction_split_high',{**base,'northbound_share':.7}),('volume_upper_sensitivity',{**base,'demand_scale':1.4}),('weekend_reference',{**base,'date':'2026-08-02'})]
 evidence={'status':'RUNNING','stages':['A source/network audit','B sparse evidence database','C time-aware demand','D actual SUMO','E operational changes','F conceptual executable infrastructure','G network-wide impacts','H research UI acceptance'],'jobs':[],'failures':[],'checks':[]};results={}
 for i,(name,req)in enumerate(jobs):
  save(DOC/'acceptance-progress.json',{'status':'RUNNING','total':len(jobs),'completed':evidence['jobs'],'next':name});print('START',i+1,name,flush=True)
  try:
   result=run(req);results[name]=result;evidence['jobs'].append({'name':name,'run_id':result['run_id'],'status':'PASS'if result['quality']=='NO_RECORDED_PERMISSION_COLLISION_TELEPORT_EVENTS'else'REQUIRES_REVIEW','requested':result['requested'],'routed':result['routed'],'arrived':result['arrived'],'failed_routes':result['failed_routes'],'not_departed':result['not_departed'],'running_at_end':result['running_at_end'],'flyover_assigned':result['flyover_assigned'],'actual_flyover_vehicles':result['actual_flyover_vehicles'],'warmup_active':result['warmup_state']['active_road_vehicles'],'quality':result['quality']})
  except Exception as exc:evidence['failures'].append({'name':name,'error':str(exc),'traceback':traceback.format_exc()});print('FAILED',name,str(exc),flush=True)
  save(DOC/'acceptance-results.json',evidence)
 def check(name,condition,details=None):evidence['checks'].append({'check':name,'status':'PASS'if condition else'FAIL','details':details})
 for req in [{'date':'2026-05-05','time':'16:00'},{'date':'2026-08-04','time':'21:00','demand_mode':'REFERENCE_ESTIMATE','acknowledge_estimate':True}]:
  try:build_demand(req);check('Unsupported target time rejected',False)
  except ValueError as exc:check('Unsupported target time rejected',str(exc).startswith('MISSING'),str(exc))
 try:run({**base,'scenario':{'id':'S05'}});check('No invented second corridor controller',False)
 except ValueError as exc:check('No invented second corridor controller','BLOCKED'in str(exc),str(exc))
 check('07 and17 use different input cohort and source counts','morning_base'in results and'evening_base'in results and results['morning_base']['cohort_sha256']!=results['evening_base']['cohort_sha256'])
 check('Source weekday/weekend changes real demand','morning_base'in results and'weekend_reference'in results and results['morning_base']['requested']!=results['weekend_reference']['requested'])
 for name,r in results.items():check(name+' mass balance',r['requested']==r['routed']+r['failed_routes']and r['routed']==r['departed']+r['not_departed']and r['departed']==r['arrived']+r['running_at_end']and r['not_arrived']==r['requested']-r['arrived']);check(name+' no illegal permissions or teleports',not r['illegal_permissions']and not r['teleports']);check(name+' warmup vehicles loaded',r['warmup_state']['active_road_vehicles']>0)
 if'morning_base'in results:
  a=results['morning_base']
  for name in ['signal_adjustment','turn_management','frontage_coordination','heavy_schedule','flyover_A','flyover_B','construction_partial','construction_full']:
   if name not in results:continue
   b=results[name];comparison=compare(a,b);save(DOC/'comparisons'/(name+'.json'),comparison);check(name+' equivalent cohort comparison',comparison['comparable'])
  for name in ['flyover_A','flyover_B']:check(name+' actual vehicles traversed new network',name in results and results[name]['network_sha256']!=a['network_sha256']and results[name]['actual_flyover_vehicles']>0)
  for name in ['morning_without_trains','morning_signal_off']:
   if name in results:
    b=results[name];keys=['arrived','not_departed','running_at_end','departed_including_unfinished_mean_waiting_s','max_lane_queue_extent_m'];check(name+' physically changes results',any(a.get(k)!=b.get(k)for k in keys),{k:[a.get(k),b.get(k)]for k in keys})
  if'construction_full'in results:check('Full closure changes routes or exposes unaccommodated demand',results['construction_full']['rerouted']>0 or results['construction_full']['lost_routes']>0)
 evidence['status']='PASS_WITH_DATA_AND_ENGINEERING_LIMITATIONS'if not evidence['failures']and all(c['status']=='PASS'for c in evidence['checks'])and all(j['status']=='PASS'for j in evidence['jobs'])else'PARTIAL_REQUIRES_REVIEW';evidence['summary']={'actual_runs':len(results),'observed_2026_data':'MISSING','flyover_engineering':'UNVERIFIED ENGINEERING CONCEPT','corridor_S05':'BLOCKED_SECOND_CONTROLLER_MISSING','offpeak':'Only explicit synthetic engine test; observed/reference profile missing','old_M12_release_updated':False};save(DOC/'acceptance-results.json',evidence);save(DOC/'acceptance-progress.json',{'status':evidence['status'],'completed':evidence['jobs'],'failures':evidence['failures']});print(evidence['status'],flush=True)
if __name__=='__main__':main()
