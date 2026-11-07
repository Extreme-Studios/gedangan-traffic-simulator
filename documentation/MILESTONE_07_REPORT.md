# MILESTONE 07 — Gedangan Traffic Growth Projection 2026–2040

Tanggal: 31 Oktober 2026, Asia/Jakarta. Lingkup hanya M07. M08 belum dimulai.

## Executive summary dan dua status acceptance

**TECHNICAL PROJECTION ENGINE: PARTIAL — INTERNAL BROWSER QA INCOMPLETE.**

**EMPIRICAL FORECAST VALIDITY: BLOCKED — BASELINE AND GROWTH EVIDENCE REQUIRED.**

PROVISIONAL 2026 BASELINE — CONDITIONAL FORECAST, NOT EMPIRICALLY VALIDATED. ILLUSTRATIVE TRAFFIC PROJECTION — 2026 BASELINE NOT CALIBRATED. Seluruh angka di bawah adalah conditional scenario projection dan keluaran model, bukan prakiraan resmi atau pengukuran Gedangan. Baseline M06 tetap BLOCKED. Tahun 2026–2040 semuanya didukung; 45 tabel demand LOW/REFERENCE/HIGH tersedia. SUMO 1.28.0 benar-benar dijalankan untuk 2026/2030/2035/2040 pada jaringan aktual, kedua arah, beberapa kelas kendaraan dan beberapa seed. Tidak ada M08 infrastructure change.

## Audit awal dan source preservation

Initial regression 182 tests OK. Final regression 234 tests OK. Baseline SHA256 M07 melindungi 2820 file M01–M06: source, config, geodata, network, demand, hasil dan laporan. Dependency, cache, dist, dan vendor dikecualikan dari snapshot M07; binary toolchain dan manifest lama diperiksa melalui tests/manifest masing-masing. Pemeriksaan akhir tidak menemukan perubahan pada protected files. M06 status historis dan reports tetap utuh; tidak ditulis ulang agar tampak maju.

Laporan M04/M04.5/M05/M05.1/M06, governance/architecture/roadmap, registry/OD, actual corrected policy, network M051, signal/railway/queue modules, causal detector, observation schemas dan empirical gate diperiksa. Primary network adalah M051 Provisional hash 0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c; lihat individual manifests untuk setiap variant. M051 copy tetap byte-identical model M05; stop line/clearance belum disurvei.

## Source audit dan provenance pertumbuhan

M06 public-source register dihash dan dipakai sebagai konteks, bukan diubah. Audit baru:

