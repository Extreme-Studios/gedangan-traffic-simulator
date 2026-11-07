# MILESTONE 08.5 — GEDANGAN FIELD SURVEY WORKBENCH

Generated: 2026-11-01T03:56:43.389+07:00

## 1. Executive summary

**PARTIAL — browser acceptance pending. FIELD DATA COLLECTION SYSTEM belum dinyatakan TECHNICAL READY.**

OBSERVED GEDANGAN DATA: **NOT YET COLLECTED**. EMPIRICAL BASELINE 2026: **BLOCKED — DATA REQUIRED**. M09 **NOT STARTED**.

M08.5 menambahkan workbench lokal 13 panel, SQLite/IndexedDB, manual/video-assisted annotation, QC dan ekspor M06. 325 tes lulus, 6128 hash lama tetap cocok, build dan fixture ekspor direproduksi. Bukti UI desktop/mobile/playback/recovery browser belum tersedia; laporan ini sengaja tidak mengubahnya menjadi PASS. Tidak ada SUMO run baru, optimizer M06, data survei buatan yang dipresentasikan sebagai Gedangan, dependency baru atau cloud upload.

## 2. M06 assets audit

Audit actual source, governance, architecture, M06–M08 reports dan survey plan telah dilakukan sebelum implementasi. `m085/M06_ASSETS_AUDIT.json` menyimpan 25 asset hashes, enam schema yang identik dengan generated schema importer lama, sembilan CSV header yang tepat, enam JSON template kosong, serta integritas ZIP dan sembilan sheet workbook. Workbook dan importer M06 tidak diubah. M06 normalized observed records tetap 0.

Baseline awal meliputi 6.128 file / 16.657.695.561 byte. Dependencies `.venv`, `node_modules`, toolchain, caches dan lock runtime dikecualikan; source/config/dataset/geodata/simulation outputs/reports/build lama termasuk. Koreksi preflight mengeluarkan stdout baru milik preflight sendiri; draft baseline disimpan, tanpa mengubah entry M01–M08.

## 3. Survey location registry

Tujuh rencana berasal dari M06. Semua lokasi fisik tetap PLANNED; geometri edge bukan posisi kamera atau pengamatan yang telah disahkan.

| Location | Candidate SUMO edge | Field status |
|---|---|---|
| MAIN_NB | `w562358500_s16_p0_0_f` | PLANNED |
| MAIN_SB | `w512351908_s4_p0_0_f` | PLANNED |
| GEDANGAN_FEEDER | `w266287930_s0_p0_0_f` | PLANNED |
| FRONTAGE | `w1118947356_s0_p0_0_f` | PLANNED |
| KETAJEN | `w1240685448_s1_p2_0_f` | PLANNED |
| STATION_CROSSING | `w1240685448_s1_p2_0_r` | PLANNED |
| UPSTREAM_STORAGE | `w512351908_s3_p0_0_f` | PLANNED |

Peta SVG lokal menggunakan actual lane shape dan candidate connection network M05.1, dengan hash sumber. Tidak menggunakan external tiles dan tidak membuat koordinat kamera.

## 4. Reconnaissance system

Form mencatat observer, tanggal kunjungan, bukti/hash foto, koordinat/CRS/akurasi/metode, posisi/arah kamera, lajur/gerakan terlihat, coverage gaps, occlusion, signal/rail visibility, pencahayaan, posisi aman dan izin. Bukti sintetis tersimpan sebagai latihan dan tidak mempromosikan lokasi. Reviewer harus memeriksa bukti field, safe position dan permission sebelum FIELD_VERIFIED; APPROVED_FOR_SURVEY merupakan langkah berikutnya. Coverage gaps menjadi dasar kebutuhan observer/kamera tambahan, bukan rekomendasi jumlah kamera rekaan.

## 5. Manual counter

Sepuluh kelas identik dengan registry M04: motorcycle, car, pickup_van, minibus, bus, light_truck, medium_truck, heavy_truck, trailer, oversize. Mencatat kendaraan oversize yang terlihat tidak memberikan izin routing/legalitas kendaraan pada jaringan.

