"""Synthetic toolchain-only smoke test. Not geography or traffic for Gedangan."""
import json
from pathlib import Path
import subprocess
from .sumo_env_m02 import activate, ROOT

def main():
    home=activate()
    output=ROOT/'toolchain/smoke/synthetic-not-gedangan';output.mkdir(parents=True,exist_ok=True)
    result={'purpose':'Synthetic software test only; NOT Gedangan data or model','sumo_home':str(home),'versions':{}}
    for name in ['sumo','sumo-gui','netedit','netconvert']:
        run=subprocess.run([str(home/'bin'/f'{name}.exe'),'--version'],capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
        result['versions'][name]={'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr}
        if run.returncode:raise RuntimeError(f'{name} --version failed: {run.stderr}')
    (output/'nodes.nod.xml').write_text('<nodes><node id="synthetic_a" x="0" y="0"/><node id="synthetic_b" x="250" y="0"/><node id="synthetic_c" x="500" y="0"/></nodes>')
    (output/'edges.edg.xml').write_text('<edges><edge id="synthetic_ab" from="synthetic_a" to="synthetic_b" numLanes="1" speed="10"/><edge id="synthetic_bc" from="synthetic_b" to="synthetic_c" numLanes="1" speed="10"/></edges>')
    net=output/'synthetic.net.xml'
    conversion=subprocess.run([str(home/'bin/netconvert.exe'),'-n',str(output/'nodes.nod.xml'),'-e',str(output/'edges.edg.xml'),'-o',str(net),'--no-turnarounds','true'],capture_output=True,text=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
    result['netconvert']={'returncode':conversion.returncode,'stdout':conversion.stdout,'stderr':conversion.stderr}
    if conversion.returncode:raise RuntimeError(conversion.stderr)
    routes=output/'synthetic.rou.xml'
    routes.write_text('<routes><route id="synthetic_route" edges="synthetic_ab synthetic_bc"/><vehicle id="software_test_vehicle" route="synthetic_route" depart="0"/></routes>')
    import traci
    import sumolib
    result['imports']={'traci':traci.__file__,'sumolib':sumolib.__file__,'sumolib_edge_count':len(sumolib.net.readNet(str(net)).getEdges())}
    conn=None
    try:
        traci.start([str(home/'bin/sumo.exe'),'-n',str(net),'-r',str(routes),'--seed','42','--step-length','1','--no-step-log','true','--duration-log.disable','true'],label='m02-synthetic-test',stdout=subprocess.DEVNULL)
        conn=traci.getConnection('m02-synthetic-test')
        result['traci_handshake']=conn.getVersion()
        for _ in range(12):conn.simulationStep()
        result['synthetic_test']={'time_s':conn.simulation.getTime(),'vehicle_ids':list(conn.vehicle.getIDList()),'steps':12}
        assert result['imports']['sumolib_edge_count']==2
        assert result['synthetic_test']['time_s']==12
        assert result['synthetic_test']['vehicle_ids']==['software_test_vehicle']
        result['status']='PASS'
    finally:
        if conn is not None:conn.close()
    (ROOT/'documentation/m02/sumo-smoke.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
