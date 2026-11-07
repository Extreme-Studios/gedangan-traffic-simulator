# MILESTONE 01 REPORT

**Gedangan Traffic Simulator — Project Foundation & Research Architecture**  
Tanggal: **31 Oktober 2026**  
Status: **M01 SELESAI sebagai fondasi. FOUNDATION / ENGINE NOT CONNECTED.**  
**M02 belum dimulai. Tidak ada simulasi lalu lintas aktual atau baseline yang telah dikalibrasi.**

## 1. Pekerjaan selesai

- Audit direktori, Windows, Python/pip, Node/npm, Git, browser, SUMO/TraCI, Blender dan kondisi dependensi.
- Frontend lokal React + TypeScript + Vite + Three.js, UI profesional dengan navigasi, canvas 3D, informasi riset, panel simulasi/skenario, status backend/engine dan validasi data.
- Scene abstrak ringan dengan orbit, grid toggle dan reset; secara eksplisit bukan geometri Gedangan. Kontrol simulasi disabled, metrik tidak mempunyai angka pengukuran rekaan.
- Backend standard-library Python yang dapat dijalankan, endpoint health/status/config/null metrics, dan tujuh modul domain terpisah.
- Konfigurasi baseline 2026, schema seluruh entitas yang diminta, empat kategori dataset kosong, validator provenance/topologi dasar, kontrak pertumbuhan per tahun/kelas/zona tanpa persentase default.
- Dokumentasi riset, tata kelola, arsitektur, charter, roadmap lengkap 12 milestone, audit dan laporan ini. Brief pengguna dipertahankan dalam dokumentasi.
- START_DEV.bat dan launcher Python yang memeriksa prasyarat, memiliki dua proses server, mendeteksi konflik port dan menghentikan keduanya. Tidak membuat START_SIMULATION karena prasyarat engine/data belum terpenuhi.

## 2. Folder proyek

Semua source, dokumentasi, konfigurasi dan bukti berada di:

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

```text
Simulasi Kemacetan Lalu Lintas/
  README.md
  START_DEV.bat
  .gitignore
  frontend/
    src/main.tsx, style.css
    index.html, vite.config.ts, tsconfig.json
    package.json, package-lock.json
    node_modules/                 dependency lokal, ignored
    dist/                         hasil build, ignored
  backend/
    server.py
    requirements.txt             tanpa runtime dependency tambahan
    gedangan/
      simulation_controller.py
      traffic_network.py
      vehicle_demand.py
      vehicle_behavior.py
      railway_interaction.py
      scenario_manager.py
      metrics_collector.py
  simulation/
    README.md, networks/, demand/, runs/
  traffic-data/
    observed_data/dataset.json
    research_reference/dataset.json
    assumptions/dataset.json
    simulated_results/dataset.json
  scenarios/
    README.md, baseline/, alternatives/
  assets/
    README.md, blender/, models/, textures/
  documentation/
    PROJECT_CHARTER.md
    ARCHITECTURE.md
    DATA_GOVERNANCE.md
    RESEARCH_REGISTER.md
    MILESTONE_ROADMAP.md
    ENVIRONMENT_AUDIT.md
    MILESTONE_01_REPORT.md
    USER_BRIEF_M01.md
    evidence/
  tests/
    test_foundation.py
    requirements.txt, requirements-lock.txt
  configuration/
    project.json
    schemas/dataset.schema.json, project.schema.json
    build_schemas.py, validate_data.py, start_dev.py
  .venv/                          alat tes lokal, ignored
```

Folder awal kosong dan tidak ada pekerjaan lama yang dihapus atau ditimpa. File yang dibuat pada tugas ini diperbaiki ketika tes menemukan masalah. Tidak init Git, commit, push, deployment atau EXE.

## 3. Software dan dependensi

Windows 11 Pro build 26300; Python 3.12.10; pip 25.0.1; Node 24.22.1; npm 12.0.1; Git 2.56.0. Chrome 156.0.8078.76 diuji. Edge tercatat pada registry tetapi belum diuji. Blender 5.2.2 terdeteksi tetapi belum dijalankan.

Frontend terpasang: React/React DOM 19.3.1, Three.js 0.180.0, Vite 7.3.7, TypeScript 5.9.3, plugin-react 5.2.0. Lockfile tersedia. Backend HTTP tidak memerlukan pip runtime. jsonschema 4.25.1 dan dependency tes dipasang hanya di `.venv`, dengan lock daftar terpasang.

