from pathlib import Path
from datetime import datetime
import subprocess,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2];run=ROOT/'simulation/runs/m051/E_combined_seed42';out=ROOT/'simulation/runs/m051'/('gui-review-'+datetime.now().strftime('%Y%m%d-%H%M%S'));out.mkdir(parents=True,exist_ok=False)
add=ET.parse(run/'controls.add.xml').getroot()
for detector in add.findall('laneAreaDetector'):detector.set('file',str(out/'e2.xml'))
ET.ElementTree(add).write(out/'controls.add.xml',encoding='utf-8',xml_declaration=True)
args=[str(ROOT/'toolchain/sumo-win64-1.28.0/bin/sumo-gui.exe'),'-c',str(run/'run.sumocfg'),'--seed','42','--additional-files',str(out/'controls.add.xml'),'--gui-settings-file',str(ROOT/'documentation/m05/gui-view.xml'),'--tripinfo-output',str(out/'tripinfo.xml'),'--fcd-output',str(out/'fcd.xml'),'--summary-output',str(out/'summary.xml'),'--start','--delay','50','--breakpoints','105,130']
subprocess.Popen(args,cwd=ROOT);print('Output GUI terpisah:',out)
