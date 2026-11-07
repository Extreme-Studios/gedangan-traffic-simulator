# MILESTONE 08.5 — GEDANGAN TRAFFIC DIGITAL TWIN
## Field Survey Operations, Video-Assisted Traffic Counting & Evidence Capture System

**MODEL: GPT-6.1 SOL — MEDIUM**

Lanjutkan proyek Gedangan Traffic Simulator dari M01 sampai M08.

**KERJAKAN MILESTONE 08.5 SAJA. JANGAN MEMULAI M09.**

M08 telah menyelesaikan Solution Scenario Engine dengan 289 regression tests, 37 actual SUMO runs dan satu independent reproduction.

Namun, empirical baseline Gedangan 2026 masih belum terkalibrasi.

M06 sudah memiliki:
- Six observation schemas.
- CSV/JSON importer.
- Data quality validation.
- Seven planned survey locations.
- Nine CSV templates.
- Six JSON observation templates.
- Gedangan_Survey_Forms.xlsx.
- SURVEY_METHOD.md.
- Provenance registry.

Jangan membangun ulang semua pekerjaan tersebut.

**Tujuan M08.5 adalah mengubah fondasi survei M06 menjadi perangkat pengumpulan data lapangan yang praktis, offline, mudah dioperasikan dan langsung kompatibel dengan M06.**

Fokus utama:

1. Manual traffic counting.
2. Video-assisted traffic counting.
3. Vehicle classification.
4. Turning movement counting.
5. Queue measurement.
6. Travel time observation.
7. Traffic signal observation.
8. Railway crossing event recording.
9. Geometric field survey.
10. Data quality review dan export.

Semua hasil harus dapat ditelusuri sumbernya.

---

# 1. PROJECT DIRECTORY

Gunakan:

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

Audit sebelum implementasi:

- MILESTONE_06_REPORT.md.
- MILESTONE_07_REPORT.md.
- MILESTONE_08_REPORT.md.
- M06 SURVEY_METHOD.md.
- M06 survey-plan.json.
- M06 six observation schemas.
- M06 data/templates/m06.
- M06 CSV/JSON importer.
- M06 quality-control engine.
- M06 provenance registry.
- M08 scenario catalog.
- M08 browser.
- M08 network and geometry.
- Existing project governance.

Baca source code dan periksa implementasi aktual.

Buat baseline SHA-256 untuk seluruh source, configuration, dataset, simulation output dan report M01–M08.

Jangan mengubah file lama.

Semua implementasi baru harus berada pada namespace M08.5.

# 2. PROJECT OBJECTIVE

Bangun:

**GEDANGAN FIELD SURVEY & DATA ACQUISITION LAB**

Aplikasi lokal berbasis browser yang dapat dipakai untuk mengumpulkan data lalu lintas Gedangan menggunakan komputer atau laptop Windows.

Aplikasi harus bekerja offline.

Tidak boleh bergantung pada:
- Cloud database.
- Internet.
- Cloud AI.
- External API.
- CCTV online.
- Paid subscription.
- External authentication.

Gunakan backend dan frontend project yang sudah tersedia.

Data disimpan secara lokal dengan backup dan export yang dapat diverifikasi.

# 3. SURVEY LOCATION REGISTRY

Gunakan tujuh titik rencana M06.

Lokasi ini masih PLANNED dan harus melalui reconnaissance sebelum dipakai untuk survei sebenarnya.

| ID | Lokasi | Fokus |
|---|---|---|
| MAIN_NB | Sidoarjo → Surabaya | Arus utama |
| MAIN_SB | Surabaya → Sidoarjo | Arus sebaliknya |
| GEDANGAN_FEEDER | Feeder Gedangan | Kendaraan masuk/keluar |
| FRONTAGE | Frontage road | Arus frontage |
| KETAJEN | Kawasan Ketajen | Pergerakan lokal |
| STATION_CROSSING | Perlintasan kereta | Interaksi kereta dan jalan |
| UPSTREAM_STORAGE | Hulu simpang | Panjang antrean |

Gunakan mapping kandidat M06:

