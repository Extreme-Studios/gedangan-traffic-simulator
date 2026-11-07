"""Metric source/baseline/derivative comparison. No invented survey tolerances."""
import math,xml.etree.ElementTree as E
from pathlib import Path
from shapely.geometry import LineString,Point,Polygon,mapping
from pyproj import Transformer
from .m04_demand import ROOT,load,save,sha
DOC=ROOT/'documentation/m051';NET=ROOT/'simulation/network/m051'
def coords(text):return [tuple(map(float,p.split(','))) for p in text.split()]
def measure():
 a=E.parse(ROOT/'simulation/network/m045/provisional/network.net.xml').getroot();b=E.parse(ROOT/'simulation/network/m05/provisional/network.net.xml').getroot();origin=load(ROOT/'simulation/network/m045/provisional/inspection.json')['origin_utm_m'];tr=Transformer.from_crs(4326,32749,always_xy=True)
 raw=load(ROOT/'geodata/raw/gedangan-network.json')['elements'];nodes={n['id']:n for n in raw if n['type']=='node'};ways={w['id']:w for w in raw if w['type']=='way'}
 def xy(i):
  n=nodes[i];x,y=tr.transform(n['lon'],n['lat']);return (x-origin[0],y-origin[1])
 center=xy(859708050);road=LineString([xy(i) for i in ways[1240685448]['nodes']]);rail=LineString([xy(i) for i in load(ROOT/'simulation/network/m05/provisional/rail-provenance.json')['source_node_chain']]);ae={e.get('id'):e for e in a.findall('edge')};be={e.get('id'):e for e in b.findall('edge')};al={l.get('id'):l for e in a.findall('edge') for l in e.findall('lane')};bl={l.get('id'):l for e in b.findall('edge') for l in e.findall('lane')}
 differences=[];overlay=[];vectors=[]
 for kind,old,new in [('edge',ae,be),('lane',al,bl)]:
  for id,e in old.items():
   if id not in new or not e.get('shape') or not new[id].get('shape'):continue
   p,q=coords(e.get('shape')),coords(new[id].get('shape'))
   if p==q:continue
   if Point(center).distance(LineString(p))>100 and Point(center).distance(LineString(q))>100:continue
   ls0,ls1=LineString(p),LineString(q);d={'kind':kind,'id':id,'internal':id.startswith(':'),'before':p,'after':q,'start_displacement_m':math.dist(p[0],q[0]),'end_displacement_m':math.dist(p[-1],q[-1]),'hausdorff_m':ls0.hausdorff_distance(ls1),'length_delta_m':ls1.length-ls0.length,'before_shape_length_m':ls0.length,'after_shape_length_m':ls1.length,'comparison_warning':'Internal IDs may be reassigned; use movement-keyed connector audit for semantic road comparisons.' if id.startswith(':') else None,'before_max_distance_to_reference_way1240685448_m':max(Point(ls0.interpolate(i/max(1,math.ceil(ls0.length)),normalized=True)).distance(road) for i in range(max(1,math.ceil(ls0.length))+1)) if not id.startswith(':') and kind=='lane' else None};differences.append(d)
   for x,y in [(p[0],q[0]),(p[-1],q[-1])]:
    if x!=y:vectors.append({'id':id,'kind':kind,'from':x,'to':y,'m':math.dist(x,y)})
 for kind,source,color in [('m045',al,'#65d8e8'),('m05',bl,'#ffbb75')]:
  for id,l in source.items():
   pts=coords(l.get('shape'));line=LineString(pts)
   if Point(center).distance(line)<90:overlay.append({'kind':kind,'id':id,'points':pts,'internal':id.startswith(':'),'rail':l.get('allow')=='rail','color':color})
 connections=[];stops=[];conflicts=[]
 for c in b.findall('connection'):
  if c.get('tl')!='osm_859708050' or c.get('from','').startswith('m05_rail_'):continue
  lid=c.get('from')+'_'+c.get('fromLane');to=c.get('to')+'_'+c.get('toLane');via=c.get('via');p=coords(bl[lid].get('shape'));v=coords(bl[via].get('shape'));q=coords(bl[to].get('shape'));u=(p[-1][0]-p[-2][0],p[-1][1]-p[-2][1]);norm=math.hypot(*u);normal=(-u[1]/norm,u[0]/norm);width=float(bl[lid].get('width','3.2'));stop=[(p[-1][0]+normal[0]*width/2,p[-1][1]+normal[1]*width/2),(p[-1][0]-normal[0]*width/2,p[-1][1]-normal[1]*width/2)];cross=LineString(v).intersection(rail);localrail=coords(bl['m05_rail_7_0'].get('shape'));rv=(localrail[-1][0]-localrail[0][0],localrail[-1][1]-localrail[0][1]);angle=math.degrees(math.acos(min(1,abs(u[0]*rv[0]+u[1]*rv[1])/(norm*math.hypot(*rv)))))
  stops.append({'lane':lid,'stop_line':stop,'model_position':p[-1],'distance_to_rail_centerline_m':Point(p[-1]).distance(rail),'distance_to_nominal_train_body_m':Point(p[-1]).distance(rail)-1.4,'rail_road_angle_deg':angle,'status':'NEEDS FIELD VERIFICATION','method':'SUMO incoming lane endpoint cross-section; Euclidean distance to projected source rail polyline; angle of incoming last segment vs incoming rail segment. Not a surveyed stop line.'})
  connections.append({'from':lid,'via':via,'to':to,'incoming_gap_m':math.dist(p[-1],v[0]),'outgoing_gap_m':math.dist(v[-1],q[0]),'incoming_heading_kink_deg':math.degrees(math.acos(min(1,max(-1,(u[0]*(v[1][0]-v[0][0])+u[1]*(v[1][1]-v[0][1]))/(norm*math.dist(v[0],v[1])))))),'road_crosses_rail_geometrically':not cross.is_empty,'allowed_crossing_only_when_controller_permits':True,'path':p+v+q})
  region=LineString(v).buffer(width/2).intersection(rail.buffer(1.4))
  if not region.is_empty:conflicts.append(mapping(region))
 j=next(j for j in b.findall('junction') if j.get('id')=='osm_859708050');center_offset=math.dist(center,(float(j.get('x')),float(j.get('y'))))
 old_connections={(c.get('from'),c.get('to'),c.get('fromLane'),c.get('toLane')):c for c in a.findall('connection') if not c.get('from','').startswith(':')}
 connector_comparisons=[]
 for c in b.findall('connection'):
  key=(c.get('from'),c.get('to'),c.get('fromLane'),c.get('toLane'));old=old_connections.get(key)
  if old is None or not old.get('via') or not c.get('via'):continue
  if 'osm_859708050' not in c.get('via') and not any(e.startswith('w1240685448_s1_') for e in key[:2]):continue
  p0=coords(al[old.get('via')].get('shape'));p1=coords(bl[c.get('via')].get('shape'));connector_comparisons.append({'movement':key,'old_internal_id':old.get('via'),'new_internal_id':c.get('via'),'before':p0,'after':p1,'hausdorff_m':LineString(p0).hausdorff_distance(LineString(p1)),'method':'Compare same external road movement, not reused internal numeric IDs.'})
 old_junctions={j.get('id'):j for j in a.findall('junction')};junction_changes=[]
 for jn in b.findall('junction'):
  old=old_junctions.get(jn.get('id'))
  if old is not None and not jn.get('id').startswith(':') and any(old.get(k)!=jn.get(k) for k in ['shape','type','radius']):junction_changes.append({'id':jn.get('id'),'old':dict(old.attrib),'new':dict(jn.attrib),'position_displacement_m':math.hypot(float(old.get('x'))-float(jn.get('x')),float(old.get('y'))-float(jn.get('y')))})
 ri=ways[1240685448]['nodes'].index(859708050);road_tangent=(xy(ways[1240685448]['nodes'][ri+1])[0]-xy(ways[1240685448]['nodes'][ri-1])[0],xy(ways[1240685448]['nodes'][ri+1])[1]-xy(ways[1240685448]['nodes'][ri-1])[1]);rn=ways[1330582010]['nodes'];ii=rn.index(859708050);rail_tangent=(xy(rn[ii+1])[0]-xy(rn[ii-1])[0],xy(rn[ii+1])[1]-xy(rn[ii-1])[1]);raw_angle=math.degrees(math.acos(abs(sum(x*y for x,y in zip(road_tangent,rail_tangent)))/(math.hypot(*road_tangent)*math.hypot(*rail_tangent))))
 result={'status':'PARTIAL — NEEDS FIELD SURVEY','crs':'EPSG:32749 metres, local offset from M04.5 origin','origin_utm_m':origin,'source_center':center,'model_center_offset_m':center_offset,'source_node_coordinates_changed':False,'differences':differences,'movement_keyed_connector_comparisons':connector_comparisons,'junction_envelope_changes':junction_changes,'raw_source_crossing_angle_deg':raw_angle,'added_internal_lane_ids':sorted(set(bl)-set(al)),'retired_internal_lane_ids':sorted(set(al)-set(bl)),'stop_lines':stops,'connections':connections,'tolerance':'MISSING: no official/survey tolerance. Numerical differences are not declared physically safe by an invented threshold.','reason':'OSM provides shared topology and approximate centerlines; physical stop line, gate position, track clearance and swept path not surveyed.','source_sha256':sha(ROOT/'geodata/raw/gedangan-network.json'),'m045_sha256':sha(ROOT/'simulation/network/m045/provisional/network.net.xml'),'m05_sha256':sha(ROOT/'simulation/network/m05/provisional/network.net.xml')}
 save(DOC/'geometry.json',result);save(DOC/'geometry-overlay.json',{'center':center,'road_source':list(road.coords),'rail_source':list(rail.coords),'layers':overlay,'vectors':vectors,'stop_lines':stops,'conflict_regions':conflicts,'junction_envelope':coords(j.get('shape')),'status':result['status']})
 NET.mkdir(parents=True,exist_ok=True)
 import shutil
 for mode in ['strict','provisional']:
  (NET/mode).mkdir(exist_ok=True)
  for name in ['network.net.xml','rail-provenance.json']:
   src=ROOT/'simulation/network/m05'/mode/name
   if src.exists():shutil.copy2(src,NET/mode/name)
 save(NET/'comparison-manifest.json',{'strategy':'No unsupported geometric remediation. M05.1 execution copies are byte-identical M05 networks; measured source ambiguity retained, not beautified.','provisional_sha256':sha(NET/'provisional/network.net.xml'),'equal_to_m05':sha(NET/'provisional/network.net.xml')==result['m05_sha256'],'new_road_connections':0})
 print('external',[(d['kind'],d['id'],round(d['hausdorff_m'],3)) for d in differences if not d['internal']]);print('stops',stops)
 return result
if __name__=='__main__':measure()
