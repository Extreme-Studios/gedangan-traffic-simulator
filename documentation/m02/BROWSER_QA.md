# Internal Browser QA · M02

Tanggal 31 Oktober 2026. Browser utama adalah **Codex internal browser (IAB)**. Chrome tidak dibuka atau dipakai sebagai fallback pada M02. Peta disajikan Vite localhost pada http://127.0.0.1:5174/mapping.html.

| Pengujian | Hasil aktual |
|---|---|
| Localhost | Halaman M02 terbuka dengan judul yang benar |
| Data | Bundle dari data GeoJSON OSM dimuat; count layer tampil; raw/derived hashes diuji terpisah |
| WebGL | THREE.js canvas menampilkan WEBGL READY · EPSG:32749 |
| Jalan | Kedua carriageway utama dan frontage terlihat sebagai garis yang berbeda |
| Rel/stasiun/perlintasan | Rel kuning, marker stasiun, titik crossing dan label tampil |
| Core/context | Tombol mengubah framing kamera ke dua batas berbeda |
| Visibility | Frontage unchecked: garis/labelling dan highlight frontage hilang; checked: kembali |
| Junction layer | Checkbox persimpangan mengaktifkan marker shared-node candidates |
| Pemilihan map | Label Frontage Gedangan dan Ahmad Yani membuka atribut source way yang benar |
| Raycast langsung | Klik koordinat canvas pada viewport normal memilih osm-way:266287935:segment:6, Jalan Jendral Ahmad Yani, bukan hanya label/list |
| Orbit | Drag pada canvas mengubah orientasi geometri; kompas mengikuti utara |
| Zoom | Wheel/scroll di canvas mengubah skala geometri |
| Reset | Mengembalikan kamera dari orbit/zoom ke framing north-up |
| Sumber | Panel menampilkan snapshot, tanggal ambil, EPSG, ODbL dan observasi pengguna Unverified |
| Kualitas | Panel menampilkan 29 komponen, 380 ujung dan atribut Missing, tanpa mengklaim topology sempurna |
| JavaScript final | Tidak ada warning/error baru pada captured logs setelah reload final; lihat browser-final-state.json |
| 1080p | Viewport override 1920×1080 diuji; scrollWidth=1920, tidak ada overflow horizontal |

Screenshot core/context bersifat full-page (dapat lebih tinggi dari viewport karena footer), bukan rekonstruksi desain. Browser internal awal sempit; snapshot native yang hanya memperlihatkan panel sempit tidak berarti seluruh canvas gagal. Screenshot tab full-page dan DOM dimensions digunakan untuk pemeriksaan viewport 1080p. Override dikembalikan ke ukuran normal setelah QA.

Temuan pengembangan: HMR pernah memunculkan warning duplicate React createRoot. Entry M02 diperbaiki untuk mempertahankan root saat update. Pengujian kontrol juga menemukan orientasi up-vector kamera tidak sesuai OrbitControls; kamera diperbaiki menjadi y-up dengan reset north-up dan kompas dinamis. Setelah perbaikan, reload final, orbit dan zoom diuji kembali. Bukti akhir tidak mengklaim bahwa log historis sesi tidak pernah memuat warning.

Screenshot: browser-core-final.jpg, browser-context-final.jpg, browser-frontage-hidden.jpg, browser-source-panel.jpg, browser-quality-panel.jpg, browser-orbit-zoom.jpg. Sebagian screenshot antara menyimpan versi sebelum koreksi kamera; core/context **final** adalah rujukan visual akhir.

Tidak dilakukan benchmark GPU/FPS/VRAM/baterai, uji perangkat AMD fisik, simulasi kendaraan Gedangan, audit semua browser atau pemutusan internet fisik. Tidak ada kebutuhan fallback Chrome karena internal browser berhasil merender WebGL.
