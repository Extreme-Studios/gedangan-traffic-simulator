# Gedangan Traffic Simulator — M10

Presentasi teknis dengan rekaman SUMO aktual. Demand, timing dan konteks bangunan tetap ilustratif; ini bukan hasil pengukuran kemacetan Gedangan.

Tanggal: 1 November 2026. M11/M12 tidak dimulai.

Jalankan `START_GEDANGAN_M10.bat` dari folder utama proyek. Alamat M10: **http://127.0.0.1:5186/visual.html**. M09 tetap tersedia terpisah pada port 5185. Browser internal telah berhasil membuka M10 dan memperlihatkan rekaman 3D.

Tunggu tombol **START PRESENTATION** aktif. Lima rekaman utama dimuat terlebih dahulu. Tidak diperlukan internet, Node, SUMO live, login, perubahan firewall, atau layanan berbayar untuk menjalankan hasil build. Python lokal proyek tetap diperlukan. Tutup layanan melalui tombol **Tutup layanan M10**, atau Ctrl+C pada terminal layanan.

Untuk presentasi, gunakan START PRESENTATION, lalu Fullscreen. Tombol Sebelumnya/Berikutnya atau tombol panah memindahkan sepuluh bagian; Escape keluar. Space mengendalikan playback saat fokus tidak berada di input/tombol. Timeline dapat digeser, diulang, dan diputar 0.5× hingga 16×. Memilih tahun/skenario tanpa rekaman menghasilkan NOT RUN, bukan rekaman pengganti.

Kamera: aerial, main, reverse, intersection, railway, frontage, follow dan free orbit. Simpan sudut/Buka sudut menyimpan satu bookmark selama sesi. Reset kamera mengembalikan komposisi preset; free orbit membatasi zoom dan kemiringan. Klik kendaraan atau pilih kendaraan aktif di Analisis & filter, lalu Ikuti pilihan.

Overlay tersedia di bawah kanvas:

- Kendaraan berhenti & ekor: merah untuk speed <0.3 m/s; cincin amber menunjukkan posisi depan kendaraan berhenti paling belakang pada setiap lajur. Ini sampel posisi, bukan antrean yang sudah diverifikasi sebab/durasinya.
- Occupied lane length: panjang badan kendaraan yang diproyeksikan pada lajur, gabungan interval yang tumpang tindih, dibagi panjang lajur. Ini bukan detector occupancy. Warna hijau ke amber/merah menunjukkan proporsi ruang, bukan random heatmap.
- Jalan utama/frontage: arterial amber, frontage turquoise. Tidak menggabungkan geometri atau akses kedua jalan.

Jumlah aktif/berhenti dan state perlintasan/APILL mengikuti rekaman. Hasil spillback pada kartu adalah total episode dalam horizon dari run, bukan klaim bahwa sebuah kejadian sedang berlangsung pada posisi timeline sekarang. Peta sebab bottleneck/antrean berdurasi belum tersedia pada overlay ini; jangan menyamakannya dengan warna occupied length. Geometri pendek/angular pada jaringan sumber tetap dipertahankan. Tidak ada pengesahan clearance atau swept path.

Statistik horizon 0–2100 s dipisahkan menjadi requested, routable, failed routes, loaded, departed, not departed, running at end dan arrived. **NOT ARRIVED BY SIMULATION END = requested − arrived**, mencakup gagal rute, belum berangkat dan masih berjalan. Completion memakai arrived/requested dalam horizon 35 menit. Throughput model bukan kapasitas jalan terukur; elapsed departed cohort bukan arrived-only mean untuk semua demand.

Untuk memperlihatkan hasil negatif, pilih 2040 / HIGH / Alternatif timing APILL / COMPARISON. Cohort, seed dan horizon harus cocok. Baseline **356 arrived** versus intervensi **328 arrived** ditampilkan sebagai **WORSENED IN THIS SIMULATION · ARRIVED ONLY**. Status hanya menyatakan perubahan jumlah tiba; waiting, unfinished trips dan spillback tetap perlu dibaca bersama. Tidak ada penetapan solusi terbaik atau rekomendasi kebijakan otomatis.

