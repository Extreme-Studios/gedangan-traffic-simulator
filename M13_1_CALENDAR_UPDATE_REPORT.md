# M13.1 — Pembaruan Kalender Lintas Tahun

Tanggal audit: 2026-11-01T13:29:43.784786+00:00

[Buka kalender M13.1](http://127.0.0.1:5198/). Launcher: `START_GEDANGAN_HISTORICAL_M13_1.bat`. Layanan M13 lama tetap di port 5197 dan runner SUMO di 5196. EXE M12 tidak diperbarui.

Database aktif baru: `data\official\m13_1\historical_v2.sqlite`. Dibuat melalui SQLite backup read-only dari M13; hash asal ada di `documentation/m13_1/database-origin.json`. Derivative awal `historical.sqlite` tetap disimpan sebagai checkpoint. Database asli M13 tidak ditimpa.

Kalender kini menerima bulan/tahun 1900–2100. Daftar bulan observasi A/B terverifikasi berasal dari DB dan saat ini kosong. Bulan arsip B yang tertahan, November/Desember 2023, ditampilkan terpisah dan tidak mengaktifkan jam historis. Pemilihan bulan tidak mengganti tanggal/jam ke sumber lain.

Frontend `frontend/m13_1/` membaca API monthly/daily/hourly, `/api/archive` dan `/api/references`. Hijau tetap memerlukan interval lengkap untuk seluruh scope yang ditampilkan selama 24 jam; kuning berarti parsial; merah berarti tidak ada observasi yang memenuhi scope. Aggregate B/C dan metadata D tidak mengubah denominator atau mengisi count kosong.

Penyimpanan B/C bersifat append-only. Ada 49 kandidat B pada interval asli yang masuk quarantine dan 43 baris C SMP/jam. Verifikasi observasi baru memerlukan kualitas A/B yang tersimpan, source type pengamatan, tanggal/jam, satuan, lokasi dan kelas yang valid, serta review bukti eksplisit. Source legacy yang belum punya pemetaan A/B tidak dapat dipromosikan otomatis. C/D/E dan synthetic tests ditolak sebagai observasi historis.

Hasil acceptance: **PASS - 18 tests**, dengan pengujian HTTP nyata atas impor–review–refresh pada database fixture terisolasi, dukungan tahun 2022–2026, partial-hour, duplicate, unit, lokasi, pemisahan metadata dan preservasi. Data fixture tidak masuk DB aktif. Browser QA dicatat di `documentation/m13_1/browser-acceptance.json`; screenshot memakai data aktif dan tidak dibuat hijau untuk demonstrasi.

Historical SUMO run baru belum diklaim siap. Mode reference-based tetap estimasi. Tidak ada perubahan geometri atau visual 3D. Preservasi source M13 dan baseline SUMO terpilih: **PASS**.
