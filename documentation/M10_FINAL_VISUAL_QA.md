# M10 final visual QA — 1 November 2026

**VISUAL PRESENTATION READY PASS**

Actual M09 baseline screenshots were inspected before polish. M10 actual screenshot contact sheet, twelve Full HD frames and ten actual class views were reviewed after functional testing. Review decisions and individual image findings: `presentation_demo/m10/qa/visual-review.json`.

Before/after panels: `presentation_demo/m10/screenshots/before-after-main.png`, `before-after-intersection.png`, `before-after-railway.png`, `before-after-vehicle.png`. Framing and layout intentionally differ; these are visual comparisons, not paired measurements of traffic benefit.

The internal browser was independently opened and operated on port 5186. Road/rail scene, actual train, closure badge and stopped-vehicle overlay were visibly verified. The saved internal-browser stats are one paused rendering window, not the full workload benchmark. A subsequent final reload returned Local browser use is disabled in Work settings; no final-IAB-matrix success is claimed. A Codex panel open request was queued separately, which is not a rendered-state verification. Chrome/Playwright captures supply the Full HD artifact evidence.

Final browser QA: 18 flows, 0 errors, 0 missing/error responses, 0 external requests. Class views: 10; oversize not fabricated. Capture status: PASS; actual demo video: PASS.

Issues found during development were retained as failed evidence: presenter controls initially exceeded the 1080p viewport. The layout was changed to bounded flex allocation and all 18 flows rerun. Aerial framing was subsequently fitted to modeled bounds for four aspect ratios; final screenshots must show the full network rather than merely a tiny or cropped diagram.

| Workload | Mean FPS | Minimum rolling p5 FPS | Maximum >50 ms stalls in a rolling window | JS heap after GC MiB |
|---|---|---|---|---|
| 2026 baseline | 119.7 | 117.6 | 0 | 103.6 |
| 2040 REFERENCE | 119.8 | 117.6 | 0 | 103.8 |
| 2040 HIGH | 119.6 | 117.6 | 0 | 135.3 |
| railway crossing | 119.1 | 117.6 | 0 | 135.3 |
| split 2040 HIGH adverse | 78.2 | 59.5 | 0 | 188.3 |
| follow vehicle | 119.8 | 117.6 | 0 | 172.3 |
| fullscreen 2040 HIGH | 119.3 | 117.6 | 0 | 172.3 |
| occupied lane overlay | 119.2 | 117.6 | 0 | 172.6 |

Additional renderer checks: 5 PASS, including pixel-stable paused screenshots, visible context/overlay toggles, separate unavailable causal-map/geometry warnings, and S07 no-traffic schematic. Browser zoom 125%/150% verified in isolated native Chrome settings.

Preload: 7207 ms. Renderer: ANGLE (AMD, AMD Radeon Graphics (0x000015BF) Direct3D11 vs_5_0 ps_5_0, D3D11). Samples: eight rolling windows per workload after warmup, same installed Chrome/native WebGL. Stall counts overlap between windows and must not be summed. JS heap is not total process/GPU memory. Repeated transitions: {'count': 12, 'heap_before': 180960896, 'heap_after': 180872920}. No physical VRAM capacity inferred. Background desktop activity may affect measurements.

Remaining boundaries:

- Empirical baseline remains BLOCKED; demand, growth, controller timing and registry dimensions are assumptions pending field validation.
- Buildings, trees, road arrows, streetlights and contact shading are stylized context, not surveyed physical Gedangan assets. No verified building footprints were supplied.
- Source short/internal lanes and angular junction boundaries remain in the retained network. Thin boundary marks may remain visible in close views; no source geometry/topology was changed to conceal this.
- Vehicles use lightweight procedural engineering forms, including rectilinear buses and cargo bodies. No articulated suspension, wheel spin or photorealistic asset set is claimed.
- Aerial overview prioritizes whole-network coverage; individual lanes/vehicles require corridor/follow close-up.
- Stopped/tail/occupied-length overlays are sampled spatial diagnostics, not measured detector occupancy, proven queues or bottleneck cause maps. Timed causal zone overlay is NOT AVAILABLE.
- Camera presets and context spacing reduce occlusion but do not certify collision-free navigation for every arbitrary orbit/follow path. Context can be toggled off.
- Actual internal browser successfully rendered and was operated earlier in this session; its final reload was blocked by Work settings. Final build matrix is verified in installed Chrome, not falsely reported as a final native-IAB matrix.
- M08.5 historical status is not promoted. Engineering clearance, swept path, legal access and S06/S07 feasibility remain unverified. M11/M12 are not started.
