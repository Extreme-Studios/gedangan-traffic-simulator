# MILESTONE 08 — GEDANGAN TRAFFIC DIGITAL TWIN
## Solution Scenario Engine, Traffic Intervention Modeling & Comparative Evaluation

**MODEL: GPT-6.1 SOL — MEDIUM**

Lanjutkan proyek Gedangan Traffic Simulator dari M01 sampai M07.

**KERJAKAN MILESTONE 08 SAJA. JANGAN MEMULAI M09.**

M08 harus membangun mesin simulasi untuk membandingkan berbagai solusi kemacetan Gedangan secara objektif, termasuk pengaturan lampu lalu lintas, manajemen akses, optimalisasi frontage, pengaturan kendaraan berat, flyover, dan underpass.

Jangan menetapkan flyover sebagai solusi terbaik sebelum hasil pengujian mendukungnya.

**ATURAN UTAMA: setiap intervensi wajib diuji menggunakan perhitungan SUMO yang sebenarnya, dengan demand dan kondisi pembanding yang terkendali. Tidak boleh membuat peningkatan performa palsu melalui perubahan rute ilegal, penghapusan kendaraan, atau manipulasi hasil.**

---

# 1. PROJECT DIRECTORY

Gunakan:

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

Baca dan audit implementasi aktual:

- MILESTONE_03_REPORT.md
- MILESTONE_04_REPORT.md
- MILESTONE_04_5_REPORT.md
- MILESTONE_05_REPORT.md
- MILESTONE_05_1_REPORT.md
- MILESTONE_06_REPORT.md
- MILESTONE_07_REPORT.md
- Project architecture.
- Data governance.
- M04 vehicle registry dan OD.
- M04.5 corrected access policies.
- M05 railway dan signal systems.
- M05.1 causal spillback detector.
- M06 calibration readiness dan structural blockers.
- M07 growth projection, scenarios, run results, comparison engine dan manifests.

Jangan berasumsi semua fitur dalam laporan bekerja tanpa memeriksa source code.

Sebelum implementasi:
1. Jalankan 234 regression tests M07.
2. Simpan baseline SHA-256.
3. Audit dependensi SUMO 1.28.0.
4. Periksa hasil actual SUMO M07.
5. Periksa keterbatasan struktur jaringan.
6. Inventarisasi pending issues.
7. Buat execution plan M08 yang terukur.

Jangan mengubah atau menimpa sumber M01–M07.

# 2. SELESAIKAN PENDING BROWSER QA M07

M07 mempunyai status PARTIAL karena final internal browser QA belum selesai.

Sebelum membangun UI M08, lakukan final QA terhadap:

- Pemilihan tahun 2026–2040.
- Pemilihan LOW/REFERENCE/HIGH.
- Custom growth scenario.
- Penyimpanan custom scenario.
- Actual run initiation.
- Cache dan run status.
- Comparison.
- Recorded playback.
- NOT RUN state.
- Desktop 1920×1080.
- Mobile 390×844.
- Browser console.

M07 menggunakan port 5182 dan API 8772.

Jangan menulis ulang browser M07.

Jika internal browser tersedia, lakukan pemeriksaan langsung dan simpan screenshot serta log.

Jika browser dinonaktifkan oleh lingkungan Work/Codex, jangan mengubah setting keamanan, mengklaim pengujian berhasil, atau membangun ulang UI tanpa alasan.

Catat status BLOCKED_BY_ENVIRONMENT dengan bukti, lalu lanjutkan backend M08.

Buat dokumen `M07_BROWSER_QA_CLOSURE.md`.

# 3. TARGET UTAMA M08

Bangun **Solution Scenario Engine** yang dapat:

1. Menggunakan baseline jaringan Gedangan.
2. Membuat skenario intervensi.
3. Memilih tahun 2026–2040.
4. Memilih demand LOW/REFERENCE/HIGH/custom.
5. Menguji setiap skenario menggunakan SUMO.
6. Menggunakan kendaraan dan OD yang konsisten.
7. Membandingkan baseline dengan intervensi.
8. Mengukur perubahan antrean dan waktu perjalanan.
9. Memeriksa spillback.
10. Memeriksa pengaruh terhadap frontage dan feeder.
11. Memeriksa keselamatan interaksi rel dan jalan.
12. Menganalisis keterbatasan dan dampak samping.
13. Menyimpan hasil yang reproducible.
14. Menampilkan perbandingan di internal browser.
15. Menyiapkan fondasi analisis solusi sampai 2040.

Status semua pengujian saat ini:

**SYNTHETIC / CONDITIONAL TRAFFIC EXPERIMENT — NOT AN EMPIRICALLY VALIDATED GEDANGAN FORECAST.**

Baseline M06 masih belum terkalibrasi berdasarkan data lapangan 2026.

Tidak boleh menaikkan statusnya menjadi empirical baseline hanya karena M08 berhasil menghasilkan angka perbandingan.