Tombol sentuh, shortcut yang dapat dikonfigurasi, Shift-arrows, Ctrl+Z, context approach/direction/movement/lane, timestamp WIB, confidence, notes/incidents, pause/resume dan checkpoint tersedia. Interval default 900 detik. Raw tidak ditimpa; edit/undo/duplicate menambah correction dan void projection. Button totals menyatakan jumlah input, bukan nol volume yang diverifikasi. Count hanya menjadi volume angka bila explicit COMPLETE coverage tunggal; tanpa itu count NULL dengan partial_count dalam notes. Boundary interval diuji, bukan dibulatkan menjadi volume 15 menit penuh.

SQLite autosave event mempunyai IndexedDB outbox per port. Pending tidak dianggap committed. FAILED dapat dikirim ulang atau diarsipkan dengan alasan, tanpa menghilangkan payload penolakan. Draft form yang belum dikirim belum durable; indikator draft menyatakan hal ini. Keyboard/touch browser belum diuji aktual.

## 6. Video annotation

HTML video memakai file/Blob lokal dan incremental SHA256 worker 1 MiB; tidak ada upload video atau AI model. File hash, durasi, FPS bila diketahui, recording clock/offset, camera/permission dan anonymous tokens disimpan. Playback controls, timeline, .25/.5/1/2×, fullscreen, zoom, nominal stepping dan penanda frame tersedia di source.

Unknown clock tetap VIDEO_TIME_ONLY; modification time bukan recording time. Raw menyimpan video seconds dan presented frame time bila tersedia, tanpa mengarang jam. Reviewer dapat menambah versi clock mapping dan window; ekspor memakai mapping efektif, raw asli tetap sama. Same observer + same hash + same token ditolak lintas sesi/referensi. Rewind/overlap memerlukan konfirmasi kendaraan lain yang belum dihitung dengan alasan audit. Guard ini tidak mengenali identitas fisik otomatis; human review tetap diperlukan.

Fixture MP4 H.264 640×360, 25 FPS, 12 detik, 1.195.595 byte ber-watermark synthetic color test pattern. SHA256 `cdab965c524ecf63df7850a7f997a72cd76a8a77fb6365cc9ed2ce485f586bf0`. SHA diuji dalam 64 variasi melawan Node crypto, termasuk chunk boundaries. Playback dan timestamp browser aktual masih pending. Frame stepping nominal tidak menjamin frame-exact pada VFR/semua codec.

## 7. Turning movement counting

Counter yang sama mencatat straight/left/right/other_legal/unknown per approach/arah/lajur; ringkasan tetap berstrata. Unknown tidak diubah menjadi straight. Peta memperlihatkan geometri kandidat koneksi. Other_legal adalah klasifikasi operator yang memerlukan pemeriksaan lapangan, bukan perubahan izin/koneksi SUMO. Listener counter video dilepas saat panel tersembunyi untuk mencegah shortcut ganda; pemeriksaan interaksi browser tetap pending.

## 8. Queue measurement

Jumlah kendaraan, panjang meter, maximum extent, duration, composition, definition, lane dan boundary censor dicatat terpisah. Meter memerlukan measured reference distance >0, bukti dan konfirmasi dasar ukuran. Tanpa itu panjang tetap NULL / LENGTH NOT MEASURED. Penanda stop line/first/rearmost/queue tail/spillback candidate menyimpan koordinat frame, bukan meter atau kejadian spillback terverifikasi. Export mempertahankan censoring dan units. Tes membuktikan queue_count 7 tidak berubah menjadi panjang 7 m.

## 9. Travel time observation

Asal/tujuan/koridor/rute, anonymous sample token dan metode authorized probe/GPS/two observers/video endpoints dicatat. Durasi dihitung dari endpoint aktual; rute berbeda tidak digabung. Unknown recording clock masih dapat menyimpan durasi video relatif, tetapi tidak diekspor sebagai observasi M06 bertanggal. Tidak menyimpan pelat/wajah/identitas pengemudi. OD dan kecukupan repeated travel samples tetap kebutuhan pengumpulan data.

