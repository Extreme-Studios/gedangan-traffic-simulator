"""One final annual rate per OD/class/year. No multiplying overlapping rates."""
import math,hashlib,json
BASE=2026;END=2040
LABEL='ILLUSTRATIVE TRAFFIC PROJECTION — 2026 BASELINE NOT CALIBRATED'
CONDITIONAL='PROVISIONAL 2026 BASELINE — CONDITIONAL FORECAST, NOT EMPIRICALLY VALIDATED'
def fingerprint(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def annual(schedule,year):
 mode=schedule['mode']
 if mode=='constant':value=schedule['rate']
 elif mode=='year_specific':
  if str(year) not in schedule['rates']:raise ValueError('MISSING annual rate '+str(year))
  value=schedule['rates'][str(year)]
 elif mode=='piecewise':
  rows=[r for r in schedule['periods'] if r['start']<=year<=r['end']]
  if len(rows)!=1:raise ValueError('Missing/ambiguous piecewise period')
  value=rows[0]['rate']
 else:raise ValueError('Unsupported rate schedule')
 if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not -.95<=value<=.20:raise ValueError('Rate outside illustrative technical envelope [-.95,.20]')
 return value
def resolve(rules,cls,od,year,scope='Gedangan model study area'):
 options=[]
 for r in rules:
  if r['vehicle_class']!=cls or r['od_relation'] not in ['*',od] or r['geographic_scope']!=scope or not r['start_year']<=year<=r['end_year']:continue
  if not r.get('provenance_id') or not r.get('source') or not r.get('estimation_method'):raise ValueError('Growth provenance missing')
  verified=r['status']=='VERIFIED_LOCAL_TRAFFIC_GROWTH' and r.get('local_flow_evidence_verified') is True
  if r['status'] not in ['SYNTHETIC_ILLUSTRATIVE_ASSUMPTION','VERIFIED_LOCAL_TRAFFIC_GROWTH']:continue
  if r['status']=='VERIFIED_LOCAL_TRAFFIC_GROWTH' and not verified:raise ValueError('Unverified source promoted to local traffic growth')
  priority=(0 if r['od_relation']==od else 1) if verified else (2 if r['od_relation']==od else 3)
  options.append((priority,r))
 if not options:raise ValueError(f'MISSING growth {cls}/{od}/{year}')
 rank=min(p for p,r in options);chosen=[r for p,r in options if p==rank]
 if len(chosen)!=1:raise ValueError('Ambiguous growth rates at same priority')
 r=chosen[0];return annual(r['schedule'],year),r
def factor(year,rules,cls,od):
 if isinstance(year,bool) or not isinstance(year,int) or not BASE<=year<=END:raise ValueError('Year outside2026–2040')
 value=1.;audit=[]
 for y in range(BASE+1,year+1):
  rate,source=resolve(rules,cls,od,y);value*=1+rate;audit.append({'year':y,'annual_rate':rate,'provenance_id':source['provenance_id'],'rule_id':source['id'],'status':source['status']})
 return value,audit
def integer_allocate(exact):
 """Global round-half-up total; Hamilton allocation; lexical stable tie order."""
 if any(not math.isfinite(v) or v<0 for v in exact.values()):raise ValueError('Invalid fractional demand')
 target=math.floor(math.fsum(exact.values())+.5);counts={k:math.floor(v) for k,v in exact.items()}
 for k in sorted(exact,key=lambda k:(-(exact[k]-counts[k]),k))[:target-sum(counts.values())]:counts[k]+=1
 return counts,{'exact_total':math.fsum(exact.values()),'rounded_total':target,'rounding_error':target-math.fsum(exact.values()),'method':'Global half-up total, largest remainder across OD/class/interval; stable lexical key ties; no random rounding'}
