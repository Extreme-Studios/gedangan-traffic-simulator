"""Evidence-gated M06 report/manifest. Never activates empirical calibration."""
import re,sys,platform
from pathlib import Path
from .m04_demand import ROOT,load,save,sha
from .m06_reproducibility import baseline_check
DOC=ROOT/'documentation/m06'
def main():
 regression=(DOC/'final-regression.txt').read_text(encoding='utf-8-sig')
 match=re.search(r'Ran (\d+) tests.*?\n\s*OK\s*$',regression,re.S)
 if not match:raise RuntimeError('Full successful regression evidence required')
 build=(DOC/'production-build.txt').read_text(encoding='utf-8-sig')
 if 'built in' not in build:raise RuntimeError('Successful production build evidence required')
 qa=load(DOC/'browser-qa.json')
 if len(qa['checks'])!=10 or any(c['scrollWidth']>c['width'] for c in qa['checks']) or qa['console']:raise RuntimeError('Browser QA incomplete or unresolved errors')
 protected=baseline_check();recovery=load(DOC/'synthetic-recovery.json');repro=load(DOC/'reproducibility.json');perf=load(DOC/'performance.json');unc=load(DOC/'uncertainty.json')
 assert recovery['technical_recovery_success'] and all(repro['repeat_best_physics_equal'].values())
 assert load(ROOT/'data/observations/m06/normalized/observations.json')==[], 'Review newly supplied observations before refreshing the zero-observation report'
 n=int(match[1]);technical=['Data inventory','Missing-data register','Six observation schemas','CSV/JSON ingestion and QA','Survey templates','Exact spatial mapping/manual review','Provisional baseline configuration','Structural blockers','Offline calibration engine','Synthetic recovery','Independent split framework','Sensitivity/uncertainty','Railway/signal interfaces','Internal browser QA','Full regression','Original source immutability','Reproducible rebuild']
 empirical=['Verified observed traffic data','Adequate temporal/spatial coverage','Geometry fit for selected metric','Measured controls/timing','Empirical parameter basis','Fitting to real observations','Independent field validation','Empirical uncertainty','Unresolved field mismatches reviewed','Reproducible empirical baseline']
 acceptance={'technical':[{'id':i+1,'criterion':v,'status':'PASS'} for i,v in enumerate(technical)],'empirical':[{'id':i+1,'criterion':v,'status':'BLOCKED — DATA REQUIRED'} for i,v in enumerate(empirical)]}
 save(DOC/'acceptance.json',acceptance)
 status={'technical_readiness':'PASS','empirical_baseline':'BLOCKED — DATA REQUIRED','empirical_phase':'BLOCKED — INSUFFICIENT OBSERVED DATA','observed_records':0,'baseline_year':2026,'M07_started':False,'regression_tests':n,'protected_baseline_files':protected}
 save(DOC/'status.json',status);save(ROOT/'frontend/public/m06/status.json',status)
 completeness='\n'.join(f"| {m['metric']} | {m.get('records_2026','—')} | {m['status']} | {m['priority']} |" for m in load(DOC/'missing-register.json'))
 sites='\n'.join(f"| {s['location_id']} | {s['direction']} | `{s['edge_id']}` |" for s in load(DOC/'survey-plan.json'))
 rows='\n'.join(f"| {t['parameters']['vehicle_count']} | {t['parameters']['speed_factor']} | {t['loss']:.8f} |" for t in recovery['trials'])
 criteria='\n'.join(f"| {v['id']} | {v['criterion']} | {v['status']} |" for v in acceptance['technical'])
 emprows='\n'.join(f"| {v['id']} | {v['criterion']} | {v['status']} |" for v in acceptance['empirical'])
 inv=load(DOC/'inventory.json');inventory='\n'.join(f'| {k} | {v} |' for k,v in inv['by_class'].items())
 report=f'''# MILESTONE 06 — Baseline 2026 Data Readiness & Calibration Lab

Tanggal pelaksanaan: 31 Oktober 2026, Asia/Jakarta. Lingkup hanya M06. M07 belum dimulai.

## Executive summary

**TECHNICAL READINESS: PASS. EMPIRICAL BASELINE: BLOCKED — DATA REQUIRED.**

Phase A dan B selesai untuk fondasi data dan pengujian software terbatas. Phase C **BLOCKED — INSUFFICIENT OBSERVED DATA**. Tidak ditemukan observasi lapangan Gedangan 2026 yang terverifikasi pada input lokal yang diaudit. Tidak ada observed values yang dibuat. Tahun konfigurasi 2026 bukan bukti baseline empiris.

SUMO lokal 1.28.0 benar-benar menjalankan fixture terisolasi 600 m. Bounded search menemukan hidden vehicle_count=36 dan speed_factor=0.9, loss training=0 dan holdout sintetis=0. Hasil ini hanya **SOFTWARE CALIBRATION TEST — NOT EMPIRICAL CALIBRATION**. Fixture bebas konflik ini tidak membuktikan perilaku mixed traffic, sinyal, palang, antrean macet, atau kondisi fisik Gedangan.

## Perlindungan sumber dan audit awal

Laporan M03, M04, M04.5, M05, M05.1, governance, konfigurasi, jaringan, registry dan keluaran aktual diperiksa. Baseline SHA256 merekam {protected} file sebelum M06; pemeriksaan akhir tidak menemukan perubahan. Arsip/jaringan lama tetap utuh. M06 menambah modul/konfigurasi/viewer sendiri; tidak membangun ulang geometri Gedangan. Initial regression:152 tests OK. Final regression:{n} tests OK, termasuk seluruh152 lama.

`baseline-sha256.json` adalah bukti per-file, bukan sekadar pernyataan berdasarkan laporan lama. `reproducibility.json` menyimpan verifikasi fresh SUMO dan checkpoint. `delivery-manifest.json` merekam source/config/input/output M06, versi runtime, seed, serta hash artefak.

## Inventory, provenance dan sumber publik

Inventaris lokal adalah triage berdasarkan jenis/asal file; label tidak menaikkan asumsi menjadi observasi. Metadata asli dan audit sumber tetap berwenang. Seluruh daftar berada di `inventory.json`.

| Kelas sumber lokal | File dalam triage |
|---|---:|
{inventory}

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
{completeness}

**CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION:** tally15menit per kelas/arah/gerakan pada koridor utama dua arah, simpang, frontage, feeder dan akses stasiun; OD/turn shares dengan metode yang dapat ditelusuri; travel-time per rute dengan sampel; panjang antrean meter dan count terpisah; signal-head/phase/cycle/offset aktual; warning/closure/train pass/clearance/reopen/release aktual; survei centerline, stop-line, gate, lane/storage dan clearance; hari/sesi independen yang dicadangkan sebelum fitting. Sumber harus menyertakan tanggal, lokasi, metode, uncertainty dan provenance yang dapat diverifikasi.

**IMPORTANT — IMPROVES CONFIDENCE:** pengulangan hari/cuaca, visibilitas, hambatan samping, event log dan hitung ganda independen. **OPTIONAL — FUTURE REFINEMENT:** trajectory lateral anonim yang berizin setelah data dasar memadai. Tidak ada jaminan validitas berdasarkan jumlah hari saja; cakupan harus dinilai terhadap tujuan studi.

## Survey methodology dan template

Tujuh lokasi di bawah adalah **rencana**, bukan titik observasi terverifikasi. `survey-plan.json` menyimpan lane/junction/source-way, alasan, kelas, metrik, metode, sesi, bias dan kejadian khusus. Usulan3hari kerja+1akhir pekan dengan sesi07–09/12–14/16–18 WIB harus dikonfirmasi melalui reconnaissance; belum ada klaim jam puncak.

| Lokasi rencana | Arah model | Edge model |
|---|---|---|
{sites}

Metode rinci pada `SURVEY_METHOD.md`: clock tersinkron, dua pencacah/checks, 15min tally, rute travel-time konsisten, definisi queue/body/batas visibilitas, event control/rail dan survei berwenang. Video hanya sah/berizin; minimalkan identitas; tidak scraping CCTV privat. Field mapping frontage dan OD tetap perlu review manual.

`data/templates/m06` menyediakan9CSV header-only,6JSON kosong per jenis observasi, registry provenance dan panduan10kelas M04. Workbook opsional `Gedangan_Survey_Forms.xlsx` mempunyai9sheet:8form kosong dan1panduan klasifikasi; panduan metodologi adalah dokumen ke10. Sel worksheet pengamatan tidak diisi angka sintetis. JSON/CSV dapat diimpor; workbook adalah form manual, bukan importer XLSX. Template arrays harus diisi sebelum import. Contoh DEMO_SYNTHETIC berada di folder terpisah.

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

Loss adalah rata-rata berbobot squared error yang dinormalisasi, dengan term terpisah untuk count/turn/TT/speed/queue/wait/rail closure ketika target tersedia. Missing evidence pada term yang diminta membuat evaluasi gagal. MAE,RMSE,bias, relative error dengan denominator max(abs(observed),1unit), serta empiricalCDF distance tersedia. GEH dibatasi pada hitungan kendaraan hourly yang kompatibel;15mincount tidak otomatis dikalikan menjadi observedhour. Tidak ada threshold universal yang menjamin validitas.

Fixture: jalan lurus600m, passenger,1lane,limit12m/s,4.5m car,Krauss,tau1.2,minGap2.5,accel2,decel4,sigma0.3,speedDev0. Departures seragam0–240s;horizon600s;step0.5s;warmup0untuk fixture terbatas ini. Metrikcount adalah kendaraan selesai dalam horizon600s, bukan flow kendaraan/jam. Seluruh kendaraan diminta harus arrived atau trial ditolak. Error-log teleport/collision/permission membuat trial gagal.

Search hanya menerima target metrics; hidden parameters disimpan terpisah untuk evaluasi software. Calibration seeds11/12, reserved holdout21/22. Fixtureholdout tidak pernah menjadi fieldholdout. Objective yang digunakan hanya count(scale36) dan travel-time(scale60s), bobot1:1. Closure null karena tidak ada rail. Turningcount pada fixture adalah arus lurus tunggal, bukan TMCsimpang. Tidak mengoptimasi tujuh parameter sekaligus tanpa data.

| Vehicle count | Speed factor | Normalized training loss |
|---:|---:|---:|
{rows}

Best36/0.9, meanTT59.0138889s, trainingloss0; syntheticheldoutloss0. Seluruh36kendaraan arrived per best run dan FCD aktual tersedia. Hasil identik di fixture ini tidak membuktikan robustness pada jaringan macet atau generalisasi tahun2030/2040.

Unit audit: versi diagnostikv1 sempat menamai stopped-vehicle count sebagai queue_lengths. Diperbaiki sebelum empirical use: runnerm06-2 memisahkan queue_counts(vehicles) dan queue_lengths(m,instantaneous stopped-front extent+4.5mbody). V1 disimpan sebagai diagnostic saja; current recovery/sensitivity memakaiv2. Di fixture, stoppeddeparture tunggal dapat menghasilkan1vehicle/4.5m; itu bukan bukti antrean kemacetan Gedangan. Tidak ada observed data yang terdampak. Lihat `unit-correction-audit.json`.

## Independent validation dan uncertainty

Framework split menyisihkan date/group sebelum fitting, melarang ID sama atau measurementfingerprint sama pada dua set. Empty fold ditolak. Empiricalgate memerlukan verified2026records, structuralreview, independentobservations dan predeclared acceptancejustification/review. Gate tidak otomatis memberikan label calibrated.

**INDEPENDENT VALIDATION NOT POSSIBLE WITH AVAILABLE DATA.** Synthetic seeds21/22 hanya holdout software. Secant sensitivity di boundedgrid menghasilkan Jacobian count/TT tidak singular ({unc['two_metric_jacobian_determinant']:.6f}) sehingga dua parameter identifiable pada fixture/grid ini saja. Zero queue/spillback sensitivity tidak mengidentifikasi congested behavior. Seed min/max/mean tersimpan; bukan confidenceinterval untuk kekurangan data. OD, observationquality, crossinggeometry dan structuralconfounding tetap unknown/provisional. Tidak ada posterior atau empiricalCI yang dikarang.

## Signal, railway dan spillback

Interfaces menerima signalhead/phase/timing dan event warning/closure/approach/pass/clearance/reopen/release, chronology dan duration. Jadwal keberangkatan tidak sama dengan waktu palang tertutup. Sinkronisasi membutuhkan clockyangsama dan queue/roadrelease/phaseyangdiamati. Geometri crossing tetap provisional; tidak menganggap pilot mencakup seluruh operasi stasiun.

37episode spillback model M05.1 (termasuk2alias bukti;35independen) tetap SIMULATED_RESULT. Matching mendukung location,affectededge,trigger,timeoverlap,uncertainty, onset/duration/recovery error dan one-to-onegreedynearest. Dengan observed[]:0matched,37unmatchedsimulated,0unmatchedobserved. Tidak ada klaim detector terverifikasi lapangan. Tolerance5s adalah defaultdiagnostic, bukan universal acceptance.

## Performance, browser, regression dan reproducibility

Total{perf['simulations']}proses SUMO aktual tersimpan: {perf['current_runner_simulations']} correctedrunner (20target/search/holdoutunique+18freshreproduction) dan {perf['retained_v1_diagnostics']}legacydiagnosticv1. Cachedrepeat tidak dihitung sebagai eksekusi baru. Failed simulations={perf['failed_simulations']}; wallSUMOtotal={perf['wall_seconds_total']:.3f}s; CPUtotal={perf['cpu_seconds_total']:.3f}s; peak sampled per-processRAM={perf['max_peak_working_set_bytes_sampled']/1048576:.2f}MiB. Counter Windows disampling sekitar20ms; peakbukan wholemachineRAM/VRAM. Tidak ada klaimGPUbenchmark.

Fresh independent search benar-benar dihentikan sesudah2candidate, dilanjutkan menjadi9; bestparameter sama. Seluruh atribut fisika tripinfo/FCD best run sama saat freshreplay; processheaders/path/whitespace dikecualikan dari digest. Networkfixturehash sebelum/sesudah rebuild sama. Completedcheckpoint idempotent. Input/config/networksignature mengunci resume; perubahan input harus memakai eksperimen versioned. {protected}baselinehash lama tetap sama.

Final Python:{n}testsOK. TypeScriptnoEmit dan ViteproductionbuildPASS. Browserinternal desktop1920×1080/mobile390×844:5tabmasing-masing, nohorizontalpageoverflow,0capturedconsoleerrors/warnings; stationfrontage dan trialselector diuji; empiricalactiondisabled. Ini QA interaksi terbatas, bukan profiler jangka panjang. Browseraccess baru berfungsi setelah restart Codex; serverlokal dijalankan kembali. ViewerM051/source tetap utuh dan memakai port5180;M06port5181.

![Desktop Data Readiness](m06/browser-desktop.jpg)
![Survey mapping](m06/browser-survey.jpg)
![Synthetic recovery](m06/browser-recovery.jpg)
![Mobile](m06/browser-mobile.jpg)

## Technical acceptance — 17 kriteria

PASS berikut berarti kesiapan software/dataframework yang telah diuji, bukan validitas empiris Gedangan.

| No | Kriteria | Hasil |
|---:|---|---|
{criteria}

## Empirical acceptance — 10 kriteria

Belum ada dataset yang memungkinkan penilaian empiris; semua kriteria di bawah menunggu bukti lapangan. Framework ketidakpastian tersedia tetapi empirical uncertainty belum dapat diestimasi.

| No | Kriteria | Hasil |
|---:|---|---|
{emprows}

## Batas, isu terbuka dan kesiapan M07

Belum ada observations2026, independentholdout, verifiedOD/turn/composition, measuredcontrols, clearance/legalitasheavy atau physicalnetworkvalidation. Mapping rencana bukan persetujuan lokasi survei; geometri crossing/shortlanes menghalangi klaim queue/storage. Calibrationrunner saat ini sengaja terbatas pada isolatedfixture; adaptasi empiricalexperiment harus dilakukan setelah data/studyobjective/structuralreview, bukan langsung mengarahkan optimizer ke seluruh parameter Gedangan.

Sumber publik historis hanya referensi. Template dan importer tidak membuat data menjadi verified dengan sendirinya. Tidak ada synthetic measurement yang disebut pengukuran Gedangan. M07 **tidak dimulai** dan tetap membutuhkan persetujuan pengguna; untuk kajian empiris, data critical dan structuralreview di atas harus diselesaikan terlebih dahulu.
'''
 # Keep generated prose readable without modifying code paths or source identifiers.
 for before,after in {'seluruh152':'seluruh 152','Initial regression:152':'Initial regression: 152','Final regression:':'Final regression: ','SUMOtotal':'SUMO total','CPUtotal':'CPU total','proses SUMO':' proses SUMO','external lanes':'external lanes','38legacy':'38 legacy','9candidate':'9 candidate','37episode':'37 episode','2alias':'2 alias','35independen':'35 independen','0matched':'0 matched','37unmatchedsimulated':'37 unmatched simulated','0unmatchedobserved':'0 unmatched observed','2026records':'2026 records','15min':'15 min','15menit':'15 menit','3hari':'3 hari','1akhir':'1 akhir','9CSV':'9 CSV','6JSON':'6 JSON','9sheet':'9 sheet','8form':'8 form','1panduan':'1 panduan','10kelas':'10 kelas','600m':'600 m','600s':'600 s','240s':'240 s','36kendaraan':'36 kendaraan','12m/s':'12 m/s','4.5m car':'4.5 m car','0.5s':'0.5 s','5tabmasing-masing':'5 tab masing-masing','0capturedconsoleerrors/warnings':'0 captured console errors/warnings','blocker':'blocker'}.items():report=report.replace(before,after)
 (ROOT/'documentation/MILESTONE_06_REPORT.md').write_text(report,encoding='utf-8')
 readme='''# M06 — cara menjalankan

Technical readiness PASS. Empirical baseline BLOCKED — DATA REQUIRED. M07 belum dimulai.

Jalankan dari root proyek Windows:

```bat
START_CALIBRATION_M06.bat
REBUILD_CALIBRATION_M06.bat
```

Viewer: http://127.0.0.1:5181/calibration.html. Server hanya127.0.0.1; viewer sebelumnya memakai port sendiri. Launcher start tidak mengubah data. Rebuild menjalankan isolated SUMO recovery/reproduction/sensitivity/export, seluruh regression, TypeScript dan productionbuild; tidak mengaktifkan empiricalcalibration atau mereset observations. Gunakan Python .venv lokal dan toolchain SUMO1.28.0 yang sudah tersedia; tidak menginstal paket atau membutuhkan akun cloud.

Data/template: `data/templates/m06/` (CSV header-only, JSONemptyarrays, XLSXformmanual). Metode: `documentation/m06/SURVEY_METHOD.md`. Isi ISOtimestamps dengan+07:00,timezoneAsia/Jakarta. Empty/NULL/MISSING tidak berubah menjadi0. Queue m terpisah dari vehiclecount. Jangan mengimpor panduan klasifikasi sebagai trafficcounts.

Contoh import demo terpisah (pakai ID baru setiap kali):

```bat
.venv\\Scripts\\python.exe -m backend.gedangan.m06_observations data/observations/m06/synthetic-demo/example.json --provenance data/observations/m06/synthetic-demo/provenance.json --import-id demo-review-02 --demo
```

Untuk CSV/JSON lapangan, ganti input/provenance, hapus --demo. ProvenanceJSON adalah mapping provenance_id ke metadata, bukan array registrytemplate. Fieldwajib:source_title,source_uri,license_notes,method,spatial_scope,accessed_on,source_class=OBSERVED_FIELD,field_evidence_verified=true hanya setelah review bukti nyata. Jangan mengisi flagverified tanpa bukti. Import menyimpan raw,normalized,rejected,qualityflags,summary/hash pada `data/observations/m06/imports/ID/`. Review semua flags,duplicate lintasimport,mapping dan provenance sebelum menyusun datasetobservasi yang disetujui; tidak ada automaticpromotion ke baseline.

Normalized approveddataset terpisah: `data/observations/m06/normalized/observations.json`. Sekarang[]; provenance{}. Syntheticdemo dan modeloutputs terpisah. Rebuild tidak mengganti dataset ini. `m06_data` adalah initializer/builder spesifikasi M06, bukan workflow memasukkan fielddata; jangan menjalankannya untuk mempromosikan observations. Data baru memerlukan pembaruan inventory/coverage/report secara sadar, structuralreview dan independentholdout; laporan otomatis menolak zero-observationreport jika dataset telah diisi.

Audit: `documentation/m06/{baseline-sha256,reproducibility,synthetic-recovery,unit-correction-audit,browser-qa,acceptance,delivery-manifest}.json`; actualSUMOinputs/FCD/tripinfo/processlogs: `simulation/runs/m06/`. V1diagnostic retained, correctedrunner=m06-2. Main checkpoint dapat diresume; inputmismatch ditolak. Untuk freshexperiment gunakan folderversionbaru melalui runner API, jangan hapus hasil lama. CPU/RAMcounter bukan wholemachinebenchmark.

Perintah manual:

```bat
.venv\\Scripts\\python.exe -m backend.gedangan.m06_calibration
.venv\\Scripts\\python.exe -m backend.gedangan.m06_reproducibility
.venv\\Scripts\\python.exe -m backend.gedangan.m06_uncertainty
.venv\\Scripts\\python.exe -m backend.gedangan.m06_reporting
.venv\\Scripts\\python.exe -m unittest discover -s tests -v
```

Laporan lengkap: `documentation/MILESTONE_06_REPORT.md`. Tidak ada fit kondisi Gedangan2026 atau klaim validasi lapangan. Criticaldata: counts+turn/composition/OD, matchedTT, meter/countqueue, measuredsignals/railclosure, surveyedgeometry/clearance, independentdays. M07 tetap menunggu persetujuan.
'''
 (ROOT/'documentation/MILESTONE_06_README.md').write_text(readme,encoding='utf-8')
 folders=['configuration/calibration-m06','data/templates/m06','data/observations/m06','simulation/runs/m06','frontend/src/m06','frontend/public/m06','tests/m06']
 paths=[p for f in folders for p in (ROOT/f).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
 paths += list((ROOT/'backend/gedangan').glob('m06_*.py'))
 paths += [ROOT/p for p in ['START_CALIBRATION_M06.bat','REBUILD_CALIBRATION_M06.bat','frontend/calibration.html','frontend/vite.calibration.config.ts','documentation/MILESTONE_06_REPORT.md','documentation/MILESTONE_06_README.md']]
 paths += [p for p in DOC.iterdir() if p.is_file() and p.name not in ['delivery-manifest.json','rebuild-execution.txt']]
 save(DOC/'delivery-manifest.json',{'label':'M06 SOFTWARE/DATA READINESS — NOT EMPIRICAL CALIBRATION','python':sys.version,'platform':platform.platform(),'sumo_version':'1.28.0','toolchain_sha256':{name:sha(ROOT/'toolchain/sumo-win64-1.28.0/bin'/name) for name in ['sumo.exe','netconvert.exe']},'python_executable_sha256':sha(Path(sys.executable)),'seeds':[11,12,21,22],'baseline_files_checked':protected,'files':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in paths}})
 print('M06 evidence-gated report written; technical PASS, empirical BLOCKED; tests',n)
if __name__=='__main__':main()