S06/S07 menampilkan skema transparan tanpa alignment teknis: **CONCEPTUAL INFRASTRUCTURE — ENGINEERING FEASIBILITY NOT VERIFIED**. Tidak ada ramp buatan, kendaraan melintasi konsep, metrik efektivitas, atau klaim kelayakan.

Bukti visual dan distribusi:

- `presentation_demo/m10/screenshots/01_intro.png` sampai `12_presentation.png`.
- `presentation_demo/m10/M10_VISUAL_CONTACT_SHEET.png`.
- `presentation_demo/m10/GEDANGAN_3D_DEMO.mp4` setelah capture/transcode berhasil; statusnya dinyatakan dalam laporan penerimaan.
- `presentation_demo/m10/acceptance.json` dan `documentation/M10_PRESENTATION_ACCEPTANCE.md` adalah keputusan penerimaan, bukan status historis M09.

Source M10 berada di `frontend/src/m10/`; build di `frontend/dist-m10/`; host stdlib di `backend/gedangan/m10_server.py`. Data gerakan tetap dibaca dari cache M09 yang hash-nya diverifikasi sebelum host berjalan. Tidak menulis ulang network, demand, registry, trajectory atau laporan milestone lama.

Rebuild memakai `REBUILD_VISUAL_M10.bat`; memakai TypeScript/Vite lokal yang sudah terpasang. Tidak mengunduh dependency. Validasi core: `node tests/m10/test_core.cjs`. Regresi lama: `.venv\Scripts\python.exe -m unittest discover -s tests -v`. Browser QA memakai installed Chrome dan Playwright dari bundled runtime; environment `M09_RUNTIME_PACKAGES` menunjuk direktori `node_modules` runtime tersebut. Nama environment ini dipertahankan agar harness lama tetap kompatibel.

Urutan QA: baseline M09, build M10, `tests/m10/browser-qa.cjs`, `class-qa.cjs`, `capture.cjs`, `performance.cjs`, `capture.cjs --video`. Jangan rebuild build yang sedang dipakai tes. Video direkam dari UI aktual, lalu ditranscode ke H.264 Full HD menggunakan FFmpeg lokal. Contact sheet hanya mengomposisikan screenshot aktual.

Jalankan `.venv\Scripts\python.exe -m backend.gedangan.m10_checkpoint --verify` untuk memeriksa 7055 file lama. Checkpoint mengecualikan namespace M10, dependency/toolchain, SQLite hidup/cache/locks dan log telemetry browser M09 yang append-only. Lihat `documentation/m10/baseline-scope.json` untuk cakupan tepatnya.

Sebelum rapat, buka launcher, tunggu preload, pilih adegan, lalu gunakan Fullscreen. Jangan menjalankan profiling berat bersamaan dengan demo. Angka performa dalam laporan berlaku untuk workload dan perangkat yang benar-benar diuji; bukan jaminan untuk semua GPU. Tidak ada klaim 6 GB VRAM dari shared-memory adapter.

Paket offline `presentation_demo/m10/GEDANGAN_M10_PRESENTATION_PACKAGE.zip` menyertakan build, cache rekaman asli, host stdlib dan bukti M10. Ekstrak seluruhnya lalu jalankan START_GEDANGAN_M10.bat; Python yang sudah tersedia tetap diperlukan. Paket ini bukan backup seluruh workspace penelitian 16 GB. Verifikasi 7055 file dan regresi legacy berlaku pada workspace asli.

Perekaman sesi ini memakai executable FFmpeg lokal yang sudah terpasang, disalin ke cache tooling M10 agar dikenali perekam Playwright. Tidak ada unduhan atau instalasi dependency baru. Binary tooling dan WebM mentah tidak dimasukkan ke paket offline.
