"""Isolated location-context layer; traffic network and parent outputs remain immutable."""
from .m156_common import ROOT,load,save,sha,identity,now,Path,json,NETWORK,EXPECTED
DOC=ROOT/'documentation/m1561';DATA=ROOT/'staging/m1561';RUNS=ROOT/'simulation/runs/m1561';SCENARIOS=DATA/'scenarios';PARENT_RUNS=ROOT/'simulation/runs/m155'
def protect():assert sha(NETWORK)==EXPECTED,'Frozen network mismatch'
def verify():
 b=load(DOC/'preservation-before.json');changed=[p for p,h in b.items()if not(ROOT/p).is_file()or sha(ROOT/p)!=h];v={'checked':len(b),'changed':changed,'status':'PASS'if not changed else'FAIL','network_sha256':sha(NETWORK)};save(DOC/'preservation-after.json',v);return v
