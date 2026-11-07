"""Future empirical bundle contract. Does not create or approve observations."""
from .m04_demand import ROOT,load,sha
from .m07_projection import baseline
def validate_bundle(bundle):
 required=['cells','movements','demand_window','measurement_window','day_period','provenance','review_document','reviewed','independently_validated','m06_observation_sha256']
 if any(k not in bundle for k in required):raise ValueError('Incomplete calibrated baseline bundle')
 if not bundle['reviewed'] or not bundle['independently_validated']:raise ValueError('Empirical review/independent validation required')
 if bundle['demand_window']!=[0,1800] or bundle['measurement_window']!=[0,2100]:raise ValueError('This M07 runner requires two15min windows/fixed2100s; create an explicit version for other windows')
 keys=set()
 for c in bundle['cells']:
  if type(c['count'])!=int or c['count']<0 or c['key'] in keys or c['interval_start'] not in [0,900] or c['interval_end']!=c['interval_start']+900 or c['od_id'] not in bundle['movements']:raise ValueError('Invalid empirical cells/mapping')
  keys.add(c['key'])
 if not keys:raise ValueError('Empty empirical demand')
 return bundle
def resolve(kind='PROVISIONAL_SYNTHETIC_BASELINE',bundle=None):
 if kind=='PROVISIONAL_SYNTHETIC_BASELINE':return baseline()
 if kind!='EMPIRICALLY_CALIBRATED_BASELINE':raise ValueError('Unknown baseline type')
 gate=load(ROOT/'documentation/m06/empirical-gate.json');config=load(ROOT/'configuration/calibration-m06/baseline-2026.json')
 if not gate['enabled'] or not config['empirical_baseline']['enabled']:raise ValueError('M06 empirical gate BLOCKED — DATA REQUIRED')
 validate_bundle(bundle)
 source=ROOT/'data/observations/m06/normalized/observations.json';observations=load(source)
 if not observations or bundle['m06_observation_sha256']!=sha(source) or any(r['source_class']!='OBSERVED_FIELD' or r['quality']!='VERIFIED' for r in observations):raise ValueError('Verified observation lineage mismatch')
 review=(ROOT/bundle['review_document']).resolve()
 if not review.is_relative_to(ROOT) or not review.is_file():raise ValueError('Local review evidence required')
 return {**bundle,'kind':kind,'year':2026,'status':'EMPIRICALLY_CALIBRATED_INPUT_REVIEWED_EXTERNALLY','source':bundle['provenance'],'review_document_sha256':sha(review),'m06_gate_sha256':sha(ROOT/'documentation/m06/empirical-gate.json')}
