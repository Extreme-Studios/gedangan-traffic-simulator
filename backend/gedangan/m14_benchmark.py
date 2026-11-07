"""Actual runs, not generated benchmark numbers."""
import copy
from .m14_engine import run
from .m14_demand import default
from .m14_common import *

def main():
 results=[]
 for n in [500,1000,3000,5000]:
  req=default();req['total']=n;req['name']=f'M14 benchmark {n}';r=run(req);results.append(r);save(DOC/'sumo-benchmarks.json',results);print({k:r[k]for k in ['run_id','requested','routed','departed','arrived','active','not_departed','failed_routes','quality','simulation_wall_s']},flush=True)
 manual=default();manual.update(name='All ten classes, nominal assumptions',mode='manual',counts={k:5 for k in manual['counts']});manual['approaches']={k:100 if k=='northbound'else 0 for k in manual['approaches']};manual['temporal']={'mode':'custom','interval_s':300,'weights':[100,0,0]};r=run(manual);save(DOC/'class-validation.json',r)
 base=default();base['total']=160;base['name']='Rail control sensitivity';base['weights']={k:100 if k=='car'else 0 for k in base['weights']};base['approaches']={k:100 if k=='rail_crossing'else 0 for k in base['approaches']};base['rail']['arrivals_s']=[180,420,660];a=run(base);no=copy.deepcopy(base);no['rail']['arrivals_s']=[];b=run(no);save(DOC/'rail-sensitivity.json',{'with_train':a,'without_train':b})
 base=default();base['total']=500;base['name']='Signal timing sensitivity';base['approaches']={k:100 if k=='northbound'else 0 for k in base['approaches']};a=run(base);other=copy.deepcopy(base);other['signal']['green_s']=30;b=run(other);save(DOC/'signal-sensitivity.json',{'baseline':a,'edited':b})
if __name__=='__main__':main()
