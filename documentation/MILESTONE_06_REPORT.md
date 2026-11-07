# MILESTONE 06 — Baseline 2026 Data Readiness & Calibration Lab

Tanggal pelaksanaan: 31 Oktober 2026, Asia/Jakarta. Lingkup hanya M06. M07 belum dimulai.

## Executive summary

**TECHNICAL READINESS: PASS. EMPIRICAL BASELINE: BLOCKED — DATA REQUIRED.**

Phase A dan B selesai untuk fondasi data dan pengujian software terbatas. Phase C **BLOCKED — INSUFFICIENT OBSERVED DATA**. Tidak ditemukan observasi lapangan Gedangan 2026 yang terverifikasi pada input lokal yang diaudit. Tidak ada observed values yang dibuat. Tahun konfigurasi 2026 bukan bukti baseline empiris.

SUMO lokal 1.28.0 benar-benar menjalankan fixture terisolasi 600 m. Bounded search menemukan hidden vehicle_count=36 dan speed_factor=0.9, loss training=0 dan holdout sintetis=0. Hasil ini hanya **SOFTWARE CALIBRATION TEST — NOT EMPIRICAL CALIBRATION**. Fixture bebas konflik ini tidak membuktikan perilaku mixed traffic, sinyal, palang, antrean macet, atau kondisi fisik Gedangan.

## Perlindungan sumber dan audit awal

Laporan M03, M04, M04.5, M05, M05.1, governance, konfigurasi, jaringan, registry dan keluaran aktual diperiksa. Baseline SHA256 merekam 5661 file sebelum M06; pemeriksaan akhir tidak menemukan perubahan. Arsip/jaringan lama tetap utuh. M06 menambah modul/konfigurasi/viewer sendiri; tidak membangun ulang geometri Gedangan. Initial regression: 152 tests OK. Final regression: 182 tests OK, termasuk seluruh 152 lama.

`baseline-sha256.json` adalah bukti per-file, bukan sekadar pernyataan berdasarkan laporan lama. `reproducibility.json` menyimpan verifikasi fresh SUMO dan checkpoint. `delivery-manifest.json` merekam source/config/input/output M06, versi runtime, seed, serta hash artefak.

## Inventory, provenance dan sumber publik

Inventaris lokal adalah triage berdasarkan jenis/asal file; label tidak menaikkan asumsi menjadi observasi. Metadata asli dan audit sumber tetap berwenang. Seluruh daftar berada di `inventory.json`.

| Kelas sumber lokal | File dalam triage |
|---|---:|
| ENGINEERING_INFERENCE | 453 |
| MODEL_ASSUMPTION | 39 |
| GEOSPATIAL_REFERENCE | 49 |
| SYNTHETIC_TEST | 303 |
| SIMULATED_RESULT | 1135 |

Kategori OBSERVED_FIELD tidak mempunyai data terverifikasi. OFFICIAL_ADMINISTRATIVE dan PUBLISHED_RESEARCH dicatat terpisah pada `public-source-register.json`. MISSING dipakai pada register kebutuhan, bukan sebagai pengukuran. OSM/atribut jalan adalah GEOSPATIAL_REFERENCE; policy/interpretasi adalah ENGINEERING_INFERENCE; kendaraan, OD, sinyal dan jadwal sintetis adalah MODEL_ASSUMPTION/SYNTHETIC_TEST; FCD/tripinfo adalah SIMULATED_RESULT.

Audit daring 31 Oktober 2026:

