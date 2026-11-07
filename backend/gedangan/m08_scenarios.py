"""Explicit operational experiments versus gated infrastructure concepts."""
import jsonschema,copy
from .m04_demand import ROOT,load,save
from .m07_growth import fingerprint
CONF=ROOT/'configuration/scenarios-m08';DOC=ROOT/'documentation/m08'
LABEL='SYNTHETIC / CONDITIONAL TRAFFIC EXPERIMENT — NOT AN EMPIRICALLY VALIDATED GEDANGAN FORECAST'
STATUSES=['DRAFT','CONCEPT_ONLY','STRUCTURALLY_BLOCKED','SIMULATION_READY_PROVISIONAL','SIMULATED','NEEDS_FIELD_VERIFICATION']
SCHEMA={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'required':['id','version','name','kind','status','operation','parameters','provenance','assumptions','blockers'],'properties':{'id':{'enum':['S00','S01','S02','S03','S04','S05','S06','S07']},'version':{'type':'string','minLength':1},'name':{'type':'string'},'kind':{'enum':['OPERATIONAL','INFRASTRUCTURE_CONCEPT']},'status':{'enum':STATUSES},'operation':{'enum':['baseline','signal','movement_restriction','frontage_restriction','heavy_deferral','coordination','flyover','underpass']},'parameters':{'type':'object'},'provenance':{'type':'string','minLength':1},'assumptions':{'type':'array','items':{'type':'string'}},'blockers':{'type':'array','items':{'type':'string'}}}}
def validate(s):
 jsonschema.Draft202012Validator(SCHEMA).validate(s)
 if s['kind']=='INFRASTRUCTURE_CONCEPT' and s['status'] in ['SIMULATION_READY_PROVISIONAL','SIMULATED']:raise ValueError('Infrastructure gate requires surveyed topology/design evidence; current catalog cannot activate it')
 if s['operation']=='signal' and (set(s['parameters'])!={'green','yellow','all_red','offset'} or not 5<=s['parameters']['green']<=30 or s['parameters']['yellow']<3 or s['parameters']['all_red']<2):raise ValueError('Unsafe/out-of-envelope signal timing')
 return fingerprint(s)
def initialize():
 CONF.mkdir(parents=True,exist_ok=True);save(CONF/'scenario.schema.json',SCHEMA)
 specs=[('S00','Baseline / no intervention','baseline',{}),('S01','Synthetic signal timing alternatives','signal',{'green':8,'yellow':3,'all_red':2,'offset':0}),('S02','Existing feeder left-turn closure','movement_restriction',{'from':'w266287930_s0_p1_0_f','to':'w266287935_s0_p0_0_f'}),('S03','Existing frontage exit closure','frontage_restriction',{'from':'w1188011989_s0_p0_0_f','to':'w266287937_s0_p0_0_f'}),('S04','Heavy vehicles deferred from first15min','heavy_deferral',{'classes':['light_truck','medium_truck','heavy_truck','trailer'],'restricted_window_s':[0,900],'deferral_s':900}),('S05','Corridor coordination','coordination',{}),('S06','Flyover concept','flyover',{}),('S07','Underpass concept','underpass',{})]
 for sid,name,op,params in specs:
  concept=sid in ['S06','S07'];blocked=sid=='S05';s={'id':sid,'version':'m08-1','name':name,'kind':'INFRASTRUCTURE_CONCEPT' if concept else 'OPERATIONAL','status':'CONCEPT_ONLY' if concept else 'STRUCTURALLY_BLOCKED' if blocked else 'SIMULATION_READY_PROVISIONAL','operation':op,'parameters':params,'provenance':'M08-ENGINEERING-ASSUMPTION-01','assumptions':['Software intervention proposal, not an approved legal traffic order or measured design','M06 empirical baseline blocked; M07 growth illustrative'],'blockers':['Surveyed topology/elevation/ROW/clearance/utilities/geotechnical/drainage/authority approvals missing'] if concept else ['Only one road signal controller; railway crossing cannot be treated as a second arbitrary road controller'] if blocked else []}
  validate(s)
  if not (CONF/(sid+'.json')).exists():save(CONF/(sid+'.json'),s)
def read(sid):
 if sid not in [f'S{i:02d}' for i in range(8)]:raise ValueError('Invalid scenario ID')
 s=load(CONF/(sid+'.json'));validate(s);return s
def signal_candidate(green):
 s=copy.deepcopy(read('S01'));s['version']='m08-signal-green'+str(green);s['parameters']['green']=green;validate(s);return s
if __name__=='__main__':initialize()
