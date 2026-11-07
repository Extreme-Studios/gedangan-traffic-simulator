# MILESTONE 07 — GEDANGAN TRAFFIC DIGITAL TWIN
## Automatic Traffic Growth Projection 2026–2040, OD Forecasting & Scenario Comparison

**MODEL: GPT-6.1 SOL — MEDIUM**

Lanjutkan proyek Gedangan Traffic Simulator dari M01 sampai M06.

**KERJAKAN MILESTONE 07 SAJA. JANGAN MEMULAI M08.**

Tujuan M07 adalah membuat sistem proyeksi pertumbuhan permintaan kendaraan yang otomatis, transparan, dapat dikonfigurasi, dan reproducible untuk tahun 2026–2040.

**PENTING: M06 technical readiness PASS, tetapi empirical baseline 2026 masih BLOCKED — DATA REQUIRED. Karena itu, seluruh hasil proyeksi harus diperlakukan sebagai CONDITIONAL SCENARIO PROJECTION, bukan prediksi lalu lintas Gedangan yang telah tervalidasi.**

---

# 1. PROJECT DIRECTORY

Gunakan folder:

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

Baca laporan dan source code M01–M06, terutama:

- MILESTONE_04_REPORT.md
- MILESTONE_04_5_REPORT.md
- MILESTONE_05_REPORT.md
- MILESTONE_05_1_REPORT.md
- MILESTONE_06_REPORT.md
- M06 baseline-2026.json
- M06 data completeness dan empirical gate
- M04 vehicle registry
- M04 OD Matrix dan demand generator
- M04.5 corrected vehicle permissions
- M05 signal, railway, queue dan spillback modules
- M05.1 causal detector
- M06 observation schemas, calibration engine dan provenance
- Project architecture, data governance dan roadmap

Periksa implementasi aktual, bukan hanya laporan.

Sebelum bekerja:
1. Jalankan regression M06.
2. Catat jumlah tes awal.
3. Simpan manifest SHA-256 baseline.
4. Periksa status empirical calibration.
5. Identifikasi network dan demand yang valid untuk eksperimen.

Jangan mengubah output milestone sebelumnya.

# 2. OBJECTIVE

Membangun Traffic Growth Projection Engine dengan kemampuan:

1. Baseline year 2026.
2. Simulasi semua tahun 2026–2040.
3. Preset cepat 2026, 2030, 2035 dan 2040.
4. Pemilihan tahun secara interaktif.
5. Pertumbuhan otomatis berdasarkan tahun.
6. Pertumbuhan berbeda menurut jenis kendaraan.
7. Pertumbuhan berbeda menurut pasangan OD.
8. Skenario LOW, REFERENCE dan HIGH.
9. Pertumbuhan per periode waktu.
10. Reproducible SUMO demand generation.
11. Actual projected-network SUMO simulation.
12. Perbandingan hasil antar-tahun.
13. Sensitivity dan uncertainty analysis.
14. Provenance dan asumsi eksplisit.
15. Kemampuan mengganti baseline sintetis dengan observed baseline yang telah dikalibrasi nanti.

Jangan meminta pengguna memilih hanya satu tahun proyeksi untuk dibangun. Semua tahun harus didukung dalam aplikasi.

# 3. BASELINE POLICY 2026

Pertahankan baseline 2026 dari M06.

Status baseline saat ini:

**2026 PROVISIONAL — NOT EMPIRICALLY CALIBRATED**

Jangan mengganti status menjadi calibrated secara otomatis.

Buat baseline adapter yang mendukung:

A. PROVISIONAL_SYNTHETIC_BASELINE

B. EMPIRICALLY_CALIBRATED_BASELINE

Untuk sementara, A dapat digunakan untuk eksperimen software.

B hanya dapat diaktifkan jika empirical gate dari M06 benar-benar lolos.

Jangan menganggap nilai LOW/MEDIUM/STRESS M04 sebagai volume kendaraan riil Gedangan.

Jangan mengubah profil synthetic test menjadi observed data.

Jika data empiris belum tersedia, tampilkan label jelas:

