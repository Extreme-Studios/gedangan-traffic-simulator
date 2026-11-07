# Gedangan Geographic Mapping · M02

M01 tetap utuh. M02 menambahkan data referensi geografis OSM dan toolchain SUMO portable. **Tidak ada mikrosimulasi Gedangan, demand, kalibrasi atau skenario infrastruktur final.** Baseline tetap 2026.

## Buka peta

Jalankan **START_MAPPING.bat**. Buka **http://127.0.0.1:5174/mapping.html** melalui browser internal Codex. Launcher sengaja tidak membuka Chrome/default browser. M01 masih tersedia melalui START_DEV.bat seperti sebelumnya; kedua entry dipisah agar source M01 tidak ditimpa.

Kontrol: Core area / Context area, reset kamera, drag untuk orbit, roda untuk zoom, checkbox layer, klik garis/label peta untuk atribut. Pencarian nama/ID OSM tersedia. Panel Sumber berisi provenance/CRS/atribusi dan unduhan GeoJSON. Panel Kualitas memaparkan atribut hilang dan keterbatasan topologi.

Biarkan launcher terbuka selama preview; Ctrl+C menghentikan proses. `START_MAPPING.bat --check` memeriksa prasyarat. Tidak ada backend atau koneksi SUMO yang diperlukan untuk membaca peta.

## File yang dapat diperiksa tanpa server

- `geodata/processed/gedangan-core-map.svg` dan `gedangan-context-map.svg`: peta vektor mandiri dengan atribusi dan skala geometris.
- `geodata/processed/all_features.geojson`: WGS84, longitude/latitude (EPSG:4326), bisa dibuka dengan GIS yang mendukung GeoJSON.
- `geodata/processed/*.csv`: tabel atribut jalan, simpang, rel, perlintasan dan akses.
- `geodata/quality_assurance/`: laporan QA JSON, komponen, ujung jaringan, atribut hilang dan kandidat yang perlu ditinjau.
- `documentation/MILESTONE_02_REPORT.md`: laporan hasil dan acceptance.
- `documentation/m02/`: screenshot browser, log build/tes/SUMO, snapshot source M01 dan checksum.

Semua runtime memakai data lokal. Tautan OSM/referensi eksternal memerlukan internet. Tidak ada map tiles, Google Maps scraping, bangunan atau kendaraan realistis.

## Build dan verifikasi

```powershell
# Root proyek, dependency dasar M01 sudah terpasang
.\.venv\Scripts\python.exe -m pip install -r configuration\requirements-m02-lock.txt
.\.venv\Scripts\python.exe geodata\scripts\process_geodata.py
.\.venv\Scripts\python.exe geodata\scripts\export_maps.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v

cd frontend
node node_modules\typescript\bin\tsc --noEmit
node node_modules\vite\bin\vite.js build --config vite.mapping.config.ts
```

Output build M02 adalah `frontend/dist-m02/`, terpisah dari build M01. Untuk preview production, jalankan Vite dengan `preview --config vite.mapping.config.ts`, lalu buka URL `/mapping.html`. Paket frontend M01 tidak diubah; dependency geospasial dipasang dalam `.venv` proyek saja. Lock baru tidak mengganti lock M01.

Akuisisi raw tidak dijalankan otomatis. Query Overpass dan script ada di geodata/sources dan geodata/scripts. Raw yang sudah ada direuse, bukan diunduh ulang/ditimpa. Jika perlu snapshot baru, gunakan nama dataset baru dan perbarui provenance secara eksplisit.

## Toolchain SUMO

Distribusi resmi stabil Windows x64 **1.28.0** pada `toolchain/sumo-win64-1.28.0/`. SUMO, SUMO-GUI, NETEDIT, NETCONVERT dan tools tersedia. TraCI dan sumolib diimpor dari tools dalam distribusi yang sama, sehingga tidak ada paket pip berbeda versi.

Untuk sesi terminal proyek, jalankan `call SUMO_ENV_M02.bat` dari Command Prompt. Ini hanya mengubah environment proses/sesi tersebut. Tidak mengubah registry atau PATH sistem. Dari Python, helper `configuration.sumo_env_m02.activate()` mengatur SUMO_HOME dan sys.path khusus proses.

Smoke test: `.\.venv\Scripts\python.exe -m configuration.smoke_sumo_m02`. Ini memakai fixture **synthetic-not-gedangan** pada toolchain/smoke, bukan jaringan penelitian. Jangan memasukkan angka dari fixture tersebut sebagai data Gedangan.

SUMO-GUI/NETEDIT diuji melalui `--version`, belum diuji interaksi GUI. Checksum ZIP lokal dan pemeriksaan CRC disimpan; belum dibandingkan dengan checksum publisher independen. Tidak ada instalasi administrator.

## Batas ilmiah

Kesetiaan terhadap snapshot OSM sudah diperiksa. Status keseluruhan **Partially verified**, karena arah tanpa tag, jumlah/lebar lajur, akses/legal turns, pintu masuk stasiun dan kondisi fisik belum seluruhnya diverifikasi. Batas context berdasarkan konektivitas/anchor dan panjang pendekat; kecukupannya untuk antrean/spillback tetap perlu diuji pada M03/M06. Unknown tidak dianggap nol atau dua arah.

**M03 belum dimulai dan memerlukan persetujuan pengguna.**
