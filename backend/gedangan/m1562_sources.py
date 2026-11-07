"""Bounded, cached public geographic source acquisition. No imagery bypass."""
from .m1562_common import *
import urllib.request,xml.etree.ElementTree as ET

def main():
 sources=DOC/'sources';sources.mkdir(parents=True,exist_ok=True)
 attempts=[]
 for label,url,filename in [
  ('OSM API bounded map','https://api.openstreetmap.org/api/0.6/map?bbox=112.718,-7.402,112.736,-7.374','gedangan.osm'),
  ('Wikimedia station metadata','https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url%7Cextmetadata&titles=File:StGedanganSDA.jpg','station-metadata.json')]:
  path=sources/filename
  try:
   if not path.exists():
    req=urllib.request.Request(url,headers={'User-Agent':'GedanganVisualResearch/15.6.2 (local educational simulator; public data only)'})
    with urllib.request.urlopen(req,timeout=45)as response:raw=response.read(30000000)
    path.write_bytes(raw)
   attempts.append({'source':label,'url':url,'status':'ACQUIRED','path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'bytes':path.stat().st_size})
  except Exception as exc:attempts.append({'source':label,'url':url,'status':'UNAVAILABLE','error':str(exc)})
 save(DOC/'source-attempts.json',{'retrieved_utc':now(),'attempts':attempts,'local_osm':'geodata/raw/gedangan-network.json: 52013 elements, zero building tags; prior road-focused extraction cannot provide footprints','osm_license':'ODbL 1.0; OpenStreetMap contributors; https://www.openstreetmap.org/copyright'})
 print(json.dumps(attempts))
if __name__=='__main__':main()
