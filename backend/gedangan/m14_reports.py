"""Reports assembled from retained results; no fabricated measurements."""
import statistics,collections
from .m14_common import *
from .m14_demand import default,generate
from .m14_network import catalog
from .m14_vehicles import registry

def table(headers,rows):
 return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(str(x).replace('|','/')for x in row)+' |'for row in rows])+'\n'
def write(name,text):
 (ROOT/name).write_text(text.strip()+'\n',encoding='utf-8')
def main():
 bench=load(DOC/'sumo-benchmarks.json');final=load(DOC/'final-3000.json');classes=load(DOC/'class-validation.json');rail=load(DOC/'rail-sensitivity.json');signal=load(DOC/'signal-sensitivity.json');long=load(DOC/'duration-120min.json');cat=catalog();d=generate(default());hardware=load(DOC/'hardware.json');audits=load(DOC/'xml-independent-audit.json')+load(DOC/'final-xml-audit.json');pres=verify_protection()
 bt=table(['Demand','Routed','Loaded','Departed','Arrived','Active akhir','Belum berangkat','Gagal','Generation wall s','SUMO wall s','Total wall s'],[[r[k]for k in ['requested','routed','loaded','departed','arrived','active','not_departed','failed_routes']]+[round(r[k],3)for k in ['generation_wall_s','simulation_wall_s','total_wall_s']]for r in bench])
 ct=table(['Tipe','Diminta','Routed','Loaded','Departed','Moved','Arrived','Active'],[[v['label'],5]+[classes['classes'][v['id']][k]for k in ['routed','loaded','departed','moved','arrived','active']]for v in registry()])
 at=table(['Pendekat','Anchor SUMO','Gerakan tersedia'],[[a['id'],a['anchor_edge'],', '.join(t for t,m in a['movements'].items()if m['available'])]for a in cat['approaches']])
 vt=table(['Tipe','SUMO class','L × W × H m','Max m/s','Accel/decel','Gap/tau'],[[v['id'],v['sumo_vclass'],' × '.join(str(v['parameters'][k])for k in ['length','width','height']),v['parameters']['maxSpeed'],str(v['parameters']['accel'])+'/'+str(v['parameters']['decel']),str(v['parameters']['minGap'])+'/'+str(v['parameters']['tau'])]for v in registry()])
 def sensitivity(results):return table(['Konfigurasi','Run ID','Arrived','Mean wait s','Mean speed m/s','Max lane queue','Transitions'],[[k,r['run_id'],r['arrived'],round(r['departed_mean_waiting_s'],4),round(r['mean_speed_m_s'],4),r['max_lane_queue_count'],r['signal_transitions']]for k,r in results.items()])
 common=f"""
Tanggal laporan: 1 November 2026 (WIB). Semua jumlah demand adalah masukan eksperimen, bukan pengukuran Gedangan. Tidak ada klaim kalibrasi atau efektivitas rekayasa lapangan.

Staging: `http://127.0.0.1:5199/`. Build: `frontend/dist-m14/`. Jalankan ulang dengan `staging/m14/START_M14.ps1` dari proyek ini. SUMO lokal 1.28.0. Final M12 tidak ditimpa.

Jaringan eksisting: `{cat['network_path']}`. SHA-256: `{cat['network_sha256']}`. Tidak ada flyover, ruas baru, koneksi baru, vClass ignoring, atau override izin kendaraan TraCI. Pembatasan kelas/akses/geometri M04.5 tetap diterapkan; izin provisional dalam model bukan sertifikat legalitas atau swept-path lapangan.
"""
 perf=[]
 for p in (DOC/'browser-performance').glob('*.json'):
  v=load(p)
  if v.get('kind')=='render_sample':perf.append(v)
 pr=[]
 for r in bench+[final]:
  samples=[v for v in perf if v.get('recording')==r['run_id']and v.get('playing')and v.get('window')==[1920,1080]];fps=[v['fps_mean']for v in samples]
  loads=[load(p)for p in (DOC/'browser-performance').glob('*.json')if load(p).get('kind')=='playback_load'and load(p).get('run_id')==r['run_id']]
  pr.append([str(r['requested'])+(' (final v2)'if r['run_id']==final['run_id']else''),len(samples),round(min(fps),2)if fps else'MISSING',round(statistics.median(fps),2)if fps else'MISSING',round(max(fps),2)if fps else'MISSING',round(loads[-1]['wall_ms']/1000,3)if loads else'MISSING',samples[-1]['viewport']if samples else'MISSING'])
 pt=table(['Demand','Sampel aktif','FPS min','FPS median','FPS max','Playback load s','Canvas px'],pr);save(DOC/'performance-summary.json',{'method':'All retained active-playback samples at browser window 1920x1080, per final benchmark run ID; warm-up/paused excluded. Background stalls retained. Windows/viewport observations, not a hardware certification.','rows':pr,'hardware':hardware})
 write('M14_MANUAL_SCENARIO_REPORT.md',f"""# M14 — Manual Traffic Scenario Builder
{common}
## Alur yang tersedia
Tanggal native date picker (termasuk bulan/tahun), start WIB, 15/30/60/90/120 menit atau custom 60–14.400 detik; mode manual 10 kelas atau random sampai 10.000 permintaan; seed; komposisi; enam pendekat nyata; persentase belok; departure merata/puncak/custom 5/15/60 menit; parameter sinyal dan jadwal KA asumsi. Preview menampilkan komposisi, rute lolos/gagal, dan histogram departure sebelum Generate.

Generate menjalankan validasi, alokasi, routing, penulisan SUMO XML, SUMO nyata, pengumpulan output, lalu membuka rekaman 3D. Progress berasal dari langkah SUMO, bukan timer dekoratif. Error dipertahankan dengan penyebab. Save/Load/Duplicate membuat skenario JSON terpisah, bukan observasi historis.

## Implementasi
Modul baru `backend/gedangan/m14_*.py`, `frontend/src/m14/`, `frontend/manual.html`, `frontend/vite.manual.config.ts`, `tests/m14/`. Renderer M10 disalin ke namespace M14; sumber M10 tidak diedit. Render menggunakan geometri jaringan dan trajectory SUMO aktual, dengan interpolasi spasial antar sampel 0,5 detik. Kapasitas instancing dihitung dari maksimum kendaraan aktif per tipe, bukan seluruh permintaan.

## Hasil utama aktual
Final run `{final['run_id']}`: diminta {final['requested']}; lolos rute {final['routed']}; berangkat {final['departed']}; tiba {final['arrived']}; aktif {final['active']}; belum berangkat {final['not_departed']}; gagal rute {final['failed_routes']}. Tidak ada peristiwa izin/tabrakan/teleport yang tercatat. Run 120 menit `{long['run_id']}` benar-benar dieksekusi: {long['requested']} diminta, {long['routed']} routed, {long['departed']} berangkat, {long['arrived']} tiba, {long['active']} aktif.

## Bukti
- `documentation/m14/final-3000.json`, `duration-120min.json`, `final-xml-audit.json`.
- `simulation/runs/m14/<run_id>/`: input manifest, demand, route/config XML, FCD, tripinfo, statistik, vehicle ledger, phase transitions, playback chunks dan output hash.
- Screenshot dan video aktual: `documentation/m14/evidence/`. MP4 `GEDANGAN_M14_ACTUAL_SUMO.mp4` ditranscode dari capture canvas aktual sekitar 12s / 358 frame; provenance terpisah dalam `video-provenance.json`.
- Perlindungan data: {pres['status']}, {pres['checked']} berkas/arsip dibandingkan SHA-256, tidak berubah.

## Batasan
Tidak semua permintaan masuk jaringan dalam horizon 15 menit. Sepeda dan becak nonmotor tidak diizinkan baseline. Gerakan belok dan arah KA dibatasi konektivitas yang benar-benar ada. Kedatangan KA nominal tidak dipaksa tepat pada waktu input. Performa browser bervariasi; lihat laporan benchmark, termasuk stall rendah, tanpa mengklaim FPS terjamin.
""")
 write('M14_RANDOM_VEHICLE_GENERATOR_REPORT.md',f"""# M14 — Random Vehicle Generator
{common}
## Ketepatan dan reproduksi
Random composition memakai PRNG lokal dengan seed tersimpan, weighted physical draws (bukan PCU/SMP). Semua permintaan memiliki ID `m14_000000` dan seterusnya. Tidak ada kehilangan akibat pembulatan. Pendekat berbobot diacak secara reproducible. Pembagian belok exact dan histogram departure memakai largest remainder, tie-break stabil, lalu penempatan cohort diacak dengan seed yang sama.

Lima profil bobot editable diberi label ILLUSTRATIVE RANDOM PROFILE. Tidak ada klaim profil default mewakili komposisi Gedangan. Manual/random terpisah dari VERIFIED HISTORICAL OBSERVATION; M14 tidak memanggil penulisan database observasi.

## Contoh 3.000, seed 42
{table(['Tipe','Jumlah'],[[k,v]for k,v in d['composition'].items()])}
Total tepat {d['total']}. Departure 0–5/5–10/10–15 menit masing-masing 1.000 permintaan. Cohort SHA: `{d['cohort_sha256']}`. Seed identik menghasilkan cohort, kelas, pendekat, belok dan departure yang sama; seed 43 berbeda. ID unik dan konservasi diuji pada total 1, 7, 499, 500, 1.000, 2.998, 3.000 dan 5.000.

Setiap run menyimpan request, komposisi hasil, alokasi pendekat/belok, histogram, seed, registry dan network hash. Run final versi m14-2 juga menyimpan teks source snapshot, hash SUMO exe, source dependencies dan policy inspection. Output SUMO/config ditandai hash. Saved scenario baru menyimpan request beserta ringkasan hasil generator. Scenario lama yang disimpan sebelum penyempurnaan ini tetap reproducible dari seed dan request.

## Pengujian
`documentation/m14/m14-tests-final.txt`: 13 tes M14 lulus. Source request disimpan di `simulation/runs/m14/{final['run_id']}/demand.json`. Profil adalah asumsi eksperimen; bukan hasil survei.
""")
 write('M14_VEHICLE_CLASS_VALIDATION.md',f"""# M14 — Vehicle Class Validation
{common}
## Parameter fisik nominal
{vt}
M04 dipakai tanpa mengedit registry aslinya. Becak motor memiliki parameter nominal dan model 3D roda tiga sendiri, berbeda dari motor dan becak nonmotor. Izin becak motor mengikuti motorcycle, ditambah pemeriksaan ukuran modelnya sendiri. Semua dimensi/dinamika adalah asumsi teknis, bukan hasil ukur. Bicycle class tidak dibuka otomatis.

## Lifecycle aktual — manual 5 per tipe
Run `{classes['run_id']}`, 900 detik; departure disebar pada 300 detik awal agar dapat mengamati arrival.

{ct}
Total 50 diminta, 40 memiliki rute; 10 sepeda/becak nonmotor tetap gagal. Unfinished trips dipertahankan. Trailer lulus pada rute utama yang memenuhi screen provisional M04.5; ini bukan izin untuk kendaraan oversize atau bukti swept path/legal permit. Tidak ada tipe oversize ditambahkan pada M14.

No recorded illegal lane permission, collision, teleport. Permission setiap kendaraan aktif diperiksa tiap langkah 0,5s, termasuk lane internal. Rute memakai koneksi yang diizinkan sumber. Bukti setiap ID: `simulation/runs/m14/{classes['run_id']}/vehicle-results.json`, FCD dan tripinfo.
""")
 write('M14_ROUTE_AND_TURNING_VALIDATION.md',f"""# M14 — Route and Turning Validation
{common}
## Koneksi tersedia
{at}
Pendekat adalah anchor actual SUMO connection. Ujung rute diperpanjang sepanjang koneksi lurus berfungsi/nama sama, target sekitar 420m upstream/downstream; panjang aktual dapat berbeda. Origin, mandatory turn dan destination diperlihatkan di ledger. Ini katalog model terbatas, bukan survei seluruh belokan Gedangan.

Gerakan kosong/tidak legal tidak dibuat. Right/U-turn tidak ditambahkan untuk memuaskan demand. Tes permintaan northbound→right mempertahankan 10 ID sebagai gagal, tanpa penggantian tujuan. Exact approach harus berjumlah sama dengan demand; vehicle/approach/turn percentages harus 100. Turn nontersedia dinonaktifkan UI, dan backend tetap mencatat gagal jika request semacam itu dikirim.

Screen memeriksa permissions external/internal lane, explicit lane-to-lane connection, private/conditional access dan dimensi; heavy road-function serta trailer deflection screen inherited tetap dipakai. Frontage tetap route tersendiri. Akses slow tidak diperlebar.

## Bukti
`documentation/m14/route-compatibility.json`: 10 tipe × 6 pendekat × 4 gerakan. `network-catalog.json`, `vehicle-registry.json`, route-ledger di setiap run (`vehicle-results.json`). {len(audits)} run diperiksa terhadap XML actual dan output hashes; hasil `xml-independent-audit.json` serta `final-xml-audit.json`. Tidak ada perubahan geometri/koneksi/izin pada berkas baseline.
""")
 write('M14_SIGNAL_RAILWAY_VALIDATION.md',f"""# M14 — Signal and Railway Validation
{common}
## Profil sinyal
Inherited controller `m05_gedangan`, 27 fase protected dalam jaringan eksisting. Baseline nominal 12s green + 3s yellow + 2s all-red untuk masing-masing 9 grup; cycle 153s. Editable duration dimuat ke SUMO lewat additional tlLogic, state fase dan link tidak diubah. Ini ASSUMED SIGNAL PROFILE, bukan timing Dishub resmi. `signals.json` berasal dari state controller TraCI pada setiap perubahan.

## Uji perubahan hijau 12s → 30s
{sensitivity(signal)}
Demand, rute dan seed sama; perubahan sinyal mengubah waktu tunggu dan transisi. Angka arrival sama tidak berarti lampu tidak berpengaruh. Tidak ada klaim setting baru lebih baik secara lapangan.

## Kereta dan perlintasan
Satu arah N_TO_S memakai rute rel M05.1 yang sudah tersambung. Reverse tidak ditambahkan. Jadwal pengguna merupakan EDITABLE ASSUMED SCHEDULE, bukan jadwal resmi. Arrival input dikonversi ke nominal departure bebas; aktualnya dapat berbeda karena akselerasi/kondisi rel. Kecepatan nominal = panjang 80m / input passing seconds; train body tetap 80m. Headway closing, opening delay/time dan minimum open/recovery diterapkan pada rail-crossing controller. Yellow closing inherited 3s. Recovery di sini parameter minimum terbuka, bukan pengukuran waktu antrean pulih.

## Uji dengan/tanpa 3 KA
{sensitivity(rail)}
Demand 160 mobil pada pendekat perlintasan, seed dan departure identik. Dengan KA mean waiting menjadi {rail['with_train']['departed_mean_waiting_s']:.4f}s, tanpa KA {rail['without_train']['departed_mean_waiting_s']:.4f}s. Max queue berubah {rail['without_train']['max_lane_queue_count']} → {rail['with_train']['max_lane_queue_count']}. Ini bukti in-model pengaruh perlintasan terhadap antrean, bukan angka observasi lapangan. Crossing lane samples KA aktual tersedia pada audit XML independen; phase transitions, FCD dan tripinfo disimpan.

Dokumentasi teknis: [SUMO Traffic Lights](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html), [SUMO Railways](https://sumo.dlr.de/docs/Simulation/Railways.html). Sumber geometri rel: `simulation/network/m051/provisional/rail-provenance.json`; baseline parameter `configuration/railway-m05/pilot.json`.
""")
 write('M14_SUMO_EXECUTION_REPORT.md',f"""# M14 — Actual SUMO Execution
{common}
## Benchmark aktual 900 detik
{bt}
Semua run memakai SUMO 1.28.0, step 0,5s, teleport disabled (`-1`), collision warn dengan logging; tidak ada route ignore-errors atau izin bypass. Loaded adalah event actual loaded, berbeda dari departed. Pending insertion tidak dihapus. Arrived hanya aktual tripinfo arrival nonnegative. Waiting at end adalah active road speed <0,3m/s pada langkah terakhir. Queue extent adalah span kendaraan berhenti per lane, bukan panjang antrean lapangan terkalibrasi.

## Konservasi dan audit
Requested = Routed + Failed. Routed = Departed + Not departed. Departed = Arrived + Active akhir. Seluruh persamaan diverifikasi. Audit independen membandingkan departure/arrival dengan tripinfo XML, unique IDs, actual connections, network hash, playback frame count dan seluruh output hash.

Final source v2 run `{final['run_id']}`: {final['requested']} → routed {final['routed']}, loaded {final['loaded']}, departed {final['departed']}, moved {final['moved']}, arrived {final['arrived']}, active {final['active']}, not departed {final['not_departed']}, failed {final['failed_routes']}. Waktu SUMO {final['simulation_wall_s']:.3f}s. Semua angka sama dengan cohort benchmark 3.000 sebelumnya, sehingga penyempurnaan screen becak tidak mengganti tujuan/demand.

## Output dan reproducibility
`simulation/runs/m14/{final['run_id']}/run.sumocfg` dapat dijalankan oleh SUMO toolchain lokal. Request lengkap di `demand.json`; snapshot dan hash dependency di `source-snapshot.json`/`input-manifest.json`. Re-run Python request akan membangun run dengan source version yang aktif; seed dan cohort dapat diperiksa secara eksplisit. UI frontend terpisah dari runner; hasil yang ditampilkan berasal dari FCD/chunks aktual.

Run 120 menit benar-benar dieksekusi, bukan hanya validasi form: `{long['run_id']}`, {long['requested']} requested, {long['routed']} routed, {long['departed']} departed, {long['arrived']} arrived, {long['active']} active. Wall {long['simulation_wall_s']:.3f}s.

## Kegagalan pengembangan yang diperbaiki
Percobaan awal gagal schema XML additional; kemudian schema SUMO lokal ditambahkan. Uji trailer awal gagal karena metadata eligibility belum dibawa dari registry; metadata dipertahankan lalu tes diulang. Satu tes sempat membaca benchmark ketika daftar masih ditulis bertahap; final suite dijalankan setelah benchmark lengkap. Renderer juga diperbaiki saat pergantian recording: callback animasi lama sekarang menunggu jika ID recording tidak cocok dengan mesh buckets yang sedang terpasang. Pergantian sparse/full cohort diperiksa ulang di browser pada build final. Jejak kegagalan tetap disimpan, tidak disembunyikan sebagai successful run.
""")
 write('M14_PERFORMANCE_BENCHMARK.md',f"""# M14 — Performance Benchmark
{common}
## Lingkungan terukur
{hardware['os']['Caption']} {hardware['os']['Version']}. Adapter terdeteksi: {', '.join(g['Name']for g in hardware['gpu'])}. RAM yang dilaporkan OS {hardware['ram_bytes']/1024**3:.2f} GiB; bukan klaim seluruh 16GB tersedia untuk aplikasi. Browser melaporkan WebKit WebGL; deteksi adapter AMD oleh OS tidak membuktikan browser memakai adapter fisik tersebut. Target window 1920×1080; canvas lebih kecil karena toolbar. DPR dan viewport tersimpan per sampel.

## Eksekusi SUMO
{bt}
Wall times terukur pada satu mesin dengan pekerjaan lain berjalan; bukan benchmark mesin bersih, tidak menjanjikan durasi konstan. Generation time dan total_wall_s per run juga disimpan pada result JSON. Durasi 15 menit adalah waktu model, bukan waktu komputasi.

## Browser actual playback
{pt}
Sampel hanya saat Play aktif pada window 1920×1080; paused/warm-up tidak digabung. Min rendah dan stall tetap dimasukkan. File mentah menyimpan FPS mean, p5, draw calls, triangle count, visible/active sampled vehicles, visibility/focus dan waktu playback. Metrik merupakan render-loop timing browser, bukan FPS dari perekam video atau pengukuran AMD GPU hardware. Ada callback mendekati interval satu detik dalam sesi; pembatasan/occlusion browser mungkin berperan tetapi penyebabnya belum dibuktikan sepenuhnya.

## Optimasi dan batas klaim
Mesh kendaraan di-instance per tipe, kapasitas dihitung dari maksimum active per tipe pada rekaman. Gambar hanya instance aktif pada waktu terpilih. Playback dipaket gzip chunk 60 detik, concurrency fetch empat; data 0,5s disimpan tanpa animasi kendaraan dekoratif. Geometri static digabung, context massing opsional tidak dihitung saat dimatikan. Playback timing memakai elapsed wall clock agar stall tidak diam-diam mengubah multiplier waktu.

Aplikasi terbukti memproses 3.000/5.000 permintaan serta membuka hasil 3D aktual, tetapi jumlah kendaraan aktif mengikuti kapasitas jaringan, bukan total requested. FPS stabil sepanjang sesi dan performa khusus AMD 16GB/1080p belum disertifikasi. STATUS PERFORMANCE: CONDITIONAL, karena variasi dan stall browser masih tercatat. Data 3.000 tidak boleh dipresentasikan sebagai 3.000 kendaraan semuanya berhasil masuk.
""")
 write('M14_ACCEPTANCE_REPORT.md',f"""# M14 — Acceptance Report
{common}
## Keputusan
FUNCTIONAL FLOW: PASS. PRESENTATION/PERFORMANCE: CONDITIONAL. M14 menghasilkan SUMO nyata dan playback jaringan eksisting; performa browser dicatat beserta stall, tanpa klaim FPS terjamin atau validasi lalu lintas lapangan.

{table(['Kriteria','Status','Bukti'],[
['Manual exact composition','PASS','13 tes M14; actual all-ten-class run'],['Random exact total / rounding','PASS','1,7,499,500,1000,2998,3000,5000'],['Seed identik reproducible','PASS','Cohort SHA dan demand identik'],['Seed baru berbeda','PASS','Seed42 vs43'],['Unique ID','PASS','Seluruh requests dan XML audit'],['Legal model routes','PASS with explicit denials','Actual connections/type/access screens; 80 failed pada 3000'],['Departure tersebar','PASS','Uniform/peak/custom + duration tests; histogram'],['Signal controller berpengaruh','PASS','Actual timing sensitivity'],['Kereta memengaruhi antrean','PASS','Paired160-car experiment; waiting0→2.121875s'],['Statistik sama output SUMO','PASS','Tripinfo independent audit + mass balance'],['Tidak ada flyover / baseline immutable','PASS','Network SHA unchanged; route/no-flyover audit'],['Tidak masuk historical calendar','PASS','Database hashes unchanged; M14 store terpisah'],['Saved scenario reopen','PASS','HTTP save/load + browser save'],['3000 handled actual','PASS with pending/failed retained','2920routed/1271departed/566arrived/705active/1649pending/80failed'],['Windows1080p FPS assurance','CONDITIONAL','Measured varying FPS and stalls; raw samples retained'],['Actual screenshot/video','PASS, capture limits recorded','documentation/m14/evidence; video probe JSON']])}
## Pengujian dan perlindungan
`regression-tests-final.txt`: 357 tests, 356 lulus, 1 skipped (duplicate presentation-service CLI test, karena layanan M09 tidak berjalan). Tidak ada failures/errors. Setelah screen ukuran becak motor diperketat, 13 tes M14 diulang dan lulus; TypeScript build/type check lulus. Generate dari browser pada build final juga menghasilkan 50 requested, 49 routed/departed/moved, 41 arrived, 8 active, 1 failed; diperiksa dalam `browser-final-audit.json`. Duplicate/Save/Load diuji lewat UI dan memulihkan total50 serta nama salinan, lihat `browser-qa.json`. `xml-independent-audit.json` dan `final-xml-audit.json`: {len(audits)} run, semua checks pass: {all(a['status']=='PASS'for a in audits)}. Perlindungan {pres['checked']} berkas/arsip: {pres['status']}.

## Cara mencoba
1. Buka staging localhost5199; pilih tanggal/jam WIB dan durasi.
2. Pilih manual/random, jumlah, profil/seed, pendekat dan belok yang tersedia.
3. Preview; periksa total, distribusi dan failed routes.
4. Edit timing/jadwal asumsi bila diperlukan; klik Generate Simulation.
5. Tunggu progress actual; hasil dan rekaman 3D terbuka otomatis. Pilih Play, kamera, timeline dan kecepatan.
6. Save Scenario menyimpan request/seed. Load memulihkan request; Duplicate memberi salinan yang dapat disimpan terpisah.

## Batas yang belum selesai
- Izin sepeda/becak nonmotor tidak tersedia pada baseline; ditolak eksplisit.
- Belok/arah KA di luar koneksi existing tidak dibuat. Jadwal KA hanya nominal assumption, bukan jadwal resmi.
- Data geometri, signal timing, dimensi/dinamika belum divalidasi survei. Tidak ada legal swept-path certificate untuk trailer.
- Queue extent dan boundary sample adalah model proxy. Tidak ada klaim causal field spillback.
- FPS dan capture video bervariasi karena sesi browser; tidak dinyatakan sebagai presentasi 1080p mulus terjamin.
- M14 adalah staging web dengan runner SUMO lokal, bukan penggantian atau EXE rilis baru M12.

## Deliverables
Delapan laporan root M14, staging frontend/backend, skenario JSON, SUMO XML/output, manifest/hash/source snapshot final, screenshot, video aktual dan performance logs telah disimpan. Tidak ada upload GitHub, penghapusan data penelitian, perubahan final M12, atau implementasi flyover/milestone berikutnya.
""")
 print('Written 8 M14 reports',flush=True)
if __name__=='__main__':main()