- MAIN_NB: `w562358500_s16_p0_0_f`
- MAIN_SB: `w512351908_s4_p0_0_f`
- GEDANGAN_FEEDER: `w266287930_s0_p0_0_f`
- FRONTAGE: `w1118947356_s0_p0_0_f`
- KETAJEN: `w1240685448_s1_p2_0_f`
- STATION_CROSSING: `w1240685448_s1_p2_0_r`
- UPSTREAM_STORAGE: `w512351908_s3_p0_0_f`

Jangan menganggap mapping tersebut sebagai posisi kamera atau titik survei fisik yang sudah disahkan.

Sediakan fungsi:
- Open location on map.
- Show associated SUMO edge.
- View source geometry.
- Field coordinate input.
- Camera position.
- Observation direction.
- Visibility assessment.
- Lane coverage.
- Field notes.
- Survey approval status.

Status:
- PLANNED.
- NEEDS_RECONNAISSANCE.
- FIELD_VERIFIED.
- APPROVED_FOR_SURVEY.
- INACTIVE.

Jangan mengaktifkan FIELD_VERIFIED tanpa konfirmasi pengukuran atau pemeriksaan lapangan.

# 4. FIELD RECONNAISSANCE

Buat fitur reconnaissance sebelum survei.

Petugas dapat mencatat:

- Titik pengamatan.
- Posisi observer.
- Posisi kamera.
- Arah kamera.
- Jumlah lajur terlihat.
- Jalur belok yang terlihat.
- Hambatan visual.
- Pohon/bangunan/kendaraan yang menghalangi.
- Kemampuan membaca pergerakan kendaraan.
- Titik antrean maksimum yang dapat terlihat.
- Railway visibility.
- Signal head visibility.
- Kondisi pencahayaan.
- Safe observer position.
- Legal recording permission.
- Foto dokumentasi jika diizinkan.
- Catatan tambahan.

Bila kamera tidak dapat melihat seluruh pergerakan, jangan mengklaim satu video cukup untuk menghitung seluruh simpang.

Sediakan rekomendasi kebutuhan beberapa kamera/observer berdasarkan coverage yang benar-benar teridentifikasi.

Jangan menentukan posisi kamera berdasarkan koordinat tebakan.

# 5. MANUAL TRAFFIC COUNTING

Buat modul manual counting yang sederhana dan cepat.

Operator memilih:

- Survey location.
- Date.
- Session.
- Direction.
- Approach.
- Movement.
- Vehicle class.

Gunakan sepuluh kategori kendaraan M04:

1. Motorcycle.
2. Passenger car.
3. Pickup/van.
4. Minibus/public transport.
5. Bus.
6. Light truck.
7. Medium truck.
8. Heavy truck.
9. Trailer/container.
10. Oversize/special.

Buat tombol besar untuk setiap kategori kendaraan.

Sediakan keyboard shortcuts agar penghitungan cepat.

Contoh:
- Tombol untuk motor.
- Tombol untuk mobil.
- Tombol untuk pickup.
- Tombol untuk bus.
- Tombol untuk truk.
- Tombol untuk setiap gerakan belok/lurus.

Operator dapat mengubah shortcut.

Setiap input menyimpan:
- Timestamp.
- Survey ID.
- Location.
- Approach.
- Direction.
- Turning movement.
- Vehicle class.
- Observer ID.
- Observation method.
- Quality flag.

Interval default:
**15 menit.**

Tampilkan live counter:
- Current 15-minute interval.
- Total per vehicle class.
- Total per movement.
- Total per direction.
- Total per location.

Sediakan:
- Undo last count.
- Edit record.
- Mark duplicate.
- Pause.
- Resume.
- Add field note.
- Mark incident.
- Save checkpoint.

Jangan mengubah count nol menjadi missing atau sebaliknya.

Setiap sesi harus memiliki timestamp yang eksplisit dengan timezone Asia/Jakarta.

# 6. VIDEO-ASSISTED TRAFFIC COUNTING

Ini salah satu fitur terpenting M08.5.

Bangun video review dan annotation workstation.

Operator dapat memilih file video lokal dari komputer.

Format yang perlu didukung mengikuti kemampuan browser lokal, minimal MP4 yang kompatibel.

Jangan mengupload video ke cloud.

## Video Player

Fitur:
- Play/pause.
- Frame forward.
- Frame backward.
- Playback 0.25×.
- Playback 0.5×.
- Playback 1×.
- Playback 2×.
- Timeline scrubbing.
- Current timestamp.
- Video duration.
- Fullscreen.
- Zoom jika memungkinkan.
- Keyboard shortcuts.

