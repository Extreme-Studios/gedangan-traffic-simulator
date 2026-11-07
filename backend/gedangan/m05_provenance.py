"""Independent deterministic rebuild and paired repeat comparison."""
import xml.etree.ElementTree as ET,hashlib
from .m04_demand import ROOT,activate,sha,save
from .m05_behavior import build
from .m05_railway import build_block_control
def main():
    paths=[ROOT/f'simulation/network/m05/{v}/network.net.xml' for v in ['strict','provisional','provisional-block-control']];before={str(p.relative_to(ROOT)):sha(p) for p in paths}
    home=activate();build(home);build_block_control(home);after={str(p.relative_to(ROOT)):sha(p) for p in paths}
    a=ROOT/'simulation/runs/m05/C_single_seed42';b=ROOT/'simulation/runs/m05/I_repro_single_seed42';checks={}
    for name in ['tripinfo.xml','fcd.xml','summary.xml']:checks[name]=hashlib.sha256(ET.tostring(ET.parse(a/name).getroot())).hexdigest()==hashlib.sha256(ET.tostring(ET.parse(b/name).getroot())).hexdigest()
    result={'network_before':before,'network_after':after,'all_network_hashes_identical':before==after,'run_pair':['C_single_seed42','I_repro_single_seed42'],'identical_demand':sha(a/'demand.json')==sha(b/'demand.json'),'xml_element_results_identical':checks,'note':'XML comments/process headers omitted, all simulation elements and attributes retained; runtime is not deterministic.'}
    save(ROOT/'documentation/m05/reproducibility.json',result);assert before==after and all(checks.values()) and result['identical_demand']
if __name__=='__main__':main()
