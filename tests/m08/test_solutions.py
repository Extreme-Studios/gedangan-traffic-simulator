import unittest,copy,xml.etree.ElementTree as E
from pathlib import Path
from backend.gedangan.m04_demand import ROOT,load,sha,registry
from backend.gedangan.m08_scenarios import read,validate,signal_candidate
from backend.gedangan.m08_network import build,geometry,links,allowed,signal_safe
from backend.gedangan.m08_runner import RUNS
from backend.gedangan.m08_reporting import results,baseline_check
from backend.gedangan.m08_interventions import cohort,apply_schedule,identity
from backend.gedangan.m07_projection import baseline,project
from backend.gedangan.m07_scenarios import read as growth
from backend.gedangan.m08_comparison import guard,compare
from backend.gedangan.m08_evaluation import evaluate
from backend.gedangan.m08_feasibility import assess
DOC=ROOT/'documentation/m08'
class ScenarioUnitTests(unittest.TestCase):
 def test_schema_and_stable_eight_IDs(self):
  self.assertEqual([read(f'S{i:02d}')['id'] for i in range(8)],[f'S{i:02d}' for i in range(8)])
  with self.assertRaises(Exception):validate({**read('S00'),'unexpected':True})
 def test_version_hash_changes(self):
  a=read('S01');b={**a,'version':'different'};self.assertNotEqual(validate(a),validate(b))
 def test_unsafe_signal_yellow_and_allred_rejected(self):
  for key,value in [('green',0),('yellow',1),('all_red',0)]:
   s=read('S01');s['parameters'][key]=value
   with self.assertRaises(ValueError):validate(s)
 def test_concepts_cannot_be_promoted_by_status(self):
  for sid in ['S06','S07']:
   with self.assertRaises(ValueError):validate({**read(sid),'status':'SIMULATION_READY_PROVISIONAL'})
 def test_coordination_not_invented_from_railway_controller(self):
  root=E.parse(ROOT/'simulation/network/m051/provisional/network.net.xml').getroot();self.assertEqual([t.get('id') for t in root.findall('tlLogic')],['m05_gedangan']);self.assertEqual(read('S05')['status'],'STRUCTURALLY_BLOCKED')
 def test_baseline_bytes_identical_to_parent(self):
  folder,m=build(read('S00'));self.assertEqual(m['parent_network_sha256'],sha(folder/'network.net.xml'));self.assertEqual(m['connection_changes'],[])
 def test_operational_network_geometry_and_edge_identity(self):
  for sid in ['S01','S02','S03']:
   folder,m=build(read(sid));self.assertEqual(geometry(E.parse(folder/'network.net.xml').getroot()),geometry(E.parse(ROOT/m['parent_network']).getroot()));self.assertEqual(m['connections_added'],[]);self.assertEqual(m['connections_removed'],[])
 def test_NETCONVERT_intermediate_drift_quarantined(self):
  folder,m=build(read('S01'));audit=load(folder/'netconvert-intermediate-audit.json');self.assertFalse(audit['used_as_final_network']);self.assertTrue(m['geometry_unchanged'])
 def test_only_declared_movement_permissions_narrow(self):
  for sid in ['S02','S03']:
   folder,m=build(read(sid));self.assertTrue(m['connection_changes']);expected=read(sid)['parameters']
   for c in m['connection_changes']:self.assertEqual(c['key'][:2],[expected['from'],expected['to']]);self.assertFalse(allowed(E.Element('connection',c['after']))-allowed(E.Element('connection',c['before'])))
 def test_lane_permissions_never_expand(self):
  for sid in ['S01','S02','S03']:
   folder,m=build(read(sid));old={l.get('id'):l for e in E.parse(ROOT/m['parent_network']).getroot().findall('edge') for l in e.findall('lane')}
   for e in E.parse(folder/'network.net.xml').getroot().findall('edge'):
    for lane in e.findall('lane'):self.assertFalse(allowed(lane)-allowed(old[lane.get('id')]))
 def test_source_lineage_preserved(self):
  folder,m=build(read('S03'));source={e['id'] for e in load(ROOT/'simulation/network/m045/provisional/inspection.json')['edges']};external={e.get('id') for e in E.parse(folder/'network.net.xml').getroot().findall('edge') if e.get('function')!='internal' and not e.get('id').startswith('m05_rail_')};self.assertEqual(external,source)
 def test_signal_phase_allocation_and_clearance_safety(self):
  folder,m=build(read('S01'));audits=signal_safe(E.parse(folder/'network.net.xml').getroot());self.assertTrue(all(a['one_protected_link'] for a in audits));self.assertEqual(m['rail_crossing_connections_unchanged'],True)
 def test_conflicting_green_negative(self):
  folder,m=build(read('S01'));root=E.parse(folder/'network.net.xml').getroot();phase=next(t for t in root.findall('tlLogic') if t.get('id')=='m05_gedangan').find('phase');phase.set('state','GG'+'r'*(len(phase.get('state'))-2))
  with self.assertRaises(ValueError):signal_safe(root)
 def test_source_turnrestrictions_and_rail_connections_retained(self):
  folder,m=build(read('S02'));a=E.parse(ROOT/m['parent_network']).getroot();b=E.parse(folder/'network.net.xml').getroot();self.assertEqual(set(links(a)),set(links(b)));self.assertTrue(m['rail_crossing_connections_unchanged'])
 def test_frontage_existing_not_added(self):
  folder,m=build(read('S03'));p=read('S03')['parameters'];roles={e['id']:e['road_function'] for e in load(ROOT/'simulation/network/m045/provisional/inspection.json')['edges']};self.assertEqual(roles[p['from']],'frontage_road');self.assertEqual(m['connections_added'],[])
 def test_heavy_deferral_conservation_and_explicit_cost(self):
  base=baseline();p=project(2026,growth('REFERENCE'));original=cohort(p,base,'provisional',42);rows,ledger=apply_schedule(original,read('S04'));self.assertEqual({r['id'] for r in original},{r['id'] for r in rows});self.assertEqual(len(original),len(rows));self.assertGreater(sum(r['deferred'] for r in ledger),0);self.assertTrue(all(abs(r['deferred_seconds']-(900 if r['deferred'] else 0))<1e-8 for r in ledger));self.assertEqual(sum(r['displaced_outside_demand_window'] for r in ledger),0)
 def test_nonheavy_and_OD_not_displaced_by_freight_rule(self):
  b=baseline();original=cohort(project(2040,growth('REFERENCE')),b,'provisional',42);rows,ledger=apply_schedule(original,read('S04'));index={q['id']:q for q in original}
  for q in rows:
   old=index[q['id']];self.assertEqual(q['od_id'],old['od_id']);self.assertEqual(q['origin_edge'],old['origin_edge']);self.assertEqual(q['destination_edge'],old['destination_edge'])
   if q['vehicle_type_id'] not in read('S04')['parameters']['classes']:self.assertEqual(q['depart_seconds'],old['depart_seconds'])
 def test_unknown_cost_land_not_zero(self):
  for sid in ['S06','S07']:
   c=assess(sid);self.assertIsNone(c['cost']['construction_IDR']);self.assertIsNone(c['land']['area_m2']);self.assertIsNone(c['performance_metrics'])
 def test_flyover_and_underpass_grade_separation_gate(self):
  for sid in ['S06','S07']:
   c=assess(sid);self.assertFalse(c['grade_separation_gate']['ready']);self.assertFalse(c['grade_separation_gate']['explicit_ramps']);self.assertEqual(c['modelability'],'NOT_SIMULATION_READY');self.assertEqual(c['hypothetical_ramp_arithmetic']['single_ramp_horizontal_run_m'],150);self.assertFalse(c['hypothetical_ramp_arithmetic']['clearance_verified'])
 def test_no_invented_ramp_network(self):
  for sid in ['S06','S07']:
   with self.assertRaises(ValueError):build(read(sid))
 def test_feasibility_has_eighteen_checks_each(self):
  for sid in ['S06','S07']:self.assertEqual(len(assess(sid)['evidence_register']),18)
 def test_multicriteria_unknowns_not_summed_or_ranked_as_zero(self):
  e=evaluate([]);self.assertFalse(e['unknown_cost_is_zero']);self.assertFalse(e['unknown_land_is_zero']);self.assertFalse(e['concepts_in_traffic_ranking']);self.assertIn('NO DEFENSIBLE',e['overall_winner'])
 def test_original_milestones_immutable(self):self.assertGreater(baseline_check(),3500)