# 4. SCENARIO CATALOG

Buat katalog intervensi dengan scenario IDs yang stabil.

## S00 — BASELINE / NO INTERVENTION

Gunakan jaringan dan kontrol M07 yang dipilih tanpa perubahan solusi.

Ini menjadi pembanding utama.

Catat:
- Network hash.
- Demand hash.
- Signal control.
- Railway operation.
- Vehicle permissions.
- Seed.
- Measurement period.
- Model assumptions.

## S01 — TRAFFIC SIGNAL TIMING OPTIMIZATION

Uji alternatif pengaturan lampu lalu lintas pada simpang yang sudah mempunyai controller valid.

Variabel:
- Green duration.
- Yellow duration.
- All-red.
- Cycle length.
- Phase allocation.
- Offset jika didukung.
- Approach-specific demand.

Pertahankan clearance dan keselamatan fase.

Jangan mengizinkan conflicting green yang berbahaya.

Jangan menganggap sinyal sintetis M05 merupakan pengaturan lampu aktual Gedangan.

Buat parameter search yang terbatas, dapat diaudit, dan tidak berlebihan.

Pisahkan skenario tuning menggunakan demand latihan dari evaluasi pada demand/seed yang tidak dipakai untuk memilih program sinyal.

Jangan mengoptimasi signal timing dengan cara yang hanya menguntungkan satu arah dan mengabaikan pendekat lainnya.

## S02 — TURNING MOVEMENT & ACCESS MANAGEMENT

Uji intervensi berupa:
- Restriksi belok tertentu.
- Pengaturan akses jalan pengumpan.
- Pengaturan konflik pergerakan simpang.
- Perbaikan distribusi arus pada koneksi yang memang tersedia.

Hanya gunakan gerakan yang mempunyai dasar source topology.

Jangan mengizinkan U-turn atau belokan ilegal.

Jika skenario menutup suatu gerakan, kendaraan yang sebelumnya menggunakan gerakan itu harus:
- Mendapat rute alternatif legal berdasarkan graph yang valid; atau
- Dilaporkan sebagai reroute failure/unserved demand.

Jangan menghapus permintaan perjalanan tersebut.

## S03 — FRONTAGE ACCESS MANAGEMENT

Frontage road sudah ada pada kondisi geografis sumber.

Jangan membuat frontage baru sebagai kondisi baseline.

Jangan menganggap frontage merupakan sumber masalah hanya karena letaknya paralel dengan jalan utama.

Uji:
- Pengaturan akses masuk.
- Pengaturan akses keluar.
- Konflik merge.
- Pembatasan kelas kendaraan sesuai policy.
- Pemisahan perjalanan lokal versus through traffic.
- Pengaruh terhadap jalan utama dan feeder.

Jangan membuat sambungan frontage-main yang tidak ada pada source topology.

Apabila suatu alternatif membutuhkan akses fisik baru, klasifikasikan sebagai PROPOSED INFRASTRUCTURE dan jangan menyamakannya dengan pengaturan akses existing.

Observasi pengguna bahwa frontage relatif lancar merupakan catatan kualitatif, bukan target kecepatan numerik.

## S04 — HEAVY VEHICLE MANAGEMENT

Uji alternatif pengaturan kendaraan berat:

- Time-window restrictions.
- Class-specific access restrictions.
- Freight-routing policy pada jaringan legal yang tersedia.
- Pembatasan sementara pergerakan kendaraan tertentu.
- Alternatif akses hanya jika rute valid.

Jangan memindahkan truk ke jalan lokal yang tidak mengizinkan kendaraan berat.

Jangan menghilangkan demand truk dari total permintaan.

Jika truk tidak bisa diberangkatkan akibat pembatasan, tampilkan akibat tersebut secara eksplisit.

Skenario pembatasan waktu harus membedakan:
- Demand deferred.
- Demand served.
- Demand displaced outside the measurement window.
- Demand unserved.

Jangan menganggap penundaan perjalanan sebagai pengurangan kemacetan tanpa biaya atau dampak.

## S05 — SIGNAL COORDINATION / CORRIDOR MANAGEMENT

Jika terdapat dua atau lebih controller yang benar-benar valid pada network, uji koordinasi fase dan offset.

Jika controller lain belum siap, jangan mengarang lampu lalu lintas tambahan.

Boleh membuat control fixture terpisah untuk membuktikan mekanisme koordinasi, tetapi jangan memberi label bahwa koridor Gedangan telah terkoordinasi secara aktual.

Prioritaskan validitas network.

## S06 — FLYOVER CONCEPT

Buat candidate flyover sebagai **konsep infrastruktur hipotetis**, bukan desain konstruksi final.

