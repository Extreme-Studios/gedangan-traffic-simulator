"""Explain stopped vehicles with recorded controls and downstream storage evidence."""
import xml.etree.ElementTree as E
from collections import defaultdict,Counter
from .m15_common import *
from .recovery_routing import context
def explain(folder,target):
 root=E.parse(NETWORK).getroot();net,*_=context(str(NETWORK.resolve()),sha(NETWORK));lanes={l.getID():l for e in net.getEdges(withInternal=True)for l in e.getLanes()};cs=defaultdict(list)
 for c in root.findall('connection'):cs[c.get('from')+'_'+c.get('fromLane')].append(c.attrib)
 rows={q['id']:q for q in load(folder/'vehicle-results.json')};events=load(folder/'signals.json');index=0;states={};counts=Counter();samples=[]
 for _,node in E.iterparse(folder/'fcd.xml',events=('end',)):
  if node.tag!='timestep':continue
  t=float(node.get('time'))+.5
  if t%10:
   node.clear();continue
  while index<len(events)and events[index]['time']<=t:
   event=events[index];states[event['controller']]=event['state'];index+=1
  vehicles=[dict(v.attrib)for v in node.findall('vehicle')if v.get('id')in rows];bylane=defaultdict(list)
  for v in vehicles:bylane[v['lane']].append(v)
  for v in vehicles:
   if float(v['speed'])>=.3:continue
   lane=lanes[v['lane']];pos=float(v['pos']);q=rows[v['id']];reason='QUEUE_BODY_OR_UNRESOLVED';evidence={}
   if lane.getLength()-pos<=15:
    links=[c for c in cs.get(v['lane'],[])if c.get('to')in q['edges']]
    ctrl=[(c.get('tl'),int(c['linkIndex']))for c in links if c.get('tl')]
    values=[states.get(tl,'')[i:i+1]for tl,i in ctrl]
    if values and all(s in ['r','R','y','Y']for s in values):reason='RECORDED_RED_OR_YELLOW_AT_NEXT_CONTROL';evidence={'signal_states':values,'controllers':ctrl}
    else:
     free=[]
     for c in links:
      down=c['to']+'_'+c['toLane'];vs=bylane.get(down,[]);tail=min((float(x['pos'])-float(x.get('length','0'))for x in vs),default=lanes[down].getLength()if down in lanes else 0);free.append({'lane':down,'observed_front_positions_min_m':round(tail,2),'vehicles':len(vs)})
     if free and all(f['vehicles']and f['observed_front_positions_min_m']<5 for f in free):reason='DOWNSTREAM_ENTRY_OCCUPIED_PROXY';evidence={'downstream':free}
     else:reason='HEAD_NEAR_JUNCTION_PRIORITY_OR_SAFETY_UNRESOLVED';evidence={'controller_states':values,'downstream':free}
   counts[reason]+=1
   if len(samples)<600:samples.append({'time_s':t,'vehicle':v['id'],'approach':q['approach'],'lane':v['lane'],'edge':lane.getEdge().getID(),'speed_m_s':float(v['speed']),'distance_to_lane_end_m':round(lane.getLength()-pos,2),'classification':reason,'evidence':evidence})
  node.clear()
 value={'run_id':folder.name,'sample_period_s':10,'classification':'RECORDED_MODEL_CONTROL + INFERRED_STORAGE_PROXY','counts':dict(counts),'examples_first600':samples,'limitations':['Stop classification sampled every10s, not full duration attribution','Red state is observed, causal persistence through upstream queue is not proved','Downstream front-position proxy conservative; exact safe gap and priority may differ','FCD time+0.5 aligns TraCI post-step state; no teleport or fabricated motion used']};save(target,value);return value
if __name__=='__main__':
 for r in load(DOC/'one-hour-results.json'):explain(RUNS/r['run_id'],DOC/'explanations'/(r['run_id']+'.json'))
 explain(ROOT/'simulation/runs/m14/67e1a759e0845754c09be215',DOC/'m14-reconstruction/stop-explanation.json')
