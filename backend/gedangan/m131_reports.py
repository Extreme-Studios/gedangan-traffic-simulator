"""Seven requested reports, with physical counts / equivalents / metadata kept separate."""
import csv,collections
from pathlib import Path
from .m131_research import *
from .m13_common import connect
from .m131_database import initialize
def link(p,label=None):return '['+(label or Path(p).name)+'](<'+Path(p).resolve().as_posix()+'>)'
def md(name,title,body):
 replacements={
 '92reference aggregates disimpan pada tabel terpisah di DB turunanM13.1; tidak mengubah kalenderobservasi.':'49kandidat parsial B melewati validated import dan seluruhnya masukquarantine karena interval12jam tidak memenuhi resolusi/mapping kalenderperjam.92arsip B/C disimpan terpisah; bukan92observasi siap dipakai.',
 'KategoriC/D/E tidak pernah menjadi historicalobservations.':'KategoriC/D/E tidak pernah menjadi historicalobservations; B yang belum memenuhi gate tetapquarantine.',
 'ArsipC terstruktur:':'Arsip B tertahan / C referensi terstruktur:',
 'Tabelreference_aggregatesappend-only menyimpan92recordC terpisah.':'Tabelreference_aggregatesappend-only menyimpan49recordB tertahan dan43recordC terpisah. KandidatB dikirim melalui workflowimpor;49barisquarantine,0admitted. Derivativeawal historical.sqlite tetapdisimpan sebagai checkpoint; versiaktif historical_v2.sqlite.',
 'DaftarbulanC2023-11/12ditampilkan dengan labelagregat':'DaftarbulanarsipB2023-11/12ditampilkan dengan labeltertahan/agregat'}
 for a,b in replacements.items():body=body.replace(a,b)
 (ROOT/name).write_text('# '+title+'\n\nAudit date: '+now()+'\n\n'+body+'\n',encoding='utf-8')