Analisis:
- Tujuan flyover.
- Arus kendaraan yang dialihkan.
- Lokasi kandidat.
- Arah perjalanan.
- Kebutuhan ramp.
- Akses jalan yang dipertahankan.
- Interaksi dengan simpang.
- Interaksi dengan rel.
- Frontage connectivity.
- Vehicle eligibility.
- Konsekuensi terhadap feeder.
- Potensi pemindahan bottleneck.
- Kebutuhan lahan.
- Dampak terhadap bangunan dan akses warga.
- Kebutuhan studi struktur/clearance.

Jika membuat network turunan:
- Gunakan grade separation yang eksplisit.
- Jangan menghubungkan jalan dan rel hanya karena bertumpuk secara horizontal.
- Jangan membiarkan kendaraan berpindah dari flyover ke jalan di bawahnya tanpa ramp.
- Jangan membuat ramp yang tidak realistis hanya agar routing berhasil.
- Jangan menghapus persimpangan existing tanpa memodelkan akses yang harus dipertahankan.
- Jangan memalsukan geometri elevasi atau clearance.

Perhitungan panjang ramp, kelandaian dan kebutuhan ruang harus berdasarkan asumsi desain yang terlihat jelas dan dinyatakan sebagai engineering concept, bukan hasil survei.

Jika informasi geometri, ROW/lahan, atau topology tidak cukup untuk membangun flyover yang dapat dipertanggungjawabkan, sediakan **CONCEPT_ONLY / NOT SIMULATION_READY**.

Jangan memaksakan network runnable dengan koneksi rekaan.

## S07 — UNDERPASS CONCEPT

Evaluasi kandidat underpass dengan standar yang setara dengan flyover.

Periksa:
- Lokasi dan orientasi kandidat.
- Jalan yang dilalui.
- Rel dan persimpangan.
- Akses menuju ruas existing.
- Kebutuhan ramp.
- Perubahan elevasi.
- Jarak bebas kendaraan.
- Potensi konflik frontage.
- Drainase dan risiko genangan.
- Utilitas bawah tanah.
- Kebutuhan pompa jika relevan.
- Pembebasan lahan.
- Biaya konstruksi dan pemeliharaan.
- Dampak saat konstruksi.

Jangan menganggap underpass otomatis lebih murah atau lebih efektif daripada flyover.

Jangan menetapkan elevasi tanah, muka air tanah, utilitas, clearance, atau biaya sebagai fakta tanpa sumber.

Jika data tidak mencukupi, status **CONCEPT_ONLY / NEEDS ENGINEERING SURVEY**.

# 5. TWO-LEVEL SCENARIO ARCHITECTURE

Pisahkan katalog menjadi dua jenis.

## A. OPERATIONAL SCENARIOS

Intervensi yang dapat dijalankan berdasarkan jaringan existing:
- Signal timing.
- Valid access restrictions.
- Freight management.
- Existing frontage management.
- Valid control coordination.

Boleh menjalankan eksperimen SUMO langsung jika seluruh dependensi teknis valid.

## B. INFRASTRUCTURE CONCEPTS

Intervensi yang membutuhkan jaringan baru:
- Flyover.
- Underpass.
- New ramps.
- New access connections.
- Road widening atau geometric redesign.

Jangan memberi label SIMULATION_READY sebelum:
- Topologi kandidat lengkap.
- Road permissions benar.
- Ramp/access mapping jelas.
- Conflict geometry jelas.
- Grade separation benar.
- Perubahan terhadap jaringan dapat diaudit.
- Model tidak membuat akses secara diam-diam.

Status yang harus didukung:
- DRAFT.
- CONCEPT_ONLY.
- STRUCTURALLY_BLOCKED.
- SIMULATION_READY_PROVISIONAL.
- SIMULATED.
- NEEDS_FIELD_VERIFICATION.

Konsep tidak boleh dianggap lebih efektif hanya berdasarkan gambar ilustrasi.

# 6. NETWORK DERIVATIVE ENGINE

Setiap skenario memiliki:

- Scenario ID.
- Version.
- Parent network hash.
- Scenario network hash.
- Intervention type.
- Parameter changes.
- Source provenance.
- Assumptions.
- Affected edges.
- Affected junctions.
- Added edges jika ada.
- Removed/restricted movements.
- Vehicle permissions.
- Railway interaction.
- Validation status.

Buat scenario builder yang menghasilkan derivative network tanpa mengubah original M03/M04.5/M05/M05.1/M07.

Gunakan NETCONVERT untuk perubahan network sesuai kemampuan SUMO 1.28.0.

Audit:
- Node consistency.
- Edge geometry.
- Lane connections.
- Oneway.
- Allowed/disallowed vClass.
- Turn restrictions.
- Road-rail separation.
- Level crossings.
- Source-to-edge lineage.
- Network component changes.
- Route reachability.

Untuk operational scenario, jangan mengubah geometri bila tidak diperlukan.

Untuk infrastructure scenario, setiap perubahan topologi harus dijelaskan, dan harus jelas mana geometri sumber serta mana desain hipotetis.

