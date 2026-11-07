"""Cross-process single SUMO worker lease on Windows; no stale file locks."""
from contextlib import contextmanager
import msvcrt
from .m04_demand import ROOT

@contextmanager
def worker():
 path=ROOT/'documentation/m08/worker.lock';path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('a+b') as stream:
  if stream.tell()==0:stream.write(b'0');stream.flush()
  stream.seek(0)
  try:msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1)
  except OSError:raise RuntimeError('Another M08 SUMO worker is active')
  try:yield
  finally:stream.seek(0);msvcrt.locking(stream.fileno(),msvcrt.LK_UNLCK,1)
