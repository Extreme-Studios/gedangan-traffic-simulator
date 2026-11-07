from .m1562_common import ROOT
def main():
 p=ROOT/'frontend/src/m1562/main.tsx';s=p.read_text(encoding='utf-8');s=s.replace("const media=new MediaRecorder(stream,{mimeType:'video/webm'}),chunks:BlobPart[]=[];", "const media=new MediaRecorder(stream,{mimeType:'video/webm',videoBitsPerSecond:12000000}),chunks:BlobPart[]=[];const tour=['rail','junctionClose','station','frontageClose','overview'],timers=tour.map((name,i)=>setTimeout(()=>{SCam(name);SReset(v=>v+1)},i*10000));")
 s=s.replace("media.onstop=()=>resolve();","media.onstop=()=>{timers.forEach(clearTimeout);resolve()};")
 s=s.replace("await navigator.mediaDevices.getDisplayMedia({video:","await navigator.mediaDevices.getDisplayMedia({video:")
 p.write_text(s,encoding='utf-8')
if __name__=='__main__':main()