## 10. Signal recording

Enam tahap green start/end, yellow start/end, red start/end dicatat terpisah; signal group, phase dan measured offset tersedia. Urutan yang mundur ditolak, tahap tak terlihat tetap NULL. Durasi dan cycle tidak diisi dari konfigurasi sintetis M05. Export hanya menghitung durasi dari pasangan timestamp yang ada; cycle tidak dibuat dari parsial yang tidak lengkap.

## 11. Railway recording

Sepuluh kejadian: warning_starts, barrier_begins_closing, road_fully_closed, train_approaches, train_arrives, train_passes, train_clears, barrier_begins_reopening, barrier_fully_opens, road_traffic_released. Closure ID dan train token memisahkan kejadian yang berulang. Additional train movements dalam closure yang sama disimpan sebagai structured JSON dengan empat tahap kereta; kronologi diuji.

Kontrak M06 mempunyai subset field railway dan satu primary train per row. Semua sepuluh tahap dan kereta tambahan dipertahankan di notes/raw/sidecars; importer M06 lama tidak otomatis menafsirkan struktur tambahan tersebut sebagai row train terpisah. Dedup M06 yang tidak membedakan train token tetap dihormati; penolakan dipertahankan. Tidak membuat timestamp epsilon atau jadwal palsu agar lolos.

## 12. Geometry survey

CRS, coordinate point, accuracy, instrument, method, source, units, lane/track count, width/storage/angle/clearance, centerlines, stop line, barrier/junction boundary dan akses tersedia. Dimensi jalan memakai meter; koordinat mengikuti CRS. EPSG:4326 dibatasi longitude/latitude legal. NULL tidak menjadi 0. CSV GNSS maksimal 5.000 row / UI 2 MiB memakai parsing+validasi terlebih dahulu dan transaksi; accepted/rejected raw CSV, original SHA dan submitted-text SHA disimpan. Empty GNSS header tersedia di data/templates/m085; tidak membuat XLSX importer baru.

## 13. Session planner

Session mempunyai location, observer, date/window WIB, camera, survey type, source, method, sample group, status dan notes. PLANNED/RECONNAISSANCE/READY/IN_PROGRESS/COMPLETED/NEEDS_REVIEW dan independent review APPROVED tersedia. Parameter sesi dengan raw tidak dapat ditimpa; buat sesi/revisi terpisah. Readiness field memerlukan lokasi disetujui dan observer terlatih. Usulan tiga hari kerja/satu akhir pekan dengan 07–09/12–14/16–18 didokumentasikan sebagai proposal, bukan jam puncak atau bukti otomatis kecukupan data.

## 14. Observer quality control

Alias/role/training registry, independent double count dan adjudication tersedia. Perbandingan hanya untuk shared sample group, lokasi/arah/approach/window sama dan pengamat berbeda. Difference dihitung per class/movement/interval: absolute |A−B|, relative |A−B|/mean(A,B); dua nol sah →0, missing →NULL. Ambang default .1 adalah pemicu review ilustratif, dapat dikonfigurasi, bukan standar universal. Reviewer berbeda dari kedua pencacah memilih A/B/RECOUNT_REQUIRED dengan alasan; tidak ada automatic averaging. Comparison ID berubah bila hasil berubah; adjudikasi stale ditolak.

## 15. Privacy and safety

Original video/photo tetap lokal; database dan backup hanya references/hash/metadata/annotations. Media payload memiliki whitelist. Key video/frame bytes, data URI dan driver/plate/face fields terlarang ditolak dan disunting bahkan pada rejected log. Ini bukan pengenal otomatis PII di semua free text; operator tidak boleh memasukkan identitas pribadi dalam notes.

