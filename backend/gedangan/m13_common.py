"""M13 is additive: old observations, runs and release are read-only inputs."""
from pathlib import Path
from datetime import datetime,date,timedelta,timezone
import json,hashlib,sqlite3
from contextlib import contextmanager
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/'documentation/m13';DATA=ROOT/'data/historical/m13';DB=DATA/'historical.sqlite'
START=date(2026,8,1);END=date(2026,10,31)
CLASSES=['motorcycle','car','pickup_van','minibus','bus','light_truck','medium_truck','heavy_truck','trailer','oversize']
TYPES=['OBSERVED_PRIMARY','OBSERVED_SECONDARY','REFERENCE_STUDY','SIMULATION_OUTPUT','SYNTHETIC_TEST','MISSING']
METRICS=['vehicle_count','turning_movement','speed','queue_length','travel_time']
def now():return datetime.now(timezone.utc).isoformat()
def save(path,data):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def load(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def identity(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()
@contextmanager
def connect(path=DB,readonly=False):
 c=sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro' if readonly else str(path),uri=readonly,timeout=15);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON')
 try:
  yield c
  if not readonly:c.commit()
 except Exception:
  if not readonly:c.rollback()
  raise
 finally:c.close()
