# MILESTONE 06 — GEDANGAN TRAFFIC SIMULATOR
## 2026 Baseline Data Readiness, Calibration Engine & Independent Validation

**MODEL: GPT-6.1 SOL — MEDIUM**

Lanjutkan proyek Gedangan Traffic Simulator dari Milestone 01 hingga Milestone 05.1.

Kerjakan **MILESTONE 06 SAJA**.

Jangan melanjutkan Milestone 07 sebelum ada persetujuan pengguna.

Prioritas tertinggi M06 adalah integritas data, validitas ilmiah, dan kesiapan kalibrasi kondisi Gedangan tahun 2026.

**ATURAN MUTLAK: JANGAN MENGARANG DATA LALU LINTAS, MENGKLAIM KALIBRASI TANPA PENGAMATAN, ATAU MENGUBAH PARAMETER HANYA AGAR GRAFIK TERLIHAT COCOK.**

---

# 1. PROJECT DIRECTORY

Gunakan:

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

Sebelum mulai, periksa laporan, konfigurasi, dan implementasi aktual dari:

- MILESTONE_03_REPORT.md
- MILESTONE_04_REPORT.md
- MILESTONE_04_5_REPORT.md
- MILESTONE_05_REPORT.md
- MILESTONE_05_1_REPORT.md
- Dokumen governance dan arsitektur.
- Jaringan M03 dan corrected M04.5.
- Railway/signal network M05.
- M05.1 geometry audit.
- M05.1 spillback causal events.
- M04 vehicle registry dan OD schema.
- Semua data OBSERVED yang benar-benar sudah ada.
- Semua baseline manifests dan regression tests.

Periksa file aktual, jangan hanya mengandalkan laporan sebelumnya.

Pastikan seluruh source dan output lama tetap terlindungi.

Jangan menggunakan data sintetis M04/M05 sebagai pengganti data pengamatan nyata.

# 2. KONDISI AWAL DAN BATAS MODEL

M05.1 dilaporkan memiliki 152 automated tests lulus.

Fondasi yang sudah tersedia:
- Geospatial road network.
- SUMO network Strict/Provisional.
- Multiclass vehicle system.
- OD Matrix.
- Synthetic demand generator.
- Traffic signals.
- Railway crossing pilot.
- Motorcycle sublane experiment.
- Queue measurement.
- Spillback causal detector.
- Recorded traffic visualization.

Masalah terbuka:
- Volume aktual 2026 belum tersedia.
- OD aktual belum tersedia.
- Turning movement counts belum tersedia.
- Traffic composition belum terukur.
- Signal timing aktual belum terukur.
- Railway crossing closures belum terukur.
- Travel time dan queue length belum terukur.
- Geometri stop line dan perlintasan belum divalidasi lapangan.
- Legalitas dan swept path kendaraan berat belum tervalidasi.
- Beberapa ruas dan koneksi Strict belum lengkap.

Geometri perlintasan juga mempunyai perubahan lokal yang terukur dari M05:
- Sekitar 1,6 meter pada empat endpoint.
- Hingga 7,178 meter pada tujuh lane shapes.
- Beberapa lane model menjadi sangat pendek, sekitar 0,10 meter.

Temuan ini harus tetap menjadi uncertainty/validation blockers.

Jangan menyatakan jaringan telah tervalidasi secara fisik.

# 3. STRATEGI MILESTONE 6 — DATA-FIRST

Bagi pekerjaan menjadi tiga fase:

## PHASE A — DATA READINESS

Dapat dikerjakan tanpa data lapangan lengkap.

Hasil:
- Data inventory.
- Data quality audit.
- Source provenance.
- Data collection templates.
- Observation schema.
- Spatial observation mapping.
- Coverage analysis.
- Missing data register.
- Data ingestion pipeline.

## PHASE B — CALIBRATION INFRASTRUCTURE

Dapat dikerjakan dengan synthetic fixture untuk menguji software.

Hasil:
- Calibration configuration.
- Parameter registry.
- Loss functions.
- Search/optimization engine.
- Calibration/validation split.
- Sensitivity analysis.
- Reproducible experiment runner.
- Diagnostics dan visualization.

## PHASE C — EMPIRICAL CALIBRATION

Hanya dapat dinyatakan berhasil apabila tersedia pengamatan nyata yang cukup dan relevan.

