# M15.6.1 — Gedangan Environment Report

2 November 2026, WIB. Staging terpisah: http://127.0.0.1:5203/.

**ASSUMED CONTEXT MODEL.** Bentuk/posisi/tinggi bangunan bukan hasil survei.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.**


## Status

Arah visual baru sudah diimplementasikan dan diperiksa dalam browser. Lima screenshot 1920×1080 dan video aktual 49.94 detik tersedia. **Visual acceptance: REQUIRES VISUAL REWORK**, dengan alasan dan bukti pada pemeriksaan browser aktual di bawah.

## Lingkungan yang diubah

Blok massing lama diganti dengan 550 model rendah: 164 ruko, 263 rumah, 122 workshop, dan satu model konteks stasiun. Tinggi dinding maksimum 6.40 m; termasuk atap maksimum 8.03 m. Tidak ada tower, gedung kaca, skyline CBD, atau skybox perkotaan.

Ruko memakai modul rolling shutter, kanopi, dan bukaan lantai atas bila dua lantai. Rumah memakai atap pelana berwarna genteng, bukaan sederhana, dan pagar rendah. Workshop memakai atap metal. Palet cream, abu, sage, dan bata dibuat tenang. Beberapa plot mempunyai pohon kecil, bentuk tanaman menyerupai palem, dan tiang utilitas. Bentuk, spesies, ukuran, jumlah, posisi, dan pemakaian plot semuanya asumsi visual.

Ada 81 model dalam radius 500 m koordinat lokal simpang. Bangunan mengikuti arah koridor sumber dengan setback dan celah bervariasi. Tidak ada akses jalan baru yang dibuat untuk bangunan. Area yang tidak lolos pemeriksaan ruang tetap dibiarkan kosong.

## Stasiun dan referensi lokasi

