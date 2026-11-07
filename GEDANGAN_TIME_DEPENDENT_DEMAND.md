# Gedangan — Time-dependent Demand

Dibuat dari actual outputs, 1 November 2026. Status penelitian: **belum dikalibrasi terhadap observasi Gedangan 2026**.

## Perilaku yang diimplementasikan

Date/time WIB, weekday/weekend aktual tanggal, year, vehicle types, seed, horizon dan warm-up masuk request serta signature run. Elapsed0 terpisah dari jam pengukuran. Hari libur tidak ditebak. Pergantian tanggal bukan bukti adanya observasi pada tanggal itu.

EXACT_OBSERVED mencari bukti sesuai tanggal/jam dan gagal tertutup jika arah/OD/review belum cukup. REFERENCE_ESTIMATE membutuhkan persetujuan eksplisit asumsi dan hanya mendukung07–08,12–13,17–18. Night atau contoh5Mei16:00 menghasilkan MISSING. Night dapat diuji lewat SYNTHETIC_SCENARIO dengan input OD/class/veh-per-hour eksplisit.

Weekday memakai mean sampel Selasa/Kamis; weekend sampel Minggu. Split NB default0,5 (rentang0,3–0,7), demand scale0,5–1,5, turning0–0,25. Turning diambil dari volume through, bukan ditambahkan. Truk agregat sumber hanya ditransfer menjadi light_truck dengan asumsi eksplisit. Tidak ada automatic annual growth atau pembagian subclass berat tanpa bukti.

Sub-hour flat profile dan stationary selected-hour warm-up adalah asumsi. Warm-up bukan keadaan awal terukur. Ledger menyimpan interval, sumber, status dan count; deterministic stratified departures dengan seed; cumulative rounding diuji untuk profile referensi flat. Batas12.000requests/run, horizon60–3600s dan warm-up0–1800s.

07:00 dan17:00 menghasilkan cohort berbeda; actual SUMO dijalankan terpisah. Cache hanya berlaku pada request/cohort/network/runner hashes identik dan output hashes valid. Tidak ada substitusi rekaman lain ketika data atau run hilang.

Demand/cohort tiap run ada di folder input/manifest terkait. Baseline07:00 [a26221f9ee8ea7be339ab9de](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/simulation/runs/realism_recovery/a26221f9ee8ea7be339ab9de>). Tabel hasil aktual: [GEDANGAN_PEAK_HOUR_SUMO_TEST.md](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/GEDANGAN_PEAK_HOUR_SUMO_TEST.md>).


Bukti lengkap: [acceptance-results.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/acceptance-results.json>), [supplemental-acceptance.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/supplemental-acceptance.json>), [api-acceptance.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/api-acceptance.json>).
