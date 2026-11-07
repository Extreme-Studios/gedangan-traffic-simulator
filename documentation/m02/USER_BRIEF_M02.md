# MILESTONE 02 — GEDANGAN GEOGRAPHIC MAPPING
## Real-World Geographic Data Acquisition & Road Network Mapping

Lanjutkan proyek Gedangan Traffic Simulator dari Milestone 1 yang sudah dinyatakan lulus.

Kerjakan MILESTONE 02 SAJA.

## 1. FOLDER KERJA

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

Baca README, PROJECT_CHARTER, ARCHITECTURE, DATA_GOVERNANCE, RESEARCH_REGISTER, ENVIRONMENT_AUDIT, dan MILESTONE_01_REPORT sebelum melakukan perubahan.

Jangan menghapus atau menimpa pekerjaan M1.

## 2. TUJUAN MILESTONE 02

Membangun basis data geografis kawasan Gedangan, Sidoarjo berdasarkan kondisi geografis sebenarnya.

Lokasi penelitian mencakup:
- Perempatan Gedangan.
- Koridor utama Sidoarjo–Surabaya.
- Koridor Surabaya–Sidoarjo.
- Frontage road.
- Jalan pengumpan dan akses kawasan.
- Persimpangan sekitar Stasiun Gedangan.
- Stasiun Gedangan.
- Jalur rel kereta api dan perlintasannya.
- Ruas jalan yang berpotensi mengalami antrean akibat queue spillback.

Prioritas utama adalah koridor jalan utama Sidoarjo–Surabaya.

Frontage road harus dipetakan sebagai jaringan tersendiri, bukan digabung dengan jalan utama.

Berdasarkan pengamatan pengguna, frontage relatif lancar, sedangkan arus utama dari Sidoarjo menuju Surabaya belum memiliki alternatif kapasitas yang memadai. Simpan informasi ini sebagai observasi pengguna yang belum diverifikasi, bukan fakta pengukuran.

## 3. PENGUMPULAN DATA GEOGRAFIS

Gunakan sumber geografis yang dapat dipertanggungjawabkan.

Prioritas sumber:

1. OpenStreetMap untuk geometri jalan, rel, stasiun, simpang, dan jaringan penghubung.
2. Geofabrik atau Overpass API untuk memperoleh data OSM.
3. Sumber pemerintah daerah dan instansi jalan/kereta untuk memeriksa rencana dan informasi infrastruktur.
4. Sumber geospasial resmi lainnya apabila tersedia dan mempunyai izin penggunaan yang sesuai.

Website referensi:
- https://www.openstreetmap.org/
- https://download.geofabrik.de/
- https://www.geofabrik.de/data/
- https://eclipse.dev/sumo/

Jangan mengambil data dengan cara scraping Google Maps atau menggunakan data peta berhak cipta tanpa izin.

Catat sumber, tanggal pengambilan, lisensi, dan atribusi setiap dataset.

Jika data suatu ruas tidak ditemukan, jangan membuat geometri berdasarkan tebakan.

## 4. PENENTUAN AREA PENELITIAN

Buat dua cakupan geografis:

A. Core Study Area

Meliputi perempatan utama, jaringan frontage, simpang sekitar stasiun, akses pengumpan, dan perlintasan kereta.

B. Context Study Area

Meliputi ruas jalan yang cukup panjang untuk menangkap:
- Antrean kendaraan.
- Queue spillback.
- Perubahan distribusi arus.
- Jalur alternatif yang benar-benar tersedia.
- Pengaruh simpang lain terhadap Gedangan.

Jangan menetapkan batas penelitian hanya berdasarkan radius sembarang.

Tentukan batas berdasarkan konektivitas jaringan, panjang pendekat jalan, dan kebutuhan menangkap antrean.

Dokumentasikan alasan pemilihan batas tersebut.

## 5. KLASIFIKASI JARINGAN JALAN

Setiap ruas jalan harus dapat dibedakan berdasarkan fungsinya:

- Main arterial road.
- Frontage road.
- Feeder road.
- Collector road.
- Local access road.
- Service road.
- Connector road.

Petakan kedua arah perjalanan pada koridor utama.

Identifikasi:
- Jalan satu arah dan dua arah.
- Jumlah lajur jika tersedia.
- Arah pergerakan.
- Persimpangan.
- Akses masuk dan keluar.
- Titik merge dan diverge.
- U-turn.
- Penyempitan jalan.
- Hambatan fisik.
- Titik konflik kendaraan.

