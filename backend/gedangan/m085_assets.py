"""Read-only M06 assets audit and local source geometry. Never rebuild old assets."""
import csv,json,zipfile,xml.etree.ElementTree as E
from .m04_demand import ROOT,load,registry
from .m06_observations import KINDS,schema
from .m085_baseline import DOC,digest
def audit():
 rows=[];headers=load(ROOT/'configuration/calibration-m06/template-columns.json')
 for kind in KINDS:
  p=ROOT/f'configuration/calibration-m06/{kind}.schema.json';same=load(p)==schema(kind)
  if not same:raise ValueError('Stored/generated M06 schema differs: '+kind)
  rows.append({'asset':str(p.relative_to(ROOT)),'sha256':digest(p),'schema_matches_unchanged_importer':same})
 for kind,expected in headers.items():
  p=ROOT/f'data/templates/m06/{kind}.csv'
  with p.open(encoding='utf-8-sig',newline='') as f:actual=next(csv.reader(f))
  if actual!=expected:raise ValueError('M06 CSV header differs: '+kind)
  rows.append({'asset':str(p.relative_to(ROOT)),'sha256':digest(p),'header':actual})
 workbook=ROOT/'data/templates/m06/Gedangan_Survey_Forms.xlsx'
 with zipfile.ZipFile(workbook) as z:
  if z.testzip() is not None:raise ValueError('M06 workbook archive invalid')
  ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};sheets=[e.get('name') for e in E.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',ns)]
 plans=load(ROOT/'documentation/m06/survey-plan.json');ids=['MAIN_NB','MAIN_SB','GEDANGAN_FEEDER','FRONTAGE','KETAJEN','STATION_CROSSING','UPSTREAM_STORAGE'];assert [p['location_id'] for p in plans]==ids
 for relative in ['documentation/m06/SURVEY_METHOD.md','documentation/m06/survey-plan.json','backend/gedangan/m06_observations.py','backend/gedangan/m06_validation.py','data/observations/m06/provenance.json','documentation/MILESTONE_06_REPORT.md','documentation/MILESTONE_07_REPORT.md','documentation/MILESTONE_08_REPORT.md','documentation/ARCHITECTURE.md','documentation/DATA_GOVERNANCE.md']:
  p=ROOT/relative;rows.append({'asset':relative,'sha256':digest(p),'read_only':True})
 value={'assets':rows,'six_schemas':len(KINDS),'nine_CSV_headers':len(headers),'six_JSON_templates':[{'kind':k,'sha256':digest(ROOT/f'data/templates/m06/{k}.template.json'),'empty_template':load(ROOT/f'data/templates/m06/{k}.template.json')==[]} for k in KINDS],'workbook':{'sha256':digest(workbook),'sheets':sheets,'rebuilt':False},'seven_locations':plans,'M04_classes':[v['id'] for v in registry()],'M06_source_class_contract':['OBSERVED_FIELD','DEMO_SYNTHETIC'],'M085_bridge':'Original source classifications retained in immutable raw/notes/provenance. Only reviewed evidence-eligible manual/video inputs map to OBSERVED_FIELD. Synthetic maps to DEMO_SYNTHETIC, never field.','observed_M06_records':len(load(ROOT/'data/observations/m06/normalized/observations.json')),'old_importer_modified':False,'M09_started':False}
 DOC.mkdir(parents=True,exist_ok=True);(DOC/'M06_ASSETS_AUDIT.json').write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');return value
def map_data(location_id):
 plans=load(ROOT/'documentation/m06/survey-plan.json');selected=next(p for p in plans if p['location_id']==location_id);root=E.parse(ROOT/'simulation/network/m051/provisional/network.net.xml').getroot();edges={e.get('id'):e for e in root.findall('edge') if e.get('function')!='internal'};candidate=[c for c in root.findall('connection') if c.get('from')==selected['edge_id'] or c.get('to')==selected['edge_id']];related={selected['edge_id']}|{c.get('from') for c in candidate}|{c.get('to') for c in candidate}
 return {'location_id':location_id,'selected_edge':selected['edge_id'],'model_reference_only':True,'field_camera_position':None,'source_network_sha256':digest(ROOT/'simulation/network/m051/provisional/network.net.xml'),'locations':plans,'edges':[{'id':eid,'shape':[[float(v) for v in p.split(',')] for p in edges[eid].find('lane').get('shape').split()],'model_lanes':len(edges[eid].findall('lane'))} for eid in sorted(related) if eid in edges],'candidate_connections':[dict(c.attrib) for c in candidate],'mapping_status':'NEEDS FIELD VERIFICATION — not an approved physical camera position'}
if __name__=='__main__':print('M06 assets audited:',len(audit()['assets']))
