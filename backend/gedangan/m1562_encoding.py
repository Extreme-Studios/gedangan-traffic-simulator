from .m1562_common import ROOT
import ftfy
def main():
 for p in (ROOT/'frontend/src/m1562').glob('*.ts*'):
  s=ftfy.fix_text(p.read_text(encoding='utf-8-sig'))
  if p.name=='main.tsx':s=s.replace("from'./LocationMap'","from'./SourceMap'")
  p.write_text(s,encoding='utf-8')
 for p in (ROOT/'backend/gedangan').glob('m1562_*.py'):
  s=p.read_text(encoding='utf-8').replace('.read_text(encoding='utf-8')',".read_text(encoding='utf-8')")
  p.write_text(s,encoding='utf-8')
if __name__=='__main__':main()