## Annotation Panel

Saat video berjalan atau dijeda, operator dapat mencatat kendaraan:

- Vehicle class.
- Direction.
- Approach.
- Turning movement.
- Lane group.
- Timestamp.
- Confidence.
- Notes.

Setiap kendaraan yang dihitung mempunyai event ID unik.

Jangan menghitung ulang kendaraan yang sama akibat:
- Rewind.
- Playback ulang.
- Frame stepping.
- Perubahan kecepatan playback.

Sediakan annotation ledger agar operator dapat mengoreksi atau menghapus record secara terkontrol.

## Video Time Mapping

Simpan:
- Original video filename.
- File SHA-256.
- Video duration.
- Frame rate jika tersedia.
- Recording timestamp jika tersedia.
- Timezone.
- Survey location.
- Camera ID.
- Offset video terhadap jam observasi.
- Observer.
- Annotation session.

Jika timestamp perekaman tidak diketahui, jangan mengarang waktu aktual.

Tandai sebagai VIDEO_TIME_ONLY.

## Manual Review

Sediakan:
- Per-interval annotation.
- Per-class count.
- Per-movement count.
- Per-lane count.
- Annotation progress.
- Unreviewed interval.
- Review discrepancy.

Hasil video counting harus bisa dibandingkan dengan manual counting.

Jangan menyebut hasil video sebagai automatic traffic detection jika sebenarnya dicatat manual.

## Optional Local Computer Vision

Jika model object detection lokal sudah tersedia, Codex boleh membuat adapter eksperimental.

Tetapi:
- Jangan mengunduh model secara otomatis.
- Jangan membutuhkan GPU NVIDIA.
- Jangan menganggap AMD GPU mendukung setiap backend.
- Jangan menambahkan dependency berat tanpa kebutuhan.
- Jangan menjadikan deteksi otomatis sebagai sumber resmi.
- Setiap hasil deteksi harus diverifikasi manusia.
- Confidence threshold harus dapat dikonfigurasi.
- False positive/false negative harus dicatat.

Jika tidak ada model lokal, video annotation manual harus tetap berfungsi penuh.

Jangan membuat klaim AI counting yang tidak benar-benar diimplementasikan.

# 7. TURNING MOVEMENT COUNTING

Buat mode khusus untuk perempatan.

Tampilkan diagram pergerakan simpang berdasarkan geometri M02/M03 yang tersedia.

Operator memilih:
- Approach.
- Straight.
- Left turn.
- Right turn.
- Other/legal movement jika ada.

Hubungkan dengan lane/edge kandidat M06.

Jangan mengasumsikan jumlah lajur atau gerakan fisik dari gambar OSM saja.

Jika geometri gerakan tidak jelas:
**NEEDS FIELD VERIFICATION**.

Tampilkan:
- Total per approach.
- Total per movement.
- Vehicle class breakdown.
- Interval comparison.
- Missing movement data.

Jangan memaksakan turning count balance.

Selisih pencatatan harus ditampilkan sebagai discrepancy.

# 8. QUEUE MEASUREMENT

Bangun queue observation tool.

Operator dapat mencatat:

- Timestamp.
- Location.
- Approach.
- Lane group.
- Queue vehicle count.
- Queue length in meters.
- Maximum visible queue extent.
- Queue start.
- Queue tail.
- Duration.
- Vehicle composition.
- Boundary censoring.
- Measurement method.
- Confidence.

Pisahkan:
- Queue vehicle count.
- Queue length.
- Queue duration.

Jangan mencampur satuan.

Sediakan video frame annotation untuk menandai:
- Stop line.
- First stopped vehicle.
- Rear-most stopped vehicle.
- Queue tail.
- Spillback candidate.

Panjang antrean harus mempunyai dasar pengukuran:
- Surveyed reference distance.
- Verified road markings.
- Measured landmarks.
- Approved geometry.

Jika tidak tersedia, catat:
**LENGTH NOT MEASURED**.

Jangan mengubah estimasi visual menjadi ukuran meter yang seolah-olah akurat.

Boundary-censored queues wajib ditandai.

# 9. TRAVEL TIME OBSERVATION

Buat modul travel time survey.

