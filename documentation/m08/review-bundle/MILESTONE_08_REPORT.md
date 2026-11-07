# MILESTONE 08 — GEDANGAN TRAFFIC DIGITAL TWIN

## 1. Executive summary

SYNTHETIC / CONDITIONAL TRAFFIC EXPERIMENT — NOT AN EMPIRICALLY VALIDATED GEDANGAN FORECAST


Technical engine: **PASS**. 37 actual non-reproduction runs; 1 independent reproduction. Four operational interventions tested on existing model topology. No intervention is established as the best real-world Gedangan solution.


**INFRASTRUCTURE ENGINEERING FEASIBILITY: NOT VERIFIED — SURVEY AND DESIGN REQUIRED.**


**POLICY RECOMMENDATION: NOT YET DEFENSIBLE.** M06 empirical baseline is still blocked. M09 has not started.

## 2. Technical acceptance status

| Gate | Status |
| --- | --- |
| technical_engine | PASS |
| engineering_feasibility | NOT VERIFIED — SURVEY AND DESIGN REQUIRED |
| policy_recommendation | NOT YET DEFENSIBLE |
| empirical_baseline | BLOCKED / NOT CALIBRATED |
| M07_browser_closure | CLOSED_WITH_KNOWN_ISSUE |
| actual_nonreproduction_runs | 37 |
| fresh_reproduction_runs | 1 |
| regression_count | 289 |
| regression_pass | True |
| baseline_files_unchanged | 3576 |
| M09_started | False |

## 3. M07 browser QA closure

CLOSED_WITH_KNOWN_ISSUE. All 15 years, LOW/REFERENCE/HIGH, custom edit/save, actual job/cache endpoint, comparison, recorded playback, NOT RUN, desktop 1920×1080/mobile 390×844 and console inspected. M07-UI-01 remains: Comparison on mobile has22 px horizontal overflow. This was corrected in the QA record, not concealed. Original M07 source/reports/results were not edited. QA-specific custom copies/job ledger live under M08. See `documentation/m08/M07_BROWSER_QA_CLOSURE.md`.

## 4. Scenario catalog

| ID | Scenario | Catalog status | Actual results |
| --- | --- | --- | --- |
| S00 | Baseline / no intervention | SIMULATION_READY_PROVISIONAL | 9 |
| S01 | Synthetic signal timing alternatives | SIMULATION_READY_PROVISIONAL | 12 |
| S02 | Existing feeder left-turn closure | SIMULATION_READY_PROVISIONAL | 5 |
| S03 | Existing frontage exit closure | SIMULATION_READY_PROVISIONAL | 5 |
| S04 | Heavy vehicles deferred from first15min | SIMULATION_READY_PROVISIONAL | 6 |
| S05 | Corridor coordination | STRUCTURALLY_BLOCKED | 0 |
| S06 | Flyover concept | CONCEPT_ONLY | 0 |
| S07 | Underpass concept | CONCEPT_ONLY | 0 |

## 5. Scenario design methodology

Schema/versioned JSON; bounded sequential execution. S01 training uses only2026 REFERENCE seed11, green grid8/12/16s, yellow3s/all-red2s. Holdout evaluation seeds42/43 were not used to choose timing. Objective: departed-cohort waiting +2100s per unserved request + worst-OD mean waiting×OD count. This is a transparent software experiment objective, not calibrated social cost. No combined-intervention additivity assumed.

## 6. Baseline setup

M051 Pilot Provisional is primary; M051 Strict tested separately where compatible. Corrected Provisional is selectable for S00/S02/S03/S04; S01 requires existing road controller. M04 types/OD and M07 projections reused. Step0.5s; demand0–1800s; fixed horizon0–2100s; warm-up0s; optional drain0s. Same railway settings and train schedule70/970s for primary comparisons. No one-sided longer drain, teleport rescue, vClass ignoring, permission expansion, new road connections or demand deletion.

## 7. Operational intervention models

| Scenario | Declared mechanism | Limits |
| --- | --- | --- |
| S01 | One protected link per phase; chosen green8s; original phase order, yellow3s/all-red2s | Synthetic controller, not verified actual APILL |
| S02 | Restrict one existing feeder-to-main left-turn movement; reroute on existing legal graph | No U-turn/new connectivity; failures retained |
| S03 | Restrict one existing frontage exit movement | Existing frontage stays separate; local/feeder harm reported |
| S04 | Defer four truck/trailer categories originally departing before900s by900s | Original ID/OD/type demand retained; deferral costs explicit |
| S05 | No runnable coordination scenario | One valid road controller; railway crossing is not a second road controller |

## 8. Flyover conceptual feasibility

S06 CONCEPT_ONLY / NOT_SIMULATION_READY. Main arterial near existing Gedangan signal group is only a reference area, not a designed alignment. No ramp, elevated edge, false clearance or performance result created. Illustrative +6m/4%=150m each ramp; two ramps300m excluding vertical curves, landings, deck depth, frontage/feeder access and clearances. Footprint area and ROW fit unknown.

## 9. Underpass conceptual feasibility

S07 held to the same18-check gate. Illustrative −6m/4%=150m each ramp has the same exclusions and is not surveyed terrain/design. Groundwater, flooding, drainage/pump needs, utilities, foundation, railway construction staging, cost and land remain unknown. No cheaper/easier/better claim. Both concepts keep traffic metrics NULL and Run disabled.

## 10. Network lineage and derivative audit

Parent→scenario hashes and full declared changes are in each derivative `manifest.json`, linked from each `m08-input.json`. S00/S04 are byte copies. Operational geometry, lane lengths/speeds/shapes, junctions, connection identities, source edge lineage and railway crossing connections stay identical. S02/S03 narrow only declared movement permission; internal connector permissions are intersected with remaining legal incoming movements. No access expansion.

NETCONVERT1.28.0 unexpectedly recomputed/merged internal geometry during a timing-only roundtrip. Its intermediate XML and drift audit are retained and never used as final network. The final XML starts from the parent and receives only the verified semantic timing/permission delta. Actual SUMO validates/runs the final XML. This approach avoids quietly accepting NETCONVERT geometry drift.

Permission-graph component diagnostics (external edges; lane/via/connection permissions, not physical vehicle eligibility):

