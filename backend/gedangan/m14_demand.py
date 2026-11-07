"""Exact, reproducible scenario cohorts, independent of historical databases."""
import random,math,copy
from collections import Counter
from datetime import datetime
from .m14_common import *
from .m14_network import catalog,route
from .m14_vehicles import registry,PROFILES

def default():
 c=catalog();return {'name':'Eksperimen Gedangan','date':'2026-11-01','time':'07:00','duration_s':900,'seed':42,'mode':'random','total':3000,'profile':'Motorcycle Dominant','weights':dict(zip([v['id']for v in registry()],PROFILES['Motorcycle Dominant'])),'counts':{v['id']:0 for v in registry()},'approach_mode':'weighted','approaches':{a['id']:({'northbound':35,'southbound':35,'sukodono':8,'ketajen':8,'frontage':4,'rail_crossing':10}[a['id']])for a in c['approaches']},'turns':{a['id']:{t:100 if t=='straight'else 0 for t in a['movements']}for a in c['approaches']},'temporal':{'mode':'uniform','interval_s':300},'signal':{'green_s':12,'yellow_s':3,'all_red_s':2},'rail':{'arrivals_s':[300,660],'direction':'N_TO_S','delay_s':0,'closing_s':15,'passing_s':10,'reopen_delay_s':3,'opening_s':3,'recovery_s':5}}

def integer(x,label,lo=0,hi=100000):
 if isinstance(x,bool)or not isinstance(x,(int,float))or not math.isfinite(x)or int(x)!=x or not lo<=x<=hi:raise ValueError(label+' must be an integer '+str(lo)+'..'+str(hi))
 return int(x)

def weights(values,keys,label):
 if set(values)!=set(keys):raise ValueError(label+' keys must match catalog')
 if any(isinstance(v,bool)or not isinstance(v,(int,float))or not math.isfinite(v)or v<0 for v in values.values()):raise ValueError(label+' weights must be finite and nonnegative')
 if abs(sum(values.values())-100)>1e-6:raise ValueError(label+' percentages must sum to 100')
 return values

def allocate(n,w,rng,randomized=False):
 keys=list(w)
 if randomized:
  c=Counter(rng.choices(keys,weights=list(w.values()),k=n));return {k:c[k]for k in keys}
 raw={k:n*v/100 for k,v in w.items()};out={k:math.floor(v)for k,v in raw.items()};order=sorted(keys,key=lambda k:(-(raw[k]-out[k]),k))
 for k in order[:n-sum(out.values())]:out[k]+=1
 return out

def expand(c,rng):
 ids=[k for k,n in c.items()for _ in range(n)];rng.shuffle(ids);return ids

def generate(request):
 req=copy.deepcopy(request);datetime.strptime(req['date']+'T'+req['time'],'%Y-%m-%dT%H:%M');h=integer(req['duration_s'],'duration_s',60,14400);seed=integer(req['seed'],'seed',0,2147483647);rng=random.Random(seed);keys=[v['id']for v in registry()];aa=[a['id']for a in catalog()['approaches']]
 if req['mode']=='manual':
  if set(req['counts'])!=set(keys):raise ValueError('Manual counts must include all vehicle types')
  counts={k:integer(v,k)for k,v in req['counts'].items()};n=sum(counts.values())
 elif req['mode']=='random':
  n=integer(req['total'],'total',1,10000);counts=allocate(n,weights(req['weights'],keys,'Vehicle'),rng,True)
 else:raise ValueError('Unknown vehicle input mode')
 integer(n,'total demand',1,10000)
 if req['approach_mode']=='exact':
  if set(req['approaches'])!=set(aa):raise ValueError('Approaches must match existing network')
  allocations={k:integer(v,k)for k,v in req['approaches'].items()}
  if sum(allocations.values())!=n:raise ValueError('Exact approach counts must equal total demand')
 elif req['approach_mode']=='weighted':allocations=allocate(n,weights(req['approaches'],aa,'Approach'),rng,True)
 else:raise ValueError('Unknown approach mode')
 turns={}
 for a in aa:
  w=weights(req['turns'][a],['straight','left','right','uturn'],'Turn '+a);turns[a]=allocate(allocations[a],w,rng,req.get('turn_mode','exact')=='random')
 interval=integer(req['temporal']['interval_s'],'interval_s',60,3600)
 if interval not in [300,900,3600]:raise ValueError('Custom temporal interval must be 5, 15 or 60 minutes')
 bins=math.ceil(h/interval);mode=req['temporal']['mode'];lens=[min(interval,h-i*interval)for i in range(bins)]
 if mode=='uniform':w={str(i):100*l/h for i,l in enumerate(lens)}
 elif mode=='peak':
  raw=[lens[i]*(1+4*math.exp(-((i+.5-bins*.5)/max(1,bins*.2))**2))for i in range(bins)];w={str(i):100*v/sum(raw)for i,v in enumerate(raw)}
 elif mode=='custom':w=weights({str(i):v for i,v in enumerate(req['temporal']['weights'])},[str(i)for i in range(bins)],'Temporal')
 else:raise ValueError('Unknown departure profile')
 hist=allocate(n,w,rng);times=sorted(round(i*interval+(j+.5)*lens[i]/hist[str(i)],3)for i in range(bins)for j in range(hist[str(i)]))
 vehicles=expand(counts,rng);movements=[(a,t)for a in aa for t in expand(turns[a],rng)];rng.shuffle(movements);rows=[]
 for i,(typ,(a,t),depart)in enumerate(zip(vehicles,movements,times)):
  rows.append({'id':f'm14_{i:06d}','vehicle_type_id':typ,'approach':a,'turn':t,'depart_seconds':depart,**route(typ,a,t)})
 assert len(rows)==n==sum(counts.values())==sum(allocations.values())==sum(hist.values())and len({r['id']for r in rows})==n
 return {'request':req,'classification':'MANUAL INPUT SCENARIO'if req['mode']=='manual'else'RANDOMIZED SCENARIO — NOT FIELD OBSERVATION','is_observation':False,'seed':seed,'total':n,'composition':counts,'approach_allocation':allocations,'turn_allocation':turns,'departure_histogram':[{'start_s':i*interval,'end_s':min(h,(i+1)*interval),'count':hist[str(i)]}for i in range(bins)],'requests':rows,'cohort_sha256':identity(rows),'network_sha256':catalog()['network_sha256'],'routed':sum(bool(r['edges'])for r in rows),'failed_routes':sum(not r['edges']for r in rows)}
