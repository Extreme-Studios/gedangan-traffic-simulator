"""Copy retained actual-network renderer into M14; original M10 remains untouched."""
from .m14_common import ROOT
def main():
 src=ROOT/'frontend/src/m10';dst=ROOT/'frontend/src/m14';dst.mkdir(parents=True,exist_ok=True)
 (dst/'core.ts').write_text((src/'core.ts').read_text(encoding='utf-8'),encoding='utf-8')
 w=(src/'world.tsx').read_text(encoding='utf-8')
 lines=w.splitlines();lines=[line for line in lines if 'const concept=new T.Mesh'not in line];w='\n'.join(lines).replace('concept.visible=current.concept;','')
 w=w.replace("const capacity=props.recording.vehicles.filter((k:D)=>k.type===v.type).length;","const capacity=Math.max(1,...props.recording.frames.map(f=>f.p.reduce((n,p)=>n+(props.recording.vehicles[p[0]].type===v.type?1:0),0)));")
 w=w.replace("if(type==='motorcycle'){", "if(type==='becak_nonmotor'||type==='becak_motor'){wheels([-.65],w*.8,.28);wheels([.85],0,.28);box(w*.9,.4,l*.48,body,0,.65,-.4);box(w*.8,.12,l*.4,rubber,0,.95,-.4);box(w,.08,l*.5,body,0,1.65,-.4);for(const x of [-w*.43,w*.43])box(.04,.7,.04,silver,x,1.3,-.8);part(new T.SphereGeometry(.16,8,6),body,0,1.35,.5);box(.35,.4,.3,rubber,0,1,.4);return p}if(type==='bicycle'){wheels([-.65,.65],0,.3);box(.06,.5,1,silver,0,.55,0);box(.32,.1,.4,rubber,0,.9,-.1);part(new T.SphereGeometry(.17,8,6),body,0,1.4,0);return p}if(type==='motorcycle'){")
 w=w.replace("{props.recording.scenario==='S00'?'BASELINE':'INTERVENTION '+props.recording.scenario}","{'EXISTING NETWORK · ACTUAL SUMO'}").replace('ARRIVED · 35 MIN','ARRIVED · {props.recording.duration_s/60} MIN')
 w=w.replace("scope:'Browser-measured render loop; no physical VRAM capacity inferred'", "visibility:document.visibilityState,has_focus:document.hasFocus(),sample_window_frames:durations.length,scope:'Browser-measured render loop including throttling; no physical VRAM capacity inferred'")
 # Context is disabled for M14. Skip unneeded fictional massing placement work.
 w=w.replace('for(const [x,y]of contextPoints){','for(const [x,y]of (props.context?contextPoints:[])){')
 w=w.replace('durations.length>1200','durations.length>120')
 # A stale animation callback may run after props update, before effect cleanup.
 # Never read new recording indices with the preceding recording's mesh buckets.
 w=w.replace('const current=latest.current,dt=', 'const current=latest.current;if(current.recording.id!==props.recording.id)return;const dt=')
 (dst/'world.tsx').write_text(w+'\n',encoding='utf-8')
if __name__=='__main__':main()
