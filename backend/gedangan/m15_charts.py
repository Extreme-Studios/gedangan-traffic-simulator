"""Publication artifacts from retained actual results, not illustrative traffic data."""
import sys,xml.etree.ElementTree as E
from .m15_common import *
sys.path.insert(0,str(DATA/'plot-dependencies'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def main():
 evidence=DOC/'evidence';evidence.mkdir(exist_ok=True);plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10});results=load(DOC/'one-hour-results.json');r=next(x for x in results if x['requested']==3000);timeline=load(RUNS/r['run_id']/'demand-timeline.json');analysis=r['analysis']['approaches'];old=load(DOC/'m14-reconstruction/reconstructed-result.json');fig,axes=plt.subplots(2,2,figsize=(14,9),layout='constrained');fig.suptitle('M15 — 3,000 requested vehicles / 60 minutes | ACTUAL SUMO / HYPOTHETICAL INPUT',fontsize=14)
 for key,color,label in [('pending_scheduled_not_departed','#bd4b37','Pending insertion'),('active','#237e74','Active road vehicles'),('arrived','#71649a','Cumulative arrived')]:axes[0,0].plot([t['time_s']/60 for t in timeline],[t[key]for t in timeline],label=label,color=color)
 axes[0,0].axvspan(0,r['warmup_s']/60,color='#b5beb7',alpha=.2,label='Warm-up exclusion');axes[0,0].set(xlabel='Model minutes',ylabel='Physical vehicles',title='Lifecycle over the selected horizon');axes[0,0].legend(fontsize=8)
 x=list(range(len(analysis)));axes[0,1].bar(x,[a['entering']for a in analysis],label='Departed',color='#237e74');axes[0,1].bar(x,[a['pending']for a in analysis],bottom=[a['entering']for a in analysis],label='Pending',color='#bd4b37');axes[0,1].set_xticks(x,[a['approach']for a in analysis],rotation=25,ha='right');axes[0,1].set(title='Requested cohort by approach',ylabel='Vehicles');axes[0,1].legend(fontsize=8)
 pending=load(RUNS/r['run_id']/'insertion-samples.json');counts={}
 for s in pending:counts[s['reason']]=counts.get(s['reason'],0)+1
 axes[1,0].bar(['Entry gap proxy short','Other safety / priority unresolved'],[counts.get('OBSERVED_ENTRY_SPACE_SHORTAGE',0),sum(v for k,v in counts.items()if 'UNRESOLVED'in k or 'unresolved'in k)],color=['#b0633a','#7d8799']);axes[1,0].set(title='Insertion evidence, every10s by origin/class',ylabel='Grouped samples (not unique vehicles)');axes[1,0].tick_params(axis='x',labelsize=8)
 edges=r['analysis']['bottleneck_candidates'][:6];axes[1,1].barh([e['edge']for e in edges][::-1],[e['stopped_vehicle_seconds']/3600 for e in edges][::-1],color='#a68438');axes[1,1].set(title='Observed model stopped-time hotspots',xlabel='Stopped vehicle-hours, analysis window');axes[1,1].tick_params(axis='y',labelsize=8)
 for ax in axes.flat:ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
 fig.savefig(evidence/'pending-insertion-diagnostics.png',dpi=160);fig.savefig(evidence/'pending-insertion-diagnostics.pdf');plt.close(fig)
 # Scalar capacity plot retains different demands; no calibrated capacity claim.
 fig,ax=plt.subplots(figsize=(10,5),layout='constrained');x=[z['requested']for z in results]
 for key,label,color in [('departed','Actually departed','#237e74'),('not_departed','Pending at60min','#bd4b37'),('arrived','Arrived','#71649a')]:ax.plot(x,[z[key]for z in results],marker='o',label=label,color=color)
 ax.set(title='M15 — actual one-hour runs, assumed controls / uncalibrated demand',xlabel='Requested vehicles over60min',ylabel='Physical vehicles');ax.legend();ax.grid(alpha=.2);fig.savefig(evidence/'one-hour-demand-accounting.png',dpi=160);plt.close(fig)
 save(DOC/'chart-provenance.json',{'created_utc':now(),'run_id':r['run_id'],'inputs':{str(p.relative_to(ROOT)):sha(p)for p in [DOC/'one-hour-results.json',RUNS/r['run_id']/'demand-timeline.json',RUNS/r['run_id']/'insertion-samples.json']},'note':'Charts aggregate actual model outputs. No observed Gedangan counts or calibrated capacity claims.'})
if __name__=='__main__':main()
