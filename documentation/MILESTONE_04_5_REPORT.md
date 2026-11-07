# MILESTONE 04.5 — Multiclass Network Permission Remediation

Tanggal: **31 Oktober 2026**. Proyek: `C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`.

**SYNTHETIC TEST — NOT CALIBRATED GEDANGAN TRAFFIC.**

## Hasil utama dan status

**M04.5 selesai untuk remediation software, uji multiclass dan acceptance teknis dengan batas sumber yang eksplisit.** Sembilan kategori non-oversize terbukti dirutekan, dimuat, berangkat, berpindah posisi dan tiba pada corrected provisional main corridor. Strict juga menjalankan motorcycle, passenger, pickup/van, minibus dan bus sesuai policy. Oversize tetap ditolak. Seluruh 112 tes, TypeScript/production build, internal browser dan pemeriksaan SUMO-GUI lulus.

Original M03/M04 dipertahankan. Tidak ada geometri, junction, lane shape/dimensi atau pasangan koneksi baru. Tidak ada vClass ignoring, override TraCI, auto route repair, restorasi ruas yang sudah dikecualikan M03, data survei rekaan atau pekerjaan M05. **Izin model yang inferred/provisional tidak sama dengan legalitas lapangan terverifikasi.**

## Akar masalah

`configuration/network-m03/build_network.py` baris **127** menulis literal `'allow':'passenger'` ke setiap plain XML edge. Itu filter fixture passenger M03, bukan hasil pemetaan OSM per kelas. NETCONVERT mewariskan batas tersebut ke external lanes dan internal links. Original strict mempunyai 323 road lanes dan provisional 2.043 road lanes, semuanya passenger-only. Permission probe M04 menolak kelas lain secara benar berdasarkan input ini; penyebabnya bukan kegagalan vehicle registry atau bug SUMO.

Audit meliputi converter/policy M03, plain edge/lane XML, NETCONVERT input/output, class permissions, OSM tags/raw restriction relations, registry M04, compatibility dan issue M03-PERM-01. Detail sumber, hash dan literal ada di `m045/root-cause-audit.json`. Tidak ada explicit per-class access tag pada 83 arterial edges dan 17 frontage edges sumber. Karena itu, pembukaan kelas tambahan tidak diberi status VERIFIED tanpa tag positif.

## Source code dan struktur turunan

- `backend/gedangan/m045_access.py`: evaluator access hierarchy; permission patch/NETCONVERT; audit geometri dan internal permissions; private M04 adapter; physical/type/route screens; simulation, FCD, lifecycle dan manifest.
- `configuration/access-m045/policy.json`: class hierarchy, road-role rules, status/provenance, conditional quarantine dan trailer trial guard.
- `configuration/access-m045/rebuild.py`, `start_preview.py`, `finalize_report.py`; root `REBUILD_MULTICLASS_M045.bat` dan `START_MULTICLASS_M045.bat`.
- `simulation/network/m045/{strict,provisional}/`: corrected networks, `.edg.xml`/`.con.xml` permission patches, NETCONVERT config, access decisions, geometry/permission audits, logs dan manifests.
- `simulation/demand/m045/`: compatibility/request/trips/routes/failure records, OD interval counts dan manifests.
- `simulation/runs/m045/`: delapan actual runs, tripinfo, FCD, state/metric/per-type lifecycle, config/log/manifests.
- `frontend/multiclass.html`, `src/m045/`, config/build `dist-m045/`; viewer baru terpisah dari M04.
- `tests/m045/`: 24 tests tambahan; 88 tests M01–M04 tetap utuh.

M04 registry, OD matrix, profiles dan model Krauss/LC2013 digunakan tanpa diubah. Adapter memuat modul M04 dalam instance privat; tidak mengganti global pada modul original atau mengubah output lamanya. Reuse route checks diperluas untuk menghormati **corrected connection-class permission** dan access hierarchy, bukan hanya blanket passenger filter.