Jika belum ada data:
- Jangan membuat observed values.
- Jangan melatih model menggunakan synthetic outputs lalu menyebutnya kondisi aktual.
- Jangan mengisi kekosongan dengan perkiraan tak bersumber.
- Jangan menyatakan VALIDATED 2026 BASELINE.

Phase C harus berstatus:
**BLOCKED — INSUFFICIENT OBSERVED DATA**

atau PARTIAL apabila hanya sebagian data sudah tersedia.

Jalankan Phase A dan Phase B secara lengkap meskipun Phase C terblokir.

# 4. DATA DISCOVERY & SOURCE AUDIT

Periksa sumber data lokal proyek terlebih dahulu.

Inventaris semua data:
- Raw OSM M02.
- Source road attributes.
- Railway source tags.
- Vehicle assumptions.
- OD fixtures.
- Signal configurations.
- Railway schedules synthetic.
- SUMO recorded results.
- Existing field observation data, jika ada.

Buat source classification:

1. OBSERVED_FIELD.
2. OFFICIAL_ADMINISTRATIVE.
3. PUBLISHED_RESEARCH.
4. GEOSPATIAL_REFERENCE.
5. ENGINEERING_INFERENCE.
6. MODEL_ASSUMPTION.
7. SYNTHETIC_TEST.
8. SIMULATED_RESULT.
9. MISSING.

Lakukan pencarian sumber publik apabila akses tersedia, dengan prioritas sumber otoritatif seperti:
- Dinas Perhubungan Kabupaten Sidoarjo.
- Dinas Perhubungan Provinsi Jawa Timur.
- Badan Pusat Statistik.
- Instansi pengelola jalan terkait.
- Sumber resmi operator perkeretaapian dan pengelola infrastruktur.
- Publikasi akademik yang dapat diverifikasi.
- Dokumen transportasi resmi yang relevan.

Jangan menyatakan suatu dataset tersedia sebelum berhasil ditemukan dan diperiksa.

Jangan menganggap statistik jumlah kendaraan tingkat kabupaten sebagai volume pada Simpang Gedangan.

Jika menggunakan data tahun selain 2026, beri label tahun aslinya serta batas penggunaannya.

Jika sumber daring tidak dapat diakses:
- Catat keterbatasannya.
- Lanjutkan menggunakan data lokal.
- Jangan mengarang hasil pencarian.

Semua sumber yang berhasil diunduh harus mempunyai metadata, tanggal akses, lisensi dan provenance. Eksekusi simulator tetap harus bisa dilakukan offline setelah input tersedia lokal.

# 5. OBSERVATION DATA SCHEMA

Buat schema data lapangan yang dapat dibaca mesin.

## A. Traffic Counts

Wajib mendukung:
- Observation ID.
- Date.
- Time interval start/end.
- Timezone Asia/Jakarta.
- Location ID.
- Approach.
- Direction.
- Turning movement.
- Vehicle class.
- Count.
- Observation method.
- Observer/source.
- Confidence/quality.
- Provenance ID.

Interval standar:
- 15 menit.

Support interval lebih pendek atau panjang jika sumbernya memang demikian, dengan aturan agregasi yang terdokumentasi.

Hitungan yang tidak tersedia adalah NULL/MISSING, bukan nol.

Nol hanya berarti benar-benar diamati dan tidak ada kendaraan.

## B. Travel Time

Wajib mendukung:
- Origin.
- Destination.
- Route/corridor.
- Date and time.
- Vehicle class.
- Observed travel time.
- Sample count.
- Source method.
- Uncertainty.
- Data quality.

## C. Queue Measurement

Wajib mendukung:
- Observation point.
- Approach/lane group.
- Time.
- Queue length.
- Queue count.
- Maximum observed extent.
- Units.
- Measurement method.
- Boundary censoring.
- Quality.

Panjang antrean harus konsisten dengan definisi pengukurannya.

Jangan mencampur jumlah kendaraan dengan panjang antrean dalam meter.

## D. Signal Observations

Wajib mendukung:
- Intersection.
- Signal head/group.
- Phase.
- Green duration.
- Yellow duration.
- Red duration.
- Cycle time.
- Offset, jika diketahui.
- Date/time observed.
- Source and quality.

Jangan memakai program M05 sebagai fakta lampu Gedangan.

## E. Railway Crossing Observations