**ILLUSTRATIVE TRAFFIC PROJECTION — 2026 BASELINE NOT CALIBRATED**

# 4. VEHICLE CLASS GROWTH MODEL

Gunakan sepuluh kategori kendaraan dari registry M04:

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

Oversize tetap NOT_ROUTABLE sampai gate fisik dan legalitas M04.5 dapat dipenuhi. Pertumbuhan demand oversize tidak boleh membuatnya otomatis masuk jaringan.

Buat growth-rate registry menurut:
- Vehicle class.
- Scenario.
- Calendar year.
- Geographic scope.
- OD relation.
- Source and publication year.
- Estimation method.
- Data confidence.
- Applicable period.
- Provenance status.

Motor tidak harus tumbuh dengan laju yang sama dengan mobil.

Kendaraan penumpang tidak harus tumbuh dengan laju yang sama dengan truk.

Tidak boleh menggunakan satu growth rate untuk seluruh kendaraan tanpa alasan eksplisit.

# 5. COMPOUND ANNUAL GROWTH ENGINE

Gunakan pertumbuhan majemuk tahunan.

Untuk laju konstan:

Demand(year) = Demand(2026) × (1 + growth_rate)^(year - 2026)

Untuk pertumbuhan berbeda per tahun:

Demand(year) = Demand(2026) × PRODUCT(1 + annual_rate[y])

untuk setiap tahun y dari 2027 sampai tahun tujuan.

Implementasikan:
- Constant annual rate.
- Piecewise annual rates.
- Year-specific rates.
- Zero growth.
- Negative growth.
- Class-specific rates.
- OD-specific modifiers jika dapat dipertanggungjawabkan.
- Scenario-specific assumptions.

Pastikan tidak ada double counting antara class growth dan OD multiplier.

Jika OD growth adalah parameter final tersendiri, jangan sekaligus mengalikan class growth lagi tanpa definisi model yang jelas.

Pilih satu rumusan utama yang terdokumentasi dan transparan, misalnya:

Demand(y, OD, class, interval)
= Demand(2026, OD, class, interval) × cumulative_growth(y, OD, class)

Sediakan growth-rate resolution policy:
1. Verified OD-and-class-specific rate jika tersedia.
2. Verified class-specific rate pada cakupan yang cocok.
3. Explicit documented scenario assumption.
4. Missing jika tidak ada dasar.

Jangan silent fallback menggunakan angka nasional sebagai angka lokal Gedangan.

Uji:
- 2026 factor selalu 1.
- Zero growth tidak mengubah demand.
- Negative growth menurunkan demand tanpa membuat count negatif.
- Piecewise rates bekerja benar.
- Semua tahun reproducible.
- Tidak ada off-by-one antara 2026 dan 2027.

# 6. EVIDENCE-BASED GROWTH SOURCING

Audit kembali public-source register M06.

Jika internet tersedia, telusuri sumber yang relevan dan dapat diverifikasi:

- BPS Kabupaten Sidoarjo.
- BPS Provinsi Jawa Timur.
- Dinas Perhubungan Sidoarjo.
- Dinas Perhubungan Jawa Timur.
- Instansi pengelola jalan yang relevan.
- Publikasi kajian transportasi terpercaya.
- Data pergerakan kendaraan historis jika tersedia.

Jangan mengarang URL, dataset, nilai pertumbuhan, atau tahun observasi.

PENTING:

Pertumbuhan jumlah kendaraan terdaftar TIDAK otomatis sama dengan pertumbuhan arus lalu lintas pada satu koridor.

Pertumbuhan penduduk TIDAK otomatis sama dengan pertumbuhan kendaraan di Simpang Gedangan.

Pertumbuhan ekonomi TIDAK otomatis sama dengan pertumbuhan perjalanan truk.

Jika data resmi hanya tersedia pada tingkat provinsi/kabupaten:
- Catat cakupan geografisnya.
- Catat metrik aslinya.
- Jelaskan perbedaan dengan traffic flow.
- Gunakan sebagai contextual reference atau scenario assumption, bukan ground truth koridor.
- Jangan memberi label VERIFIED LOCAL TRAFFIC GROWTH.

