"""Native SUMO-GUI evidence session with isolated outputs."""
from pathlib import Path
import subprocess,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2];folder=ROOT/'documentation/m05/gui-session';folder.mkdir(parents=True,exist_ok=True)
add=ET.parse(ROOT/'simulation/runs/m05/G_e2_instrumented/controls.add.xml').getroot()
for d in add.findall('laneAreaDetector'):d.set('file',str(folder/'e2.xml'))
ET.ElementTree(add).write(folder/'controls.add.xml',encoding='utf-8',xml_declaration=True)
args=[str(ROOT/'toolchain/sumo-win64-1.28.0/bin/sumo-gui.exe'),'-c',str(ROOT/'simulation/runs/m05/G_e2_instrumented/run.sumocfg'),'--seed','42','--additional-files',str(folder/'controls.add.xml'),'--gui-settings-file',str(ROOT/'documentation/m05/gui-view.xml'),'--fcd-output',str(folder/'fcd.xml'),'--tripinfo-output',str(folder/'tripinfo.xml'),'--summary-output',str(folder/'summary.xml')]
if '--qa-release' in sys.argv:args+=['--start','--delay','0','--breakpoints','130']
else:args+=['--start','--delay','100','--breakpoints','105,130']
p=subprocess.Popen(args,cwd=ROOT);print('SUMO-GUI PID',p.pid)