Wajib mendukung:
- Crossing site ID.
- Train movement if observed.
- Warning start.
- Road closure.
- Train approach.
- Train arrival/pass.
- Train clearance.
- Barrier reopening.
- Road release.
- Observation method.
- Date/time.
- Uncertainty.

Jangan menganggap jadwal keberangkatan kereta sama dengan waktu palang tertutup.

## F. Geometry Observations

Wajib mendukung:
- Survey point.
- CRS.
- Road centerline.
- Rail centerline.
- Lane count.
- Lane width.
- Stop-line position.
- Barrier/gate position.
- Crossing angle.
- Track count if verified.
- Clearance data.
- Survey accuracy.
- Source provenance.

Buat schema geometry evidence yang dapat dibandingkan dengan M05.1 geometry audit.

# 6. SURVEY PLAN GEDANGAN

Buat rencana survei yang realistis dan dapat digunakan untuk mengumpulkan data.

Prioritaskan:

A. Jalan utama Sidoarjo menuju Surabaya.

B. Jalan utama Surabaya menuju Sidoarjo.

C. Perempatan Gedangan.

D. Frontage road.

E. Feeder Ketajen.

F. Area Stasiun Gedangan dan perlintasan kereta.

G. Persimpangan hulu/hilir yang relevan dengan spillback.

Untuk tiap titik, dokumentasikan:
- Lokasi dan edge IDs.
- Alasan pemilihan.
- Arah pergerakan.
- Jenis kendaraan.
- Metrik yang perlu direkam.
- Instrumen/metode.
- Periode pengamatan.
- Keterkaitan dengan model SUMO.
- Potensi bias pengukuran.

Buat formulir dan template spreadsheet/CSV yang dapat diisi secara manual.

Jangan menetapkan jam puncak sebagai fakta sebelum observasi tersedia.

Boleh mengusulkan sesi pagi, siang, sore, hari kerja dan akhir pekan sebagai desain pengamatan, bukan hasil pengukuran.

Sertakan rencana pencatatan kejadian khusus:
- Perlintasan kereta tertutup.
- Lampu lalu lintas berubah.
- Kendaraan berat.
- Aktivitas akses frontage.
- Antrean merambat.
- Hambatan samping.
- Kejadian luar biasa.

Jika menggunakan video:
- Gunakan sumber yang sah dan berizin.
- Jangan melakukan scraping CCTV privat.
- Kurangi data identitas pribadi seperti wajah dan plat nomor yang tidak diperlukan.
- Dokumentasikan kesalahan hitung dan keterbatasan visibilitas.

# 7. DATA INGESTION & QUALITY CONTROL

Bangun importer lokal untuk CSV/JSON dan format sederhana yang relevan.

Validasi:
- Tanggal dan timezone.
- Duplikasi record.
- Observation ID.
- Lokasi dan arah.
- Valid vehicle class.
- Nonnegative counts.
- Interval consistency.
- Unit consistency.
- Missing versus zero.
- Outliers.
- Data gaps.
- Source and provenance.
- Vehicle count aggregation.
- Turning movement consistency.

Jangan otomatis membuang outlier tanpa audit.

Simpan:
- Raw imported data.
- Normalized observation data.
- Rejected records.
- Quality flags.
- Import summary.
- Source hash.

Buat observation mapping dari lokasi pengamatan ke:
- SUMO edge.
- Lane.
- Junction.
- Turning movement.
- Detector.
- OD zone.

Mapping tidak boleh dilakukan berdasarkan proximity saja jika ada ambiguitas topologi atau arah.

Jika mapping ambigu, tampilkan opsi kandidat dan status NEEDS MANUAL REVIEW.

# 8. MODEL STRUCTURAL READINESS

Sebelum mengkalibrasi parameter kendaraan, periksa apakah model cukup representatif.

Audit:

1. Network directions.
2. Number of lanes.
3. Allowed vehicle classes.
4. Junction connections.
5. Main arterial continuity.
6. Frontage access.
7. Feeder access.
8. Traffic signal controllers.
9. Railway crossings.
10. Short edges around crossing.
11. Lane storage lengths.
12. Actual observed geometry gaps.

Klasifikasikan:

- READY_FOR_CALIBRATION.
- PROVISIONAL_WITH_UNCERTAINTY.
- STRUCTURAL_BLOCKER.
- NEEDS_FIELD_SURVEY.

Jangan menggunakan optimasi demand untuk menyembunyikan kesalahan geometri atau topologi.