# 7. RAILWAY SAFETY

Railway pilot M05 dan M05.1 harus dipertahankan.

Jangan menonaktifkan rail crossing hanya untuk memperlancar kendaraan.

Jangan mengatur lampu kereta secara tidak aman.

Jika flyover/underpass secara konsep menggantikan perlintasan sebidang:
- Pastikan grade separation secara topologis benar.
- Pastikan akses yang tersisa tetap terhubung.
- Pastikan rail operations tidak terganggu.
- Pastikan road vehicles tidak memasuki railway lane.
- Pastikan tidak ada road-rail conflict karena network bug.

Jika crossing tidak benar-benar digantikan pada skenario, built-in rail crossing harus tetap bekerja.

Jangan menyebut eliminasi penutupan palang sebagai manfaat tanpa mengimplementasikan jaringan pemisahan yang valid.

# 8. SCENARIO TEST MATRIX

Dukung tahun:
- 2026.
- 2030.
- 2035.
- 2040.
- Custom 2027–2039.

Demand scenarios:
- LOW.
- REFERENCE.
- HIGH.
- Custom jika dikonfigurasi.

Vehicle classes:
- Semua kategori M04 yang valid.
- Oversize tetap dibatasi.

Network families:
- Strict jika skenario kompatibel.
- Corrected Provisional.
- Railway/Signal Pilot.

Jangan langsung menjalankan seluruh kombinasi apabila biaya komputasinya besar.

Prioritas eksperimen:

**PHASE 1**
- S00 baseline 2026.
- S01 traffic signal 2026.
- S02 turning/access 2026 jika perubahan legal.
- S03 frontage access 2026 jika feasible.
- S04 heavy vehicle management 2026 jika feasible.

**PHASE 2**
- Ulangi operational scenarios pada 2030 dan 2040.
- Gunakan setidaknya dua seed untuk comparison terpilih.
- 2035 disiapkan dan dijalankan sebagai representative test apabila resource memadai.

**PHASE 3**
- Uji infrastructure concept yang benar-benar lolos network feasibility.
- Jika belum lolos, hasilnya adalah feasibility register, bukan angka performa palsu.

Semua fase harus mempunyai log pekerjaan, hasil dan status.

# 9. FAIR BASELINE COMPARISON

Ini bagian paling penting dalam M08.

Untuk membandingkan S00 dan intervensi:

Gunakan:
- Tahun sama.
- Demand scenario sama.
- Source demand cohort sama.
- OD request set sama.
- Vehicle-class composition sama.
- Departure schedule sama.
- Measurement horizon sama.
- Seed policy sama.
- Railway events sama kecuali memang variabel intervensi yang diuji.
- Signal control sama kecuali intervensi mengubah signal.
- Metrik dan definisi sama.

Network hash boleh berbeda karena intervensi memang mengubah network.

Namun, model harus membuktikan bahwa perbedaannya memang berasal dari intervention manifest.

Jangan membuat comparison guard yang selalu menolak network berbeda, karena infrastructure interventions memang membutuhkan perubahan network.

Sebaliknya, jangan menerima perbedaan jaringan yang tidak dijelaskan.

Sediakan:
- Input parity audit.
- Network change audit.
- Cohort parity audit.
- Intervention isolation audit.
- Output completeness audit.

Jika demand rerouted oleh suatu solusi, pertahankan origin/destination dan identitas cohort.

Jika suatu kendaraan menjadi tidak dapat dirutekan, laporkan sebagai unserved, bukan menghilangkannya.

# 10. TRAFFIC METRICS

Gunakan SUMO actual outputs dan TraCI jika perlu.

Per skenario, hitung:

## Travel Performance
- Requested vehicles.
- Routable vehicles.
- Failed routes.
- Departed.
- Arrived.
- Running at end.
- Not departed.
- Throughput.
- Travel time.
- Waiting time.
- Time loss.
- Depart delay.

## Congestion
- Queue length in meters.
- Queue vehicle count.
- Queue duration.
- Maximum stopped vehicles.
- Lane occupancy.
- Queue tail.
- Spillback episodes verified in model.
- Unresolved congestion events.

## Road Segments
- Main Sidoarjo → Surabaya.
- Main Surabaya → Sidoarjo.
- Frontage.
- Feeder.
- Gedangan junction.
- Ketajen.
- Station crossing.
- Upstream/downstream links.

## Safety Diagnostics
- Collisions.
- Emergency braking indicators jika valid.
- Illegal movements.
- Road-rail conflicts.
- Teleports.
- Heavy-vehicle access violations.
- Geometry and clearance warnings.

Collision=0 dalam SUMO bukan bukti keselamatan fisik atau sertifikasi desain.

Gunakan metric definitions yang konsisten dengan M05.1 dan M07.

# 11. CENSORING & UNSERVED DEMAND

Jangan menghitung hanya kendaraan arrived.

