# MILESTONE 05.1 — Railway Geometry & Spillback Causality

**Status keseluruhan: PARTIAL — NEEDS FIELD DATA. M06 tidak dimulai.**

## 1. Executive summary

Audit geometri selesai pada data sumber dan model; tidak ada dasar survei untuk mengesahkan posisi stop line atau clearance fisik. Jaringan M05.1 tetap byte-identical dengan M05, tanpa koreksi bentuk yang diada-adakan. Empat endpoint berubah sekitar 1.60 m dan tujuh lane shapes berubah hingga 7.178 m pada turunan M05, dengan perubahan internal/junction yang dijelaskan secara terpisah.

Causal detector diperbaiki untuk membaca actual vehicle-specific link priority/open/foe, spatial queue footprint, route/permissions, legal movement, durasi dan recovery. Pada 22 result sets M05 (20 replay baru dan2 validated evidence aliases), **37 vehicle-event episodes memenuhi definisi VERIFIED_SPILLBACK dalam simulasi**; 35 berasal dari replay independen. Tiga kontrol terisolasi dijalankan, dengan 1 positive-control event terverifikasi. Ini bukan jumlah lokasi fisik dan bukan bukti kemacetan aktual Gedangan. Seluruh 114 kandidat M05 pada 22 run mempunyai audit tersimpan; follower tanpa head-specific trace diklasifikasikan melalui posisi rekaman, bukan diberi priority trace fiktif. Kasus yang tidak memenuhi seluruh syarat tetap candidate/unresolved, tidak dipaksa menjadi verified.

Seluruh baseline M01–M05 tetap immutable. Ran 152 tests in 43.855s; 134 tes warisan tetap dipertahankan. Browser validation baru terpisah port 5180, viewer M05 port 5179 tetap tersedia. Native SUMO-GUI baru memperlihatkan kereta/crossing pada 105 s dan road release 130 s.

**SYNTHETIC TEST — NOT OBSERVED OR CALIBRATED GEDANGAN TRAFFIC.**

## 2. Snapshot dan sumber

Sebelum perubahan dibuat baseline-sha256.json untuk 5175 file dan baseline-source-snapshot.zip. baseline-complete.zip kemudian mengarsipkan seluruh entri manifest tersebut, termasuk raw data, toolchain, network dan run outputs; snapshot-manifest.json menyimpan hash arsip. Dependencies/cache/build yang dapat direkreasi (.venv,node_modules,__pycache__,dist) dikecualikan secara eksplisit. Original source outputs tidak ditimpa. Initial regression 134 tests lulus; log tersimpan.

Referensi aktual: rawOSM M02 snapshot2026-10-31T04:34:22Z, rail_tracks/level_crossings, M04.5inspection/access policy/registry, M03/M04.5/M05 reports, M05before-after audits, recorded FCD/control events/queue candidates dan SUMO1.28.0lokal. Source crossing859708050; road1240685448; main rail1330582009→562358494→1330582010; nearby1268453702adalah siding, tidak dioperasikan sebagai mainline. Bridge562358494tidak dijadikan road join berdasarkan proximity.

## 3. Metode geometri dan CRS

RawOSM4326 diproyeksikan dengan pyproj keEPSG:32749, lalu dikurangi originUTM M04.5 `[690790.3858550353, 9182879.516448068]`. Semua jarak berikut dalam meter. Perbandingan meliputi raw road, M04.5edge/lane, M05edge/lane, rel, internal connector dan junction envelope.

Endpoint displacement=Euclidean between corresponding ends; lane-shape displacement=Shapely Hausdorff symmetric; perubahan panjang=polyline length difference. Maksimum jarak ke reference way1240685448 adalah jarak sampel lane ke polyline referensi tersebut, bukan error survei. Angka untuk ruas dari way lain tidak diperlakukan sebagai deviasi centerline jalannya sendiri. Rail-road angle sumber menggunakan tangent node sebelum/sesudah shared node. Angle model menggunakan incoming lane/rail last segment. Connector heading kink dihitung pada tangent sambungan.

Tidak ada toleransi resmi/survei untuk memberi label aman. Ukuran footprint nominal memakai assumed train width2.8m dan modeled lane width; bukan swept path atau legal clearance.

## 4. Edge endpoint comparison

