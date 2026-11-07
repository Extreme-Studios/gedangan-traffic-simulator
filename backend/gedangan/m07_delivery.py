"""Report technical and empirical acceptance separately; retain failures/blockers."""
import re,sys,platform
from pathlib import Path
from .m04_demand import ROOT,load,save,sha
from .m07_growth import LABEL,CONDITIONAL,fingerprint
from .m07_validation import baseline_check
from .m07_reporting import publish
DOC=ROOT/'documentation/m07'
def main():
 publish();protected=baseline_check();runs=load(DOC/'run-summary.json');q=load(DOC/'run-queue.json');repro=load(DOC/'reproducibility.json');sensitivity=load(DOC/'sensitivity.json')
 text=(DOC/'final-regression.txt').read_text(encoding='utf-8-sig');match=re.search(r'Ran (\d+) tests.*?\n\s*OK\s*$',text,re.S)
 if not match:raise RuntimeError('Full regression must pass before delivery')
 if 'built in' not in (DOC/'production-build.txt').read_text(encoding='utf-8-sig'):raise RuntimeError('Production build evidence missing')
 browser=load(DOC/'browser-qa.json') if (DOC/'browser-qa.json').exists() else {'status':'BLOCKED','reason':'Internal browser QA incomplete'}
 ui_pass=browser.get('status')=='PASS';technical='PASS' if ui_pass else 'PARTIAL — INTERNAL BROWSER QA INCOMPLETE';n=int(match[1])
 primary_ids={j['run_id'] for j in q['completed']};primary=[r for r in runs if r['run_id'] in primary_ids];assert len(primary)==12 and q['status']=='COMPLETE';assert all(repro['physics_attributes_equal'].values())
 criteria=['All years2026–2040','Browser year selection','Correct compound growth','Vehicle-class growth','OD-specific final rate','15-minute demand intervals','Three scenarios','Versioned custom scenarios','Growth provenance','Missing rates remain missing','Deterministic demand generation','Route/access validation','Actual representative SUMO runs','Requested versus served ledger','SUMO-derived congestion metrics','Censoring/unserved accounting','Fair comparison/parity guard','Sensitivity framework','Internal browser desktop/mobile QA','All M01–M06 regression','Previous source immutability','Reproducible rebuild']
 acceptance=[{'id':i+1,'criterion':c,'status':('PASS' if ui_pass else 'PARTIAL — BROWSER QA') if i in [1,7,18] else 'PASS'} for i,c in enumerate(criteria)]
 status={'technical_projection_engine':technical,'empirical_forecast_validity':'BLOCKED — BASELINE AND GROWTH EVIDENCE REQUIRED','baseline_status':'2026 PROVISIONAL — NOT EMPIRICALLY CALIBRATED','years_supported':list(range(2026,2041)),'observed_baseline_activated':False,'M08_started':False,'initial_regression_tests':182,'final_regression_tests':n,'original_files_checked':protected,'browser_qa':browser.get('status'),'acceptance':acceptance}
 save(DOC/'status.json',status)
 demand=[]
 for y in [2026,2030,2035,2040]:demand.append('| '+str(y)+' | '+' | '.join(str(load(ROOT/f'simulation/projections/m07/{s}-{y}.json')['requested']) for s in ['LOW','REFERENCE','HIGH'])+' |')
 rates=[]
 for cls in [v['id'] for v in load(ROOT/'configuration/demand-m04/vehicle-registry.json')['vehicles']]:rates.append('| '+cls+' | '+' | '.join(f"{next(r['schedule']['rate'] for r in load(ROOT/f'configuration/growth-m07/{s}.json')['rules'] if r['vehicle_class']==cls and r['od_relation']=='*')*100:g}%" for s in ['LOW','REFERENCE','HIGH'])+' |')
 runrows='\n'.join(f"| {r['year']} | {r['scenario']} | {r['network_variant']} | {r['seed']} | {r['requested']} | {r['routable']} | {r['failed_routes']} | {r['loaded']} | {r['departed']} | {r['arrived']} | {r['running_at_end']} | {r['not_departed']} | {r['max_stopped_count']} | {r['max_lane_queue_extent_m']:.2f} |" for r in sorted(primary,key=lambda r:(r['year'],r['scenario'],r['network_variant'],r['seed'])))
 benchmark='\n'.join(f"| {r['year']} {r['scenario']} {r['network_variant']} seed{r['seed']} | {r['wall_seconds']:.2f} | {r['sumo_cpu_seconds'] or 0:.2f} | {r['sumo_peak_working_set_bytes_sampled']/1048576:.2f} |" for r in primary)
 dims=['vehicle_class','od_id','interval_start'];breakdowns=[]
 for dim in dims:
  keys=sorted({c[dim] for c in load(ROOT/'simulation/projections/m07/REFERENCE-2026.json')['cells']})
  table='\n'.join('| '+str(k)+' | '+' | '.join(str(sum(c['count'] for c in load(ROOT/f'simulation/projections/m07/REFERENCE-{y}.json')['cells'] if c[dim]==k)) for y in [2026,2030,2035,2040])+' |' for k in keys)
  breakdowns.append(f'### {dim}\n\n| Group | 2026 | 2030 | 2035 | 2040 |\n|---|---:|---:|---:|---:|\n{table}\n')
 failures=[{'folder':str(p.parent.relative_to(ROOT)),'error':load(p)['error']} for p in (ROOT/'simulation/runs/m07').glob('*/failure.json')];save(DOC/'failure-audit.json',failures)
 guards='\n'.join(f"| {a['id']} | {a['criterion']} | {a['status']} |" for a in acceptance)
 screenshot_text='\n'.join(f'![{p.stem}](m07/{p.name})' for p in DOC.glob('browser-*.jpg')) or 'Screenshot M07 belum tersedia karena internal browser QA terhambat. Screenshot milestone lama tidak digunakan sebagai bukti M07.'
 report=f'''# MILESTONE 07 — Gedangan Traffic Growth Projection 2026–2040

Tanggal:31 Oktober2026, Asia/Jakarta. Lingkup hanya M07. M08 belum dimulai.

## Executive summary dan dua status acceptance

**TECHNICAL PROJECTION ENGINE: {technical}.**

**EMPIRICAL FORECAST VALIDITY: BLOCKED — BASELINE AND GROWTH EVIDENCE REQUIRED.**

{CONDITIONAL}. {LABEL}. Seluruh angka di bawah adalah conditional scenario projection dan keluaran model, bukan prakiraan resmi atau pengukuran Gedangan. Baseline M06 tetap BLOCKED. Tahun2026–2040 semuanya didukung;45tabel demand LOW/REFERENCE/HIGH tersedia. SUMO1.28.0 benar-benar dijalankan untuk2026/2030/2035/2040 pada jaringan aktual, kedua arah, beberapa kelas kendaraan dan beberapa seed. Tidak ada M08 infrastructure change.

## Audit awal dan source preservation

Initial regression182testsOK. Final regression{n}testsOK. Baseline SHA256 M07 melindungi{protected}file M01–M06:source,config,geodata,network,demand,hasil dan laporan. Dependency/cache/dist/vendor dikecualikan dari snapshot M07; binarytoolchain dan manifest lama diperiksa melalui tests/manifest masing-masing. Pemeriksaan akhir tidak menemukan perubahan pada protectedfiles. M06status historis dan reports tetap utuh; tidak ditulis ulang agar tampak maju.

Laporan M04/M04.5/M05/M05.1/M06, governance/architecture/roadmap, registry/OD, actual corrected policy, network M051, signal/railway/queue modules, causal detector, observation schemas dan empiricalgate diperiksa. Primary network adalah M051Provisional hash{next(r for r in primary if r['network_variant']=='pilot-provisional')['network_sha256']};lihat individual manifests untuk setiap variant. M051copy tetap byte-identical model M05; stopline/clearance belum disurvei.

## Source audit dan provenance pertumbuhan

M06 public-source register dihash dan dipakai sebagai konteks, bukan diubah. Audit baru:

- [Dishub inventory portal](https://opendata.sidoarjokab.go.id/dataset/data-inventarisasi-dan-analisis-situasi-arus-lalu-lintas) mempunyai resource2023–2025. [Actual CKAN resource](https://opendata.sidoarjokab.go.id/dataset/data-inventarisasi-dan-analisis-situasi-arus-lalu-lintas/resource/c6ac3f3e-ed21-43b3-a929-6df9b628e593) dan API berhasil diperiksa: unit **Dokumen**, records30/0/0. Ini jumlah dokumen administrasi, bukan arus kendaraan; tidak dibuat traffic-growthrate. No License Provided tetap dicatat.
- [BPS Jawa Timur registered-vehicle table](https://jatim.bps.go.id/id/statistics-table/3/VjJ3NGRGa3dkRk5MTlU1bVNFOTVVbmQyVURSTVFUMDkjMyMzNTAw/jumlah-kendaraan-bermotor-menurut-kabupaten-kota-dan-jenis-kendaraan-di-provinsi-jawa-timur-unit-.html?year=2024): stock kendaraan terdaftar menurut kabupaten/kota, bukan corridor flow. Akses langsung403; nilai tidak diekstrak. Perbedaan title/queryyear dicatat sebagai keterbatasan, bukan ditebak.
- [BPS/Bina Marga LHR2024 metadata](https://sirusa.web.bps.go.id/metadata/kegiatan/ea59d0d3-08ed-ec86-2234-72ce7e359071): kegiatan kompilasi average daily two-direction traffic, cakupan subsetJatim; Sidoarjo tidak tercantum pada daftar yang diperiksa. Metadata bukan raw time-series Gedangan atau annual class-growth evidence.

Tidak ditemukan verified local traffic growth yang eligible. Tidak ada fallback nasional/provinsi, penduduk atau pertumbuhan ekonomi menjadi corridor growth. `source-register.json` menyimpan URL,title,publisher,publicationdate asli/unknown,measurementperiod,classification,geographicscope,originalmetric,derivedrate=null,limitations,confidence,snapshot/hash atau errorunduhan. Simulasi berjalan offline setelah input tersedia.

## Baseline adapter dan metode pertumbuhan

Adapter A=PROVISIONAL_SYNTHETIC_BASELINE. Baseline240requests/two15min berasal dari konfigurasi software M04medium120/interval dan composition M04, dengan ODweights eksplisit. Ini bukan volume riil. Joint largest-remainder allocation berarti composition integer aktual sedikit berbeda dari fractional starting shares; breakdown disajikan di bawah.

Adapter B=EMPIRICALLY_CALIBRATED_BASELINE tetap diblokir M06gate. `m07_baseline_adapter.resolve` menyiapkan contractbundle yang mempertahankan OD,cells,window,day,provenance,observationhash dan reviewevidence. B tidak dapat diaktifkan hanya dengan mengubah nama, year atau satu flaginput. Gate M06 dan configuredempiricalbaseline, verifiedobservations, reviewed/independentvalidation dan evidencehash harus sesuai. Belum ada bundle empiris yang diaktifkan atau diuji sebagai fakta.

Rumus utama:

`D(y,OD,class,interval) = D(2026,OD,class,interval) × PRODUCT(1+r[t,OD,class]), t=2027..y`.

2026factor=1;2027satu aplikasi rate. Constant,piecewise,year-specific,zero dan negativegrowth tersedia. Priorityresolution:verifiedOD/class,verifiedclass pada scope sama,explicitOD/classassumption,explicitclassassumption; missing/ambiguity ditolak. Satu finalrate dipilih, tidak mengalikan classgrowth dengan ODgrowth lagi. Wrongscope tidak silentlyfallthrough ke nationalstockgrowth.

### Class-wide annual assumptions

Semua nilai tabel adalah **SYNTHETIC ILLUSTRATIVE ASSUMPTION / M07-ASSUMPTION-01**, editable, bukan rekomendasi pertumbuhan Gedangan. Envelope−95%..+20% adalah batas software konservatif untuk konfigurasi contoh, bukan prior empiris.

| Class | LOW | REFERENCE | HIGH |
|---|---:|---:|---:|
{chr(10).join(rates)}

ODoverride motorcycle northbound adalah finalannualrate LOW0%,REFERENCE4%,HIGH7%, menggantikan class-wide motorcycle rate. Contoh independentformula REFERENCE NBmotor2030factor=1.04^4, bukan1.04^4×1.025^4. Setiap cell mempunyai resolved annualschedule,ruleID,provenance dan factor. REFERENCE adalah nama skenario, bukan label resmi/probabilitas.

## OD, interval, integer allocation dan demonstrasi pemilihan tahun

M04ODanchors dipertahankan untuk northbound Sidoarjo→Surabaya, southbound, feeders, frontagecontinuity/access, Gedanganjunction, stationjunction danlocal. Source-connected Ketajencrossing berasal dari probe M05 yang sudah ada, tanpa koneksi/geometri baru; Strictendpoint tidak tersedia dan tetap gagal. Frontage paralel terpisah. Observasi awal pengguna bahwa frontage relatif lancar adalah konteks belum terukur; tidak dijadikan synthetic congestion cause atau fakta terkalibrasi.

| Year | LOW requests | REFERENCE requests | HIGH requests |
|---:|---:|---:|---:|
{chr(10).join(demand)}

REFERENCE240→269→311→360 adalah perubahan yang dihitung engine, bukan multiplier visual manual. Semua15tahun dihitung dari baseline2026 yang sama. Profilebaseline dua interval0–900/900–1800s dipertahankan; day=ILLUSTRATIVE_DAY, bukan jam puncak lapangan. Explicitprofileoverride75/25 tersedia dan diuji sebagai sensitivitas tambahan, bukan klaim peakspreading.

Global half-up rounding dari totalfractional, kemudian largestremainder acrossOD/class/interval dengan lexicalstableties. Jumlahclass=jumlahOD=jumlahinterval=totalinteger. Errorpembulatan eksplisit perproyeksi. No randomrounding. Departure stratifiedjitter memakai seed; IDs stable dan unik dalam run; IDs yang sama antar pairedseed sengaja merepresentasikan cohortyangsama, bukan collision di satuSUMOrun.

{chr(10).join(breakdowns)}

## Actual SUMO routing, lifecycle dan congestion

DUAROUTER repair=false, ignore-errors=true hanya agar batch tetap dilanjutkan; setiap request hilang dari outputrouter direkonsiliasi sebagai failure, tidak dibuang. SourceOSMconditional/access/oneway/turn, laneconnection, roadfunction,width/dimension/load dan trailerdeflection screens diwarisi dari M04.5. Tidak ada ignoringvClass, speed/positionoverride, newconnection atau requestdipindah keODlain. Oversize tetap explicitNOT_ROUTABLE. HeavyProvisional adalah asumsi model, bukan izin legal fisik.

Primary comparison memakai network/control yang sama: M051Provisional, synthetic signals, trains70/970s, openingassumptions lama, registryyangsama. Demandwindow0–1800s,measurementhorizon0–2100s,step0.5s,warmup0,optionaldrain0. Tidak ada penambahanhorizon diam-diam. Teleport **explicitly disabled(time-to-teleport=-1)** untuk seluruh M07; berbeda dari default lama dan terdokumentasi. Antrean/gridlock tidak dihapus agar semua kendaraan tiba.

| Year | Scenario | Network | Seed | Requested | Routable | Failed | Loaded | Departed | Arrived | Running | Notdeparted | Maxstopped | Maxlaneextent m |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{runrows}

Accounting:requested=failedroutes+arrived+running+notdeparted; routable=departed+notdeparted;departed=arrived+running. Loaded,moved dan actual pending insertion tersimpan. Initial getLoadedIDList telemetry melewatkan event awal: derived loaded count direkonsiliasi dari terminal SUMO summary minus actual train tripinfo. `lifecycle-audit.json` menyimpan nilai logger mentah, corrected loaded, source hashes, serta pemeriksaan inserted/arrived/discarded. Raw result.json dan physics output tidak ditimpa. SUMO1.28.0 tripinfo **write-unfinished/write-undeparted** diparse dan harus mempunyai record untuk setiap acceptedrequest. XMLdepart/arrival−1 dibandingkan dengan actualTraCIsets. Tidak menganggap running/notdeparted sebagai perjalanan selesai.

PerOD disediakan completedtripduration(arrived-only, label eksplisit), elapsedduration/waiting/timeloss bagi seluruh departed termasuk unfinished, dan departDelay acceptedcohort termasukundeparted. Tidak ada complete-cohort meantravel-time palsu untuk semua request. `supplementary-audits.json` memakai actualFCD untuk speeddistribution/histogram seluruh activevehicles, segment-rolebreakdown dan laneoccupancyfullhorizon termasukemptysamples. Occupancy adalah clippedunion front-assignedbodyfootprints; bodymelintasedge lain tidak direkonstruksi.

Queue count berbeda dari meterextent. Extent body-inclusive maxfront−mintail perlane; maximumstoppedcount adalah jumlahstoppedroadvehicles pada sampel1s, bukan satu physicalqueue. Durasi adalah lane-seconds dengan antrean terdeteksi1ssamples. Extent model sekitar shortlanes/stoplines belum physicallyvalidated. Entryinsertionpending dan horizonrunning tetap warning **DEMAND EXCEEDS INSERTION OR NETWORK CAPACITY** pada model ini, bukan bukti kapasitas Gedangan riil.

## Railway, spillback dan segment analysis

Actualtraintripinfo,FCDmovement IDs dan crossingroadlinkstatewindows ada pada supplementaryaudit. Trainplanneddepartures dibedakan dari actualtripinfo. Closure adalah statusroadlinks model, bukan fieldgate telemetry. Stoppedvehicle-seconds dekat crossingred adalah asosiasikonteks, bukan incrementalcausalraildelay. Queue recovery causal dibuktikan hanya jika M051detector menemukan storage release dan vehiclemovementyangsesuai; kasus tanpa bukti tetap candidate/unresolved.

Detector M051 dipakai tanpa mengubah definisi:vehicle-specific nextLinks priority/open/foe, fullFCDfootprints, legalmovement, continuousblocking dan recovery. Verified-in-model events tidak disebut fieldvalidated. Candidates tidak dinaikkan otomatis menjadi spillback. `causal-events.json`,classification-summary danpriority-trace tersimpan di setiap run. Frontage,feeder,Gedangan,NB,SB,station/Ketajen dibaca melalui actualOD/role metrics, bukan animasi acak.

## Fair comparisons, sensitivity dan uncertainty

`comparison.json` memeriksa networkhash,baselinehash,seed,window dancontroloptions. Differencecontrol/network diberi NOTCOMPARABLE_AS_PURE_GROWTH; perubahan meanarrivedonly saatcensored tidak ditampilkan sebagai peningkatankinerja. Demand,throughput,queuecount,extent danspillbackdelta tersimpan. Failedroutecohort tetap warning meskipun semua routable tiba. LOW/REFERENCE/HIGH bukan confidenceinterval.

Burst stress dua kali baseline mencapai batas driver180s dan dicatat FAILED_RESOURCE_BUDGET tanpa completed traffic metrics; main HIGH2040 tetap memberi bukti censoring pada horizon penuh. Run yang terputus saat restart Codex diarsipkan terpisah, lalu dilanjutkan dari cache run yang selesai.

Sensitivity terpisah mencakup growth scenario,classmix/baselinetotal,ODdistribution,explicitdepartureprofile,rarequency,signaloff,behaviorheadwayproxy danboundedburststress. Mixing/headwayproxy tidak disebut estimasi physicalroadcapacity. Capacityuncertainty asli tetap structuralblocker; tidak ada pelebaranjalan atau perubahaninfrastruktur. Lihat `sensitivity.json` untuk request/served/censoring dan confounds setiap run. Seed42/43 merupakan simulationrandomness, bukan pengganti uncertaintybaseline/OD/growth/geometry.

## Performance, failures dan reproducibility

Sequentialconcurrency1. Primary12runs ditambah sensitivity/freshreproduction; cache berdasarkan projection/source/config/network/seed/options hashes. Runstatus,manifest,requestledger,routerstderr,tripinfo/FCD dan failureevidence dipertahankan. Cachehit memverifikasi hashcoreoutputs; supplementaryaudit adalah derivasi terpisah. Actualfreshreplay numerictripinfo/FCD parity={repro['physics_attributes_equal']}; cachemanifest tidak berubah={repro['cache_output_manifest_unchanged']}. Tidak ada FPS/GPUbenchmark diklaim.

| Actual run | Wall s | SUMO CPU s | Sampled peak SUMO RAM MiB |
|---|---:|---:|---:|
{benchmark}

Resourcecounter adalah processSUMO Windows, bukan wholemachineRAM/VRAM; puncak disampling1ssimulationinterval. Wall mencakup driver/causalanalysis dan tidak sama dengan CPUSUMO. Initialfailure tambahanXMLschema direkam, lalu diperbaiki dengan localadditional_file.xsd. Semua failurefolders tetap pada `failure-audit.json`; tidak dipakai sebagai completedtrafficmetric.

## Internal browser dan testing

Browser status: {browser.get('status')}. Detail:{browser.get('reason','Lihat browser-qa.json untuk actions, viewport dan result checks.')}. Halaman M07 terpisah port5182/API8772, hanyaloopback. Demandcalculation read-onlyGET; savecustom/run memakai validatedPOST. NoCORS wildcard, exactHost/Origin, boundedbodydanrunqueue. Skenario yang belum disimulasikan menampilkan NOTRUN, bukan queue/speed/TT rekaan. Runbutton benar-benar mengantrekan runnerlokal, cachedresults memakai verifiedhashes. Saat offlineexperiment aktif, interactivejob harus menunggu.

UI menyediakan semua15tahun/preset,scenarios/customeditor,OD/class/intervaldashboard,geographicrecordedplayback,playpause/speed/timeline/zoom/layers,comparison/provenance/uncertainty. Playback hanyaactualSUMO5ssamples, tanpa randommotion. Tidak mengklaim mobile/desktopPASS bila verifikasi belum selesai.

{screenshot_text}

Initial182regression dipertahankan. Final{n}testsOK meliputi independentDecimal/piecewise/year-specific calculations,negative/zero/missing/provenance/scope/ODsubstitution,integer/tie/conservation/seedIDs,actualroutes/FCDpermissions,oversize/frontage/Strict,completecensoredledger,stress,cachefreshreplay,sourceimmutability dan empiricalgate. TypeScriptnoEmit dan ViteproductionbuildPASS. SUMO-GUI M07 tidak dijalankan; buktiGUI milestonelama tidak dipresentasikan sebagai M07.

## Technical acceptance — 22 kriteria

| No | Kriteria | Status |
|---:|---|---|
{guards}

## Empirical acceptance, unresolved issues dan M08 readiness

Seluruh enam prasyarat empiricalforecast masih BLOCKED:baseline2026empiricalcalibration,relevantlocalgrowth,verifiedOD/composition,geometry/controlfitness,independentvalidation,defensibleforecastuncertainty. Tidak ada klaim FULLPASS ilmiah.

Knownblockers diwarisi:crossingendpoint~1.6m/laneshapehingga7.178m,shortlanes~0.10m,stopsurvey/clearance/heavylegalitasbelumada,Strictgaps,syntheticsignals/trains,unverifiedOD/vehicleparameters. Missingfielddata tidak ditutupi optimizer atau growthassumptions. HIGHcensoring bukan error yang disembunyikan dan bukan prakiraankemacetan nyata. InternalbrowserQA yang belum selesai tetap isu teknis, bukan bukti keberhasilan.

M08 **tidak dimulai**. Untuk melanjutkan pekerjaan M08 diperlukan persetujuan pengguna. Kajian crediblefutureforecast juga membutuhkan baselineobservations2026,multi-yearlocalclass/ODflowevidence,control/geometryreview,independentvalidation dan acceptancejustification yang sesuai tujuan studi.
'''
 # Improve generated prose without touching paths or machine-readable identifiers.
 fixes={'31 Oktober2026':'31 Oktober 2026','45tabel':'45 tabel','SUMO1.28.0':'SUMO 1.28.0','untuk2026/2030/2035/2040':'untuk 2026/2030/2035/2040','182testsOK':'182 tests OK','testsOK':' tests OK','melindungi{protected}file':'melindungi {protected} file','protectedfiles':'protected files','Dependency/cache/dist/vendor':'Dependency, cache, dist, dan vendor','binarytoolchain':'binary toolchain','stockkendaraan':'stock kendaraan','verified local traffic growth':'verified local traffic growth','No License Provided':'No License Provided','derivedrate=null':'derived rate=null','errorunduhan':'error unduhan','240requests/two15min':'240 requests / two 15-minute','M04medium120/interval':'M04 medium 120/interval','composition M04':'composition M04','ODweights':'OD weights','Joint largest-remainder':'Joint largest remainder','contractbundle':'contract bundle','provenance,observationhash':'provenance, observation hash','reviewevidence':'review evidence','configuredempiricalbaseline':'configured empirical baseline','verifiedobservations':'verified observations','independentvalidation':'independent validation','evidencehash':'evidence hash','2026factor=1;2027satu':'2026 factor=1; 2027 satu','Constant,piecewise,year-specific,zero':'Constant, piecewise, year-specific, zero','negativegrowth':'negative growth','Priorityresolution':'Priority resolution','verifiedOD/class':'verified OD/class','verifiedclass':'verified class','explicitOD/classassumption':'explicit OD/class assumption','explicitclassassumption':'explicit class assumption','finalrate':'final rate','classgrowth':'class growth','ODgrowth':'OD growth','Wrongscope':'Wrong scope','silentlyfallthrough':'silently fall through','nationalstockgrowth':'national stock growth','ODoverride':'OD override','finalannualrate':'final annual rate','class-wide motorcycle rate':'class-wide motorcycle rate','independentformula':'independent formula','NBmotor2030factor':'NB motorcycle 2030 factor','northbound Sidoarjo':'northbound Sidoarjo','M04ODanchors':'M04 OD anchors','frontagecontinuity/access':'frontage continuity/access','Gedanganjunction':'Gedangan junction','stationjunction danlocal':'station junction dan local','Ketajencrossing':'Ketajen crossing','Strictendpoint':'Strict endpoint','synthetic congestion cause':'synthetic congestion cause','Profilebaseline':'Profile baseline','Explicitprofileoverride75/25':'Explicit profile override 75/25','peakspreading':'peak spreading','totalfractional':'total fractional','acrossOD/class/interval':'across OD/class/interval','lexicalstableties':'lexical stable ties','Jumlahclass=jumlahOD=jumlahinterval=totalinteger':'Jumlah class = jumlah OD = jumlah interval = total integer','Errorpembulatan':'Error pembulatan','perproyeksi':'per proyeksi','randomrounding':'random rounding','stratifiedjitter':'stratified jitter','pairedseed':'paired seed','cohortyangsama':'cohort yang sama','satuSUMOrun':'satu SUMO run','SourceOSMconditional/access/oneway/turn':'Source OSM conditional/access/oneway/turn','laneconnection':'lane connection','roadfunction':'road function','trailerdeflection':'trailer deflection','ignoringvClass':'ignoring vClass','speed/positionoverride':'speed/position override','newconnection':'new connection','requestdipindah':'request dipindah','keODlain':'ke OD lain','explicitNOT_ROUTABLE':'explicit NOT_ROUTABLE','HeavyProvisional':'Heavy Provisional','M051Provisional':'M051 Provisional','trains70/970s':'trains 70/970s','openingassumptions':'opening assumptions','registryyangsama':'registry yang sama','Demandwindow':'Demand window','measurementhorizon':'measurement horizon','step0.5s,warmup0,optionaldrain0':'step 0.5s, warmup 0, optional drain 0','penambahanhorizon':'penambahan horizon','requested=failedroutes+arrived+running+notdeparted':'requested = failed routes + arrived + running + not departed','routable=departed+notdeparted;departed=arrived+running':'routable = departed + not departed; departed = arrived + running','acceptedrequest':'accepted request','actualTraCIsets':'actual TraCI sets','PerOD':'Per OD','completedtripduration':'completed trip duration','elapsedduration/waiting/timeloss':'elapsed duration / waiting / time loss','acceptedcohort':'accepted cohort','complete-cohort meantravel-time':'complete cohort mean travel time','speeddistribution/histogram':'speed distribution/histogram','activevehicles':'active vehicles','segment-rolebreakdown':'segment role breakdown','laneoccupancyfullhorizon':'lane occupancy full horizon','includingemptysamples':'including empty samples','Queue count berbeda dari meterextent':'Queue count berbeda dari meter extent','body-inclusive maxfront−mintail perlane':'body-inclusive max(front) − min(tail) per lane','maximumstoppedcount':'maximum stopped count','stoppedroadvehicles':'stopped road vehicles','physicalqueue':'physical queue','lane-seconds':'lane seconds','terdeteksi1ssamples':'terdeteksi pada sampel 1s','shortlanes/stoplines':'short lanes / stop lines','physicallyvalidated':'physically validated','Entryinsertionpending':'Entry insertion pending','horizonrunning':'horizon running','Actualtraintripinfo,FCDmovement':'Actual train tripinfo, FCD movement','crossingroadlinkstatewindows':'crossing road-link state windows','Trainplanneddepartures':'Train planned departures','actualtripinfo':'actual tripinfo','statusroadlinks':'status road links','fieldgate':'field gate','Stoppedvehicle-seconds':'Stopped vehicle-seconds','crossingred':'crossing red','asosiasikonteks':'asosiasi konteks','incrementalcausalraildelay':'incremental causal rail delay','M051detector':'M051 detector','vehiclemovementyangsesuai':'vehicle movement yang sesuai','fullFCDfootprints':'full FCD footprints','legalmovement':'legal movement','continuousblocking':'continuous blocking','fieldvalidated':'field validated','Frontage,feeder,Gedangan,NB,SB,station/Ketajen':'Frontage, feeder, Gedangan, NB, SB, station/Ketajen','actualOD/role':'actual OD/role','Differencecontrol/network':'Perbedaan control/network','meanarrivedonly saatcensored':'mean arrived-only saat censored','peningkatankinerja':'peningkatan kinerja','Failedroutecohort':'Failed route cohort','rarequency':'rail frequency','classmix/baselinetotal':'class mix/baseline total','ODdistribution':'OD distribution','explicitdepartureprofile':'explicit departure profile','behaviorheadwayproxy':'behavior headway proxy','boundedburststress':'bounded burst stress','physicalroadcapacity':'physical road capacity','Capacityuncertainty':'Capacity uncertainty','structuralblocker':'structural blocker','pelebaranjalan':'pelebaran jalan','perubahaninfrastruktur':'perubahan infrastruktur','Seed42/43':'Seed 42/43','simulationrandomness':'simulation randomness','Sequentialconcurrency1':'Sequential concurrency 1','Primary12runs':'Primary 12 runs','Cachehit':'Cache hit','hashcoreoutputs':'hash core outputs','supplementaryaudit':'supplementary audit','Actualfreshreplay':'Actual fresh replay','numerictripinfo/FCD':'numeric tripinfo/FCD','Resourcecounter':'Resource counter','processSUMO':'process SUMO','wholemachineRAM/VRAM':'whole-machine RAM/VRAM','CPU SUMO':'CPU SUMO','Initialfailure':'Initial failure','tambahanXMLschema':'tambahan XML schema','localadditional_file.xsd':'local additional_file.xsd','failurefolders':'failure folders','completedtrafficmetric':'completed traffic metrics','NoCORS':'No CORS','exactHost/Origin':'exact Host/Origin','boundedbodydanrunqueue':'bounded body dan run queue','NOTRUN':'NOT RUN','Runtime':'Runtime','Runbutton':'Run button','runnerlokal':'runner lokal','cachedresults':'cached results','verifiedhashes':'verified hashes','offlineexperiment':'offline experiment','interactivejob':'interactive job','M07 terpisah port5182/API8772':'M07 terpisah port 5182 / API 8772','semua15tahun':'semua 15 tahun','OD/class/intervaldashboard':'OD/class/interval dashboard','geographicrecordedplayback':'geographic recorded playback','actualSUMO5ssamples':'actual SUMO 5s samples','randommotion':'random motion','TypeScriptnoEmit':'TypeScript noEmit','ViteproductionbuildPASS':'Vite production build PASS','SUMO-GUI M07':'SUMO-GUI M07','milestonelama':'milestone lama','Seluruh enam prasyarat empiricalforecast':'Seluruh enam prasyarat empirical forecast','Knownblockers':'Known blockers','Missingfielddata':'Missing field data','growthassumptions':'growth assumptions','HIGHcensoring':'HIGH censoring','prakiraankemacetan':'prakiraan kemacetan','InternalbrowserQA':'Internal browser QA','baselineobservations2026':'baseline observations 2026','multi-yearlocalclass/ODflowevidence':'multi-year local class/OD flow evidence','acceptancejustification':'acceptance justification'}
 fixes.update({'Tanggal:31':'Tanggal: 31','Tahun2026':'Tahun 2026',';45 tabel':'; 45 tabel','regression182':'regression 182','regression234':'regression 234','melindungi2820file':'melindungi 2820 file','M01–M06:source,config,geodata,network,demand,hasil':'M01–M06: source, config, geodata, network, demand, hasil','M06status':'M06 status','empiricalgate':'empirical gate','hash0b470':'hash 0b470',';lihat':'; lihat','M051copy':'M051 copy','stopline/clearance':'stop line/clearance','resource2023':'resource 2023','records30':'records 30','traffic-growthrate':'traffic growth rate','langsung403':'langsung 403','title/queryyear':'title/query year','LHR2024':'LHR 2024','subsetJatim':'subset Jawa Timur','URL,title,publisher,publicationdate asli/unknown,measurementperiod,classification,geographicscope,originalmetric,derived rate=null,limitations,confidence,snapshot/hash':'URL, title, publisher, publication date asli/unknown, measurement period, classification, geographic scope, original metric, derived rate=null, limitations, confidence, snapshot/hash','Baseline240':'Baseline 240','M06gate':'M06 gate','OD,cells,window,day,provenance':'OD, cells, window, day, provenance','flaginput':'flag input','resolution:verified':'resolution: verified',',verified':', verified',',explicit':', explicit','Envelope−95%':'Envelope −95%','LOW0%,REFERENCE4%,HIGH7%':'LOW 0%, REFERENCE 4%, HIGH 7%','Setiap cell mempunyai resolved annualschedule,ruleID,provenance':'Setiap cell mempunyai resolved annual schedule, rule ID, provenance','120→':'120 →','240→269→311→360':'240 → 269 → 311 → 360','dua interval0':'dua interval 0','0–900/900–1800s':'0–900 / 900–1800s','15menit':'15 menit','routable tiba':'routable tiba','Initial182regression':'Initial 182 regression','Final234':'Final 234','sourceimmutability':'source immutability','empiricalgate':'empirical gate','year-specific calculations':'year-specific calculations','independentDecimal/piecewise':'independent Decimal/piecewise','negative/zero/missing/provenance/scope/ODsubstitution':'negative/zero/missing/provenance/scope/OD substitution','actualroutes/FCDpermissions':'actual routes/FCD permissions','completecensoredledger':'complete censored ledger','cachefreshreplay':'cache fresh replay','baseline2026empiricalcalibration,relevantlocalgrowth,verifiedOD/composition,geometry/controlfitness,independent validation,defensibleforecastuncertainty':'baseline 2026 empirical calibration, relevant local growth, verified OD/composition, geometry/control fitness, independent validation, defensible forecast uncertainty','crossingendpoint~1.6m/laneshapehingga7.178m,shortlanes~0.10m,stopsurvey/clearance/heavylegalitasbelumada,Strictgaps,syntheticsignals/trains,unverifiedOD/vehicleparameters':'crossing endpoint sekitar 1.6m / lane shape hingga 7.178m, short lanes sekitar 0.10m, stop-line survey/clearance/legalitas heavy belum tersedia, Strict gaps, synthetic signals/trains, unverified OD/vehicle parameters','45demand':'45 demand','12primary':'12 primary','tahun2026':'tahun 2026','seeds42/43':'seeds 42/43','seed42':'seed 42','maksimum2500request':'maksimum 2500 request','time180s':'time 180s','port8772':'port 8772','software fixture M04':'software fixture M04'})
 for a,b in fixes.items():report=report.replace(a,b)
 (ROOT/'documentation/MILESTONE_07_REPORT.md').write_text(report,encoding='utf-8')
 readme=r'''# M07 Projection Lab — penggunaan lokal

M07 saja. Semua proyeksi kondisional, bukan prakiraan empiris tervalidasi. M08 belum dimulai.

## Membuka aplikasi

Dari root proyek, jalankan `START_PROJECTION_M07.bat`. UI: http://127.0.0.1:5182/projection.html. API hanya loopback, port8772. Launcher memeriksa kedua layanan sebelum membuka halaman. Viewer M01–M06 dan launchernya tidak diubah.

Pilih tahun2026–2040 dan LOW/REFERENCE/HIGH. Demand langsung dihitung, tetapi metrik lalu lintas hanya muncul setelah actual SUMO run. Kombinasi yang belum disimulasikan menampilkan NOT RUN. Growth editor mengubah laju tahunan konstan dan menyimpan CUSTOM dengan ID/hash baru; preset tidak ditimpa. Konfigurasi JSON juga mendukung piecewise dan year-specific schedules.

Primary precompute:2026/2030/2035/2040 REFERENCE seeds42/43;2040 LOW/HIGH seed42;2026 Strict dan M04.5 Provisional. UI dapat mengantrekan kombinasi lain melalui tombol Run. Satu worker SUMO, maksimum2500request/run dan batas wall time180s. Jangan menjalankan rebuild offline bersamaan dengan interactive job. Resource-bound failure tetap dicatat, tanpa hasil trafik rekaan.

## Rebuild dan audit

Jalankan `REBUILD_PROJECTION_M07.bat`. Tahap berurutan:scenario initialization,45demand projections,12primary SUMO jobs, sensitivity, fresh reproduction, audit/export, regression, TypeScript dan production build, lalu laporan. Cache memverifikasi source/config/network/seed dan core-output hashes. File tambahan audit dapat dihitung ulang; network dan output milestone lama tidak diubah.

Folder utama:

- `configuration/growth-m07/`:LOW/REFERENCE/HIGH,versioned CUSTOM,baseline adapter dan launcher helper.
- `simulation/projections/m07/`:setiap cell OD/class/15menit, fractional count,integer allocation,annual schedule dan provenance.
- `simulation/runs/m07/`:actual request/route/failure ledger,XML,tripinfo,FCD,priority trace,causal events,playback,process logs dan manifests.
- `documentation/m07/`:source audit,run summary,comparisons,sensitivity,reproduction,tests,browser QA dan hashes.
- `documentation/MILESTONE_07_REPORT.md`:hasil serta acceptance teknis dan empiris terpisah.

Rumus final rate:baseline(2026,OD,class,interval) × PRODUCT(1+r[2027..year]). Final OD/class rate menggantikan class-wide rate; tidak dikalikan dua kali. Missing/ambiguous rate adalah error, bukan fallback0. Integer total memakai global half-up dan largest remainder dengan stable lexical ties. Seed mengatur departure jitter, bukan menutupi selisih pembulatan.

## Batas ilmiah dan simulasi

Baseline240request/two15min berasal dari software fixture M04, bukan volume Gedangan. Seluruh growth rate demo adalah SYNTHETIC ILLUSTRATIVE ASSUMPTION. Registered vehicle stock, populasi, ekonomi atau jumlah dokumen tidak menjadi local traffic growth secara otomatis.

Jaringan dan kontrol utama tetap M05.1 Provisional. Fixed demand window0–1800s, horizon2100s,step0.5s,warmup0,no optional drain. Teleport=-1 dinyatakan eksplisit. Requested=failed routes+arrived+running+notdeparted. Tripinfo unfinished/undeparted tetap diparse. Loaded direkonsiliasi dari actual SUMO summary minus train records; raw initial telemetry dipertahankan di lifecycle audit. Arrived-only travel time tidak mewakili seluruh demand.

Oversize tetap NOT_ROUTABLE; heavy access Provisional bukan legal clearance. Tidak ada perubahan geometry,oneway,turn restrictions atau permission demi meluluskan rute. Queue count dan meter extent terpisah. Crossing/stop-line/short-edge metrics masih memerlukan survei. Signal dan train schedule sintetis; verified-in-model spillback bukan field validation.

Burst stress ekstrem yang melampaui180s berstatus FAILED_RESOURCE_BUDGET, tanpa completed traffic metrics. HIGH2040 primary run tetap menunjukkan censoring pada horizon penuh. Interrupted runs setelah restart diarsipkan, bukan dipresentasikan selesai.

## Penggunaan lanjutan

Public-source refresh bersifat opsional (`python -m backend.gedangan.m07_sources`); runtime simulator tidak memerlukan internet. Future empirical bundle menggunakan `m07_baseline_adapter.resolve` hanya setelah M06gate,approved observations,lineage hash,review evidence dan independent validation benar-benar lolos. Gate sekarang menolak empirical activation. Window baru memerlukan versi runner eksplisit, bukan penambahan horizon diam-diam.

Status browser terakhir dan item QA yang belum selesai ada di `documentation/m07/browser-qa.json`. Screenshot yang ada merupakan bukti saat capture, bukan jaminan QA versi akhir. M08 tetap menunggu persetujuan pengguna.
'''
 for a,b in fixes.items():readme=readme.replace(a,b)
 (ROOT/'documentation/MILESTONE_07_README.md').write_text(readme,encoding='utf-8')
 folders=['configuration/growth-m07','simulation/projections/m07','simulation/runs/m07','documentation/m07','frontend/src/m07','frontend/public/m07','tests/m07'];paths=[p for f in folders for p in (ROOT/f).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['delivery-manifest.json','rebuild-execution.txt','delivery-execution.txt']]
 paths+=list((ROOT/'backend/gedangan').glob('m07_*.py'));paths +=[ROOT/p for p in ['START_PROJECTION_M07.bat','REBUILD_PROJECTION_M07.bat','frontend/projection.html','frontend/vite.projection.config.ts','documentation/MILESTONE_07_REPORT.md','documentation/MILESTONE_07_README.md']]
 save(DOC/'delivery-manifest.json',{'label':LABEL,'python':sys.version,'platform':platform.platform(),'sumo_version':'1.28.0','protected_files':protected,'files':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in paths}})
 print('M07 report:',technical,'tests',n,'empirical forecast BLOCKED',flush=True)
if __name__=='__main__':main()
