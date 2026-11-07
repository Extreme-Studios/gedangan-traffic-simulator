"""Rail/road connector entry and closed-barrier checks from actual trace/state events."""
import xml.etree.ElementTree as E,math
from collections import defaultdict
from .m155_common import *
def audit(r):
 from shapely.geometry import LineString,Point
 root=E.parse(NETWORK).getroot();edges={e.get('id'):e for e in root.findall('edge')};lanes={l.get('id'):l for e in edges.values()for l in e.findall('lane')};via={c.get('via'):int(c.get('linkIndex'))for c in root.findall('connection')if c.get('tl')=='osm_859708050'and not c.get('from','').startswith(('m05_rail',':'))};folder=RUNS/r['run_id'];events=load(folder/'signals.json');i=0;state={};previous_signal={};previous_lane={};redentries=[];ambiguous=[];rail_offtrack=[];traincross=defaultdict(list);closedstopped=0;road_ids={q['id']for q in load(folder/'vehicle-results.json')}
 for _,n in E.iterparse(folder/'fcd.xml',events=('end',)):
  if n.tag!='timestep':continue
  t=float(n.get('time'))+.5
  while i<len(events)and events[i]['time']<=t:state[events[i]['controller']]=events[i]['state'];i+=1
  sig=state.get('osm_859708050','');curr={}
  for v in n.findall('vehicle'):
   vid=v.get('id');lane=v.get('lane');curr[vid]=lane
   if vid not in road_ids:
    shape=[list(map(float,p.split(',')[:2]))for p in lanes[lane].get('shape').split()];distance=LineString(shape).distance(Point(float(v.get('x')),float(v.get('y'))))
    if distance>.03:rail_offtrack.append({'time':t,'id':vid,'lane':lane,'distance_m':distance})
    if lane.startswith(':osm_859708050'):traincross[vid].append(t)
   else:
    if lane in via and previous_lane.get(vid)!=lane:
     link=via[lane];s=sig[link:link+1];old=previous_signal.get('osm_859708050','')[link:link+1]
     if s in ['r','R']:
      (redentries if old in ['r','R']else ambiguous).append({'time':t,'id':vid,'lane':lane,'state':s,'previous_state':old})
    if sig and float(v.get('speed'))<.3 and lane.startswith('w1240685448'):closedstopped+=int('r'in sig[:2].lower())
  previous_lane=curr;previous_signal=dict(state);n.clear()
 value={'run_id':r['run_id'],'road_crossing_via_links':via,'train_lane_geometry_offset_above_0_03m':rail_offtrack,'steady_red_first_entry_samples':redentries,'phase_boundary_ambiguous_entry_samples':ambiguous,'closed_crossing_stopped_road_samples':closedstopped,'train_front_crossing_sample_intervals':{k:{'first_s':min(v),'last_s':max(v)}for k,v in traincross.items()},'status':'NO_RECORDED_OFF_TRACK_OR_STEADY_RED_ENTRY'if not rail_offtrack and not redentries else'REQUIRES_REVIEW','limitations':['0.5s sampled front entry, not continuous swept-volume clearance','Building footprints not in retained source; no surveyed building collision certification','Only inherited one-direction rail graph; no reverse direction manufactured','Crossing controller states are actual model output, schedule remains ASSUMED']};save(DOC/'rail-audits'/(r['run_id']+'.json'),value);return value
if __name__=='__main__':
 r=load(DOC/'cases/baseline-3000.json');print(audit(r)['status'],flush=True)
