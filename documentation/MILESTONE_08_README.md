# M08 — Solution Comparison Lab

Technical engine: **PASS**. Synthetic/conditional experiments only. Engineering feasibility NOT VERIFIED; policy recommendation NOT YET DEFENSIBLE. M09 not started.

## Open

Run `START_SOLUTIONS_M08.bat` from the project. Viewer: http://127.0.0.1:5183/solutions.html, API:127.0.0.1:8773. Old M07 remains5182/8772. No new dependencies installed.

## Use

Choose S00–S07, year2026–2040, LOW/REFERENCE/HIGH/existing custom, seed42/43 and compatible parent. Comparison always pairs the same original request cohort with S00. Run queues actual local SUMO or verifies a cached result. Fresh/cached state is explicit. Unrun combinations show NOT RUN. S05 lacks two valid road controllers; S06/S07 are concept-only with Run disabled. Never interpret their reference circles as engineered ramps or traffic performance.

Map & playback uses actual5s recorded positions,0.5s physics; Play/Pause/Reset/Speed/Timeline/zoom/2D orbit/class filter. Orange queue rings/counts come from the selected recorded frame. Red square/S markers show active verified-in-model spillback at actual recorded vehicle positions; unresolved candidates are not promoted to verified markers. Full-horizon spillback counts are separate. Feasibility shows both18-check registers and unknown costs/ROW. Evidence shows hashes/change manifests/training split.

## Rebuild

Run `REBUILD_SOLUTIONS_M08.bat`. Sequential worker lease prevents concurrent interactive/offline SUMO. The workflow validates caches, completes27 primary runs plus3 training and6 robustness runs, plus the saved actual browser-validation case if present, then one independent fresh reproduction, full-FCD audits, comparison publication, full regression, TypeScript and Vite build. It regenerates the M08 report/review bundle. Do not change core scenario/runner/network/intervention source while a batch is active; their hashes identify reproducible results. Inspect offline-stage.json/failure logs before resuming an interrupted RUNNING marker. After the previous process has stopped, `REBUILD_SOLUTIONS_M08.bat --resume` verifies the single-worker lease and rejects any active headless SUMO process before resuming cached checkpoints. Never discard failed or censored trips.

## Evidence and limits

Read MILESTONE_08_REPORT.md and documentation/m08/status.json. M07 QA is CLOSED_WITH_KNOWN_ISSUE:22px mobile Comparison overflow retained because old sources are immutable. M08 browser QA is PASS. Baseline SHA check: 3576 original files unchanged. Every actual run retains request/route/lifecycle/deferral ledgers, SUMO logs/XML, network/control/cohort hashes, resource samples and output checksums. Actual run cache is verified, not fabricated animation.

Oversize is blocked. Heavy access is inherited/provisional; no field legal/clearance certification. Original railway safety remains. Flyover/underpass need terrain, ramps, clearance, ROW, utilities, geotechnical, drainage, access, staging and approvals before executable infrastructure simulation. No overall winner, fake cost, fake land area or empirical2026 claim.
