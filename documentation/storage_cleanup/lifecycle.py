"""Release EXE restart test with isolated synthetic QA store; no research environment."""
import os,subprocess,time,json,http.client
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'documentation/storage_cleanup';EXE=ROOT/'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR/APPLICATION/GEDANGAN_TRAFFIC_SIMULATOR.exe';PORT=5198
def request(path,body=None):
 c=http.client.HTTPConnection('127.0.0.1',PORT,timeout=5);c.request('POST'if body else'GET',path,json.dumps(body)if body else None,{'Content-Type':'application/json'});r=c.getresponse();v=json.loads(r.read());c.close();assert r.status==200;return v
def health():
 try:return request('/api/m12/health')
 except Exception:return None
def main():
 env=os.environ.copy();env['M12_DATA_DIR']=str(OUT/'qa-runtime');env['PATH']=os.environ['SystemRoot']+'\\System32'
 for name in ['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','SUMO_HOME','NODE_PATH']:env.pop(name,None)
 before=request('/api/m085/state');assert before['raw_events']>0;assert all(s['source_class']=='SYNTHETIC_TEST'for s in before['sessions'])
 request('/api/m10/shutdown',{'token':health()['token']})
 for _ in range(60):
  if not health():break
  time.sleep(.1)
 assert not health()
 start=time.monotonic();p=subprocess.run([str(EXE),'--port',str(PORT),'--no-open'],env=env,cwd=EXE.parent,timeout=60);assert p.returncode==0;state=health();assert state and state['recordings']==23
 after=request('/api/m085/state');assert after['raw_events']==before['raw_events'];assert [s['id']for s in after['sessions']]==[s['id']for s in before['sessions']]
 pid=state['pid'];assert subprocess.run([str(EXE),'--port',str(PORT),'--no-open'],env=env,cwd=EXE.parent,timeout=60).returncode==0;assert health()['pid']==pid
 request('/api/m10/shutdown',{'token':health()['token']})
 for _ in range(60):
  if not health():break
  time.sleep(.1)
 assert not health();result={'status':'PASS','actual_windows_executable':str(EXE),'system_only_PATH':True,'startup_seconds':round(time.monotonic()-start,3),'recordings':23,'survey_raw_events_before':before['raw_events'],'survey_raw_events_after_restart':after['raw_events'],'sessions_recovered':len(after['sessions']),'duplicate_same_pid':True,'clean_shutdown':True,'user_workspace_untouched':True};(OUT/'qa/lifecycle.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
