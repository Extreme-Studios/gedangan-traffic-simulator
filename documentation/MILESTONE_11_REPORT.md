# MILESTONE 11 — Paket Presentasi Teknis Gedangan

**TECHNICAL PRESENTATION PACKAGE READY PASS**

Tanggal: 1 November 2026, Asia/Jakarta. Lingkup hanya M11.

## Executive summary

Paket berisi aplikasi M10 yang dipakai kembali, launcher satu langkah, deck 15 slide Indonesia, PDF 15 halaman, deck HTML offline dengan penjelasan Eksekutif/Teknis, video M10 aktual 106,4 detik, naskah 5/15 menit, lembar diskusi dua halaman, checklist, lampiran teknis dan referensi tanya jawab. Posisi produk: GEDANGAN TRAFFIC SIMULATOR, 3D Traffic Digital Twin & Scenario Analysis, EXTREME STUDIOS. Status ilmiah PRESENTATION-READY ILLUSTRATIVE TRAFFIC SIMULATION; baseline 2026 NOT EMPIRICALLY CALIBRATED.

## Source audit dan reuse M10

Laporan M09/M10, initial/final audit, acceptance, contact sheet, video, browser/class evidence, source renderer/runtime, 23 recording indexes, scenario manifests, M06 empirical gate dan kesiapan M08.5 diperiksa. Audit sumber dan hash per berkas tersimpan pada qa/source-audit.json. 95 berkas manifest M10 cocok. Video M11 adalah salinan byte-identical dari video M10 dan benar-benar dimainkan melalui elemen video Chrome. Tidak ada footage simulasi buatan. Sumber/caption screenshot M10 dipertahankan.

Checkpoint M11 melindungi 8104 file lama, 17.301.071.597 byte, source checkpoint 726 file. Daftar hash dan scope berada di documentation/m11. Exclusions: M11 namespace, installed dependencies/toolchain, caches/locks, SQLite hidup/WAL dan telemetry append-only M09/M10. M11 testing menggunakan port terisolasi dan log M11; output/source/network/data M01–M10 tidak ditimpa.

## Changes made

Tidak ada frontend 3D baru. Build dan renderer M10 tetap byte-identical. m11_launch.py memakai host M10 yang sama, protokol service/port detection yang kompatibel, preflight hash seluruh cache, instance reuse dan clean shutdown. Service yang dibuat M11 mengalihkan telemetry ke namespace M11. Port produksi 5186; port 5187/5188 hanya uji terisolasi.

Adapter presentasi M11 menambahkan stylesheet/skrip lewat response HTML, bukan menulis ulang build M10. CSS ringkas memperbaiki ruang kanvas pada 1366×768 dengan zoom 150%. Skrip hanya memperjelas pesan pemulihan agar path teknis tidak tampil kepada audiens. Tidak mengubah metrics, routes, controller, FCD, camera math, demand atau playback lifecycle. Halaman awal lokal memisahkan verifikasi disk dari preload browser: START tetap diblokir sampai preload M10 selesai. Pemilihan rekaman lain memiliki indikator loading dan tidak memakai run pengganti.

## Deck dan bahan pertemuan

Urutan 15 slide mengikuti brief: cover, pertanyaan lalu lintas, area, 3D, kendaraan/simpang/rel, SUMO, baseline, growth, indikator, skenario, comparison, konsep infrastruktur, keterbatasan, survei dan penutup. Native tables pada slide 7/10, native chart pada slide 8, editable text dan speaker notes. Grafik memakai snapshot literal dari angka audit; tidak mengklaim formula source workbook dipertahankan. Final PPTX lolos pemeriksaan integritas/layout/font/chart workbook dan first-party import. Semua slide final diimpor ulang dan dirender. PDF statis memakai render 1920×1080 tersebut; bukan file kosong. Review individual dan contact sheet ada pada qa/visual-review.json dan M11_SLIDE_CONTACT_SHEET.png.

Naskah menjelaskan tampilan, sumber, makna, batas dan pertanyaan audiens pada sepuluh bagian. Durasi naskah merupakan target, bukan klaim kecepatan bicara manusia. Mode Eksekutif/Teknis pada deck HTML hanya mengganti kedalaman catatan dari satu file konten, tanpa dataset kedua. Materi utama bebas terminal, raw JSON, benchmark dan stack trace. Lampiran audit/provenance disimpan terpisah.