Anchor stasiun berasal dari retained OSM node 1359952188. Model konteks memakai dinding cream/grey, atap genteng miring, teritis, dan bukaan berulang. Referensi karakter adalah [foto Stasiun Gedangan 2020](https://commons.wikimedia.org/wiki/File:Stasiun_Gedangan_2020.jpg), karya Rizal Febri Ardiansyah, 12 September 2020, berlisensi [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Foto lokal benar-benar diperiksa; hash dan atribusi ada pada source register. Foto tidak ditempel sebagai facade, aerial background, atau pengganti model 3D.

Model stasiun berukuran asumsi 12×27 m, dinding 4.1 m dan atap 1.7 m. Anchor render berjarak 18.00 m dari node sumber agar tidak menutupi road/rail buffer. Ini keputusan penempatan visual, bukan ukuran footprint atau gate stasiun yang terverifikasi. Label GEDANGAN menandai konteks, bukan sertifikasi rekonstruksi gedung aktual.

[Kajian PTDI-STTD 2024](https://digilib.ptdisttd.ac.id/8270/) memberi konteks simpang utama, simpang stasiun, frontage, dan rel. Teks publik diperiksa, tetapi screenshot PDF timeout; tidak mengklaim foto PDF berhasil diperiksa. Proposal infrastruktur dalam penelitian tidak dimasukkan sebagai kondisi eksisting.

Retained OSM 31 Oktober 2026 dan [Peta Jalan Pemkab Sidoarjo](https://sidoarjokab.go.id/peta-jalan) tetap menjadi referensi geografis road/rail. Attempt baru untuk building footprint melalui Overpass Kumi timeout. Tidak ada footprint baru, citra satelit, atau rekonstruksi posisi dari street view yang berhasil diperoleh. Karena itu semua bangunan tetap **ASSUMED CONTEXT MODEL**. Foto historis tidak dipakai untuk mengklaim kondisi lengkap 2026.

## Jaringan dibekukan dan ruang kendaraan dilindungi

Network SHA256 tetap `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. Lane shape, junction polygon, signal heads, presets, crossing, dan bounds sama persis dengan scene M15.6. Alignment jalan/rel, frontage, width, median, legal turning, permissions, demand, traffic model, dan statistik tidak diubah.

Polygon penuh setiap model, termasuk margin kanopi dan pad, diperiksa terhadap seluruh lane asli. Buffer road memakai setengah lebar SUMO ditambah 2.5 m; rail memakai buffer 7 m dari centerline. Hasil: nol overlap dengan envelope tersebut dan nol overlap antarmodel. Transform yaw mengikuti konversi XY SUMO ke X/−Z renderer. Pemeriksaan ini adalah screen geometri model, bukan sertifikat clearance bangunan atau swept path lapangan.

Kereta, lampu, palang, kendaraan, dan arah gerak tetap memakai actual playback. Tidak ada track balik, platform operasional, akses stasiun, atau jalan tambahan yang dibuat. Kelas yang gagal rute tetap gagal; konteks visual tidak menambah kendaraan bergerak.

## UI dan kamera

Dashboard/header gelap, viewport dominan, analytics, current/end statistics, Inspector, dan watermark dipertahankan. Preset baru adalah Overview Gedangan, Frontage Relationship, dan Presentation Dashboard. Kamera main corridor, close-up junction, rail, follow, top-down, aerial, dan orbit tetap tersedia.

Frontage Relationship memakai midpoint antara preset frontage asli dan crossing. Frontage tidak dipindah agar terlihat dekat. Peta jaringan kecil memakai koordinat SUMO dan titik kendaraan aktual yang disampel untuk keterbacaan; active count tidak dikurangi. Material aspal dihaluskan melalui noise dan UV rendering, bukan perubahan geometri.

Recorder disiapkan untuk 50 detik live canvas 1920×1080 dengan watermark, timestamp, dan end counts. Recorder telah dijalankan; video aktual dan metadata tersedia. Hanya FPS UI singkat yang diamati; masalah memori M15.6 belum dinyatakan selesai.

## Aset dan Blender

Blender tidak digunakan. Aset dibuat native procedural Three.js agar batching, material, dan provenance penempatan dapat diperiksa langsung. Tidak ada file blend/GLB atau klaim export Blender. Karena Blender tidak dipakai, laporan Blender opsional tidak dibuat.

Daftar aset ada di `documentation/m1561/environment-assets.json`: ruko rendah, rumah beratap genteng, workshop, konteks stasiun, vegetasi, utilitas, dan plot tanah. Source berada di `frontend/src/m1561/LocalContext.ts`. Vehicle asset dan traffic logic lama dipertahankan. Tidak ada paid asset, generated photo, aerial-photo-as-3D, atau brand bangunan rekaan.

## Pengujian dan preservasi

Sepuluh tes M15.6.1 lulus: network hash, kesamaan scene, batas low-rise, label asumsi, pemeriksaan polygon penuh, pemisahan bangunan, batas anchor stasiun, hash foto, hasil parent tetap utuh, dan XML identik. TypeScript dan isolated Vite build lulus. Chunk JS sekitar 850.57 KB masih memberi warning lebih dari 500 KB. Ini bukti kode/model, bukan bukti kualitas visual atau performa browser.

Preservasi M15.6: 604 file lama diperiksa, status PASS, tanpa perubahan. Checkpoint ancestor 2984 file juga hash-equal melalui pembandingan read-only; laporan parent tidak ditulis ulang.

Staging berada di port 5203, source `frontend/src/m1561`, build `frontend/dist-m1561`, evidence/data `documentation/m1561`, dan launcher `staging/m1561/START_M1561.ps1`. M12 hingga M15.6 tidak ditimpa. Tidak ada penghapusan, upload GitHub, final EXE, atau milestone lanjutan.

## Rencana pemeriksaan awal (sudah dilaksanakan; hasil di bawah)

Setelah Browser Use aktif: ambil screenshot overview, intersection, railway crossing, frontage relationship, dan presentation mode pada 1920×1080. Periksa atap, facade, ground contact, coverage koridor/stasiun, serta posisi kendaraan dan kereta. Rekam actual playback 45–60 detik lalu periksa frame awal/tengah/akhir serta metadata. Nilai kecocokan lokasi secara jujur; jangan memberikan PASS jika masih terasa metropolitan atau seperti arena mainan.

## Pemeriksaan browser aktual — 2 November 2026

Browser internal berhasil diakses setelah restart dan server port 5203 dihidupkan kembali. Lima screenshot aktual 1920×1080 tersedia pada `documentation/m1561/evidence`: overview.jpg, intersection.jpg, railway-crossing.jpg, frontage-relationship.jpg, dan presentation.jpg. Tangkapan memakai clip viewport eksplisit; hasil awal screenshot default terpotong sehingga diganti dengan tangkapan penuh, tanpa resize atau gambar buatan.

Video `actual-playback.webm` berasal dari recorder live canvas, 1920×1080, durasi **49.942472 detik**, ukuran 12,795,630 byte. Metadata diperiksa dengan ffprobe; frame detik 1, 30, dan 48 dirender dan diperiksa. Timestamp maju dari sekitar 1796 ke 1846 detik. Kamera overview/presentation beralih ke intersection selama perekaman. Video merekam canvas kendaraan/lingkungan beserta watermark; seluruh dashboard dan peta kecil ditunjukkan dalam screenshot, bukan disertakan sebagai DOM dalam video. Log warning/error browser yang dikembalikan saat pemeriksaan kosong.

Rekaman memakai hasil tersimpan M15.5 baseline-3000: 3000 diminta, 1914 berangkat/bergerak, 1346 tiba, 568 aktif akhir, 1086 belum berangkat. Ini playback aktual skenario random, bukan observasi lalu lintas Gedangan dan bukan pengujian SUMO baru. Kereta terlihat pada screenshot railway-crossing t=1796 detik; kendaraan dan antrean mengikuti rekaman.

**Keputusan visual: REQUIRES VISUAL REWORK.** Arah metropolitan sudah tidak terlihat. Ruko, rumah beratap genteng, workshop dan konteks stasiun rendah lebih sesuai konteks Indonesia. Namun bangunan masih berulang dan generik, jarak antarbangunan renggang, tanah relatif kosong, material dan detail tepi jalan sederhana. Jalan dan lingkungan masih terasa model/mainan. Kamera frontage memperlihatkan hubungan geografis, tetapi pada jarak itu bangunan dan kendaraan terlalu kecil untuk menilai detail. Identitas Gedangan terutama berasal dari jaringan jalan/rel dan anchor stasiun; bentuk lingkungan belum merupakan rekonstruksi lokasi yang dapat diverifikasi.

Target arah low-rise terpenuhi; target kualitas lingkungan realistis untuk presentasi belum lulus. Jangan menyebut hasil ini photorealistic, final release, atau real-location model tervalidasi. Prioritas perbaikan berikutnya dalam M15.6.1 adalah referensi footprint/facade koridor yang dapat diverifikasi, kontinuitas lingkungan tepi jalan, variasi aset, material tanah/tepi jalan dan framing frontage yang lebih terbaca, tanpa mengubah network atau traffic model.

Sepuluh tes konteks dijalankan ulang dan lulus. FPS UI singkat selama perekaman sekitar 59–72 dan setelah pause sekitar 106–120; ini bukan benchmark berkelanjutan atau bukti memory target lulus. Tidak ada klaim masalah heap M15.6 telah diperbaiki. Hash dan metadata bukti ada di `documentation/m1561/visual-status.json`.
