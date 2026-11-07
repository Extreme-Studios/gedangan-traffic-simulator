"""Conservative one-protected-link-at-a-time synthetic signal plans."""
import xml.etree.ElementTree as ET
from .m04_demand import ROOT,load
HEADS=['osm_2718664256','osm_3201485055','osm_4513024622','osm_2718664280']
def node_patch():
    ns=ET.Element('nodes')
    for nid in HEADS:ET.SubElement(ns,'node',id=nid,type='traffic_light',tl='m05_gedangan')
    return ns
def programs(root):
    config=load(ROOT/'configuration/signals-m05/program.json');audits=[]
    for tl in root.findall('tlLogic'):
        if tl.get('id')!='m05_gedangan':continue
        tl.set('offset',str(config['offset']))
        count=max(int(c.get('linkIndex')) for c in root.findall('connection') if c.get('tl')==tl.get('id'))+1
        for phase in list(tl):tl.remove(phase)
        for i in range(count):
            for duration,state in [(config['green'],''.join('G' if j==i else 'r' for j in range(count))),(config['yellow'],''.join('y' if j==i else 'r' for j in range(count))),(config['all_red'],'r'*count)]:ET.SubElement(tl,'phase',duration=str(duration),state=state)
        audits.append({'controller':tl.get('id'),'logical_source_stop_heads':HEADS,'links':count,'status':'ASSUMPTION','green':config['green'],'yellow':config['yellow'],'all_red':config['all_red'],'offset':config['offset'],'safety':'At most one protected green controlled connection; no guessed opposing green pairs','limitation':'Conservative technical plan; not observed field timing or full junction controller reconstruction'})
    return audits
