# M15 — Signal and Railway Test

2 November 2026, WIB. Scope M15 only. All traffic inputs are MANUAL INPUT SCENARIO or RANDOMIZED SCENARIO — NOT FIELD OBSERVATION. No empirical Gedangan traffic calibration or claimed field capacity.

Staging: `http://127.0.0.1:5200/`; build `frontend/dist-m15/`; launcher `staging/m15/START_M15.ps1`. The existing M14 source/build/results and M12 release remain separate. Existing network `simulation\network\m051\provisional\network.net.xml`, SHA-256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. No flyover or M16 implementation. No permission override, forced insertion, new road/turn, geometry widening or removal of queued demand.

## Assumed controllers, no fictitious priority-node lights
M05_gedangan is an inherited distributed controller with27phases and9controlled links; baseline cycle153s. Each controlled link receives12s green per cycle (about7.84%); yellow3s and all-red2s per isolated-link sequence. At two-lane approaches the links are separate protected phases, not simultaneous full-road service. This conservative uncalibrated arrangement is a credible model constraint, not evidence of actual Gedangan timing.

All phase states/link indices and topology remain unchanged; edited durations are loaded as a separate M15 tlLogic program. Priority nodes downstream of split stop-lines are not converted to traffic lights. Detailed per-link red/green allocation: `signal-service-audit.json`. Actual transitions are recorded from SUMO.

## Paired signal test, one-hour500requests northbound
| Configuration | Run ID | Departed | Arrived | Mean waiting s | Signal transitions |
| --- | --- | --- | --- | --- | --- |
| baseline | 1bf6203cdba7c62ff1f13605 | 495 | 283 | 573.1768 | 648 |
| green30 | fa0a139743a73cc41cab0409 | 500 | 350 | 457.785 | 320 |

Same seed/cohort/departure/network; green12→30s, cycle153→315s. Actual waiting and arrival change, proving controls affect traffic. This sensitivity is not a calibrated optimization or recommendation of official timing. The longer cycle also changes service to other links by design.

## Assumed railway test
One existing N_TO_S rail route,80m train, passing time converts to nominal speed; event list, delay, approach/closing headway, opening delay/time and minimum open/recovery are editable. Event frequency is controlled by the explicit arrival list. A nominal arrival is converted to an approximate free-flow departure; actual crossing samples and state transitions can differ. No reverse rail connection or exact official daily schedule is fabricated.

| Configuration | Run ID | Departed | Arrived | Mean waiting s | Signal transitions |
| --- | --- | --- | --- | --- | --- |
| with_trains | 34b5b80dafd8c17f0f773c97 | 400 | 391 | 0.4562 | 648 |
| without_trains | a642afaa0cdf7c2a3689bdcd | 400 | 391 | 0.0 | 636 |

400car requests on rail-crossing cohort, same seed/cohort; three assumed events versus none. Waiting changes from0.00000s to0.45625s. Arrival totals can be identical while queue/wait changes. This demonstrates in-model influence; it is not field closure evidence. Stop explanation samples and signals.json expose controller states at actual times.

Sources: inherited pilot config and network tlLogic; [SUMO Traffic Lights](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html), [SUMO Railways](https://sumo.dlr.de/docs/Simulation/Railways.html). Timing official verification remains MISSING.
