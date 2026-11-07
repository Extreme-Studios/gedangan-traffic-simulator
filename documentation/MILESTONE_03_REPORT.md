# MILESTONE 03 — Gedangan Traffic Network Engine

Tanggal pemeriksaan: **31 Oktober 2026**. Folder proyek: `C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`.

## Ringkasan dan status

Implementasi M03 selesai untuk konversi, inspeksi dan pengujian topologi. Dua jaringan SUMO dibangun dari dataset lokal M02, dapat dibuka di SUMO-GUI/NETEDIT, dan ditampilkan di browser internal Codex. **Kedua arah koridor utama berhasil dirutekan pada kedua varian.**

Status keseluruhan: **selesai dengan batas validasi yang eksplisit**. Konektivitas feeder, akses frontage dan simpang stasiun belum lulus sebagai jaringan strict yang lengkap. Keberhasilan provisional bergantung pada asumsi arah dan koneksi; legalitas belok, penggunaan lajur, kontrol simpang dan kapasitas belum tervalidasi lapangan. Tidak ada simulasi kemacetan atau pekerjaan M04.

## Sumber, environment dan pipeline

Laporan M01/M02, README, arsitektur, tata kelola data, laporan kualitas, inventaris jalan dan implementasi aktual diperiksa sebelum konversi. Sumber utama adalah raw OSM `geodata/raw/gedangan-network.json` beserta `all_roads`, `main_arterial`, `frontage`, `feeders`, junctions, crossing, access points dan turn restrictions M02. Snapshot sumber: **2026-10-31T04:34:22Z**, 52.013 elemen raw. Dataset jalan M02 memiliki 1.417 fitur dari 907 way sumber. Tidak ada pengunduhan ulang atau perubahan dataset mentah.

SUMO, SUMO-GUI, NETEDIT, NETCONVERT dan DUAROUTER diperiksa pada **1.28.0**, semuanya dari `toolchain/sumo-win64-1.28.0/`. Helper M02 dan SUMO_HOME digunakan kembali; TraCI/sumolib berasal dari tools portable yang sama. Tidak ada instalasi SUMO kedua. Log versi tersimpan di `m03/*-version.json`.

Pipeline `configuration/network-m03/build_network.py`:

1. Membaca data lokal, menghitung hash sumber dan menerapkan policy terpisah per varian.
2. Mempertahankan OSM way/node ID, urutan node asli dan feature ID M02. Pemotongan memakai node sumber yang sudah ada, termasuk junction, barrier, crossing dan restriction via-node. Tidak ada snapping atau sambungan berdasarkan kedekatan visual.
3. Memproyeksikan ke EPSG:32749 dengan origin node Stasiun Gedangan OSM 1359952188. `<location>` SUMO menyimpan projection dan offset; koordinat output SUMO dibulatkan hingga sentimeter. Geometri lane/junction adalah hasil engine, bukan hasil survei lajur.
4. Menulis `.nod.xml`, `.edg.xml`, `.con.xml` dan `.netccfg`, lalu menjalankan NETCONVERT dengan lalu lintas kiri, tanpa junction join atau geometry removal.
5. Memeriksa koneksi yang benar-benar dihasilkan NETCONVERT. Koneksi tambahan di luar whitelist dihapus melalui **konversi kedua dengan connection delete XML**. File `.net.xml` tidak diedit manual. Sebanyak 66 koneksi lajur strict dan 51 provisional ditahan; koneksi tak disetujui yang tersisa: **0**.
6. Menguji load SUMO tanpa demand pada waktu 0, menjalankan fixture DUAROUTER tanpa repair rute, mengekspor geometri/parameter aktual final XML untuk viewer, lalu menghasilkan audit dan manifest.

ID edge berbentuk `w{way}_s{segmenM02}_p{piece}_{loop}_{f/r}`. Pemetaan menyimpan way, feature, node sumber, urutan geometri, status dan alasan parameter. CSV lintas varian berada di `simulation/network/m03/source-to-edge.csv`.

## Struktur dan jumlah jaringan

