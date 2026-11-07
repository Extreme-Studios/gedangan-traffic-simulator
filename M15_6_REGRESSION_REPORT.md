# M15.6 — Regression Report

2 November 2026, WIB. Separate staging http://127.0.0.1:5202/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL NETWORK — NOT FIELD CALIBRATED.**

Network SHA256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. M12/M14/M15/M15.5 retained; no flyover, added road, permission change, GitHub upload or final EXE.

## Results

Existing full suite:395tests,394passed,1legacy M09 presentation-service test skipped (service not running). Final focused M15.6 suite12testsPASS. One initial focused HTTP read failed with Windows connection reset on `/api/runs`; the initial log is retained, and the same unchanged test suite passed on rerun. No test was weakened or source network edited to force success. Logs: `regression-tests.txt`, `m156-tests-initial.txt`, `m156-tests.txt`.

Network byte hash stays `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. Scene lane/junction/head coordinate arrays exactly match export of frozen network. No edge/connection/rail/permission differences. Original M15.5 references include SHA256 result and output manifests; tests verify those retained results did not change.

Actual new100request run `25c64412778e7c7c50322609` compared against `db7bf706bc67e37ce0910eef`: exact vehicle IDs/classes/routes/departure cohort equality and actual end statistics equality. Independent XML/FCD auditPASS, input/source/output manifests retained. Generator reproducibility, unsupported bicycle failure retention, manual exact totals, parent/new recording API access and manual save/load are tested. No override to force an illegal class through the network.

Live UI tests are separate from backend tests: Save/Load/Duplicate, date/time, rate/total/manual/random, preview, actual Generate, inspector, overlays, compare selector, playback controls, video and ten presets were exercised as recorded in `browser-workflow.json`. Ten vehicle envelopes/ground/distinctgeometry auditsPASS. GPU artwork approval and field calibration are not established by Python tests.

Preservation checkpoint: 1146existingM15.5files checked, PASS, changed=[]. Parent milestone snapshot of2984files also checked through prior preservation logic; M12 release and original network remain untouched. Staging5202 only writes newM156scenario/run/evidence namespaces. Old traffic code is imported read-only; new runner copies it only to select isolated output folders/source identity, not to change demand/control mathematics.