Library grafik belum dipasang karena belum ada hasil simulasi; kandidat dan titik integrasinya didokumentasikan untuk M11. Tidak ada SUMO/TraCI yang dipasang pada M01.

## 4. Hasil audit lingkungan

- Python, Node/npm, Git dan Chrome siap untuk foundation lokal.
- SUMO tidak terdeteksi pada PATH/registry yang diperiksa dan SUMO_HOME tidak terisi. TraCI/sumolib tidak dapat ditemukan oleh Python audit. Ini bukan klaim pencarian seluruh disk.
- RAM fisik 16 GiB terdeteksi; RAM terlihat OS sekitar 11.70 GiB. AMD Radeon Graphics terdeteksi. VRAM 6 GB belum diverifikasi.
- Tidak ada instalasi administrator atau perubahan PATH/registry/firewall.
- Rincian ada di ENVIRONMENT_AUDIT.md dan evidence/environment.json.

## 5. Build dan testing aktual

| Pemeriksaan | Hasil | Bukti |
|---|---|---|
| TypeScript + production build | PASS, exit 0 | evidence/frontend-build-final.txt |
| Dependency tree frontend | PASS | evidence/frontend-dependencies.txt |
| npm audit, seluruh dependency tree | 0 advisory pada waktu pemeriksaan | evidence/npm-audit.json; bukan audit keamanan menyeluruh |
| Schema | PASS: 2 schema, config, 4 kategori dataset | evidence/schema-validation.txt |
| Backend/domain/data tests | PASS: 18/18, exit 0 | evidence/backend-tests.txt |
| HTTP frontend | 200 | evidence/http-smoke.json |
| Proxy frontend → API | PASS; FOUNDATION, baseline 2026, engine not connected | evidence/http-smoke.json |
| Chrome lokal | PASS: halaman dan scene Three.js tampil | evidence/BROWSER_QA.md |
| Interaksi visual/navigasi | PASS: orbit, reset, grid, data/riset/12 roadmap | evidence/BROWSER_QA.md |
| Launcher | PASS: prasyarat, startup dua server, konflik port ditolak | evidence/launcher-check.json |
| Shutdown | kedua port tidak lagi listening setelah Ctrl+C | evidence/launcher-check.json |

Tes menguji guard engine (start/step ditolak), null metrics, health bukan simulasi, config dan HTTP 404/409, kategori terpisah, provenance wajib, ID ganda, foreign key dasar, baseline salah, field tak dikenal, geometri null, missing/duplicate/undocumented/nonfinite growth. Fixture sintetis hanya ada pada kode tes dan tidak disimpan sebagai data Gedangan.

Satu pengulangan tes menemukan WinError 10054 pada POST; handler memperbaiki pembacaan body terbatas sebelum penolakan. Hasil gagal awal disimpan pada evidence/backend-tests-before-fix.txt; hasil setelah perbaikan 18/18 PASS. Tidak menyembunyikan kegagalan awal.

Build akhir menghasilkan JS sekitar **741.72 kB / gzip 201.27 kB**, CSS 10.61 kB / gzip 3.02 kB; ada warning chunk >500 kB. Tidak ada error build tersisa. Saat source diedit, Vite sempat melakukan full page reload karena batas Fast Refresh main.tsx; aplikasi kembali tampil normal. Ini kejadian dev, bukan kegagalan production build.

QA browser memakai Chrome terpasang dan window desktop yang dimaksimalkan, capture 1280×696. Tidak mengklaim pengujian fisik 1080p, benchmark FPS/VRAM/baterai, browser Edge, audit console menyeluruh, atau sesi SUMO. Batas desain render 30 fps/pixel ratio 1.5 bukan hasil benchmark.

## 6. Menjalankan aplikasi

Dependency proyek sudah terpasang. Klik dua kali **START_DEV.bat**, lalu buka **http://127.0.0.1:5173** di Chrome/Edge. Launcher mencoba membuka browser default secara otomatis. Backend pada **http://127.0.0.1:8765**. Keduanya loopback lokal.

Biarkan jendela launcher terbuka. Tekan Ctrl+C untuk menghentikan kedua server. Sesi PTY PowerShell uji melaporkan exit 1 ketika Ctrl+C diinjeksi; launcher mencetak penghentian dan kedua port terbukti tertutup. Tidak ada server uji yang sengaja ditinggal hidup.

