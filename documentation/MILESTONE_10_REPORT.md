# MILESTONE 10 — Gedangan Traffic Simulator

**VISUAL PRESENTATION READY PASS** · 1 November 2026 · M10 only

M10 adds a separate visual application and leaves M09 intact. Source: `frontend/src/m10/`; build: `frontend/dist-m10/`; read-only stdlib host: `backend/gedangan/m10_server.py`; launch: `START_GEDANGAN_M10.bat`; rebuild: `REBUILD_VISUAL_M10.bat`; URL: http://127.0.0.1:5186/visual.html.

Actual M09 screenshots identified broken dash phase/seams, repetitive tall context, floating/duplicated motorcycle wheels, plain vehicle silhouettes, weak camera composition, small labels and incorrect UNSERVED terminology. The initial audit documents priorities and evidence before renderer edits; source inspection alone was not used to judge appearance.

Road ribbons now share bounded miter vertices and dash phase follows polyline distance. Main and frontage remain separate, with distinct surface treatment and optional role colors. Direction indicators follow directed SUMO lane shapes; they are visual assumptions, not surveyed road markings. Junctions still use the original polygons; source topology is not edited to conceal geometric limitations. Railway keeps authoritative polylines, track gauge display, ballast, sleepers and actual controller states.

Context uses lower, spaced massing with roof caps, textured windows, trunk/canopy vegetation, contact shading and limited streetlights rejected near retained roads/rail. No landmark, building footprint, curb/shoulder or engineering clearance is invented as measured fact. Daylight is the default; lighting/shadow budgets favor readable roads and vehicles.

Vehicle models preserve M04/M09 registry dimensions and actual FCD identities. Cars gain tapered body geometry; truck/bus/trailer/minibus retain distinct proportions, wheels, windows, lamps and cargo/cab structure. Motorcycle duplicate wheels were removed; ground offsets align tires to the planar displayed road. Static local parts are baked per material/coach and instanced, reducing submission overhead without altering trajectories. Train coaches follow the existing retained rail chain. No oversize record is fabricated.

All eight cameras remain. Corridor/junction/rail views are closer, follow is heading-aware and dimension-aware, train follow uses a wider lateral view, aerial distance fits retained bounds/aspect ratio, and a session bookmark restores a saved viewpoint. Zoom/pan/tilt constraints and reset remain. Presentation layout reserves room for controls and notes within fullscreen rather than overflowing the projector viewport.

Playback preserves the M09 interpolation/visibility logic: 0.5 s FCD, 1 s control samples, +0.5 s FCD/TraCI clock alignment, no early spawn, no interpolation across invalid gaps, shortest-angle heading, real departures/arrivals. No movement data, demand, network permission or control sequence is changed.

Stopped-body/tail, occupied-length and role overlays use actual poses/lanes. Occupied intervals are merged; stopped threshold is 0.3 m/s. Overlays are sampled spatial indicators, not detector occupancy, verified queues, causal congestion or measured Gedangan traffic. Verified spillback on the dashboard is a horizon metric; no instantaneous cause map is fabricated. Conceptual infrastructure is separately labelled; S06/S07 show schematic transparent massing, no alignment/ramps/clearance or vehicles through an unvalidated concept.

Requested, routable, failed routes, loaded, departed, not departed, running at end and arrived are separated. NOT ARRIVED BY SIMULATION END = requested − arrived. All 23 cached run accounting identities were checked: requested=routable+failed; routable=departed+not departed; departed=arrived+running. Completion gives arrived/requested and 35-minute horizon. Throughput remains a fixed-horizon model rate, not measured capacity.

Comparison retains paired cohort/seed/horizon checks and shared camera/clock. Fullscreen includes the scoped result status and arrival counts. The adverse 2040 HIGH case shows S00 356 versus S01 328 arrived / 500 requested, WORSENED IN THIS SIMULATION · ARRIVED ONLY. Actual OD-specific arrived/running/not-departed/waiting deltas expose tradeoffs, with conditional-cohort warnings. Other metrics remain available; no global best solution or real-world effectiveness is inferred.

Validation: baseline M09 18 browser flows and 10 class views; M01–M09 344 Python tests in 173.933 s; M10 31 core assertions including all-run accounting and camera bounds; TypeScript/build with byte-identical repeat build; six actual host/launcher checks; final M10 18 browser flows and ten class views; responsive/capture checks, native Chrome zoom 125% and 150%; eight measured workloads and 12 repeated transitions. Functional and visual tests are reported separately, not added into an invented Python test count. The 35-minute recording completed at 16× without page crash.

Original protection: 7055 file hashes still match the pre-M10 checkpoint, including old source/config/data/network/outputs/reports/builds. Scope/exclusions are in `documentation/m10/baseline-scope.json`. M09 append-only browser telemetry is explicitly excluded. The M10 host hashes every original index, chunk and scene before use; original source cache is read-only. Extracted offline package was cold-started with global Python (stdlib only, no research venv/Node/SUMO), served the build and original recording gzip, returned 23 recordings and the correct acceptance status, then shut down cleanly on port 5187. Evidence: qa/package-smoke.json. This is a distribution runtime check, not a claim that the entire 16 GB research workspace is packaged.

Performance and hardware evidence: `M10_FINAL_VISUAL_QA.md`, `presentation_demo/m10/qa/performance-workloads.json`, `documentation/m10/hardware.json`. Results are per actual workload; no VRAM or universal hardware guarantee is inferred. The internal browser was visibly verified; the full matrix uses installed Chrome/Playwright. Preload 7207 ms; all measured mean/p5 windows meet 30 FPS: True.

Deliverables: twelve actual 1920×1080 screenshots under `presentation_demo/m10/screenshots/`, contact sheet `M10_VISUAL_CONTACT_SHEET.png`, actual H.264 Full HD demo `presentation_demo/m10/GEDANGAN_3D_DEMO.mp4` (106.40 s), final visual QA, README, 18-gate acceptance and evidence manifests. Video is screen capture of real local playback; no AI-generated traffic footage or fake measurement is used.

Remaining boundaries and candidates for later work:

- Empirical baseline remains BLOCKED; demand, growth, controller timing and registry dimensions are assumptions pending field validation.
- Buildings, trees, road arrows, streetlights and contact shading are stylized context, not surveyed physical Gedangan assets. No verified building footprints were supplied.
- Source short/internal lanes and angular junction boundaries remain in the retained network. Thin boundary marks may remain visible in close views; no source geometry/topology was changed to conceal this.
- Vehicles use lightweight procedural engineering forms, including rectilinear buses and cargo bodies. No articulated suspension, wheel spin or photorealistic asset set is claimed.
- Aerial overview prioritizes whole-network coverage; individual lanes/vehicles require corridor/follow close-up.
- Stopped/tail/occupied-length overlays are sampled spatial diagnostics, not measured detector occupancy, proven queues or bottleneck cause maps. Timed causal zone overlay is NOT AVAILABLE.
- Camera presets and context spacing reduce occlusion but do not certify collision-free navigation for every arbitrary orbit/follow path. Context can be toggled off.
- Actual internal browser successfully rendered and was operated earlier in this session; its final reload was blocked by Work settings. Final build matrix is verified in installed Chrome, not falsely reported as a final native-IAB matrix.
- M08.5 historical status is not promoted. Engineering clearance, swept path, legal access and S06/S07 feasibility remain unverified. M11/M12 are not started.

M11/M12 are not started. Empirical calibration requires verified field observations and independent validation; M10 does not promote historical M08.5 status or legal/engineering feasibility. Later work is recorded as a candidate only, not authorized by this report.
