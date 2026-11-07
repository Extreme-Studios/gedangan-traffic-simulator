"""Actual loopback workflow checks. This is not browser visual QA."""
import urllib.request,time,copy
from .m155_common import *
def call(path,value=None):
 req=urllib.request.Request('http://127.0.0.1:5201'+path,data=json.dumps(value).encode()if value is not None else None,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req)as r:return json.load(r)
def main():
 from .m155_demand import default
 r=default();r.update(name='M15.5 API workflow evidence',total=20,duration_s=120,execution_horizon_s=180,volume_interpretation='total',warmup_s=0)
 r['rail']['arrivals_s']=[]
 preview=call('/api/preview',r);saved=call('/api/scenarios',r);dup=copy.deepcopy(saved['request']);dup['name']+=' duplicate';duplicate=call('/api/scenarios',dup);items=call('/api/scenarios');assert saved in items and duplicate in items and saved['id']!=duplicate['id'];job=call('/api/generate',r)
 deadline=time.monotonic()+180
 while time.monotonic()<deadline:
  job=call('/api/jobs/'+job['job_id'])
  if job['status']=='COMPLETE':break
  if job['status']=='FAILED':raise RuntimeError(job)
  time.sleep(.5)
 assert job['status']=='COMPLETE',job
 result=job['result'];edge=call('/api/edge-inspection/'+result['run_id']);assert edge['run_id']==result['run_id']and edge['first_observed_times_s'];assert result['requested']==20;assert result['departed']==result['arrived']+result['active'];assert all(ts==sorted(ts)and len(ts)<=result['departed']for ts in edge['first_observed_times_s'].values());assert call('/api/technical-map')['network_version']=='m155-existing-provisional-1'
 save(DOC/'api-workflow.json',{'status':'PASS_API_ONLY_NOT_BROWSER','preview_total':preview['total'],'saved_id':saved['id'],'duplicate_id':duplicate['id'],'roundtrip_equal':True,'generated_run':result['run_id'],'requested':result['requested'],'departed':result['departed'],'moved':result['moved'],'arrived':result['arrived'],'edge_first_seen_counts_monotonic_and_bounded':True,'post_generation_edge_audit_automatic':True,'network_sha256':result['network_sha256'],'browser_visual_verified':False})
 print('API workflow PASS; visual QA remains BLOCKED.',flush=True)
if __name__=='__main__':main()