class ActualScenarioTests(unittest.TestCase):
 def setUp(self):
  self.runs=results();self.a=next(r for r in self.runs if r['solution_id']=='S00' and r['year']==2026 and r['seed']==42 and r['growth_scenario']=='REFERENCE' and r['network_variant']=='pilot-provisional');self.b=next(r for r in self.runs if r['solution_id']=='S01' and r['year']==2026 and r['seed']==42 and r['growth_scenario']=='REFERENCE' and r['network_variant']=='pilot-provisional')
 def test_operational_matrix_actually_completed(self):
  expected={(s,y,se) for s in ['S00','S01','S02','S03','S04'] for y in [2026,2030,2040] for se in ([42,43] if y in [2026,2040] else [42])};self.assertTrue(expected<={(r['solution_id'],r['year'],r['seed']) for r in self.runs});self.assertTrue({2035}<={r['year'] for r in self.runs})
 def test_request_cohort_parity_includes_original_departures(self):
  for b in self.runs:
   if b['seed'] not in [42,43] or b['solution_id']=='S00':continue
   a=next(r for r in self.runs if r['solution_id']=='S00' and r['year']==b['year'] and r['seed']==b['seed'] and r['growth_scenario']==b['growth_scenario'] and r['m08_input']['family']==b['m08_input']['family']);self.assertEqual(load(RUNS/a['run_id']/'cohort-original.json'),load(RUNS/b['run_id']/'cohort-original.json'));self.assertTrue(guard(a,b)['comparable'])
 def test_all_requested_accounted_no_hidden_drop(self):
  for r in self.runs:self.assertEqual(r['requested'],r['failed_routes']+r['arrived']+r['running_at_end']+r['not_departed']);self.assertEqual(r['routable'],r['loaded']);self.assertEqual(r['departed'],r['arrived']+r['running_at_end'])
 def test_actual_control_timing_and_trace_difference(self):
  training=load(DOC/'signal-training.json');runs=[next(r for r in self.runs if r['run_id']==c['run_id']) for c in training['candidates']];a=next(r for r in runs if r['intervention_manifest']['parameters']['green']==8);b=next(r for r in runs if r['intervention_manifest']['parameters']['green']==12);self.assertNotEqual(a['rail_events'],b['rail_events']);self.assertEqual(a['cohort_sha256'],b['cohort_sha256']);self.assertNotEqual(a['intervention_manifest']['signal_audit'][0]['cycle_s'],b['intervention_manifest']['signal_audit'][0]['cycle_s'])
 def test_signal_training_and_holdout_separate(self):
  t=load(DOC/'signal-training.json');self.assertNotIn(t['training_seed'],t['evaluation_seeds']);self.assertEqual(t['candidate_grid'],[8,12,16]);self.assertEqual({r['seed'] for r in self.runs if r['solution_id']=='S01' and r['seed']!=11},{42,43})
 def test_actual_rerouting_or_failed_ledger_preserves_endpoints(self):
  old={q['id']:q for q in load(RUNS/self.a['run_id']/'route-ledger.json')}
  for sid in ['S02','S03']:
   b=next(r for r in self.runs if r['solution_id']==sid and r['year']==2026 and r['seed']==42 and r['growth_scenario']=='REFERENCE' and r['network_variant']=='pilot-provisional');rows=load(RUNS/b['run_id']/'route-ledger.json');self.assertEqual(len(rows),b['requested']);params=read(sid)['parameters']
   self.assertGreater(sum(q['edges']!=old[q['id']]['edges'] for q in rows),0)
   for q in rows:
    if q['route_status']=='ROUTABLE':self.assertNotIn((params['from'],params['to']),list(zip(q['edges'],q['edges'][1:])))
    else:self.assertTrue(q['reason'])
 def test_oversize_and_heavy_local_constraints(self):
  for r in self.runs:
   rows=load(RUNS/r['run_id']/'route-ledger.json');self.assertTrue(all(q['route_status']=='NOT_ROUTABLE' for q in rows if q['vehicle_type_id']=='oversize'))
   self.assertFalse(r['illegal_permissions'])
 def test_freight_accounting_includes_deferral(self):
  r=next(r for r in self.runs if r['solution_id']=='S04');self.assertGreater(r['deferral']['demand_deferred'],0);self.assertGreater(r['deferral']['deferred_vehicle_seconds'],0);self.assertEqual(r['deferral']['displaced_outside_demand_window'],0)
 def test_road_rail_and_permission_safety_full_FCD(self):
  for r in self.runs:
   s=r['safety_audit'];self.assertGreater(s['samples'],1000);self.assertFalse(s['road_on_rail']);self.assertFalse(s['road_inside_crossing_when_all_closed_red']);self.assertFalse(r['collisions']);self.assertFalse(r['teleports']);self.assertFalse(r['illegal_permissions']);self.assertFalse(s['physical_safety_certification'])
 def test_fixed_horizon_censoring_and_arrived_mean_suppressed(self):
  c=compare(self.a,self.b);self.assertEqual(self.a['fixed_horizon_s'],2100);self.assertIsNotNone(c['censoring_warning']);self.assertTrue(all(v['arrived_only_travel_time_delta_s'] is None for v in c['OD_impacts'].values()))
 def test_negative_compare_year_or_seed_rejected(self):
  for key,value in [('year',2040),('seed',99),('cohort_sha256','tampered')]:
   b=copy.deepcopy(self.b);b[key]=value;self.assertFalse(guard(self.a,b)['comparable']);self.assertIsNone(compare(self.a,b)['deltas'])
 def test_explained_network_difference_accepted_unexplained_rejected(self):
  self.assertNotEqual(self.a['network_sha256'],self.b['network_sha256']);self.assertTrue(guard(self.a,self.b)['comparable']);b=copy.deepcopy(self.b);b['intervention_manifest']['parent_network_sha256']='unknown';self.assertFalse(guard(self.a,b)['comparable'])
 def test_hidden_departure_or_geometry_change_rejected(self):
  for mutate in ['schedule','geometry','added']:
   b=copy.deepcopy(self.b)
   if mutate=='schedule':b['effective_schedule_sha256']='changed'
   if mutate=='geometry':b['intervention_manifest']['geometry_unchanged']=False
   if mutate=='added':b['intervention_manifest']['connections_added']=['invented']
   self.assertFalse(guard(self.a,b)['comparable'])
 def test_queue_and_spillback_are_actual_driver_outputs(self):
  for r in [self.a,self.b]:
   playback=load(RUNS/r['run_id']/'playback.json');self.assertTrue(playback['frames']);self.assertGreaterEqual(r['max_stopped_count'],0);self.assertGreaterEqual(r['max_lane_queue_extent_m'],0);events=load(RUNS/r['run_id']/'causal-events.json');self.assertEqual(sum(e['cause']=='VERIFIED_SPILLBACK' for e in events),r['verified_in_model_spillback'])
 def test_original_source_and_output_hash_manifest(self):
  for r in self.runs:
   f=RUNS/r['run_id']
   for name,h in load(f/'m08-output-manifest.json').items():self.assertEqual(sha(f/name),h)
 def test_fresh_replay_and_checkpoint(self):
  r=load(DOC/'reproducibility.json');self.assertTrue(all(r['physics_equal'].values()));self.assertTrue(r['cache_manifest_unchanged']);self.assertEqual(load(DOC/'run-queue.json')['status'],'COMPLETE')
 def test_full_resolution_permissions_and_actual_class_transitions(self):
  for r in self.runs:
   audit=load(RUNS/r['run_id']/'full-FCD-audit.json');self.assertEqual(audit['resolution_s'],.5);self.assertGreater(audit['full_FCD_samples_checked'],1000);self.assertFalse(audit['illegal_permission_samples']);self.assertTrue(audit['no_ignoring_class'])
   if r['class_lifecycle']['motorcycle']['departed']>0:self.assertGreater(audit['actual_lane_transitions_per_type'].get('motorcycle',0),0)
 def test_LOW_HIGH_and_strict_are_actual_complete_runs(self):
  q=load(DOC/'robustness-queue.json');self.assertEqual(q['status'],'COMPLETE');self.assertEqual(len(q['completed']),6)
  self.assertTrue({(g,s) for g in ['LOW','HIGH'] for s in ['S00','S01']}<={(r['growth_scenario'],r['solution_id']) for r in self.runs if r['year']==2040})
  self.assertTrue({'S00','S01'}<={r['solution_id'] for r in self.runs if r['m08_input']['family']=='pilot-strict'})
 def test_freight_effective_departures_preserve_original_request(self):
  r=next(r for r in self.runs if r['solution_id']=='S04');ledger=load(RUNS/r['run_id']/'deferral-ledger.json');self.assertEqual(len(ledger),r['requested']);self.assertEqual(sum(q['deferred'] for q in ledger),r['deferral']['demand_deferred']);self.assertLessEqual(r['deferral']['deferred_arrived'],r['deferral']['deferred_departed'])
 def test_family_and_growth_mismatch_rejected(self):
  for key,value in [('family','pilot-strict'),('projection_hash','unknown')]:
   b=copy.deepcopy(self.b);b['m08_input'][key]=value;self.assertFalse(guard(self.a,b)['comparable'])
 def test_permission_graph_components_do_not_gain_movements(self):
  audits=load(DOC/'topology-audits.json');self.assertTrue(audits)
  for row in audits:
   for value in row['classes'].values():
    self.assertLessEqual(value['after']['permitted_movements'],value['before']['permitted_movements']);self.assertEqual(value['after']['permitted_road_edges'],value['before']['permitted_road_edges'])
    if row['scenario'] in ['S00','S01','S04']:self.assertEqual(value['before'],value['after'])
if __name__=='__main__':unittest.main()