## Kebijakan akses dan provenance

Urutan evaluasi: explicit OSM access hierarchy → dokumen jalan terverifikasi bila tersedia → classification inference terdokumentasi → provisional assumption bila diizinkan. Belum ada dokumen otoritas jalan spesifik yang memverifikasi izin/clearance kendaraan untuk ruas ini; tier tersebut tetap MISSING, tidak diganti dengan klaim hasil riset.

Hierarchy memakai access → vehicle → motor_vehicle → motorcycle/motorcar/goods/psv/bus/hgv/hgv:articulated. Key lebih spesifik, termasuk arah forward/backward sesuai source order, mengalahkan key umum. `yes/designated` eksplisit diberi VERIFIED terhadap tag OSM. `no/private/destination/customers/delivery/permit` dan purpose limits lain ditolak sesuai hierarki; nilai ambigu ditahan. Conditional dan lane-specific access yang belum dapat ditafsirkan dikarantina, bukan dianggap yes. Generic turn restrictions dan class-specific/conditional/via-way relations juga diperiksa; exception M03 tidak dipakai untuk memulihkan gerakan yang telah diblokir.

| Road role | Strict access tanpa tag positif | Tambahan provisional | Batas |
|---|---|---|---|
| Main arterial / trunk | motorcycle, passenger, delivery, bus: INFERRED | truck/trailer: ASSUMPTION | Bukan izin legal lokal yang sudah disurvei |
| Frontage / tertiary | motorcycle, passenger, delivery: INFERRED | Tidak ada heavy otomatis | Bus/truck/trailer butuh explicit class evidence |
| Feeder / collector | motorcycle, passenger, delivery: INFERRED | bus: ASSUMPTION | Type-specific M04 eligibility/dimensi tetap membatasi full-size bus |
| Local residential/living street | light classes: INFERRED; tag eksplisit diprioritaskan | Tidak ada heavy otomatis | Ketiadaan larangan tidak diubah menjadi kepastian hukum |
| Service | Positive source only; missing ditahan | light classes: ASSUMPTION | Bus/truck/trailer tidak otomatis diizinkan |
| Private/limited/conditional | Sesuai restriction paling spesifik; unresolved ditahan | Tidak dibuka sebagai jalan umum | M03 exclusions tidak dipulihkan |

`VERIFIED` berarti tag sumber mendukung keputusan, bukan legalitas lapangan. `INFERRED` adalah interpretasi classification/hierarchy untuk model. `ASSUMPTION` adalah temporary access trial. `MISSING` berarti dasar izin belum cukup sehingga ditahan. Tiap edge/class menyimpan keputusan, status, basis, source way/tags, provenance M045-ACCESS-01 dan field_legal_verified=false.

| Variant | vClass | VERIFIED allow edges | INFERRED allow edges | ASSUMPTION allow edges | MISSING denied edges |
|---|---|---:|---:|---:|---:|
| strict | motorcycle | 5 | 214 | 0 | 22 |
| strict | passenger | 5 | 214 | 0 | 22 |
| strict | delivery | 0 | 219 | 0 | 22 |
| strict | bus | 0 | 83 | 0 | 158 |
| strict | truck | 0 | 0 | 0 | 241 |
| strict | trailer | 0 | 0 | 0 | 241 |
| provisional | motorcycle | 117 | 1446 | 396 | 2 |
| provisional | passenger | 5 | 1558 | 396 | 2 |
| provisional | delivery | 0 | 1563 | 396 | 2 |
| provisional | bus | 0 | 83 | 384 | 1494 |
| provisional | truck | 0 | 0 | 83 | 1878 |
| provisional | trailer | 0 | 0 | 83 | 1878 |

Angka dihitung per directed edge, bukan jalan fisik atau hasil survei. Dua edge provisional bertag access=permissive ditahan konservatif sebagai akses yang tidak cukup pasti. Explicit class-positive evidence dapat mengalahkan generic access, tetapi tidak memulihkan ruas/topologi yang sudah hilang dari baseline M03.