- [Dishub inventory portal](https://opendata.sidoarjokab.go.id/dataset/data-inventarisasi-dan-analisis-situasi-arus-lalu-lintas) mempunyai resource 2023–2025. [Actual CKAN resource](https://opendata.sidoarjokab.go.id/dataset/data-inventarisasi-dan-analisis-situasi-arus-lalu-lintas/resource/c6ac3f3e-ed21-43b3-a929-6df9b628e593) dan API berhasil diperiksa: unit **Dokumen**, records 30/0/0. Ini jumlah dokumen administrasi, bukan arus kendaraan; tidak dibuat traffic growth rate. No License Provided tetap dicatat.
- [BPS Jawa Timur registered-vehicle table](https://jatim.bps.go.id/id/statistics-table/3/VjJ3NGRGa3dkRk5MTlU1bVNFOTVVbmQyVURSTVFUMDkjMyMzNTAw/jumlah-kendaraan-bermotor-menurut-kabupaten-kota-dan-jenis-kendaraan-di-provinsi-jawa-timur-unit-.html?year=2024): stock kendaraan terdaftar menurut kabupaten/kota, bukan corridor flow. Akses langsung 403; nilai tidak diekstrak. Perbedaan title/query year dicatat sebagai keterbatasan, bukan ditebak.
- [BPS/Bina Marga LHR 2024 metadata](https://sirusa.web.bps.go.id/metadata/kegiatan/ea59d0d3-08ed-ec86-2234-72ce7e359071): kegiatan kompilasi average daily two-direction traffic, cakupan subset Jawa Timur; Sidoarjo tidak tercantum pada daftar yang diperiksa. Metadata bukan raw time-series Gedangan atau annual class-growth evidence.

Tidak ditemukan verified local traffic growth yang eligible. Tidak ada fallback nasional/provinsi, penduduk atau pertumbuhan ekonomi menjadi corridor growth. `source-register.json` menyimpan URL, title, publisher, publication date asli/unknown, measurement period, classification, geographic scope, original metric, derived rate=null, limitations, confidence, snapshot/hash atau error unduhan. Simulasi berjalan offline setelah input tersedia.

## Baseline adapter dan metode pertumbuhan

Adapter A=PROVISIONAL_SYNTHETIC_BASELINE. Baseline 240 requests / two 15-minute berasal dari konfigurasi software M04 medium 120/interval dan composition M04, dengan OD weights eksplisit. Ini bukan volume riil. Joint largest remainder allocation berarti composition integer aktual sedikit berbeda dari fractional starting shares; breakdown disajikan di bawah.

Adapter B=EMPIRICALLY_CALIBRATED_BASELINE tetap diblokir M06 gate. `m07_baseline_adapter.resolve` menyiapkan contract bundle yang mempertahankan OD, cells, window, day, provenance, observation hash dan review evidence. B tidak dapat diaktifkan hanya dengan mengubah nama, year atau satu flag input. Gate M06 dan configured empirical baseline, verified observations, reviewed/independent validation dan evidence hash harus sesuai. Belum ada bundle empiris yang diaktifkan atau diuji sebagai fakta.

Rumus utama:

`D(y,OD,class,interval) = D(2026,OD,class,interval) × PRODUCT(1+r[t,OD,class]), t=2027..y`.

2026 factor=1; 2027 satu aplikasi rate. Constant, piecewise, year-specific, zero dan negative growth tersedia. Priority resolution: verified OD/class, verified class pada scope sama, explicit OD/class assumption, explicit class assumption; missing/ambiguity ditolak. Satu final rate dipilih, tidak mengalikan class growth dengan OD growth lagi. Wrong scope tidak silently fall through ke national stock growth.

### Class-wide annual assumptions

Semua nilai tabel adalah **SYNTHETIC ILLUSTRATIVE ASSUMPTION / M07-ASSUMPTION-01**, editable, bukan rekomendasi pertumbuhan Gedangan. Envelope −95%..+20% adalah batas software konservatif untuk konfigurasi contoh, bukan prior empiris.

| Class | LOW | REFERENCE | HIGH |
|---|---:|---:|---:|
| motorcycle | -0.5% | 2.5% | 5.5% |
| car | 0.5% | 3.5% | 6% |
| pickup_van | 0.5% | 3% | 5% |
| minibus | 0% | 1% | 2.5% |
| bus | 0% | 1.5% | 3% |
| light_truck | 1% | 3.5% | 6% |
| medium_truck | 1% | 3% | 5.5% |
| heavy_truck | 1% | 2.5% | 5% |
| trailer | 0.5% | 2.5% | 4.5% |
| oversize | 0% | 0% | 2% |

OD override motorcycle northbound adalah final annual rate LOW 0%, REFERENCE 4%, HIGH 7%, menggantikan class-wide motorcycle rate. Contoh independent formula REFERENCE NB motorcycle 2030 factor=1.04^4, bukan1.04^4×1.025^4. Setiap cell mempunyai resolved annual schedule, rule ID, provenance dan factor. REFERENCE adalah nama skenario, bukan label resmi/probabilitas.

## OD, interval, integer allocation dan demonstrasi pemilihan tahun

M04 OD anchors dipertahankan untuk northbound Sidoarjo→Surabaya, southbound, feeders, frontage continuity/access, Gedangan junction, station junction dan local. Source-connected Ketajen crossing berasal dari probe M05 yang sudah ada, tanpa koneksi/geometri baru; Strict endpoint tidak tersedia dan tetap gagal. Frontage paralel terpisah. Observasi awal pengguna bahwa frontage relatif lancar adalah konteks belum terukur; tidak dijadikan synthetic congestion cause atau fakta terkalibrasi.

| Year | LOW requests | REFERENCE requests | HIGH requests |
|---:|---:|---:|---:|
| 2026 | 240 | 240 | 240 |
| 2030 | 243 | 269 | 295 |
| 2035 | 248 | 311 | 384 |
| 2040 | 252 | 360 | 500 |

REFERENCE240 → 269 → 311 → 360 adalah perubahan yang dihitung engine, bukan multiplier visual manual. Semua15tahun dihitung dari baseline2026 yang sama. Profile baseline dua interval 0–900 / 900–1800s dipertahankan; day=ILLUSTRATIVE_DAY, bukan jam puncak lapangan. Explicit profile override 75/25 tersedia dan diuji sebagai sensitivitas tambahan, bukan klaim peak spreading.

Global half-up rounding dari total fractional, kemudian largestremainder across OD/class/interval dengan lexical stable ties. Jumlah class = jumlah OD = jumlah interval = total integer. Error pembulatan eksplisit per proyeksi. No random rounding. Departure stratified jitter memakai seed; IDs stable dan unik dalam run; IDs yang sama antar paired seed sengaja merepresentasikan cohort yang sama, bukan collision di satu SUMO run.

### vehicle_class

| Group | 2026 | 2030 | 2035 | 2040 |
|---|---:|---:|---:|---:|
| bus | 8 | 8 | 8 | 8 |
| car | 100 | 124 | 136 | 164 |
| heavy_truck | 8 | 8 | 8 | 8 |
| light_truck | 16 | 16 | 28 | 28 |
| medium_truck | 8 | 8 | 12 | 16 |
| minibus | 16 | 16 | 16 | 16 |
| motorcycle | 44 | 49 | 54 | 60 |
| oversize | 8 | 8 | 8 | 8 |
| pickup_van | 24 | 24 | 33 | 44 |
| trailer | 8 | 8 | 8 | 8 |

### od_id

| Group | 2026 | 2030 | 2035 | 2040 |
|---|---:|---:|---:|---:|
| feeder_to_main | 14 | 16 | 20 | 22 |
| frontage_continuity | 32 | 35 | 44 | 46 |
| frontage_exit | 32 | 34 | 43 | 46 |
| gedangan_junction | 14 | 16 | 18 | 22 |
| ketajen_crossing | 10 | 12 | 12 | 16 |
| local_trip | 10 | 12 | 12 | 16 |
| main_to_feeder | 10 | 12 | 12 | 16 |
| northbound | 54 | 60 | 70 | 82 |
| southbound | 54 | 60 | 68 | 78 |
| station_junction | 10 | 12 | 12 | 16 |

### interval_start

| Group | 2026 | 2030 | 2035 | 2040 |
|---|---:|---:|---:|---:|
| 0 | 120 | 135 | 156 | 180 |
| 900 | 120 | 134 | 155 | 180 |


## Actual SUMO routing, lifecycle dan congestion

DUAROUTER repair=false, ignore-errors=true hanya agar batch tetap dilanjutkan; setiap request hilang dari outputrouter direkonsiliasi sebagai failure, tidak dibuang. Source OSM conditional/access/oneway/turn, lane connection, road function,width/dimension/load dan trailer deflection screens diwarisi dari M04.5. Tidak ada ignoring vClass, speed/position override, new connection atau request dipindah ke OD lain. Oversize tetap explicit NOT_ROUTABLE. Heavy Provisional adalah asumsi model, bukan izin legal fisik.

Primary comparison memakai network/control yang sama: M051 Provisional, synthetic signals, trains 70/970s, opening assumptions lama, registry yang sama. Demand window0–1800s,measurement horizon0–2100s,step 0.5s, warmup 0, optional drain 0. Tidak ada penambahan horizon diam-diam. Teleport **explicitly disabled(time-to-teleport=-1)** untuk seluruh M07; berbeda dari default lama dan terdokumentasi. Antrean/gridlock tidak dihapus agar semua kendaraan tiba.

| Year | Scenario | Network | Seed | Requested | Routable | Failed | Loaded | Departed | Arrived | Running | Notdeparted | Maxstopped | Maxlaneextent m |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026 | REFERENCE | corrected-provisional | 42 | 240 | 206 | 34 | 206 | 206 | 187 | 19 | 0 | 2 | 16.50 |
| 2026 | REFERENCE | pilot-provisional | 42 | 240 | 206 | 34 | 206 | 206 | 183 | 23 | 0 | 13 | 51.34 |
| 2026 | REFERENCE | pilot-provisional | 43 | 240 | 206 | 34 | 206 | 206 | 182 | 24 | 0 | 13 | 51.34 |
| 2026 | REFERENCE | pilot-strict | 42 | 240 | 124 | 116 | 124 | 124 | 112 | 12 | 0 | 9 | 51.34 |
| 2030 | REFERENCE | pilot-provisional | 42 | 269 | 235 | 34 | 235 | 235 | 210 | 25 | 0 | 11 | 51.34 |
| 2030 | REFERENCE | pilot-provisional | 43 | 269 | 235 | 34 | 235 | 235 | 210 | 25 | 0 | 12 | 51.34 |
| 2035 | REFERENCE | pilot-provisional | 42 | 311 | 267 | 44 | 267 | 267 | 240 | 27 | 0 | 14 | 51.34 |
| 2035 | REFERENCE | pilot-provisional | 43 | 311 | 267 | 44 | 267 | 267 | 237 | 30 | 0 | 15 | 51.34 |
| 2040 | HIGH | pilot-provisional | 42 | 500 | 444 | 56 | 444 | 436 | 356 | 80 | 8 | 48 | 62.59 |
| 2040 | LOW | pilot-provisional | 42 | 252 | 218 | 34 | 218 | 218 | 194 | 24 | 0 | 12 | 51.34 |
| 2040 | REFERENCE | pilot-provisional | 42 | 360 | 316 | 44 | 316 | 316 | 282 | 34 | 0 | 19 | 51.34 |
| 2040 | REFERENCE | pilot-provisional | 43 | 360 | 316 | 44 | 316 | 316 | 281 | 35 | 0 | 19 | 51.34 |

Accounting:requested = failed routes + arrived + running + not departed; routable = departed + not departed; departed = arrived + running. Loaded,moved dan actual pending insertion tersimpan. Initial getLoadedIDList telemetry melewatkan event awal: derived loaded count direkonsiliasi dari terminal SUMO summary minus actual train tripinfo. `lifecycle-audit.json` menyimpan nilai logger mentah, corrected loaded, source hashes, serta pemeriksaan inserted/arrived/discarded. Raw result.json dan physics output tidak ditimpa. SUMO 1.28.0 tripinfo **write-unfinished/write-undeparted** diparse dan harus mempunyai record untuk setiap accepted request. XMLdepart/arrival−1 dibandingkan dengan actual TraCI sets. Tidak menganggap running/notdeparted sebagai perjalanan selesai.

Per OD disediakan completed trip duration(arrived-only, label eksplisit), elapsed duration / waiting / time loss bagi seluruh departed termasuk unfinished, dan departDelay accepted cohort termasukundeparted. Tidak ada complete cohort mean travel time palsu untuk semua request. `supplementary-audits.json` memakai actualFCD untuk speed distribution/histogram seluruh active vehicles, segment role breakdown dan lane occupancy full horizon termasukemptysamples. Occupancy adalah clippedunion front-assignedbodyfootprints; bodymelintasedge lain tidak direkonstruksi.

Queue count berbeda dari meter extent. Extent body-inclusive max(front) − min(tail) per lane; maximum stopped count adalah jumlahstopped road vehicles pada sampel1s, bukan satu physical queue. Durasi adalah lane seconds dengan antrean terdeteksi pada sampel 1s. Extent model sekitar short lanes / stop lines belum physically validated. Entry insertion pending dan horizon running tetap warning **DEMAND EXCEEDS INSERTION OR NETWORK CAPACITY** pada model ini, bukan bukti kapasitas Gedangan riil.

## Railway, spillback dan segment analysis

Actual train tripinfo, FCD movement IDs dan crossing road-link state windows ada pada supplementary audit. Train planned departures dibedakan dari actual tripinfo. Closure adalah status road links model, bukan field gate telemetry. Stopped vehicle-seconds dekat crossing red adalah asosiasi konteks, bukan incremental causal rail delay. Queue recovery causal dibuktikan hanya jika M051 detector menemukan storage release dan vehicle movement yang sesuai; kasus tanpa bukti tetap candidate/unresolved.

Detector M051 dipakai tanpa mengubah definisi:vehicle-specific nextLinks priority/open/foe, full FCD footprints, legal movement, continuous blocking dan recovery. Verified-in-model events tidak disebut field validated. Candidates tidak dinaikkan otomatis menjadi spillback. `causal-events.json`,classification-summary danpriority-trace tersimpan di setiap run. Frontage, feeder, Gedangan, NB, SB, station/Ketajen dibaca melalui actual OD/role metrics, bukan animasi acak.

## Fair comparisons, sensitivity dan uncertainty

`comparison.json` memeriksa networkhash,baselinehash,seed,window dancontroloptions. Perbedaan control/network diberi NOTCOMPARABLE_AS_PURE_GROWTH; perubahan mean arrived-only saat censored tidak ditampilkan sebagai peningkatan kinerja. Demand,throughput,queuecount,extent danspillbackdelta tersimpan. Failed route cohort tetap warning meskipun semua routable tiba. LOW/REFERENCE/HIGH bukan confidenceinterval.

Burst stress dua kali baseline mencapai batas driver180s dan dicatat FAILED_RESOURCE_BUDGET tanpa completed traffic metrics; main HIGH2040 tetap memberi bukti censoring pada horizon penuh. Run yang terputus saat restart Codex diarsipkan terpisah, lalu dilanjutkan dari cache run yang selesai.

Sensitivity terpisah mencakup growth scenario,class mix/baseline total,OD distribution, explicit departure profile,rail frequency,signaloff,behavior headway proxy danbounded burst stress. Mixing/headwayproxy tidak disebut estimasi physical road capacity. Capacity uncertainty asli tetap structural blocker; tidak ada pelebaran jalan atau perubahan infrastruktur. Lihat `sensitivity.json` untuk request/served/censoring dan confounds setiap run. Seed 42/43 merupakan simulation randomness, bukan pengganti uncertaintybaseline/OD/growth/geometry.

## Performance, failures dan reproducibility

Sequential concurrency 1. Primary 12 runs ditambah sensitivity/freshreproduction; cache berdasarkan projection/source/config/network/seed/options hashes. Runstatus,manifest,requestledger,routerstderr,tripinfo/FCD dan failureevidence dipertahankan. Cache hit memverifikasi hash core outputs; supplementary audit adalah derivasi terpisah. Actual fresh replay numeric tripinfo/FCD parity={'tripinfo.xml': True, 'fcd.xml': True}; cachemanifest tidak berubah=True. Tidak ada FPS/GPUbenchmark diklaim.

| Actual run | Wall s | SUMO CPU s | Sampled peak SUMO RAM MiB |
|---|---:|---:|---:|
| 2035 REFERENCE pilot-provisional seed 42 | 66.98 | 31.44 | 67.51 |
| 2030 REFERENCE pilot-provisional seed43 | 63.08 | 29.06 | 67.50 |
| 2026 REFERENCE pilot-provisional seed43 | 60.62 | 26.50 | 67.37 |
| 2026 REFERENCE corrected-provisional seed 42 | 31.32 | 15.86 | 67.07 |
| 2030 REFERENCE pilot-provisional seed 42 | 65.14 | 29.34 | 67.61 |
| 2040 HIGH pilot-provisional seed 42 | 126.19 | 56.30 | 67.91 |
| 2040 REFERENCE pilot-provisional seed43 | 80.61 | 37.34 | 67.71 |
| 2040 LOW pilot-provisional seed 42 | 67.05 | 31.09 | 67.52 |
| 2040 REFERENCE pilot-provisional seed 42 | 83.36 | 37.86 | 67.76 |
| 2026 REFERENCE pilot-provisional seed 42 | 59.64 | 25.36 | 67.34 |
| 2035 REFERENCE pilot-provisional seed43 | 74.98 | 33.53 | 66.66 |
| 2026 REFERENCE pilot-strict seed 42 | 38.02 | 17.14 | 35.89 |

Resource counter adalah process SUMO Windows, bukan whole-machine RAM/VRAM; puncak disampling1ssimulationinterval. Wall mencakup driver/causalanalysis dan tidak sama dengan CPUSUMO. Initial failure tambahan XML schema direkam, lalu diperbaiki dengan local additional_file.xsd. Semua failure folders tetap pada `failure-audit.json`; tidak dipakai sebagai completed traffic metrics.

## Internal browser dan testing

Browser status: PARTIAL. Detail:Browser recovered after Codex restart and verified years/scenarios/custom save/actual run initiation, playback page and desktop/mobile panel widths. During final screenshot/comparison checks, browser tool returned Local browser use is disabled in Work settings. No claim of full final browser acceptance.. Halaman M07 terpisah port 5182 / API 8772, hanyaloopback. Demandcalculation read-onlyGET; savecustom/run memakai validatedPOST. No CORS wildcard, exact Host/Origin, bounded body dan run queue. Skenario yang belum disimulasikan menampilkan NOT RUN, bukan queue/speed/TT rekaan. Run button benar-benar mengantrekan runner lokal, cached results memakai verified hashes. Saat offline experiment aktif, interactive job harus menunggu.

UI menyediakan semua 15 tahun/preset,scenarios/customeditor,OD/class/interval dashboard,geographic recorded playback,playpause/speed/timeline/zoom/layers,comparison/provenance/uncertainty. Playback hanyaactual SUMO 5s samples, tanpa random motion. Tidak mengklaim mobile/desktopPASS bila verifikasi belum selesai.

![browser-custom](m07/browser-custom.jpg)
![browser-desktop](m07/browser-desktop.jpg)
![browser-not-run](m07/browser-not-run.jpg)
![browser-playback](m07/browser-playback.jpg)

Initial 182 regression dipertahankan. Final 234 tests OK meliputi independent Decimal/piecewise/year-specific calculations,negative/zero/missing/provenance/scope/OD substitution,integer/tie/conservation/seedIDs,actual routes/FCD permissions,oversize/frontage/Strict,complete censored ledger,stress,cache fresh replay,source immutability dan empirical gate. TypeScript noEmit dan Vite production build PASS. SUMO-GUI M07 tidak dijalankan; buktiGUI milestone lama tidak dipresentasikan sebagai M07.

## Technical acceptance — 22 kriteria

| No | Kriteria | Status |
|---:|---|---|
| 1 | All years2026–2040 | PASS |
| 2 | Browser year selection | PARTIAL — BROWSER QA |
| 3 | Correct compound growth | PASS |
| 4 | Vehicle-class growth | PASS |
| 5 | OD-specific final rate | PASS |
| 6 | 15-minute demand intervals | PASS |
| 7 | Three scenarios | PASS |
| 8 | Versioned custom scenarios | PARTIAL — BROWSER QA |
| 9 | Growth provenance | PASS |
| 10 | Missing rates remain missing | PASS |
| 11 | Deterministic demand generation | PASS |
| 12 | Route/access validation | PASS |
| 13 | Actual representative SUMO runs | PASS |
| 14 | Requested versus served ledger | PASS |
| 15 | SUMO-derived congestion metrics | PASS |
| 16 | Censoring/unserved accounting | PASS |
| 17 | Fair comparison/parity guard | PASS |
| 18 | Sensitivity framework | PASS |
| 19 | Internal browser desktop/mobile QA | PARTIAL — BROWSER QA |
| 20 | All M01–M06 regression | PASS |
| 21 | Previous source immutability | PASS |
| 22 | Reproducible rebuild | PASS |

## Empirical acceptance, unresolved issues dan M08 readiness

Seluruh enam prasyarat empirical forecast masih BLOCKED:baseline2026empiricalcalibration,relevantlocalgrowth, verifiedOD/composition,geometry/controlfitness,independent validation,defensibleforecastuncertainty. Tidak ada klaim FULLPASS ilmiah.

Known blockers diwarisi:crossing endpoint sekitar 1.6m / lane shape hingga 7.178m, short lanes sekitar 0.10m, stop-line survey/clearance/legalitas heavy belum tersedia, Strict gaps, synthetic signals/trains, unverified OD/vehicle parameters. Missing field data tidak ditutupi optimizer atau growth assumptions. HIGH censoring bukan error yang disembunyikan dan bukan prakiraan kemacetan nyata. Internal browser QA yang belum selesai tetap isu teknis, bukan bukti keberhasilan.

M08 **tidak dimulai**. Untuk melanjutkan pekerjaan M08 diperlukan persetujuan pengguna. Kajian crediblefutureforecast juga membutuhkan baseline observations 2026,multi-year local class/OD flow evidence,control/geometryreview,independent validation dan acceptance justification yang sesuai tujuan studi.
