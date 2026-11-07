"""Source-node rail pilot. Operational parameters are synthetic assumptions."""
import xml.etree.ElementTree as ET
from pyproj import Transformer
from .m04_demand import ROOT,load,save,xml,sha
PILOT=[1330582009,562358494,1330582010]
CROSSING='osm_859708050'
def source_pilot(folder, inspection):
    features=load(ROOT/'geodata/railways/rail_tracks.geojson')['features']
    selected=[next(f for f in features if f['properties']['osm_id']==i) for i in PILOT]
    raw=load(ROOT/'geodata/raw/gedangan-network.json')['elements']; nodes={n['id']:n for n in raw if n['type']=='node'}
    ids=[]
    for f in selected:
        seq=f['properties']['osm_node_ids']; assert not ids or ids[-1]==seq[0]
        ids.extend(seq if not ids else seq[1:])
    assert 859708050 in ids
    tr=Transformer.from_crs(4326,32749,always_xy=True); ox,oy=inspection['origin_utm_m']
    ns=ET.Element('nodes'); es=ET.Element('edges'); cs=ET.Element('connections'); route=[]
    for i in ids:
        n=nodes[i];x,y=tr.transform(n['lon'],n['lat'])
        ET.SubElement(ns,'node',id=f'osm_{i}',x=str(x-ox),y=str(y-oy),type='rail_crossing' if i==859708050 else 'priority')
    for i,(a,b) in enumerate(zip(ids,ids[1:])):
        eid=f'm05_rail_{i}';route.append(eid)
        ET.SubElement(es,'edge',id=eid,**{'from':f'osm_{a}','to':f'osm_{b}'},allow='rail',speed='8',numLanes='1',width='3.2',spreadType='center')
        if i:ET.SubElement(cs,'connection',**{'from':route[-2],'to':eid,'fromLane':'0','toLane':'0','allow':'rail'})
    xml(folder/'rail.nod.xml',ns);xml(folder/'rail.edg.xml',es);xml(folder/'rail.con.xml',cs)
    save(folder/'rail-provenance.json',{'source_features':selected,'source_node_chain':ids,'route':route,'source_status':'VERIFIED against retained OSM, not field survey','operation_status':'ASSUMPTION: one direction, one mapped centerline, not full station track plan','excluded_siding':1268453702,'crossing':CROSSING,'gate_count':'MISSING; shared nodes are not physical gate counts','source_sha256':sha(ROOT/'geodata/railways/rail_tracks.geojson')})
    return ns,es,cs,route

def build_block_control(home):
    from .m04_demand import execute
    from .m045_access import external_connections
    folder=ROOT/'simulation/network/m05/provisional-block-control';folder.mkdir(parents=True,exist_ok=True)
    base=ROOT/'simulation/network/m05/provisional/network.net.xml';ns=ET.Element('nodes')
    for nid in ['osm_11781097631','osm_11781097634']:ET.SubElement(ns,'node',id=nid,type='rail_signal')
    xml(folder/'block.nod.xml',ns)
    result=execute([home/'bin/netconvert.exe','--sumo-net-file',base,'--node-files',folder/'block.nod.xml','--offset.disable-normalization','true','--no-turnarounds','true','--geometry.remove','false','-o',folder/'network.net.xml'],folder/'build-log.json');assert result['returncode']==0,result['stderr']
    root=ET.parse(folder/'network.net.xml').getroot();xml(folder/'network.net.xml',root)
    before=ET.parse(base).getroot();road=lambda r:{k for k in external_connections(r) if not k[0].startswith('m05_rail_')}
    assert road(before)==road(root)
    old={e.get('id'):e for e in before.findall('edge') if e.get('function')!='internal' and not e.get('id').startswith('m05_rail_')}
    assert all(ET.tostring(e)==ET.tostring(old[e.get('id')]) for e in root.findall('edge') if e.get('id') in old)
    save(folder/'manifest.json',{'baseline_sha256':sha(base),'network_sha256':sha(folder/'network.net.xml'),'category':'ASSUMPTION','synthetic_rail_block_signals':['osm_11781097631','osm_11781097634'],'purpose':'Built-in safe rail block separation for short-schedule-gap test; these are synthetic operating controls, not mapped actual signal equipment','new_road_connections':0,'external_road_edges_unchanged':True})
    return folder/'network.net.xml'

def audit_source():
    raw=load(ROOT/'geodata/raw/gedangan-network.json')['elements'];ways=[w for w in raw if w['type']=='way'];tracks=load(ROOT/'geodata/railways/rail_tracks.geojson')['features'];cross=[]
    for n in raw:
        if n['type']!='node' or n.get('tags',{}).get('railway')!='level_crossing':continue
        rails=[f['properties'] for f in tracks if n['id'] in f['properties']['osm_node_ids']];roads=[{'id':w['id'],'tags':w.get('tags',{})} for w in ways if n['id'] in w['nodes'] and 'highway' in w.get('tags',{})]
        cross.append({'source_node':n,'mapped_rail_parts':[{'id':r['osm_id'],'tags':r['tags']} for r in rails],'shared_road_ways':roads,'status':'VERIFIED_SOURCE_SHARED_NODE' if rails and roads else 'OUTSIDE_RETAINED_RAIL_SCOPE_OR_MISSING_SHARED_TOPOLOGY','physical_gate_count':'MISSING','grade_separation':'At-grade inferred only at source-shared level_crossing; nearby bridge tags are not proximity joins.'})
    save(ROOT/'documentation/m05/railway-source-audit.json',{'raw_context_level_crossing_nodes':len(cross),'mapped_core_crossing_nodes':sum(bool(x['mapped_rail_parts']) for x in cross),'scope_note':'24 raw context crossing nodes; 11 intersect retained M02 rail parts. Neither count is physical gate count.','crossings':cross,'pilot_group':[859708050,11781097618],'group_basis':'Same Ketajen source road across mapped main and siding centerlines about seven metres apart; candidate physical-site group, actual track/gate count missing.','all_rail_parts':[f['properties'] for f in tracks],'pilot_main_chain':PILOT,'bridge_segment':562358494,'bridge_policy':'No road/rail join at bridge. Only source shared node 859708050 activated.'})