| Scenario | Family | vClass | Movements before | Movements after | Weak components before/after | Strong components before/after |
| --- | --- | --- | --- | --- | --- | --- |
| S00 | pilot-provisional | passenger | 2721 | 2721 | 67/67 | 1028/1028 |
| S00 | pilot-provisional | truck | 81 | 81 | 2/2 | 83/83 |
| S01 | pilot-provisional | passenger | 2721 | 2721 | 67/67 | 1028/1028 |
| S01 | pilot-provisional | truck | 81 | 81 | 2/2 | 83/83 |
| S03 | pilot-provisional | passenger | 2721 | 2720 | 67/67 | 1028/1035 |
| S03 | pilot-provisional | truck | 81 | 81 | 2/2 | 83/83 |
| S02 | pilot-provisional | passenger | 2721 | 2720 | 67/67 | 1028/1028 |
| S02 | pilot-provisional | truck | 81 | 81 | 2/2 | 83/83 |
| S00 | pilot-strict | passenger | 156 | 156 | 63/63 | 219/219 |
| S00 | pilot-strict | truck | 0 | 0 | 0/0 | 0/0 |
| S01 | pilot-strict | passenger | 156 | 156 | 63/63 | 219/219 |
| S01 | pilot-strict | truck | 0 | 0 | 0/0 | 0/0 |
| S01 | pilot-provisional | passenger | 2721 | 2721 | 67/67 | 1028/1028 |
| S01 | pilot-provisional | truck | 81 | 81 | 2/2 | 83/83 |

## 11. Demand cohort parity

Frozen original cohort includes every request ID, OD/endpoints, type and original departure. Hashes and full JSON must match before comparison. Manifest explains network hash differences; unexpected topology, parent, cohort, year, seed, family, projection, rail or schedule changes are rejected. Only S04 is allowed to change effective departures, with a per-ID deferral ledger. All comparison guards below passed.

| Year | Seed | Solution | Requests retained | Legal routes changed | New routing failures | Became routable |
| --- | --- | --- | --- | --- | --- | --- |
| 2026 | 43 | S03 | 240 | 18 | 0 | 0 |
| 2030 | 42 | S02 | 269 | 14 | 0 | 0 |
| 2026 | 43 | S02 | 240 | 12 | 0 | 0 |
| 2030 | 42 | S03 | 269 | 20 | 0 | 0 |
| 2040 | 42 | S02 | 360 | 18 | 0 | 0 |
| 2026 | 42 | S03 | 240 | 18 | 0 | 0 |
| 2040 | 42 | S03 | 360 | 28 | 0 | 0 |
| 2040 | 43 | S03 | 360 | 28 | 0 | 0 |
| 2040 | 43 | S02 | 360 | 18 | 0 | 0 |
| 2026 | 42 | S02 | 240 | 12 | 0 | 0 |

Changed routes retain original OD/type/endpoints. Full per-ID route sequences and failure reasons remain in both actual route ledgers. No illegal shortcut or invented connection is accepted.

## 12. Actual SUMO simulation matrix

| Year | Growth | Family | Seed | Scenario | Run ID | Requested | Arrived | Running | Failed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026 | REFERENCE | pilot-provisional | 11 | S01 | 8197ad47153d4866c91f | 240 | 179 | 27 | 34 |
| 2026 | REFERENCE | pilot-provisional | 11 | S01 | 86248095848e9d339be3 | 240 | 179 | 27 | 34 |
| 2026 | REFERENCE | pilot-provisional | 11 | S01 | de7568c6e739ebe40951 | 240 | 178 | 28 | 34 |
| 2026 | REFERENCE | pilot-provisional | 42 | S00 | 7e4475b8c3ecdfa4b025 | 240 | 183 | 23 | 34 |
| 2026 | REFERENCE | pilot-provisional | 42 | S01 | e123699c6b6c1169a364 | 240 | 185 | 21 | 34 |
| 2026 | REFERENCE | pilot-provisional | 42 | S02 | edec692f96b10c6f9bd1 | 240 | 182 | 24 | 34 |
| 2026 | REFERENCE | pilot-provisional | 42 | S03 | b508acf039d081329c7a | 240 | 178 | 28 | 34 |
| 2026 | REFERENCE | pilot-provisional | 42 | S04 | 21a640bd45c810fef10d | 240 | 181 | 25 | 34 |
| 2026 | REFERENCE | pilot-provisional | 43 | S00 | e2024af176edefe1fa09 | 240 | 182 | 24 | 34 |
| 2026 | REFERENCE | pilot-provisional | 43 | S01 | 3924797eddf6d506d4a1 | 240 | 182 | 24 | 34 |
| 2026 | REFERENCE | pilot-provisional | 43 | S02 | 2550eb4e924f93072146 | 240 | 182 | 24 | 34 |
| 2026 | REFERENCE | pilot-provisional | 43 | S03 | 1e8ad2b8af66d97edc90 | 240 | 180 | 26 | 34 |
| 2026 | REFERENCE | pilot-provisional | 43 | S04 | f11ddf7ded6919f2d21b | 240 | 178 | 28 | 34 |
| 2026 | REFERENCE | pilot-strict | 42 | S00 | 6570ec6983d96e451759 | 240 | 112 | 12 | 116 |
| 2026 | REFERENCE | pilot-strict | 42 | S01 | 6767885b80f521497b5a | 240 | 110 | 14 | 116 |
| 2030 | REFERENCE | pilot-provisional | 42 | S00 | af98a52bc855e571a5da | 269 | 210 | 25 | 34 |
| 2030 | REFERENCE | pilot-provisional | 42 | S01 | 0e8e117bc8c9dd748d17 | 269 | 215 | 20 | 34 |
| 2030 | REFERENCE | pilot-provisional | 42 | S02 | 1f27e42dd39f9c37396b | 269 | 210 | 25 | 34 |
| 2030 | REFERENCE | pilot-provisional | 42 | S03 | 40885ba6cee2c9e75912 | 269 | 203 | 32 | 34 |
| 2030 | REFERENCE | pilot-provisional | 42 | S04 | 8561749ea3a307e46086 | 269 | 204 | 31 | 34 |
| 2035 | REFERENCE | pilot-provisional | 42 | S00 | 7f08e6ef5870623160e4 | 311 | 240 | 27 | 44 |
| 2035 | REFERENCE | pilot-provisional | 42 | S01 | e920640d22cc237763de | 311 | 242 | 25 | 44 |
| 2035 | REFERENCE | pilot-provisional | 42 | S04 | a20837c2168d59bc80b2 | 311 | 235 | 32 | 44 |
| 2040 | HIGH | pilot-provisional | 42 | S00 | f6b49f6119ee784cf062 | 500 | 356 | 80 | 56 |
| 2040 | HIGH | pilot-provisional | 42 | S01 | 9c9e07a0a18d0cfec64f | 500 | 328 | 102 | 56 |
| 2040 | LOW | pilot-provisional | 42 | S00 | e21233cd873d98ccfde9 | 252 | 194 | 24 | 34 |
| 2040 | LOW | pilot-provisional | 42 | S01 | 0db16f329f2618e4c381 | 252 | 197 | 21 | 34 |
| 2040 | REFERENCE | pilot-provisional | 42 | S00 | 60628c2402702667a3f0 | 360 | 282 | 34 | 44 |
| 2040 | REFERENCE | pilot-provisional | 42 | S01 | 6588c128003ce0c8dbbb | 360 | 282 | 34 | 44 |
| 2040 | REFERENCE | pilot-provisional | 42 | S02 | 9438c051a9846e38c62b | 360 | 278 | 38 | 44 |
| 2040 | REFERENCE | pilot-provisional | 42 | S03 | c026e1d4667c65fc441b | 360 | 255 | 61 | 44 |
| 2040 | REFERENCE | pilot-provisional | 42 | S04 | 565ddf032b0934470df8 | 360 | 272 | 44 | 44 |
| 2040 | REFERENCE | pilot-provisional | 43 | S00 | 13214a24a46b15e13cfa | 360 | 281 | 35 | 44 |
| 2040 | REFERENCE | pilot-provisional | 43 | S01 | 2430e3ac4706a9c52bf7 | 360 | 285 | 31 | 44 |
| 2040 | REFERENCE | pilot-provisional | 43 | S02 | dfa2b5d19d5f8e66f2bf | 360 | 279 | 37 | 44 |
| 2040 | REFERENCE | pilot-provisional | 43 | S03 | c1b17b98da7dcc444d54 | 360 | 262 | 54 | 44 |
| 2040 | REFERENCE | pilot-provisional | 43 | S04 | 0064701b27ce5fa07b21 | 360 | 273 | 43 | 44 |