Jika 2040 menghasilkan demand tinggi:
- Tetap catat kendaraan yang gagal routing.
- Tetap catat pending insertion.
- Tetap catat running-at-end.
- Tetap catat trip yang tidak selesai.
- Tetap catat perbedaan cohort antarskenario.

Gunakan fixed measurement horizon yang dapat dibandingkan.

Optional drain horizon harus dilaporkan terpisah.

Jangan menambah horizon hanya untuk satu skenario supaya semua kendaraan tiba.

Jangan menggunakan perubahan rata-rata waktu perjalanan arrived-only sebagai bukti solusi membaik jika kendaraan yang paling terlambat belum tiba.

Laporkan hasil dengan censoring warning.

Jika perlu, tampilkan incomplete-journey lower bounds dan distribusi keterlambatan dengan definisi yang tepat.

# 12. SCENARIO EVALUATION FRAMEWORK

Bangun evaluation engine multi-kriteria.

Dimensi:

A. Traffic performance.
B. Queue/spillback reduction.
C. Road safety indicators.
D. Implementation feasibility.
E. Land requirements.
F. Construction cost.
G. Maintenance cost.
H. Railway operational impact.
I. Community and access impact.
J. Environmental and construction disruption.
K. Robustness until 2040.
L. Data confidence.

Jangan mencampur simulated traffic metrics dengan biaya atau kebutuhan lahan yang tidak memiliki bukti.

Gunakan tiga kelas evidence:

1. QUANTIFIED_SIMULATED.
2. QUALITATIVE_SCREENING.
3. UNKNOWN_REQUIRES_STUDY.

Biaya yang belum didukung sumber harus tetap UNKNOWN.

Jangan mengarang estimasi rupiah.

Kebutuhan pembebasan lahan yang belum diukur tetap UNKNOWN.

Untuk flyover/underpass, tambahkan technical feasibility checklist dan risk register.

# 13. MULTI-CRITERIA COMPARISON

Sediakan perbandingan:
- Baseline versus each intervention.
- Operational versus infrastructure concepts.
- 2026 versus 2040.
- LOW versus HIGH demand.
- Main arterial versus frontage impacts.

Jangan memilih pemenang tunggal dengan menjumlah angka yang unitnya berbeda secara sembarangan.

Jika membuat weighted scoring:
- Bobot harus eksplisit.
- User dapat mengubah bobot.
- Metrik unknown tidak otomatis menjadi nilai nol.
- Tampilkan sensitivity terhadap bobot.
- Tampilkan Pareto/non-dominated scenarios jika dapat dihitung.
- Pisahkan ranking berdasarkan traffic performance saja dari overall feasibility.

Jika data penting hilang, tampilkan:
**NO DEFENSIBLE OVERALL WINNER WITH CURRENT EVIDENCE.**

Sebuah opsi boleh memperbaiki perjalanan Sidoarjo→Surabaya tetapi memperburuk feeder/frontage.

Trade-off seperti ini wajib terlihat.

# 14. FRONTAGE-SPECIFIC CHECKS

Perhatikan fakta bahwa frontage sudah tersedia.

Jangan mengklaim pembangunan frontage baru sebagai solusi jika yang dimaksud adalah jalan existing.

Uji:
- Existing frontage baseline.
- Access management changes.
- Merge conflicts.
- Local trip accessibility.
- Heavy vehicle permissions.
- Changes in main corridor volume.
- Queue migration to feeder.
- Travel-time impact across OD.

Jika main arterial membaik tetapi frontage memburuk, laporkan keduanya.

Jangan menyembunyikan pemindahan kemacetan dari satu ruas ke ruas lain.

# 15. FLYOVER & UNDERPASS FEASIBILITY GATE

Buat feasibility analysis terpisah.

Minimal audit:

1. Relevant road corridors.
2. Intersections affected.
3. Railway interaction.
4. Existing buildings and road access.
5. Ramp connection feasibility.
6. Elevation assumptions.
7. Required clearance.
8. Approximate footprint from explicit assumptions.
9. Road/rail construction conflict.
10. Drainage and flood exposure.
11. Utility relocation uncertainty.
12. Land ownership/ROW data availability.
13. Construction disruption.
14. Long-term maintenance.
15. Emergency access.
16. Pedestrian/motorcycle/local access.
17. Heavy vehicle swept-path uncertainty.
18. Permitting and authority requirements.

Hasil harus berupa:
- Feasibility status.
- Evidence register.
- Missing surveys.
- Conceptual constraints.
- Blocking issues.
- Modelability status.

Jangan mengarang hasil survei geoteknik, elevasi, ROW, atau dampak sosial.

Bila informasi belum cukup, pertahankan sebagai concept dan jangan memalsukan traffic effectiveness.

# 16. SCENARIO ENGINE & REPRODUCIBILITY

Buat scenario specification JSON dengan schema validation.

