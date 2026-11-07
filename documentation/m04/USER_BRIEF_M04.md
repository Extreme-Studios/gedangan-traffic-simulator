# MILESTONE 04 — GEDANGAN TRAFFIC SIMULATOR
## Vehicle System, Origin-Destination Matrix & Synthetic Traffic Demand

**MODEL: GPT-6.1 SOL — MEDIUM**

Lanjutkan Gedangan Traffic Simulator dari Milestone 1, 2, dan 3 yang sudah dikerjakan.

Kerjakan **MILESTONE 04 SAJA**. Jangan memulai M05 atau milestone berikutnya.

## 1. FOLDER PROYEK

Gunakan folder:

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

Baca laporan dan implementasi M01–M03 sebelum mulai.

Periksa:
- MILESTONE_03_REPORT.md
- MILESTONE_03_README.md
- NETWORK dan route test M03
- PROJECT_CHARTER.md
- ARCHITECTURE.md
- DATA_GOVERNANCE.md
- MILESTONE_ROADMAP.md
- Konfigurasi serta source-to-edge mapping M03

Jangan menghapus dataset, source code, atau dokumentasi milestone sebelumnya.

## 2. TUJUAN UTAMA

Membangun sistem kendaraan dan demand generator yang dapat menggerakkan berbagai jenis kendaraan pada jaringan SUMO Gedangan.

Kendaraan harus memiliki:
- ID unik.
- Vehicle class.
- Panjang dan lebar.
- Karakteristik akselerasi/deselerasi awal.
- Kecepatan maksimum.
- Waktu keberangkatan.
- Origin.
- Destination.
- Rute yang valid.
- Informasi sumber parameter.
- Status keberangkatan dan kedatangan.

Buat arsitektur yang siap mendukung kalibrasi, pertumbuhan kendaraan tahunan, dan berbagai skenario solusi pada milestone berikutnya.

## 3. KENDARAAN YANG HARUS DIDUKUNG

Implementasikan vehicle type registry dengan kategori:

1. Sepeda motor.
2. Mobil penumpang.
3. Pickup dan van.
4. Angkutan umum/minibus.
5. Bus.
6. Truk ringan.
7. Truk sedang.
8. Truk berat.
9. Trailer dan truk kontainer.
10. Kendaraan oversize/khusus.

Gunakan SUMO vClass yang sesuai, misalnya motorcycle, passenger, delivery, bus, truck, dan trailer.

Kategori lokal dan SUMO vClass harus dipetakan secara eksplisit. Jangan menganggap seluruh kategori memiliki vClass berbeda jika SUMO tidak menyediakannya.

Untuk setiap jenis, buat parameter:
- length
- width
- height jika didukung
- maxSpeed
- accel
- decel
- emergencyDecel
- minGap
- tau
- sigma
- car-following model
- lane-change model
- vehicle permissions

Periksa nama dan dukungan atribut terhadap SUMO 1.28.0 yang terpasang.

Nilai awal boleh berupa parameter teknis sementara untuk pengujian, tetapi setiap nilai wajib diberi status ASSUMPTION dan sumber atau alasan pemilihannya.

Jangan mengklaim dimensi atau karakteristik tersebut sudah dikalibrasi untuk kendaraan di Gedangan.

Kendaraan oversize harus memiliki pembatasan geometri dan legalitas rute. Jangan menganggap kendaraan besar dapat melewati seluruh jalan permukiman atau setiap persimpangan.

## 4. VEHICLE BEHAVIOR FOUNDATION

Gunakan sistem car-following dan lane-changing bawaan SUMO sebagai fondasi.

Jangan membangun ulang algoritma mikroskopis dari nol.

Persiapkan konfigurasi untuk:
- Jarak mengikuti kendaraan.
- Kecepatan.
- Akselerasi dan pengereman.
- Kebutuhan ruang kendaraan berat.
- Perpindahan jalur.
- Perilaku motor.

Perilaku detail lalu lintas Indonesia akan dikembangkan dan dikalibrasi pada M05/M06.

Untuk sepeda motor, evaluasi kemampuan SUMO Sublane Model secara terpisah.

Buat pengujian kecil untuk mengetahui apakah beberapa kendaraan roda dua dapat menempati area lateral yang memungkinkan pada sebuah lajur.

