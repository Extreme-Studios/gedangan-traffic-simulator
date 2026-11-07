# PROJECT HANDOVER — GEDANGAN TRAFFIC SIMULATOR

**Status: FROZEN / SOURCE BACKUP VERIFIED.** Diperbarui 8 November 2026 (Asia/Jakarta). Pengguna membekukan pekerjaan. Jangan memulai fitur atau milestone baru sebelum ada permintaan lanjutan.

Repository: https://github.com/Extreme-Studios/gedangan-traffic-simulator . Titik source sebelum dokumen freeze: commit `3f1c4a3324f52e76c8801756e3421ae04c9bbdb6`. Snapshot saat itu 755 file / 47.750.835 byte; semua hash cocok dengan salinan persiapan. Perubahan freeze berikutnya hanya dokumentasi dan manifest. **Dokumen ini dan README adalah acuan status terkini; laporan milestone lama adalah catatan historis.**

## 1. Produk terakhir yang dilanjutkan

Versi aktif adalah **Simple 20K**, kelanjutan visual M15.6.2. Antarmuka satu kolom jumlah kendaraan (bilangan bulat 1–20.000) dan tombol Jalankan simulasi. Tidak mengembalikan editor OD, persentase per kelas, durasi, sinyal, atau kereta ke tampilan utama tanpa diminta pengguna.

Jumlah berarti total permintaan selama satu jam simulasi, bukan semua kendaraan tampil bersamaan. Campuran otomatis asumsi: motor 65%, mobil 22%, angkot 6%, truk ringan 4%, truk berat 2%, trailer 1%. Pembulatan largest remainder menjaga jumlah tepat. Komposisi ditampilkan segera, lalu SUMO menghitung hasil aktual sebelum diputar di 3D pada kecepatan 5×. Jumlah berangkat, tiba, masih di jalan, menunggu masuk, dan rute ditolak dibedakan.

- Frontend aktif: `frontend/src/simple`, konfigurasi `frontend/vite.simple.config.ts`, output lokal `frontend/dist-simple`.
- Backend aktif: `backend/gedangan/simple_server.py`, `simple_demand.py`, `simple_vehicles.py`, `simple_engine.py`, `simple_recording.py` dan modul `simple_*` lainnya. Modul ini memakai adaptor M04.5/M14/M15/M15.5 yang tetap disertakan.
- `simple_server` melayani API dan frontend di loopback; UI memanggil POST `/api/generate` dengan `{ "total": 100 }`, memantau GET `/api/jobs/<job_id>`, lalu membaca `/api/packed/<run_id>/index.json` dan chunk rekaman. POST `/api/preview` memeriksa demand tanpa menjalankan seluruh simulasi.
- Input kosong, pecahan, nol, negatif, dan >20.000 harus ditolak. Jangan memaksa rute gagal agar seluruh angka tampak lulus.
- Renderer memakai scene `documentation/simple/scene.json`. Worker memeriksa ukuran buffer Float64 dan mencoba ulang respons chunk tidak lengkap; jangan hapus pemeriksaan ini.

## 2. Batasan yang harus dipertahankan

**Pejalan kaki belum didukung.** Baseline tidak mempunyai jalur legal pedestrian. Jangan menampilkan pedestrian dekoratif sebagai peserta SUMO aktual. Angkot menggunakan proxy dimensi/perilaku van (delivery), bukan model angkot terkalibrasi. Trailer hanya mengikuti screening provisional yang diwarisi; belum ada sertifikat clearance lapangan, legalitas oversize, atau swept path.

Network, kapasitas, demand, campuran kendaraan, tinggi/fasad bangunan dan perilaku belum dikalibrasi terhadap survei Gedangan. Geometri konteks bersumber OSM; jangan menyebut angka skenario sebagai pengukuran atau prediksi terkalibrasi. Atribusi OpenStreetMap/ODbL harus dipertahankan. Frontage tetap terpisah; jangan membuat koneksi baru atau mengubah permission agar routing berhasil. Jangan gunakan vClass ignoring atau override TraCI untuk bypass.

Baseline immutable: `simulation/network/m155/provisional/network.net.xml`.
SHA256: `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`.
Jaringan M05.1 yang dipakai adaptor routing juga disertakan dan identik. Pertahankan bytes baseline, oneway, conditional access, larangan belok dan konektivitas. Koreksi jaringan baru, jika diminta, harus varian turunan dengan provenance.

