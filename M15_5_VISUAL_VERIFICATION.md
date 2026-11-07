# M15.5 — Visual Verification and Performance

2 November 2026, WIB. Staging http://127.0.0.1:5201/.

MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.

PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.


## Keputusan setelah browser terbuka

**Browser functional workflow terverifikasi dengan batas pengujian; VISUAL QUALITY PENDING; PERFORMANCE CONDITIONAL; GEOSPATIAL PARTIAL.** Blocker Browser Use lama sudah teratasi setelah restart. Server5201 yang berhenti dinyalakan kembali. Laporan ini menggantikan status visual BLOCKED sebelumnya, bukan menaikkan validitas fisik jaringan.

## Pemeriksaan UI aktual

Rekaman500,1000,3000,5000 dipilih melalui UI. Kamera top-down, intersection dan rail, fullscreen/return, play/pause, kecepatan1/5/10, slider Home/End/PageUp/PageDown serta repeated switching diuji. Baseline3000 menampilkan1346tiba/568aktifakhir/1086pending terpisah dari current timestamp. Road selector `w562358500_s11_p0_0_f` menampilkan source562358500, lane2×101.25m, classes dan dua downstream connections. Pada t3240s:49active/49stopped,461distinct first-observed edge visits,600pendingorigin akhir. Count cohort tidak disebut count edge.

Save Scenario dan Duplicate→Save diuji. Input100 diubah999, kemudian Load memulihkan100. Generate dua kali pada nama original/salinan benar-benar menjalankan SUMO: run `db7bf706bc67e37ce0910eef` dan `9524cce7fcc0fd378229cf83`, exact road request cohort sama. Keduanya100requested/routed/loaded/departed/moved,93arrived,7active,0pending,0failed; independent FCD/XML audits PASS. Tidak ada console error/warning pada pemeriksaan browser. Ini menambah dua audit terpisah di luar delapan eksperimen utama.

## Bukti visual aktual

`documentation/m155/evidence/topdown-3000.jpg`, `intersection-5000.jpg`, `connectivity-origin.jpg`, `rail-camera.jpg` adalah screenshot browser baru. Teks screenshot cenderung lunak pada kualitas capture; nilai diperiksa lewat DOM, video watermark diperiksa terpisah. Screenshot `rail-camera.jpg` pada t688s berada setelah event crossing. Bukti tambahan `rail-crossing-1796.jpg` pada baseline5000 memperlihatkan kereta aktual di rel crossing, barrier tertutup dan antrean road; audit FCD baseline5000 juga menghasilkan0recorded offtrack/steady-red-entry. Tidak mengklaim clearance fisik lapangan. Validasi red-entry/offtrack tetap berasal dari FCD/controller audit yang tersimpan.

Video actual `documentation/m155/evidence/actual-playback.webm`:1280×800, durasi11.935s, 358decoded frames. Tombol recorder merekam live canvas baseline3000 pada1× sekitart3240s, dengan dua watermark, tanggal/WIB, timestamp dan statistik akhir. Frame5s diekstrak dengan FFmpeg dan diperiksa: gambar jalan/antrean aktual tampak, tulisan terbaca, tidak blank. Salinan MP4 H.264 juga tersedia di `actual-playback.mp4` untuk pemutaran umum. Ini rekaman aktual yang diberi overlay teks, bukan kendaraan sintetis/animasi pengganti. `video-frame-5s.png` adalah frame video, bukan screenshot UI.

![Frame actual video baseline3000](documentation/m155/evidence/video-frame-5s.png)

Renderer geometry/movement dipertahankan. Perubahan `world.tsx` hanya menambahkan telemetry median/camera/time/network version; bukan desain ulang atau perbaikan geometri. Kendaraan/road/context masih sederhana; visual tidak diberi premium/presentation aesthetic PASS. Desktop1920×1080 diuji; default panel sempit tidak otomatis mendapat sertifikasi layout responsif.

## Performa browser terukur

Raw 74files / 66render samples, 58sudah mempunyai FPSmedian. Retain semua sample lama dan baru, termasuk rendah. Page session maksimum tercatat604.2s. Ini durasi halaman terbuka, **bukan klaim seluruh waktu merupakan playback kontinu**. Segmen playback kontinu5000 teramati darit0s ke1494.2s pada10x (sekitar149s wall), kemudian seek1796untuk crossing dan resume menuju horizon. Long playback yang teramati dan timestamp ada di raw sample; background/offscreen serta switching tetap memengaruhi pengukuran. Tidak menyebut seluruh horizon60min dimainkan kontinu1× atau soak test berjam-jam.

