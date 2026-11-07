"""Physical scenario types. Sizes/behavior assumptions are never field calibration."""
import copy,xml.etree.ElementTree as E
from .m14_common import *
from .m04_demand import registry as inherited
def registry():
 labels={'motorcycle':'Sepeda motor','car':'Mobil pribadi','pickup_van':'Pickup / van','bus':'Bus','light_truck':'Truk ringan','heavy_truck':'Truk berat','trailer':'Trailer / gandeng'};old={v['id']:v for v in inherited()};out=[]
 for key,label in labels.items():
  v=copy.deepcopy(old[key]);out.append({**v,'id':key,'label':label,'parameters':v['parameters'],'sumo_vclass':v['sumo_vclass'],'source_type_id':key,'classification':'SCENARIO PHYSICAL ASSUMPTION','provenance':'Unchanged M04 nominal dimensions/dynamics; M04.5 access/clearance screens retained. Not measured or calibrated Gedangan.'})
 for key,label,cls,dim,speed,acc,decel in [('becak_nonmotor','Becak nonmotor','bicycle',[2.6,1.2,1.6],3.5,.45,1.5),('becak_motor','Becak motor','motorcycle',[2.7,1.25,1.7],8.3,.8,2.5),('bicycle','Sepeda / kendaraan lambat','bicycle',[1.8,.65,1.5],5,.7,2)]:
  p={'vClass':cls,'length':dim[0],'width':dim[1],'height':dim[2],'maxSpeed':speed,'accel':acc,'decel':decel,'emergencyDecel':max(4,decel),'minGap':1.2,'tau':1.5,'sigma':.3,'carFollowModel':'Krauss','laneChangeModel':'LC2013','speedFactor':1,'speedDev':0}
  out.append({'id':key,'label':label,'parameters':p,'sumo_vclass':cls,'eligibility':copy.deepcopy(old['motorcycle']['eligibility']),'source_type_id':'motorcycle'if cls=='motorcycle'else None,'classification':'ASSUMPTION — NOT FIELD OBSERVATION','provenance':'Distinct three-wheel/slow technical model; inherited explicit lane permissions not widened. No surveyed dimensions or legal clearance claim.'})
 return out
def types_element():
 from .m04_demand import activate
 root=E.Element('routes',{'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance','xsi:noNamespaceSchemaLocation':str(activate()/'data/xsd/routes_file.xsd')})
 for v in registry():E.SubElement(root,'vType',id=v['id'],**{k:str(x)for k,x in v['parameters'].items()})
 return root
PROFILES={
 'Motorcycle Dominant':[70,20,3,1,2,1,0,0,2,1],
 'Mixed Traffic':[48,30,6,3,5,3,1,0,3,1],
 'Heavy Vehicle Scenario':[28,25,8,5,14,12,6,0,2,0],
 'Local Urban Traffic':[45,28,7,1,3,1,0,5,7,3],
 'Custom Vehicle Mix':[50,25,5,3,5,3,1,2,4,2]}
