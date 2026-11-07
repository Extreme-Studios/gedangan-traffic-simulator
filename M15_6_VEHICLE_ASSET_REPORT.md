# M15.6 — Vehicle Asset Report

2 November 2026, WIB. Separate staging http://127.0.0.1:5202/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL NETWORK — NOT FIELD CALIBRATED.**

Network SHA256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. M12/M14/M15/M15.5 retained; no flyover, added road, permission change, GitHub upload or final EXE.

## Asset system

Ten road definitions retain their SUMO dimensions. Procedural per-class assemblies contain geometry for body, glazing, wheels, hubs, lamps and class-specific structure. Motorcycles include rider/helmet/two wheels; cars have an extruded tapered shell; pickup has an open load bed; buses have long glazing and bus proportions; trucks differ in size/axle arrangement; trailer has a tractor cab/chassis, distinct coupling gap and long ribbed trailer with separate axle group. Becak and bicycle assemblies remain separate from passenger vehicles. Deterministic muted instance paints vary appearance without changing class or count.

| ID | SUMO length × width × height m | Parts | Vertices | Envelope |
| --- | --- | --- | --- | --- |
| motorcycle | 2.1 × 0.8 × 1.4 | 12 | 465 | PASS |
| car | 4.5 × 1.8 × 1.5 | 26 | 1032 | PASS |
| pickup_van | 5.2 × 1.9 × 2.1 | 29 | 1104 | PASS |
| bus | 12 × 2.5 × 3.5 | 40 | 1212 | PASS |
| light_truck | 6.5 × 2.1 × 2.6 | 24 | 828 | PASS |
| heavy_truck | 11.5 × 2.5 × 3.8 | 28 | 1060 | PASS |
| trailer | 16.5 × 2.55 × 4 | 85 | 2700 | PASS |
| becak_nonmotor | 2.6 × 1.2 × 1.6 | 14 | 559 | PASS |
| becak_motor | 2.7 × 1.25 × 1.7 | 14 | 559 | PASS |
| bicycle | 1.8 × 0.65 × 1.5 | 8 | 347 | PASS |

Automated asset audit verifies all ten normalized geometry envelopes to1e-5m, minimum modelY=0 and ten distinct geometry hashes. Front-bumper FCD transforms subtract half actual length for render centre; render-surface offset is separate. Rail has eight coaches following the source rail path. Asset dimensions are model definitions, not measurements of a specific Indonesian vehicle fleet.

Trailer is visibly a tractor/gandengan assembly. It shares the SUMO heading as a rigid visual proxy; no independent trailer heading/physical articulation telemetry or swept-path certificate exists. Do not use the hitch gap to claim turn-clearance legality.

## Legal visibility and comparison

Live road traffic only instantiates IDs present in actual playback. Rejected bicycle/nonmotorized/heavy-route requests remain explicit failures and are not placed into roads. The stationary asset comparison is labelled MODEL PREVIEW ONLY — NOT ROUTED TRAFFIC, so all10definitions can be inspected without misrepresenting their route eligibility. Its screenshot proves visible form differences; actual movement proof remains FCD/ledger, not the gallery.

## Optimization

Per-material geometry is baked once, reused through dynamic InstancedMesh batches; maximum class capacities are computed in one pass through recordings. Source road surfaces are spatially tiled in200m render buckets without moving vertices. Camera-frustum tests exclude off-camera instances from draw batches. Glazing/wheel/hub detail drops beyond220m (LOD), while the body remains visible. Current active counts are computed from recordings, independent of culling or LOD. Shared procedural road/facade textures and instanced colours avoid per-vehicle image loads; no third-party texture atlas is required for these procedural assets. GPU resources are disposed when recordings change; old recording React state is cleared before loading the next. Entire actual frame data remains retained, not decimated to improve FPS.

Evidence: `vehicle-asset-audit.json`, `verify-assets.mjs`, `vehicle-assets.mjs`, registry snapshot and actual model-comparison screenshot. No paid/external vehicle assets or generated photographs were used.