Tidak ada facial recognition, ALPR, cloud API/auth/subscription/model/GPU dependency. Server bind IPv4 loopback, exact Host/Origin, JSON/body bounds dan self-only CSP. Tidak mengubah browser/Windows security settings. Retention days/basis dapat dicatat; aplikasi memensiunkan referensi beserta audit, tidak menghapus video asli milik pengguna. Penghapusan asli dikelola pemilik sesuai izin/kewajiban dokumentasi.

## 16. M06 integration

Enam schema dan importer lama digunakan read-only melalui private module instance. Output staging/preview sepenuhnya berada di M08.5; OBS target lama tidak diubah. Tidak menjalankan ingest ke normalized M06 atau optimizer.

M06 hanya menerima OBSERVED_FIELD dan DEMO_SYNTHETIC. Sembilan source classes M08.5 dipertahankan pada raw/provenance/notes: reviewed field/video yang memenuhi gates dapat menjadi OBSERVED_FIELD; SYNTHETIC_TEST hanya DEMO_SYNTHETIC. Reference/assumption/simulation/missing tidak dipromosikan. Video tanpa clock atau bukti/review gagal diekspor sebagai field. Dataset approval tidak berarti baseline terkalibrasi.

## 17. CSV/JSON compatibility

Semua enam jenis melewati importer M06 aktual pada JSON dan CSV (12 format) dengan fixture sintetis terpisah. Exact headers, nullable metrics, timestamp +07:00, direction/movement/class/confidence/source/method dipertahankan. Count confidence diambil konservatif dari evidence strata. Observed zero memerlukan COMPLETE coverage; interval parsial/missing tetap NULL.

ZIP mencakup CSV/JSON, provenance, raw, corrections, registry clock/window versions, lineage, rejected commands/adjudications/audit, preimport rejected, importer rejected, quality flags dan manifests dengan source/schema/importer hashes. CSV details dapat diunduh per jenis. Original video tidak disertakan. Unsupported detail seperti semua railway stages/lane composition/instrument/raw source class dipertahankan dalam notes dan sidecars, tanpa menambah field yang melanggar additionalProperties=false.

## 18. Offline browser QA

**PARTIAL.** Python-only static HTML/JS/CSS dan API telah benar-benar disajikan via HTTP 200 dengan chunk framing; asset body cocok byte-for-byte. Backend diuji dengan external socket creation ditolak. Self-only CSP tidak memerlukan external resources. Ini membuktikan transport/server offline, bukan seluruh interaksi browser.

Internal preview request dikembalikan queued. Fallback Computer Use berhenti karena tidak dapat memastikan current Chrome URL untuk enforcement policy. Tidak ada input UI berikutnya, bypass, screenshot atau klaim playback/mobile PASS. Daftar skenario tersedia di `m085/BROWSER_QA_PENDING.md`. Listener/codec/IndexedDB restart/form/touch/layout perlu verifikasi aktual sebelum TECHNICAL READY.

## 19. Backup and recovery

SQLite WAL/FULL, transaction, idempotent command IDs, immutable triggers, raw SHA, chained audit dan projection/version replay menyediakan integritas aplikasi. Backup menggunakan SQLite backup API dan ZIP berisi hanya survey.sqlite + manifest. Restore memeriksa whitelist ZIP, bounded size, database checksum dan integrity sebelum atomic pointer switch ke cabang baru; cabang lama dipertahankan.

Tes membuktikan backup/restore actual raw dan database reopen, corrupted backup ditolak, projection tamper terdeteksi, immutable DELETE/UPDATE ditolak dan duplicate retry tidak menggandakan event. Backup tidak memuat file ekspor lama, video asli, draft form atau IndexedDB; simpan paket ekspor terpisah. Hash chain bukan tanda tangan kebal administrator. Recovery IndexedDB setelah browser restart masih belum diuji UI.

## 20. Performance

Synthetic-only benchmark: 3.000 event dengan individual SQLite transactions dalam 36.048s; median 11.490ms, p95 15.131ms. Ledger 50 row pada offset 2.950: 48.024ms. Peak Python traced allocations 118,268 byte, bukan total RAM proses/OS/browser. Semua raw/audit diperiksa sesudahnya.

