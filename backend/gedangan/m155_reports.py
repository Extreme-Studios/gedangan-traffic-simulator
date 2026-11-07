"""Reports derived from actual retained evidence; incomplete gates remain explicit."""
from .m155_common import *
def table(head,rows):return '\n'.join(['| '+' | '.join(head)+' |','| '+' | '.join(['---']*len(head))+' |']+['| '+' | '.join(str(v).replace('|',' / ')for v in r)+' |'for r in rows])
def main():
 cases={p.stem:load(p)for p in (DOC/'cases').glob('*.json')};base=cases['baseline-3000'];geo=load(DOC/'network-reality-audit.json');orig=load(ROOT/'documentation/m15/geometry-audit.json');rc=load(DOC/'rootcause'/(base['run_id']+'.json'));pairs=load(DOC/'controlled-comparisons.json');rail=load(DOC/'rail-audits'/(base['run_id']+'.json'));manual=load(DOC/'manual.json');audits=load(DOC/'xml-audit-summary.json');protection=load(DOC/'preservation-after.json');cat=load(DOC/'approach-catalog.json');api=load(DOC/'api-workflow.json')
 header='2 November 2026, WIB. Staging M15.5 terpisah: http://127.0.0.1:5201/.\n\n**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**\n\n**PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.**\n\n'
 def write(name,title,body):
  (ROOT/name).write_text('# M15.5 — '+title+'\n\n'+header+body.strip()+'\n',encoding='utf-8')
 refs='''
## Sumber dan batas interpretasi

[Peta Jalan Pemkab Sidoarjo](https://sidoarjokab.go.id/peta-jalan) dan [GeoJSON yang dipakai halaman tersebut](https://sidoarjokab.go.id/jalan) dipertahankan lokal beserta hash/tanggal/rights pada `documentation/m155/source-register.json`. Ada 23 fitur yang memotong extent studi. Ini referensi peta publik; bukan survei lane, median, rambu atau kapasitas 2026.

[Repositori penelitian PTDI-STTD 2024](https://digilib.ptdisttd.ac.id/8270/) memberi konteks simpang utama, simpang stasiun dan frontage. Proposal perubahan infrastruktur dalam penelitian tersebut tidak diubah menjadi kondisi eksisting.

[Penelitian UINSA 2023](https://digilib.uinsa.ac.id/63857/2/Nurul%20Aulia%20Fadilah_H95219051%20ok.pdf), PDF halaman indeks 66/69, memberi titik lokasi bernama Jenggolo. Teks PDF dibaca melalui web; download PDF lokal gagal TLS. Tidak ada klaim hash PDF lokal. Titik itu mendukung pemeriksaan alias spasial, bukan penggantian nama atau legalitas belok secara otomatis.

Snapshot OSM 31 Oktober 2026: `geodata/raw/gedangan-network.json`, hash `4bc46117ffae23aa90ade1e9c155601cfd90217cbca82c5bcc69fedbae0849f1`, atribusi OpenStreetMap contributors, ODbL-1.0. Kesamaan antarpeta tidak dianggap validasi lapangan independen.
'''
 status=table(['Segmen / parameter','Status','Makna'],[
 ['1961 external road edges','VERIFIED FROM SOURCE','Source way/nodes/koordinat terhubung ke snapshot OSM; bukan 1961 ruas tersurvei'],
 ['Lane count/width/speed/direction/control','PROVISIONAL; status parameter rinci tetap disimpan','VERIFIED/INFERRED/ASSUMPTION/MISSING diwarisi per parameter, tidak dihapus'],
 ['Median opening, U-turn, station gate, clearance','UNKNOWN / REQUIRES FIELD CHECK','Kedekatan geometri tidak memberi izin legal'],
 ['Kapasitas, OD, count dan timing resmi 2026','MISSING','Demand contoh tidak dikalibrasi'],
 ['Jenggolo vs label OSM Ketajen','PROVISIONAL alias','Near-match 6.03m / 4.65m; Sedati/Jenggala belum dipastikan']])
 write('M15_5_NETWORK_REALITY_AUDIT.md','Network Reality Audit',f'''
## Hasil

**GEOSPATIAL ACCEPTANCE: PARTIAL.** Tidak ada dasar yang cukup untuk memindahkan centerline atau membuat koneksi baru. Seluruh 1961 road edge mempunyai inventaris source ID, koordinat geografis, arah, entry/exit, kelas lane dan koneksi downstream. Belum ada edge yang mendapat sertifikasi fisik lapangan.

{status}

## Pemeriksaan actual source

Audit membaca network XML `simulation/network/m051/provisional/network.net.xml`, raw OSM, M03 source-to-edge, lane geometry, connection/via/controller, serta run FCD/tripinfo/ledger. Laporan M15 tidak dipakai sebagai bukti PASS tunggal: hasil 3000 dihitung ulang dari staging baru dan diverifikasi terhadap XML dan playback.

Proyeksi node OSM ke SUMO: galat maksimum {orig['max_node_projection_error_m']:.5f}m. Offset centerline terhadap sumber mempunyai median {orig['median_centerline_source_offset_m']:.5f}m; ini konsistensi konversi sumber, bukan galat terhadap as-built. Renderer membaca koordinat lane yang sama (galat array geometry {orig['renderer_lane_shape_error_m']}m). Sampling playback/FCD diperiksa terpisah.

Frontage anchor lama berjarak {geo['frontage_m15_anchor_distance_from_crossing_m']:.2f}m dari crossing. Frontage tidak dipindah ke simpang pusat. Ketajen dan railway-crossing adalah cohort yang berbagi ruang koridor, bukan dua count cordon independen. Nama Sedati/Jenggolo/Jenggala serta seluruh aliran boundary belum tervalidasi. Stasiun memakai OSM node 1359952188; road frontage terdekat 18.13m bukan bukti adanya gate kendaraan yang legal.

## Overlay yang dapat diperiksa

`documentation/m155/segment-status-overlay.geojson`: koordinat lon/lat, source status dan status aturan terpisah per segmen. `road-inventory.json`: tabel lengkap semua edge dan lane. `technical-map.json`: overlay interaktif termasuk sumber Pemkab dan selisih midpoint per edge. SVG/PNG EPSG:32749: `figures/georeferenced-extent`, `georeferenced-junction`, `georeferenced-station`. Offset lokal SUMO dikembalikan ke UTM pada plot. Overlay memperlihatkan perbedaan antarsumber; sumber Pemkab tidak diperlakukan sebagai centerline lajur terukur.

![Overlay simpang](documentation/m155/figures/georeferenced-junction.png)
{refs}
''')
 topology=table(['Komponen XML','Original','M15.5','Diff'],[[k,geo['before_topology'][k],geo['after_topology'][k],v]for k,v in geo['topology_diff'].items()])
 write('M15_5_NETWORK_CORRECTION_REPORT.md','Network Correction Report',f'''
## Keputusan koreksi

**Tidak ada koreksi geometri yang terverifikasi.** M15.5 menyediakan frozen execution copy berlabel `m155-existing-provisional-1`, bukan mengklaim sebuah network physically corrected. Byte salinan identik dengan baseline M05.1/M15; tidak menjalankan NETCONVERT untuk menyusun ulang geometri tanpa kebutuhan yang terbukti.

Original: `simulation/network/m051/provisional/network.net.xml`.
Copy eksekusi: `simulation/network/m155/provisional/network.net.xml`.
Kedua SHA256: `{geo['network_sha256']}`.

{topology}

Connection/junction/railway diff kosong; route compatibility change akibat network = 0. Original tetap immutable. Tidak ada flyover, widening, median opening, reverse train track, bypass vClass atau forced insertion.

## Perubahan source code yang dilakukan

Semua penambahan dipisahkan dengan namespace M155. `m155_common` menjaga snapshot dan salinan frozen. `m155_reality` membuat inventaris dan overlay publik. `m155_network` mewarisi rute legal M15 tanpa mengubah graf. `m155_demand`/`m155_engine` memisahkan 60 menit pembentukan demand dari execution horizon, mencatat checkpoint 3600s, hash cohort, dan discharge censored. Ekspor playback gzip dioptimalkan tanpa mengubah traffic model. `m155_rootcause`, `m155_rail_audit`, `m155_evidence` dan `m155_edge_inspection` membaca bukti aktual. `m155_server` menyediakan API staging dan postprocess FCD; frontend `src/m155` menambah debugger, top-down dan penjelasan statistik. Renderer world M15 dipertahankan.

Network routing helper lama masih membaca baseline yang byte-identik. Karena itu validasi membandingkan hash kedua file sebelum menjalankan; apabila ada revisi geometri berikutnya, helper harus diisolasi ke graph baru sebelum dapat disebut corrected network.

## Reproduksi

Dari root proyek: `.venv/Scripts/python.exe -m backend.gedangan.m155_experiments bench`, kemudian `controls` dan `manual`. Run beridentitas input/source/toolchain disimpan pada `simulation/runs/m155/`; bila identitas sama, hasil tersimpan digunakan kembali. Untuk rerun baru gunakan nama eksperimen baru, tanpa menghapus run lama. Jalankan `m155_rootcause`, `m155_evidence`, `m155_edge_inspection`, `m155_rail_audit`, `m155_figures` untuk bukti turunan. `network-version.json`, `network-topology-diff.json`, source snapshots dan input/output manifests menyimpan provenance.

## Batas

Menggeser jalan mengikuti satu peta publik yang lebih kasar tidak dibenarkan. Kesalahan nyata berupa gate, jumlah track, median, lebar efektif, lane assignment, atau turn restriction masih membutuhkan bukti. Semua tetap PROVISIONAL/UNKNOWN. Tidak ada klaim improvement before/after geometry karena tidak ada perubahan fisik yang didukung.
''')
 approaches=[]
 for a in cat['approaches']:
  approaches.append([a['id'],a.get('anchor_edge'),', '.join(t for t,m in a['movements'].items()if m.get('available')),a.get('boundary_status','Selected model cohort')])
 write('M15_5_APPROACH_CONNECTIVITY_REPORT.md','Approach Connectivity Report',f'''
## Coverage

Inventaris mencakup **semua 1961 external road edge**, bukan hanya enam fixture. Field lengkap: road/source name, way/node ID, lon/lat, edge/lane ID, entry/exit node, kelas lane, arah koneksi, via, controller/link, dan downstream names. Lihat `documentation/m155/road-inventory.json`. Semua koneksi berasal dari actual XML, tidak dibuat dari jarak antargaris.

{table(['Cohort input','Anchor','Gerakan model ditawarkan','Batas interpretasi'],approaches)}

`approach-catalog.json` menyimpan prefix/suffix dan chain koneksi yang dipakai. `route-compatibility.json` menyimpan hasil per class/approach/turn beserta reason. Kelas yang memiliki lane permission belum otomatis lolos registry/access screen. Kedekatan akses stasiun tidak ditambahkan sebagai OD legal baru.

## Missing movements

1. **Anchor salah / split junction:** omission M14 telah diperbaiki M15 dengan traversal koneksi eksplisit lintas signal/priority node. M15.5 mempertahankannya dan mengaudit adjacency; bukan membuat belokan baru.
2. **Tidak ada koneksi model:** debugger menampilkan outgoing kosong/terminal. Ini membuktikan ketiadaan di model, tidak membuktikan larangan fisik. Terminal di boundary juga bukan otomatis bug.
3. **Koneksi source hilang ketika conversion:** belum ada kasus yang terbukti hanya dari referensi publik. Tidak ada repair yang direkayasa untuk menaikkan route success.
4. **Aturan belum diketahui:** label UNKNOWN / REQUIRES FIELD CHECK. Direct U-turn tertentu di graf tidak otomatis dipromosikan ke gerakan default; median/larangan aktual belum terverifikasi.

Nama koridor timur pada OSM adalah Ketajen. Titik penelitian 2023 bernama Jenggolo berjarak 6.03m dan 4.65m dari dua edge tersebut, sehingga menjadi kandidat alias provisional. Nama Sedati/Jenggala dan batas arus penting lain belum dipastikan. Perlu survei turning, boundary cordon dan rambu sebelum seluruh pendekat dapat disebut lengkap.

## Regresi demand dan izin

Manual 10 kategori @12 = {manual['requested']} request; {manual['routed']} routed/loaded/departed, {manual['moved']} moved, {manual['arrived']} arrived, {manual['active']} active, {manual['not_departed']} pending, {manual['failed_routes']} explicit route failures. Bicycle/nonmotorized dan kendaraan berat yang gagal screen dipertahankan sebagai kegagalan, tidak diganti passenger. Default runnable mix tidak dipromosikan menjadi komposisi Gedangan terukur.

Raw per vehicle: `simulation/runs/m155/{manual['run_id']}/vehicle-results.json`; alasan kegagalan juga ada di XML audit. Shape/lane/connection immutable; frontend tidak boleh menambahkan koneksi agar input terlihat berhasil.
{refs}
''')
 evidence=table(['Kondisi teramati akhir 3600s','Unique pending IDs','Persen /1086'],[[q['category'],q['vehicles'],f"{q['percent_of_unique_pending']:.2f}%"]for q in rc['evidence_coverage']])
 write('M15_5_PENDING_INSERTION_ROOT_CAUSE.md','Pending Insertion Root Cause',f'''
## Temuan utama

**Full causal attribution: UNRESOLVED.** Run `{base['run_id']}` mereproduksi tepat 3000 requested/routed/loaded, 1914 departed/moved, 1346 arrived, 568 active dan 1086 pending. Semua 1086 pending tetap di ledger; tidak dibuang atau diubah menjadi gagal rute. Northbound 600 (55.25%), southbound 486 (44.75%); cohort lain tidak memiliki pending akhir.

{evidence}

Persentase menggunakan **unique pending ID pada horizon**, bukan jumlah sampel 10s. Kategori pertama berarti tidak ada lane berizin dengan ruang geometris nominal length+minGap yang cukup pada snapshot akhir. Ini bukti kondisi yang menghalangi, bukan angka “23.39% disebabkan geometri”. Pada 832 lainnya, proxy celah cukup di setidaknya satu lane tetapi safe insertion/route lane/downstream/junction checks tidak terpisah. SUMO tidak mengembalikan reason lengkap per kendaraan; tidak diberi persentase sebab sinyal/kereta palsu. Snapshot akhir juga bukan riwayat lengkap penyebab sepanjang jam.

## Bukti origin, antrean dan penyimpanan

Northbound origin `w562358500_s11_p0_0_f` panjang lane 101.25m; southbound `w512351908_s1_p0_0_f` 169.30m. **0/1086** berasal dari origin di bawah 5m. Ini menolak penjelasan langsung “semua pending karena boundary edge terlalu pendek”; tidak membuktikan storage downstream telah realistis.

Maksimum sampel northbound: 51 aktif pada edge, 28 berhenti pada satu lane, stopped span 101.04m, 107763 vehicle-s berhenti. Southbound: 87 aktif, 47 berhenti pada satu lane, span 169.12m, 147930.5 vehicle-s berhenti. Edge count dan single-lane max adalah metrik berbeda. Queue mendekati panjang lane menunjukkan antrean nyata **dalam model**, bukan visual congestion buatan. Boundary samples berulang bukan persentase unique kendaraan atau sertifikasi spillback lapangan.

546 external dan 1911 internal lane di bawah 5m ada pada network sumber; segmentation tidak otomatis kesalahan. Kecepatan/occupancy/queue tiap edge, route concentration, origin/class, insertion delay dan censorship tersedia di `edge-diagnostics.json`, `insertion-samples.json`, `approach-analysis.json`, `demand-timeline.json`, FCD dan ledger.

## Pengujian penjelasan alternatif

Controller asumsi mengisolasi sembilan link protected (27 phase, cycle153s, green12/yellow3/allred2). Ini kandidat bottleneck konservatif; bukan timing APILL resmi. Green30 memberi 1483 arrived /970 pending. Menghilangkan train events memberi 1342 arrived /1084 pending. Efek ini terukur di model dan tidak mengisolasi kontribusi kausal aditif; interaction dan safe insertion tetap ada. Jangan mengartikan delta dua kendaraan sebagai persentase sebab seluruh backlog.

Menambah execution horizon menjadi7200 tanpa demand baru menghasilkan 2071 arrived, 475 active, 454 pending. Setelah tambahan60 menit jaringan belum kosong; discharge time **censored**, bukan “selesai dalam120 menit”. Route concentration (35% masing-masing cohort utama), assumed signals, insertion lane safety dan downstream storage masih perlu pengukuran/detector diagnostics lebih lanjut sebelum disimpulkan sebagai kapasitas Gedangan atau bug conversion.

Tidak ada mass-balance loss, illegal permission, collision atau unexplained teleport pada audit run ini. Itu tidak mengesahkan seluruh konektivitas fisik. Implementasi berhasil mempertahankan backlog; validitas bottleneck terhadap lapangan belum selesai.

Data per-ID: `documentation/m155/rootcause/{base['run_id']}.json`. Bukti counterfactual: `controlled-comparisons.json`. Tidak ada forced insertion, ignore permission, route rewrite atau queue removal.
''')
 comparisons=table(['Kasus','Execution menit','Departed akhir','Arrived akhir','Active akhir','Pending akhir','Mean wait departed (s)'],[[r['case'],r['execution_horizon_s']//60,r['end']['departed'],r['end']['arrived'],r['end']['active'],r['end']['not_departed'],f"{r['mean_waiting_s_departed_censored']:.2f}"]for r in pairs['comparisons']])
 bench=table(['Requested /60min','Routed','Loaded','Departed','Moved','Arrived','Active','Pending','SUMO loop wall s','Run ID'],[[r[k]if k!='simulation_wall_s'else f"{r[k]:.3f}"for k in ['requested','routed','loaded','departed','moved','arrived','active','not_departed','simulation_wall_s','run_id']]for r in load(DOC/'one-hour-results.json')])
 write('M15_5_3000_VEHICLE_COMPARISON.md','3000 Vehicle Comparison',f'''
## Fair comparison

Seluruh pasangan memakai **exact full request list yang sama**, tidak hanya seed yang sama: ID, vehicle category, approach, movement, edge route dan jadwal departure. Cohort SHA256 `{base['cohort_sha256']}`. Network SHA256 `{geo['network_sha256']}`. Semua road demand dibuat selama3600s. Semua perbandingan mempunyai 3000 routed/loaded, 0 route failure.

{comparisons}

Baseline3600 dan discharge7200 mempunyai checkpoint3600 yang persis sama: 1914 departed,1346 arrived,568 active,1086 pending. Kolom discharge adalah **akhir120 menit**, bukan hasil jam pertama yang membaik. Tambahan60 menit belum mengosongkan jaringan. Clearance time/additional discharge completion tetap null/censored; jangan mengisi estimasi buatan.

Green30 hanya mengganti green12→30, urutan sembilan protected links/yellow3/allred2 tetap. Cycle berubah153→315s sebagai konsekuensi parameter tersebut, bukan faktor tersembunyi. No-trains hanya menghapus daftar event KA, road request list tidak berubah. Discharge tidak menambah request atau event KA setelah jam pertama. Tidak ada perbandingan before/after geometry improvement karena tidak ada koreksi geometri terverifikasi.

Mean waiting menghitung departed termasuk trip aktif censored; berbeda dari travel time arrived-only dan belum mencakup semua delay pending. Tidak boleh membandingkannya sebagai indikator penelitian sebelum demand/network dikalibrasi.

## Regresi empat load level, actual SUMO

{bench}

Waktu adalah wall-clock loop SUMO+TraCI dan pencatatan pada mesin ini, beberapa workload berjalan bersamaan. Bukan pure CPU benchmark terisolasi atau FPS browser. `generation_wall_s` dan `total_wall_s` tetap ada pada raw result; playback loading time, median/p5 FPS, stalls dan memory M15.5 belum tersedia karena browser ditolak.

## Pembacaan throughput yang benar

Raw inherited key `throughput_arrivals_per_hour` memakai jumlah tiba akhir-eksekusi dibagi durasi demand. Pada extended run definisi itu **bukan** laju dua jam atau hasil jam pertama. Raw output dipertahankan utuh; `controlled-comparisons.json` menghitung dua rate eksplisit dan UI memakai checkpoint. Pada discharge, first-hour arrivals/h =1346; execution-window arrivals/h =1035.5 (2071/2). Tidak memakai angka2071 sebagai throughput jam pertama.

![Perbandingan dan kondisi pending](documentation/m155/figures/actual-comparisons.png)

Run evidence lengkap: `simulation/runs/m155/<run_id>/` (request, demand, XML, FCD, tripinfo, ledger, playback, signal events, input/source/output manifests). Delapan audit independen lulus; jumlah request tidak disamakan dengan jumlah kendaraan yang terlihat pada suatu frame.
''')
 write('M15_5_RAIL_SIGNAL_NETWORK_REPORT.md','Rail and Signal Network Report',f'''
## Alignment dan crossing actual output

18 inherited rail edge dan crossing node `osm_859708050` dipertahankan. Actual road crossing via-links: `{rail['road_crossing_via_links']}`. FCD baseline3000 memeriksa front kendaraan pada sample0.5s; {len(rail['train_lane_geometry_offset_above_0_03m'])} train front keluar garis lane di atas0.03m, {len(rail['steady_red_first_entry_samples'])} steady-red road first entry, {len(rail['phase_boundary_ambiguous_entry_samples'])} ambiguous phase-boundary entry. Ada {rail['closed_crossing_stopped_road_samples']} sampel road stopped saat state crossing tertutup. Ini sampel vehicle-time, bukan863 kendaraan berbeda.

Train-front crossing intervals: `{rail['train_front_crossing_sample_intervals']}`. Waktu ini actual sample, berbeda dari nominal assumed arrivals600/1800/3000s. Palang/controller dan sinyal pada playback membaca event rekaman SUMO, tidak memakai timer dekoratif.

## Arah dan clearance

Graph hanya mendukung N_TO_S. Referensi penelitian memberi konteks stasiun/track yang lebih rumit, tetapi tidak cukup untuk menciptakan reverse route dengan legalitas/clearance terverifikasi. Dua arah **UNAVAILABLE**, bukan dipalsukan. Nominal timetable, closing/opening/recovery parameter tetap editable dan ASSUMED.

Tidak tersedia footprint bangunan tersurvei atau swept-volume train/road clearance. Tidak mengklaim “tidak menabrak bangunan” hanya karena titik FCD berada di rail lane. Audit sampling front0.5s juga tidak memberi jaminan continuous-body clearance, signal interlocking fisik, stop-line atau posisi gate aktual. GEOSPATIAL PARTIAL.

## Sensitivitas yang dapat diulang

Pada same3000 road cohort, no-trains menghasilkan1916 departed,1342 arrived,574 active,1084 pending; baseline1914/1346/568/1086. Perubahan kecil dan mixed-sign tidak mendukung klaim kereta sebagai penyebab utama1086 pending. Green30 meningkatkan arrived dalam model, tetapi isolated protected-link program belum sesuai timing lapangan yang diverifikasi. Hasil tidak menjadi rekomendasi rekayasa APILL.

Data audit: `documentation/m155/rail-audits/{base['run_id']}.json`; raw `signals.json`, `fcd.xml` dan train schedule pada result. Tidak ada rail geometry edit, reverse connection buatan, atau kendaraan yang diizinkan menembus closure melalui override.
{refs}
''')
 write('M15_5_VISUAL_VERIFICATION.md','Visual Verification and Performance',f'''
## Status aktual

**BROWSER VISUAL QA: BLOCKED. VISUAL QUALITY PENDING. PERFORMANCE ACCEPTANCE PENDING.** Browser tool ditolak dengan “Local browser use is disabled in Work settings”. Pengguna telah diberi permintaan untuk mengaktifkan akses. Tidak ada screenshot UI/top-down, real video, FPS median/p5, stall, loading time atau memory M15.5 yang berhasil diambil pada sesi ini. Bukti visual/FPS M15 tidak dipakai ulang sebagai bukti M15.5. Tidak ada bypass headless browser untuk menutupi blocker.

## Yang sudah dibuat dan dapat diperiksa setelah akses tersedia

Staging http://127.0.0.1:5201/ memakai isolated `frontend/dist-m155`. Renderer world lama dipertahankan, bukan redesign premium. Top-down camera ditambah berdasarkan posisi heads junction aktual. Visual Network Debugger memungkinkan memilih1961 edge, overlay OSM/Pemkab/SUMO/rail, source ID, koordinat, lane direction/permission/length, downstream/via/controller/link, signal states, rail closure, active/stopped samples dan pending origin.

Jumlah masuk edge memakai unique ID pertama teramati di FCD0.5s, bukan jumlah input cohort. Kunjungan edge pendek antarsampel dapat terlewat. Queue summary memakai actual edge-diagnostics; data tidak tersedia ditulis MISSING, bukan dianggap nol. End pending circles dan maksimum queue ditandai sebagai statistik horizon; current active/stopped mengikuti timestamp. Source geometry status dan physical-rule status dipisahkan. Terminal edge bukan otomatis jalan ilegal/putus secara fisik.

Presentation band memuat tanggal/jam WIB, request/routed/departed/arrived/active/pending/failed akhir, dan current sampled moving/stopped. Fullscreen tetap menampilkan backlog dan dua watermark. Tidak ada decorative moving traffic. Source-array geometry sama; actual playback dipasangkan ke FCD post-step +0.5s. Pada delapan audit, matched-position error maksimum0m dengan toleransi0.02m.

## Verifikasi yang sudah selesai

TypeScript dan isolated Vite production build lulus (bundle~831KB; warning chunk>500KB). {len(audits)} XML/FCD audits lulus, seluruh frame-count dan permission check konsisten. API Save/Load/Duplicate/Preview/Generate serta derivasi edge-count otomatis lulus pada run `{api['generated_run']}`; ini API evidence, **bukan interaksi browser**. Static maps SVG/PNG dan chart eksperimen sudah dirender dan diperiksa; diberi label derived figure, bukan screenshot UI.

Actual SUMO execution wall times empat beban ada di laporan perbandingan dan raw result. Tidak ada klaim seluruh sesi lancar dari satu FPS sample. Mesh sederhana tetap memerlukan review pengguna; tidak diberi aesthetic PASS.

## Checklist browser yang masih wajib

1. Load setiap500/1000/3000/5000 recording, ukur loading/time, network version dan active count.
2. Pilih road, periksa detail, koneksi dan permission pada core/full/selected map.
3. Jalankan top-down dan intersection, play/pause/speed, switching dan repeat; rekam actual memory, median/p5 FPS serta stalls termasuk sample rendah.
4. Long-session playback dan repeated Generate; verify save/load/duplicate melalui UI.
5. Ambil screenshot top-down/crossing/connectivity serta real video actual playback dengan watermark/statistik terbaca.

Jangan menutup gate visual sebelum bukti tersebut ada. Status/daftar evidence kosong tercatat di `documentation/m155/visual-status.json`. Tidak ada berkas video kosong atau screenshot substitusi.
''')
 write('M15_5_ACCEPTANCE_REPORT.md','Acceptance Report',f'''
## Keputusan

**M15.5 BELUM FULLY ACCEPTED. Backend execution/accounting/regression terverifikasi; GEOSPATIAL ACCEPTANCE PARTIAL; pending full causal attribution UNRESOLVED; browser visual/performance BLOCKED/PENDING.** Tidak memaksa PASS hanya karena request dapat dirutekan.

{table(['Gate','Status','Bukti / batas'],[
 ['Source / public map comparison','PARTIAL','1961 edge inventory,23 public map features, source-provenance overlay; no field calibration'],
 ['Proven geometry correction','NONE JUSTIFIED','No physical defect with sufficient correction evidence; frozen copy explicitly byte-identical'],
 ['No fictional road/flyover/illegal bypass','VERIFIED within artifacts','Identical network hash; zero topology/permission changes'],
 ['All road connections catalogued','VERIFIED model / PARTIAL physical','Inventory of existing connections; complete field OD/turn rules unknown'],
 ['Rail crossing function','MODEL EVIDENCE','863 stopped road samples;0 recorded steady-red entry/off-track; no building clearance proof'],
 ['3000/60min executed','VERIFIED','3000routed/loaded,1914departed,1346arrived,568active,1086pending'],
 ['Pending causal explanation','PARTIAL / UNRESOLVED','254 observed entry-space shortage;832 other insertion checks unresolved'],
 ['Fair controlled comparisons','VERIFIED model','Exact cohort equality, full requests/route/departure hash; no fictitious geometry improvement'],
 ['Mass balance / permissions / playback','VERIFIED sampled checks','8 independent XML/FCD audits PASS; no unexplained teleport/collision'],
 ['Manual/random and total/rate','VERIFIED backend','Determinism/ten-class failures/Save Load Duplicate API; UI still unverified'],
 ['Regression M01–M15 plus M15.5','PASS with one skip','395 run,394passed,1 legacy presentation-service skip'],
 ['TypeScript / isolated build','PASS','831KB JS warning remains; not a browser performance measurement'],
 ['Original preservation',protection['status'],str(protection['checked'])+' existing file hashes equal; no old artifact overwritten'],
 ['Visual inspector usability / real video','BLOCKED','Browser Use disabled in Work settings; no M15.5 UI evidence yet'],
 ['Visual quality / sustained performance','PENDING','Retained simplified renderer; FPS/loading/memory/session QA not measured']])}

## Hasil penting

3000road requests selama60min tidak berarti3000 kendaraan berangkat atau tiba. Setelah execution120min,454 belum masuk dan475 masih aktif. Green30:1483 arrived/970pending; no-trains:1342arrived/1084pending. Tidak ada angka yang dipromosikan menjadi kondisi/kapasitas historis Gedangan.

## Laporan dan evidence

- `M15_5_NETWORK_REALITY_AUDIT.md`
- `M15_5_NETWORK_CORRECTION_REPORT.md`
- `M15_5_APPROACH_CONNECTIVITY_REPORT.md`
- `M15_5_PENDING_INSERTION_ROOT_CAUSE.md`
- `M15_5_3000_VEHICLE_COMPARISON.md`
- `M15_5_RAIL_SIGNAL_NETWORK_REPORT.md`
- `M15_5_VISUAL_VERIFICATION.md`
- `M15_5_ACCEPTANCE_REPORT.md`

Evidence root `documentation/m155/`; actual runs `simulation/runs/m155/`; separate frontend `frontend/dist-m155`; frozen network `simulation/network/m155`. `artifact-manifest.json` memberi SHA256 source/build/report/derived evidence; tiap run memiliki input, source snapshots dan output manifest. Source snapshots mewakili code saat eksperimen, bukan disamakan secara keliru dengan semua editor code terbaru.

## Menjalankan staging

Gunakan `staging/m155/START_M155.ps1`, atau dari root `.venv/Scripts/python.exe -m backend.gedangan.m155_server --port 5201`, kemudian buka http://127.0.0.1:5201/. Server aktif saat laporan dibuat. Original M14/M15/M12 tetap terpisah. Tidak membuat final EXE, upload GitHub, menghapus workspace, atau memulai M16.

## Pekerjaan tersisa sebelum acceptance penuh

Aktifkan Browser Use dan jalankan checklist visual/performance, simpan screenshot/video M15.5 aktual; verifikasi nama/boundary/median/gate/track/clearance melalui sumber atau survei yang cukup; kumpulkan APILL dan OD/count resmi. Untuk832pending dengan gap proxy cukup, perlu instrumentasi insertion checks lebih rinci sebelum menyatakan penyebab selesai. Tidak ada izin menuju flyover/M16 yang disimpulkan dari laporan ini.
''')
 print('Eight M15.5 reports written; acceptance remains PARTIAL/BLOCKED.',flush=True)
if __name__=='__main__':main()
