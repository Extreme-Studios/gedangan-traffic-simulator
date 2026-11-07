"""Deterministic low-rise render context, screened against full frozen lane envelopes."""
import math,random
from shapely.geometry import LineString,Polygon,Point
from shapely.ops import unary_union
from shapely.affinity import rotate,translate
from .m1561_common import *
def footprint(x,y,w,d,a):
 p=Polygon([(-w/2,-d/2),(w/2,-d/2),(w/2,d/2),(-w/2,d/2)]);return translate(rotate(p,math.degrees(a),origin=(0,0)),xoff=x,yoff=y)
def main():
 protect();scene=load(ROOT/'documentation/m156/scene.json');lanes=scene['lanes'];road=unary_union([LineString(l['shape']).buffer(l['width']/2+2.5)for l in lanes if not l['rail']]);rail=unary_union([LineString(l['shape']).buffer(7)for l in lanes if l['rail']]);exclude=unary_union([road,rail]);rng=random.Random(1561);placed=[];polys=[];skipped=0
 # Geographic anchors belong to frozen scene; building footprints never become traffic geometry.
 station=load(ROOT/'documentation/m155/network-reality-audit.json')['station'];sx,sy=station['point'];stationpoly=footprint(sx-6,sy,12,27,0);station_x,station_y=sx-6,sy
 for ox,oy in [(-12,0),(-18,0),(-24,0),(-18,18),(-24,25),(-30,35)]:
  candidate=footprint(sx+ox,sy+oy,14,29,0)
  if not candidate.intersects(exclude):stationpoly=candidate;station_x,station_y=sx+ox,sy+oy;break
 if not stationpoly.intersects(exclude):
  placed.append({'id':'station-context','kind':'station','x':station_x,'y':station_y,'rotation':0,'width':12,'depth':27,'height':4.1,'roof_height':1.7,'status':'ASSUMED CONTEXT MODEL','source':'OSM station node1359952188; photo2020 roof/facade character, no footprint survey','footprint':list(stationpoly.exterior.coords)});polys.append(stationpoly.buffer(3))
 # Match longitudinal roadside alignment; allow quiet gaps and low-rise strips, no CBD grid.
 unique=set()
 for l in lanes:
  if l['internal']or l['rail']or l['role']not in ['main_arterial_road','feeder_road','frontage_road','collector_road']:continue
  line=LineString(l['shape'])
  if line.length<15:continue
  role=l['role'];step=28 if role!='frontage_road'else 40
  for dist in range(12,int(line.length)-2,step):
   c=line.interpolate(dist);a=line.interpolate(max(0,dist-1));b=line.interpolate(min(line.length,dist+1));dx,dy=b.x-a.x,b.y-a.y;length=math.hypot(dx,dy)
   if not length:continue
   dx/=length;dy/=length
   for side in [-1,1]:
    if rng.random()<.19:continue
    width=rng.uniform(9,18);depth=rng.uniform(7,11);offset=l['width']/2+depth/2+rng.uniform(7,14);x,y=c.x-dy*side*offset,c.y+dx*side*offset
    key=(round(x/12),round(y/12))
    if key in unique:continue
    # group local-front vector points towards the road; Y→negative Z in renderer.
    angle=math.atan2(side*dy,side*dx);poly=footprint(x,y,width+2.2,depth+3.4,angle)
    if poly.intersects(exclude)or any(poly.intersects(p)for p in polys):skipped+=1;continue
    unique.add(key);polys.append(poly.buffer(2));kind='ruko'if role in ['main_arterial_road','feeder_road']and rng.random()<.65 else'house'if rng.random()<.7 else'workshop';height=rng.choice([3.6,3.9,6.4])if kind=='ruko'else rng.uniform(3,4.1)
    placed.append({'id':f'context-{len(placed):04d}','kind':kind,'x':round(x,3),'y':round(y,3),'rotation':angle,'width':width,'depth':depth,'height':height,'roof_height':rng.uniform(1.1,1.65),'units':max(2,round(width/4.5))if kind=='ruko'else 1,'palette':rng.randrange(6),'anchor_lane':l['id'],'status':'ASSUMED CONTEXT MODEL','source':'Frozen roadside direction; contextual type/position/dimensions only, no building footprint assertion','footprint':list(poly.exterior.coords)})
    if len(placed)>=550:break
   if len(placed)>=550:break
  if len(placed)>=550:break
 # Verify the entire padded building/awning envelope, not just its centroid.
 errors=[r['id']for r in placed if Polygon(r['footprint']).intersects(exclude)];assert not errors
 scene['environment']={'version':'m1561-lowrise-1','status':'ASSUMED CONTEXT MODEL','buildings':placed,'station':station,'source_reference':'2020 Rizal Febri Ardiansyah station photo; 2024STTD study; retainedOSM/network','clearance_note':'Padded render footprint excludes frozen lane width/2+2.5m road and7mrail; not field/overhead swept-path certification','maximum_wall_height_m':max(r['height']for r in placed),'forbidden_style':['CBD','glass towers','metropolitan skyline'],'road_or_rail_added':0}
 save(DOC/'scene.json',scene);save(DOC/'context-placement-audit.json',{'status':'PASS_RENDER_FOOTPRINT_EXCLUSION','network_sha256':sha(NETWORK),'count':len(placed),'height_max_wall_m':max(r['height']for r in placed),'height_max_total_m':max(r['height']+r['roof_height']for r in placed),'station_context_placed':any(r['kind']=='station'for r in placed),'rejected_placements':skipped,'overlapping_frozen_envelopes':errors,'source_status':'ASSUMED CONTEXT MODEL; geometry screen is not real building validation','road_buffer_extra_m':2.5,'rail_center_buffer_m':7});save(DOC/'environment-assets.json',{'assets':[{'id':'ruko-lowrise','description':'1–2storey concrete shop strip, shutters/awnings, no brand'},{'id':'house-tile-roof','description':'single-storey house, pitched terracotta roof'},{'id':'workshop-lowrise','description':'single-storey metal-roof roadside workshop'},{'id':'station-context','description':'cream/grey low-rise tiled-roof station character; sourceOSManchor, shape assumed'},{'id':'local-vegetation','description':'small trees/palms, not surveyed species/positions'},{'id':'utilities','description':'poles/fences within screened plot, no fictitious road access'},{'id':'open-parcels','description':'muted earth patches only, not traffic road/shoulder'}],'status':'ASSUMED CONTEXT MODEL','modeling_tool':'Procedural Three.js, no Blender used','third_party_meshes':False,'context_count':len(placed)});print({'buildings':len(placed),'station':any(r['kind']=='station'for r in placed),'max_height':max(r['height']+r['roof_height']for r in placed)},flush=True)
if __name__=='__main__':main()