Isi:
- Scenario ID/version.
- Parent baseline.
- Intervention manifest.
- Year.
- Growth scenario.
- Demand hash.
- Network hash.
- Control hash.
- Registry hash.
- Railway configuration.
- Vehicle composition.
- Seed.
- Measurement window.
- Analysis version.
- Run status.
- Validation status.

Buat run manager dengan:
- Queue.
- Bounded concurrency.
- Caching.
- Checkpoints.
- Retry yang aman.
- Failure ledger.
- Reproducibility check.

Target Windows 11, 16 GB RAM, AMD GPU 6 GB VRAM.

Jangan menjalankan semua kombinasi secara paralel.

SUMO headless runs diutamakan untuk batch experiments.

Gunakan internal browser untuk visualisasi dan inspeksi.

# 17. INTERNAL BROWSER — SOLUTION COMPARISON LAB

Buat halaman baru:

**GEDANGAN TRAFFIC SOLUTION LAB**

Jangan merusak viewer M07.

Sediakan:

## A. Scenario Selector
- S00 Baseline.
- S01 Signal.
- S02 Turning/access.
- S03 Frontage.
- S04 Heavy vehicle.
- S05 Coordination.
- S06 Flyover concept.
- S07 Underpass concept.

## B. Year Selector
- 2026.
- 2030.
- 2035.
- 2040.
- Custom year.

## C. Growth Selector
- LOW.
- REFERENCE.
- HIGH.
- Custom.

## D. Comparison Mode

Pilih baseline dan intervention.

Tampilkan berdampingan:
- Requested.
- Served.
- Arrived.
- Waiting.
- Travel time.
- Queue.
- Spillback.
- Frontage impact.
- Feeder impact.
- Safety diagnostics.

Jangan membuat dua simulasi yang berbeda input cohort lalu menampilkan selisihnya sebagai efek intervensi murni.

## E. Interactive Map

Tampilkan:
- Main arterial.
- Frontage.
- Feeder.
- Station/crossing.
- Traffic signals.
- Railways.
- Intervention locations.
- Added/removed network elements.
- Queue and spillback indicators.

Untuk flyover/underpass concept-only, tampilkan sebagai layer konseptual, bukan kendaraan yang seolah-olah benar-benar memakai infrastruktur tersebut.

## F. Recorded Playback

Jika ada actual SUMO run:
- Play.
- Pause.
- Reset.
- Speed.
- Timeline.
- Camera orbit/zoom.
- Vehicle type filters.
- Before/after playback.

Semua posisi kendaraan harus berasal dari actual SUMO outputs.

## G. Feasibility Panel

Tampilkan:
- Intervention status.
- Source confidence.
- Land requirements.
- Engineering blockers.
- Cost status.
- Railway issues.
- Community impacts.
- Uncertainty.

## H. Recommendation Panel

Boleh menampilkan:
- Best traffic performance under selected synthetic assumptions.
- Pareto candidates.
- Trade-offs.
- Evidence limitations.

Jangan otomatis menulis:
"Flyover merupakan solusi terbaik bagi Gedangan."

Jika evidence belum cukup, tampilkan:
**NO VERIFIED POLICY RECOMMENDATION — BASELINE NOT EMPIRICALLY CALIBRATED.**

# 18. ACTUAL RUN BUTTON

Jika menyediakan tombol Run Simulation:
- Harus memanggil backend lokal yang nyata.
- Harus mengantrekan SUMO job valid.
- Harus menampilkan progress/status.
- Harus menangani errors.
- Harus memuat result setelah selesai.
- Harus memisahkan cached dan fresh runs.

Jika suatu skenario concept-only tidak mempunyai valid executable network, tombol Run harus dinonaktifkan dengan alasan yang jelas.

Jangan memakai animasi loading lalu menampilkan angka palsu.

# 19. OPTIONAL SOLUTION EXPERIMENTS

Jika fondasi utama sudah stabil, evaluasi tambahan:

- Restricted turning movement.
- Freight time shifting.
- Existing frontage flow management.
- Signal optimization with queue fairness.
- Railway closure interaction sensitivity.
- Increased demand stress test.
- Progressive scenario combination.

Jangan membuat kombinasi intervensi otomatis tanpa memisahkan efek individual.

Combined interventions adalah eksperimen tersendiri.

Jangan mengklaim efek S01 + S03 selalu sama dengan penjumlahan manfaat masing-masing.

# 20. EXPERIMENTAL DESIGN & ROBUSTNESS

Untuk pasangan eksperimen yang valid:

- Gunakan demand cohort yang sama.
- Gunakan minimal dua seed pada perbandingan utama.
- Jangan tuning parameter berdasarkan seed evaluasi.
- Catat measurement horizon dan warm-up.
- Pertahankan fixed railway schedule untuk perbandingan operasional yang tidak mengubah rel.
- Pertahankan vehicle permissions kecuali merupakan intervensi eksplisit.
- Pertahankan baseline network source.
- Pastikan intervention change set diketahui.

