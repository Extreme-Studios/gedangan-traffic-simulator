# M15.6 — Performance Report

2 November 2026, WIB. Separate staging http://127.0.0.1:5202/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL NETWORK — NOT FIELD CALIBRATED.**

Network SHA256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. M12/M14/M15/M15.5 retained; no flyover, added road, permission change, GitHub upload or final EXE.

## Decision

**TARGETS_NOT_FULLY_MET.** All low samples are retained; no universal smoothness claim. Target3000:median≥45/windowp5≥30; target5000:median≥30/windowp5≥20. Heap target3000≤800MiB is assessed separately. The window p5 gate uses the lowest recorded window in the declared measurement interval, not an average chosen to pass.

| Demand | Samples | Median window medians FPS | Worst saved window p5 FPS | Max window stalls>50ms | Heap max MiB | Actual active | FPS target |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 500 | 4 | 119.05 | 117.65 | 0 | 716.3 | [27, 30] | REFERENCE |
| 1000 | 4 | 119.05 | 116.28 | 0 | 587.2 | [104, 109] | REFERENCE |
| 3000 | 4 | 119.05 | 60.61 | 0 | 1626.1 | [549, 563] | PASS |
| 5000 | 4 | 119.05 | 59.88 | 0 | 1542.0 | [689, 690] | PASS |

Heap maksimum per kasus memakai seluruh sampel final untuk run tersebut, termasuk transisi/idle; nilai window45s juga disimpan terpisah. Heap3000 gate: NOT MET. Raw result may have high frame medians while p5 drops sharply; this is not converted into a PASS. The reason for any long intervals is not proven as GPU saturation or browser throttling; visible/focus flags and raw durations remain evidence, not a diagnosis. CPU load/device state can affect results and the initial exploratory windows were kept separately, not silently merged into the final comparison.

## Consistent protocol

Same user Windows device,1920×1080/DPR1, fullscreen browser viewport, camera junction, speed1×, context on, no density/stopped overlay, nominal playbackt1800s. Each predeclared45s wall interval analyses seconds5–45 after5s settling. Actual stop time may be later due orchestration; the fixed analysis interval stays45s for everycase, recorded before inspection of results. Samples are logged about10s apart, each uses rolling120frames. Median of window FPS medians is reported, not a falsely precise lossless global frame median. Saved windows overlap; maximum stall count is not summed as unique stalls. Exact interval UTC boundaries and raw file list are in `benchmark-intervals.json` and `performance-summary.json`.

No demand totals, pending counts or active statistics were reduced to improve FPS. Rendered-instance range can be lower because actual camera frustum/LOD culls offscreen geometry; active remains actual recording count. No frame decimation or synthetic smoother flow was introduced.

## Browser soak

Final build tested: `m156-RwcClyM_.js`. Start 2026-11-02T08:50:14.792Z; end 2026-11-02T09:13:22.123577+00:00; elapsed wall 1387.3s, meeting minimum900s. Activity includes actual playback, four load levels, camera/recording switches, overlays, model review, inspector and UI operations. This is a mixed-activity soak, not15min uninterrupted playback at1×. Console errors/warnings at end: No errors reported in prior observed checks; durable final console snapshot was not saved before restart. All136saved renderer samples in this final session remain. Worst p5 across entire soak:39.84FPS; maximum JS heap:1626.1MiB, including transitions and idle. No claim of no memory leak from this bounded session.

## Device and loading

ASUS ROG Ally RC71L, installed RAM16GiB, OS usable11.70GiB, AMD Radeon Graphics/UMA.6GBVRAM allocation not independently certified. Heap is JavaScript heap, not total RAM/VRAM. Device state/thermal/power modes were not controlled as a laboratory benchmark. This evidence cannot certify every16GB/6GB Windows11 machine.

| Run | Fetch/decode wall ms | Frames | Positions |
| --- | --- | --- | --- |
| cc419452a995456df324fd05 | 1815.1 | 7200 | 3441615 |
| 4920f24adfe00bd29341b5eb | 708.3 | 7200 | 37417 |
| ae6c842a279f3d42d1dc9fbc | 760.3 | 7200 | 707465 |
| cc419452a995456df324fd05 | 1736.1 | 7200 | 3441615 |
| 569df9741bf6f16d1cffa31e | 2195.5 | 7200 | 4550529 |
| 49da5fe5c9c3f965850389e1 | 612.5 | 7200 | 190992 |

Loading timer measures actual recording fetch/decode. Reliable GPU first-present timing is MISSING; not included under a misleading loading claim. Raw renderer geometry/texture/drawcalls, viewport, speed, recordingID, active, camera, focus/visibility, and heap are preserved per sample. Bundle~848KB has Vite chunk>500KB warning; TypeScript and isolated build pass. No unsupported “6GB VRAM measured” or “all cameras always smooth” statement.
