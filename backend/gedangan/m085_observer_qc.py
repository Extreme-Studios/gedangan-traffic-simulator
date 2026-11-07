"""Independent comparison. Missing coverage is not zero; no automatic averaging."""
from collections import defaultdict
from .m085_provenance import fingerprint
def compare_counts(store,a_id,b_id):
 from .m085_export import materialize
 with store.lock,store.connect() as c:
  a,b=store.get(c,a_id,'session'),store.get(c,b_id,'session');threshold=store.get(c,'settings')['review_relative_difference']
  if a['observer_id']==b['observer_id']:raise ValueError('Double count membutuhkan observer independen')
  if not a.get('sample_group') or a.get('sample_group')!=b.get('sample_group'):raise ValueError('Nyatakan shared sample group yang sama; waktu/lokasi saja belum membuktikan coverage sama')
  for key in ['location_id','start','end','direction','approach']:
   if a[key]!=b[key]:raise ValueError('Window/lokasi/arah/approach tidak sama; jangan menyebutnya agreement sampel yang sama')
  ra,_,_=materialize(store,c,a,for_comparison=True);rb,_,_=materialize(store,c,b,for_comparison=True)
  key=lambda r:tuple(r[k] for k in ['interval_start','interval_end','approach','direction','vehicle_class','turning_movement'])
  aa={key(r):r for r in ra if r['kind']=='traffic_count'};bb={key(r):r for r in rb if r['kind']=='traffic_count'};rows=[]
  for k in sorted(set(aa)|set(bb)):
   x,y=aa.get(k,{}).get('count'),bb.get(k,{}).get('count');diff=None if x is None or y is None else abs(x-y);relative=None if diff is None else 0 if x+y==0 else diff/((x+y)/2)
   rows.append({'stratum':dict(zip(['interval_start','interval_end','approach','direction','vehicle_class','movement'],k)),'A':x,'B':y,'absolute_difference':diff,'relative_difference':relative,'status':'MISSING_COVERAGE' if diff is None else 'REVIEW_REQUIRED' if relative>threshold else 'WITHIN_CONFIGURED_REVIEW_THRESHOLD'})
  return {'id':fingerprint([a_id,b_id,rows]),'session_A':a_id,'session_B':b_id,'observer_A':a['observer_id'],'observer_B':b['observer_id'],'threshold':threshold,'threshold_basis':'Configurable review trigger, not a universal standard','relative_definition':'abs(A-B)/mean(A,B); both zero =>0; missing =>NULL','rows':rows,'automatic_average':False,'adjudications':store.objects(c,'adjudication')}