Angka edge/lane berikut mencakup jalan eksternal. Internal connector SUMO dihitung terpisah.

| Ukuran | Strict | Provisional |
|---|---:|---:|
| Nodes | 225 | 1.022 |
| Directed road edges | 241 | 1.961 |
| Lanes | 323 | 2.043 |
| Lane-to-lane connections | 242 | 2.874 |
| Internal edges SUMO | 163 | 3.231 |
| Weak node components | 15 | 23 |
| Node pada komponen terbesar | 162 | 963 |
| Weak components graf pergerakan edge aktual | 78 | 67 |
| Strong components graf pergerakan edge aktual | 241 | 1.030 |
| Dead-end junctions | 71 | 347 |
| Edge tanpa incoming connection | 78 | 358 |
| Edge tanpa outgoing connection | 78 | 357 |
| Fitur M02 included / excluded | 215 / 1.202 | 1.055 / 362 |

Weak node components hanya mengukur sambungan geometri node, bukan keterjangkauan kendaraan. Graf pergerakan memakai koneksi lajur yang benar-benar terbit. Jumlah strong components strict yang besar juga mencerminkan koridor berarah tanpa U-turn, sehingga tidak boleh dianggap seluruh edge rusak.

**29 komponen M02 tidak disambungkan.** Setiap komponen hasil hanya memiliki lineage ke satu komponen M02; komponen yang tidak terwakili dicatat bersama ukuran aslinya pada `connectivity.json`. Perbedaan 15/23 dengan 29 disebabkan subset/filter arah dan akses, bukan perbaikan konektivitas. Boundary mengikuti pasangan node sumber, termasuk bagian kecil di luar batas seleksi awal.

| Fungsi jalan — directed edges | Strict | Provisional |
|---|---:|---:|
| Main arterial | 83 | 83 |
| Frontage | 17 | 17 |
| Feeder | 53 | 229 |
| Collector | 19 | 155 |
| Local access | 43 | 1.077 |
| Service | 22 | 396 |
| Connector | 4 | 4 |

Main arterial dan frontage mempertahankan geometri serta identitas way terpisah. Tidak ada merge ke jalan utama hanya karena sejajar. Cabang Sukodono, Ketajen, Santren, Nangka, Rajawali dan jalan lain mengikuti fitur yang tersedia dalam M02; keberadaan fitur bukan jaminan semua cabang bisa dirutekan strict. Access/merge frontage hanya berasal dari node bersama yang lolos policy, dengan batas interpretasi yang dicatat.

Rel tetap berupa **13 bagian geometri dan 11 titik crossing sumber**, bukan 11 lokasi fisik yang sudah diverifikasi. Disimpan sebagai overlay georeferensi `.add.xml`; tidak ada rail edge untuk operasi kereta, jadwal atau durasi penutupan palang.

## Arah, parameter dan missing data

`VERIFIED` berarti didukung tag/geometri sumber OSM/M02. Ini tidak berarti survei lapangan. `INFERRED` berarti interpretasi terdokumentasi. `ASSUMPTION` berarti parameter sementara engine. `MISSING` tetap tidak diisi sebagai fakta.

Strict mempertahankan `oneway=yes/-1/no` eksplisit. Aturan implisit roundabout/motorway tersedia dalam policy, tetapi hasil strict saat ini seluruhnya memiliki arah berstatus VERIFIED. Arah yang belum diketahui dikecualikan. Kontinuitas antar-way strict hanya diterima pada node sumber yang sama dengan kesamaan nama/kontinuitas arterial dan defleksi maksimum 45 derajat; belokan lintas-way lain ditahan.

Provisional mengizinkan arah dua arah sementara hanya pada kelas `secondary`, `tertiary`, `unclassified`, `residential`, `living_street`, `service`, `road`, dengan guard conditional/subtag. **Tidak semua ruas tanpa oneway otomatis menjadi dua arah.** Tambahan 1.720 directed edges berstatus arah ASSUMPTION.