Jika nilai pertumbuhan kredibel belum tersedia, jangan berhenti membangun engine.

Sediakan konfigurasi contoh LOW/REFERENCE/HIGH dengan nilai yang dapat diubah dan label SYNTHETIC ILLUSTRATIVE ASSUMPTION.

Angka contoh bukan rekomendasi atau estimasi aktual Gedangan.

Simpan:
- Source URL.
- Title.
- Publisher.
- Publication date.
- Measurement period.
- Vehicle classification.
- Geographic coverage.
- Original metric.
- Derived rate calculation.
- Limitations.
- Confidence.
- Provenance.
- Local source snapshot/hash jika boleh diunduh.

Jangan bergantung pada internet saat simulator berjalan.

# 7. OD-SPECIFIC PROJECTION

Gunakan OD zones M04/M06.

Prioritas movement:
- Sidoarjo → Surabaya.
- Surabaya → Sidoarjo.
- Feeder → main road.
- Main road → feeder.
- Frontage internal.
- Frontage access.
- Gedangan junction movements.
- Ketajen.
- Station access.
- Local movements.

Perhatikan:

**Koridor Sidoarjo menuju Surabaya merupakan bottleneck utama yang ingin dianalisis pengguna.**

Namun, arah sebaliknya tetap wajib disimulasikan.

Frontage sudah tersedia dan menurut observasi pengguna relatif lancar. Modelkan frontage sebagai jaringan paralel tersendiri, dengan access/merge yang valid. Jangan secara otomatis menganggap frontage sebagai sumber kemacetan.

Untuk setiap pasangan OD:
- Baseline demand.
- Vehicle-class composition.
- Departure interval.
- Growth source/status.
- Annual growth schedule.
- Forecast demand.
- Network feasibility.
- Routable fraction.
- Unserved demand.

Pertumbuhan OD tidak boleh menghasilkan rute ilegal.

Jangan memindahkan kendaraan dari OD yang gagal ke OD lain agar jumlah kendaraan terlihat berhasil.

Konektivitas Strict yang gagal tetap dilaporkan.

# 8. TIME-OF-DAY PROJECTION

Pertahankan interval 15 menit agar kompatibel dengan schema survei M06.

Demand harus dapat diperinci menurut:
- Tahun.
- Skenario.
- Jenis kendaraan.
- OD.
- Interval waktu.
- Hari/periode yang dipilih.

Sediakan engine untuk mempertahankan time profile baseline atau memakai perubahan time profile yang dikonfigurasi secara eksplisit.

Jangan otomatis menganggap jam puncak bergeser atau melebar tanpa dasar.

Jika peak spreading diuji, perlakukan sebagai skenario tambahan dan dokumentasikan metode serta asumsi.

Pastikan jumlah per interval menjumlah tepat ke demand keseluruhan.

# 9. INTEGER ALLOCATION & CONSERVATION

Demand hasil compound growth sering pecahan.

Implementasikan deterministic integer allocation.

Gunakan pendekatan seperti largest remainder atau metode lain yang terdokumentasi.

Persyaratan:
- Tidak ada jumlah kendaraan negatif.
- Integer counts.
- Total sesuai aturan pembulatan eksplisit.
- Alokasi berdasarkan class/OD/interval.
- Seed deterministik.
- Stable ordering.
- Unique vehicle ID.
- Tidak ada kendaraan hilang tanpa ledger.
- Error pembulatan tercatat.

Buat audit requested demand versus generated trips.

Jangan menggunakan randomness untuk menutupi selisih total.

# 10. DEMAND GENERATION & NETWORK COMPATIBILITY

Gunakan M04 demand generator dan vehicle registry dengan adapter M07.

Gunakan SUMO 1.28.0 lokal.

Untuk setiap run:
1. Tentukan year/scenario.
2. Resolve baseline.
3. Resolve growth rates.
4. Calculate projected OD × class × interval.
5. Generate trips.
6. Validate permissions.
7. Route using actual network.
8. Record route failures.
9. Execute SUMO.
10. Collect lifecycle dan traffic metrics.