Periksa terutama pengaruh lane sekitar 0,10m, posisi stop line dan crossing connector terhadap queue/storage metrics.

Jika sebuah indikator tidak bisa dibandingkan dengan observasi karena struktur network belum layak, blokir indikator tersebut dari klaim kalibrasi.

# 9. BASELINE 2026 CONFIGURATION

Buat konfigurasi baseline tahun 2026 yang memisahkan:

- Geographic network.
- Network variant.
- Vehicle classes.
- Demand.
- OD.
- Traffic signal.
- Railway operations.
- Behavior parameters.
- Measurement windows.
- Observation dataset.
- Source confidence.

Buat setidaknya dua status:

**2026 PROVISIONAL BASELINE**

Menggunakan data dan asumsi yang tersedia.

**2026 EMPIRICALLY CALIBRATED BASELINE**

Hanya boleh aktif setelah observed data dan independent validation benar-benar memenuhi kriteria yang ditetapkan.

Jangan menamai skenario 2026 sebagai calibrated hanya karena field `year=2026`.

Gunakan asumsi yang sudah ada sebagai starting configuration, bukan ground truth.

# 10. CALIBRATION PARAMETER REGISTRY

Buat daftar parameter yang boleh dipertimbangkan untuk kalibrasi:

## Traffic demand
- Vehicle flow by interval.
- Composition by class.
- Origin-destination proportions.
- Departure time distribution.
- Turning movement distribution.

## Vehicle dynamics
- Desired speed.
- Speed factor/distribution.
- Acceleration/deceleration.
- MinGap.
- Tau.
- Lateral behavior, jika data mendukung.

## Traffic control
- Signal phases.
- Signal cycle and offset.
- Crossing closure timing.
- Train arrival profiles.

Namun, traffic signal timing dan railway closure yang dapat diamati langsung sebaiknya dimasukkan sebagai measured boundary conditions, bukan parameter bebas untuk dipilih optimizer demi mendapatkan skor bagus.

Buat:
- Parameter ID.
- Scope.
- Initial value.
- Allowed bounds.
- Unit.
- Source.
- Calibration eligibility.
- Sensitivity.
- Dependency.
- Prior information.
- Status.

Jangan memberi rentang parameter yang tidak masuk akal atau tidak didukung batas teknis SUMO.

Gunakan batas parameter yang dapat dipertanggungjawabkan.

Tidak semua parameter harus dikalibrasi sekaligus.

# 11. CALIBRATION ENGINE

Implementasikan mesin kalibrasi menggunakan Python dan SUMO offline.

Dukungan:
- Calibration configuration.
- Repeatable SUMO runner.
- Parameter injection.
- Objective function evaluation.
- Multiple random seeds.
- Trial history.
- Optimizer checkpoint.
- Best parameter set.
- Reproduction manifests.

Gunakan pendekatan sederhana yang dapat diaudit terlebih dahulu, seperti bounded parameter search dan sensitivity analysis.

Jika perlu, evaluasi optimization methods yang tersedia secara lokal, tanpa menambah dependency berat yang tidak diperlukan.

Jangan membuat optimizer yang mengubah puluhan parameter ketika data observasi hanya sedikit.

## Multi-objective calibration

Dukung perbandingan:

1. Traffic counts.
2. Turning movement counts.
3. Travel times.
4. Speeds.
5. Queue lengths.
6. Waiting times.
7. Railway closure events jika observed.

Gunakan loss terms terpisah, dengan definisi normalisasi dan bobot yang terdokumentasi.

Metrik dapat mencakup:
- MAE.
- RMSE.
- Relative error dengan perlakuan khusus untuk nilai nol.
- Count discrepancy.
- GEH untuk traffic counts jika satuan dan interval kompatibel.
- Distribution comparisons.
- Bias.

Jangan menetapkan satu threshold statistik sebagai jaminan universal bahwa model sudah valid.

Threshold acceptance harus mempunyai justifikasi dan sesuai tujuan simulasi, ukuran sampel, dan kualitas data.

Jangan mengoptimasi menggunakan SIMULATED_RESULT yang sama sebagai pengganti observed ground truth.

# 12. CALIBRATION WORKFLOW

Gunakan alur:

1. Import verified observations.
2. Validate data.
3. Map observations ke network.
4. Check network structural readiness.
5. Partition calibration/validation sets.
6. Select identifiable parameters.
7. Run baseline.
8. Calculate error.
9. Optimize parameters.
10. Evaluate calibrated set.
11. Validate on independent data.
12. Report uncertainty and failure.

