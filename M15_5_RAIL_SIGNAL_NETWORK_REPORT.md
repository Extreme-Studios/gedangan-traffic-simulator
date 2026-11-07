# M15.5 — Rail and Signal Network Report

2 November 2026, WIB. Staging M15.5 terpisah: http://127.0.0.1:5201/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.**

## Alignment dan crossing actual output

18 inherited rail edge dan crossing node `osm_859708050` dipertahankan. Actual road crossing via-links: `{':osm_859708050_2_0': 1, ':osm_859708050_0_0': 0}`. FCD baseline3000 memeriksa front kendaraan pada sample0.5s; 0 train front keluar garis lane di atas0.03m, 0 steady-red road first entry, 0 ambiguous phase-boundary entry. Ada 863 sampel road stopped saat state crossing tertutup. Ini sampel vehicle-time, bukan863 kendaraan berbeda.

Train-front crossing intervals: `{'m15_train_0': {'first_s': 596.0, 'last_s': 596.5}, 'm15_train_1': {'first_s': 1796.0, 'last_s': 1796.5}, 'm15_train_2': {'first_s': 2996.0, 'last_s': 2996.5}}`. Waktu ini actual sample, berbeda dari nominal assumed arrivals600/1800/3000s. Palang/controller dan sinyal pada playback membaca event rekaman SUMO, tidak memakai timer dekoratif.

## Arah dan clearance

Graph hanya mendukung N_TO_S. Referensi penelitian memberi konteks stasiun/track yang lebih rumit, tetapi tidak cukup untuk menciptakan reverse route dengan legalitas/clearance terverifikasi. Dua arah **UNAVAILABLE**, bukan dipalsukan. Nominal timetable, closing/opening/recovery parameter tetap editable dan ASSUMED.

Tidak tersedia footprint bangunan tersurvei atau swept-volume train/road clearance. Tidak mengklaim “tidak menabrak bangunan” hanya karena titik FCD berada di rail lane. Audit sampling front0.5s juga tidak memberi jaminan continuous-body clearance, signal interlocking fisik, stop-line atau posisi gate aktual. GEOSPATIAL PARTIAL.

## Sensitivitas yang dapat diulang

Pada same3000 road cohort, no-trains menghasilkan1916 departed,1342 arrived,574 active,1084 pending; baseline1914/1346/568/1086. Perubahan kecil dan mixed-sign tidak mendukung klaim kereta sebagai penyebab utama1086 pending. Green30 meningkatkan arrived dalam model, tetapi isolated protected-link program belum sesuai timing lapangan yang diverifikasi. Hasil tidak menjadi rekomendasi rekayasa APILL.

Data audit: `documentation/m155/rail-audits/cc419452a995456df324fd05.json`; raw `signals.json`, `fcd.xml` dan train schedule pada result. Tidak ada rail geometry edit, reverse connection buatan, atau kendaraan yang diizinkan menembus closure melalui override.

## Sumber dan batas interpretasi

[Peta Jalan Pemkab Sidoarjo](https://sidoarjokab.go.id/peta-jalan) dan [GeoJSON yang dipakai halaman tersebut](https://sidoarjokab.go.id/jalan) dipertahankan lokal beserta hash/tanggal/rights pada `documentation/m155/source-register.json`. Ada 23 fitur yang memotong extent studi. Ini referensi peta publik; bukan survei lane, median, rambu atau kapasitas 2026.

[Repositori penelitian PTDI-STTD 2024](https://digilib.ptdisttd.ac.id/8270/) memberi konteks simpang utama, simpang stasiun dan frontage. Proposal perubahan infrastruktur dalam penelitian tersebut tidak diubah menjadi kondisi eksisting.

[Penelitian UINSA 2023](https://digilib.uinsa.ac.id/63857/2/Nurul%20Aulia%20Fadilah_H95219051%20ok.pdf), PDF halaman indeks 66/69, memberi titik lokasi bernama Jenggolo. Teks PDF dibaca melalui web; download PDF lokal gagal TLS. Tidak ada klaim hash PDF lokal. Titik itu mendukung pemeriksaan alias spasial, bukan penggantian nama atau legalitas belok secara otomatis.

Snapshot OSM 31 Oktober 2026: `geodata/raw/gedangan-network.json`, hash `4bc46117ffae23aa90ade1e9c155601cfd90217cbca82c5bcc69fedbae0849f1`, atribusi OpenStreetMap contributors, ODbL-1.0. Kesamaan antarpeta tidak dianggap validasi lapangan independen.