- [Studi STTD Gedangan](https://digilib.ptdisttd.ac.id/8279/1/Jurnal%20Kajian%20Rencana%20Pengendalian%20Simpang%20Gedangan%20M.Rizky%20Bima.P.pdf) memuat studi historis 2024/referensi2022, bukan raw observations2026. PDF terbaca melalui penelusuran web; unduhan biner lokal403. Tidak direplikasi sebagai dataset lapangan.
- [Artikel UMPR](https://journal.umpr.ac.id/index.php/mits/article/download/11418/6353/45315) terbit Januari2026 tetapi metode menyebut survei Mei2025. Tahun publikasi tidak diubah menjadi tahun survei. Web PDF diperiksa; unduhan biner lokal403. Tidak eligible untuk baseline2026.
- [Portal Dishub Sidoarjo](https://opendata.sidoarjokab.go.id/id/dataset/data-indentifikasi-masalah-lalu-lintas) berisi resource2023–2025, dengan keterangan No License Provided. HTML disimpan dengan hash; XLS belum berhasil diparsing oleh alat penelusuran. Tidak ada directional interval counts2026 yang diekstrak.
- [Metadata kegiatan BPS](https://sirusa.bps.go.id/sirusa/kegiatan/c4e9f75e-ff36-bfba-8aab-e1a79719b138) adalah metadata kegiatan statistik, bukan bukti dataset time-series Gedangan telah diterbitkan. Akses langsung403. Tidak dihitung sebagai observasi tersedia.

Lisensi/izin penggunaan ulang yang belum jelas tetap dicatat. Statistik kepemilikan kendaraan kabupaten tidak digunakan sebagai volume simpang. `public-review-notes.json` memisahkan pemeriksaan web dari keberhasilan unduhan lokal. Eksperimen SUMO memakai semua input lokal dan tidak memerlukan jaringan internet.

## Data completeness dan prioritas pengumpulan

| Domain | Record2026 | Status | Prioritas |
|---|---:|---|---|
| traffic_count | 0 | MISSING | CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION |
| travel_time | 0 | MISSING | CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION |
| queue | 0 | MISSING | CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION |
| signal | 0 | MISSING | CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION |
| railway | 0 | MISSING | CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION |
| geometry | 0 | MISSING | CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION |
| OD_and_turning | — | MISSING | CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION |
| independent_days | — | MISSING | CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION |
| repeat_weather_side_friction | — | MISSING | IMPORTANT — IMPROVES CONFIDENCE |
| fine_lateral_trajectories | — | MISSING | OPTIONAL — FUTURE REFINEMENT |

**CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION:** tally15 menit per kelas/arah/gerakan pada koridor utama dua arah, simpang, frontage, feeder dan akses stasiun; OD/turn shares dengan metode yang dapat ditelusuri; travel-time per rute dengan sampel; panjang antrean meter dan count terpisah; signal-head/phase/cycle/offset aktual; warning/closure/train pass/clearance/reopen/release aktual; survei centerline, stop-line, gate, lane/storage dan clearance; hari/sesi independen yang dicadangkan sebelum fitting. Sumber harus menyertakan tanggal, lokasi, metode, uncertainty dan provenance yang dapat diverifikasi.

**IMPORTANT — IMPROVES CONFIDENCE:** pengulangan hari/cuaca, visibilitas, hambatan samping, event log dan hitung ganda independen. **OPTIONAL — FUTURE REFINEMENT:** trajectory lateral anonim yang berizin setelah data dasar memadai. Tidak ada jaminan validitas berdasarkan jumlah hari saja; cakupan harus dinilai terhadap tujuan studi.

## Survey methodology dan template

Tujuh lokasi di bawah adalah **rencana**, bukan titik observasi terverifikasi. `survey-plan.json` menyimpan lane/junction/source-way, alasan, kelas, metrik, metode, sesi, bias dan kejadian khusus. Usulan3 hari kerja+1 akhir pekan dengan sesi07–09/12–14/16–18 WIB harus dikonfirmasi melalui reconnaissance; belum ada klaim jam puncak.

| Lokasi rencana | Arah model | Edge model |
|---|---|---|
| MAIN_NB | northbound | `w562358500_s16_p0_0_f` |
| MAIN_SB | southbound | `w512351908_s4_p0_0_f` |
| GEDANGAN_FEEDER | eastbound | `w266287930_s0_p0_0_f` |
| FRONTAGE | source_direction | `w1118947356_s0_p0_0_f` |
| KETAJEN | eastbound | `w1240685448_s1_p2_0_f` |
| STATION_CROSSING | westbound | `w1240685448_s1_p2_0_r` |
| UPSTREAM_STORAGE | southbound | `w512351908_s3_p0_0_f` |

Metode rinci pada `SURVEY_METHOD.md`: clock tersinkron, dua pencacah/checks, 15 min tally, rute travel-time konsisten, definisi queue/body/batas visibilitas, event control/rail dan survei berwenang. Video hanya sah/berizin; minimalkan identitas; tidak scraping CCTV privat. Field mapping frontage dan OD tetap perlu review manual.

`data/templates/m06` menyediakan9 CSV header-only,6 JSON kosong per jenis observasi, registry provenance dan panduan10 kelas M04. Workbook opsional `Gedangan_Survey_Forms.xlsx` mempunyai9 sheet:8 form kosong dan1 panduan klasifikasi; panduan metodologi adalah dokumen ke10. Sel worksheet pengamatan tidak diisi angka sintetis. JSON/CSV dapat diimpor; workbook adalah form manual, bukan importer XLSX. Template arrays harus diisi sebelum import. Contoh DEMO_SYNTHETIC berada di folder terpisah.

## Schema, ingestion dan QA

Enam Draft2020-12schemas mencakup traffic_count, travel_time, queue, signal, railway dan geometry. Timestamp harus eksplisit+07:00/Asia/Jakarta; field metrik wajib hadir tetapi boleh null. NULL/MISSING berbeda dari count0 yang diamati. Jenis kendaraan mengikuti10kategori M04+all. Geometry mempertahankan CRS/akurasi/centerlines/stop-line/gate/clearance. Provenance observasi memerlukan sumber lapangan yang direview.

Importer CSV/JSON menyimpan raw immutable, normalized per-import, rejected, quality-flags, summary dan source SHA256. ID import tidak dapat ditimpa. QA menolak duplicateID/measurement, countnegatif, kelas invalid, timezone salah, nonfinite termasuk koordinat nested dan satuan queue yang salah. Outlier dicatat tanpa dibuang diam-diam. Aggregation menolak gap/overlap/splitting dan mempertahankan missing. OD dan turning balance tidak memaksakan keseimbangan palsu.

Demo QA:2accepted dan3rejected (duplikasi, countnegatif, offset salah); lihat `import-qa-demo.json`. Demo0 dan null dipertahankan berbeda. Tidak ada demo yang dipromosikan ke observed. Import hanya menyiapkan kandidat; review flags/mapping/provenance dan seleksi dataset sebelum memasukkan normalized observations yang disetujui. Tidak ada promosi otomatis atau tombol yang menyatakan empirical baseline aktif.

## Spatial mapping dan structural readiness

Mapping memakai location+direction+movement registry ke edge/lane/junction, proposed detector dan ODzone. Tidak memakai proximity snap. Ambiguitas menghasilkan kandidat dan NEEDS MANUAL REVIEW. DetectorID adalah rencana, bukan perangkat terpasang. Frontage tetap terpisah dari arterial, ODzone belum disahkan.

M05.1 crossing: empat endpoint bergeser sekitar1.6m, tujuh lane shapes hingga7.178m, sebagian lane sekitar0.10m. Audit M06 menemukan249external lanes<1m di seluruh jaringan; jumlah ini bukan jumlah lane perlintasan. Daftar persis tersimpan. Stop-line/storage belum diukur; queue/storage/spillback/railway-response tidak eligible untuk klaim empiris di lokasi tersebut sebelum review fisik. OD optimization tidak boleh menutupi geometri salah.

Vehicle access/heavy clearance tetap provisional, oversize tetap blocked; Strict station/branch connectivity belum lengkap. Directions/lane counts/turns masih berdasarkan referensi OSM dan policy sebelumnya, belum physical validation. Signal timing dan railway pilot tetap sintetis. M06 tidak mengubah koneksi, permission atau geometri demi skor.

## Baseline dan parameter registry

`baseline-2026.json` memisahkan network M051Provisional/hash, vehicle registry M04, demand/ODfixture, signal, railway, behavior, window dan observationdataset. Semua path referensi diperiksa tersedia. **2026 PROVISIONAL BASELINE** adalah konfigurasi awal; empirical.enabled=false.

Registry memisahkan parameter eligible, locked dan missing. Hanya count12–60 dan speedFactor0.6–1.2 dibuka untuk fixture; grid24/36/48×0.7/0.9/1.1. Bounds adalah envelope teknis uji kecil, bukan prior empiris Gedangan. Composition/OD/departures/turns belum eligible. Tau/minGap/accel/decel dan lateral behavior tidak diestimasi tanpa observasi yang mengidentifikasikannya. Signal cycle/offset, closure dan train-arrival yang dapat diukur harus menjadi measured boundary conditions.

## Objective functions dan synthetic recovery

Loss adalah rata-rata berbobot squared error yang dinormalisasi, dengan term terpisah untuk count/turn/TT/speed/queue/wait/rail closure ketika target tersedia. Missing evidence pada term yang diminta membuat evaluasi gagal. MAE,RMSE,bias, relative error dengan denominator max(abs(observed),1unit), serta empiricalCDF distance tersedia. GEH dibatasi pada hitungan kendaraan hourly yang kompatibel;15 mincount tidak otomatis dikalikan menjadi observedhour. Tidak ada threshold universal yang menjamin validitas.

Fixture: jalan lurus600 m, passenger,1lane,limit12 m/s,4.5 m car,Krauss,tau1.2,minGap2.5,accel2,decel4,sigma0.3,speedDev0. Departures seragam0–240 s;horizon600 s;step0.5 s;warmup0untuk fixture terbatas ini. Metrikcount adalah kendaraan selesai dalam horizon600 s, bukan flow kendaraan/jam. Seluruh kendaraan diminta harus arrived atau trial ditolak. Error-log teleport/collision/permission membuat trial gagal.

Search hanya menerima target metrics; hidden parameters disimpan terpisah untuk evaluasi software. Calibration seeds11/12, reserved holdout21/22. Fixtureholdout tidak pernah menjadi fieldholdout. Objective yang digunakan hanya count(scale36) dan travel-time(scale60s), bobot1:1. Closure null karena tidak ada rail. Turningcount pada fixture adalah arus lurus tunggal, bukan TMCsimpang. Tidak mengoptimasi tujuh parameter sekaligus tanpa data.

| Vehicle count | Speed factor | Normalized training loss |
|---:|---:|---:|
| 24 | 0.7 | 0.08890866 |
| 24 | 0.9 | 0.05555558 |
| 24 | 1.1 | 0.06812696 |
| 36 | 0.7 | 0.03336806 |
| 36 | 0.9 | 0.00000000 |
| 36 | 1.1 | 0.01266333 |
| 48 | 0.7 | 0.08893109 |
| 48 | 0.9 | 0.05555564 |
| 48 | 1.1 | 0.06820968 |

Best36/0.9, meanTT59.0138889s, trainingloss0; syntheticheldoutloss0. Seluruh36 kendaraan arrived per best run dan FCD aktual tersedia. Hasil identik di fixture ini tidak membuktikan robustness pada jaringan macet atau generalisasi tahun2030/2040.

Unit audit: versi diagnostikv1 sempat menamai stopped-vehicle count sebagai queue_lengths. Diperbaiki sebelum empirical use: runnerm06-2 memisahkan queue_counts(vehicles) dan queue_lengths(m,instantaneous stopped-front extent+4.5mbody). V1 disimpan sebagai diagnostic saja; current recovery/sensitivity memakaiv2. Di fixture, stoppeddeparture tunggal dapat menghasilkan1vehicle/4.5m; itu bukan bukti antrean kemacetan Gedangan. Tidak ada observed data yang terdampak. Lihat `unit-correction-audit.json`.

## Independent validation dan uncertainty

Framework split menyisihkan date/group sebelum fitting, melarang ID sama atau measurementfingerprint sama pada dua set. Empty fold ditolak. Empiricalgate memerlukan verified2026 records, structuralreview, independentobservations dan predeclared acceptancejustification/review. Gate tidak otomatis memberikan label calibrated.

**INDEPENDENT VALIDATION NOT POSSIBLE WITH AVAILABLE DATA.** Synthetic seeds21/22 hanya holdout software. Secant sensitivity di boundedgrid menghasilkan Jacobian count/TT tidak singular (-62.621528) sehingga dua parameter identifiable pada fixture/grid ini saja. Zero queue/spillback sensitivity tidak mengidentifikasi congested behavior. Seed min/max/mean tersimpan; bukan confidenceinterval untuk kekurangan data. OD, observationquality, crossinggeometry dan structuralconfounding tetap unknown/provisional. Tidak ada posterior atau empiricalCI yang dikarang.

## Signal, railway dan spillback

Interfaces menerima signalhead/phase/timing dan event warning/closure/approach/pass/clearance/reopen/release, chronology dan duration. Jadwal keberangkatan tidak sama dengan waktu palang tertutup. Sinkronisasi membutuhkan clockyangsama dan queue/roadrelease/phaseyangdiamati. Geometri crossing tetap provisional; tidak menganggap pilot mencakup seluruh operasi stasiun.

37 episode spillback model M05.1 (termasuk2 alias bukti;35 independen) tetap SIMULATED_RESULT. Matching mendukung location,affectededge,trigger,timeoverlap,uncertainty, onset/duration/recovery error dan one-to-onegreedynearest. Dengan observed[]:0 matched,37 unmatched simulated,0 unmatched observed. Tidak ada klaim detector terverifikasi lapangan. Tolerance5s adalah defaultdiagnostic, bukan universal acceptance.

## Performance, browser, regression dan reproducibility

Total76 proses SUMO aktual tersimpan: 38 correctedrunner (20target/search/holdoutunique+18freshreproduction) dan 38 legacydiagnosticv1. Cachedrepeat tidak dihitung sebagai eksekusi baru. Failed simulations=0; wallSUMO total=26.517s; CPU total=20.578s; peak sampled per-processRAM=25.71MiB. Counter Windows disampling sekitar20ms; peakbukan wholemachineRAM/VRAM. Tidak ada klaimGPUbenchmark.

Fresh independent search benar-benar dihentikan sesudah2candidate, dilanjutkan menjadi9; bestparameter sama. Seluruh atribut fisika tripinfo/FCD best run sama saat freshreplay; processheaders/path/whitespace dikecualikan dari digest. Networkfixturehash sebelum/sesudah rebuild sama. Completedcheckpoint idempotent. Input/config/networksignature mengunci resume; perubahan input harus memakai eksperimen versioned. 5661baselinehash lama tetap sama.

Final Python:182testsOK. TypeScriptnoEmit dan ViteproductionbuildPASS. Browserinternal desktop1920×1080/mobile390×844:5 tab masing-masing, nohorizontalpageoverflow,0 captured console errors/warnings; stationfrontage dan trialselector diuji; empiricalactiondisabled. Ini QA interaksi terbatas, bukan profiler jangka panjang. Browseraccess baru berfungsi setelah restart Codex; serverlokal dijalankan kembali. ViewerM051/source tetap utuh dan memakai port5180;M06port5181.

![Desktop Data Readiness](m06/browser-desktop.jpg)
![Survey mapping](m06/browser-survey.jpg)
![Synthetic recovery](m06/browser-recovery.jpg)
![Mobile](m06/browser-mobile.jpg)

## Technical acceptance — 17 kriteria

PASS berikut berarti kesiapan software/dataframework yang telah diuji, bukan validitas empiris Gedangan.

| No | Kriteria | Hasil |
|---:|---|---|
| 1 | Data inventory | PASS |
| 2 | Missing-data register | PASS |
| 3 | Six observation schemas | PASS |
| 4 | CSV/JSON ingestion and QA | PASS |
| 5 | Survey templates | PASS |
| 6 | Exact spatial mapping/manual review | PASS |
| 7 | Provisional baseline configuration | PASS |
| 8 | Structural blockers | PASS |
| 9 | Offline calibration engine | PASS |
| 10 | Synthetic recovery | PASS |
| 11 | Independent split framework | PASS |
| 12 | Sensitivity/uncertainty | PASS |
| 13 | Railway/signal interfaces | PASS |
| 14 | Internal browser QA | PASS |
| 15 | Full regression | PASS |
| 16 | Original source immutability | PASS |
| 17 | Reproducible rebuild | PASS |

## Empirical acceptance — 10 kriteria

Belum ada dataset yang memungkinkan penilaian empiris; semua kriteria di bawah menunggu bukti lapangan. Framework ketidakpastian tersedia tetapi empirical uncertainty belum dapat diestimasi.

| No | Kriteria | Hasil |
|---:|---|---|
| 1 | Verified observed traffic data | BLOCKED — DATA REQUIRED |
| 2 | Adequate temporal/spatial coverage | BLOCKED — DATA REQUIRED |
| 3 | Geometry fit for selected metric | BLOCKED — DATA REQUIRED |
| 4 | Measured controls/timing | BLOCKED — DATA REQUIRED |
| 5 | Empirical parameter basis | BLOCKED — DATA REQUIRED |
| 6 | Fitting to real observations | BLOCKED — DATA REQUIRED |
| 7 | Independent field validation | BLOCKED — DATA REQUIRED |
| 8 | Empirical uncertainty | BLOCKED — DATA REQUIRED |
| 9 | Unresolved field mismatches reviewed | BLOCKED — DATA REQUIRED |
| 10 | Reproducible empirical baseline | BLOCKED — DATA REQUIRED |

## Batas, isu terbuka dan kesiapan M07

Belum ada observations2026, independentholdout, verifiedOD/turn/composition, measuredcontrols, clearance/legalitasheavy atau physicalnetworkvalidation. Mapping rencana bukan persetujuan lokasi survei; geometri crossing/shortlanes menghalangi klaim queue/storage. Calibrationrunner saat ini sengaja terbatas pada isolatedfixture; adaptasi empiricalexperiment harus dilakukan setelah data/studyobjective/structuralreview, bukan langsung mengarahkan optimizer ke seluruh parameter Gedangan.

Sumber publik historis hanya referensi. Template dan importer tidak membuat data menjadi verified dengan sendirinya. Tidak ada synthetic measurement yang disebut pengukuran Gedangan. M07 **tidak dimulai** dan tetap membutuhkan persetujuan pengguna; untuk kajian empiris, data critical dan structuralreview di atas harus diselesaikan terlebih dahulu.