All configured2026–2040 years and existing custom M07 growth scenarios are supported; unexecuted combinations remain NOT RUN. Training rows seed11 are excluded from holdout Pareto/comparison.

## 13. Before/after comparison — 2026 and2040

| Year | Seed | Scenario | Requested | Routable | Failed | Loaded | Departed | Arrived | Running | Not departed | Unserved |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026 | 42 | S00 | 240 | 206 | 34 | 206 | 206 | 183 | 23 | 0 | 57 |
| 2026 | 42 | S01 | 240 | 206 | 34 | 206 | 206 | 185 | 21 | 0 | 55 |
| 2026 | 42 | S02 | 240 | 206 | 34 | 206 | 206 | 182 | 24 | 0 | 58 |
| 2026 | 42 | S03 | 240 | 206 | 34 | 206 | 206 | 178 | 28 | 0 | 62 |
| 2026 | 42 | S04 | 240 | 206 | 34 | 206 | 206 | 181 | 25 | 0 | 59 |
| 2026 | 43 | S00 | 240 | 206 | 34 | 206 | 206 | 182 | 24 | 0 | 58 |
| 2026 | 43 | S01 | 240 | 206 | 34 | 206 | 206 | 182 | 24 | 0 | 58 |
| 2026 | 43 | S02 | 240 | 206 | 34 | 206 | 206 | 182 | 24 | 0 | 58 |
| 2026 | 43 | S03 | 240 | 206 | 34 | 206 | 206 | 180 | 26 | 0 | 60 |
| 2026 | 43 | S04 | 240 | 206 | 34 | 206 | 206 | 178 | 28 | 0 | 62 |
| 2040 | 42 | S00 | 360 | 316 | 44 | 316 | 316 | 282 | 34 | 0 | 78 |
| 2040 | 42 | S01 | 360 | 316 | 44 | 316 | 316 | 282 | 34 | 0 | 78 |
| 2040 | 42 | S02 | 360 | 316 | 44 | 316 | 316 | 278 | 38 | 0 | 82 |
| 2040 | 42 | S03 | 360 | 316 | 44 | 316 | 316 | 255 | 61 | 0 | 105 |
| 2040 | 42 | S04 | 360 | 316 | 44 | 316 | 316 | 272 | 44 | 0 | 88 |
| 2040 | 43 | S00 | 360 | 316 | 44 | 316 | 316 | 281 | 35 | 0 | 79 |
| 2040 | 43 | S01 | 360 | 316 | 44 | 316 | 316 | 285 | 31 | 0 | 75 |
| 2040 | 43 | S02 | 360 | 316 | 44 | 316 | 316 | 279 | 37 | 0 | 81 |
| 2040 | 43 | S03 | 360 | 316 | 44 | 316 | 316 | 262 | 54 | 0 | 98 |
| 2040 | 43 | S04 | 360 | 316 | 44 | 316 | 316 | 273 | 43 | 0 | 87 |

| Year | Seed | Intervention | Δarrived | Δunserved | Δmax stopped | Δmax extent m |
| --- | --- | --- | --- | --- | --- | --- |
| 2040 | 43 | S04 | -8 | 8 | -1 | 0.00 |
| 2026 | 43 | S03 | -2 | 2 | 1 | -0.00 |
| 2026 | 42 | S04 | -2 | 2 | -1 | 0.00 |
| 2040 | 43 | S01 | 4 | -4 | 0 | 0.00 |
| 2026 | 43 | S02 | 0 | 0 | 0 | -0.00 |
| 2026 | 43 | S01 | 0 | 0 | -2 | 0.25 |
| 2040 | 42 | S04 | -10 | 10 | 2 | 6.47 |
| 2040 | 42 | S01 | 0 | 0 | 0 | 0.00 |
| 2040 | 42 | S02 | -4 | 4 | 4 | 9.26 |
| 2026 | 42 | S03 | -5 | 5 | 2 | 0.00 |
| 2040 | 42 | S03 | -27 | 27 | 23 | 18.33 |
| 2040 | 43 | S03 | -19 | 19 | 15 | 0.08 |
| 2040 | 43 | S02 | -2 | 2 | -1 | 0.35 |
| 2026 | 42 | S01 | 2 | -2 | -3 | 0.00 |
| 2026 | 42 | S02 | -1 | 1 | 1 | 0.00 |
| 2026 | 43 | S04 | -4 | 4 | -1 | -0.00 |

