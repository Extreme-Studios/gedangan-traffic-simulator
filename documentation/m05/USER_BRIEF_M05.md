# MILESTONE 05 — GEDANGAN TRAFFIC SIMULATOR
## Mixed Traffic Behavior, Traffic Signals, Railway Integration & Queue Spillback

**MODEL: GPT-6.1 SOL — MEDIUM**

Lanjutkan proyek Gedangan Traffic Simulator dari M01, M02, M03, M04, dan M04.5.

**KERJAKAN MILESTONE 05 SAJA.**

Jangan melanjutkan M06 sebelum mendapatkan persetujuan pengguna.

---

## 1. PROJECT DIRECTORY

Gunakan:

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

Sebelum memulai:

1. Baca laporan M03, M04, dan M04.5.
2. Audit source code dan konfigurasi aktual.
3. Periksa jaringan corrected Strict dan Provisional M04.5.
4. Periksa registry kendaraan dan OD Matrix M04.
5. Periksa kemampuan SUMO 1.28.0.
6. Jalankan pemeriksaan regresi awal.
7. Catat status dan keterbatasan yang diwarisi.

Jangan menghapus atau menimpa pekerjaan sebelumnya.

## 2. OBJECTIVE

Membangun model perilaku lalu lintas campuran, persimpangan bersinyal, perlintasan kereta dinamis, dan mekanisme antrean yang dapat merambat antar-ruas.

M05 harus membuktikan bahwa:

- Kendaraan berinteraksi secara mikroskopis.
- Kendaraan mengikuti lampu lalu lintas.
- Kendaraan berhenti ketika perlintasan kereta ditutup.
- Kereta dapat melintas melalui jaringan rel yang valid.
- Kendaraan kembali bergerak setelah perlintasan aman dibuka.
- Antrean dapat terbentuk, bertambah, berkurang, dan jika kondisinya memungkinkan merambat ke ruas hulu.
- Dampak tersebut diukur berdasarkan output simulasi SUMO, bukan animasi buatan.

Seluruh hasil saat ini masih **SYNTHETIC TEST — NOT CALIBRATED GEDANGAN TRAFFIC**.

## 3. SUMO ENGINE

Gunakan SUMO portable 1.28.0 yang sudah terpasang.

Komponen:
- SUMO.
- SUMO-GUI.
- NETCONVERT.
- NETEDIT.
- Python.
- TraCI.
- sumolib.

Gunakan built-in microscopic simulation SUMO sebagai mesin perhitungan utama.

Jangan mengimplementasikan ulang car-following, lane-changing, traffic signals, atau train priority dari nol apabila sudah tersedia fitur SUMO yang dapat digunakan.

Verifikasi seluruh opsi CLI, atribut XML, dan API TraCI terhadap versi 1.28.0 lokal.

## 4. NETWORK FOUNDATION

Gunakan corrected networks M04.5 sebagai baseline immutable.

Bangun varian turunan M05 untuk:
- Perilaku kendaraan.
- Persimpangan bersinyal.
- Perlintasan kereta.
- Pengujian antrean.

Pertahankan:
- Source OSM ID.
- Node dan edge lineage.
- Geometri jalan asli.
- Main arterial dan frontage sebagai jaringan terpisah.
- Kebijakan akses multiclass.
- Oneway dan turn restrictions.
- Data provenance.
- Parameter missing dan assumptions.

Jangan menyambungkan jalan yang tidak terhubung hanya untuk memudahkan simulasi.

Jika penambahan infrastruktur rel memerlukan perubahan topologi, buat turunan eksplisit M05. Catat semua node, rail edge, crossing node, koneksi, dan perubahan yang dilakukan.

Jangan mengubah jaringan M03/M04.5 asli.

## 5. MIXED TRAFFIC BEHAVIOR

Gunakan sepuluh kategori registry M04:

1. Motorcycle.
2. Passenger car.
3. Pickup/van.
4. Minibus.
5. Bus.
6. Light truck.
7. Medium truck.
8. Heavy truck.
9. Trailer/container.
10. Oversize vehicle.

Oversize tetap diblokir sampai persyaratan fisik dan legalitas terpenuhi.

### Car-following

Gunakan Krauss sebagai baseline dan parameter M04 yang sudah tersedia.

Evaluasi:
- Kecepatan.
- Acceleration.
- Deceleration.
- Minimum gap.
- Reaction time.
- Braking behavior.
- Following distance.
- Perbedaan karakteristik kendaraan ringan dan berat.