| Parameter/status edge | Strict | Provisional |
|---|---|---|
| Direction | VERIFIED 241 | VERIFIED 241; ASSUMPTION 1.720 |
| Lanes | VERIFIED 97; ASSUMPTION 144 | VERIFIED 97; ASSUMPTION 1.864 |
| Speed | VERIFIED 14; ASSUMPTION 227 | VERIFIED 14; ASSUMPTION 1.947 |
| Lane width | ASSUMPTION 241 | INFERRED 14; ASSUMPTION 1.947 |
| Capacity | MISSING 241 | MISSING 1.961 |

Kekurangan sumber M02 tetap berlaku: 1.220 fitur tanpa lanes, 1.408 tanpa width, 1.403 tanpa maxspeed, 1.187 tanpa oneway dan seluruhnya tanpa kapasitas terukur. Angka di atas dihitung per edge hasil konversi, sehingga berbeda dari jumlah fitur sumber.

Asumsi engine: satu lajur per arah bila tidak diketahui; pembagian total lajur dua arah merupakan asumsi; speed sementara sekitar 30 km/jam; width 3,2 m/lajur jika tidak diketahui; prioritas 1; radius junction 0,1 m; node priority tanpa program sinyal. Nilai speed/width pada viewer mengikuti angka final XML yang telah dibulatkan SUMO; nilai input presisi tetap disimpan. Width yang dihitung dari lebar sumber/jumlah lajur diberi INFERRED. Tidak ada typemap bawaan yang diterapkan diam-diam. Kapasitas tetap null.

## Junction, restrictions dan kualitas konektivitas

Actual emitted connections diuji terhadap whitelist, indeks lajur, node bersama, arah dan pasangan yang diblokir. Duplikasi ID dan referensi node diperiksa. U-turn/reverse movement dan defleksi lebih dari 165 derajat ditahan. Barrier sumber dikarantina secara konservatif, kecuali cattle_grid. Akses privat/no dan kelas destination/customers/delivery/permit serta pembatasan kendaraan terkait dikecualikan untuk fixture passenger ini.

Via-node restrictions memblokir pasangan from/to sumber. **Via-way restrictions dikarantina pada masuknya from-way ke via-way**, sehingga dapat memblokir pergerakan lain yang sebenarnya sah. Conditional restrictions diterapkan sepanjang waktu secara konservatif. Ini belum merupakan model legal restriction dinamis yang lengkap. Relation ID dan alasan semua blocked movements tersimpan dalam `connection-provenance.json`.

Bridge/tunnel tags dipertahankan: 15 edge bertag bridge pada setiap varian; tidak ada tunnel=yes yang terwakili. Jalan yang berpotongan secara geometri tanpa node sumber bersama tidak digabung. Tidak ada model elevasi hasil survei atau jaminan bahwa topologi OSM sendiri sempurna.

Warning unresolved: radius/angle tajam, connector belok kiri yang saling berpotongan pada konstruksi awal provisional, serta lajur tanpa incoming/outgoing akibat boundary, barrier atau penahanan belokan. Log awal/final berisi 5/13 baris warning strict dan 16/26 provisional. Angka ini termasuk ringkasan pesan berulang, bukan jumlah cacat fisik unik. Geometri tidak diluruskan dan komponen tidak disambung untuk menghilangkan warning.

## Hasil DUAROUTER

Fixture terpisah dijalankan dengan seed 42 dan repair=false. Rute mengikuti koneksi aktual final network. Endpoints, arah, urutan lengkap edge, status, return code dan alasan tersedia di [route-test-results.json](m03/route-test-results.json) serta folder route-tests masing-masing varian.

| Fixture | Strict | Provisional |
|---|---|---|
| Sidoarjo → Surabaya | FOUND, 56 edges | FOUND, 56 edges |
| Surabaya → Sidoarjo | FOUND, 27 edges | FOUND, 27 edges |
| Feeder → main | NOT_FOUND | FOUND, 50 edges |
| Main → feeder | NOT_FOUND | FOUND, 53 edges |
| Frontage continuity | FOUND, 17 edges | FOUND, 17 edges |
| Frontage exit → akses timur | NOT_FOUND | FOUND, 68 edges |
| Simpang Gedangan | FOUND, 7 edges | FOUND, 7 edges |
| Simpang sekitar stasiun → Ketajen | NOT_FOUND | FOUND, 62 edges |

