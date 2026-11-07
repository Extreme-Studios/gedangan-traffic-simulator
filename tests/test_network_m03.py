"""Actual SUMO output constraints, no mocked route success or traffic volumes."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from pyproj import Transformer

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'simulation/network/m03'
def load(p):return json.loads(p.read_text(encoding='utf-8'))

class NetworkM03Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data={mode:load(OUT/mode/'inspection.json') for mode in ['strict','provisional']}
        cls.maps={mode:load(OUT/mode/'source-to-edge.json')['edges'] for mode in cls.data}
        cls.raw=load(ROOT/'geodata/raw/gedangan-network.json');cls.nodes={e['id']:e for e in cls.raw['elements'] if e['type']=='node'};cls.ways={e['id']:e for e in cls.raw['elements'] if e['type']=='way'}
        cls.routes={mode:load(OUT/mode/'route-tests/results.json')['results'] for mode in cls.data}

    def test_all_preexisting_sources_unchanged(self):
        manifest=load(ROOT/'documentation/m03/previous-milestones-sha256.json')
        self.assertEqual([p for p,h in manifest.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h],[])

    def test_source_hashes_match_metadata(self):
        for p,h in load(OUT/'network-metadata.json')['source_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),h)

    def test_source_node_subsequence_and_projected_geometry(self):
        fwd=Transformer.from_crs(4326,32749,always_xy=True)
        origin=load(OUT/'network-metadata.json')['coordinate_origin_utm_m']
        for rows in self.maps.values():
            for e in rows:
                ids=e['osm_node_ids'];way=self.ways[e['source_way_id']]['nodes'];check=ids if e['sign']==1 else list(reversed(ids))
                self.assertTrue(any(check==way[i:i+len(check)] for i in range(len(way))),e['id'])
                for nid,point in zip(ids,e['shape']):
                    n=self.nodes[nid];x,y=fwd.transform(n['lon'],n['lat']);self.assertAlmostEqual(point[0],x-origin[0],places=5);self.assertAlmostEqual(point[1],y-origin[1],places=5)

    def test_strict_directions_have_explicit_or_defined_evidence(self):
        for e in self.maps['strict']:
            self.assertIn(e['direction_source_status'],['VERIFIED','INFERRED'])
            if e['direction_source_status']=='VERIFIED':self.assertIn(e['tags'].get('oneway'),['yes','1','true','-1','no','0','false'])

    def test_provisional_unknown_direction_not_universal(self):
        policy=load(ROOT/'configuration/network-m03/policy.json')
        for e in self.maps['provisional']:
            if e['direction_source_status']=='ASSUMPTION':self.assertIn(e['tags']['highway'],policy['provisional_bidirectional_highways']);self.assertNotIn('oneway',e['tags'])
        decisions=load(OUT/'provisional/edge-decisions.json')['source_features']
        self.assertTrue(any(d['action']=='EXCLUDED' and any('Direction unknown' in r for r in d['reasons']) for d in decisions))

    def test_all_source_features_accounted_for(self):
        source={f['id'] for f in load(ROOT/'geodata/roads/all_roads.geojson')['features']}
        for mode in self.data:self.assertEqual({d['source_feature_id'] for d in load(OUT/mode/'edge-decisions.json')['source_features']},source)

    def test_private_and_disallowed_passenger_roads_excluded(self):
        blocked=load(ROOT/'configuration/network-m03/policy.json')['excluded_access_values']
        for rows in self.maps.values():
            for e in rows:
                for key in ['access','vehicle','motor_vehicle','motorcar']:self.assertNotIn(e['tags'].get(key),blocked)

    def test_unique_edges_and_valid_node_references(self):
        for n in self.data.values():
            ids=[e['id'] for e in n['edges']];self.assertEqual(len(ids),len(set(ids)));nodes={j['id'] for j in n['nodes']}
            for e in n['edges']:self.assertIn(e['from'],nodes);self.assertIn(e['to'],nodes);self.assertNotEqual(e['from'],e['to'])

    def test_actual_lane_connection_whitelist(self):
        for mode,n in self.data.items():
            approved={(c['from'],c['to'],c['fromLane'],c['toLane']) for c in load(OUT/mode/'connection-provenance.json')['approved_connections']}
            emitted={(c['from'],c['to'],c['fromLane'],c['toLane']) for c in n['connections']}
            self.assertTrue(emitted<=approved);self.assertEqual(n['qa']['unapproved_connections'],0)

    def test_connections_share_source_node_and_lane_indices_exist(self):
        for n in self.data.values():
            edges={e['id']:e for e in n['edges']}
            for c in n['connections']:
                a,b=edges[c['from']],edges[c['to']];self.assertEqual(a['to'],b['from']);self.assertLess(c['fromLane'],a['lanes']);self.assertLess(c['toLane'],b['lanes']);self.assertNotEqual(a['from'],b['to'])

    def test_restriction_blocked_pairs_do_not_survive(self):
        for mode,n in self.data.items():
            pairs={(c['from'],c['to']) for c in n['connections']};blocked=load(OUT/mode/'connection-provenance.json')['blocked_movements']
            for c in blocked:
                if c['restriction_relation_ids']:self.assertNotIn((c['from'],c['to']),pairs)
            self.assertTrue(any(c['restriction_relation_ids'] for c in blocked))

    def test_components_never_join_original_m02_components(self):
        for mode in self.data:
            for part in load(OUT/mode/'connectivity.json')['components']:self.assertEqual(len(part['m02_component_ids']),1)

    def test_main_and_frontage_keep_distinct_source_way_ids(self):
        for n in self.data.values():
            main={e['source_way_id'] for e in n['edges'] if e['road_function']=='main_arterial_road'};front={e['source_way_id'] for e in n['edges'] if e['road_function']=='frontage_road'}
            self.assertTrue(main);self.assertTrue(front);self.assertFalse(main&front)

    def test_both_priority_routes_run_duarouter_and_are_nontrivial(self):
        for mode,rows in self.routes.items():
            for name in ['northbound','southbound']:
                row=next(r for r in rows if r['test_id']==name);self.assertTrue(row['router_executed']);self.assertEqual(row['router_returncode'],0);self.assertEqual(row['status'],'FOUND');self.assertGreater(len(row['edges']),10)

    def test_all_found_routes_follow_emitted_connections(self):
        for mode,rows in self.routes.items():
            allowed={(c['from'],c['to']) for c in self.data[mode]['connections']}
            for row in rows:
                if row['status']=='FOUND':self.assertEqual(row['edges'][0],row['starting_edge']);self.assertEqual(row['edges'][-1],row['destination_edge']);self.assertTrue(all((a,b) in allowed for a,b in zip(row['edges'],row['edges'][1:])))

    def test_strict_missing_station_endpoint_does_not_get_fake_route(self):
        row=next(r for r in self.routes['strict'] if r['test_id']=='station_junction');self.assertEqual(row['status'],'NOT_FOUND');self.assertIsNone(row['destination_edge']);self.assertEqual(row['edges'],[])

    def test_parameters_unknown_source_not_labeled_survey(self):
        for rows in self.maps.values():
            for e in rows:
                self.assertFalse(e['field_verified']);self.assertIsNone(e['capacity_vehicles_per_hour']);self.assertEqual(e['parameter_status']['capacity'],'MISSING')
                if 'maxspeed' not in e['tags']:self.assertEqual(e['parameter_status']['speed'],'ASSUMPTION')
                if 'lanes' not in e['tags'] and 'lanes:forward' not in e['tags'] and 'lanes:backward' not in e['tags']:self.assertEqual(e['parameter_status']['lanes'],'ASSUMPTION')

    def test_viewer_reads_actual_sumo_lane_shapes_and_parameters(self):
        for mode,n in self.data.items():
            root=ET.parse(OUT/mode/'network.net.xml').getroot();byid={e.get('id'):e for e in root.findall('edge') if e.get('function')!='internal'}
            for e in n['edges']:
                ls=byid[e['id']].findall('lane');self.assertEqual(len(ls),e['lanes']);self.assertEqual(float(ls[0].get('speed')),e['speed_m_per_s'])
                self.assertEqual(e['shape'],[list(map(float,p.split(','))) for p in ls[0].get('shape').split()])

    def test_sumo_load_only_succeeded_without_demand(self):
        for mode in self.data:
            self.assertEqual(load(OUT/mode/'sumo-load-log.json')['returncode'],0)
            root=ET.parse(OUT/mode/'inspect.sumocfg').getroot();self.assertIsNone(root.find('input/route-files'));self.assertEqual(root.find('time/end').get('value'),'0')

    def test_no_train_edges_or_traffic_calibration(self):
        for n in self.data.values():
            self.assertEqual(len(n['rail_overlay']),13);self.assertEqual(len(n['crossing_overlay']),11)
            self.assertTrue(all(e['road_function'].endswith('_road') for e in n['edges']))
        self.assertFalse(load(OUT/'network-metadata.json')['rail_operations'])

    def test_web_exports_identical_to_network_inspection(self):
        for mode in self.data:self.assertEqual((ROOT/f'frontend/public/network/m03/{mode}.json').read_bytes(),(OUT/mode/'inspection.json').read_bytes())

if __name__=='__main__':unittest.main()