S01 effects vary across seeds and years. Closing the frontage exit can worsen arrivals and unfinished demand; these losses remain visible. Freight deferral is charged explicitly and does not remove truck requests. No overall winner follows from these conditional changes.

## 14. Travel time results

| Year | Seed | Scenario | Waiting mean s | Elapsed trip duration mean s incl unfinished | Arrived-only benefit |
| --- | --- | --- | --- | --- | --- |
| 2026 | 42 | S00 | 46.25 | 423.44 | SUPPRESSED — censored/unserved |
| 2026 | 42 | S01 | 44.26 | 420.98 | SUPPRESSED — censored/unserved |
| 2026 | 42 | S02 | 45.81 | 428.11 | SUPPRESSED — censored/unserved |
| 2026 | 42 | S03 | 71.43 | 449.24 | SUPPRESSED — censored/unserved |
| 2026 | 42 | S04 | 48.23 | 422.73 | SUPPRESSED — censored/unserved |
| 2026 | 43 | S00 | 47.36 | 427.59 | SUPPRESSED — censored/unserved |
| 2026 | 43 | S01 | 45.38 | 425.82 | SUPPRESSED — censored/unserved |
| 2026 | 43 | S02 | 47.83 | 432.74 | SUPPRESSED — censored/unserved |
| 2026 | 43 | S03 | 58.01 | 440.88 | SUPPRESSED — censored/unserved |
| 2026 | 43 | S04 | 49.05 | 425.94 | SUPPRESSED — censored/unserved |
| 2040 | 42 | S00 | 53.48 | 430.61 | SUPPRESSED — censored/unserved |
| 2040 | 42 | S01 | 62.04 | 438.63 | SUPPRESSED — censored/unserved |
| 2040 | 42 | S02 | 61.20 | 441.95 | SUPPRESSED — censored/unserved |
| 2040 | 42 | S03 | 137.88 | 504.70 | SUPPRESSED — censored/unserved |
| 2040 | 42 | S04 | 57.18 | 430.73 | SUPPRESSED — censored/unserved |
| 2040 | 43 | S00 | 53.04 | 431.25 | SUPPRESSED — censored/unserved |
| 2040 | 43 | S01 | 55.27 | 433.58 | SUPPRESSED — censored/unserved |
| 2040 | 43 | S02 | 57.87 | 441.04 | SUPPRESSED — censored/unserved |
| 2040 | 43 | S03 | 113.17 | 481.54 | SUPPRESSED — censored/unserved |
| 2040 | 43 | S04 | 52.96 | 426.62 | SUPPRESSED — censored/unserved |

Means describe departed-cohort exposure up to fixed horizon and include unfinished trips; they are not full requested-cohort journey-time estimates. Time loss/depart-delay/distributions and arrived-only raw durations remain in per-OD result data, with denominator/censoring labels. Lower elapsed time alone is not a benefit when late trips fail or remain unfinished.

## 15. Queue results

| Year | Seed | Scenario | Max stopped count | Max lane extent m | Queue lane-seconds |
| --- | --- | --- | --- | --- | --- |
| 2026 | 42 | S00 | 13 | 51.34 | 6640.00 |
| 2026 | 42 | S01 | 10 | 51.34 | 6461.00 |
| 2026 | 42 | S02 | 14 | 51.34 | 6136.00 |
| 2026 | 42 | S03 | 15 | 51.34 | 7230.00 |
| 2026 | 42 | S04 | 12 | 51.34 | 6907.00 |
| 2026 | 43 | S00 | 13 | 51.34 | 6908.00 |
| 2026 | 43 | S01 | 11 | 51.59 | 6282.00 |
| 2026 | 43 | S02 | 13 | 51.34 | 6100.00 |
| 2026 | 43 | S03 | 14 | 51.34 | 7172.00 |
| 2026 | 43 | S04 | 12 | 51.34 | 6937.00 |
| 2040 | 42 | S00 | 19 | 51.34 | 7557.00 |
| 2040 | 42 | S01 | 19 | 51.34 | 7770.00 |
| 2040 | 42 | S02 | 23 | 60.60 | 6924.00 |
| 2040 | 42 | S03 | 42 | 69.67 | 10565.00 |
| 2040 | 42 | S04 | 21 | 57.81 | 7389.00 |
| 2040 | 43 | S00 | 19 | 51.34 | 7795.00 |
| 2040 | 43 | S01 | 19 | 51.34 | 7722.00 |
| 2040 | 43 | S02 | 18 | 51.69 | 6832.00 |
| 2040 | 43 | S03 | 34 | 51.42 | 10747.00 |
| 2040 | 43 | S04 | 18 | 51.34 | 7669.00 |

Stopped threshold<0.3m/s; queue count and physical extent are distinct. Extent uses rear-most stopped body tail to furthest front; tails can extend below lane0 and are flagged boundary-censored. Bodies across adjacent edges are not reconstructed; internal/boundary uncertainty persists. Driver queues sampled1s; playback/queue-tail audit5s; occupancy/speed supplement0.5s. Queue lane-seconds sum over occupied queue lanes, not vehicle waiting time. Full-horizon occupancy includes empty samples; original conditional-on-nonempty occupancy is also retained and labelled.

## 16. Spillback results

| Year | Seed | Scenario | Verified in model | Unresolved candidates |
| --- | --- | --- | --- | --- |
| 2026 | 42 | S00 | 0 | 0 |
| 2026 | 42 | S01 | 0 | 0 |
| 2026 | 42 | S02 | 0 | 0 |
| 2026 | 42 | S03 | 0 | 0 |
| 2026 | 42 | S04 | 0 | 0 |
| 2026 | 43 | S00 | 0 | 0 |
| 2026 | 43 | S01 | 0 | 0 |
| 2026 | 43 | S02 | 0 | 0 |
| 2026 | 43 | S03 | 0 | 1 |
| 2026 | 43 | S04 | 0 | 0 |
| 2030 | 42 | S00 | 0 | 0 |
| 2030 | 42 | S01 | 0 | 0 |
| 2030 | 42 | S02 | 0 | 0 |
| 2030 | 42 | S03 | 0 | 2 |
| 2030 | 42 | S04 | 0 | 0 |
| 2035 | 42 | S00 | 0 | 0 |
| 2035 | 42 | S01 | 0 | 0 |
| 2035 | 42 | S04 | 0 | 0 |
| 2040 | 42 | S00 | 0 | 1 |
| 2040 | 42 | S01 | 0 | 0 |
| 2040 | 42 | S02 | 0 | 1 |
| 2040 | 42 | S03 | 4 | 31 |
| 2040 | 42 | S04 | 0 | 2 |
| 2040 | 43 | S00 | 0 | 0 |
| 2040 | 43 | S01 | 0 | 0 |
| 2040 | 43 | S02 | 0 | 0 |
| 2040 | 43 | S03 | 2 | 33 |
| 2040 | 43 | S04 | 1 | 2 |

