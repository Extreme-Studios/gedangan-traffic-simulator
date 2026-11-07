import unittest,copy,json,xml.etree.ElementTree as E
from backend.gedangan.recovery_common import *
from backend.gedangan.recovery_data import build_demand,calendar,initialize
from backend.gedangan.recovery_network import build,validate
from backend.gedangan.recovery_routing import find_path,movements
class RecoveryContracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):initialize();cls.req={'date':'2026-08-04','time':'07:00','demand_mode':'REFERENCE_ESTIMATE','acknowledge_estimate':True,'horizon_s':900,'warmup_s':300,'seed':42,'scenario':{'id':'S00'}}
 def test_exact_date_missing_not_another_run(self):
  with self.assertRaisesRegex(ValueError,'MISSING'):build_demand({'date':'2026-05-05','time':'16:00'})
 def test_unsupported_evening_and_night_missing(self):
  for hour in ['16:00','18:00','21:00']:
   with self.assertRaisesRegex(ValueError,'MISSING'):build_demand({**self.req,'time':hour})
 def test_estimate_acknowledgement_required(self):
  with self.assertRaises(ValueError):build_demand({**self.req,'acknowledge_estimate':False})
 def test_07_17_and_weekend_actual_demand_different(self):
  a=build_demand(self.req);b=build_demand({**self.req,'time':'17:00'});c=build_demand({**self.req,'date':'2026-08-02'});self.assertNotEqual(a['cohort_sha256'],b['cohort_sha256']);self.assertNotEqual(a['requested'],c['requested'])
 def test_warmup_and_WIB_elapsed_separated(self):
  d=build_demand(self.req);self.assertEqual(d['elapsed_zero_wib'],'2026-08-04T06:55:00+07:00');self.assertEqual(d['measurement_start_wib'],'2026-08-04T07:00:00+07:00');self.assertGreater(d['warmup_requested'],0);self.assertEqual(d['requested'],sum(r['requested']for r in d['ledger']))
 def test_day_selection_and_year(self):
  self.assertEqual(calendar({'date':'2026-08-02','time':'07:00'})['day_type'],'WEEKEND');self.assertEqual(calendar({'date':'2030-01-01','time':'17:00'})['year'],2030)
 def test_repeat_same_seed_same_cohort(self):self.assertEqual(build_demand(self.req),build_demand(self.req))
 def test_all_demand_retained_when_increased(self):
  a=build_demand(self.req);b=build_demand({**self.req,'demand_scale':1.4});self.assertGreater(b['requested'],a['requested']);self.assertEqual(len(b['requests']),b['requested']);self.assertEqual(sum(r['requested']for r in b['ledger']),b['requested'])
 def test_no_flyover_without_concept_ack(self):
  with self.assertRaises(ValueError):validate({'id':'S06A'})
 def test_no_invented_second_signal(self):
  with self.assertRaisesRegex(ValueError,'BLOCKED'):validate({'id':'S05'})
 def test_signal_derivative_really_changes_tl(self):
  p,m=build({'id':'S01','green_s':25});r=E.parse(p/'network.net.xml').getroot();t=next(t for t in r.findall('tlLogic')if t.get('id')=='m05_gedangan');self.assertTrue(all(float(v.get('duration'))==25 for v in t.findall('phase')if any(c in'gG'for c in v.get('state'))));self.assertNotEqual(m['network_sha256'],sha(PARENT))
 def test_flyovers_distinct_network_and_lanes(self):
  a,ma=build({'id':'S06A','acknowledge_concept':True});b,mb=build({'id':'S06B','acknowledge_concept':True});self.assertNotEqual(ma['network_sha256'],mb['network_sha256']);self.assertEqual(len(ma['new_edges']),6);self.assertEqual(len(E.parse(a/'network.net.xml').getroot().find("edge[@id='recovery_fo_nb_1']").findall('lane')),1);self.assertEqual(len(E.parse(b/'network.net.xml').getroot().find("edge[@id='recovery_fo_nb_1']").findall('lane')),2)
 def test_oversize_still_denied_and_trailer_no_concept(self):
  p,_=build({'id':'S06A','acknowledge_concept':True});ends=movements()['northbound'];r,info=find_path(p/'network.net.xml',ends['origin_edge'],ends['destination_edge'],'oversize');self.assertIsNone(r);r,info=find_path(p/'network.net.xml',ends['origin_edge'],ends['destination_edge'],'trailer');self.assertFalse(r and any(e.startswith('recovery_fo_')for e in r))
 def test_frontage_no_heavy_permission_expansion(self):
  ends=movements()['frontage_continuity'];r,why=find_path(PARENT,ends['origin_edge'],ends['destination_edge'],'heavy_truck');self.assertIsNone(r)
if __name__=='__main__':unittest.main(verbosity=2)
