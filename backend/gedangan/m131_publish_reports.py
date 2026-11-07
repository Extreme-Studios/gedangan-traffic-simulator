"""Readable final narrative around machine-verified M13.1 retrieval evidence."""
from .m131_research import *
from .m131_database import DB131
from pathlib import Path
def write(name,title,text):(ROOT/name).write_text('# '+title+'\n\nTanggal audit: '+now()+'\n\n'+text.strip()+'\n',encoding='utf-8')
def main():
 m=load(ROOT/'M13_1_DOWNLOADED_FILES_MANIFEST.json');s=load(DOC/'integration-summary.json');p=load(DOC/'preservation-verification.json');tests=load(DOC/'acceptance-summary.json')if(DOC/'acceptance-summary.json').exists()else{'status':'See acceptance-reviewed.log'}
 bps='https://sirusa.web.bps.go.id/metadata/kegiatan/c4e9f75e-ff36-bfba-8aab-e1a79719b138';bps24='https://sirusa.web.bps.go.id/metadata/kegiatan/7ba8b075-98b5-54cd-ba7f-3ee5a3818382';pnl='https://e-jurnal.pnl.ac.id/portal/article/download/5567/pdf';upn='https://repository.upnjatim.ac.id/47744/6/21035010023-bab5.pdf';ckan='https://opendata.sidoarjokab.go.id/dataset/data-inventarisasi-dan-analisis-situasi-arus-lalu-lintas'
 write('M13_1_DISHUB_SEARCH_REPORT.md','M13.1 — Hasil Pencarian Data Resmi Dishub',f'''
## Hasil utama

Ditemukan bukti hitungan kendaraan yang lebih kaya daripada arsip M13: **49 nilai observasi parsial kategori B**, berupa hitungan 12 jam per hari dalam penelitian Jalan Raya Jenggolo. Semuanya disimpan dengan interval dan kelas sumber, lalu dikirim melalui validasi. **49 baris masuk quarantine; belum ada observasi per jam baru yang diterima untuk kalender atau demand SUMO.** Hasil ini tidak berarti hitungan tersebut palsu. Resolusi waktu, pemisahan arah, kelas, dan lokasi belum memenuhi syarat pemakaian model.

## Jawaban atas sepuluh pertanyaan

1. **Sumber resmi:** ditinjau {m['dishub_catalog_entries_reviewed']} entri katalog Dishub melalui CKAN. Pemeriksaan mendalam mencakup **15 dataset Dishub dan dua kegiatan metadata BPS**, yaitu 17 sumber pemerintah pada tingkat dataset/kegiatan. Publikasi PNL, UMPR dan repository UPN dicatat terpisah sebagai sumber akademik primer. Jumlah entri katalog bukan jumlah dataset pencacahan yang tersedia.
2. **File aktual:** **{m['complete_distinct_binary_files_retrieved_and_inspected']} file biner lengkap** diambil dan diperiksa isinya. Sebanyak **{m['new_distinct_complete_binary_files_saved']} original baru** disimpan; **{m['existing_complete_originals_reused_by_sha256']} original lama** digunakan kembali setelah hash cocok. Dua ekspor JSON BPS dan respons API/HTML disimpan terpisah dan tidak dihitung sebagai file raw traffic. Dua PDF yang terunduh tidak lengkap tidak dihitung sebagai file lengkap.
3. **File berisi hitungan fisik:** **satu file**, paper Jenggolo, memuat 49 nilai hitungan 12 jam. Dua file V/C, yaitu PDF dan XLS untuk dataset yang sama, berisi volume ekuivalen SMP/jam, bukan hitungan kendaraan fisik. Spreadsheet administratif tidak dihitung sebagai traffic counts.
4. **Tanggal survei terbaru:** dokumen primer lengkap Bab V UPN menyebut **16 Mei 2025**, tetapi menyajikan hasil analisis, bukan tabel raw count. Tanggal terbaru dengan angka hitungan fisik yang berhasil diperiksa adalah **3 Desember 2023**. Paper menyatakan rentang 27 November–3 Desember 2023 dan nama hari pada tabel; pemetaan nama hari ke tanggal unik dalam rentang itu dicatat dalam provenance. Tahun publikasi tidak dijadikan tanggal pengamatan.
5. **Jam yang tersedia:** hitungan 2023 mewakili **06.00–18.00 WIB sebagai satu blok 12 jam per hari**. Tidak tersedia 12 hitungan per jam. Bab V UPN menyebut jendela analisis pagi/sore tahun 2025; raw count pada jendela itu belum diperoleh. **Jam historis baru yang diaktifkan: nol.**
6. **Lokasi dan arah:** sumber Jenggolo menyatakan ruas sekitar 300 meter di Kecamatan Gedangan, dua arah digabung. Koordinat stasiun hitung dan batas segmen belum digeoreferensi. Nama literal dipertahankan; tidak otomatis disamakan dengan inti Simpang Gedangan, Jenggala, Ketajen atau Aloha. Dataset Dishub 2022 memuat 43 nama ruas kabupaten, termasuk Raya Sukodono, tanpa tanggal/jam, arah dan kelas pengamatan.
7. **Jumlah kendaraan tercatat:** penjumlahan tujuh kelompok kelas yang dicetak pada tabel 1–7 adalah **{s['pnl_sum_of_published_class_counts']:,} kendaraan selama tujuh blok 12 jam**. Tabel ini tidak mencakup sepeda motor dan tidak memisahkan arah. Angka tersebut bukan total seluruh lalu lintas Gedangan, bukan volume per jam, dan tidak dijumlahkan lagi dengan LHR/ekuivalensi sebagai pengamatan tambahan. Perbedaan terhadap jumlah rata-rata kelas yang dibulatkan pada paper tetap dicatat; nilai asli tidak diubah.
8. **Siap untuk SUMO:** **nol observasi A/B baru terverifikasi dan nol baris demand yang siap dipakai langsung**. Kandidat B tetap quarantine; volume SMP tidak diubah menjadi kendaraan fisik. CSV VERIFIED_OBSERVATIONS hanya berisi header, bukan baris dengan count nol.
9. **Masih kosong:** pencacahan satu jam/15 menit per tanggal, titik, arah dan kelas yang cocok dengan jaringan; turning counts, queue/travel-time samples serta timestamp sinyal dan palang aktual. Data lama Aloha tidak dipindahkan ke Gedangan 2026.
10. **BPS Agustus 2026:** halaman dan ekspor JSON aktual berhasil diambil. Jadwal pengumpulan 7–17 Agustus 2026 dan rilis 4 Januari 2027 adalah rencana, bukan tabel hasil. Hasil publik awal tidak ditemukan pada sumber dan endpoint yang diperiksa: **NOT PUBLICLY AVAILABLE AS OF AUDIT DATE**. Ini tidak menyatakan bahwa instansi tidak memiliki datanya.

## Apa yang benar-benar diunduh dan diperiksa

Pencarian tidak mengulang audit 385 berkas lokal. Register M13 hanya dipakai untuk deduplikasi hash. Pengambilan memakai `package_show`, `package_search`, katalog organisasi Dishub, resource download dan **15 endpoint datastore aktif**. Seluruh worksheet dari 30 resource Dishub diperiksa, termasuk versi XLSX lama dan XLS 2023–2025. Resource bertajuk inventarisasi arus ternyata berisi hitungan dokumen administratif. V/C 2022 diperiksa silang antara PDF, XLS dan datastore untuk menjaga satuan SMP/jam.

Ekspor BPS diperoleh dari URL yang benar-benar tercantum di script halaman metadata. Ekspor tersebut memuat definisi, jadwal dan rancangan kegiatan; bukan observasi kendaraan. Hasil portal nasional dengan judul serupa tetapi wilayah lain tidak dipakai sebagai data Sidoarjo.

PDF UMPR dicoba melalui jalur publik penerbit, view PDF, DOI dan alias domain yang dicantumkan penerbit; akses HTTP masih gagal dan navigasi browser timeout. Bab II–IV serta lampiran UPN berstatus terbatas dan tidak diminta. Hanya bagian publik yang dicoba; Bab V lengkap, sedangkan unduhan Bab I/Cover yang rusak ditandai E. Tidak ada login, CAPTCHA, pembatasan repository, atau pemeriksaan sertifikat yang dilewati.

## Bukti dan hasil pekerjaan

- Original baru: `data/official/m13_1/originals/`. Original lama yang dipakai ulang ditunjuk oleh manifest, tanpa salinan biner kedua.
- `M13_1_OFFICIAL_SOURCE_REGISTER.csv`: URL, kategori A–E, format aktual, hasil inspeksi, SHA256, ukuran dan keputusan penggunaan.
- `M13_1_DOWNLOADED_FILES_MANIFEST.json`: file lengkap, unduhan rusak, reuse hash, status HTTP dan alasan gagal.
- `documentation/m13_1/extracted/` dan `datastore/`: isi worksheet/PDF dan respons datastore yang diperiksa.
- `documentation/m13_1/partial-import.json`: 49 baris B yang ditolak masuk kalender per jam. Interval tidak dipecah atau diberi angka asumsi.
- `M13_1_VERIFIED_OBSERVATIONS.csv`: nol baris baru yang lolos gate kalender.

Pengujian: **{tests.get('status')}**; rincian di `documentation/m13_1/acceptance-reviewed.log`. Preservasi: **{p['status']}**. Database M13 dan output SUMO lama tetap utuh. Tidak ada permohonan yang dikirim, upload GitHub, penghapusan workspace, redesign 3D atau milestone berikutnya.

Sumber utama: [Dishub]({ckan}), [BPS 2026]({bps}), [BPS 2024]({bps24}), [paper Jenggolo]({pnl}), [Bab V UPN]({upn}).
''')
 write('M13_1_GEDANGAN_COVERAGE_REPORT.md','M13.1 — Cakupan Bukti Gedangan',f'''
## Observasi per jam yang diterima

**Nol observasi baru lolos kalender per jam.** Target Agustus–Oktober 2026 tetap 92 tanggal merah dan 2.208 jam kosong. Kalender lintas tahun dapat diperiksa tanpa memindahkan bukti ke tanggal lain.

## Bukti B yang tersedia tetapi tertahan

[Paper Jenggolo]({pnl}) menyediakan 49 nilai pada tujuh kelompok kelas selama 27 November–3 Desember 2023, pukul 06.00–18.00 WIB per hari. Nilai asli, tanggal yang diselesaikan dari nama hari dalam rentang eksplisit, URL, SHA, nomor tabel dan halaman disimpan. Jumlah nilai kelas adalah {s['pnl_sum_of_published_class_counts']:,} kendaraan; ini bukan seluruh traffic Gedangan atau count per jam.

Kandidat dikirim melalui workflow impor sebagai OBSERVED_SECONDARY dengan kualitas B. Seluruhnya masuk quarantine karena interval 12 jam tidak memenuhi gate per jam. Hambatan lain juga dipertahankan: dua arah digabung, kelas ringan mencampur mobil/pickup/truk box, dan posisi segmen belum cocok ke edge. Tidak ada pembagian kelas/arah atau distribusi per jam yang dibuat untuk meloloskannya.

## Referensi C dan metadata D

V/C Dishub berisi 43 ruas untuk survei 2022. Tanggal 11 Januari 2023 pada surat adalah tanggal dokumen; tanggal/jam hitung tetap NULL. Volume Raya Sukodono 713,2 SMP/jam tidak menjadi 713 kendaraan/jam. XLS, PDF dan datastore adalah representasi dataset yang sama, bukan tiga survei independen.

Bab V UPN memuat hasil analisis untuk 16 Mei 2025. Raw count berada pada bagian yang belum dapat diakses secara sah. Dj dan tundaan hasil analisis tidak diubah menjadi raw traffic count atau sampel perjalanan individual.

Metadata BPS 2024/2026 tetap D. Jadwal pengumpulan 15–16 Agustus 2024 dan 7–17 Agustus 2026 tidak mengaktifkan tanggal. Tidak ditemukan count baru A/B yang dapat langsung dipetakan untuk Sedati/Jenggala, frontage, Ketajen, akses stasiun atau perlintasan rel.

Arsip B/C: `documentation/m13_1/reference-aggregates.json` dan `INSPECTED_AGGREGATES_NOT_HOURLY_OBSERVATIONS.csv`. Keduanya menunjuk hitungan sumber yang sama dengan kandidat quarantine, bukan hitungan tambahan untuk dijumlahkan. Verifikasi tersedia pada `partial-import.json` dan source register.
''')
 write('M13_1_CALENDAR_UPDATE_REPORT.md','M13.1 — Pembaruan Kalender Lintas Tahun',f'''
[Buka kalender M13.1](http://127.0.0.1:5198/). Launcher: `START_GEDANGAN_HISTORICAL_M13_1.bat`. Layanan M13 lama tetap di port 5197 dan runner SUMO di 5196. EXE M12 tidak diperbarui.

Database aktif baru: `{DB131.relative_to(ROOT)}`. Dibuat melalui SQLite backup read-only dari M13; hash asal ada di `documentation/m13_1/database-origin.json`. Derivative awal `historical.sqlite` tetap disimpan sebagai checkpoint. Database asli M13 tidak ditimpa.

Kalender kini menerima bulan/tahun 1900–2100. Daftar bulan observasi A/B terverifikasi berasal dari DB dan saat ini kosong. Bulan arsip B yang tertahan, November/Desember 2023, ditampilkan terpisah dan tidak mengaktifkan jam historis. Pemilihan bulan tidak mengganti tanggal/jam ke sumber lain.

Frontend `frontend/m13_1/` membaca API monthly/daily/hourly, `/api/archive` dan `/api/references`. Hijau tetap memerlukan interval lengkap untuk seluruh scope yang ditampilkan selama 24 jam; kuning berarti parsial; merah berarti tidak ada observasi yang memenuhi scope. Aggregate B/C dan metadata D tidak mengubah denominator atau mengisi count kosong.

Penyimpanan B/C bersifat append-only. Ada 49 kandidat B pada interval asli yang masuk quarantine dan 43 baris C SMP/jam. Verifikasi observasi baru memerlukan kualitas A/B yang tersimpan, source type pengamatan, tanggal/jam, satuan, lokasi dan kelas yang valid, serta review bukti eksplisit. Source legacy yang belum punya pemetaan A/B tidak dapat dipromosikan otomatis. C/D/E dan synthetic tests ditolak sebagai observasi historis.

Hasil acceptance: **{tests.get('status')}**, dengan pengujian HTTP nyata atas impor–review–refresh pada database fixture terisolasi, dukungan tahun 2022–2026, partial-hour, duplicate, unit, lokasi, pemisahan metadata dan preservasi. Data fixture tidak masuk DB aktif. Browser QA dicatat di `documentation/m13_1/browser-acceptance.json`; screenshot memakai data aktif dan tidak dibuat hijau untuk demonstrasi.

Historical SUMO run baru belum diklaim siap. Mode reference-based tetap estimasi. Tidak ada perubahan geometri atau visual 3D. Preservasi source M13 dan baseline SUMO terpilih: **{p['status']}**.
''')
 # Keep the machine-generated unavailable URL/error register, append a clear boundary summary.
 unavailable=ROOT/'M13_1_UNAVAILABLE_DATA_REGISTER.md'
 text=unavailable.read_text(encoding='utf-8');text+='\n## Batas kesimpulan\n\nHTTP 403/404/502, timeout, sertifikat tidak cocok, atau PDF rusak tidak membuktikan data tidak ada di instansi. Semua kegagalan dibatasi pada URL dan waktu akses yang dicatat. Jadwal BPS bukan bukti survei terlaksana atau bukti hasil sudah dipublikasikan.\n';unavailable.write_text(text,encoding='utf-8')
 write('M13_1_DRAFT_PERMOHONAN_DATA.md','DRAFT Permohonan Data — BELUM DIKIRIM',f'''
Kontak resmi yang diverifikasi dari BPS/CKAN: **dishub@sidoarjokab.go.id**, Dinas Perhubungan Kabupaten Sidoarjo, Jl. Raya Candi No.107, Gelam. Sumber: [metadata BPS 2026]({bps}). Tidak ada pengiriman email atau formulir.

**Subjek: Permohonan data pencacahan lalu lintas kawasan Gedangan untuk simulator penelitian/portofolio**

Yth. Dinas Perhubungan Kabupaten Sidoarjo,

Mohon informasi ketersediaan data pencacahan asli untuk Simpang Gedangan, Jalan Raya Ahmad Yani arah Surabaya–Sidoarjo dan sebaliknya, jalur Sedati/Jenggala/Jenggolo sesuai identifikasi lokasi, Sukodono, frontage, Ketajen, akses Stasiun Gedangan dan perlintasan rel.

Kami membutuhkan data terbaru yang dapat digunakan secara sah, termasuk tahun 2026, 2025, 2024 atau sebelumnya. Target kajian awal adalah 1 Agustus–31 Oktober 2026, dengan prioritas jam 06.00–10.00 dan 16.00–22.00 WIB.

Apabila tersedia, mohon data CSV/XLSX dengan tanggal dan jam aktual, interval 15 menit/satu jam, lokasi/koordinat titik, arah/gerakan belok, kelas dan hitungan kendaraan, satuan asli kendaraan/SMP/SKR/PCU, metode survei, quality flags, serta provenance dan izin penggunaan. Kami juga memerlukan data fase sinyal, kejadian penutupan palang, antrean dan sampel waktu perjalanan bila tersedia. Data LHR/V/C agregat dapat diberikan terpisah dengan periode dan metode yang jelas.

Mohon informasi rilis atau mekanisme permohonan hasil kegiatan V/C 2026 dengan rekomendasi BPS K-26.3515.063. Data akan digunakan untuk simulator penelitian/portofolio dengan pembedaan tegas antara observasi, agregat dan estimasi.

Identitas dan afiliasi pemohon belum diisi. Pengguna perlu menyetujui isi serta pengiriman sebelum draft digunakan.
''')
 print('Final readable reports written',flush=True)
if __name__=='__main__':main()
