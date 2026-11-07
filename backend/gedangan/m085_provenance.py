"""Survey evidence gates and explicit clocks. No promotion of synthetic inputs."""
import json,hashlib,re,math
from datetime import datetime,timedelta,timezone
JAKARTA=timezone(timedelta(hours=7));SOURCES=['OBSERVED_FIELD','VIDEO_OBSERVATION','OFFICIAL_ADMINISTRATIVE','PUBLISHED_RESEARCH','ENGINEERING_REFERENCE','ASSUMPTION','SYNTHETIC_TEST','SIMULATED_RESULT','MISSING']
def now():return datetime.now(JAKARTA).isoformat(timespec='milliseconds')
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
def fingerprint(value):return hashlib.sha256(canonical(value).encode()).hexdigest()
def identifier(value):
 if not isinstance(value,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,99}',value):raise ValueError('ID harus sederhana, maksimal100 karakter')
 return value
def clock(value):
 if not isinstance(value,str):raise ValueError('Timestamp pengamatan belum tersedia')
 t=datetime.fromisoformat(value)
 if t.utcoffset()!=timedelta(hours=7):raise ValueError('Timestamp wajib eksplisit +07:00 / Asia/Jakarta')
 return t
def number(value,label,minimum=0,nullable=True):
 if value is None and nullable:return None
 if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<minimum:raise ValueError(label+' harus angka finite dalam satuan yang dinyatakan')
 return value
def text(value,label):
 if not isinstance(value,str) or not value.strip():raise ValueError(label+' wajib diisi')
 return value.strip()
def interval(t):
 d=clock(t);start=d.replace(minute=d.minute//15*15,second=0,microsecond=0);return start.isoformat(),(start+timedelta(minutes=15)).isoformat()
def gate_source(session,review,media=None):
 source=session['source_class']
 if source=='SYNTHETIC_TEST':return 'DEMO_SYNTHETIC'
 if source not in ['OBSERVED_FIELD','VIDEO_OBSERVATION']:raise ValueError('Sumber referensi/asumsi/simulasi bukan pengamatan lapangan M06')
 if not review or review.get('decision')!='APPROVED' or not review.get('human_reviewed') or not review.get('field_evidence_verified'):raise ValueError('Pengamatan belum lolos review manusia dan pemeriksaan bukti lapangan')
 if source=='VIDEO_OBSERVATION' and (not media or not media.get('recording_start') or not media.get('permission_confirmed')):raise ValueError('VIDEO_TIME_ONLY atau izin video belum lengkap; tidak mengarang jam pengamatan')
 return 'OBSERVED_FIELD'
