# Gedangan Traffic Simulator

**Status: FROZEN. Mulai dari [PROJECT_HANDOVER.md](PROJECT_HANDOVER.md) untuk memulihkan dan melanjutkan proyek.**

Source backup for the Gedangan traffic simulator by Extreme Studios. React/Three.js renders actual SUMO outputs on a location-based OSM environment. This repository contains source and the minimum retained network/context data for **Simple 20K mode**. It does not contain the complete research archive, installed dependencies, EXE distribution, or historical simulation recordings.

## Current simple mode

One input: **1–20,000 vehicle requests over one simulated hour**. The assumed automatic mix is 65% motorcycles, 22% cars, 6% angkot, 4% light trucks, 2% heavy trucks and 1% trailers; rounding preserves the total. Actual departures, arrivals, waiting insertion and rejected routes are reported separately. More demand does not force every vehicle onto the network at once.

Angkot uses assumed van parameters. Pedestrians are not available because the retained network does not provide legal pedestrian paths. Trailer routes retain provisional permission and geometric screens; this is not oversize authorization or a certified swept-path assessment. Network, demand, building heights and facades are provisional/assumed, **not calibrated Gedangan measurements or forecasts**.

## Run locally — Windows x64

Requirements: Python 3.12, Node.js compatible with Vite 7 (22.12+), and SUMO **1.28.0**. Install dependencies locally; none are included in Git.

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r tests/requirements.txt
cd frontend
npm ci
npm run check:simple
npm run build:simple
cd ..
```

Download SUMO 1.28.0 from the official URL recorded in `configuration/sumo-m02.json`. Extract so `toolchain/sumo-win64-1.28.0/bin/sumo.exe`, `tools/traci`, `tools/sumolib` and `data/xsd` exist. The project activates that local toolchain explicitly; a system SUMO_HOME alone is not used. Preserve vendor notices and licenses. Toolchain binaries are intentionally not committed.

```powershell
.venv/Scripts/python.exe -m backend.gedangan.simple_server --port 5206
```

Open http://127.0.0.1:5206/ in a WebGL2 browser. Enter a count and run. The first run calculates actual SUMO output before playback; large requests can take several minutes. New results are written locally under `simulation/runs/simple` and packed recordings under `staging/simple/recordings` (ignored by Git).

## Source coverage and historical milestones

`backend`, `frontend/src`, `configuration`, `tests` and human-readable milestone reports are retained. Frozen M15.5 and M05.1 network files, M04.5 permission metadata, source-to-edge mappings, the scene and required OD fixture are included for the simple application. Older launchers/tests are historical source: their datasets, exports and recorded runs are not all included, so this is not a claim that every milestone can be reproduced from this repository alone.

Portable packaging source is retained under `staging/m1562/portable`. Building an EXE package requires the local Python/SUMO runtime and Windows .NET compiler; no EXE or Release is uploaded here. Historical documents may describe local artifacts not present in this source backup. See `SOURCE_BACKUP.md` and `SOURCE_MANIFEST.json` for current coverage.

## Provenance and rights

Road/building geometry derives from OpenStreetMap contributors, ODbL 1.0: https://www.openstreetmap.org/copyright . Retain source tags/provenance and comply with ODbL obligations for adapted databases. Python, SUMO and npm dependencies retain their respective vendor licenses; install them separately. No new blanket software license is granted by this upload. Public availability of source is not a replacement for a license.
