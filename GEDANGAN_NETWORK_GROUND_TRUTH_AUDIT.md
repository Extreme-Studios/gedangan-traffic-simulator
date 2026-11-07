# Gedangan — Network Ground Truth Audit

Dibuat dari actual outputs, 1 November 2026. Status penelitian: **belum dikalibrasi terhadap observasi Gedangan 2026**.

## Ruang lingkup dan metode

Parent immutable: `simulation/network/m051/provisional/network.net.xml`, SHA256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. 1961 external road edges dan 3248 internal edges diperiksa. OSM snapshot 31 Oktober 2026; directional/split SUMO edges tidak sama dengan jumlah original OSM segments.

Koordinat sumber WGS84 diproyeksikan UTM49S (EPSG32749), lalu diberi netOffset asli. Setiap shape edge SUMO dibandingkan dengan centerline way OSM asal, bukan dengan gambar layar. Maksimum jarak centerline sumber sekitar 3,731m; lane offset dan junction trimming turut memengaruhi angka ini. **Ini bukan akurasi survei lapangan.**

Overlay: [network-source-overlay.geojson](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/network-source-overlay.geojson>) dan [network-source-overlay.svg](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/network-source-overlay.svg>). Angka per edge: [source-geometry-comparison.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/source-geometry-comparison.json>). Audit/controller/class connectivity: [network-audit.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/network-audit.json>).

## Cakupan arah dan celah

- Koridor utama NB Sidoarjo→Surabaya dan SB sebaliknya menggunakan OD M04 dan existing explicit lane connections.
- Sukodono, Ketajen, frontage, local/feeder/service dan railway vicinity dipetakan melalui source metadata. Akses frontage tetap tersendiri.
- Nama Sedati/Jenggolo tidak ditemukan sebagai koridor eksplisit. Label Ketajen tidak diganti secara spekulatif; ini gap identitas/cakupan yang perlu pemeriksaan lapangan.
- Rute melalui area stasiun bukan bukti semua driveway stasiun tersambung. Road alternatives hanya yang ada dalam graph.
- Upstream/downstream tercakup sampai batas network; demand boundary eksternal dan pembentukan antrean di luar batas belum terukur.

## Topologi dan izin

Tidak ada perubahan geometri/topologi ground network untuk mengejar routing sukses. Pemeriksaan rute menggunakan explicit connections, lane/via permissions, M04 registry, M04.5 access/type/dimension/conditional screens. Conditional yang tidak dapat dievaluasi ditolak. Oversize ditolak. Izin provisional model tidak sama dengan izin legal lapangan yang telah disahkan.

S00 menggunakan salinan parent. S02/S03/S07 hanya membatasi gerakan/lane yang memang ada. S06 menambah struktur konsep yang diberi identitas tersendiri; bukan mengaku jalan tersebut sudah ada.

Hanya satu road controller Gedangan dimodelkan (27 phases: protected link pergerakan individual), ditambah rail crossing. Signal plan ini asumsi model lama, bukan timing lapangan terukur. S05 ditolak karena controller kedua belum tersedia.

