"""Multi-year calendar and separately labelled aggregate archive. Legacy services unchanged."""
from .m13_server import handler as base_handler,ThreadingHTTPServer
from . import m13_server as legacy
from .m13_common import *
from .m131_database import initialize
from urllib.parse import urlparse
def handler(store,port):
 base=base_handler(store,port)
 class Handler(base):
  def do_GET(self):
   if not self.allowed():return self.send({'error':'Host/Origin denied'},403)
   path=urlparse(self.path).path
   if path=='/api/health':return self.send({'service':'Gedangan M13.1 public evidence archive','dataset_version':store.version(),'test_database':store.test_fixture,'old_M13_database_unchanged':True})
   if path=='/api/archive':return self.send(store.archive_months())
   if path=='/api/references':return self.send({'quality_class':'B_PENDING_AND_C','historical_calendar_eligible':False,'records':store.reference_rows(),'note':'B partial observations remain quarantined from the hourly calendar; C aggregates are references only. Original intervals/units retained; no prorating or synthetic splitting.'})
   if path=='/api/source-audit':return self.send({'download_manifest':load(ROOT/'M13_1_DOWNLOADED_FILES_MANIFEST.json'),'integration':load(ROOT/'documentation/m13_1/integration-summary.json')})
   return super().do_GET()
 return Handler
def main():
 legacy.UI=ROOT/'frontend/m13_1';store=initialize();server=ThreadingHTTPServer(('127.0.0.1',5198),handler(store,5198));print('M13.1 http://127.0.0.1:5198/ - Multi-year observed calendar and separate C-aggregate archive',flush=True);server.serve_forever()
if __name__=='__main__':main()