Tujuh calon lokasi M06/M08.5 dipertahankan dan tidak dianggap disetujui. Lembar rapat menyediakan ruang keputusan tentang ruas/arah, izin, posisi aman, sesi, kelas, turning, event palang, fase sinyal, travel time, antrean/count/meter/censoring, hambatan samping, QC, PIC dan kelengkapan. Tidak ada keputusan peserta yang diisi otomatis.

## Numeric data audit

Semua 23 run memiliki ID, tahun, scenario/growth, seed, horizon, manifest/index hash, units, definisi dan provisional classification. Accounting: requested=routable+failed routes; routable=departed+not departed; departed=arrived+running; not arrived=requested-arrived. Baseline 2026 S00 REFERENCE: requested 240, routable/departed 206, arrived 183, running 23, failed 34, not departed 0, not arrived 57. Identitas ini diverifikasi terhadap index asli.

Pasangan 2040 HIGH comparable: S00 f6b49f6119ee784cf062 arrived 356 / requested 500; S01 9c9e07a0a18d0cfec64f arrived 328 / requested 500. Delta -28, WORSENED IN THIS SIMULATION untuk arrived. Running 80/102, not departed 8/14, failed routes 56/56, not arrived 144/172. Waiting mean departed bersyarat, bukan manfaat seluruh demand. Growth REFERENCE requested 240/269/311/360 untuk 2026/2030/2035/2040. Rate mobil 3,5%/tahun, motor umum 2,5% dan override northbound 4% adalah asumsi M07, bukan prakiraan resmi.

## Actual rehearsal A / B / C

| Rehearsal | Hasil | Durasi / batas |
|---|---|---|
| A eksekutif | PASS_ACTUAL_TIMED_UI_REHEARSAL | 300.44 s, sepuluh bagian, start/replay/overview/shutdown |
| B teknis | PASS_ACTUAL_TIMED_UI_REHEARSAL | 900.66 s, sepuluh bagian, tahun/skenario/adverse comparison |
| C gangguan | PASS | 52.49 s, service stop, refused reload, browser restart, offline deck/video, cache reverify dan recovery |

A/B adalah UI otomatis bertimed dengan screenshot tiap bagian, console/failed responses, loading dan frame pacing. Tidak ada klaim presenter manusia menjalankan naskah. Percobaan awal A terputus saat sesi berganti dan disimpan sebagai interrupted, bukan PASS. A/B penuh kemudian dijalankan ulang dalam helper tersembunyi. C memiliki log console/request failures yang menandai connection-refused saat shutdown sebagai gangguan disengaja. Video C merekam sesi aktual sebelum/sesudah restart; video utama cadangan tetap MP4 M10.

## Projector UX, offline, fallback dan recovery

Enam kombinasi native Chrome: 1920×1080 dan 1366×768 pada zoom 100/125/150%, fullscreen guided presentation, camera change dan split. Batas presenter/kanvas, horizontal overflow, comparison banner serta actual screenshots diperiksa. Ini viewport simulasi, bukan proyektor fisik. Semua aset/font sistem/gambar/video lokal, external request 0 pada uji yang memblokir akses luar.

Missing-index fault injection benar-benar mengembalikan 404 pada fetch browser terisolasi. Start tetap disabled, canvas tidak menampilkan run lain, pesan recovery jelas. Setelah fault dilepas, reload kembali ke rekaman valid. Deck HTML 15 slide dan MP4 tersedia saat host berhenti. Uji C menutup host test sungguhan, merestart browser/server dan memverifikasi ulang 23 recordings. Tidak ada output sumber yang dihapus untuk mensimulasikan kerusakan. Paket ZIP diekstrak ke lokasi uji yang diperiksa, cold-start dengan global Python, lalu actual Chrome membuka renderer, CSS M11, baseline 2026, kamera rel dan playback. Seluruh 23 recording lolos preflight dan host hasil ekstraksi berhenti bersih. Bukti qa/package-smoke.json, package-browser-smoke.json dan package-extracted-runtime.png.

## Regression dan performa

344 tes Python legacy lulus dalam 153.854 s. M10 core 31 assertions dan baseline 18 browser flows lulus terpisah. M11 menambah timed rehearsals, enam projector cases, fault/fallback dan pemeriksaan dokumen/numeric/source. Count ini tidak digabung menjadi jumlah Python test fiktif.