Pertahankan corrected access policy M04.5.

Jangan bypass:
- Oneway.
- Turn restrictions.
- Lane permissions.
- Heavy-vehicle constraints.
- Oversize gate.
- Railway road separation.

Gunakan DUAROUTER repair=false atau pendekatan yang sama ketatnya.

Tidak boleh ada silent dropped trips.

# 11. NETWORK & CONTROL SCENARIOS

Untuk M07, gunakan jaringan yang sudah dibangun:

- Strict.
- Corrected Provisional.
- M05/M05.1 traffic signal and railway pilot derivatives, jika kompatibel.

Pisahkan eksperimen:
A. Constant network and controls.
B. Demand changes by year.
C. Traffic-control sensitivity jika diperlukan sebagai analisis tambahan.

Perbandingan pertumbuhan tahunan utama harus memakai jaringan dan konfigurasi kontrol yang sama, agar efek demand dapat dipisahkan.

Jangan secara otomatis memperlebar jalan, menambahkan flyover, mengubah signal plan, atau meningkatkan kapasitas untuk mengatasi demand masa depan.

Perubahan infrastruktur merupakan target M08.

Control timing dan train schedules yang masih sintetis tetap diberi label asumsi.

# 12. CONGESTION & PERFORMANCE METRICS

Untuk setiap projected run, hitung:

A. Demand
- Requested vehicles.
- Routable vehicles.
- Failed routes.
- Loaded.
- Departed.
- Arrived.
- Running at end.
- Not departed/pending.
- Teleports.
- Collisions.

B. Traffic Performance
- Corridor travel time.
- Waiting time.
- Travel-time loss.
- Mean and distribution of speed.
- Throughput.
- Queue count.
- Queue extent in meters.
- Maximum stopped queue.
- Queue duration.
- Lane occupancy.
- Spillback candidate/verified-in-model events.

C. Segment Analysis
- Sidoarjo → Surabaya.
- Surabaya → Sidoarjo.
- Frontage.
- Feeder roads.
- Gedangan intersection.
- Ketajen/station crossing area.

D. Railway Interaction
- Train movement events.
- Crossing closure.
- Road delay related to closure.
- Queue recovery.

Gunakan actual SUMO outputs.

Jangan menghitung rata-rata hanya untuk kendaraan yang arrived lalu mengabaikan kendaraan yang masih berjalan atau belum bisa masuk.

Untuk fixed horizon, laporkan censoring.

Gunakan unfinished/undeparted vehicle output jika didukung SUMO 1.28.0 dan validasi melalui actual parser.

Buat diagnostic:
**DEMAND EXCEEDS INSERTION OR NETWORK CAPACITY**

jika demand yang diminta tidak dapat dimuat/diselesaikan dalam horizon.

Jangan menganggap kendaraan tidak berangkat sebagai perjalanan yang selesai atau sebagai demand hilang.

# 13. HEAVY DEMAND & GRIDLOCK HANDLING

Proyeksi sampai 2040 dapat menaikkan demand melewati kemampuan jaringan model.

Jangan memaksakan semua kendaraan harus tiba dengan:
- Mengubah rute secara ilegal.
- Menambah lajur tanpa dasar.
- Menonaktifkan konflik.
- Menghapus antrean.
- Mengubah teleport policy tanpa dokumentasi.
- Menambah simulation horizon secara diam-diam.
- Membuang request yang tidak dapat dimuat.

Buat bounded stress-testing stages.

Periksa:
- Entry bottleneck.
- Insertion delays.
- Network saturation.
- Gridlock indicators.
- Boundary queue censoring.
- Vehicle accumulation.
- Route failures.

Jika semua kendaraan tidak selesai sampai akhir run, catat.

Sediakan fixed demand window dengan measurement horizon yang konsisten; optional drain period harus dipisah agar arrival dan queue metrics antar-tahun tetap comparable.

# 14. GROWTH SCENARIOS

Sediakan minimal tiga skenario:

**LOW GROWTH**

**REFERENCE GROWTH**

**HIGH GROWTH**

Skenario-skenario ini bukan probability-based confidence intervals.

Setiap skenario mempunyai:
- Growth rate per class.
- Growth rate per OD atau explicit modifier.
- Start/end year.
- Source.
- Assumption ID.
- Status.
- Explanation.
- Scenario version/hash.

User dapat membuat dan mengedit skenario.

Buat growth editor dengan validasi parameter.

Jika tidak ada data tingkat pertumbuhan empiris yang layak, seluruh skenario demo harus diberi label:

**ILLUSTRATIVE / UNVALIDATED GROWTH ASSUMPTIONS**

Jangan memakai nama REFERENCE untuk memberi kesan bahwa angka tersebut sudah merupakan prakiraan resmi.

# 15. SENSITIVITY & UNCERTAINTY

Bangun sensitivity analysis untuk:
- Annual growth rates.
- Class mix.
- OD distribution.
- Departure profile.
- Rail crossing frequency assumptions.
- Signal-control assumptions.
- Road network capacity uncertainty.

Prioritaskan perubahan demand sambil menjaga variabel lain konstan.

Gunakan beberapa random seeds untuk hasil stokastik yang relevan.

Tampilkan hasil dalam rentang skenario, bukan confidence interval statistik apabila belum mempunyai dasar probabilistik.

Pisahkan:
- Growth-rate uncertainty.
- Baseline-demand uncertainty.
- OD composition uncertainty.
- Network/geometry uncertainty.
- SUMO behavioral uncertainty.
- Random seed variation.

Baseline yang belum terkalibrasi tidak boleh kehilangan label ketidakpastian hanya karena proyeksi memiliki beberapa skenario.

# 16. FAIR YEAR-TO-YEAR COMPARISON

Implementasikan comparison engine:

- 2026 versus 2030.
- 2026 versus 2035.
- 2026 versus 2040.
- Custom year comparison.
- Scenario A versus Scenario B.

Jaga:
- Network variant yang sebanding.
- Signal dan rail operation assumptions yang sama untuk pertumbuhan murni.
- OD definition konsisten.
- Demand interval window sama.
- Vehicle classification sama.
- Seed policy jelas.
- Measurement window sama.
- Unit/metric definitions sama.

Buat perbandingan:
- Total demand growth.
- Growth per class.
- Growth per OD.
- Throughput change.
- Queue change.
- Travel-time change.
- Spillback-event change.

Jika metrik tidak comparable akibat sebagian besar demand tidak terlayani, tampilkan warning dan jangan menyajikan perubahan mean travel-time arrived-only sebagai peningkatan kinerja.

# 17. INTERNAL BROWSER — PROJECTION LAB

Gunakan internal browser Codex.

Buat halaman M07 terpisah dari M06.

Judul:

**GEDANGAN TRAFFIC PROJECTION LAB — 2026 TO 2040**

Sediakan:

A. Year Selector
- 2026.
- 2030.
- 2035.
- 2040.
- Semua tahun lain 2027–2039.
- Slider atau dropdown tahun.

Saat tahun dipilih, projected demand harus dihitung ulang berdasarkan konfigurasi yang dipilih.

B. Growth Scenario
- LOW.
- REFERENCE.
- HIGH.
- Custom.

C. Growth Parameter Panel
- Motorcycle growth.
- Passenger growth.
- Pickup growth.
- Bus growth.
- Truck growth.
- Trailer growth.
- OD-specific policy.
- Provenance and confidence.

D. Demand Dashboard
- Baseline 2026.
- Projected demand.
- Class composition.
- OD demand.
- Year-over-year growth.
- Cumulative growth.
- 15-minute profile.

E. Geographic Visualization
- Main Sidoarjo → Surabaya.
- Main Surabaya → Sidoarjo.
- Frontage.
- Feeders.
- Gedangan intersection.
- Railway crossing.
- Queue and congestion indicators.

F. Simulation Results
- SUMO run status.
- Departed/arrived/pending.
- Speed.
- Travel time.
- Queue.
- Spillback.
- Censoring flags.

