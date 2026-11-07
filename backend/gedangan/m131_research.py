"""Public-only retrieval with byte-level provenance and existing-content reuse."""
import urllib.request,urllib.parse,urllib.error,csv,re,sys,time,concurrent.futures
from .m13_common import ROOT,sha,load,save,now,identity
DOC=ROOT/'documentation/m13_1';DATA=ROOT/'data/official/m13_1';BASE='https://opendata.sidoarjokab.go.id';LOG=DOC/'http-register.json'
def known_hashes():
 result={}
 for p in [ROOT/'documentation/m13/source-file-audit.json',ROOT/'documentation/m13/web-source-audit.json']:
  for r in load(p):
   if r.get('sha256')and r.get('path'):result[r['sha256']]=r['path']
 for p in (DATA/'originals').glob('*'):
  if p.is_file():result[sha(p)]=p.relative_to(ROOT).as_posix()
 return result
def fetch(url,kind='metadata',tag=None):
 DOC.mkdir(parents=True,exist_ok=True);records=load(LOG)if LOG.exists()else[]
 # Cache only successful previous retrieval in this audit, not failures.
 existing=next((r for r in records if r['url']==url and r.get('status')=='RETRIEVED'),None)
 if existing:return existing
 record={'url':url,'kind':kind,'tag':tag,'accessed_utc':now()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Gedangan-Public-Research-M13.1/1.0','Accept':'*/*'})
  with urllib.request.urlopen(req,timeout=30)as response:
   body=response.read(24000001);record.update(http_status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type',''))
  if len(body)>24000000:raise ValueError('24MB research retrieval bound exceeded')
  digest=__import__('hashlib').sha256(body).hexdigest();record.update(sha256=digest,bytes=len(body),status='RETRIEVED')
  pdf=body.startswith(b'%PDF');xls=body.startswith(b'\xd0\xcf\x11\xe0');xlsx=body.startswith(b'PK\x03\x04');binary=pdf or xls or xlsx
  if kind=='data'and not(binary or any(t in record['content_type']for t in ['csv','json','xml','text/plain'])):record['content_warning']='Actual response is not a recognized table/PDF; inspect HTML rather than assume data.'
  ext='.pdf'if pdf else'.xls'if xls else'.xlsx'if xlsx else'.json'if body.lstrip().startswith((b'{',b'['))else'.csv'if'csv'in record['content_type']else'.html'
  known=known_hashes()
  if binary and digest in known:record.update(path=known[digest],reused_existing_original=True,new_original_saved=False)
  else:
   folder=DATA/'originals'if binary or kind=='data'and ext=='.csv'else DOC/'http';p=folder/(digest[:24]+ext);p.parent.mkdir(parents=True,exist_ok=True)
   if not p.exists():p.write_bytes(body)
   record.update(path=p.relative_to(ROOT).as_posix(),reused_existing_original=False,new_original_saved=bool(binary or folder==DATA/'originals'))
 except Exception as exc:record.update(status='UNAVAILABLE',error=str(exc),http_status=getattr(exc,'code',None))
 records.append(record);save(LOG,records);return record
def action(name,**kwargs):
 url=BASE+'/api/3/action/'+name+'?'+urllib.parse.urlencode(kwargs);r=fetch(url,'ckan',name)
 if r['status']=='RETRIEVED':
  try:
   value=load(ROOT/r['path'])
   if value.get('success'):return value['result']
  except (ValueError,AttributeError):pass
 return None
def discover():
 packages={}
 for name in ['data-inventarisasi-dan-analisis-situasi-arus-lalu-lintas','data-indentifikasi-masalah-lalu-lintas','analisis-dampak-lalu-lintas']:
  p=action('package_show',id=name)
  if p:packages[p['id']]=p
 terms=['volume lalu lintas','v/c ratio','kinerja ruas','lalu lintas','Gedangan','LHR','kecepatan','simpang']
 for term in terms:
  result=action('package_search',q=term,rows=100)
  if result:
   for p in result['results']:packages[p['id']]=p
 organizations={p['organization']['name']for p in packages.values()if p.get('organization')and any(s in p.get('organization',{}).get('title','').lower()for s in ['perhubungan','dishub'])}
 for org in organizations:
  result=action('package_search',fq='organization:'+org,rows=1000)
  if result:
   for p in result['results']:packages[p['id']]=p
 save(DOC/'ckan-packages.json',list(packages.values()))
 print('Packages',len(packages),'organizations',organizations,flush=True)
 for p in packages.values():
  print(json_line({'id':p['id'],'name':p['name'],'title':p['title'],'organization':p.get('organization',{}).get('title'),'resources':[{'id':r['id'],'name':r.get('name'),'format':r.get('format'),'url':r['url']}for r in p.get('resources',[])]}),flush=True)
def json_line(v):return __import__('json').dumps(v,ensure_ascii=False)
if __name__=='__main__':discover()
