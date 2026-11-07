"""Download selected official resources and inspect all worksheets / PDF text."""
import sys,re,json
from .m131_research import *
sys.path.insert(0,str(ROOT/'documentation/m13/audit-dependencies'))
def inspect_record(r):
 if r['status']!='RETRIEVED':return r
 p=ROOT/r['path'];body=p.read_bytes();summary={}
 try:
  if body.startswith(b'%PDF'):
   from pypdf import PdfReader
   pdf=PdfReader(p);pages=[page.extract_text()or''for page in pdf.pages];summary={'format':'PDF','pages':len(pages),'text_characters':sum(map(len,pages)),'locations':sorted({x for x in ['Gedangan','Jenggolo','Jenggala','Sukodono','Ketajen','Aloha','Pahlawan','Ahmad Yani','A. Yani']if x.lower()in '\n'.join(pages).lower()})};save(DOC/'extracted'/(r['sha256']+'.json'),{'pages':[{'page':i+1,'text':s}for i,s in enumerate(pages)]})
  elif body.startswith((b'\xd0\xcf\x11\xe0',b'PK\x03\x04')):
   import pandas as pd
   sheets={}
   for name,frame in pd.read_excel(p,sheet_name=None,header=None,dtype=object).items():
    values=[]
    for row in frame.itertuples(index=False,name=None):
     values.append([None if pd.isna(v)else v.isoformat()if hasattr(v,'isoformat')else v.item()if hasattr(v,'item')else v for v in row])
    sheets[name]={'rows':len(frame),'columns':len(frame.columns),'values':values}
   summary={'format':'XLS/XLSX','sheets':{n:{k:v for k,v in x.items()if k!='values'}for n,x in sheets.items()},'all_values':sheets};save(DOC/'extracted'/(r['sha256']+'.json'),summary)
  else:summary={'format':'HTML/JSON_METADATA_OR_ERROR','not_raw_observation_table':True}
  return {**r,'inspection_status':'INSPECTED','inspection':summary}
 except Exception as exc:return {**r,'inspection_status':'PARSE_ERROR','inspection_error':str(exc)}
def main():
 packages=load(DOC/'ckan-packages.json');selected=[]
 for p in packages:
  if p.get('organization',{}).get('name')=='dinas-perhubungan'and re.search(r'v-c-ratio|inventarisasi-dan-analisis|indentifikasi-masalah|^analisis-dampak|frekuensi-lalu|pengendalian-lalu|pengendalian-Lalu|^alat-pemberi|batas-kecepatan|data-frekuensi|data-ruang-lalu|asal-tujuan-perjalanan',p['name'],re.I):selected.append(p)
 save(DOC/'selected-ckan-packages.json',selected);out=[]
 for p in selected:
  fetch(BASE+'/dataset/'+p['name'],'metadata',p['name'])
  for resource in p.get('resources',[]):
   r=fetch(resource['url'],'data',p['name']);r={**r,'package_id':p['id'],'dataset_title':p['title'],'resource_id':resource['id'],'resource_name':resource.get('name'),'publisher':'Dinas Perhubungan Kabupaten Sidoarjo'};out.append(inspect_record(r))
   print(p['name'],r['status'],r.get('bytes'),flush=True)
 extras=[
 ('BPS_2026','https://sirusa.web.bps.go.id/metadata/kegiatan/c4e9f75e-ff36-bfba-8aab-e1a79719b138','metadata'),
 ('BPS_2024','https://sirusa.web.bps.go.id/metadata/kegiatan/7ba8b075-98b5-54cd-ba7f-3ee5a3818382','metadata'),
 ('UMPR_ARTICLE','https://journal.umpr.ac.id/index.php/mits/article/view/11418','metadata'),
 ('UMPR_PDF_VIEW','https://journal.umpr.ac.id/index.php/mits/article/view/11418/6353','metadata'),
 ('UMPR_PDF','https://journal.umpr.ac.id/index.php/mits/article/download/11418/6353/45315','data'),
 ('JENGGOLO_2023','https://e-jurnal.pnl.ac.id/portal/article/download/5567/pdf','data'),
 ('UPN_2025_REPOSITORY','https://repository.upnjatim.ac.id/47744/','metadata')]
 for tag,url,kind in extras:out.append(inspect_record(fetch(url,kind,tag)))
 save(DOC/'resource-inspections.json',out);print('Inspected',len(out),'resources',flush=True)
if __name__=='__main__':main()