Dukung:
- Origin.
- Destination.
- Corridor.
- Vehicle class.
- Start timestamp.
- End timestamp.
- Travel duration.
- Sample ID.
- Observation method.
- Observer.
- Route.
- Quality.

Metode yang dapat digunakan:
- Authorized probe vehicle.
- GPS logger lokal.
- Two-observer anonymous timestamp matching.

Jangan memakai pelat nomor atau pengenalan wajah untuk identifikasi kendaraan.

Jika menggunakan dua observer, gunakan temporary anonymous sample token.

Simpan jumlah sampel dan ketidakpastian.

Jangan menggabungkan rute yang berbeda menjadi satu rata-rata.

# 10. TRAFFIC SIGNAL OBSERVATION

Bangun signal event recorder.

Catat:
- Signal group.
- Approach.
- Phase.
- Green start/end.
- Yellow start/end.
- Red start/end.
- Cycle time.
- Offset jika dapat diamati.
- Date.
- Time.
- Source.
- Observer.
- Confidence.

Sediakan stopwatch dan video-assisted phase annotation.

Jangan menganggap konfigurasi sinyal M05 sebagai program lampu aktual Gedangan.

Jika warna signal head tidak dapat terlihat, tandai missing.

Simpan seluruh siklus yang diamati.

# 11. RAILWAY CROSSING OBSERVATION

Buat railway event recorder khusus perlintasan.

Setiap event memiliki timestamp tersendiri:

1. Warning starts.
2. Barrier begins closing.
3. Road fully closed.
4. Train approaches.
5. Train arrives.
6. Train passes.
7. Train clears.
8. Barrier begins reopening.
9. Barrier fully opens.
10. Road traffic released.

Jangan menyamakan waktu keberangkatan kereta dengan waktu penutupan palang.

Jangan menyamakan waktu kereta lewat dengan waktu jalan kembali dibuka.

Sediakan:
- Event timeline.
- Video annotation.
- Multiple train movement support.
- Multiple closure events.
- Event duration.
- Uncertainty.
- Observer notes.

Hasilnya harus kompatibel dengan M06 railway observation schema.

# 12. GEOMETRIC FIELD SURVEY

Buat modul pencatatan geometri lapangan.

Prioritaskan:
- Road centerline.
- Lane width.
- Number of lanes.
- Stop line.
- Barrier position.
- Rail centerline.
- Track count.
- Crossing angle.
- Storage length.
- Junction boundary.
- Clearance.
- Roadside access.
- Ramp/access candidates.

Setiap pengukuran wajib memiliki:
- Coordinates.
- CRS.
- Units.
- Instrument.
- Measurement method.
- Survey accuracy.
- Observer.
- Date.
- Source.
- Quality.

Sediakan import data dari pengukuran GNSS atau dokumen survei yang diizinkan jika formatnya kompatibel.

Jangan membuat geometri baru dari asumsi visual.

Jangan melakukan pengukuran di jalur rel atau badan jalan aktif tanpa izin dan prosedur keselamatan yang sesuai.

# 13. SURVEY SESSION PLANNER

Gunakan rancangan M06 sebagai starting point:

- Tiga hari kerja.
- Satu hari akhir pekan.
- Sesi pagi 07.00–09.00.
- Sesi siang 12.00–14.00.
- Sesi sore 16.00–18.00.

Ini adalah jadwal usulan, bukan fakta jam puncak.

Buat planner yang memungkinkan perubahan:
- Date.
- Start/end.
- Location.
- Observer.
- Camera.
- Survey type.
- Status.
- Notes.

Sediakan status:
- PLANNED.
- RECONNAISSANCE.
- READY.
- IN_PROGRESS.
- COMPLETED.
- NEEDS_REVIEW.
- APPROVED.

Jangan menetapkan peak hour otomatis sebelum data tersedia.

# 14. OBSERVER QUALITY CONTROL

Sediakan:
- Observer registry.
- Observer training checklist.
- Independent double count.
- Inter-observer comparison.
- Video review verification.
- Discrepancy register.
- Adjudication.
- Audit trail.

Pada subset sesi, dua observer harus dapat menghitung sampel yang sama secara independen.

Hitung:
- Absolute count difference.
- Relative difference.
- Agreement by class.
- Agreement by movement.
- Agreement by interval.

Jangan menganggap satu angka agreement sebagai standar universal.

