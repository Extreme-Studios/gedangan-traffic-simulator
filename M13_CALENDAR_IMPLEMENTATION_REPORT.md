# M13 — Calendar Implementation

## Aplikasi

[Buka kalender lokal](http://127.0.0.1:5197/). Launcher: [START_GEDANGAN_HISTORICAL_M13.bat](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/START_GEDANGAN_HISTORICAL_M13.bat>). Layanan M13 terpisah dari research runner5196 dan EXE M12. Tidak mengubah visual3D atau merilis EXE baru.

Backend: backend/gedangan/m13_database.py, m13_server.py. UI: frontend/m13/. Semua warna berasal dari API database aktual.92tanggal dihasilkan dari calendar arithmetic; daftar tanggal hijau/kuning/merah tidak dihardcode. Scope default adalah dua titik monitor koridor utama NB/SB yang memakai existing OD endpoints, sepuluh kelas M04, lima parameter. Bukan klaim seluruh1.961roadedges punya pengamatan. Ruas lain dapat diimpor bila ID ada pada katalog. Titik/arah target baru yang lolosverifikasi otomatis ditambahkan pada scope dan pilihanfilter; denominator baru tetap diperlihatkan.

Hijau=seluruh24jam untuk semua pasangan ruas/arah, kelas dan parameter scope terisi intervalobserved lengkap. Kuning=adaobservasi tetapi interval/dimensi lain kurang. Merah=tidakadaobservasi scope. Coverage menggunakan union interval percell agar overlap tidak membuat persentase melebihi100%. Filter mempersempit denominator secara eksplisit; label scope tetap ditampilkan. Count tidak dibagi rata ke jam lain. Seluruh jamMISSING disabled dan POSTselection ditolak backend. Tanggalmerah dapat diklik untuk inspeksi, tetapi tidak dipakai historicalsimulation.

Saat memilih tanggal, jam tidak dipindahkan ke tanggal lain. Jamparsial memperlihatkan missing/partial cells perruas/arah/kelas/parameter serta availableparameters dansourceIDs. Selection hanya memilih evidence; route/ODmapping dan kalibrasi untuk historical SUMO belum diklaim tersedia.

## API

GET /api/monthly?month=2026-08; /api/daily?date=2026-08-01; /api/hourly?date=2026-08-01&hour=7; /api/roads; /api/directions; /api/classes; /api/provenance; /api/source-audit; /api/staged; /api/template. Filters road_segment/direction/vehicle_class/parameter opsional dan ditampilkan dalam scope. POST/api/import, /api/review, /api/select. Import CSV/XLSX/JSON, maximum6MB/20.000rows. SQLite lama diaudit read-only; generic SQLite tidak dimerge tanpa mapping, ekspor ke supported schema diperlukan.

Source immutable+SHA archive, staged observations, quarantine perbaris, review append-only. File/source/type/status/unit/date/time/road/direction/class/interval/duplicate/overlap divalidasi. XLSX formulas dan numericExceldates tidak ditebak sebagai bukti; dates wajibISOtext. Blank→NULL, nilai0dipertahankan hanya dari sumber. Unknown/missing source classification ditolak; reference/simulation/synthetic tidak dapat diverifikasi sebagaiobserved. Reviewer/note/evidencecheck eksplisit wajib.

Cachemonthly memakai dataset_version; import/review mengubahversion, UI memeriksa setiap5detik dan membaca kalender ulang. Tidak harus restartserver. Existing dates/jam user tidak disubstitusi otomatis. Mode **REFERENCE-BASED TRAFFIC SCENARIO** terpisah, banner estimasi permanen, preview dari referensi2023 hanya07/12/17. Link actualSUMOrunner tersedia, tanpa submit atau mengganti tanggalnya otomatis.

## Acceptance

20 automated tests: production red/missing, isolatedfixture yellow/green, disabled selection backend, sourceclass exclusion, adjacentdate nonfallback, NULL/realzero distinction, cacheinvalidasi setelahimport/review via realHTTP, provenanceSHA, invalid/duplicate quarantine, immutability, explicitunits, intervalunion, reviewgate, class-conflict gate, XLSXvalue/formula guard dan penambahan otomatis titikmonitor baru. Log [acceptance-tests-final.log](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/m13/acceptance-tests-final.log>). **Yellow/green dibuktikan di database testsementara yang ditandai fixture, tidak pernah di databasehistoris aktif**. Kalender produksi sekarang seluruhnya merah karena data memang belum tersedia. Browser functional smoke test PASS:92tanggalmerah,24jamdisabled,tombolhistoricaldisabled,reference16MISSINGdan07estimasi. Bukti documentation/m13/browser-acceptance.json dan calendar-production-red.png. Green/yellow tetap diuji pada databasefixture, bukan direkayasa pada kalenderaktif.

