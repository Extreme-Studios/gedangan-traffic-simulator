# M02 Architecture Addendum

Dokumen M01 dipertahankan sebagai rekaman historis. Checksum 66 file asli berada pada m01-original-sha256.json dan source snapshot ZIP tersedia. Entry M02: frontend/mapping.html, src/mapping/, vite.mapping.config.ts. Config/package/source M01 tidak dimodifikasi. Build M02 terpisah pada dist-m02.

## Data pipeline

```text
Overpass query → raw JSON snapshot + metadata/hash
             → node/way extraction, original coordinates retained
             → EPSG:32749 projection and network extent selection
             → source-node-only road segmentation + QA
             → GeoJSON EPSG:4326 / CSV / projected JSON bundle / SVG maps
             → local static frontend data → Three.js renderer + feature inspector
```

ProjectedMapBundle diberi label EPSG:32749 dan bukan GeoJSON WGS84. GeoJSON utama tetap EPSG:4326 tanpa custom CRS member, sesuai urutan longitude/latitude. Browser tidak melakukan proyeksi perkiraan skala latitude; ia memakai hasil pyproj dalam meter. Offset origin adalah koordinat UTM marker Stasiun Gedangan yang tersimpan; Three.js menggunakan x=easting−origin_x, z=−(northing−origin_y), y untuk ketinggian simbol. Offset tampilan ini mempunyai referensi geografis eksplisit dan dapat dibalik.

Perbedaan height simbol jalan/rel/titik mencegah tumpang tindih rendering, **bukan** elevasi survei. Tidak ada model terrain, bangunan atau lebar permukaan jalan. Kamera ortografis memulai north-up, OrbitControls menggunakan sumbu vertikal y dan kompas mengikuti proyeksi arah utara. Layer visibility tidak mengubah dataset; selection memakai raycast garis/titik dan label sumber. Highlight tetap menghormati visibility layer.

Render dilakukan pada perubahan kontrol, ukuran, layer atau seleksi, tanpa loop animasi kendaraan. Pixel ratio dibatasi 1.5. Ini pilihan efisiensi, bukan benchmark perangkat AMD atau jaminan FPS. Viewport browser internal 1920×1080 diuji, termasuk layout tanpa horizontal overflow; pengukuran performa fisik belum dilakukan.

## Scope dan status

Geodata adalah **research_reference** OSM, bukan observed_data survei. Batas riset adalah **assumptions** yang diturunkan dari anchor dan jaringan; pengamatan pengguna disimpan sebagai Unverified assumptions. Status data memakai Verified / Partially verified / Unverified / Missing beserta lingkup verifikasi. Verified terhadap raw OSM tidak berubah menjadi verified lapangan atau dokumen resmi.

Ketujuh klasifikasi fungsi jalan merupakan klasifikasi riset dari nama/konektivitas/tag OSM, bukan keputusan status legal jalan. Raw tags dan classification_basis dipertahankan. `lanes` adalah total tag OSM, tidak otomatis lajur per arah. `oneway` tidak bertag tetap unknown; tidak diasumsikan dua arah. Arah utara/selatan adalah orientasi ujung geometri berdasarkan oneway, bukan OD atau data arus.

Raw geometry tidak disnap, diinterpolasi untuk menutup celah, atau digambar ulang. Segmen dipilih pada pasangan node asli yang beririsan dengan polygon context; sebagian endpoint dapat sedikit melampaui outline. Batas polygon mempunyai margin kartografis, bukan batas antrean. Jalur shortest-path digunakan untuk pemilihan cakupan **undirected**, bukan routing kendaraan yang sah.

## Toolchain

SUMO portable 1.28.0 berada di proyek. Helper environment eksplisit memakai tools/traci dan tools/sumolib dari ZIP yang sama; M01 controller tidak diubah dan tidak tersambung ke mesin. SUMO smoke test sintetis berdiri sendiri. NETCONVERT belum mengimpor jaringan Gedangan dan tidak ada `.net.xml` Gedangan di simulation/networks.

M03 kelak perlu meninjau arah/legal turns, access dan restrictions, junction clustering, grade separation, topology repair berbasis bukti, konversi jaringan, boundary sensitivity dan laporan tersendiri. M02 tidak mengisi OD, behavior, volume, pertumbuhan atau skenario flyover.
