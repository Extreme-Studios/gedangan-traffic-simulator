# MILESTONE 01 — GEDANGAN TRAFFIC SIMULATOR
## Project Foundation & Research Architecture

Kita akan membangun aplikasi bernama **Gedangan Traffic Simulator**, sebuah interactive 3D transportation digital twin untuk menganalisis kemacetan di kawasan Gedangan, Sidoarjo.

Ini adalah proyek jangka panjang yang terdiri dari 12 milestone. Pada tahap ini, kerjakan MILESTONE 01 SAJA.

## 1. LOKASI PROYEK

Gunakan folder kerja:

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

Semua source code, dokumentasi, konfigurasi, dan laporan harus berada di dalam folder tersebut.

Periksa isi folder sebelum melakukan perubahan. Jangan menghapus atau menimpa pekerjaan yang sudah ada.

## 2. VISI APLIKASI

Aplikasi final harus mempunyai kemampuan:

- Menampilkan kawasan Gedangan dalam lingkungan 3D interaktif.
- Mensimulasikan lalu lintas kendaraan secara mikroskopis.
- Mengakomodasi sepeda motor, mobil, bus, truk, trailer, dan kendaraan khusus berukuran besar.
- Memodelkan perlintasan kereta api.
- Memodelkan interaksi beberapa persimpangan yang saling memengaruhi.
- Menggunakan Origin-Destination Matrix.
- Menghitung panjang antrean, waktu perjalanan, kepadatan, kecepatan, dan kapasitas.
- Memproyeksikan pertumbuhan permintaan kendaraan mulai tahun dasar 2026 hingga tahun-tahun mendatang.
- Menguji berbagai alternatif solusi kemacetan.
- Membandingkan kondisi sebelum dan sesudah perubahan infrastruktur.
- Menyediakan kontrol interaktif seperti game simulasi.
- Berjalan secara lokal dan offline setelah seluruh dependensi terpasang.

## 3. KARAKTERISTIK LOKASI

Fokus penelitian adalah kawasan Perempatan Gedangan dan jaringan transportasi sekitarnya.

Karakteristik yang wajib menjadi dasar arsitektur:

1. Koridor utama Sidoarjo–Surabaya merupakan fokus utama persoalan kapasitas lalu lintas.
2. Arus dari Sidoarjo menuju Surabaya belum memiliki alternatif kapasitas yang memadai menurut pengamatan pengguna.
3. Frontage road sudah tersedia dan relatif lancar. Modelkan sebagai jalur tersendiri, termasuk akses masuk dan keluar.
4. Terdapat berbagai jenis kendaraan, mulai dari motor hingga kendaraan sangat besar.
5. Terdapat jaringan rel dan perlintasan kereta api.
6. Persimpangan Gedangan dan kawasan Stasiun Gedangan mempunyai interaksi lalu lintas.
7. Antrean dari satu ruas dapat menghambat ruas atau persimpangan lainnya.
8. Pertumbuhan penduduk dan kendaraan harus diperhitungkan dalam proyeksi jangka panjang.

Jangan mengarang geometri jalan, volume kendaraan, kapasitas, dan tingkat pertumbuhan. Data yang belum tersedia harus ditandai sebagai belum terverifikasi.

## 4. TEKNOLOGI

Gunakan arsitektur berikut:

Frontend:
- React
- TypeScript
- Vite
- Three.js

Traffic simulation:
- Eclipse SUMO
- Python
- TraCI

3D assets:
- Blender

Dashboard:
- React dan library grafik yang sesuai.

Pengembangan awal dijalankan melalui browser lokal Chrome atau Edge.

Jangan membuat aplikasi EXE pada milestone ini.

## 5. TUGAS MILESTONE 01

A. Environment Audit

Periksa:
- Windows version.
- Python dan pip.
- Node.js dan npm.
- Git.
- Ketersediaan SUMO.
- Ketersediaan TraCI.
- Browser.
- Kondisi dependensi.

Jangan menginstal software dengan hak administrator atau melakukan perubahan sistem destruktif tanpa persetujuan.

B. Project Structure

Buat struktur modular yang siap dikembangkan sampai 12 milestone.

Pisahkan:
- frontend
- backend
- simulation
- traffic-data
- scenarios
- assets
- documentation
- tests
- configuration

C. Frontend Foundation

Buat aplikasi React + TypeScript + Vite + Three.js.

Buat halaman awal profesional dengan:
- Nama Gedangan Traffic Simulator.
- Area visualisasi 3D.
- Panel informasi.
- Navigasi utama.
- Panel simulasi.
- Panel skenario.
- Status koneksi mesin simulasi.
- Status validasi data.

Untuk sementara gunakan scene 3D placeholder yang ringan.

Jangan menampilkan angka lalu lintas palsu seolah-olah merupakan hasil pengukuran aktual.

