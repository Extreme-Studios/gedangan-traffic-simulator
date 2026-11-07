"""Reference-only local media; hashing is streamed and replay identity is anonymous."""
import hashlib,re
from datetime import timedelta
from pathlib import Path
from .m085_provenance import clock,number,text
def hash_file(path):
 p=Path(path)
 if not p.is_absolute() or p.suffix.lower() not in ['.mp4','.m4v','.webm','.mov','.jpg','.jpeg','.png']:raise ValueError('Pilih path absolut video/foto lokal yang didukung')
 before=p.stat();h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 after=p.stat()
 if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise ValueError('Berkas berubah selama hashing; pilih ulang')
 return {'filename':p.name,'size':after.st_size,'sha256':h.hexdigest(),'local_path':str(p),'hash_method':'BACKEND_STREAMED_1MiB'}
def validate_media(p):
 allowed={'id','filename','size','sha256','duration_s','fps','recording_start','clock_offset_s','timezone','permission_confirmed','camera_id','hash_method','local_path','kind','notes','last_modified'}
 if set(p)-allowed:raise ValueError('Metadata saja; video/frame/identitas tidak boleh disimpan di database')
 if len(p.get('filename',''))>512 or len(p.get('notes','') or '')>4000:raise ValueError('Metadata media terlalu panjang')
 text(p.get('filename'),'Nama berkas')
 if not re.fullmatch('[a-f0-9]{64}',p.get('sha256','')):raise ValueError('SHA256 asli wajib dihitung sebelum anotasi')
 number(p.get('size'),'Ukuran berkas',nullable=False);number(p.get('duration_s'),'Durasi video',nullable=False);number(p.get('fps'),'FPS',minimum=.001)
 if p.get('recording_start'):clock(p['recording_start'])
 if p.get('clock_offset_s') is not None:number(p['clock_offset_s'],'Offset clock',minimum=-86400)
 return {**p,'timezone':'Asia/Jakarta','time_status':'KNOWN_RECORDING_CLOCK' if p.get('recording_start') else 'VIDEO_TIME_ONLY','automatic_detection':False,'original_file_uploaded':False}
def observation_time(media,seconds):
 number(seconds,'Posisi video',nullable=False)
 if seconds>media['duration_s']+.001:raise ValueError('Timestamp melewati durasi video')
 if not media.get('recording_start'):return None
 return (clock(media['recording_start'])+timedelta(seconds=seconds+(media.get('clock_offset_s') or 0))).isoformat(timespec='milliseconds')
def anonymous_token(value):
 if not re.fullmatch(r'ANON_[a-f0-9-]{8,36}',value or ''):raise ValueError('Gunakan token acak anonim, bukan pelat atau identitas pengemudi')
 return value