Jangan memaksakan sublane model aktif untuk seluruh jaringan jika performa belum terbukti.

Jangan mengaktifkan parameter perilaku agresif tanpa alasan atau bukti.

## 5. ORIGIN-DESTINATION MATRIX

Bangun sistem OD Matrix.

OD harus mencerminkan struktur perjalanan pada jaringan yang sudah tersedia.

Minimal kelompok pergerakan:

A. Sidoarjo menuju Surabaya.

B. Surabaya menuju Sidoarjo.

C. Jalan pengumpan menuju jalan utama.

D. Jalan utama menuju jalan pengumpan.

E. Perjalanan yang menggunakan frontage.

F. Perjalanan menuju kawasan stasiun atau area pengumpan sekitarnya.

G. Perjalanan antarkawasan lokal apabila rute tersedia.

Definisikan OD zone berdasarkan geometri dan edge pada M03.

Pisahkan:
- Geographic zone.
- Origin candidate edges.
- Destination candidate edges.
- Vehicle class eligibility.
- Network variant.
- Zone-to-edge assignment.
- Data confidence.
- Source/provenance.

Jangan menciptakan zona perjalanan baru tanpa keterkaitan dengan jaringan geografis.

Pemetaan zona dan distribusi perjalanan yang belum diketahui harus diberi label ASSUMPTION.

Pastikan origin dan destination merupakan edge yang valid dan dapat diakses oleh kelas kendaraan terkait.

Rute tidak boleh melawan arah jalan atau melewati koneksi yang diblokir.

## 6. TRAFFIC DEMAND GENERATOR

Buat generator kendaraan berdasarkan:
- OD Matrix.
- Vehicle composition.
- Departure interval.
- Demand profile.
- Traffic flow per interval.
- Seed deterministik.
- Network variant.
- Vehicle permissions.

Gunakan sistem SUMO trips/flows, DUAROUTER, dan od2trips bila sesuai dengan representasi OD yang dipilih.

Jangan langsung menggunakan randomTrips sebagai pendekatan utama karena kita membutuhkan OD yang terstruktur.

Semua data harus dapat direproduksi.

Buat tiga profil pengujian sintetis:

1. LOW TEST DEMAND
2. MEDIUM TEST DEMAND
3. STRESS TEST DEMAND

Ketiganya merupakan profil pengujian software, bukan volume aktual Gedangan.

Angka volume sintetis harus diletakkan dalam konfigurasi yang mudah diubah, disertai alasan pemilihan dan label SYNTHETIC.

Jangan membuat angka seolah-olah hasil survei jam sibuk.

Siapkan struktur untuk interval waktu 15 menit agar nanti kompatibel dengan data survei volume lalu lintas.

Jangan mengimplementasikan pertumbuhan kendaraan 2027–2040 pada M04. Itu dilakukan pada M07.

Namun, desain schema harus sudah mendukung baseline 2026 dan pertumbuhan berdasarkan tahun, OD, dan jenis kendaraan.

## 7. STRICT VS PROVISIONAL NETWORK

Gunakan kedua network hasil M03.

Strict:
- Hanya gunakan pergerakan yang didukung policy strict.
- Jangan memperbaiki rute dengan mengubah jaringan secara otomatis.
- Jika OD tidak dapat dirutekan, catat sebagai NOT_ROUTABLE.
- Jangan memaksakan 100% rute berhasil.

Provisional:
- Boleh digunakan untuk percobaan kendaraan lebih luas.
- Simpan seluruh status ASSUMPTION.
- Jangan menyatakan hasil provisional sebagai kondisi aktual.

Hasil kedua network harus dapat dibedakan.

Jangan membandingkan kinerja lalu lintas kedua varian sebagai bukti kebijakan sebelum perbedaan konektivitas dan input demand dikendalikan.

## 8. ROUTE GENERATION & VALIDATION

Gunakan SUMO 1.28.0 dari toolchain M02.

Untuk setiap demand batch:

1. Validasi OD.
2. Validasi kendaraan.
3. Validasi akses rute sesuai vehicle class.
4. Generate trips/flows.
5. Jalankan routing.
6. Simpan route files.
7. Periksa disconnected route.
8. Periksa invalid vehicle type.
9. Periksa invalid departure/destination.
10. Simpan kegagalan secara eksplisit.

