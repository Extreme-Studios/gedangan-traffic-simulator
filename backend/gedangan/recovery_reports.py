"""Build reviewable reports from saved actual outputs; never manufacture results."""
from .recovery_common import *

def link(p,label=None):
 p=Path(p).resolve();return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(str(x)for x in r)+' |'for r in rows)+'\n'
def write(name,title,body):
 (ROOT/name).write_text('# '+title+'\n\nDibuat dari actual outputs, 1 November 2026. Status penelitian: **belum dikalibrasi terhadap observasi Gedangan 2026**.\n\n'+body+'\n',encoding='utf-8')
def main():
 a=load(DOC/'acceptance-results.json');assert a['status']!='RUNNING'
 jobs={j['name']:load(RUNS/j['run_id']/'result.json')for j in a['jobs']};base=jobs['morning_base'];pres=load(DOC/'preservation-verification.json');impact=load(DOC/'network-impact-analysis.json')
 evidence='\n\nBukti lengkap: '+link(DOC/'acceptance-results.json')+', '+link(DOC/'supplemental-acceptance.json')+', '+link(DOC/'api-acceptance.json')+'.'
 def outputs(r):return link(RUNS/r['run_id'],r['run_id'])
 audit=load(DOC/'network-audit.json')
 write('GEDANGAN_NETWORK_GROUND_TRUTH_AUDIT.md','Gedangan — Network Ground Truth Audit',f'''## Ruang lingkup dan metode

Parent immutable: `simulation/network/m051/provisional/network.net.xml`, SHA256 `{audit['network_sha256']}`. {audit['road_edges']} external road edges dan {audit['internal_edges']} internal edges diperiksa. OSM snapshot 31 Oktober 2026; directional/split SUMO edges tidak sama dengan jumlah original OSM segments.

Koordinat sumber WGS84 diproyeksikan UTM49S (EPSG32749), lalu diberi netOffset asli. Setiap shape edge SUMO dibandingkan dengan centerline way OSM asal, bukan dengan gambar layar. Maksimum jarak centerline sumber sekitar 3,731m; lane offset dan junction trimming turut memengaruhi angka ini. **Ini bukan akurasi survei lapangan.**

Overlay: {link(DOC/'network-source-overlay.geojson')} dan {link(DOC/'network-source-overlay.svg')}. Angka per edge: {link(DOC/'source-geometry-comparison.json')}. Audit/controller/class connectivity: {link(DOC/'network-audit.json')}.

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
''')
 write('GEDANGAN_HISTORICAL_DATA_COVERAGE.md','Gedangan — Historical Data Coverage',f'''## Hasil pencarian

Target 1 Agustus–31 Oktober 2026: **0 directional observations yang memenuhi syarat exact demand**. Kalender 92 hari ×96 interval15menit =8.832 time slots MISSING; bukan angka nol kendaraan. Count arah/turning/signal/rail events/travel time/queue/OD target tetap MISSING.

Database {link(DATA/'historical.sqlite')}; schema {link(DOC/'historical-schema.json')}; coverage {link(DOC/'target-coverage-view.json')}; sumber unduhan dan SHA {link(DOC/'source-register.json')}.

36 record historis dipertahankan sebagai OBSERVED dalam lingkup sumber aslinya: Kusuma & Sholikhah, Table1 p927, survei 9/11/14 Mei2023, jam07/12/17, empat kelompok kendaraan. Lokasi Ahmad Yani terdampak konstruksi Aloha, arah UNSPECIFIED. Ini bukan hitungan simpang inti Gedangan 2026. Sumber [paper2024](https://ejournal.undip.ac.id/index.php/ilmulingkungan/article/download/56951/pdf).

Jumlah tiga jam pengamatan tidak diartikan sebagai volume per jam atau data sepanjang hari. Data15menit asli tidak tersedia. Tabel Juni dengan ketidaksesuaian hari/tanggal dikeluarkan. Sumber2022 berunit skr/jam tidak diubah menjadi kendaraan/jam; PDF-nya belum dapat diunduh. Data signal paper dengan waktu/unit tidak cukup pasti tidak dijadikan count2026.

## Kebijakan penyimpanan

Setiap evidence mempunyai date/daytype/start-end WIB/interval/road/direction/entry/exit/class/metric/value/unit/status/source-year/provenance. Status OBSERVED, REFERENCE_BASED_ESTIMATE, SYNTHETIC_SCENARIO, MISSING dibedakan. UPDATE/DELETE evidence ditolak SQLite; perubahan melalui record/version baru. Simulated results disimpan di experiments/run outputs, tidak dipromosikan menjadi observasi.

Estimasi hanya memakai jam referensi yang tersedia. Range ketidakpastian adalah sensitivity envelope, bukan confidence interval statistik. Pengisian coverage observasi membutuhkan sumber terverifikasi, count arah, entry/exit, review kualitas dan endpoint network; agregat tanpa arah tidak otomatis lolos.
''')
 write('GEDANGAN_TIME_DEPENDENT_DEMAND.md','Gedangan — Time-dependent Demand',f'''## Perilaku yang diimplementasikan

Date/time WIB, weekday/weekend aktual tanggal, year, vehicle types, seed, horizon dan warm-up masuk request serta signature run. Elapsed0 terpisah dari jam pengukuran. Hari libur tidak ditebak. Pergantian tanggal bukan bukti adanya observasi pada tanggal itu.

EXACT_OBSERVED mencari bukti sesuai tanggal/jam dan gagal tertutup jika arah/OD/review belum cukup. REFERENCE_ESTIMATE membutuhkan persetujuan eksplisit asumsi dan hanya mendukung07–08,12–13,17–18. Night atau contoh5Mei16:00 menghasilkan MISSING. Night dapat diuji lewat SYNTHETIC_SCENARIO dengan input OD/class/veh-per-hour eksplisit.

Weekday memakai mean sampel Selasa/Kamis; weekend sampel Minggu. Split NB default0,5 (rentang0,3–0,7), demand scale0,5–1,5, turning0–0,25. Turning diambil dari volume through, bukan ditambahkan. Truk agregat sumber hanya ditransfer menjadi light_truck dengan asumsi eksplisit. Tidak ada automatic annual growth atau pembagian subclass berat tanpa bukti.

Sub-hour flat profile dan stationary selected-hour warm-up adalah asumsi. Warm-up bukan keadaan awal terukur. Ledger menyimpan interval, sumber, status dan count; deterministic stratified departures dengan seed; cumulative rounding diuji untuk profile referensi flat. Batas12.000requests/run, horizon60–3600s dan warm-up0–1800s.

07:00 dan17:00 menghasilkan cohort berbeda; actual SUMO dijalankan terpisah. Cache hanya berlaku pada request/cohort/network/runner hashes identik dan output hashes valid. Tidak ada substitusi rekaman lain ketika data atau run hilang.

Demand/cohort tiap run ada di folder input/manifest terkait. Baseline07:00 {outputs(base)}. Tabel hasil aktual: {link(ROOT/'GEDANGAN_PEAK_HOUR_SUMO_TEST.md')}.
'''+evidence)
 rows=[];metrics=[]
 for name,r in jobs.items():
  rows.append([name,r['requested'],r['routed'],r['loaded'],r['departed'],r['arrived'],r['running_at_end'],r['failed_routes'],r['not_departed']])
  metrics.append([name,round(r['arrived_only_mean_travel_s'],2)if r['arrived_only_mean_travel_s']is not None else'MISSING',round(r['network_sampled_mean_speed_m_s'],3),round(r['departed_including_unfinished_mean_waiting_s'],2),round(r['max_lane_queue_extent_m'],1),r['throughput_arrivals_per_hour_measurement']])
 write('GEDANGAN_PEAK_HOUR_SUMO_TEST.md','Gedangan — Actual Peak-hour SUMO Tests',f'''## Eksperimen

SUMO1.28.0 lokal, step0,5s, FCD1s. Main suite: {a['status']}, {len(a['jobs'])} actual runs, {len(a['checks'])} checks. Reference tests memakai tanggal4Agustus2026, horizon900s + warm-up300s, seed42, turnshare0,1; tanggal hanya memilih kalender/estimasi historis. Offpeak adalah input sintetis. Weekend memakai2Agustus. Tidak ada pengukuran volume2026 atau kalibrasi kapasitas.

Mass balance **seluruh horizon termasuk warm-up**:

'''+table(['Run','Requested','Routed','Loaded','Departed','Arrived','Running','Failed','Not departed'],rows)+'''
Requested=Routed+Failed; Routed=Departed+Not departed; Departed=Arrived+Running. Unserved tidak dibuang. Measurement-only cohort dan warm-up state disimpan terpisah di result.json.

## Metrik model

'''+table(['Run','TT arrived-only s','Mean sample speed m/s','Wait departed s','Max queue extent m','Throughput veh/h'],metrics)+f'''
Travel time hanya yang tiba; trips unfinished tersensor dan tidak diberi waktu0. Speed adalah vehicle-time sample mean. Queue extent adalah proxy lane, bukan panjang antrean lapangan. Throughput adalah arrivals pada measurement window diekstrapolasi ke perjam, bukan demand atau countobserved.

Spillback dievaluasi sebagai consecutive storage-blockage candidate samples; final continuous episodes ada di analysis.json. Tidak membuktikan penyebab lapangan dan dapat undercount. Jangan gunakan jumlah span samples engine sebagai durasi continuous.

Teleports dinonaktifkan (`time-to-teleport=-1`), illegal permissions/collision/teleport/occupancy ketika palang tutup tetap direkam. Status clean berarti tidak tercatat pada resolusi pengujian, bukan sertifikasi keselamatan.

Registry/kelas uji: {link(DOC/'multiclass-compatibility.json')}. Heavy truck bergerak tetapi belum tiba dalam fixture; oversize seluruhnya ditolak. Trailer hanya pada rute existing yang lolos screen sementara, tidak melalui flyover konsep.

Output raw per run: FCD, tripinfo, summary, statistics, config, demand ledger, route ledger, vehicle results, signal/rail state, edge impact dan manifests. Run directory: {link(RUNS)}.
'''+evidence)
 fo=[]
 for n in ['morning_base','flyover_A','flyover_B']:
  r=jobs[n];an=load(RUNS/r['run_id']/'analysis.json');fo.append([n,r['network_sha256'],r['actual_flyover_vehicles'],an['actual_flyover_max_z_m'],r['arrived'],r['not_departed']])
 write('GEDANGAN_FLYOVER_ALTERNATIVES.md','Gedangan — Executable Flyover Alternatives','''## Batas sumber resmi

[Pemkab22September2026](https://www.sidoarjokab.go.id/berita/detail/1790214058/0) membahas enam lajur **di bawah** flyover. [Pemkab1Oktober2026](https://www.sidoarjokab.go.id/berita/detail/1790902516/0) membahas ROW dan koordinasi lintas instansi. Angka tersebut tidak diterapkan sebagai deck lane count. Final DED, georeferenced approved alignment, lahan, clearance KAI, izin dan swept path belum tersedia/terverifikasi. Pengumuman lokasi dicatat sebagai sumber, bukan DED yang sudah didigitasi.

## Konsep executable

Keduanya **UNVERIFIED ENGINEERING CONCEPT**, hanya sensitivitas lalu lintas. A:1lane/direction; B:2lanes/direction. Ground existing2lanes/direction dipertahankan. East offset20m/35m, deckz8m (input6–10m) adalah parameter konsep, bukan clearance legal.

NB: existing approach `w562358500_s13_p0_0_f` menuju exit `w266287935_s6_p0_0_f`. SB: `w512351908_s1_p0_0_f` menuju `w562358499_s1_p0_0_f`. Enam deck/ramp edges dan empat intermediate elevated nodes; koneksi hanya di endpoint koridor yang ada. Tidak ada ramp instan ke frontage/local. Grade screen maksimum6%; geometric grade screen bukan persetujuan struktur.

Motor/car/pickup/minibus/bus/light/medium truck diizinkan dalam konsep; heavy/trailer/oversize ditolak karena special-vehicle clearance belum memadai. Rail route dan at-grade crossing tetap ada; kendaraan deck melewati level berbeda. Ground controller tetap, tidak dihapus untuk memberi keuntungan semu. Local access ground dipertahankan dalam konsep operasi; constructability belum dibuktikan.

NETCONVERT1.28.0 mengekspor ulang dengan projection/offset asli, menjaga existing edge IDs dan movements; tidak menambah existing-to-existing movement. Build manifest menyimpan parent/spec/builder hashes, commands dan screening constraints.

'''+table(['Run','Network SHA256','Actual deck vehicles','FCD max z m','Arrived','Not departed'],fo)+f'''
Baseline tiba96; A504 tetapi not-departed meningkat766→949. B508 dan522not-departed. Angka ini tradeoff pada demand/controller asumsi yang sama, **bukan persentase pengurangan kemacetan Gedangan yang tervalidasi**. Kendaraan benar-benar tercatat pada deck, bukan sekadar assigned.

Manifest/network: {link(NETS)}; actual route/FCD analysis: {link(DOC/'network-impact-analysis.json')}. Rebuild berdasarkan request/spec dari result.json dan runner revision yang dicatat; sumber generator revisi awal diarsipkan bila berubah.
''')
 full=jobs['construction_full'];partial=jobs['construction_partial'];trip=load(DOC/'construction-triplet.json')
 write('GEDANGAN_CONSTRUCTION_DIVERSION.md','Gedangan — Construction and Diversion',f'''## Parameter dan batas

S07 one_lane menutup satu lane; full_closure menutup seluruh edge uji `w512351908_s3_p0_0_f`. Custom closed_edge harus existing ordinary road. Connection/lane/via permissions dipersempit, tidak dibuat jalan pengalihan baru. Work zone ini skenario teknis, bukan approved construction traffic management plan. Worksite detail, temporary signage, ROW, KAI agreement dan akses persil lapangan belum cukup.

Izin kelas dan conditional access tetap berlaku. Frontage bukan kapasitas tak terbatas; kendaraan berat yang tidak memenuhi screen tetap ditolak. Local access di graph lain dipertahankan, tetapi akses langsung pada edge yang ditutup dapat tidak terlayani dan dicatat.

'''+table(['State','Requested','Routed','Failed','Arrived','Not departed'],[[n,r['requested'],r['routed'],r['failed_routes'],r['arrived'],r['not_departed']]for n,r in [('before',base),('one_lane',partial),('full_closure',full),('post_concept_A',jobs['flyover_A'])]])+f'''
Full closure: **{full['rerouted']} rerouted, {full['lost_routes']} lost routes**, gagal total{full['failed_routes']} (baseline{base['failed_routes']}). Tidak seluruh overflow bisa dialihkan legal.

Triplet {link(DOC/'construction-triplet.json')} memuat {len(trip['rows'])} kendaraan dengan route before/during/after berubah, origin/destination/class, additional distance, transferred assigned volume per existing alternative edge. Added actual travel time hanya bila kendaraan yang sama tiba pada kedua run; lainnya null+censored. Free-flow additional cost tidak disamakan dengan actual travel-time gain.

Volume assigned per edge bukan kendaraan unik seluruh network. Actual entered volume tersedia di edge-impact dan per-vehicle traces. Post-construction adalah executable concept A, bukan rancangan operasi resmi.
''')
 comparisons=[]
 for p in (DOC/'comparisons').glob('*.json'):
  c=load(p);comparisons.append([p.stem,c.get('comparable'),link(p)])
 analysisbase=load(RUNS/base['run_id']/'analysis.json');regions=analysisbase['network_regions']
 write('GEDANGAN_NETWORK_IMPACT_REPORT.md','Gedangan — Network-wide Impact',f'''## Hasil dan cara membaca

{len(impact['runs'])} actual runs dianalisis terhadap network connections dan FCD, status {impact['status']}. Main NB/SB, frontage, Sukodono, Ketajen/rail vicinity, local/feeder/service dan deck konsep diagregasi; OD lebih rinci ada pada masing-masing analysis.json. Sedati/Jenggolo tetap MISSING/possible alias; driveway stasiun belum terverifikasi.

Baseline regional model proxies:

'''+table(['Region','Edges','Vehicle seconds','Queued lane seconds','Max queue extent m'],[[n,r['edges'],round(r['vehicle_seconds'],1),round(r['queued_lane_seconds'],1),round(r['max_queue_extent_m'],1)]for n,r in regions.items()])+'''
Penjumlahan per-edge bisa menghitung kendaraan yang sama di beberapa ruas. Volume assigned dan actual entered disajikan terpisah. Export per-ruas berisi delta assigned, actual unique entered, queue, speed dan vehicle-seconds. New bottleneck candidates ditentukan berdasarkan model queue, bukan diumumkan sebagai temuan lapangan.

'''+table(['Intervention','Comparable cohort','Per-road comparison'],comparisons)+f'''
S01 meningkatkan arrivals dalam fixture; tidak membuktikan signal plan optimum. S02 default dan S03 pada reference cohort tidak berpengaruh karena gerakan yang dibatasi tidak dipakai. Targeted supplemental tests membuktikan24rerouted untuk masing-masing intervensi; frontage arrivals justru25→21. Hasil negatif dipertahankan.

S06A menaikkan arrivals tetapi menambah belum-departed di boundary. S07 full meningkatkan failed routes18→94. Ini alasan tidak memberi ranking berdasarkan satu indikator simpang pusat saja. S05 belum executable karena kekurangan controller kedua, tidak ada klaim dampak atau koordinasi palsu.

Spillback: final {link(DOC/'network-impact-analysis.json')} mencantumkan sustained storage proxy episodes perrun; lane pairs/timestamps ada di analysis.json. Sampling/resolusi dan causal ambiguity membatasi interpretasi. Pengukuran network di luar boundary, demand calibration, field signal/rail timings dan perumahan/feeder observations masih diperlukan.
''')
 checks=table(['Check','Status'],[[c['check'],c['status']]for c in a['checks']])
 write('GEDANGAN_REALISM_RECOVERY_REPORT.md','Gedangan — Functional Realism Recovery',f'''## Keputusan penerimaan

**Core research engine implemented and exercised. H internal-browser functional smoke test PASS; user acceptance remains pending. Empirical traffic validity and engineering approval NOT established.** Ini research runner baru; EXE M12 lama tetap cached presentation viewer dan tidak diperbarui.

## Status A–H

'''+table(['Tahap','Hasil','Batas'],[['A','Audit/overlay/connectivity tersedia','Sedati/Jenggolo dan akses persil perlu verifikasi'],['B','SQLite/schema/provenance/coverage tersedia','Target2026 MISSING'],['C','Date/WIB/class demand berjalan','Historical transfer; no all-day interpolation'],['D',str(len(a['jobs']))+' actual SUMO matrix +5 supplemental +API run','Not calibrated; source/controller assumptions'],['E','S00–04 actual changes','S05 BLOCKED second controller missing'],['F','A/B deck executable, construction executable','UNVERIFIED ENGINEERING CONCEPT'],['G','Per-edge/OD/class/reroute/spillback proxy exports','No field impact claim'],['H','Loopback API actual run/export PASS; controls implemented','Browser new SUMO run/playback/comparison PASS; user acceptance pending']])+f'''
## Buka dan jalankan

Saat layanan aktif: [Research experiments](http://127.0.0.1:5196/). Untuk menjalankan kembali, double-click {link(ROOT/'START_GEDANGAN_RESEARCH.bat')}. Memerlukan `.venv` proyek dan toolchain SUMO1.28.0 lokal. Belum paket portable baru; jangan memindahkan launcher sendirian.

Pilih tanggal/jam, sumber dan pengakuan asumsi, horizon/warm-up/kelas, intervensi, lalu **Periksa demand → Jalankan SUMO baru**. Hasil tersimpan dengan run ID; pilih actual result untuk trace, baseline setara untuk comparison, JSON/CSV untuk ekspor. Pilih reference07/12/17 atau synthetic eksplisit; jangan berharap exact2026 tersedia. Example missing5Mei16:00 ditolak.

## Perubahan source

Namespace `backend/gedangan/recovery_*.py`: checkpoint/audit, source-evidence database, observed lookup, demand, permissions/pathfinding, derivative NETCONVERT, actual SUMO run, comparison, analysis, loopback service, launcher, acceptance dan report generation. Frontend `frontend/realism_recovery/` adalah technical2D inspection, tanpa redesign3D. Tests di `tests/recovery/`. Sumber M01–M12 tidak diedit.

## Bukti uji

Main suite **{a['status']}**, {len(a['jobs'])} runs, {len(a['checks'])} checks;5supplemental multiclass/targeted reroute actual runs PASS; HTTP API creates real SUMO experiment and serves traces/exports. Source/data contracts test log: {link(DOC/'contracts-tests.log')}. API integration PASS. Browser kemudian berhasil diakses: penolakan MISSING, playback WIB/elapsed, comparable flyover result dan new SUMO run264ede0fdfcecd93104bda52 diuji langsung. Screenshot browser-flyover-actual.png dan browser-new-experiment.png tersedia; browser-acceptance.json mencatat lingkup uji.18 data/source contracts PASS.

{checks}

## Pemeriksaan integritas akhir

Final evidence verification: **PASS, 27 saved actual runs**. Seluruh output hashes, network hashes, sumber runner sesuai revision, cohort demand dan mass balance diperiksa. Bukti: documentation/realism_recovery/final-evidence-verification.json. Tidak mengklaim seluruh historical milestone regression tests dijalankan ulang; preexisting files diverifikasi SHA256.

## Preservasi dan reproducibility

{pres['unchanged_preexisting_files']} preexisting files SHA256 unchanged. Satu receipt checkpoint baru yang tertangkap kosong saat command mulai dikecualikan eksplisit; baseline hash tidak diedit. Old finalZIP SHA256 `{pres['old_M12_release_sha256']}` tetap sama. Source checkpointZIP dan inventory: {link(DOC/'checkpoint')}; hasil {link(DOC/'preservation-verification.json')}.

Setiap successful run menyimpan request, deterministic cohort, network manifest/hash, runner modules, registry dan binary hashes, commands, input/output manifests. Failed attempts dipertahankan dan tidak dihitung sebagai successful run. Run kembali lewat module/actual request menggunakan revision sumber yang dicatat; exact matching cache harus lolos output hashes. Main matrix dapat diulang `.venv/Scripts/python.exe -m backend.gedangan.recovery_acceptance`; analysis dan reports melalui module bernama sama. Tidak mengubah data lama atau upload GitHub.

## Blockers dan pekerjaan berikut yang belum diklaim selesai

1. Directional/class/turning/signal/rail/queue/travel-time survey target2026 belum ada. Perlu input sah dan review, lalu kalibrasi/validasi independen.
2. S05 membutuhkan representasi controller koridor kedua berbukti; bukan menambahkan lampu palsu.
3. Flyover membutuhkan approved DED/ROW/lahan/clearance/KAI/swept path/constructability dan staging akses yang benar. Konsep sekarang hanya sensitivitas traffic.
4. Hambatan Work settings teratasi pada pemeriksaan ulang. Browser smoke test dan screenshot tersedia; penerimaan pengguna, semua variasi kontrol serta ukuran layar lain belum diuji menyeluruh.
5. Baseline kontrol27phase individual dan boundary demand perlu kalibrasi. High queue dan banyak unfinished trips bukan bukti kemacetan nyata Gedangan.
6. Belum ada EXE research baru atau final3D redesign. Release lama tetap preserved. Tidak ada GitHub upload atau penghapusan research dataset.

Laporan rinci: {', '.join(link(ROOT/n)for n in ['GEDANGAN_NETWORK_GROUND_TRUTH_AUDIT.md','GEDANGAN_HISTORICAL_DATA_COVERAGE.md','GEDANGAN_TIME_DEPENDENT_DEMAND.md','GEDANGAN_PEAK_HOUR_SUMO_TEST.md','GEDANGAN_FLYOVER_ALTERNATIVES.md','GEDANGAN_CONSTRUCTION_DIVERSION.md','GEDANGAN_NETWORK_IMPACT_REPORT.md'])}.
'''+evidence)
 print('Generated 8 recovery reports',flush=True)
if __name__=='__main__':main()
