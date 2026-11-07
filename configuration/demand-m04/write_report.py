"""Render the M04 review report from recorded run metrics; no simulation."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from backend.gedangan.m04_demand import load,DOC,CONF,RUNS,DEMAND,registry

def main():
    runs=load(DOC/'run-summary.json');vehicles=registry();compat=load(DOC/'compatibility-results.json');sub=load(RUNS/'isolated-motorcycle-sublane/results.json');zones=load(DEMAND/'od-zones.json')['zones']
    types='\n'.join(f"| {v['label']} | {v['sumo_vclass']} | {v['parameters']['length']} × {v['parameters']['width']} × {v['parameters']['height']} | {v['parameters']['maxSpeed']} | {v['parameters']['accel']} / {v['parameters']['decel']} / {v['parameters']['emergencyDecel']} | {v['parameters']['minGap']} |" for v in vehicles)
    totals='\n'.join(f"| {r['network_variant']} | {r['profile']} | {r['requested_trips']} | {r['routable_trips']} | {r['failed_routes']} | {r['loaded_vehicles']} | {r['departed_vehicles']} | {r['arrived_vehicles']} | {r['moved_vehicles_recorded']} | {r['pending_insertion']} | {r['teleported_vehicles']} |" for r in runs)
    performance='\n'.join(f"| {r['network_variant']} / {r['profile']} | {r['wall_seconds']:.3f} | {r['process_cpu_seconds']:.3f} | {r['peak_working_set_bytes_sampled']/1048576:.1f} | {r['simulation_end_seconds']/r['wall_seconds']:.0f} |" for r in runs)
    bymode={mode:{r['od_id']:r for r in rows if r['vehicle_type_id']=='car'} for mode,rows in compat.items()}
    odrows='\n'.join(f"| {key} | {bymode['strict'][key]['route_status']} ({len(bymode['strict'][key]['edges'])}) | {bymode['provisional'][key]['route_status']} ({len(bymode['provisional'][key]['edges'])}) |" for key in bymode['strict'])
    zrows='\n'.join(f"| {i+1} | {z['id']} | {z['geographic_zone']['source_way_id']} | {z['geographic_zone']['source_edge']} |" for i,z in enumerate(zones))
    report=f'''# MILESTONE 04 — Vehicle System, OD Matrix & Synthetic Demand

Tanggal: **31 Oktober 2026**. Proyek: `C:\\Users\\ROG ALLY\\Documents\\EXTREME STUDIOS\\PROJECT\\Simulasi Kemacetan Lalu Lintas`.

**SYNTHETIC TEST — NOT CALIBRATED GEDANGAN TRAFFIC.**

## Status dan ringkasan

Status **PARTIAL untuk pergerakan multiclass — implementasi fondasi, pengujian SUMO dan QA browser selesai**. Registry 10 kategori, OD geografis, generator deterministik, tiga profil, validation/failure ledger, delapan run Gedangan dan viewer M04 terpisah telah dibuat. Semua kendaraan yang berhasil dirutekan dalam run ini berangkat dan tiba, tanpa teleport/pending di akhir. Source M01–M03 tetap utuh.

Batas utama yang tersisa: seluruh lajur M03 hanya mengizinkan `passenger`, sehingga sembilan kategori kendaraan lain belum bisa diuji bergerak pada Gedangan. Browser internal sempat melaporkan disabled meskipun UI sudah aktif; setelah aplikasi dibuka ulang akses berhasil, server preview dijalankan kembali dan QA visual/interaksi diselesaikan. Tidak ada bypass izin network. M05 tidak dimulai.

## Source code dan environment

Laporan M01–M03, charter, arsitektur, governance, roadmap, README M03 serta konfigurasi dan output aktual diperiksa. Dokumen lama tetap rekaman historis dan tidak ditulis ulang. Implementasi baru:

- `backend/gedangan/m04_demand.py`: registry/input validation, exact allocation, zona/OD, permission/route checks, batch generator, SUMO process runner, FCD/lifecycle extraction dan manifest.
- `configuration/demand-m04/`: registry/provenance, demand profiles, dua schema OD, rebuild wrapper, preview launcher dan report renderer.
- `simulation/demand/m04/`: request JSON, trips XML, route/failure JSON, accepted route XML, interval counts, compatibility/probe dan manifest.
- `simulation/runs/m04/`: delapan run Gedangan dan fixture sublane terisolasi, lengkap config/log/metrics/XML/trajectory/manifest.
- `frontend/demand.html`, `src/demand/`, `vite.demand.config.ts`: viewer baru port 5176, output `dist-m04/`.
- `tests/m04/`: 31 tes M04, bersama 57 regresi sebelumnya.

SUMO, NETCONVERT dan DUAROUTER **1.28.0** berasal dari portable M02, diaktifkan lewat helper environment yang sama. SUMO-GUI yang sama digunakan untuk bukti desktop. Tidak ada SUMO baru, instalasi administrator, fetch geodata, atau perubahan sistem. Parameter diperiksa terhadap installed `data/xsd/types/route.xsd` dan runtime parser dengan `--xml-validation always`.

## Registry kendaraan dan provenance

Semua nilai tabel berikut adalah **ASSUMPTION / A-VEH-01**, bukan dimensi kendaraan hasil pengukuran Gedangan. Satuan dimensi meter, maxSpeed m/s, accel/decel/emergencyDecel m/s², minGap meter. Tujuannya membedakan ukuran/dinamika secara teknis dalam test fixture.

| Kategori lokal | SUMO vClass | Length × width × height (m) | maxSpeed (m/s) | accel / decel / emergencyDecel | minGap |
|---|---|---|---:|---|---:|
{types}

Semua menggunakan **Krauss, LC2013, tau=1,2 s, sigma=0,3, speedFactor=1, speedDev=0**. Tidak ada parameter agresif atau algoritma mikroskopis buatan. Car-following/lane-changing bawaan SUMO digunakan; nilai model tetap belum dikalibrasi. Height didukung parser sebagai dimensi, tetapi tidak otomatis membuktikan clearance jembatan atau swept path.

Setiap atribut, termasuk pilihan vClass/model, memiliki status, alasan dan provenance_id dalam registry. Pemetaan minibus/bus sama-sama `bus`; tiga ukuran truk memakai `truck`; trailer/oversize memakai `trailer`. Tidak mengarang vClass lokal yang tidak tersedia. Nilai nominal bukan salinan survei atau klaim default SUMO yang diterapkan tanpa jejak.

Eligibility `A-ELIG-01`: bus/truk sedang/berat/trailer hanya pada main arterial dalam screen awal; width lane minimal vehicle width + 0,4m; seluruh lane/source access harus lolos. Width screen hanyalah asumsi teknis, bukan analisis radius/swept path. Oversize selalu ditahan karena geometry/legal/load/height clearance tidak tersedia. Keberadaan definisi valid tidak sama dengan izin rute.

## Temuan permission M03

Pemeriksaan XML dan sumolib menemukan seluruh road lane M03 `allow="passenger"`. Permission probe independen memasukkan sepuluh tipe pada rute northbound ke DUAROUTER: hanya `permission_probe_car` yang terbit. Penolakan sembilan tipe lain tercatat sebagai warning pada log lengkap. Tidak ada relabel truk menjadi passenger, vClass ignoring, TraCI permission override, atau patch network.

Compatibility matrix per varian mencakup **90 pasangan (10 tipe × 9 OD)**. Strict: 5 routable / 85 gagal. Provisional: 9 routable / 81 gagal. Pada masing-masing varian, 72 kasus ditolak karena lane permission dan 9 oversize ditolak karena clearance. Empat kegagalan tambahan strict adalah dua route disconnected dan dua endpoint excluded. Bus/truk/kendaraan panjang telah diuji kompatibilitas dan ditolak; **belum ada smoke pergerakan heavy vehicle pada Gedangan**.

Isu ini dicatat pada `m04/M03-issue-register.json`. Pembaruan izin akses memerlukan kajian source M03 tersendiri; M04 mempertahankan network.

## OD zones, assignment dan fixture

Terdapat **{len(zones)} geographic anchors** dari actual M03 edges. Envelope display ±50m dari centroid edge berstatus ASSUMPTION, bukan batas zona perjalanan hasil survei. CRS/offset mengikuti M03. Geographic zone dipisahkan dari daftar origin candidate, destination candidate, endpoint permission eligibility per tipe, network variant, confidence dan source way/edge. Daftar eligibility endpoint hanya screen izin lajur; hasil route lengkap terdapat dalam compatibility ledger.

| Marker | Zona | Source OSM way | Anchor edge |
|---:|---|---:|---|
{zrows}

Sembilan kelompok movement menggunakan endpoint fixture M03; local_trip menggunakan dua edge lokal berbeda yang benar-benar bersebelahan pada way yang sama. Semua mempunyai provenance `A-ZONE-01`. Distribusi bobot sama adalah asumsi software, bukan distribusi perjalanan Gedangan. Missing endpoint strict tidak diganti dengan edge lain agar rute terlihat berhasil.

| OD fixture (mobil) | Strict: status (edge count) | Provisional: status (edge count) |
|---|---|---|
{odrows}

Ini meliputi main kedua arah, feeder masuk/keluar, frontage internal/exit, Gedangan junction, station/Ketajen dan local. Rute frontage continuity hanya memakai frontage source ways, tetap terpisah dari main arterial. Keberhasilan frontage tidak membuktikan kelancaran observasi pengguna atau suatu kecepatan lapangan.

Schema movement disimpan di `od-matrix.schema.json`, fixture di `simulation/demand/m04/od-matrix.fixture.json`. Setiap batch memiliki `od-interval-counts.json` yang memisahkan year, OD, type, variant, interval, requested/routable/failed, dengan schema `od-interval.schema.json`. Struktur mendukung year/OD/type untuk perluasan; hanya baseline **2026** yang dihasilkan, growth records kosong dan projection tidak diimplementasikan.

## Demand generation dan routing

Profil **LOW=40, MEDIUM=120, STRESS=300 requested trips per interval 900 detik** adalah SYNTHETIC_TEST. Alasan: mulai dari smoke kecil, meningkat 3× untuk accounting/insertion, lalu stress terbatas ratusan request. Tidak ada ribuan kendaraan atau klaim peak hour. Komposisi teknis: motor 20%, mobil 40%, pickup/van 8%, minibus 6%, bus 4%, truk ringan 6%, sedang/berat/trailer/oversize masing-masing 4%.

Seed tetap **20261031**. Largest remainder allocation mengonservasi total integer per kelas dan OD; urutan kelas/OD diacak dengan RNG lokal seeded. Departures memakai stratified uniform jitter dalam 0–900s dan diurutkan. Request selection/class/departure sama antarvarian; endpoint/izin/konektivitas tetap berbeda. Tidak ada proyeksi atau randomTrips sebagai generator. Trips XML dipilih karena assignment edge sudah eksplisit; od2trips/flow XML tidak diperlukan untuk representasi ini.

Urutan batch: validate registry dan OD → precheck endpoint/permissions/clearance → generate trips → DUAROUTER repair=false → periksa output route, lane permissions, source access dan emitted lane connections → accepted routes → SUMO. `--ignore-errors true` hanya memungkinkan router melanjutkan request berikutnya; semua yang tidak terbit direkonsiliasi ke failure ledger. Precheck failures tetap ada di requested JSON meskipun tidak dimasukkan ke runnable trips XML.

Runtime error fatal menghentikan pipeline dan mempertahankan log. Tidak ada auto-repair arah atau connectivity. Output route invalid tidak diteruskan ke simulasi. Arah diuji melalui urutan from/to dan actual M03 lane movements; source conditional access belum terselesaikan ditahan konservatif.

## Hasil run dan lifecycle

SUMO berjalan 0–2.100 detik, step 1s, seed tetap, lateral model biasa, time-to-teleport 300s. Satu interval demand 0–900s memberi waktu tambahan untuk drain. Coverage smoke memakai 90 pasangan type×OD untuk memastikan mobil pada main NB/SB dan frontage diuji, bukan profil arus lapangan. Enam run LOW/MEDIUM/STRESS dijalankan setelah smoke, bertingkat dari kecil dan diukur.

| Variant | Profile | Requested | Routable | Failed | Loaded | Departed | Arrived | Movement proved in FCD | Pending at end | Teleports |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{totals}

Semua run exit code 0, tidak ada kendaraan running pada akhir horizon dan tidak ada warning SUMO pada delapan run headless ini. Warning routing/rejection tetap disimpan, bukan disamakan dengan warning simulation. Loaded berasal dari statistik SUMO, depart/arrival dari tripinfo; NOT_ROUTABLE disimpan per ID terpisah. Requested = routable + failed; routable = departed + pending; departed = arrived + running at end pada run tanpa teleport ini.

**Movement proved** memakai perubahan koordinat lebih dari 1m antar-sampel FCD. Periodenya 5s, sehingga beberapa local trips yang sangat pendek selesai sebelum dua sampel tertangkap. Mereka tetap mempunyai tripinfo arrival; tidak diklaim memiliki bukti perpindahan FCD bila tidak terekam. Pada kedua varian, fixture main NB, SB dan frontage masing-masing terbukti bergeser lebih dari 50m dan tiba. Feeders/station provisional juga diuji melalui coverage, strict gagal tetap dicatat.

Pending akhir nol tidak berarti tidak pernah ada penundaan insertion. Jumlah seluruh percobaan insertion yang gagal sesaat tidak diinstrumentasi sebagai counter tersendiri; raw summary/tripinfo mempertahankan waiting/departDelay. Tidak ada klaim terhadap antrean atau bottleneck aktual Gedangan. Konflik connector dan kontrol priority yang diwarisi tetap hipotesis untuk kajian lanjutan, bukan kesimpulan kinerja kebijakan.

## Uji motorcycle sublane terpisah

Fixture **sintetis lurus 500m, satu lane 3,2m**, tidak memakai/mengubah network Gedangan. Dua motor nominal width 0,8m, departure longitudinal sama dan lateral ±0,9m. Regular LC2013 menghasilkan {sub['regular']['same_lane_lateral_overlap_samples']} sampel dua motor overlap longitudinal pada lane yang sama; SL2015 pada lateral-resolution 0,4m menghasilkan **{sub['sublane']['same_lane_lateral_overlap_samples']} sampel**, dan keduanya tiba. Step fixture 0,2s, horizon 90s.

Ini membuktikan kemampuan teknis lateral untuk setup tersebut, bukan pembentukan filtering spontan atau perilaku motor Indonesia. Posisi lateral keberangkatan dipilih eksplisit. minGapLat=0,2m, maxSpeedLat=1m/s dan latAlignment=arbitrary merupakan asumsi fixture tambahan. Sublane tidak diaktifkan pada Gedangan. Performa dua kendaraan tidak diekstrapolasi ke ribuan kendaraan atau seluruh network.

## Bukti SUMO-GUI

SUMO-GUI aktual membuka dan menjalankan provisional coverage. Vehicle Chooser menampilkan ID aktif, salah satu passenger terlihat pada lane, kemudian meninggalkan view setelah waktu dilanjutkan. Run GUI dihentikan sekitar 169s untuk inspeksi: summary terakhir loaded/inserted 9, arrived 2, running 7, pending 0, collisions/teleports 0. Bukti kedatangan penuh berasal dari run headless selesai, bukan klaim GUI menuntaskan semua kendaraan. Output GUI terpisah agar manifest run regresi tidak rusak.

![SUMO-GUI vehicle actual](m04/sumo-gui-vehicle-paused.jpg)

![SUMO-GUI vehicle IDs](m04/sumo-gui-vehicle-list.jpg)

Overview dan later-time screenshot juga disimpan; detail di [GUI_QA.md](m04/GUI_QA.md). Aplikasi GUI yang dibuka agent telah ditutup. Tidak ada editor network atau perubahan permission.

## Viewer M04 dan browser QA

Halaman baru memiliki variant/profile, 10 vehicle classes/parameters, OD zones dan schematic connections, route/failure ledger, requested/routable counts, hasil smoke, issue register, provenance dan status **SUMO OFFLINE · RECORDED RESULTS**. Playback terbatas membaca koordinat SUMO FCD langsung, tanpa gerakan acak/interpolasi. Marker ukuran display bukan model kendaraan fisik. Real-time engine integration tidak dikerjakan.

**Internal browser QA PASS.** Setelah aplikasi dibuka ulang, viewer berhasil diperiksa langsung melalui browser internal Codex. Delapan kombinasi strict/provisional × LOW/MEDIUM/STRESS/coverage menampilkan counts yang sesuai hasil SUMO. OD route selection, zone/schematic layer toggles, filter status/type, inspector kegagalan station strict, registry sepuluh kategori dan QA issue panel diperiksa.

Playback berubah dari 5 ke 290 detik, pause/reset berhasil, scrub mencapai sampel akhir 575s, dan koordinat setiap marker pada frame 290s cocok dengan actual SUMO FCD. Tidak ada gerakan acak/interpolasi. Screenshot akhir memakai frame aktual 105s. Desktop 1920×1080 dan layout 390×844 tidak menunjukkan overflow horizontal; console warn/error kosong. Evidence lengkap di [BROWSER_QA.md](m04/BROWSER_QA.md) dan browser-qa-results.json. Pemeriksaan ini memakai Vite dev server; build produksi diverifikasi terpisah, bukan deployment.

![M04 browser actual](m04/browser-final-m04.jpg)

![Strict station route failure](m04/browser-strict-station-failure.jpg)

## Performance observations

Berikut hasil proses headless lokal, bukan benchmark target perangkat lengkap atau angka lalu lintas. Semua run horizon 2.100 simulation seconds. Wall clock mencakup proses startup dan disk output. CPU adalah process CPU seconds; RAM adalah Windows peak working-set counter yang disampel sekitar 20ms. Proses pendek dapat melewatkan puncak; VRAM/GPU dan beban total sistem tidak diukur.

| Variant / profile | Wall s | CPU process s | Sampled peak working set MiB | Simulated s / wall s |
|---|---:|---:|---:|---:|
{performance}

STRESS adalah 300 **requested**, bukan 300 kendaraan serentak: strict hanya 70 dan provisional 120 accepted, akibat permission/connectivity. Karena perbedaan itu, hasil antarvarian tidak dibandingkan sebagai bukti efektivitas kebijakan atau throughput jaringan nyata. Tidak ada optimasi 3D besar pada M04.

## Automated tests, build dan reproduksi

**88/88 tests PASS**: 31 M04 + 57 regresi M01–M03. Meliputi registry bounds/provenance, unsupported class rejection, zone geometry/edge assignment, schema movement/counts, exact allocation/deterministic seed, unique IDs, intervals, immutable lane permission, independent DUAROUTER rejection, heavy eligibility, failure conservation, actual lane route validation, main NB/SB/frontage arrival/movement, manifest hash, XML/JSON validity, sublane separation dan FCD playback-source equality.

TypeScript noEmit dan Vite production build M04 PASS. Bundle JS sekitar 238,57kB (gzip 74,89kB), CSS 7,82kB (gzip 2,41kB). Browser visual/interaksi juga diuji secara terpisah di internal browser. Log di `m04/tests.txt`, `typescript.txt`, `frontend-build.txt`.

Full rebuild benar-benar dijalankan; seluruh **8 trajectory JSON** identik hash sebelum/sesudah, termasuk ID, timestep, position, speed dan lane. Generation seed determinism juga diuji. Raw XML comments timestamp dan performance readings tidak dijanjikan byte-identik. Run/demand manifests menyimpan network byte hash, seed, versi SUMO, config/registry/OD hashes, source code hashes, waktu run dan validation status. Fixture sublane mempunyai manifest terpisah. Rebuild membaca input lokal yang sama tanpa fetch.

Sebanyak **311 berkas preexisting** M01–M03 yang dicatat sebelum pekerjaan tetap identik SHA-256; termasuk raw M02, konfigurasi/output network dan frontend M03 serta source/docs sebelumnya. Tidak ada data sintetis di observed_data. Baseline manifest dan metadata audit tersedia di `m04/previous-milestones-sha256.json` dan build-manifest.json.

Koreksi selama implementasi tetap dicatat: SUMO menolak `latAlignment=keep`; diganti `arbitrary` yang didukung XSD dan parser. Path ekspor coverage smoke awal diperbaiki agar mengambil compatibility directory. CSS import kosong yang menggagalkan build dihapus. Assertion test awal yang mengharapkan Error diganti pemeriksaan warning penolakan aktual. Error awal tidak disembunyikan sebagai run berhasil; bukti error parser/export dipertahankan dalam dokumentasi.

## Data governance dan issue register

OBSERVED tetap kosong/tidak ditulis. RESEARCH_REFERENCE memuat sumber M03 dan dokumentasi SUMO; ASSUMPTION mencakup dimensi, model, eligibility dan zone assignment; SYNTHETIC_TEST mencakup requests/komposisi/volume; SIMULATED_RESULT mencakup routes, lifecycle, FCD dan metrics. Model belum dikalibrasi dan label ini tampak pada output/viewer.

M03-PERM-01 menahan multiclass; M03-CONN-02 mencatat empat OD strict gagal; M03-GEOM-03 menahan oversize karena clearance tidak diketahui; M03-JUNCTION-04 mempertahankan warning geometri/priority-control sumber. Rekomendasi adalah meninjau permission/access sources dan lane-level turning geometry sebelum memakai kelas kendaraan beragam. Tidak ada perubahan diam-diam yang membuat requested terkesan 100% berhasil.

## Acceptance criteria satu per satu

| No. | Kriteria | Status dan bukti/batas |
|---:|---|---|
| 1 | Semua kategori mempunyai definisi valid | PASS schema/parser untuk 10 tipe; izin gerak Gedangan hanya passenger |
| 2 | Registry mempunyai provenance | PASS, setiap parameter ASSUMPTION dengan alasan |
| 3 | OD zone/matrix terstruktur | PASS, source anchor, candidates, eligibility, variant, schema/fixture/counts |
| 4 | Generator berjalan | PASS, LOW/MEDIUM/STRESS di dua varian |
| 5 | Sintetis reproducible | PASS, seeded generation dan actual rebuild trajectory hashes |
| 6 | Routing menghormati arah/permissions | PASS, denied classes tetap gagal; no network repair |
| 7 | Koridor utama kedua arah diuji | PASS untuk passenger; multiclass Gedangan belum didukung izin M03 |
| 8 | Frontage terpisah diuji | PASS passenger, 17-edge route dan recorded movement/arrival |
| 9 | SUMO menjalankan sintetis | PASS, 8 run headless ditambah GUI dan fixture motor terpisah |
| 10 | Depart/move/arrive terverifikasi | PASS main NB/SB/frontage; sparse local FCD limitation dicatat |
| 11 | Route failures tidak tersembunyi | PASS, full requested/failure records dan router logs |
| 12 | Strict/provisional terpisah | PASS, network hashes, IDs, configs dan outputs terpisah |
| 13 | Browser internal menampilkan M04 | PASS, actual UI, variant/profile/layers/filter/registry/playback dan screenshots |
| 14 | Tests dan build | PASS 88 tests + TypeScript/Vite dan internal browser QA |
| 15 | Source M01–M03 utuh | PASS 311 baseline hashes dan unchanged network |
| 16 | Tidak mengklaim kondisi aktual | PASS, synthetic/not-calibrated labels dan batas hasil eksplisit |

Seluruh kriteria fondasi yang tercantum telah diperiksa; batas terhadap tujuan pergerakan multiclass tetap berlaku karena izin sumber M03. Ini belum membuktikan motor/bus/truk berjalan pada Gedangan. Tidak ada M05/M06 behavior calibration, operasi kereta, signal plan final, flyover comparison, projection 2027–2040, final dashboard, realistic 3D atau presentasi final.

## Rekomendasi M05 — belum dikerjakan

Browser QA M04 telah selesai. Tinjau terlebih dahulu izin akses M03 untuk motorcycle/delivery/bus/truck/trailer dengan source dan policy yang jelas; rerun permission/route checks dan smoke setelah perubahan jaringan ditinjau. Peroleh clearance oversize dan lakukan analisis gerakan kendaraan panjang; width screen saja tidak cukup. Setelah fondasi itu, M05 dapat mengevaluasi perilaku mengikuti/lateral dan operasi perlintasan memakai sumber terpisah. Semua rekomendasi ini belum dijalankan dan M05 memerlukan persetujuan pengguna.

## Referensi

- [Vehicle definitions SUMO](https://eclipse.dev/sumo/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html): nama parameter dan model; runtime 1.28 lokal tetap otoritas implementasi.
- [Vehicle permissions](https://eclipse.dev/sumo/docs/Simulation/VehiclePermissions.html): hubungan vClass dengan izin lajur; diperiksa langsung pada network M03.
- [Sublane Model](https://eclipse.dev/sumo/docs/Simulation/SublaneModel.html): lateral resolution dan parallel two-wheel technical capability.
- [SUMO FCD output](https://eclipse.dev/sumo/docs/Simulation/Output/FCDOutput.html): ekspor posisi/speed dan sampling period.
- [OpenStreetMap contributors / ODbL](https://www.openstreetmap.org/copyright): geometri M02/M03.
'''
    (ROOT/'documentation/MILESTONE_04_REPORT.md').write_text(report,encoding='utf-8')
    print('Wrote M04 report from',len(runs),'recorded runs;',len(zones),'zones')

if __name__=='__main__':main()
