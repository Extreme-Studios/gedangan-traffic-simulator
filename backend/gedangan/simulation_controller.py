"""Lifecycle boundary. Engine availability never implies a live connection."""
import importlib.util
import os
from pathlib import Path
import shutil

class EngineNotConnected(RuntimeError):
    pass

class SimulationController:
    def status(self):
        home = os.environ.get('SUMO_HOME')
        binary = shutil.which('sumo') or (str(Path(home) / 'bin' / 'sumo.exe') if home and (Path(home) / 'bin' / 'sumo.exe').is_file() else None)
        return {'phase': 'FOUNDATION', 'engine': 'ENGINE NOT CONNECTED',
                'baseline_year': 2026, 'sumo_available': binary is not None,
                'traci_available': importlib.util.find_spec('traci') is not None,
                'data_validation': 'UNVERIFIED', 'calibration_status': 'NOT_STARTED',
                'simulation_running': False, 'network_loaded': False}

    def start(self):
        raise EngineNotConnected('M01 foundation: no verified network, demand, or TraCI session. Simulation is unavailable.')

    def step(self):
        raise EngineNotConnected('No active TraCI session.')
