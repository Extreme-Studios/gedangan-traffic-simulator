# M15.5 — Acceptance Report

2 November 2026, WIB. Staging M15.5 terpisah: http://127.0.0.1:5201/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.**

## Keputusan

**M15.5 BELUM FULLY ACCEPTED. Backend execution/accounting/regression terverifikasi; GEOSPATIAL ACCEPTANCE PARTIAL; pending full causal attribution UNRESOLVED; browser workflow terverifikasi dengan batas; visual quality PENDING; performance CONDITIONAL.** Tidak memaksa PASS hanya karena request dapat dirutekan.

| Gate | Status | Bukti / batas |
| --- | --- | --- |
| Source / public map comparison | PARTIAL | 1961 edge inventory,23 public map features, source-provenance overlay; no field calibration |
| Proven geometry correction | NONE JUSTIFIED | No physical defect with sufficient correction evidence; frozen copy explicitly byte-identical |
| No fictional road/flyover/illegal bypass | VERIFIED within artifacts | Identical network hash; zero topology/permission changes |
| All road connections catalogued | VERIFIED model / PARTIAL physical | Inventory of existing connections; complete field OD/turn rules unknown |
| Rail crossing function | MODEL EVIDENCE | 863 stopped road samples;0 recorded steady-red entry/off-track; no building clearance proof |
| 3000/60min executed | VERIFIED | 3000routed/loaded,1914departed,1346arrived,568active,1086pending |
| Pending causal explanation | PARTIAL / UNRESOLVED | 254 observed entry-space shortage;832 other insertion checks unresolved |
| Fair controlled comparisons | VERIFIED model | Exact cohort equality, full requests/route/departure hash; no fictitious geometry improvement |
| Mass balance / permissions / playback | VERIFIED sampled checks | 8 independent XML/FCD audits PASS; no unexplained teleport/collision |
| Manual/random and total/rate | VERIFIED backend | Determinism/ten-class failures/Save Load Duplicate API; UI Save/Load/Duplicate dan dua Generate aktual juga terverifikasi |
| Regression M01–M15 plus M15.5 | PASS with one skip | 395 run,394passed,1 legacy presentation-service skip |
| TypeScript / isolated build | PASS | 832KB JS warning remains; not a browser performance measurement |
| Original preservation | PASS | 2984 existing file hashes equal; no old artifact overwritten |
| Visual inspector usability / real video | VERIFIED with limits | Road selector/source/permissions/actual counts; new screenshots and actual11.94s watermarked video; capture text soft |
| Visual quality / sustained performance | PENDING / CONDITIONAL | Actual loads/FPSmedian/p5/stalls/heap recorded; low samples retained; no multi-hour stability guarantee |

## Hasil penting

3000road requests selama60min tidak berarti3000 kendaraan berangkat atau tiba. Setelah execution120min,454 belum masuk dan475 masih aktif. Green30:1483 arrived/970pending; no-trains:1342arrived/1084pending. Tidak ada angka yang dipromosikan menjadi kondisi/kapasitas historis Gedangan.

## Laporan dan evidence

- `M15_5_NETWORK_REALITY_AUDIT.md`
- `M15_5_NETWORK_CORRECTION_REPORT.md`
- `M15_5_APPROACH_CONNECTIVITY_REPORT.md`
- `M15_5_PENDING_INSERTION_ROOT_CAUSE.md`
- `M15_5_3000_VEHICLE_COMPARISON.md`
- `M15_5_RAIL_SIGNAL_NETWORK_REPORT.md`
- `M15_5_VISUAL_VERIFICATION.md`
- `M15_5_ACCEPTANCE_REPORT.md`

Evidence root `documentation/m155/`; actual runs `simulation/runs/m155/`; separate frontend `frontend/dist-m155`; frozen network `simulation/network/m155`. `artifact-manifest.json` memberi SHA256 source/build/report/derived evidence; tiap run memiliki input, source snapshots dan output manifest. Source snapshots mewakili code saat eksperimen, bukan disamakan secara keliru dengan semua editor code terbaru.

## Menjalankan staging

Gunakan `staging/m155/START_M155.ps1`, atau dari root `.venv/Scripts/python.exe -m backend.gedangan.m155_server --port 5201`, kemudian buka http://127.0.0.1:5201/. Server aktif saat laporan dibuat. Original M14/M15/M12 tetap terpisah. Tidak membuat final EXE, upload GitHub, menghapus workspace, atau memulai M16.

## Pekerjaan tersisa sebelum acceptance penuh

Browser QA dan video kini tersedia; lanjutkan soak test lebih panjang dan review mutu visual pengguna. Verifikasi nama/boundary/median/gate/track/clearance melalui sumber atau survei yang cukup; kumpulkan APILL dan OD/count resmi. Untuk832pending dengan gap proxy cukup, perlu instrumentasi insertion checks lebih rinci sebelum menyatakan penyebab selesai. Tidak ada izin menuju flyover/M16 yang disimpulkan dari laporan ini.


## Pembaruan browser setelah restart

Blocker Browser Use sudah terselesaikan. Lihat laporan visual terbaru, `documentation/m155/browser-workflow.json`, `browser-performance-summary.json` dan `visual-status.json`. Keempat load level sudah dibuka, dua simulasi100kendaraan dijalankan dari UI dengan cohort identik, dan video actual telah diperiksa. Belum ada alasan menaikkan geospatialPARTIAL, full causalUNRESOLVED, visualqualityPENDING atau performanceCONDITIONAL menjadi PASS penuh.