Strict feeder/main gagal karena koneksi belok konservatif ditahan. Strict frontage exit/stasiun memiliki endpoint timur pada way 266287937 yang dikecualikan karena arah belum didukung; DUAROUTER **tidak dijalankan** untuk dua fixture tanpa endpoint tersebut. File fixture kosong dan log executed=false mencatat kondisi ini; tidak ada rute palsu atau hasil lama yang dipakai. Target stasiun diperbaiki selama QA agar menguji keluar menuju Ketajen, bukan hanya sirkulasi pendek dalam pocket akses.

Label keberhasilan strict adalah `STRICT_DIRECTION_WITH_PARAMETER_ASSUMPTIONS`, dan provisional `PROVISIONAL_ASSUMPTIONS`. FOUND hanya membuktikan keterjangkauan topologis pada model ini. Fixture tersebut bukan OD final atau permintaan kendaraan aktual.

## Pemeriksaan aplikasi dan browser

SUMO-GUI membuka strict/inspect.sumocfg dan NETEDIT membuka provisional/network.net.xml dengan overlay rel; keduanya **load selesai tanpa fatal error**. Overview aktual menunjukkan koridor utama/frontage, cabang, simpang dan konteks rel/crossing. Tidak ada playback atau pengeditan/simpan network dari GUI. Detail setiap connector tidak diklaim tervalidasi visual satu per satu; pemeriksaan XML, tests dan inspector browser melengkapi overview. Lihat [GUI_INSPECTION.md](m03/GUI_INSPECTION.md).

![SUMO-GUI strict](m03/sumo-gui-strict.jpg)

![NETEDIT provisional](m03/netedit-provisional-context.jpg)

Viewer baru `frontend/network.html` membaca ekspor aktual final XML: lane shapes, node/junction, koneksi internal, direction, attributes dan provenance. Layer fungsi jalan/arah/node/koneksi/rel/crossing dapat diatur. Klik lane melalui raycast atau pencarian membuka edge ID, source way/feature, from/to, parameter dan status. Rute sukses ditampilkan putih; kegagalan tetap terlihat dan tidak diberi highlight sukses.

Pengujian browser internal mencakup pergantian varian, layer frontage/node/connector, pencarian, klik canvas, orbit/zoom/reset, route selection dan Evidence. Desktop 1920×1080 tidak overflow horizontal; layout sempit tetap dapat digunakan. WebGL READY dan console final tidak mencatat warn/error. Bukti di [BROWSER_QA.md](m03/BROWSER_QA.md) dan browser-final-state.json. Tidak ada benchmark performa, deployment atau klaim SUMO executable berjalan dalam browser.

![Strict edge inspector](m03/browser-strict-inspector.jpg)

![Provisional network](m03/browser-provisional-network.jpg)

## Build, tests dan reproducibility

**57/57 automated tests PASS**: 36 tes M01/M02 dan 21 tes M03. Pemeriksaan mencakup sumber tetap utuh, urutan node/geometri, arah, exclusion, restrictions, koneksi lajur aktual, lineage komponen, route sequences, parameter status, ekspor viewer, zero-step load dan overlay rel. TypeScript noEmit dan Vite production build M03 PASS. Log: tests.txt, typescript.txt, frontend-build.txt di m03/.

Bundle JavaScript sekitar 733,17 kB, gzip 198,84 kB. Vite memberi warning chunk >500 kB; tidak fatal dan belum dioptimasi sebagai bagian topologi. Error TypeScript awal dan penanganan visibility panah telah diperbaiki sebelum build terakhir.

