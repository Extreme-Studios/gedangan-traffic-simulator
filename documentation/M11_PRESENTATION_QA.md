# QA presentasi M11

**TECHNICAL PRESENTATION PACKAGE READY PASS**. Hanya viewport simulasi dan browser terpasang yang diuji.

| Pengujian | Hasil / bukti |
|---|---|
| Python M01–M10 | 344 PASS, documentation/m11/baseline-regression.txt |
| M10 baseline controls | 18 PASS, qa/baseline/browser-qa.json |
| M10 core | 31 assertions, documentation/m11/baseline-m10-core.txt |
| Source preservation | 8104 hashes unchanged |
| Rehearsal A | 300.44s, qa/REHEARSAL_A.json |
| Rehearsal B | 900.66s, qa/REHEARSAL_B.json |
| Interruption / recovery | qa/REHEARSAL_C_FINAL.json, actual before/after video |
| Projector viewports / native zoom | six cases PASS, qa/projector-qa.json |
| Fault / offline fallback | PASS, qa/fallback-qa.json; injected404 classified as deliberate |
| PPTX | 15slides, two editable tables, one editable chart with workbook snapshot, final import/render PASS |
| PDF / handout | 15pages / 2pages, Poppler renders visually inspected |
| Video | 106.4s,1920×1080, copied byte-identical and browser-played |
| Visual review | qa/visual-review.json, M11_SLIDE_CONTACT_SHEET.png |

No simulated physical projector, human speech, official traffic prediction or field effectiveness is claimed. No M01–M10 output was overwritten. Browser-independent fallback HTML/PDF/video remains available without local server. Actual default BAT cold-start/reuse and isolated shutdown/restart were exercised. Details and initial failures/fixes are in MILESTONE_11_REPORT.md.