Jangan langsung mengganti seluruh parameter M04.

Buat behavioral profile turunan yang memiliki provenance dan status ASSUMPTION.

### Motorcycle sublane

Buat eksperimen SL2015 menggunakan lateral-resolution yang kompatibel.

Uji:
- Posisi lateral motor.
- Dua motor dalam satu lajur jika secara geometris memungkinkan.
- Motor bergerak di samping kendaraan lain.
- Perpindahan lateral.
- Clearance lateral.
- Konflik dengan kendaraan besar.
- Waktu komputasi.

Jangan mengasumsikan motor selalu menyelip agresif.

Jangan mengaktifkan nilai lcPushy atau perilaku berbahaya tanpa dasar pengujian.

Bandingkan regular lane-changing dengan sublane model.

Jika seluruh jaringan Gedangan belum cocok untuk sublane, lakukan eksperimen terkontrol dan dokumentasikan batasnya.

## 6. TRAFFIC SIGNAL SYSTEM

Bangun model traffic signal untuk lokasi persimpangan Gedangan yang dapat dipetakan dan mempunyai konektivitas memadai.

Prioritaskan:
- Simpang utama Gedangan.
- Persimpangan sekitar Stasiun Gedangan.
- Simpang penghubung yang memengaruhi antrean.

Periksa source traffic-signal nodes M02 dan final SUMO connections M04.5.

Jangan menganggap setiap OSM traffic-signal node merupakan satu controller independen.

### Signal program

Buat configurable signal programs:
- Green.
- Yellow.
- Red.
- All-red clearance bila diperlukan.
- Cycle length.
- Phase duration.
- Phase offset.
- Signal group.
- Controlled connections.

Jangan menggunakan cycle time dari asumsi sebagai kondisi aktual 2026.

Buat scenario configuration dengan label SYNTHETIC.

Periksa signal link indices dan conflict movements sebelum memberikan green phase.

Gerakan kendaraan yang saling berkonflik tidak boleh diberi prioritas bersamaan tanpa aturan yield yang benar.

Perhatikan sistem lalu lintas kiri Indonesia.

### Pengujian

Buktikan:
1. Kendaraan berhenti saat red.
2. Kendaraan bergerak saat green.
3. Pergantian fase berjalan benar.
4. Tidak ada conflicting green yang tidak aman.
5. Antrean terbentuk ketika arus masuk melebihi arus yang dilepas.
6. Antrean dapat berkurang setelah fase green.

Simpan actual traffic light phase log dan vehicle movement evidence.

## 7. RAILWAY NETWORK INTEGRATION

Ini bagian yang sangat penting.

M03 masih menyimpan rel sebagai overlay statis.

Pada M05, evaluasi apakah rel dapat dibuat sebagai jaringan kereta SUMO yang terhubung secara topologis dan georeferensi dengan perlintasan jalan.

Gunakan dataset M02:
- Rail geometries.
- Station Gedangan.
- Level crossing source nodes.
- Source railway tags.
- Crossing candidates.

### Railway topology audit

Sebelum membangun:
1. Identifikasi lokasi perlintasan fisik yang dapat dibedakan.
2. Periksa shared nodes sumber.
3. Periksa konektivitas segmen rel.
4. Periksa klasifikasi rel.
5. Periksa grade separation.
6. Jangan menganggap 11 crossing nodes berarti 11 palang fisik.
7. Jangan mengarang jumlah track aktual.

Pilih satu lokasi perlintasan yang mempunyai bukti geografis dan topologi paling layak sebagai pilot.

### Railway network construction

Jika data mendukung, buat:
- Railway edges.
- Railway lanes.
- Train-compatible connections.
- Railway route.
- Train vehicle definition.
- Rail crossing node/controller.
- Train movement scenario.

Gunakan vClass railway yang sesuai dengan SUMO 1.28.0.

Pastikan kereta tidak berjalan pada road lane dan kendaraan jalan tidak menggunakan railway lane.

Gunakan node type rail_crossing serta mekanisme prioritas kereta bawaan SUMO jika sesuai.

Jangan sekadar menampilkan objek kereta melewati perlintasan tanpa interaksi dengan arus jalan.

Jika integrasi ke jaringan Gedangan tidak memungkinkan tanpa perubahan yang tidak terverifikasi, buat railway-crossing fixture terpisah yang jelas diberi label synthetic isolated test.

Dalam kasus tersebut, tandai integrasi dinamis Gedangan sebagai PARTIAL, bukan PASS.