| Edge | Start displacement m | End displacement m | Hausdorff m |
|---|---:|---:|---:|
| w1240685448_s1_p1_0_f | 0.000 | 1.598 | 1.598 |
| w1240685448_s1_p1_0_r | 1.601 | 0.000 | 1.601 |
| w1240685448_s1_p2_0_f | 1.604 | 0.000 | 1.604 |
| w1240685448_s1_p2_0_r | 0.000 | 1.600 | 1.600 |

## 5. Lane shape comparison

| Lane | Before shape length m | After shape length m | Hausdorff m |
|---|---:|---:|---:|
| w1240685448_s1_p0_0_f_0 | 2.787 | 3.060 | 0.273 |
| w1240685448_s1_p0_0_r_0 | 2.683 | 2.952 | 0.268 |
| w1240685448_s1_p1_0_f_0 | 7.066 | 0.102 | 7.155 |
| w1240685448_s1_p1_0_r_0 | 7.097 | 0.100 | 7.178 |
| w1240685448_s1_p2_0_f_0 | 12.793 | 10.523 | 3.231 |
| w1240685448_s1_p2_0_r_0 | 12.793 | 10.199 | 3.278 |
| w160009748_s0_p0_0_f_0 | 338.210 | 338.615 | 0.404 |

Keempat edge endpoints disnap NETCONVERT ke existing shared node; source node tidak digeser. Tujuh lane shapes terkena trimming junction envelope, termasuk segmen di antara main crossing dan nearby siding/source crossing. Lajur terpendek menjadi sekitar0.10m pada representasi model; vehicle body dapat melintasi beberapa edge sekaligus. Ini keterbatasan representasi geometri/capacity, bukan bukti ruas fisik sepanjang0.10m atau clearance bus/trailer yang layak.

## 6. Crossing center, stop line dan alignment

Offset source center terhadap koordinat junction XML = **0.004571m**; selisih berada pada pembulatan XML, bukan toleransi fisik. Angle raw source = **58.732°**.

| Incoming road lane | Model stop-to-rail centerline m | Local model crossing angle | Status |
|---|---:|---:|---|
| w1240685448_s1_p1_0_f_0 | 6.898 | 73.029° | NEEDS FIELD VERIFICATION |
| w1240685448_s1_p2_0_r_0 | 2.936 | 65.104° | NEEDS FIELD VERIFICATION |

Stop line di sini hanya cross-section pada akhir incoming SUMO lane. Tidak tersedia koordinat stop marking/gate/barrier hasil survei. Jarak Euclidean tersebut tidak boleh dipromosikan menjadi jarak aman atau dasar izin kendaraan berat. Model nominal train-body margin tersimpan untuk diagnostik, bukan acceptance clearance.

| Movement | Incoming gap m | Outgoing gap m | Heading kink deg |
|---|---:|---:|---:|
| w1240685448_s1_p1_0_f_0 → w1240685448_s1_p2_0_f_0 | 0.000 | 0.000 | 1.909 |
| w1240685448_s1_p2_0_r_0 → w1240685448_s1_p1_0_r_0 | 0.000 | 0.000 | 2.777 |

## 7. Internal geometry, topology dan remediation decision

Internal IDs dapat diberi nomor ulang ketika railway connections ditambah. Membandingkan `:junction_1_0` berdasarkan ID saja dapat membandingkan road connector lama dengan rail connector baru. Audit **movement-keyed_connector_comparisons** mencocokkan tuple(from,to,fromLane,toLane) yang sama dan menyimpan old/new via IDs, shapes serta displacement. Added/retired internal IDs dan7junction shape/type changes dicatat lengkap di geometry.json. Source coordinates dipertahankan; access, oneway, frontage dan connection whitelist tetap sesuai baseline.

Kedua crossing road paths tersambung tanpa celah pada resolusi XML. Road connector memang berpotongan secara geometris dengan rel pada crossing at-grade; legal separation bersifat temporal melalui built-in rail_crossing. Menghapus persilangan geometris tersebut justru merusak topologi sumber. Tidak ada koneksi baru atau pergeseran source node untuk memperindah GUI.

**Remediation decision:** tidak melakukan perubahan koordinat tanpa bukti. simulation/network/m051 menyimpan execution copies byte-identical dengan M05 dan comparison-manifest.json. M5.1-A tetap **PARTIAL — NEEDS FIELD SURVEY**: ukur actual centerlines, stop markings/barrier positions, siding/main track footprint dan vehicle clearance/swept path sebelum pengesahan fisik. Tidak ada NETCONVERT baru yang mengklaim perbaikan geometri tanpa sumber; toolchain1.28.0digunakan untuk simulasi/fixtures, NETCONVERT log baseline tetap tersedia.

