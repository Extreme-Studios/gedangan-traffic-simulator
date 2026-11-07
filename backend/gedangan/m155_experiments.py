"""Single-factor comparisons retain exact demand/route/departure cohort."""
import copy
from .m155_common import *
from .m155_demand import default
from .m155_engine import run
def run_case(label,**changes):
 r=default();r.update(name='M15.5 '+label,**changes);v=run(r);save(DOC/'cases'/(label+'.json'),v);print({k:v[k]for k in ['run_id','requested','departed','arrived','active','not_departed','execution_horizon_s','simulation_wall_s']},flush=True);return v
def main(group):
 freeze()
 if group=='bench':
  results=[]
  for n in [500,1000,3000,5000]:results.append(run_case('baseline-'+str(n),total=n));save(DOC/'one-hour-results.json',results)
 elif group=='controls':
  run_case('discharge-3000',execution_horizon_s=7200)
  s=copy.deepcopy(default()['signal']);s['green_s']=30;run_case('green30-3000',signal=s)
  rail=copy.deepcopy(default()['rail']);rail['arrivals_s']=[];run_case('no-trains-3000',rail=rail)
 elif group=='manual':
  r=default();r.update(name='M15.5 manual ten classes',mode='manual',volume_interpretation='total',counts={k:12 for k in r['counts']});save(DOC/'manual.json',run(r))
if __name__=='__main__':
 import sys
 main(sys.argv[1]if len(sys.argv)>1 else'bench')
