# M15.6 — Acceptance Report

2 November 2026, WIB. Separate staging http://127.0.0.1:5202/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL NETWORK — NOT FIELD CALIBRATED.**

Network SHA256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. M12/M14/M15/M15.5 retained; no flyover, added road, permission change, GitHub upload or final EXE.

## Decision

**NOT AN UNCONDITIONAL PRESENTATION-GRADE ACCEPTANCE.** Visual implementation and functional checks delivered; network/traffic preservation verified. Visual quality requires user review; performance status **TARGETS_NOT_FULLY_MET**. Geospatial acceptance remains inheritedPARTIAL. A material/facade improvement is not a field-valid digital-twin certification.

| Gate | Status | Evidence / boundary |
| --- | --- | --- |
| Network/permissions/demand freeze | PASS within verified scope | 0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c |
| No flyover/road/frontage/rail change | PASS | Same XML and exported lane/junction/head coordinates |
| Class-specific assets | PASS model audit / REVIEW artwork | 10distinctgeometries, dimensions/ground contact exact; actual screenshots |
| Trailer gandengan | VISIBLE assembly / LIMITED articulation | Tractor, coupling gap, cargo and axle group; rigidSUMOheading proxy |
| Only actual moving traffic | PASS recorded checks | Retained FCD; rejected classes not placed in roads; separate labelled static asset preview |
| Lights / barriers / train | PASS sampled model consistency | Actual event playback and rail traces; physical interlocking/clearance unverified |
| Cameras / presentation / workflow | FUNCTIONAL with limits | 10presets,pan/orbit/reset/follow, Save/Load/Duplicate, Generate, Inspector and overlays |
| Actual screenshots / video | AVAILABLE | Allpreset captures, before/after, assetreview, livewatermarkedvideo |
| Performance benchmark | COMPLETE / TARGETS_NOT_FULLY_MET | 4fixedwindows; low p5 retained; JS heap measured |
| 15minute browser soak | COMPLETED | 1387.3s mixed activity, not hours of stability |
| Regression | PASS with one old skip | 395existingtests/394pass/1skip;12focusedpass; assetaudits |
| Preservation | PASS | 1146existingM15.5files equal plus ancestorcheckpoint |
| Building physical accuracy | NOT VERIFIED | Public footprint download502; neutral assumed massing only |
| Professional visual approval | REVIEW REQUIRED | Simplified shapes, neutral context and source road irregularities remain |
| Geospatial / historical calibration | PARTIAL / NOT CALIBRATED | Inheritedlimitations not removed by rendering |

## Deliverables

- `M15_6_3D_VISUAL_REPORT.md`
- `M15_6_VEHICLE_ASSET_REPORT.md`
- `M15_6_PRESENTATION_MODE_REPORT.md`
- `M15_6_PERFORMANCE_REPORT.md`
- `M15_6_REGRESSION_REPORT.md`
- `M15_6_ACCEPTANCE_REPORT.md`

Source `frontend/src/m156`, isolated build `frontend/dist-m156`, backend `m156_*`, new runs `simulation/runs/m156`, evidence `documentation/m156`, launcher `staging/m156/START_M156.ps1`. Read-only parent recordings use original IDs/hashes. `artifact-manifest.json` covers source/build/report/evidence and run input/source/output manifests. The live staging remains http://127.0.0.1:5202/.

## Remaining limits

Review real video and every camera for aesthetic approval. Placeholder context is not surveyed Gedangan. Road/source geometry sharpness, provisional lane widths, restricted classes, one-direction rail and pending root-cause limitations remain. No attempt to smooth traffic by modifying model, inventing roads, hiding pending demand or replacing failures. Further optimization should address measured low frame windows and memory/load limits, with repeat measurements rather than sample deletion. No next milestone, final EXE, destructive cleanup or external upload was started.
