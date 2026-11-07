# Roadmap 12 Milestone

Hanya M01 dikerjakan. M02–M12 belum dimulai. Perubahan status tahap berikutnya memerlukan pekerjaan dan verifikasi tersendiri; M02 menunggu persetujuan pengguna.

| # | Milestone | Hasil dan gate rencana |
|---|---|---|
| 01 | Project Foundation & Research Architecture | struktur, audit, frontend/browser/Three.js, backend foundation, schema, dokumentasi dan pengujian |
| 02 | Gedangan Geographic Mapping | batas studi disetujui, sumber/izin/CRS jelas, geometri koridor utama–frontage–akses–stasiun–rel diverifikasi |
| 03 | Traffic Network Engine | executable SUMO/TraCI siap, net import dan koneksi lajur/simpang/kapasitas dapat diuji tanpa klaim kalibrasi |
| 04 | Vehicle System & OD Demand | enam kelas kendaraan, dimensi bersumber, zona dan OD per periode, konservasi demand dan rute |
| 05 | Traffic Behavior & Railway Integration | perilaku lateral/following, event palang/stasiun, interaksi simpang dan spillback teruji |
| 06 | Baseline Calibration 2026 | observasi 2026, parameter/ambang terdokumentasi, validasi independen, uncertainty dan hasil review |
| 07 | Traffic Growth Projection | growth per tahun/kelas/zona bersumber, populasi/demand dibedakan, sensitivitas dan horizon |
| 08 | Solution Scenario Engine | alternatif versioned, baseline immutable, parameter perubahan dan perbandingan konsisten |
| 09 | Interactive Simulation Control | start/pause/step/speed/reset tersinkron ke clock SUMO, bukan hanya animasi |
| 10 | 3D World Visualization | aset Blender/glTF, koordinat world benar, LOD/instancing dan target AMD/1080p |
| 11 | Analytics Dashboard & Presentation Mode | grafik antrean/waktu/kepadatan/kecepatan/kapasitas, before/after dan ekspor berlabel provenance |
| 12 | Optimization, Validation & Final Trial | benchmark perangkat target, offline trial, regression, validasi skenario, reproducibility dan batas penerapan |

Setiap milestone harus mempunyai laporan pengujian aktual, daftar keterbatasan dan acceptance yang dapat ditelusuri. Penelitian historis dan asumsi tidak boleh diam-diam menjadi baseline. Kebutuhan baru dapat memperinci kontrak tanpa menggabungkan otoritas visualisasi dan engine.