Threshold review harus dapat dikonfigurasi dan dijelaskan.

Jangan otomatis merata-ratakan hasil dua observer yang berbeda.

Semua discrepancy harus dapat ditelusuri dan diselesaikan oleh reviewer.

# 15. DATA QUALITY & PROVENANCE

Gunakan schema M06 sebagai kontrak utama.

Jangan membuat schema observasi baru yang tidak kompatibel.

Setiap dataset harus mempunyai:
- Dataset ID.
- Survey ID.
- Observation ID.
- Location ID.
- Source type.
- Original file hash.
- Observer.
- Recording method.
- Date/time.
- Timezone.
- Spatial mapping.
- Confidence.
- Review status.
- Provenance.
- Version.

Source classification:
- OBSERVED_FIELD.
- VIDEO_OBSERVATION.
- OFFICIAL_ADMINISTRATIVE.
- PUBLISHED_RESEARCH.
- ENGINEERING_REFERENCE.
- ASSUMPTION.
- SYNTHETIC_TEST.
- SIMULATED_RESULT.
- MISSING.

VIDEO_OBSERVATION baru dapat dipromosikan ke approved observation setelah human review.

Raw observation harus immutable.

Jangan mengubah:
- NULL menjadi 0.
- Missing menjadi 0.
- Unreviewed menjadi approved.
- Synthetic menjadi observed.

# 16. PRIVACY & FIELD SAFETY

Patuhi:
- Hanya merekam pada lokasi yang sah dan aman.
- Dapatkan izin yang diperlukan.
- Jangan menggunakan CCTV privat tanpa izin.
- Jangan mengakses railway right-of-way tanpa izin.
- Jangan menghalangi lalu lintas.
- Jangan merekam identitas pribadi yang tidak diperlukan.
- Jangan membuat fitur facial recognition.
- Jangan membuat fitur automatic license plate recognition.
- Jangan menyimpan data identitas pengemudi.

Video asli tetap berada di penyimpanan lokal.

Database survei hanya menyimpan referensi file, hash, metadata dan anotasi yang diperlukan.

Sediakan retention policy dan opsi penghapusan rekaman sesuai izin dan kebutuhan dokumentasi.

# 17. M06 INTEGRATION

Ini persyaratan kritis.

M08.5 harus mengeluarkan data yang dapat langsung diproses importer M06.

Gunakan:
- Existing six schemas.
- Existing CSV headers.
- Existing JSON structures.
- Existing provenance registry.
- Existing quality validation.

Sediakan:
- Export CSV.
- Export JSON.
- Export survey package.
- Import preview.
- Validation preview.
- Accepted records.
- Rejected records.
- Quality flags.
- Source hashes.

Workbook M06 tetap dapat digunakan sebagai formulir manual.

Tidak perlu membangun XLSX importer baru kecuali ada alasan teknis yang jelas.

Pastikan data dari M08.5 dapat melewati M06 importer tanpa kehilangan:
- Timestamp.
- Vehicle class.
- Direction.
- Movement.
- Units.
- Source.
- Confidence.
- Missing/null semantics.

Data yang berhasil diimpor belum otomatis menjadi empirical baseline.

Tetap diperlukan review dan persetujuan dataset.

# 18. OFFLINE BROWSER WORKBENCH

Buat halaman baru:

**GEDANGAN FIELD SURVEY WORKBENCH**

Gunakan internal browser Codex sebagai preview utama.

Sediakan menu:

A. Survey Dashboard.

B. Location Reconnaissance.

C. Manual Traffic Counter.

D. Video Annotation.

E. Turning Movement Counter.

F. Queue Measurement.

G. Travel Time Survey.

H. Traffic Signal Recorder.

I. Railway Crossing Recorder.

J. Geometry Survey.

K. Survey Session Planner.

L. Observer Quality Control.

M. Data Validation & Export.

Tampilan harus:
- Profesional.
- Ringkas.
- Cepat digunakan.
- Mudah dibaca.
- Tombol counter besar.
- Cocok untuk layar laptop 1080p.
- Responsif untuk tablet/mobile.

Manual counter harus mudah digunakan tanpa keyboard jika operator memakai layar sentuh.

Video annotation harus dapat bekerja dengan file video lokal.

Sediakan save checkpoint agar sesi tidak hilang ketika browser ditutup.

