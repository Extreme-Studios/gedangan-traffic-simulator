# MILESTONE 03 — GEDANGAN TRAFFIC NETWORK ENGINE
## Geographic Road Network Conversion & SUMO Network Validation

Lanjutkan proyek Gedangan Traffic Simulator dari Milestone 1 dan 2 yang sudah selesai dan disetujui.

Kerjakan MILESTONE 03 SAJA.

## 1. FOLDER PROYEK

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

Baca:
- MILESTONE_01_REPORT.md
- MILESTONE_02_REPORT.md
- README.md
- ARCHITECTURE.md
- DATA_GOVERNANCE.md
- dokumentasi M02
- DATA_QUALITY_REPORT.md
- ROAD_INVENTORY.md

Periksa implementasi aktual, jangan hanya mengandalkan laporan.

Jangan menghapus, menimpa, atau mengubah dataset mentah M02.

Pastikan seluruh hasil M03 dapat dilacak ke data sumber M02.

## 2. TUJUAN UTAMA

Mengubah jaringan geografis Gedangan menjadi jaringan transportasi yang dapat dijalankan oleh Eclipse SUMO.

Jaringan mencakup:

1. Koridor utama Sidoarjo–Surabaya.
2. Koridor Surabaya–Sidoarjo.
3. Frontage road.
4. Jalan pengumpan.
5. Collector roads.
6. Local access roads yang relevan.
7. Persimpangan Gedangan.
8. Persimpangan sekitar Stasiun Gedangan.
9. Akses dan konektor jalan.
10. Posisi jalur rel dan perlintasan kereta.

Prioritas tertinggi adalah konektivitas koridor utama Sidoarjo–Surabaya.

Frontage harus tetap menjadi jaringan terpisah yang terhubung melalui akses yang benar-benar tersedia.

## 3. SUMO ENVIRONMENT

Gunakan instalasi yang sudah tersedia:

`toolchain/sumo-win64-1.28.0/`

Periksa helper environment M02, termasuk SUMO_ENV_M02.bat.

Pastikan:
- SUMO 1.28.0.
- SUMO_HOME.
- NETCONVERT.
- NETEDIT.
- SUMO-GUI.
- TraCI.
- sumolib.

Jangan menginstal versi kedua jika versi M02 masih berfungsi.

Gunakan executable dan tools dari versi yang sama.

## 4. PEMBANGUNAN NETWORK

Buat pipeline konversi yang reproducible.

Gunakan data lokal M02 sebagai sumber utama:
- geodata/raw/gedangan-network.json
- geodata/roads/all_roads.geojson
- dataset main arterial.
- dataset frontage.
- dataset feeders.
- junctions.
- railway crossings.
- access points.

Periksa skema aktual setiap dataset sebelum membuat converter.

Gunakan NETCONVERT dan/atau proses konversi berbasis Python yang mempertahankan identitas node dan way sumber.

Jangan membuat node atau menyambungkan jalan hanya berdasarkan kedekatan visual.

Setiap perubahan konektivitas harus mempunyai alasan dan provenance.

## 5. NETWORK ARCHITECTURE

Buat struktur jaringan yang memisahkan:

A. Main Arterial Network
- Arah Sidoarjo menuju Surabaya.
- Arah Surabaya menuju Sidoarjo.
- Koneksi pendekat persimpangan.
- Koneksi jalan pengumpan.

B. Frontage Network
- Geometri frontage tersendiri.
- Akses masuk.
- Akses keluar.
- Titik merge.
- Koneksi ke jaringan utama.

C. Feeder Network
- Sukodono.
- Ketajen.
- Santren.
- Nangka.
- Rajawali.
- Jalan penghubung lainnya yang tersedia pada dataset.

D. Junction Network
- Simpang utama Gedangan.
- Simpang sekitar Stasiun Gedangan.
- Koneksi antarpendekat.
- Koneksi antarjalan.

E. Railway Infrastructure
- Geometri rel.
- Lokasi perlintasan.
- Hubungan spasial jalan dan rel.
- Metadata crossing.

Jangan menjalankan simulasi kereta pada M03. Operasi kereta dan interaksi dinamis dengan kendaraan akan dikembangkan pada milestone berikutnya.

## 6. PENANGANAN DATA YANG BELUM LENGKAP

