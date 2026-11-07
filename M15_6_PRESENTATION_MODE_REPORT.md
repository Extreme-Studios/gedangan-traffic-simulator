# M15.6 — Presentation Mode Report

2 November 2026, WIB. Separate staging http://127.0.0.1:5202/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL NETWORK — NOT FIELD CALIBRATED.**

Network SHA256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. M12/M14/M15/M15.5 retained; no flyover, added road, permission change, GitHub upload or final EXE.

## Presenter view

GEDANGAN TRAFFIC SIMULATOR is the title. The default view fills the browser viewport, with technical builder, comparisons and network debugging panels hidden behind controls. This is a full browser-viewport presentation mode, not a claim of OS-level exclusive fullscreen. Kembali exposes the full scenario builder; no manual/random functionality was removed.

HUD shows selected date/startWIB, duration/timestamp, total demand, actual active count/current mean speed/stopped count, end arrived/pending and end maximum queue extent. Vehicle composition comes from retained result classes. End statistics are explicitly labelled akhir; moving/current values are recomputed from the selected recording/time. Pending remains a number and never creates traffic instances. Two watermarks and assumed-context/source notes remain visible. All displayed traffic numbers retain their original actual definitions.

Controls: play/pause/reset, speed1/5/10 (also0.5/2), actual recording selection, ten camera presets, reset camera, viewport enlargement, video capture, context/vehicle-label/road-label/status toggles and actual density/stopped overlays. Vehicle-follow chooses an actual active ID or user-selected actual vehicle. No diagnostic knowledge is required to choose the primary presets.

## Workflow verification

Browser workflow evidence: `documentation/m156/browser-workflow.json`. Save/Load/Duplicate, preview, seed/date/time, manual/random controls, actual SUMO execution, comparison and Inspector were exercised. Actual M15.6 SUMO run `25c64412778e7c7c50322609` has the exact same physical request cohort and result counts as original100request run `db7bf706bc67e37ce0910eef`:100routed/loaded/departed/moved,93arrived,7active,0pending,0failed. This confirms the visual wrapper did not change traffic in this tested cohort; it is not exhaustive proof for every possible input.

Video uses live3Dcanvas with timestamp/end-metric watermarks. Encoded metadata, hashes and frame verification are recorded in `video-verification.json`; no synthetic display traffic was substituted. Camera screenshots include static actual timestamps as well as running playback. Switching recordings pauses playback and preserves each run's actual end metrics.

## Limits

Neutral context is visibly approximate. Vehicle labels are a limited actual-ID roster and source road names are a legend; these are not screen-space labels anchored to every object. GPU first-present latency and a6GB VRAM allocation are not certified. No statistical outcome is presented as a calibrated historical measurement. Review the actual video and presets before presentation acceptance.
