"""Read-only parent UI with all new benchmark telemetry isolated in M15.6.2."""
from . import m1562_server as server
from .m1562_common import ROOT,save,load
server.UI=ROOT/'frontend/dist-m1561'
server.DOC=ROOT/'documentation/m1562/baseline'
server.DOC.mkdir(parents=True,exist_ok=True)
save(server.DOC/'scene.json',load(ROOT/'documentation/m1561/scene.json'))
parent=server.handler
def handler(port):
 cls=parent(port)
 original=cls.do_GET
 def get(self):
  if self.path=='/':self.path='/m1561.html'
  return original(self)
 cls.do_GET=get
 return cls
server.handler=handler
if __name__=='__main__':server.main()