Ini bagian yang sangat penting.

Laporan M02 mencatat:
- 1.220 segmen belum memiliki informasi lanes.
- 1.408 segmen belum memiliki informasi width.
- 1.403 segmen belum memiliki maxspeed.
- 1.187 segmen belum memiliki oneway.
- Seluruh segmen belum memiliki kapasitas terukur.

Jangan mengisi semua kekosongan dengan angka default tanpa dokumentasi.

Buat tiga kategori:

1. VERIFIED
   Informasi yang didukung sumber data.

2. INFERRED
   Informasi yang berasal dari aturan atau interpretasi sumber yang terdokumentasi.

3. ASSUMPTION
   Parameter sementara yang diperlukan mesin simulasi.

Buat dua varian jaringan bila diperlukan:

A. STRICT NETWORK

Hanya menggunakan konektivitas arah yang dapat dipertanggungjawabkan.

B. PROVISIONAL NETWORK

Mengizinkan parameter sementara yang terdokumentasi, dengan asumsi terpisah untuk arah, jumlah lajur, dan kecepatan.

Pastikan hasil keduanya tidak dicampur atau dianggap sama tingkat validasinya.

Untuk arah perjalanan:
- Pertahankan tag oneway eksplisit.
- Periksa aturan default OSM secara terdokumentasi.
- Jangan otomatis menganggap semua ruas tanpa tag sebagai dua arah.
- Jangan membuat koneksi belok yang tidak didukung data.
- Catat setiap edge yang dikecualikan atau diinferensikan.

Untuk lanes dan speed:
- Pertahankan nilai sumber yang tersedia.
- Jika menggunakan typemap bawaan SUMO, catat file, versi, dan nilai yang diterapkan.
- Tandai semua nilai yang berasal dari default sebagai asumsi.
- Jangan menyebut asumsi sebagai hasil survei.

## 7. JUNCTION DAN CONNECTION VALIDATION

Periksa:
- Node yang tidak terhubung.
- Edge yang terputus.
- Duplikasi edge.
- Arah edge.
- Koneksi antar-lajur.
- Koneksi antar-junction.
- Konflik koneksi belok.
- Turn restrictions.
- U-turn restrictions.
- Akses privat.
- Grade separation.
- Bridge dan tunnel.
- Dead-end.
- Boundary edges.
- Komponen jaringan yang terisolasi.

Perhatikan khusus 29 komponen yang ditemukan pada M02.

Jangan menyambungkan komponen hanya untuk membuat jaringan terlihat utuh.

Setiap perbaikan harus mempunyai referensi geografis atau bukti sumber.

## 8. ROUTE CONNECTIVITY TEST

Buat pengujian rute kendaraan pada jaringan yang dihasilkan.

Prioritas pengujian:

1. Sidoarjo menuju Surabaya.
2. Surabaya menuju Sidoarjo.
3. Jalan pengumpan menuju jalan utama.
4. Jalan utama menuju jalan pengumpan.
5. Frontage menuju akses yang tersedia.
6. Koneksi simpang Gedangan.
7. Koneksi simpang sekitar stasiun.

Gunakan routing tools SUMO, misalnya DUAROUTER, sesuai kemampuan versi 1.28.0.

Buat fixture pengujian terpisah.

Untuk setiap rute catat:
- Starting edge.
- Destination edge.
- Daftar edge yang dilewati.
- Arah perjalanan.
- Status route found atau not found.
- Alasan kegagalan.
- Status validasi.

Jangan membuat rute palsu ketika koneksi sebenarnya tidak tersedia.

Rute yang menggunakan asumsi harus diberi label provisional.

## 9. SUMO-GUI DAN NETEDIT

Buka jaringan hasil konversi melalui:

- SUMO-GUI.
- NETEDIT.

Verifikasi secara langsung:
- Jalan utama.
- Frontage.
- Jalan pengumpan.
- Persimpangan.
- Arah jalan.
- Koneksi edge.
- Posisi perlintasan.
- Boundary network.

Pastikan file network dapat dibuka tanpa fatal error.

Simpan screenshot hasil pemeriksaan.

Jika GUI tidak dapat dibuka karena keterbatasan desktop, dokumentasikan dan jangan mengklaim pemeriksaan visual berhasil.

