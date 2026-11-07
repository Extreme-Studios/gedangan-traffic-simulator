import http.client,json,subprocess,time
from pathlib import Path
root=Path.cwd();log=root/'documentation/m11/actual-launcher.txt'
assert json.loads(log.read_text(encoding='utf-8-sig'))['instance_reused'] is False,'This test may only restart the M11-owned service it created'
c=http.client.HTTPConnection('127.0.0.1',5186,timeout=3);c.request('GET','/api/m10/health');r=c.getresponse();h=json.loads(r.read());c.close()
c=http.client.HTTPConnection('127.0.0.1',5186,timeout=3);c.request('POST','/api/m10/shutdown',json.dumps({'token':h['token']}),{'Content-Type':'application/json'});r=c.getresponse();assert r.status==200;r.read();c.close();time.sleep(.7)
result=subprocess.run([str(root/'.venv/Scripts/python.exe'),'-m','backend.gedangan.m11_launch','--no-open'],cwd=root,capture_output=True,text=True)
print(result.stdout);assert result.returncode==0
(root/'documentation/m11/adapter-start.txt').write_text(result.stdout,encoding='utf-8')
