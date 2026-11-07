# M15 — Performance and Playback Report

2 November 2026, WIB. Scope M15 only. All traffic inputs are MANUAL INPUT SCENARIO or RANDOMIZED SCENARIO — NOT FIELD OBSERVATION. No empirical Gedangan traffic calibration or claimed field capacity.

Staging: `http://127.0.0.1:5200/`; build `frontend/dist-m15/`; launcher `staging/m15/START_M15.ps1`. The existing M14 source/build/results and M12 release remain separate. Existing network `simulation\network\m051\provisional\network.net.xml`, SHA-256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. No flyover or M16 implementation. No permission override, forced insertion, new road/turn, geometry widening or removal of queued demand.

## Actual compute
| Requested | Routed | Loaded | Departed | Moved | Arrived | Active end | Pending end | Failed | Generation s | SUMO wall s | Total wall s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 500 | 500 | 500 | 500 | 500 | 468 | 32 | 0 | 0 | 2.266 | 21.438 | 23.719 |
| 1000 | 1000 | 1000 | 1000 | 1000 | 848 | 152 | 0 | 0 | 0.234 | 53.735 | 54.0 |
| 3000 | 3000 | 3000 | 1914 | 1914 | 1346 | 568 | 1086 | 0 | 0.453 | 232.391 | 232.906 |
| 5000 | 5000 | 5000 | 2385 | 2384 | 1644 | 741 | 2615 | 0 | 0.609 | 378.422 | 379.172 |

Runs use SUMO1.28.0, step0.5s. Wall times include real local concurrent workloads; no isolated hardware certification. All5000requests are processed, but only2385depart and759is the maximum active count. Requested must not be equated with visible vehicles. Gzip playback loads the actual one-hour traces (7200frames), not generated decorative trajectories.

## Browser measurements
| Demand/h | Samples | FPS min | FPS median | p5 min | Max active sampled | Max draw calls | Rolling stall observations | JS heap peak MiB | Latest load s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3000 | 27 | 67.48 | 86.05 | 58.82 | 563 | 127 | 0 | 368.3 | 2.121 |
| 5000 | 28 | 68.42 | 83.33 | 39.84 | 745 | 126 | 0 | 472.6 | 3.736 |

These rows use active playback on the memo-map build. Measurements record mean FPS,p5, rolling stalls>50ms, sampled active count, draw calls, canvas/window dimensions, visibility/focus, session elapsed time and JS heap. A sum of rolling stall observations can double-count a stall; raw windows are preserved. Renderer active counts include recorded train objects when present and do not mean that every instance lies within the camera view; road accounting excludes the separately scheduled trains. FPS/counters update at sampled intervals. The viewport target was1920×1080, canvas height is smaller due controls. Heap is JavaScript telemetry only; it is not full browser RAM or VRAM. Compare actual per-sample dimensions in raw files.

## Performance finding and change
The first M15 build re-rendered the static SVG/source map and analysis table on every parent playback timestamp update. This produced low FPS despite the retained instanced3D renderer. React memoization now keeps static map/diagnostics work separate unless their result/selection changes. The M14 world/core renderer is retained; no premium redesign or fake fallback traffic was added. Early low/stalled samples remain in the audit, rather than being dropped to claim success.

Repeated run loading,3k→5k switching, high-active playback and camera switches were exercised in the internal browser. Latest observed session span1442.9s. Long-session memory is a bounded local observation only: garbage collection/load peaks and stalls remain visible; this is not a leak-free endurance certification. No promise of smooth performance across every Windows/AMD machine is made.

## Gate
PERFORMANCE ACCEPTANCE = CONDITIONAL. Actual playable workloads and the tested FPS/heap are evidenced, but initial stalls and short local endurance scope prevent an unconditional presentation-ready claim. See `performance-summary.json`, raw browser-performance files, browser QA evidence, video probe and screenshot artifacts.
