"""Project-scoped SUMO environment, explicitly enabled by callers."""
import json
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]

def activate():
    config=json.loads((ROOT/'configuration/sumo-m02.json').read_text())
    home=(ROOT/config['sumo_home_relative']).resolve()
    if not home.is_relative_to(ROOT.resolve()):raise ValueError('SUMO_HOME outside project')
    if not (home/'bin/sumo.exe').is_file():raise RuntimeError('Project SUMO missing; see M02 report')
    os.environ['SUMO_HOME']=str(home)
    tools=str(home/'tools')
    if tools not in sys.path:sys.path.insert(0,tools)
    return home