## 8. RAILWAY CROSSING BEHAVIOR

Bangun railway crossing control dengan parameter konfigurasi:
- Train approach detection.
- Crossing closure.
- Warning phase.
- Minimum safety gap.
- Train priority.
- Opening delay.
- Reopening.
- Consecutive train handling.
- Road vehicle queue formation.

Gunakan mekanisme SUMO rail_crossing jika dapat diimplementasikan secara benar.

Jadwal dan frekuensi kereta belum boleh diklaim sebagai jadwal aktual Gedangan.

Gunakan jadwal uji sintetis:
- No train.
- Single train passing.
- Two trains with separated arrivals.
- Consecutive trains with short gap.
- Longer closure duration, hanya jika didukung mekanisme aman dan konfigurasi jelas.

Buat event log untuk setiap crossing:
- Train ID.
- Approach time.
- Closure time.
- Train entry.
- Train exit.
- Reopen time.
- Actual road vehicle stop.
- Actual queue formation.

Pisahkan status simulated event dari asumsi jadwal.

### Acceptance

Buktikan:
1. Kereta mempunyai valid route.
2. Kereta benar-benar bergerak.
3. Perlintasan mempunyai kontrol aktif.
4. Kendaraan tidak melintasi crossing ketika kereta mendapat hak prioritas.
5. Kendaraan mengantre.
6. Kendaraan bergerak kembali setelah crossing dibuka.
7. Tidak terjadi konflik road–rail pada test.
8. Event tersimpan dalam log.

Jangan menganggap lampu merah statis sebagai bukti implementasi kereta dinamis.

## 9. QUEUE FORMATION & SPILLBACK

Bangun measurement system untuk:
- Queue length.
- Queue vehicle count.
- Stopped vehicles.
- Waiting time.
- Travel time.
- Speed reduction.
- Edge occupancy.
- Lane occupancy.
- Queue growth.
- Queue dissipation.
- Queue spillback.

Gunakan output SUMO dan/atau TraCI.

Evaluasi E2 lane-area detectors, queue output, tripinfo, lane data dan vehicle state.

Verifikasi dukungan fitur pada SUMO lokal.

### Spillback definition

Jangan menyebut setiap antrean panjang sebagai spillback.

Spillback dinyatakan terjadi apabila ada bukti antrean mencapai atau menghambat ruang hilir yang dibutuhkan pergerakan dari ruas/persimpangan hulu, sehingga mengganggu arus upstream.

Buat indikator:
- Queue tail position.
- Downstream occupancy.
- Upstream blocked movement.
- Duration.
- Affected edges.
- Maximum observed queue extent.

Jika antrean mencapai batas jaringan, catat sebagai boundary censoring dan jangan mengklaim panjang antrean sebenarnya sudah terukur.

### Experiment

Lakukan eksperimen demand sintetis bertingkat.

Gunakan OD dan vehicle composition yang sama untuk paired comparisons jika sedang mengevaluasi efek perubahan kontrol.

Skenario pengujian:
A. Tanpa gangguan.
B. Dengan traffic signal.
C. Dengan penutupan crossing kereta.
D. Dengan permintaan kendaraan meningkat.
E. Dengan dua gangguan yang berdekatan.
F. Dengan potensi antrean merambat ke simpang lain.

Jangan memaksakan hasil spillback dengan memindahkan posisi kendaraan secara manual.

Jika jaringan Gedangan tidak menghasilkan spillback dengan setup yang valid, catat hasil negatifnya.

Boleh menggunakan synthetic isolated fixture untuk membuktikan algoritma deteksi spillback, tetapi jangan mengklaim hal tersebut sebagai bukti spillback aktual di Gedangan.

## 10. CONTROLLED COMPARISON

Untuk eksperimen yang membandingkan skenario:

- Gunakan network yang sebanding.
- Gunakan demand, OD dan vehicle composition identik jika ingin mengisolasi efek satu variabel.
- Gunakan seed yang terdokumentasi.
- Gunakan warm-up dan measurement window yang sama.
- Jalankan pengulangan dengan beberapa seed bila memungkinkan.
- Laporkan variasi hasil.
- Catat teleports, collisions, uninserted demand, dan failed routes.
- Jangan menghitung hanya kendaraan yang tiba lalu mengabaikan kendaraan yang tertahan.

Tampilkan hasil keseluruhan, termasuk kegagalan dan keterbatasan.

Tujuannya menguji mekanisme software, belum menyimpulkan efektivitas kebijakan Gedangan.

