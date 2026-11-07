"""Compact causal-event index for recorded playback, no fabricated positions."""
from .m04_demand import load,save,sha
def spillback_index(folder):
 path=folder/'causal-events.json';cache=folder/'m08-spillback-index.json';digest=load(folder/'m08-output-manifest.json')['causal-events.json']
 if cache.exists():
  value=load(cache)
  if value['causal_events_sha256']==digest:return value['events']
 if sha(path)!=digest:raise ValueError('Causal event recording hash mismatch')
 events=[{k:e[k] for k in ['id','vehicle','upstream_lane','downstream_lane','start','end','cause','right_censored','affected_edges']} for e in load(path) if e['cause']=='VERIFIED_SPILLBACK'];save(cache,{'causal_events_sha256':digest,'events':events,'scope':'Verified in model only. Marker positions must come from the actual matching recorded vehicle frame; no fallback/interpolation.'});return events
