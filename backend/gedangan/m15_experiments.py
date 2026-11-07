"""Explicit experiments: no capacity tuning to force successful insertion."""
import copy
from .m15_common import *
from .m15_engine import run
from .m15_demand import default
def main():
 results=[]
 for n in [500,1000,3000,5000]:
  r=default();r.update(total=n,name=f'M15 {n} vehicles per hour / 60 min');v=run(r);results.append(v);save(DOC/'one-hour-results.json',results);print({k:v[k]for k in ['run_id','requested','routed','departed','arrived','active','not_departed','failed_routes','simulation_wall_s']},flush=True)
 r=default();r.update(mode='manual',volume_interpretation='total',name='M15 manual multiclass one hour',counts={k:50 for k in r['counts']});save(DOC/'manual-one-hour.json',run(r))
 r=default();r.update(total=3000,duration_s=900,name='M15 3000 TOTAL in 15 min',volume_interpretation='total');r['rail']['arrivals_s']=[300,660];save(DOC/'total3000-15min.json',run(r))
 # Same class/cohort clock, immutable network; only controller duration differs.
 r=default();r.update(total=500,name='M15 signal sensitivity');r['approaches']={k:100 if k=='northbound'else 0 for k in r['approaches']};a=run(r);b=copy.deepcopy(r);b['signal']['green_s']=30;save(DOC/'signal-sensitivity.json',{'baseline':a,'green30':run(b)})
 r=default();r.update(total=400,name='M15 railway sensitivity');r['approaches']={k:100 if k=='rail_crossing'else 0 for k in r['approaches']};r['weights']={k:100 if k=='car'else 0 for k in r['weights']};a=run(r);b=copy.deepcopy(r);b['rail']['arrivals_s']=[];save(DOC/'rail-sensitivity.json',{'with_trains':a,'without_trains':run(b)})
if __name__=='__main__':main()