### Heavy dan oversize gate

Registry M04 menjaga bus besar/truk sedang/berat/trailer pada main arterial, serta minimal nominal width = vehicle width + 0,4m. Truk ringan juga tunduk pada class truck policy, sehingga tidak otomatis masuk permukiman/service. Source maxwidth/height/length diperiksa numerik; unknown/unit/conditional clearance ditahan. Source weight/axle restrictions ditahan karena registry tidak mempunyai mass/load bersumber.

Trailer nominal 16,5m × 2,55m × 4m hanya percobaan **provisional arterial**, margin width nominal dan source-centreline connector deflection ≤25°. Ini screen konfigurasi sementara, bukan swept-path analysis, clearance jembatan/tinggi/beban atau permit. Kurva internal tetap hasil engine M03. Oversize 20m × 3m × 4,5m selalu NOT_ROUTABLE sampai geometri/legalitas/swept-path clearance tersedia. Walaupun vClass-nya sama dengan trailer, type-level gate tidak membiarkannya masuk accepted routes.

## Network sebelum dan sesudah

SUMO NETCONVERT **1.28.0** lokal memuat original `.net.xml` bersama plain permission edge/lane/connection patches. `.net.xml` final tidak diedit manual. Connection permission adalah irisan izin from/to lane, dipersempit restriction sumber. Tidak ada permission pada internal lane yang lebih luas dari union gerakan yang menggunakannya.

| Variant | Original → corrected nodes | Edges | Road lanes | External lane connections | New movements | Geometry sections changed |
|---|---:|---:|---:|---:|---:|---:|
| Strict | 225 → 225 | 241 → 241 | 323 → 323 | 242 → 242 | 0 | 0 |
| Provisional | 1022 → 1022 | 1961 → 1961 | 2043 → 2043 | 2874 → 2874 | 0 | 0 |

Audit exact XML mempertahankan location/projection/offset, node/junction coordinates dan shapes, seluruh external/internal edge IDs, lane shapes/length/width/speed dan connection tuples. Tidak ada join/straightening/connection baru. Oneway, withheld U-turn, boundary, barrier dan restriction M03 tetap berlaku. Main dan frontage tetap mempunyai source way terpisah. M03 source exclusions, 29 source components dan batas legal-turn/control sebelumnya tidak dianggap selesai oleh perubahan izin ini.

Audit internal: zero mismatches pada kedua varian. NETCONVERT warning mengenai terminal/withheld connections tetap disimpan, tidak disembunyikan. Fixture traffic signal/rail dinamis tidak ditambahkan.

## Compatibility dan lifecycle per kategori

Coverage memakai sepuluh kategori × sembilan OD = 90 requested cases per varian. Departures diselang 3s untuk pemeriksaan kendaraan, berbeda dari fixture coverage M04 yang lebih awal. Ini bukan demand lapangan dan bukan kontrol eksperimen kinerja trafik. LOW/MEDIUM/STRESS tetap memakai OD/type/departures M04 yang identik, hanya ID prefix dan network family yang dibedakan.

| Kategori | vClass | Strict routable / requested | Provisional routable / requested | Loaded provisional | Departed | Moved in FCD | Arrived | Failed provisional |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Sepeda motor | motorcycle | 5 / 9 | 9 / 9 | 9 | 9 | 9 | 9 | 0 |
| Mobil penumpang | passenger | 5 / 9 | 9 / 9 | 9 | 9 | 9 | 9 | 0 |
| Pickup dan van | delivery | 5 / 9 | 9 / 9 | 9 | 9 | 9 | 9 | 0 |
| Angkutan umum/minibus | bus | 3 / 9 | 6 / 9 | 6 | 6 | 6 | 6 | 3 |
| Bus | bus | 3 / 9 | 3 / 9 | 3 | 3 | 3 | 3 | 6 |
| Truk ringan | truck | 0 / 9 | 3 / 9 | 3 | 3 | 3 | 3 | 6 |
| Truk sedang | truck | 0 / 9 | 3 / 9 | 3 | 3 | 3 | 3 | 6 |
| Truk berat | truck | 0 / 9 | 3 / 9 | 3 | 3 | 3 | 3 | 6 |
| Trailer dan kontainer | trailer | 0 / 9 | 3 / 9 | 3 | 3 | 3 | 3 | 6 |
| Oversize/khusus | trailer | 0 / 9 | 0 / 9 | 0 | 0 | 0 | 0 | 9 |