Video asli diputar melalui File/Blob dan hashing potongan 1 MiB; ledger dibatasi 100 row maksimal per request. Export/QC mematerialisasikan sesi secara lokal. Tidak ada benchmark GPU, video RAM total atau jaminan seluruh codec/16 GB yang diklaim. Lihat `m085/verification.json`.

## 21. Regression tests

**PASS: 325 tests dalam 133.949s.** Repo aktual mempunyai 293 tes lama, empat lebih banyak daripada angka 289 pada brief; semuanya dipertahankan. Ditambah 32 tes M08.5. Bukti lengkap `m085/final-regression.txt`, focused `m085/focused-tests.txt`, SHA 64 checks di `m085/sha256-tests.json`.

Satu percobaan sebelumnya menghasilkan static GET 404 akibat tes berbarengan dengan rebuild yang mengosongkan dist. Akar masalah diisolasi: tes transport memakai temporary static fixture agar tidak tergantung race build; production asset smoke dilakukan terpisah terhadap build aktual. Regresi akhir lulus. Tidak menyembunyikan kegagalan awal; `m085/full-regression.txt` dipertahankan.

## 22. Reproducibility

Dua build Vite berturut-turut menghasilkan empat artifact identik SHA256; tidak menyalin public output simulasi lama. TypeScript lulus. Dua workspace independen dengan fixed software clock/session/event IDs menghasilkan enam CSV + enam JSON identik byte-for-byte; backup/restore masing-masing diuji. Fixture hanya dua observasi count (satu motor, satu nol mobil dengan explicit coverage), bukan traffic dataset.

Identitas seluruh ZIP/database/audit UUID/timestamp tidak diklaim. Lihat `m085/build-reproduction.json`, `m085/verification.json` dan namespace `data/surveys/m085/verification/`. Launcher rebuild memeriksa baseline, semua tests, SHA, TypeScript/build dan baseline akhir; tidak menjalankan generator M01–M08.

## 23. Screenshots

**Belum tersedia.** Tidak membuat screenshot mockup atau menggunakan screenshot milestone lama sebagai bukti M08.5. Tidak ada klaim UI telah dirender/diklik berdasarkan build saja. Pengambilan screenshot desktop/tablet/mobile dan actual video/count/export harus dilanjutkan setelah alat browser dapat mengendalikan URL lokal secara sah. Referensi prosedur: `m085/BROWSER_QA_PENDING.md`.

## 24. Remaining limitations

Browser acceptance/playback/shortcut/touch/IndexedDB restart masih pending dan menjadi blocker technical readiness. VFR stepping nominal, bukan frame-exact. Replay guard berbasis token/hash/time dan human confirmation, bukan computer vision. Free text tidak dideteksi PII otomatis. Draft form dan frame marks belum autosaved sebagai event sebelum submit. Additional trains memakai structured JSON dan M06 lama hanya menafsirkan primary flat fields; details tetap dipertahankan. Dedup M06 tidak diubah atau diakali. Retention source deletion dilakukan pemilik, bukan otomatis.

Tidak ada lokasi physical-approved, observed data atau baseline calibration. Ketersediaan pengukuran/izin/reviewer independen, coverage spasial/temporal dan kecukupan sampel harus dipastikan di lapangan. Acceptance per 23 kriteria ada di bawah; backend PASS tidak menggantikan UI QA.

