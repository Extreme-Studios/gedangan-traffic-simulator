"""Keep measured 12h aggregates and smp/hour tables outside hourly calendar."""
import re,json
from .m131_research import DOC,ROOT,load,save,sha,identity
from .m13_common import date,timedelta
from .m131_database import initialize
def aggregates():
 records=load(DOC/'resource-inspections.json');pnl=next(r for r in records if r.get('tag')=='JENGGOLO_2023');pages=load(DOC/'extracted'/(pnl['sha256']+'.json'))['pages'];text='\n'.join(p['text']for p in pages)
 assert re.search(r'27\s+November\s+2023',text)and re.search(r'3\s+Desember\s+2023',text)
 assert re.search(r'06\.00\s+sampai\s*18\.00',text)
 classes={1:'Kendaraan ringan (mobil, pick up, truk box)',2:'Bus kecil',3:'Bus besar',4:'Truk2as',5:'Truk3as',6:'Truk4as',7:'Truk5as'};names=['senin','selasa','rabu','kamis','jumat','sabtu','minggu'];dates={names[i]:(date(2023,11,27)+timedelta(days=i)).isoformat()for i in range(7)};rows=[]
 for n,cls in classes.items():
  start=re.search(r'Tabel\s*'+str(n)+r'\.',text).end();end=re.search(r'Tabel\s*'+str(n+1)+r'\.',text[start:]);section=text[start:start+end.start()]if end else text[start:];values=re.findall(r'(Senin|Selasa|Rabu|Kamis|Jumat|Sabtu|Minggu)\s+(\d+)',section,re.I);assert len(values)==7,(n,values)
  for dayname,count in values:
   d=dates[dayname.lower()];rows.append({'source_id':'PNL_JENGGOLO_2023','source_url':pnl['url'],'source_sha256':pnl['sha256'],'source_path':pnl['path'],'quality_class':'C','source_evidence_type':'PUBLISHED_OBSERVED_12H_AGGREGATE','observation_date':d,'date_resolution':'Weekday uniquely mapped within explicitly stated27Nov–3Dec2023 single week; not publication date','interval_start':d+'T06:00:00+07:00','interval_end':d+'T18:00:00+07:00','road_segment_source':'Jalan Raya Jenggolo, ±300m, Kecamatan Gedangan, source Figure6','network_edge':None,'direction':'BOTH_DIRECTIONS_COMBINED','vehicle_class_source':cls,'vehicle_count':int(count),'unit':'vehicles/12h','table':n,'page':3 if n<=5 else 4,'calendar_eligible':False,'sumo_ready':False,'limitations':['No per-hour/15min decomposition','Direction not separated','Source light class combines cars,pickups,box trucks; no unsupported registry split','Exact station coordinates/extent not georeferenced; literal road name retained','Motorcycles not enumerated in these seven class tables; not all traffic']})
 xls=next(r for r in records if r.get('tag')=='v-c-ratio-di-jalan-kabupaten-kota'and r.get('inspection',{}).get('format')=='XLS/XLSX');pdf=next(r for r in records if r.get('tag')=='v-c-ratio-di-jalan-kabupaten-kota'and r.get('inspection',{}).get('format')=='PDF')
 for raw in xls['inspection']['all_values']['Sheet1']['values'][1:]:
  rows.append({'source_id':'DISHUB_VC_2022','source_url':xls['url'],'source_sha256':xls['sha256'],'source_path':xls['path'],'quality_class':'C','source_evidence_type':'OFFICIAL_EQUIVALENT_VOLUME_CAPACITY_TABLE','observation_date':None,'survey_year':2022,'publication_document_date':'2023-01-11','interval_start':None,'interval_end':None,'road_segment_source':raw[0],'direction':None,'vehicle_class_source':None,'vehicle_count':None,'volume_original':raw[3],'capacity_original':raw[4],'vc_ratio':raw[5],'LOS':raw[6],'unit':'smp/hour','unit_provenance_paired_pdf_sha256':pdf['sha256'],'calendar_eligible':False,'sumo_ready':False,'limitations':['XLS has no exact observation date/hour/direction/class','smp/hour is not physical vehicles/hour','Unit and2022survey attribution cross-checked against paired official PDF','No automatic matching of countywide road names to source station edges']})
 for row in rows:
  if row['source_id']=='PNL_JENGGOLO_2023':row.update(quality_class='B',admission_status='QUARANTINED_FROM_HOURLY_CALENDAR')
 return rows
def main():
 store=initialize();rows=aggregates();store.add_aggregates(rows);save(DOC/'reference-aggregates.json',rows);pnl=[r for r in rows if r['source_id']=='PNL_JENGGOLO_2023']
 normalized=[{'observation_date':r['observation_date'],'observation_time':'06:00:00','time_zone':'Asia/Jakarta','interval_start':r['interval_start'],'interval_end':r['interval_end'],'road_segment':r['road_segment_source'],'direction':r['direction'],'vehicle_class':r['vehicle_class_source'],'vehicle_count':r['vehicle_count'],'measurement_unit':json.dumps({'vehicle_count':r['unit']}),'original_pdf_sha256':r['source_sha256'],'original_source_url':r['source_url'],'source_table':r['table'],'source_page':r['page'],'date_resolution':r['date_resolution']}for r in pnl]
 source={'source_type':'OBSERVED_SECONDARY','quality_class':'B','source_name':'Malik & Ikhwanuddin2024, published Jenggolo12h class totals','source_location':pnl[0]['road_segment_source'],'source_url':pnl[0]['source_url'],'survey_method':'Published manual counts27Nov–3Dec2023,06–18WIB,both directions combined; original source units/class groups retained; interval and endpoint mapping unresolved','original_pdf_sha256':pnl[0]['source_sha256'],'original_pdf_path':pnl[0]['source_path']}
 try:result=store.import_bytes('PNL_2023_PARTIAL_ORIGINAL_INTERVALS.json',json.dumps(normalized,ensure_ascii=False).encode(),source);save(DOC/'partial-import.json',result)
 except ValueError as exc:
  if 'Duplicate file'not in str(exc):raise
  result=load(DOC/'partial-import.json')
 assert not result['staged_ids']and len(result['quarantine'])==49
 summary={'reference_aggregate_records':len(rows),'new_partial_B_candidate_rows':49,'B_rows_quarantined_from_hourly_calendar':49,'pnl_12h_physical_count_values':len(pnl),'pnl_sum_of_published_class_counts':sum(r['vehicle_count']for r in pnl),'pnl_unique_dates':sorted({r['observation_date']for r in pnl}),'official_vc_road_rows':sum(r['source_id']=='DISHUB_VC_2022'for r in rows),'new_verified_hourly_observations':0,'sumo_ready_direct_demand_rows':0,'original_m13_sha_unchanged':sha(ROOT/'data/historical/m13/historical.sqlite')==load(DOC/'database-origin.json')['original_sha256'],'scope_warning':'PNL total sums only reported seven non-motorcycle class groups over7×12h; not total Gedangan traffic, not hourly rate.'};save(DOC/'integration-summary.json',summary);print(summary,flush=True)
if __name__=='__main__':main()
