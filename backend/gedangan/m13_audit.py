"""Inspect source contents read-only; catalogs and simulation are not observations."""
import os,csv,re,collections,urllib.request,sys
from .m13_common import *
sys.path.insert(0,str(DOC/'audit-dependencies'))
SKIP={'.venv','node_modules','__pycache__','.git','build-env','toolchain','FINAL_RELEASE','m13'}
def candidates():
 for parent,dirs,files in os.walk(ROOT):
  dirs[:]=[d for d in dirs if d not in SKIP and not(Path(parent)/d).is_junction()]
  for n in files:
   if n.startswith('M13_'):continue # Current milestone reports are outputs, not preexisting source evidence.
   p=Path(parent)/n
   if p.suffix.lower()in ['.csv','.xlsx','.xls','.sqlite','.db']or(p.suffix=='.pdf'and 'source'in str(p).lower()):yield p
 for rel in ['data/observations/m06/normalized/observations.json','geodata/raw/gedangan-network.json']:
  p=ROOT/rel
  if p.exists():yield p
 for p in sorted((ROOT/'simulation/runs').glob('**/result.json')):yield p
def inspect(p):
 rel=p.relative_to(ROOT).as_posix();kind='REFERENCE_STUDY';info={};tags=collections.Counter();dates=collections.Counter();count=0
 def examine(row):
  nonlocal count
  count+=1
  if isinstance(row,dict):
   for k,v in row.items():
    if k in ['source_class','source_type','classification','status','observation_status','verification_status']and isinstance(v,str):tags[v]+=1
    if k in ['date','observation_date','start_wib','interval_start','timestamp']and isinstance(v,str)and re.match(r'\d{4}-\d{2}-\d{2}',v):dates[v[:10]]+=1
 if p.suffix.lower()=='.csv':
  with p.open(encoding='utf-8-sig',newline='')as f:
   reader=csv.DictReader(f);info['columns']=reader.fieldnames
   for r in reader:examine(r)
 elif p.suffix.lower()in ['.sqlite','.db']:
  tables={}
  with connect(p,True)as c:
   info['integrity_check']=c.execute('PRAGMA integrity_check').fetchone()[0]
   for t, in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
    quoted='"'+t.replace('"','""')+'"';cols=[r[1]for r in c.execute('PRAGMA table_info('+quoted+')')];n=c.execute('SELECT COUNT(*) FROM '+quoted).fetchone()[0];tables[t]={'rows':n,'columns':cols}
    if 'body'in cols:
     for r in c.execute('SELECT body FROM '+quoted):
      try:examine(json.loads(r[0]))
      except (ValueError,TypeError):pass
    elif t in ['evidence','observations']:
     for r in c.execute('SELECT * FROM '+quoted):examine(dict(r))
   info['tables']=tables
 elif p.suffix.lower()in ['.xlsx','.xls']:
  import pandas as pd
  sheets={}
  for name,frame in pd.read_excel(p,sheet_name=None,dtype=object).items():
   sheets[name]={'rows':len(frame),'columns':[str(x)for x in frame.columns]}
   for r in frame.to_dict('records'):examine(r)
  info['sheets']=sheets
 elif p.suffix=='.pdf':
  from pypdf import PdfReader
  pdf=PdfReader(p);text='\n'.join(page.extract_text()or''for page in pdf.pages);info={'pages':len(pdf.pages),'text_characters':len(text),'years_found':sorted(set(re.findall(r'\b20[0-3]\d\b',text))),'contains_2026':bool(re.search(r'\b2026\b',text)),'review':'Publication date/year is not a dated directional interval count. Candidate requires table/method review.'}
  extracted=DOC/'extracted'/(p.stem+'.txt');extracted.parent.mkdir(parents=True,exist_ok=True);extracted.write_text(text,encoding='utf-8')
 else:
  value=load(p)
  if isinstance(value,list):
   for r in value:examine(r)
  elif isinstance(value,dict):
   examine(value);info['top_level_keys']=list(value)[:25]
   if 'elements'in value:info['osm_elements']=len(value['elements'])
 info.update(records_inspected=count,source_status_tags=dict(tags),dates_found=dict(dates))
 if '/simulation/'in '/'+rel or rel.startswith('simulation/'):kind='SIMULATION_OUTPUT'
 elif any(x in rel.lower()for x in ['synthetic','fixture','/qa','/verification/','/portable-user-data','/templates/','/example']):kind='SYNTHETIC_TEST'
 elif any('SYNTHETIC'in t or 'DEMO'in t for t in tags):kind='SYNTHETIC_TEST'
 elif rel=='data/realism_recovery/historical.sqlite':kind='OBSERVED_SECONDARY'
 return {'path':rel,'sha256':sha(p),'bytes':p.stat().st_size,'classification':kind,'calendar_auto_imported':False,'target_2026_verified_rows':0,'inspection_status':'CONTENT_INSPECTED','details':info,'decision':'No automatic promotion. Explicit source scope/date/location/method and review required; source tags alone are not evidence.'}
