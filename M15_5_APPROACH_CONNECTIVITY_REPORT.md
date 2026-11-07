# M15.5 — Approach Connectivity Report

2 November 2026, WIB. Staging M15.5 terpisah: http://127.0.0.1:5201/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.**

## Coverage

Inventaris mencakup **semua 1961 external road edge**, bukan hanya enam fixture. Field lengkap: road/source name, way/node ID, lon/lat, edge/lane ID, entry/exit node, kelas lane, arah koneksi, via, controller/link, dan downstream names. Lihat `documentation/m155/road-inventory.json`. Semua koneksi berasal dari actual XML, tidak dibuat dari jarak antargaris.

| Cohort input | Anchor | Gerakan model ditawarkan | Batas interpretasi |
| --- | --- | --- | --- |
| ketajen | w266287927_s0_p0_0_f | straight, left, right | MODEL ROUTE COHORT BOUNDARY, not a measured external traffic cordon |
| sukodono | w266287930_s0_p0_0_f | straight, left, right | MODEL ROUTE COHORT BOUNDARY, not a measured external traffic cordon |
| southbound | w512351908_s4_p0_0_f | straight, left | MODEL ROUTE COHORT BOUNDARY, not a measured external traffic cordon |
| northbound | w562358500_s16_p0_0_f | straight, left | MODEL ROUTE COHORT BOUNDARY, not a measured external traffic cordon |
| frontage | w1181141358_s0_p0_0_f | straight | MODEL ROUTE COHORT BOUNDARY, not a measured external traffic cordon |
| rail_crossing | w1240685448_s1_p1_0_f | straight | MODEL ROUTE COHORT BOUNDARY, not a measured external traffic cordon |

`approach-catalog.json` menyimpan prefix/suffix dan chain koneksi yang dipakai. `route-compatibility.json` menyimpan hasil per class/approach/turn beserta reason. Kelas yang memiliki lane permission belum otomatis lolos registry/access screen. Kedekatan akses stasiun tidak ditambahkan sebagai OD legal baru.

## Missing movements

1. **Anchor salah / split junction:** omission M14 telah diperbaiki M15 dengan traversal koneksi eksplisit lintas signal/priority node. M15.5 mempertahankannya dan mengaudit adjacency; bukan membuat belokan baru.
2. **Tidak ada koneksi model:** debugger menampilkan outgoing kosong/terminal. Ini membuktikan ketiadaan di model, tidak membuktikan larangan fisik. Terminal di boundary juga bukan otomatis bug.
3. **Koneksi source hilang ketika conversion:** belum ada kasus yang terbukti hanya dari referensi publik. Tidak ada repair yang direkayasa untuk menaikkan route success.
4. **Aturan belum diketahui:** label UNKNOWN / REQUIRES FIELD CHECK. Direct U-turn tertentu di graf tidak otomatis dipromosikan ke gerakan default; median/larangan aktual belum terverifikasi.

Nama koridor timur pada OSM adalah Ketajen. Titik penelitian 2023 bernama Jenggolo berjarak 6.03m dan 4.65m dari dua edge tersebut, sehingga menjadi kandidat alias provisional. Nama Sedati/Jenggala dan batas arus penting lain belum dipastikan. Perlu survei turning, boundary cordon dan rambu sebelum seluruh pendekat dapat disebut lengkap.

## Regresi demand dan izin

Manual 10 kategori @12 = 120 request; 76 routed/loaded/departed, 76 moved, 68 arrived, 8 active, 0 pending, 44 explicit route failures. Bicycle/nonmotorized dan kendaraan berat yang gagal screen dipertahankan sebagai kegagalan, tidak diganti passenger. Default runnable mix tidak dipromosikan menjadi komposisi Gedangan terukur.

Raw per vehicle: `simulation/runs/m155/be646fb03052c7a64f8cba8b/vehicle-results.json`; alasan kegagalan juga ada di XML audit. Shape/lane/connection immutable; frontend tidak boleh menambahkan koneksi agar input terlihat berhasil.

## Sumber dan batas interpretasi

[Peta Jalan Pemkab Sidoarjo](https://sidoarjokab.go.id/peta-jalan) dan [GeoJSON yang dipakai halaman tersebut](https://sidoarjokab.go.id/jalan) dipertahankan lokal beserta hash/tanggal/rights pada `documentation/m155/source-register.json`. Ada 23 fitur yang memotong extent studi. Ini referensi peta publik; bukan survei lane, median, rambu atau kapasitas 2026.

[Repositori penelitian PTDI-STTD 2024](https://digilib.ptdisttd.ac.id/8270/) memberi konteks simpang utama, simpang stasiun dan frontage. Proposal perubahan infrastruktur dalam penelitian tersebut tidak diubah menjadi kondisi eksisting.

[Penelitian UINSA 2023](https://digilib.uinsa.ac.id/63857/2/Nurul%20Aulia%20Fadilah_H95219051%20ok.pdf), PDF halaman indeks 66/69, memberi titik lokasi bernama Jenggolo. Teks PDF dibaca melalui web; download PDF lokal gagal TLS. Tidak ada klaim hash PDF lokal. Titik itu mendukung pemeriksaan alias spasial, bukan penggantian nama atau legalitas belok secara otomatis.

Snapshot OSM 31 Oktober 2026: `geodata/raw/gedangan-network.json`, hash `4bc46117ffae23aa90ade1e9c155601cfd90217cbca82c5bcc69fedbae0849f1`, atribusi OpenStreetMap contributors, ODbL-1.0. Kesamaan antarpeta tidak dianggap validasi lapangan independen.