Bedakan:
- Requested trips.
- Routable trips.
- Failed routes.
- Loaded vehicles.
- Departed vehicles.
- Arrived vehicles.
- Teleported vehicles.
- Vehicles pending insertion.

Jangan menghapus failed trips secara diam-diam hanya untuk membuat hasil tampak sukses.

Pertahankan log lengkap.

## 9. SIMULATION SMOKE TEST

Pada M04, izinkan simulasi kendaraan sintetis dalam SUMO untuk membuktikan sistem berfungsi.

Buat test kecil yang:
- Menggunakan network M03.
- Memuat vehicle types.
- Memuat trips/routes.
- Menjalankan sejumlah langkah simulasi.
- Memeriksa apakah kendaraan benar-benar berangkat.
- Memeriksa pergerakan kendaraan.
- Memeriksa kendaraan tiba.
- Memeriksa warning/error SUMO.

Lakukan pengujian pada koridor utama dua arah.

Lakukan pengujian kendaraan beragam ukuran, termasuk motor dan truk berat apabila rute valid.

Buktikan perubahan posisi atau progress kendaraan selama simulasi.

Jangan mengklaim model telah mereproduksi kemacetan nyata.

Gunakan seed tetap untuk tes regresi dan simpan konfigurasi SUMO yang dipakai.

Jika terjadi teleport, gagal berangkat, atau macet buatan akibat koneksi provisional, catat sebagai temuan.

## 10. FRONTAGE & HEAVY VEHICLE TEST

Buat tes khusus:

A. Kendaraan berjalan pada koridor utama Sidoarjo–Surabaya.

B. Kendaraan berjalan pada arah sebaliknya.

C. Kendaraan berjalan pada frontage yang memiliki rute valid.

D. Kendaraan dari feeder masuk ke jalan utama jika koneksi didukung.

E. Bus dan truk berat menguji kompatibilitas rute.

F. Kendaraan panjang menguji kelayakan konfigurasi sementara.

Perhatikan bahwa frontage menurut observasi pengguna relatif lancar.

Namun, jangan menerapkan angka kecepatan atau kelancaran tertentu sebagai fakta tanpa pengukuran.

Catat kemungkinan bottleneck dan konflik sebagai hipotesis untuk M05/M06.

## 11. OUTPUT DAN DATA GOVERNANCE

Buat struktur khusus:

`configuration/demand-m04/`

`simulation/demand/m04/`

`simulation/runs/m04/`

`documentation/m04/`

`tests/m04/` jika kompatibel dengan struktur tes yang ada.

Simpan:
- vehicle-types XML/JSON.
- OD zone definitions.
- OD matrix schema dan fixture.
- Demand configurations.
- Generated trips.
- Generated routes.
- Route validation results.
- SUMO test configurations.
- Run metrics.
- Simulation logs.
- Data provenance.
- Failure records.
- Run manifest dan hashes.

Pemisahan data:
- OBSERVED.
- RESEARCH_REFERENCE.
- ASSUMPTION.
- SYNTHETIC_TEST.
- SIMULATED_RESULT.

Jangan menulis data sintetis ke observed_data.

Setiap run harus memiliki ID, network hash, seed, SUMO version, konfigurasi demand, waktu simulasi, dan status validasi.

Pastikan seluruh output dapat dibangun ulang dari input yang sama.

## 12. INTERNAL BROWSER CODEX

Gunakan internal browser Codex sebagai tempat pemeriksaan visual utama.

Tambahkan halaman M04 yang terpisah dari viewer M03.

Tampilkan:
- Network variant.
- Vehicle classes.
- OD zones.
- OD connections.
- Traffic demand profile.
- Route status.
- Jumlah kendaraan sintetis yang diminta.
- Jumlah kendaraan yang berhasil dirutekan.
- Hasil smoke test SUMO.
- Status SUMO.

Jika memungkinkan, tampilkan playback terbatas dari hasil lintasan kendaraan yang benar-benar direkam dari SUMO.

Playback harus memakai data SUMO, bukan gerakan acak atau animasi kendaraan yang tidak sesuai rute.

Jika playback membutuhkan pengembangan yang terlalu luas, cukup sediakan viewer demand, route, dan hasil pengujian. Integrasi real-time penuh dijadwalkan untuk M09–M10.

Label secara jelas:

"SYNTHETIC TEST — NOT CALIBRATED GEDANGAN TRAFFIC".

