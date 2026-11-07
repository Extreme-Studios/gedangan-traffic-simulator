"""Publish actual recorded trajectories for an offline browser viewer."""
import shutil,xml.etree.ElementTree as ET
from .m04_demand import ROOT,save,load
PUBLIC=ROOT/'frontend/public/m05'
def main():
    PUBLIC.mkdir(parents=True,exist_ok=True);root=ET.parse(ROOT/'simulation/network/m05/provisional/network.net.xml').getroot()
    roles={e['id']:e['road_function'] for e in load(ROOT/'simulation/network/m045/provisional/inspection.json')['edges']}
    lanes=[]
    for e in root.findall('edge'):
        for l in e.findall('lane'):
            lanes.append({'id':l.get('id'),'edge':e.get('id'),'to':e.get('to'),'rail':e.get('id').startswith('m05_rail_') or l.get('allow')=='rail','role':roles.get(e.get('id'),'rail' if e.get('id').startswith('m05_rail') else 'internal'),'internal':e.get('function')=='internal','width':float(l.get('width','3.2')),'shape':[[float(v) for v in p.split(',')] for p in l.get('shape').split()]})
    save(PUBLIC/'network.json',{'lanes':lanes,'controlled_links':[dict(c.attrib) for c in root.findall('connection') if c.get('tl')],'junctions':[dict(j.attrib) for j in root.findall('junction')],'attribution':'© OpenStreetMap contributors, retained snapshot 2026-10-31; SUMO 1.28.0 derivative','limitations':'Pilot operates one mapped main centerline; nearby siding not operated. Signals, demand, train timing and behavior are assumptions.'})
    results=load(ROOT/'documentation/m05/scenario-results.json')
    save(PUBLIC/'runs.json',results)
    for r in results:shutil.copy2(ROOT/f"simulation/runs/m05/{r['name']}/playback.json",PUBLIC/f"{r['name']}.json")
    shutil.copy2(ROOT/'documentation/m05/sublane-results.json',PUBLIC/'sublane.json')
if __name__=='__main__':main()
