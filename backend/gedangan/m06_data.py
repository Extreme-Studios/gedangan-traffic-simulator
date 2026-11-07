"""Data readiness inventory and proposed survey mapping; no fabricated observation."""
import xml.etree.ElementTree as ET
from collections import Counter
from .m04_demand import ROOT,load,save,sha
from .m06_observations import KINDS,schema
DOC=ROOT/'documentation/m06';CONF=ROOT/'configuration/calibration-m06';DATA=ROOT/'data/observations/m06';TEMPL=ROOT/'data/templates/m06'
def build():
 for d in [DOC,CONF,DATA/'raw',DATA/'normalized',DATA/'synthetic-demo',TEMPL]:d.mkdir(parents=True,exist_ok=True)
 inventory=[]
 for p,h in load(DOC/'baseline-sha256.json').items():
  if p.startswith('toolchain/'):continue
  cat='SIMULATED_RESULT' if p.startswith(('simulation/runs','frontend/public')) else 'SYNTHETIC_TEST' if any(x in p for x in ['demand/m04','demand/m045','tests/']) else 'GEOSPATIAL_REFERENCE' if p.startswith('geodata/') else 'MODEL_ASSUMPTION' if p.startswith('configuration/') else 'ENGINEERING_INFERENCE'
  inventory.append({'path':p,'sha256':h,'source_class':cat,'scope':'Project artifact; classification is triage, not field verification','accessed_on':'2026-10-31'})
 observed=load(ROOT/'traffic-data/observed_data/dataset.json')
 save(DOC/'inventory.json',{'files':inventory,'by_class':dict(Counter(r['source_class'] for r in inventory)),'observed_domain_record_counts':{k:len(v) for k,v in observed.items() if isinstance(v,list)},'verified_2026_observations':0,'note':'OSM/reference/synthetic outputs cannot substitute field counts.'})
 
 for relative,empty in [('normalized/observations.json',[]),('provenance.json',{})]:
  if not (DATA/relative).exists():save(DATA/relative,empty)
 for kind in KINDS:save(CONF/f'{kind}.schema.json',schema(kind));save(TEMPL/f'{kind}.template.json',[])
 insp=load(ROOT/'simulation/network/m045/provisional/inspection.json');eds={e['id']:e for e in insp['edges']};plans=[];mappings=[]
 choices=[('MAIN_NB','northbound','w562358500_s16_p0_0_f','arterial'),('MAIN_SB','southbound','w512351908_s4_p0_0_f','arterial'),('GEDANGAN_FEEDER','eastbound','w266287930_s0_p0_0_f','feeder'),('FRONTAGE','source_direction',next(e['id'] for e in insp['edges'] if e['road_function']=='frontage_road'),'frontage'),('KETAJEN','eastbound','w1240685448_s1_p2_0_f','feeder'),('STATION_CROSSING','westbound','w1240685448_s1_p2_0_r','crossing'),('UPSTREAM_STORAGE','southbound','w512351908_s3_p0_0_f','arterial')]
 net=ET.parse(ROOT/'simulation/network/m051/provisional/network.net.xml').getroot();elements={e.get('id'):e for e in net.findall('edge')}
 for loc,direction,eid,role in choices:
  e=eds[eid];m={'location_id':loc,'direction':direction,'edge_id':eid,'lane_ids':[f'{eid}_{i}' for i in range(e['lanes'])],'junction_id':e['to'],'turning_movement':'straight','detector_id':'proposed_m06_'+loc,'od_zone':'NEEDS MANUAL REVIEW','role':role,'source_way_id':e['source_way_id'],'physical_status':'NEEDS_FIELD_SURVEY','shape':[[float(v) for v in p.split(',')] for p in elements[eid].find('lane').get('shape').split()]};mappings.append(m)
  plans.append({**m,'reason':'Corridor/turning/storage/crossing coverage','vehicle_classes':'Ten M04 local categories; ambiguous labels flagged','metrics':list(KINDS),'method':'Authorized manual/video15min tally, clock synchronization, matched travel-time route, defined queue extent, qualified geometric survey','sessions':'PROPOSED weekday/weekend morning/midday/afternoon after reconnaissance; not observed peak times','biases':['occlusion','class ambiguity','double counting','clock drift','boundary censoring','selection bias'],'special_events':['rail closure','phase changes','heavy vehicles','frontage access','side friction','blocked movement/recovery','exceptional incident']})
 save(CONF/'observation-mapping.json',mappings);save(DOC/'survey-plan.json',plans)
 short=[{'lane':l.get('id'),'length_m':float(l.get('length'))} for e in net.findall('edge') if e.get('function')!='internal' for l in e.findall('lane') if float(l.get('length'))<1]
 structural=[{'id':'CROSSING_GEOMETRY','status':'NEEDS_FIELD_SURVEY','locations':['STATION_CROSSING','KETAJEN'],'blocked_metrics':['queue','storage','spillback','railway_response'],'evidence':'M05.1 four endpoints~1.6m/seven lane shapes<=7.178m; stop lines not surveyed','short_lanes':short},{'id':'ACCESS_HEAVY','status':'PROVISIONAL_WITH_UNCERTAINTY','locations':['all'],'blocked_metrics':['heavy_vehicle_clearance'],'evidence':'No legal/swept-path approval; oversize blocked'},{'id':'STRICT_CONNECTIVITY','status':'STRUCTURAL_BLOCKER','locations':['station','feeder'],'blocked_metrics':['OD_assignment'],'evidence':'Strict lacks some station/branch routes'},{'id':'CONTROL_TIMING','status':'PROVISIONAL_WITH_UNCERTAINTY','locations':['all'],'blocked_metrics':['empirical_control_response'],'evidence':'Synthetic signal/train operation'},{'id':'FIELD_NETWORK','status':'NEEDS_FIELD_SURVEY','locations':['all'],'blocked_metrics':['physical_baseline_validation'],'evidence':'OSM directions/lanes/turns not physically validated'}]
 save(DOC/'structural-readiness.json',structural)
 missing=[{'metric':kind,'status':'MISSING','records_2026':0,'priority':'CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION','required':'Dated/georeferenced/classified field records, reviewed provenance and independent holdout'} for kind in KINDS]
 missing += [{'metric':'OD_and_turning','status':'MISSING','priority':'CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION','required':'OD/turn shares by class and interval; county ownership is not intersection volume'},{'metric':'independent_days','status':'MISSING','priority':'CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION','required':'Reserve independent day/session/location before fitting'},{'metric':'repeat_weather_side_friction','status':'MISSING','priority':'IMPORTANT — IMPROVES CONFIDENCE','required':'Replicates, visibility and event logs'},{'metric':'fine_lateral_trajectories','status':'MISSING','priority':'OPTIONAL — FUTURE REFINEMENT','required':'Authorized anonymous trajectories after basic coverage'}]
 save(DOC/'missing-register.json',missing)
 save(CONF/'baseline-2026.json',{'year':2026,'status':'2026 PROVISIONAL BASELINE','network':'simulation/network/m051/provisional/network.net.xml','network_sha256':sha(ROOT/'simulation/network/m051/provisional/network.net.xml'),'vehicle_registry':'configuration/demand-m04/vehicle-registry.json','demand':'SYNTHETIC_M04_STARTING_CONFIG_NOT_TRUTH','OD':'simulation/demand/m04/od-matrix.fixture.json','signal':'configuration/signals-m05/program.json','railway':'configuration/railway-m05/pilot.json','behavior':'configuration/behavior-m05/profiles.json','measurement_window':{'timezone':'Asia/Jakarta','empirical':None,'fixture_seconds':[0,600]},'observation_dataset':'data/observations/m06/normalized/observations.json','observed_records':0,'source_confidence':'MODEL_ASSUMPTIONS_AND_OSM_REFERENCE','empirical_baseline':{'status':'BLOCKED — INSUFFICIENT OBSERVED DATA','enabled':False,'independent_validation':'INDEPENDENT VALIDATION NOT POSSIBLE WITH AVAILABLE DATA'},'structural_blockers':[s['id'] for s in structural]})
 save(TEMPL/'vehicle-classification.json',load(ROOT/'configuration/demand-m04/vehicle-registry.json')['vehicles'])
 save(TEMPL/'source-provenance.template.json',{'sources':[],'required_fields':['provenance_id','source_title','source_uri','source_class','field_evidence_verified','source_year','accessed_on','survey_period','method','spatial_scope','license_notes','limitations']})
 (DOC/'SURVEY_METHOD.md').write_text('''# Rencana survei Gedangan

Titik/sesi pada survey-plan.json masih rencana. Cek akses aman dan izin. Tidak berdiri di lajur aktif atau area rel; geometri diukur personel berwenang. Clock Asia/Jakarta disinkronisasi. Tally per15menit menurut kelas/arah/gerakan. NULL/MISSING adalah tidak diamati;0 hanya hitungan nol yang diamati. Dua pencacah memeriksa sebagian interval secara independen; discrepancy dan outlier dipertahankan sebagai flag.

Jangan menjumlah approach-total dengan semua turns sebagai dua arus. Travel-time memakai route/endpoints/sample count; queue harus mempunyai definisi front/rear/body dan boundary censoring. Signal/rail events memakai timestamp dan uncertainty asli. Departure timetable tidak sama dengan closure.

Usulkan hari kerja/akhir pekan dan sesi pagi/siang/sore setelah reconnaissance, tanpa klaim peak hour. Reserve holdout sebelum fitting. Rekam hambatan samping, heavy vehicles, frontage access dan recovery. Video hanya berizin; tidak scrape CCTV privat. Minimalkan wajah/plat; simpan tally anonim dan log visibilitas. Proposed detector IDs bukan alat terpasang.
''',encoding='utf-8')
if __name__=='__main__':build()