Jika Step 1–5 gagal karena data nyata belum tersedia, jangan menjalankan empirical calibration.

Sebagai gantinya, gunakan isolated synthetic recovery experiment untuk membuktikan bahwa sistem optimizer mampu menemukan parameter sintetis yang sudah diketahui.

Label:
**SOFTWARE CALIBRATION TEST — NOT EMPIRICAL CALIBRATION**.

# 13. CALIBRATION VS INDEPENDENT VALIDATION

Pisahkan data untuk:
- Calibration.
- Independent validation.
- Optional out-of-sample stress.

Contoh pemisahan yang bisa didukung:
- Waktu yang berbeda.
- Hari yang berbeda.
- Lokasi pengamatan yang berbeda.
- Pergerakan atau kelas kendaraan yang tidak dipakai untuk fitting.

Jenis split harus sesuai data aktual dan tujuan studi.

Jangan memakai record yang sama di kedua himpunan.

Jika data tidak cukup untuk holdout, tulis:
**INDEPENDENT VALIDATION NOT POSSIBLE WITH AVAILABLE DATA**.

Jangan menyebut goodness-of-fit pada training data sebagai validasi independen.

Jangan mengklaim generalisasi sampai 2030/2040 dari data 2026 yang belum tervalidasi.

# 14. IDENTIFIABILITY & UNCERTAINTY

Buat analisis sensitivitas untuk menentukan parameter mana yang paling memengaruhi:
- Traffic counts.
- Travel times.
- Waiting times.
- Queue lengths.
- Spillback events.

Periksa parameter confounding, misalnya demand versus signal capacity, speed versus travel time, dan demand routing versus vehicle turning counts.

Jika beberapa parameter memberikan hasil yang sama, jangan mengklaim telah menemukan nilai sebenarnya.

Sediakan:
- Parameter uncertainty.
- Observation quality uncertainty.
- Network/geometry uncertainty.
- OD uncertainty.
- Scenario structural uncertainty.

Pisahkan uncertainty dari random seeds dengan uncertainty akibat kurangnya data.

# 15. RAILWAY & SIGNAL CALIBRATION

Railway pilot M05 sudah bekerja tetapi jadwal/timing masih sintetis.

Buat framework untuk memasukkan:
- Observed train movements.
- Observed crossing closure.
- Warning and reopening duration.
- Observed signal timing.
- Observed road queue response.

Jangan mengklaim jadwal resmi kereta membuktikan durasi aktual penutupan palang.

Jangan menganggap crossing pilot sudah mewakili seluruh operasi stasiun.

Persiapkan pemeriksaan synchronization antara:
- Train movement.
- Crossing state.
- Road stop/release.
- Queue.
- Traffic signal phase.

Apabila data geometri perlintasan belum tersedia, railway calibration tetap PROVISIONAL.

# 16. SPILLBACK VALIDATION

Gunakan causal detector M05.1 yang telah lulus pengujian.

Bedakan:

A. Simulated spillback events.

B. Observed field evidence.

C. Matched events.

D. Unmatched simulated events.

E. Unmatched observed events.

Tanpa observed queue/vehicle movement data, jangan mengklaim detektor sudah tervalidasi untuk kondisi fisik Gedangan.

Buat event matching framework dengan:
- Location.
- Time interval.
- Duration.
- Affected edge.
- Trigger.
- Recovery.
- Uncertainty.

Tidak wajib memperoleh observed spillback pada M06 apabila data lapangan belum tersedia.

# 17. DATA QUALITY & SCIENTIFIC REPORTING

Untuk setiap hasil tampilkan:

- Source.
- Date.
- Spatial scope.
- Temporal coverage.
- Vehicle classes.
- Number of samples.
- Missing values.
- Method.
- Uncertainty.
- Validation status.
- Assumptions.
- Reproducibility information.

Pisahkan:
**VERIFIED OBSERVATION**
**REFERENCE**
**ASSUMPTION**
**SYNTHETIC SOFTWARE TEST**
**SIMULATED OUTPUT**
**UNVALIDATED ESTIMATE**

Jika ada pernyataan bahwa Gedangan mengalami peningkatan kemacetan, pertumbuhan kendaraan atau penurunan kecepatan, wajib ada data dan sumber yang mendukung.

