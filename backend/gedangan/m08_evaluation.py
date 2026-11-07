"""Traffic-only Pareto screening; missing cost/land never become zero."""
def evaluate(runs):
 # Compare only the same year/growth/seed; retain full request accountability.
 groups={}
 for r in runs:
  if r['seed'] not in [42,43]:continue
  key=(r['year'],r['growth_scenario'],r['seed'],r['m08_input']['family']);groups.setdefault(key,[]).append(r)
 output=[]
 for key,rows in groups.items():
  eligible=[r for r in rows if not r['collisions'] and not r['teleports'] and not r['illegal_permissions'] and not r['safety_audit']['road_on_rail'] and not r['safety_audit']['road_inside_crossing_when_all_closed_red']]
  def vector(r):return [r['unserved_total_at_horizon'],r['max_stopped_count'],r['max_lane_queue_extent_m'],r['deferral']['deferred_vehicle_seconds']]
  pareto=[r['solution_id'] for r in eligible if not any(all(x<=y for x,y in zip(vector(other),vector(r))) and any(x<y for x,y in zip(vector(other),vector(r))) for other in eligible if other['run_id']!=r['run_id'])]
  output.append({'year':key[0],'growth':key[1],'seed':key[2],'family':key[3],'traffic_only_pareto_solutions':sorted(set(pareto)),'criteria_units':['unserved vehicles, minimize','maximum sampled stopped vehicles, minimize','maximum lane queue extent m, minimize','deliberate heavy deferral vehicle-seconds, minimize'],'no_weighted_mixed_unit_score':True,'scope':'Traffic-only partial ordering under synthetic assumptions. Different metrics can trade off; not overall feasibility ranking.'})
 return {'groups':output,'overall_winner':'NO DEFENSIBLE OVERALL WINNER WITH CURRENT EVIDENCE','policy':'NO VERIFIED POLICY RECOMMENDATION — BASELINE NOT EMPIRICALLY CALIBRATED','dimensions':{k:{'evidence':'QUANTIFIED_SIMULATED' if k in ['traffic_performance','queue_spillback','model_safety_diagnostics','rail_model_interaction'] else 'QUALITATIVE_SCREENING' if k in ['implementation_screening','community_access_tradeoffs','robustness_under_tested_assumptions'] else 'UNKNOWN_REQUIRES_STUDY','value':None if k in ['land','construction_cost','maintenance_cost','environment_construction_disruption','field_safety','physical_engineering_feasibility'] else 'See per-run model metrics and feasibility evidence'} for k in ['traffic_performance','queue_spillback','model_safety_diagnostics','rail_model_interaction','implementation_screening','community_access_tradeoffs','robustness_under_tested_assumptions','land','construction_cost','maintenance_cost','environment_construction_disruption','field_safety','physical_engineering_feasibility']},'unknown_cost_is_zero':False,'unknown_land_is_zero':False,'concepts_in_traffic_ranking':False}
