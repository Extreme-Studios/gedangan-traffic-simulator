"""Isolated SQLite software fixtures; never inserted into research evidence."""
import unittest,tempfile,sqlite3,json
from pathlib import Path
from unittest.mock import patch
from contextlib import closing
from backend.gedangan import recovery_data as d
from backend.gedangan.recovery_observed import lookup
from backend.gedangan.recovery_routing import movements

class ObservedLookup(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.db=Path(self.tmp.name)/'test.sqlite'
  with closing(sqlite3.connect(d.DB))as original,closing(sqlite3.connect(self.db))as target:original.backup(target)
 def insert(self,review=True,od='local_trip',origin=None):
  ends=movements()[od];p={'od_id':od,'review':{k:review for k in ['source_evidence_verified','quality_reviewed','network_endpoints_verified']}}
  with closing(sqlite3.connect(self.db))as c:
   c.execute('INSERT INTO evidence VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',('isolated_software_fixture','2026-08-04','WEEKDAY','07:00','07:15',900,'ISOLATED_TEST_ONLY','NB',origin or ends['origin_edge'],ends['destination_edge'],'car','traffic_count',30,'vehicles/interval','OBSERVED','ISOLATED_TEST_NOT_REAL',2026,json.dumps(p)));c.commit()
 def test_missing_real_2026_fails_closed(self):
  with self.assertRaisesRegex(ValueError,'MISSING'):lookup(self.db,'2026-08-04','07:00')
 def test_unreviewed_observation_rejected(self):
  self.insert(False)
  with self.assertRaisesRegex(ValueError,'MISSING'):lookup(self.db,'2026-08-04','07:00')
 def test_reviewed_interval_lookup_and_demand(self):
  self.insert();self.assertEqual(lookup(self.db,'2026-08-04','07:05')[0]['veh_per_hour'],120)
  with patch.object(d,'DB',self.db):
   result=d.build_demand({'date':'2026-08-04','time':'07:00','horizon_s':900,'warmup_s':0})
  self.assertEqual(result['requested'],30);self.assertEqual(result['ledger'][0]['status'],'OBSERVED')
  with self.assertRaisesRegex(ValueError,'MISSING'):lookup(self.db,'2026-08-04','07:15')
 def test_verified_flag_cannot_substitute_actual_OD_endpoints(self):
  self.insert(origin='not_a_real_edge')
  with patch.object(d,'DB',self.db),self.assertRaisesRegex(ValueError,'endpoints'):d.build_demand({'date':'2026-08-04','time':'07:00','horizon_s':900,'warmup_s':0})
