# M15.6.2 — Visual Improvement Report

2 November 2026, WIB. Staging terpisah: http://127.0.0.1:5204/.

**REVIEW REQUIRED — menunggu pengguna memeriksa video aktual.**

MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION. PROVISIONAL NETWORK — NOT FIELD CALIBRATED.

## Defect register sebelum implementasi

Delapan cacat berperingkat ditulis sebelum implementasi dalam `documentation/m1562/DEFECT_REGISTER.md` dan JSON terkait. Screenshot overview/rail M15.6.1, video aktual dan laporan M15.6/performance diperiksa. Prioritas: sumber footprint, nested playback memory, stasiun generik, terrain kosong, kamera frontage terlalu jauh, aset berulang, video canvas-only dan lifecycle switching.

## Perubahan yang terlihat

Footprint rekaan dihapus dari scene turunan dan diganti polygon OSM sumber di tiga area prioritas. Kontinuitas permukiman mengikuti lokasi polygon, bukan generator populasi acak. Tinggi, orientasi detail dan material tetap berlabel asumsi. Stasiun memakai footprint sumber dan karakter cream/grey, shutter, band, teritis/bracket, plinth dan sign GEDANGAN berdasarkan foto2020; belum merupakan rekonstruksi terukur.

Ground beige seragam diganti tone terrain lebih tenang, micrograin bersama dan10 polygon landuse sumber. Road-edge material transition selebar0.6m total di bawah permukaan asphalt adalah asumsi render saja, bukan sidewalk, drainase, shoulder legal atau road geometry tambahan. Roof/material dan trim dibatch; tidak menambah pohon dekoratif berlebihan, tiang/utilitas rekaan, nama usaha, stasiun gate atau infrastruktur rel baru. Existing crossing furniture, rail alignment dan recorded controller events dipertahankan.

Kamera station, junction close-up dan frontage close-up baru melengkapi preset lama. Frontage relationship tetap overview geografis berjarak; detail memakai kamera terpisah. Tidak memindahkan frontage atau memampatkan jarak. Matched before/after memakai kamera warisan junction/rail dan timestamp1796 pada baseline3000 yang sama. Peta keyakinan sumber interaktif menandai provenance footprint dan approximation.

Blender **tidak digunakan**. Geometri ini berupa polygon map, detail sederhana dan material berulang; batching procedural Three.js dipakai agar sumber/transform bisa diaudit. Tidak ada GLB/BLEND atau klaim pipeline Blender. Laporan Blender opsional tidak dibuat. Aset kendaraan warisan tetap mengikuti actual SUMO recording. Tidak ada flyover, fictional sensors atau V2I live claim.

## Batas visual

Geografi bangunan lebih berdasar dibanding M15.6.1, tetapi facade/roof dan material masih sederhana, belum photorealistic atau as-built. Tidak ada data street-level koridor terbaru yang terverifikasi. Ground dan station furnishing belum diverifikasi kondisi2026. Peta OSM bisa tidak lengkap/bergeser relatif jaringan model. Konflik render ditahan dan dicatat, bukan ditutup dengan bangunan fiksi. Status tetap REVIEW REQUIRED sampai pengguna menilai video.

Screenshot dan video aktual, beserta hash/metadata, tercantum dalam `review-package.json`. Video delivery memang merekam UI lengkap dan tur lima kamera secara aktual. Raw berdurasi49.933s memiliki pergantian ukuran awal; output mempertahankan seluruh rekaman lalu scale ke ukuran delivery1920×1080, sehingga5.685s awal masih berisi perubahan viewport dan bukan source native1920. Sesudah itu source native1920×1080. Tidak menambah still frame atau mensintesis gerakan. Ketajaman teks screen-capture lebih rendah daripada screenshot langsung; kualitas capture tetap perlu review. Video awal retained `first-screen-review.webm` memiliki framing stasiun terhalang; percobaan324×546 retained `failed-small-viewport-tour.webm`. Keduanya tidak dihapus atau dipromosikan menjadi proof final tour.
