"""M13 deliverables computed from actual current database and inspected sources."""
import csv,collections
from .m13_common import *
from .m13_database import Store
from .m13_seed import seed
def link(path):return '['+Path(path).name+'](<'+Path(path).resolve().as_posix()+'>)'
def md(name,title,body):(ROOT/name).write_text('# '+title+'\n\n'+body+'\n',encoding='utf-8')
def build():
 store=Store();seed(store);months=[store.monthly('2026-'+str(m).zfill(2))for m in [8,9,10]];days=[];missing=[]
 for month in months:
  for summary in month['days']:
   d=store.daily(summary['date']);compact={k:v for k,v in d.items()if k not in ['hours','scope']};compact['hours']=[]
   for h in d['hours']:
    compact['hours'].append({k:v for k,v in h.items()if k not in ['missing_or_partial_cells','scope']})
    if h['status']!='OBSERVED':missing.append({'date':d['date'],'hour_wib':f"{h['hour']:02d}:00",'time_zone':'Asia/Jakarta','status':h['status'],'scope_expected_cell_seconds':h['expected_cell_seconds'],'observed_cell_seconds':h['observed_cell_seconds'],'reason':'No verified observations in requested scope'if h['status']=='MISSING'else'Incomplete interval/road/direction/class/parameter coverage','vehicle_count':None})
   days.append(compact)
 eligible=[r for r in store.rows(eligible=True)if START.isoformat()<=r['observation_date']<=END.isoformat()];allrows=store.rows();summary={'dates_with_observations':sum(d['color']!='RED'for d in days),'dates_without_observations':sum(d['color']=='RED'for d in days),'dates_complete':sum(d['color']=='GREEN'for d in days),'dates_partial':sum(d['color']=='YELLOW'for d in days),'complete_hours':sum(d['complete_hours']for d in days),'partial_hours':sum(d['partial_hours']for d in days),'missing_hours':sum(d['missing_hours']for d in days),'total_days':92,'total_hours':2208,'quarter_hour_calendar_slots':8832,'verified_target_records':len(eligible),'outside_target_stored_source_records':sum(not START.isoformat()<=r['observation_date']<=END.isoformat()for r in allrows)}
 coverage={'period':[START.isoformat(),END.isoformat()],'time_zone':'Asia/Jakarta','summary':summary,'scope':store.scope(),'dataset_version':store.version(),'days':days,'road_coverage':store.dimensions('road_segment'),'directional_coverage':store.dimensions('direction'),'vehicle_class_coverage':store.dimensions('vehicle_class'),'parameter_coverage':{k:sum(r[k]is not None for r in eligible)for k in METRICS},'meaning_of_zero':'Availability counters only. Missing vehicle observations retain NULL; zero counts only exist in a source that actually measured zero.','fixtures_in_production':False};save(ROOT/'M13_HISTORICAL_COVERAGE.json',coverage)
 with (ROOT/'M13_MISSING_DATES_AND_HOURS.csv').open('w',encoding='utf-8-sig',newline='')as f:
  w=csv.DictWriter(f,fieldnames=['date','hour_wib','time_zone','status','scope_expected_cell_seconds','observed_cell_seconds','reason','vehicle_count']);w.writeheader();w.writerows(missing)
 audit=load(DOC/'source-file-audit.json');web=load(DOC/'web-source-audit.json');before=load(DOC/'preexisting-source-sha256.json');changed=[p for p,h in before.items()if not(ROOT/p).is_file()or sha(ROOT/p)!=h]
 legacy_sources=load(ROOT/'documentation/realism_recovery/current-runner-sources.json');legacy_changed=[p for p,h in legacy_sources.items()if not(ROOT/p).is_file()or sha(ROOT/p)!=h]
 baseline=load(ROOT/'documentation/realism_recovery/checkpoint/BASELINE_SHA256.json')['files'];protected={p:h for p,h in baseline.items()if p.startswith(('backend/','frontend/src/','frontend/m12/','configuration/','simulation/network/'))};protected_changed=[p for p,h in protected.items()if not(ROOT/p).is_file()or sha(ROOT/p)!=h]
 with connect(store.path,True)as c:
  integrity=c.execute('PRAGMA integrity_check').fetchone()[0];fk=[list(r)for r in c.execute('PRAGMA foreign_key_check')];columns=[dict(r)for r in c.execute('PRAGMA table_info(observations)')]
 oldrelease=ROOT/'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR_v1.0.0_PORTABLE.zip';release_expected=load(ROOT/'documentation/realism_recovery/checkpoint/RELEASE_CHECKPOINT.json')['sha256'];release_same=sha(oldrelease)==release_expected
 verified={'status':'PASS'if not changed and not legacy_changed and not protected_changed and integrity=='ok'and not fk and release_same else'FAIL','checked_existing_source_files':len(before),'changed_existing_sources':changed,'checked_recovery_source_files':len(legacy_sources),'changed_recovery_sources':legacy_changed,'checked_M01_M12_source_configuration_network_files':len(protected),'changed_M01_M12_files':protected_changed,'sqlite_integrity_check':integrity,'foreign_key_errors':fk,'old_release_sha256':release_expected,'old_release_unchanged':release_same,'synthetic_test_rows_in_active_target_database':sum(r['source_type']=='SYNTHETIC_TEST'and START.isoformat()<=r['observation_date']<=END.isoformat()for r in allrows),'no_old_observation_database_migration':True};save(DOC/'integrity-verification.json',verified);save(DOC/'schema.json',{'database':str(store.path.relative_to(ROOT)),'fields':columns,'source_fields_in_joined_view':['source_type','source_name','source_location','source_url','survey_method','source_sha256','current_verification_status'],'tables':['metadata','sources','batches','observations','quarantine','reviews'],'nullable_metrics':METRICS,'intervals':'ISO8601 +07:00, observation_time exact HH:MM:SS, max3600s; original count never prorated','review':'Initial verification_status retained immutably. current_verification_status resolved from latest append-only reviews event.'})
 counts=collections.Counter(r['classification']for r in audit)
 md('M13_HISTORICAL_DATA_AUDIT.md','M13 — Historical Data Audit',f'''Periode target: **1Agustus–31Oktober2026**, Asia/Jakarta. Audit menyelesaikan pemeriksaan isi **{len(audit)} berkas lokal**: CSV/XLSX, read-only SQLite tables/JSON, source PDFs, OSM metadata, dan result SUMO. Duplicate build/export/backup tetap tercatat perfile dengan hash, bukan dianggap observasi independen. Pemeriksaan gagal sebelumnya karena parser belum tersedia diulang memakai bundled reader; final seluruh385lokal CONTENT_INSPECTED. Source register: {link(ROOT/'M13_DATA_SOURCE_REGISTER.csv')}; rincian {link(DOC/'source-file-audit.json')}.

## Hasil aktual

- Tanggal punya observasi target: **{summary['dates_with_observations']}**. Tanpa observasi: **{summary['dates_without_observations']} dari92**.
- Jam lengkap: **{summary['complete_hours']}**, parsial: **{summary['partial_hours']}**, kosong: **{summary['missing_hours']} dari2.208**.
- Ruas/arah/kelas teramati terverifikasi pada target: **tidak ditemukan dalam sumber yang diperiksa**. Seluruhparameter target tetap NULL/MISSING.
- {summary['outside_target_stored_source_records']} record asli publikasi2023 disalin ke DB M13 sebagai OBSERVED_SECONDARY dengan tanggal/lokasi sumber, arah UNSPECIFIED, review scope PENDING_REVIEW. Tidak dipetakan secara rekaan ke edge dan tidak masuk kalender2026.
- Distribusi file berdasarkan fungsi audit: {dict(counts)}. Tag sumber pada file tidak otomatis menjadi bukti; tabel fixture dan synthetic-only workspaces tetap dikeluarkan.

## Pemeriksaan sumber publik

Unduhan XLS Dishub [identifikasi masalah lalu lintas](https://opendata.sidoarjokab.go.id/id/dataset/data-indentifikasi-masalah-lalu-lintas) berisi satu baris administratif dengan **satuan Dokumen**, nilai2023=1,2024=1,2025=0. Ini bukan jumlah kendaraan dan bukan data2026.

[Lampiran Dishub2023](https://opendata.sidoarjokab.go.id/dataset/2ed97d4c-cba0-4e5b-ba53-dc4e5d9ff48b/resource/ab78e87f-5332-4876-a6a3-7ef2d2816c79/download/outcome-visi-ratio-ruas-jalan-kab-sda-.pdf) menyatakan sumber survei2022, berunit SMP/jam; tanggal/jam arah count mentah target tidak tersedia. Bukan observasi2026.

[Kajian STTD](https://digilib.ptdisttd.ac.id/8279/1/Jurnal%20Kajian%20Rencana%20Pengendalian%20Simpang%20Gedangan%20M.Rizky%20Bima.P.pdf) kini berhasil diunduh dan diekstrak13halaman, memuat analisis2024 dan referensi2022. Tidak menyediakan tabel pencacahan bertanggal Agustus–Oktober2026. Tidak menyalin existing/model scenario numbers menjadi observations. Publication year tidak dianggap observation_date.

[Kusuma & Sholikhah](https://ejournal.undip.ac.id/index.php/ilmulingkungan/article/download/56951/pdf), Table1p927: sembilan jendela1jam Mei2023 ×4kelas; lokasi AhmadYani konteks Aloha. Diperiksa sebagai sumber historis terpisah, bukan pengganti count2026. OSM membuktikan atribut/geometri referensi, bukan volume kendaraan.

UMPR download masih502, directional2022 masih403; dicatat UNAVAILABLE, tidak menganggap halaman publikasi sebagai dataset yang sudah dimiliki. Pencarian publik bukan bukti bahwa data tidak ada di lembaga mana pun. Rincian URL/hash/akses: {link(DOC/'web-source-audit.json')}.

## Data yang perlu diminta / disurvei

Pencacahan asli1Agustus–31Oktober2026 per lokasi terpetakan/arah/kelas/interval15menit, dengan date-clock WIB, source permission, metode dan quality review. Prioritas06–10dan16–22WIB tetap MISSING. Minta Dishub data count mentah, turning counts, speed/travel-time samples, queue definition/timestamps, actual signal phases dan rail closure events; data geometri/OSM sendiri tidak memenuhi itu. Tidak ada pesan/permohonan yang dikirim atas nama pengguna pada pekerjaan ini.
''')
 md('M13_CALENDAR_IMPLEMENTATION_REPORT.md','M13 — Calendar Implementation',f'''## Aplikasi

[Buka kalender lokal](http://127.0.0.1:5197/). Launcher: {link(ROOT/'START_GEDANGAN_HISTORICAL_M13.bat')}. Layanan M13 terpisah dari research runner5196 dan EXE M12. Tidak mengubah visual3D atau merilis EXE baru.

Backend: backend/gedangan/m13_database.py, m13_server.py. UI: frontend/m13/. Semua warna berasal dari API database aktual.92tanggal dihasilkan dari calendar arithmetic; daftar tanggal hijau/kuning/merah tidak dihardcode. Scope default adalah dua titik monitor koridor utama NB/SB yang memakai existing OD endpoints, sepuluh kelas M04, lima parameter. Bukan klaim seluruh1.961roadedges punya pengamatan. Ruas lain dapat diimpor bila ID ada pada katalog. Titik/arah target baru yang lolosverifikasi otomatis ditambahkan pada scope dan pilihanfilter; denominator baru tetap diperlihatkan.

Hijau=seluruh24jam untuk semua pasangan ruas/arah, kelas dan parameter scope terisi intervalobserved lengkap. Kuning=adaobservasi tetapi interval/dimensi lain kurang. Merah=tidakadaobservasi scope. Coverage menggunakan union interval percell agar overlap tidak membuat persentase melebihi100%. Filter mempersempit denominator secara eksplisit; label scope tetap ditampilkan. Count tidak dibagi rata ke jam lain. Seluruh jamMISSING disabled dan POSTselection ditolak backend. Tanggalmerah dapat diklik untuk inspeksi, tetapi tidak dipakai historicalsimulation.

Saat memilih tanggal, jam tidak dipindahkan ke tanggal lain. Jamparsial memperlihatkan missing/partial cells perruas/arah/kelas/parameter serta availableparameters dansourceIDs. Selection hanya memilih evidence; route/ODmapping dan kalibrasi untuk historical SUMO belum diklaim tersedia.

## API

GET /api/monthly?month=2026-08; /api/daily?date=2026-08-01; /api/hourly?date=2026-08-01&hour=7; /api/roads; /api/directions; /api/classes; /api/provenance; /api/source-audit; /api/staged; /api/template. Filters road_segment/direction/vehicle_class/parameter opsional dan ditampilkan dalam scope. POST/api/import, /api/review, /api/select. Import CSV/XLSX/JSON, maximum6MB/20.000rows. SQLite lama diaudit read-only; generic SQLite tidak dimerge tanpa mapping, ekspor ke supported schema diperlukan.

Source immutable+SHA archive, staged observations, quarantine perbaris, review append-only. File/source/type/status/unit/date/time/road/direction/class/interval/duplicate/overlap divalidasi. XLSX formulas dan numericExceldates tidak ditebak sebagai bukti; dates wajibISOtext. Blank→NULL, nilai0dipertahankan hanya dari sumber. Unknown/missing source classification ditolak; reference/simulation/synthetic tidak dapat diverifikasi sebagaiobserved. Reviewer/note/evidencecheck eksplisit wajib.

Cachemonthly memakai dataset_version; import/review mengubahversion, UI memeriksa setiap5detik dan membaca kalender ulang. Tidak harus restartserver. Existing dates/jam user tidak disubstitusi otomatis. Mode **REFERENCE-BASED TRAFFIC SCENARIO** terpisah, banner estimasi permanen, preview dari referensi2023 hanya07/12/17. Link actualSUMOrunner tersedia, tanpa submit atau mengganti tanggalnya otomatis.

## Acceptance

20 automated tests: production red/missing, isolatedfixture yellow/green, disabled selection backend, sourceclass exclusion, adjacentdate nonfallback, NULL/realzero distinction, cacheinvalidasi setelahimport/review via realHTTP, provenanceSHA, invalid/duplicate quarantine, immutability, explicitunits, intervalunion, reviewgate, class-conflict gate, XLSXvalue/formula guard dan penambahan otomatis titikmonitor baru. Log {link(DOC/'acceptance-tests-final.log')}. **Yellow/green dibuktikan di database testsementara yang ditandai fixture, tidak pernah di databasehistoris aktif**. Kalender produksi sekarang seluruhnya merah karena data memang belum tersedia. Browser functional smoke test PASS:92tanggalmerah,24jamdisabled,tombolhistoricaldisabled,reference16MISSINGdan07estimasi. Bukti documentation/m13/browser-acceptance.json dan calendar-production-red.png. Green/yellow tetap diuji pada databasefixture, bukan direkayasa pada kalenderaktif.
''')
 md('M13_DATA_INTEGRITY_REPORT.md','M13 — Data Integrity',f'''## Status

Database SQLite integrity_check: **{integrity}**; foreign_key_check errors: **{len(fk)}**. Preservation: **{verified['status']}**, {len(before)} preexisting source/output files dibandingSHA, changed={len(changed)}. {len(legacy_sources)} recovery source files dibanding snapshot, changed={len(legacy_changed)}. FinalreleaseM12unchanged={release_same}; SHA256 `{release_expected}`. Evidence {link(DOC/'integrity-verification.json')}.

## Pemisahan data

DB baru: {link(store.path)}. Database penelitian M06/M08.5/recovery lama dibaca read-only, bukan dimigrasi di tempat.36record2023 dibawa beserta tanggal/arah/provenance asli ke namespaceM13, di luar target dan belum lolosscope-review. Dataset2026 aktif mempunyai **{len(eligible)} verified records**; syntheticfixture target aktif **{verified['synthetic_test_rows_in_active_target_database']}**. Test menghasilkan data hanya pada TemporaryDirectorydatabase yang jelas test_fixture=true; tidak digabungkan atau diimpor keDBproduksi. Warna kalenderproduksi bukan demonstrasi keberhasilanfixture.

Schema: {link(DOC/'schema.json')}. observation_date/time, timezone, interval, location/direction/class, metricsnullable, units, statuses dan provenance disimpan pada observations. Source_name/location/url/method/type/SHA pada tabel sources yang direlasikan melalui FK dan diekspos observation_records view. Initial verification_status immutable; current_verification_status memakai latestappend-onlyreview. Tidak ada angka default atau randomfill. SourceURLyangtidakada tetapNULL; OBSERVED_SECONDARYbaru mensyaratkan URLpublikasiasli.

UPDATE/DELETE pada source/batch/observation/quarantine/review ditolak trigger. Rejection/review baru dicatat sebagai event; originalrecord tidak ditimpa. Ini perlindungan integritas aplikasi, bukan sistem identitas/otorisasi multiuser atau sertifikatkeaslian pengamatan. Review tetap tanggungjawab pemeriksa bukti.

## Cakupan dan batas

{summary['dates_with_observations']}tanggal punyaobservasi; {summary['dates_without_observations']}tanggal kosong. {summary['complete_hours']}jam lengkap, {summary['partial_hours']}parsial, {summary['missing_hours']}kosong. Hasilcoverage {link(ROOT/'M13_HISTORICAL_COVERAGE.json')}; missingtime ledger {link(ROOT/'M13_MISSING_DATES_AND_HOURS.csv')}. Angka2208menyatakan jumlahslotjam, bukan jumlahkendaraan. Records kosong tidak menjadi0vehiclecount.

Tidak ada kalibrasi, inferensi pola2026, pengubahantraffic simulation hasil lama, penghapusanworkspace atau uploadGitHub. Milestoneberikutnya belum dimulai. Sourcepipeline dapat menerima bukti baru tetapi data target masih perlu diperoleh dan direview.
''')
 print(json.dumps({'summary':summary,'integrity':verified['status'],'reports':6}),flush=True)
if __name__=='__main__':build()
