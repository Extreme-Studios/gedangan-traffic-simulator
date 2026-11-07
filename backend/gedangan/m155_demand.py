"""Preserve M15 cohort IDs, class/route/time exactly for controlled comparisons."""
from .m15_demand import default as parent_default,generate as parent_generate,integer,volume,weights,allocate
def default():
 r=parent_default();r.update(name='M15.5 existing network reality check',execution_horizon_s=3600);return r
def generate(request):
 d=parent_generate(request);h=integer(request.get('execution_horizon_s',request['duration_s']),'execution horizon',request['duration_s'],14400);d['execution_horizon_s']=h;d['demand_duration_s']=request['duration_s'];d['network_status']='PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED';return d