Instalasi ulang: jalankan `npm ci` di frontend; jika ada kendala sertifikat, gunakan CA sistem sesuai README. Tes schema: buat `.venv` lalu pasang `tests/requirements-lock.txt` (atau requirements.txt untuk dependency langsung), jalankan `python -m configuration.validate_data` dan `python -m unittest discover -s tests -v` memakai interpreter `.venv`. Build: `npm run build` dalam frontend. README memberi langkah terminal terpisah dan preview build.

UI/API dirancang berjalan offline setelah dependensi terpasang: tidak ada CDN, font, peta, telemetry atau aset jarak jauh. Tautan penelitian membutuhkan internet. Pemutusan jaringan fisik belum diuji; offline tidak berarti service worker/instalasi aplikasi.

## 7. Kendala dan keterbatasan

- SUMO/TraCI belum tersedia dan jaringan/demand belum ada; engine tidak terhubung. Ini sesuai mode foundation yang diminta.
- npm awal gagal verifikasi rantai sertifikat; diselesaikan dengan Node `--use-system-ca`, tanpa menonaktifkan TLS. npm 12 memblokir postinstall esbuild sebagai warning; build tetap berhasil dengan platform dependency terpasang.
- Chunk Three.js/React masih besar. Belum ada beban kendaraan, analitik atau aset dunia nyata untuk benchmark.
- Metadata/abstrak PTDI–STTD diperiksa, naskah lengkap dan konteks angka belum diverifikasi. Halaman/PDF primer ITS tidak dapat dibaca melalui alat pada sesi ini; kandidat tetap berlabel belum diverifikasi. Tidak ada angka yang disalin ke model.
- Schema/validator M01 memeriksa bentuk serta relasi dasar, bukan kebenaran survei, semua link lintas dataset/run, interval waktu atau kelayakan fisik jaringan. Penguatan dilakukan ketika data nyata tersedia.
- Koneksi API belum melakukan polling otomatis; tombol periksa ulang tersedia. Koneksi backend tidak berarti engine terhubung.

## 8. Pekerjaan belum selesai (di luar lingkup M01)

Pemetaan geografis, sumber geometri dan CRS; SUMO network; kendaraan/OD dan perilaku; kereta/palang; kalibrasi 2026; engine proyeksi pertumbuhan; implementasi skenario; kontrol simulasi; aset Blender dunia nyata; grafik analitik dan mode presentasi; optimasi serta uji akhir. Tidak ada klaim bahwa modul placeholder telah mengimplementasikan kemampuan tersebut.

## 9. Acceptance criteria M01

| # | Kriteria | Status dan batas |
|---|---|---|
| 1 | Struktur tersedia | PASS, sembilan area modular terpisah |
| 2 | Frontend berhasil dijalankan | PASS, Vite lokal + HTTP 200 |
| 3 | Dibuka melalui browser lokal | PASS, Chrome aktual |
| 4 | Scene Three.js tampil | PASS, canvas/mesh/orbit/grid/reset aktual; placeholder nongeografis |
| 5 | Backend berjalan atau prasyarat terdokumentasi | PASS, API berjalan; SUMO/TraCI missing terdokumentasi |
| 6 | Konfigurasi/schema | PASS, baseline 2026 dan kontrak entitas, validator lulus |
| 7 | Dokumentasi lengkap | PASS, tujuh dokumen wajib + README/brief/bukti |
| 8 | Arsitektur mendukung 12 milestone | PASS sebagai fondasi/kontrak; fitur M02–M12 belum diimplementasikan |
| 9 | Tidak ada klaim data aktual tanpa bukti | PASS, dataset model kosong, metrics null, scene diberi label |
| 10 | Laporan dan hasil pengujian | PASS, laporan ini dan evidence aktual |

## 10. Rekomendasi M02 (belum dikerjakan)

Setelah persetujuan pengguna, sepakati extent jaringan yang cukup untuk antrean/spillback, pilih sumber geospasial berlisensi dan CRS, identifikasi koridor utama/frontage/akses serta dua simpang/perlintasan, lalu verifikasi geometri di lapangan. Lengkapi register data dan naskah riset primer sebelum mengambil nilai. Tentukan paket survei 2026 dan kebutuhan OD/kelas kendaraan/operasi kereta untuk tahap berikutnya.

**Tidak melanjutkan ke Milestone 02 tanpa persetujuan pengguna.**