Tetap pertahankan internal browser sebagai lingkungan utama.

## 13. PERFORMANCE

Perangkat target:
- Windows 11.
- RAM 16 GB.
- AMD GPU.
- VRAM target 6 GB.
- Resolusi 1080p.

Jangan langsung menguji ribuan kendaraan tanpa pengukuran.

Lakukan pengujian bertingkat dari demand kecil.

Pantau:
- Simulation runtime.
- Simulation speed atau time ratio.
- CPU usage jika dapat diukur.
- Peak RAM jika dapat diukur.
- Warning SUMO.
- Failed insertions.
- Teleport events.

Tidak perlu mengoptimasi render 3D skala besar. Itu masuk milestone lanjutan.

## 14. AUTOMATED TESTING

Buat tes untuk:
- Keunikan vehicle ID.
- Validitas vehicle class.
- Parameter kendaraan positif dan wajar secara teknis.
- Validitas OD zone.
- Validitas edge origin/destination.
- Kepatuhan arah rute.
- Kepatuhan lane permissions.
- Deterministic demand generation.
- Status provenance.
- Validitas route XML.
- Validitas data JSON.
- Penanganan route failure.
- Kedua arah koridor utama.
- Pemisahan frontage.
- Heavy vehicle eligibility.
- Regression terhadap M01–M03.

Jalankan:
- Unit tests.
- SUMO smoke tests.
- TypeScript check.
- Frontend production build.
- Internal browser QA.

Jangan menyembunyikan kegagalan.

## 15. BATASAN

Jangan memulai:
- Kalibrasi lalu lintas aktual.
- Simulasi perilaku motor Indonesia tingkat lanjut.
- Perlintasan kereta dinamis.
- Pengaturan lampu lalu lintas final.
- Perbandingan solusi flyover.
- Proyeksi pertumbuhan tahunan.
- Dashboard analitik final.
- Dunia 3D realistis.
- Presentasi final.

Semua pekerjaan tersebut berada pada milestone berikutnya.

Jangan memodifikasi jaringan M03 secara diam-diam untuk membuat kendaraan berjalan.

Jika masalah jaringan muncul, buat issue register M03 dan dokumentasikan dampaknya.

## 16. ACCEPTANCE CRITERIA

M04 dianggap berhasil apabila:

1. Semua kategori kendaraan mempunyai definisi yang valid.
2. Vehicle type registry memiliki provenance.
3. OD zone dan OD Matrix terstruktur.
4. Demand generator dapat berjalan.
5. Demand sintetis dapat direproduksi.
6. Routing menghormati arah jalan dan vehicle permissions.
7. Dua arah koridor utama berhasil diuji dengan kendaraan yang sesuai.
8. Frontage diuji secara terpisah.
9. SUMO menjalankan simulasi kendaraan sintetis.
10. Keberangkatan, pergerakan, dan kedatangan dapat diverifikasi.
11. Route failures tidak disembunyikan.
12. Strict dan provisional tetap terpisah.
13. Browser internal menampilkan hasil M04.
14. Automated tests dan build lulus.
15. Source M01–M03 tetap utuh.
16. Tidak ada klaim kondisi lalu lintas aktual yang belum terkalibrasi.

## 17. LAPORAN AKHIR

Buat:

`MILESTONE_04_REPORT.md`

Isi wajib:
- Ringkasan pekerjaan.
- Struktur source code.
- Daftar vehicle types.
- Parameter dan provenance.
- OD zones.
- OD Matrix dan fixture.
- Demand generation.
- Strict/provisional results.
- Route success/failure.
- Jumlah requested/departed/arrived vehicles.
- Hasil smoke test.
- SUMO-GUI evidence.
- Internal browser evidence.
- Performance observations.
- Automated test results.
- Limitasi data.
- Isu jaringan yang ditemukan.
- Rekomendasi M05.
- Acceptance criteria satu per satu.

Buat pula MILESTONE_04_README.md yang menjelaskan cara menjalankan, membangun ulang, dan menguji hasil M04.

Jangan melanjutkan M05 tanpa persetujuan pengguna.

**MULAI MILESTONE 04 SEKARANG.**

Prioritaskan kebenaran demand, konsistensi asal–tujuan, legalitas rute, dan kemampuan reproduksi hasil dibandingkan visual yang menarik.