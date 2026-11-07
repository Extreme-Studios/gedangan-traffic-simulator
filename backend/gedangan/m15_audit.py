"""Retained geospatial/source audit and read-only M14 insertion reconstruction."""
import xml.etree.ElementTree as E,math,statistics,copy
from collections import Counter
from .m15_common import *
from .m15_network import model,catalog,route
from .m14_vehicles import registry
from .m04_demand import activate
def geometry():
 activate()
 from pyproj import Transformer
 from shapely.geometry import LineString,Point
 from .recovery_routing import context
 net,root,meta,_=context(str(NETWORK.resolve()),sha(NETWORK));raw=load(ROOT/'geodata/raw/gedangan-network.json');nodes={n['id']:(n['lon'],n['lat'])for n in raw['elements']if n['type']=='node'};ways={w['id']:w for w in raw['elements']if w['type']=='way'};tr=Transformer.from_crs(4326,32749,always_xy=True);offset=list(map(float,root.find('location').get('netOffset').split(',')));source=[];sumo=[];geo=[];features=[];seen=set()
 for eid,m in meta.items():
  e=net.getEdge(eid);w=ways.get(m['source_way_id']);ll=[nodes[n]for n in w['nodes']if n in nodes]if w else[]
  if not ll and w:ll=[(p['lon'],p['lat'])for p in w.get('geometry',[])]
  pts=[(tr.transform(lon,lat)[0]+offset[0],tr.transform(lon,lat)[1]+offset[1])for lon,lat in ll];line=LineString(pts)if len(pts)>1 else None;dist=max((line.distance(Point(x,y))for x,y in e.getShape()),default=0)if line else None
  if m['source_way_id']not in seen and pts:
   row={'id':str(m['source_way_id']),'name':m.get('name'),'points':pts};source.append(row);features.append({'type':'Feature','geometry':{'type':'LineString','coordinates':ll},'properties':{'layer':'OSM_SOURCE','way_id':m['source_way_id'],'name':m.get('name'),'status':'OSM_REFERENCE_NOT_FIELD_VERIFIED'}});seen.add(m['source_way_id'])
  row={'id':eid,'name':m.get('name'),'role':m['road_function'],'points':e.getShape(),'source_way_id':m['source_way_id'],'source_offset_m':dist};sumo.append(row);features.append({'type':'Feature','geometry':{'type':'LineString','coordinates':[net.convertXY2LonLat(x,y)for x,y in e.getShape()]},'properties':{'layer':'SUMO','edge':eid,'source_way_id':m['source_way_id'],'source_offset_m':dist}});geo.append({'edge':eid,'source_way_id':m['source_way_id'],'source_max_center_offset_m':dist,'parameter_status':m['parameter_status']})
 node_error=[]
 for j in root.findall('junction'):
  if j.get('id','').startswith('osm_')and int(j.get('id')[4:])in nodes:
   x,y=tr.transform(*nodes[int(j.get('id')[4:])]);node_error.append(math.hypot(float(j.get('x'))-x-offset[0],float(j.get('y'))-y-offset[1]))
 lanes=[{'id':l.get('id'),'edge':e.get('id'),'internal':e.get('function')=='internal','length_m':float(l.get('length')),'width_m':float(l.get('width','3.2')),'allowed':l.get('allow'),'points':[[float(v)for v in p.split(',')[:2]]for p in l.get('shape').split()]}for e in root.findall('edge')for l in e.findall('lane')];short=sorted([l for l in lanes if l['length_m']<5],key=lambda l:l['length_m']);origins=[]
 for a in catalog()['approaches']:
  rr=route('car',a['id'],'straight');origin=net.getEdge(rr['origin_edge']);origins.append({'approach':a['id'],'anchor_edge':a['anchor_edge'],'anchor_node':net.getEdge(a['anchor_edge']).getToNode().getID(),'origin_edge':origin.getID(),'origin_length_m':origin.getLength(),'upstream_route_m':a['upstream_length_m'],'exit_edge':rr['destination_edge'],'exit_length_m':net.getEdge(rr['destination_edge']).getLength(),'route_length_m':rr['route_length_m'],'source_way_id':meta[origin.getID()]['source_way_id'],'source_status':'OSM topological provenance; lengths/lanes not surveyed'})
 from .m09_export import scene
 sc=scene(NETWORK);renderer_error=max(math.hypot(p[0]-q[0],p[1]-q[1])for l in lanes for p,q in zip(l['points'],next(x['shape']for x in sc['lanes']if x['id']==l['id'])));rails=[l for l in lanes if l['edge'].startswith('m05_rail')];named=[]
 for label,needle in [('A. Yani','yani'),('Sukodono','sukodono'),('Ketajen','ketajen'),('Frontage','frontage'),('Sedati','sedati'),('Jenggolo','jenggolo'),('Jenggala','jenggala')]:
  hits=[e['id']for e in meta.values()if needle in(e.get('name')or'').lower()];named.append({'corridor':label,'matched_edges':hits,'status':'OSM_NAMED_REFERENCE'if hits else'UNVERIFIED_NAME_NOT_FOUND_IN_RETAINED_EXTENT'})
 summary={'status':'PARTIAL','reason':'Agreement with retained OSM reference, not an independent survey/2026 ground truth. Missing names, width/timing/storage assumptions and restrictive network remain visible.','network_sha256':sha(NETWORK),'raw_source_sha256':sha(ROOT/'geodata/raw/gedangan-network.json'),'source_metadata':load(ROOT/'geodata/sources/gedangan-network.metadata.json'),'crs':'EPSG:32749','offset':offset,'node_osm_comparisons':len(node_error),'max_node_projection_error_m':max(node_error),'road_edge_count':len(sumo),'max_centerline_source_offset_m':max(g['source_max_center_offset_m']for g in geo if g['source_max_center_offset_m']is not None),'median_centerline_source_offset_m':statistics.median(g['source_max_center_offset_m']for g in geo if g['source_max_center_offset_m']is not None),'renderer_lane_shape_error_m':renderer_error,'short_external_under5m':sum(not l['internal']for l in short),'short_internal_under5m':sum(l['internal']for l in short),'minimum_lane_length_m':min(l['length_m']for l in lanes),'lane_widths_m':dict(Counter(l['width_m']for l in lanes)),'named_corridors':named,'boundaries':origins,'source_turn_restrictions':sum(w['type']=='relation'and w.get('tags',{}).get('type')=='restriction'for w in raw['elements']),'new_edges':0,'new_connections':0,'network_derivative_required':False,'correction_scope':'Approach/routing catalog only; network geometry and permissions not changed','rail_status':'Mapped single directed centerline, source shared crossing; reverse rail topology/stopline/gate physical survey unverified'}
 save(DOC/'geometry-audit.json',summary);save(DOC/'source-geometry-comparison.json',geo);save(DOC/'short-lanes.json',short);save(DOC/'network-source-overlay.geojson',{'type':'FeatureCollection','features':features,'attribution':'OpenStreetMap contributors / ODbL1.0, retained2026-10-31 source; no field certification'});save(DOC/'technical-map.json',{'bounds':list(map(float,root.find('location').get('convBoundary').split(','))),'crs':'EPSG:32749 local SUMO x/y + inverse netOffset','source':source,'sumo':sumo,'lanes':lanes,'rail':rails,'signals':sc['heads'],'crossing':sc['crossing'],'boundaries':origins,'catalog':catalog(),'attribution':'OpenStreetMap contributors / ODbL1.0; geometry acceptance PARTIAL'})
 # Standalone inspectable source/network overlay; inverse transform retained in GeoJSON.
 xmin,ymin,xmax,ymax=list(map(float,root.find('location').get('convBoundary').split(',')));scale=min(1120/(xmax-xmin),800/(ymax-ymin));svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900"><rect width="1200" height="900" fill="#f5f7f4"/><text x="25" y="28" font-family="Arial" font-size="18">M15 Gedangan: OSM source / SUMO existing network</text><text x="25" y="50" font-family="Arial" font-size="12">EPSG:32749 + netOffset. Teal SUMO / gray source. PARTIAL - not independently field surveyed.</text>']
 for rows,color,width in [(source,'#9ba7a4',2),(sumo,'#087f75',.7),(rails,'#b5633d',1.5)]:
  for row in rows:
   pts=' '.join(f'{30+(x-xmin)*scale:.2f},{75+(ymax-y)*scale:.2f}'for x,y in row['points']);svg.append(f'<polyline points="{pts}" stroke="{color}" stroke-width="{width}" fill="none"/>')
 svg.append('</svg>');(DOC/'network-source-overlay.svg').write_text(''.join(svg),encoding='utf-8');save(DOC/'route-compatibility.json',[{'class':v['id'],'approach':a['id'],'turn':t,**route(v['id'],a['id'],t)}for v in registry()for a in catalog()['approaches']for t in a['movements']]);return summary