Frame pacing aktual A/B: [{"rehearsal": "A", "samples": 129, "mean_reported_fps": 114.73914747064227, "minimum_rolling_p5_fps": 59.52380952374765, "max_over_50ms_in_rolling_window": 0, "scope": "Overlapping browser windows, sampled every ~2 s during automated presentation. Authoring/other desktop work may be concurrent. Do not sum stalls or infer physical VRAM."}, {"rehearsal": "B", "samples": 428, "mean_reported_fps": 112.55452896446322, "minimum_rolling_p5_fps": 39.37007874012139, "max_over_50ms_in_rolling_window": 0, "scope": "Overlapping browser windows, sampled every ~2 s during automated presentation. Authoring/other desktop work may be concurrent. Do not sum stalls or infer physical VRAM."}]. Window saling tumpang tindih dan dapat mencakup transisi/loading serta aktivitas authoring lain. Jangan menjumlahkan stalls atau menafsirkan shared GPU memory sebagai kapasitas VRAM. Benchmark M10 tetap bukti historis terpisah, tidak ditulis ulang sebagai hasil M11.

## Issues found and fixed

- Canvas terlalu kecil pada 1366×768 zoom 150%: CSS adapter M11, rerun enam kasus PASS.
- Selector link entry offline tidak valid: ganti ke ID eksplisit, fallback QA rerun PASS.
- Wording recovery menampilkan path teknis: adapter pesan presenter, detail terpisah dari tampilan utama.
- Font API awal mengabaikan family: gunakan typeface Arial, verifikasi final 148 text-script uses. Chart memakai style font sendiri.
- Kesalahan konfigurasi finalizer/table policy/runtime modules/receipt path diperbaiki, lalu final artifact berhasil divalidasi. Tidak dianggap kegagalan simulator.
- Uji C awal memiliki syntax harness error, kemudian jalur auto-C mengalami race dengan halaman chrome-error setelah service mati. Harness dibetulkan dengan tab baru sesudah refused navigation. Uji C lengkap terpisah (console, failure, actual video, restart) lulus; log awal tetap dipertahankan.

## Remaining limitations dan M12

- Baseline 2026 belum terkalibrasi empiris. Semua angka lalu lintas yang dipakai berasal dari simulasi dengan demand/kontrol/pertumbuhan provisional.
- Bangunan, vegetasi, marka/furniture dan dimensi model belum menjadi geometri/armada hasil survei.
- Short/internal lanes, rail/stop-line alignment dan clearance tetap memiliki batas jaringan sumber. M11 tidak mengubah topologi atau mengesahkan legalitas.
- Native PowerPoint GUI dan proyektor fisik belum diperiksa. PPTX telah divalidasi struktur, diimpor ulang dan dirender melalui Artifact Tool; PDF memakai render final tersebut. Penerimaan presenter manusia dan ruangan rapat tetap terpisah.
- M08.5 tetap PARTIAL_BROWSER_ACCEPTANCE_PENDING. Lembar diskusi/form preview tidak mengesahkan workbench untuk survei produksi.
- Bila launcher memakai ulang layanan M10 lama tanpa adapter M11, halaman awal menjelaskan perlunya menutup layanan melalui aplikasi dan menjalankan launcher M11 kembali untuk layout ringkas pada layar kecil/zoom besar. Tidak ada layanan lain yang dihentikan diam-diam.
- Presenter sebaiknya memakai zoom 100%/125% di 1366×768 agar ruang 3D lebih luas. Zoom 150% telah diuji dengan adapter M11 dan seluruh kontrol tetap dapat diakses.
- Internet tidak diperlukan untuk demo. Python 3.12+ lokal tetap diperlukan untuk layanan 3D; deck HTML/PDF/video tersedia tanpa server.
- M12 tidak dimulai. Tidak ada klaim official forecast, solusi terbaik, efektivitas lapangan atau kesiapan konstruksi.

M11 siap sebagai paket teknis menurut 20 gate yang tercatat. Penerimaan lapangan/proyektor tetap pending secara terpisah. Kesiapan ini bukan izin otomatis memulai M12 atau klaim release produksi/efektivitas kebijakan.
