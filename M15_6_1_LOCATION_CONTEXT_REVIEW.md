# M15.6.1 — Location Context Review

2 November 2026, WIB. Staging terpisah: http://127.0.0.1:5203/.

**ASSUMED CONTEXT MODEL.** Bentuk/posisi/tinggi bangunan bukan hasil survei.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.**


## Keputusan

**Review browser selesai.** Lima screenshot baru dan video aktual 49.94 detik tersedia. Kualitas lokasi **REQUIRES VISUAL REWORK**, bukan PASS. Tabel berikut adalah checkpoint source awal; penilaian aktual menggantikannya pada bagian akhir.

| Pertanyaan | Bukti source/model | Review visual aktual |
| --- | --- | --- |
| Masih terasa CBD/kota besar? | Tidak ada tower atau skyline; seluruh model rendah, maksimum 8.03 m termasuk atap | Tidak terlihat skyline/CBD dalam browser |
| Konteks Gedangan mulai terasa? | Road/rail freeze, OSM station anchor, referensi foto stasiun Gedangan, ruko/rumah beratap genteng | Terlihat konteks low-rise dan rail; identitas bangunan masih generik |
| Bangunan masih terlalu generik? | Ya, masih archetype. Footprint, posisi, tinggi, dan facade tetap asumsi | Harus tetap dicatat walaupun tampilannya nanti lebih baik |
| Jalan masih seperti mainan? | Source junction/centerline tidak diubah; hanya material dihaluskan | Close-up masih terasa model/mainan; tidak photorealistic |
| Lebih cocok untuk presentasi Gedangan? | Arah desain dan UI sudah disesuaikan | Lebih sesuai arah low-rise; belum presentation-grade |

## Approximation yang tetap ada

- Semua 550 building footprint, tinggi, posisi, jumlah, dan pemakaian plot; bukan inventaris aktual Gedangan.
- Modul ruko, shutter, kanopi, rumah, workshop, facade, warna, pagar, vegetasi, dan utilitas.
- Model stasiun 12×27 m dengan dinding 4.1 m dan atap 1.7 m. Penempatan render berjarak 18.00 m dari node OSM untuk menjaga envelope road/rail; bukan hasil ukur gedung.
- Road paint, furniture, lane-width/control assumptions warisan dan render height offsets.
- Kamera dan peta kecil adalah alat presentasi; tidak memberi kalibrasi lapangan baru.

## Sumber dan kekosongan data

Foto Stasiun Gedangan 2020 benar-benar diperiksa untuk karakter bangunan rendah; tidak mengesahkan kondisi 2026. Teks kajian PTDI-STTD 2024 memberi konteks geografis. OSM dan peta publik retained memberi road/rail provenance. Download footprint baru timeout. Citra satelit dan street-view positional reconstruction tidak diperoleh. Tidak ada foto udara ditempel atau skybox metropolitan.

## Paket review

- `M15_6_1_GEDANGAN_ENVIRONMENT_REPORT.md`.
- `documentation/m1561/source-register.json` dan foto sumber beratribusi.
- `environment-assets.json`, `context-placement-audit.json`, `context-tests.txt`.
- `preservation-after.json`, `ancestor-preservation.json`, `visual-status.json`.
- Source/build/staging terpisah di port 5203.

Bukti screenshot/video M15.6 tidak dipromosikan menjadi hasil M15.6.1. Blender tidak digunakan; tidak dibuat laporan Blender seolah ada export. Daftar lima screenshot dan metadata video aktual tersedia pada `visual-status.json`.

## Batas acceptance

Preservasi jaringan dan pemeriksaan geometri statis lulus. TypeScript, build, dan sepuluh tes konteks lulus. **Visual/location acceptance belum lulus: REQUIRES VISUAL REWORK** karena terlalu generik dan seperti model/mainan, meskipun arah metropolitan sudah dihindari. Tidak ada release final atau pekerjaan milestone berikutnya yang dimulai.

## Pemeriksaan browser aktual — 2 November 2026

Browser internal berhasil diakses setelah restart dan server port 5203 dihidupkan kembali. Lima screenshot aktual 1920×1080 tersedia pada `documentation/m1561/evidence`: overview.jpg, intersection.jpg, railway-crossing.jpg, frontage-relationship.jpg, dan presentation.jpg. Tangkapan memakai clip viewport eksplisit; hasil awal screenshot default terpotong sehingga diganti dengan tangkapan penuh, tanpa resize atau gambar buatan.

Video `actual-playback.webm` berasal dari recorder live canvas, 1920×1080, durasi **49.942472 detik**, ukuran 12,795,630 byte. Metadata diperiksa dengan ffprobe; frame detik 1, 30, dan 48 dirender dan diperiksa. Timestamp maju dari sekitar 1796 ke 1846 detik. Kamera overview/presentation beralih ke intersection selama perekaman. Video merekam canvas kendaraan/lingkungan beserta watermark; seluruh dashboard dan peta kecil ditunjukkan dalam screenshot, bukan disertakan sebagai DOM dalam video. Log warning/error browser yang dikembalikan saat pemeriksaan kosong.

Rekaman memakai hasil tersimpan M15.5 baseline-3000: 3000 diminta, 1914 berangkat/bergerak, 1346 tiba, 568 aktif akhir, 1086 belum berangkat. Ini playback aktual skenario random, bukan observasi lalu lintas Gedangan dan bukan pengujian SUMO baru. Kereta terlihat pada screenshot railway-crossing t=1796 detik; kendaraan dan antrean mengikuti rekaman.

**Keputusan visual: REQUIRES VISUAL REWORK.** Arah metropolitan sudah tidak terlihat. Ruko, rumah beratap genteng, workshop dan konteks stasiun rendah lebih sesuai konteks Indonesia. Namun bangunan masih berulang dan generik, jarak antarbangunan renggang, tanah relatif kosong, material dan detail tepi jalan sederhana. Jalan dan lingkungan masih terasa model/mainan. Kamera frontage memperlihatkan hubungan geografis, tetapi pada jarak itu bangunan dan kendaraan terlalu kecil untuk menilai detail. Identitas Gedangan terutama berasal dari jaringan jalan/rel dan anchor stasiun; bentuk lingkungan belum merupakan rekonstruksi lokasi yang dapat diverifikasi.

Target arah low-rise terpenuhi; target kualitas lingkungan realistis untuk presentasi belum lulus. Jangan menyebut hasil ini photorealistic, final release, atau real-location model tervalidasi. Prioritas perbaikan berikutnya dalam M15.6.1 adalah referensi footprint/facade koridor yang dapat diverifikasi, kontinuitas lingkungan tepi jalan, variasi aset, material tanah/tepi jalan dan framing frontage yang lebih terbaca, tanpa mengubah network atau traffic model.

Sepuluh tes konteks dijalankan ulang dan lulus. FPS UI singkat selama perekaman sekitar 59–72 dan setelah pause sekitar 106–120; ini bukan benchmark berkelanjutan atau bukti memory target lulus. Tidak ada klaim masalah heap M15.6 telah diperbaiki. Hash dan metadata bukti ada di `documentation/m1561/visual-status.json`.
