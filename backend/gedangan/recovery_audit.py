"""Georeferenced OSM/SUMO reference audit, never field-ground-truth certification."""
import json,math,xml.etree.ElementTree as E,urllib.request,statistics
from collections import Counter
from .recovery_common import *
def acquire():
 sources=[('FO_SEP','https://www.sidoarjokab.go.id/berita/detail/1790214058/0','html'),('FO_OCT','https://www.sidoarjokab.go.id/berita/detail/1790902516/0','html'),('FO_JUN','https://www.sidoarjokab.go.id/berita/detail/1782800688/next','html'),('FO_LOCATION','https://www.sidoarjokab.go.id/berita/pengumuman/1792489024/next','html'),('REFERENCE_2023','https://ejournal.undip.ac.id/index.php/ilmulingkungan/article/download/56951/pdf','pdf'),('DIRECTIONAL_2022','https://ejournal.unitomo.ac.id/index.php/gestram/article/download/4649/2441/','pdf'),('SIGNAL_PAPER','https://e-jurnal.pnl.ac.id/portal/article/download/4836/pdf','pdf')]
 rows=[]
 for sid,url,ext in sources:
  p=DOC/'sources'/(sid+'.'+ext)
  try:
   if not p.exists():
    request=urllib.request.Request(url,headers={'User-Agent':'GedanganResearch/1.0 public source audit'})
    with urllib.request.urlopen(request,timeout=35)as r:data=r.read(20*1024*1024)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
   rows.append({'id':sid,'url':url,'local_path':str(p.relative_to(ROOT)),'sha256':sha(p),'status':'RETRIEVED','accessed_utc':datetime.now(timezone.utc).isoformat(),'classification':'OFFICIAL_REFERENCE'if sid.startswith('FO_')else'PUBLISHED_RESEARCH','redistribution':'Original rights retained; local research reference, not included in old portable release'})
  except Exception as exc:rows.append({'id':sid,'url':url,'status':'DOWNLOAD_UNAVAILABLE','error':str(exc),'browser_text_inspected':True})
 save(DOC/'source-register.json',rows);return rows
