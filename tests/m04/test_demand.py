from collections import Counter
import copy
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import jsonschema
from backend.gedangan import m04_demand as m

class DemandM04Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        m.activate();cls.config=m.load(m.CONF/'demand-config.json');cls.vehicles=m.registry();cls.matrix=m.load(m.DEMAND/'od-matrix.fixture.json');cls.runs=m.load(m.DOC/'run-summary.json');cls.compat=m.load(m.DOC/'compatibility-results.json')
        cls.edges={mode:m.edge_index(mode) for mode in ['strict','provisional']};cls.nets={mode:m.sumonet(mode) for mode in cls.edges}

    def test_previous_milestone_sources_unchanged(self):m.verify_baseline()
    def test_ten_unique_types_and_explicit_shared_sumo_classes(self):
        self.assertEqual(len({v['id'] for v in self.vehicles}),10);self.assertEqual(len({v['sumo_vclass'] for v in self.vehicles}),6)
        self.assertEqual({v['sumo_vclass'] for v in self.vehicles if 'truck' in v['id']},{'truck'})
    def test_input_validation_accepts_technical_parameters(self):m.validate_inputs(self.vehicles,self.config)
    def test_rejects_nonfinite_negative_and_mismatched_parameters(self):
        for key,value in [('length',-1),('width',float('nan')),('emergencyDecel',.1),('vClass','ship')]:
            vehicles=copy.deepcopy(self.vehicles);vehicles[0]['parameters'][key]=value
            with self.assertRaises(ValueError):m.validate_inputs(vehicles,self.config)
    def test_every_vehicle_parameter_has_assumption_provenance(self):
        for v in self.vehicles:
            self.assertEqual(set(v['parameters']),set(v['parameter_provenance']))
            self.assertTrue(all(p['status']=='ASSUMPTION' and p['provenance_id']=='A-VEH-01' for p in v['parameter_provenance'].values()))
    def test_no_growth_projection_or_observed_volume(self):
        self.assertFalse(self.config['year_dimensions']['projection_implemented']);self.assertEqual(self.config['year_dimensions']['future_growth_records'],[]);self.assertEqual(m.load(m.CONF/'provenance.json')['observed_records'],[])
    def test_od_matrix_schema_and_zone_references(self):
        jsonschema.validate(self.matrix,m.load(m.CONF/'od-matrix.schema.json'));zones={z['id'] for z in m.load(m.DEMAND/'od-zones.json')['zones']}
        for row in self.matrix['movements']:self.assertIn(row['origin_zone'],zones);self.assertIn(row['destination_zone'],zones)
    def test_zone_geometry_is_anchored_to_actual_m03_edge(self):
        for z in m.load(m.DEMAND/'od-zones.json')['zones']:
            geo=z['geographic_zone'];eid=geo['source_edge'];edge=next(es[eid] for es in self.edges.values() if eid in es)
            self.assertEqual(geo['source_way_id'],edge['source_way_id'])
            self.assertEqual(geo['anchor_xy_m'],[sum(p[i] for p in edge['shape'])/len(edge['shape']) for i in [0,1]])
    def test_origin_destination_candidates_valid_and_permission_assignment_true(self):
        bytype={v['id']:v for v in self.vehicles}
        for z in m.load(m.DEMAND/'od-zones.json')['zones']:
            for mode,a in z['assignments'].items():
                for key in ['origin_candidate_edges','destination_candidate_edges']:
                    self.assertTrue(all(e in self.edges[mode] for e in a[key]))
                    for typeid,assigned in a['vehicle_class_eligibility'].items():
                        for e in assigned[key]:self.assertTrue(any(l.allows(bytype[typeid]['sumo_vclass']) for l in self.nets[mode].getEdge(e).getLanes()))
    def test_largest_remainder_conserves_requested_composition(self):
        for n in [1,40,120,300]:self.assertEqual(sum(m.allocate(n,self.config['composition']).values()),n)
        with self.assertRaises(ValueError):m.allocate(10,{'x':0})
    def test_demand_is_seed_deterministic_and_seed_sensitive(self):
        a=m.generate('strict','low',self.config,self.matrix);self.assertEqual(a,m.generate('strict','low',self.config,self.matrix))
        c=copy.deepcopy(self.config);c['seed']+=1;self.assertNotEqual(a,m.generate('strict','low',c,self.matrix))
    def test_vehicle_ids_unique_globally_across_batches(self):
        ids=[]
        for mode in self.edges:
            for profile in self.config['profiles']:ids += [q['id'] for q in m.generate(mode,profile,self.config,self.matrix)]
        self.assertEqual(len(ids),len(set(ids)))
    def test_departures_sorted_and_in_15_minute_interval(self):
        for mode in self.edges:
            for profile in self.config['profiles']:
                qs=m.generate(mode,profile,self.config,self.matrix);times=[q['depart_seconds'] for q in qs]
                self.assertEqual(times,sorted(times));self.assertTrue(all(0<=t<900 for t in times));self.assertTrue(all(q['category']=='SYNTHETIC_TEST' for q in qs))
    def test_strict_and_provisional_have_same_requested_od_composition(self):
        for profile in self.config['profiles']:
            a=m.generate('strict',profile,self.config,self.matrix);b=m.generate('provisional',profile,self.config,self.matrix)
            self.assertEqual([(q['od_id'],q['vehicle_type_id'],q['depart_seconds']) for q in a],[(q['od_id'],q['vehicle_type_id'],q['depart_seconds']) for q in b])
    def test_m03_permissions_are_immutable_passenger_only(self):
        for net in self.nets.values():
            for e in net.getEdges():
                if e.getFunction()=='internal':continue
                for l in e.getLanes():self.assertTrue(l.allows('passenger'));self.assertFalse(l.allows('motorcycle'));self.assertFalse(l.allows('truck'))
    def test_router_independently_rejects_disallowed_classes(self):
        for mode in self.edges:
            folder=m.DEMAND/'compatibility'/mode;log=m.load(folder/'permission-probe-log.json');self.assertEqual(log['returncode'],0)
            emitted={v.get('id') for v in ET.parse(folder/'permission-probe.rou.xml').getroot().findall('vehicle')}
            self.assertEqual(emitted,{'permission_probe_car'});self.assertIn('is not allowed to depart',log['stderr'])
    def test_heavy_and_oversize_never_bypass_permissions_or_clearance(self):
        for rows in self.compat.values():
            for r in rows:
                if r['vehicle_type_id']!='car':self.assertEqual(r['route_status'],'NOT_ROUTABLE')
                if r['vehicle_type_id']=='oversize':self.assertIn('CLEARANCE_UNVERIFIED',r['reason'])
        heavy=[v for v in self.vehicles if v['id'] in ['bus','heavy_truck','trailer']]
        self.assertTrue(all(v['eligibility']['allowed_road_functions']==['main_arterial_road'] for v in heavy))
    def test_strict_failures_are_preserved_without_fake_route(self):
        for key in ['feeder_to_main','main_to_feeder','frontage_exit','station_junction']:
            r=next(r for r in self.compat['strict'] if r['vehicle_type_id']=='car' and r['od_id']==key);self.assertEqual(r['route_status'],'NOT_ROUTABLE');self.assertEqual(r['edges'],[])
    def test_all_accepted_routes_follow_actual_lane_permissions_and_connections(self):
        vs={v['id']:v for v in self.vehicles}
        for mode,rows in self.compat.items():
            connections=m.inspect(mode)['connections']
            for r in rows:
                if r['route_status']=='ROUTABLE':self.assertIsNone(m.validate_route(r['edges'],r,vs[r['vehicle_type_id']],self.edges[mode],self.nets[mode],connections))
    def test_direction_mismatch_and_disconnected_sequence_rejected(self):
        row=next(r for r in self.compat['strict'] if r['route_status']=='ROUTABLE');v=next(v for v in self.vehicles if v['id']=='car')
        self.assertIsNotNone(m.validate_route(list(reversed(row['edges'])),row,v,self.edges['strict'],self.nets['strict'],m.inspect('strict')['connections']))
        ids=[row['edges'][0],row['edges'][-1]];self.assertIsNotNone(m.validate_route(ids,row,v,self.edges['strict'],self.nets['strict'],m.inspect('strict')['connections']))
    def test_both_corridor_directions_and_frontage_actually_move_and_arrive(self):
        for mode in self.edges:
            states=m.load(m.RUNS/f'm04-{mode}-smoke-seed{self.config["seed"]}'/'vehicle-states.json')['states']
            for od in ['northbound','southbound','frontage_continuity']:
                s=next(s for s in states if s['od_id']==od and s['vehicle_type_id']=='car');self.assertEqual(s['status'],'ARRIVED');self.assertTrue(s['moved_in_recorded_fcd']);self.assertGreater(s['position_extent_m'],50)
    def test_frontage_route_separate_from_main(self):
        for mode,rows in self.compat.items():
            r=next(r for r in rows if r['od_id']=='frontage_continuity' and r['vehicle_type_id']=='car');self.assertTrue(all(self.edges[mode][e]['road_function']=='frontage_road' for e in r['edges']))
    def test_requested_routable_failure_and_lifecycle_accounting(self):
        for r in self.runs:
            self.assertEqual(r['requested_trips'],r['routable_trips']+r['failed_routes']);self.assertEqual(r['loaded_vehicles'],r['routable_trips']);self.assertEqual(r['routable_trips'],r['departed_vehicles']+r['pending_insertion']);self.assertEqual(r['departed_vehicles'],r['arrived_vehicles']+r['running_at_end']);self.assertEqual(r['sumo_returncode'],0)
    def test_interval_od_counts_schema_and_conservation(self):
        for r in self.runs:
            folder=m.DEMAND/'compatibility'/r['network_variant'] if r['profile']=='smoke' else m.DEMAND/r['network_variant']/r['profile'];counts=m.load(folder/'od-interval-counts.json');jsonschema.validate(counts,m.load(m.CONF/'od-interval.schema.json'))
            self.assertEqual(sum(q['requested_trips'] for q in counts['rows']),r['requested_trips']);self.assertEqual(sum(q['failed_routes'] for q in counts['rows']),r['failed_routes'])
            for q in counts['rows']:self.assertEqual(q['interval_end_seconds']-q['interval_start_seconds'],900);self.assertEqual(q['year'],2026);self.assertEqual(q['requested_trips'],q['routable_trips']+q['failed_routes'])
    def test_failed_trips_have_explicit_status_and_reason(self):
        for r in self.runs:
            states=m.load(m.RUNS/r['run_id']/'vehicle-states.json')['states'];self.assertEqual(sum(s['status']=='NOT_ROUTABLE' for s in states),r['failed_routes'])
            folder=m.DEMAND/'compatibility'/r['network_variant'] if r['profile']=='smoke' else m.DEMAND/r['network_variant']/r['profile']
            failed=m.load(folder/'failed-trips.json')['failures'];self.assertEqual(len(failed),r['failed_routes']);self.assertTrue(all(x['reason'] and not x['edges'] for x in failed))
    def test_run_manifests_and_unchanged_network_hash(self):
        for r in self.runs:
            folder=m.RUNS/r['run_id'];manifest=m.load(folder/'run-manifest.json');self.assertEqual(manifest['network_sha256'],m.sha(m.M03/r['network_variant']/'network.net.xml'))
            for p,h in manifest['files'].items():self.assertEqual(m.sha(folder/p),h)
    def test_json_and_generated_route_xml_parse(self):
        for base in [m.DEMAND,m.RUNS]:
            for p in base.rglob('*.json'):self.assertIsInstance(m.load(p),(dict,list))
            for p in base.rglob('*.rou.xml'):self.assertEqual(ET.parse(p).getroot().tag,'routes')
    def test_registry_attributes_supported_by_installed_xsd(self):
        self.assertTrue(m.load(m.DOC/'attribute-support.json')['all_registry_attributes_present'])
        for r in self.runs:self.assertIn('--xml-validation',m.load(m.RUNS/r['run_id']/'simulation-log.json')['command'])
    def test_motorcycle_sublane_isolated_proof_and_not_enabled_in_gedangan(self):
        r=m.load(m.RUNS/'isolated-motorcycle-sublane/results.json');self.assertFalse(r['enabled_on_gedangan']);self.assertEqual(r['regular']['same_lane_lateral_overlap_samples'],0);self.assertGreater(r['sublane']['same_lane_lateral_overlap_samples'],1);self.assertEqual(r['sublane']['arrived'],2)
        for run in self.runs:self.assertIsNone(ET.parse(m.RUNS/run['run_id']/'run.sumocfg').getroot().find('.//lateral-resolution'))
    def test_playback_exactly_matches_sumo_fcd_source(self):
        r=next(r for r in self.runs if r['profile']=='smoke' and r['network_variant']=='strict');folder=m.RUNS/r['run_id'];frames=m.load(folder/'trajectory.json')['frames'];source={float(t.get('time')):{v.get('id'):v.attrib for v in t.findall('vehicle')} for t in ET.parse(folder/'fcd.xml').getroot().findall('timestep')}
        for frame in frames:
            for v in frame['vehicles']:
                q=source[frame['time_seconds']][v['id']];self.assertEqual([v['x'],v['y'],v['pos_m']],[float(q[k]) for k in ['x','y','pos']]);self.assertEqual(v['lane'],q['lane'])
    def test_web_exports_are_actual_recorded_outputs(self):
        web=m.ROOT/'frontend/public/demand/m04';summary=m.load(web/'summary.json');self.assertFalse(summary['field_calibrated']);self.assertEqual(summary['runs'],self.runs)
        for r in self.runs:self.assertEqual((web/f'{r["run_id"]}.trajectory.json').read_bytes(),(m.RUNS/r['run_id']/'trajectory.json').read_bytes())

if __name__=='__main__':unittest.main()
