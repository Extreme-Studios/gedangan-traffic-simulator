"""Foundation acceptance tests. Synthetic fixtures are tests, not Gedangan data."""
import copy
import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.server import ThreadingHTTPServer
from backend.server import Handler
from backend.gedangan.simulation_controller import SimulationController, EngineNotConnected
from backend.gedangan.metrics_collector import MetricsCollector
from backend.gedangan.traffic_network import TrafficNetwork
from backend.gedangan.vehicle_demand import VehicleDemand
from configuration.validate_data import ROOT, load, validate_dataset
from jsonschema import ValidationError

class DataContractTests(unittest.TestCase):
    def setUp(self):
        self.data=load(ROOT/'traffic-data/assumptions/dataset.json')

    def record(self):
        self.data['data_provenance']=[{'id':'test-source','category':'assumptions','source_title':'Synthetic test fixture only','source_uri':'urn:test','source_year':None,'accessed_on':'2026-10-31','survey_period':None,'method':None,'spatial_scope':None,'license_notes':None,'verification_status':'unverified','limitations':'Not traffic data'}]
        self.data['road_nodes']=[{'id':'test-node','category':'assumptions','provenance_id':'test-source','calibration_status':'unverified','x_m':None,'y_m':None,'crs':None,'zone_id':None}]

    def test_all_categories_validate(self):
        for p in (ROOT/'traffic-data').glob('*/dataset.json'):validate_dataset(load(p))

    def test_wrong_baseline_rejected(self):
        self.data['baseline_year']=2025
        with self.assertRaises(ValidationError):validate_dataset(self.data)

    def test_missing_provenance_rejected(self):
        self.record();self.data['data_provenance']=[]
        with self.assertRaises(ValueError):validate_dataset(self.data)

    def test_categories_cannot_be_mixed(self):
        self.record();self.data['road_nodes'][0]['category']='observed_data'
        with self.assertRaises(ValueError):validate_dataset(self.data)

    def test_duplicate_ids_rejected(self):
        self.record();self.data['road_nodes'].append(copy.deepcopy(self.data['road_nodes'][0]))
        with self.assertRaises(ValueError):validate_dataset(self.data)

    def test_unknown_field_rejected(self):
        self.data['fake_capacity']=123
        with self.assertRaises(ValidationError):validate_dataset(self.data)

    def test_broken_reference_rejected(self):
        self.record();self.data['road_nodes'][0]['zone_id']='nonexistent'
        with self.assertRaises(ValueError):validate_dataset(self.data)

    def test_null_geometry_valid_but_unverified(self):
        self.record();validate_dataset(self.data)
        with self.assertRaises(ValueError):TrafficNetwork(nodes=self.data['road_nodes']).require_verified()

    def test_missing_growth_never_defaults_zero(self):
        with self.assertRaises(ValueError):VehicleDemand().rate_for(2027,'test-class','test-zone')

    def test_growth_requires_documentation_and_unique_key(self):
        row={'year':2027,'vehicle_class_id':'test-class','zone_id':'test-zone','annual_rate':0.0,'provenance_id':None}
        d=VehicleDemand(growth_rates=[row])
        with self.assertRaises(ValueError):d.rate_for(2027,'test-class','test-zone')
        row['provenance_id']='test-source'
        self.assertEqual(d.rate_for(2027,'test-class','test-zone'),0)
        d.growth_rates.append(copy.deepcopy(row))
        with self.assertRaises(ValueError):d.rate_for(2027,'test-class','test-zone')

    def test_nonfinite_and_invalid_growth_rejected(self):
        for rate in [float('nan'),float('inf'),-1.1,True]:
            d=VehicleDemand(growth_rates=[{'year':2027,'vehicle_class_id':'c','zone_id':'z','annual_rate':rate,'provenance_id':'p'}])
            with self.assertRaises(ValueError):d.rate_for(2027,'c','z')

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.base=f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()

    def get(self,path):
        with urlopen(self.base+path,timeout=3) as response:
            self.assertEqual(response.headers['Cache-Control'],'no-store')
            return json.load(response)

    def test_health_is_not_simulation(self):
        self.assertFalse(self.get('/api/health')['simulation_running'])

    def test_status_never_claims_connected(self):
        s=self.get('/api/status');self.assertEqual(s['engine'],'ENGINE NOT CONNECTED');self.assertEqual(s['baseline_year'],2026);self.assertFalse(s['network_loaded'])

    def test_metrics_are_unknown_not_zero(self):
        s=self.get('/api/metrics');self.assertIsNone(s['queue_length_m']);self.assertIsNone(s['capacity_vehicles_per_hour']);self.assertIsNone(s['run_id'])

    def test_config(self):
        self.assertEqual(self.get('/api/config')['growth']['rates'],[])

    def test_unknown_endpoint(self):
        with self.assertRaises(HTTPError) as e:self.get('/api/does-not-exist')
        self.assertEqual(e.exception.code,404)

    def test_simulation_start_rejected(self):
        with self.assertRaises(HTTPError) as e:urlopen(Request(self.base+'/api/simulation/start',data=b'{}',method='POST'),timeout=3)
        self.assertEqual(e.exception.code,409)

    def test_controller_blocks_start_and_step(self):
        for action in [SimulationController().start,SimulationController().step]:
            with self.assertRaises(EngineNotConnected):action()

if __name__ == '__main__':unittest.main()