| Run / kamera | Sampel | Median window-median FPS | Minimum window p5 | Active range | Max rolling stalls >50ms | JS heap MiB |
| --- | --- | --- | --- | --- | --- | --- |
| 49da5fe5c9c3f965850389e1 / junction | 2 | 119.8 | 116.3 | [24, 24] | 0 | [84.55599117279053, 85.44777297973633] |
| 49da5fe5c9c3f965850389e1 / topdown | 2 | 117.0 | 59.5 | [5, 19] | 0 | [79.75048065185547, 102.20217227935791] |
| 569df9741bf6f16d1cffa31e / junction | 15 | 59.9 | 17.1 | [226, 754] | 11 | [395.42245388031006, 1043.4921112060547] |
| 569df9741bf6f16d1cffa31e / rail | 4 | 119.0 | 116.3 | [688, 688] | 0 | [405.32516860961914, 509.67070960998535] |
| 569df9741bf6f16d1cffa31e / topdown | 15 | 59.9 | 40.0 | [46, 675] | 0 | [408.1583614349365, 485.0313959121704] |
| 9524cce7fcc0fd378229cf83 / junction | 2 | 119.0 | 117.6 | [4, 4] | 0 | [63.62509632110596, 81.69739818572998] |
| ae6c842a279f3d42d1dc9fbc / junction | 1 | 117.6 | 59.9 | [4, 4] | 0 | [130.33144855499268, 130.33144855499268] |
| ae6c842a279f3d42d1dc9fbc / topdown | 1 | 119.0 | 117.6 | [46, 46] | 0 | [212.67916202545166, 212.67916202545166] |
| cc419452a995456df324fd05 / junction | 2 | 119.0 | 117.6 | [137, 137] | 0 | [323.0827388763428, 494.43230628967285] |
| cc419452a995456df324fd05 / rail | 7 | 119.0 | 17.2 | [224, 378] | 9 | [335.29356956481934, 706.8078603744507] |
| cc419452a995456df324fd05 / topdown | 3 | 117.6 | 58.8 | [571, 575] | 0 | [336.26055240631104, 363.6778755187988] |
| db7bf706bc67e37ce0910eef / junction | 4 | 119.0 | 116.3 | [4, 4] | 0 | [64.02379322052002, 1115.4375562667847] |

Minimum p5 di seluruh sample yang dipertahankan:17.12FPS. JS heap maksimum1115.4MiB. Penurunan/stalls saat switching/video/fullscreen tidak dibuang. Tidak ada klaim seluruh sesi lancar atau bebas memory leak. Raw viewport, visibility/focus, speed, time, active, draw calls, memory dan run ID tersedia per file pada `browser-performance/`.

Pemuatan rekaman:

| Run | Wall ms | Frame | Positions |
| --- | --- | --- | --- |
| cc419452a995456df324fd05 | 2179.9 | 7200 | 3441615 |
| db7bf706bc67e37ce0910eef | 889.4 | 7200 | 37417 |
| 49da5fe5c9c3f965850389e1 | 668.1 | 7200 | 190992 |
| 9524cce7fcc0fd378229cf83 | 778.5 | 7200 | 37417 |
| 569df9741bf6f16d1cffa31e | 2823.4 | 7200 | 4550529 |
| cc419452a995456df324fd05 | 1806.6 | 7200 | 3441615 |
| ae6c842a279f3d42d1dc9fbc | 946.1 | 7200 | 707465 |
| 569df9741bf6f16d1cffa31e | 2618.0 | 7200 | 4550529 |

FPSwindow memakai rolling120frame; median dari window medians bukan median seluruh frame. P5 minimum adalah window terburuk yang tersimpan; stall rolling tidak dijumlahkan sebagai unique events. Raw sampling sekitar10s tidak menangkap semua stall. JS heap bukanVRAM. Perlu lebih banyak uji perangkat, sesi berjam-jam dan layout panel sempit sebelum janji stabilitas umum.

## Build, regression dan batas

TypeScript dan Vite isolated build terbaru PASS; chunk JS~832KB memberi warning>500KB. Backend model/permission/network tidak diubah saat visual QA. Regresi sebelumnya395tes/394pass/1skip tetap bukti backend; focused17 M15.5 diuji ulang setelah browser QA. Source/output manifests dan snapshot baseline dipertahankan. Original2984files diperiksa ulang saat finalisasi. Tidak menganggap API success sebagai bukti UI; workflow browser aktual dicatat di `browser-workflow.json`.

GeoJSON/source overlays tersedia, tetapi gate station/median/nama/double-track/clearance dan timing resmi belum dipastikan. Pending832lainnya tetapUNRESOLVED. Tidak ada flyover/M16/finalEXE/deletion/GitHub upload.
