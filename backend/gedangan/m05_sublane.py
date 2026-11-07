"""Isolated lateral-clearance comparison; not Gedangan field behavior."""
import xml.etree.ElementTree as ET
from .m04_demand import ROOT,activate,xml,save,execute,registry,load
DIR=ROOT/'simulation/runs/m05/sublane-fixture'
def main():
    home=activate();DIR.mkdir(parents=True,exist_ok=True)
    nodes=ET.Element('nodes');ET.SubElement(nodes,'node',id='a',x='0',y='0');ET.SubElement(nodes,'node',id='b',x='600',y='0')
    edges=ET.Element('edges');ET.SubElement(edges,'edge',id='road',**{'from':'a','to':'b'},speed='12',width='3.2',numLanes='1',allow='motorcycle passenger truck')
    xml(DIR/'nodes.xml',nodes);xml(DIR/'edges.xml',edges)
    r=execute([home/'bin/netconvert.exe','-n',DIR/'nodes.xml','-e',DIR/'edges.xml','-o',DIR/'network.net.xml'],DIR/'build-log.json');assert r['returncode']==0
    profile=load(ROOT/'configuration/behavior-m05/profiles.json')['sublane_fixture'];output=[]
    for model in ['LC2013','SL2015']:
        routes=ET.Element('routes')
        for v in registry():
            if v['id'] not in ['motorcycle','car','heavy_truck']:continue
            p={k:str(x) for k,x in v['parameters'].items()};p['laneChangeModel']=model
            if model=='SL2015':p.update(**{k:str(profile[k]) for k in ['minGapLat','maxSpeedLat','lcPushy']},latAlignment='arbitrary')
            ET.SubElement(routes,'vType',id=v['id'],**p)
        probes=[('motor_a','motorcycle',5,-.8),('motor_b','motorcycle',5,.8),('car_a','car',150,-.55),('motor_car','motorcycle',150,1.05),('truck','heavy_truck',300,0),('motor_truck','motorcycle',300,'random_free')]
        for vid,typ,pos,lat in probes:
            a={'id':vid,'type':typ,'depart':'0','departPos':str(pos),'departSpeed':'0'}
            if model=='SL2015':a['departPosLat']=str(lat)
            v=ET.SubElement(routes,'vehicle',**a);ET.SubElement(v,'route',edges='road')
        xml(DIR/f'{model}.rou.xml',routes)
        cmd=[home/'bin/sumo.exe','-n',DIR/'network.net.xml','-r',DIR/f'{model}.rou.xml','--step-length','0.2','--end','150','--seed','42','--fcd-output',DIR/f'{model}.fcd.xml','--fcd-output.acceleration','true','--fcd-output.max-leader-distance','100','--tripinfo-output',DIR/f'{model}.tripinfo.xml','--no-step-log','true']
        if model=='SL2015':cmd+=['--lateral-resolution',str(profile['lateral_resolution'])]
        log=execute(cmd,DIR/f'{model}-log.json');assert log['returncode']==0,log['stderr']
        frames=[];seen=set();pairs=[];accels=[];positions={};widths={'motor_a':.8,'motor_b':.8,'car_a':1.8,'motor_car':.8,'truck':2.5,'motor_truck':.8};lengths={'motor_a':2.1,'motor_b':2.1,'car_a':4.5,'motor_car':2.1,'truck':11.5,'motor_truck':2.1}
        for step in ET.parse(DIR/f'{model}.fcd.xml').getroot():
            vs={v.get('id'):v.attrib for v in step.findall('vehicle')};seen.update(vs)
            for vid,v in vs.items():
                positions.setdefault(vid,[]).append(float(v.get('y')));accels.append(float(v.get('acceleration','0')))
            for a,b in [('motor_a','motor_b'),('car_a','motor_car'),('truck','motor_truck')]:
                if a in vs and b in vs:
                    va,vb=vs[a],vs[b];pa,pb=float(va['pos']),float(vb['pos'])
                    overlap=min(pa,pb)-max(pa-lengths[a],pb-lengths[b])
                    if overlap>0:pairs.append({'time':float(step.get('time')),'pair':[a,b],'longitudinal_overlap_m':round(overlap,3),'lateral_body_gap_m':round(abs(float(va['y'])-float(vb['y']))-(widths[a]+widths[b])/2,3)})
        trips=ET.parse(DIR/f'{model}.tripinfo.xml').getroot().findall('tripinfo')
        result={'model':model,'category':'ISOLATED_SYNTHETIC_TEST','lane_width_m':3.2,'lateral_resolution':.4 if model=='SL2015' else None,'lcPushy':0,'requested':6,'departed':len(seen),'arrived':len(trips),'runtime_wall_seconds':log['wall_seconds'],'peak_working_set_bytes_sampled':log['peak_working_set_bytes_sampled'],'overlap_observations':pairs,'lateral_span_m':{k:round(max(v)-min(v),3) for k,v in positions.items()},'min_acceleration_m_s2':min(accels),'max_acceleration_m_s2':max(accels),'notes':'All physical dynamics inherited from M04; only lane-changing model/lateral parameters differ. No position override after insertion. Heavy-plus-motor has insufficient 0.25 m lateral clearance on 3.2 m lane.'}
        save(DIR/f'{model}-result.json',result);output.append(result)
    save(ROOT/'documentation/m05/sublane-results.json',output)
if __name__=='__main__':main()
