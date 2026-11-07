"""Pin the complete existing local SUMO toolchain for workflow/cache reuse."""
from .m04_demand import ROOT,load,save,sha
DOC=ROOT/'documentation/m08';BIN=ROOT/'toolchain/sumo-win64-1.28.0/bin'
def record():
 names=['sumo','netconvert','duarouter']
 for name in names:
  log=load(DOC/(name+'-version.json'))
  if log['returncode'] or '1.28.0' not in log['stdout']:raise ValueError('Required audited toolchain1.28.0 missing')
 value={'version':'1.28.0','scope':'Current executable hashes supplement the initial actual --version logs; not claimed as a pre-implementation binary snapshot','sha256':{str((BIN/(name+'.exe')).relative_to(ROOT)):sha(BIN/(name+'.exe')) for name in names},'cache_contract':'Workflow and interactive entrypoints reject changed binaries before reusing cached physics. Core run signature separately includes sumo.exe.'};save(DOC/'toolchain-sha256.json',value);return value
def verify():
 value=load(DOC/'toolchain-sha256.json');bad=[name for name,h in value['sha256'].items() if sha(ROOT/name)!=h]
 if bad:raise ValueError('Pinned M08 toolchain changed; version/rebuild audit required: '+str(bad))
 return value
if __name__=='__main__':
 import sys
 record() if '--record' in sys.argv else verify()