| # | Criterion | Status | Evidence / limit |
|---|---|---|---|
| 1 | M06 assets audit | PASS | 25 assets, six schema contracts, nine CSV headers, six JSON templates, workbook integrity. |
| 2 | Seven planned locations | PASS | Actual M06 registry; no approved camera or field coordinates invented. |
| 3 | Reconnaissance | PARTIAL | Implemented field/safety/evidence gates; UI acceptance pending. |
| 4 | Manual counter | PARTIAL | Backend ten classes/undo/edit/interval tests pass; touch and keyboard UI pending. |
| 5 | Video annotation | PARTIAL | Hash/clock/replay backend tested; actual browser playback pending. |
| 6 | Duplicate prevention/audit | PASS_BACKEND_UI_PENDING | Idempotent commands, anonymous tokens, same-hash replay gate, immutable corrections. |
| 7 | Turning counter | PARTIAL | Movement strata and source geometry implemented; browser interaction pending. |
| 8 | Queue measurement | PARTIAL | Count/meters/censoring gates pass; UI acceptance pending. |
| 9 | Travel time | PARTIAL | Endpoint/token/duration gates pass; UI acceptance pending. |
| 10 | Signal recorder | PARTIAL | Six stages/missing/chronology tested; UI acceptance pending. |
| 11 | Railway recorder | PARTIAL | Ten stages plus multiple movements preserved; UI acceptance pending. |
| 12 | Geometry survey | PARTIAL | CRS/units/CSV transaction and rejected rows tested; UI acceptance pending. |
| 13 | Session planner | PARTIAL | Planning/readiness gates implemented; browser acceptance pending. |
| 14 | Observer QC | PARTIAL | Aligned double count, missing/difference/adjudication tests pass; UI acceptance pending. |
| 15 | M06 CSV compatible | PASS | All six kinds accepted through unchanged importer in isolated staging. |
| 16 | M06 JSON compatible | PASS | All six kinds accepted through unchanged importer in isolated staging. |
| 17 | Provenance | PASS | Original source class, clock versions, hashes, raw, corrections, row lineage retained. |
| 18 | Offline mode | PARTIAL | Python-only HTTP/CSP and no-external backend test pass; browser offline flow pending. |
| 19 | Backup/restore | PASS_BACKEND_UI_PENDING | Actual SQLite backup, hash/integrity validation and branch restore; browser flow pending. |
| 20 | Desktop/mobile browser QA | BLOCKED_TOOL | Tool could not confidently determine current Chrome URL. No screenshots claimed. |
| 21 | Existing + new regression | PASS | 325 tests pass; 133.949s. 293 old + 32 new. |
| 22 | Old M01–M08 unchanged | PASS | 6128 baseline file hashes verified; old observations/registry untouched. |
| 23 | Rebuild reproducible | PASS_SCOPED | Two production builds identical; six CSV + six JSON controlled fixture exports identical. ZIP identity not claimed. |

## 25. Field deployment checklist

Panduan langkah pertama di Perempatan Gedangan tersedia pada `MILESTONE_08_5_README.md`; checklist printable di `m085/FIRST_SURVEY_CHECKLIST.md` dan Dashboard. Urutan: reconnaissance+izin → pengamat terlatih → reviewer lokasi → planner/sample groups → sinkronisasi clock/media hash → actual count/coverage/measurements → independent QC → dataset human review → export+accepted/rejected → backup/retention. Selesaikan browser acceptance terlebih dahulu sebelum membawa perangkat untuk pengumpulan data produksi.

## 26. M09 readiness

**M09 NOT STARTED / NOT READY FOR EMPIRICAL WORK.** M08.5 technical acceptance masih PARTIAL. Tidak ada data Gedangan baru, tidak ada synthetic promotion dan tidak ada optimizer/calibration.

CRITICAL yang harus dikumpulkan/diverifikasi: count 15 menit per kelas/arah, turning movement, OD, travel time, queue length, signal timing, railway crossing events, geometry/stop line dan independent validation. IMPORTANT: repeated sessions, cuaca, hambatan samping, observer agreement dan visibility. OPTIONAL: anonymous lateral trajectories dan detailed behavior observations dengan izin/tujuan yang sesuai.

Empat hari yang diusulkan tidak otomatis mencukupi penelitian. Tinjau cakupan spasial/temporal, variasi kondisi dan tujuan simulasi. M09 membutuhkan data observasi yang dapat diverifikasi dan instruksi pengguna berikutnya; tidak dimulai oleh laporan atau keberhasilan importer.
