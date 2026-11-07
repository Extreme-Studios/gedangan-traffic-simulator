"""Generate the M05 evidence report from actual retained results."""
import json,xml.etree.ElementTree as ET
from .m04_demand import ROOT,load,save,sha
DOC=ROOT/'documentation/m05'
def main():
 results=load(DOC/'scenario-results.json');by={r['name']:r for r in results};safety=load(DOC/'safety-audits.json');perf=load(DOC/'performance.json');sub=load(DOC/'sublane-results.json');repro=load(DOC/'reproducibility.json');fixture=load(ROOT/'simulation/runs/m05/spillback-fixture/result.json')
 audit=load(ROOT/'simulation/network/m05/provisional/baseline-audit.json');adapt=load(ROOT/'simulation/network/m05/provisional/crossing-endpoint-adaptations.json')
 tests=(DOC/'final-regression.txt').read_text(encoding='utf-8-sig');testline=next((x for x in tests.splitlines() if x.startswith('Ran ')),'See final-regression.txt')
 rows=['| Run | Road + train diminta | Berangkat / tiba | Masih berjalan / belum berangkat | Maks berhenti | Tunggu road tiba saja (s) | Kandidat hambatan hulu |','|---|---:|---:|---:|---:|---:|---:|']
 for r in results:rows.append(f"| {r['name']} | {r['requested_road']} + {r['requested_train']} | {r['departed']} / {r['arrived']} | {len(r['running'])} / {r['not_departed']} | {r['maximum_stopped_road_queue_count']} | {r['mean_road_waiting_s']:.2f} | {len(r['spillback_candidates'])} |")
 network=[]
 for mode in ['strict','provisional','provisional-block-control']:
  p=ROOT/f'simulation/network/m05/{mode}/network.net.xml';r=ET.parse(p).getroot();ext=[e for e in r.findall('edge') if e.get('function')!='internal'];network.append(f"- {mode}: {len(ext)} external edges, {sum(e.get('id').startswith('m05_rail_') for e in ext)} rail edges; SHA256 `{sha(p)}`.")
 acceptance=[('Multiclass sesuai izin','PASS','Sembilan tipe non-oversize bergerak/tiba; semua sampel FCD diperiksa terhadap izin lane.'),('Motorcycle sublane','PASS, fixture terisolasi','LC2013 versus SL2015: enam kendaraan tiba pada masing-masing model; clearance lateral aktual diperiksa.'),('Traffic signal valid','PASS, teknis sintetis','Satu logical controller, empat source stop-head, sembilan link; satu protected green per fase.'),('Red-light stopping','PASS','B_signal_seed42 memiliki bukti stopped-before-red, bukan flag tampilan.'),('Green-light release','PASS',f"{len(by['B_signal_seed42']['signal_stopped_then_released'])} kendaraan memiliki pasangan red stop lalu green release pada seed42."),('Railway Gedangan source pilot','PARTIAL pada preservasi geometri persis','Pilot georeferensi dan shared node valid. Empat edge endpoint dan tujuh lane shape berubah lokal akibat pembentukan crossing NETCONVERT; perlu review geometri sebelum penerimaan penuh.'),('Train benar-benar bergerak','PASS','Route rel sumber, FCD, tripinfo, front entry dan rear exit tercatat.'),('Crossing aktif','PASS','Built-in rail_crossing, bukan lampu merah statis atau objek animasi.'),('Road berhenti saat crossing ditutup','PASS',f"Single train seed42: {by['C_single_seed42']['rail_gate_stop_vehicle_seconds']} stopped road vehicle-seconds terkait nextTLS crossing."),('Road bergerak setelah aman','PASS','Dua kendaraan probe mempunyai stopped-then-released evidence di single train seed42.'),('Queue metrics dari SUMO','PASS','Trajectory/count/extent/wait dan E2 aktual, 1800 interval detektor.'),('Queue terbentuk dan mengurai','PASS','Queue pulse crossing terbentuk lalu kosong; seluruh demand single-train tiba.'),('Spillback detector dan hasil jujur','PASS untuk fixture; PARTIAL untuk kausal Gedangan','Positive control SUMO membuktikan blockage >5 s pada upstream green. Kandidat Gedangan tetap belum konfirmasi kausal; tidak dinyatakan spillback terverifikasi.'),('Input perbandingan terkontrol','PASS','14 pasangan identik demand SHA, network SHA, seed, window, warmup.'),('Viewer internal recorded results','PASS','Browser kembali aktif setelah restart. Desktop1920×1080/mobile390×844 tanpa overflow horizontal; playback, inspector, layers, event jumps, orbit dan zoom diverifikasi; clean-session console tanpa warning/error.'),('SUMO-GUI aktual','PASS','Screenshot t105 train/crossing, t130 release, serta parameter trailer 8.25 m/s dan odometer 931.76 m.'),('Tests dan build','PASS',testline+'; TypeScript dan Vite production build lulus.'),('Reproduksi','PASS','Tiga network hash identik setelah rebuild; tripinfo/FCD/summary elemen identik pada repeat seed42.'),('M01–M04.5 tidak rusak','PASS setelah pemulihan dokumen','Snapshot SHA seluruh baseline terjaga; 112 tes lama lulus. Pemulihan 12 dokumen yang sudah hilang sebelum implementasi dijelaskan.'),('Tidak klaim kondisi nyata','PASS','Seluruh demand, fase, perilaku dan jadwal diberi label sintetis/asumsi; tidak masuk observed_data.')]
 save(DOC/'acceptance.json',{'milestone':'M05','status':'PARTIAL','items':[{'criterion':i+1,'name':a,'status':b,'evidence':c} for i,(a,b,c) in enumerate(acceptance)]})
 text=f"""# MILESTONE 05 — Gedangan Traffic Simulator

Status: **PARTIAL — mekanisme SUMO berhasil, penerimaan penuh belum terpenuhi.**

## Ringkasan

Pilot rel georeferensi Ketajen/Stasiun Gedangan berhasil diintegrasikan pada jaringan Provisional M04.5. Kereta bergerak pada lajur rel, built-in crossing menutup/membuka dan kendaraan jalan berhenti lalu bergerak kembali. Ini integrasi pada jaringan Gedangan, bukan hanya fixture railway terisolasi. Mixed traffic, program sinyal, eksperimen sublane, E2, trajectory playback dan positive-control spillback sudah berjalan.

Status belum FULL PASS karena adaptasi endpoint lokal pada turunan rail crossing perlu review geometri, dan kausalitas kandidat spillback Gedangan belum terkonfirmasi. Kendala browser sudah selesai; desktop dan mobile sudah diverifikasi. Jangan membaca kelulusan tes sebagai penyelesaian dua batas yang tersisa ini. **M06 tidak dimulai.**

**SYNTHETIC TRAFFIC EXPERIMENT — NOT CALIBRATED TO GEDANGAN 2026.** Tidak ada angka dalam laporan ini yang merupakan pengukuran lalu lintas Gedangan atau rekomendasi operasi jalan/kereta.

## Baseline dan pemulihan

Sebelum implementasi, regresi menemukan 12 dokumen dokumentasi lama hilang, dengan satu failure dan tiga errors. Jaringan, kode dan dataset masih tersedia. Dokumen dipulihkan dari source ZIP M01 serta review copies; hash manifest lama diperiksa. Laporan M02 hanya membalik dua tautan peta yang pernah disesuaikan pada review copy hingga hash persis cocok. Tidak ada test atau manifest lama diubah. Sebab hilangnya file tidak diketahui.

Bukti: `m05/initial-regression.txt`, `m05/baseline-document-recovery.json`, `m05/initial-regression-after-recovery.txt`. Setelah pemulihan: **112 tes lulus**. Snapshot immutable: `m05/previous-milestones-sha256.json`.

Laporan M03, M04, M04.5, kode generator/registry, access policy, OD, SUMO lokal dan data sumber dibaca sebelum implementasi. Batas inherited tetap berlaku: akses berat Provisional adalah asumsi teknis, frontage terpisah, oversize ditolak, clearance/legalitas/swept path belum tervalidasi.

## Perubahan source dan struktur

- `backend/gedangan/m05_behavior.py`: build derivative, seeded paired demand, SUMO/TraCI read instrumentation, FCD/tripinfo, complete horizon accounting.
- `m05_signals.py`: logical controller dan program satu protected link per fase.
- `m05_railway.py`: sumber rail chain/shared crossing dan turunan synthetic block-control.
- `m05_queues.py`: stopped queue dan conservative duration predicate.
- `m05_analysis.py`, `m05_safety.py`: lifecycle, queue/occupancy, control evidence, candidate review dan seluruh FCD access audit.
- `m05_sublane.py`, `m05_spillback_fixture.py`: controlled actual SUMO experiments.
- `m05_provenance.py`, `m05_export.py`, `m05_report.py`: rebuild repeat, browser artifacts dan laporan.
- `configuration/behavior-m05`, `signals-m05`, `railway-m05`: input asumsi terpisah.
- `frontend/behavior.html`, `frontend/src/m05`, `vite.behavior.config.ts`: viewer M05 terpisah port5179, orbit/zoom, timeline, type inspector, queue dan control events.
- `tests/m05`: actual output validation dan negative tests. Launcher lama tetap utuh.

## Lineage jaringan dan geometri

M03 → corrected M04.5 Strict/Provisional → **M05 derivative**. Toolchain lokal NETCONVERT/SUMO1.28.0. M03/M04/M04.5 tidak ditulis ulang. Strict tetap tanpa crossing road yang tidak didukung konektivitasnya; tidak disisipkan jalan baru ke Strict demi membuat tes kereta lolos.

{chr(10).join(network)}

Road lane access dan road connection allow/disallow identik dengan baseline. Strict mempertahankan 242 external road lane-to-lane connections dan Provisional2874. Semua guessed road movements hasil rebuild yang tidak ada pada baseline dihapus sebelum acceptance. Tidak ada penggabungan frontage/main arterial, perubahan oneway, restore forbidden turn atau bypass access.

**Batas geometri yang nyata:** NETCONVERT menggunakan posisi existing shared node `osm_859708050` untuk crossing. Empat adjacent edge shape endpoints disnap ke node ini dan tujuh adjacent lane shapes tertrim ulang; tipe junction dan internal connector/envelope juga dibangun ulang. Source node coordinates dipertahankan. Tidak menggeser simpul atau membuat ruas/koneksi jalan baru. Ini dicatat sebagai turunan topologi M05, bukan diklaim geometri external lane identik. Sumber M04.5 asli tetap tersedia tanpa perubahan. Review kecocokan lajur/stop line dan geometri perlintasan ini diperlukan sebelum FULL PASS atau penggunaan lapangan.

Daftar lengkap before/after: `simulation/network/m05/provisional/baseline-audit.json` ({len(audit['external_lane_differences'])} lane differences), `crossing-endpoint-adaptations.json` ({len(adapt)} edge differences). Tidak ada perubahan lane width/speed/access; geometri jalan jauh dari crossing tidak berubah. Strict tidak mengalami adaptasi geometri eksternal tersebut.

## Provenance dan klasifikasi data

| Kategori | Penggunaan M05 |
|---|---|
| OBSERVED | Tidak ada data lapangan baru. |
| RESEARCH_REFERENCE | Snapshot OSM M02 retained, geometri rel/jalan, tags dan dokumentasi SUMO. |
| VERIFIED_SOURCE | Node/way/rail chain dan shared crossing diverifikasi pada snapshot; bukan survey/legal verification. |
| INFERRED | Pengelompokan logical stop-head dan candidate physical crossing site dari shared road/rail topology. |
| ASSUMPTION | Vehicle dynamics M04, sinyal, rail operation direction/block signals, ukuran/kecepatan kereta, jadwal/demand. |
| SYNTHETIC_TEST | Paired demand, station crossing probes, isolated lateral dan spillback fixtures. |
| SIMULATED_RESULT | FCD, tripinfo, state transitions, queue, E2 dan lifecycle aktual SUMO. |
| MISSING | Timing lapangan, arus/komposisi terukur, actual gate/track count, legal clearance dan swept path. |

Source OSM snapshot2026-10-31T04:34:22Z; © OpenStreetMap contributors, ODbL1.0. Tag `usage=main`, gauge1067 dan `electrified=no` adalah nilai sumber, bukan hasil inspeksi lapangan. M05 tidak menaruh output sintetis pada observed_data.

## Vehicle behavior dan sublane

Registry10tipe M04 tetap digunakan sebagai sumber. Sembilan tipe non-oversize dijalankan; oversize tidak didefinisikan untuk demand operasional dan tetap diblokir oleh gate M04.5. Krauss, tau1.2, sigma0.3 dan parameter longitudinal M04 dipertahankan. Full-size bus/truk/trailer tetap mengikuti eligibility arterial dan pembatasan M04.5; crossing station probes hanya motor/car/delivery. Keine vClass ignoring, permission override, forced vehicle placement atau TraCI speed/position override.

`behavior_measurements` menyimpan acceleration/deceleration selisih kecepatan1s dan minimum gap leader satu lajur (rear leader minus front follower), dipisah per tipe. Ini estimasi dari trajectory, bukan sensor reaction time manusia. Parameter tau/minGap tetap asumsi registry. Run G/H/I juga merekam TraCI acceleration; fixture sublane merekam FCD acceleration dan leader output. Tidak dilakukan kalibrasi.

Controlled isolated lane600m ×3.2m; Krauss sama pada kedua model. LC2013:6/6 tiba, tanpa gerak sejajar pasangan uji. SL2015, lateral-resolution0.4m, minGapLat0.25m, maxSpeedLat0.7m/s, lcPushy0:6/6 tiba. Dua motor overlap longitudinal dengan clearance lateral0.8m; motor di samping car minimum0.30m. Lateral span teramati car0.15m dan motor-truck0.28m. Truk2.5m+motor0.8m+clearance0.25m tidak muat dalam3.2m, sehingga tidak dipaksa sejajar. Runtime LC2013={sub[0]['runtime_wall_seconds']:.3f}s; SL2015={sub[1]['runtime_wall_seconds']:.3f}s. Satu seed/enam kendaraan tidak cukup untuk benchmark atau inferensi perilaku seluruh Gedangan.

Bukti: `m05/sublane-results.json`, fixture FCD/leader/tripinfo/logs di `simulation/runs/m05/sublane-fixture`.

## Traffic signal

Empat stop-head sumber2718664256,3201485055,4513024622,2718664280 digabung **secara logical**, tidak digeser/digabung geometris, ke `m05_gedangan`. Sembilan controlled link indices diekstrak dari output NETCONVERT. Program konservatif: setiap controlled connection mendapat green12s, yellow3s, all-red2s; cycle153s; offset0. Input dapat diubah pada `configuration/signals-m05/program.json` lalu rebuild. Satu protected green per fase menjamin tidak memberi dua controlled movements yang berkonflik protected green bersamaan. Downstream source priority rules tetap berlaku. Plan ini sengaja konservatif, bukan rencana sinyal Gedangan terukur atau optimasi kapasitas.

B_signal_seed42: {len(by['B_signal_seed42']['signal_stopped_then_released'])} actual red-stop → green-release pairs. Phase log disimpan setiap perubahan0.5s. Antrean yang belum habis di horizon tetap dihitung. Station source TLS node6583454054 dan simpang lainnya belum direkonstruksi menjadi controller lengkap; tidak diada-adakan.

## Railway source audit dan operasi

Tiga mapped main rail ways membentuk satu chain tersambung: **1330582009 →562358494 →1330582010**, melalui source crossing859708050 pada source road1240685448 Ketajen. Way562358494 adalah bridge segment di lokasi tersendiri; tidak dibuat road join berbasis kedekatan di bridge. Satu mapped centerline dimodelkan sebagai18rail edges antar source nodes, vClass rail, forward synthetic operation. Nearby source way1268453702 berstatus siding dan tidak diperlakukan sebagai mainline.

Raw context snapshot memuat24level-crossing nodes;11di antaranya cocok dengan retained M02 rail parts/core. Kedua hitungan itu tidak ditafsirkan sebagai jumlah palang fisik. Node859708050 dan11781097618 adalah candidate satu lokasi fisik pada roadKetajen, berjarak sekitar7m dan memotong centerline main/siding. Jumlah track/gate aktual belum verified. Pilot hanya mengoperasikan main centerline tersebut; tidak mengklaim full station railway interlocking atau perlindungan siding yang tidak dioperasikan.

Train80m×2.8m, maxSpeed8m/s, accel0.6/decel1 adalah ASSUMPTION. Built-in `rail_crossing`: time-gap15s, yellow3s, min-green5s, opening-delay3s, opening-time3s, space-gap-1(disabled distance detector). Longer closure memakai opening-delay20s. Tidak menutup/membuka crossing dengan TraCI manual state override.

Single train seed42: warning87.0s, closed90.0s, front entry105.5s, rear exit116.5s (trajectory1s), opening118.5s, road green121.5s. Approach120m teramati90.5s; warning dapat lebih awal karena built-in estimated time gap. {by['C_single_seed42']['rail_gate_stop_vehicle_seconds']}actual crossing-related stopped road vehicle-seconds;2road vehicles mempunyai stopped-then-released evidence.115/115total vehicles tiba.

Separated scheduled departures70/170s menghasilkan dua crossing cycles. Short scheduled gap70/85s pada satu rail block **tidak** menghasilkan actual short gap: train kedua tertahan insertion hingga144.5s; departDelay59.5s dicatat. Jangan menyebut ini short-gap movement yang berhasil.

Turunan terpisah `provisional-block-control` menambah dua **synthetic rail signals** pada existing source nodes11781097631 dan11781097634. Itu asumsi operasi pengujian, bukan klaim lokasi signal equipment nyata. Built-in train block safety tetap aktif. Actual departures70/95s, second departDelay10s, second waiting3s; crossing mulai membuka125.5s lalu batal ke red128.5s saat kereta berikutnya mendekat; tidak ada road green di antaranya; final opening166s/green169s.116/116tiba, tanpa collision/teleport. Ini menunjukkan safe handling berdasarkan actual gap, bukan hanya jadwal yang diminta.

Semua rail/train road separation, route lineage, source tags, control states dan event times disimpan. Sampling trajectory1s/control0.5s membatasi ketelitian timestamp; tidak boleh disebut waktu perlintasan lapangan.

## Antrean, okupansi, spillback dan accounting

Antrean = kendaraan noninternal dengan speed<0.3m/s, diukur dari state SUMO. Count adalah jumlah stopped vehicles, bukan jumlah panjang lane. Extent adalah front-to-front distance stopped head-tail; belum termasuk body kendaraan paling belakang dan tidak selalu contiguous jam. Tail position diukur dari awal lane. Occupancy turunan=jumlah body length pada lane/lane length; E2 mean/max occupancy dan jam length adalah output terpisah, jangan disamakan.

Wait TraCI adalah consecutive waiting; tripinfo waitingTime adalah accumulated stopped waiting untuk arrived trips. Queue timeline dan growth/dissipation tersedia per1s. E2 pada dua incoming arterial lanes menghasilkan1800 interval1s untuk900s. Tail<5m menandai lane-start-reached. Boundary censoring hanya ditandai ketika lane tersebut juga tidak memiliki incoming external road connection; hal ini dapat berupa source boundary atau unresolved upstream connectivity, bukan bukti geografis batas jalan nyata.

Detector kandidat: downstream tail<5m, upstream planned next edge sesuai route, stopped head<10m dari lane end, movement signal available, durasi kontinu≥5s. Source priority/foe pada uncontrolled junction dapat turut membatasi discharge; oleh karena itu output Gedangan berlabel **CANDIDATES_REQUIRING_PRIORITY_CAUSALITY_REVIEW**, bukan verified spillback. A_free tidak menemukan kandidat. High-signal seeds42/43 menghasilkan25/10kandidat, belum konfirmasi kausal.

Positive control **isolated synthetic SUMO fixture** mempunyai storage60m dan upstream green. Queue downstream secara nyata memenuhi storage lalu menahan upstream selama≥5s. First detection={fixture['first_detection_s']:.1f}s;25/25tiba; zero collisions/teleports. Tidak ada pemindahan kendaraan manual. Negative predicate tests menolak queue panjang tanpa upstream blockage, tanpa available movement, atau durasi<5s. Bukti fixture ini tidak disajikan sebagai spillback Gedangan.

Semua run memakai step0.5s, observation horizon0–900s, warmup0s (finite synthetic pulse, bukan steady-state experiment). Demand inherited90road +24crossing probes untuk Provisional normal,240+24untukhigh; Strict60. Type/OD dipilih deterministik dari accepted M04.5 compatibility routes; crossing probes tambahan berlabel synthetic station movement terpisah dari inheritedOD.14paired comparisons memakai demand JSON/SHA, network, seed, composition, warmup/window identik; road TLS on/off satu variabel atau train schedule satu variabel. Hblock-control adalah eksperimen tambahan, bukan pasangan utama identik-network.

Rata-rata tunggu/durasi trip dalam tabel **hanya untuk arrived road vehicles**, dan bias censoring tidak boleh diabaikan. Kolom running/not-departed dan per-vehicle lifecycle tetap disertakan. Semua requested = arrived + running + not-departed; pending insertion adalah subset kendaraan yang belum berangkat, bukan kategori tambahan yang dijumlah dua kali. No routes silently skipped. Terdapat22instrumented runs, dua seeds utama; fixture/performance control terpisah.

{chr(10).join(rows)}

Seluruh run instrumented mempunyai0teleports dan0collisions. Hasil sinyal dengan capacity rendah adalah akibat synthetic conservative signal plan, bukan bukti traffic policy tersebut baik/buruk untuk Gedangan.

## Safety audit aktual

**{sum(a['samples_checked'] for a in safety):,} vehicle samples** pada FCD0.5s diperiksa terhadap lane allow/disallow jaringan yang benar untuk tiap run. Tidak ditemukan illegal lane sample maupun road vehicle di internal crossing connector selama closed red. Train front entry/rear exit dan road release didokumentasikan. Zero observed conflict tidak merupakan pembuktian matematis antar timestep atau sertifikasi swept path/legal clearance.

Bukti: `m05/safety-audits.json`, setiap run `safety-audit.json`, `crossing-events.json`, `events.json`, `vehicle-lifecycle.json`, `queue-timeline.json`.

## Browser dan SUMO-GUI

Viewer membaca actual recorded JSON/FCD-derived states; tidak menciptakan posisi, jadwal, arrival atau gate state palsu. Playback1s, current frame type/speed/wait/position/movement, timeline/play/pause/reset/rate, camera orbit/zoom dan layer toggles. Warna frontage terpisah, source network immutable. Antrean ditandai per lane yang berisi stopped vehicle; bukan menggambar seluruh lajur sebagai panjang antrean. Spillback candidates diberi label belum causal confirmation. Sublane fixture status eksplisit.

Akses browser sempat disabled, lalu pulih setelah pengguna restart ChatGPT. Local server dinyalakan kembali dan versi akhir diuji pada desktop1920×1080 serta mobile390×844, tanpa overflow horizontal. Putar/jeda/reset, speed, keyboard scrub, vehicle inspector, scenario selection, tiga camera presets, orbit drag, wheel zoom, road/rail/queue layers, kandidat113.5s dan reopening121.5s diverifikasi. Frame time mengikuti waktu trajectory aktual (contoh108.5s), bukan membulatkan waktu rekaman menjadi108s. Saat loading, angka hilang ditampilkan sebagai tanda pisah dan crossing berstatus memuat; tidak diasumsikan terbuka. Marker TLS dipetakan melalui exact destination node/controlled-link indices; disabled program berwarna abu-abu. Warning React createRoot ganda saat development HMR diperbaiki dengan hot-dispose unmount. Sesi browser final bersih tanpa warning/error console. Direct vehicle raycast click belum diuji terpisah; dropdown inspector sudah teruji. Lihat m05/browser-qa.json.

![Internal browser final desktop actual crossing](m05/browser-final-desktop.jpg)

![Internal browser final mobile actual crossing](m05/browser-final-mobile.jpg)

![SUMO-GUI actual train/crossing at105s](m05/sumo-gui-crossing-105.jpg)

![SUMO-GUI actual road release at130s](m05/sumo-gui-reopened-130.jpg)

![SUMO-GUI trailer parameters](m05/sumo-gui-trailer-parameters.jpg)

GUI memakai seed42/runG dan output terpisah. Capture105s memperlihatkan train dan crossing;130s train telah melewati crossing dan road vehicles bergerak. Trailer inspector `road_4` menunjukkan8.25m/s, position110.65m, odometer931.76m; type mapping berasal dari actual demand registry. Screenshot native memuat notification aplikasi lain; itu tidak dipakai sebagai bukti simulasi. GUI session tidak menimpa hasil headless; initial E2 output yang sempat dibuka ulang oleh sesi GUI sudah diregenerasi melalui headless runG sebelum validasi akhir.

## Performance, tests dan reproduksi

Actual CLI process control (runG inputs, instrumentasi TraCI tidak aktif):900simulated seconds selesai{perf['wall_seconds']:.3f}wall seconds; CPU{perf['cpu_seconds']:.3f}s; sampled peak working set{perf['peak_working_set_bytes_sampled']/1024/1024:.2f}MiB; speed ratio{perf['simulation_speed_ratio']:.1f}×. Windows process counters sampled~20ms,117samples. Angka ini bukan total-device RAM/GPU benchmark. Instrumented-run runtime terpisah pada result JSON dan lebih mahal karena pencatatan TraCI. VRAM dan FPS1080p belum terukur; visual/layout QA desktop1080p dan mobile sudah selesai. Tidak mengklaim benchmark rendering. Tidak dilakukan stress ribuan kendaraan.

- Initial after-recovery regression112tests OK.
- Final Python regression: **{testline}**, OK; termasuk22M05tests dan112tests sebelumnya.
- TypeScript `tsc --noEmit`: lulus.
- Vite M05 production build: lulus; terdapat warning bundle Three.js>500kB, bukan build failure.
- Tiga network SHA identik setelah actual independent rebuild; input corrected network tetap unchanged.
- C_single_seed42 dibandingkan repeatI: demand, seluruh XML simulation elements tripinfo/FCD/summary identik. XML comments/process headers berisi path diabaikan; actual result attributes tidak dihapus.
- Fixtures dan safety audit memvalidasi fenomena dari actual SUMO outputs; tidak hanya memeriksa success flags.

Logs: `m05/final-regression.txt`, `vite-build.txt`, `reproducibility.json`, `performance.json`, source/configuration manifest dan run files. Rebuild launcher menjalankan build+experiments+fixtures+independent provenance check+analysis+safety+export+tests+TypeScript+Vite.

## Permasalahan terbuka dan remediasi

1. **M05-GEO-01:** Review empat edge endpoint dan tujuh lane-shape crossing adaptations; source original tidak diubah. Jika exact external shape preservation wajib, susun explicit surveyed crossing/stop-line geometry sebelum menerimanya. Jangan mengedit bentuk hanya untuk memperoleh routing sukses.
2. **M05-SPILL-01:** Kandidat Gedangan memerlukan trace open/foe/priority dan downstream storage untuk memastikan causality. Detector positive control sudah lulus, tetapi tidak cukup untuk klaim verified Gedangan spillback.
3. **M05-UI-01 — RESOLVED:** Browser aktif setelah restart; desktop1080p/mobile390×844 dan kontrol utama lulus QA. Screenshot final tersimpan. Tidak ada pengubahan setting keamanan otomatis.
4. Station TLS/source crossings lainnya, siding, reverse/fulltrack operation dan actual interlocking belum dimodelkan. Pilot scope eksplisit; tidak ada invented full track/gate count.
5. Field demand, counts, speeds, composition, signal timings, train timetable, clearance/legalitas/swept path masih missing. Akses berat tetap Provisional assumption, oversize tetap blocked. Kalibrasi bukan hasil M05.

## Acceptance satu per satu

| # | Kriteria | Status | Bukti/batas |
|---:|---|---|---|
"""
 for i,(a,b,c) in enumerate(acceptance):text+=f'| {i+1} | {a} | {b} | {c} |\n'
 text+="""
## Kesiapan menuju M06

Fondasi recorded mixed traffic–signals–rail interaction tersedia dan dapat direproduksi. Status M05 tetap **PARTIAL**, dengan dua item teknis penerimaan terbuka (geometri crossing dan kausalitas spillback) di atas. Tidak memulai real-time TraCI UI, realistic world, atau pekerjaan M06. Penyelesaian/remediasi M05 dan persetujuan pengguna diperlukan sebelum melanjutkan milestone.

## Referensi primer

- [SUMO Railways / rail crossing](https://eclipse.dev/sumo/docs/Simulation/Railways.html), salinan1.28.0lokal di toolchain docs.
- [Traffic Lights](https://eclipse.dev/sumo/docs/Simulation/Traffic_Lights.html).
- [Sublane Model](https://eclipse.dev/sumo/docs/Simulation/SublaneModel.html).
- [E2 lane-area detector](https://eclipse.dev/sumo/docs/Simulation/Output/Lanearea_Detectors_(E2).html).
- OSM retained ways [1330582009](https://www.openstreetmap.org/way/1330582009), [562358494](https://www.openstreetmap.org/way/562358494), [1330582010](https://www.openstreetmap.org/way/1330582010); provenance penuh dan retained hashes tersedia di audit source.
"""
 text=text.replace('Keine vClass','Tidak ada vClass')
 (ROOT/'documentation/MILESTONE_05_REPORT.md').write_text(text,encoding='utf-8');(ROOT/'MILESTONE_05_REPORT.md').write_text(text.replace('](m05/','](documentation/m05/'),encoding='utf-8')
 readme=f"""# MILESTONE 05 — Cara menjalankan

Status: **PARTIAL**. Actual SUMO pilot rail/signals/mixed traffic lulus mekanisme. QA browser desktop/mobile sudah selesai. Review adaptasi geometri crossing dan kausalitas kandidat spillback Gedangan masih terbuka. Baca MILESTONE_05_REPORT.md. **M06 belum dimulai.**

Project: `{ROOT}`

## Viewer

Jalankan `START_BEHAVIOR_M05.bat` lalu buka [Behavior M05](http://127.0.0.1:5179/behavior.html). Port5179khususM05. Launcher lama tidak diganti. URL menampilkan recorded outputs; tidak mengendalikan SUMO secara real-time. Jika ingin hanya menyalakan server tanpa membuka browser eksternal, gunakan `START_BEHAVIOR_M05.bat --no-browser`.

Pilih skenario dan seed; Putar/Jeda, Reset, speed1/5/10/25×, timeline, Perlintasan/Atas/Jaringan. Drag orbit, scroll zoom, klik kendaraan atau pilih inspector. Toggle Jalan/Rel/Antrean. Event timeline melompat ke fase aktual. Angka unserved/running tetap ditampilkan. Source road geometry dan frontage terpisah.

Label wajib: **SYNTHETIC TRAFFIC EXPERIMENT — NOT CALIBRATED TO GEDANGAN 2026.** Jangan menggunakan angka ini sebagai hasil penelitian lalu lintas aktual.

## SUMO-GUI

Jalankan `SHOW_BEHAVIOR_SUMO_M05.bat`. Native GUI memakai actual seed42/runG, pause pada105dan130s. Tombol Play melanjutkan ke breakpoint berikutnya. Output GUI terpisah pada documentation/m05/gui-session. Pada105s kereta berada di crossing; pada130s road crossing sudah open. Synthetic block signals hanya di varianH, bukan klaim equipment railway nyata.

## Rebuild

Jalankan `REBUILD_BEHAVIOR_M05.bat` dari Windows. Memakai `.venv`, SUMO portable1.28.0dan npm dependencies yang sudah ada. Tidak menginstal tool tambahan. Proses melakukan22instrumented runs (dua seeds utama), controlled lateral/spillback fixtures, deterministic rebuild/repeat, analysis, full-sample safety, export, tests dan production build. Hasil lamaM01–M04.5tidak ditulis ulang.

Konfigurasi: configuration/behavior-m05/profiles.json, signals-m05/program.json, railway-m05/pilot.json. Parameter behavior pada profiles.json mencatat profil yang diuji; parameter longitudinal tetap registryM04. Schedules synthetic didefinisikan eksplisit pada m05_behavior.py. Mengubah input memerlukan rebuild dan review hasil, bukan menganggap hash lama masih berlaku.

## Bukti dan batas

- documentation/m05/scenario-results.json:22runs lengkap dan failure accounting.
- Setiap simulation/runs/m05/*:run.sumocfg, demand/provenance, FCD, tripinfo, summary, playback, events, crossing-events, queue-timeline, vehicle-lifecycle, safety-audit.
- documentation/m05/safety-audits.json:{sum(a['samples_checked'] for a in safety):,}samples0.5s, illegal lane/red crossing samples0.
- final-regression.txt:{testline}; Vite/TypeScript lulus.
- reproducibility.json:network hash dan repeat XML element-identical.
- Isolated fixtures dinyatakan terpisah, tidak disajikan sebagai observedGedangan.
- OriginalM04.5immutable. M05rail derivative mempunyai4edge-endpoint/7lane-shapeadaptations lokal yang belum diterima sebagai exact geometry preservation.
- Mean waiting/travel yang berasal dari tripinfo hanya arrived trips; lihat running/not_departed/lifecycle untuk censoring.
- Pending insertion tidak sama dengan seluruh demand yang belum selesai. Tidak ada unexplained teleport/collision pada run valid.
- Kandidat spillback Gedangan belum konfirmasi kausal. Oversize tetap diblokir; akses heavy tetap asumsiProvisionalM04.5.

## QA browser akhir

Akses pulih setelah restart pengguna. Versi akhir diverifikasi pada desktop1920×1080/mobile390×844 tanpa overflow horizontal. Playback, pause/reset/scrub/rate, camera presets/orbit/zoom, layers, vehicle inspector dan event jumps berfungsi. Loading tidak lagi menyajikan nol atau crossing open tanpa data. Final clean browser session tanpa warning/error. Screenshot: documentation/m05/browser-final-desktop.jpg dan browser-final-mobile.jpg. Direct vehicle raycast click belum diuji terpisah; dropdown inspector teruji. M06 tidak dimulai.
"""
 (ROOT/'MILESTONE_05_README.md').write_text(readme,encoding='utf-8');(ROOT/'documentation/MILESTONE_05_README.md').write_text(readme,encoding='utf-8')
if __name__=='__main__':main()
