# Data Quality Report · M02

Kesetiaan sumber OSM diperiksa; status keseluruhan **Partially verified**, survei lapangan **Unverified**. Format valid bukan bukti keadaan operasional benar.

## Geometri dan CRS

- Storage: EPSG:4326, longitude/latitude; analysis: EPSG:32749, meter.
- Semua geometri master nonempty/valid dalam pengujian; tidak ada geometri jalan invalid atau duplikasi identik pada QA.
- Maksimum error roundtrip: 1.42e-14 derajat.
- Maksimum perbedaan relatif panjang UTM vs ellipsoid WGS84: 0.006098%. Ini validasi proyeksi, bukan validasi survei.

## Topologi

| Pemeriksaan | Hasil |
|---|---:|
| undirected_component_count | 29 |
| deadend_or_boundary_nodes_count | 380 |
| unconnected_geometric_intersection_count | 0 |
| shared_road_rail_crossings | 11 |
| unknown_oneway_segments | 1187 |

Komponen terbesar memuat 2219 dari 2448 node. Semua node utama dan frontage berada di komponen terbesar (tes), tetapi ini hanya konektivitas undirected. Komponen lain dapat berupa akses privat/ujung hasil pemilihan/putus OSM dan harus ditinjau, bukan disambung otomatis.

Pasangan dangling endpoint dalam 3 meter: 0. Nilai nol tidak membuktikan tidak ada celah di luar toleransi tersebut. Geometric crossings tanpa shared node diperiksa hanya pada line crossing setara layer dan tanpa bridge/tunnel; tidak mengesahkan semua junction atau grade separation.

## Atribut Missing

| Atribut | Segmen tanpa nilai | Status |
|---|---:|---|
| lanes | 1220 / 1417 | Missing / null |
| width_m | 1408 / 1417 | Missing / null |
| maxspeed_kmh | 1403 / 1417 | Missing / null |
| oneway | 1187 / 1417 | Missing / null |
| capacity_vehicles_per_hour | 1417 / 1417 | Missing / null |

Angka di atas adalah jumlah record, bukan angka lalu lintas. Tidak ada kapasitas yang diturunkan dari highway class atau default lajur. `lanes` yang tersedia adalah tag total OSM, bukan angka per arah yang telah disurvei. Arah tidak bertag tidak diasumsikan bidirectional.

## Titik dan konflik

11 titik OSM crossing berbagi node dengan sumber road dan rail. Dua titik rel di satu jalan dapat merupakan satu lokasi perlintasan fisik. Jumlah track fisik, closure, headway dan jadwal tetap null. 552 shared-node junction candidates, 81 akses/merge candidates dan 108 barrier nodes adalah fitur OSM/topologis, bukan daftar konflik terukur.

13 restriction relations dipertahankan, termasuk 5 no_u_turn serta satu conditional restriction. Tidak adanya tag bukan izin belok/U-turn. GeoJSON via-node disimpan untuk pemeriksaan; belum menjadi aturan routing SUMO. Station access mempunyai 9 proximity candidates dengan status Unverified dan tidak mempunyai entrance yang telah diverifikasi.

## Tindak lanjut

Periksa 29 komponen dan 380 terminal dengan sumber tambahan/survei; verifikasi one-way/legal turns, lane width, bottleneck, lokasi entrance stasiun, kondisi frontage/akses di lapangan, grade separation dan penamaan. Audit setiap modifikasi dengan source/version; jangan snap atau isi parameter default secara diam-diam. Uji kecukupan batas terhadap antrean pada tahap traffic engine/calibration.
