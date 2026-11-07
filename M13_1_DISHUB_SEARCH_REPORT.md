# M13.1 — Hasil Pencarian Data Resmi Dishub

Tanggal audit: 2026-11-01T13:29:43.783775+00:00

## Hasil utama

Ditemukan bukti hitungan kendaraan yang lebih kaya daripada arsip M13: **49 nilai observasi parsial kategori B**, berupa hitungan 12 jam per hari dalam penelitian Jalan Raya Jenggolo. Semuanya disimpan dengan interval dan kelas sumber, lalu dikirim melalui validasi. **49 baris masuk quarantine; belum ada observasi per jam baru yang diterima untuk kalender atau demand SUMO.** Hasil ini tidak berarti hitungan tersebut palsu. Resolusi waktu, pemisahan arah, kelas, dan lokasi belum memenuhi syarat pemakaian model.

## Jawaban atas sepuluh pertanyaan

1. **Sumber resmi:** ditinjau 172 entri katalog Dishub melalui CKAN. Pemeriksaan mendalam mencakup **15 dataset Dishub dan dua kegiatan metadata BPS**, yaitu 17 sumber pemerintah pada tingkat dataset/kegiatan. Publikasi PNL, UMPR dan repository UPN dicatat terpisah sebagai sumber akademik primer. Jumlah entri katalog bukan jumlah dataset pencacahan yang tersedia.
2. **File aktual:** **32 file biner lengkap** diambil dan diperiksa isinya. Sebanyak **30 original baru** disimpan; **2 original lama** digunakan kembali setelah hash cocok. Dua ekspor JSON BPS dan respons API/HTML disimpan terpisah dan tidak dihitung sebagai file raw traffic. Dua PDF yang terunduh tidak lengkap tidak dihitung sebagai file lengkap.
3. **File berisi hitungan fisik:** **satu file**, paper Jenggolo, memuat 49 nilai hitungan 12 jam. Dua file V/C, yaitu PDF dan XLS untuk dataset yang sama, berisi volume ekuivalen SMP/jam, bukan hitungan kendaraan fisik. Spreadsheet administratif tidak dihitung sebagai traffic counts.
4. **Tanggal survei terbaru:** dokumen primer lengkap Bab V UPN menyebut **16 Mei 2025**, tetapi menyajikan hasil analisis, bukan tabel raw count. Tanggal terbaru dengan angka hitungan fisik yang berhasil diperiksa adalah **3 Desember 2023**. Paper menyatakan rentang 27 November–3 Desember 2023 dan nama hari pada tabel; pemetaan nama hari ke tanggal unik dalam rentang itu dicatat dalam provenance. Tahun publikasi tidak dijadikan tanggal pengamatan.
5. **Jam yang tersedia:** hitungan 2023 mewakili **06.00–18.00 WIB sebagai satu blok 12 jam per hari**. Tidak tersedia 12 hitungan per jam. Bab V UPN menyebut jendela analisis pagi/sore tahun 2025; raw count pada jendela itu belum diperoleh. **Jam historis baru yang diaktifkan: nol.**
6. **Lokasi dan arah:** sumber Jenggolo menyatakan ruas sekitar 300 meter di Kecamatan Gedangan, dua arah digabung. Koordinat stasiun hitung dan batas segmen belum digeoreferensi. Nama literal dipertahankan; tidak otomatis disamakan dengan inti Simpang Gedangan, Jenggala, Ketajen atau Aloha. Dataset Dishub 2022 memuat 43 nama ruas kabupaten, termasuk Raya Sukodono, tanpa tanggal/jam, arah dan kelas pengamatan.
7. **Jumlah kendaraan tercatat:** penjumlahan tujuh kelompok kelas yang dicetak pada tabel 1–7 adalah **15,478 kendaraan selama tujuh blok 12 jam**. Tabel ini tidak mencakup sepeda motor dan tidak memisahkan arah. Angka tersebut bukan total seluruh lalu lintas Gedangan, bukan volume per jam, dan tidak dijumlahkan lagi dengan LHR/ekuivalensi sebagai pengamatan tambahan. Perbedaan terhadap jumlah rata-rata kelas yang dibulatkan pada paper tetap dicatat; nilai asli tidak diubah.
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

Pengujian: **PASS - 18 tests**; rincian di `documentation/m13_1/acceptance-reviewed.log`. Preservasi: **PASS**. Database M13 dan output SUMO lama tetap utuh. Tidak ada permohonan yang dikirim, upload GitHub, penghapusan workspace, redesign 3D atau milestone berikutnya.

Sumber utama: [Dishub](https://opendata.sidoarjokab.go.id/dataset/data-inventarisasi-dan-analisis-situasi-arus-lalu-lintas), [BPS 2026](https://sirusa.web.bps.go.id/metadata/kegiatan/c4e9f75e-ff36-bfba-8aab-e1a79719b138), [BPS 2024](https://sirusa.web.bps.go.id/metadata/kegiatan/7ba8b075-98b5-54cd-ba7f-3ee5a3818382), [paper Jenggolo](https://e-jurnal.pnl.ac.id/portal/article/download/5567/pdf), [Bab V UPN](https://repository.upnjatim.ac.id/47744/6/21035010023-bab5.pdf).
