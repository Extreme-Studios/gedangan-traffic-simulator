# M15.5 — Network Reality Audit

2 November 2026, WIB. Staging M15.5 terpisah: http://127.0.0.1:5201/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.**

## Hasil

**GEOSPATIAL ACCEPTANCE: PARTIAL.** Tidak ada dasar yang cukup untuk memindahkan centerline atau membuat koneksi baru. Seluruh 1961 road edge mempunyai inventaris source ID, koordinat geografis, arah, entry/exit, kelas lane dan koneksi downstream. Belum ada edge yang mendapat sertifikasi fisik lapangan.

| Segmen / parameter | Status | Makna |
| --- | --- | --- |
| 1961 external road edges | VERIFIED FROM SOURCE | Source way/nodes/koordinat terhubung ke snapshot OSM; bukan 1961 ruas tersurvei |
| Lane count/width/speed/direction/control | PROVISIONAL; status parameter rinci tetap disimpan | VERIFIED/INFERRED/ASSUMPTION/MISSING diwarisi per parameter, tidak dihapus |
| Median opening, U-turn, station gate, clearance | UNKNOWN / REQUIRES FIELD CHECK | Kedekatan geometri tidak memberi izin legal |
| Kapasitas, OD, count dan timing resmi 2026 | MISSING | Demand contoh tidak dikalibrasi |
| Jenggolo vs label OSM Ketajen | PROVISIONAL alias | Near-match 6.03m / 4.65m; Sedati/Jenggala belum dipastikan |

## Pemeriksaan actual source

Audit membaca network XML `simulation/network/m051/provisional/network.net.xml`, raw OSM, M03 source-to-edge, lane geometry, connection/via/controller, serta run FCD/tripinfo/ledger. Laporan M15 tidak dipakai sebagai bukti PASS tunggal: hasil 3000 dihitung ulang dari staging baru dan diverifikasi terhadap XML dan playback.

Proyeksi node OSM ke SUMO: galat maksimum 0.01218m. Offset centerline terhadap sumber mempunyai median 1.59383m; ini konsistensi konversi sumber, bukan galat terhadap as-built. Renderer membaca koordinat lane yang sama (galat array geometry 0.0m). Sampling playback/FCD diperiksa terpisah.

Frontage anchor lama berjarak 1428.74m dari crossing. Frontage tidak dipindah ke simpang pusat. Ketajen dan railway-crossing adalah cohort yang berbagi ruang koridor, bukan dua count cordon independen. Nama Sedati/Jenggolo/Jenggala serta seluruh aliran boundary belum tervalidasi. Stasiun memakai OSM node 1359952188; road frontage terdekat 18.13m bukan bukti adanya gate kendaraan yang legal.

## Overlay yang dapat diperiksa

`documentation/m155/segment-status-overlay.geojson`: koordinat lon/lat, source status dan status aturan terpisah per segmen. `road-inventory.json`: tabel lengkap semua edge dan lane. `technical-map.json`: overlay interaktif termasuk sumber Pemkab dan selisih midpoint per edge. SVG/PNG EPSG:32749: `figures/georeferenced-extent`, `georeferenced-junction`, `georeferenced-station`. Offset lokal SUMO dikembalikan ke UTM pada plot. Overlay memperlihatkan perbedaan antarsumber; sumber Pemkab tidak diperlakukan sebagai centerline lajur terukur.

![Overlay simpang](documentation/m155/figures/georeferenced-junction.png)

## Sumber dan batas interpretasi

[Peta Jalan Pemkab Sidoarjo](https://sidoarjokab.go.id/peta-jalan) dan [GeoJSON yang dipakai halaman tersebut](https://sidoarjokab.go.id/jalan) dipertahankan lokal beserta hash/tanggal/rights pada `documentation/m155/source-register.json`. Ada 23 fitur yang memotong extent studi. Ini referensi peta publik; bukan survei lane, median, rambu atau kapasitas 2026.

[Repositori penelitian PTDI-STTD 2024](https://digilib.ptdisttd.ac.id/8270/) memberi konteks simpang utama, simpang stasiun dan frontage. Proposal perubahan infrastruktur dalam penelitian tersebut tidak diubah menjadi kondisi eksisting.

[Penelitian UINSA 2023](https://digilib.uinsa.ac.id/63857/2/Nurul%20Aulia%20Fadilah_H95219051%20ok.pdf), PDF halaman indeks 66/69, memberi titik lokasi bernama Jenggolo. Teks PDF dibaca melalui web; download PDF lokal gagal TLS. Tidak ada klaim hash PDF lokal. Titik itu mendukung pemeriksaan alias spasial, bukan penggantian nama atau legalitas belok secara otomatis.

Snapshot OSM 31 Oktober 2026: `geodata/raw/gedangan-network.json`, hash `4bc46117ffae23aa90ade1e9c155601cfd90217cbca82c5bcc69fedbae0849f1`, atribusi OpenStreetMap contributors, ODbL-1.0. Kesamaan antarpeta tidak dianggap validasi lapangan independen.
