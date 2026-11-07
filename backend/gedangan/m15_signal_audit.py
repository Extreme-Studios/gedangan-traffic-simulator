"""Quantify inherited assumed signal service without declaring field capacity."""
import xml.etree.ElementTree as E
from collections import defaultdict
from .m15_common import *
from .m15_network import catalog
def audit():
 root=E.parse(NETWORK).getroot();tls=next(t for t in root.findall('tlLogic')if t.get('id')=='m05_gedangan');phases=[{'duration':float(p.get('duration')),'state':p.get('state')}for p in tls.findall('phase')];cycle=sum(p['duration']for p in phases);links=[]
 for q in root.findall('connection'):
  if q.get('tl')!='m05_gedangan':continue
  i=int(q.get('linkIndex'));green=sum(p['duration']for p in phases if p['state'][i]in'gG');yellow=sum(p['duration']for p in phases if p['state'][i]in'yY');links.append({**q.attrib,'green_s_per_cycle':green,'yellow_s_per_cycle':yellow,'red_s_per_cycle':cycle-green-yellow,'green_fraction':green/cycle,'status':'ASSUMED_CONTROLLER_NOT_ACTUAL_GEDANGAN_TIMING'})
 result={'classification':'ASSUMED SIGNAL CONFIGURATION','cycle_s':cycle,'phase_count':len(phases),'controlled_connections':links,'finding':'Inherited nine-link isolated protected green sequence allocates only12 green seconds per link per153-second cycle. This conservative uncalibrated control can constrain model throughput; no field capacity inference. Priority nodes after the split stop-lines are not given invented lights.','source_network_sha256':sha(NETWORK),'phase_states_preserved':True};save(DOC/'signal-service-audit.json',result);return result
if __name__=='__main__':print(audit()['finding'])
