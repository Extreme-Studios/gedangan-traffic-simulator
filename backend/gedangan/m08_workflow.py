"""Sequential reproducible M08 workflow, guarded against another SUMO worker."""
import sys,time,subprocess,traceback,csv,io
from datetime import datetime,timezone
from .m04_demand import ROOT,load,save
from .m08_reporting import DOC
from .m08_lock import worker

def browser_validation_cases():
 """Replay bounded browser-selected cases without losing their original evidence."""
 from .m08_server import COMPATIBILITY
 from .m08_scenarios import read
 from .m07_scenarios import read as growth
 cases=[]
 if (DOC/'browser-run-request.json').exists():cases.append(load(DOC/'browser-run-request.json'))
 if (DOC/'browser-run-requests.json').exists():
  extra=load(DOC/'browser-run-requests.json')
  if not isinstance(extra,list):raise ValueError('Browser validation requests must be a list')
  cases.extend(extra)
 if len(cases)>4:raise ValueError('At most four browser validation cases per rebuild')
 for case in cases:
  if not isinstance(case,dict) or set(case)!={'solution','year','growth','seed','family'}:raise ValueError('Invalid browser validation case fields')
  if type(case['year'])!=int or not 2026<=case['year']<=2040 or type(case['seed'])!=int or case['seed'] not in [42,43]:raise ValueError('Invalid bounded browser year or seed')
  spec=read(case['solution']);growth(case['growth'])
  if spec['status'] not in ['SIMULATION_READY_PROVISIONAL','SIMULATED'] or case['family'] not in COMPATIBILITY[case['solution']]:raise ValueError('Browser validation case is not executable in its parent')
 return cases

def main():
 state={'status':'RUNNING','stage':'waiting for primary batch' if '--after-batch' in sys.argv else 'primary batch','completed':[],'started_utc':datetime.now(timezone.utc).isoformat()}
 def stage(name,action):
  state['stage']=name;save(DOC/'offline-stage.json',state);action();state['completed'].append(name);save(DOC/'offline-stage.json',state)
 with worker():
  from .m08_toolchain import verify
  verify()
  save(DOC/'offline-stage.json',state)
  try:
   if '--after-batch' in sys.argv:
    deadline=time.monotonic()+3600
    while load(DOC/'run-queue.json')['status']!='COMPLETE':
     if '--wait' not in sys.argv or time.monotonic()>deadline:raise RuntimeError('Primary batch not complete')
     time.sleep(2)
   else:
    if (DOC/'run-queue.json').exists() and load(DOC/'run-queue.json')['status']=='RUNNING':
     if '--resume' not in sys.argv:raise RuntimeError('Primary batch marked RUNNING. Inspect retained failure/progress records; use REBUILD_SOLUTIONS_M08.bat --resume only after the previous process stopped.')
     process_list=subprocess.run(['tasklist.exe','/FI','IMAGENAME eq sumo.exe','/FO','CSV','/NH'],capture_output=True,text=True,check=True).stdout
     if any(row and row[0].lower()=='sumo.exe' for row in csv.reader(io.StringIO(process_list))):raise RuntimeError('Cannot resume while a headless SUMO process is active; no process was stopped')
    from .m08_runner import batch
    stage('primary batch',batch)
   from .m08_verification import robustness,all_audits
   from .m08_reporting import reproduce,publish,results,RUNS
   from .m07_reporting import supplement
   stage('LOW/HIGH and Strict robustness',robustness)
   requests=browser_validation_cases()
   if requests:
    def replay_browser_case():
     from .m08_runner import run
     for request in requests:
      args=(request['year'],request['growth'],request['seed'],request['family'])
      selected=load(DOC/'signal-training.json')['selected'] if request['solution']=='S01' else None
      run('S00',*args);run(request['solution'],*args,specification=selected)
    stage('replay recorded browser validation cases',replay_browser_case)
   stage('fresh independent reproduction',reproduce)
   stage('full-FCD permission audit',all_audits)
   def supplements():
    values=[supplement(RUNS/r['run_id']) for r in results()];save(DOC/'supplementary-audits.json',values)
   stage('full-horizon occupancy, speeds and crossing windows',supplements)
   stage('comparison publication',publish)
   def command(args,filename,cwd=ROOT):
    with (DOC/filename).open('w',encoding='utf-8') as stream:
     subprocess.run(args,cwd=cwd,stdout=stream,stderr=subprocess.STDOUT,check=True)
   stage('final regression',lambda:command([sys.executable,'-m','unittest','discover','-s','tests','-v'],'final-regression.txt'))
   stage('TypeScript',lambda:command(['cmd','/c','npx','--no-install','tsc','--noEmit'],'typescript.txt',ROOT/'frontend'))
   stage('Vite production build',lambda:command(['cmd','/c','npx','--no-install','vite','build','--config','vite.solutions.config.ts'],'production-build.txt',ROOT/'frontend'))
   state.update(status='COMPLETE',stage='complete',finished_utc=datetime.now(timezone.utc).isoformat());save(DOC/'offline-stage.json',state)
  except Exception as e:
   state.update(status='FAILED',error=str(e),traceback=traceback.format_exc(),failed_utc=datetime.now(timezone.utc).isoformat());save(DOC/'offline-stage.json',state)
   ledger=load(DOC/'workflow-failures.json') if (DOC/'workflow-failures.json').exists() else [];ledger.append(state);save(DOC/'workflow-failures.json',ledger);raise
if __name__=='__main__':main()