def parent_diagnosis():
 from .m15_diagnostics import Diagnostics
 from .recovery_routing import context
 parent=ROOT/'simulation/runs/m14/67e1a759e0845754c09be215';result=copy.deepcopy(load(parent/'result.json'));ledger=load(parent/'vehicle-results.json');demand=load(parent/'demand.json');dest=DOC/'m14-reconstruction';dest.mkdir(parents=True,exist_ok=True);save(dest/'demand.json',demand);net,*_=context(str(NETWORK.resolve()),sha(NETWORK));d=Diagnostics(demand['requests'],net,0);departed=set();arrived=set();dep=sorted((float(q['tripinfo']['depart']),q['id'])for q in ledger if q['departed']);arr=sorted((float(q['tripinfo']['arrival']),q['id'])for q in ledger if q['arrived']);di=ai=0
 for _,node in E.iterparse(parent/'fcd.xml',events=('end',)):
  if node.tag!='timestep':continue
  t=float(node.get('time'))+.5
  while di<len(dep)and dep[di][0]<t:departed.add(dep[di][1]);di+=1
  while ai<len(arr)and arr[ai][0]<t:arrived.add(arr[ai][1]);ai+=1
  states=[{'id':v.get('id'),'lane':v.get('lane'),'speed':float(v.get('speed')),'pos':float(v.get('pos'))}for v in node.findall('vehicle')];d.sample(t,states,departed,arrived);node.clear()
 d.finish(ledger,result,dest);save(dest/'reconstructed-result.json',result);save(dest/'provenance.json',{'source_run':'m14/67e1a759e0845754c09be215','source_hashes':{p:sha(parent/p)for p in ['demand.json','vehicle-results.json','fcd.xml','tripinfo.xml']},'clock':'FCD time +0.5s aligns post-step M14 TraCI samples. Cumulative departure uses actual times < sample boundary. Reconstructed pending not live TraCI reject reasons.','no_parent_writes':True});return result
if __name__=='__main__':
 protect();print(geometry()['status'],flush=True);print({k:v for k,v in parent_diagnosis().items()if k in ['requested','routed','departed','arrived','not_departed']},flush=True)
