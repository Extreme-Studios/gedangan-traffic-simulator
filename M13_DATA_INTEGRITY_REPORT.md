# M13 — Data Integrity

## Status

Database SQLite integrity_check: **ok**; foreign_key_check errors: **0**. Preservation: **PASS**, 385 preexisting source/output files dibandingSHA, changed=0. 23 recovery source files dibanding snapshot, changed=0. FinalreleaseM12unchanged=True; SHA256 `5a0b36c4f8a20ec86a3bcb8d5b906ff0b3814cfa3465f376fc7df7cc8e76d520`. Evidence [integrity-verification.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/m13/integrity-verification.json>).

## Pemisahan data

DB baru: [historical.sqlite](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/data/historical/m13/historical.sqlite>). Database penelitian M06/M08.5/recovery lama dibaca read-only, bukan dimigrasi di tempat.36record2023 dibawa beserta tanggal/arah/provenance asli ke namespaceM13, di luar target dan belum lolosscope-review. Dataset2026 aktif mempunyai **0 verified records**; syntheticfixture target aktif **0**. Test menghasilkan data hanya pada TemporaryDirectorydatabase yang jelas test_fixture=true; tidak digabungkan atau diimpor keDBproduksi. Warna kalenderproduksi bukan demonstrasi keberhasilanfixture.

Schema: [schema.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/m13/schema.json>). observation_date/time, timezone, interval, location/direction/class, metricsnullable, units, statuses dan provenance disimpan pada observations. Source_name/location/url/method/type/SHA pada tabel sources yang direlasikan melalui FK dan diekspos observation_records view. Initial verification_status immutable; current_verification_status memakai latestappend-onlyreview. Tidak ada angka default atau randomfill. SourceURLyangtidakada tetapNULL; OBSERVED_SECONDARYbaru mensyaratkan URLpublikasiasli.

UPDATE/DELETE pada source/batch/observation/quarantine/review ditolak trigger. Rejection/review baru dicatat sebagai event; originalrecord tidak ditimpa. Ini perlindungan integritas aplikasi, bukan sistem identitas/otorisasi multiuser atau sertifikatkeaslian pengamatan. Review tetap tanggungjawab pemeriksa bukti.

## Cakupan dan batas

0tanggal punyaobservasi; 92tanggal kosong. 0jam lengkap, 0parsial, 2208kosong. Hasilcoverage [M13_HISTORICAL_COVERAGE.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/M13_HISTORICAL_COVERAGE.json>); missingtime ledger [M13_MISSING_DATES_AND_HOURS.csv](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/M13_MISSING_DATES_AND_HOURS.csv>). Angka2208menyatakan jumlahslotjam, bukan jumlahkendaraan. Records kosong tidak menjadi0vehiclecount.

Tidak ada kalibrasi, inferensi pola2026, pengubahantraffic simulation hasil lama, penghapusanworkspace atau uploadGitHub. Milestoneberikutnya belum dimulai. Sourcepipeline dapat menerima bukti baru tetapi data target masih perlu diperoleh dan direview.

