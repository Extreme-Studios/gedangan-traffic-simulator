"""Visual staging only. Frozen network and inherited demand policies."""
from .m155_common import ROOT,load,save,sha,identity,now,Path,json
DOC=ROOT/'documentation/m156';DATA=ROOT/'staging/m156';RUNS=ROOT/'simulation/runs/m156';SCENARIOS=DATA/'scenarios';NETWORK=ROOT/'simulation/network/m155/provisional/network.net.xml';PARENT_RUNS=ROOT/'simulation/runs/m155'
EXPECTED='0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c'
def protect():
 assert sha(NETWORK)==EXPECTED,'Frozen network mismatch'
def verify():
 b=load(DOC/'preservation-before.json');changed=[p for p,h in b.items()if not(ROOT/p).is_file()or sha(ROOT/p)!=h];v={'status':'PASS'if not changed else'FAIL','checked':len(b),'changed':changed,'network_sha256':sha(NETWORK)};save(DOC/'preservation-after.json',v);return v