## 8. Causal model dan confounding

M05 memakai stopped head dekat lane end, downstream tail dan available signal. M05.1 menambah:

1. Actual `getNextLinks` untuk rute kendaraan yang bersangkutan: next lane/via, priority, opened, foe dan current link state; route serta lane permission dicocokkan dengan immutable network.
2. Actual FCD body footprints pada lane downstream. Queue harus merentang dari head≤10m dari lane end sampai tail rear≤5m dari entry, dengan gap antarbodi stopped vehicles≤10m. Satu kendaraan berhenti dekat entry pada lane yang masih kosong jauh ke hilir ditolak sebagai full-storage proof.
3. Entry free space dari rearmost body, dibandingkan panjang kendaraan+registry minGap untuk conservative blockage screening. Upstream harus lane head, berhenti<0.3m/s dan dalam10m dari akhir lane.
4. Local movement harus opened dan tanpa foe; connector blocker, invalid route/permission, red/yellow, dan konflik prioritas dipisahkan. **Red pada TLS yang lebih jauh tidak otomatis berarti local movement merah.** Controller diidentifikasi melalui actual current connection; red farther downstream dapat menjadi sumber queue yang merambat.
5. Bukti kondisi bertahan≥5s pada samples1s (simulation step0.5s). Ini continuous observed samples, bukan klaim setiap instant di antara samples. Full FCD safety terpisah diperiksa setiap0.5s.
6. Recovery harus menunjukkan free entry≥vehicle body length pada movement yang sama, legal dan foe-free sampai release, lalu actual discharge sample>1m/s pada original via connector/downstream lane dalam5s; creeping pada upstream lane tidak diterima sebagai recovery proof. Queue head dapat mulai mengurai sebelum storage entry tersedia; dissipation lag dicatat tanpa menolak recovery hanya karena shockwave memerlukan>5s. Bila kesempatan legal putus atau vehicle meninggalkan movement sebelum bukti space, status tidak dinaikkan menjadi verified.

Threshold di analysis-policy.json adalah definisi analisis sintetis, bukan toleransi geometri/clearance resmi. Posisi/trip/control adalah output actual SUMO; Raw occupancy TraCI disimpan sebagai nilai asli tanpa asumsi satuan persen. Occupancy percent tampilan adalah derived clipped union body coverage dari FCD front-assigned vehicles, dibagi panjang lajur; body dengan front di edge lain belum direkonstruksi. Ini dipisahkan dari actual raw value dan derived gap/duration/classification.

Kategori: SIGNAL_QUEUE, RAILWAY_QUEUE, PRIORITY_OR_FOE_QUEUE, BLOCKED_CONNECTOR, FOLLOWING_OR_APPROACH_QUEUE, STORAGE_BLOCKAGE_CANDIDATE, MULTI_CAUSAL_EVENT dan VERIFIED_SPILLBACK. Multiple factors dipertahankan sebagai context dan multi-causal bila control/foe dan storage sama-sama membatasi. Tidak memaksa satu root cause bila bukti tidak cukup. Upstream blocked count per event=1tracked head vehicle; overlapping episodes tidak boleh dijumlah sebagai jumlah unique sites atau total-delay tanpa deduplikasi.

## 9. Controlled experiments dan input parity

20Gedangan replays mencakup A_free/B_signal/C_single/E_combined/F_high_free/F_high_signal dan D_two/D_consecutive/D_long ×seeds42/43, ditambah H_close_block_control dan Strict seed42. G_e2 dan I_repro mempunyai validated aliases terhadap corresponding E_combined/C_single: original demand/tripinfo dan complete FCD attributes identik, sehingga tidak dihitung sebagai eksekusi independen tambahan. Horizon0–900s, warmup0, same vehicle registry/M04OD-derived demand, same immutable geometry; signal on/off dan train schedule adalah tested controls. Tidak ada speed/position override, vClass ignoring, atau forced insertion. Demand hashes, FCD vehicle attributes dan tripinfo sama dengan corresponding M05 runs.

