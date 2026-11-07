"""Source-positioned polygons; never relocate a footprint to clear frozen traffic."""
from .m1562_common import *
import xml.etree.ElementTree as ET,math
from pyproj import Transformer
from shapely.geometry import Polygon,Point,LineString,mapping
from shapely.ops import unary_union

def main():
 protect();scene=load(ROOT/'documentation/m1561/scene.json')
 root=ET.parse(DOC/'sources/gedangan.osm').getroot()
 transform=Transformer.from_crs('EPSG:4326','EPSG:32749',always_xy=True)
 def xy(lon,lat):
  x,y=transform.transform(lon,lat);return [x-690790.39,y-9182879.52]
 nodes={n.get('id'):xy(float(n.get('lon')),float(n.get('lat')))for n in root.findall('node')}
 junction=Point(-80,-78);station=Point(-19,-3);frontage=Point(scene['presets']['FRONTAGE'])
 corridor=LineString([(-70,-400),(-63,400),(50,1350)])
 roi=unary_union([junction.buffer(230),station.buffer(210),frontage.buffer(220),corridor.buffer(100)])
 road=unary_union([LineString(l['shape']).buffer(l['width']/2+.25)for l in scene['lanes']if not l['rail']])
 rail=unary_union([LineString(l['shape']).buffer(1.8)for l in scene['lanes']if l['rail']])
 selected=[];conflicts=[];landuse=[];all_count=0;invalid=0
 for w in root.findall('way'):
  tags={t.get('k'):t.get('v')for t in w.findall('tag')}
  if not('building'in tags or 'landuse'in tags or tags.get('natural')in['water','wood','scrub']):continue
  refs=[n.get('ref')for n in w.findall('nd')]
  if not all(n in nodes for n in refs)or len(refs)<4 or refs[0]!=refs[-1]:continue
  points=[nodes[n]for n in refs];poly=Polygon(points)
  if not poly.is_valid or poly.area<5:invalid+=1;continue
  if 'building'in tags:all_count+=1
  if not poly.intersects(roi):continue
  if 'building'not in tags:
   landuse.append({'id':'osm-way-'+w.get('id'),'tags':tags,'polygon':points,'confidence':'SOURCE-MAPPED LANDUSE; surface appearance assumed'})
   continue
  # Full source polygon stays unchanged. Conflicts are withheld, not shifted/scaled.
  if poly.intersection(road).area>.25 or poly.intersects(rail):
   conflicts.append({'id':w.get('id'),'road_overlap_m2':poly.intersection(road).area,'rail_intersection':poly.intersects(rail),'action':'WITHHELD_RENDER; footprint retained in source; no network edit'})
   continue
  rect=list(poly.minimum_rotated_rectangle.exterior.coords)[:4]
  edges=[math.dist(rect[i],rect[(i+1)%4])for i in range(4)]
  ix=edges.index(max(edges));a,b=rect[ix],rect[(ix+1)%4];length=edges[ix];depth=edges[(ix+1)%4]
  center=poly.centroid
  # Station facade is on the west side in source photo. For other polygons the closest road-facing edge informs detail only.
  is_station=tags.get('building')=='train_station'
  detail=poly.distance(junction)<105 or is_station or poly.distance(frontage)<90 or poly.distance(station)<90
  height=4.0 if is_station else 3.4 if poly.area<200 else 5.8 if poly.area<700 else 7.2
  selected.append({'id':'osm-way-'+w.get('id'),'source_id':w.get('id'),'source_version':w.get('version'),'source_timestamp':w.get('timestamp'),'tags':tags,'polygon':points,'x':center.x,'y':center.y,'area_m2':poly.area,'rectangle':rect,'width':length,'depth':depth,'rotation':math.atan2(b[1]-a[1],b[0]-a[0]),'height':height,'roof_height':1.65 if is_station else min(1.6,depth*.16),'kind':'station'if is_station else'industrial'if tags['building']=='industrial'or poly.area>700 else'house','detailed':detail,'footprint_confidence':'SOURCE-MAPPED FOOTPRINT','appearance_confidence':'PHOTO-REFERENCED APPEARANCE (2020 station only)'if is_station else'ASSUMED VISUAL CONTEXT','height_confidence':'ASSUMED 3D HEIGHT','roof_confidence':'ASSUMED VISUAL CONTEXT','position_note':'Exact source polygon transformed through frozen UTM49S/netOffset; not surveyed verification'})
 scene['buildings']=[] # discard inherited guessed massing; source arrays above are the only environmental buildings.
 scene['environment']={'version':'m1562-source-polygons-1','buildings':selected,'landuse':landuse,'status':'SOURCE-MAPPED FOOTPRINT / ASSUMED 3D HEIGHT / ASSUMED VISUAL CONTEXT','station_photo':'documentation/m1561/sources/station-2020.jpg','source':'OpenStreetMap contributors, ODbL 1.0; https://www.openstreetmap.org/copyright','road_or_rail_added':0,'roi_note':'Three priority locations and connecting corridor; no fictional infill'}
 save(DOC/'scene.json',scene)
 save(DOC/'footprint-audit.json',{'source_sha256':sha(DOC/'sources/gedangan.osm'),'source_total_building_ways':all_count,'selected_rendered':len(selected),'detailed':sum(b['detailed']for b in selected),'landuse':len(landuse),'height_tags':0,'withheld_network_conflicts':conflicts,'invalid_or_incomplete_polygons':invalid,'station':next((b for b in selected if b['kind']=='station'),None),'network_sha256':sha(NETWORK),'shifted_buildings':0,'invented_footprints':0})
 features=[{'type':'Feature','geometry':mapping(Polygon(b['polygon'])),'properties':{k:b[k]for k in ['id','source_version','source_timestamp','height','footprint_confidence','appearance_confidence','height_confidence','detailed']}}for b in selected]
 save(DOC/'footprints-local.geojson',{'type':'FeatureCollection','coordinate_system':'SUMO local metres UTM49S plus frozen netOffset; not lon/lat','features':features})
 print({'source':all_count,'rendered':len(selected),'landuse':len(landuse),'conflicts':len(conflicts),'station':any(b['kind']=='station'for b in selected)})
if __name__=='__main__':main()
