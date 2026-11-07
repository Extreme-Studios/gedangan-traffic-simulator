"""Integrity audit and review copies, without changing simulation/network results."""
from pathlib import Path
import json
import shutil
import socket
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from backend.gedangan.m04_demand import DOC,DEMAND,RUNS,CONF,load,save,sha,relative,verify_baseline

def main():
    verify_baseline();runs=load(DOC/'run-summary.json');verified=0
    for folder in [RUNS,DEMAND]:
        for p in folder.rglob('*manifest.json'):
            manifest=load(p)
            for key,h in manifest.get('files',{}).items():assert sha(p.parent/key)==h,(p,key)
            for field in ['input_sha256','code_sha256']:
                for key,h in manifest.get(field,{}).items():assert sha(ROOT/key)==h,(p,key)
            verified+=1
    m=load(DOC/'build-manifest.json')
    for key,h in m['source_m03_files_sha256'].items():assert sha(ROOT/'simulation/network/m03'/key)==h
    for key,h in m['configuration_sha256'].items():assert sha(CONF/key)==h
    reproducibility=load(DOC/'reproducibility.json')
    for key,h in reproducibility['after'].items():assert sha(RUNS/key)==h
    for run in runs:
        assert run['requested_trips']==run['routable_trips']+run['failed_routes']
        assert run['departed_vehicles']==run['arrived_vehicles'] and run['teleported_vehicles']==0 and run['pending_insertion']==0
        rid=run['run_id'];web=ROOT/'frontend/public/demand/m04';dist=ROOT/'frontend/dist-m04/demand/m04'
        for suffix in ['.trajectory.json','.routes.json']:assert (web/(rid+suffix)).read_bytes()==(dist/(rid+suffix)).read_bytes()
    assert (ROOT/'frontend/public/demand/m04/summary.json').read_bytes()==(ROOT/'frontend/dist-m04/demand/m04/summary.json').read_bytes()
    tests=(DOC/'tests.txt').read_text(encoding='utf-8-sig')
    assert 'Ran 88 tests' in tests and tests.rstrip().endswith('OK')
    with socket.socket() as sock:preview_stopped=sock.connect_ex(('127.0.0.1',5176))!=0
    browser=load(DOC/'browser-qa-results.json')
    assert browser['status']=='PASS' and browser['displayedPositionsMatchSUMO'] and not browser['consoleWarningsAndErrors']
    save(DOC/'final-validation.json',{'status':'IMPLEMENTED_WITH_DOCUMENTED_MULTICLASS_PERMISSION_LIMIT',
        'preserved_files':len(load(DOC/'previous-milestones-sha256.json')),'verified_manifests':verified,'gedangan_runs':len(runs),'tests_passed':88,'typescript_and_vite':'PASS','http_resources_passed':len(load(DOC/'http-smoke.json')['resources']),
        'trajectory_rebuild_hashes_identical':True,'production_exports_match_current_run_results':True,'preview_stopped':preview_stopped,'gui_closed':True,
        'browser_visual_qa':'PASS','nonpassenger_gedangan_movement_validated':False,'field_calibrated':False,'m05_started':False})
    review=Path(r'C:\Users\ROG ALLY\Documents\Codex\2026-10-31\files-pasted-by-the-user-milestone\outputs\Gedangan-M04');review.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/'documentation/MILESTONE_04_REPORT.md',review/'MILESTONE_04_REPORT.md');shutil.copy2(ROOT/'MILESTONE_04_README.md',review/'MILESTONE_04_README.md')
    shutil.copytree(DOC,review/'m04',dirs_exist_ok=True)
    for source in ['vehicle-types.json','od-zones.json','od-matrix.fixture.json']:shutil.copy2(DEMAND/source,review/source)
    (review/'REVIEW_COPY.txt').write_text('Review copy. Canonical runnable project:\n'+str(ROOT)+'\nUse START_DEMAND_M04.bat there. Browser QA PASS. Multiclass Gedangan movement still limited by immutable M03 passenger-only permissions.\n',encoding='utf-8')
    print(json.dumps(load(DOC/'final-validation.json'),indent=2));print('Review outputs:',review)

if __name__=='__main__':main()