Jika baseline high-demand menyebabkan unfinished trips, jangan memaksa traffic performance comparison tanpa censoring diagnostics.

Stress test bukan validasi empiris.

# 21. PROJECT STRUCTURE

Buat modul terpisah sesuai arsitektur aktual.

Usulan:

`backend/gedangan/m08_scenarios.py`

`backend/gedangan/m08_network.py`

`backend/gedangan/m08_interventions.py`

`backend/gedangan/m08_runner.py`

`backend/gedangan/m08_comparison.py`

`backend/gedangan/m08_feasibility.py`

`backend/gedangan/m08_evaluation.py`

`backend/gedangan/m08_reporting.py`

`configuration/scenarios-m08/`

`simulation/network/m08/`

`simulation/runs/m08/`

`simulation/comparisons/m08/`

`documentation/m08/`

`frontend/solutions.html`

`frontend/src/m08/`

`tests/m08/`

Buat:

`START_SOLUTIONS_M08.bat`

`REBUILD_SOLUTIONS_M08.bat`

Gunakan port terpisah dan pertahankan launcher lama.

# 22. AUTOMATED TESTS

Pertahankan seluruh 234 regression tests M07.

Tambahkan tes untuk:

1. Scenario schema.
2. Scenario versioning.
3. Baseline immutability.
4. Valid network derivative.
5. Controlled network changes.
6. Source-to-edge lineage.
7. Turn restriction preservation.
8. Vehicle access permissions.
9. Heavy-vehicle constraints.
10. Frontage separation.
11. Railway safety.
12. Signal phase safety.
13. Signal timing modification.
14. OD cohort parity.
15. Demand conservation.
16. Rerouting and route failures.
17. Unserved demand.
18. Censored run accounting.
19. Intervention isolation.
20. Actual SUMO simulation.
21. Queue/travel-time measurement.
22. Spillback classification.
23. Negative scenario comparisons.
24. Unknown cost treatment.
25. Unknown land data treatment.
26. Infrastructure concept gating.
27. Flyover grade-separation topology checks.
28. Underpass grade-separation topology checks.
29. No invented ramp connections.
30. Feasibility statuses.
31. Comparison fairness.
32. Multi-criteria scoring safeguards.
33. Multiple seed handling.
34. Cache and checkpoint.
35. Browser scenario selection.
36. Browser actual run/result state.
37. Browser concept-only state.
38. Reproducibility.
39. Original files preserved.

Jangan membuat tes hanya untuk memastikan nama skenario muncul di UI.

Harus ada actual SUMO tests yang membuktikan intervensi operasional menghasilkan mekanisme kontrol/pergerakan berbeda dari baseline, serta accounting kendaraan lengkap.

Hasil yang tidak membaik tetap dianggap eksperimen valid apabila metodologi dan output benar.

# 23. ACCEPTANCE CRITERIA — TECHNICAL ENGINE

M08 technical engine dinyatakan PASS apabila:

1. M07 browser QA ditutup atau blocker lingkungan terdokumentasi.
2. Scenario catalog tersedia.
3. Baseline S00 dapat dijalankan.
4. Minimal tiga skenario operasional yang benar-benar feasible dapat dijalankan; jika tidak feasible, status parsial dijelaskan.
5. Scenario builder tidak mengubah jaringan original.
6. Network derivative dapat diaudit.
7. Vehicle legality tetap dijaga.
8. Railway safety tetap bekerja.
9. Demand cohort parity terbukti.
10. SUMO menjalankan before/after experiments.
11. Tidak ada dropped trips tersembunyi.
12. Travel time/queue/spillback berasal dari SUMO.
13. Censoring ditangani.
14. Comparison fairness berfungsi.
15. Class/OD/feeder/frontage impacts terlihat.
16. Tahun 2026, 2030, 2035, 2040 dapat dipilih.
17. Feasibility framework berfungsi.
18. Flyover concept mempunyai status kelayakan yang jujur.
19. Underpass concept mempunyai status kelayakan yang jujur.
20. Tidak ada biaya atau data lahan rekaan.
21. Internal browser menampilkan hasil dan keterbatasan.
22. Semua regression tests lulus.
23. Rebuild reproducible.
24. M01–M07 source tetap utuh.

# 24. ACCEPTANCE — ENGINEERING FEASIBILITY

Pisahkan dari technical engine.

Flyover/underpass tidak boleh dinyatakan engineering-feasible atau layak dibangun tanpa data memadai tentang:
- Topografi/elevasi.
- Ruang bebas dan geometri ramp.
- ROW/lahan.
- Utilitas.
- Tanah dan fondasi.
- Drainase/banjir.
- Operasi perkeretaapian.
- Dampak akses warga.
- Biaya dan kelayakan konstruksi.
- Persetujuan instansi terkait.

