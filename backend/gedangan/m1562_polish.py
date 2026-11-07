from .m1562_common import ROOT
def main():
 p=ROOT/'frontend/src/m1562/core.ts';s=p.read_text(encoding='utf-8').replace('position:[x-42,22,z+28]','position:[x-23,16,z+16]');p.write_text(s,encoding='utf-8')
 p=ROOT/'frontend/src/m1562/MappedContext.ts';s=p.read_text(encoding='utf-8')
 needle="if(station){box(w,.14,1.55,'roof',0,3,d/2+.64,matrix);"
 replace="""if(station){
     // Photo-referenced grey horizontal bands, louvers, eave brackets and stone-tone plinth.
     box(w,.22,.12,'base',0,2.95,d/2+.10,matrix);box(w,.18,.12,'base',0,1.08,d/2+.10,matrix);box(w,.7,.14,'base',0,.36,d/2+.10,matrix);
     for(let i=0;i<8;i++){const x=-w/2+unit*(i+.5);for(let y=1.3;y<2.5;y+=.13)box(Math.min(unit*.6,1.2),.035,.11,'wood',x,y,d/2+.08,matrix);box(.17,3.2,.14,'base',x-unit*.45,1.65,d/2+.10,matrix)}
     box(w,.14,1.55,'roof',0,3,d/2+.64,matrix);"""
 assert needle in s;s=s.replace(needle,replace);p.write_text(s,encoding='utf-8')
 # Terminate background loading on unmount; user-initiated switches already abort the old worker.
 p=ROOT/'frontend/src/m1562/main.tsx';s=p.read_text(encoding='utf-8');needle=" useEffect(()=>{if(!playing||!rec)return;";s=s.replace(needle," useEffect(()=>()=>loadController.current?.abort(),[]);\n"+needle);p.write_text(s,encoding='utf-8')
if __name__=='__main__':main()
