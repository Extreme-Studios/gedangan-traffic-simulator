# M15 — 3,000 Vehicles / One Hour Test

2 November 2026, WIB. Scope M15 only. All traffic inputs are MANUAL INPUT SCENARIO or RANDOMIZED SCENARIO — NOT FIELD OBSERVATION. No empirical Gedangan traffic calibration or claimed field capacity.

Staging: `http://127.0.0.1:5200/`; build `frontend/dist-m15/`; launcher `staging/m15/START_M15.ps1`. The existing M14 source/build/results and M12 release remain separate. Existing network `simulation\network\m051\provisional\network.net.xml`, SHA-256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. No flyover or M16 implementation. No permission override, forced insertion, new road/turn, geometry widening or removal of queued demand.

## Actual run
ID `cc809887025583f7156769c7`. Seed42; date2026-11-02,start07:00WIB; rate3000veh/h; duration3600s; physical requested3000. Nominal runnable random mix, weighted actual approaches, uniform departures across12five-minute bins of250 requests each. Warm-up is first300s of this same horizon; analysis window300–3600s, without hidden extra demand. Signal assumption12/3/2s per protected phase, cycle153s; three assumed nominal KA events600/1800/3000s. Schedule is not official.

| Lifecycle | Count |
| --- | --- |
| requested | 3000 |
| routed | 3000 |
| scheduled_departure | 3000 |
| loaded | 3000 |
| departed | 1914 |
| delayed_insertion_departed | 590 |
| moved | 1914 |
| arrived | 1346 |
| active | 568 |
| not_departed | 1086 |
| failed_routes | 0 |

Requested=Routed+Failed; Routed=Departed+NotDeparted; Departed=Arrived+Active. All equalities hold. SUMO wall time232.391s; total compute232.906s. NO_RECORDED_PERMISSION_COLLISION_TELEPORT_EVENTS. Teleports0, collisions0, illegal permission events0.

## Per direction
| Approach | Input | Routed | Departed | Arrived | Active | Pending | Failed | Mean insertion delay s | Mean speed m/s | Mean waiting s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontage | 111 | 111 | 111 | 110 | 1 | 0 | 0 | 0.195 | 7.998 | 0.0 |
| ketajen | 225 | 225 | 225 | 142 | 83 | 0 | 0 | 0.284 | 0.911 | 587.473 |
| northbound | 1085 | 1085 | 485 | 278 | 207 | 600 | 0 | 460.315 | 0.548 | 998.959 |
| rail_crossing | 275 | 275 | 275 | 271 | 4 | 0 | 0 | 0.962 | 7.816 | 0.576 |
| southbound | 1048 | 1048 | 562 | 307 | 255 | 486 | 0 | 259.353 | 0.501 | 984.799 |
| sukodono | 256 | 256 | 256 | 238 | 18 | 0 | 0 | 0.311 | 3.909 | 129.449 |

Northbound and southbound pending dominate. Low frontage waiting is not proof that all frontage traffic is uncongested: that selected cohort is smaller and spatially remote. Travel time is arrived-only and therefore censored; unfinished trips are retained. Means of waiting include departed but unfinished vehicles. Mean speed/density/stopped-time analysis excludes the warm-up window.

## Output/replay
`simulation/runs/m15/cc809887025583f7156769c7/`:demand.json, run.sumocfg, demand.rou.xml, controls.add.xml, FCD, summary/tripinfo/statistics XML, vehicle ledger, phase transitions, input/source snapshots/output hashes, approach/edge/insertion diagnostics and gzip playback chunks. TraCI samples0.5s; FCD interval-start clock +0.5s is checked against actual playback coordinates in independent XML audit. The original geometry hash is unchanged.

Video `documentation/m15/evidence/GEDANGAN_M15_3000_ONE_HOUR_ACTUAL.mp4` demonstrates a real excerpt of this one-hour run. It is not60minutes of realtime video or observed Gedangan footage. Video source/provenance and ffprobe metadata are saved separately. Screenshots show actual renderer positions, not decorative traffic.

## Conclusion
The one-hour request is actually executed and every ID accounted for. The model does not admit all3000within the hour under these assumptions. This is a documented model bottleneck, not a claim of measured road capacity or proof of presentation readiness.
