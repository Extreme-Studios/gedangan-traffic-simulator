# Gedangan M04 — Vehicles, OD and synthetic demand

**SYNTHETIC TEST — NOT CALIBRATED GEDANGAN TRAFFIC.**

M04 menyediakan registry 10 kategori kendaraan, zona/OD terstruktur, generator deterministik, tiga profil sintetis, routing SUMO dan rekaman hasil. Status penerimaan masih **PARTIAL**: jaringan M03 hanya mengizinkan passenger; sembilan kategori lain belum dapat diuji bergerak pada Gedangan. QA browser internal telah lulus setelah aplikasi dibuka ulang, termasuk pergantian profil, registry, failure inspector dan playback FCD.

## Jalankan viewer

Dari folder proyek `C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`, jalankan `START_DEMAND_M04.bat`, lalu buka **http://127.0.0.1:5176/demand.html** di browser internal Codex. Bila browser internal disabled, aktifkan melalui Work settings. Launcher tidak mengubah pengaturan dan tidak membuka browser lain. `START_DEMAND_M04.bat --check` memeriksa output, Node/Vite dan port 5176 tanpa menjalankan server. Ctrl+C menghentikan preview.

Halaman ini terpisah dari M03. Pilih network variant dan profil; periksa requested/routable/failed/departed/arrived/teleports. Request ledger mempertahankan kegagalan. Panel Vehicles menampilkan parameter berlabel ASSUMPTION. QA & issues menjelaskan batas izin M03 dan metrik proses.

Playback menggunakan sampel FCD aktual setiap 5 detik, tanpa interpolasi atau gerakan acak. Tombol playback mengendalikan pemutaran rekaman, bukan engine SUMO. Sambungan OD putus-putus hanya diagram asal–tujuan; rute aktual terpilih ditampilkan putih. Warna titik kendaraan tidak mewakili ukuran fisik kendaraan dalam scene 3D.

## Rebuild dan pengujian

Gunakan **REBUILD_DEMAND_M04.bat**. Skrip membaca snapshot M03 dan konfigurasi lokal, lalu menimpa hasil turunan M04. Data/source M01–M03 dipertahankan dan diperiksa SHA-256. Tidak ada unduhan, perubahan permission network, registry sistem atau instalasi kedua.

```powershell
.\.venv\Scripts\python.exe configuration\demand-m04\build_demand.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
cd frontend
.\node_modules\.bin\tsc.cmd --noEmit
.\node_modules\.bin\vite.cmd build --config vite.demand.config.ts
```

Dependency memakai `.venv`, Node/Vite dan SUMO 1.28.0 dari milestone sebelumnya. Build frontend M04 berada di `frontend/dist-m04/`. Tidak menjalankan API/backend M01 atau server real-time.

## Input yang dapat diubah

- `configuration/demand-m04/vehicle-registry.json`: vClass, dimensi, dinamika, model Krauss/LC2013 dan provenance per parameter.
- `configuration/demand-m04/demand-config.json`: seed, komposisi, LOW 40 / MEDIUM 120 / STRESS 300 request per interval 900 detik, horizon 2.100 detik. Batas awal generator 500 request/interval; naikkan hanya setelah pengukuran dan perubahan guard yang ditinjau.
- `od-matrix.schema.json` dan `od-interval.schema.json`: kontrak movement fixture dan count per tahun/OD/type/interval. Growth records tetap kosong; tidak ada proyeksi tahunan.
- `provenance.json`: ASSUMPTION, RESEARCH_REFERENCE dan SYNTHETIC_TEST; hasil run SIMULATED_RESULT. Tidak ada data sintetis ditulis ke observed_data.

`initialize_config.py` hanya pembuat fixture awal; **tidak dipanggil oleh rebuild** agar konfigurasi yang diedit tidak dikembalikan ke nilai awal. Pembagian zona dihasilkan dari endpoint sumber M03; untuk perubahan assignment geografis, tinjau `make_zones()` bersama fixture dan provenance.

## Output

`simulation/demand/m04/` berisi vehicle XML/JSON, zona, OD fixture, compatibility 10 type × 9 OD per varian, batch requested trips, accepted routes, seluruh failure records, interval counts, DUAROUTER log dan demand manifest. Generated trips XML berisi request yang lolos precheck; JSON requested tetap berisi seluruh request, termasuk yang ditolak sebelum router.

`simulation/runs/m04/` berisi delapan run Gedangan, setiap run dengan config, tripinfo, FCD, summary/statistics, metrics, lifecycle vehicle states, trajectory JSON, log dan manifest. Dua coverage smoke memakai 90 pasangan type/OD; enam run lainnya memakai tiga profil di dua varian. `isolated-motorcycle-sublane/` adalah fixture lurus 500m terpisah yang tidak merepresentasikan Gedangan.

`documentation/m04/` menyimpan laporan QA, issue register M03, compatibility, test/build logs, hash preservasi dan bukti GUI. Laporan utama: `documentation/MILESTONE_04_REPORT.md`.

## Buka SUMO-GUI

```powershell
& '.\toolchain\sumo-win64-1.28.0\bin\sumo-gui.exe' -c '.\simulation\runs\m04\m04-provisional-smoke-seed20261031\run.sumocfg'
```

Config memakai output file run yang sama. Untuk menjaga hasil/headless manifest saat pemeriksaan GUI tambahan, override output ke direktori lain atau rebuild sesudah inspeksi. Pemeriksaan GUI M04 menggunakan override ke `documentation/m04/gui-*.xml`, bukan menimpa bukti regresi.

Izin passenger-only tidak dibypass dengan vClass `ignoring`, relabel truk sebagai passenger, TraCI permission override atau network patch. Uji motor/bus/truk Gedangan memerlukan pembaruan policy akses M03 yang ditinjau tersendiri. Oversize tetap diblokir sampai ada clearance geometri/legalitas. M05 belum dimulai.