def audit():
 import sys
 sys.path.insert(0,str(ROOT/'configuration'));from sumo_env_m02 import activate
 activate();import sumolib
 from pyproj import Transformer
 from shapely.geometry import LineString,Point
 net=sumolib.net.readNet(str(PARENT),withInternal=True);root=E.parse(PARENT).getroot();inspection=load(ROOT/'simulation/network/m045/provisional/inspection.json');meta={e['id']:e for e in inspection['edges']};raw=load(ROOT/'geodata/raw/gedangan-network.json');nodes={n['id']:(n['lon'],n['lat'])for n in raw['elements']if n['type']=='node'};ways={w['id']:w for w in raw['elements']if w['type']=='way'};project=Transformer.from_crs(4326,32749,always_xy=True);offset=[float(x)for x in root.find('location').get('netOffset').split(',')];features=[];qa=[];georows=[]
 for eid,e in meta.items():
  edge=net.getEdge(eid);shape=edge.getShape();lonlat=[net.convertXY2LonLat(x,y)for x,y in shape];source=ways.get(e['source_way_id']);sourcepts=[]
  if source:
   sourcepts=[nodes[n]for n in source.get('nodes',[])if n in nodes]
   if not sourcepts:sourcepts=[(g['lon'],g['lat'])for g in source.get('geometry',[])]
  distance=None
  if len(sourcepts)>1:
   projected=LineString([(project.transform(lon,lat)[0]+offset[0],project.transform(lon,lat)[1]+offset[1])for lon,lat in sourcepts]);distance=max(projected.distance(Point(x,y))for x,y in shape)
   features.append({'type':'Feature','geometry':{'type':'LineString','coordinates':sourcepts},'properties':{'layer':'OSM_SOURCE','way_id':e['source_way_id'],'name':e.get('name'),'classification':'OSM_REFERENCE_NOT_SURVEYED'}})
  features.append({'type':'Feature','geometry':{'type':'LineString','coordinates':lonlat},'properties':{'layer':'SUMO','edge':eid,'way_id':e['source_way_id'],'name':e.get('name'),'road_function':e['road_function'],'source_max_offset_m':distance,'allowed':[v for v in ['motorcycle','passenger','delivery','bus','truck','trailer']if any(l.allows(v)for l in edge.getLanes())]}})
  georows.append({'edge':eid,'way_id':e['source_way_id'],'source_max_offset_m':distance,'lanes':len(edge.getLanes()),'source_parameter_status':e['parameter_status']})
 distances=[v['source_max_offset_m']for v in georows if v['source_max_offset_m']is not None];save(DOC/'network-source-overlay.geojson',{'type':'FeatureCollection','features':features,'attribution':'OpenStreetMap contributors / ODbL 1.0; 2026-10-31 snapshot, not physical survey'});save(DOC/'source-geometry-comparison.json',{'network_sha256':sha(PARENT),'source_sha256':sha(ROOT/'geodata/raw/gedangan-network.json'),'max_offset_m':max(distances),'median_offset_m':statistics.median(distances),'note':'Lane-derived SUMO reference center vs whole source OSM way; lane offset/junction trimming expected. This is agreement with OSM, not absolute field accuracy.','edges':georows})
 movements=load(ROOT/'simulation/demand/m04/od-matrix.fixture.json')['movements'];movementrows=[]
 for m in movements:
  ends=m['endpoints']['provisional'];row={'id':m['id'],**ends,'vehicle_classes':{}}
  for v in ['motorcycle','passenger','delivery','bus','truck','trailer']:
   if not ends['origin_edge']or not ends['destination_edge']:row['vehicle_classes'][v]={'connected':False,'reason':'MISSING_ENDPOINT'};continue
   p,cost=net.getShortestPath(net.getEdge(ends['origin_edge']),net.getEdge(ends['destination_edge']),vClass=v)
   row['vehicle_classes'][v]={'connected':p is not None,'route':[e.getID()for e in p]if p else[],'length_m':cost if math.isfinite(cost)else None,'note':'SUMO lane/class path. Conditional, source/tag/type/oversize screens performed again in experiment runner; not a field access approval.'}
  movementrows.append(row)
 missingnames=[]
 for name,needle in [('Sedati/Jenggolo','jenggolo'),('Sukodono','sukodono'),('Ketajen','ketajen'),('Ahmad Yani','yani')]:
  found=[e['id']for e in meta.values()if needle in(e.get('name')or'').lower()];qa.append({'corridor':name,'named_edges':found,'status':'OSM_REFERENCE'if found else'MISSING_OR_ALIASED_NAME'})
  if not found:missingnames.append(name)
 # Include station and railway evidence independently of arterial naming aliases.
 rail=[{'id':e.get('id'),'lane_shapes':[l.get('shape')for l in e.findall('lane')]}for e in root.findall('edge')if e.get('id').startswith('m05_rail_')];save(DOC/'network-audit.json',{'network':str(PARENT.relative_to(ROOT)),'network_sha256':sha(PARENT),'osm_snapshot_date':'2026-10-31','road_edges':len(meta),'internal_edges':sum(e.get('function')=='internal'for e in root.findall('edge')),'road_functions':dict(Counter(e['road_function']for e in meta.values())),'named_corridors':qa,'rail':rail,'source_restriction_relations':sum(e['type']=='relation'and e.get('tags',{}).get('type')=='restriction'for e in raw['elements']),'field_verified':False,'missing_named_corridors':missingnames,'ground_topology_changes':[],'policy':'No existing road geometry/connectivity changed without evidence; road name aliases and disconnected OD gaps are reported, not repaired by invention.','movement_connectivity':movementrows})
 bounds=root.find('location').get('convBoundary').split(',');xmin,ymin,xmax,ymax=map(float,bounds);width,height=1200,900;scale=min((width-40)/(xmax-xmin),(height-90)/(ymax-ymin));svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#f3f6f4"/><text x="20" y="26" font-family="Arial" font-size="18">Gedangan: OSM reference (gray) / SUMO road geometry (teal)</text><text x="20" y="48" font-family="Arial" font-size="12">EPSG:32749 + preserved netOffset; source 2026-10-31. Reference agreement is not field verification.</text>']
 for feature in features:
  layer=feature['properties']['layer'];pts=[]
  for lon,lat in feature['geometry']['coordinates']:
   x,y=project.transform(lon,lat);pts.append(f'{20+(x+offset[0]-xmin)*scale:.2f},{70+(ymax-y-offset[1])*scale:.2f}')
  svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{"#a1a9aa"if layer=="OSM_SOURCE"else"#087d70"}" stroke-width="{2 if layer=="OSM_SOURCE"else .7}"/>')
 svg.append('</svg>');(DOC/'network-source-overlay.svg').write_text(''.join(svg),encoding='utf-8');print(json.dumps({'roads':len(meta),'offset_max_m':max(distances),'corridor_naming_gaps':missingnames}),flush=True)
if __name__=='__main__':
 import sys
 acquire()if '--sources'in sys.argv else audit()
