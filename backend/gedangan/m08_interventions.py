"""Cohort-preserving operational schedules; deferral is a cost, not deleted demand."""
from .m07_projection import requests
from .m07_growth import fingerprint
def cohort(projection,base,mode,seed):return requests(projection,base,mode,seed)
def apply_schedule(original,spec):
 rows=[];ledger=[]
 for q in original:
  row=dict(q);planned=q['depart_seconds'];effective=planned
  if spec['operation']=='heavy_deferral' and q['vehicle_type_id'] in spec['parameters']['classes'] and spec['parameters']['restricted_window_s'][0]<=planned<spec['parameters']['restricted_window_s'][1]:effective=planned+spec['parameters']['deferral_s']
  row['depart_seconds']=effective;rows.append(row);ledger.append({'id':q['id'],'class':q['vehicle_type_id'],'od_id':q['od_id'],'original_depart_s':planned,'effective_depart_s':effective,'deferred':effective>planned,'deferred_seconds':effective-planned,'displaced_outside_demand_window':effective>=1800,'outside_measurement_horizon':effective>=2100})
 return sorted(rows,key=lambda r:(r['depart_seconds'],r['id'])),ledger
def identity(rows):return fingerprint([{k:q[k] for k in ['id','vehicle_type_id','od_id','origin_zone','destination_zone','origin_edge','destination_edge','depart_seconds']} for q in rows])