Loaded per tipe berasal dari actual tripinfo records; departure/arrival dari vehicle states, movement dari perubahan posisi >1m pada FCD 1s. Seluruh kategori non-oversize mempunyai actual northbound arrival dan displacement >50m. Total teleport **0** membuktikan tidak ada kelas yang menyelesaikan perjalanan melalui teleport pada run ini. Failure tetap disimpan per requested ID.

| Kategori — provisional | Main NB | Main SB | Frontage continuity | Feeder → main | Station/Ketajen |
|---|---|---|---|---|---|
| Sepeda motor | ROUTABLE | ROUTABLE | ROUTABLE | ROUTABLE | ROUTABLE |
| Mobil penumpang | ROUTABLE | ROUTABLE | ROUTABLE | ROUTABLE | ROUTABLE |
| Pickup dan van | ROUTABLE | ROUTABLE | ROUTABLE | ROUTABLE | ROUTABLE |
| Angkutan umum/minibus | ROUTABLE | ROUTABLE | NOT_ROUTABLE | ROUTABLE | ROUTABLE |
| Bus | ROUTABLE | ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE |
| Truk ringan | ROUTABLE | ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE |
| Truk sedang | ROUTABLE | ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE |
| Truk berat | ROUTABLE | ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE |
| Trailer dan kontainer | ROUTABLE | ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE |
| Oversize/khusus | NOT_ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE | NOT_ROUTABLE |

Minibus dan full-size bus berbagi vClass bus tetapi mempunyai eligibility M04 berbeda; izin lajur bus tidak otomatis membuktikan bus besar cocok untuk semua feeder. Strict masih menahan empat OD branch/endpoint lama: feeder→main, main→feeder, frontage exit dan station east. Permission remediation tidak menciptakan belokan atau endpoint agar seluruh rute berhasil.

## LOW, MEDIUM dan STRESS corrected runs

Tiga profil sintetis M04 digunakan: 40/120/300 requested trips per 900s, seed 20261031, baseline schema 2026. Simulasi 0–2100s, step 1s, M04 car-following/lane-change/dimensi tetap ASSUMPTION. DELIBERATE failure tidak dihapus dari denominator. DUAROUTER repair=false; ignore-errors melanjutkan kasus lain tetapi setiap yang tidak terbit direkonsiliasi ke ledger.

| Variant | Profile | Requested | Routable | Failed | Loaded | Departed | Moved | Arrived | Teleports |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| strict | smoke | 90 | 21 | 69 | 21 | 21 | 21 | 21 | 0 |
| provisional | smoke | 90 | 48 | 42 | 48 | 48 | 48 | 48 | 0 |
| strict | low | 40 | 16 | 24 | 16 | 16 | 16 | 16 | 0 |
| provisional | low | 40 | 30 | 10 | 30 | 30 | 30 | 30 | 0 |
| strict | medium | 120 | 51 | 69 | 51 | 51 | 51 | 51 | 0 |
| provisional | medium | 120 | 95 | 25 | 95 | 95 | 95 | 95 | 0 |
| strict | stress | 300 | 124 | 176 | 124 | 124 | 124 | 124 | 0 |
| provisional | stress | 300 | 243 | 57 | 243 | 243 | 243 | 243 | 0 |

