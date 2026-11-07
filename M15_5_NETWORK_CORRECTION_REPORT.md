# M15.5 — Network Correction Report

2 November 2026, WIB. Staging M15.5 terpisah: http://127.0.0.1:5201/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.**

## Keputusan koreksi

**Tidak ada koreksi geometri yang terverifikasi.** M15.5 menyediakan frozen execution copy berlabel `m155-existing-provisional-1`, bukan mengklaim sebuah network physically corrected. Byte salinan identik dengan baseline M05.1/M15; tidak menjalankan NETCONVERT untuk menyusun ulang geometri tanpa kebutuhan yang terbukti.

Original: `simulation/network/m051/provisional/network.net.xml`.
Copy eksekusi: `simulation/network/m155/provisional/network.net.xml`.
Kedua SHA256: `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`.

| Komponen XML | Original | M15.5 | Diff |
| --- | --- | --- | --- |
| edges | 5227 | 5227 | 0 |
| lanes | 5329 | 5329 | 0 |
| junctions | 1417 | 1417 | 0 |
| connections | 6159 | 6159 | 0 |
| rail_edges | 18 | 18 | 0 |

Connection/junction/railway diff kosong; route compatibility change akibat network = 0. Original tetap immutable. Tidak ada flyover, widening, median opening, reverse train track, bypass vClass atau forced insertion.

## Perubahan source code yang dilakukan

Semua penambahan dipisahkan dengan namespace M155. `m155_common` menjaga snapshot dan salinan frozen. `m155_reality` membuat inventaris dan overlay publik. `m155_network` mewarisi rute legal M15 tanpa mengubah graf. `m155_demand`/`m155_engine` memisahkan 60 menit pembentukan demand dari execution horizon, mencatat checkpoint 3600s, hash cohort, dan discharge censored. Ekspor playback gzip dioptimalkan tanpa mengubah traffic model. `m155_rootcause`, `m155_rail_audit`, `m155_evidence` dan `m155_edge_inspection` membaca bukti aktual. `m155_server` menyediakan API staging dan postprocess FCD; frontend `src/m155` menambah debugger, top-down dan penjelasan statistik. Renderer world M15 dipertahankan.

Network routing helper lama masih membaca baseline yang byte-identik. Karena itu validasi membandingkan hash kedua file sebelum menjalankan; apabila ada revisi geometri berikutnya, helper harus diisolasi ke graph baru sebelum dapat disebut corrected network.

## Reproduksi

Dari root proyek: `.venv/Scripts/python.exe -m backend.gedangan.m155_experiments bench`, kemudian `controls` dan `manual`. Run beridentitas input/source/toolchain disimpan pada `simulation/runs/m155/`; bila identitas sama, hasil tersimpan digunakan kembali. Untuk rerun baru gunakan nama eksperimen baru, tanpa menghapus run lama. Jalankan `m155_rootcause`, `m155_evidence`, `m155_edge_inspection`, `m155_rail_audit`, `m155_figures` untuk bukti turunan. `network-version.json`, `network-topology-diff.json`, source snapshots dan input/output manifests menyimpan provenance.

## Batas

Menggeser jalan mengikuti satu peta publik yang lebih kasar tidak dibenarkan. Kesalahan nyata berupa gate, jumlah track, median, lebar efektif, lane assignment, atau turn restriction masih membutuhkan bukti. Semua tetap PROVISIONAL/UNKNOWN. Tidak ada klaim improvement before/after geometry karena tidak ada perubahan fisik yang didukung.