## 10. INTERNAL BROWSER CODEX

Internal browser tetap menjadi preview utama aplikasi.

Buat tampilan network inspection yang membaca hasil ekspor jaringan SUMO.

Tampilkan:
- Nodes.
- Edges.
- Lane direction.
- Main arterial.
- Frontage.
- Feeders.
- Junctions.
- Railway crossing.
- Network connectivity.
- Edge attributes.
- Data provenance.
- Status verified, inferred, assumption, dan missing.

Sediakan layer visibility dan pemilihan edge.

Pengguna harus dapat mengklik sebuah ruas dan melihat:
- Edge ID.
- Source OSM way ID.
- From node.
- To node.
- Jumlah lajur.
- Kecepatan.
- Arah.
- Status data.
- Sumber informasi.

Jangan membuat data baru hanya untuk memperindah tampilan.

Browser digunakan untuk memvisualisasikan dan menginspeksi network, bukan menjalankan executable SUMO di dalam browser.

## 11. OUTPUT FILES

Buat struktur output M03 yang rapi dan tidak merusak M02.

Minimal hasilkan:

- Network XML.
- Network configuration.
- Source-to-edge mapping.
- Network metadata.
- Network manifest.
- Strict network.
- Provisional network jika dapat dibangun secara benar.
- Route test fixtures.
- Route test results.
- Connectivity report.
- QA report.
- Browser visualization.
- Automated tests.

Simpan hasil network pada direktori khusus, misalnya:

`simulation/network/m03/`

Dokumentasi pada:

`documentation/m03/`

Konfigurasi pada:

`configuration/network-m03/`

Buat skrip rebuild agar network dapat dibuat ulang dari data M02 tanpa mengunduh ulang sumber.

## 12. BATASAN MILESTONE

Jangan:
- Membuat OD Matrix final.
- Memasukkan volume kendaraan aktual.
- Membuat pertumbuhan kendaraan.
- Menjalankan simulasi kemacetan.
- Mengkalibrasi perilaku kendaraan.
- Membuat jadwal kereta.
- Mengembangkan solusi flyover final.
- Membuat sistem kendaraan interaktif.
- Mengklaim jaringan sudah tervalidasi lapangan.

M03 hanya membangun dan memvalidasi network topology.

## 13. ACCEPTANCE CRITERIA

M03 dianggap lulus apabila:

1. Network SUMO berhasil dibangun dari data M02.
2. Jalan utama kedua arah teridentifikasi.
3. Frontage terpisah dan koneksinya terdokumentasi.
4. Feeder network terhubung sesuai bukti sumber.
5. Junction dan edge diperiksa.
6. Komponen jaringan yang terisolasi terdokumentasi.
7. Arah perjalanan tidak dikarang.
8. Parameter asumsi diberi label.
9. Route test Sidoarjo–Surabaya dijalankan.
10. Route test Surabaya–Sidoarjo dijalankan.
11. SUMO-GUI berhasil membuka jaringan jika lingkungan GUI tersedia.
12. NETEDIT berhasil membuka jaringan jika lingkungan GUI tersedia.
13. Browser internal menampilkan network hasil konversi.
14. Build dan automated tests lulus.
15. Seluruh output dapat direproduksi.
16. Tidak ada data mentah M02 yang rusak atau berubah.

## 14. LAPORAN AKHIR

Buat:

`MILESTONE_03_REPORT.md`

Isi:
- Ringkasan pekerjaan.
- Struktur network.
- Jumlah nodes.
- Jumlah edges.
- Jumlah lanes.
- Komponen jaringan.
- Kualitas konektivitas.
- Pemisahan main arterial dan frontage.
- Hasil route test dua arah.
- Daftar asumsi.
- Daftar missing data.
- Hasil SUMO-GUI.
- Hasil NETEDIT.
- Hasil internal browser.
- Screenshot.
- Automated test results.
- Kendala.
- Rekomendasi M04.

Berikan status acceptance criteria secara transparan.

Jangan lanjut ke M04 tanpa persetujuan pengguna.

MULAI MILESTONE 03 SEKARANG.

Prioritaskan akurasi jaringan dan legalitas koneksi dibandingkan jumlah edge yang berhasil dibuat atau tampilan visual yang menarik.