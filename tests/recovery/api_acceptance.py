"""Actual loopback research service + real SUMO queued experiment, no mock API."""
import urllib.request,urllib.error,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'documentation/realism_recovery';BASE='http://127.0.0.1:5196'
def call(path,body=None):
 request=urllib.request.Request(BASE+path,data=json.dumps(body).encode()if body is not None else None,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(request,timeout=60)as r:return r.status,r.read()
def main():
 checks=[];h=json.loads(call('/api/health')[1]);assert h['engine']=='ACTUAL LOCAL SUMO1.28.0';checks.append('Live research host identity, old EXE not misrepresented')
 try:call('/api/run',{'date':'2026-05-05','time':'16:00'});raise AssertionError('Missing source admitted')
 except urllib.error.HTTPError as e:assert e.code==400 and'MISSING'in e.read().decode();checks.append('Missing exact historical request rejected with actual HTTP400')
 for p in ['/','/app.js','/style.css','/api/network','/evidence/network-source-overlay.geojson','/evidence/network-source-overlay.svg']:
  status,data=call(p);assert status==200 and data;checks.append('Local resource '+p)
 req={'date':'2026-08-04','time':'21:00','demand_mode':'SYNTHETIC_SCENARIO','acknowledge_estimate':True,'horizon_s':120,'warmup_s':60,'seed':77,'scenario':{'id':'S00'},'train_times_s':[],'flows':[{'od_id':'local_trip','vehicle_type_id':'car','veh_per_hour':120},{'od_id':'local_trip','vehicle_type_id':'motorcycle','veh_per_hour':120}]};job=json.loads(call('/api/run',req)[1])['job_id'];checks.append('Actual SUMO job queued from HTTP POST')
 try:call('/api/run',req);raise AssertionError('Concurrent job admitted')
 except urllib.error.HTTPError as e:assert e.code==409;checks.append('Duplicate concurrent job prevented')
 for _ in range(180):
  state=json.loads(call('/api/state')[1]);j=state['jobs'][job]
  if j['status']in ['COMPLETE','FAILED']:break
  time.sleep(1)
 assert j['status']=='COMPLETE',j;rid=j['run_id'];r=next(r for r in state['runs']if r['run_id']==rid);assert r['status']=='ACTUAL_SUMO_RESULT'and r['requested']==r['routed']+r['failed_routes'];assert r['arrived']>0;checks.append('New run completed, actual vehicles arrived, immutable manifest and accounting available')
 for p in ['/api/playback?run='+rid,'/api/export?run='+rid+'&format=json','/api/export?run='+rid+'&format=csv']:
  status,data=call(p);assert status==200 and data;checks.append('Actual output '+p.split('?')[0])
 try:call('/api/playback?run='+'0'*24);raise AssertionError('Missing replay fallback admitted')
 except urllib.error.HTTPError as e:assert e.code==400;checks.append('Missing run never substituted with another recording')
 value={'status':'PASS','checks':checks,'run_id':rid,'actual_requested':r['requested'],'actual_arrived':r['arrived'],'browser_visual_acceptance':'NOT CLAIMED - internal browser disabled in Work settings; API test is not a browser interaction test'};(OUT/'api-acceptance.json').write_text(json.dumps(value,indent=2));print(json.dumps(value))
if __name__=='__main__':main()
