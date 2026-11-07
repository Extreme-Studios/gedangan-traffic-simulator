"""Reconcile loaded telemetry against actual SUMO summary, retaining raw driver samples."""
from functools import lru_cache
from pathlib import Path
import xml.etree.ElementTree as E
from .m04_demand import load,save,sha
@lru_cache(maxsize=64)
def _audit(folder,result_mtime,summary_mtime):
 folder=Path(folder);raw=load(folder/'result.json');last=E.parse(folder/'summary.xml').getroot()[-1];trains=[t for t in E.parse(folder/'tripinfo.xml').getroot().findall('tripinfo') if t.get('vType')=='m05_train'];train_loaded=len(trains);train_departed=sum(float(t.get('depart'))>=0 for t in trains);train_arrived=sum(float(t.get('arrival'))>=0 for t in trains)
 loaded=int(last.get('loaded'))-train_loaded
 if loaded!=raw['routable'] or loaded<raw['departed'] or int(last.get('inserted'))-train_departed!=raw['departed'] or int(last.get('arrived'))-train_arrived!=raw['arrived'] or int(last.get('discarded','0')):raise ValueError('SUMO summary/lifecycle reconciliation failed')
 audit={'raw_loaded_events_sampled_after_initial_step':raw['loaded'],'loaded_road_from_SUMO_summary':loaded,'summary_loaded_including_trains':int(last.get('loaded')),'loaded_train_tripinfo_records':train_loaded,'initial_loaded_events_not_sampled':loaded-raw['loaded'],'basis':'Actual terminal SUMO summary loaded minus actual train tripinfo records; all requests scheduled before1800s/end2100s. Departed/arrived reconciled separately.','limitation':'Initial driver sampled getLoadedIDList after stepping and missed initial load events. Raw result and event sets retained unchanged; derived loaded count comes from SUMO summary.','raw_result_sha256':sha(folder/'result.json'),'summary_sha256':sha(folder/'summary.xml')}
 save(folder/'lifecycle-audit.json',audit)
 return {**raw,'loaded':loaded,'loaded_event_samples_after_initial_step':raw['loaded'],'loaded_reconciliation':audit}
def audited_result(folder):
 folder=Path(folder);return _audit(str(folder),(folder/'result.json').stat().st_mtime_ns,(folder/'summary.xml').stat().st_mtime_ns)