## 11. TRAFFIC ANALYTICS FOUNDATION

Buat output data terstruktur:

- Per-vehicle trajectory.
- Vehicle class.
- Speed.
- Acceleration jika tersedia.
- Waiting time.
- Trip duration.
- Queue events.
- Signal phase changes.
- Railway crossing states.
- Train movement.
- Spillback events.
- Run summary.

Simpan:
- Measurement definitions.
- Units.
- Sampling interval.
- Scenario ID.
- Network hash.
- Demand hash.
- SUMO version.
- Seed.
- Provenance.
- Validation status.

Bedakan:
OBSERVED, RESEARCH_REFERENCE, ASSUMPTION, SYNTHETIC_TEST dan SIMULATED_RESULT.

Jangan memasukkan hasil simulasi sintetis ke observed_data.

## 12. INTERNAL BROWSER CODEX

Gunakan internal browser sebagai preview utama.

Buat halaman M05 terpisah tanpa merusak viewer M04.5.

Tampilkan:

### A. Network View
- Jalan utama.
- Frontage.
- Persimpangan.
- Rel.
- Crossing.
- Kendaraan.

### B. Vehicle Behavior
- Vehicle type.
- Position.
- Speed.
- Waiting.
- Movement state.

### C. Traffic Signal
- Current phase.
- Green/red state.
- Signal controller.
- Signal timeline.

### D. Railway
- Train position.
- Train route.
- Crossing open/closed state.
- Event timeline.

### E. Congestion
- Queue length.
- Waiting time.
- Stopped vehicles.
- Spillback detection.
- Affected road segments.

### F. Playback
- Play.
- Pause.
- Reset.
- Speed control.
- Timeline scrub.
- Camera orbit/zoom.
- Layer visibility.

Playback harus berasal dari recorded SUMO outputs.

Jangan membuat animasi lalu lintas atau perlintasan palsu untuk mengisi data yang belum tersedia.

Real-time interactive TraCI control dan dunia 3D realistis tetap target milestone selanjutnya. M05 cukup menyediakan recorded playback yang valid.

Tampilkan label:
**SYNTHETIC TRAFFIC EXPERIMENT — NOT CALIBRATED TO GEDANGAN 2026.**

Jika sebuah fitur hanya berhasil pada isolated fixture, tampilkan statusnya secara eksplisit.

## 13. SUMO-GUI EVIDENCE

Buka hasil simulasi pada SUMO-GUI.

Periksa secara visual:
- Motor dan kendaraan besar.
- Lampu lalu lintas.
- Kendaraan berhenti.
- Kendaraan bergerak kembali.
- Kereta dan crossing, jika integrasi berhasil.
- Pembentukan antrean.

Ambil screenshot dari state aktual SUMO.

Jangan menggunakan screenshot ilustrasi atau render terpisah sebagai bukti mesin berjalan.

## 14. PERFORMANCE

Target komputer:
- Windows 11.
- RAM 16 GB.
- AMD GPU dengan VRAM target 6 GB.
- Resolusi 1080p.

Uji secara bertahap.

Catat:
- Runtime.
- CPU usage jika terukur.
- Peak RAM jika terukur.
- Simulation speed ratio.
- Jumlah kendaraan aktif.
- Jumlah kendaraan menunggu insertion.
- Teleport count.
- Collision count.
- Warning/error.
- Dampak sublane terhadap waktu komputasi.

Jangan melakukan stress test ribuan kendaraan tanpa tahapan dan observabilitas.

Jika komputer mengalami resource pressure, hentikan pengujian dan dokumentasikan.

## 15. PROJECT STRUCTURE

Buat modul terpisah:

`backend/gedangan/m05_behavior.py`

`backend/gedangan/m05_signals.py`

`backend/gedangan/m05_railway.py`

`backend/gedangan/m05_queues.py`

`configuration/behavior-m05/`

`configuration/signals-m05/`

`configuration/railway-m05/`

`simulation/network/m05/`

`simulation/runs/m05/`

`frontend/behavior.html`

`frontend/src/m05/`

`documentation/m05/`

`tests/m05/`

Sesuaikan dengan arsitektur aktual proyek apabila diperlukan.

Buat launcher:

`START_BEHAVIOR_M05.bat`

Dan rebuild script:

`REBUILD_BEHAVIOR_M05.bat`

Gunakan port lokal tersendiri dan jangan mengganggu launcher milestone sebelumnya.

## 16. AUTOMATED TESTING