Tiga isolated controls memakai geometri dan demand25cars yang sama, seed42, horizon350s. Positive_storage: upstream green/downstream red120s lalu release. Negative_free: keduanya green. Negative_signal: upstream red90s, downstream green. Network geometry/connections sama; program phase berbeda adalah intervensi eksplisit, bukan perbandingan dua geometri berbeda. C_single provides actual railway-only control; combined/high-demand memberi faktor berdekatan; recovery diuji pada positive control dan setiap verified event. Control data tidak dianggap pengukuran Gedangan. H memakai inherited block-control network; Strict memakai inherited limited network/OD. Keduanya tidak dipasangkan langsung dengan Provisional untuk klaim satu variabel. Controlled A/B/C/E/F pairs memakai network/demand/seed yang identik.

## 10. Positive dan negative controls

Positive_storage: **1VERIFIED_SPILLBACK**, full stopped queue duration **73.0s**, event47.5–120.5s; space available129.5s, discharge evidence130.5s. Downstream-head release mendahului entry-space recovery; lag dicatat pada recovery. Original M05positive fixture juga tetap lolos regression.

Negative_free:0verified spillback. Negative_signal:actual SIGNAL_QUEUE,0verified spillback. Negative tests juga menolak foe/red opportunity, invalid/full-storage evidence, serta lone stopped vehicle pada entry dengan storage belum penuh. Negative controls bukan sekadar flag keberhasilan.

## 11. Gedangan event results

| Run | Verified vehicle-events | Signal queue | Railway queue | Storage candidates | Other/unresolved episodes |
|---|---:|---:|---:|---:|---:|
| A_free_seed42 | 0 | 0 | 0 | 0 | 5 |
| A_free_seed43 | 2 | 0 | 0 | 1 | 6 |
| B_signal_seed42 | 2 | 32 | 0 | 11 | 12 |
| B_signal_seed43 | 1 | 31 | 0 | 11 | 13 |
| C_single_seed42 | 0 | 0 | 1 | 1 | 8 |
| C_single_seed43 | 2 | 0 | 1 | 2 | 7 |
| D_consecutive_seed42 | 0 | 0 | 2 | 2 | 6 |
| D_consecutive_seed43 | 1 | 0 | 2 | 4 | 9 |
| D_long_seed42 | 1 | 0 | 1 | 1 | 8 |
| D_long_seed43 | 0 | 0 | 1 | 3 | 8 |
| D_two_seed42 | 2 | 0 | 2 | 2 | 7 |
| D_two_seed43 | 0 | 0 | 2 | 4 | 9 |
| E_combined_seed42 | 2 | 30 | 1 | 10 | 14 |
| E_combined_seed43 | 2 | 30 | 1 | 11 | 16 |
| F_high_free_seed42 | 2 | 0 | 0 | 19 | 89 |
| F_high_free_seed43 | 4 | 0 | 0 | 11 | 70 |
| F_high_signal_seed42 | 9 | 65 | 0 | 46 | 259 |
| F_high_signal_seed43 | 3 | 56 | 0 | 31 | 176 |
| G_e2_instrumented | 2 | 30 | 1 | 10 | 14 |
| H_close_block_control | 1 | 0 | 1 | 1 | 7 |
| I_repro_single_seed42 | 0 | 0 | 1 | 1 | 8 |
| negative_free | 0 | 0 | 0 | 0 | 0 |
| negative_signal | 0 | 1 | 0 | 0 | 0 |
| positive_storage | 1 | 1 | 0 | 0 | 1 |
| strict_signal_seed42 | 1 | 24 | 0 | 6 | 7 |

Contoh model Gedangan: `A_free_seed43_36`, vehicle`road_47`, 460.5–480.5s, affected`w562358500_s16_p0_0_f → w562358500_s16_p1_0_f`. Downstream storage10.71m; current link opened/no foe sepanjang episode; queue spans modeled storage; space tersedia483.5s lalu kendaraan bergerak486.5s. Full evidence/control/root-context tersimpan, bukan disimpulkan dari berhenti saja.

**37verified episodes adalah hasil pada model, bukan validasi jaringan fisik Gedangan.** Very short edges/junction envelopes dan synthetic timing dapat mendominasi storage behavior; dua seed tidak mengkalibrasi kapasitas lapangan. Main corridor, connected feeder dan crossing dianalisis sepanjang rute yang benar-benar dilalui. Frontage tetap terpisah; ketiadaan trace pada ruas/OD yang tidak dilalui bukan bukti ruas bebas spillback.

## 12. Audit semua kandidat M05