M051 causal trace/detector retained. Zero detected episodes means none under the specific detector/model/horizon; it is not proof Gedangan has no real spillback. Congestion/queues are not automatically promoted to verified spillback.

## 17–18. Frontage and feeder impacts; per-OD trade-offs

Delta B−S00, REFERENCE seed42. Same endpoints and requested counts. Negative arrival delta is adverse. Waiting differences are conditional exposure, not a policy benefit.

| Year | Scenario | OD | Δrequested | Δarrived | Δfailed | Δrunning | Δwaiting mean s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026 | S04 | feeder_to_main | 0 | 0 | 0 | 0 | 0.12 |
| 2026 | S04 | frontage_continuity | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S04 | frontage_exit | 0 | 0 | 0 | 0 | -0.03 |
| 2026 | S04 | gedangan_junction | 0 | 0 | 0 | 0 | 1.43 |
| 2026 | S04 | ketajen_crossing | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S04 | local_trip | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S04 | main_to_feeder | 0 | 0 | 0 | 0 | 1.70 |
| 2026 | S04 | northbound | 0 | -1 | 0 | 1 | -0.55 |
| 2026 | S04 | southbound | 0 | -1 | 0 | 1 | 7.65 |
| 2026 | S04 | station_junction | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S04 | feeder_to_main | 0 | 0 | 0 | 0 | -0.03 |
| 2040 | S04 | frontage_continuity | 0 | 0 | 0 | 0 | -0.02 |
| 2040 | S04 | frontage_exit | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S04 | gedangan_junction | 0 | 0 | 0 | 0 | -26.32 |
| 2040 | S04 | ketajen_crossing | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S04 | local_trip | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S04 | main_to_feeder | 0 | -1 | 0 | 1 | 3.41 |
| 2040 | S04 | northbound | 0 | -6 | 0 | 6 | 9.12 |
| 2040 | S04 | southbound | 0 | -3 | 0 | 3 | 12.69 |
| 2040 | S04 | station_junction | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S01 | feeder_to_main | 0 | 0 | 0 | 0 | -11.94 |
| 2040 | S01 | frontage_continuity | 0 | 0 | 0 | 0 | -0.04 |
| 2040 | S01 | frontage_exit | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S01 | gedangan_junction | 0 | 0 | 0 | 0 | 20.73 |
| 2040 | S01 | ketajen_crossing | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S01 | local_trip | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S01 | main_to_feeder | 0 | -1 | 0 | 1 | 35.75 |
| 2040 | S01 | northbound | 0 | -3 | 0 | 3 | 25.19 |
| 2040 | S01 | southbound | 0 | 4 | 0 | -4 | -1.61 |
| 2040 | S01 | station_junction | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S02 | feeder_to_main | 0 | -2 | 0 | 2 | 28.97 |
| 2040 | S02 | frontage_continuity | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S02 | frontage_exit | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S02 | gedangan_junction | 0 | 0 | 0 | 0 | 15.32 |
| 2040 | S02 | ketajen_crossing | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S02 | local_trip | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S02 | main_to_feeder | 0 | 0 | 0 | 0 | 2.97 |
| 2040 | S02 | northbound | 0 | -2 | 0 | 2 | 25.39 |
| 2040 | S02 | southbound | 0 | 0 | 0 | 0 | -6.55 |
| 2040 | S02 | station_junction | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S03 | feeder_to_main | 0 | 0 | 0 | 0 | 0.08 |
| 2026 | S03 | frontage_continuity | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S03 | frontage_exit | 0 | -2 | 0 | 2 | 176.67 |
| 2026 | S03 | gedangan_junction | 0 | 0 | 0 | 0 | 0.07 |
| 2026 | S03 | ketajen_crossing | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S03 | local_trip | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S03 | main_to_feeder | 0 | 0 | 0 | 0 | 25.40 |
| 2026 | S03 | northbound | 0 | 0 | 0 | 0 | -2.80 |
| 2026 | S03 | southbound | 0 | -3 | 0 | 3 | 36.43 |
| 2026 | S03 | station_junction | 0 | 0 | 0 | 0 | 0.20 |
| 2040 | S03 | feeder_to_main | 0 | 0 | 0 | 0 | -0.06 |
| 2040 | S03 | frontage_continuity | 0 | 0 | 0 | 0 | 0.18 |
| 2040 | S03 | frontage_exit | 0 | -9 | 0 | 9 | 324.70 |
| 2040 | S03 | gedangan_junction | 0 | 0 | 0 | 0 | 6.61 |
| 2040 | S03 | ketajen_crossing | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S03 | local_trip | 0 | 0 | 0 | 0 | 0.00 |
| 2040 | S03 | main_to_feeder | 0 | -6 | 0 | 6 | 223.47 |
| 2040 | S03 | northbound | 0 | 0 | 0 | 0 | 5.46 |
| 2040 | S03 | southbound | 0 | -12 | 0 | 12 | 176.55 |
| 2040 | S03 | station_junction | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S01 | feeder_to_main | 0 | 0 | 0 | 0 | -10.50 |
| 2026 | S01 | frontage_continuity | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S01 | frontage_exit | 0 | 0 | 0 | 0 | -0.06 |
| 2026 | S01 | gedangan_junction | 0 | 0 | 0 | 0 | -2.57 |
| 2026 | S01 | ketajen_crossing | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S01 | local_trip | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S01 | main_to_feeder | 0 | 0 | 0 | 0 | -8.25 |
| 2026 | S01 | northbound | 0 | 0 | 0 | 0 | -7.30 |
| 2026 | S01 | southbound | 0 | 2 | 0 | -2 | 4.14 |
| 2026 | S01 | station_junction | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S02 | feeder_to_main | 0 | -1 | 0 | 1 | 21.71 |
| 2026 | S02 | frontage_continuity | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S02 | frontage_exit | 0 | 0 | 0 | 0 | -0.03 |
| 2026 | S02 | gedangan_junction | 0 | 0 | 0 | 0 | -31.75 |
| 2026 | S02 | ketajen_crossing | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S02 | local_trip | 0 | 0 | 0 | 0 | 0.00 |
| 2026 | S02 | main_to_feeder | 0 | 0 | 0 | 0 | -5.60 |
| 2026 | S02 | northbound | 0 | 0 | 0 | 0 | -1.30 |
| 2026 | S02 | southbound | 0 | 0 | 0 | 0 | 4.17 |
| 2026 | S02 | station_junction | 0 | 0 | 0 | 0 | 0.00 |