Tambahkan test untuk:
- Vehicle registry compatibility.
- Multiclass movement.
- Motorcycle sublane.
- Signal state transitions.
- Signal controlled-link consistency.
- Red-light stopping.
- Green-light release.
- Train route validity.
- Train movement.
- Rail crossing closure.
- Crossing reopening.
- No road–rail conflict.
- Queue calculation.
- Spillback event detection.
- Trip accounting.
- FCD consistency.
- Provenance.
- Reproducibility.
- Source immutability.
- M01–M04.5 regression.

Jangan membuat unit test yang hanya memeriksa flag keberhasilan tanpa menjalankan atau memvalidasi fenomena yang diklaim.

Pertahankan negative tests yang memang seharusnya gagal.

Jalankan:
- Python tests.
- SUMO integration tests.
- TypeScript checks.
- Vite production build.
- Internal browser QA.
- SUMO-GUI inspection.

## 17. ACCEPTANCE CRITERIA

M05 baru dinyatakan FULL PASS apabila:

1. Multiclass traffic berjalan sesuai izin jaringan.
2. Motorcycle sublane berhasil diuji.
3. Traffic signal yang valid berfungsi.
4. Red-light stopping terbukti.
5. Green-light release terbukti.
6. Railway network Gedangan pilot berhasil dibangun dengan sumber geometri yang jelas.
7. Kereta benar-benar bergerak pada jaringan pilot.
8. Railway crossing aktif dan terkendali.
9. Kendaraan berhenti ketika crossing ditutup.
10. Kendaraan bergerak kembali setelah crossing aman.
11. Queue metrics berasal dari SUMO.
12. Antrean dapat terbentuk dan mengurai.
13. Spillback detector teruji, serta kondisi terjadi/tidak terjadi pada jaringan Gedangan dilaporkan jujur.
14. Perbandingan eksperimen menggunakan input terkontrol.
15. Viewer internal menampilkan recorded results.
16. SUMO-GUI memperlihatkan mekanisme yang berhasil.
17. Automated tests dan build lulus.
18. Hasil dapat direproduksi.
19. Data M01–M04.5 tidak rusak.
20. Tidak ada klaim kondisi lalu lintas nyata tanpa validasi.

Jika integrasi rel Gedangan tidak berhasil tetapi isolated railway fixture lulus, status keseluruhan wajib PARTIAL.

Jangan menyatakan FULL PASS hanya berdasarkan keberhasilan fixture terisolasi.

Jika satu acceptance criterion tidak terpenuhi, laporkan secara transparan, lengkap dengan sebab dan usulan remediasi.

## 18. REPORTING

Buat:

`MILESTONE_05_REPORT.md`

Dan:

`MILESTONE_05_README.md`

Laporan wajib memuat:
1. Executive summary.
2. Status PASS / PARTIAL / FAIL.
3. Perubahan source code.
4. Network lineage.
5. Vehicle behavior results.
6. Motorcycle sublane evaluation.
7. Traffic signal configuration.
8. Railway topology evidence.
9. Train/crossing actual run results.
10. Queue and spillback results.
11. Experiment comparisons.
12. SUMO-GUI screenshots.
13. Internal browser screenshots.
14. Performance results.
15. Build and regression tests.
16. Missing data dan asumsi.
17. Limitasi ilmiah.
18. Unresolved issues.
19. Acceptance criteria satu per satu.
20. Kesiapan menuju M06.

Simpan semua log dan konfigurasi eksperimen.

Jangan memalsukan, memperkirakan, atau melengkapi hasil testing yang belum dilakukan.

## 19. WORKFLOW RULES

- Tetap di folder proyek.
- Jangan mengubah milestone lama.
- Jangan menginstal software tambahan jika tools lokal yang ada sudah cukup.
- Gunakan SUMO built-in features.
- Hindari kode duplikatif.
- Utamakan modularitas.
- Semua data asumsi harus terlacak.
- Jangan menonaktifkan validasi untuk memaksa test PASS.
- Jika menemukan bug yang sama 2–3 kali, berhenti mengulang pendekatan dan analisis akar masalah. Eskalasi ke Astra Pro jika perlu.
- Jangan memulai M06.

**MULAI MILESTONE 05 SEKARANG.**

Prioritas tertinggi adalah membuktikan interaksi kendaraan, lampu lalu lintas, kereta, dan pembentukan antrean melalui perhitungan SUMO yang sebenarnya. Keindahan visual belum menjadi prioritas.