Sebanyak114candidate dari22inherited result sets ditautkan ke priority trace timestamp/vehicle, joined spatial FCD evidence bila ada, current controller dan new causal event IDs. Tidak hanya contoh yang lolos dipilih. `m05-candidate-audit.json` menyimpan original candidate, matched trace, classification at original detection dan related episodes. Detection-time classification dapat tetap candidate walaupun suatu episode kemudian mempunyai recovery proof; kategori akhir episode terpisah. Sampel tunggal tanpa full spatial chain/event-duration evidence tidak dinyatakan verified. Inventory seluruh M05, jumlah matched priority samples dan positional follower evidence tercantum pada complete-m05-candidate-coverage.json. Kasus tanpa syarat kausal lengkap tetap unresolved, tidak dianggap negatif atau verified.

Unknown/route-or-permission cases, following queues, blocked connectors dan cases without recovery tetap unresolved/candidate. Tidak ada klaim spillback pada semua long queues. Verified status berlaku pada gerakan lane-specific, bukan seluruh kapasitas koridor atau proyeksi kebijakan lalu lintas.

## 13. Safety, crossing dan lifecycle

Actual replay safety audit: **2,814,465FCD vehicle samples** pada0.5s,0illegal lane samples,0road connector occupancy during closed crossing,0collisions dan0teleports. Semua demand lifecycle termasuk unserved/running disimpan dari private M05runner. Loaded count diambil dari final SUMO summary, agar initial preloaded vehicles tidak hilang dari event-set counter; requested = arrived + running + not departed diperiksa. Zero observed collision tidak membuktikan swept path/physical clearance antar samples. Bus/truck/trailer eligibility tetap Provisional M04.5assumptions; oversize tetap diblokir.

Original M03/M04.5/M05 network dan semua baseline files hash-checked. Tidak ada data sintetis ke observed_data. Tidak ada penambahan koneksi untuk membuat spillback.

## 14. Browser validation view

