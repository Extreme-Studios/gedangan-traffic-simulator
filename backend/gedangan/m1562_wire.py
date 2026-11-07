"""One-time isolated frontend/transport wiring, rerun from bootstrap only."""
from .m1562_common import ROOT
def main():
 p=ROOT/'frontend/src/m1562/main.tsx';s=p.read_text(encoding='utf-8');s="import{loadRecording}from'./RecordingLoader';"+s;s=s.replace('const videoState=useRef<D>({});','const loadController=useRef<AbortController>();const videoState=useRef<D>({});')
 start=s.index(' async function openRun(');end=s.index(' function onStats(',start)
 s=s[:start]+''' async function openRun(id:string){loadController.current?.abort();const controller=new AbortController();loadController.current=controller;SPlay(false);SD(undefined);SSelected(null);SStats({});SN('Memuat rekaman Float64 lossless…');const started=performance.now();try{const r=await loadRecording(id,controller.signal);if(controller.signal.aborted)return;if(r.metrics.hour_checkpoint){r.metrics.throughput_arrivals_per_hour=r.metrics.hour_checkpoint.arrived*3600/r.metrics.request.duration_s;r.metrics.throughput_arrivals_per_execution_hour=r.metrics.arrived*3600/r.duration_s}SD(r);ST(Math.min(180,r.duration_s/3));SN('Rekaman aktual siap. '+r.frames.length+' frame / '+r.positions+' posisi; Float64 lossless '+(r.typed_bytes/1048576).toFixed(1)+' MiB; '+((performance.now()-started)/1000).toFixed(2)+' detik pemuatan.');await api('performance',{kind:'playback_load',build:'m1562-source-packed-1',run_id:id,wall_ms:performance.now()-started,frames:r.frames.length,positions:r.positions,typed_bytes:r.typed_bytes,window:[innerWidth,innerHeight]})}catch(e){if(!controller.signal.aborted)throw e}}
'''+s[end:]
 start=s.index(' async function video(');end=s.index(' if(!req||!c)',start)
 s=s[:start]+''' async function video(){SRecording(true);let stream:MediaStream|undefined;try{stream=await navigator.mediaDevices.getDisplayMedia({video:{width:{ideal:1920},height:{ideal:1080},frameRate:{ideal:30}},audio:false,preferCurrentTab:true}as any);SPlay(true);const media=new MediaRecorder(stream,{mimeType:'video/webm'}),chunks:BlobPart[]=[];await new Promise<void>((resolve,reject)=>{media.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};media.onerror=()=>reject(Error('Screen recorder failed'));media.onstop=()=>resolve();media.start(1000);setTimeout(()=>{if(media.state!=='inactive')media.stop()},50000);stream!.getVideoTracks()[0].onended=()=>{if(media.state!=='inactive')media.stop()}});const blob=new Blob(chunks,{type:'video/webm'}),r=await fetch('/api/video',{method:'POST',body:blob});if(!r.ok)throw Error('Video save failed');SN('Rekaman layar penuh aktual tersimpan; metadata durasi/resolusi perlu diverifikasi.')}finally{stream?.getTracks().forEach(t=>t.stop());SRecording(false)}}
'''+s[end:]
 s=s.replace('Rekam Video 50s','Rekam Layar Penuh 50s').replace('Konteks bangunan asumsi','Bangunan sumber OSM').replace('m1562-local-context-1','m1562-source-packed-1');p.write_text(s,encoding='utf-8')
 p=ROOT/'frontend/src/m1562/world.tsx';s=p.read_text(encoding='utf-8');s=s.replace('const capacities:D={};for(const f of props.recording.frames)','const capacities:D={...props.recording.max_active_by_type};if(!props.recording.max_active_by_type)for(const f of props.recording.frames)');p.write_text(s,encoding='utf-8')
 p=ROOT/'backend/gedangan/m1562_server.py';s=p.read_text(encoding='utf-8');marker="    if path=='/api/catalog':"
 insert='''    if len(parts)==4 and parts[:2]==['api','packed']:
     key,name=parts[2],parts[3]
     if len(key)!=24 or not all(c in '0123456789abcdef'for c in key):return self.send({'error':'Invalid ID'},400)
     if name!='index.json'and not(name.endswith('.f64.gz')and '/'not in name and '..'not in name):return self.send({'error':'Invalid chunk'},400)
     from .m1562_recording import build
     base=DATA/'recordings'/key
     if not(base/'index.json').exists():build(key)
     p=(base/name).resolve()
     if not p.is_relative_to(base.resolve())or not p.is_file():return self.send({'error':'Not found'},404)
     return self.send(p.read_bytes(),kind='application/octet-stream'if name.endswith('.gz')else'application/json',encoding='gzip'if name.endswith('.gz')else None)
'''
 assert marker in s;s=s.replace(marker,insert+marker);p.write_text(s,encoding='utf-8')
 p=ROOT/'backend/gedangan/m1562_context.py';s=p.read_text(encoding='utf-8').replace('math.atan2(-(b[1]-a[1]),b[0]-a[0])','math.atan2(b[1]-a[1],b[0]-a[0])');p.write_text(s,encoding='utf-8')
if __name__=='__main__':main()
