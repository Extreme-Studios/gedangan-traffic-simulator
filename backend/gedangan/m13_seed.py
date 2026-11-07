"""Copy published 2023 records into separate M13 database with scope gaps retained."""
from .m13_database import Store
from .m13_common import *
def seed(store=None):
 store=store or Store();old=ROOT/'data/realism_recovery/historical.sqlite';pdf=ROOT/'documentation/realism_recovery/sources/REFERENCE_2023.pdf';digest=sha(pdf);sid='REFERENCE_2023_PUBLISHED_TABLE1'
 with connect(old,True)as original:rows=[dict(r)for r in original.execute('SELECT * FROM evidence')]
 with connect(store.path)as c:
  c.execute('INSERT OR IGNORE INTO sources VALUES(?,?,?,?,?,?,?,?,?)',(sid,'OBSERVED_SECONDARY','Kusuma & Sholikhah2024 Table1 p927','Ahmad Yani / Aloha construction context; not verified core Gedangan station','https://ejournal.undip.ac.id/index.php/ilmulingkungan/article/download/56951/pdf','Published hourly vehicle counts; original survey9/11/14May2023; directions and sub-hour profile unspecified',digest,str(pdf),now()))
  for r in rows:
   prov={'original_database':str(old.relative_to(ROOT)),'original_record_id':r['id'],'source_table':'Table1 p927','scope_limits':['2023 only','Direction unspecified','No mapped measurement station edge','Not 2026 target observation'],'original_provenance':json.loads(r['provenance_json'])}
   values=[r['id'],identity([sid,r['id']]),sid,None,r['date'],r['start_wib']+':00','Asia/Jakarta',r['date']+'T'+r['start_wib']+':00+07:00',r['date']+'T'+r['end_wib']+':00+07:00',r['road_segment'],'UNSPECIFIED',r['vehicle_class'],int(r['value']),None,None,None,None,json.dumps({'vehicle_count':'vehicles/interval'}),'OBSERVED','PENDING_REVIEW',json.dumps(prov)]
   c.execute('INSERT OR IGNORE INTO observations VALUES('+','.join('?'for _ in values)+')',values)
 return {'copied_source_records':len(rows),'target_calendar_eligible':0,'source_sha256':digest,'source_database_unchanged':True}
if __name__=='__main__':print(seed())