Halaman terpisah [M05.1Validation](http://127.0.0.1:5180/validation.html), viewerM05tetap port5179. Overlay roadM04.5/M05/raw, source rail, difference vectors, source center, model stop lines, nominal conflict region; numeric measurement table. Event inspector menampilkan time span, affected edges, head/tail/storage/occupancy, link priority/open/foe, gate state, cause, confidence, timeline dan recovery evidence. Semua diekspor dari actual outputs; tidak membuat event pengganti bila tidak ada event.

![Validation desktop](m051/browser-desktop.jpg)

![Validation mobile](m051/browser-mobile.jpg)

Browser QA desktop1920×1080/mobile390×844, layer toggles dan event/run selection; detail di browser-qa.json. Physical geometry status tetap NEEDS FIELD SURVEY meskipun rendering berhasil.

## 15. Native SUMO-GUI

SHOW_VALIDATION_SUMO_M051.bat dapat membuka ulang simulasi dengan folder output baru setiap sesi. SUMO-GUI bukti memakai actual M05.1 E_combined_seed42 configuration, seed42, output terpisah pada gui-session. Pada105s train berada di crossing;130s jalan dibuka kembali. Tampilan sama dengan baseline memang diharapkan karena tidak ada unsupported geometry remediation.

![Actual M05.1 SUMO-GUI105s](m051/sumo-gui-105.jpg)

![Actual M05.1 SUMO-GUI130s](m051/sumo-gui-130.jpg)

Sesi bukti dihentikan setelah capture130s; file GUI bukan sumber full-horizon lifecycle, yang berasal dari headless runs. Screenshot tidak mengesahkan clearance, legalitas kendaraan berat, jumlah physical tracks/gates atau siding operation.

## 16. Regression dan development findings

Initial134regression tests lulus. Final: **Ran 152 tests in 43.855s**, OK; semua134tests lama dipertahankan dan18tests M05.1ditambah. TypeScript dan production Vite build lulus; existing viewerM05tidak dibangun ulang.

Initial new-test failure dipertahankan di initial-new-tests-failure.txt: positive recovery ditolak oleh window yang terlalu sempit dari awal queue dissipation, dan FCD serialized-whitespace digest tidak stabil terhadap iterparse buffering. Perbaikan memisahkan dissipation lag dari post-space movement window serta memakai canonical step/vehicle attributes; semua actual A_free timestep/vehicle attributes memang identik. Tests tidak dihapus/dilonggarkan untuk mengabaikan physical state mismatch.

Installed SUMO1.28actual nextLinks tuple mengikuti lane-link field order meski vehicle Python docstring memberi urutan berbeda. Tracer menormalisasi observed tuple type; initial invalid diagnostic traces disimpan terpisah dan tidak digunakan untuk causal claims. Departure subscription dipasang pada setiap0.5sstep sebelum decimation ke1s. Correction logs menjelaskan temuan ini.

## 17. Reproducibility

Jaringan execution copies byte-identical M05; geometric comparison dapat diulang tanpa memodifikasi source.22demand hashes identik dengan corresponding M05; canonical FCD step/vehicle attributes dan tripinfo elements identik. Header execution paths, comments dan XML whitespace tidak dihitung; actual vehicle numeric/state attributes tetap lengkap. Classification dijalankan ulang dari saved traces dan identik secara hash; event order/IDs disortir deterministik. Sumber/config/run manifests, full priority traces, FCD, causal evidence dan audit hasil tersedia.

`REBUILD_VALIDATION_M051.bat` menjalankan geometry audit, isolated controls,20Gedangan replays +2 validated aliases, safety/repeat verification, publication, full tests, TypeScript dan validation Vite build. Bukan mengulang implementasi M05 atau memulai M06. Runtime dan GUI timestamps tidak dimasukkan ke deterministic physics equality.

## 18. Data yang masih hilang

Survei centerline jalan/rel, stop marking/gate/barrier positions, track/siding layout/clearance, legal heavy-vehicle clearance serta swept path. Tidak ada official geometric tolerance, actual traffic counts/demand calibration, signal timing/timetable aktual atau field causal congestion data. Geometry remains PARTIAL — NEEDS FIELD SURVEY; verified model spillback bukan verified physical Gedangan condition.

## 19. Acceptance satu per satu

| # | Criterion | Status |
|---:|---|---|
|1|Railway geometry audit selesai|PASS perhitungan/sumber; pengesahan fisik PARTIAL|
|2|Seluruh perubahan dapat dijelaskan|PASS; source-node snapping/junction trimming dan internal ID reassignment dicatat|
|3|Crossing topology valid|PASS secara model; no new road movements|
|4|Stop line dan continuity diperiksa|PARTIAL — stop line physical NEEDS SURVEY; numeric continuity checked|
|5|Causal positive control|PASS actual SUMO + recovery|
|6|Negative false-positive rejection|PASS free/signal controls dan negative predicates|
|7|Signal vs railway queue|PASS current-connection controller trace|
|8|Gedangan candidates analyzed|PASS seluruh114original candidate diaudit|
|9|Spillback status evidence-based|PASS in simulation; unresolved retained, no field claim|
|10|No unverifiable physical claim|PASS explicit NEEDS FIELD SURVEY|
|11|Internal browser audit|PASS desktop/mobile QA, actual exported data|
|12|SUMO-GUI|PASS new105/130s captures|
|13|All regression tests|PASS152including134inherited|
|14|M03–M05 source preserved|PASS entire baseline SHA verification|
|15|Reproducible results|PASS network/demand/physics attributes/event classification|

## 20. Rekomendasi dan batas M06

Remediasi detektor M05-SPILL-01 lolos kontrol kausal dan memberi bukti terverifikasi pada **model/cohort yang ditelusuri**. Jangan menutup seluruh register tanpa mempertahankan kasus unresolved dan positional-following evidence secara eksplisit. M05-GEO-01 telah terukur dan terdokumentasi tetapi belum memperoleh pengesahan fisik; jangan menutupnya sebagai FULLPASS. Kumpulkan survei stop line/crossing/track clearance dan validasi representasi short edges sebelum klaim fisik. Tidak mulai M06; keputusan lanjut tetap memerlukan persetujuan pengguna terhadap hasil M05.1.

## 21. Primary references dan artifact index

- [SUMO vehicle value retrieval](https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html) dan installed1.28.0traci source: position merupakan front-bumper center; actual tuple layout diverifikasi lewat runtime.
- [SUMO lane value retrieval](https://sumo.dlr.de/docs/TraCI/Lane_Value_Retrieval.html): actual lane occupancy, links dan priority/open/foe semantics. Open/foe data serta recorded connector occupants dipakai bersama, bukan open flag saja.
- geometry.json / geometry-overlay.json / simulation/network/m051/comparison-manifest.json.
- event-index.json / m05-candidate-audit.json / experiment-summary.json.
- setiap simulation/runs/m051: priority-trace, causal-events, run manifest, FCD, tripinfo, controls dan result.
- baseline-sha256, snapshot-manifest, reproducibility, safety, final-regression, browser-qa dan artifact-manifest di documentation/m051.
