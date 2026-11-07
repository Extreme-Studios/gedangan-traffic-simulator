# M15.6.2 — Location Source Report

2 November 2026, WIB. Staging terpisah: http://127.0.0.1:5204/.

**REVIEW REQUIRED — menunggu pengguna memeriksa video aktual.**

MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION. PROVISIONAL NETWORK — NOT FIELD CALIBRATED.

## Sumber yang benar-benar diperoleh

[OSM API v0.6](https://wiki.openstreetmap.org/wiki/API_v0.6) berhasil mengembalikan map terbatas bbox 112.718,-7.402,112.736,-7.374. Raw XML 14,346,506 byte berada di `documentation/m1562/sources/gedangan.osm`, SHA256 `8333e6d13aba3916604b32de327d8396da35721ed3c06288e180b165cb658949`. Ditemukan 11124 building ways, termasuk Stasiun Gedangan way 472866576. OSM adalah sumber pemetaan publik, bukan survei independen kondisi bangunan 2026. Atribusi [OpenStreetMap contributors / ODbL 1.0](https://www.openstreetmap.org/copyright) ditampilkan pada peta sumber aplikasi.

Dataset lokal lama `geodata/raw/gedangan-network.json` berisi 52.013 elemen namun nol tag building. Ini menjelaskan mengapa ekstraksi jaringan lama tidak bisa menjadi inventaris bangunan. Tidak mengubah dataset lama atau mengartikan nol building sebagai tidak ada bangunan.

Karakter stasiun mengacu pada [foto Stasiun Gedangan 2020](https://commons.wikimedia.org/wiki/File:Stasiun_Gedangan_2020.jpg), Rizal Febri Ardiansyah, 12 September 2020, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Foto asli retained benar-benar diperiksa: dinding cream, band abu, shutter, teritis/bracket dan atap genteng rendah. Tidak ditempel menjadi aerial background. Bentuk detail model merupakan interpretasi, bukan hasil fotogrametri. Metadata foto Wikimedia 2022 diperoleh, tetapi download original mengembalikan HTTP403; tidak diterobos dan tidak mengklaim foto 2022 sudah dilihat.

## Alternatif yang diperiksa

[Geofabrik Java PBF](https://download.geofabrik.de/asia/indonesia/java.html) tersedia sekitar 857 MB; tidak diunduh karena source OSM bounded 14 MB sudah memenuhi kebutuhan footprint. [Overture](https://docs.overturemaps.org/getting-data/) mendukung ekstrak bbox; client resmi dipasang dan CLI diperiksa, tetapi data Overture tidak diekstrak atau dicampur seolah sudah diperiksa. [Informasi pemetaan Kecamatan Gedangan](https://gedangan.sidoarjokab.go.id/001/1784184566) ditemukan, tetapi berita workshop bukan dataset koordinat footprint yang bisa digunakan. Dataset bangunan pemerintah yang dapat dipakai pada pekerjaan ini tetap UNAVAILABLE. Tidak memakai citra satelit/street-view terlindungi atau bypass akses.

## Keyakinan dan tiga area prioritas

| Area | Anchor/sumber | Keyakinan posisi | Penampilan |
| --- | --- | --- | --- |
| Simpang utama | Frozen SUMO road/signal + footprint OSM sekitarnya | Source-mapped; registrasi UTM deterministik | Tinggi/fasad/atap/material asumsi |
| Stasiun/perlintasan | Way 472866576 + frozen rail/crossing + foto 2020 | Footprint sumber, tanpa pergeseran | PHOTO-REFERENCED APPEARANCE hanya karakter stasiun; ukuran detail asumsi |
| Koridor/frontage | Preset/lanes frozen + footprint OSM di area prioritas | Frontage tetap di koordinat asli | Tinggi/fasad dan material asumsi; close-up terpisah |

Source-confidence map menampilkan footprint sumber hijau, stasiun dengan referensi karakter foto emas, serta seluruh tinggi/fasad berlabel asumsi. Area di luar cakupan render tidak diisi bangunan rekaan. Semua URL, hash, kegagalan dan alasan alternatif ada di `source-attempts.json`.