Frontage is existing source geography, not newly constructed. User observation of relatively smooth frontage is qualitative, not a target speed. S03 can worsen accessibility or shift queues; these outcomes are retained. Upstream/downstream lane traces, station, Ketajen, junction and corridor OD diagnostics remain available per run.

## 19. Heavy vehicles and class impacts

| Year | Seed | Deferred requests | Deferred departed | Deferred arrived | Deferral vehicle-s | Outside demand window | Outside horizon |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026 | 42 | 20 | 11 | 9 | 18000.00 | 0 | 0 |
| 2026 | 43 | 20 | 11 | 7 | 18000.00 | 0 | 0 |
| 2030 | 42 | 20 | 11 | 7 | 18000.00 | 0 | 0 |
| 2035 | 42 | 28 | 14 | 9 | 25200.00 | 0 | 0 |
| 2040 | 42 | 30 | 16 | 12 | 27000.00 | 0 | 0 |
| 2040 | 43 | 30 | 16 | 10 | 27000.00 | 0 | 0 |

| Year | Scenario | Vehicle type | Requested | Routable | Departed | Moved | Arrived |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026 | S00 | bus | 8 | 4 | 4 | 4 | 4 |
| 2026 | S00 | car | 100 | 100 | 100 | 100 | 89 |
| 2026 | S00 | heavy_truck | 8 | 4 | 4 | 4 | 2 |
| 2026 | S00 | light_truck | 16 | 10 | 10 | 10 | 9 |
| 2026 | S00 | medium_truck | 8 | 4 | 4 | 4 | 4 |
| 2026 | S00 | minibus | 16 | 12 | 12 | 12 | 10 |
| 2026 | S00 | motorcycle | 44 | 44 | 44 | 44 | 40 |
| 2026 | S00 | oversize | 8 | 0 | 0 | 0 | 0 |
| 2026 | S00 | pickup_van | 24 | 24 | 24 | 24 | 22 |
| 2026 | S00 | trailer | 8 | 4 | 4 | 4 | 3 |
| 2026 | S04 | bus | 8 | 4 | 4 | 4 | 4 |
| 2026 | S04 | car | 100 | 100 | 100 | 100 | 90 |
| 2026 | S04 | heavy_truck | 8 | 4 | 4 | 4 | 1 |
| 2026 | S04 | light_truck | 16 | 10 | 10 | 10 | 8 |
| 2026 | S04 | medium_truck | 8 | 4 | 4 | 4 | 4 |
| 2026 | S04 | minibus | 16 | 12 | 12 | 12 | 10 |
| 2026 | S04 | motorcycle | 44 | 44 | 44 | 44 | 40 |
| 2026 | S04 | oversize | 8 | 0 | 0 | 0 | 0 |
| 2026 | S04 | pickup_van | 24 | 24 | 24 | 24 | 22 |
| 2026 | S04 | trailer | 8 | 4 | 4 | 4 | 2 |
| 2040 | S00 | bus | 8 | 4 | 4 | 4 | 3 |
| 2040 | S00 | car | 164 | 164 | 164 | 164 | 149 |
| 2040 | S00 | heavy_truck | 8 | 4 | 4 | 4 | 3 |
| 2040 | S00 | light_truck | 28 | 16 | 16 | 16 | 13 |
| 2040 | S00 | medium_truck | 16 | 8 | 8 | 8 | 6 |
| 2040 | S00 | minibus | 16 | 12 | 12 | 12 | 11 |
| 2040 | S00 | motorcycle | 60 | 60 | 60 | 60 | 53 |
| 2040 | S00 | oversize | 8 | 0 | 0 | 0 | 0 |
| 2040 | S00 | pickup_van | 44 | 44 | 44 | 44 | 41 |
| 2040 | S00 | trailer | 8 | 4 | 4 | 4 | 3 |
| 2040 | S04 | bus | 8 | 4 | 4 | 4 | 3 |
| 2040 | S04 | car | 164 | 164 | 164 | 164 | 145 |
| 2040 | S04 | heavy_truck | 8 | 4 | 4 | 4 | 3 |
| 2040 | S04 | light_truck | 28 | 16 | 16 | 16 | 11 |
| 2040 | S04 | medium_truck | 16 | 8 | 8 | 8 | 6 |
| 2040 | S04 | minibus | 16 | 12 | 12 | 12 | 10 |
| 2040 | S04 | motorcycle | 60 | 60 | 60 | 60 | 52 |
| 2040 | S04 | oversize | 8 | 0 | 0 | 0 | 0 |
| 2040 | S04 | pickup_van | 44 | 44 | 44 | 44 | 40 |
| 2040 | S04 | trailer | 8 | 4 | 4 | 4 | 2 |

Oversize remains explicitly unroutable. Heavy vehicles use only inherited model permissions; no local-road diversion to bypass restrictions, no TraCI permission override. Existing trailer/heavy access remains provisional, not clearance/legal/swept-path certification.

## 20. Railway and crossing safety

Crossing logic and railway topology are preserved; actual train FCD/tripinfo, closed windows and controller states are retained. Road-lane occupancy during closed states and road-on-rail are checked at0.5s. Contextual crossing-near-red stopped vehicle-seconds are association only, not incremental causal rail delay. Neither concept eliminates any crossing closure in the executed model.

## 21. Safety diagnostics