Pada delapan run corrected: exit 0, warning SUMO kosong, pending insertion/running at end 0, dan semua accepted tiba. Penundaan insertion sesaat masih mungkin; GUI heavy truck mencatat depart delay 9s. Pending akhir nol tidak berarti tidak pernah ada attempt tertunda. Summary/tripinfo lengkap dipertahankan. Route failure warnings dan NETCONVERT warnings tetap ada di log masing-masing.

Original M04 runs tetap tersedia terpisah dan tidak ditimpa. Coverage original strict 5/90 dan provisional 9/90, semuanya passenger; corrected strict 21/90 dan provisional 48/90. Angka ini menunjukkan coverage software/izin, **bukan** kenaikan kapasitas, kelancaran atau manfaat kebijakan. FCD original 5s dan corrected 1s juga berbeda; jumlah movement samples tidak dibandingkan sebagai metrik kinerja trafik.

## SUMO-GUI dan browser evidence

SUMO-GUI 1.28.0 actual membuka corrected provisional coverage. Vehicle Chooser memperlihatkan motor, pickup, minibus, bus, truk dan trailer. Truk berat northbound yang dipilih berada di lane w35344052_s3_p0_0_f_0 dengan odometer **553,57m**, posisi 72,38m dan speed 8,29m/s. Run GUI berhenti sekitar 104s: loaded 41, inserted/running 26, arrived 0, collisions/teleports 0. Tidak mengklaim GUI pendek ini menuntaskan demand; arrival dibuktikan run headless 2100s. Output GUI terpisah, tidak merusak manifest hasil utama.

![SUMO-GUI multiclass IDs](m045/sumo-gui-multiclass-list.jpg)

![Actual heavy vehicle parameters](m045/sumo-gui-heavy-parameters.jpg)

Internal browser menguji seluruh 16 family/variant/profile combinations, sepuluh type selectors, actual lifecycle/route ledger, permission/OD layer, source edge lookup, frontage heavy denial, arterial ASSUMPTION dan oversize failure. Playback 0→83s memuat berbagai kelas, dan semua marker pada frame 83s cocok dengan actual FCD x/y. Reset/scrub sampai 646s berfungsi. Desktop 1920×1080 dan viewport 390×844 tidak overflow horizontal; console warn/error kosong. Build produksi diverifikasi terpisah; UI QA memakai dev preview, bukan deployment. Lihat BROWSER_QA.md dan browser-qa.json.

![M04.5 browser](m045/browser-final.jpg)

![Frontage heavy access withheld](m045/browser-frontage-permissions.jpg)

## Regression, build dan reproducibility

**112/112 tests PASS**: 88 M01–M04 dan 24 M04.5. Tes memeriksa baseline hashes, private adapter isolation, root cause, exact geometry/structural connections, hierarchy/conditional/private/directional rules, heavy/frontage/service policy, source status, actual external/internal lane permissions, class-specific restrictions, numeric clearance, actual routes/lifecycle kedua arah, oversize rejection, OD/type/departure conservation, manifests dan viewer export.

TypeScript noEmit dan Vite production build `dist-m045/` PASS. Peringatan createRoot saat hot reload viewer diperbaiki dengan reuse root host M04.5; reload dan interaksi akhir mempunyai console bersih. Tidak ada kebutuhan install dependency baru. Source/output preexisting yang dijaga berjumlah **633 file** dan seluruh SHA-256 tetap sama, termasuk network M03, registry/config/OD dan hasil M04. Tidak ada data sintetis masuk observed_data.

Full rebuild benar-benar dijalankan: semantic XML network pada kedua varian dan seluruh delapan recorded trajectory JSON identik hash sebelum/sesudah. XML timestamp comments dan wall/CPU/RAM readings tidak dijanjikan byte-identik. Manifest mencatat original/corrected network hash, source policy/registry/config/OD/raw/mapping/code hashes, SUMO version, seed, simulation period dan seluruh output. Files baru M04.5 dibangun dari sumber lokal tanpa fetch.

## Performance observations

