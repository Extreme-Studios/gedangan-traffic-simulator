"""Follow links actually exposed by official metadata / publisher pages."""
import re
from .m131_research import *
from .m131_collect import inspect_record
def main():
 rows=[]
 for r in list(load(LOG)):
  if r.get('tag')in ['BPS_2026','BPS_2024']and r['status']=='RETRIEVED':
   text=(ROOT/r['path']).read_text(encoding='utf-8');match=re.search("const apiUrl = '([^']+)'",text)
   if match:rows.append(inspect_record(fetch('https://sirusa.web.bps.go.id'+match[1],'metadata',r['tag']+'_EXPORT')))
 # These chapter links are PUBLIC on the repository record; restricted chapters/appendix are not requested.
 for tag,url in [('UPN_2025_BAB1','https://repository.upnjatim.ac.id/47744/2/21035010023-bab1.pdf'),('UPN_2025_BAB5','https://repository.upnjatim.ac.id/47744/6/21035010023-bab5.pdf'),('UPN_2025_COVER','https://repository.upnjatim.ac.id/47744/1/21035010023-cover.pdf')]:rows.append(inspect_record(fetch(url,'data',tag)))
 for tag,url in [('DISHUB_HOME','https://www.dishub.sidoarjokab.go.id/'),('DATA_GO_ID_SEARCH_RESULT','https://data.go.id/dataset/dataset/data-inventarisasi-dan-analisis-situasi-arus-lalu-lintas')]:rows.append(inspect_record(fetch(url,'metadata',tag)))
 for package in load(DOC/'selected-ckan-packages.json'):
  for resource in package['resources']:
   if resource.get('datastore_active'):
    result=action('datastore_search',resource_id=resource['id'],limit=10000)
    if result is not None:save(DOC/'datastore'/(resource['id']+'.json'),{'dataset':package['name'],'resource':resource['id'],'result':result})
 save(DOC/'followup-inspections.json',rows);print([(r['tag'],r['status'],r.get('path'),r.get('bytes'),r.get('error'))for r in rows],flush=True)
if __name__=='__main__':main()
