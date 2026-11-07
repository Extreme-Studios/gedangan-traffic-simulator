# Architecture · M01

## Aliran sistem

```text
Browser Chrome/Edge (127.0.0.1:5173)
  React UI + Three.js placeholder
       | same-origin /api proxy (Vite dev / preview)
Python HTTP foundation API (127.0.0.1:8765)
       | status + null metrics + project config (read only)
Domain boundaries
       | TraCI adapter (future; not connected)
Eclipse SUMO (future; owns simulation time/traffic state)
```

Vite merupakan build/dev server; frontend produksi hasil build statis di frontend/dist. M01 memakai HTTPServer standard library Python, bukan server deployment publik. Host hanya loopback, tidak memakai wildcard CORS. Tidak ada endpoint write atau start aktif; POST ditolak 409. Tidak ada API key atau data sensitif.

## Tanggung jawab modul Python

| Modul | Fondasi sekarang | Perluasan berikutnya |
|---|---|---|
| simulation_controller | deteksi executable/import, status foundation, blok start/step | lifecycle session TraCI, state machine, scheduler, seed |
| traffic_network | kumpulan nodes/edges/lanes/junctions, guard kelengkapan/verifikasi | SUMO net import, lane connectivity, spillback |
| vehicle_demand | struktur OD dan lookup pertumbuhan yang menolak nilai hilang | OD assignment, time profiles, sampling terkontrol |
| vehicle_behavior | enam kelas, parameter belum diisi | car following, lateral behavior, dimensi dan kalibrasi |
| railway_interaction | struktur crossing/events kosong | event palang, rel ganda, station dwell, konflik |
| scenario_manager | daftar skenario kosong; apply belum diimplementasi | baseline immutable, perubahan infrastruktur dan pembandingan |
| metrics_collector | snapshot null tanpa run | koleksi metrik dari SUMO dengan unit dan provenance |

Metode placeholder sengaja mengembalikan error, bukan hasil fiktif. Terpasangnya SUMO/TraCI tidak mengubah status menjadi connected: harus ada handshake session dan jaringan/demand yang tervalidasi pada implementasi mendatang.

## Kontrak data dan koordinat

configuration/schemas/dataset.schema.json berisi road_nodes, road_edges, lanes, junctions, railway_crossings, vehicle_classes, zones, od_matrix, traffic_demand, traffic_signals, infrastructure_scenarios, simulation_metrics, data_provenance, calibration_status, growth_rates. Setiap record ilmiah mempunyai category, provenance_id, calibration_status. Tahun dasar 2026 dikunci. Geometri dan parameter tidak diketahui menggunakan null.

Jaringan future menyimpan koordinat metrik dan CRS eksplisit; transformasi GIS → SUMO → Three.js harus tercatat dan dapat dibalik. M01 belum memilih EPSG, extent, origin, atau geometri jalan. Bentuk hexagon/ring/kubus canvas adalah konsep nongeografis tanpa satuan lapangan.

Validator memeriksa JSON Schema, kategori, keunikan ID, provenance, referensi topologi utama, relasi edge/lane timbal balik, dan kunci unik pertumbuhan. Validator bukan verifikasi survei, validator SUMO net, atau validator seluruh keterkaitan lintas dataset/run. Referensi skenario/run/kalibrasi lintas dataset memerlukan registry dan validator berikutnya; tidak ada dataset tersebut yang terisi pada M01.

## Batas frontend

Three.js menampilkan scene ringan dengan OrbitControls, grid toggle dan reset. Tidak membuat kendaraan bergerak, jaringan Gedangan atau angka dashboard. Navigasi Workspace, Data & validasi, Riset dan Roadmap tersedia. UI menampilkan status API secara terpisah dari status SUMO. Metrik “—” berarti belum ada hasil, bukan nol kendaraan. Kontrol simulasi dan engine skenario belum aktif.

Library grafik ditunda sampai M11; Recharts merupakan kandidat React, belum dipasang/diuji dan harus dievaluasi saat kontrak metrik tersedia. Ini menghindari paket dan grafik kosong yang tidak bermanfaat pada M01.

## Kinerja, aset dan offline

Pixel ratio maksimum 1.5; render loop dibatasi 30 fps; geometri sederhana, tanpa shadow maps atau tekstur eksternal. Dispose geometry/material/renderer dan ResizeObserver saat unmount. Ini batas desain, bukan benchmark perangkat 1080p. RAM fisik 16 GiB terdeteksi, tetapi yang terlihat OS sekitar 11.70 GiB; VRAM 6 GB belum diverifikasi.

Blender untuk authoring pada M10, ekspor glTF/GLB, instancing dan LOD. Hindari membundel data historis besar ke React; future transport snapshot terukur dan throttled dari engine, misalnya WebSocket. Tetapkan versi kontrak, unit, run_id, timestep dan sequence agar UI tidak mengubah waktu simulasi secara independen.

Saat dependensi terpasang, UI/API memakai localhost tanpa CDN, font web, tile map, analytics atau resource jarak jauh. Tautan literatur memerlukan internet. Pengujian M01 tidak mencakup pemutusan koneksi jaringan fisik.

## Reproducibility dan perluasan

package-lock.json mengunci dependency tree frontend; tests/requirements-lock.txt mengunci alat validasi Python. Run masa depan wajib membawa hash jaringan/demand, config version, scenario ID, seed, versi SUMO, interval pengukuran dan calibration status. Bandingkan skenario dengan common demand/seed serta warm-up dan horizon yang sama. M02–M12 belum diimplementasikan; pemisahan modul memungkinkan penggantian API/framework tanpa mengubah peran SUMO atau provenance.
