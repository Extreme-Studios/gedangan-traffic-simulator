"""Validate all recorded 0.5 s vehicle samples against derived lane access."""
import xml.etree.ElementTree as ET
from .m04_demand import ROOT,load,save,sha
from .m05_railway import CROSSING
def main():
    results=load(ROOT/'documentation/m05/scenario-results.json');types={v['id']:v['sumo_vclass'] for v in load(ROOT/'configuration/demand-m04/vehicle-registry.json')['vehicles']};types['m05_train']='rail';audits=[]
    for r in results:
        folder=ROOT/'simulation/runs/m05'/r['name'];net=ET.parse(ROOT/r.get('network_path',f"simulation/network/m05/{r['mode']}/network.net.xml")).getroot();lanes={l.get('id'):l for e in net.findall('edge') for l in e.findall('lane')};events=[e for e in load(folder/'events.json') if e['controller']==CROSSING];index=0;state='';samples=0;illegal=[];red=[]
        for event,step in ET.iterparse(folder/'fcd.xml',events=['end']):
            if step.tag!='timestep':continue
            t=float(step.get('time'))+.5
            while index<len(events) and events[index]['time']<=t:state=events[index]['state'];index+=1
            for v in step.findall('vehicle'):
                samples+=1;lane=v.get('lane');l=lanes[lane];cls=types[v.get('type')];allow=l.get('allow');deny=l.get('disallow','').split()
                if (allow is not None and cls not in allow.split()) or cls in deny or 'all' in deny:illegal.append({'time':t,'vehicle':v.get('id'),'class':cls,'lane':lane})
                if cls!='rail' and lane.startswith(':'+CROSSING+'_') and state and set(state)<=set('rR'):red.append({'time':t,'vehicle':v.get('id'),'lane':lane})
            step.clear()
        audit={'run':r['name'],'record_resolution_s':.5,'samples_checked':samples,'illegal_lane_samples':illegal,'road_internal_crossing_samples_during_closed_red':red,'collisions':r['collisions'],'teleports':r['teleports'],'network_sha256':r['network_sha256'],'scope':'Recorded lane/access and closed-road occupancy validation; zero sampled conflict is not mathematical collision proof between steps or swept-path legal certification.'};save(folder/'safety-audit.json',audit);audits.append(audit)
    save(ROOT/'documentation/m05/safety-audits.json',audits)
if __name__=='__main__':main()