## 3. Melanjutkan dari komputer baru

Gunakan Windows x64. Instal Python **3.12**, Node.js **22.12+** yang kompatibel dengan Vite 7, dan SUMO **1.28.0** dari sumber resmi. Tidak membutuhkan browser Codex untuk menjalankan aplikasi; Chrome/Edge dengan WebGL2 cukup.

Clone dengan konversi line ending dimatikan agar hash baseline tidak berubah:

```powershell
git -c core.autocrlf=false clone https://github.com/Extreme-Studios/gedangan-traffic-simulator.git
cd gedangan-traffic-simulator
git config core.autocrlf false
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r tests/requirements.txt
cd frontend
npm ci
npm run check:simple
npm run build:simple
cd ..
```

URL resmi dan versi/hash arsip SUMO tercatat di `configuration/sumo-m02.json`. Ekstrak distribusi lengkap sehingga tersedia:

```text
toolchain/sumo-win64-1.28.0/bin/sumo.exe
toolchain/sumo-win64-1.28.0/tools/traci/
toolchain/sumo-win64-1.28.0/tools/sumolib/
toolchain/sumo-win64-1.28.0/data/xsd/
```

Sertakan DLL dan notice/lisensi vendor. `activate()` menuntut toolchain berada di dalam root proyek; SUMO_HOME global atau junction menuju luar proyek akan ditolak. Jangan mengubah safeguard tersebut sekadar untuk lolos tes. `configuration/prepare_sumo_m02.py` tersedia sebagai source historis; periksa sebelum dijalankan karena dapat membuat artefak M02. Instalasi Python melalui requirements backend lain tidak diperlukan untuk entry point simple jika dependensi tests sudah terpenuhi.

Cek hash sebelum menjalankan:

```powershell
(Get-FileHash simulation/network/m155/provisional/network.net.xml -Algorithm SHA256).Hash
.venv/Scripts/python.exe -m backend.gedangan.simple_server --port 5206
```

Buka http://127.0.0.1:5206/ . Mulai uji 100 kendaraan, kemudian 3.000 atau 20.000 bila diperlukan. Network hash mismatch setelah clone dapat disebabkan konversi line ending: bandingkan raw blob atau unduh ZIP source GitHub; jangan mengganti hash EXPECTED untuk menutupi masalah.

Runtime output dibuat ulang di `simulation/runs/simple` dan `staging/simple/recordings`; keduanya diabaikan Git. Hasil lama tidak otomatis tersedia sesudah clone. Snapshot ZIP GitHub telah diverifikasi byte for byte; manifest `SOURCE_MANIFEST.json` mencatat berkas selain dirinya sendiri.

## 4. Bukti terakhir dan uji saat resume

Pada 8 November 2026, salinan source terpisah lulus npm ci, TypeScript dan build Vite simple. Uji SUMO 1.28.0 nyata dengan 100 permintaan: 98 mendapat rute, 98 berangkat/bergerak, 92 tiba, 6 masih di jalan dan 2 rute ditolak. Seluruh enam kategori bergerak. Ini hasil uji sebelum freeze, bukan klaim pengujian ulang di komputer berikutnya.

Uji 20.000 pada 6 November 2026: 19.574 routed, 426 ditolak, 3.569 berangkat/bergerak, 2.891 tiba, 678 masih di jalan dan 16.005 menunggu masuk pada akhir satu jam. Tidak tercatat teleport, collision, atau illegal permission. Waktu hitung mesin saat itu sekitar 440 detik; bukan target performa universal. Ringkasan tercantum di `documentation/simple/SIMPLE_UI_REPORT.md`; file FCD/rekaman besar tidak diunggah.

Saat resume: jalankan TypeScript/build, cek manifest/hash jaringan, uji 100 permintaan di SUMO, verifikasi movement dan arrival keenam kategori, penolakan input 20.001, komposisi tepat 20.000, pengunduhan chunk dengan ukuran benar dan playback aktual di browser. Periksa `illegal_permissions`, `teleports`, `collisions`, pending insertion dan rejected routes di result.json; jangan hanya melihat jumlah route sukses. Jangan menjalankan seluruh tes milestone lama lalu mengasumsikan semua dataset historis tersedia.

