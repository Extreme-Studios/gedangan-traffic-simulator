"""Intervention-aware guards accept only explained network/schedule differences."""
from .m07_growth import fingerprint
def guard(a,b):
 errors=[];x,y=a['m08_input'],b['m08_input']
 if a['solution_id']!='S00':errors.append('A_NOT_BASELINE_S00')
 for key in ['year','growth_scenario','seed','cohort_sha256','fixed_horizon_s','demand_window_s','warmup_s','optional_drain_s']:
  if a[key]!=b[key]:errors.append('MISMATCH_'+key)
 for key in ['projection_hash','vehicle_registry_sha256','railway_config_sha256','family']:
  if x[key]!=y[key]:errors.append('INPUT_MISMATCH_'+key)
 manifest=b['intervention_manifest'];spec=y['scenario_specification'];op=spec['operation']
 if manifest['parent_network_sha256']!=a['network_sha256']:errors.append('UNEXPLAINED_PARENT_NETWORK')
 if manifest['scenario_network_sha256']!=b['network_sha256'] or manifest['spec_hash']!=y['scenario_spec_hash']:errors.append('DERIVATIVE_MANIFEST_MISMATCH')
 if not manifest['geometry_unchanged'] or manifest['connections_added'] or manifest['connections_removed'] or not manifest['rail_crossing_connections_unchanged']:errors.append('UNAPPROVED_TOPOLOGY_OR_RAIL_CHANGE')
 if op in ['baseline','heavy_deferral','signal'] and manifest['connection_changes']:errors.append('UNEXPECTED_CONNECTION_PERMISSION_CHANGE')
 if op in ['movement_restriction','frontage_restriction']:
  if not manifest['restricted_movements'] or not manifest['connection_changes']:errors.append('MISSING_RESTRICTION_MECHANISM')
  for c in manifest['connection_changes']:
   if c['key'][:2]!=[spec['parameters']['from'],spec['parameters']['to']]:errors.append('UNDECLARED_MOVEMENT_CHANGE')
 if op!='heavy_deferral' and a['effective_schedule_sha256']!=b['effective_schedule_sha256']:errors.append('UNEXPLAINED_DEPARTURE_CHANGE')
 if a['train_departures']!=b['train_departures']:errors.append('RAIL_SCHEDULE_CHANGED')
 for r in [a,b]:
  if r['requested']!=r['failed_routes']+r['arrived']+r['running_at_end']+r['not_departed'] or r['routable']!=r['departed']+r['not_departed']:errors.append('INCOMPLETE_LIFECYCLE_LEDGER')
 return {'comparable':not errors,'errors':sorted(set(errors)),'network_hash_may_differ':True,'cohort_parity':a['cohort_sha256']==b['cohort_sha256'],'schedule_change_explicit':op=='heavy_deferral','intervention_isolation':'Validated manifest delta; no unexplained extra movement/geometry/rail changes','baseline':a['run_id'],'intervention':b['run_id']}
def compare(a,b):
 parity=guard(a,b)
 if not parity['comparable']:return {'parity':parity,'deltas':None,'status':'REJECTED_UNFAIR_COMPARISON'}
 keys=['requested','routable','failed_routes','departed','arrived','running_at_end','not_departed','unserved_total_at_horizon','max_stopped_count','max_lane_queue_extent_m','verified_in_model_spillback','crossing_delay_vehicle_seconds_contextual'];deltas={k:b[k]-a[k] for k in keys}
 od={}
 for key,aa in a['od'].items():
  bb=b['od'][key];metrics={k:bb[k]-aa[k] for k in ['requested','routable','failed_routes','departed','arrived','running','not_departed']}
  for metric in ['waiting_s_departed_including_unfinished','time_loss_s_departed_including_unfinished','depart_delay_s_accepted_including_undeparted','elapsed_trip_duration_s_departed_including_unfinished']:
   x,y=aa[metric]['mean'],bb[metric]['mean'];metrics[metric+'_delta']=None if x is None or y is None else y-x
  metrics['mean_comparison_caution']='Different completed/served cohorts and unfinished trips; means are conditional diagnostics, not complete-demand benefit estimates'
  metrics['arrived_only_travel_time_delta_s']=None if a['censored'] or b['censored'] or a['failed_routes'] or b['failed_routes'] else (bb['completed_trip_duration_s_arrived_only']['mean']-aa['completed_trip_duration_s_arrived_only']['mean'] if aa['completed_trip_duration_s_arrived_only']['mean'] is not None and bb['completed_trip_duration_s_arrived_only']['mean'] is not None else None)
  od[key]=metrics
 classes={cls:{key:b['class_lifecycle'][cls][key]-a['class_lifecycle'][cls][key] for key in a['class_lifecycle'][cls]} for cls in a['class_lifecycle']}
 return {'parity':parity,'status':'CONDITIONAL_COMPARISON_NOT_POLICY_RECOMMENDATION','baseline':a['run_id'],'intervention':b['run_id'],'solution_id':b['solution_id'],'year':b['year'],'growth':b['growth_scenario'],'seed':b['seed'],'deltas':deltas,'OD_impacts':od,'class_impacts':classes,'deferral':b['deferral'],'censoring_warning':'CENSORED / UNSERVED — arrived-only travel-time reduction is not evidence of overall improvement' if a['censored'] or b['censored'] or a['failed_routes'] or b['failed_routes'] else None,'safety_certification':False}