G. Comparison
- Baseline versus projected year.
- Low/reference/high.
- Vehicle-class breakdown.
- OD breakdown.
- Warnings and limitations.

H. Provenance
- Source.
- Assumptions.
- Baseline status.
- Model version.
- Scenario hash.
- Network hash.
- Uncertainty labels.

I. Playback
- Recorded results from actual SUMO.
- Play/pause.
- Speed.
- Timeline.
- Camera and layers.

Jangan membuat kendaraan masa depan bergerak memakai animasi acak.

Jika sebuah kombinasi year/scenario belum disimulasikan, tampilkan status NOT RUN, bukan memalsukan hasil SUMO.

Projected demand boleh dihitung langsung melalui engine; metrik lalu lintas seperti queue, speed dan travel time hanya boleh ditampilkan sebagai simulated results setelah SUMO benar-benar berjalan.

Sediakan tombol run hanya jika dapat benar-benar memulai proses lokal melalui backend yang tersedia. Jika tidak, gunakan workflow rebuild/precompute dengan kontrol UI yang jujur.

Label wajib:

**PROVISIONAL 2026 BASELINE — CONDITIONAL FORECAST, NOT EMPIRICALLY VALIDATED**

# 18. REBUILD & PERFORMANCE

Target perangkat:
- Windows 11.
- RAM 16GB.
- AMD GPU target 6GB VRAM.
- 1080p.

Jangan menjalankan semua tahun × semua skenario × semua seed secara bersamaan tanpa resource budgeting.

Gunakan:
- Run queue.
- Sequential or bounded concurrency.
- Cache berdasarkan source/config/network/seed hashes.
- Progress status.
- Failure recovery.
- Checkpoint.
- Deterministic rerun.

Prioritaskan benchmark beberapa kombinasi:
- 2026.
- 2030.
- 2035.
- 2040.

Tambahkan year lain sesuai kebutuhan.

Catat wall time, CPU, RAM jika dapat diukur.

Jangan menyebut FPS atau GPU benchmark tanpa pengukuran.

# 19. PROJECT FILE STRUCTURE

Buat modul modular sesuai arsitektur aktual.

Usulan:

`backend/gedangan/m07_growth.py`

`backend/gedangan/m07_projection.py`

`backend/gedangan/m07_scenarios.py`

`backend/gedangan/m07_runner.py`

`backend/gedangan/m07_analysis.py`

`backend/gedangan/m07_validation.py`

`backend/gedangan/m07_reporting.py`

`configuration/growth-m07/`

`simulation/projections/m07/`

`simulation/runs/m07/`

`documentation/m07/`

`frontend/projection.html`

`frontend/src/m07/`

`tests/m07/`

Sediakan:

`START_PROJECTION_M07.bat`

`REBUILD_PROJECTION_M07.bat`

Gunakan port sendiri dan jangan merusak launcher M01–M06.

# 20. AUTOMATED TESTING

Pertahankan seluruh 182 regression tests M06.

Tambahkan tests untuk:

1. Baseline 2026 multiplier.
2. Compounding growth.
3. Constant annual rates.
4. Piecewise rates.
5. Negative growth.
6. Missing growth data.
7. Growth-rate provenance.
8. Class-specific projections.
9. OD-specific projections.
10. No double counting.
11. Per-interval conservation.
12. Integer allocation.
13. Deterministic seed.
14. Stable vehicle IDs.
15. Route validation.
16. Vehicle permission restrictions.
17. Oversize rejection.
18. Frontage separation.
19. Strict/provisional differences.
20. Requested/routable/failed accounting.
21. Departed/arrived/pending accounting.
22. Fixed horizon censoring.
23. High-demand saturation behavior.
24. Year/scenario comparison parity.
25. Synthetic scenario labeling.
26. Empirical-calibration gate.
27. No source-data mutation.
28. Cache/rebuild reproducibility.
29. Browser year selection.
30. Browser scenario selection.
31. UI no-result state.
32. Actual SUMO output consistency.