Jika belum tersedia, tulis:

**INFRASTRUCTURE ENGINEERING FEASIBILITY: NOT VERIFIED — SURVEY AND DESIGN REQUIRED.**

Ini tidak menghalangi pembuatan conceptual simulation tools, tetapi menghalangi klaim kelayakan fisik.

# 25. ACCEPTANCE — POLICY RECOMMENDATION

Jangan memberi rekomendasi final kebijakan Gedangan sebelum:

1. Baseline 2026 terkalibrasi dengan observasi.
2. OD dan traffic counts tervalidasi.
3. Geometri dan controls yang relevan terverifikasi.
4. Skenario comparable.
5. Future growth assumptions mempunyai justifikasi.
6. Dampak dan ketidakpastian dievaluasi.
7. Biaya, keselamatan dan kelayakan fisik relevan tersedia.

Jika belum terpenuhi:

**POLICY RECOMMENDATION: NOT YET DEFENSIBLE.**

Hasil M08 tetap dapat memperlihatkan opsi yang lebih baik di dalam simulasi sintetis, dengan batasan yang jelas.

# 26. PERFORMANCE

Target perangkat:
- Windows 11.
- RAM 16GB.
- AMD GPU target 6GB VRAM.
- Internal browser 1080p.

Gunakan:
- Sequential bounded execution.
- Cache manifests.
- Reproducible seeds.
- Incremental runs.
- Run-time monitoring.
- CPU/RAM monitoring jika tersedia.

Jangan menghabiskan resource untuk seluruh combinatorial experiment matrix sekaligus.

Jangan mengejar dunia 3D realistis pada M08; itu tugas M10.

# 27. FINAL REPORT

Buat:

`MILESTONE_08_REPORT.md`

`MILESTONE_08_README.md`

Isi laporan wajib:

1. Executive summary.
2. Technical acceptance status.
3. M07 browser QA closure.
4. Scenario catalog.
5. Scenario design methodology.
6. Baseline setup.
7. Operational intervention models.
8. Flyover conceptual feasibility.
9. Underpass conceptual feasibility.
10. Network lineage dan derivative audit.
11. Demand cohort parity.
12. SUMO simulation matrix.
13. Before/after comparison.
14. Travel time results.
15. Queue results.
16. Spillback results.
17. Frontage impacts.
18. Feeder impacts.
19. Heavy-vehicle impacts.
20. Railway and crossing safety.
21. Safety diagnostics.
22. Censoring/unserved results.
23. Multi-criteria evaluation.
24. Pareto/trade-off findings jika didukung.
25. Growth year comparisons.
26. Sensitivity and uncertainty.
27. Performance.
28. Internal browser screenshots.
29. Regression tests.
30. Reproducibility.
31. Source immutability.
32. Engineering blockers.
33. Empirical limitations.
34. Acceptance criteria satu per satu.
35. M09 readiness.

Tampilkan tabel perbandingan baseline dan intervensi untuk setidaknya tahun 2026 dan 2040 pada skenario yang berhasil dijalankan.

Jangan mengarang data untuk skenario yang belum dapat dijalankan.

Skenario yang tidak feasible atau tidak memiliki cukup sumber harus tetap terlihat dalam katalog dengan status yang benar.

# 28. WORKFLOW RULES

- Tetap di folder proyek.
- Jangan memulai M09.
- Jangan mengubah laporan milestone lama.
- Gunakan SUMO 1.28.0 lokal.
- Gunakan Codex internal browser sebagai preview utama.
- Jangan menginstal dependency baru kecuali benar-benar diperlukan.
- Jangan mengubah source OSM untuk mempercantik skenario.
- Jangan membuat rute ilegal.
- Jangan memalsukan geometri flyover/underpass.
- Jangan menyebut angka biaya tanpa sumber.
- Jangan menyembunyikan dampak buruk intervensi.
- Jangan menilai solusi berdasarkan satu metrik saja.
- Jangan memaksa satu solusi menang.
- Jangan menyebut hasil sintetis sebagai prediksi kemacetan nyata.
- Jika pendekatan yang sama gagal berulang 2–3 kali, audit akar masalah dan hentikan pengulangan yang tidak produktif.

**MULAI MILESTONE 08 SEKARANG.**

Prioritas M08:

1. Tutup QA M07 yang tertunda.
2. Bangun Solution Scenario Engine.
3. Jalankan eksperimen operasional yang benar-benar valid.
4. Bangun feasibility gate untuk flyover dan underpass.
5. Lakukan perbandingan yang adil berdasarkan SUMO.
6. Tampilkan hasil di internal browser.
7. Simpan semua bukti dan laporan.

**TUJUAN AKHIR: kita harus dapat membandingkan berbagai opsi penanganan kemacetan Gedangan secara transparan, tanpa menganggap suatu intervensi pasti terbaik sebelum didukung data dan hasil pengujian yang sah.**