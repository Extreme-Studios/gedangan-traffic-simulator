# M15 — Acceptance Report

2 November 2026, WIB. Scope M15 only. All traffic inputs are MANUAL INPUT SCENARIO or RANDOMIZED SCENARIO — NOT FIELD OBSERVATION. No empirical Gedangan traffic calibration or claimed field capacity.

Staging: `http://127.0.0.1:5200/`; build `frontend/dist-m15/`; launcher `staging/m15/START_M15.ps1`. The existing M14 source/build/results and M12 release remain separate. Existing network `simulation\network\m051\provisional\network.net.xml`, SHA-256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. No flyover or M16 implementation. No permission override, forced insertion, new road/turn, geometry widening or removal of queued demand.

## Decision
FUNCTIONAL / ACCOUNTING: PASS within the tested existing model. GEOSPATIAL ACCEPTANCE: PARTIAL. PERFORMANCE / PRESENTATION: CONDITIONAL. The simulator now explains modeled congestion and pending insertion with inspectable evidence, but retained OSM alignment and backend tests do not establish field-valid or presentation-ready Gedangan behavior.

| Gate | Status | Evidence / limit |
| --- | --- | --- |
| Existing source alignment | PARTIAL | OSM/source/SUMO overlay; independent survey and naming gaps remain |
| Road/rail topology | MODEL VALID / PARTIAL physical | Existing connection graph unchanged; single rail direction |
| Approach provenance | PASS selected cohorts | Source IDs, anchor nodes and boundary table; not complete field OD |
| Legal model turns / no fabricated turn | PASS | 120 actual cars across all offered turns arrived; connection/type screens |
| Volume total vs rate | PASS | 3000/h ×15min=750; TOTAL3000/15min=12000/h equivalent |
| Seed/composition conservation | PASS | Reproducible generator and manual-rate rounding tests |
| Unsupported classes warned | PASS | Per-approach support and explicit rejection reasons shown; custom failures retained |
| 3000/60min actual SUMO | PASS | 3000routed,1914departed,1346arrived,568active,1086pending |
| Mass balance/no missing vehicles | PASS | Requested/routed/departed partitions and XML audit |
| Pending explained | PASS with causal limits | Origin/class/time/gap/permission and queue evidence; unresolved cases explicit |
| Bottleneck location | PASS model evidence | Per-edge stopped time, storage boundary and control samples |
| Signal influence | PASS model sensitivity | Edited duration actually loaded; arrival/wait changes |
| Railway influence | PASS model sensitivity | Same400-car cohort with/without trains, actual wait change |
| Playback actual traces | PASS tested | FCD/TraCI0.5s clock check; no renderer fallback traffic |
| No flyover / M16 | PASS | Existing geometry hash unchanged; no added topology |
| Inspectable2D map | PASS | Interactive source/SUMO/route/control/queue/pending view |
| Regression | See final test logs | Missing old M14 service corrected before final rerun |
| Preservation | PASS | 1698 source/input/output hashes compared |
| Performance assurance | CONDITIONAL | Measured workloads, stalls, memory and bounded session scope |
| Field calibration / official timing | MISSING | Manual/random scenarios are not historical observations |

## Validation evidence
Final regression: 377 tests, status PASS, one M09 presentation-service CLI test skipped because that legacy presentation service is not running. The remaining 376 passed. Logs: `documentation/m15/regression-tests-final.txt` and `m15-tests-final.txt` (21 M15 tests pass after the final failure-explanation endpoint was added). TypeScript type check and isolated production build pass. Browser Generate100/hour also completed3600s:100routed/departed/moved,93arrived,7active,0pending,0failed; Save/Duplicate/Load restored the100/hour request. See `browser-workflow.json`. Independent XML/FCD audits currently12runs, all pass=True; final artifact manifest records source/output hashes. Initial regression failures were two old M14 HTTP tests because its service was not running; source was not changed to bypass them. The original M14 service was started and the suite rerun. M15 staging is separate5200.

## Remaining issues
Retained geometry/width/clearance and official signal/train timing remain unverified. Sedati/Jenggolo/Jenggala naming and full boundary/approach coverage are incomplete. Frontage is spatially remote; Ketajen/rail-crossing fixtures overlap corridor space. Pending1086at3000/h and2615at5000/h are retained; no model capacity inflation hides them. Gap and spillback indicators are proxies where direct cause is not available. The data cannot be presented as measured traffic or an empirically calibrated capacity study.

## Deliverables and workflow
Eight root M15 reports; separate frontend/backend staging; source/network GeoJSON/SVG overlay; route changes and samples; actual one-hour500/1000/3000/5000runs; manual multiclass and actual-turn tests; paired signal/rail tests; per-ID/edge/approach insertion diagnostics; charts, real3D screenshots and a real excerpt video. Save/Load/Duplicate and descriptive comparison use scenario-only JSON storage.

Open localhost5200, choose date/startWIB, total/rate and60min, edit mix/seed/approaches, Preview, Generate SUMO, inspect progress/result/pending causes and Play. Save a scenario or compare a retained run. No source or data is uploaded to GitHub, no research deletion, no replacement M12 EXE and no M16/flyover work.