Catatan kualitatif pengguna bahwa frontage relatif lancar dapat dicatat sebagai USER_REPORTED_FIELD_OBSERVATION, bukan pengukuran kecepatan atau kapasitas.

Jangan mengubahnya menjadi target angka kalibrasi.

# 18. INTERNAL BROWSER CODEX

Buat halaman M06:

**Baseline 2026 — Data & Calibration Lab**

Gunakan internal browser Codex sebagai tempat inspeksi utama.

Tampilkan:

A. Data Readiness Dashboard
- Inventory.
- Coverage.
- Missing data.
- Confidence.
- Source dates.
- Quality flags.

B. Geographic Observation Map
- Observation points.
- Road/lane/turn mapping.
- Frontage.
- Railway crossing.
- Unmapped or ambiguous data.

C. Traffic Counts
- Actual observed counts jika tersedia.
- Synthetic model output.
- Error comparison hanya jika observed data tersedia.

D. Calibration
- Parameter set.
- Objective function.
- Trial history.
- Best candidate.
- Status empirically calibrated atau software test only.

E. Validation
- Holdout data.
- Errors.
- Pass/fail criteria.
- Coverage and uncertainty.

F. Railway/Geometry
- Stop-line geometry status.
- Crossing survey status.
- Rail operation data completeness.
- Structural blockers.

G. Audit
- Sources.
- Assumptions.
- Run manifests.
- Reproducibility.

Jangan mengisi grafik observed dengan angka sintetis.

Jika data observed belum ada, tampilkan:
**NO VERIFIED 2026 OBSERVATIONS AVAILABLE**

Playback atau plot untuk tes optimizer boleh menggunakan sintetis dengan watermark/status yang jelas.

Viewer M05.1 harus tetap berfungsi.

# 19. SURVEY DOCUMENTS & DATA TEMPLATES

Siapkan dokumen praktis untuk survei:

1. Traffic count tally sheet.
2. Vehicle classification sheet.
3. Turning movement count sheet.
4. Travel time observation sheet.
5. Queue length measurement sheet.
6. Traffic signal timing sheet.
7. Railway crossing event sheet.
8. Geometric survey sheet.
9. Data source and provenance registry.
10. Survey methodology and quality instructions.

Buat CSV/JSON templates untuk ingestion otomatis.

Boleh menambahkan template Excel jika dependency tersedia dan sesuai kebutuhan, tetapi jangan menjadikannya penghalang penyelesaian.

Sediakan satu contoh data DEMO SYNTHETIC pada folder terpisah. Jangan mengisinya sebagai observed.

# 20. PERFORMANCE

Target mesin:
- Windows 11.
- RAM 16GB.
- AMD GPU 6GB VRAM.
- 1080p internal browser.

Lakukan test optimizer secara bertingkat.

Hindari brute-force dengan ribuan SUMO runs jika belum diperlukan.

Periksa:
- Per-run wall time.
- CPU.
- RAM peak jika terukur.
- Number of simulations.
- Number of seeds.
- Failed simulations.
- Optimizer recovery.
- Browser responsiveness.

Optimasi M06 adalah parameter model, bukan optimasi tampilan 3D.

# 21. PROJECT FILES

Buat struktur modular, disesuaikan dengan proyek:

`backend/gedangan/m06_data.py`

`backend/gedangan/m06_observations.py`

`backend/gedangan/m06_calibration.py`

`backend/gedangan/m06_validation.py`

`backend/gedangan/m06_uncertainty.py`

`backend/gedangan/m06_reporting.py`

`configuration/calibration-m06/`

`data/observations/m06/`

`data/templates/m06/`

`simulation/runs/m06/`

`documentation/m06/`

`frontend/calibration.html`

`frontend/src/m06/`

`tests/m06/`

Jaga pemisahan raw data, normalized observation, synthetic test, dan simulated result.

Buat launcher:

`START_CALIBRATION_M06.bat`

`REBUILD_CALIBRATION_M06.bat`

Gunakan port lokal tersendiri yang tidak mengganggu viewer sebelumnya.

# 22. TESTING

Pertahankan seluruh 152 regression tests dari M05.1.

