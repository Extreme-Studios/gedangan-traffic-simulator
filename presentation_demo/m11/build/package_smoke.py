from pathlib import Path
import zipfile,subprocess,json,http.client,time,os
root=Path.cwd();out=root/'presentation_demo/m11';target=(out/'tooling/package-smoke').resolve();target.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out/'GEDANGAN_M11_PAKET_PRESENTASI.zip')as z:
 for name in z.namelist():assert(target/name).resolve().is_relative_to(target),'Archive path escape'
 assert z.testzip()is None
 z.extractall(target)
process=subprocess.run(['python','-m','backend.gedangan.m11_launch','--port','5189','--no-open'],cwd=target,capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW);assert process.returncode==0,process.stderr+process.stdout;result=json.loads(process.stdout.strip().split('\n')[-1]);assert result['recordings_verified']==23 and result['m11_presentation_adapter']is True
browser=subprocess.run(['node','tests/m11/package-smoke.cjs'],cwd=root,capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW)
(root/'documentation/m11/package-browser-process.txt').write_text(browser.stdout+'\n'+browser.stderr,encoding='utf-8');assert browser.returncode==0,browser.stderr
c=http.client.HTTPConnection('127.0.0.1',5189,timeout=5);c.request('GET','/api/m10/health');r=c.getresponse();h=json.loads(r.read());c.close();c=http.client.HTTPConnection('127.0.0.1',5189,timeout=5);c.request('POST','/api/m10/shutdown',json.dumps({'token':h['token']}),{'Content-Type':'application/json'});r=c.getresponse();assert r.status==200;r.read();c.close()
report={'status':'PASS','archive_crc':'PASS','extract_path_checked':True,'global_python_launch':True,'m11_adapter':True,'recordings_verified':23,'actual_chrome_render_and_playback':'PASS','clean_shutdown':True,'port':5189,'scope':'Extracted distribution runtime verified, not a full copy of the research workspace'}
(out/'qa/package-smoke.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
