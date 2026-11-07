# M15.6.2 — Memory Optimization Report

2 November 2026, WIB. Staging terpisah: http://127.0.0.1:5204/.

**REVIEW REQUIRED — menunggu pengguna memeriksa video aktual.**

MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION. PROVISIONAL NETWORK — NOT FIELD CALIBRATED.

## Akar beban dan perubahan

Decoder lama menahan seluruh posisi sebagai array JavaScript bersarang: 3,441,615 posisi pada demand3000 dan 4,550,529 pada demand5000. Loading empat chunk JSON sekaligus juga membuat object graph sementara. Renderer lama memindai semua frame untuk capacity kendaraan. Ini menjelaskan overhead yang ditargetkan; bukan klaim heap profiler membuktikan setiap byte atau leak tertentu.

Transport baru mengemas enam field asli dalam Float64 little-endian. Tidak menggunakan Float32/quantization, tidak memotong frame, posisi, vehicle totals atau SUMO output. Worker mengambil chunk berurutan lalu mentransfer ArrayBuffer; main thread menyimpan buffer dan descriptor frame. Maksimum tiga frame yang dimaterialisasi menjadi tuple disimpan dalam cache. Capacity maksimum dihitung dari seluruh rekaman di preprocessing. Switch membatalkan worker sebelumnya, dan unmount membatalkan loading. Peta sumber diperbarui satu kali/detik; frame traffic tetap mengikuti timestamp asli dan interpolasi warisan.

Verifikasi penuh membandingkan **semua enam field di semua 7,992,144 posisi** kedua run, termasuk times/frame descriptors, vehicle registry, events dan metrics. Dua run masing-masing tetap 7200 frame. Hasil EXACT_FLOAT64_EQUAL ada di `lossless-verification.json`. Buffer source3000 157.54 MiB; source5000 208.31 MiB. File SUMO/JSON/gzip asli hanya dibaca.

## Before/after aktual

| Kasus | Sampel | Median window FPS | Worst window p5 FPS | Max browser heap MiB | Typed MiB | Heap + typed konservatif MiB |
| --- | --- | --- | --- | --- | --- | --- |
| baseline_3000 | 4 | 88.0 | 58.8 | 659.4 | 0.0 | 659.4 |
| baseline_5000 | 4 | 60.2 | 40.0 | 1078.0 | 0.0 | 1078.0 |
| corrected_3000 | 4 | 117.0 | 59.2 | 291.8 | 157.5 | 449.4 |
| corrected_5000 | 4 | 114.9 | 59.5 | 617.9 | 208.3 | 826.2 |

Satu interval45s per kasus, analisis detik5–45, perangkat sama, viewport1920×1080/DPR1, kamera junction, context on, speed1x, overlay none, mulai t1800. Baseline memakai source/build M15.6.1 melalui server5205 dengan telemetry diarahkan ke folder M15.6.2; corrected5204 memakai build `m1562-iYjj4v-k.js`. Raw exploratory windows, transisi dan pengamatan yang lebih lama tetap disimpan; tidak dicampur untuk mempercantik interval final. Semua raw filename/UTC dan resource GPU ada di `benchmark-summary.json`.

`performance.memory` adalah metrik browser, bukan total process RAM/VRAM. Typed bytes disajikan terpisah; penjumlahan konservatif bisa menghitung sebagian byte dua kali karena accounting browser. Target lama3000≤800MiB terpenuhi pada interval ini, termasuk penjumlahan konservatif. Pada5000, penjumlahan konservatif masih melebihi800MiB; jangan klaim semua demand memenuhi batas tersebut. Garbage collection saat switch tidak dipaksa. Penurunan heap bukan sertifikat bebas leak atau kapasitas VRAM.

Aset lingkungan dibatch per material; kendaraan tetap instanced. Cleanup renderer lama dipertahankan untuk controls, RAF, resize observer, listeners, geometry, materials, textures dan renderer. Tidak ada salinan texture per bangunan; hanya tekstur grain bersama dan sign stasiun. Peta SVG dimemoisasi. Capture memakai stream layar aktual, potongan data video sementara, timer tour dihentikan pada stop dan semua media tracks dihentikan. Rekaman video dapat menambah RAM sementara; bukan bagian interval benchmark.

Tidak dilakukan soak multi-jam atau GPU memory profiler. Device/power/thermal/background activity tidak dikendalikan sebagai eksperimen laboratorium; perubahan FPS tidak boleh dipresentasikan sebagai hasil penelitian lalu lintas Gedangan. M15.6 historis pernah mencapai>1.5GiB; tabel ini adalah pengukuran baru dengan protokol tercatat, bukan menulis ulang laporan lama.