Tampilkan:
- Unsaved changes.
- Last saved.
- Current session.
- Active observer.
- Current interval.
- Data quality warning.

Jangan membuat dummy data terlihat sebagai observasi aktual.

Demo UI harus mempunyai watermark:
**DEMO SYNTHETIC — NOT OBSERVED GEDANGAN TRAFFIC.**

# 19. LOCAL STORAGE & BACKUP

Sediakan penyimpanan lokal yang andal.

Gunakan mekanisme backend/local database yang sesuai arsitektur proyek.

Fitur:
- Autosave.
- Manual checkpoint.
- Backup.
- Restore.
- Export.
- Source hash.
- Session recovery.
- Duplicate prevention.
- Transaction-safe import.

Jangan mengandalkan browser memory saja untuk menyimpan ribuan annotation events.

Jika local storage tidak tersedia, tampilkan error yang jelas.

# 20. PERFORMANCE

Target:
- Windows 11.
- RAM 16GB.
- AMD GPU 6GB VRAM.
- 1080p.
- Offline operation.

Jangan memuat seluruh video ke RAM.

Gunakan streaming playback dari file lokal dan pagination annotation.

Jangan membuat background AI detection yang membebani sistem.

Jangan memerlukan GPU untuk manual counting.

Jangan menginstal dependency berat jika tidak diperlukan.

# 21. FILE STRUCTURE

Sesuaikan dengan struktur proyek aktual.

Usulan:

`backend/gedangan/m085_survey.py`

`backend/gedangan/m085_video_annotation.py`

`backend/gedangan/m085_observer_qc.py`

`backend/gedangan/m085_provenance.py`

`backend/gedangan/m085_export.py`

`configuration/survey-m085/`

`data/surveys/m085/`

`data/survey-media/`

`data/templates/m085/`

`documentation/m085/`

`frontend/survey.html`

`frontend/src/m085/`

`tests/m085/`

Buat:

`START_SURVEY_M085.bat`

`REBUILD_SURVEY_M085.bat`

Gunakan port terpisah.

Jangan mengganggu M06 Calibration Lab atau M08 Solution Lab.

# 22. TESTING

Pertahankan seluruh 289 regression tests M08.

Tambahkan pengujian untuk:

1. Survey schema compatibility.
2. Manual counter.
3. Keyboard shortcuts.
4. Undo/edit.
5. Interval boundaries.
6. Timezone.
7. Video time mapping.
8. Duplicate annotations.
9. Video playback timestamp.
10. Video file hash.
11. Vehicle classification.
12. Turning movement.
13. Queue count versus queue length.
14. Boundary censoring.
15. Travel time calculation.
16. Signal event sequence.
17. Railway event sequence.
18. Geometry units and CRS.
19. Observer comparison.
20. Discrepancy review.
21. Null versus zero.
22. Raw immutability.
23. Provenance.
24. M06 CSV export.
25. M06 JSON export.
26. M06 importer round-trip.
27. Rejected-record preservation.
28. Backup and restore.
29. Session recovery.
30. Offline functionality.
31. Privacy safeguards.
32. Browser desktop QA.
33. Browser mobile/tablet QA.
34. Existing M01–M08 regression.

Gunakan fixture sintetis terpisah untuk pengujian.

Jangan memasukkan fixture ke folder OBSERVED_FIELD.

# 23. ACCEPTANCE CRITERIA

M08.5 technical readiness PASS apabila:

1. Seluruh M06 survey assets berhasil diaudit.
2. Tujuh planned locations tersedia.
3. Reconnaissance module berfungsi.
4. Manual traffic counter berfungsi.
5. Video annotation berfungsi.
6. Duplicate counting dapat dicegah dan diaudit.
7. Turning movement counter berfungsi.
8. Queue measurement berfungsi.
9. Travel time module berfungsi.
10. Signal recorder berfungsi.
11. Railway event recorder berfungsi.
12. Geometry survey module berfungsi.
13. Session planner berfungsi.
14. Observer quality control berfungsi.
15. M06 CSV export kompatibel.
16. M06 JSON export kompatibel.
17. Data provenance lengkap.
18. Offline mode lulus.
19. Backup/restore lulus.
20. Browser QA desktop/mobile lulus.
21. Seluruh regression tests lulus.
22. Source M01–M08 tidak berubah.
23. Rebuild reproducible.

