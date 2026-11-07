"""M02 geographic integrity tests against the retained OSM snapshot."""
import hashlib
import json
from pathlib import Path
import unittest
from pyproj import Transformer
from shapely.geometry import shape

ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))

class GeographicMappingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=load('geodata/raw/gedangan-network.json')
        cls.nodes={e['id']:e for e in cls.raw['elements'] if e['type']=='node'}
        cls.ways={e['id']:e for e in cls.raw['elements'] if e['type']=='way'}
        cls.roads=load('geodata/roads/all_roads.geojson')['features']
        cls.all=load('geodata/processed/all_features.geojson')['features']
        cls.bundle=load('geodata/processed/map-utm49s.json')
        cls.qa=load('geodata/quality_assurance/quality_report.json')

    def test_original_m01_files_unchanged(self):
        manifest=load('documentation/m02/m01-original-sha256.json')
        changed=[name for name,digest in manifest.items() if not (ROOT/name).exists() or hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest]
        self.assertEqual(changed,[])

    def test_source_hash_matches_retained_raw(self):
        meta=load('geodata/sources/gedangan-network.metadata.json')
        self.assertEqual(hashlib.sha256((ROOT/meta['raw_file']).read_bytes()).hexdigest(),meta['sha256'])
        self.assertEqual(meta['license'],'ODbL-1.0')

    def test_features_have_unique_ids(self):
        ids=[f['id'] for f in self.all];self.assertEqual(len(ids),len(set(ids)))

    def test_all_geometries_nonempty_valid(self):
        for f in self.all:
            geom=shape(f['geometry']);self.assertFalse(geom.is_empty,f['id']);self.assertTrue(geom.is_valid,f['id'])

    def test_road_coordinates_are_exact_osm_subsequences(self):
        for f in self.roads:
            p=f['properties'];w=self.ways[p['osm_id']];ids=p['osm_node_ids']
            self.assertTrue(any(ids==w['nodes'][i:i+len(ids)] for i in range(len(w['nodes']))),f['id'])
            self.assertEqual(f['geometry']['coordinates'],[[self.nodes[n]['lon'],self.nodes[n]['lat']] for n in ids])

    def test_rail_coordinates_are_exact_source_nodes(self):
        for f in load('geodata/railways/rail_tracks.geojson')['features']:
            self.assertEqual(f['geometry']['coordinates'],[[self.nodes[n]['lon'],self.nodes[n]['lat']] for n in f['properties']['osm_node_ids']])

    def test_station_is_named_gedangan_source_marker(self):
        f=load('geodata/railways/stations.geojson')['features'][0]
        self.assertEqual(f['properties']['osm_id'],1359952188)
        self.assertEqual(f['properties']['name'],'Gedangan')
        self.assertEqual(f['geometry']['coordinates'],[112.7285913,-7.3889859])

    def test_crs_roundtrip_and_distance(self):
        self.assertLess(self.qa['geometry']['max_crs_roundtrip_error_degrees'],1e-8)
        self.assertLess(self.qa['geometry']['max_utm_vs_geodesic_relative_length_error'],.001)
        fwd=Transformer.from_crs(4326,32749,always_xy=True)
        x,y=fwd.transform(112.7285913,-7.3889859)
        self.assertLess(abs(x-self.bundle['origin_utm_m'][0]),1e-6)
        self.assertLess(abs(y-self.bundle['origin_utm_m'][1]),1e-6)

    def test_geographic_bounds_in_utm49s_area_of_use(self):
        for f in self.all:
            xmin,ymin,xmax,ymax=shape(f['geometry']).bounds
            self.assertTrue(108<=xmin<=xmax<=114)
            self.assertTrue(-80<=ymin<=ymax<=0)

    def test_main_and_frontage_distinct_both_main_directions(self):
        main=self.bundle['layers']['main_arterial_road'];frontage=self.bundle['layers']['frontage_road']
        self.assertTrue(main);self.assertTrue(frontage)
        self.assertFalse({f['properties']['osm_id'] for f in main}&{f['properties']['osm_id'] for f in frontage})
        self.assertEqual({f['properties']['approximate_direction'] for f in main},{'northward','southward'})
        self.assertTrue(all('frontage' in f['properties']['tags'].get('name','').lower() for f in frontage))

    def test_all_seven_function_classes_present(self):
        self.assertEqual(len({f['properties']['road_function'] for f in self.roads}),7)

    def test_missing_fields_stay_null(self):
        for f in self.roads:
            p=f['properties'];t=p['tags']
            for tag,field in [('lanes','lanes'),('width','width_m'),('maxspeed','maxspeed_kmh'),('oneway','oneway')]:
                if tag not in t:self.assertIsNone(p[field],f['id'])
            self.assertIsNone(p['capacity_vehicles_per_hour'])
            if 'oneway' not in t:self.assertEqual(p['movement_direction'],'unknown')

    def test_crossings_share_actual_road_rail_nodes_without_timing(self):
        for f in load('geodata/railways/level_crossings.geojson')['features']:
            p=f['properties'];self.assertTrue(p['shared_road_rail_node']);nid=p['osm_id']
            for wid in p['road_way_ids']+p['rail_way_ids']:self.assertIn(nid,self.ways[wid]['nodes'])
            for field in ['closure_duration_s','train_frequency_per_hour','schedule','physical_track_count']:self.assertIsNone(p[field])

    def test_core_is_within_context(self):
        fs=load('geodata/boundaries/study_areas.geojson')['features'];byid={f['id']:f for f in fs}
        self.assertTrue(shape(byid['boundary:context']['geometry']).buffer(1e-10).covers(shape(byid['boundary:core']['geometry'])))
        self.assertTrue(all(f['properties']['category']=='assumptions' for f in fs))

    def test_backbone_nodes_in_largest_component(self):
        largest=set(load('geodata/quality_assurance/components.json')['components'][0]['osm_node_ids'])
        for kind in ['main_arterial_road','frontage_road']:
            for f in self.bundle['layers'][kind]:self.assertTrue(set(f['properties']['osm_node_ids'])<=largest,f['id'])

    def test_source_reference_is_not_field_verification(self):
        for f in self.all:
            if f['properties']['category']=='research_reference':
                self.assertEqual(f['properties']['field_survey_check'],'Unverified')
                self.assertEqual(f['properties']['source_id'],'osm-gedangan-network')

    def test_web_data_identical_to_processed(self):
        for rel in ['processed/map-utm49s.json','processed/all_features.geojson','quality_assurance/quality_report.json','boundaries/study_areas.geojson']:
            path=ROOT/'geodata'/rel;web=ROOT/'frontend/public/geodata/m02'/path.name
            self.assertEqual(path.read_bytes(),web.read_bytes())

    def test_project_has_no_gedangan_sumo_network(self):
        self.assertEqual(list((ROOT/'simulation/networks').glob('*.net.xml')),[])
        for p in (ROOT/'traffic-data').glob('*/dataset.json'):
            self.assertTrue(all(not v for v in load(str(p.relative_to(ROOT))).values() if isinstance(v,list)))

if __name__=='__main__':unittest.main()
