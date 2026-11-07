"""Georeferenced source overlays and actual experiment plots, not UI screenshots."""
import sys,xml.etree.ElementTree as E
from .m155_common import *
sys.path.insert(0,str(ROOT/'staging/m15/plot-dependencies'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
def main():
 d=load(DOC/'technical-map.json');offset=list(map(float,E.parse(NETWORK).getroot().find('location').get('netOffset').split(',')));out=DOC/'figures';out.mkdir(exist_ok=True)
 for view,b in [('extent',d['bounds']),('junction',[-300,-300,300,200]),('station',[-160,-200,270,200])]:
  fig,ax=plt.subplots(figsize=(12,9));ax.set_facecolor('#f4f5ef')
  def draw(rows,color,width,style='solid'):
   for row in rows:
    p=row['points'];ax.plot([v[0]-offset[0]for v in p],[v[1]-offset[1]for v in p],color=color,lw=width,ls=style)
  draw(d['source'],'#b6b6aa',3);draw(d['government'],'#7188c0',1.8,'dashed');draw(d['road_inventory'],'#24796f',.7);draw(d['rail'],'#25252b',1.5)
  for s in d['signals']:ax.plot(s['point'][0]-offset[0],s['point'][1]-offset[1],'o',ms=3,color='#b64b39')
  for p in d['reference_points']:ax.plot(p['point'][0]-offset[0],p['point'][1]-offset[1],'x',color='#8450ac',ms=8)
  ax.plot(d['station']['point'][0]-offset[0],d['station']['point'][1]-offset[1],'s',ms=6,color='#354c84');ax.plot(d['crossing'][0]-offset[0],d['crossing'][1]-offset[1],'o',ms=12,fillstyle='none',color='#803c78')
  ax.set_xlim(b[0]-offset[0],b[2]-offset[0]);ax.set_ylim(b[1]-offset[1],b[3]-offset[1]);ax.set_aspect('equal');ax.ticklabel_format(style='plain',useOffset=False);ax.grid(alpha=.15);ax.set_xlabel('Easting m · EPSG:32749');ax.set_ylabel('Northing m · EPSG:32749');ax.set_title('M15.5 Gedangan '+view+' — source comparison, not field survey')
  handles=[Line2D([0],[0],color=c,lw=2,label=l,ls=sty)for c,l,sty in [('#b6b6aa','Retained OSM source','solid'),('#24796f','SUMO road centre / provisional rules','solid'),('#7188c0','Public Pemkab map / currency unknown','dashed'),('#25252b','Inherited rail / one model direction','solid')]];ax.legend(handles=handles,loc='lower left',fontsize=8);fig.text(.05,.015,'PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED | OSM contributors ODbL1.0 / Pemkab Sidoarjo public Peta Jalan',fontsize=8);fig.tight_layout(rect=[0,.035,1,1]);fig.savefig(out/f'georeferenced-{view}.png',dpi=160);fig.savefig(out/f'georeferenced-{view}.svg');plt.close(fig)
 rows=load(DOC/'controlled-comparisons.json')['comparisons'];fig,axs=plt.subplots(1,2,figsize=(13,5));labels=['Baseline 60min','Discharge 120min','Green30 60min','No trains 60min'];start=[0]*4
 for key,label,color in [('arrived','Arrived','#3b8c73'),('active','Active','#d2ab3c'),('not_departed','Pending','#bb625d')]:
  vals=[r['end'][key]for r in rows];axs[0].bar(labels,vals,bottom=start,label=label,color=color);start=[a+b for a,b in zip(start,vals)]
 axs[0].set_ylabel('Same 3000 road vehicle requests');axs[0].tick_params(axis='x',rotation=17);axs[0].legend();base=load(DOC/'rootcause'/f"{rows[0]['run_id']}.json")
 axs[1].barh(['Entry-space shortage observed','Other insertion check unresolved'],[q['vehicles']for q in base['evidence_coverage']],color=['#bb625d','#7788aa']);axs[1].set_xlabel('Unique pending IDs at 3600s, denominator 1086');axs[1].set_title('Observed conditions, not causal percentages')
 for i,q in enumerate(base['evidence_coverage']):axs[1].text(q['vehicles']+5,i,f"{q['vehicles']} / {q['percent_of_unique_pending']:.2f}%",va='center',fontsize=9)
 axs[1].set_xlim(0,1100);fig.suptitle('MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION');fig.tight_layout();fig.savefig(out/'actual-comparisons.png',dpi=160);fig.savefig(out/'actual-comparisons.svg');plt.close(fig)
 save(DOC/'figure-register.json',{'status':'DERIVED_STATIC_FIGURES_NOT_BROWSER_SCREENSHOTS','crs':'EPSG:32749','network_sha256':sha(NETWORK),'net_offset_xy':offset,'sources':['Retained OSM geodata/raw/gedangan-network.json','S-GOV-GEO','Actual M15.5 FCD/tripinfo results'],'figures':{p.name:sha(p)for p in out.iterdir()}})
 print('Static overlays and actual comparison plots saved.',flush=True)
if __name__=='__main__':main()
