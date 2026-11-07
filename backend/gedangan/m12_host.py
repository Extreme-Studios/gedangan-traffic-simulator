"""Frozen offline release host. Earlier engine, renderer and survey contracts reused."""
import sys,os,json,secrets,threading,argparse,subprocess,time,webbrowser,http.client,hashlib,csv,io,traceback,socket
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from http.server import ThreadingHTTPServer
APP=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(os.environ.get('M12_APP_ROOT',Path(__file__).resolve().parents[2]/'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/APPLICATION'))
from . import m04_demand
m04_demand.ROOT=APP;m04_demand.CONF=APP/'configuration/demand-m04'
from . import m10_server as host
host.ROOT=APP;host.BASE_OUT=APP/'presentation_demo/m09';host.CACHE=host.BASE_OUT/'cache'
from . import m085_server as survey
from .m085_survey import SurveyStore
VERSION='1.0.0';RELEASE='PRESENTATION-READY ILLUSTRATIVE RELEASE'
DATA=Path(os.environ.get('M12_DATA_DIR',str(APP.parent/'USER_DATA')))
host.OUT=DATA/'runtime'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def report_data(q):
 rows=load(APP/'release/audit.json')['rows'];rid=q.get('run',[None])[0]
 a=next((r for r in rows if r['run_id']==rid),None)
 if not a:raise ValueError('Run ID tidak tersedia; pilih rekaman aktual.')
 b=next((r for r in rows if r['year']==a['year'] and r['demand_type']==a['demand_type'] and r['scenario']=='S00'),None)
 if b and (b['cohort_sha256']!=a['cohort_sha256'] or b['seed']!=a['seed'] or b['horizon_s']!=a['horizon_s']):raise ValueError('Pasangan cohort/seed/horizon tidak sesuai')
 return {'produk':'GEDANGAN TRAFFIC SIMULATOR','versi':VERSION,'status_rilis':RELEASE,'jenis':q.get('kind',['technical'])[0],'klasifikasi':'HASIL SIMULASI ILUSTRATIF, BUKAN PENGUKURAN GEDANGAN','baseline_empiris':'BLOCKED - DATA REQUIRED','selected':a,'baseline':b,'delta_arrived':a['metrics']['arrived']-b['metrics']['arrived'] if b else None,'batasan':['Demand belum dikalibrasi; single seed 42; horizon 2100 detik.','Failed routes berbeda dari running at end. Not arrived = requested - arrived.','Flyover/underpass CONCEPT ONLY; tidak ada klaim kelayakan atau efektivitas lapangan.','Paket memutar jejak SUMO 1.28.0 yang direkam; tidak menjalankan SUMO live.']}