# 24. EMPIRICAL STATUS GATE

M08.5 tidak bertugas melakukan kalibrasi empiris.

Jika belum ada data lapangan, tampilkan:

**FIELD DATA COLLECTION SYSTEM: TECHNICAL READY**

**OBSERVED GEDANGAN DATA: NOT YET COLLECTED**

**EMPIRICAL BASELINE 2026: BLOCKED — DATA REQUIRED**

Jangan membuat data pengamatan otomatis.

Jangan mengubah data demo menjadi data lapangan.

Jangan menjalankan optimizer M06 untuk mengklaim baseline Gedangan terkalibrasi.

Jangan mengubah status M08 atau M06.

# 25. FINAL REPORT

Buat:

`MILESTONE_08_5_REPORT.md`

`MILESTONE_08_5_README.md`

Laporan harus mencakup:

1. Executive summary.
2. M06 assets audit.
3. Survey location registry.
4. Reconnaissance system.
5. Manual counter.
6. Video annotation.
7. Turning movement counting.
8. Queue measurement.
9. Travel time observation.
10. Signal recording.
11. Railway recording.
12. Geometry survey.
13. Session planner.
14. Observer quality control.
15. Privacy and safety.
16. M06 integration.
17. CSV/JSON compatibility.
18. Offline browser QA.
19. Backup and recovery.
20. Performance.
21. Regression tests.
22. Reproducibility.
23. Screenshots.
24. Remaining limitations.
25. Field deployment checklist.
26. M09 readiness.

Sertakan panduan operasional singkat:

**Bagaimana pengguna melakukan survei pertama di Perempatan Gedangan dari persiapan sampai data siap diimpor ke M06.**

Buat checklist yang dapat dicetak atau dibuka dari browser.

# 26. M09 READINESS

M09 baru dapat dimulai setelah pengguna mempunyai data lapangan atau sumber observasi yang dapat diverifikasi.

M08.5 harus menjelaskan data yang masih perlu dikumpulkan:

CRITICAL:
- Traffic count 15 menit per kelas/arah.
- Turning movement.
- OD.
- Travel time.
- Queue length.
- Signal timing.
- Railway crossing events.
- Geometry dan stop line.
- Independent validation observations.

IMPORTANT:
- Pengulangan sesi.
- Cuaca.
- Hambatan samping.
- Observer agreement.
- Visibility.

OPTIONAL:
- Anonymous lateral trajectory.
- Detailed vehicle behavior observations.

Jangan mengklaim bahwa empat hari pengamatan otomatis cukup untuk seluruh kebutuhan penelitian. Kecukupan data harus dinilai berdasarkan cakupan spasial, temporal, variasi kondisi dan tujuan simulasi.

**JANGAN MEMULAI M09.**

# 27. FINAL EXECUTION RULES

- Gunakan folder proyek yang sama.
- Audit sebelum implementasi.
- Reuse M06.
- Jangan mengulang M08.
- Jangan mengubah source lama.
- Jangan mengunduh model AI secara otomatis.
- Jangan mengarang lokasi kamera.
- Jangan mengarang data survei.
- Jangan menggunakan CCTV tanpa izin.
- Jangan mengklaim video annotation sebagai AI detection.
- Jangan mempromosikan data tanpa review.
- Gunakan internal browser.
- Simpan semua evidence.
- Jalankan full regression.
- Jika ada kegagalan, cari akar masalah sebelum mengulang.
- Jangan menghabiskan usage untuk mengerjakan ulang komponen yang sudah berfungsi.

**MULAI MILESTONE 08.5 SEKARANG.**

Prioritas tertinggi:

1. Field-ready survey system.
2. Manual dan video-assisted counting.
3. Data quality dan observer verification.
4. Direct compatibility dengan M06.
5. Offline operation.
6. Persiapan pengumpulan data nyata Gedangan.

Hasil akhir harus membuat pengguna bisa membawa laptop, menyiapkan rekaman video yang sah, melakukan pencatatan lalu lintas, memeriksa hasilnya, dan mengekspor data untuk proses kalibrasi berikutnya.

**TUJUAN: ketika M09 dimulai, kita tidak lagi sibuk membangun alat survei. Kita sudah siap bekerja dengan data lalu lintas Gedangan yang benar-benar dikumpulkan.**