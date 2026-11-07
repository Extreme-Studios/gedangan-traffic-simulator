# MILESTONE 02 REPORT

**Gedangan Traffic Simulator — Real-World Geographic Mapping**  
Tanggal: **31 Oktober 2026**  
Status: **M02 selesai untuk pemetaan referensi geografis dan kesiapan toolchain.**  
Kualitas ilmiah dataset: **Partially verified**. Geometri diperiksa terhadap snapshot OSM; belum diverifikasi lapangan.  
**M03 belum dimulai. ENGINE NOT CONNECTED untuk model Gedangan.**

## 1. Ringkasan hasil

Data asli OpenStreetMap diperoleh melalui Overpass, disimpan bersama query, timestamp, object ID/version, lisensi dan SHA256. Dibuat core/context study area berdasarkan anchor serta konektivitas jalan. Jalan utama kedua arah, frontage, pengumpan, rel, stasiun dan titik perlintasan tersimpan sebagai fitur terpisah. Tidak ada geometri jalan tebakan, snapping atau penyambungan celah otomatis.

Three.js menampilkan geometri metrik hasil proyeksi, layer visibility, orbit/zoom/reset, pemilihan ruas, atribut, legenda, sumber dan QA. Browser internal Codex berhasil digunakan; Chrome tidak dipakai pada M02. SUMO portable resmi stabil 1.28.0 dipasang lokal proyek dan lulus smoke test sintetis. Tidak ada jaringan SUMO Gedangan atau simulasi kendaraan penelitian.

Semua pekerjaan utama berada dalam:

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

M01 dipertahankan: **66 file asli lulus pemeriksaan checksum tanpa perubahan**. Snapshot source dan manifest ada di `documentation/m02/`. Halaman/config/build M02 terpisah dari M01; dokumen M01 tetap merupakan rekaman historis keadaan saat M01, termasuk audit SUMO yang saat itu belum tersedia.

## 2. Akuisisi, sumber dan lisensi

