# M15.6.2 — Building Footprint Report

2 November 2026, WIB. Staging terpisah: http://127.0.0.1:5204/.

**REVIEW REQUIRED — menunggu pengguna memeriksa video aktual.**

MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION. PROVISIONAL NETWORK — NOT FIELD CALIBRATED.

## Hasil

11124 closed building ways ditemukan dalam source map. Seleksi area simpang, stasiun, frontage dan strip koridor menghasilkan **953 footprint sumber yang dirender**, 219 dengan detail fasad. Ini penggantian 550 footprint rekaan, bukan penambahan ratusan bangunan fiksi. Sepuluh polygon landuse sumber memberi konteks permukaan; warna/materialnya tetap asumsi.

58 footprint ditahan karena overlap envelope jaringan model. Daftarnya tersimpan lengkap dalam `footprint-audit.json`; polygon sumber tetap di raw XML. Bangunan tidak dipindah, diperkecil atau diputar agar lolos. Tidak memperbaiki jalan dengan menggeser sumber. Tidak ada guessed infill. Relation/multipolygon kompleks tidak dirakit menjadi klaim bangunan lengkap; ruang lingkup ini closed ways dengan node lengkap dan polygon valid.

## Koordinat dan tinggi

WGS84 diproyeksikan ke EPSG:32749 (UTM49S), kemudian memakai netOffset frozen (-690790.39,-9182879.52). Konversi SUMO XY ke Three.js X/-Z tidak mengubah graph. `footprints-wgs84.geojson` memakai lon/lat; `footprints-local.geojson` adalah ekspor koordinat lokal untuk audit dan diberi label sistem koordinat lokal. Scene menyimpan setiap vertex sumber, version, timestamp, tag, dan OSM ID.

Tidak ditemukan height/building:levels pada building ways yang diperiksa. Semua tinggi adalah **ASSUMED 3D HEIGHT**: station 4m wall, bangunan kecil 3.4m, menengah 5.8m dan besar 7.2m, ditambah atap asumsi. Angka tersebut bukan konversi tag lantai atau pengukuran. Orientasi berasal dari oriented rectangle footprint, sedangkan body tetap memakai polygon penuh. Atap/fasad adalah interpretasi visual; atap persegi panjang dipakai hanya bila polygon mengisi >94% oriented rectangle, lainnya memakai roof polygon datar. Ini tidak memvalidasi bentuk atap aktual.

Stasiun source way 472866576 berluas sekitar **392.63 m²**. Body memakai footprint itu persis, tanpa offset buatan M15.6.1. Referensi foto tidak menyediakan height survey atau seluruh elevasi; fasad dan kedalaman teritis tetap approximation.

## Label wajib

- SOURCE-MAPPED FOOTPRINT: vertex OSM yang berhasil diperoleh dan diproyeksikan.
- PHOTO-REFERENCED APPEARANCE: karakter stasiun berdasarkan foto 2020; bukan seluruh gedung rekonstruksi presisi.
- ASSUMED 3D HEIGHT: seluruh tinggi bangunan.
- ASSUMED VISUAL CONTEXT: fasad selain karakter stasiun, roof form, warna, material, awning dan trim.
- UNAVAILABLE: height survey, facade inventory koridor, georeferenced imagery terbaru dan footprint pemerintah yang dapat dipakai.

Delapan tes integritas lulus, termasuk pemeriksaan setiap vertex render terhadap node OSM sumber. Network SHA256 tetap `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`.