Pengukuran proses headless lokal, bukan benchmark GPU/VRAM atau klaim kondisi trafik. Windows process working-set disampel sekitar 20ms; proses pendek bisa melewatkan peak. Horizon tiap run 2100s. Profil diuji bertingkat, paling besar 300 requested, bukan ribuan kendaraan serentak.

| Variant / profile | Wall seconds | CPU process seconds | Sampled peak working set MiB |
|---|---:|---:|---:|
| strict / smoke | 0.418 | 0.328 | 28.5 |
| provisional / smoke | 0.930 | 0.875 | 59.2 |
| strict / low | 0.460 | 0.375 | 28.4 |
| provisional / low | 0.830 | 0.734 | 59.1 |
| strict / medium | 0.542 | 0.469 | 28.6 |
| provisional / medium | 1.160 | 1.078 | 59.0 |
| strict / stress | 0.932 | 0.859 | 28.8 |
| provisional / stress | 1.980 | 1.828 | 60.0 |

## Acceptance dan isu yang belum selesai

| Kriteria | Status dan batas |
|---|---|
| Seluruh regresi M01–M04 lulus | PASS; 88 lama + 24 baru |
| Motor dan beberapa non-passenger bergerak | PASS; sembilan kategori non-oversize main NB provisional, lima kategori strict |
| Parameter akses/source jelas | PASS; per-edge/class ledger, hierarchy, tier/status dan missing authority evidence |
| Frontage terpisah | PASS; source/geometri tetap, heavy tidak otomatis diizinkan |
| Original M03 immutable | PASS; original beserta M04 outputs tetap identik |
| Corrected reproducible | PASS; full semantic network/trajectory rebuild proof |
| Tidak ada bypass legalitas | PASS pada model/source constraints; tidak berarti legalitas lapangan tersertifikasi |
| Oversize tetap dibatasi | PASS; 0 routed/loaded/departed/arrived |
| Browser dan SUMO-GUI actual | PASS; screenshot, logs dan FCD match |
| Sintetis tidak dipresentasikan sebagai pengukuran | PASS; labels dan provenance tetap eksplisit |

M03-PERM-01 **remediated pada turunan M04.5**, bukan ditutup dengan menulis ulang baseline. Masih perlu verifikasi otoritas/lapangan atas akses per kelas, load/height/width dan operasi frontage; swept-path kendaraan panjang; legal restriction conditional/via-way yang sekarang dikarantina; source roads yang dikecualikan M03; serta control/connector geometry assumptions dan empat OD strict yang gagal. SUMO lane compatibility tidak membuktikan kemampuan fisik kendaraan articulated atau izin melintas nyata.

Kesiapan menuju M05: fondasi multiclass teknis kini tersedia untuk tahap berikutnya dengan batas tersebut. Kalibrasi perilaku, operasi rel/palang, signal plan final, OD/volume aktual, growth dan flyover comparison **belum dikerjakan**. **M05 tidak dimulai dan menunggu persetujuan pengguna.**

## Referensi

- [OSM access hierarchy](https://wiki.openstreetmap.org/wiki/Key:access): hubungan generic/mode-specific restriction; bukan dokumen izin lokal Indonesia.
- [OSM highway classification](https://wiki.openstreetmap.org/wiki/Key:highway): dasar classification inference model yang dinyatakan eksplisit.
- [OSM conditional restrictions](https://wiki.openstreetmap.org/wiki/Conditional_restrictions): kondisi yang belum terselesaikan ditahan.
- [SUMO Plain XML](https://eclipse.dev/sumo/docs/Networks/PlainXML.html): patch plain XML melalui NETCONVERT, tanpa hand edit network.
- [SUMO vehicle permissions](https://eclipse.dev/sumo/docs/Simulation/VehiclePermissions.html): vClass dan lane access; diperiksa pada toolchain 1.28.0 lokal.
- [OpenStreetMap contributors / ODbL](https://www.openstreetmap.org/copyright): sumber geografis M02/M03 yang dipertahankan.
