"""Versioned editable illustrative scenarios; official contextual sources are separate."""
from .m04_demand import ROOT,load,save,registry
from .m07_growth import annual,fingerprint
CONF=ROOT/'configuration/growth-m07'
def validate(scenario):
 if not scenario.get('id') or scenario.get('status')!='SYNTHETIC_ILLUSTRATIVE_ASSUMPTION':raise ValueError('Custom/demo scenario must retain illustrative label')
 if scenario.get('od_policy')!='FINAL_RATE_SUBSTITUTION':raise ValueError('No overlapping class/OD multiplication')
 for rule in scenario['rules']:
  if not rule.get('provenance_id') or not rule.get('source'):raise ValueError('Source required')
  for year in range(2027,2041):annual(rule['schedule'],year)
 return fingerprint(scenario)
def initialize():
 CONF.mkdir(parents=True,exist_ok=True)
 classes=[v['id'] for v in registry()]
 values={'LOW':[-.005,.005,.005,0,0,.01,.01,.01,.005,0],'REFERENCE':[.025,.035,.03,.01,.015,.035,.03,.025,.025,0],'HIGH':[.055,.06,.05,.025,.03,.06,.055,.05,.045,.02]}
 for name,rates in values.items():
  rules=[]
  for cls,rate in zip(classes,rates):
   rules.append({'id':name+'_'+cls,'vehicle_class':cls,'scenario':name,'geographic_scope':'Gedangan model study area','od_relation':'*','source':'Software experiment design, not official estimate','publication_year':2026,'measurement_period':None,'start_year':2027,'end_year':2040,'schedule':{'mode':'constant','rate':rate},'estimation_method':'Explicit editable synthetic annual assumption','confidence':'UNVALIDATED','provenance_id':'M07-ASSUMPTION-01','status':'SYNTHETIC_ILLUSTRATIVE_ASSUMPTION','local_flow_evidence_verified':False})
  for cls,rate in [('motorcycle',{'LOW':0,'REFERENCE':.04,'HIGH':.07}[name])]:
   rules.append({**rules[0],'id':name+'_northbound_'+cls,'vehicle_class':cls,'od_relation':'northbound','schedule':{'mode':'constant','rate':rate},'estimation_method':'Final OD/class rate substitutes the class-wide rate; no multiplier'})
  value={'id':name,'version':'m07-1','status':'SYNTHETIC_ILLUSTRATIVE_ASSUMPTION','label':'ILLUSTRATIVE / UNVALIDATED GROWTH ASSUMPTIONS','od_policy':'FINAL_RATE_SUBSTITUTION','rules':rules,'explanation':'Software scenarios only. REFERENCE is a name, not an official forecast. Oversize demand remains NOT_ROUTABLE.'}
  if not (CONF/(name+'.json')).exists():save(CONF/(name+'.json'),value)
  validate(load(CONF/(name+'.json')))
def read(name):
 if not name.replace('_','').isalnum():raise ValueError('Invalid scenario ID')
 value=load(CONF/(name+'.json'));validate(value);return value
if __name__=='__main__':initialize()