D. Backend Foundation

Siapkan kerangka Python yang modular untuk integrasi SUMO dan TraCI.

Pisahkan modul:
- Simulation controller.
- Traffic network.
- Vehicle demand.
- Vehicle behavior.
- Railway interaction.
- Scenario manager.
- Metrics collector.

Jika SUMO belum tersedia, gunakan status FOUNDATION / ENGINE NOT CONNECTED. Jangan mengklaim simulasi nyata telah berjalan.

E. Data Architecture

Siapkan struktur data untuk:
- Road nodes.
- Road edges.
- Lanes.
- Junctions.
- Railway crossings.
- Vehicle classes.
- Origin-Destination Matrix.
- Traffic demand.
- Traffic signals.
- Infrastructure scenarios.
- Simulation metrics.
- Data provenance.
- Calibration status.

Pisahkan empat kategori data:
1. Observed data.
2. Research reference.
3. Assumptions.
4. Simulated results.

Baseline year wajib 2026.

Pertumbuhan kendaraan harus dapat dikonfigurasi berdasarkan tahun, jenis kendaraan, dan zona perjalanan. Jangan menetapkan persentase pertumbuhan tanpa sumber atau dokumentasi asumsi.

F. Research Documentation

Buat dokumen:
- PROJECT_CHARTER.md
- ARCHITECTURE.md
- DATA_GOVERNANCE.md
- RESEARCH_REGISTER.md
- MILESTONE_ROADMAP.md
- ENVIRONMENT_AUDIT.md
- MILESTONE_01_REPORT.md

Masukkan penelitian terdahulu tentang Gedangan sebagai referensi awal, tetapi jangan menyalin angka tanpa memeriksa sumber dan konteksnya.

## 6. ROADMAP 12 MILESTONE

Catat seluruh roadmap berikut:

01. Project Foundation & Research Architecture.
02. Gedangan Geographic Mapping.
03. Traffic Network Engine.
04. Vehicle System & OD Demand.
05. Traffic Behavior & Railway Integration.
06. Baseline Calibration 2026.
07. Traffic Growth Projection.
08. Solution Scenario Engine.
09. Interactive Simulation Control.
10. 3D World Visualization.
11. Analytics Dashboard & Presentation Mode.
12. Optimization, Validation & Final Trial.

Pastikan fondasi arsitektur tidak menghalangi pengembangan berikutnya.

## 7. PERALATAN TARGET

Target perangkat:
- Windows 11.
- AMD GPU.
- VRAM 6 GB.
- RAM 16 GB.
- Resolusi 1080p.

Optimalkan aplikasi untuk perangkat tersebut.

Prioritaskan software gratis dan open-source.

## 8. TESTING DAN ACCEPTANCE CRITERIA

Milestone 1 dianggap selesai apabila:

1. Struktur proyek sudah tersedia.
2. Frontend berhasil dijalankan.
3. Halaman aplikasi dapat dibuka melalui browser lokal.
4. Scene Three.js dapat ditampilkan.
5. Backend Python dapat dijalankan atau status prasyaratnya terdokumentasi.
6. Konfigurasi dan schema data tersedia.
7. Dokumentasi proyek lengkap.
8. Arsitektur mendukung 12 milestone.
9. Tidak ada klaim data lalu lintas aktual yang belum terbukti.
10. Laporan pengujian dan hasil pekerjaan tersedia.

Buat skrip START_SIMULATION.bat jika prasyarat sudah terpenuhi. Jika belum, buat START_DEV.bat dengan instruksi yang jelas.

## 9. ATURAN PENGERJAAN

- Kerjakan hanya Milestone 1.
- Jangan mulai Milestone 2.
- Jangan membuat jaringan jalan final berdasarkan tebakan.
- Jangan memasukkan angka lalu lintas tanpa sumber.
- Jangan menghapus file yang sudah ada.
- Jangan mengerjakan semua fitur sekaligus.
- Jalankan build dan testing yang memungkinkan.
- Catat semua error dan keterbatasan.
- Jangan mengklaim fitur berhasil jika belum diuji.

## 10. LAPORAN AKHIR

Buat MILESTONE_01_REPORT.md yang menjelaskan:

1. Pekerjaan yang sudah selesai.
2. Struktur folder.
3. Software dan dependensi.
4. Hasil environment audit.
5. Hasil build dan testing aktual.
6. Cara menjalankan aplikasi melalui browser.
7. Kendala yang ditemukan.
8. Pekerjaan yang belum selesai.
9. Status acceptance criteria.
10. Rekomendasi untuk Milestone 2.

**PENTING: Jangan melanjutkan ke Milestone 2 sebelum mendapatkan persetujuan pengguna.**

Mulai sekarang dengan mengaudit folder dan lingkungan pengembangan, kemudian implementasikan Milestone 1 secara bertahap.