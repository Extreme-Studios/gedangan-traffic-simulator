# Gedangan M03 — Network inspection

M03 menghasilkan dua jaringan SUMO dari snapshot lokal M02. Strict membatasi arah dan belokan yang belum didukung bukti; provisional menambahkan asumsi arah pada kelas jalan terpilih. Keduanya masih memakai asumsi parameter engine dan belum tervalidasi lapangan.

## Menjalankan viewer

Di folder proyek, jalankan `START_NETWORK_M03.bat`, lalu buka **http://127.0.0.1:5175/network.html** melalui browser internal Codex. Launcher tidak membuka Chrome. Hentikan terminal dengan Ctrl+C setelah selesai. Node dan dependency frontend M01/M02 yang sudah tersedia digunakan kembali. `START_NETWORK_M03.bat --check` memeriksa prasyarat tanpa menjalankan server; port 5175 harus kosong.

Pilih Strict/Provisional, atur Layers, klik lane atau cari Edge ID, lalu periksa sumber dan status setiap parameter. Route tests menampilkan hasil DUAROUTER, termasuk NOT_FOUND. Garis putih adalah urutan rute fixture; tidak ada kendaraan yang disimulasikan. Rel dan titik crossing hanya overlay statis.

## Rebuild tanpa unduh data

Jalankan `REBUILD_NETWORK_M03.bat` dari folder proyek. Skrip memakai `.venv/Scripts/python.exe`, helper `configuration/sumo_env_m02.py`, dan toolchain lokal `toolchain/sumo-win64-1.28.0/`. Tidak ada instalasi SUMO kedua atau pengunduhan sumber. Rebuild menimpa **hasil turunan M03**, mempertahankan dataset M02, menjalankan NETCONVERT, fixture DUAROUTER, zero-step load SUMO, serta audit dan ekspor browser.

Untuk pemeriksaan otomatis:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
cd frontend
.\node_modules\.bin\tsc.cmd --noEmit
.\node_modules\.bin\vite.cmd build --config vite.network.config.ts
```

Build viewer disimpan di `frontend/dist-m03/`, terpisah dari build M01/M02.

## Membuka aplikasi SUMO

Gunakan `SUMO_ENV_M02.bat` bila ingin mengaktifkan environment pada terminal sendiri. Dari root proyek, executable yang digunakan untuk pemeriksaan adalah:

```powershell
& '.\toolchain\sumo-win64-1.28.0\bin\sumo-gui.exe' -c '.\simulation\network\m03\strict\inspect.sumocfg'
& '.\toolchain\sumo-win64-1.28.0\bin\netedit.exe' --sumo-net-file '.\simulation\network\m03\provisional\network.net.xml' --additional-files '.\simulation\network\m03\provisional\rail-reference.add.xml'
```

Konfigurasi inspect tidak berisi demand dan berakhir pada waktu 0. Jangan menafsirkan load test sebagai simulasi lalu lintas.

## Struktur dan batas hasil

- `configuration/network-m03/`: policy, converter, audit, launcher preview.
- `simulation/network/m03/strict/` dan `provisional/`: plain XML input, NETCONVERT configuration, network final, connection provenance, keputusan sumber, komponen, overlay rel, fixtures, log lengkap, inspection export.
- `simulation/network/m03/`: metadata, manifest SHA-256 dan pemetaan source-to-edge JSON/CSV.
- `documentation/MILESTONE_03_REPORT.md`: laporan utama dan acceptance criteria.
- `documentation/m03/`: QA, connectivity, hasil routing lengkap, reproducibility, log pengujian, screenshot GUI/browser.

`VERIFIED` berarti sesuai sumber OSM/M02, bukan hasil survei. `INFERRED` berarti interpretasi terdokumentasi. `ASSUMPTION` berarti parameter sementara. Kapasitas tetap `MISSING/null`.

Strict: 225 nodes / 241 edges / 323 lanes, 4/8 fixture FOUND. Provisional: 1.022 nodes / 1.961 edges / 2.043 lanes, 8/8 FOUND dengan asumsi. Kedua arah koridor utama FOUND pada keduanya. Komponen terisolasi, belokan tertahan, radius tajam dan konflik connector tetap dicatat. Tidak ada OD final, volume aktual, kalibrasi, operasi kereta atau simulasi kemacetan. M04 belum dimulai.