- Sumber geometri: **© OpenStreetMap contributors**, [ODbL 1.0](https://www.openstreetmap.org/copyright), melalui `https://overpass-api.de/api/interpreter`.
- Discovery menemukan marker stasiun OSM **node 1359952188**, nama Gedangan, pada **112.7285913, -7.3889859** (longitude, latitude). Posisi ini adalah referensi OSM, bukan hasil survei.
- Snapshot jaringan: **2026-10-31T04:34:22Z**; diambil **2026-10-31T04:35:28.995466+00:00**. Raw berisi **52.013 elemen**, ukuran **12.314.919 byte**. Tidak seluruh raw menjadi area studi.
- Query dan raw tersimpan pada `geodata/sources/gedangan-network.overpassql` dan `geodata/raw/gedangan-network.json`; provenance/hash pada metadata JSON di sources. Pengunduhan menggunakan HTTPS, tanpa mematikan validasi sertifikat.
- [Berita resmi Pemkab Sidoarjo, 28 Oktober 2026](https://www.sidoarjokab.go.id/berita/detail/1793241723/0) diperiksa sebagai konteks proses pengadaan tanah flyover. Tidak digunakan untuk menggambar as-built atau membuat skenario.
- [Sumber resmi frontage Buduran, 15 Oktober 2026](https://www.sidoarjokab.go.id/berita/detail/1792113943/0) ditemukan, tetapi pembacaan penuh melalui web gagal karena batas ukuran respons. Tetap Unverified, tidak membuktikan seluruh frontage tersambung atau selesai.

Tidak ada geometri pemerintah, gambar berhak cipta, tile komersial atau Google Maps yang diambil. Tidak ada scraping Google Maps. Detail penggunaan sumber pada `geodata/sources/LICENSE_AND_ATTRIBUTION.md` dan `official-context.json`.

Observasi pengguna—frontage relatif lancar dan alternatif kapasitas arus utama menuju Surabaya belum memadai—disimpan pada `geodata/sources/user-observations.json` sebagai **Unverified assumptions**, bukan pengukuran observed_data.

## 3. Batas geografis dan alasannya

Envelope rectangular Overpass hanya area pengambilan untuk menelusuri jaringan. **Bukan batas penelitian.** Batas studi mengikuti backbone jaringan terpilih, kedua carriageway, frontage dan pengumpan/alternatif yang ditemukan. Anchor node dan jalur extent disimpan pada `geodata/sources/study-selection.json` serta `geodata/boundaries/network_anchor_paths.json`.

### Core Study Area

Mencakup sistem Simpang Gedangan, simpang frontage/Ketajen di sisi stasiun, marker Stasiun Gedangan, crossing, frontage dan pendekat utama hingga sistem simpang Nangka/Rajawali. Anchor utara memakai Muncul Industri/S. Parman–Ahmad Yani dan frontage/Pahlawan; barat memakai split Sukodono; timur memakai sambungan permukiman pertama setelah crossing stasiun.

Bounding box pembungkus polygon core (bukan polygon rectangular itu sendiri): **112.7262443, -7.3999968, 112.7302955, -7.3837458** (west, south, east, north).

### Context Study Area

| Pendekat | Anchor jaringan aktual | Jarak geometri jaringan dari node pusat |
|---|---|---:|
| Utara | S. Parman/Juanda, pendekat Aloha; dua carriageway | sekitar 1.439–1.449 m |
| Selatan | Jalan utama/Veteran–Lingkar Timur; dua carriageway | sekitar 2.550–2.560 m |
| Barat | Sukodono/Santren | sekitar 2.116 m |
| Barat daya | Santren/Nangka | sekitar 2.130 m |
| Timur | Ketajen/Rajawali | sekitar 2.255 m |

Angka tersebut merupakan panjang shortest path **undirected** dari node OSM pusat 2718664260 untuk pemilihan cakupan. Bukan jarak rute kendaraan yang diizinkan, panjang antrean, waktu tempuh, atau hasil simulasi.

Bounding box pembungkus polygon context: **112.7102330, -7.4135878, 112.7482805, -7.3758327**. Polygon mencakup koridor tambahan dan akses lateral, bukan radius dari stasiun.

Margin kartografis core **60 m** dan context **100 m** dipakai di sekitar backbone yang telah dipilih untuk memasukkan frontage paralel, rel dan akses dekat jaringan. Margin adalah **asumsi cakupan yang terdokumentasi**, bukan lebar jalan atau panjang antrean. Core tercakup di context, diperiksa dengan tes geometri.

Belum ada observasi antrean untuk membuktikan batas cukup. M03/M06 harus memperluas batas bila antrean mencapai terminal, rute alternatif terpotong atau distribusi arus sensitif terhadap batas. Tidak mengklaim cakupan ini sudah menangkap seluruh spillback nyata.

## 4. Inventaris jalan dan klasifikasi

| Fungsi riset | Segmen |
|---|---:|
| Main arterial road | 78 |
| Frontage road | 17 |
| Feeder road | 132 |
| Collector road | 79 |
| Local access road | 707 |
| Service road | 382 |
| Connector road | 22 |
| **Total** | **1.417** |

Segmen berasal dari **907 OSM ways**, dengan **53 nama jalan unik** plus ruas tanpa nama. Banyak segmen dapat berasal dari satu way; angka ini bukan jumlah jalan fisik. Pemotongan dilakukan hanya pada node OSM asli/shared junction atau batas rangkaian node terpilih. Segmen ujung bisa sedikit melampaui outline context karena tidak dibuat titik jalan baru pada potongan polygon.

Koridor utama memuat geometri terpisah arah utara dan selatan dengan tag oneway asli. Nama sumber antara lain **Jalan Jendral Ahmad Yani** dan **Jalan Letnan Jenderal S. Parman**, serta ruas ref 1 tanpa nama. Ejaan OSM dipertahankan. **Jalan Frontage Gedangan** mempunyai way ID tersendiri dan tidak digabung menjadi lajur jalan utama.

Pengumpan/alternatif yang teridentifikasi meliputi **Jalan Raya Sukodono, Jalan Raya Ketajen, Jalan Santren, Jalan Nangka, Jalan Rajawali**, dan sambungan lokal yang ada dalam sumber. Keterhubungan geometri tidak membuktikan semua ruas legal untuk semua jenis kendaraan.

Daftar lengkap: [inventaris nama dan source way IDs](m02/ROAD_INVENTORY.md), `geodata/processed/roads.csv`, `geodata/roads/all_roads.geojson`; file main_arterial/frontage/feeders/other dipisahkan. Klasifikasi fungsi adalah klasifikasi penelitian dari tag/nama/koneksi, **bukan verifikasi status hukum jalan**. `classification_basis` disimpan per fitur.

## 5. Persimpangan, akses, U-turn dan hambatan

- **552 shared-node junction candidates**, bukan 552 persimpangan fisik yang telah disurvei. Sistem utama direpresentasikan oleh node OSM pada pertemuan carriageway dengan Sukodono/Ketajen; simpang frontage/Ketajen memakai node **1720713565**.
- **81 network access/merge-diverge candidates**, **14 traffic-signal nodes**, **108 barrier nodes**. Posisi bersumber OSM; legal turns, pergerakan konflik, timing sinyal dan status hambatan belum diverifikasi lapangan.
- **13 restriction relations** disimpan: termasuk **5 no_u_turn** dan satu conditional restriction. Geometri via-node, JSON relation, dan subset U-turn ada di `geodata/access_points/`. Tidak adanya tag bukan izin U-turn atau belok.
- Perbedaan tag lajur pada node disimpan sebagai lane_transition_candidates. Dapat berasal dari jalan samping; **bukan bukti penyempitan**. Bottleneck fisik dan kapasitas masih kebutuhan survei.

Daftar simpang beserta koordinat pada `geodata/processed/junctions.csv` dan `geodata/junctions/road_junctions.geojson`. Akses/barrier/restriction terpisah pada `geodata/access_points/`.

## 6. Rel, stasiun dan perlintasan

- **13 bagian geometri rel** dari OSM, bukan 13 track fisik.
- **1 marker Stasiun Gedangan**; lokasi dan metadata OSM dipertahankan.
- **11 titik OSM level_crossing**, seluruhnya berbagi node dengan sumber jalan dan rel. Beberapa titik dapat mewakili rel berbeda pada satu lokasi perlintasan fisik; jangan mengartikan 11 titik sebagai 11 pintu/perlintasan independen.
- Crossing sistem Ketajen dekat stasiun antara lain **859708050** dan **11781097618**. Crossing di koridor lain tetap disimpan sesuai data asal.
- **9 proximity candidates** akses stasiun disimpan; **belum ada entrance yang verified**. Kedekatan terhadap marker stasiun tidak digunakan untuk mengklaim pintu masuk atau izin akses.
- Jumlah track fisik, jadwal, frekuensi, headway, durasi palang dan operasi stasiun **tidak diasumsikan**. Nilai belum tersedia tetap null.

Dataset dan tabel: `geodata/railways/rail_tracks.geojson`, `stations.geojson`, `level_crossings.geojson`, `geodata/processed/railways.csv`, `crossings.csv`, dan `access_points/station_access_candidates.json`.

## 7. CRS dan format

GeoJSON utama memakai **EPSG:4326** dengan urutan longitude,latitude. Analisis panjang/batas memakai **EPSG:32749**, easting/northing meter, melalui pyproj dengan `always_xy=True`.

Error roundtrip maksimum sekitar **1,42 × 10⁻¹⁴ derajat**. Perbedaan panjang proyeksi UTM terhadap panjang ellipsoid WGS84 maksimum sekitar **0,006098%**. Semua feature master berada dalam area penggunaan UTM 49S. Ini menguji konsistensi proyeksi; bukan mengukur ketelitian posisi OSM di lapangan.

Bundle browser bertipe `ProjectedMapBundle`, CRS EPSG:32749, dengan origin UTM marker stasiun yang tercatat. Offset Three.js bersifat tampilan dan mempunyai transformasi balik; bukan koordinat lokal tanpa referensi. Tinggi simbol render bukan elevasi fisik. Panjang dan ukuran simbol tidak dianggap data volume/kapasitas.

Format tersedia: **GeoJSON, CSV, metadata JSON, projected JSON, SVG**. GeoPackage tidak dibuat karena tidak dibutuhkan untuk cakupan ini.

## 8. Topologi dan kualitas

| Pemeriksaan | Hasil |
|---|---|
| Geometri master kosong/invalid | tidak ditemukan dalam tes |
| Geometri jalan duplikat identik | 0 |
| Komponen jaringan undirected | 29 |
| Node pada komponen terbesar | 2.219 dari 2.448 |
| Jalan utama dan frontage | semua nodenya berada pada komponen terbesar |
| Ujung/dead-end/boundary node | 380, dicatat untuk review |
| Dangling endpoints berjarak ≤3 m | 0 pasangan; bukan bukti tidak ada gap lain |
| Crossing geometris jalan tanpa shared node pada pemeriksaan setara layer | 0; pengecualian bridge/tunnel terdokumentasi |
| Crossing jalan–rel | 11 titik mempunyai shared node sumber |
| Arah tanpa tag oneway | 1.187 segmen, tetap unknown |

Komponen lain dapat berupa akses privat, dead-end, pemotongan cakupan atau kekurangan OSM. Tidak disambungkan otomatis. Graph undirected tidak mengesahkan routing legal kendaraan; unknown direction tidak dianggap dua arah.

Status: **Verified** hanya untuk kesetiaan geometri terhadap sumber/tes yang disebutkan; **Partially verified** untuk dataset keseluruhan; **Unverified** untuk survei/operasi fisik; **Missing** untuk atribut belum tersedia.

| Atribut Missing/null | Segmen |
|---|---:|
| lanes | 1.220 |
| width_m | 1.408 |
| maxspeed_kmh | 1.403 |
| oneway | 1.187 |
| capacity_vehicles_per_hour | 1.417 |

`lanes` yang tersedia adalah tag total OSM dan belum otomatis dibagi per arah. Nilai tidak diketahui tidak diganti angka default. Laporan lengkap: [DATA_QUALITY_REPORT.md](m02/DATA_QUALITY_REPORT.md), JSON/GeoJSON/CSV temuan di `geodata/quality_assurance/`.

## 9. Instalasi dan verifikasi SUMO

Audit awal M02 kembali tidak menemukan SUMO pada PATH/registry yang diperiksa, SUMO_HOME kosong, TraCI/sumolib tidak terdeteksi. Setelah itu distribusi stabil resmi **Windows x64 1.28.0** dari [halaman unduhan Eclipse SUMO](https://eclipse.dev/sumo/docs/Downloads.html) diunduh melalui tautan resminya:

`https://sumo.dlr.de/releases/1.28.0/sumo-win64-1.28.0.zip`

Lokasi portable: **toolchain/sumo-win64-1.28.0/**. Tidak menjalankan MSI, tidak membutuhkan administrator, tidak mengubah registry/PATH sistem, tidak menonaktifkan keamanan Windows, dan tidak memasang versi SUMO lain.

| Komponen | Pengujian aktual |
|---|---|
| sumo.exe | --version, exit 0, 1.28.0 |
| sumo-gui.exe | --version, exit 0, 1.28.0; interaksi GUI belum diuji |
| netedit.exe | --version, exit 0, 1.28.0; interaksi GUI belum diuji |
| netconvert.exe | --version exit 0; konversi jaringan sintetis exit 0 |
| SUMO tools | folder dan modul dalam archive tersedia |
| TraCI | import dari bundled tools, handshake SUMO 1.28.0 |
| sumolib | import bundled tools, membaca dua edge fixture sintetis |

Fixture **synthetic-not-gedangan** mempunyai tiga node, dua edge dan satu kendaraan software-test. TraCI menjalankan **12 langkah / 12 detik sintetis**, memeriksa vehicle ID, lalu menutup sesi. Ini smoke test software yang diizinkan pada M02, **bukan simulasi Gedangan atau data lalu lintas**. Tidak dibuat jaringan SUMO final/awal Gedangan.

SUMO_HOME dan sys.path diaktifkan hanya per proses melalui helper Python; `SUMO_ENV_M02.bat` menyediakan environment sesi proyek. Python interface berasal dari archive yang sama, tidak dipasang paket pip TraCI/sumolib beda versi. Smoke test menggunakan `.venv` proyek.

Archive berukuran **185.412.541 byte**, SHA256 lokal **822aa9c57a07a895200d536fd2b3fe8785e36baa9b97ecbe75688e08a636fb8e**, ZIP CRC lulus. **Tidak dibandingkan dengan checksum publisher independen**; tidak mengklaim verifikasi tanda tangan. Metadata pada `configuration/sumo-m02.json`; hasil aktual pada `documentation/m02/sumo-smoke.json`.

## 10. Versi dan dependency

Tool M01 dipertahankan: Python **3.12.10**, Node **24.22.1**, Vite **7.3.7**, React **19.3.1**, TypeScript **5.9.3**, Three.js **0.180.0**. Dependency geospasial dipasang hanya dalam `.venv`: **pyproj 3.8.0, Shapely 2.2.0**, beserta dependency transitif; lock lengkap baru pada `configuration/requirements-m02-lock.txt`. Lock M01 tidak diganti.

Tidak membuat EXE aplikasi, deployment atau instalasi admin. SUMO executable adalah toolchain resmi, bukan paket aplikasi final proyek.

## 11. Build, tes dan browser internal

- **TypeScript check PASS**, exit 0.
- **Production build M02 PASS**, exit 0, output terpisah `frontend/dist-m02`.
- **36/36 unit/integration tests PASS**: 18 foundation M01 dan 18 geodata M02. Termasuk checksum M01, raw SHA, koordinat sumber asli, ID unik, geometri, CRS, kedua arah utama, pemisahan frontage, unknown/null, crossing shared-node dan kesamaan data web.
- Schema/config/four-category dataset M01 tetap lulus regresi. Dataset traffic-data M01 tetap kosong.
- SUMO synthetic smoke PASS, terpisah dari dataset penelitian.
- IAB berhasil menampilkan localhost, data, geometri, rel, frontage, layer dan atribut; orbit/zoom/reset, pemilihan label dan **raycast langsung canvas** diuji. Panel sumber dan QA bekerja.
- Viewport virtual **1920×1080**, scrollWidth **1920**, canvas aktif dan status WebGL READY. Ini bukan benchmark perangkat fisik 1080p/AMD.
- Captured console setelah reload final tidak memuat warning/error baru. Tidak ada kegagalan rendering yang membutuhkan fallback Chrome.

Build JS sekitar **735,66 kB / gzip 199,64 kB**, CSS **9,01 kB / gzip 2,62 kB**, dengan warning chunk >500 kB. Data projected bundle sekitar 3,08 MB dimuat lokal. Warning ukuran tidak disembunyikan; kinerja beban besar belum diuji.

Temuan selama pengembangan: deprecation transform Shapely diperbaiki dengan API transform saat ini; warning duplicate createRoot saat HMR diperbaiki; up-axis kamera disesuaikan untuk orbit dan north-up reset. Tes/control dan reload akhir dilakukan sesudah perbaikan. Rincian batas QA pada [BROWSER_QA.md](m02/BROWSER_QA.md), log build/tes dan browser-final-state.json.

## 12. Peta dan screenshot

Peta mandiri yang dapat dibuka tanpa server: [Core SVG](../geodata/processed/gedangan-core-map.svg) dan [Context SVG](../geodata/processed/gedangan-context-map.svg). Peta memakai geometri sumber/proyeksi metrik, skala dan atribusi; lebar stroke bukan lebar jalan. GeoJSON master dapat diperiksa pada GIS atau melalui unduhan panel Sumber.

**Core area — screenshot browser internal:**

![Core area pada browser internal Codex](m02/browser-core-final.jpg)

**Context area — screenshot browser internal:**

![Context area pada browser internal Codex](m02/browser-context-final.jpg)

Screenshot tambahan mencatat layer frontage nonaktif, panel sumber, panel kualitas dan orbit/zoom. Seluruh screenshot asli berada di `documentation/m02/`.

## 13. Cara menjalankan

Jalankan **START_MAPPING.bat**, lalu buka **http://127.0.0.1:5174/mapping.html** di browser internal Codex. Launcher tidak membuka Chrome otomatis. Biarkan terminal launcher terbuka; **Ctrl+C** menghentikan preview. Periksa prasyarat dengan `START_MAPPING.bat --check` saat port kosong.

Peta tidak memerlukan backend atau SUMO aktif. M01 tetap dijalankan melalui START_DEV.bat. Build, akuisisi ulang, pemrosesan, smoke test dan environment dijelaskan pada **MILESTONE_02_README.md**. Aplikasi memakai data/aset lokal tanpa CDN atau tile service; tautan referensi eksternal memerlukan internet. Pemutusan jaringan fisik belum diuji.

Server QA telah dihentikan; port 5174 terbukti tertutup, lalu START_MAPPING.bat --check kembali PASS. PTY shell melaporkan exit 1 pada Ctrl+C yang diinjeksi, tetapi tidak ada proses preview yang ditinggalkan. Catatan shutdown ada pada `documentation/m02/launcher-shutdown.json`. Kedua SVG lulus parsing XML dan peta context juga diperiksa langsung melalui browser internal.

## 14. Acceptance criteria

| # | Kriteria | Status |
|---|---|---|
| 1 | Area Gedangan terpetakan | PASS sebagai referensi OSM, core/context berbasis jaringan |
| 2 | Utama dan frontage terpisah | PASS, source way/geometry berbeda |
| 3 | Jaringan pengumpan | PASS, dataset/klasifikasi/inventaris tersedia |
| 4 | Simpang dan kawasan stasiun | PASS, source nodes/marker/akses kandidat; entrance fisik belum verified |
| 5 | Rel dan perlintasan | PASS, geometri dan shared nodes; track count fisik/timing belum tersedia |
| 6 | Format data dapat digunakan | PASS, GeoJSON/CSV/metadata/JSON/SVG |
| 7 | CRS diperiksa | PASS, 4326/32749 dan uji proyeksi |
| 8 | Topologi/kualitas diperiksa | PASS, temuan 29 komponen/380 terminal dicatat tanpa repair tebakan |
| 9 | Sumber/lisensi | PASS, query/raw/hash/metadata/ODbL/atribusi tersimpan |
| 10 | SUMO terpasang/teruji atau kendala | PASS, portable 1.28.0 dan synthetic smoke; GUI hanya version check |
| 11 | Internal browser/fallback | PASS, IAB WebGL dan interaksi berhasil; Chrome tidak diperlukan |
| 12 | Tidak ada klaim belum terverifikasi | PASS, perbedaan OSM/document/field dan Missing/null dipertahankan |

PASS di sini menyatakan pekerjaan pemetaan/toolchain M02 terpenuhi. **Tidak menyatakan dataset seluruhnya verified lapangan atau siap dipakai sebagai model lalu lintas tervalidasi.**

## 15. Keterbatasan dan rekomendasi M03

Sebelum membangun traffic network, review one-way yang missing, restrictions/conditional turns, akses privat dan eligibility kendaraan, 29 komponen, terminal batas, grade separation, junction clustering, frontage entrances/exits, pintu stasiun, jumlah lajur/lebar serta titik penyempitan fisik. Setiap repair harus mempunyai bukti dan provenance, bukan snapping otomatis atau default kapasitas.

Periksa sumber resmi/as-built dan survei kondisi 2026 karena pekerjaan infrastruktur sekitar frontage/flyover masih mempunyai konteks perubahan. Kelengkapan snapshot OSM tidak membuktikan semua perubahan tersebut telah termuat. Tetapkan sensitivitas batas context sebelum memasukkan OD dan kalibrasi pada milestone berikutnya.

**Tidak ada OD final, behavior, kalibrasi volume, proyeksi pertumbuhan atau skenario flyover final yang dikerjakan. M03 menunggu persetujuan pengguna.**