Rebuild penuh dari data lokal benar-benar dijalankan, bukan sekadar dibandingkan dua salinan file. Semantic XML hash jaringan dan seluruh urutan rute identik sebelum/sesudah rebuild; lihat reproducibility.json. Byte-for-byte XML/log tidak dijanjikan karena komentar/timestamp SUMO berubah. Hash semantik final:

- Strict: `f838d8245f9b249c8475b558f34afd1367c48c397a6b3509d102293afe552085`
- Provisional: `47e8a60ac46e81e6b8cc52d75396703f756a8d02dd8c93e833ad91d885673b20`

Manifest network berisi SHA-256 setiap output turunannya. Sebanyak **115 berkas preexisting** yang dicatat sebelum M03 tetap identik, termasuk dataset, konfigurasi, frontend dan dokumentasi sebelumnya. Pemeriksaan tidak menganggap cache/build output sebagai data sumber.

## Acceptance criteria

| No. | Kriteria | Hasil dan batas |
|---:|---|---|
| 1 | Network dari M02 | PASS, lokal dan source-traceable |
| 2 | Main arterial dua arah | PASS, dua fixture aktual FOUND |
| 3 | Frontage terpisah dan koneksi dicatat | PASS; strict exit belum tersedia, provisional asumsi |
| 4 | Feeder terhubung sesuai bukti | TERBATAS; node sumber dipertahankan, strict feeder/main gagal, provisional berhasil dengan asumsi |
| 5 | Junction/edge diperiksa | PASS untuk audit; warning connector tetap unresolved |
| 6 | Komponen terisolasi dicatat | PASS, node dan movement graph serta lineage M02 |
| 7 | Arah tidak dikarang sebagai fakta | PASS policy; semua tambahan provisional jelas ASSUMPTION, belum validasi lapangan |
| 8 | Asumsi diberi label | PASS, per parameter dan per varian |
| 9 | Uji Sidoarjo–Surabaya | PASS, 56 edges |
| 10 | Uji Surabaya–Sidoarjo | PASS, 27 edges |
| 11 | SUMO-GUI | PASS, load aktual tanpa fatal error |
| 12 | NETEDIT | PASS, load aktual tanpa fatal error |
| 13 | Browser internal | PASS, ekspor aktual, seleksi/layer/provenance |
| 14 | Build dan tests | PASS, TypeScript/Vite dan 57 tests |
| 15 | Reproducibility | PASS pada semantik jaringan dan urutan rute; timestamp berbeda |
| 16 | Raw M02 tetap utuh | PASS, hash sumber dan baseline preexisting |

## Output dan rekomendasi tahap berikutnya

Konfigurasi berada di `configuration/network-m03/`, hasil di `simulation/network/m03/`, dokumentasi/evidence di `documentation/m03/`, dan viewer di `frontend/src/network/`. Jalankan `REBUILD_NETWORK_M03.bat` untuk membangun ulang atau `START_NETWORK_M03.bat` untuk preview. Petunjuk lengkap ada di `MILESTONE_03_README.md` pada root proyek.

Sebelum memakai jaringan untuk kajian kemacetan: verifikasi arah dan akses Ketajen/feeder/frontage, legalitas setiap gerakan simpang/stasiun, restriction via-way/conditional, lane-use, lebar, speed dan kontrol simpang. Prioritaskan warning connector dan pemisahan titik crossing dari lokasi fisik. Data kapasitas, volume dan OD harus diperoleh melalui proses data terpisah. Daftar tersebut adalah rekomendasi; **M04 belum dimulai dan memerlukan persetujuan pengguna**.

## Referensi teknis dan lisensi

- [SUMO Plain XML](https://eclipse.dev/sumo/docs/Networks/PlainXML.html): input network eksplisit dan penanganan connection/delete.
- [SUMO DUAROUTER](https://eclipse.dev/sumo/docs/duarouter.html): routing fixture dan opsi repair.
- [OSM Key:oneway](https://wiki.openstreetmap.org/wiki/Key:oneway): arah relatif urutan way dan aturan implisit tertentu.
- [OpenStreetMap contributors — ODbL](https://www.openstreetmap.org/copyright): atribusi sumber geografis M02.
