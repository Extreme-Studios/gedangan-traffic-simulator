# M15 — Traffic Behavior and Bottleneck Report

2 November 2026, WIB. Scope M15 only. All traffic inputs are MANUAL INPUT SCENARIO or RANDOMIZED SCENARIO — NOT FIELD OBSERVATION. No empirical Gedangan traffic calibration or claimed field capacity.

Staging: `http://127.0.0.1:5200/`; build `frontend/dist-m15/`; launcher `staging/m15/START_M15.ps1`. The existing M14 source/build/results and M12 release remain separate. Existing network `simulation\network\m051\provisional\network.net.xml`, SHA-256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. No flyover or M16 implementation. No permission override, forced insertion, new road/turn, geometry widening or removal of queued demand.

## Direction comparison,3000/60min
| Approach | Input | Routed | Departed | Arrived | Active | Pending | Failed | Mean insertion delay s | Mean speed m/s | Mean waiting s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontage | 111 | 111 | 111 | 110 | 1 | 0 | 0 | 0.195 | 7.998 | 0.0 |
| ketajen | 225 | 225 | 225 | 142 | 83 | 0 | 0 | 0.284 | 0.911 | 587.473 |
| northbound | 1085 | 1085 | 485 | 278 | 207 | 600 | 0 | 460.315 | 0.548 | 998.959 |
| rail_crossing | 275 | 275 | 275 | 271 | 4 | 0 | 0 | 0.962 | 7.816 | 0.576 |
| southbound | 1048 | 1048 | 562 | 307 | 255 | 486 | 0 | 259.353 | 0.501 | 984.799 |
| sukodono | 256 | 256 | 256 | 238 | 18 | 0 | 0 | 0.311 | 3.909 | 129.449 |

Entering/exiting here mean actual depart/arrival of the selected route cohort, not measured counts across a field cordon. Vehicle density is computed only where lane storage length and sampled vehicle-seconds exist: mean vehicle-seconds / analysis duration / lane-km. It includes the sampled edge's modeled lanes and is not calibrated saturation density. Stopped means speed<0.3m/s.

## Why vehicles stop
Recorded-control explanation at10s samples for3000/60min: {'QUEUE_BODY_OR_UNRESOLVED': 101775, 'HEAD_NEAR_JUNCTION_PRIORITY_OR_SAFETY_UNRESOLVED': 4424, 'RECORDED_RED_OR_YELLOW_AT_NEXT_CONTROL': 8525, 'DOWNSTREAM_ENTRY_OCCUPIED_PROXY': 14237}. M14 reconstructed baseline: {'HEAD_NEAR_JUNCTION_PRIORITY_OR_SAFETY_UNRESOLVED': 1915, 'QUEUE_BODY_OR_UNRESOLVED': 28585, 'DOWNSTREAM_ENTRY_OCCUPIED_PROXY': 3311, 'RECORDED_RED_OR_YELLOW_AT_NEXT_CONTROL': 2118}. A stopped head near a controlled link with recorded red/yellow is labelled as observed control state; downstream entry occupied is only a proxy. Queue bodies and head-near-junction priority/safety cases remain unresolved where evidence cannot distinguish causes. These sample counts overlap vehicles across time; they are not unique delayed vehicle counts or causal duration shares.

## Largest stopped-time model hotspots
| Edge | Stopped vehicle-seconds | Max stopped/lane | Max stopped span m | Mean speed m/s | Mean density veh/lane/km |
| --- | --- | --- | --- | --- | --- |
| w512351908_s2_p0_0_f | 267390.0 | 65 | 249.74 | 0.256 | 209.76 |
| w512351908_s1_p0_0_f | 147930.5 | 47 | 169.12 | 0.37 | 177.8 |
| w562358500_s15_p0_0_f | 137838.0 | 30 | 117.65 | 0.192 | 219.84 |
| w512351908_s3_p0_0_f | 120466.0 | 27 | 95.62 | 0.193 | 226.3 |
| w562358500_s11_p0_0_f | 107763.0 | 28 | 101.04 | 0.273 | 199.76 |
| w562358500_s14_p0_0_f | 91335.5 | 23 | 83.45 | 0.217 | 212.63 |
| w562358500_s13_p0_0_f | 86930.0 | 23 | 77.63 | 0.241 | 211.03 |
| w562358500_s16_p0_0_f | 69045.0 | 14 | 56.8 | 0.189 | 220.06 |
| w512351908_s4_p0_0_f | 62519.0 | 14 | 45.83 | 0.174 | 245.75 |
| w266287937_s0_p1_0_r | 48473.0 | 26 | 106.23 | 0.297 | 160.73 |

The congested mainline edges include upstream origins, so congestion cannot be summarized as an isolated central-junction queue. Pending accumulates outside the active network; its delay must not be omitted from a smooth-looking3D scene. Source geometry includes very short edges; controller service, priority links and finite storage jointly matter. No unsupported geometry correction is justified solely by a low throughput number.

## Interactive evidence
Preview also lists failed request counts by class/approach/turn and the first failing edge with an Indonesian explanation. The2D view overlays actual source/SUMO shapes, candidate routes, source-tag provenance, route entry/exit, signals/crossing and stopped-time hotspots. Choose an approach to inspect input/routed/entered/arrived/pending/failed; route candidates show explicit connection chains and destination choices. Saved-run comparison is descriptive and warns against causal interpretation across different inputs. Graphs show pending over time rather than hiding uninserted demand.

Data: `explanations/<run>.json`, per-run edge-diagnostics.json, insertion-samples.json, approach-analysis.json, demand-timeline.json and vehicle-results.json. Queue extent is a sampled model span. Boundary censoring is not certified physical spillback.
