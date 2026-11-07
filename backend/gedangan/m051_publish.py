"""Deterministic audit/event publication, without modifying M05."""
from collections import Counter
from .m04_demand import ROOT,load,save,sha
from .m051_causality import analyze_trace
import shutil,sys,xml.etree.ElementTree as ET
DOC=ROOT/'documentation/m051';RUNS=ROOT/'simulation/runs/m051';PUBLIC=ROOT/'frontend/public/m051'
def main(reanalyze=True):
 PUBLIC.mkdir(parents=True,exist_ok=True);all_events=[];summaries=[]
 for p in sorted(RUNS.glob('*/priority-trace.json')):
  events=analyze_trace(p.parent) if reanalyze else load(p.parent/'causal-events.json');summary=load(p.parent/'classification-summary.json');summary['fixture']='positive_' in p.parent.name or 'negative_' in p.parent.name
  if (p.parent/'run-manifest.json').exists():summary['manifest']=load(p.parent/'run-manifest.json')
  summaries.append(summary)
  for e in events:
   e['run']=p.parent.name;e['evidence_rows']=len(e['evidence']);e['evidence_source']=str((p.parent/'causal-events.json').relative_to(ROOT));e['supporting_first']=e['evidence'][0];e['supporting_last']=e['evidence'][-1];e['timeline']=[{'time':r['time'],'speed':r['speed'],'entry_free_m':r.get('entry_free_m'),'queue_count':r.get('queue_count'),'occupancy':r.get('occupancy_percent'),'link_state':r['next_link'][5] if r.get('next_link') else None,'opened':r['next_link'][3] if r.get('next_link') else None,'foe':r['next_link'][4] if r.get('next_link') else None,'gate':r.get('gate_state')} for r in e['evidence']];e.pop('evidence');all_events.append(e)
 save(DOC/'event-index.json',all_events);save(DOC/'experiment-summary.json',summaries)
 # Every inherited candidate is linked to its new vehicle-specific priority/storage trace, not only examples that pass.
 audit=[]
 for summary in summaries:
  if summary['fixture']:continue
  name=summary['run'];positional_frames=None;old=load(ROOT/f'simulation/runs/m05/{name}/spillback-events.json');trace=load(RUNS/name/'priority-trace.json');bytime={f['time']:f['observations'] for f in trace};joined={(r['id'],r['time']):r for event in load(RUNS/name/'causal-events.json') for r in event['evidence']}
  for i,e in enumerate(old):
   rows=[joined.get((r['id'],r['time']),r) for r in bytime.get(e['time'],[]) if r['id']==e['vehicle']]
   nr=ET.parse(ROOT/'simulation/network/m051/provisional/network.net.xml').getroot();controllers={(c.get('from')+'_'+c.get('fromLane'),c.get('to')+'_'+c.get('toLane')):c.get('tl') for c in nr.findall('connection') if not c.get('from','').startswith(':')}
   for r in rows:r['movement_controller']=controllers.get((r['lane'],r.get('downstream_lane')))
   from .m051_causality import classify
   category=classify(rows[0]) if rows else 'UNRESOLVED_NO_MATCHING_TRACE';following=None
   if not rows:
    if positional_frames is None:positional_frames={f['time']:f for f in load(ROOT/f'simulation/runs/m05/{name}/playback.json')['frames']}
    frame=positional_frames.get(e['time']);vehicle=next((v for v in frame['vehicles'] if v['id']==e['vehicle']),None) if frame else None
    ahead=[v for v in frame['vehicles'] if vehicle and v['lane']==vehicle['lane'] and v['pos']>vehicle['pos']] if frame else []
    if ahead:category='FOLLOWING_QUEUE_POSITIONAL_EVIDENCE';following={'time':e['time'],'vehicle':vehicle,'vehicles_ahead':ahead,'source':f'simulation/runs/m05/{name}/playback.json','limitation':'Follower position is observed; head-specific priority is not assigned to this follower.'}
   audit.append({'candidate_id':f'{name}_M05_{i}','run':name,'original':e,'matched_trace':rows,'classification_at_original_detection':category,'positional_following_evidence':following,'related_events':[v['event_id'] for v in all_events if v['run']==name and v['vehicle']==e['vehicle'] and v['start']<=e['time']<=v['end']]})
 save(DOC/'m05-candidate-audit.json',audit)
 coverage=[];replayed={s['run'] for s in summaries if not s['fixture']}
 for source in sorted((ROOT/'simulation/runs/m05').glob('*/spillback-events.json')):
  original=load(source);coverage.append({'run':source.parent.name,'candidate_count':len(original),'new_priority_replay_or_validated_alias':source.parent.name in replayed})
 save(DOC/'complete-m05-candidate-coverage.json',{'all_original_runs':len(coverage),'original_candidate_total':sum(r['candidate_count'] for r in coverage),'candidates_in_replayed_runs':sum(r['candidate_count'] for r in coverage if r['new_priority_replay_or_validated_alias']),'direct_priority_matched':sum(bool(r['matched_trace']) for r in audit),'positional_followers_without_head_trace':sum(r['positional_following_evidence'] is not None for r in audit),'runs':coverage})
 for name in ['geometry.json','geometry-overlay.json','event-index.json','experiment-summary.json','m05-candidate-audit.json']:shutil.copy2(DOC/name,PUBLIC/name)
 save(PUBLIC/'status.json',{'milestone':'M05.1','status':'PARTIAL — NEEDS FIELD DATA','geometry':'NEEDS FIELD SURVEY: modeled stop lines are not measured stop lines','gedangan_verified_events':sum(e['cause']=='VERIFIED_SPILLBACK' and not any(k in e['run'] for k in ['positive','negative']) for e in all_events),'candidate_status':'Only events meeting all recorded causal conditions are verified; lack of proof remains unresolved, not absence of spillback.','synthetic_label':'SYNTHETIC TEST — NOT OBSERVED GEDANGAN TRAFFIC'})
 print('runs',len(summaries),'events',Counter(e['cause'] for e in all_events),'old candidates',len(audit))
if __name__=='__main__':main('--reuse' not in sys.argv)
