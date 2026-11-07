# M10 initial visual audit — 1 November 2026

Status: actual M09 screenshots inspected before M10 renderer changes. This is an audit, not final acceptance. M09 was opened through the real launcher, then its read-only server was restarted after the interrupted session. Internal browser access now works at port 5185.

Evidence: `presentation_demo/m10/baseline/` contains actual Chrome baseline screenshots and class views. `initial-contact.png` is a composite of those screenshots. Internal browser observation independently confirmed the opening/main corridor with actual recorded vehicles at 105.5 s.

| Priority | Observed problem | Actual screenshot | Source | Planned correction |
|---|---|---|---|---|
| P0 | Requested minus arrived is labelled UNSERVED, mixing incomplete trips with routing failure | main-corridor-2026, baseline-2040 | m09/main.tsx metrics | Separate all lifecycle counters, completion denominator and horizon |
| P0 | Comparison has raw deltas but no scoped result status; adverse 2040 HIGH must remain visible | before-after-split | m09/main.tsx comparison | Explicit arrived-cohort result with tradeoffs and 356 versus 328 adverse case |
| P1 | Asphalt strips have angular seams; dash spacing restarts per segment | main-corridor-2026, gedangan-intersection | m09/world.tsx ribbon/marking | Joined ribbon with bounded miters; continuous arc-length dashes; road role distinction |
| P1 | Repeated tall facade blocks dominate a sparse flat context; trees lack trunks | main-corridor-2026, reverse-corridor | m09/world.tsx urban | Lower varied massing, roof detail, trunks and believable clearances; retain decorative provenance |
| P1 | Vehicles read as plain boxes; wheels appear detached from road; motorcycle wheels duplicated | class-car, class-motorcycle, class-bus | m09/world.tsx vehicleParts | Improve body shaping, roof/glass/bumper detail, contact shadows and wheel contact |
| P1 | Railway is a long pale strip; crossing controls difficult to identify from distant view | railway-closed-train, railway-release | m09/world.tsx rails/heads; core.ts cameras | Improve ballast contrast, sleepers, crossing focus; keep actual controller states |
| P1 | Aerial camera leaves entire network as a tiny diagram in empty ground | aerial-overview, fullscreen-presentation | m09/core.ts cameraPreset | Fit network using view aspect and bounded camera composition |
| P1 | Follow camera foreground buildings obscure vehicles and train is cropped | class views | m09/world.tsx follow | Heading-aware follow offset scaled by actual class dimensions; context toggle |
| P1 | Fullscreen class view leaves unused lower band; presentation viewport too small | class views, fullscreen-presentation | m09/style.css fullscreen | Allocate remaining height to canvas, compact controls and presenter note |
| P1 | No actual-recording queue/occupancy overlays, road roles not immediately legible | traffic-signals, frontage-road | m09/world.tsx | Optional sampled overlays, definitions and unavailable-data states |
| P2 | Small typography and raw internal metric names impede projection readability | before-after-split, tablet-playback | m09/style.css/main.tsx | Larger labels, human-readable tables and compact lifecycle panel |
| P2 | Mobile fits width but has long stacked controls before scene | mobile-playback | m09/style.css | Compress secondary controls and preserve accessible touch targets |

Baseline checkpoint: `documentation/m10/baseline-scope.json` records 7055 original files / 16,736,365,758 bytes; source checkpoint SHA256 b7e6695ce5ce9886110da98fa279a9b882e80057a14925b295d012dc58b8daea. Excludes M10 namespaces and M09 append-only browser telemetry. Original network, recordings and old source remain immutable.

Baseline checks: TypeScript and isolated M09 build completed. The interrupted regression and 18-flow browser logs have no complete final result yet; they must be completed before acceptance. Actual class tests are running separately. Screenshots for rail-before closure and 1366×768 still need explicit capture; existing opening, aerial, both corridors, junction, frontage, closed/open rail, signals, 2026, 2040 HIGH, split, presentation, desktop/tablet/mobile and class evidence are retained.

No empirical calibration, field measurement or engineering feasibility is inferred from any image. M10 uses the original actual SUMO recordings read-only. M11/M12 are outside scope.

## Baseline verification completed

The previously interrupted runs were restarted: 344 Python tests PASS (173.933 s), M09 18 browser flows PASS, ten actual class views PASS, TypeScript and isolated baseline build PASS. Supplementary immutable-M09 rail-before-closure and 1366×768 captures were taken after the initial audit; they are explicitly not backdated as pre-polish evidence. See `baseline/railway-before-closure.png`, `baseline/desktop-1366.png` and `qa/zoom-and-baseline-extra.json`.