Observed safety diagnostic check: PASS. Full-FCD permission audit covers 8,298,873 vehicle samples across 37 actual runs. Collisions, teleports, sampled illegal permissions, road-on-rail and sampled all-red crossing road occupancy are recorded explicitly. Emergency braking NOT MEASURED: no calibrated threshold. Collision0 does not certify geometry/clearance or real-world safety. Existing very short crossing lanes/geometry-provisional warnings remain.

## 22. Censoring and unserved demand

Every requested vehicle reconciles to failed route + arrived + running-at-end + not-departed. SUMO terminal summary loaded count is reconciled excluding actual train trips; raw driver event count is retained because initial loaded events can occur before polling. Failed routes, unfinished and pending insertions remain visible. Fixed2100s horizon for all pairs; no hidden demand reduction/drain.

## 23. Multi-criteria evaluation

| Dimension | Evidence | Treatment |
| --- | --- | --- |
| traffic_performance | QUANTIFIED_SIMULATED | See per-run model metrics and feasibility evidence |
| queue_spillback | QUANTIFIED_SIMULATED | See per-run model metrics and feasibility evidence |
| model_safety_diagnostics | QUANTIFIED_SIMULATED | See per-run model metrics and feasibility evidence |
| rail_model_interaction | QUANTIFIED_SIMULATED | See per-run model metrics and feasibility evidence |
| implementation_screening | QUALITATIVE_SCREENING | See per-run model metrics and feasibility evidence |
| community_access_tradeoffs | QUALITATIVE_SCREENING | See per-run model metrics and feasibility evidence |
| robustness_under_tested_assumptions | QUALITATIVE_SCREENING | See per-run model metrics and feasibility evidence |
| land | UNKNOWN_REQUIRES_STUDY | MISSING / NOT MEASURED |
| construction_cost | UNKNOWN_REQUIRES_STUDY | MISSING / NOT MEASURED |
| maintenance_cost | UNKNOWN_REQUIRES_STUDY | MISSING / NOT MEASURED |
| environment_construction_disruption | UNKNOWN_REQUIRES_STUDY | MISSING / NOT MEASURED |
| field_safety | UNKNOWN_REQUIRES_STUDY | MISSING / NOT MEASURED |
| physical_engineering_feasibility | UNKNOWN_REQUIRES_STUDY | MISSING / NOT MEASURED |

## 24. Traffic-only Pareto/trade-offs

| Year | Growth | Seed | Family | Traffic-only Pareto candidates |
| --- | --- | --- | --- | --- |
| 2040 | REFERENCE | 43 | pilot-provisional | S00, S01, S02, S04 |
| 2040 | LOW | 42 | pilot-provisional | S00, S01 |
| 2030 | REFERENCE | 42 | pilot-provisional | S00, S01, S02 |
| 2026 | REFERENCE | 43 | pilot-provisional | S01, S02, S04 |
| 2026 | REFERENCE | 42 | pilot-provisional | S00, S01, S04 |
| 2040 | REFERENCE | 42 | pilot-provisional | S00 |
| 2026 | REFERENCE | 42 | pilot-strict | S00, S01 |
| 2035 | REFERENCE | 42 | pilot-provisional | S00, S01 |
| 2040 | HIGH | 42 | pilot-provisional | S00 |

Minimize unserved requests, maximum stopped count, maximum lane queue extent and deliberate freight-deferral vehicle-seconds. No weighted sum mixes incompatible units. No overall winner: costs, land, engineering, field safety and community impacts are not quantified. Concepts are excluded from performance ranking.

## 25. Growth-year comparisons

REFERENCE requested2026=240,2030=269,2035=311,2040=360 in the inherited illustrative projection; LOW2040=252 and HIGH2040=500. Growth-year effects use separate labelled demand cohorts and must not be confused with same-year intervention effects. Primary2026/2040 holdout seeds42/43;2030seed42;2035 representative S00/S01seed42.

## 26. Sensitivity and uncertainty

Bounded LOW/HIGH2040 S00/S01seed42 and Strict2026 S00/S01seed42 are actual sensitivity runs, not empirical validation. Seed11 training is separate. These checks do not exhaust15years×growth×seed×families×solutions; unrun combinations remain NOT RUN. Network/source access uncertainty, synthetic driver parameters, OD/growth, railway timetable and censoring limit transfer to real Gedangan.

| Year | Growth | Family | Seed | Solution | Requested | Arrived | Running | Not departed | Unserved |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2040 | HIGH | pilot-provisional | 42 | S00 | 500 | 356 | 80 | 8 | 144 |
| 2040 | HIGH | pilot-provisional | 42 | S01 | 500 | 328 | 102 | 14 | 172 |
| 2040 | LOW | pilot-provisional | 42 | S00 | 252 | 194 | 24 | 0 | 58 |
| 2040 | LOW | pilot-provisional | 42 | S01 | 252 | 197 | 21 | 0 | 55 |
| 2026 | REFERENCE | pilot-strict | 42 | S00 | 240 | 112 | 12 | 0 | 128 |
| 2026 | REFERENCE | pilot-strict | 42 | S01 | 240 | 110 | 14 | 0 | 130 |

Signal timing selected on2026 training demand can worsen a high-demand holdout. Read any loss of arrivals or growth of pending/unfinished trips as an adverse outcome, not a reason to retune on evaluation seeds. Selection remains frozen; no attempt to force a winning result.

## 27. Performance

| Quantity | Measured value |
| --- | --- |
| Actual run wall time range s | 43.56–175.08 |
| Total actual run wall time s (excluding fresh reproduction) | 2946.26 |
| Max sampled SUMO working set MiB | 67.88 |
| Concurrency | 1 |
| Per-run process budget | 180s inherited bound |
| GPU/VRAM telemetry | NOT MEASURED; headless SUMO and SVG recorded playback |

Windows target16GB RAM/AMD GPU6GB is a target, not a certified benchmark. Process CPU seconds and sampled working set are saved per run. Cache manifests validate content before reuse. UI uses bounded five-frame playback pages, no dual live TraCI control.

## 28. Internal browser screenshots

M08 browser QA status: PASS. See `documentation/m08/m08-browser-qa.json` and screenshot files. Screenshots show actual recorded data or explicit concept-only state.

