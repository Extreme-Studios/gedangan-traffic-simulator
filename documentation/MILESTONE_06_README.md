# M06 — cara menjalankan

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
.venv\Scripts\python.exe -m backend.gedangan.m06_observations data/observations/m06/synthetic-demo/example.json --provenance data/observations/m06/synthetic-demo/provenance.json --import-id demo-review-02 --demo
```

Untuk CSV/JSON lapangan, ganti input/provenance, hapus --demo. ProvenanceJSON adalah mapping provenance_id ke metadata, bukan array registrytemplate. Fieldwajib:source_title,source_uri,license_notes,method,spatial_scope,accessed_on,source_class=OBSERVED_FIELD,field_evidence_verified=true hanya setelah review bukti nyata. Jangan mengisi flagverified tanpa bukti. Import menyimpan raw,normalized,rejected,qualityflags,summary/hash pada `data/observations/m06/imports/ID/`. Review semua flags,duplicate lintasimport,mapping dan provenance sebelum menyusun datasetobservasi yang disetujui; tidak ada automaticpromotion ke baseline.

Normalized approveddataset terpisah: `data/observations/m06/normalized/observations.json`. Sekarang[]; provenance{}. Syntheticdemo dan modeloutputs terpisah. Rebuild tidak mengganti dataset ini. `m06_data` adalah initializer/builder spesifikasi M06, bukan workflow memasukkan fielddata; jangan menjalankannya untuk mempromosikan observations. Data baru memerlukan pembaruan inventory/coverage/report secara sadar, structuralreview dan independentholdout; laporan otomatis menolak zero-observationreport jika dataset telah diisi.

Audit: `documentation/m06/{baseline-sha256,reproducibility,synthetic-recovery,unit-correction-audit,browser-qa,acceptance,delivery-manifest}.json`; actualSUMOinputs/FCD/tripinfo/processlogs: `simulation/runs/m06/`. V1diagnostic retained, correctedrunner=m06-2. Main checkpoint dapat diresume; inputmismatch ditolak. Untuk freshexperiment gunakan folderversionbaru melalui runner API, jangan hapus hasil lama. CPU/RAMcounter bukan wholemachinebenchmark.

Perintah manual:

```bat
.venv\Scripts\python.exe -m backend.gedangan.m06_calibration
.venv\Scripts\python.exe -m backend.gedangan.m06_reproducibility
.venv\Scripts\python.exe -m backend.gedangan.m06_uncertainty
.venv\Scripts\python.exe -m backend.gedangan.m06_reporting
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Laporan lengkap: `documentation/MILESTONE_06_REPORT.md`. Tidak ada fit kondisi Gedangan2026 atau klaim validasi lapangan. Criticaldata: counts+turn/composition/OD, matchedTT, meter/countqueue, measuredsignals/railclosure, surveyedgeometry/clearance, independentdays. M07 tetap menunggu persetujuan.
