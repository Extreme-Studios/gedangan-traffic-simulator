"""Explicit synthetic performance/reproduction evidence; never writes M06 data."""
import json,time,statistics,tracemalloc,re,http.client,threading,subprocess
from pathlib import Path
from unittest.mock import patch
from http.server import ThreadingHTTPServer
from .m085_survey import SurveyStore,uid,TRAINING
from .m085_export import export_session
from .m085_assets import audit
from .m085_baseline import digest,DOC,ROOT
from .m085_server import handler
STAMP='2026-01-01T07:00:00.000+07:00'
def fixed_fixture(folder):
 store=SurveyStore(folder,True)
 with patch('backend.gedangan.m085_survey.now',return_value=STAMP),patch('backend.gedangan.m085_export.now',return_value=STAMP):
  def cmd(a,p):return store.command(a,p,uid())
  cmd('observer_save',{'id':'FIXTURE_OBSERVER','name':'Synthetic software fixture','roles':['OBSERVER'],'training':TRAINING})
  s=cmd('session_save',{'id':'FIXTURE_SESSION','location_id':'MAIN_NB','observer_id':'FIXTURE_OBSERVER','source_class':'SYNTHETIC_TEST','start':STAMP,'end':'2026-01-01T07:15:00.000+07:00','direction':'northbound','approach':'MAIN_NB','method':'MANUAL_COUNT'})
  cmd('session_status',{'session_id':s['id'],'status':'READY'});cmd('session_status',{'session_id':s['id'],'status':'IN_PROGRESS'})
  for event_id,kind,data in [('FIXTURE_COUNT','COUNT',{'vehicle_class':'motorcycle'}),('FIXTURE_COVERAGE','COVERAGE',{'classes':['motorcycle','car'],'coverage_status':'COMPLETE','coverage_start':STAMP,'coverage_end':s['end']})]:
   cmd('event_add',{'session_id':s['id'],'event_id':event_id,'type':kind,'data':{'timestamp':'2026-01-01T07:00:10.000+07:00','direction':'northbound','approach':'MAIN_NB','movement':'straight','lane_group':'A','confidence':'HIGH',**data}})
  v=export_session(store,s['id']);folder=store.root/'exports'/v['id'];files={p.name:digest(p) for p in folder.iterdir() if p.suffix in ['.csv','.json'] and p.stem in ['traffic_count','queue','travel_time','signal','railway','geometry']}
  backup=store.backup();before=store.integrity();restored=store.restore(store.root/'backups'/(backup['id']+'.zip'),'RESTORE_AS_NEW_BRANCH');assert before['raw_events']==restored['integrity']['raw_events']==2
 return {'export':v,'contract_files':files,'backup':backup,'restored':restored,'root':str(store.root.relative_to(ROOT))}
def production_smoke():
 # A separate process runs the Python server only: no Vite/Node serves requests.
 import tempfile
 with tempfile.TemporaryDirectory(prefix='m085-http-') as folder:
  store=SurveyStore(folder,True);server=ThreadingHTTPServer(('127.0.0.1',0),handler(store,[]));port=server.server_port;server.RequestHandlerClass=handler(store,[port]);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();rows=[]
  try:
   html=(ROOT/'frontend/dist-m085/survey.html').read_text(encoding='utf-8');paths=['/survey.html']+re.findall(r'(?:src|href)="(/assets/[^"]+)"',html)+['/api/m085/state']
   for path in paths:
    c=http.client.HTTPConnection('127.0.0.1',port);c.request('GET',path,headers={'Accept-Encoding':'identity'});r=c.getresponse();body=r.read();assert r.status==200 and body;row={'path':path,'status':r.status,'bytes':len(body),'transport':r.getheader('Transfer-Encoding')}
    if path.startswith('/assets/'):assert body==(ROOT/'frontend/dist-m085'/path.lstrip('/')).read_bytes()
    if path=='/survey.html':row['CSP']=r.getheader('Content-Security-Policy');assert "connect-src 'self'" in row['CSP']
    rows.append(row);c.close()
  finally:server.shutdown();server.server_close();thread.join()
 return {'python_only_static_serving':True,'requests':rows,'browser_playback_QA':'PENDING_TOOL_BLOCK','external_resources_required':False,'internet_adapter_not_disabled':True}
def main():
 folder=ROOT/'data/surveys/m085/verification'/uid();folder.mkdir(parents=True);a=fixed_fixture(folder/'reproduction-A');b=fixed_fixture(folder/'reproduction-B');assert a['contract_files']==b['contract_files']
 store=SurveyStore(folder/'benchmark',True);s=store.command('demo_create',{},uid());latencies=[];tracemalloc.start();started=time.perf_counter()
 for i in range(3000):
  t=time.perf_counter();store.command('event_add',{'session_id':s['id'],'type':'COUNT','data':{'timestamp':s['start'],'vehicle_class':'motorcycle','direction':s['direction'],'approach':s['approach'],'movement':'straight','lane_group':'A'}},uid());latencies.append((time.perf_counter()-t)*1000)
 elapsed=time.perf_counter()-started;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop();t=time.perf_counter();page=store.ledger(s['id'],2950,50);paged_ms=(time.perf_counter()-t)*1000;assert len(page['events'])==50 and page['total']==3000
 integrity=store.integrity();value={'source_class':'SYNTHETIC_TEST','fixture_not_observed_Gedangan':True,'reproduction_A':a,'reproduction_B':b,'six_CSV_and_six_JSON_byte_equal':True,'package_ZIP_byte_equal_claimed':False,'reproduction_scope':'Fixed timestamps, event/session IDs and controlled software fixture. Volatile package IDs/audit UUIDs/ZIP times are excluded; no empirical reproducibility claim.','benchmark':{'committed_events':3000,'individual_SQLite_transactions':True,'elapsed_s':elapsed,'median_commit_ms':statistics.median(latencies),'p95_commit_ms':sorted(latencies)[int(len(latencies)*.95)],'paged_50_ms':paged_ms,'python_tracemalloc_peak_bytes':peak,'memory_scope':'Python allocations only, not OS/browser/video memory; no GPU benchmark claimed','integrity':integrity},'offline_server':production_smoke(),'M06_assets':len(audit()['assets']),'M09_started':False}
 DOC.mkdir(parents=True,exist_ok=True);(DOC/'verification.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'reproduction':True,'committed_events':3000,'elapsed_s':elapsed,'p95_ms':value['benchmark']['p95_commit_ms'],'static_server':'PASS','browser_QA':'PENDING_TOOL_BLOCK'}),flush=True)
if __name__=='__main__':main()
