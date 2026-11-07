"""Public reference acquisition, no inference of present-day rules from old maps."""
import urllib.request,urllib.parse
from .m155_common import *
SOURCES=[('S-GOV-PETA','https://sidoarjokab.go.id/peta-jalan','html'),('S-GOV-GEO','https://sidoarjokab.go.id/jalan','json'),('S-STTD','https://digilib.ptdisttd.ac.id/8270/','html'),('S-UIN','https://digilib.uinsa.ac.id/63857/2/Nurul%20Aulia%20Fadilah_H95219051%20ok.pdf','pdf')]
def main():
 rows=[]
 for sid,url,ext in SOURCES:
  p=DOC/'sources'/(sid+'.'+ext)
  try:
   if not p.exists():
    request=urllib.request.Request(url,headers={'User-Agent':'GedanganRealityCheck/1.0 public research reference'})
    with urllib.request.urlopen(request,timeout=45)as r:data=r.read(25000000);status=r.status
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
   rows.append({'id':sid,'url':url,'local_file':str(p.relative_to(ROOT)),'sha256':sha(p),'accessed_utc':now(),'status':'RETRIEVED','purpose':'Public map/corridor naming reference only; not official2026 lane/turn/signal clearance','rights':'Original rights retained. Local research reference, not bundled into M12 or promoted to observation.'})
  except Exception as e:rows.append({'id':sid,'url':url,'status':'UNAVAILABLE','error':str(e)})
 save(DOC/'source-register.json',rows);print([{k:r[k]for k in ['id','status']}for r in rows],flush=True)
if __name__=='__main__':main()