def main():
 sources=load(DOC/'resource-inspections.json')+load(DOC/'followup-inspections.json')+load(DOC/'alternative-source-inspections.json');byurl={}
 for r in sources:byurl[r['url']]=r
 sources=list(byurl.values());downloads=load(LOG);rows=load(DOC/'reference-aggregates.json');summary=load(DOC/'integration-summary.json');store=initialize();register=[]
 for r in sources:
  tag=r.get('tag','');inspection=r.get('inspection',{});fmt=inspection.get('format');complete=r['status']=='RETRIEVED'and r.get('inspection_status')=='INSPECTED';binary=fmt in ['PDF','XLS/XLSX']
  if not complete:quality='E';decision=r.get('inspection_error',r.get('error','Retrieval/inspection incomplete'))
  elif tag.startswith('BPS'):quality='D';decision='Actual metadata/export inspected; planned survey schedule and variable definitions, not observation result table'
  elif tag=='JENGGOLO_2023':quality='B';decision='49published real partial observations on original12h/day intervals, both directions combined; submitted through validated import, all49quarantined for hourly admission. Raw interval/class/unit retained; no invented mapping or prorating.'
  elif tag.startswith('UPN'):quality='C';decision='Public derived study conclusions;2025survey dates reported, raw counts in restricted chapters/appendix not requested'
  elif fmt=='XLS/XLSX'and tag!='v-c-ratio-di-jalan-kabupaten-kota':quality='C';decision='Administrative annual counts/documents/units, not class-specific dated traffic counts; all sheets inspected'
  elif tag=='v-c-ratio-di-jalan-kabupaten-kota':quality='C';decision='2022road table, equivalent smp/hour volume/capacity, no exact observation date/hour/direction/classes; paired PDF/XLS/datastore reconciled'
  else:quality='D';decision='Catalog/metadata page only; no raw observations admitted'
  register.append({'tag':tag,'publisher':r.get('publisher','BPS'if tag.startswith('BPS')else'Primary academic publisher/repository'if tag.startswith(('UPN','UMPR','JENGGOLO'))else'Public portal'),'dataset_title':r.get('dataset_title',tag),'resource_name':r.get('resource_name'),'source_url':r['url'],'resource_id':r.get('resource_id'),'quality_class':quality,'http_status':r.get('http_status'),'retrieval_status':r['status'],'inspection_status':r.get('inspection_status'),'format_actual':fmt,'sha256':r.get('sha256'),'bytes':r.get('bytes'),'original_path':r.get('path'),'reused_existing_hash':r.get('reused_existing_original',False),'complete_binary_file':bool(binary and complete),'calendar_eligible':False,'decision':decision})
 save(DOC/'classified-sources.json',register)
 with (ROOT/'M13_1_OFFICIAL_SOURCE_REGISTER.csv').open('w',encoding='utf-8-sig',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(register[0]));w.writeheader();w.writerows(register)
 complete_files={r['sha256']:r for r in register if r['complete_binary_file']};new_files={k:r for k,r in complete_files.items()if not r['reused_existing_hash']};actual_counts=[r for r in register if r['tag']=='JENGGOLO_2023'and r['complete_binary_file']]
 manifest={'audit_utc':now(),'government_dataset_sources_in_depth':15,'bps_metadata_sources_in_depth':2,'dishub_catalog_entries_reviewed':sum(p.get('organization',{}).get('name')=='dinas-perhubungan'for p in load(DOC/'ckan-packages.json')),'ckan_selected_packages':len(load(DOC/'selected-ckan-packages.json')),'ckan_selected_resource_files':30,'ckan_datastore_resources_inspected':len(list((DOC/'datastore').glob('*.json'))),'complete_distinct_binary_files_retrieved_and_inspected':len(complete_files),'new_distinct_complete_binary_files_saved':len(new_files),'existing_complete_originals_reused_by_sha256':len(complete_files)-len(new_files),'complete_files_containing_physical_vehicle_counts':len(actual_counts),'equivalent_volume_files_not_physical_counts':sum(r['tag']=='v-c-ratio-di-jalan-kabupaten-kota'and r['complete_binary_file']for r in register),'metadata_export_json_count':sum(r['tag']in ['BPS_2026_EXPORT','BPS_2024_EXPORT']and r['retrieval_status']=='RETRIEVED'for r in register),'corrupt_or_incomplete_pdf_downloads':[r for r in register if r.get('inspection_status')=='PARSE_ERROR'],'files':register,'http_attempts':downloads,'no_restricted_chapters_requested':True,'contact_request_sent':False,'no_captcha_login_or_certificate_bypass':True};save(ROOT/'M13_1_DOWNLOADED_FILES_MANIFEST.json',manifest)
 # This file contains only fully admitted A/B observations, never category C values.
 eligible=[r for r in store.rows(eligible=True)if r['batch_id']is not None];headers=['observation_date','observation_time','time_zone','interval_start','interval_end','road_segment','direction','vehicle_class','vehicle_count','measurement_unit','source_type','source_name','source_url','source_sha256','current_verification_status']
 with (ROOT/'M13_1_VERIFIED_OBSERVATIONS.csv').open('w',encoding='utf-8-sig',newline='')as f:
  w=csv.DictWriter(f,fieldnames=headers,extrasaction='ignore');w.writeheader();w.writerows(eligible)
 with (DOC/'INSPECTED_AGGREGATES_NOT_HOURLY_OBSERVATIONS.csv').open('w',encoding='utf-8-sig',newline='')as f:
  keys=['source_id','quality_class','observation_date','interval_start','interval_end','road_segment_source','direction','vehicle_class_source','vehicle_count','volume_original','capacity_original','vc_ratio','unit','source_url','source_sha256','calendar_eligible'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)
 original=load(DOC/'database-origin.json');m13sources=load(ROOT/'documentation/m13/implementation-sha256.json');changed=[p for p,h in m13sources.items()if sha(ROOT/p)!=h]
 # A narrowly selected actual SUMO baseline verifies old simulation outputs, without another local385-source audit.
 run=ROOT/'simulation/runs/realism_recovery/a26221f9ee8ea7be339ab9de';out=load(run/'output-manifest.json');run_changed=[n for n,h in out.items()if sha(run/n)!=h]
 protected={'M13_original_database_unchanged':sha(ROOT/'data/historical/m13/historical.sqlite')==original['original_sha256'],'M13_source_files_changed':changed,'selected_SUMO_baseline_outputs_changed':run_changed,'M13_source_files_checked':len(m13sources),'selected_SUMO_baseline_files_checked':len(out),'status':'PASS'if not changed and not run_changed and sha(ROOT/'data/historical/m13/historical.sqlite')==original['original_sha256']else'FAIL'};save(DOC/'preservation-verification.json',protected)
 bps=next(r for r in register if r['tag']=='BPS_2026_EXPORT');b2024=next(r for r in register if r['tag']=='BPS_2024_EXPORT');pnl=next(r for r in register if r['tag']=='JENGGOLO_2023');upn=next(r for r in register if r['tag']=='UPN_2025_BAB5');unavailable=[r for r in register if r['quality_class']=='E']
 md('M13_1_DISHUB_SEARCH_REPORT.md','M13.1 — Official Dishub Traffic Data Retrieval',f'''## Hasil yang bisa dipertanggungjawabkan

1. **{manifest['dishub_catalog_entries_reviewed']} entri katalog Dishub** ditinjau lewat CKAN; **15 dataset Dishub relevan +2metadata BPS** diperiksa mendalam. Ini17sumber pemerintah pada tingkatdataset/kegiatan, bukan17dataset pencacahan. Publikasi/repository akademik terkait dicatat terpisah.
2. **{len(complete_files)} file biner lengkap** berhasil diambil dan diperiksa:30resourceXLS/XLSX/PDFDishub serta publikasi primer yang lengkap. **{len(new_files)} original baru** disimpan, **{len(complete_files)-len(new_files)} original lama** dikenali denganSHA256 dan digunakan kembali tanpa duplikasi. Dua eksporJSON BPS dan responsAPI/HTML tidak dihitung sebagai raw traffic files. Unduhan rusak tidak dihitung sebagaifilelengkap.
3. **{len(actual_counts)} file memuat hitungan kendaraan fisik**: penelitianJenggolo2023,49nilai hitungan agregat12jam. Dua fileV/C(PDF+XLS) memuat volume ekuivalenSMP/jam, bukan jumlah kendaraan fisik, dan merupakan dataset43ruas yang sama. Spreadsheet administrasi tidak dihitung sebagai trafficcounts.
4. Tanggal survei terbaru yang **disebut dalam dokumen primer lengkap yang berhasil diperoleh**: **16Mei2025**, kesimpulan skripsiUPN BabV. Dokumen ini memberi hasilanalisis/tundaan, bukan tabel rawcounts. Tanggal terbaru dengan **angka hitungan fisik yang berhasil diperiksa**: **3Desember2023**, agregat12jam; tanggalweekday diselesaikan dalam rentang satu minggu yang dinyatakan eksplisit. Publication date tidak digunakan sebagai observationdate.
5. Hitungan2023 tersedia pada jendela **06.00–18.00 WIB sebagai satu agregat12jam perhari**, bukan12angka perjam. Tahun2025 menyebut jendela analisis pagi/sore, tetapi rawcount tablebelum didapat. Tidak ada jamhistorisA/B baru yang diaktifkan.
6. Lokasi sumberJenggolo: nama ruas literal ±300m, KecamatanGedangan, kedua arah digabung. Titik/extent belum digeoreferensi dan tidak disamakan otomatis dengan intiSimpangGedangan, Jenggala, Ketajen, maupunAloha. Dishub2022memuat43nama ruas kabupaten termasukRayaSukodono, tetapi tidak memiliki arah/jam/kelas pengamatan.
7. **{summary['pnl_sum_of_published_class_counts']:,} kendaraan** adalah penjumlahan nilai pada tujuh kelompok kelas yang benar-benar dicetak untuk7×12jam dalam paperJenggolo. Ini bukan keseluruhan trafficGedangan; tabel tersebut tidak mencakup sepeda motor dan tidak memisahkan arah. Jangan menjumlahkannya dengan LHR/hasil ekuivalensi sebagai pengamatan tambahan. Ketidaksesuaian pembulatan rata-rata pada paper dipertahankan sebagaiflag.
8. **{len(eligible)} observasiA/B baru terverifikasi dan0baris demand yang siap dipakai langsung untukSUMO.** File VERIFIED_OBSERVATIONS.csv hanyaheader, bukan barisnol kendaraan.92reference aggregates disimpan pada tabel terpisah di DB turunanM13.1; tidak mengubah kalenderobservasi.
9. Masihkosong: rawcount arah/kelas/15menitatau1jam yang mengikat tanggal, titik dan metode; turning counts, queue/travel-time samples, real signal/rail event timestamps. DataAloha2023lama tidak dipindahkan keGedangan2026.
10. MetadataBPS2026 beserta **eksporJSON aktual** berhasil diunduh. Rencana pengumpulan7–17Agustus2026 dan rilis4Januari2027 adalah jadwal, bukan bukti observasi setiap hari. Tidak ditemukan hasilpublik awal yang dapat digunakan pada portal/resource yang diperiksa: **NOT PUBLICLY AVAILABLE AS OF AUDIT DATE** untuk hasil yang dimaksud, dengan batas bahwa kegagalanakses bukan bukti ketiadaan di instansi.

## Metode dan penelusuran

Tidak mengulang audit385filelokal. RegisterM13 dibaca untuk dedupSHA. CKAN package_show/package_search, daftar organisasiDishub,15resource datastore_search, halaman dataset dan unduhanoriginal dipakai. Seluruhworksheet resource diperiksa, termasuk XLSXlama dan XLS2023–2025; pairingPDF/XLS/datastoreV/C memastikan satuanSMP/jam. ResponsmetadataBPS ditelusuri ke endpoint export yang benar-benar tercantum pada script halaman, bukan menebak angka dari jadwal.

Portalnasional data.go.id ditelusuri; hasil denganjudulserupa tetapi provinsi/kabupatenlain dikeluarkan. Linkhasilcache yang404dicatat, tidak dianggapdatasetSidoarjo. PublisherUMPR dicoba melaluiPDF/view/DOI dan alias domain yang dicantumkan publisher, masih gagal. Browsernavigate juga timeout. RepositoryUPN membatasiBabII–IVsampai2027danLampiranuntukstaf; bagian itu tidak diminta atau dibypass. HanyaBabI/V/Cover yang berstatuspublik dicoba; yangtruncatedtidak dianggaplengkap.

Originals baru: {link(DATA/'originals')}. Reuseoriginalslama besertahash terlihat dalam {link(ROOT/'M13_1_DOWNLOADED_FILES_MANIFEST.json')}. Pemeriksaan isi: {link(DOC/'resource-inspections.json')}, {link(DOC/'followup-inspections.json')}, folderextracted dan15responsdatastore. KategoriC/D/E tidak pernah menjadi historicalobservations.

Sumber kunci: [Dishub inventarisasi](https://opendata.sidoarjokab.go.id/dataset/data-inventarisasi-dan-analisis-situasi-arus-lalu-lintas), [BPS2026]({bps['source_url']}), [BPS2024]({b2024['source_url']}), [paperJenggolo]({pnl['source_url']}), [UPNBabV]({upn['source_url']}).

Tidak ada email/formulir yang dikirim, uploadGitHub, perubahanSUMOlama, penghapusanworkspace atau redesign3D. Preservasi **{protected['status']}**.
''')
 md('M13_1_GEDANGAN_COVERAGE_REPORT.md','M13.1 — Gedangan Coverage and Source Scope',f'''## Observasi yang bisa masuk kalender

ObservasiA/B baru terverifikasi: **{len(eligible)}**; jamaktifbaru: **0**. TargetAgustus–Oktober2026 tetap92tanggalmerah/2.208jamkosong. Bulan/tahun lain kini dapat diperiksa; kosong tetapmerah, bukan mengulang pola2026atau sourcebulanlain.

## Bukti yang tersedia tetapi bukan input perjam

- PNL2024:49physicalcountvalues untuk27November–3Desember2023,06.00–18.00WIB,dua arah digabung,tujuh kelas sumber. Sum **{summary['pnl_sum_of_published_class_counts']}**; sumbermenyebut rata-rataharian2.214, sedangkan rekonstruksi langsungtabel1–7 dibagi7 tidak persissama. Rawvaluesdipertahankan tanpa memaksa cocok. Kelasringanmencampur mobil/pickup/trukbox; tidak dipisah menjadi registrytypesdenganasumsi. Titikbelumgeoreferenced, sehingga tidak diklaim rawcount intiGedangan.
- Dishub2022:43roadrows dalamSMP/jam. Exactdate,time,direction,class=NULL. Tanggal11Januari2023adalah suratpublikasi, bukan tanggalpencacahan. VolumeRayaSukodono713,2SMP/jam tidak dikonversi menjadi713kendaraan/jam.
- UPN2025BabV: hasilanalisis untuk16Mei2025. RawcountdataBabIV/Lampiranterbatasakses; hasilDj/tundaan bukan rawtrafficcount atau observedtriptimeindividual. Dokumen lengkapBabVdisimpan sebagaiC.
- BPS2024/2026: metadataD, termasuk rencana pengumpulan15–16Agustus2024dan7–17Agustus2026. Tanggalrencana tersebut tidak diaktifkan.

ArsipC terstruktur: {link(DOC/'reference-aggregates.json')} dan {link(DOC/'INSPECTED_AGGREGATES_NOT_HOURLY_OBSERVATIONS.csv')}. Satuagregat12jam tidak diprorata menjadi12observasi1jam. Bukti perclass/day tetap dapatditelusuri kePDFSHA/table/page. Arah, kelas dan geometri yang belumterverifikasi tetapNULLatau literalcombined, bukan asumsi tersembunyi.

RuasSedati/Jenggala, frontage, Ketajen, aksesstasiun dan perlintasanrel belum memiliki countbaruA/B yang dapatdipetakan secara aman. Prioritas06–10dan16–22tetap perlu rawdata sah. Data dariAloha tidak diperlakukan sebagai SimpangGedangan.
''')
 md('M13_1_CALENDAR_UPDATE_REPORT.md','M13.1 — Multi-year Calendar and Integration',f'''[Buka kalenderM13.1](http://127.0.0.1:5198/). M13lama tetap di5197, researchSUMOrunner5196 dan EXEM12tidakdiubah.

DBturunan: {link(store.path)}. SQLitebackupread-onlydariM13, sourcehashbefore/after tersimpan di documentation/m13_1/database-origin.json; originalM13unchanged={protected['M13_original_database_unchanged']}. Tabelreference_aggregatesappend-only menyimpan92recordC terpisah. NolA/Bbaru berarti verifiedobservationsCSVheader-only dan tidak ada fabricatedavailabledate.

Pemilihbulan/tahun kini menerima1900–2100, tidak dibatasiAgustus–Oktober2026. DaftarbulanA/Bterverifikasi dihasilkan dari DB; sekarangkosong. DaftarbulanC2023-11/12ditampilkan dengan labelagregat, tidak mengaktifkan jam. /api/archive, /api/references dan calendar/monthly/daily/hourly memakaiDBaktual. Modelgreen/yellow/redtetap berdasarkan intervalunion dan scopeparameter/class/direction, bukan tanggalpublikasi atau activityschedule.

UIBaru frontend/m13_1/ dan backendm131_database/m131_server menggunakan validasi/staging/reviewM13 tanpa mengedit sourceM13. Observedimport memerlukanquality_classA/B; C/D/E ditolak sebagaiobservasi. Isi count harus vehicles/interval, matchedexistingroad/date/time/class/unit; skr/smp/pcu bukan physicalvehiclecounts. Unverifiedrows tetapPENDING_REVIEW/quarantine. HistoricalselectionMISSING ditolak backend; tidak ada fallbacktanggal atau class/directionsplitting. ApprovedA/Bnyata di tahunkapanpun akan mengubahkalender pada bulan sumbernya.

ActualSUMOhistoricalrun belumdiklaimsiap karena belumadaA/Bbaru. Referencebasedscenario tetapberlabelestimasi. Tidak ada perubahanengine/geometry/3D.

Acceptance log dan JSON berada di documentation/m13_1/. Ujitanggal2024dan2025 menggunakan isolatedsoftwarefixtures, tidak menyisipkan angka keDBaktif. BrowserQAterpisah dicatat bila dilakukan. PreservasiM13source **{protected['status']}**, {protected['M13_source_files_checked']}sourcefiles dicek; chosenSUMObaseline {protected['selected_SUMO_baseline_files_checked']}files unchanged. Tidak mengulang audit385filedata.
''')
 md('M13_1_UNAVAILABLE_DATA_REGISTER.md','M13.1 — Unavailable and Restricted Data','''## Bukan bukti data tidak ada di instansi

HasilmetadataBPS2026 belumditemukan sebagai public observationresults pada endpointyangdiaudit. Status NOT PUBLICLY AVAILABLE AS OF AUDIT DATE bersifatpenelusuranpublik, bukan pernyataan instansi tidakmemilikidata. Publikasidigitaldirencanakan4Januari2027; jadwalpengumpulan7–17Agustus2026 tidak menjadiavailabledate.

'''+ '\n\n'.join(f"- `{r['tag']}`: {r['source_url']} — {r['decision']}. Original jika ada: `{r.get('original_path')}`; SHA `{r.get('sha256')}`. Tidak masukcalendar."for r in unavailable)+'''

RepositoryUPN: BabII–IVrestricteduntil4December2027; appendixstaff-only. Restrictedchapters tidakdiambil. PublicBabI/Cover yang terunduhparsial/parse-error dipertahankan sebagai failedretrieval, bukan buktilengkap. BabVlengkapdapatdibaca.

Dishubwww host mempunyai certificatehostname mismatch; tidak dinonaktifkan pemeriksaanTLS. Kontakresmi tetapdiverifikasi dari BPSmetadata dan CKANpublisher. Draftpermohonan disiapkanterpisah; belumdikirim.
''')
 md('M13_1_DRAFT_PERMOHONAN_DATA.md','DRAFT — Permohonan Data Dishub (BELUM DIKIRIM)',f'''Tujuan resmi terverifikasi: **dishub@sidoarjokab.go.id**, DinasPerhubunganKabupatenSidoarjo, Jl.RayaCandi107Gelam. Kontak dari eksporBPS2026 dan publisherCKAN; sumber {bps['source_url']}. Tidak dikirim.

Subjek: Permohonan data pencacahan lalu lintas kawasanGedangan untuk penelitian/simulatorportofolio

Yth.DinasPerhubunganKabupatenSidoarjo,

Mohon informasi ketersediaan data pencacahan asli kawasanSimpangGedangan, JalanRayaAhmadYani arahSurabaya–Sidoarjo dan sebaliknya, Sedati/Jenggala/Jenggolo sesuai identifikasi lokasi, Sukodono, frontage, Ketajen, aksesStasiunGedangan dan perlintasanrel. Kami membutuhkan data terbaru yang boleh digunakan, termasuk2026/2025/2024/tahunsebelumnya; targetkajianawal1Agustus–31Oktober2026, dengan prioritas06.00–10.00dan16.00–22.00WIB.

Jika tersedia, mohon formatCSV/XLSX beserta tanggal/jamactual, interval15menit/1jam, lokasi/koordinat/titik, arah/gerakanbelok, kelas danhitungan kendaraan, definisiunitskendaraan/SMP/SKR/PCU, surveymethod/qualityflags, signalphases, railclosureevents, queue/travel-time samples, provenance dan izinpenggunaan. AgregatLHR atau hasilV/C dipersilakan terpisah dari rawcounts, dengan periode/metodejelas. Mohon informasi rilis atau mekanisme permohonanhasilkegiatan V/C2026(BPSK-26.3515.063).

Data akan digunakan untuk simulatorportofolio/penelitian, dengan pembedaan tegas observasi, agregat dan estimasi. Identitas/afiliasi pemohon belum diisi; pengguna perlu menyetujui isi serta pengiriman terlebih dahulu.
''')
 save(DOC/'report-summary.json',{'complete_binary_files':len(complete_files),'new_binary_files':len(new_files),'official_in_depth_sources':17,'physical_count_files':len(actual_counts),'verified_observations':len(eligible),'sumo_ready':0,'published_12h_count_sum':summary['pnl_sum_of_published_class_counts'],'preservation':protected['status']});print('Generated7required reports/exports + clearly labelled aggregate archive and unsent request draft',flush=True)
if __name__=='__main__':main()
