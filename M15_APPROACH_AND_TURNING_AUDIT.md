# M15 — Approach and Turning Audit

2 November 2026, WIB. Scope M15 only. All traffic inputs are MANUAL INPUT SCENARIO or RANDOMIZED SCENARIO — NOT FIELD OBSERVATION. No empirical Gedangan traffic calibration or claimed field capacity.

Staging: `http://127.0.0.1:5200/`; build `frontend/dist-m15/`; launcher `staging/m15/START_M15.ps1`. The existing M14 source/build/results and M12 release remain separate. Existing network `simulation\network\m051\provisional\network.net.xml`, SHA-256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. No flyover or M16 implementation. No permission override, forced insertion, new road/turn, geometry widening or removal of queued demand.

## Root finding
M14 chose anchor-level signal connections. Ketajen, Sukodono and northbound signals are split points on a distributed junction, with only a straight immediate connection. Legal model branches occur at priority nodes after those signal splits. Thus straight-only lists were partly catalog extraction/boundary limitations, not proof that all other field turns are forbidden.

M15 traverses existing explicit connections from each signal anchor across compact split nodes, ending at the first longer outgoing corridor (over70m or accumulated200m; bounded16-link search). Local/service branches are not promoted to default primary corridor choices. Macro straight/left/right labels are INFERRED from incoming/outgoing headings; legality is screened per vehicle over all underlying lane-to-lane connections. No macro U-turn is invented. A turn absent from this selected catalog is not a blanket statement about every location in Gedangan.

| Approach | M14 catalog turns | M15 catalog turns | M14 route m | M15 route m |
| --- | --- | --- | --- | --- |
| ketajen | straight | straight, left, right | 462.62 | 885.99 |
| sukodono | straight | straight, left, right | 523.39 | 1048.01 |
| southbound | straight, left | straight, left | 1165.38 | 1165.38 |
| northbound | straight | straight, left | 886.07 | 1140.15 |
| frontage | straight | straight | 938.33 | 938.33 |
| rail_crossing | straight | straight | 524.62 | 524.62 |

Changed catalog candidate chains, source edge IDs, origin/destination and route length before/after are in `documentation/m15/approach-changes.json`. Different exit choices/lengths mean M14 and M15 totals are not an isolated intervention comparison.

## Actual SUMO proof
Run `49a472f38812b548519176a5`:120 manual cars,20 per cohort, distributed across all offered macro turns. Routed120; loaded120; departed120; moved120; arrived120; active0; failed0. Every offered approach/turn has at least one actual arrival. Each route follows explicit existing connections and class/access screens. `actual-turns.json`, run vehicle ledger/FCD and independent audit retain every ID. `actual-route-samples.geojson` exports12 actually traveled FCD trajectories (one per approach/turn) in EPSG:4326, including internal movement, with vehicle IDs and input/output provenance.

## Six-cohort limits
These six cohorts are useful model fixtures, not a complete directional OD survey. Frontage is northern. Railway road traffic also has a westbound connection but it is not a seventh selected cohort. Source U-turn connections elsewhere are not automatically offered. Named Sedati/Jenggolo/Jenggala coverage remains UNVERIFIED. User-selectable candidate examples are topology references, not permission for every class: heavy vehicles can still be denied feeder/local/width/conditional access routes.

Random default uses73%motorcycle,22%car,3%pickup/van,2%becak motor, all nominal assumptions supported on the default six straight routes. Bus/truck/trailer remain custom choices with per-approach compatibility shown. Bicycle/nonmotor becak are never converted to motorcycles; unsupported custom demand remains failed.