Jika informasi jumlah lajur, lebar jalan, atau kecepatan tidak tersedia, gunakan null atau status unknown.

Jangan mengarang atribut jalan.

## 6. PEMETAAN KERETA API

Petakan:
- Jalur rel.
- Jumlah jalur rel apabila dapat diverifikasi.
- Stasiun Gedangan.
- Posisi perlintasan.
- Hubungan antara rel dan jalan raya.
- Lokasi akses stasiun.
- Titik yang berpotensi mengalami konflik arus kendaraan.

Jangan mengasumsikan durasi penutupan palang, frekuensi kereta, atau jadwal perjalanan tanpa sumber.

Data yang belum tersedia harus dicatat sebagai kebutuhan survei berikutnya.

## 7. SISTEM KOORDINAT

Gunakan:

- EPSG:4326 untuk penyimpanan koordinat geografis.
- EPSG:32749 untuk analisis jarak dan pengukuran dalam meter.

Periksa transformasi koordinat dan pastikan semua geometri berada pada lokasi yang benar.

Jangan menggunakan koordinat lokal yang tidak memiliki referensi geografis.

## 8. INSTALASI SUMO

Audit terlebih dahulu apakah SUMO sudah tersedia.

Berdasarkan laporan M1, SUMO dan TraCI belum terdeteksi.

Karena SUMO diperlukan pada Milestone 3, lakukan persiapan instalasi sekarang.

Unduh hanya dari sumber resmi Eclipse SUMO:

https://eclipse.dev/sumo/

Gunakan distribusi Windows x64 yang stabil dan kompatibel.

Komponen yang harus tersedia:

1. SUMO command-line engine.
2. SUMO-GUI.
3. NETEDIT.
4. NETCONVERT.
5. SUMO tools.
6. TraCI Python interface.
7. sumolib.

Aturan instalasi:

- Audit versi dan lokasi instalasi.
- Gunakan instalasi lokal pengguna jika memungkinkan.
- Jangan mengubah registry atau PATH sistem secara destruktif.
- Jangan menonaktifkan keamanan Windows.
- Jangan menggunakan installer pihak ketiga yang tidak terpercaya.
- Jika membutuhkan hak administrator, berhenti dan minta persetujuan.
- Jangan memasang beberapa versi SUMO yang saling bertentangan.
- Pastikan versi TraCI sesuai dengan versi SUMO.
- Siapkan konfigurasi SUMO_HOME untuk lingkungan proyek.
- Jika diperlukan, pasang TraCI dan sumolib pada virtual environment proyek.
- Dokumentasikan lokasi executable dan dependensi.

Verifikasi ketersediaan:
- sumo.exe
- sumo-gui.exe
- netedit.exe
- netconvert.exe
- TraCI import.
- sumolib import.

Lakukan smoke test SUMO sederhana dengan jaringan pengujian sementara yang bukan jaringan Gedangan.

PENTING: Instalasi SUMO adalah persiapan toolchain. Jangan membangun jaringan simulasi SUMO final pada milestone ini. Itu pekerjaan Milestone 3.

Jika unduhan atau instalasi gagal, dokumentasikan penyebab dan jangan mengklaim instalasi berhasil.

## 9. PENGOLAHAN DATA GEOGRAFIS

Buat struktur direktori:

geodata/
- raw/
- processed/
- boundaries/
- roads/
- railways/
- junctions/
- access_points/
- quality_assurance/
- sources/

Format data utama:
- GeoJSON.
- CSV untuk tabel atribut.
- Metadata JSON.
- GeoPackage jika memang diperlukan dan dapat dibuat dengan benar.

Buat dataset terpisah untuk:
- Jalan utama.
- Frontage road.
- Jalan pengumpan.
- Persimpangan.
- Jalur kereta.
- Stasiun.
- Perlintasan.
- Batas penelitian.

Setiap objek mempunyai ID unik dan atribut sumber.

Jangan menggabungkan data hasil observasi, data referensi, dan asumsi ke dalam satu kategori tanpa penanda provenance.

## 10. VALIDASI TOPOLOGI DAN GEOMETRI

Lakukan pemeriksaan:

- Geometri kosong.
- Koordinat tidak valid.
- Ruas jalan terputus.
- Node yang tidak tersambung.
- Duplikasi ruas jalan.
- Arah jalan.
- Persimpangan yang tidak terhubung.
- Posisi jalur rel.
- Titik pertemuan frontage dan jalan utama.
- Konsistensi CRS.
- Kelengkapan metadata sumber.