Tests tidak boleh sekadar memeriksa bahwa tahun 2040 ditampilkan di layar.

Wajib ada pengujian yang menghitung expected growth secara independen dan membandingkannya dengan output engine.

Wajib ada actual SUMO runs untuk tahun-tahun perwakilan dan beberapa jenis kendaraan.

# 21. ACCEPTANCE CRITERIA — TECHNICAL

M07 technical readiness dinyatakan PASS apabila:

1. Tahun 2026–2040 didukung.
2. Tahun dapat dipilih dari browser.
3. Growth engine menghitung secara benar.
4. Pertumbuhan per vehicle class berfungsi.
5. Pertumbuhan per OD berfungsi.
6. Time-interval demand berfungsi.
7. Three scenarios tersedia.
8. Custom scenario dapat dikonfigurasi.
9. Provenance growth rates jelas.
10. Missing rates tidak dipromosikan menjadi fakta.
11. Demand generation reproducible.
12. Routing dan vehicle access tetap valid.
13. Actual SUMO run berhasil pada representative projection years.
14. Projected demand versus served demand tercatat.
15. Congestion metrics berasal dari SUMO.
16. Censoring dan demand tidak terlayani dilaporkan.
17. Year comparison valid dan transparan.
18. Sensitivity framework berfungsi.
19. Internal browser lulus QA.
20. M01–M06 regression tests tetap lulus.
21. Source datasets tidak berubah.
22. Hasil rebuild reproducible.

# 22. ACCEPTANCE CRITERIA — EMPIRICAL FORECAST

Empirically credible future traffic forecast belum boleh PASS sebelum:

- Baseline 2026 terkalibrasi secara empiris.
- Growth rates mempunyai dasar yang relevan.
- OD dan vehicle composition tervalidasi.
- Geometri/control model layak.
- Independent validation tersedia.
- Forecast uncertainty dan limitations dapat dipertanggungjawabkan.

Jika syarat tidak terpenuhi, tulis:

**TECHNICAL PROJECTION ENGINE: PASS/PARTIAL**

**EMPIRICAL FORECAST VALIDITY: BLOCKED — BASELINE AND GROWTH EVIDENCE REQUIRED**

Jangan menggabungkan keduanya sebagai satu FULL PASS.

# 23. FINAL REPORT

Buat:

`MILESTONE_07_REPORT.md`

`MILESTONE_07_README.md`

Isi laporan:

1. Executive summary.
2. Technical projection status.
3. Empirical validity status.
4. Source audit.
5. Growth methodology.
6. Growth-rate provenance.
7. Vehicle-class growth model.
8. OD-specific growth model.
9. Formula dan perhitungan tahun.
10. Skenario LOW/REFERENCE/HIGH.
11. Output demand 2026, 2030, 2035, 2040.
12. Class/OD/interval conservation.
13. SUMO run results.
14. Route failure dan unserved demand.
15. Queue/travel-time/throughput analysis.
16. Spillback analysis.
17. Year comparisons.
18. Sensitivity and uncertainty.
19. Performance benchmark.
20. Internal browser screenshots.
21. SUMO-GUI evidence jika dilakukan.
22. Regression tests.
23. Reproducibility.
24. Known structural blockers.
25. Scientific limitations.
26. Acceptance criteria.
27. M08 readiness.

Sertakan demonstrasi bahwa pilihan tahun 2030/2035/2040 menghasilkan perubahan jumlah kendaraan yang sesuai rumus dan konfigurasi.

Jika proyeksi menghasilkan kemacetan berat atau demand tidak terlayani, jangan menganggapnya sebagai error yang harus disembunyikan.

Namun, jangan pula menganggapnya sebagai prediksi kemacetan nyata karena baseline belum dikalibrasi.

**JANGAN MEMULAI M08.**

MULAI MILESTONE 07 SEKARANG.

Fokus pada automatic year selection, growth model yang benar, perbedaan kendaraan/OD, actual SUMO simulation dan kualitas bukti.

Jangan mengejar tampilan visual yang spektakuler sebelum hasil perhitungan dapat diaudit.