Tambahkan tests untuk:
- Observation schemas.
- Missing versus zero.
- Interval aggregation.
- Timezone.
- Source provenance.
- Import validation.
- Duplicate detection.
- Edge mapping.
- Vehicle class mapping.
- OD aggregation.
- Data leakage prevention.
- Calibration/validation separation.
- Calibration loss metrics.
- Synthetic parameter recovery.
- Parameter constraints.
- Sensitivity analysis.
- Uncertainty reporting.
- Railway observation alignment.
- Geometry blockers.
- Spillback event matching.
- Manifest/reproducibility.
- Baseline source immutability.
- UI data-state correctness.

Pengujian synthetic recovery wajib membuktikan bahwa algoritma dapat menemukan parameter yang disembunyikan dalam eksperimen terkontrol, dalam batas identifiability yang dapat dibenarkan.

Jangan menjadikan keberhasilan synthetic recovery sebagai bukti empirical calibration.

Jalankan:
- Full Python regression.
- SUMO integration tests.
- TypeScript noEmit.
- Vite production build.
- Internal browser desktop QA.
- Browser mobile QA.
- Reproducibility checks.

# 23. ACCEPTANCE CRITERIA

Pisahkan dua kategori acceptance.

## A. TECHNICAL READINESS ACCEPTANCE

M06 technical readiness dinyatakan PASS jika:

1. Data inventory selesai.
2. Missing data register jelas.
3. Observation schemas valid.
4. Data ingestion dan QA berfungsi.
5. Survey templates siap.
6. Spatial observation mapping berfungsi.
7. Baseline 2026 provisional configuration valid.
8. Structural blockers tercatat.
9. Calibration engine dapat berjalan.
10. Synthetic parameter-recovery test berhasil.
11. Independent validation split framework tersedia.
12. Sensitivity/uncertainty framework berfungsi.
13. Railway/signal calibration interfaces tersedia.
14. Browser internal menampilkan data readiness yang benar.
15. Seluruh regression tests lulus.
16. Source M01–M05.1 tidak rusak.
17. Rebuild reproducible.

## B. EMPIRICAL BASELINE ACCEPTANCE

2026 EMPIRICALLY CALIBRATED BASELINE hanya boleh PASS jika:

1. Observed traffic data tersedia dan tervalidasi.
2. Temporal/spatial coverage cukup untuk tujuan studi.
3. Network geometry cukup layak pada lokasi yang dievaluasi.
4. Control/timing data yang relevan tersedia.
5. Calibration parameters mempunyai dasar yang jelas.
6. Calibration benar-benar menggunakan observed data.
7. Independent validation berhasil.
8. Uncertainty dilaporkan.
9. Mismatch yang belum terpecahkan tidak disembunyikan.
10. Baseline dapat direproduksi.

Jika observasi belum cukup, tampilkan:

**TECHNICAL READINESS: PASS/PARTIAL**

**EMPIRICAL BASELINE: BLOCKED — DATA REQUIRED**

Jangan menggabungkan kedua status tersebut menjadi satu FULL PASS yang menyesatkan.

# 24. FINAL REPORT

Buat:

`MILESTONE_06_REPORT.md`

`MILESTONE_06_README.md`

Laporan wajib memuat:
- Executive summary.
- Technical readiness status.
- Empirical calibration status.
- Data inventory.
- Source provenance.
- Data completeness matrix.
- Identified observed datasets.
- Missing data.
- Survey methodology.
- Data collection templates.
- Import/QA results.
- Network structural readiness.
- Baseline configuration.
- Calibration parameters.
- Objective functions.
- Synthetic recovery results.
- Independent validation architecture.
- Sensitivity/uncertainty.
- Traffic signal/railway status.
- Geometry blockers.
- Spillback validation readiness.
- Internal browser screenshots.
- Regression results.
- Reproducibility.
- Scientific limitations.
- Unresolved issues.
- M07 readiness and blockers.

Sertakan satu daftar prioritas pengumpulan data dengan pemisahan:

**CRITICAL — REQUIRED FOR EMPIRICAL CALIBRATION**

**IMPORTANT — IMPROVES CONFIDENCE**

**OPTIONAL — FUTURE REFINEMENT**

Jelaskan dengan spesifik data mana yang benar-benar harus disediakan pengguna melalui survei atau sumber yang bisa dipertanggungjawabkan.

Jangan memulai Milestone 07.

**MULAI MILESTONE 06 SEKARANG.**

Bangun sistem kalibrasi secara serius, reproducible dan berbasis pengamatan. Jangan mengarang data 2026, jangan memaksakan hasil validasi, dan jangan menyembunyikan masalah geometri atau konektivitas yang belum terselesaikan.