Buat laporan kualitas data.

Tandai setiap data dengan status:
- Verified.
- Partially verified.
- Unverified.
- Missing.

Bedakan verifikasi dari OSM, dokumen resmi, dan survei lapangan.

## 11. VISUALISASI MELALUI INTERNAL BROWSER CODEX

Gunakan internal browser Codex sebagai lingkungan preview utama.

Jangan otomatis menggunakan Chrome.

Buat visualisasi geografis dasar berdasarkan data yang berhasil dikumpulkan.

Gunakan Three.js yang sudah tersedia untuk menampilkan:
- Garis jalan utama.
- Frontage road dengan jalur terpisah.
- Jalan pengumpan.
- Jalur rel.
- Stasiun.
- Persimpangan.
- Batas area penelitian.

Wajib:
- Menggunakan geometri geografis asli.
- Menampilkan posisi objek secara proporsional.
- Memiliki kontrol zoom dan orbit.
- Memiliki layer visibility.
- Dapat memilih ruas jalan untuk melihat atributnya.
- Memiliki panel informasi sumber data.
- Menampilkan legenda warna.

Jangan membuat bangunan atau kendaraan realistis terlebih dahulu. Fokus pada ketepatan peta.

Lakukan pengujian internal browser:
1. Localhost berhasil dibuka.
2. GeoJSON berhasil dimuat.
3. Geometri jalan tampil.
4. Jalur rel tampil.
5. Frontage dan jalan utama dapat dibedakan.
6. Layer dapat diaktifkan dan dinonaktifkan.
7. Pemilihan ruas jalan berfungsi.
8. Tidak ada error JavaScript yang menghambat.
9. WebGL berjalan dengan baik.

Jika internal browser gagal mendukung rendering, catat penyebab dan gunakan Chrome sebagai fallback hanya untuk verifikasi kompatibilitas.

## 12. BATASAN MILESTONE

Jangan:
- Memulai simulasi kendaraan.
- Membuat OD Matrix final.
- Membuat perilaku kendaraan.
- Mengkalibrasi volume lalu lintas.
- Membuat proyeksi pertumbuhan kendaraan.
- Mengklaim kondisi kemacetan sudah terukur.
- Membuat skenario flyover final.
- Mengarang geometri jalan.
- Melanjutkan Milestone 3.

Fokus hanya pada pemetaan geografis dan kesiapan toolchain.

## 13. ACCEPTANCE CRITERIA

Milestone 2 dianggap selesai jika:

1. Area penelitian Gedangan berhasil dipetakan.
2. Koridor utama dan frontage road terpisah.
3. Jaringan pengumpan teridentifikasi.
4. Persimpangan dan kawasan stasiun terpetakan.
5. Jalur rel dan perlintasan teridentifikasi.
6. Data geografis tersimpan dalam format yang dapat digunakan.
7. CRS telah diperiksa.
8. Topologi dan kualitas data diperiksa.
9. Semua sumber dan lisensi terdokumentasi.
10. SUMO terinstal dan teruji, atau kendala instalasinya terdokumentasi secara jelas.
11. Internal browser berhasil menampilkan peta, atau kegagalan dan fallback didokumentasikan.
12. Tidak ada klaim data yang belum terverifikasi.

## 14. LAPORAN AKHIR

Buat:

MILESTONE_02_REPORT.md

Isi laporan:
- Ringkasan pekerjaan.
- Batas geografis penelitian.
- Peta hasil pemetaan.
- Daftar ruas jalan.
- Daftar persimpangan.
- Daftar jaringan rel dan perlintasan.
- Daftar atribut yang belum tersedia.
- Sumber data dan lisensi.
- Hasil pemeriksaan topologi.
- Hasil instalasi SUMO.
- Versi software.
- Hasil pengujian internal browser.
- Screenshot visualisasi.
- Kendala.
- Rekomendasi untuk Milestone 3.

Sertakan peta hasil pemetaan yang bisa diperiksa.

Jangan lanjut ke Milestone 3 tanpa persetujuan pengguna.

MULAI MILESTONE 02 SEKARANG.

Audit proyek terlebih dahulu, lalu kerjakan secara bertahap. Prioritaskan akurasi geografis daripada kecepatan pengerjaan atau keindahan visual.