URLS={
 'DISHUB_2022_VC':'https://opendata.sidoarjokab.go.id/dataset/2ed97d4c-cba0-4e5b-ba53-dc4e5d9ff48b/resource/ab78e87f-5332-4876-a6a3-7ef2d2816c79/download/outcome-visi-ratio-ruas-jalan-kab-sda-.pdf',
 'STTD_2024':'https://digilib.ptdisttd.ac.id/8279/1/Jurnal%20Kajian%20Rencana%20Pengendalian%20Simpang%20Gedangan%20M.Rizky%20Bima.P.pdf',
 'DISHUB_2023_2025_XLS':'https://opendata.sidoarjokab.go.id/dataset/c2b1338b-8c70-4bac-8b4a-16822cac1995/resource/c8e8e01a-6ff4-4da6-89c5-e39700402bae/download/089_2.15.000246_data-indentifikasi-masalah-lalu-lintas.xls',
 'UMPR_2025':'https://journal.umpr.ac.id/index.php/mits/article/download/11418/6353/45315',
 'DIRECTIONAL_2022':'https://ejournal.unitomo.ac.id/index.php/gestram/article/download/4649/2441/'
}
def main():
 DOC.mkdir(parents=True,exist_ok=True);web=[]
 for key,url in URLS.items():
  ext='.xls'if key.endswith('XLS')else'.pdf';p=DOC/'sources'/(key+ext)
  try:
   if not p.exists():
    request=urllib.request.Request(url,headers={'User-Agent':'Gedangan-M13-research/1.0'})
    with urllib.request.urlopen(request,timeout=25)as response:body=response.read(20000000)
    if not(body.startswith(b'%PDF')or ext=='.xls'):raise ValueError('Not a PDF document')
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body)
   entry=inspect(p);entry.update(source_url=url,source_id=key);web.append(entry)
  except Exception as exc:web.append({'source_id':key,'source_url':url,'classification':'REFERENCE_STUDY','inspection_status':'UNAVAILABLE_OR_PARSE_ERROR','error':str(exc),'target_2026_verified_rows':0})
 save(DOC/'web-source-audit.json',web)
 rows=[];before={}
 for p in candidates():
  before[p.relative_to(ROOT).as_posix()]=sha(p)
  try:r=inspect(p)
  except Exception as exc:r={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'classification':'MISSING','inspection_status':'UNREADABLE_REQUIRES_REVIEW','error':str(exc),'calendar_auto_imported':False}
  rows.append(r)
 save(DOC/'source-file-audit.json',rows);save(DOC/'preexisting-source-sha256.json',before)
 # Content and metadata of known reference registers retained separately for human review.
 for rel in ['frontend/public/m06/public-source-register.json','documentation/realism_recovery/source-register.json']:
  p=ROOT/rel
  if p.exists():save(DOC/(p.parent.name+'-'+p.name),load(p))
 with (ROOT/'M13_DATA_SOURCE_REGISTER.csv').open('w',encoding='utf-8-sig',newline='')as f:
  keys=['path','source_id','source_url','sha256','bytes','classification','inspection_status','target_2026_verified_rows','decision','details','error'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader()
  for r in rows+web:w.writerow({**r,'details':json.dumps(r.get('details',{}),ensure_ascii=False)})
 print('Audited',len(rows),'local source/output files and',len(web),'online downloads',flush=True)
if __name__=='__main__':main()