![m08-comparison-desktop](m08/m08-comparison-desktop.jpg)
![m08-comparison-mobile](m08/m08-comparison-mobile.jpg)
![m08-concept-mobile](m08/m08-concept-mobile.jpg)
![m08-final-overview](m08/m08-final-overview.jpg)
![m08-high-comparison-desktop](m08/m08-high-comparison-desktop.jpg)
![m08-high-spillback-desktop](m08/m08-high-spillback-desktop.jpg)
![m08-playback-desktop](m08/m08-playback-desktop.jpg)
![m08-underpass-feasibility](m08/m08-underpass-feasibility.jpg)

## 29. Regression tests

Initial old suite:234 tests PASS. Final: 289 tests in 117.310s; PASS. Logs: initial-regression.txt, final-regression.txt, typescript.txt, production-build.txt. Meaningful negative guards, actual SUMO mechanisms, full conservation/permission/rail audits, API and concept gates tested.

A post-browser suite exposed an intermittent incomplete-response failure in the local HTTP transport. The failed logs were retained; identity responses could stop after195840 of245099 declared bytes despite a complete server write. SO_LINGER was tested and removed because it did not resolve it. The tested correction is HTTP/1.1 with bounded16KiB chunk framing, plus compact polling and source-scoped request recovery. Both gzip and identity responses passed12 direct/proxy checks. Exact OS/intermediary cause is not claimed. Final regression covers the correction and the added browser-run data. See transport-root-cause.json and transport-chunked-check.json.

## 30. Reproducibility

```json
{
  "fresh_independent_SUMO_run": "simulation\\runs\\m08\\fresh-reproduction",
  "physics_equal": {
    "tripinfo.xml": true,
    "fcd.xml": true
  },
  "cache_manifest_unchanged": true,
  "baseline_files_checked": 3576,
  "original_files_drift": [],
  "method": "Exact numeric XML attributes excluding process/path headers; original input cohort preserved."
}
```

Fresh independent S00 run compares canonical numeric tripinfo/FCD XML, excluding process/path headers. Cache rerun verifies original output manifest unchanged. REBUILD_SOLUTIONS_M08.bat reuses verified caches and executes missing work sequentially; failed scientific setup attempts remain separately visible.

## 31. Source immutability

3576 baseline M01–M07 files rehashed unchanged. M08 modules/config/derivatives/results/documentation/viewer/launchers isolated. Original OSM, controls, M07 custom scenarios and reports preserved. Dynamic M07 QA copies are exclusively under M08. No dependencies installed. The three executable hashes are pinned in toolchain-sha256.json and checked by workflow/interactive entrypoints before cache reuse; initial --version logs separately prove actual1.28.0.

## 32. Engineering blockers

Surveyed elevations/ROW/land ownership/buildings/access, utilities, geotechnical/foundations, flood/groundwater/drainage, road/rail clearances, realistic ramp geometry, heavy swept paths, construction staging/emergency/local/pedestrian access and authority approvals missing. S05 additional valid controller missing. Concepts remain visible and blocked.

## 33. Empirical limitations

No calibrated2026 observation counts/OD/speeds/queues/signal/rail timetable. No synthetic number presented as a Gedangan measurement. No rupiah, acquisition area or field benefit invented. M08 advances experiment tooling and transparent conditional comparisons, not validated prediction or construction approval.

## 34. Acceptance criteria one by one

| No. | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | M07 browser QA closed or environment blocker documented | PASS | M07_BROWSER_QA_CLOSURE.md; M07-UI-01 mobile Comparison overflow22 px retained |
| 2 | Stable scenario catalog S00–S07 | PASS | configuration/scenarios-m08; schema validated |
| 3 | Actual S00 baseline | PASS | SUMO XML + lifecycle + route ledger |
| 4 | At least three feasible operational scenarios | PASS | S01/S02/S03/S04 actual; executable software mechanism, not field approval |
| 5 | Original network immutable | PASS | baseline-sha256.json |
| 6 | Auditable network derivatives | PASS | Per-network manifest; NETCONVERT intermediate quarantined |
| 7 | Vehicle permissions preserved | PASS | full-FCD-audits.json; oversize remains blocked |
| 8 | Rail crossing safety remains active | PASS | 0.5s FCD occupancy + actual crossing events; not physical certification |
| 9 | Demand cohort parity | PASS | cohort-original.json + paired parity guards |
| 10 | Actual before/after SUMO experiments | PASS | 27 primary +3 training; robustness separate |
| 11 | No hidden dropped trips | PASS | requested = failed + arrived + running + not departed |
| 12 | Actual travel/queue/spillback metrics | PASS | tripinfo.xml, full FCD, sampled queue trace, causal-events.json |
| 13 | Censoring handled | PASS | Arrived-only benefit suppressed; unfinished retained |
| 14 | Comparison fairness guards | PASS | Negative year/seed/family/cohort/geometry/schedule tests |
| 15 | Class/OD/feeder/frontage impacts visible | PASS | UI tables + full class/OD ledger + report tables |
| 16 | 2026/2030/2035/2040 selection | PASS | Browser all15 years; unrun combinations explicitly NOT RUN |
| 17 | Feasibility framework | PASS | Two18-check evidence/risk registers |
| 18 | Flyover honest concept gate | PASS | No ramp geometry or traffic metrics emitted |
| 19 | Underpass honest concept gate | PASS | Drainage/groundwater/utilities unresolved |
| 20 | No fabricated cost/land | PASS | UNKNOWN, never zero |
| 21 | Internal browser actual results/limitations | PASS | m08-browser-qa.json + screenshots + interactive job ledger |
| 22 | All regression tests pass | PASS | final-regression.txt |
| 23 | Rebuild reproducible | PASS | Fresh independent SUMO reproduction, exact canonical numeric XML |
| 24 | M01–M07 source/output intact | PASS | 3576-file initial baseline SHA-256 audit |

## 35. M09 readiness

Software comparison foundation is available subject to the technical status above. Empirical and engineering gaps remain explicit. **M09 NOT STARTED.** Starting it requires a new user instruction.

## Source and evidence index

`documentation/m08/source-register.json`, baseline-sha256.json, toolchain version JSON, EXECUTION_PLAN.md, run-queue.json, robustness-queue.json, offline-stage.json, signal-training.json, comparisons.json, full-FCD-audits.json, supplementary-audits.json, failure-ledger.json, acceptance.json, reproducibility.json and delivery-manifest.json. Canonical actual inputs/logs/XML/traces/recordings are under simulation/runs/m08; derivative manifests/NETCONVERT intermediates under simulation/network/m08.