## 5. Membuat ulang EXE portable

EXE merupakan launcher C# Windows yang menjalankan server Python/SUMO lokal lalu membuka dashboard di browser default. Ini bukan aplikasi 3D native standalone. ZIP EXE yang sudah dibuat **tidak ada di GitHub** dan tidak dapat diunduh dari Releases repository ini.

Setelah dependensi, toolchain lengkap dan build frontend siap, gunakan source packaging:

```powershell
.venv/Scripts/python.exe staging/m1562/portable/build_simple.py staging/simple/portable/release-build
```

Compiler yang dipakai skrip: `C:/Windows/Microsoft.NET/Framework64/v4.0.30319/csc.exe`. Build menggunakan runtime CPython lokal; versi Python 3.12 penting karena nama DLL hardcoded. Hasil: `staging/simple/portable/release-build/GEDANGAN_TRAFFIC_SIMULATOR_SIMPLE_20K_PORTABLE/`. Pertahankan EXE bersama folder App; jangan menyalin EXE saja.

Skrip `verify_simple.py` mengharapkan hasil ekstraksi di `staging/simple/portable/qa/GEDANGAN_TRAFFIC_SIMULATOR_SIMPLE_20K_PORTABLE/`. Siapkan folder itu dari paket baru lalu jalankan skrip. Verifikasi launcher, SUMO bawaan, kelas bergerak, batas input dan seluruh chunk. Jangan memasukkan hasil tes, runtime atau source ZIP ke riwayat Git. Build helper belum mengotomatiskan keseluruhan laporan/manifest/ZIP final; packaging final harus menyertakan README_FIRST.md, MASTER_REPORT.md, PROJECT_HANDOVER.md dan bukti penting, kemudian CRC/extraction/hash check.

## 6. Yang tersimpan dan yang tidak

GitHub menyimpan source, lockfile/config, tes, laporan teks, scene dan data jaringan minimum simple mode, serta source pembuat portable. Snapshot source awal diverifikasi 755/755 file. Dokumen freeze ini menambah satu berkas; manifest diperbarui untuk revisi dokumen.

**Tidak tersimpan di GitHub:** EXE/ZIP portable final, Python/npm/SUMO terpasang, raw/historical observation database, ekspor frontend public, seluruh FCD/rekaman/screenshot/video, output eksperimen dan artefak presentasi besar. Sebagian dapat dibuat ulang dari source; hasil eksperimen historis dan data observasi yang tidak diunggah tidak dapat dipulihkan hanya dari repository. Laporan lama yang merujuk path lokal tidak membuktikan berkas itu ada di GitHub.

Permintaan freeze dan handover ini bukan instruksi menghapus folder lokal. Bila pengguna kemudian memilih membuang riwayat lokal, jelaskan bahwa aplikasi dapat dikembangkan lagi dari source tetapi arsip penelitian yang tidak dibackup akan hilang. Simpan satu ZIP portable terbaru di luar folder proyek bila pengguna masih ingin menjalankan build lama tanpa rebuild.

## 7. Prompt siap tempel untuk melanjutkan

> Lanjutkan Gedangan Traffic Simulator dari https://github.com/Extreme-Studios/gedangan-traffic-simulator . Baca PROJECT_HANDOVER.md, README.md dan SOURCE_MANIFEST.json terlebih dahulu. Proyek terakhir dibekukan pada Simple 20K: satu input 1–20.000 kendaraan per satu jam, campuran otomatis enam kelas, backend SUMO 1.28.0 dan frontend React/Three.js. Pulihkan dependency/toolchain lokal, verifikasi hash network immutable, lalu jalankan smoke test 100 kendaraan dan playback aktual sebelum mengubah fitur. Jangan menganggap dataset/EXE/rekaman historis ada di repository. Pejalan kaki belum legal, angkot masih proxy van, trailer tetap provisional, model belum terkalibrasi. Jangan rusak yang sudah benar; ubah hanya lapisan yang diperlukan. Tanyakan tujuan lanjutan bila belum ditentukan. Jangan memulai milestone baru, menghapus data, mengganti geometri/permission atau mengunggah EXE tanpa permintaan pengguna.
