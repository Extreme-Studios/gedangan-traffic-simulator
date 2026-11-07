"""Actual isolated SUMO positive control for storage-induced upstream blockage."""
import xml.etree.ElementTree as ET
from .m04_demand import ROOT,activate,xml,save,execute
from .m05_queues import spillback_candidate
DIR=ROOT/'simulation/runs/m05/spillback-fixture'
def main():
    home=activate();import traci
    DIR.mkdir(parents=True,exist_ok=True);ns=ET.Element('nodes');es=ET.Element('edges')
    for nid,x in [('a',0),('b',200),('c',260),('d',500)]:ET.SubElement(ns,'node',id=nid,x=str(x),y='0',type='traffic_light' if nid in ['b','c'] else 'priority')
    for eid,a,b in [('upstream','a','b'),('storage','b','c'),('exit','c','d')]:ET.SubElement(es,'edge',id=eid,**{'from':a,'to':b},numLanes='1',speed='10',allow='passenger')
    xml(DIR/'nodes.xml',ns);xml(DIR/'edges.xml',es)
    log=execute([home/'bin/netconvert.exe','-n',DIR/'nodes.xml','-e',DIR/'edges.xml','--no-turnarounds','true','-o',DIR/'network.net.xml'],DIR/'build-log.json');assert log['returncode']==0
    root=ET.parse(DIR/'network.net.xml').getroot()
    for tl in root.findall('tlLogic'):
        for child in list(tl):tl.remove(child)
        if tl.get('id')=='b':ET.SubElement(tl,'phase',duration='1000',state='G')
        else:
            for duration,state in [(120,'r'),(300,'G'),(3,'y'),(2,'r')]:ET.SubElement(tl,'phase',duration=str(duration),state=state)
    xml(DIR/'network.net.xml',root);routes=ET.Element('routes');ET.SubElement(routes,'vType',id='car',vClass='passenger',length='4.5',minGap='2.5',tau='1.2',sigma='0')
    for i in range(25):
        v=ET.SubElement(routes,'vehicle',id=f'car{i}',type='car',depart=str(i*2));ET.SubElement(v,'route',edges='upstream storage exit')
    xml(DIR/'demand.rou.xml',routes);traci.start([str(home/'bin/sumo.exe'),'-n',str(DIR/'network.net.xml'),'-r',str(DIR/'demand.rou.xml'),'--step-length','0.5','--no-step-log','true','--tripinfo-output',str(DIR/'tripinfo.xml'),'--fcd-output',str(DIR/'fcd.xml')],label='spillback_fixture');c=traci.getConnection('spillback_fixture');observations=[];active=0;first=None;collisions=[];teleports=[]
    for i in range(700):
        c.simulationStep();t=c.simulation.getTime();collisions.extend(c.simulation.getCollidingVehiclesIDList());teleports.extend(c.simulation.getStartingTeleportIDList())
        stopped=[v for v in c.lane.getLastStepVehicleIDs('storage_0') if c.vehicle.getSpeed(v)<.3];tail=min([c.vehicle.getLanePosition(v) for v in stopped],default=1e9);up=[v for v in c.lane.getLastStepVehicleIDs('upstream_0') if c.vehicle.getSpeed(v)<.3 and c.lane.getLength('upstream_0')-c.vehicle.getLanePosition(v)<10];green=c.trafficlight.getRedYellowGreenState('b')=='G'
        candidate=bool(stopped and tail<5 and up and green);active=active+.5 if candidate else 0
        detected=spillback_candidate({'tail_position':tail} if stopped else None,bool(up),green,active)
        if detected and first is None:first=t
        if candidate:observations.append({'time':t,'downstream_queue_count':len(stopped),'tail_m':tail,'downstream_occupancy_percent':c.lane.getLastStepOccupancy('storage_0'),'upstream_stopped':up,'upstream_green':green,'continuous_blocked_s':active,'detected':detected})
    c.close();arrived=len(ET.parse(DIR/'tripinfo.xml').getroot().findall('tripinfo'))
    save(DIR/'result.json',{'category':'ISOLATED_SYNTHETIC_POSITIVE_CONTROL_NOT_GEDANGAN','requested':25,'arrived':arrived,'first_detection_s':first,'observations':observations,'teleports':teleports,'collisions':collisions,'definition':'Downstream stopped queue tail within 5 m of start, upstream head stopped within 10 m of end, upstream controlled movement green, continuous blockage >=5 s. No vehicle repositioning or access override.'})
    assert first is not None and arrived==25 and not collisions and not teleports
if __name__=='__main__':main()