def pdf_bytes(d):
 from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
 from reportlab.lib.styles import getSampleStyleSheet
 from reportlab.lib import colors
 from reportlab.graphics.shapes import Drawing,Rect,String
 from xml.sax.saxutils import escape
 out=io.BytesIO();styles=getSampleStyleSheet();story=[]
 def p(s,sty='Normal'):story.append(Paragraph(escape(str(s)),styles[sty]));story.append(Spacer(1,8))
 p('GEDANGAN TRAFFIC SIMULATOR','Title');p('Laporan '+{'executive':'Eksekutif','technical':'Teknis','comparison':'Perbandingan'}.get(d['jenis'],'Teknis'),'Heading1');p('EXTREME STUDIOS | v'+VERSION);p(d['klasifikasi']);a=d['selected'];p(f"Tahun {a['year']} | {a['demand_type']} | {a['scenario']} | Run {a['run_id']}");p('Baseline empiris: '+d['baseline_empiris'])
 names={'requested':'Diminta','routable':'Rute tersedia','failed_routes':'Rute gagal','departed':'Berangkat','arrived':'Tiba','running_at_end':'Masih berjalan','not_departed':'Belum berangkat','unserved_total_at_horizon':'Belum tiba total','waiting_s':'Rata-rata tunggu (detik)','max_lane_queue_extent_m':'Maksimum extent antrean (m)','verified_in_model_spillback':'Spillback dalam model'}
 data=[['Metrik','Baseline S00','Pilihan']]
 for k,label in names.items():data.append([label,str(round(d['baseline']['metrics'].get(k,0),3)) if d['baseline'] else '-',str(round(a['metrics'].get(k,0),3))])
 t=Table(data,colWidths=[255,110,110],repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#d6e8e5')),('GRID',(0,0),(-1,-1),.3,colors.grey),('FONTSIZE',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),7)]));story.extend([t,Spacer(1,14)])
 p('Grafik kendaraan tiba','Heading2');g=Drawing(460,100);vals=[d['baseline']['metrics']['arrived'] if d['baseline'] else 0,a['metrics']['arrived']];mx=max(vals+[1])
 for i,v in enumerate(vals):g.add(Rect(100,60-i*40,300*v/mx,22,fillColor=colors.HexColor('#317e78')));g.add(String(0,67-i*40,['Baseline','Pilihan'][i],fontSize=10));g.add(String(410,67-i*40,str(v),fontSize=10))
 story.append(g);p('Perubahan tiba: '+str(d['delta_arrived'])+' kendaraan. Nilai negatif berarti lebih sedikit tiba dalam horizon yang sama.')
 if d['jenis']!='executive':
  p('Provenance dan kontrak','Heading2')
  for key in ['horizon_s','seed','network_sha256','cohort_sha256','source_index_sha256']:p(key+': '+str(a[key]))
  p('Kelas kendaraan: '+', '.join(v['id'] for v in host.load(host.CACHE/'catalog.json')['registry']));p('Requested = Routable + Failed routes; Routable = Departed + Not departed; Departed = Arrived + Running at end; Not arrived = Requested - Arrived.');p('Jejak FCD 0,5 detik; kontrol signal/rail 1 detik; alignment +0,5 detik. Queue extent adalah diagnostik model dengan censoring, bukan pengukuran lapangan.')
 else:
  p('Provenance ringkas','Heading2');p('Horizon: '+str(a['horizon_s'])+' detik; seed '+str(a['seed'])+'. Network SHA-256: '+a['network_sha256']);p('Demand/cohort SHA-256: '+a['cohort_sha256']);p('Kelas model: '+', '.join(v['id'] for v in host.load(host.CACHE/'catalog.json')['registry'])+'. Registry dan pembatasan akses dipertahankan; oversize tidak diberi bypass.')
 p('Batasan dan validitas','Heading2')
 for v in d['batasan']:p(v)
 SimpleDocTemplate(out,title='Laporan Teknis Gedangan',author='EXTREME STUDIOS',leftMargin=45,rightMargin=45,topMargin=40,bottomMargin=45).build(story)
 return out.getvalue()
def handler(port,token,catalog,store):
 Base=host.handler(port,token,catalog);Survey=survey.handler(store,[port])
 class Handler(Base):
  body=Survey.body
  def file(self,path,attachment=False):
   path=Path(path)
   if path.name=='survey.html' and path.is_file():
    data=path.read_bytes().replace(b'</head>',b'<link rel="stylesheet" href="/release/survey.css"><script defer src="/release/survey.js"></script></head>')
    return self.send(data,'text/html; charset=utf-8')
   return Survey.file(self,path,attachment)
  def send_header(self,k,v):
   if k.lower()=='content-security-policy':
    v=v.replace("frame-ancestors 'none'","frame-ancestors 'self'")
    if 'media-src' not in v:v+="; media-src 'self' blob:"
    if 'frame-src' not in v:v+="; frame-src 'self'"
   return super().send_header(k,v)
  def send(self,data,kind='application/json; charset=utf-8',status=200,encoding=None):
   if kind.startswith('text/html') and status==200 and b'/assets/' in data and b'visual' in data:
    data=data.replace(b'</head>',b'<link rel="stylesheet" href="/presenter.css"><link rel="stylesheet" href="/release/embed.css"><script src="/quality.js"></script></head>')
   return super().send(data,kind,status,encoding)
  def do_GET(self):
   if not self.allowed():return self.reply({'error':'Host/Origin ditolak'},403)
   parsed=urlparse(self.path);path=parsed.path;q=parse_qs(parsed.query)
   try:
    if path=='/api/m12/health':return self.reply({'service':'gedangan-release-m12','version':VERSION,'token':token,'root_id':hashlib.sha256(str(APP).encode()).hexdigest(),'recordings':len(catalog['runs']),'pid':os.getpid()})
    if path=='/api/m12/audit':return self.reply(load(APP/'release/audit.json'))
    if path=='/api/m12/export':
     d=report_data(q);fmt=q.get('format',['json'])[0]
     if fmt=='pdf':return self.send(pdf_bytes(d),'application/pdf')
     if fmt=='json':return self.send(json.dumps(d,ensure_ascii=False,indent=2).encode(),'application/json')
     if fmt!='csv':raise ValueError('Format laporan tidak didukung')
     stream=io.StringIO();w=csv.writer(stream);w.writerow(['run_id','year','growth','scenario','metric','value','baseline_value','delta','classification','network_sha256','cohort_sha256'])
     for k,v in d['selected']['metrics'].items():
      before=d['baseline']['metrics'].get(k) if d['baseline'] else None;delta=v-before if type(v)in [int,float] and type(before)in [int,float] else None
      w.writerow([d['selected']['run_id'],d['selected']['year'],d['selected']['demand_type'],d['selected']['scenario'],k,v,before,delta,d['klasifikasi'],d['selected']['network_sha256'],d['selected']['cohort_sha256']])
     return self.send(('\ufeff'+stream.getvalue()).encode(),'text/csv; charset=utf-8')
    if path.startswith('/api/m085/'):return Survey.do_GET(self)
    if path in ['/app','/app/']:return self.file(APP/'release/index.html')
    if path.startswith('/release/'):folder=APP/'release';rel=path[9:]
    elif path.startswith('/presentation/'):folder=APP/'presentation_demo/m11';rel=path[14:]
    elif path=='/presenter.css':folder=APP/'presentation_demo/m11/assets';rel='presenter.css'
    elif path=='/quality.js':folder=APP/'release';rel='quality.js'
    elif path=='/survey.html':return self.file(APP/'frontend/dist-m085/survey.html')
    elif path.startswith('/assets/') and not (APP/'frontend/dist-m10'/path.lstrip('/')).is_file():folder=APP/'frontend/dist-m085';rel=path.lstrip('/')
    else:return super().do_GET()
    target=(folder/rel).resolve()
    if not target.is_relative_to(folder.resolve()):return self.reply({'error':'Path tidak valid'},403)
    return self.file(target)
   except (ValueError,KeyError,StopIteration) as e:return self.reply({'error':str(e)},400)
   except Exception as e:return self.reply({'error':'Layanan tidak dapat menyelesaikan permintaan: '+str(e)},500)
  def do_POST(self):
   if self.path.startswith('/api/m085/'):return Survey.do_POST(self)
   return super().do_POST()
 return Handler
def connect(port):
 try:
  c=http.client.HTTPConnection('127.0.0.1',port,timeout=1);c.request('GET','/api/m12/health');r=c.getresponse();v=json.loads(r.read());c.close();return v if v.get('service')=='gedangan-release-m12' else None
 except Exception:return None
def verify():
 manifest=load(APP/'release/runtime-manifest.json')
 for p,h in manifest.items():
  target=(APP/p).resolve()
  if not target.is_relative_to(APP.resolve()) or not target.is_file() or host.digest(target)!=h:raise ValueError('Berkas aplikasi rusak atau tidak lengkap: '+p)
 return host.preflight()
def serve(port):
 catalog=verify();DATA.mkdir(parents=True,exist_ok=True);host.OUT.mkdir(parents=True,exist_ok=True)
 store=SurveyStore(DATA/'surveys',False);token=secrets.token_urlsafe(32)
 server=ThreadingHTTPServer(('127.0.0.1',port),handler(port,token,catalog,store))
 try:server.serve_forever()
 finally:server.server_close()
def main():
 p=argparse.ArgumentParser();p.add_argument('--serve',action='store_true');p.add_argument('--stop',action='store_true');p.add_argument('--no-open',action='store_true');p.add_argument('--port',type=int,default=5192);p.add_argument('--page',default='app');a=p.parse_args();DATA.mkdir(parents=True,exist_ok=True)
 try:
  if a.serve:return serve(a.port)
  state=connect(a.port)
  if state and state['root_id']!=hashlib.sha256(str(APP).encode()).hexdigest():raise RuntimeError('Port digunakan salinan Gedangan lain. Tutup salinan itu melalui aplikasinya dahulu.')
  if a.stop:
   if state:
    c=http.client.HTTPConnection('127.0.0.1',a.port);body=json.dumps({'token':state['token']});c.request('POST','/api/m10/shutdown',body,{'Content-Type':'application/json'});r=c.getresponse();r.read();c.close()
   return
  verify()
  if not state:
   with socket.socket() as probe:
    probe.settimeout(.5)
    if probe.connect_ex(('127.0.0.1',a.port))==0:raise RuntimeError('Port sedang dipakai aplikasi lain. Aplikasi itu tidak dihentikan. Tutup aplikasi yang memakai port atau pilih port lain.')
   cmd=[sys.executable]+([] if getattr(sys,'frozen',False) else ['-m','backend.gedangan.m12_host'])+['--serve','--no-open','--port',str(a.port)]
   log=(DATA/'runtime-launch.log').open('ab');child=subprocess.Popen(cmd,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0);log.close()
   for _ in range(100):
    state=connect(a.port)
    if state:break
    if child.poll()is not None:raise RuntimeError('Layanan berhenti saat startup. Port mungkin sedang ditahan Windows; pilih port lain atau coba lagi setelah port dilepas.')
    time.sleep(.2)
   if not state:raise RuntimeError('Layanan belum siap. Periksa kelengkapan paket atau port yang sedang dipakai.')
  if not a.no_open:webbrowser.open(f'http://127.0.0.1:{a.port}/'+('survey.html' if a.page=='survey' else 'app#presentation' if a.page=='presentation' else 'app'))
  (DATA/'last-start.json').write_text(json.dumps({'status':'READY','health':state,'version':VERSION},indent=2))
 except Exception as e:
  (DATA/'last-error.txt').write_text(traceback.format_exc(),encoding='utf-8')
  if not a.no_open and not a.serve and os.name=='nt':
   import ctypes
   ctypes.windll.user32.MessageBoxW(None,'Gedangan belum dapat dibuka. '+str(e)+'\nEkstrak ulang seluruh paket. Catatan tersimpan di USER_DATA/last-error.txt.','Gedangan Traffic Simulator',16)
  raise SystemExit(1)
if __name__=='__main__':main()
