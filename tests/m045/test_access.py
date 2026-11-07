import copy
import hashlib
import unittest
import xml.etree.ElementTree as ET
from backend.gedangan import m045_access as m
from backend.gedangan import m04_demand as original

class MulticlassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        m.adapter.activate();m.install_screens();cls.policy=m.load(m.CONF/'policy.json');cls.runs=m.load(m.DOC/'run-summary.json');cls.compat=m.load(m.DOC/'compatibility-results.json');cls.edges={mode:m.adapter.edge_index(mode) for mode in ['strict','provisional']};cls.nets={mode:m.adapter.sumonet(mode) for mode in cls.edges};cls.vs={v['id']:v for v in m.adapter.registry()}
    def fixture(self,tags=None,role='main_arterial_road'):
        e=copy.deepcopy(next(iter(self.edges['provisional'].values())));e.update(tags={'highway':'trunk',**(tags or {})},road_function=role,sign=1);return e
    def test_previous_633_sources_and_outputs_immutable(self):m.baseline_check()
    def test_private_adapter_does_not_mutate_original_m04(self):
        self.assertEqual(original.M03,m.BASE);self.assertNotEqual(original.RUNS,m.RUNS);self.assertEqual(original.registry(),m.adapter.registry())
    def test_root_cause_is_explicit_m03_passenger_literal(self):
        self.assertIn("'allow':'passenger'",(m.ROOT/'configuration/network-m03/build_network.py').read_text())
        for mode in self.edges:
            base=ET.parse(m.BASE/mode/'network.net.xml').getroot();self.assertTrue(all(l.get('allow')=='passenger' for e in base.findall('edge') for l in e.findall('lane')))
    def test_exact_geometry_and_structural_connection_preservation(self):
        for mode in self.edges:
            before=ET.parse(m.BASE/mode/'network.net.xml').getroot();after=ET.parse(m.NET/mode/'network.net.xml').getroot();self.assertEqual(m.geometry_signature(before),m.geometry_signature(after));self.assertEqual(set(m.external_connections(before)),set(m.external_connections(after)))
    def test_hierarchy_specific_class_overrides_generic_access(self):
        e=self.fixture({'access':'no','bus':'yes'});self.assertTrue(m.class_access(e,'bus','strict',self.policy)['allowed']);self.assertFalse(m.class_access(e,'passenger','strict',self.policy)['allowed'])
        self.assertFalse(m.class_access(self.fixture({'motor_vehicle':'yes','hgv':'no'}),'truck','provisional',self.policy)['allowed'])
    def test_private_access_never_automatically_grants_classes(self):
        for vc in self.policy['classes']:self.assertFalse(m.class_access(self.fixture({'access':'private'}),vc,'provisional',self.policy)['allowed'])
    def test_conditional_and_lane_access_are_quarantined(self):
        for tag in ['motor_vehicle:conditional','hgv:conditional','hgv:lanes','hgv:forward:conditional']:
            self.assertFalse(m.class_access(self.fixture({tag:'no @ (Mo-Fr)'}),'truck','provisional',self.policy)['allowed'])
    def test_directional_restriction_applies_to_correct_source_order(self):
        e=self.fixture({'motorcycle:forward':'no'});self.assertFalse(m.class_access(e,'motorcycle','strict',self.policy)['allowed']);e['sign']=-1;self.assertTrue(m.class_access(e,'motorcycle','strict',self.policy)['allowed'])
    def test_frontage_and_local_service_deny_unproven_heavy_access(self):
        for role in ['frontage_road','local_access_road','service_road']:
            for vc in ['bus','truck','trailer']:
                for variant in ['strict','provisional']:self.assertFalse(m.class_access(self.fixture(role=role),vc,variant,self.policy)['allowed'])
    def test_main_heavy_access_is_provisional_assumption_not_verified(self):
        for vc in ['truck','trailer']:
            self.assertFalse(m.class_access(self.fixture(),vc,'strict',self.policy)['allowed']);r=m.class_access(self.fixture(),vc,'provisional',self.policy);self.assertTrue(r['allowed']);self.assertEqual(r['status'],'ASSUMPTION');self.assertFalse(r['field_legal_verified'])
    def test_explicit_positive_tag_verified_and_missing_service_withheld(self):
        r=m.class_access(self.fixture({'motorcycle':'yes'},'service_road'),'motorcycle','strict',self.policy);self.assertTrue(r['allowed']);self.assertEqual(r['status'],'VERIFIED')
        r=m.class_access(self.fixture(role='service_road'),'motorcycle','strict',self.policy);self.assertFalse(r['allowed']);self.assertEqual(r['status'],'MISSING')
    def test_each_external_lane_matches_source_decision(self):
        for mode,es in self.edges.items():
            for eid,e in es.items():
                for cls in self.policy['classes']:
                    for lane in self.nets[mode].getEdge(eid).getLanes():self.assertEqual(lane.allows(cls),e['access_policy'][cls]['allowed'])
                    self.assertIn(e['access_policy'][cls]['status'],['VERIFIED','INFERRED','ASSUMPTION','MISSING'])
    def test_internal_lane_permissions_and_connection_intersections(self):
        for mode in self.edges:
            net=self.nets[mode];root=ET.parse(m.NET/mode/'network.net.xml').getroot();expect={}
            for key,c in m.external_connections(root).items():
                e0,e1,i,j=key;common={vc for vc in self.policy['classes'] if net.getEdge(e0).getLane(int(i)).allows(vc) and net.getEdge(e1).getLane(int(j)).allows(vc)};allowed=set(c.get('allow','').split()) if c.get('allow') is not None else (set() if c.get('disallow')=='all' else set(self.policy['classes']))
                self.assertTrue(allowed<=common)
                if c.get('via'):expect.setdefault(c.get('via'),set()).update(allowed)
            for lane,classes in expect.items():self.assertEqual({vc for vc in self.policy['classes'] if net.getLane(lane).allows(vc)},classes)
    def test_all_accepted_routes_obey_new_class_lane_connections(self):
        for mode,rows in self.compat.items():
            for r in rows:
                if r['route_status']=='ROUTABLE':self.assertIsNone(m.route_screen_impl(r['edges'],r,self.vs[r['vehicle_type_id']],self.edges[mode],self.nets[mode],m.adapter.inspect(mode)['connections']))
    def test_class_specific_turn_restriction_narrows_without_new_movement(self):
        es=self.edges['provisional'];row=next(r for r in self.compat['provisional'] if r['vehicle_type_id']=='car' and r['od_id']=='northbound');a,b=[es[i] for i in row['edges'][:2]]
        rel={'id':1,'tags':{'type':'restriction','restriction:hgv':'no_straight_on'},'members':[{'type':'way','role':'from','ref':a['source_way_id']},{'type':'way','role':'to','ref':b['source_way_id']},{'type':'node','role':'via','ref':int(a['to'][4:])}]}
        self.assertTrue(m.movement_denied(a,b,'truck',[rel]));self.assertFalse(m.movement_denied(a,b,'passenger',[rel]))
    def test_numeric_height_and_unresolved_load_clearance_fail(self):
        rows=self.compat['provisional'];r=next(r for r in rows if r['vehicle_type_id']=='heavy_truck' and r['route_status']=='ROUTABLE');es=copy.deepcopy(self.edges['provisional']);es[r['origin_edge']]['tags']['maxheight']='2.5';self.assertIn('DIMENSION',m.type_screen_impl(r,self.vs['heavy_truck'],es,self.nets['provisional']))
        es[r['origin_edge']]['tags']={'maxweight':'7.5'};self.assertIn('LOAD',m.type_screen_impl(r,self.vs['heavy_truck'],es,self.nets['provisional']))
    def test_motor_and_all_nonoversize_types_move_and_arrive_northbound(self):
        run=next(r for r in self.runs if r['profile']=='smoke' and r['network_variant']=='provisional');states=m.load(m.RUNS/run['run_id']/'vehicle-states.json')['states']
        for typeid in self.vs:
            s=next(s for s in states if s['vehicle_type_id']==typeid and s['od_id']=='northbound')
            if typeid=='oversize':self.assertEqual(s['status'],'NOT_ROUTABLE')
            else:self.assertEqual(s['status'],'ARRIVED');self.assertTrue(s['moved_in_recorded_fcd']);self.assertGreater(s['position_extent_m'],50)
    def test_southbound_frontage_feeder_station_supported_classes(self):
        rows=self.compat['provisional']
        for name in ['southbound','frontage_continuity','feeder_to_main','station_junction']:
            for typeid in ['motorcycle','car','pickup_van']:self.assertEqual(next(r for r in rows if r['od_id']==name and r['vehicle_type_id']==typeid)['route_status'],'ROUTABLE')
    def test_strict_failures_and_oversize_remain_explicit(self):
        for mode,rows in self.compat.items():
            for r in rows:
                if r['route_status']!='ROUTABLE':self.assertTrue(r['reason']);self.assertEqual(r['edges'],[])
                if r['vehicle_type_id']=='oversize':self.assertEqual(r['route_status'],'NOT_ROUTABLE');self.assertIn('CLEARANCE',r['reason'])
        for name in ['feeder_to_main','main_to_feeder','frontage_exit','station_junction']:self.assertEqual(next(r for r in self.compat['strict'] if r['od_id']==name and r['vehicle_type_id']=='car')['route_status'],'NOT_ROUTABLE')
    def test_original_od_and_composition_unchanged_by_corrected_generation(self):
        matrix=m.load(m.ROOT/'simulation/demand/m04/od-matrix.fixture.json');config=m.load(m.ROOT/'configuration/demand-m04/demand-config.json')
        for mode in self.edges:
            for profile in ['low','medium','stress']:
                old=original.generate(mode,profile,config,matrix);new=m.load(m.DEMAND/mode/profile/'requested-trips.json')['requests']
                self.assertEqual([{k:q[k] for k in ['od_id','vehicle_type_id','depart_seconds','origin_edge','destination_edge']} for q in old],[{k:q[k] for k in ['od_id','vehicle_type_id','depart_seconds','origin_edge','destination_edge']} for q in new])
    def test_all_runs_conserve_counts_and_expose_teleports(self):
        for r in self.runs:
            self.assertEqual(r['requested_trips'],r['routable_trips']+r['failed_routes']);self.assertEqual(r['loaded_vehicles'],r['routable_trips']);self.assertEqual(r['departed_vehicles'],r['arrived_vehicles']);self.assertEqual(r['teleported_vehicles'],0);self.assertEqual(r['pending_insertion'],0);self.assertEqual(r['running_at_end'],0)
            for c in m.load(m.RUNS/r['run_id']/'class-lifecycle.json').values():self.assertEqual(c['loaded'],c['routable']);self.assertEqual(c['departed'],c['arrived'])
    def test_frontage_never_becomes_extra_main_lane(self):
        for es in self.edges.values():
            front={e['source_way_id'] for e in es.values() if e['road_function']=='frontage_road'};main={e['source_way_id'] for e in es.values() if e['road_function']=='main_arterial_road'};self.assertTrue(front);self.assertFalse(front&main)
    def test_run_network_manifests_and_input_hashes(self):
        for p in list(m.RUNS.rglob('manifest.json'))+list(m.NET.rglob('manifest.json')):
            meta=m.load(p)
            for name,h in meta['files'].items():self.assertEqual(m.sha(p.parent/name),h)
            for name,h in meta['input_sha256'].items():self.assertEqual(m.sha(m.ROOT/name),h)
    def test_browser_exports_are_actual_corrected_or_original_records(self):
        web=m.ROOT/'frontend/public/access/m045';data=m.load(web/'summary.json');self.assertFalse(data['field_calibrated']);self.assertFalse(data['m05_started'])
        for r in self.runs:self.assertEqual((web/f'{r["run_id"]}.trajectory.json').read_bytes(),(m.RUNS/r['run_id']/'trajectory.json').read_bytes())
        for mode in self.edges:self.assertEqual(m.load(web/f'{mode}.network.json'),m.adapter.inspect(mode))

if __name__=='__main__':unittest.main()
