# M15 — Demand Capacity and Insertion Analysis

2 November 2026, WIB. Scope M15 only. All traffic inputs are MANUAL INPUT SCENARIO or RANDOMIZED SCENARIO — NOT FIELD OBSERVATION. No empirical Gedangan traffic calibration or claimed field capacity.

Staging: `http://127.0.0.1:5200/`; build `frontend/dist-m15/`; launcher `staging/m15/START_M15.ps1`. The existing M14 source/build/results and M12 release remain separate. Existing network `simulation\network\m051\provisional\network.net.xml`, SHA-256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. No flyover or M16 implementation. No permission override, forced insertion, new road/turn, geometry widening or removal of queued demand.

## Input meaning
TOTAL3000/15min =3000 physical requests and12,000veh/h equivalent. RATE3000veh/h for15min =750 physical requests. RATE3000veh/h for60min =3000 requests. Conversion is displayed before Generate, recorded in `demand.json` and result.volume, and uses explicit half-up rounding for fractional physical counts. Manual per-class rates use largest-remainder allocation to the displayed converted physical total. Weighted mix/approach allocation preserves total and seed; no unsupported class substitution.

## Reconstructed M14 baseline
Source run `m14/67e1a759e0845754c09be215`:3000requested,2920routed,1271departed,566arrived,705active,1649pending,80failed. Read-only reconstruction uses original FCD/tripinfo with their hashes and a documented0.5s FCD-to-post-step clock offset.

| Approach | Input | Departed | Pending | Failed | Mean insertion delay s |
| --- | --- | --- | --- | --- | --- |
| frontage | 111 | 109 | 0 | 2 | 0.245 |
| ketajen | 225 | 132 | 79 | 14 | 25.091 |
| northbound | 1085 | 251 | 816 | 18 | 120.97 |
| rail_crossing | 275 | 252 | 0 | 23 | 3.1 |
| southbound | 1048 | 309 | 725 | 14 | 82.078 |
| sukodono | 256 | 218 | 29 | 9 | 9.202 |

Of 80 failed requests, 39 are bicycle-class denials; the other41 are19 light trucks,12 heavy trucks and10 buses. Detailed per-edge reconstruction shows truck lane-permission denials and bus road-function eligibility denials on the selected routes. Repeated blocked edges are not counted as extra vehicles; evidence is in `m14-reconstruction/failed-route-details.json`. No demand is lost. The1649pending are816northbound,725southbound,79Ketajen and29Sukodono. Their late insertion is measurable: original northbound departed vehicles average120.970s insertion delay, southbound82.078s. These are censored departed-cohort means, not delays for all requests.

## One-hour actual load tests
| Requested | Routed | Loaded | Departed | Moved | Arrived | Active end | Pending end | Failed | Generation s | SUMO wall s | Total wall s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 500 | 500 | 500 | 500 | 500 | 468 | 32 | 0 | 0 | 2.266 | 21.438 | 23.719 |
| 1000 | 1000 | 1000 | 1000 | 1000 | 848 | 152 | 0 | 0 | 0.234 | 53.735 | 54.0 |
| 3000 | 3000 | 3000 | 1914 | 1914 | 1346 | 568 | 1086 | 0 | 0.453 | 232.391 | 232.906 |
| 5000 | 5000 | 5000 | 2385 | 2384 | 1644 | 741 | 2615 | 0 | 0.609 | 378.422 | 379.172 |

These are tests of this uncalibrated model/configuration, not estimates of true Gedangan capacity. At500 and1000 demand/h all requests enter. At3000, pending1086; at5000, pending2615. Original phase/service, conservative route boundaries, priority/internal links and growing downstream queues can constrain throughput. No capacity/geometry parameter is inflated to force insertion.

## Explicit same-total duration contrast
The separate M15 TOTAL3000/15min run `c453595af5532112c8519a78` produced1324departed,569arrived,755active and1676pending, with0failed routes. The one-hour run has the same physical request total at one quarter of the average demand rate. Train event times and analysis horizon also differ, so this is a descriptive duration/load contrast rather than an isolated causal timing test.

## Measured evidence versus inference
Delayed-insertion counts flag actual departDelay greater than one0.5s simulation step, separating ordinary discretization from longer delay. Mean insertion delay includes all departed vehicles. Each pending sample every10s records origin, class, approach, scheduled time, oldest censored delay, lane length/permission, active occupancy, observed local entry-free distance and nominal length+minGap requirement. The origin/class gap calculation is a conservative local proxy; it does not reproduce every SUMO braking, route-lane, downstream priority or crossing safety check, and cannot certify a precise rejection cause. A gap that looks sufficient can still fail safe insertion.

3000/60min grouped insertion sample classifications: {'GAP_PROXY_SUFFICIENT_BUT_PENDING: downstream/route-choice/insertion safety checks unresolved': 478, 'OBSERVED_ENTRY_SPACE_SHORTAGE': 1537}. Counts are sampled groups, not unique vehicles. Queue boundary samples are not certified field spillback. At the horizon the live TraCI pending count agrees with scheduled-not-departed accounting. Per-ID insertion delay and censoring are in vehicle-results.json. No max-depart-delay removal or forced movement is used.

## Inspectable charts
`documentation/m15/evidence/pending-insertion-diagnostics.png`/`.pdf`, `one-hour-demand-accounting.png`; source hashes in chart-provenance.json. Interactive pending/active timeline and approach comparison remain visible in staging, including failed/pending demand.

Method reference: [SUMO Vehicle Insertion](https://sumo.dlr.de/userdoc/Simulation/VehicleInsertion.html). The application follows delayed-insertion accounting without applying insertion bypasses suggested as optional controls in other workflows.
