# Gedangan — Historical Data Coverage

Dibuat dari actual outputs, 1 November 2026. Status penelitian: **belum dikalibrasi terhadap observasi Gedangan 2026**.

## Hasil pencarian

Target 1 Agustus–31 Oktober 2026: **0 directional observations yang memenuhi syarat exact demand**. Kalender 92 hari ×96 interval15menit =8.832 time slots MISSING; bukan angka nol kendaraan. Count arah/turning/signal/rail events/travel time/queue/OD target tetap MISSING.

Database [historical.sqlite](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/data/realism_recovery/historical.sqlite>); schema [historical-schema.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/historical-schema.json>); coverage [target-coverage-view.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/target-coverage-view.json>); sumber unduhan dan SHA [source-register.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/source-register.json>).

36 record historis dipertahankan sebagai OBSERVED dalam lingkup sumber aslinya: Kusuma & Sholikhah, Table1 p927, survei 9/11/14 Mei2023, jam07/12/17, empat kelompok kendaraan. Lokasi Ahmad Yani terdampak konstruksi Aloha, arah UNSPECIFIED. Ini bukan hitungan simpang inti Gedangan 2026. Sumber [paper2024](https://ejournal.undip.ac.id/index.php/ilmulingkungan/article/download/56951/pdf).

Jumlah tiga jam pengamatan tidak diartikan sebagai volume per jam atau data sepanjang hari. Data15menit asli tidak tersedia. Tabel Juni dengan ketidaksesuaian hari/tanggal dikeluarkan. Sumber2022 berunit skr/jam tidak diubah menjadi kendaraan/jam; PDF-nya belum dapat diunduh. Data signal paper dengan waktu/unit tidak cukup pasti tidak dijadikan count2026.

## Kebijakan penyimpanan

Setiap evidence mempunyai date/daytype/start-end WIB/interval/road/direction/entry/exit/class/metric/value/unit/status/source-year/provenance. Status OBSERVED, REFERENCE_BASED_ESTIMATE, SYNTHETIC_SCENARIO, MISSING dibedakan. UPDATE/DELETE evidence ditolak SQLite; perubahan melalui record/version baru. Simulated results disimpan di experiments/run outputs, tidak dipromosikan menjadi observasi.

Estimasi hanya memakai jam referensi yang tersedia. Range ketidakpastian adalah sensitivity envelope, bukan confidence interval statistik. Pengisian coverage observasi membutuhkan sumber terverifikasi, count arah, entry/exit, review kualitas dan endpoint network; agregat tanpa arah tidak otomatis lolos.

